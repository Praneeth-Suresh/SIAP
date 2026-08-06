from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


MANIFEST_NAME = "publication.toml"
VALID_KINDS = frozenset({"preface", "part", "chapter", "topic", "references"})


@dataclass(frozen=True)
class PublicationSection:
    source: str
    kind: str
    path: Path


def load_publication_manifest(book_dir: Path) -> tuple[PublicationSection, ...]:
    manifest_path = book_dir / MANIFEST_NAME
    data = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    raw_sections = data.get("section")
    if not isinstance(raw_sections, list) or not raw_sections:
        raise ValueError(f"{manifest_path} must declare at least one [[section]]")

    sections: list[PublicationSection] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_sections, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"section {index} must be a table")
        source = raw.get("source")
        kind = raw.get("kind")
        if not isinstance(source, str) or not source.endswith(".md"):
            raise ValueError(f"section {index} has an invalid Markdown source")
        if kind not in VALID_KINDS:
            raise ValueError(f"section {index} has invalid kind {kind!r}")
        if source in seen:
            raise ValueError(f"duplicate publication source: {source}")
        if source.endswith("-notes.md") or source == "continuity-ledger.md":
            raise ValueError(f"revision support cannot be published: {source}")

        path = (book_dir / source).resolve()
        try:
            path.relative_to(book_dir.resolve())
        except ValueError as exc:
            raise ValueError(f"publication source escapes book directory: {source}") from exc
        if not path.is_file():
            raise ValueError(f"missing publication source: {source}")

        seen.add(source)
        sections.append(PublicationSection(source=source, kind=kind, path=path))

    if sections[0].kind != "preface" or sections[-1].kind != "references":
        raise ValueError("publication spine must start with a preface and end with references")
    if sum(section.kind == "part" for section in sections) < 1:
        raise ValueError("publication spine must contain Part 0")
    if sum(section.kind == "chapter" for section in sections) != 4:
        raise ValueError("publication spine must contain exactly four numbered chapters")

    return tuple(sections)
