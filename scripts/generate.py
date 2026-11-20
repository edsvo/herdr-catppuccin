#!/usr/bin/env python3
"""Generate the Catppuccin themes for the Herdr desktop app.

The palette values below are taken from the official Catppuccin palette
(https://github.com/catppuccin/palette, v5). The ANSI brights are the
official ``ansiColors`` values, not a second interpolation of the base
palette, so terminal output matches the rest of the Catppuccin ecosystem.
The UI role mapping follows the official Catppuccin style guide
(https://github.com/catppuccin/catppuccin/blob/main/docs/style-guide.md).

Usage:
    python3 scripts/generate.py           # write themes/*.json
    python3 scripts/generate.py --check   # fail if the files are out of date
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"

# Official Catppuccin palette v5.
PALETTE = {
    "latte": {
        "rosewater": "#dc8a78",
        "flamingo": "#dd7878",
        "pink": "#ea76cb",
        "mauve": "#8839ef",
        "red": "#d20f39",
        "maroon": "#e64553",
        "peach": "#fe640b",
        "yellow": "#df8e1d",
        "green": "#40a02b",
        "teal": "#179299",
        "sky": "#04a5e5",
        "sapphire": "#209fb5",
        "blue": "#1e66f5",
        "lavender": "#7287fd",
        "text": "#4c4f69",
        "subtext1": "#5c5f77",
        "subtext0": "#6c6f85",
        "overlay2": "#7c7f93",
        "overlay1": "#8c8fa1",
        "overlay0": "#9ca0b0",
        "surface2": "#acb0be",
        "surface1": "#bcc0cc",
        "surface0": "#ccd0da",
        "base": "#eff1f5",
        "mantle": "#e6e9ef",
        "crust": "#dce0e8",
    },
    "frappe": {
        "rosewater": "#f2d5cf",
        "flamingo": "#eebebe",
        "pink": "#f4b8e4",
        "mauve": "#ca9ee6",
        "red": "#e78284",
        "maroon": "#ea999c",
        "peach": "#ef9f76",
        "yellow": "#e5c890",
        "green": "#a6d189",
        "teal": "#81c8be",
        "sky": "#99d1db",
        "sapphire": "#85c1dc",
        "blue": "#8caaee",
        "lavender": "#babbf1",
        "text": "#c6d0f5",
        "subtext1": "#b5bfe2",
        "subtext0": "#a5adce",
        "overlay2": "#949cbb",
        "overlay1": "#838ba7",
        "overlay0": "#737994",
        "surface2": "#626880",
        "surface1": "#51576d",
        "surface0": "#414559",
        "base": "#303446",
        "mantle": "#292c3c",
        "crust": "#232634",
    },
    "macchiato": {
        "rosewater": "#f4dbd6",
        "flamingo": "#f0c6c6",
        "pink": "#f5bde6",
        "mauve": "#c6a0f6",
        "red": "#ed8796",
        "maroon": "#ee99a0",
        "peach": "#f5a97f",
        "yellow": "#eed49f",
        "green": "#a6da95",
        "teal": "#8bd5ca",
        "sky": "#91d7e3",
        "sapphire": "#7dc4e4",
        "blue": "#8aadf4",
        "lavender": "#b7bdf8",
        "text": "#cad3f5",
        "subtext1": "#b8c0e0",
        "subtext0": "#a5adcb",
        "overlay2": "#939ab7",
        "overlay1": "#8087a2",
        "overlay0": "#6e738d",
        "surface2": "#5b6078",
        "surface1": "#494d64",
        "surface0": "#363a4f",
        "base": "#24273a",
        "mantle": "#1e2030",
        "crust": "#181926",
    },
    "mocha": {
        "rosewater": "#f5e0dc",
        "flamingo": "#f2cdcd",
        "pink": "#f5c2e7",
        "mauve": "#cba6f7",
        "red": "#f38ba8",
        "maroon": "#eba0ac",
        "peach": "#fab387",
        "yellow": "#f9e2af",
        "green": "#a6e3a1",
        "teal": "#94e2d5",
        "sky": "#89dceb",
        "sapphire": "#74c7ec",
        "blue": "#89b4fa",
        "lavender": "#b4befe",
        "text": "#cdd6f4",
        "subtext1": "#bac2de",
        "subtext0": "#a6adc8",
        "overlay2": "#9399b2",
        "overlay1": "#7f849c",
        "overlay0": "#6c7086",
        "surface2": "#585b70",
        "surface1": "#45475a",
        "surface0": "#313244",
        "base": "#1e1e2e",
        "mantle": "#181825",
        "crust": "#11111b",
    },
}

# Official ANSI palette (normal 0-7, bright 8-15).
ANSI = {
    "latte": [
        "#5c5f77", "#d20f39", "#40a02b", "#df8e1d",
        "#1e66f5", "#ea76cb", "#179299", "#acb0be",
        "#6c6f85", "#de293e", "#49af3d", "#eea02d",
        "#456eff", "#fe85d8", "#2d9fa8", "#bcc0cc",
    ],
    "frappe": [
        "#51576d", "#e78284", "#a6d189", "#e5c890",
        "#8caaee", "#f4b8e4", "#81c8be", "#a5adce",
        "#626880", "#e67172", "#8ec772", "#d9ba73",
        "#7b9ef0", "#f2a4db", "#5abfb5", "#b5bfe2",
    ],
    "macchiato": [
        "#494d64", "#ed8796", "#a6da95", "#eed49f",
        "#8aadf4", "#f5bde6", "#8bd5ca", "#a5adcb",
        "#5b6078", "#ec7486", "#8ccf7f", "#e1c682",
        "#78a1f6", "#f2a9dd", "#63cbc0", "#b8c0e0",
    ],
    "mocha": [
        "#45475a", "#f38ba8", "#a6e3a1", "#f9e2af",
        "#89b4fa", "#f5c2e7", "#94e2d5", "#a6adc8",
        "#585b70", "#f37799", "#89d88b", "#ebd391",
        "#74a8fc", "#f2aede", "#6bd7ca", "#bac2de",
    ],
}

# Theme tokens documented by Herdr (`theme()` in herdr.d.ts).
COLOR_TOKENS = {
    "background",
    "canvas",
    "chrome",
    "surface",
    "popover",
    "raised",
    "hover",
    "selected",
    "border",
    "input",
    "foreground",
    "muted",
    "dim",
    "accent",
    "accent_foreground",
    "ring",
    "solid",
    "solid_foreground",
    "selection",
    "working",
    "blocked",
    "done",
    "idle",
    "unknown",
}

HEX_DIGITS = set("0123456789abcdef")


def mix(fg: str, bg: str, weight: float) -> str:
    """Blend ``fg`` over ``bg`` at ``weight`` and return an opaque ``#rrggbb``.

    Herdr theme files use six-digit hex, so the style guide's translucent
    selection background is flattened onto the flavor's Base color instead of
    being written as an alpha channel.
    """
    fg_rgb = [int(fg[i : i + 2], 16) for i in (1, 3, 5)]
    bg_rgb = [int(bg[i : i + 2], 16) for i in (1, 3, 5)]
    out = [round(f * weight + b * (1 - weight)) for f, b in zip(fg_rgb, bg_rgb)]
    return "#{:02x}{:02x}{:02x}".format(*out)


def build(flavor: str) -> dict:
    p = PALETTE[flavor]
    # The style guide recommends Overlay 2 at 20-30% for selection. Herdr
    # needs opaque hex, so flatten the 30% selection onto Base.
    selection = mix(p["overlay2"], p["base"], 0.30)

    return {
        "background": p["base"],
        "foreground": p["text"],
        "selection": selection,
        "cursor": p["rosewater"],
        "ansi": ANSI[flavor],
        "colors": {
            # The style guide allows Crust or Mantle for secondary panes.
            # This port uses Crust for the chrome and the area behind pane
            # cards, and Mantle for secondary panels, giving the three-step
            # Base/Mantle/Crust hierarchy.
            "background": p["base"],
            "canvas": p["crust"],
            "chrome": p["crust"],
            "surface": p["mantle"],
            "popover": p["mantle"],
            # Surface 0 and Surface 2 are surface elements. The style guide
            # names the family, not a component mapping, so raised and hover
            # use Surface 0 and input uses Surface 2.
            "raised": p["surface0"],
            "hover": p["surface0"],
            "selected": selection,
            "selection": selection,
            # The style guide names Overlay 0 for the inactive terminal border
            # and Overlay 2 for selection.
            "border": p["overlay0"],
            "input": p["surface2"],
            # Text.
            "foreground": p["text"],
            "muted": p["subtext1"],
            "dim": p["overlay1"],
            # The style guide does not name a UI accent. This port uses Mauve,
            # one of the Catppuccin accent colors; Base is the recommended
            # text on accent.
            "accent": p["mauve"],
            "accent_foreground": p["base"],
            "ring": p["lavender"],
            "solid": p["mauve"],
            "solid_foreground": p["base"],
            # Agent statuses have no explicit style-guide colors. Map working
            # to Blue, blocked to Red, and done to Green; use the overlay
            # hierarchy for idle and unknown.
            "working": p["blue"],
            "blocked": p["red"],
            "done": p["green"],
            "idle": p["overlay1"],
            "unknown": p["overlay0"],
        },
    }


def render(flavor: str) -> str:
    return json.dumps(build(flavor), indent=2, ensure_ascii=False) + "\n"


def luminance(hex_color: str) -> float:
    channels = [int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    channels = [
        c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        for c in channels
    ]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def validate(flavor: str, theme: dict) -> list[str]:
    errors: list[str] = []

    for key in ("background", "foreground", "selection"):
        value = theme.get(key)
        if not isinstance(value, str) or not _is_hex(value):
            errors.append(f"{flavor}: {key} is not a #rrggbb color: {value!r}")
    if not _is_hex(theme.get("cursor")):
        errors.append(f"{flavor}: cursor is not a #rrggbb color: {theme.get('cursor')!r}")

    ansi = theme.get("ansi", [])
    if len(ansi) != 16:
        errors.append(f"{flavor}: ansi must have 16 entries, got {len(ansi)}")
    for i, value in enumerate(ansi):
        if not _is_hex(value):
            errors.append(f"{flavor}: ansi[{i}] is not a #rrggbb color: {value!r}")

    colors = theme.get("colors", {})
    unknown = sorted(set(colors) - COLOR_TOKENS)
    if unknown:
        errors.append(f"{flavor}: unknown color tokens: {', '.join(unknown)}")
    missing = sorted(COLOR_TOKENS - set(colors))
    if missing:
        errors.append(f"{flavor}: missing color tokens: {', '.join(missing)}")
    for key, value in colors.items():
        if not _is_hex(value):
            errors.append(f"{flavor}: colors.{key} is not #rrggbb: {value!r}")

    # Contrast sanity checks. These are not a WCAG conformance claim, but they
    # catch a palette mistake before it ships. Subtle text and non-text roles
    # use lower floors because the style guide deliberately makes them quiet.
    fg = colors.get("foreground")
    muted = colors.get("muted")
    dim = colors.get("dim")
    accent = colors.get("accent")
    checks = [
        ("foreground/background", fg, colors.get("background"), 4.5),
        ("foreground/chrome", fg, colors.get("chrome"), 4.5),
        ("foreground/surface", fg, colors.get("surface"), 4.5),
        ("muted/background", muted, colors.get("background"), 4.5),
        ("muted/chrome", muted, colors.get("chrome"), 4.5),
        ("muted/surface", muted, colors.get("surface"), 4.5),
        ("dim/background", dim, colors.get("background"), 2.0),
        ("dim/chrome", dim, colors.get("chrome"), 2.0),
        ("accent/background", accent, colors.get("background"), 4.5),
        ("accent/chrome", accent, colors.get("chrome"), 3.0),
        ("accent_foreground/accent", colors.get("accent_foreground"), accent, 4.5),
        ("solid_foreground/solid", colors.get("solid_foreground"), colors.get("solid"), 4.5),
        ("foreground/selected", fg, colors.get("selected"), 4.5),
        # Latte's official Green is 2.96:1 on Base, just under the 3:1
        # non-text guideline; keep the official value and allow the rounding.
        ("working/background", colors.get("working"), colors.get("background"), 2.9),
        ("blocked/background", colors.get("blocked"), colors.get("background"), 2.9),
        ("done/background", colors.get("done"), colors.get("background"), 2.9),
        ("idle/background", colors.get("idle"), colors.get("background"), 2.0),
        ("unknown/background", colors.get("unknown"), colors.get("background"), 2.0),
        ("ring/background", colors.get("ring"), colors.get("background"), 2.5),
        ("border/background", colors.get("border"), colors.get("background"), 2.0),
    ]
    for label, fg, bg, minimum in checks:
        if fg and bg and contrast(fg, bg) < minimum:
            errors.append(
                f"{flavor}: {label} contrast {contrast(fg, bg):.2f} < {minimum:.1f}"
            )

    return errors


def _is_hex(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 7
        and value[0] == "#"
        and all(c in HEX_DIGITS for c in value[1:].lower())
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the checked-in themes match the generator output",
    )
    args = parser.parse_args()

    errors: list[str] = []
    if not args.check:
        THEMES.mkdir(exist_ok=True)

    for flavor in PALETTE:
        theme = build(flavor)
        errors.extend(validate(flavor, theme))
        path = THEMES / f"catppuccin-{flavor}.json"
        text = render(flavor)

        if args.check:
            if not path.exists():
                errors.append(f"{path.relative_to(ROOT)} is missing")
            elif path.read_text(encoding="utf-8") != text:
                errors.append(f"{path.relative_to(ROOT)} is out of date")
        else:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        print("themes are up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
