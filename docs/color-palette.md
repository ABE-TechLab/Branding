# ABE TechLab Color Palette

This is the **current working palette observed in the existing GitHub logo and banner SVGs**. It documents implementation values for consistency; it is not a claim that a final corporate design system has been formally ratified.

## Core brand colors

These are the three primary identity colors. The HEX values are written in copy-ready form; RGB values are included for tools and workflows that request RGB rather than HEX.

| Name | HEX (copy-ready) | RGB | Current use |
| --- | --- | --- | --- |
| Lime green | `#A7E021` | `167, 224, 33` | Brand accent and visual highlight |
| Charcoal | `#111111` | `17, 17, 17` | Primary dark mark and text on light backgrounds |
| Off-white | `#F9F9F6` | `249, 249, 246` | Light mark on dark backgrounds; light-surface text |

### Copy-ready CSS

```css
:root {
  --abe-color-lime: #A7E021;
  --abe-color-charcoal: #111111;
  --abe-color-off-white: #F9F9F6;
}
```

For a machine-readable source, use [`tokens/brand-colors.json`](../tokens/brand-colors.json). The matching CSS custom properties already exist in [`tokens/brand.css`](../tokens/brand.css).

## Banner support colors

These colors are used in the existing profile banner as supporting colors. They are not separate core identity colors.

| Name | Hex | RGB | Use |
| --- | --- | --- | --- |
| Banner charcoal | `#101010` | 16, 16, 16 | Banner background |
| Muted gray | `#B8B8B3` | 184, 184, 179 | Supporting banner descriptor |
| Graph gray | `#777A72` | 119, 122, 114 | Geometric banner lines |
| Divider charcoal | `#383A35` | 56, 58, 53 | Subtle banner divider |

## Usage guidance

- Use charcoal for primary text and dark logo artwork on light surfaces.
- Use off-white for text and light logo artwork on dark surfaces.
- Use lime as a small, high-recognition accent.
- Do not rely on lime alone for small text on off-white; use charcoal text for readability.
- Test contrast and legibility in the actual component or output context.
- Do not infer semantic status colors (success, warning, error) from the brand palette.

## Design tokens

Machine-readable values are stored in [`tokens/brand-colors.json`](../tokens/brand-colors.json), and CSS custom properties are in [`tokens/brand.css`](../tokens/brand.css).

The [public asset page](../public/index.html) also shows the three core colors with copy buttons for their HEX values.

If a value changes in an approved source asset, update both token files, this document, and the public asset page in the same change.
