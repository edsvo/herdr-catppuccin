"""Tests for the theme generator."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "generate", ROOT / "scripts" / "generate.py"
)
generate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generate)


class GenerateTests(unittest.TestCase):
    def test_mix(self):
        self.assertEqual(generate.mix("#ffffff", "#000000", 0.5), "#808080")
        self.assertEqual(generate.mix("#000000", "#ffffff", 0.5), "#808080")
        self.assertEqual(generate.mix("#ffffff", "#000000", 1.0), "#ffffff")
        self.assertEqual(generate.mix("#ffffff", "#000000", 0.0), "#000000")

    def test_contrast(self):
        self.assertAlmostEqual(
            generate.contrast("#000000", "#ffffff"), 21.0, places=1
        )
        self.assertAlmostEqual(
            generate.contrast("#ffffff", "#ffffff"), 1.0, places=1
        )

    def test_all_themes_validate(self):
        for flavor in generate.PALETTE:
            with self.subTest(flavor=flavor):
                self.assertEqual(
                    generate.validate(flavor, generate.build(flavor)), []
                )

    def test_hex_validation(self):
        self.assertTrue(generate._is_hex("#a1b2c3"))
        self.assertTrue(generate._is_hex("#A1B2C3"))
        self.assertFalse(generate._is_hex("a1b2c3"))
        self.assertFalse(generate._is_hex("#a1b2c3d"))
        self.assertFalse(generate._is_hex("#a1b2cg"))


if __name__ == "__main__":
    unittest.main()
