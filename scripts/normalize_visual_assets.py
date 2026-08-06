#!/usr/bin/env python3
"""Give publication PNGs a deterministic, aspect-preserving safe matte."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, PngImagePlugin


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "book" / "assets"
PAPER = (244, 240, 230)
MARKER = "siap-safe-matte-v3"
LEGACY_MARKER = "siap-safe-matte-v2"


def _fit(image: Image.Image, canvas: tuple[int, int], matte: int) -> Image.Image:
    max_width = canvas[0] - 2 * matte
    max_height = canvas[1] - 2 * matte
    scale = min(max_width / image.width, max_height / image.height)
    size = (round(image.width * scale), round(image.height * scale))
    resized = image.resize(size, Image.Resampling.LANCZOS)
    framed = Image.new("RGB", canvas, PAPER)
    offset = ((canvas[0] - size[0]) // 2, (canvas[1] - size[1]) // 2)
    framed.paste(resized, offset)
    return framed


def normalize(path: Path, *, canvas: tuple[int, int], matte: int) -> bool:
    with Image.open(path) as source:
        source.load()
        if source.info.get("siap_matte") == MARKER:
            return False
        if path.parent.name == "diagrams" and source.info.get("siap_matte") == LEGACY_MARKER:
            return False
        rgb = source.convert("RGB")
        # The first cartoon pass used a non-aspect-preserving 96px inset. Undo
        # that inset before fitting the corrected frame.
        if path.parent.name == "cartoons" and source.info.get("siap_matte") == LEGACY_MARKER:
            rgb = rgb.crop((96, 96, 1440, 928)).resize(
                (1536, 1024), Image.Resampling.LANCZOS
            )
        framed = _fit(rgb, canvas, matte)
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("siap_matte", MARKER)
        framed.save(path, format="PNG", optimize=True, pnginfo=metadata)
    return True


def main() -> None:
    changed = 0
    for path in sorted((ASSET_DIR / "cartoons").glob("[0-9][0-9]-*.png")):
        if path.name.startswith("00-"):
            continue
        changed += int(normalize(path, canvas=(1536, 1024), matte=96))
    for path in sorted((ASSET_DIR / "diagrams").glob("*.png")):
        changed += int(normalize(path, canvas=(1200, 700), matte=48))
    print(f"Normalized {changed} visual asset(s) with aspect-preserving safe mattes")


if __name__ == "__main__":
    main()
