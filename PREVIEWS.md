# Preview images

The files in `assets/` are screenshots of Herdr. They are illustrative: the
space names, pane header, file sizes, font, and demo content are not part of
the themes.

## Requirements

- A running Herdr app.
- Python 3 and [Pillow](https://python-pillow.org/) for the build step:
  `python3 -m pip install Pillow`
- A maximized Herdr window. The build step resizes screenshots to 1920x1040.

## Rebuild the previews

1. In Herdr, open a terminal in this repository and run the demo screen for a
   flavor:

   ```sh
   python3 scripts/preview_screen.py latte
   ```

   Replace `latte` with `frappe`, `macchiato`, or `mocha`.

2. Apply the matching theme and appearance:

   ```sh
   herdr-app do app.theme --name catppuccin-latte
   ```

   For Latte, set `"appearance": "light"` in `settings.json`. For the dark
   flavors, set `"appearance": "dark"`.

3. Save a screenshot:

   ```sh
   herdr-app shot /tmp/preview-latte.png
   ```

4. Repeat steps 1-3 for `frappe`, `macchiato`, and `mocha`.

5. Build the individual WebP files and the composite:

   ```sh
   python3 scripts/build_previews.py \
       /tmp/preview-latte.png \
       /tmp/preview-frappe.png \
       /tmp/preview-macchiato.png \
       /tmp/preview-mocha.png
   ```

The script writes `assets/latte.webp`, `assets/frappe.webp`,
`assets/macchiato.webp`, `assets/mocha.webp`, and `assets/preview.webp`.
