from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

try:
    from PIL import Image, ImageDraw
except ImportError:  # The project dependency is installed by requirements.txt.
    Image = None
    ImageDraw = None

from audit_visuals import audit_visuals  # noqa: E402


@unittest.skipUnless(Image is not None, "Pillow is required for visual-audit tests")
class VisualAuditTests(unittest.TestCase):
    def make_book(self, *, bbox: tuple[int, int, int, int], min_padding: int = 10) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        book_dir = Path(temporary.name)
        (book_dir / "index.md").write_text("# Book\n", encoding="utf-8")
        (book_dir / "part.md").write_text("# Part 0\n", encoding="utf-8")
        for number in range(1, 5):
            (book_dir / f"chapter-{number}.md").write_text(
                f"# Chapter {number}\n",
                encoding="utf-8",
            )
        (book_dir / "references.md").write_text("# References\n", encoding="utf-8")
        (book_dir / "publication.toml").write_text(
            textwrap.dedent(
                """\
                [[section]]
                source = "index.md"
                kind = "preface"

                [[section]]
                source = "part.md"
                kind = "part"

                [[section]]
                source = "chapter-1.md"
                kind = "chapter"

                [[section]]
                source = "chapter-2.md"
                kind = "chapter"

                [[section]]
                source = "chapter-3.md"
                kind = "chapter"

                [[section]]
                source = "chapter-4.md"
                kind = "chapter"

                [[section]]
                source = "references.md"
                kind = "references"
                """
            ),
            encoding="utf-8",
        )
        (book_dir / "quotes.toml").write_text(
            "schema_version = 1\nstrict = false\nquotes = []\n",
            encoding="utf-8",
        )
        (book_dir / "assets").mkdir()
        image_path = book_dir / "assets" / "cartoon.png"
        image = Image.new("RGB", (100, 80), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((10, 12, 89, 67), fill="black")
        image.save(image_path, format="PNG")
        (book_dir / "visuals.toml").write_text(
            textwrap.dedent(
                f"""\
                schema_version = 1
                strict = false

                [[visuals]]
                id = "cartoon"
                source = "index.md"
                kind = "cartoon"
                path = "assets/cartoon.png"
                placement = "terminal"
                alt = "A test cartoon."
                width = 100
                height = 80
                content_bbox = [{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}]
                min_padding = {min_padding}
                """
            ),
            encoding="utf-8",
        )
        return book_dir

    def test_png_dimensions_bbox_and_padding_pass(self) -> None:
        book_dir = self.make_book(bbox=(10, 12, 90, 68))

        self.assertEqual(audit_visuals(book_dir), [])

    def test_bbox_drift_and_insufficient_padding_fail(self) -> None:
        book_dir = self.make_book(bbox=(11, 12, 90, 68), min_padding=13)

        issues = audit_visuals(book_dir)

        self.assertTrue(any("content bbox" in issue for issue in issues))
        self.assertTrue(any("minimum padding" in issue for issue in issues))

    def test_strict_mode_requires_one_terminal_cartoon_per_section(self) -> None:
        book_dir = self.make_book(bbox=(10, 12, 90, 68))

        issues = audit_visuals(book_dir, strict=True)

        self.assertTrue(any("references.md" in issue and "terminal cartoon" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
