from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_site  # noqa: E402


class SiteManifestTests(unittest.TestCase):
    def test_reader_manifest_has_only_published_book_pages_in_reading_order(self) -> None:
        sections = build_site.discover_publication_sections()
        files = [section.path for section in sections]

        self.assertEqual(len(files), 23)
        self.assertEqual(files[0], ROOT / "book/index.md")
        self.assertEqual(files[1], ROOT / "book/parts/00-system-in-action.md")
        self.assertEqual(files[-1], ROOT / "book/references.md")
        self.assertTrue(all(not path.name.endswith("-notes.md") for path in files))
        self.assertEqual(
            [path.name for path in files[2:7]],
            [
                "index.md",
                "topic-01-goals-environments-actions.md",
                "topic-02-belief-uncertainty-and-decision.md",
                "topic-03-world-models-and-state-abstractions.md",
                "topic-04-policies-value-and-control.md",
            ],
        )

    def test_navigation_uses_hierarchy_and_reader_routes(self) -> None:
        sections = build_site.discover_publication_sections()
        current = sections[4]

        nav = build_site.render_nav(sections, current)
        breadcrumbs = build_site.render_breadcrumbs(sections, current)
        reading_nav = build_site.render_reading_nav(sections, current)

        self.assertIn('class="book-nav__chapter"', nav)
        self.assertIn('class="book-nav__part"', nav)
        self.assertIn("Part 0: The System in Action", nav)
        self.assertIn("Chapter 1: Foundations of Agency", nav)
        self.assertIn('aria-current="page">Belief, Uncertainty, and Decision', nav)
        self.assertNotIn("-notes", nav)
        self.assertIn("Book", breadcrumbs)
        self.assertIn("Chapter 1: Foundations of Agency", breadcrumbs)
        self.assertIn("Previous", reading_nav)
        self.assertIn("Next", reading_nav)

    def test_semantic_kinds_control_site_hierarchy_not_path_names(self) -> None:
        published = build_site.discover_publication_sections()
        sections = (
            published[0],
            replace(published[1], kind="chapter"),
            replace(published[2], kind="topic"),
            published[-1],
        )
        current = sections[2]

        nav = build_site.render_nav(sections, current)
        breadcrumbs = build_site.render_breadcrumbs(sections, current)
        reading_nav = build_site.render_reading_nav(sections, current)

        self.assertNotIn('class="book-nav__part"', nav)
        self.assertIn('class="book-nav__chapter"', nav)
        self.assertIn("Part 0: The System in Action", breadcrumbs)
        self.assertIn("Chapter", reading_nav)
        self.assertIn("Part 0: The System in Action", reading_nav)

    def test_rendered_page_loads_mathjax_and_relative_assets(self) -> None:
        sections = build_site.discover_publication_sections()
        template = (ROOT / "templates/page.html").read_text(encoding="utf-8")
        current = sections[3]
        original_site_dir = build_site.SITE_DIR

        try:
            build_site.SITE_DIR = ROOT / "tmp-test-site"
            build_site.write_html_page(current, sections, template)
            page = (build_site.SITE_DIR / "chapters/01-foundations-of-agency/topic-01-goals-environments-actions.html").read_text(encoding="utf-8")
        finally:
            build_site.SITE_DIR = original_site_dir
            if (ROOT / "tmp-test-site").exists():
                import shutil

                shutil.rmtree(ROOT / "tmp-test-site")

        self.assertIn("mathjax@3", page)
        self.assertIn('href="../../assets/style.css"', page)
        self.assertIn('class="reading-nav"', page)
        self.assertIn(r"\mathcal{M}", page)
        self.assertNotIn("SIAPMATH", page)


if __name__ == "__main__":
    unittest.main()
