# ABE Product Brand Asset Agent Instructions

These instructions govern agents and contributors creating, editing, exporting, documenting, or publishing brand assets for **any ABE TechLab product or company surface**. The goal is one traceable, controlled source of truth for every logo, wordmark, icon, color token, and other brand asset that appears online.

## 1. Core responsibility

Act as a brand-asset custodian, not an unconstrained logo generator. Preserve the approved identity and make production-ready derivatives from verified source artwork. Do not invent, redraw, simplify, recolor, or "improve" an existing mark merely to make a task easier.

The parent-company identity and each product identity are separate. Do not automatically apply the ABE TechLab corporate logo, palette, typography, or visual style to ABEmail, TechTrack, Forge, or another product unless that product's own brand record explicitly says to do so.

## 2. Source-of-truth and provenance

1. Before editing, identify the exact brand and product. Inspect its brand manifest, source files, guidelines, and existing exports.
2. Use the canonical source artwork from the controlled ABE branding library. Prefer an original editable vector (SVG, PDF, EPS, or design-source export) over a PNG, screenshot, website preview, GitHub rendered image, or copied image URL.
3. Record the source path, source revision/commit, asset owner, usage rights, and approval status. Preserve the original source unchanged.
4. If the original source artwork is unavailable, conflicting, low-resolution, unlicensed, or of uncertain ownership, stop and report the gap. Do not silently trace or approximate it and label the result official.
5. Never use a temporary, expiring, signed, tokenized, preview-deployment, or GitHub blob-page URL as a production image source. Use the approved stable production asset host and exact file path.
6. Treat `draft`, `review`, `approved`, and `deprecated` as distinct asset states. Only explicitly approved assets may be described or deployed as official. A technical export does not grant brand approval.

## 3. Expected brand package for each product

For each product, maintain a product-specific record under the central library's `brands/<product-slug>/` area as that product is onboarded. Do not move or rename existing assets as part of an unrelated task. A product package should contain:

- `brand.json`: product name/slug, owner, status, approved source revision, brand tokens, canonical production asset origin, asset inventory, and approval metadata.
- `source/`: immutable, original editable logo artwork and the source files from which derivatives are made.
- `logos/svg/`: vector working masters and supported adaptive/fixed-color SVG variants.
- `logos/png/`: fixed-color raster exports for light and dark backgrounds, with transparent backgrounds wherever the design permits.
- `tokens/`: machine-readable and developer-friendly color tokens; record names, HEX, RGB, semantic roles, and status.
- `README.md`: inventory, usage rules, direct stable asset links, status, and contact/owner information.

Use the existing ABE TechLab paths and naming where they already exist. Apply this package layout to new product brands or deliberate migrations; do not reorganize the existing library just for consistency.

## 4. Required design variants

Create only the variants that are supported by the product's approved source artwork. For a full logo system, assess:

- Symbol/mark only.
- Stacked lockup (symbol above wordmark).
- Horizontal lockup (symbol beside wordmark).
- Wordmark only.
- Product-specific app icon or favicon where required.

For each applicable composition, consider:

- Adaptive SVG for compatible browser contexts, only where the artwork can change color safely through `prefers-color-scheme`.
- Fixed light-background version: dark/charcoal foreground on a transparent canvas.
- Fixed dark-background version: light/off-white foreground on a transparent canvas.
- PNG exports for both fixed color treatments. Email clients and platforms that sanitize SVG/CSS must not depend on adaptive SVG behavior.

A logo with transparency does not detect the color of the page or email section behind it. `prefers-color-scheme` follows the user's/browser's preferred color scheme; it is not a guarantee that the logo matches an arbitrary element background. Use an explicitly selected light or dark asset when the surface is known.

## 5. Precision-preserving asset workflow

Follow this sequence for every asset task:

1. **Audit:** inspect the repository tree, brand manifest, source artwork, existing variants, current embedding locations, and any related product implementation. Preserve good existing work.
2. **Establish the master:** select the exact approved vector source and record its revision. Confirm the viewBox/artboard, intrinsic proportions, transparent canvas, and expected colors. Do not edit the geometry unless the request explicitly includes a logo-design change and the authorized owner approves it.
3. **Build compositions:** make stacked, horizontal, symbol-only, or wordmark-only lockups from the same approved paths and approved typography. Maintain alignment, proportions, clear space, and consistent optical scale. Never recreate the symbol independently for different variants.
4. **Handle type deliberately:** use the approved font and licensing. When a wordmark must be identical across systems, use approved outlined/path-based letterforms. If live text is retained, disclose the font fallback behavior; do not claim pixel-identical output.
5. **Create adaptive SVG:** preserve paths and viewBox. Use transparent backgrounds and a small, documented set of theme tokens. Keep accent colors unchanged unless the brand spec says otherwise. Test the SVG as an external image and inline asset in the target browsers; support differs by context.
6. **Render fixed PNGs:** render directly from the approved vector source (not from a screenshot or a small PNG) at a deliberate high resolution. Use a consistent export scale—3× the SVG viewBox dimensions is the default for this library unless the target platform requires another size. Pin only the intended foreground color for each variant; retain the exact geometry, viewBox proportions, alignment, and transparent background. Do not crop, stretch, warp, redraw, add shadows, or add a background.
7. **Name and version:** use descriptive, predictable filenames such as `product-logo-horizontal-light-v1.png` and `product-logo-horizontal-dark-v1.png`. Keep the matching SVG and PNG names logically related. Never overwrite a published versioned filename with different artwork; increment the version.
8. **Document:** update the inventory, README, brand guidelines, product manifest, and public asset index in the same change. Explain which format is appropriate for websites, apps, documents, and email.
9. **Review:** compare all variants side-by-side at actual use sizes on both light and dark backgrounds. Request human brand approval where required.
10. **Publish:** merge through the repository's normal review process, deploy the static asset host, and verify every canonical URL from an unauthenticated context.

## 6. Raster export requirements and validation

For every newly rendered PNG:

- Keep an alpha channel and confirm that the background is genuinely transparent—not a white, black, or checkerboard fill.
- When a request explicitly requires a fixed background, create a separately named opaque-background family instead of changing the transparent exports. Confirm alpha is 255 for every pixel and verify the canvas color exactly against the documented background token.
- Confirm the expected canvas dimensions and aspect ratio against the source viewBox and export scale.
- Confirm that the dark asset uses the specified light foreground and that the light asset uses the specified dark foreground. Keep accent colors exactly on-token.
- Inspect anti-aliased edges, clear space, alignment, baseline, and clipping. Confirm the entire mark and wordmark are inside the canvas.
- Open the actual exported files. Do not rely on the renderer's success code alone.
- Composite a preview against a representative light surface and dark surface to check contrast; do not save the composite preview as the production logo.
- Verify that each PNG can be decoded and that its file type is PNG. The exporter uses a transparent indexed palette of up to 256 colors to keep the web assets efficient; this was visually checked against the full RGBA render. Use `--palette-colors 0` for a full RGBA export. Do not reduce the palette further without checking visual fidelity.
- Where email use is intended, also test a realistic email signature/message layout, fixed image dimensions, and remote image loading. Do not claim that a recipient's email client will display externally hosted images when that client blocks remote images.

## 7. Reproducible export tooling

Use `scripts/export_logo_variants.py` for the current adaptive SVG convention in this repository. It:

- Reads the existing adaptive SVG master without changing it.
- Creates separate light and dark PNGs by pinning the `.ink` color while retaining all vector paths, typography, accent shapes, and transparent canvas.
- Uses CairoSVG for rendering and Pillow for file validation and a 256-entry transparent PNG palette.
- Defaults to 3× viewBox dimensions and versioned PNG filenames; use `--palette-colors 0` to retain a full RGBA export.

Install the documented Python dependencies before running it. Inspect each output. If a source uses a different SVG structure, CSS convention, embedded image, font, filter, or mask, adapt the exporter deliberately and add a regression check; do not force a lossy conversion through a pattern it does not support.

## 8. Stable public asset hosting and product integration

1. Publish production assets from the controlled Branding repository through the designated production static host (currently the ABE Branding Vercel project). Keep the canonical production domain documented in the library.
2. Use the stable production domain and a versioned path. Do not embed Vercel preview URLs, temporary deployment URLs, GitHub file-page links, signed URLs, or expiring storage links in product code, email signatures, or public pages.
3. Keep the asset host publicly readable for public brand assets. Verify that Vercel Deployment Protection, authentication, hotlink restrictions, or access rules do not block anonymous recipients.
4. Use the correct MIME type (`image/svg+xml` or `image/png`) and verify successful HTTP responses after deployment. A link opening in an authenticated browser is not sufficient validation.
5. In HTML, provide descriptive `alt` text, explicit width/height or an aspect-ratio constraint, and responsive sizing. In email, use fixed-color PNGs and explicit pixel dimensions; do not rely on SVG, CSS media queries, or remote font downloads for critical branding.
6. A product must reference its own brand package and its approved asset paths. Do not hotlink a different ABE product's mark or copy an unreviewed asset into the product repository.
7. When an asset changes, publish a new versioned path and update all consuming products in a reviewed change. Keep a record of the old version and its migration status.

## 9. Security, licensing, and change control

- Do not fetch logo artwork from arbitrary external URLs or use third-party brand marks without recorded permission and license review.
- Do not include credentials, private links, signed URLs, or non-public source files in a public asset index.
- Check SVGs for unexpected scripts, event handlers, foreign objects, external references, embedded trackers, and untrusted content before publication. Keep published SVGs static and self-contained.
- Use pull requests for source artwork, token, manifest, and public asset changes. Keep an auditable history and require owner approval before changing approved identity assets.
- Compute and record SHA-256 checksums for released masters and exports when reproducible provenance is required.
- Do not state that an asset is legally cleared, trademark-ready, or formally approved unless that status is explicitly recorded by the responsible owner.

## 10. Definition of done

A brand-asset task is complete only when:

- The source asset and its provenance are known.
- The required SVG and/or PNG variants exist, preserve the approved design, and pass visual and technical validation.
- Light and dark treatments, transparency, sizing, and use cases are documented.
- The product/brand manifest and asset inventory point to the correct files.
- All consuming references use the canonical stable production origin and correct format.
- The production deployment is ready and each required asset URL has been verified without authentication.
- The change has the required human approval and no unverified asset is represented as official.

If any item cannot be verified, report it explicitly as incomplete rather than claiming the brand asset is ready.


### Explicit opaque-background exports

The transparent PNG family remains the default. When the asset owner explicitly requests a fixed background, use scripts/export_logo_background_variants.py to create a separate opaque family from the existing adaptive SVG sources. The current ABE TechLab package includes white (#FFFFFF), black (#000000), and lemon (#A7E021) backgrounds for the mark, stacked lockup, horizontal lockup, and wordmark. These files must be fully opaque; they must not replace or be confused with the transparent exports. The lemon-background symbol treatment uses the existing off-white brand token for its small accent detail to maintain visibility.
