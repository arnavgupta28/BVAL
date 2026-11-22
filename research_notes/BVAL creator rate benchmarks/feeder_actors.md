# Apify Store feeder Actors for BVAL (creator recent-performance metrics), as of 22 Nov 2026

Method: I pulled each Actor's public API object (`https://api.apify.com/v2/acts/{user}~{name}`: stats, `pricingInfos`) and its default build (`.../builds/default`: `inputSchema`, plus `actorDefinition.storages.dataset` as the output schema). I also read the Store README (`https://apify.com/{user}/{name}.md`), the Store search API, and public issue pages. Everything was fetched on 2026-11-22, and I ran no Actors. Prices are pay-per-event (PPE) in USD per event, given by Apify plan tier (FREE / BRONZE / SILVER / GOLD / PLATINUM / DIAMOND). Under PPE, platform compute is not billed on top ([PPE docs, linked from every README](https://docs.apify.com/actors/running/actors-in-store.md#pay-per-event)).

## Q1. Instagram: exact inputs/outputs, pricing, reliability of Reel views

### Takeaway
Only `apify/instagram-reel-scraper`, `apify/instagram-post-scraper`, `apify/instagram-scraper` and `apify/instagram-api-scraper` return `videoPlayCount`. All four share one post schema. Their own schemas mark `videoViewCount` as "Deprecated by Instagram; may be null or stale. Prefer videoPlayCount."

`apify/instagram-profile-scraper` returns `followersCount` plus a fixed 12 `latestPosts`. Its README sample `latestPosts` items carry only `videoViewCount`, never `videoPlayCount`, so it is not a good source of Reel views.

Recommended pair: `instagram-profile-scraper` for followers (1 event, about $0.0026), plus `instagram-post-scraper` (mixed feed) or `instagram-reel-scraper` (Reels only) with `resultsLimit: 30` for per-post metrics. The alternative is `instagram-scraper` called twice (`resultsType: "details"` and `"posts"`). For views, read `videoPlayCount` first, then fall back to `igPlayCount`, then `videoViewCount`. Treat `0` with suspicion.

### Cited Findings

**Shared post-item output fields** (identical names in reel-, post-, api- and instagram-scraper dataset schemas) — [build schema: reel](https://api.apify.com/v2/acts/apify~instagram-reel-scraper/builds/default), [post](https://api.apify.com/v2/acts/apify~instagram-post-scraper/builds/default), [scraper](https://api.apify.com/v2/acts/apify~instagram-scraper/builds/default), [api](https://api.apify.com/v2/acts/apify~instagram-api-scraper/builds/default)
- Engagement: `likesCount` (number|null), `commentsCount`, `videoViewCount` ("Deprecated by Instagram; may be null or stale. Prefer videoPlayCount."), `videoPlayCount` ("Number of plays for video posts"), `igPlayCount` ("Instagram-specific play count"), `fbPlayCount`, `fbLikeCount`, `sharesCount`, `reshareCount`.
- Type: `type` ("Image, Video, Sidecar, etc.") and `productType` ("feed, clips, igtv"). In the README samples a Reel is `"productType": "clips"`, and carousels can show `"carousel_container"`. In `instagram-scraper`, `resultsType: "reels"` "filters to reel content (`productType: "clips"`)" — [instagram-scraper README](https://apify.com/apify/instagram-scraper.md).
- Time: `timestamp` (ISO 8601 string). `videoDuration` is in seconds.
- Identity: `id`, `shortCode`, `url`, `ownerUsername`, `ownerId`, `ownerFullName`, `isPinned`, `caption`, `hashtags`, `mentions`, `coauthorProducers`, `paidPartnership`, `sponsors`.
- Errors: `error`, `errorDescription`, `requestErrorMessages`.
- Post items do NOT include follower count. There is no `followersCount` in the reel or post scraper schemas.
- `sharesCount` semantics vary by Actor. Reel scraper: "Number of shares/reposts of the reel (when includeSharesCount is enabled)". instagram-scraper and api-scraper: "for hashtag results only. Null when the owner hides the share count." In those two, `reshareCount` is "Deprecated: always empty".
- `likesCount` is `-1` when the owner hides likes — [post-scraper README FAQ](https://apify.com/apify/instagram-post-scraper.md).
- Counts are what logged-out visitors see and are a snapshot at run time. They may be lower than counts seen while logged in — [post-scraper README FAQ](https://apify.com/apify/instagram-post-scraper.md) (same FAQ in the reel and scraper READMEs).

**apify/instagram-profile-scraper** (id `dSCLg0C3YEZ83HzYX`) — [README](https://apify.com/apify/instagram-profile-scraper.md), [API](https://api.apify.com/v2/acts/apify~instagram-profile-scraper)
- Input: `usernames` (array of strings, **required**; accepts names, IDs or URLs), `includeAboutSection` (bool, default `false`; paid add-on).
- Output: `followersCount`, `followsCount`, `postsCount`, `verified`, `private`, `isBusinessAccount`, `businessCategoryName`, `igtvVideoCount`, `latestPosts` (array), `latestIgtvVideos`, `relatedProfiles`, `error`, `errorDescription`.
- `latestPosts` has a fixed size: "the latest 12 posts with details" and "Latest image posts, carousels, and videos (12)". There is no input to change it — [README](https://apify.com/apify/instagram-profile-scraper.md).
- Keys in the README sample `latestPosts` items: `id, type, shortCode, caption, hashtags, mentions, url, commentsCount, likesCount, videoViewCount, timestamp, ownerUsername, productType, videoDuration, isPinned, ...`. `videoViewCount` appears on video items, e.g. `"productType": "clips"`, `"videoViewCount": 926847`. **No `videoPlayCount` key appears in any latestPosts sample item** — [README sample](https://apify.com/apify/instagram-profile-scraper.md).
- Pricing (PPE, effective 2026-02-17): `profile` event FREE 0.0026 / BRONZE 0.0023 / SILVER 0.002 / GOLD 0.0016 / PLATINUM 0.0011 / DIAMOND 0.0005. Add-on `about-account` costs 0.007 on FREE down to 0.0025 on DIAMOND. There is no actor-start fee — [API pricingInfos](https://api.apify.com/v2/acts/apify~instagram-profile-scraper).
- Stats: 298,617 total users, 46,161 monthly. Last 30 days: 9,930,057 of 9,972,626 runs succeeded (32,964 timed out). Rating 4.75. Default run options are 1024 MB with a 30000 s timeout — [API](https://api.apify.com/v2/acts/apify~instagram-profile-scraper), [README](https://apify.com/apify/instagram-profile-scraper.md).

**apify/instagram-reel-scraper** (id `xMc5Ga1oCONPmWJIa`) — [README](https://apify.com/apify/instagram-reel-scraper.md), [API](https://api.apify.com/v2/acts/apify~instagram-reel-scraper)
- Input:
  - `username` (array, **required**; usernames, profile URLs, IDs or reel URLs).
  - `resultsLimit` (integer, min 1, prefill 25; "reels ... per profile"; ignored for direct reel URLs).
  - `onlyPostsNewerThan` (string: `YYYY-MM-DD`, ISO, or relative such as `"1 day"`).
  - `skipPinnedPosts` (bool, default false), `skipTrialReels` (bool, default false).
  - `includeSharesCount` (bool, default false; paid plans only, priced as an add-on).
  - `includeTranscript` (bool, default false; per minute), `includeDownloadedVideo` (bool, default false; per MB).
- README samples show both counts, e.g. `"videoViewCount": 4073, "videoPlayCount": 10977` and `"videoViewCount": 45600, "videoPlayCount": 809683`. Play count is consistently much larger than view count — [README](https://apify.com/apify/instagram-reel-scraper.md).
- Trial reels are not flagged in the output, which is why `skipTrialReels` exists — [README](https://apify.com/apify/instagram-reel-scraper.md).
- Pricing (PPE):
  - `reel`: FREE 0.0026 / BRONZE 0.0023 / SILVER 0.0014 / GOLD 0.001 / PLATINUM 0.0008 / DIAMOND 0.0004.
  - `actor-start`: 0.001 flat.
  - `shares-count` add-on: 0.007 on FREE down to 0.002 on DIAMOND, per reel.
  - `transcript`: 0.048 on FREE per started minute.
  - `minimalMaxTotalChargeUsd` 0.0073.
  - Source: [API pricingInfos](https://api.apify.com/v2/acts/apify~instagram-reel-scraper).
- Stats: 202,733 users, 29,077 monthly. Last 30 days: 3,082,877 of 3,088,972 runs succeeded. Rating 4.39 (102 reviews) — [API](https://api.apify.com/v2/acts/apify~instagram-reel-scraper), [Store API](https://api.apify.com/v2/store?search=instagram%20reel&limit=20).

**apify/instagram-post-scraper** (id `nH2AHrwxeTRJoN5hX`) — [README](https://apify.com/apify/instagram-post-scraper.md), [API](https://api.apify.com/v2/acts/apify~instagram-post-scraper)
- Input:
  - `username` (array, **required**; usernames, profile URLs or post URLs).
  - `resultsLimit` (integer, min 1, prefill 20; per profile).
  - `onlyPostsNewerThan` (string), `skipPinnedPosts` (bool, default false).
  - `includeMusicData` (bool, default false; paid).
  - `dataDetailLevel` (enum `basicData` | `detailedData`; **schema default `detailedData`**, UI prefill `basicData`; "Detailed data are paid extra").
- Pricing (PPE, effective 2026-10-07):
  - `post`: FREE 0.0017 / BRONZE 0.0015 / SILVER 0.0013 / GOLD 0.001 / PLATINUM 0.0008 / DIAMOND 0.0004.
  - `post-details` (extra, when detailedData): FREE 0.001 / BRONZE 0.0008 / … / DIAMOND 0.0001.
  - `music-data` add-on: 0.007 on FREE.
  - No actor-start event is listed. Source: [API pricingInfos](https://api.apify.com/v2/acts/apify~instagram-post-scraper).
- README sample: `"videoViewCount": 528654, "videoPlayCount": 2412253` — [README](https://apify.com/apify/instagram-post-scraper.md).
- The README FAQ says the summer-2025 "Reposts" metric is "not a part of Instagram Posts Scraper's datasets yet" — [README](https://apify.com/apify/instagram-post-scraper.md).
- Stats: 161,668 users, 21,226 monthly. Last 30 days: 6,321,318 of 6,327,469 runs succeeded. Rating 4.26 — [API](https://api.apify.com/v2/acts/apify~instagram-post-scraper), [README](https://apify.com/apify/instagram-post-scraper.md).

**apify/instagram-scraper** (id `shu8hvrXbJbY3Eb9W`) — [README](https://apify.com/apify/instagram-scraper.md), [API](https://api.apify.com/v2/acts/apify~instagram-scraper)
- Input:
  - `directUrls` (array; e.g. `https://www.instagram.com/{handle}/`).
  - `resultsType` (enum `posts` | `details` | `comments` | `reels` | `mentions` | `stories`, default `posts`).
  - `resultsLimit` (integer, min 1, prefill 100; per URL).
  - `onlyPostsNewerThan` (string).
  - `search`, `searchType` (`hashtag` | `profile` | `place` | `user`), `searchLimit` (1–250).
  - `addParentData` (bool, hidden).
  - `skipPinnedPosts` is documented in the README FAQ ("works with `resultsType: "posts"`") but is not in the input schema properties I extracted.
- `resultsType: "details"` returns one profile item with `followersCount` and `latestPosts`. `"posts"` returns post items in the shared schema.
- Pricing (PPE): one `result` event, FREE 0.0027 / BRONZE 0.0023 / SILVER 0.0019 / GOLD 0.0015 / PLATINUM 0.0009 / DIAMOND 0.0005 — [API pricingInfos](https://api.apify.com/v2/acts/apify~instagram-scraper).
- A README sample shows a Sidecar with `"videoPlayCount": 0`, so a `0` can be legitimate for non-video items — [README](https://apify.com/apify/instagram-scraper.md).
- Stats: 496,817 users, 71,061 monthly. Last 30 days: 16,866,742 of 16,931,009 runs succeeded. Rating 4.68. Default timeout 604800 s — [API](https://api.apify.com/v2/acts/apify~instagram-scraper).

**apify/instagram-api-scraper** (id `RB9HEZitC8hIUXAha`) — [README](https://apify.com/apify/instagram-api-scraper.md), [API](https://api.apify.com/v2/acts/apify~instagram-api-scraper)
- Input:
  - `directUrls`.
  - `resultsType` (`posts` | `comments` | `details` | `mentions` | `reels` | `stories` (deprecated); default `posts`).
  - `resultsLimit` (min 1, prefill 200).
  - `onlyPostsNewerThan`, `search`, `searchType` (`user` | `hashtag` | `place`), `searchLimit` (1–250), `addParentData`.
- Pricing (PPE):
  - `result`: FREE 0.0023 / BRONZE 0.002 / SILVER 0.0017 / GOLD 0.0014 / PLATINUM 0.0009 / DIAMOND 0.0004.
  - `actor-start`: 0.001.
  - `search-result`: 0.006 on FREE.
  - `filter-applied` (date filter): 0.0013 on FREE per post.
  - Source: [API pricingInfos](https://api.apify.com/v2/acts/apify~instagram-api-scraper).
- Stats: 19,901 users, 911 monthly. Rating 3.00 — [README](https://apify.com/apify/instagram-api-scraper.md), [API](https://api.apify.com/v2/acts/apify~instagram-api-scraper).

**Reel view/play reliability reports** (public Issues; dates not visible in what I fetched)
- "videoPlayCount is always returned as 0 … likesCount is always -1" — [reel-scraper issue](https://apify.com/apify/instagram-reel-scraper/issues/videoplaycount--0-li-JW5XPst0hWkYESA70)
- "the video view count is not working. Its just showing 0" — [reel-scraper issue](https://apify.com/apify/instagram-reel-scraper/issues/video-view-count-is-9HbRODGNwVfrOt1bx)
- "I did not see videoViewCount when using reel scraper" — [reel-scraper issue](https://apify.com/apify/instagram-reel-scraper/issues/no-videoviewcount-in-BOK4idXEzjvfZcnhM)
- A user reports that the views shown on Reel thumbnails differ from the scraped view/play counts — [reel-scraper issue](https://apify.com/apify/instagram-reel-scraper/issues/viewcount--playcount-YXuqFfkhDu4ieslrB)
- A user says the Actor "traditionally … displays the Instagram and Facebook viewership" and reports a regression. Search snippets say videoPlayCount includes only Instagram plays, not the combined public number — [reel-scraper issue](https://apify.com/apify/instagram-reel-scraper/issues/videoplaycount-faceb-x2farbP0DNGy7vKzw)
- "quite a few of the videos crawled have missing play counts. View counts are collected fine but play counts seem to be missing" — [post-scraper issue](https://apify.com/apify/instagram-post-scraper/issues/video-play-counts-mi-Z9MLa1rezMru0ltev)
- A third-party Actor says Instagram exposes a separate view count only for direct Reel URLs, and that `videoViewCount` is null for Reels collected from a profile. This is third-party and unverified for the apify Actors — [search result summary of fetch_cat/memo23 READMEs](https://apify.com/memo23/instagram-reel-scraper)

### Inferences
- **Recommended IG feeder:** `apify/instagram-post-scraper` with `{"username": [handle], "resultsLimit": 30, "skipPinnedPosts": true, "dataDetailLevel": "basicData"}`. It returns the mixed feed (Image / Sidecar / Reel), so you can compute engagement on all formats and views on `productType == "clips"`. Pair it with `apify/instagram-profile-scraper` `{"usernames": [handle]}` for `followersCount`.
  - Cost at FREE tier: about 30 × 0.0017 + 0.0026 ≈ **$0.054**, or about $0.084 with detailedData.
  - Set `dataDetailLevel` explicitly. The schema default is `detailedData`, so omitting it via the API costs more.
- If BVAL only prices Reels, use `apify/instagram-reel-scraper` (`resultsLimit: 30`, `skipPinnedPosts: true`) instead. It costs about 30 × 0.0026 + 0.001 ≈ $0.079 on FREE, and becomes cheaper than the post scraper on SILVER and above (0.0014/reel). It also offers `sharesCount` via a paid add-on.
- Do not use `latestPosts` from the profile scraper as the views source. It is capped at 12 items and only shows `videoViewCount`, which the Actors' own schema calls deprecated/stale.
- Read views in this order: `videoPlayCount` → `igPlayCount` → `videoViewCount`. Record which field was used. Treat `0` on a `clips` item, or `likesCount == -1`, as missing rather than real.
- `instagram-scraper` is a reasonable one-Actor alternative: two calls (`details` + `posts`), about $0.084 on FREE. `instagram-api-scraper` is functionally similar but has low adoption (911 monthly users, rating 3.0), so it is not recommended.
- Run the two calls in parallel with `Actor.start` and then wait on both, so total latency is the longer of the two runs, not their sum.

### Gaps
- Typical run time (seconds) for 30 posts is not published in the READMEs or the API stats. Benchmark it with a small test run. The task forbade running paid Actors, so I could not measure it.
- Whether `dataDetailLevel: "basicData"` still includes `videoPlayCount` is not stated. The README does not list per-level fields.
- Dates and resolution status of the issues above were not visible, so I cannot say whether they are current or fixed.

## Q2. TikTok: clockworks/tiktok-profile-scraper vs clockworks/tiktok-scraper

### Takeaway
Both Actors return the same item schema: one item per video, with the author's follower count embedded as `authorMeta.fans` on every item. Use `clockworks/tiktok-profile-scraper`. It is cheaper (FREE $0.003/result vs $0.0037), has a profile-specific input, and carries no $0.50 `minimalMaxTotalChargeUsd`. 30 videos cost about $0.09 on FREE and $0.045 on SILVER.

### Cited Findings
**clockworks/tiktok-profile-scraper** (id `0FXVyOXXEmdGcV88a`) — [README](https://apify.com/clockworks/tiktok-profile-scraper.md), [API](https://api.apify.com/v2/acts/clockworks~tiktok-profile-scraper), [build](https://api.apify.com/v2/acts/clockworks~tiktok-profile-scraper/builds/default)
- Input:
  - `profiles` (array, **required**; usernames or user IDs).
  - `resultsPerPage` (integer, **default 100**, min 1; "number of posts ... from every profile"). Set it to 30.
  - `profileSorting` (`latest` | `popular` | `oldest`, default `latest`).
  - `profileScrapeSections` (array, default `["videos"]`).
  - `excludePinnedPosts` (bool, default false).
  - `oldestPostDateUnified` / `newestPostDate` (charged date filters).
  - `mostDiggs` / `leastDiggs` (charged).
  - `maxFollowersPerProfile`, `maxFollowingPerProfile` (prefill 0).
  - `shouldDownloadVideos`, `shouldDownloadCovers`, `shouldDownloadSlideshowImages`, `shouldDownloadAvatars` (all default false).
  - `downloadSubtitlesOptions` (default `NEVER_DOWNLOAD_SUBTITLES`).
  - `commentsPerPost`, `topLevelCommentsPerPost`, `maxRepliesPerComment` (prefill 0).
- Output fields per video:
  - Counts: `playCount` ("viewed"), `diggCount` (likes), `commentCount`, `shareCount`, `collectCount` (saves), `repostCount`.
  - Time: `createTime` (unix), `createTimeISO`.
  - Type: `isSlideshow` (image post vs video), `isPinned`, `isAd`, `isSponsored`.
  - Other: `videoMeta.duration`, `webVideoUrl`, `id`, `text`.
  - Author: `authorMeta.fans` (followers), `authorMeta.following`, `authorMeta.heart` (total likes), `authorMeta.video` (video count), `authorMeta.name`, `authorMeta.verified`, `authorMeta.privateAccount`.
  - Errors: `error`, `errorCode` (e.g. `NOT_FOUND`).
- Pricing (PPE):
  - `result`: FREE 0.003 / BRONZE 0.002 / SILVER 0.0015 / GOLD 0.001 / PLATINUM 0.0006 / DIAMOND 0.0003.
  - Date filter (`filter-applied`) and popularity filter: each FREE 0.0013 / … / DIAMOND 0.00017.
  - Follower/following items: 0.004 on FREE.
  - `minimalMaxTotalChargeUsd` null. Source: [API pricingInfos](https://api.apify.com/v2/acts/clockworks~tiktok-profile-scraper).
- Stats: 68,679 users, 10,089 monthly. Last 30 days: 3,410,793 of 3,560,560 succeeded, 133,795 aborted, 7,676 failed. Rating 4.73. Default memory 4096 MB — [API](https://api.apify.com/v2/acts/clockworks~tiktok-profile-scraper), [README](https://apify.com/clockworks/tiktok-profile-scraper.md).

**clockworks/tiktok-scraper** (id `GdWCkxBtKWOsKjdch`) — [README](https://apify.com/clockworks/tiktok-scraper.md), [API](https://api.apify.com/v2/acts/clockworks~tiktok-scraper)
- Input: same profile fields as above, plus `hashtags`, `searchQueries`, `searchSection`, `postURLs`, `scrapeRelatedVideos`, `scrapeAdditionalAuthorMeta`, `aiVideoDescription`, `aiVideoSummary`, `proxyCountryCode`. No field is required.
- `resultsPerPage` has **default 1** (prefill 100, max 1,000,000), so it must be set explicitly.
- Output: same schema as the profile scraper, plus inline `comments[]`.
- Pricing (PPE): `result` FREE 0.0037 / BRONZE 0.003 / SILVER 0.0023 / GOLD 0.0017 / PLATINUM 0.001 / DIAMOND 0.0005. Same add-ons. **`minimalMaxTotalChargeUsd` 0.5** — [API pricingInfos](https://api.apify.com/v2/acts/clockworks~tiktok-scraper).
- Stats: 399,358 users, 37,589 monthly. Last 30 days: 8,892,214 of 9,057,689 succeeded, 94,556 failed, 57,889 timed out. Rating 4.75 — [API](https://api.apify.com/v2/acts/clockworks~tiktok-scraper), [README](https://apify.com/clockworks/tiktok-scraper.md).

### Inferences
- Recommended call: `clockworks/tiktok-profile-scraper` with `{"profiles": [handle], "resultsPerPage": 30, "profileSorting": "latest", "excludePinnedPosts": true}`.
  - Avoid date filters, because they are charged per item.
  - Take followers from `items[0]["authorMeta"]["fans"]`.
  - Exclude or flag `isSlideshow == true` items when computing video view rates.
- TikTok `playCount` is the only view metric, and the README samples show it is populated on every item.
- The profile scraper's 3.8% abort rate is probably user-initiated aborts. That is my reading, not a documented cause.

### Gaps
- Typical run time is not published. The Actors default to 4096 MB, which affects memory quota but not price under PPE.
- I did not verify whether `authorMeta.fans` is populated when a profile has 0 public videos.

## Q3. YouTube: streamers/youtube-scraper vs youtube-channel-scraper vs youtube-shorts-scraper

### Takeaway
`streamers/youtube-channel-scraper` is the cheapest ($0.0013/video on FREE). However, its output has **no `likes` or `commentsCount`** and its `date` is relative ("23 hours ago"). Use it only if views plus subscribers are enough.

For views + likes + comments + subscribers, use `streamers/youtube-scraper` with a channel URL in `startUrls`, plus `maxResults` (long-form) and `maxResultsShorts`. It costs $0.004/video on FREE. `youtube-shorts-scraper` has the same price and fields, but for Shorts only.

### Cited Findings
**streamers/youtube-scraper** (id `h7sDV53CddomktSi5`) — [README](https://apify.com/streamers/youtube-scraper.md), [API](https://api.apify.com/v2/acts/streamers~youtube-scraper), [build](https://api.apify.com/v2/acts/streamers~youtube-scraper/builds/default)
- Input:
  - `startUrls` (array of `{url}`, default `[]`; video, channel or playlist URLs).
  - `searchQueries` (array).
  - `maxResults` (integer, default 0, max 999999; "If you scrape a channel, acts as a limit for regular videos").
  - `maxResultsShorts` (default 0), `maxResultStreams` (default 0).
  - `sortVideosBy` (`NEWEST` | `POPULAR` | `OLDEST`).
  - `oldestPostDate` (string; charged on channels).
  - `transcriptionAndSubtitle` (default `NONE`), `aiVideoDescription` / `aiVideoSummary` (default false).
  - Search filters (`sortingOrder`, `dateFilter`, …).
- Output:
  - Video: `viewCount`, `likes`, `commentsCount`, `commentsTurnedOff`, `date` ("publish date", sample `"2024-08-27T07:47:39.000Z"`; another README sample shows `"2021-12-21"`), `duration` (`"00:03:27"` string), `type` (enum `video` | `shorts` | `stream`), `id`, `url`, `title`.
  - Channel: `numberOfSubscribers`, `channelTotalViews`, `channelTotalVideos`, `channelName`, `channelUsername`, `channelId`, `isMonetized`.
- Error items carry an `error` field with codes such as `CHANNEL_DOES_NOT_EXIST` and `VIDEO_UNAVAILABLE` — [README](https://apify.com/streamers/youtube-scraper.md).
- Pricing (PPE):
  - `result` (Video): FREE 0.004 / BRONZE 0.003 / SILVER 0.0026 / GOLD 0.0024 / PLATINUM 0.0015 / DIAMOND 0.001.
  - `date-filter`: 0.0013 on FREE.
  - AI add-ons: 0.015/min on FREE.
  - Source: [API pricingInfos](https://api.apify.com/v2/acts/streamers~youtube-scraper).
- Stats: 212,901 users, 18,378 monthly. Last 30 days: 2,580,027 of 2,603,003 succeeded. Rating 4.06 — [API](https://api.apify.com/v2/acts/streamers~youtube-scraper), [README](https://apify.com/streamers/youtube-scraper.md).

**streamers/youtube-channel-scraper** ("Fast YouTube Channel Scraper", id `67Q6fmd8iedTVcCwY`) — [README](https://apify.com/streamers/youtube-channel-scraper.md), [API](https://api.apify.com/v2/acts/streamers~youtube-channel-scraper)
- Input: `startUrls` (**required**, e.g. `[{"url": "https://www.youtube.com/@Apify"}]`), `maxResults` (default 0, prefill 10), `maxResultsShorts` (default 0), `maxResultStreams` (default 0), `oldestPostDate`, `sortVideosBy` (`NEWEST` | `POPULAR` | `OLDEST`).
- Output: `viewCount`, `type` (video | stream | shorts), `duration` (`"11:20"`), `date` ("publication date or relative time", sample `"23 hours ago"`), `numberOfSubscribers`, `channelTotalViews`, `channelTotalVideos`, `isChannelVerified`, `fromChannelListPage`. **There are no `likes` or `commentsCount` fields in the schema.**
- The README says: "You can get like and comment counts for each video by using the YouTube Scraper" — [README FAQ](https://apify.com/streamers/youtube-channel-scraper.md).
- Pricing (PPE): `result` FREE 0.0013 / BRONZE 0.001 / SILVER 0.0008 / GOLD 0.0005 / PLATINUM 0.0003 / DIAMOND 0.0002 — [API](https://api.apify.com/v2/acts/streamers~youtube-channel-scraper).
- Stats: 31,773 users, 4,252 monthly. Last 30 days: 1,844,672 of 1,870,512 succeeded, 24,253 failed (about 1.3%). Rating 4.61 — [API](https://api.apify.com/v2/acts/streamers~youtube-channel-scraper).

**streamers/youtube-shorts-scraper** (id `WT1BVWatl2aHVeFEH`) — [README](https://apify.com/streamers/youtube-shorts-scraper.md), [API](https://api.apify.com/v2/acts/streamers~youtube-shorts-scraper)
- Input: `channels` (array, **required**; username without @, or URL), `maxResultsShorts` (integer, **default 1**, prefill 10, max 999999), `oldestPostDate` (charged), `sortChannelShortsBy` (`NEWEST` | `POPULAR` | `OLDEST`).
- Output: `viewCount`, `likes`, `commentsCount`, `date` (ISO 8601), `duration`, `type` ("shorts"), `numberOfSubscribers`, `channelTotalViews`, `aboutChannelInfo.*`, `error`, `note`.
- Pricing: `result` (Short) FREE 0.004 / BRONZE 0.003 / SILVER 0.0026 / GOLD 0.0024 / PLATINUM 0.0015 / DIAMOND 0.0008. `date-filter` 0.0013 on FREE — [API](https://api.apify.com/v2/acts/streamers~youtube-shorts-scraper).
- Stats: 73,212 users, 937 monthly. Last 30 days: 88,364 of 88,519 succeeded. Rating 4.35 — [API](https://api.apify.com/v2/acts/streamers~youtube-shorts-scraper), [README](https://apify.com/streamers/youtube-shorts-scraper.md).

### Inferences
- Recommended call: `streamers/youtube-scraper` with `{"startUrls": [{"url": "https://www.youtube.com/@{handle}"}], "maxResults": 30, "maxResultsShorts": 30, "maxResultStreams": 0, "sortVideosBy": "NEWEST"}`.
  - Split the items by `type` and compute benchmarks for long-form and Shorts separately, since Shorts view rates are very different.
  - Cost is up to 60 × 0.004 = $0.24 on FREE. Use `maxResultsShorts: 0` if only long-form is priced (30 × 0.004 = $0.12).
  - Take subscribers from `items[0]["numberOfSubscribers"]`.
- The cheap option is `youtube-channel-scraper`: views + subscribers only, $0.039 for 30 videos on FREE. You would have to parse the relative `date` yourself.
- YouTube is the most expensive platform per item, so tier discounts matter most there.

### Gaps
- Typical run time is not published.
- Whether `youtube-scraper` returns `likes` and `commentsCount` for every channel-listed video, rather than only for direct video URLs, is implied by the schema but not explicitly stated for channel mode.
- `date` format inconsistency across samples (ISO datetime vs date-only) should be handled defensively.

## Q4. Calling feeders from a Python Actor (Apify SDK) and cross-platform recommendation

### Takeaway
Inside the BVAL Actor, call `await Actor.call(actor_id='apify/instagram-post-scraper', run_input={...})`. Then read the results with `await Actor.apify_client.run(run.id).dataset().list_items()`, which returns an object with `.items`. To call feeders in parallel, use `Actor.start(...)` and wait on each run. Recommended feeders:
- Instagram: post-scraper (or reel-scraper) plus profile-scraper.
- TikTok: tiktok-profile-scraper.
- YouTube: youtube-scraper (or channel-scraper if likes are not needed).

### Cited Findings
- `Actor.call` "starts another Actor on the Apify platform, and waits for the started Actor run to finish". The doc example: `actor_run = await Actor.call(actor_id='apify/screenshot-url', run_input={...})`, then `run_client = Actor.apify_client.run(actor_run.id)`, `dataset_client = run_client.dataset()`, `item_list = await dataset_client.list_items()`, `item_list.items` — [Apify SDK for Python: Interacting with other Actors](https://docs.apify.com/sdk/python/docs/concepts/interacting-with-other-actors.md)
- `Actor.start(actor_id=..., run_input=...)` "immediately returns the details of the started Actor run" (`actor_run.id`). `Actor.abort(run_id=..., gracefully=True)` stops a run — [same doc](https://docs.apify.com/sdk/python/docs/concepts/interacting-with-other-actors.md)
- Outside an Actor, the README pattern with the plain client is `client.actor("apify/instagram-profile-scraper").call(run_input={"usernames": ["humansofny"]})`, then `client.dataset(run.default_dataset_id).iterate_items()` — [profile-scraper README Python example](https://apify.com/apify/instagram-profile-scraper.md)
- All feeders listed are PPE. PPE Actors charge per event, and platform usage is not billed separately — [profile-scraper README pricing section](https://apify.com/apify/instagram-profile-scraper.md)

### Inferences
Summary table. Costs are estimates for one creator at FREE tier, computed from the pricingInfos above.

| Platform | Feeder(s) | Key input | Followers field | Views field | Likes / comments / shares | Type field | Time field | Est. cost (FREE) |
|---|---|---|---|---|---|---|---|---|
| Instagram | `apify/instagram-profile-scraper` + `apify/instagram-post-scraper` | `usernames:[h]`; `username:[h], resultsLimit:30, dataDetailLevel:"basicData", skipPinnedPosts:true` | `followersCount` | `videoPlayCount` (fallback `igPlayCount`, then `videoViewCount`) | `likesCount` (-1 = hidden), `commentsCount`, `sharesCount` (reel scraper add-on only) | `type` + `productType` (`clips` = Reel) | `timestamp` (ISO) | ~$0.054 |
| Instagram (Reels-only alt) | `apify/instagram-reel-scraper` | `username:[h], resultsLimit:30, skipPinnedPosts:true` | (none; use profile scraper) | same | same; `includeSharesCount:true` adds $0.002–0.007/reel | `productType` | `timestamp` | ~$0.079 + $0.0026 |
| TikTok | `clockworks/tiktok-profile-scraper` | `profiles:[h], resultsPerPage:30, profileSorting:"latest", excludePinnedPosts:true` | `authorMeta.fans` | `playCount` | `diggCount`, `commentCount`, `shareCount`, `collectCount` | `isSlideshow` | `createTimeISO` / `createTime` | ~$0.09 |
| YouTube | `streamers/youtube-scraper` | `startUrls:[{url}], maxResults:30, maxResultsShorts:0–30, sortVideosBy:"NEWEST"` | `numberOfSubscribers` | `viewCount` | `likes`, `commentsCount` (no shares) | `type` (`video` / `shorts` / `stream`) | `date` | ~$0.12–0.24 |
| YouTube (cheap) | `streamers/youtube-channel-scraper` | `startUrls:[{url}], maxResults:30` | `numberOfSubscribers` | `viewCount` | none | `type` | `date` (may be relative) | ~$0.039 |

- Set the `max_total_charge_usd` / `timeout` on the child runs to bound cost and latency. See the gap below on exact `Actor.call` kwargs.
- Always check for items with an `error` key: the YouTube and TikTok Actors push error items instead of failing silently.

### Gaps
- The exact keyword names for `Actor.call` timeout, memory and max-charge (e.g. `timeout`, `memory_mbytes`, `max_total_charge_usd`) were not verified. The doc page I read only shows `actor_id` and `run_input`. Check the [Actor class reference](https://docs.apify.com/sdk/python/reference/class/Actor.md).
- No source gives median run duration for any of these Actors, so whether a run finishes in under 60 s is unverified. Cold-start plus scraping for 30 items needs a measured benchmark.
