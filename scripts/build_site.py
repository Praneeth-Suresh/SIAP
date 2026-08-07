#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import posixpath
import re
import shutil
from urllib.parse import unquote, urlsplit

import markdown
from publication_enrichment import (
    PublicationEnrichment,
    adapt_semantic_divs,
    enrich_section_markdown,
    load_publication_enrichment,
)
from publication_manifest import PublicationSection, load_publication_manifest


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
SITE_DIR = ROOT / "site"
TEMPLATE_PATH = ROOT / "templates" / "page.html"
MD_EXTENSIONS = ["extra", "tables", "fenced_code", "toc"]
MATH_PATTERN = re.compile(r"\\\[(.*?)\\\]|\\\((.*?)\\\)|\$\$(.*?)\$\$", re.DOTALL)
REFERENCE_ANCHOR_PATTERN = re.compile(r"\[\]\{#(ref-[A-Za-z0-9_-]+)\}")


class PageLinks(HTMLParser):
    """Collect generated page anchors and same-site links without a browser."""

    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])


def discover_publication_sections() -> tuple[PublicationSection, ...]:
    """Return the reader-facing book in its intended reading order.

    Revision companions are deliberately absent: they support the manuscript
    workflow, but they are not chapters a reader should have to navigate.
    """
    return load_publication_manifest(BOOK_DIR)


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


def render_markdown(markdown_text: str) -> str:
    """Render Markdown without letting its escape rules dismantle TeX syntax."""
    markdown_text = adapt_semantic_divs(markdown_text, target="html")
    markdown_text = REFERENCE_ANCHOR_PATTERN.sub(r'<span id="\1"></span>', markdown_text)
    expressions: dict[str, str] = {}

    def protect(match: re.Match[str]) -> str:
        token = f"SIAPMATH{len(expressions)}TOKEN"
        expressions[token] = match.group(0)
        return token

    protected = MATH_PATTERN.sub(protect, markdown_text)
    html_body = markdown.markdown(protected, extensions=MD_EXTENSIONS)
    for token, expression in expressions.items():
        html_body = html_body.replace(token, expression)
    return html_body


def find_broken_site_links(site_dir: Path) -> list[str]:
    """Return missing generated-page endpoints and fragment anchors."""
    pages = {path.relative_to(site_dir).as_posix(): path for path in site_dir.rglob("*.html")}
    parsed_pages: dict[str, PageLinks] = {}
    for relative, path in pages.items():
        parser = PageLinks()
        parser.feed(path.read_text(encoding="utf-8"))
        parsed_pages[relative] = parser

    failures: list[str] = []
    for current, parser in parsed_pages.items():
        for href in parser.links:
            target = urlsplit(href)
            if target.scheme or target.netloc or href.startswith("//"):
                continue
            target_path = unquote(target.path)
            relative_target = posixpath.normpath(posixpath.join(posixpath.dirname(current), target_path)) if target_path else current
            if relative_target.startswith("../") or relative_target == ".." or relative_target not in pages:
                failures.append(f"{current}: missing endpoint {href}")
                continue
            fragment = unquote(target.fragment)
            if fragment and fragment not in parsed_pages[relative_target].ids:
                failures.append(f"{current}: missing anchor {href}")
    return failures


def html_path(markdown_path: Path) -> Path:
    return markdown_path.relative_to(BOOK_DIR).with_suffix(".html")


def relative_href(current: Path, target: Path) -> str:
    return posixpath.relpath(html_path(target).as_posix(), html_path(current).parent.as_posix())


def page_label(section: PublicationSection) -> str:
    return extract_title(section.path.read_text(encoding="utf-8"), section.path.stem)


def nav_link(current: PublicationSection, target: PublicationSection, label: str) -> str:
    active = ' aria-current="page"' if current == target else ""
    return f'<a href="{escape(relative_href(current.path, target.path))}"{active}>{escape(label)}</a>'


def chapter_topics(sections: tuple[PublicationSection, ...]) -> dict[PublicationSection, list[PublicationSection]]:
    grouped: dict[PublicationSection, list[PublicationSection]] = {}
    current_chapter: PublicationSection | None = None
    for section in sections:
        if section.kind == "chapter":
            current_chapter = section
            grouped[section] = []
        elif section.kind == "topic":
            if current_chapter is None:
                raise ValueError(f"topic appears before a chapter: {section.source}")
            grouped[current_chapter].append(section)
    return grouped


def parent_chapter(sections: tuple[PublicationSection, ...], current: PublicationSection) -> PublicationSection | None:
    active: PublicationSection | None = None
    for section in sections:
        if section.kind == "chapter":
            active = section
        if section == current:
            return active if current.kind == "topic" else None
    raise ValueError(f"section is absent from publication spine: {current.source}")


def render_nav(sections: tuple[PublicationSection, ...], current: PublicationSection) -> str:
    home = next(section for section in sections if section.kind == "preface")
    references = next(section for section in sections if section.kind == "references")
    grouped = chapter_topics(sections)
    parts = ['<ol class="book-nav__list">', f'<li class="book-nav__home">{nav_link(current, home, "Book home")}</li>']

    for section in sections:
        if section.kind == "part":
            parts.append(f'<li class="book-nav__part">{nav_link(current, section, page_label(section))}</li>')
        elif section.kind == "chapter":
            parts.append('<li class="book-nav__chapter">')
            parts.append(nav_link(current, section, page_label(section)))
            parts.append('<ol class="book-nav__topics">')
            for topic in grouped[section]:
                parts.append(f"<li>{nav_link(current, topic, page_label(topic))}</li>")
            parts.append("</ol></li>")

    parts.append(f'<li class="book-nav__references">{nav_link(current, references, "References")}</li>')
    parts.append("</ol>")
    return "".join(parts)


def render_breadcrumbs(sections: tuple[PublicationSection, ...], current: PublicationSection) -> str:
    home = next(section for section in sections if section.kind == "preface")
    if current.kind == "preface":
        return '<span aria-current="page">Book</span>'

    parts = [nav_link(current, home, "Book")]
    chapter = parent_chapter(sections, current)
    if chapter is not None:
        parts.append(nav_link(current, chapter, page_label(chapter)))
    parts.append(f'<span aria-current="page">{escape(page_label(current))}</span>')
    return '<span class="breadcrumbs__separator" aria-hidden="true">/</span>'.join(parts)


def render_reading_nav(sections: tuple[PublicationSection, ...], current: PublicationSection) -> str:
    position = sections.index(current)
    previous = sections[position - 1] if position else None
    following = sections[position + 1] if position + 1 < len(sections) else None
    up = parent_chapter(sections, current)

    parts = ['<nav class="reading-nav" aria-label="Reading navigation">']
    parts.append('<div class="reading-nav__previous">')
    if previous:
        parts.append(f'<span>Previous</span>{nav_link(current, previous, page_label(previous))}')
    parts.append("</div>")
    parts.append('<div class="reading-nav__up">')
    if up:
        parts.append(f'<span>Chapter</span>{nav_link(current, up, page_label(up))}')
    parts.append("</div>")
    parts.append('<div class="reading-nav__next">')
    if following:
        parts.append(f'<span>Next</span>{nav_link(current, following, page_label(following))}')
    parts.append("</div></nav>")
    return "".join(parts)


def write_html_page(
    section: PublicationSection,
    all_sections: tuple[PublicationSection, ...],
    template: str,
    enrichment: PublicationEnrichment | None = None,
) -> None:
    markdown_path = section.path
    raw_md = markdown_path.read_text(encoding="utf-8")
    if enrichment is not None:
        raw_md = enrich_section_markdown(
            markdown_path,
            raw_md,
            enrichment,
            output="web",
        )
    processed_md = rewrite_md_links(raw_md)
    title = extract_title(processed_md, markdown_path.stem)
    html_body = render_markdown(processed_md)

    target = SITE_DIR / html_path(markdown_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    page = template.format(
        title=escape(title),
        css_path=relative_href(markdown_path, BOOK_DIR / "assets" / "style.md").replace("style.html", "style.css"),
        favicon_path=relative_href(markdown_path, BOOK_DIR / "assets" / "favicon.svg").replace(".html", ".svg"),
        home_path=relative_href(markdown_path, BOOK_DIR / "index.md"),
        breadcrumbs=render_breadcrumbs(all_sections, section),
        nav=render_nav(all_sections, section),
        content=html_body,
        reading_nav=render_reading_nav(all_sections, section),
        updated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
    target.write_text(page, encoding="utf-8")


def main() -> None:
    if not BOOK_DIR.exists():
        raise SystemExit("Missing book/ directory")

    sections = discover_publication_sections()
    enrichment = load_publication_enrichment(BOOK_DIR)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    for section in sections:
        write_html_page(section, sections, template, enrichment)

    assets_source = BOOK_DIR / "assets"
    if assets_source.exists():
        shutil.copytree(assets_source, SITE_DIR / "assets", dirs_exist_ok=True)

    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")
    failures = find_broken_site_links(SITE_DIR)
    if failures:
        raise SystemExit("Generated site has broken links:\n" + "\n".join(failures))
    print(f"Built {len(sections)} reader-facing pages in {SITE_DIR}")


if __name__ == "__main__":
    main()
