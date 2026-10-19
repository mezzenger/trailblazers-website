"""Regression tests for Wikimedia Commons metadata normalization (no network)."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'audit_commons_provenance', ROOT / 'scripts/audit_commons_provenance.py'
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class CommonsMetadataTests(unittest.TestCase):
    def test_float_metadata(self):
        self.assertEqual(audit.plain(1.25), '1.25')

    def test_integer_metadata(self):
        self.assertEqual(audit.plain(12), '12')

    def test_null_and_empty_metadata(self):
        self.assertEqual(audit.plain(None), '')
        self.assertEqual(audit.plain(''), '')

    def test_html_metadata(self):
        self.assertEqual(audit.plain('<b>CC BY-SA</b> &amp; 4.0'), 'CC BY-SA & 4.0')

    def test_special_non_cc_license_families(self):
        self.assertEqual(audit.license_family('Government Open Data License – India (GODL)'), 'godl-india')
        self.assertEqual(audit.license_family('GODL-India'), 'godl-india')
        self.assertEqual(audit.license_family('Attribution-only license — author permits reuse'), 'attribution-only')
        self.assertEqual(audit.license_family('Attribution'), 'attribution-only')

    def test_explicit_licenses_remain_distinct(self):
        self.assertEqual(audit.license_family('CC BY-SA 3.0'), 'by-sa')
        self.assertEqual(audit.license_family('CC BY 2.5'), 'by')
        self.assertEqual(audit.license_family('Public domain in the United States'), 'pd')

    def test_metadata_does_not_drop_zero(self):
        self.assertEqual(audit.plain(0), '0')


if __name__ == '__main__':
    unittest.main()
