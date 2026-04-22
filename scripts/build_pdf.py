#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import shutil

import markdown


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
DIST_DIR = ROOT / "dist"
CSS_PATH = BOOK_DIR / "assets" / "style.css"
MD_EXTENSIONS = ["extra", "tables", "fenced_code", "toc"]


def rewrite_md_links(markdown_text: str) -> str:
    pattern = re.compile(r"\]\(([^)#]+)\.md(#[^)]+)?\)")
    return pattern.sub(lambda m: f"]({m.group(1)}.html{m.group(2) or ''})", markdown_text)


def gather_book_sections() -> list[Path]:
    chapter_indexes = sorted((BOOK_DIR / "chapters").glob("*/index.md"))
    topic_files = sorted(
        p
        for p in (BOOK_DIR / "chapters").glob("*/*.md")
        if p.name != "index.md" and not p.name.endswith("-notes.md")
    )
    return [BOOK_DIR / "index.md", *chapter_indexes, *topic_files, BOOK_DIR / "references.md"]


def main() -> None:
    sections = gather_book_sections()
    for section in sections:
        if not section.exists():
            raise SystemExit(f"Missing source section: {section}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    chunks = []
    for section in sections:
        text = rewrite_md_links(section.read_text(encoding="utf-8"))
        chunks.append(text)

    merged_markdown = "\n\n---\n\n".join(chunks)
    body_html = markdown.markdown(merged_markdown, extensions=MD_EXTENSIONS)
    css_text = CSS_PATH.read_text(encoding="utf-8")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Structure and Interpretation of Agentic Patterns</title>
  <style>{css_text}</style>
</head>
<body>
  <article class="content pdf-content">
  {body_html}
  </article>
</body>
</html>
"""
    html_path = DIST_DIR / "book.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"Wrote {html_path}")

    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise SystemExit(
            "PDF generation requires weasyprint. Install requirements and system libs first."
        ) from exc

    pdf_path = DIST_DIR / "book.pdf"
    HTML(string=html, base_url=str(ROOT)).write_pdf(str(pdf_path))
    print(f"Wrote {pdf_path}")

    # Copy style for external HTML consumers.
    shutil.copy2(CSS_PATH, DIST_DIR / "book.css")


if __name__ == "__main__":
    main()
