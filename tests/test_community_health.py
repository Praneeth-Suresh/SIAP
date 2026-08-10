from __future__ import annotations

from pathlib import Path
import struct
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CommunityHealthTests(unittest.TestCase):
    def test_public_contributor_surface_is_present_and_linked(self) -> None:
        required_paths = (
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "SUPPORT.md",
            "LICENSE",
            "LICENSES.md",
            "NOTICE",
            "book/LICENSE.md",
            ".github/ISSUE_TEMPLATE/config.yml",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
            ".github/ISSUE_TEMPLATE/question.yml",
            ".github/pull_request_template.md",
        )

        for relative_path in required_paths:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for relative_path in (
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "SUPPORT.md",
            "LICENSES.md",
        ):
            self.assertIn(relative_path, readme)

    def test_readme_cartoon_is_a_local_nonpublication_png(self) -> None:
        relative_path = "assets/readme/why-this-manuscript-matters.png"
        asset = ROOT / relative_path
        self.assertTrue(asset.is_file())

        header = asset.read_bytes()[:24]
        self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", header[16:24]), (1536, 1024))

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"]({relative_path})", readme)

        publication_visuals = (ROOT / "book/visuals.toml").read_text(encoding="utf-8")
        self.assertNotIn(relative_path, publication_visuals)


if __name__ == "__main__":
    unittest.main()
