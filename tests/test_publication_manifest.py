from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from publication_manifest import load_publication_manifest  # noqa: E402
import build_latex_pdf  # noqa: E402


class PublicationManifestTests(unittest.TestCase):
    def test_part_zero_precedes_theory_and_revision_notes_are_excluded(self) -> None:
        sections = load_publication_manifest(ROOT / "book")

        self.assertEqual(sections[0].source, "index.md")
        self.assertEqual(sections[1].source, "parts/00-system-in-action.md")
        self.assertEqual(sections[1].kind, "part")
        self.assertEqual(sections[2].kind, "chapter")
        self.assertEqual(sections[-1].source, "references.md")
        self.assertEqual(sum(section.kind == "chapter" for section in sections), 4)
        self.assertTrue(all(not section.source.endswith("-notes.md") for section in sections))
        self.assertTrue(all(section.source != "continuity-ledger.md" for section in sections))

    def test_latex_rewrites_part_diagram_to_repository_relative_asset(self) -> None:
        source = ROOT / "book/parts/00-system-in-action.md"
        prepared = build_latex_pdf.prepare_book_markdown(source, "part")

        self.assertIn("(book/assets/diagrams/01-publication-institution.png)", prepared)
        self.assertNotIn("(../assets/diagrams/", prepared)

    def test_latex_keeps_chapter_terminal_enrichment_after_removing_topic_list(self) -> None:
        source = ROOT / "book/chapters/01-foundations-of-agency/index.md"
        enrichment = build_latex_pdf.load_publication_enrichment(ROOT / "book")

        prepared = build_latex_pdf.prepare_book_markdown(source, "chapter", enrichment)

        self.assertIn("03-ch01-foundations.png", prepared)
        self.assertIn(r"\siapepigraphbegin", prepared)
        self.assertNotIn("## Topics", prepared)


if __name__ == "__main__":
    unittest.main()
