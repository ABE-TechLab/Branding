# ABE TechLab Logo Lockups

This guide explains when to use each current logo composition. The files are working identity assets derived from the current geometric mark; they are not yet formally approved master artwork.

## Available compositions

| Composition | Asset | Best use |
| --- | --- | --- |
| Symbol only | [Adaptive symbol SVG](../public/logos/abe-techlab-mark-adaptive.svg) | App icons, avatars, favicons, compact placements |
| Stacked | [Adaptive stacked lockup](../public/logos/abe-techlab-lockup-stacked-adaptive.svg) · [Light PNG](../public/logos/abe-techlab-lockup-stacked-light-v1.png) · [Dark PNG](../public/logos/abe-techlab-lockup-stacked-dark-v1.png) | Centered or vertical layouts, title pages, social graphics |
| Horizontal | [Adaptive horizontal lockup](../public/logos/abe-techlab-lockup-horizontal-adaptive.svg) · [Light PNG](../public/logos/abe-techlab-lockup-horizontal-light-v1.png) · [Dark PNG](../public/logos/abe-techlab-lockup-horizontal-dark-v1.png) | Website headers, footers, navigation, document headers |
| Wordmark only | [Adaptive wordmark](../public/logos/abe-techlab-wordmark-adaptive.svg) · [Light PNG](../public/logos/abe-techlab-wordmark-light-v1.png) · [Dark PNG](../public/logos/abe-techlab-wordmark-dark-v1.png) | Text-led or narrow placements, or where the symbol is already present nearby |

## Theme behavior

All four SVG assets have transparent backgrounds. The main mark and/or lettering is charcoal (`#111111`) in light color schemes and off-white (`#F9F9F6`) in dark color schemes. The geometric symbol's lime accent (`#A7E021`) remains unchanged.

The variants use the CSS `prefers-color-scheme` media feature inside the SVG. They respond to the preferred or inherited color scheme supplied by the browser; they do **not** inspect an arbitrary background color. Use the fixed light/dark symbol PNGs or another explicitly selected fixed-color asset where theme-aware SVG rendering is unsupported or unpredictable.

## Typography

The lockups use an Arial/Helvetica-style system sans-serif treatment: “ABE” is heavier and “TechLab” is medium weight. This is a working typographic treatment, not a formally approved company typeface. Since the SVG keeps the wordmark as live text, exact letterforms can vary slightly by platform depending on the available sans-serif font. For pixel-identical typesetting across every environment, an approved outlined wordmark master would be needed.

## Practical sizing and spacing

- Preserve each SVG's aspect ratio. Scale the complete lockup uniformly; never stretch only the symbol or the wordmark.
- Keep clear space around the outside of the complete lockup. Do not place nearby text or edges tight against it.
- Use the horizontal lockup at a size where the company name remains comfortably readable; switch to the stacked lockup when the horizontal version becomes too small.
- Use the symbol alone for very small placements. Do not shrink a full lockup until the text becomes illegible.
- Avoid adding shadows, gradients, strokes, or effects, and do not recolor the lime accent ad hoc.

## Email and raster use

The adaptive SVGs are intended for websites and other modern browser contexts. Email clients can sanitize SVG and embedded CSS/media queries, so do not assume the adaptive lockups will switch themes reliably in email. Each of the stacked, horizontal, and wordmark compositions now has a fixed-color transparent PNG for light and dark backgrounds. The exports are rendered at 3× their SVG viewBox dimensions: stacked 1560 × 1050, horizontal 2040 × 495, and wordmark 1590 × 336. Choose the PNG variant that matches the actual image background; PNGs do not switch colors automatically.

The source-preserving export process is documented in the repository-root [AGENTS.md](../AGENTS.md), and can be rerun with [`scripts/export_logo_variants.py`](../scripts/export_logo_variants.py). It changes only the `.ink` theme color, keeps the original geometry and accent, and validates dimensions, alpha transparency, and expected colors.

## Asset status

These compositions are working lockups built from the current symbol geometry and an initial system-sans wordmark. Review them in the actual products and placements before treating them as final company standards. When a formal brand typeface or approved master vector becomes available, update the wordmark and all lockups together.
