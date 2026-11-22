"""The email's itemised quote must add up exactly to the total it quotes (the ask)."""

import re
import unittest

from my_actor.counter_email import build_payload, format_money
from my_actor.pricing import Metrics, Terms, evaluate_deal, load_rates

RATES = load_rates()


def payload(currency='USD', fx=1.0, step=10, deliverables=None, **terms):
    m = Metrics(platform='instagram', audience=85_000, median_views={'instagram_reel': 42_000},
                engagement_rate={'instagram_reel': 0.035}, sample_size={'instagram_reel': 24}, views_field='videoPlayCount')
    t = Terms(deliverables=deliverables or [{'type': 'instagram_reel', 'qty': 1}], niche='fitness', offer_amount=800, **terms)
    r = evaluate_deal(m, t, RATES)
    money = lambda usd: format_money(usd, currency, fx, step)  # noqa: E731
    return build_payload(r, {'money': money, 'handle': 'x', 'platform': 'instagram'})


def total_of(p):
    n = lambda s: int(re.sub(r'\D', '', s)) * (-1 if s.startswith('-') else 1)  # noqa: E731
    return sum(n(li['price']) for li in p['line_items'] if li['price'] != 'included'), n(p['total_quote'])


class QuoteAddsUp(unittest.TestCase):
    def test_demo_deal_usd(self):
        p = payload(organic_usage_days=90, whitelisting_days=30, exclusivity_days=180)
        s, total = total_of(p)
        self.assertEqual(s, total)
        self.assertEqual(p['total_quote'], '$3,490')

    def test_with_package_discount(self):
        p = payload(deliverables=[{'type': 'instagram_reel', 'qty': 1}, {'type': 'instagram_story_frame', 'qty': 3}], organic_usage_days=30)
        self.assertEqual(*total_of(p))

    def test_inr(self):
        p = payload(currency='INR', fx=93.5, step=500, organic_usage_days=90, whitelisting_days=30, exclusivity_days=180)
        self.assertEqual(*total_of(p))


if __name__ == '__main__':
    unittest.main()
