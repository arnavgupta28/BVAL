"""Tests for the no-offer rate card and the evidence (stats + claims). Run: python -m unittest discover -s tests"""

import unittest

from my_actor.counter_email import format_money
from my_actor.evidence import build_evidence
from my_actor.inputs import normalize_input
from my_actor.pricing import Metrics, Terms, evaluate_deal, load_rates, resolve_market
from my_actor.rate_card import build_rate_card

RATES = load_rates()
money = lambda usd: format_money(usd, 'USD', 1, 10)  # noqa: E731
exact = lambda usd: round(usd, 2)  # noqa: E731


def ig():
    return Metrics('instagram', 85_000, {'instagram_reel': 42_000}, {'instagram_reel': 0.035}, {'instagram_reel': 24})


def reel_terms(**kw):
    return Terms(deliverables=[{'type': 'instagram_reel', 'qty': 1}], niche='fitness', **kw)


class RateCardTest(unittest.TestCase):
    def test_single_reel_matches_main_engine(self):
        rc = build_rate_card(ig(), reel_terms(), RATES, money, exact)
        fair = evaluate_deal(ig(), reel_terms(), RATES)['pricePointsUsd']['fair']
        reel = next(r for r in rc['perPost'] if r['type'] == 'instagram_reel')
        self.assertEqual(reel['fair'], money(fair))
        self.assertEqual(rc['packages'][0]['name'], 'Starter')
        self.assertEqual(rc['packages'][0]['fair'], money(fair))

    def test_packages_grow_and_ignore_the_users_rights(self):
        # The user's own package (180 days exclusivity) must not leak into the recommendations.
        rc = build_rate_card(ig(), reel_terms(exclusivity_days=180, offer_amount=800), RATES, money, exact)
        values = [p['fairValue'] for p in rc['packages']]
        self.assertEqual([p['name'] for p in rc['packages']], ['Starter', 'Standard', 'Premium'])
        self.assertEqual(values, sorted(values))
        self.assertIn('30 days category exclusivity', rc['packages'][2]['includes'])

    def test_platform_rules_respected(self):
        yt = Metrics('youtube', 120_000, {'youtube_integration': 30_000}, {'youtube_integration': 0.04}, {'youtube_integration': 20})
        rc = build_rate_card(yt, Terms(deliverables=[{'type': 'youtube_integration', 'qty': 1}]), RATES, money, exact)
        keys = {a['key'] for a in rc['addOns']}
        self.assertNotIn('whitelisting_30', keys)  # not applicable on YouTube
        self.assertNotIn('youtube_short', {r['type'] for r in rc['perPost']})  # no Shorts views: left out, not guessed
        self.assertIn('brand ads for 30 days', rc['packages'][2]['includes'])


class EvidenceTest(unittest.TestCase):
    def test_claims_follow_the_engine(self):
        r = evaluate_deal(ig(), reel_terms(), RATES)
        ev = build_evidence(r['scope']['units'][0], ig(), {'postsUsed': 24, 'sponsoredPostsInSample': 2}, r['tier'], RATES,
                            resolve_market('GLOBAL', RATES, 'instagram'), 'fitness', money)
        by = {e['stat']: e for e in ev}
        self.assertIn('42,000 / 1,000 x $20 = $840', by['Median views']['claim'])
        self.assertIn('Within the typical range', by['Engagement']['claim'])
        self.assertIn('x 1.10', by['Niche']['claim'])
        self.assertEqual(by['Result']['value'], f"{money(r['pricePointsUsd']['fair'])} per Instagram Reel")
        self.assertEqual(ev[-1]['stat'], 'Result')


class NoOfferInputTest(unittest.TestCase):
    def test_grouped_no_offer_flag_is_flattened(self):
        inp = normalize_input({'platform': 'instagram', 'handle': 'x', 'offer': {'noOffer': True, 'amount': 800}})
        self.assertTrue(inp['noOffer'])
        self.assertEqual(inp['offerAmount'], 800)  # kept, but build_terms ignores it when noOffer is set


if __name__ == '__main__':
    unittest.main()
