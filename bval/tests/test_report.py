"""Tests for the agent summary and the HTML/Markdown reports. Run: python -m unittest discover -s tests"""

import unittest

from my_actor.report import agent_fields, email_digest, html_report, markdown_report, next_action


def make_item(**overrides):
    item = {
        'handle': 'priya.fit',
        'platform': 'instagram',
        'creatorName': 'Priya <script>alert(1)</script>',
        'marketName': 'Global (US benchmarks)',
        'verdict': 'COUNTER_TRADE_SCOPE',
        'verdictText': 'Offer is well below fair value.',
        'offerDisplay': '$800',
        'offerValue': 800,
        'gapPct': 71.0,
        'fairPrice': 2760, 'askPrice': 2890, 'floorPrice': 2350, 'walkAwayPrice': 1900,
        'priceRange': {'walkAway': '$1,900', 'floor': '$2,350', 'fair': '$2,760', 'ask': '$2,890'},
        'lineItems': [{'item': '1 x Instagram Reel', 'amount': '$1,000', 'sources': ['see rates.json'], 'isAssumption': False}],
        'counterOptions': {'reducedScope': {'price': '$1,180', 'dropped': ['paid_usage', 'exclusivity']}},
        'redFlags': [{'code': 'LONG_EXCLUSIVITY', 'message': 'Exclusivity beyond 7 days is worth +$1,364.'}],
        'metrics': {'audience': 85000, 'tier': 'mid', 'medianViews': 42000, 'engagementRate': 0.035, 'postsUsed': 24},
        'confidence': 'high',
        'confidenceReasons': [],
        'counterEmail': {'subject': 'Re: Acme x Priya', 'body': 'Hi Acme, thanks <b>so much</b>.'},
        'disclaimer': 'Estimates, not advice.',
        'ratesVersion': '2026-11',
        'evaluatedAt': '2026-11-22T12:00:00+00:00',
    }
    item.update(overrides)
    return item


class AgentFieldsTest(unittest.TestCase):
    def test_next_action_covers_every_verdict(self):
        self.assertEqual(next_action('ACCEPT_STRONG'), 'accept')
        self.assertEqual(next_action('ACCEPT'), 'accept')
        self.assertEqual(next_action('COUNTER_LIGHT'), 'counter')
        self.assertEqual(next_action('COUNTER_TRADE_SCOPE'), 'counter')
        self.assertEqual(next_action('DECLINE_OR_REDUCE_SCOPE'), 'decline')
        self.assertEqual(next_action('NO_OFFER'), 'quote')

    def test_counter_summary_has_prices_options_and_flags(self):
        s = agent_fields(make_item())['summary']
        self.assertIn('Counter at $2,890', s)
        self.assertIn('71% below', s)
        self.assertIn('$1,180 by dropping paid usage, exclusivity', s)
        self.assertIn('LONG_EXCLUSIVITY', s)

    def test_no_offer_summary_quotes_ask(self):
        s = agent_fields(make_item(verdict='NO_OFFER', offerDisplay=None, offerValue=None, gapPct=None, redFlags=[]))['summary']
        self.assertEqual(s, "No offer yet: quote $2,890 for this package (fair $2,760, don't go below $2,350).")

    def test_no_offer_summary_lists_packages(self):
        s = agent_fields(make_item(verdict='NO_OFFER', offerDisplay=None, offerValue=None, gapPct=None, redFlags=[], rateCard=RATE_CARD))['summary']
        self.assertIn('Ready-made packages: Starter $1,240, Premium <b>$5,170</b>.', s)


RATE_CARD = {
    'perPost': [{'type': 'instagram_reel', 'label': 'Instagram Reel', 'fair': '$990', 'ask': '$1,240'}],
    'addOns': [{'key': 'whitelisting_30', 'label': 'Ads through <your> handle, 30 days', 'adds': '+$280'}],
    'packages': [{'name': 'Starter', 'ask': '$1,240', 'fair': '$990', 'includes': ['1 x Instagram Reel']},
                 {'name': 'Premium', 'ask': '<b>$5,170</b>', 'fair': '$4,130', 'includes': ['2 x Instagram Reel']}],
}
EVIDENCE = [{'stat': 'Median views', 'value': '42,000 <i>', 'benchmark': '$20 per 1,000 views', 'claim': '42,000 / 1,000 x $20 = $840.'}]


class NoOfferAndEvidenceTest(unittest.TestCase):
    def test_rate_card_and_numbers_sections_escaped(self):
        page = html_report(make_item(verdict='NO_OFFER', offerDisplay=None, offerValue=None, gapPct=None, rateCard=RATE_CARD, evidence=EVIDENCE))
        for part in ('id="rates"', 'Price per post', 'What each extra adds', 'id="numbers"', 'Your package: price range', 'href="#rates"'):
            self.assertIn(part, page)
        self.assertNotIn('<b>$5,170</b>', page)
        self.assertNotIn('<your>', page)
        self.assertNotIn('42,000 <i>', page)

    def test_offer_run_has_numbers_but_no_rate_card(self):
        page = html_report(make_item(evidence=EVIDENCE))
        self.assertIn('id="numbers"', page)
        self.assertNotIn('id="rates"', page)
        self.assertIn('Where the offer lands', page)

    def test_markdown_has_both_tables(self):
        md = markdown_report(make_item(verdict='NO_OFFER', offerDisplay=None, offerValue=None, gapPct=None, rateCard=RATE_CARD, evidence=EVIDENCE))
        self.assertIn('## What to charge', md)
        self.assertIn('| Starter | $1,240 | $990 | 1 x Instagram Reel |', md)
        self.assertIn('## Your numbers, and what they prove', md)


class ReportTest(unittest.TestCase):
    def test_html_escapes_scraped_and_llm_text(self):
        page = html_report(make_item())
        self.assertNotIn('<script>alert(1)</script>', page)
        self.assertIn('Priya &lt;script&gt;', page)
        self.assertIn('thanks &lt;b&gt;so much&lt;/b&gt;', page)

    def test_html_has_verdict_bar_options_and_email(self):
        page = html_report(make_item())
        self.assertTrue(page.startswith('<!doctype html>'))
        for part in ('Counter or trade scope', 'class="offer"', 'Reduced scope', 'id="email"', 'prefers-color-scheme:dark'):
            self.assertIn(part, page)

    def test_html_without_offer_or_email(self):
        page = html_report(make_item(verdict='NO_OFFER', offerDisplay=None, offerValue=None, counterEmail=None, counterOptions={}))
        self.assertNotIn('class="offer"', page)
        self.assertNotIn('id="email"', page)

    def test_counter_email_comes_before_price_details(self):
        page = html_report(make_item())
        self.assertLess(page.index('id="email"'), page.index('Where the offer lands'))

    def test_email_digest(self):
        subject, html, text = email_digest(make_item(reportUrl='https://api.apify.com/v2/key-value-stores/x/records/QUOTE.html'))
        self.assertEqual(subject, 'BVAL: Counter or trade scope for @priya.fit, offer $800 (fair $2,760)')
        self.assertIn('Open the full report', html)
        self.assertIn('thanks &lt;b&gt;so much&lt;/b&gt;', html)
        self.assertNotIn('position:absolute', html)
        self.assertIn('Subject: Re: Acme x Priya', text)
        self.assertIn('Full report: https://', text)

    def test_email_digest_skips_local_file_link(self):
        _, html, text = email_digest(make_item(reportUrl='file:///tmp/QUOTE.html', counterEmail=None))
        self.assertNotIn('Open the full report', html)
        self.assertNotIn('counter-offer email', html)
        self.assertNotIn('Full report', text)

    def test_markdown_unchanged_shape(self):
        md = markdown_report(make_item())
        self.assertIn('# BVAL deal check: @priya.fit (instagram)', md)
        self.assertIn('## Counter-offer email', md)


if __name__ == '__main__':
    unittest.main()


class DesignedCounterEmailTest(unittest.TestCase):
    BODY = ("Hi Acme team,\n\nThanks for reaching out <b>!</b>\n\nHere's the breakdown:\n- 1 x Instagram Reel: $1,240\n"
            "- Category exclusivity, 180 days: $1,700\n\nA few notes:\n- Exclusivity is priced as its own line.\n\nBest,\nPriya")

    def test_quote_lines_become_a_card_and_notes_a_list(self):
        from my_actor.report import counter_email_html
        subject, html, text = counter_email_html(make_item(counterEmail={'subject': 'Re: Acme x Priya', 'body': self.BODY}))
        self.assertEqual(subject, 'Re: Acme x Priya')
        self.assertIn('Itemised quote', html)
        self.assertIn('$1,240', html)
        self.assertIn('<li style="margin:0 0 6px">Exclusivity is priced as its own line.</li>', html)
        self.assertIn('Best,<br>Priya', html)
        self.assertNotIn('<b>!</b>', html)  # escaped
        self.assertNotIn('<script>', html)  # creatorName from make_item is hostile
        self.assertNotIn('BVAL', html)  # brand-facing: never reveal the tool
        self.assertTrue(text.startswith('Subject: Re: Acme x Priya'))

    def test_no_email_no_designed_version(self):
        from my_actor.report import counter_email_html
        self.assertIsNone(counter_email_html(make_item(counterEmail=None)))

    def test_report_links_designed_email_only_with_a_real_url(self):
        self.assertIn('Open it as a designed email', html_report(make_item(counterEmailUrl='https://x/COUNTER_EMAIL.html')))
        self.assertNotIn('Open it as a designed email', html_report(make_item(counterEmailUrl='file:///tmp/x')))
