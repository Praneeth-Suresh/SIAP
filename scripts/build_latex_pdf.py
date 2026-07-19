#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
DIST_DIR = ROOT / "dist"
LATEX_HEADER_PATH = ROOT / "templates" / "latex-header.tex"
TITLE = "Structure and Interpretation of Agentic Patterns"
AUTHOR = "Prane"
PANDOC_MARKDOWN = (
    "markdown+tex_math_dollars+tex_math_single_backslash+"
    "fenced_code_blocks+pipe_tables+header_attributes+bracketed_spans"
)


def rewrite_reference_links(markdown_text: str) -> str:
    # Convert relative links to references.md anchors into in-document anchors.
    pattern = re.compile(r"\]\((?:[^)#]*/)*references\.md(#[^)]+)\)")
    return pattern.sub(lambda m: f"]({m.group(1)})", markdown_text)


def pandoc_heading_id(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"`([^`]*)`", r"\1", slug)
    slug = re.sub(r"\\\((.*?)\\\)", r"\1", slug)
    slug = re.sub(r"[^a-z0-9 _-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "section"


def extract_title(markdown_path: Path, fallback: str) -> str:
    for line in markdown_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            return re.sub(r"^Chapter \d+:\s*", "", title)
    return fallback


def rewrite_local_markdown_links(section: Path, markdown_text: str) -> str:
    pattern = re.compile(r"\[([^\]]+)\]\((?!#)(?:[^)]+)\.md(?:#[^)]+)?\)")

    def repl(match: re.Match[str]) -> str:
        label = match.group(1)
        link_text = match.group(0)
        raw_target = link_text.split("](", 1)[1][:-1]
        target_without_anchor = raw_target.split("#", 1)[0]
        target_path = (section.parent / target_without_anchor).resolve()
        try:
            target_path.relative_to(BOOK_DIR.resolve())
        except ValueError:
            return label
        if not target_path.exists():
            return label
        title = extract_title(target_path, label)
        return f"[{label}](#{pandoc_heading_id(title)})"

    return pattern.sub(repl, markdown_text)


def gather_book_sections() -> list[tuple[Path, str]]:
    sections: list[tuple[Path, str]] = [(BOOK_DIR / "index.md", "preface")]
    for chapter_index in sorted((BOOK_DIR / "chapters").glob("*/index.md")):
        chapter_dir = chapter_index.parent
        sections.append((chapter_index, "chapter"))
        for topic_path in sorted(chapter_dir.glob("topic-*.md")):
            if not topic_path.name.endswith("-notes.md"):
                sections.append((topic_path, "topic"))
    sections.append((BOOK_DIR / "references.md", "references"))
    return sections


def demote_headings(markdown_text: str, levels: int = 1) -> str:
    def repl(match: re.Match[str]) -> str:
        hashes = match.group(1)
        return f"{hashes}{'#' * levels} "

    return re.sub(r"^(#{1,5}) ", repl, markdown_text, flags=re.MULTILINE)


def autolink_bare_urls(markdown_text: str) -> str:
    return re.sub(r"(?<![<(])(https?://[^\s>)]+)", r"<\1>", markdown_text)


def remove_markdown_section(markdown_text: str, level: int, title: str) -> str:
    hashes = "#" * level
    pattern = re.compile(
        rf"^{re.escape(hashes)} {re.escape(title)}\n.*?(?=^{'#' * level} |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", markdown_text).strip() + "\n"


def prepare_book_markdown(section: Path, section_kind: str) -> str:
    text = rewrite_reference_links(section.read_text(encoding="utf-8"))
    text = rewrite_local_markdown_links(section, text)

    if section_kind == "preface":
        text = text.replace("This draft is organized", "This book is organized")
        text = remove_markdown_section(text, 2, "Chapter map")
        text = remove_markdown_section(text, 2, "How to read this draft")
        text = re.sub(r"^## Throughline\n+", "", text, count=1, flags=re.MULTILINE)
        text = re.sub(
            r"^# .+$",
            "# Preface {-}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    elif section_kind == "chapter":
        text = remove_markdown_section(text, 2, "Topics")
        text = re.sub(
            r"^# Chapter \d+:\s*",
            "# ",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    elif section_kind == "topic":
        text = demote_headings(text, levels=1)
    elif section_kind == "references":
        text = re.sub(
            r"^# References$",
            "# References {-}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
        text = autolink_bare_urls(text)

    return text


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
    for section, _section_kind in sections:
        if not section.exists():
            raise SystemExit(f"Missing source section: {section}")

    pandoc_bin = require_binary("pandoc", "Install with: sudo apt-get install pandoc")
    pdf_engine = choose_pdf_engine()

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    merged_chunks = []
    for section, section_kind in sections:
        merged_chunks.append(prepare_book_markdown(section, section_kind))

    merged_markdown = "\n\n".join(merged_chunks)
    merged_md_path = DIST_DIR / "book-latex.md"
    tex_path = DIST_DIR / "book.tex"
    pdf_path = DIST_DIR / "book-latex.pdf"
    merged_md_path.write_text(merged_markdown, encoding="utf-8")

    common_args = [
        str(merged_md_path),
        "--from",
        PANDOC_MARKDOWN,
        "--standalone",
        "--toc",
        "--toc-depth",
        "2",
        "--number-sections",
        "--top-level-division=chapter",
        "--metadata",
        f"title={TITLE}",
        "--metadata",
        f"author={AUTHOR}",
        "--variable",
        "documentclass=book",
        "--variable",
        "geometry:margin=1in",
        "--include-in-header",
        str(LATEX_HEADER_PATH),
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
