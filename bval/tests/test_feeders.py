"""Feeder normalisers tested against real scraper output captured on 22 Nov 2026 (tests/fixtures/)."""

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from my_actor.feeders import FeederError, clean_handle, normalise_instagram, normalise_tiktok, normalise_youtube
from my_actor.pricing import Terms, evaluate_deal

FIX = Path(__file__).parent / 'fixtures'
NOW = datetime(2026, 11, 22, 12, 0, tzinfo=timezone.utc)  # fixtures were captured today; pin "now" for stable ages


def load(name):
    return json.loads((FIX / name).read_text())


class HandleParsing(unittest.TestCase):
    def test_variants(self):
        self.assertEqual(clean_handle('@humansofny'), 'humansofny')
        self.assertEqual(clean_handle('https://www.instagram.com/humansofny/'), 'humansofny')
        self.assertEqual(clean_handle('https://www.tiktok.com/@khaby.lame'), 'khaby.lame')
        self.assertEqual(clean_handle('https://www.youtube.com/@mkbhd/videos'), 'mkbhd')

    def test_rejects_garbage(self):
        with self.assertRaises(FeederError):
            clean_handle('not a handle; rm -rf /')


class InstagramFixture(unittest.TestCase):
    def setUp(self):
        self.m, self.info = normalise_instagram(load('instagram_profile.json'), load('instagram_reels.json'), NOW)

    def test_metrics(self):
        self.assertEqual(self.m.audience, 12_610_865)
        self.assertEqual(self.m.views_field, 'videoPlayCount')
        self.assertGreater(self.m.median_views['instagram_reel'], 0)
        self.assertIsNotNone(self.m.engagement_rate['instagram_reel'])

    def test_age_window(self):
        # humansofny posts rarely: only 9 of its 30 Reels are 3-120 days old. 9 >= 6, so no widening.
        self.assertFalse(self.m.age_fallback)
        self.assertEqual(self.m.sample_size['instagram_reel'], 9)

    def test_window_widens_when_too_few_recent(self):
        reels = load('instagram_reels.json')
        old_only = [r for r in reels if r['timestamp'] < '2026-07-01']  # all older than 120 days
        m, info = normalise_instagram(load('instagram_profile.json'), old_only, NOW)
        self.assertTrue(m.age_fallback)
        self.assertEqual(info['ageWindowDays'], [3, 365])

    def test_prices_end_to_end(self):
        r = evaluate_deal(self.m, Terms(deliverables=[{'type': 'instagram_reel', 'qty': 1}], offer_amount=5000))
        self.assertEqual(r['tier'], 'mega')
        self.assertIn(r['confidence'], ('medium', 'low'))

    def test_private_account(self):
        with self.assertRaises(FeederError):
            normalise_instagram([{'username': 'x', 'private': True, 'followersCount': 10}], [], NOW)


class TikTokFixture(unittest.TestCase):
    def test_metrics(self):
        m, info = normalise_tiktok(load('tiktok_profile.json'), NOW)
        self.assertEqual(m.audience, 162_900_000)
        self.assertGreaterEqual(m.sample_size['tiktok_video'], 6)
        self.assertIsNotNone(m.volatility)
        self.assertGreater(m.engagement_rate['tiktok_video'], 0)
        evaluate_deal(m, Terms(deliverables=[{'type': 'tiktok_video', 'qty': 1}]))


class YouTubeFixture(unittest.TestCase):
    def test_metrics(self):
        m, info = normalise_youtube(load('youtube_channel.json'), NOW)
        self.assertEqual(m.audience, 21_400_000)
        self.assertGreaterEqual(m.sample_size['youtube_integration'], 6)
        self.assertFalse(m.age_fallback)
        self.assertGreater(m.median_views['youtube_short'], 0)
        r = evaluate_deal(m, Terms(deliverables=[{'type': 'youtube_integration', 'qty': 1}, {'type': 'youtube_short', 'qty': 1}], niche='tech'))
        self.assertEqual(r['scope']['packageDiscountPct'], 10)

    def test_error_items(self):
        with self.assertRaises(FeederError):
            normalise_youtube([{'error': 'CHANNEL_DOES_NOT_EXIST'}], NOW)


if __name__ == '__main__':
    unittest.main()
