# ABE TechLab Brand Usage Guidelines

These guidelines describe how to use the current working brand assets consistently. They are intentionally conservative while the primary logo artwork and full visual system await formal approval.

## Asset status

The light and dark logo SVGs in `assets/logos/` are **working vector approximations** of the ABE symbol selected from a visual reference. They were copied from the public organization-profile assets and are not the original editable master artwork. Their geometry may not match the reference exactly at every curve or edge.

Use them for internal previews and current GitHub profile needs where appropriate. Do not describe them as final, trademark-ready, or pixel-perfect master artwork. Replace them with approved source artwork when it becomes available.

The profile banner is a designed SVG currently used for GitHub profile presentation. It is an application asset, not a substitute for a formal logo master.

## Logo variants

| Asset | Intended background | Foreground |
| --- | --- | --- |
| [Light mark](../assets/logos/abe-techlab-mark-light.svg) | Off-white or other light backgrounds | Charcoal + lime |
| [Dark mark](../assets/logos/abe-techlab-mark-dark.svg) | Charcoal or other dark backgrounds | Off-white + lime |
| [Stacked lockup](../public/logos/abe-techlab-lockup-stacked-adaptive.svg) | Centered and vertical placements | Adaptive charcoal/off-white wordmark + symbol; lime accent |
| [Horizontal lockup](../public/logos/abe-techlab-lockup-horizontal-adaptive.svg) | Website headers, navigation, footers, document headers | Adaptive charcoal/off-white wordmark + symbol; lime accent |
| [Wordmark only](../public/logos/abe-techlab-wordmark-adaptive.svg) | Text-led or narrow placements | Adaptive charcoal/off-white wordmark |
| [Adaptive symbol](../public/logos/abe-techlab-mark-adaptive.svg) | Compact placements, app icons, avatars | Adaptive charcoal/off-white symbol + lime accent |
| [GitHub profile banner](../assets/github/abe-techlab-profile-banner.svg) | Banner/header placements | Charcoal, off-white, lime, supporting gray |

The names “light” and “dark” refer to the background use case. Select the file that maintains strong contrast with the surface. For websites and other compatible browser contexts, the adaptive SVGs use `prefers-color-scheme`; see [Logo lockups](./logo-lockups.md) for selection guidance and browser/email limitations.

## Clear space and sizing

- Leave visible breathing room around the mark; do not crowd it with text, edges, or other graphic elements.
- Preserve the aspect ratio. Scale the entire SVG uniformly rather than stretching it.
- For small placements such as favicons or tiny avatars, test legibility at the actual output size before publishing.
- No official minimum size has been established. Do not treat an arbitrary pixel threshold as an approved rule.

## Color use

- Use charcoal on light surfaces and off-white on dark surfaces.
- Treat lime as a focused accent, not as a replacement for body text or the primary mark color.
- Avoid low-contrast lime text on off-white surfaces.
- Keep supporting banner grays within the banner's visual system unless a broader palette decision is approved.
- Use only the supplied variants for current uses. Do not recolor the SVG paths ad hoc.
- Select the stacked or horizontal lockup according to the available space; do not rebuild the wordmark from separate text in a product interface.

See [Color palette](./color-palette.md) for current implementation values and their status.

## Do

- Use the relevant light or dark variant.
- Keep the mark intact and proportionally scaled.
- Keep backgrounds simple and contrast strong.
- Prefer SVG for web and digital use where supported.
- Keep a copy of the source SVG when preparing raster exports.

## Do not

- Stretch, rotate, skew, crop, or redraw the mark.
- Add shadows, glows, gradients, outlines, or other effects to the symbol.
- Recolor individual parts or change the lime accent without a deliberate brand decision.
- Use the logo over visually busy content without a suitable clear area.
- Claim the current approximated SVG is the final master artwork.
- Label the current wordmark or lockup files “final”, “official”, or “approved” without company review.

## Typography

The current lockups use an Arial/Helvetica-style system sans-serif treatment, with “ABE” in a heavier weight and “TechLab” in a medium weight. This is a practical working treatment, not a ratified company typeface or typography scale. The SVG uses live text, so the viewer's available sans-serif font may affect exact glyph shapes and spacing slightly.

## Contributions and change control

When adding or replacing brand assets:

1. Preserve the previous source until the replacement is reviewed.
2. Record the intended use, background, color values, and source or approval context.
3. Update the asset inventory and README links.
4. Review the asset in light and dark backgrounds and at small sizes.
5. Do not label a file “official” or “approved” unless the company has explicitly approved it.
