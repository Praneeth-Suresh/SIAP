#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
DIST_DIR = ROOT / "dist"
TITLE = "Structure and Interpretation of Agentic Patterns"


def rewrite_reference_links(markdown_text: str) -> str:
    # Convert relative links to references.md anchors into in-document anchors.
    pattern = re.compile(r"\]\((?:[^)#]*/)*references\.md(#[^)]+)\)")
    return pattern.sub(lambda m: f"]({m.group(1)})", markdown_text)


def gather_book_sections() -> list[Path]:
    chapter_indexes = sorted((BOOK_DIR / "chapters").glob("*/index.md"))
    topic_files = sorted(
        p
        for p in (BOOK_DIR / "chapters").glob("*/*.md")
        if p.name != "index.md" and not p.name.endswith("-notes.md")
    )
    return [BOOK_DIR / "index.md", *chapter_indexes, *topic_files, BOOK_DIR / "references.md"]


def require_binary(name: str, install_hint: str) -> str:
    binary = shutil.which(name)
    if binary is None:
        raise SystemExit(f"Missing required binary '{name}'. {install_hint}")
    return binary


def choose_pdf_engine() -> str:
    for engine in ("tectonic", "xelatex", "lualatex", "pdflatex"):
        if shutil.which(engine):
            return engine
    raise SystemExit(
        "No LaTeX PDF engine found. Install one of: tectonic, xelatex, lualatex, pdflatex."
    )


def run_pandoc(pandoc_bin: str, args: list[str]) -> None:
    cmd = [pandoc_bin, *args]
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    if result.returncode != 0:
        raise SystemExit(f"pandoc failed with exit code {result.returncode}: {' '.join(cmd)}")


def main() -> None:
    sections = gather_book_sections()
    for section in sections:
        if not section.exists():
            raise SystemExit(f"Missing source section: {section}")

    pandoc_bin = require_binary("pandoc", "Install with: sudo apt-get install pandoc")
    pdf_engine = choose_pdf_engine()

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    merged_chunks = []
    for section in sections:
        text = rewrite_reference_links(section.read_text(encoding="utf-8"))
        merged_chunks.append(text)

    merged_markdown = "\n\n---\n\n".join(merged_chunks)
    merged_md_path = DIST_DIR / "book-latex.md"
    tex_path = DIST_DIR / "book.tex"
    pdf_path = DIST_DIR / "book-latex.pdf"
    merged_md_path.write_text(merged_markdown, encoding="utf-8")

    common_args = [
        str(merged_md_path),
        "--from",
        "markdown+tex_math_dollars+tex_math_single_backslash+fenced_code_blocks+pipe_tables",
        "--standalone",
        "--toc",
        "--number-sections",
        "--metadata",
        f"title={TITLE}",
    ]

    run_pandoc(
        pandoc_bin,
        [*common_args, "--to", "latex", "-o", str(tex_path)],
    )
    print(f"Wrote {tex_path}")

    run_pandoc(
        pandoc_bin,
        [*common_args, "--pdf-engine", pdf_engine, "-o", str(pdf_path)],
    )
    print(f"Wrote {pdf_path} (engine: {pdf_engine})")


if __name__ == "__main__":
    main()
