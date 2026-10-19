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

    def test_metadata_does_not_drop_zero(self):
        self.assertEqual(audit.plain(0), '0')


if __name__ == '__main__':
    unittest.main()
