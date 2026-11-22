"""Feeders: call existing Apify Store scrapers and normalise their output into pricing `Metrics`.

Field names were verified against real runs on 22 Nov 2026 (fixtures in tests/fixtures/):
- Instagram: apify/instagram-profile-scraper (followersCount) + apify/instagram-reel-scraper (videoPlayCount ...)
- TikTok:    clockworks/tiktok-profile-scraper (authorMeta.fans, playCount, diggCount, commentCount, shareCount)
- YouTube:   streamers/youtube-scraper (numberOfSubscribers, type, viewCount, likes, commentsCount, date)

The `normalise_*` functions are pure, so they are unit-tested against the fixtures without network calls.
"""

from __future__ import annotations

import asyncio
import re
import statistics
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

from .pricing import Metrics

IG_PROFILE_ACTOR = 'apify/instagram-profile-scraper'
IG_REEL_ACTOR = 'apify/instagram-reel-scraper'
TIKTOK_ACTOR = 'clockworks/tiktok-profile-scraper'
YOUTUBE_ACTOR = 'streamers/youtube-scraper'

IG_VIEW_FIELDS = ('videoPlayCount', 'igPlayCount', 'videoViewCount')  # first positive value wins

MIN_VALID = 6
SAMPLE_ITEMS = 30


class FeederError(RuntimeError):
    """The creator could not be scraped (private, not found, no posts)."""


# --------------------------------------------------------------------------------------------------
# Handle parsing
# --------------------------------------------------------------------------------------------------

_HANDLE_PATTERNS = [
    r'instagram\.com/([A-Za-z0-9._]+)',
    r'tiktok\.com/@([A-Za-z0-9._]+)',
    r'youtube\.com/@([A-Za-z0-9._-]+)',
    r'youtube\.com/(?:c|user)/([A-Za-z0-9._-]+)',
]


def clean_handle(raw: str) -> str:
    """Accept '@name', 'name' or a profile URL; return the bare handle."""
    s = (raw or '').strip()
    for pat in _HANDLE_PATTERNS:
        m = re.search(pat, s)
        if m:
            return m.group(1)
    s = s.lstrip('@').strip('/')
    if not re.fullmatch(r'[A-Za-z0-9._-]{1,100}', s):
        raise FeederError(f'"{raw}" does not look like a valid handle or profile URL.')
    return s


# --------------------------------------------------------------------------------------------------
# Shared maths
# --------------------------------------------------------------------------------------------------


def age_days(ts: str | None, now: datetime | None = None) -> float | None:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return ((now or datetime.now(timezone.utc)) - dt).total_seconds() / 86400


def _positive(v: Any) -> float | None:
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else None


def _windowed(rows: list[dict], lo: float, hi: float, fallback_hi: float, fallback_lo: float | None = None) -> tuple[list[dict], bool]:
    """Keep rows aged lo..hi days; if fewer than MIN_VALID, widen the window and report the fallback."""
    inside = [r for r in rows if r['age'] is not None and lo <= r['age'] <= hi]
    if len(inside) >= MIN_VALID:
        return inside, False
    flo = lo if fallback_lo is None else fallback_lo
    wider = [r for r in rows if r['age'] is not None and flo <= r['age'] <= fallback_hi]
    return wider, True


def _summary(rows: list[dict]) -> dict:
    views = [r['views'] for r in rows]
    ers = [r['er'] for r in rows if r['er'] is not None]
    out = {
        'n': len(rows),
        'median_views': statistics.median(views) if views else None,
        'er': statistics.median(ers) if ers else None,
        'likes_hidden': bool(rows) and len(ers) < len(rows) / 2,
        'volatility': None,
        'sponsored': sum(1 for r in rows if r.get('sponsored')),
    }
    if len(views) >= 4:
        q = statistics.quantiles(views, n=4)
        out['volatility'] = q[2] / q[0] if q[0] > 0 else None
    return out


# --------------------------------------------------------------------------------------------------
# Normalisers (pure)
# --------------------------------------------------------------------------------------------------


def normalise_instagram(profile_items: list[dict], reel_items: list[dict], now: datetime | None = None) -> tuple[Metrics, dict]:
    prof = next((p for p in profile_items if not p.get('error')), None)
    if prof is None:
        err = profile_items[0].get('error') if profile_items else 'no profile returned'
        raise FeederError(f'Instagram profile not found or not public ({err}).')
    if prof.get('private'):
        raise FeederError('This Instagram account is private, so its Reels cannot be analysed.')

    rows, fields_used = [], []
    for r in reel_items:
        if r.get('error') or r.get('productType') not in (None, 'clips'):
            continue
        views, field = None, None
        for f in IG_VIEW_FIELDS:
            views = _positive(r.get(f))
            if views:
                field = f
                break
        if not views:
            continue  # 0 / -1 / null = missing, never a real zero
        likes = r.get('likesCount')
        er = None
        if isinstance(likes, (int, float)) and likes >= 0:
            er = (likes + (r.get('commentsCount') or 0)) / views
        rows.append({'views': views, 'er': er, 'age': age_days(r.get('timestamp'), now), 'sponsored': bool(r.get('paidPartnership'))})
        fields_used.append(field)

    picked, widened = _windowed(rows, 3, 120, 365)
    s = _summary(picked)
    field = max(set(fields_used), key=fields_used.count) if fields_used else None
    metrics = Metrics(
        platform='instagram',
        audience=prof.get('followersCount'),
        median_views={'instagram_reel': s['median_views']},
        engagement_rate={'instagram_reel': s['er']},
        sample_size={'instagram_reel': s['n']},
        views_field=field,
        age_fallback=widened,
        likes_hidden=s['likes_hidden'],
    )
    info = {
        'displayName': prof.get('fullName'),
        'verified': prof.get('verified'),
        'postsScraped': len(reel_items),
        'postsUsed': s['n'],
        'ageWindowDays': [3, 365] if widened else [3, 120],
        'sponsoredPostsInSample': s['sponsored'],
    }
    return metrics, info


def normalise_tiktok(items: list[dict], now: datetime | None = None) -> tuple[Metrics, dict]:
    good = [i for i in items if not i.get('error') and not i.get('errorCode')]
    if not good:
        err = items[0].get('error') if items else 'no videos returned'
        raise FeederError(f'TikTok profile not found, private or empty ({err}).')
    author = good[0].get('authorMeta') or {}
    if author.get('privateAccount'):
        raise FeederError('This TikTok account is private, so its videos cannot be analysed.')

    rows = []
    for i in good:
        plays = _positive(i.get('playCount'))
        if not plays or i.get('isSlideshow') or i.get('isPinned'):
            continue
        er = ((i.get('diggCount') or 0) + (i.get('commentCount') or 0) + (i.get('shareCount') or 0)) / plays
        rows.append({'views': plays, 'er': er, 'age': age_days(i.get('createTimeISO'), now), 'sponsored': bool(i.get('isSponsored') or i.get('isAd'))})

    picked, widened = _windowed(rows, 3, 120, 365)
    s = _summary(picked)
    metrics = Metrics(
        platform='tiktok',
        audience=author.get('fans'),
        median_views={'tiktok_video': s['median_views']},
        engagement_rate={'tiktok_video': s['er']},
        sample_size={'tiktok_video': s['n']},
        volatility=s['volatility'],
        age_fallback=widened,
    )
    info = {
        'displayName': author.get('nickName') or author.get('name'),
        'verified': author.get('verified'),
        'postsScraped': len(items),
        'postsUsed': s['n'],
        'ageWindowDays': [3, 365] if widened else [3, 120],
        'sponsoredPostsInSample': s['sponsored'],
    }
    return metrics, info


def normalise_youtube(items: list[dict], now: datetime | None = None) -> tuple[Metrics, dict]:
    good = [i for i in items if not i.get('error')]
    if not good:
        err = items[0].get('error') if items else 'no videos returned'
        raise FeederError(f'YouTube channel not found or empty ({err}).')
    subs = next((i.get('numberOfSubscribers') for i in good if i.get('numberOfSubscribers')), None)

    def rows_of(kind: str) -> list[dict]:
        out = []
        for i in good:
            views = _positive(i.get('viewCount'))
            if i.get('type') != kind or not views:
                continue
            likes = i.get('likes')
            er = ((likes or 0) + (i.get('commentsCount') or 0)) / views if isinstance(likes, (int, float)) else None
            out.append({'views': views, 'er': er, 'age': age_days(i.get('date'), now), 'sponsored': bool(i.get('isPaidContent'))})
        return out

    long_rows, long_fb = _windowed(rows_of('video'), 30, 365, 365, fallback_lo=7)
    short_rows, short_fb = _windowed(rows_of('shorts'), 3, 120, 365)
    ls, ss = _summary(long_rows), _summary(short_rows)
    metrics = Metrics(
        platform='youtube',
        audience=subs,
        median_views={'youtube_integration': ls['median_views'], 'youtube_short': ss['median_views']},
        engagement_rate={'youtube_integration': ls['er'], 'youtube_short': ss['er']},
        sample_size={'youtube_integration': ls['n'], 'youtube_short': ss['n']},
        age_fallback=long_fb,
        likes_hidden=ls['likes_hidden'],
    )
    info = {
        'displayName': good[0].get('channelName'),
        'verified': good[0].get('isChannelVerified'),
        'postsScraped': len(items),
        'postsUsed': ls['n'] + ss['n'],
        'longFormUsed': ls['n'],
        'shortsUsed': ss['n'],
        'ageWindowDays': {'longForm': [7, 365] if long_fb else [30, 365], 'shorts': [3, 365] if short_fb else [3, 120]},
        'sponsoredPostsInSample': ls['sponsored'] + ss['sponsored'],
    }
    return metrics, info


# --------------------------------------------------------------------------------------------------
# Live calls (Apify SDK)
# --------------------------------------------------------------------------------------------------


async def _run_feeder(actor_id: str, run_input: dict, max_items: int, max_usd: float) -> list[dict]:
    from apify import Actor  # imported lazily so the pure functions work without the SDK runtime

    run = await Actor.call(
        actor_id,
        run_input,
        max_items=max_items,
        max_total_charge_usd=Decimal(str(max_usd)),
        timeout=timedelta(seconds=180),
        abort_with_parent=True,
    )
    if run is None:
        raise FeederError(f'{actor_id} did not start.')
    status = getattr(run, 'status', None)
    if str(status).upper().endswith(('FAILED', 'ABORTED', 'TIMED-OUT', 'TIMED_OUT')):
        raise FeederError(f'{actor_id} ended with status {status}.')
    dataset_id = getattr(run, 'default_dataset_id', None)
    page = await Actor.apify_client.dataset(dataset_id).list_items(limit=max_items)
    return list(page.items)


async def scrape(platform: str, handle: str, want_shorts: bool = False) -> tuple[Metrics, dict]:
    h = clean_handle(handle)
    if platform == 'instagram':
        profile, reels = await asyncio.gather(
            _run_feeder(IG_PROFILE_ACTOR, {'usernames': [h]}, max_items=1, max_usd=0.05),
            _run_feeder(
                IG_REEL_ACTOR,
                {'username': [h], 'resultsLimit': SAMPLE_ITEMS, 'skipPinnedPosts': True, 'skipTrialReels': True},
                max_items=SAMPLE_ITEMS,
                max_usd=0.15,
            ),
        )
        return normalise_instagram(profile, reels)
    if platform == 'tiktok':
        items = await _run_feeder(
            TIKTOK_ACTOR,
            {'profiles': [h], 'resultsPerPage': SAMPLE_ITEMS, 'profileSorting': 'latest', 'excludePinnedPosts': True},
            max_items=SAMPLE_ITEMS,
            max_usd=0.15,
        )
        return normalise_tiktok(items)
    if platform == 'youtube':
        shorts = SAMPLE_ITEMS if want_shorts else 0
        items = await _run_feeder(
            YOUTUBE_ACTOR,
            {
                'startUrls': [{'url': f'https://www.youtube.com/@{h}'}],
                'maxResults': SAMPLE_ITEMS,
                'maxResultsShorts': shorts,
                'maxResultStreams': 0,
                'sortVideosBy': 'NEWEST',
            },
            max_items=SAMPLE_ITEMS + shorts,
            max_usd=0.30,
        )
        return normalise_youtube(items)
    raise FeederError(f'Unsupported platform "{platform}".')
