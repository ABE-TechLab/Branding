# ABE TechLab — Opaque Logo Background PNGs

This set contains 12 normal, fully opaque PNG images. Unlike the existing transparent PNG exports, each image includes its own complete background and is ready to place as a single image.

The compositions come directly from the existing adaptive SVG files. Their paths, proportions, composition, and live wordmark layout are preserved; the source SVGs are not modified.

## Complete asset set

| Composition | White background | Black background | Lemon background |
| --- | --- | --- | --- |
| Symbol only | [PNG](../public/logos/abe-techlab-mark-bg-white-v1.png) | [PNG](../public/logos/abe-techlab-mark-bg-black-v1.png) | [PNG](../public/logos/abe-techlab-mark-bg-lemon-v1.png) |
| Stacked lockup (symbol above name) | [PNG](../public/logos/abe-techlab-lockup-stacked-bg-white-v1.png) | [PNG](../public/logos/abe-techlab-lockup-stacked-bg-black-v1.png) | [PNG](../public/logos/abe-techlab-lockup-stacked-bg-lemon-v1.png) |
| Horizontal lockup (symbol beside name) | [PNG](../public/logos/abe-techlab-lockup-horizontal-bg-white-v1.png) | [PNG](../public/logos/abe-techlab-lockup-horizontal-bg-black-v1.png) | [PNG](../public/logos/abe-techlab-lockup-horizontal-bg-lemon-v1.png) |
| Wordmark only | [PNG](../public/logos/abe-techlab-wordmark-bg-white-v1.png) | [PNG](../public/logos/abe-techlab-wordmark-bg-black-v1.png) | [PNG](../public/logos/abe-techlab-wordmark-bg-lemon-v1.png) |

## Background and foreground treatments

| Background | Canvas color | Main mark / lettering | Symbol accent |
| --- | --- | --- | --- |
| White | #FFFFFF | Charcoal #111111 | Lime #A7E021 |
| Black | #000000 | Off-white #F9F9F6 | Lime #A7E021 |
| Lemon | #A7E021 | Charcoal #111111 | Off-white #F9F9F6 |

The lemon version uses the existing off-white token for the symbol's small accent component. Keeping the lime accent on a lime canvas would make that portion disappear. The wordmark-only composition has no symbol accent.

## Export dimensions

Exports follow the library's 3× viewBox rendering scale:

| Composition | PNG dimensions |
| --- | ---: |
| Symbol only | 2439 × 1941 |
| Stacked lockup | 1560 × 1050 |
| Horizontal lockup | 2040 × 495 |
| Wordmark only | 1590 × 336 |

Every image is validated as a PNG with an alpha value of 255 at every pixel, the expected canvas dimensions, an exact background color, and the expected solid foreground and accent colors.

## Usage

- Use these files when the image should carry its own fixed white, black, or lemon background.
- Do not place them on another colored surface expecting transparency; these files are deliberately opaque.
- Use the existing transparent PNGs or SVG masters when the destination needs to blend into a surrounding surface.
- For email, choose the exact background treatment that matches the message or signature block. Email clients may block externally hosted images, so keep meaningful text in the message as well.

## Reproducible export

Run from the repository root:

\`\`\`bash
python -m pip install -r scripts/requirements-brand-assets.txt
python scripts/export_logo_background_variants.py --output-dir public/logos
\`\`\`

The pull-request workflow regenerates the 12 images and compares them byte-for-byte with the committed files.

## Asset status and provenance

These are reproducible derivatives of the current working ABE TechLab SVG identity in public/logos/. The repository currently describes those vectors as working approximations rather than independently verified original master artwork. This export does not upgrade their approval status, establish trademark clearance, or certify exact fidelity to an unavailable original design source. Human brand review remains required before the set is treated as formally approved.
