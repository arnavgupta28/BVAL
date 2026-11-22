"""Unit tests for the BVAL pricing engine.

Examples A, B and C reproduce the worked examples in bval_research.md (section 3), so the engine stays
faithful to the cited research. Run: python -m unittest discover -s tests
"""

import unittest

from my_actor.pricing import Metrics, PricingError, Terms, evaluate_deal, load_rates

RATES = load_rates()


def ig_example(**overrides):
    m = Metrics(
        platform='instagram',
        audience=85_000,
        median_views={'instagram_reel': 42_000},
        engagement_rate={'instagram_reel': 0.035},
        sample_size={'instagram_reel': 24},
        views_field='videoPlayCount',
    )
    t = Terms(
        deliverables=[{'type': 'instagram_reel', 'qty': 1}],
        niche='fitness',
        organic_usage_days=90,
        whitelisting_days=30,
        exclusivity_days=180,
        offer_amount=800,
    )
    for k, v in overrides.items():
        setattr(t, k, v)
    return m, t


class WorkedExampleA_Instagram(unittest.TestCase):
    def setUp(self):
        self.r = evaluate_deal(*ig_example(), RATES)

    def test_base_and_er_adjustment(self):
        unit = self.r['scope']['units'][0]
        self.assertAlmostEqual(unit['raw'], 924, delta=0.5)
        self.assertAlmostEqual(unit['erAdjustment'], 1.074, delta=0.001)
        self.assertAlmostEqual(unit['unitUsd'], 992, delta=1)
        self.assertFalse(unit['clamped'])
        self.assertEqual(self.r['tier'], 'micro')

    def test_line_items(self):
        amounts = {i['key']: i['amountUsd'] for i in self.r['scope']['addons']}
        self.assertAlmostEqual(amounts['organic_usage'], 159, delta=1)
        self.assertAlmostEqual(amounts['whitelisting'], 278, delta=1)
        self.assertAlmostEqual(amounts['exclusivity'], 1364, delta=1)

    def test_price_points_and_verdict(self):
        p = self.r['pricePointsUsd']
        self.assertAlmostEqual(p['fair'], 2793, delta=2)
        self.assertAlmostEqual(p['ask'], 3490, delta=5)
        self.assertAlmostEqual(p['floor'], 2374, delta=5)
        self.assertAlmostEqual(p['walkAway'], 910, delta=2)
        self.assertEqual(self.r['verdict'], 'DECLINE_OR_REDUCE_SCOPE')

    def test_red_flags(self):
        codes = {f['code'] for f in self.r['redFlags']}
        self.assertIn('LONG_EXCLUSIVITY', codes)
        self.assertIn('UNPRICED_WHITELISTING', codes)

    def test_reduced_scope_is_minimum_scope(self):
        self.assertAlmostEqual(self.r['reducedScope']['priceUsd'], 1071, delta=2)

    def test_india_market_flips_to_accept(self):
        r = evaluate_deal(*ig_example(market='india'), RATES)
        self.assertAlmostEqual(r['pricePointsUsd']['fair'], 698, delta=2)
        self.assertEqual(r['verdict'], 'ACCEPT')

    def test_inr_offer_is_converted(self):
        r = evaluate_deal(*ig_example(offer_amount=74_800, offer_currency='INR'), RATES)
        self.assertAlmostEqual(r['offerUsd'], 800, delta=0.01)


class WorkedExampleB_TikTok(unittest.TestCase):
    def setUp(self):
        m = Metrics(
            platform='tiktok',
            audience=220_000,
            median_views={'tiktok_video': 95_000},
            engagement_rate={'tiktok_video': 0.072},
            sample_size={'tiktok_video': 28},
            volatility=2.6,
        )
        t = Terms(
            deliverables=[{'type': 'tiktok_video', 'qty': 1}],
            niche='beauty',
            whitelisting_days=30,
            paid_usage_days=60,
            rush_hours=48,
            revision_rounds=2,
            exclusivity_days=7,
            offer_amount=1500,
        )
        self.r = evaluate_deal(m, t, RATES)

    def test_line_items(self):
        self.assertAlmostEqual(self.r['scope']['contentBaseUsd'], 1260, delta=1)
        amounts = {i['key']: i['amountUsd'] for i in self.r['scope']['addons']}
        self.assertAlmostEqual(amounts['whitelisting'], 375, delta=1)
        self.assertAlmostEqual(amounts['paid_usage'], 252, delta=1)
        self.assertAlmostEqual(amounts['rush'], 441, delta=1)
        self.assertAlmostEqual(amounts['revisions'], 189, delta=1)
        self.assertNotIn('exclusivity', amounts)  # 7 days is the free window

    def test_price_points_and_verdict(self):
        p = self.r['pricePointsUsd']
        self.assertAlmostEqual(p['fair'], 2516, delta=2)
        self.assertAlmostEqual(p['walkAway'], 1178, delta=2)
        self.assertEqual(self.r['verdict'], 'COUNTER_TRADE_SCOPE')

    def test_reduced_scope_keeps_spark_ads(self):
        red = self.r['reducedScope']
        self.assertAlmostEqual(red['priceUsd'], 1635, delta=2)
        self.assertEqual(red['droppedOrReduced'], ['rush', 'revisions', 'paid_usage'])


class WorkedExampleC_YouTube(unittest.TestCase):
    def setUp(self):
        self.m = Metrics(
            platform='youtube',
            audience=180_000,
            median_views={'youtube_integration': 60_000},
            engagement_rate={'youtube_integration': 0.042},
            sample_size={'youtube_integration': 22},
        )
        self.t = Terms(
            deliverables=[{'type': 'youtube_integration', 'qty': 1}],
            niche='tech',
            pinned_comment_link=True,
            paid_usage_days=30,
            exclusivity_days=30,
            offer_amount=3200,
        )
        self.r = evaluate_deal(self.m, self.t, RATES)

    def test_price_points_and_verdict(self):
        self.assertAlmostEqual(self.r['scope']['contentBaseUsd'], 2125, delta=1)
        self.assertAlmostEqual(self.r['pricePointsUsd']['fair'], 3559, delta=3)
        self.assertEqual(self.r['verdict'], 'COUNTER_LIGHT')

    def test_reduced_scope_drops_paid_usage(self):
        self.assertAlmostEqual(self.r['reducedScope']['priceUsd'], 3030, delta=5)

    def test_whitelisting_rejected_on_youtube(self):
        self.t.whitelisting_days = 30
        r = evaluate_deal(self.m, self.t, RATES)
        self.assertTrue(r['warnings'])
        self.assertNotIn('whitelisting', {i['key'] for i in r['scope']['addons']})


class EdgeCases(unittest.TestCase):
    def test_wrong_platform_deliverable(self):
        m, t = ig_example(deliverables=[{'type': 'tiktok_video', 'qty': 1}])
        with self.assertRaises(PricingError):
            evaluate_deal(m, t, RATES)

    def test_youtube_without_views_errors(self):
        m = Metrics(platform='youtube', audience=50_000)
        t = Terms(deliverables=[{'type': 'youtube_integration', 'qty': 1}])
        with self.assertRaises(PricingError):
            evaluate_deal(m, t, RATES)

    def test_instagram_follower_fallback_is_very_low_confidence(self):
        m = Metrics(platform='instagram', audience=50_000)
        t = Terms(deliverables=[{'type': 'instagram_reel', 'qty': 1}])
        r = evaluate_deal(m, t, RATES)
        self.assertEqual(r['confidence'], 'very_low')
        self.assertEqual(r['verdict'], 'NO_OFFER')

    def test_package_discount(self):
        m, t = ig_example(deliverables=[{'type': 'instagram_reel', 'qty': 1}, {'type': 'instagram_story_frame', 'qty': 2}])
        r = evaluate_deal(m, t, RATES)
        self.assertEqual(r['scope']['packageDiscountPct'], 15)

    def test_gifted_for_rights(self):
        m, t = ig_example(offer_amount=None, gifted_only=True)
        r = evaluate_deal(m, t, RATES)
        self.assertIn('GIFTED_FOR_RIGHTS', {f['code'] for f in r['redFlags']})

    def test_walk_away_never_above_floor(self):
        m, t = ig_example(organic_usage_days=0, whitelisting_days=0, exclusivity_days=0)
        r = evaluate_deal(m, t, RATES)
        p = r['pricePointsUsd']
        self.assertLessEqual(p['walkAway'], p['floor'])


if __name__ == '__main__':
    unittest.main()
