# TechTrack — owner-reviewed reconstructed vector package

**Status:** owner-reviewed with one explicit exclusion. The transparent, white-background and lemon-background reconstructions have been reviewed and accepted for use. The black-background reconstruction is deferred; use the transparent version on black or dark surfaces. **Provenance:** `vector-reconstructed-from-raster` — these are derived vector paths, not the original designer master artwork. These SVG paths are **not** the original vector masters. The original raster-backed SVGs in `source/` are immutable references; the original uploads in `brands/techtrack/source/` have not been changed.

## Brand essentials

- Brand: TechTrack
- Tagline (outlined in SVG paths): **Skills Today. Opportunities Tomorrow.**
- Palette (reference approximations): cyan `#03A6FC`, blue `#0464FA`, teal `#02C9AC`, navy `#041B45`, white `#FFFFFF`, black `#000000`, lemon `#FFC93D`, Kids orange `#FB693A` and yellow `#FCCA38` where applicable.
- Core compositions: `mark` (symbol), `stacked`, `horizontal`, `wordmark` (full brand lettering + tagline).
- Each composition has SVG variants named `<brand>-<composition>-white|lemon-v1.svg` under [`logos/reconstructed/svg/`](logos/svg/), plus a transparent base under [`vector/`](vector/).
- PNG files are under [`logos/reconstructed/png/`](logos/png/): `512` pixel width for marks only, plus `1024`, `2048`, and `4096` pixel widths for all compositions (preserving viewBox proportions). Transparent, white and lemon backgrounds are separate files. No black-background reconstruction is published.

## Source audit

| Composition | Reference SVG | Original artboard | SHA-256 |
| --- | --- | --- | --- |
| mark | [`techtrack-mark-bg-white-v1.svg`](source/techtrack-mark-bg-white-v1.svg) | 0 0 471 435 | `01fdbfa4f87a5b5189dca51afcceedd88861fed72f962da6d8598f937b351616` |
| stacked | [`techtrack-lockup-stacked-bg-white-v1.svg`](source/techtrack-lockup-stacked-bg-white-v1.svg) | 0 0 1113 756 | `5f3a6c2bbbaaf5146019231e293c2b737255cf1299174b8b9b8b5a77cb2bd141` |
| horizontal | [`techtrack-lockup-horizontal-bg-black-v1.svg`](source/techtrack-lockup-horizontal-bg-black-v1.svg) | 0 0 1596 435 | `2426fd97f46c2a84eb1ce2551ec0239d7f762059fb75304deb93876b7ba1ec25` |
| wordmark | [`techtrack-wordmark-bg-lemon-v1.svg`](source/techtrack-wordmark-bg-lemon-v1.svg) | 0 0 1113 348 | `e6fed8ac614f408624fbc05d4e8f0b208f4174b731d061d0a6be13c6ebe59e84` |

Full inventory, SHA-256 hashes of all original images and embedded PNGs, original SVG and image sizes, reconstruction status, and individual SVG/PNG paths: [`brand.json`](brand.json).

## Fidelity and review limitations

The shapes are smoothed silhouettes traced from the original raster image and all letterforms are path outlines (not substitute typefaces). They preserve visible layout, but These files remain raster-derived reconstructions rather than original designer vectors, so the exact original control points and all subtle raster edge details cannot be recovered. The owner-reviewed transparent, white and lemon treatments are the usable set. The black-background treatment is deliberately excluded until its contrast and detail issues are corrected. The lemon Kids treatment switches yellow details to the original orange accent for contrast.

Do not describe these reconstructions as the original designer masters. Use the transparent asset on black or dark surfaces. The source files are unchanged. Reproduce the reviewed package by running `python scripts/reconstruct_techtrack.py --root .`, then `python scripts/validate_techtrack.py`.
