"""Market (audience country) resolution and factors, from reports/BVAL country market factors.md."""

import unittest

from my_actor.pricing import Metrics, PricingError, Terms, evaluate_deal, load_rates, resolve_market

RATES = load_rates()


def ig(market, **kw):
    m = Metrics(platform='instagram', audience=85_000, median_views={'instagram_reel': 42_000},
                engagement_rate={'instagram_reel': 0.035}, sample_size={'instagram_reel': 24}, views_field='videoPlayCount')
    t = Terms(deliverables=[{'type': 'instagram_reel', 'qty': 1}], niche='fitness', market=market, **kw)
    return evaluate_deal(m, t, RATES)


class Resolution(unittest.TestCase):
    def test_global_default(self):
        mk = resolve_market(None, RATES)
        self.assertEqual(mk['code'], 'GLOBAL')
        self.assertEqual(mk['factor_by_tier']['micro'], 1.0)

    def test_named_country_and_alias(self):
        mk = resolve_market('uk', RATES)
        self.assertEqual(mk['code'], 'GB')
        self.assertEqual(mk['match'], 'country')
        self.assertLess(mk['factor_by_tier']['micro'], 1.0)

    def test_group_fallback_covers_unlisted_country(self):
        mk = resolve_market('FR', RATES)
        self.assertEqual(mk['match'], 'group')
        self.assertLess(mk['factor_by_tier']['micro'], 1.0)

    def test_every_iso_code_in_groups_resolves(self):
        for gid, g in RATES['markets']['groups'].items():
            for code in g['members']:
                with self.subTest(code=code):
                    resolve_market(code, RATES, 'instagram')

    def test_china_unsupported(self):
        with self.assertRaises(PricingError):
            resolve_market('CN', RATES)

    def test_tiktok_blocked_in_india(self):
        with self.assertRaises(PricingError):
            resolve_market('IN', RATES, 'tiktok')

    def test_invalid_code(self):
        with self.assertRaises(PricingError):
            resolve_market('not-a-country', RATES)


class Pricing(unittest.TestCase):
    def test_india_unchanged_by_merge(self):
        r = ig('IN', organic_usage_days=90, whitelisting_days=30, exclusivity_days=180, offer_amount=800)
        self.assertAlmostEqual(r['pricePointsUsd']['fair'], 698, delta=2)
        self.assertEqual(r['verdict'], 'ACCEPT')

    def test_market_ordering(self):
        fair = {c: ig(c)['pricePointsUsd']['fair'] for c in ('GLOBAL', 'GB', 'DE', 'BR', 'IN')}
        self.assertGreater(fair['GLOBAL'], fair['GB'])
        self.assertGreater(fair['GB'], fair['BR'])
        self.assertGreater(fair['BR'], 0)

    def test_indonesia_tiktok_multiplier(self):
        m = Metrics(platform='tiktok', audience=220_000, median_views={'tiktok_video': 95_000},
                    engagement_rate={'tiktok_video': 0.072}, sample_size={'tiktok_video': 28})
        t = Terms(deliverables=[{'type': 'tiktok_video', 'qty': 1}], market='ID')
        u = evaluate_deal(m, t, RATES)['scope']['units'][0]
        self.assertAlmostEqual(u['marketFactor'], 0.35 * 2.0, places=3)

    def test_offer_in_gbp(self):
        r = ig('GB', offer_amount=500, offer_currency='GBP')
        self.assertAlmostEqual(r['offerUsd'], 500 / 0.7523, delta=1)


if __name__ == '__main__':
    unittest.main()
