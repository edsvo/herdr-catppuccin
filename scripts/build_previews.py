#!/usr/bin/env python3
"""Build the individual previews and the composite from four screenshots.

Usage:
    python3 scripts/build_previews.py LATTE FRAPPE MACCHIATO MOCHA

Each argument is a screenshot taken with `herdr-app shot`. The script writes
assets/<flavor>.webp and assets/preview.webp.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Install Pillow first: python3 -m pip install Pillow")

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FLAVORS = ("latte", "frappe", "macchiato", "mocha")
SIZE = (1920, 1040)
COMPOSITE_SIZE = (3888, 2128)
BORDER = 16


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__, file=sys.stderr)
        return 2

    ASSETS.mkdir(exist_ok=True)
    images = {}
    for flavor, source in zip(FLAVORS, sys.argv[1:]):
        path = Path(source)
        if not path.exists():
            print(f"missing screenshot: {path}", file=sys.stderr)
            return 1
        image = Image.open(path).convert("RGB")
        image = image.resize(SIZE, Image.Resampling.LANCZOS)
        images[flavor] = image
        target = ASSETS / f"{flavor}.webp"
        image.save(target, format="WEBP", quality=82, method=6)
        print(f"wrote {target.relative_to(ROOT)}")

    composite = Image.new("RGB", COMPOSITE_SIZE, (0, 0, 0))
    positions = {
        "latte": (BORDER, BORDER),
        "frappe": (SIZE[0] + BORDER * 2, BORDER),
        "macchiato": (BORDER, SIZE[1] + BORDER * 2),
        "mocha": (SIZE[0] + BORDER * 2, SIZE[1] + BORDER * 2),
    }
    for flavor, position in positions.items():
        composite.paste(images[flavor], position)

    target = ASSETS / "preview.webp"
    composite.save(target, format="WEBP", quality=82, method=6)
    print(f"wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
