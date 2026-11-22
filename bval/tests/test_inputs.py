"""Grouped input form -> flat fields, and backward compatibility with the earlier flat input."""

import json
import unittest
from pathlib import Path

from my_actor.inputs import normalize_input
from my_actor.main import build_terms
from my_actor.pricing import load_rates, resolve_market

RATES = load_rates()
MARKET = resolve_market('GLOBAL', RATES)
SCHEMA = json.loads((Path(__file__).parent.parent / '.actor' / 'input_schema.json').read_text())

GROUPED = {
    'platform': 'instagram',
    'handle': ' @fitcreator ',
    'niche': 'fitness',
    'offer': {'brandName': 'Acme Protein', 'amount': 800, 'currency': 'USD'},
    'deliverables': [{'type': 'instagram_reel', 'qty': 1}, {'type': 'instagram_story_frame'}, {}],
    'rights': {'organicUsageDays': 90, 'whitelistingDays': 30, 'exclusivityDays': 180, 'exclusivityScope': 'category'},
    'extras': {'rushHours': 48, 'revisionRounds': 2},
    'contract': {'paymentTermsDays': 90, 'depositPct': 0},
}

FLAT = {
    'platform': 'instagram',
    'handle': '@fitcreator',
    'niche': 'fitness',
    'brandName': 'Acme Protein',
    'offerAmount': 800,
    'offerCurrency': 'USD',
    'deliverables': [{'type': 'instagram_reel', 'qty': 1}, {'type': 'instagram_story_frame', 'qty': 1}],
    'organicUsageDays': 90,
    'whitelistingDays': 30,
    'exclusivityDays': 180,
    'exclusivityScope': 'category',
    'rushHours': 48,
    'revisionRounds': 2,
    'paymentTermsDays': 90,
    'depositPct': 0,
}


class Normalize(unittest.TestCase):
    def test_grouped_and_flat_give_identical_terms(self):
        self.assertEqual(build_terms(normalize_input(GROUPED), MARKET), build_terms(normalize_input(FLAT), MARKET))

    def test_values_land_on_flat_names(self):
        n = normalize_input(GROUPED)
        self.assertEqual(n['offerAmount'], 800)
        self.assertEqual(n['brandName'], 'Acme Protein')
        self.assertEqual(n['whitelistingDays'], 30)
        self.assertEqual(n['depositPct'], 0)  # a real 0 must survive
        self.assertEqual(n['handle'], '@fitcreator')

    def test_empty_deliverable_rows_dropped_and_qty_defaulted(self):
        n = normalize_input(GROUPED)
        self.assertEqual(n['deliverables'], [{'type': 'instagram_reel', 'qty': 1}, {'type': 'instagram_story_frame', 'qty': 1}])

    def test_grouped_wins_over_flat(self):
        n = normalize_input({'offerAmount': 500, 'offer': {'amount': 900}})
        self.assertEqual(n['offerAmount'], 900)

    def test_minimal_input(self):
        n = normalize_input({'platform': 'tiktok', 'handle': 'creator'})
        t = build_terms(n, MARKET)
        self.assertEqual(t.deliverables, [{'type': 'tiktok_video', 'qty': 1}])
        self.assertIsNone(t.offer_amount)

    def test_none_input(self):
        self.assertEqual(normalize_input(None), {})


class SchemaShape(unittest.TestCase):
    def test_only_platform_and_handle_required(self):
        self.assertEqual(SCHEMA['required'], ['platform', 'handle'])

    def test_every_field_is_self_explanatory(self):
        def check(name, p):
            self.assertTrue(p.get('title'), f'{name} has no title')
            self.assertTrue(p.get('description'), f'{name} has no description')
            for sub, sp in (p.get('properties') or {}).items():
                check(f'{name}.{sub}', sp)
            for sub, sp in ((p.get('items') or {}).get('properties') or {}).items():
                check(f'{name}[].{sub}', sp)

        for name, p in SCHEMA['properties'].items():
            check(name, p)

    def test_group_fields_match_normalizer(self):
        from my_actor.inputs import GROUPS

        for group, mapping in GROUPS.items():
            self.assertEqual(set(SCHEMA['properties'][group]['properties']), set(mapping), group)

    def test_send_report_to_kept(self):
        self.assertIn('sendReportTo', SCHEMA['properties'])
        self.assertIn('only delivers to your own', SCHEMA['properties']['sendReportTo']['description'])


if __name__ == '__main__':
    unittest.main()
