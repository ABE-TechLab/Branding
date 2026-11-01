# ABEmail Brand Assets

The dedicated source of truth for the ABEmail product identity.

**Tagline:** (No tagline is included in the supplied Concept 1 logo artwork.)

## Source artwork

Nine original Concept 1 SVGs are preserved unchanged in [source/](./source/). They provide symbol, horizontal, and stacked compositions in light, dark, and monochrome treatments.

The artwork contains real SVG paths and no embedded raster images. The ABEmail wordmark remains editable live text in Inter Bold; the exporter creates a wordmark-only composition by extracting that text element from the horizontal source. For consistent PNG output, the automated workflow installs Inter before rendering. SVG consumers should make Inter available to retain the intended wordmark metrics.

## Exports

Generated outputs live in [logos/svg/](./logos/svg/) and [logos/png/](./logos/png/).

- Vector SVGs: symbol, horizontal, stacked, and wordmark-only compositions in light, dark, and monochrome treatments.
- Transparent PNGs: all compositions and all three treatments, rendered at 4× the source viewBox dimensions.
- Opaque PNGs: all four compositions on white (#FFFFFF), black (#000000), and lemon (#FFC93D) backgrounds, rendered at 4×.
- The opaque PNGs include their full background and are not transparent.

## Colour tokens

| Token | HEX | Use |
|---|---|---|
| Deep teal | #0C2E34 | Primary dark lettering and symbol |
| Mint green | #72E3AD | Brand accent |
| White | #FFFFFF | Dark-surface mark and accent |

The dark source SVG uses white for the secondary mark detail and lettering, with the mint accent retained. Monochrome versions use deep teal as a single foreground colour.

## Status

- Brand asset status: **review**.
- Formal approval: pending.
- SVG path geometry: preserved from supplied source.
- Wordmark: live Inter text, not outlined paths.
- Rights and redistribution review: not recorded.

A successful export or merge does not represent formal brand approval. See [brand.json](./brand.json) for machine-readable tokens and approval state.
