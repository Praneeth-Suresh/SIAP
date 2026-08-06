#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from publication_enrichment import PublicationEnrichment, VisualRecord, load_publication_enrichment
from publication_manifest import load_publication_manifest


try:
    from PIL import Image, ImageChops
except ImportError:  # pragma: no cover - exercised by the CLI error path.
    Image = None
    ImageChops = None


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"


def _content_bbox(image: object) -> tuple[int, int, int, int] | None:
    rgb = image.convert("RGB")
    background = Image.new("RGB", rgb.size, rgb.getpixel((0, 0)))
    difference = ImageChops.difference(rgb, background).convert("L")
    mask = difference.point(lambda value: 255 if value > 8 else 0)
    return mask.getbbox()


def _audit_image(book_dir: Path, visual: VisualRecord) -> list[str]:
    issues: list[str] = []
    image_path = (book_dir / visual.path).resolve()
    try:
        image_path.relative_to(book_dir.resolve())
    except ValueError:
        return [f"visual {visual.id}: asset escapes book directory"]
    if not image_path.is_file():
        return [f"visual {visual.id}: missing asset {visual.path}"]
    try:
        with Image.open(image_path) as image:
            image.load()
            if image.format != "PNG":
                issues.append(f"visual {visual.id}: expected PNG, found {image.format or 'unknown'}")
            if image.size != (visual.width, visual.height):
                issues.append(
                    f"visual {visual.id}: dimensions {image.size} do not match "
                    f"{(visual.width, visual.height)}"
                )
            actual_bbox = _content_bbox(image)
    except (OSError, ValueError) as exc:
        return [f"visual {visual.id}: cannot read {visual.path}: {exc}"]
    if actual_bbox is None:
        issues.append(f"visual {visual.id}: image has no content distinct from its background")
        return issues
    if actual_bbox != visual.content_bbox:
        issues.append(
            f"visual {visual.id}: content bbox {actual_bbox} does not match "
            f"declared {visual.content_bbox}"
        )
    left, top, right, bottom = actual_bbox
    padding = min(left, top, visual.width - right, visual.height - bottom)
    if padding < visual.min_padding:
        issues.append(
            f"visual {visual.id}: minimum padding is {padding}px; "
            f"declared contract requires {visual.min_padding}px"
        )
    return issues


def _strict_coverage(
    enrichment: PublicationEnrichment,
    publication_sources: set[str],
) -> list[str]:
    issues: list[str] = []
    for source in sorted(publication_sources):
        cartoons = [
            visual
            for visual in enrichment.visuals
            if visual.source == source
            and visual.kind == "cartoon"
            and visual.placement == "terminal"
        ]
        if len(cartoons) != 1:
            issues.append(
                f"{source}: expected exactly one terminal cartoon in strict mode; "
                f"found {len(cartoons)}"
            )
    terminal_paths = [
        visual.path
        for visual in enrichment.visuals
        if visual.kind == "cartoon" and visual.placement == "terminal"
    ]
    if len(terminal_paths) != len(set(terminal_paths)):
        issues.append("strict mode requires a distinct asset path for every terminal cartoon")
    return issues


def audit_visuals(book_dir: Path = BOOK_DIR, *, strict: bool | None = None) -> list[str]:
    if Image is None or ImageChops is None:
        raise RuntimeError("visual auditing requires Pillow; install requirements.txt")
    book_dir = book_dir.resolve()
    enrichment = load_publication_enrichment(book_dir)
    sections = load_publication_manifest(book_dir)
    publication_sources = {section.source for section in sections}
    issues: list[str] = []
    for visual in enrichment.visuals:
        if visual.source not in publication_sources:
            issues.append(f"visual {visual.id}: source {visual.source} is not in publication.toml")
        issues.extend(_audit_image(book_dir, visual))
    strict_mode = enrichment.visuals_strict if strict is None else strict
    if strict_mode:
        issues.extend(_strict_coverage(enrichment, publication_sources))
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate SIAP publication visual contracts")
    parser.add_argument("--book-dir", type=Path, default=BOOK_DIR)
    parser.add_argument("--strict", action="store_true", help="require one terminal cartoon per published section")
    args = parser.parse_args()
    try:
        issues = audit_visuals(args.book_dir, strict=True if args.strict else None)
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        raise SystemExit(1)
    print("PASS: visual contracts are valid")


if __name__ == "__main__":
    main()
