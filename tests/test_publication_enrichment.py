from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_site  # noqa: E402
from publication_enrichment import (  # noqa: E402
    adapt_semantic_divs,
    enrich_section_markdown,
    load_publication_enrichment,
)


class PublicationEnrichmentTests(unittest.TestCase):
    def test_quotes_and_terminal_cartoon_are_injected_at_semantic_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            book_dir = Path(temporary)
            section = book_dir / "chapters" / "topic.md"
            section.parent.mkdir(parents=True)
            section.write_text(
                textwrap.dedent(
                    """\
                    # A Topic

                    Body.

                    [^one]: A terminal footnote.
                    """
                ),
                encoding="utf-8",
            )
            (book_dir / "assets" / "cartoons").mkdir(parents=True)
            (book_dir / "assets" / "cartoons" / "topic.png").write_bytes(b"placeholder")
            (book_dir / "quotes.toml").write_text(
                textwrap.dedent(
                    """\
                    schema_version = 1
                    strict = false

                    [[quotes]]
                    id = "opening"
                    source = "chapters/topic.md"
                    text = "Begin with doubt."
                    speaker = "Ada"
                    work = "Notes"
                    year = "1843"
                    locator = "p. 1"
                    url = "https://example.test/opening"
                    accessed = "2026-08-06"
                    rights = "Public domain"
                    placement = "opening"

                    [[quotes]]
                    id = "closing"
                    source = "chapters/topic.md"
                    text = "End with evidence."
                    speaker = "Grace"
                    work = "Lecture"
                    year = "1952"
                    locator = "p. 2"
                    url = "https://example.test/closing"
                    accessed = "2026-08-06"
                    rights = "Used by permission"
                    placement = "closing"
                    """
                ),
                encoding="utf-8",
            )
            (book_dir / "visuals.toml").write_text(
                textwrap.dedent(
                    """\
                    schema_version = 1
                    strict = false

                    [[visuals]]
                    id = "topic-cartoon"
                    source = "chapters/topic.md"
                    kind = "cartoon"
                    path = "assets/cartoons/topic.png"
                    placement = "terminal"
                    alt = "A terminal cartoon."
                    width = 1200
                    height = 700
                    content_bbox = [60, 50, 1140, 650]
                    min_padding = 40
                    """
                ),
                encoding="utf-8",
            )

            enrichment = load_publication_enrichment(book_dir)
            rendered = enrich_section_markdown(
                section,
                section.read_text(encoding="utf-8"),
                enrichment,
            )

            self.assertLess(rendered.index("Begin with doubt."), rendered.index("Body."))
            self.assertLess(rendered.index("End with evidence."), rendered.index("topic.png"))
            self.assertLess(rendered.index("[^one]:"), rendered.index("topic.png"))
            self.assertIn("../assets/cartoons/topic.png", rendered)
            self.assertIn("::: {.epigraph .epigraph--opening}", rendered)
            self.assertNotIn("accessed 2026-08-06", rendered)

    def test_semantic_divs_render_as_html_sections_and_unnumbered_latex(self) -> None:
        source = textwrap.dedent(
            """\
            ::: {.exercise}
            ## Exercise: Break It

            Write code.
            :::

            ::: {.reader-question}
            ## Why does it fail? {.provocation}

            Because state leaked.
            :::

            ::: {.epigraph .epigraph--opening}
            > *“A compact thought.”*
            >
            > — A Human, *A Work* (1900), page 1.
            :::
            """
        )

        html_markdown = adapt_semantic_divs(source, target="html")
        html = build_site.render_markdown(source)
        latex_markdown = adapt_semantic_divs(source, target="latex")

        self.assertIn('<section class="exercise" markdown="1">', html_markdown)
        self.assertIn('<section class="reader-question" markdown="1">', html_markdown)
        self.assertIn('<section class="epigraph epigraph--opening" markdown="1">', html_markdown)
        self.assertIn('<section class="exercise">', html)
        self.assertIn(">Exercise: Break It</h2>", html)
        self.assertIn(r"\siapexercisebegin", latex_markdown)
        self.assertIn(r"\siapreaderquestionbegin", latex_markdown)
        self.assertIn(r"\siapepigraphbegin", latex_markdown)
        self.assertIn("## Exercise: Break It {.unnumbered}", latex_markdown)
        self.assertIn("## Why does it fail? {.provocation .unnumbered}", latex_markdown)

    def test_missing_quote_field_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            book_dir = Path(temporary)
            (book_dir / "quotes.toml").write_text(
                "schema_version = 1\nstrict = false\n[[quotes]]\nid = 'bad'\nsource = 'index.md'\n",
                encoding="utf-8",
            )
            (book_dir / "visuals.toml").write_text(
                "schema_version = 1\nstrict = false\nvisuals = []\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "quote record 1 is missing"):
                load_publication_enrichment(book_dir)


if __name__ == "__main__":
    unittest.main()
