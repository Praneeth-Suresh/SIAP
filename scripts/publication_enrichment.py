#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import os
import re
import tomllib


SCHEMA_VERSION = 1
STABLE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SEMANTIC_CLASSES = frozenset({"exercise", "reader-question"})
QUOTE_FIELDS = frozenset(
    {
        "id",
        "source",
        "text",
        "speaker",
        "work",
        "year",
        "locator",
        "url",
        "accessed",
        "placement",
    }
)
QUOTE_RIGHTS_FIELDS = frozenset({"rights", "rights_basis"})
VISUAL_FIELDS = frozenset(
    {
        "id",
        "source",
        "kind",
        "path",
        "placement",
        "alt",
        "width",
        "height",
        "content_bbox",
        "min_padding",
    }
)


@dataclass(frozen=True)
class QuoteRecord:
    id: str
    source: str
    text: str
    speaker: str
    work: str
    year: str
    locator: str
    url: str
    accessed: str
    rights: str
    placement: str


@dataclass(frozen=True)
class VisualRecord:
    id: str
    source: str
    kind: str
    path: str
    placement: str
    alt: str
    width: int
    height: int
    content_bbox: tuple[int, int, int, int]
    min_padding: int


@dataclass(frozen=True)
class PublicationEnrichment:
    book_dir: Path
    quotes: tuple[QuoteRecord, ...]
    visuals: tuple[VisualRecord, ...]
    quotes_strict: bool
    visuals_strict: bool

    def quotes_for(self, source: str, placement: str) -> tuple[QuoteRecord, ...]:
        return tuple(
            quote
            for quote in self.quotes
            if quote.source == source and quote.placement == placement
        )

    def visuals_for(self, source: str, placement: str) -> tuple[VisualRecord, ...]:
        return tuple(
            visual
            for visual in self.visuals
            if visual.source == source and visual.placement == placement
        )


def _load_registry(path: Path, table_name: str) -> tuple[list[object], bool]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"{path} must declare schema_version = {SCHEMA_VERSION}")
    strict = data.get("strict", False)
    if not isinstance(strict, bool):
        raise ValueError(f"{path}: strict must be true or false")
    records = data.get(table_name, [])
    if not isinstance(records, list):
        raise ValueError(f"{path}: {table_name} must be an array of tables")
    return records, strict


def _validate_id(record_id: str, registry: Path) -> None:
    if not STABLE_ID.fullmatch(record_id):
        raise ValueError(f"{registry}: invalid stable id {record_id!r}")


def _relative_source(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.endswith(".md"):
        raise ValueError(f"{label}: source must be a relative Markdown path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label}: source escapes the book directory")
    return path.as_posix()


def _relative_asset(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label}: path must be a relative asset path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label}: path escapes the book directory")
    return path.as_posix()


def _nonempty_string(value: object, *, field: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: {field} must be a non-empty string")
    return value.strip()


def _parse_quotes(path: Path) -> tuple[tuple[QuoteRecord, ...], bool]:
    raw_records, strict = _load_registry(path, "quotes")
    quotes: list[QuoteRecord] = []
    seen: set[tuple[str, str]] = set()
    for index, raw in enumerate(raw_records, start=1):
        label = f"quote record {index}"
        if not isinstance(raw, dict):
            raise ValueError(f"{label} must be a table")
        missing = QUOTE_FIELDS - raw.keys()
        if not raw.keys() & QUOTE_RIGHTS_FIELDS:
            missing.add("rights_basis")
        extra = raw.keys() - (QUOTE_FIELDS | QUOTE_RIGHTS_FIELDS)
        if missing:
            raise ValueError(f"{label} is missing fields: {', '.join(sorted(missing))}")
        if extra:
            raise ValueError(f"{label} has unknown fields: {', '.join(sorted(extra))}")
        record_id = _nonempty_string(raw["id"], field="id", label=label)
        _validate_id(record_id, path)
        source = _relative_source(raw["source"], label=label)
        key = (source, record_id)
        if key in seen:
            raise ValueError(f"duplicate quote key: {source} + {record_id}")
        seen.add(key)
        placement = _nonempty_string(raw["placement"], field="placement", label=label)
        if placement not in {"opening", "closing"}:
            raise ValueError(f"{label}: placement must be opening or closing")
        accessed = _nonempty_string(raw["accessed"], field="accessed", label=label)
        try:
            date.fromisoformat(accessed)
        except ValueError as exc:
            raise ValueError(f"{label}: accessed must be an ISO date") from exc
        url = _nonempty_string(raw["url"], field="url", label=label)
        if not url.startswith(("https://", "http://")):
            raise ValueError(f"{label}: url must use HTTP or HTTPS")
        year = raw["year"]
        if not isinstance(year, (str, int)) or isinstance(year, bool):
            raise ValueError(f"{label}: year must be a string or integer")
        quotes.append(
            QuoteRecord(
                id=record_id,
                source=source,
                text=_nonempty_string(raw["text"], field="text", label=label),
                speaker=_nonempty_string(raw["speaker"], field="speaker", label=label),
                work=_nonempty_string(raw["work"], field="work", label=label),
                year=str(year),
                locator=_nonempty_string(raw["locator"], field="locator", label=label),
                url=url,
                accessed=accessed,
                rights=_nonempty_string(
                    raw.get("rights_basis", raw.get("rights")),
                    field="rights_basis",
                    label=label,
                ),
                placement=placement,
            )
        )
    return tuple(sorted(quotes, key=lambda record: (record.source, record.id))), strict


def _parse_visuals(path: Path) -> tuple[tuple[VisualRecord, ...], bool]:
    raw_records, strict = _load_registry(path, "visuals")
    visuals: list[VisualRecord] = []
    seen: set[tuple[str, str]] = set()
    for index, raw in enumerate(raw_records, start=1):
        label = f"visual record {index}"
        if not isinstance(raw, dict):
            raise ValueError(f"{label} must be a table")
        missing = VISUAL_FIELDS - raw.keys()
        extra = raw.keys() - VISUAL_FIELDS
        if missing:
            raise ValueError(f"{label} is missing fields: {', '.join(sorted(missing))}")
        if extra:
            raise ValueError(f"{label} has unknown fields: {', '.join(sorted(extra))}")
        record_id = _nonempty_string(raw["id"], field="id", label=label)
        _validate_id(record_id, path)
        source = _relative_source(raw["source"], label=label)
        key = (source, record_id)
        if key in seen:
            raise ValueError(f"duplicate visual key: {source} + {record_id}")
        seen.add(key)
        kind = _nonempty_string(raw["kind"], field="kind", label=label)
        if kind not in {"cartoon", "diagram"}:
            raise ValueError(f"{label}: kind must be cartoon or diagram")
        placement = _nonempty_string(raw["placement"], field="placement", label=label)
        if placement not in {"opening", "inline", "terminal"}:
            raise ValueError(f"{label}: placement must be opening, inline, or terminal")
        width, height, min_padding = raw["width"], raw["height"], raw["min_padding"]
        if not all(isinstance(value, int) and not isinstance(value, bool) for value in (width, height, min_padding)):
            raise ValueError(f"{label}: width, height, and min_padding must be integers")
        if width <= 0 or height <= 0 or min_padding < 0:
            raise ValueError(f"{label}: dimensions must be positive and padding non-negative")
        bbox = raw["content_bbox"]
        if not isinstance(bbox, list) or len(bbox) != 4 or not all(isinstance(value, int) and not isinstance(value, bool) for value in bbox):
            raise ValueError(f"{label}: content_bbox must contain four integers")
        x0, y0, x1, y1 = bbox
        if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
            raise ValueError(f"{label}: content_bbox must fit inside declared dimensions")
        visuals.append(
            VisualRecord(
                id=record_id,
                source=source,
                kind=kind,
                path=_relative_asset(raw["path"], label=label),
                placement=placement,
                alt=_nonempty_string(raw["alt"], field="alt", label=label),
                width=width,
                height=height,
                content_bbox=(x0, y0, x1, y1),
                min_padding=min_padding,
            )
        )
    return tuple(sorted(visuals, key=lambda record: (record.source, record.id))), strict


def load_publication_enrichment(book_dir: Path) -> PublicationEnrichment:
    book_dir = book_dir.resolve()
    quotes, quotes_strict = _parse_quotes(book_dir / "quotes.toml")
    visuals, visuals_strict = _parse_visuals(book_dir / "visuals.toml")
    return PublicationEnrichment(
        book_dir=book_dir,
        quotes=quotes,
        visuals=visuals,
        quotes_strict=quotes_strict,
        visuals_strict=visuals_strict,
    )


def _source_key(section_path: Path, book_dir: Path) -> str:
    try:
        return section_path.resolve().relative_to(book_dir.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"section escapes book directory: {section_path}") from exc


def _quote_markdown(quote: QuoteRecord) -> str:
    text = " ".join(quote.text.splitlines())
    return (
        f"> *“{text}”*\n>\n"
        f"> — {quote.speaker}, *{quote.work}* ({quote.year}), {quote.locator}. "
        f"[Source]({quote.url}), accessed {quote.accessed}. {quote.rights}."
    )


def _visual_markdown(visual: VisualRecord, section_path: Path, book_dir: Path) -> str:
    target = book_dir / visual.path
    relative = Path(os.path.relpath(target, section_path.parent)).as_posix()
    return f"![{visual.alt}]({relative}){{.{visual.kind} .{visual.placement}-visual}}"


def _terminal_footnote_index(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if re.match(r"^\[\^[^\]]+\]:", line):
            return index
    return len(lines)


def enrich_section_markdown(
    section_path: Path,
    markdown_text: str,
    enrichment: PublicationEnrichment,
) -> str:
    source = _source_key(section_path, enrichment.book_dir)
    opening = [
        *(_quote_markdown(quote) for quote in enrichment.quotes_for(source, "opening")),
        *(
            _visual_markdown(visual, section_path, enrichment.book_dir)
            for visual in enrichment.visuals_for(source, "opening")
        ),
    ]
    terminal = [
        *(_quote_markdown(quote) for quote in enrichment.quotes_for(source, "closing")),
        *(
            _visual_markdown(visual, section_path, enrichment.book_dir)
            for visual in enrichment.visuals_for(source, "terminal")
        ),
    ]
    if not opening and not terminal:
        return markdown_text

    lines = markdown_text.rstrip("\n").splitlines()
    if opening:
        heading_index = next(
            (index for index, line in enumerate(lines) if line.startswith("# ")),
            None,
        )
        if heading_index is None:
            raise ValueError(f"{source}: cannot place opening enrichment without an H1")
        lines[heading_index + 1 : heading_index + 1] = ["", "\n\n".join(opening), ""]
    if terminal:
        insertion = _terminal_footnote_index(lines)
        lines[insertion:insertion] = ["", "\n\n".join(terminal), ""]
    return "\n".join(lines).rstrip() + "\n"


def _semantic_classes(line: str) -> tuple[str, ...] | None:
    match = re.match(r"^:::\s*\{([^}]*)\}\s*$", line)
    if not match:
        return None
    classes = tuple(token[1:] for token in match.group(1).split() if token.startswith("."))
    return classes if SEMANTIC_CLASSES.intersection(classes) else None


def _unnumber_heading(line: str) -> str:
    if not re.match(r"^#{1,6}\s+", line):
        return line
    attrs = re.match(r"^(.*?)(?:\s+\{([^}]*)\})\s*$", line)
    if attrs:
        tokens = attrs.group(2).split()
        if ".unnumbered" not in tokens:
            tokens.append(".unnumbered")
        return f"{attrs.group(1)} {{{' '.join(tokens)}}}"
    return f"{line} {{.unnumbered}}"


def adapt_semantic_divs(markdown_text: str, *, target: str) -> str:
    if target not in {"html", "latex"}:
        raise ValueError(f"unknown semantic-div target: {target}")
    output: list[str] = []
    active: tuple[str, ...] | None = None
    heading_seen = False
    code_fence: str | None = None
    for line in markdown_text.splitlines():
        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            marker = fence.group(1)[0]
            if code_fence is None:
                code_fence = marker
            elif code_fence == marker:
                code_fence = None
            output.append(line)
            continue
        classes = None if code_fence is not None else _semantic_classes(line)
        if classes is not None:
            if active is not None:
                raise ValueError("nested semantic fenced divs are not supported")
            active = classes
            heading_seen = False
            primary = "exercise" if "exercise" in classes else "reader-question"
            if target == "html":
                class_names = " ".join(classes)
                output.append(f'<section class="{class_names}" markdown="1">')
            else:
                macro = "siapexercisebegin" if primary == "exercise" else "siapreaderquestionbegin"
                output.extend([f"\\{macro}", ""])
            continue
        if active is not None and code_fence is None and line.strip() == ":::":
            primary = "exercise" if "exercise" in active else "reader-question"
            if target == "html":
                output.append("</section>")
            else:
                macro = "siapexerciseend" if primary == "exercise" else "siapreaderquestionend"
                output.extend(["", f"\\{macro}"])
            active = None
            continue
        if active is not None and target == "latex" and not heading_seen and re.match(r"^#{1,6}\s+", line):
            line = _unnumber_heading(line)
            heading_seen = True
        output.append(line)
    if active is not None:
        raise ValueError("unclosed semantic fenced div")
    return "\n".join(output) + ("\n" if markdown_text.endswith("\n") else "")
