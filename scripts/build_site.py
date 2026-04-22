#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
import re
import shutil

import markdown


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
SITE_DIR = ROOT / "site"
TEMPLATE_PATH = ROOT / "templates" / "page.html"
MD_EXTENSIONS = ["extra", "tables", "fenced_code", "toc"]


def discover_markdown_files() -> list[Path]:
    return sorted(BOOK_DIR.rglob("*.md"))


def extract_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def rewrite_md_links(markdown_text: str) -> str:
    pattern = re.compile(r"\]\(([^)#]+)\.md(#[^)]+)?\)")

    def repl(match: re.Match[str]) -> str:
        base = match.group(1)
        anchor = match.group(2) or ""
        return f"]({base}.html{anchor})"

    return pattern.sub(repl, markdown_text)


def render_nav(files: list[Path], current: Path) -> str:
    items = []
    for file_path in files:
        relative = file_path.relative_to(BOOK_DIR)
        html_rel = relative.with_suffix(".html")
        depth = len(current.relative_to(BOOK_DIR).parents) - 1
        prefix = "../" * depth
        href = f"{prefix}{html_rel.as_posix()}"
        label = relative.as_posix().replace(".md", "")
        active = " class=\"active\"" if file_path == current else ""
        items.append(f"<a{active} href=\"{escape(href)}\">{escape(label)}</a>")
    return "".join(f"<div>{item}</div>" for item in items)


def write_html_page(markdown_path: Path, all_files: list[Path], template: str) -> None:
    raw_md = markdown_path.read_text(encoding="utf-8")
    processed_md = rewrite_md_links(raw_md)
    title = extract_title(processed_md, markdown_path.stem)
    html_body = markdown.markdown(processed_md, extensions=MD_EXTENSIONS)

    relative = markdown_path.relative_to(BOOK_DIR)
    target = SITE_DIR / relative.with_suffix(".html")
    target.parent.mkdir(parents=True, exist_ok=True)

    depth = len(relative.parents) - 1
    prefix = "../" * depth
    css_path = f"{prefix}assets/style.css"
    home_path = f"{prefix}index.html"

    page = template.format(
        title=escape(title),
        css_path=css_path,
        home_path=home_path,
        nav=render_nav(all_files, markdown_path),
        content=html_body,
        updated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
    target.write_text(page, encoding="utf-8")


def main() -> None:
    if not BOOK_DIR.exists():
        raise SystemExit("Missing book/ directory")

    files = discover_markdown_files()
    if not files:
        raise SystemExit("No markdown files found under book/")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    for markdown_path in files:
        write_html_page(markdown_path, files, template)

    assets_source = BOOK_DIR / "assets"
    if assets_source.exists():
        shutil.copytree(assets_source, SITE_DIR / "assets", dirs_exist_ok=True)

    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(files)} pages in {SITE_DIR}")


if __name__ == "__main__":
    main()
