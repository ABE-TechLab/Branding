# ABE TechLab — Brand Library

The central library for ABE TechLab's visual identity assets, working color values, and practical usage guidance. Keep shared brand files organized here so company profiles, products, and communication materials can use a consistent starting point.

> **Asset status:** The logo SVGs in this repository are working vector approximations copied from the selected visual mark already used on the public GitHub profile. They are not the original editable master artwork, and exact geometry has not been independently verified against a source file. Treat them as current working assets—not as final, trademark-ready master artwork. The color values below reflect the existing SVG implementation and should be considered a working palette until formally approved.

## Quick asset index

| Use case | Asset | Notes |
| --- | --- | --- |
| Light backgrounds | [Light logo SVG](./assets/logos/abe-techlab-mark-light.svg) | Charcoal mark with lime accent; transparent canvas |
| Dark backgrounds | [Dark logo SVG](./assets/logos/abe-techlab-mark-dark.svg) | Off-white mark with lime accent; transparent canvas |
| Adaptive web and portfolio use | [Adaptive logo SVG](./public/logos/abe-techlab-mark-adaptive.svg) | One transparent SVG; charcoal in light schemes and off-white in dark schemes |
| Email and static hosting | [Email-ready light PNG](./public/logos/abe-techlab-mark-light-v1.png) · [Email-ready dark PNG](./public/logos/abe-techlab-mark-dark-v1.png) | Transparent 320 × 255 PNG exports; intended to display at 160 px wide |
| Asset hosting guide | [Email logo assets](./docs/email-logo-assets.md) | Vercel static publishing, stable URLs, adaptive SVG, and email usage |
| Public asset index | [public/index.html](./public/index.html) | Previews and direct links for hosted logo files |
| GitHub profile | [Profile banner SVG](./assets/github/abe-techlab-profile-banner.svg) | 1200 × 320 banner for the organization profile |
| GitHub asset notes | [GitHub assets guide](./assets/github/README.md) | Current public copies and embedding guidance |
| Usage guidelines | [Brand guidelines](./docs/brand-guidelines.md) | Background choice, clear space, sizing, and handling |
| Color specifications | [Color palette](./docs/color-palette.md) | Hex/RGB values and current status |
| Machine-readable tokens | [JSON color tokens](./tokens/brand-colors.json) · [CSS variables](./tokens/brand.css) | Reusable implementation values |

### GitHub profile banner

![ABE TechLab — Ideas into systems. Systems into impact.](./assets/github/abe-techlab-profile-banner.svg)

## Brand colors

These values are read from the current logo and banner assets. They are documented for consistency, not presented as final formal brand approval.

| Token | Hex | Intended role |
| --- | --- | --- |
| Charcoal | `#111111` | Primary dark mark |
| Off-white | `#F9F9F6` | Light mark and text on dark surfaces |
| Lime green | `#A7E021` | Accent |
| Banner charcoal | `#101010` | Current banner background |
| Muted gray | `#B8B8B3` | Banner secondary text |
| Graph gray | `#777A72` | Banner linework |
| Divider charcoal | `#383A35` | Banner divider |

See [Color palette](./docs/color-palette.md) for RGB values and usage notes.

## Logo usage at a glance

- Use the **light variant** on off-white and other light backgrounds.
- Use the **dark variant** on charcoal and other dark backgrounds.
- Use the **adaptive SVG** for websites, portfolio pages, and other modern browser contexts where the SVG is rendered with support for `prefers-color-scheme`. It has a transparent canvas, defaults to the charcoal mark, switches the mark to off-white in dark color schemes, and keeps the lime accent unchanged.
- Use the transparent PNG exports for email clients; retain SVGs as the editable/vector working sources.
- The PNG exports are 320 × 255 pixels and are intended to be displayed at approximately 160 pixels wide.
- Keep lime as an accent and preserve the colors and proportions of the supplied assets.
- Leave clear space around the mark; don't stretch, rotate, crop, or add effects.
- Test contrast and legibility at the actual display size, especially for small icons.
- The SVGs and PNG exports are working representations of the current logo approximation, not independently verified master artwork or trademark-ready assets.
- When the artwork changes, publish a new versioned PNG filename (for example, `-v2.png`) and update the asset guide and downstream references. This avoids stale caches serving an older logo under a reused URL.

The public GitHub portfolio currently uses a `<picture>` element with separate light/dark SVG sources as a conservative fallback. The adaptive SVG is available for contexts that support it, but the existing two-source approach remains the most predictable option for the broadest range of Markdown renderers. See the [public profile README](https://github.com/ABE-TechLab/.github/blob/main/profile/README.md).

## Static asset hosting on Vercel

The `public/` directory is the deployment output for a small static Vercel project. The Branding repository can remain private; Vercel builds/deploys from the connected repository and serves files in `public/` at the deployment root.

Recommended project settings:

| Vercel setting | Value |
| --- | --- |
| Framework Preset | Other |
| Root Directory | `./` |
| Build Command | Disabled / empty |
| Output Directory | `public` |
| Install Command | Disabled / empty |

After the production deployment is ready, the image and SVG files will be available at:

- `https://<production-domain>/logos/abe-techlab-mark-adaptive.svg`
- `https://<production-domain>/logos/abe-techlab-mark-light-v1.png`
- `https://<production-domain>/logos/abe-techlab-mark-dark-v1.png`

Replace `<production-domain>` with the production domain assigned to the Vercel project. Use the project's production domain or a custom domain—not a preview deployment URL, GitHub file-page URL, or tokenized download URL.

The root page (`/`) is a small index with previews and direct links. The exact deployment URL is determined by the Vercel project and domain configuration; it is intentionally not guessed or hardcoded here. Ensure Vercel Deployment Protection is not enabled for these public assets, otherwise email recipients and anonymous image proxies may be unable to fetch them.

See [Email logo assets](./docs/email-logo-assets.md) for the HTML examples and ABEmail configuration notes.

## Repository structure

```text
.
├── README.md
├── assets/
│   ├── github/
│   │   ├── README.md
│   │   └── abe-techlab-profile-banner.svg
│   └── logos/
│       ├── abe-techlab-mark-dark.svg
│       └── abe-techlab-mark-light.svg
├── docs/
│   ├── brand-guidelines.md
│   ├── color-palette.md
│   └── email-logo-assets.md
├── public/
│   ├── index.html
│   └── logos/
│       ├── abe-techlab-mark-adaptive.svg
│       ├── abe-techlab-mark-dark-v1.png
│       └── abe-techlab-mark-light-v1.png
└── tokens/
    ├── brand-colors.json
    └── brand.css
```

## Reuse the CSS tokens

Import or copy the tokens from [`tokens/brand.css`](./tokens/brand.css) into a compatible web project. If the values change after brand review, update the CSS, JSON, palette document, and any dependent assets in the same change.

```css
@import "./brand.css";

.brand-surface {
  background: var(--abe-color-charcoal);
  color: var(--abe-color-off-white);
}

.brand-accent {
  color: var(--abe-color-lime);
}
```

## Public and private asset locations

This repository is the **private working brand library**. Its `public/` directory is published by the separate Vercel static project; "public" here describes the deployment output, not the GitHub repository's visibility. The public GitHub organization profile also has its own copies in [`ABE-TechLab/.github`](https://github.com/ABE-TechLab/.github/tree/main/profile/assets). Keep those copies synchronized when the working assets change; don't link public README images directly to private files.

## Updating the brand library

1. Confirm the source and intended use of a proposed asset.
2. Preserve the previous file until the replacement has been reviewed.
3. Update the asset inventory, usage guidance, and token files when relevant.
4. Check light and dark backgrounds, contrast, and small-size legibility.
5. Copy approved public assets to `ABE-TechLab/.github` only when they are intended for public display.
6. Be clear about what is working draft versus formally approved.

No separate redistribution license is declared by this repository at present. Do not assume the assets are licensed for third-party redistribution.
