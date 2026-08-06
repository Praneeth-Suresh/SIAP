from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_manuscript import audit  # noqa: E402


class ManuscriptContractTests(unittest.TestCase):
    def test_editor_mandates_are_present_in_published_source(self) -> None:
        issues, counts = audit()

        self.assertEqual(issues, [], "\n".join(issues))
        self.assertGreaterEqual(counts["unique_diagrams"], 10)
        self.assertGreaterEqual(counts["footnotes"], 12)
        self.assertGreater(counts["formulas"], 0)
        self.assertEqual(counts["quotes"], 40)


if __name__ == "__main__":
    unittest.main()
