# TechTrack Kids — draft reconstructed vectors

**Provenance:** `vector-reconstructed-from-raster`. **Approval:** pending visual/designer review. These SVG paths are **not** the original vector masters. The original raster-backed SVGs in `source/` are immutable references; the original uploads in `brands/techtrack/source/` have not been changed.

## Brand essentials

- Brand: TechTrack Kids
- Tagline (outlined in SVG paths): **Learn. Play. Create.**
- Palette (reference approximations): cyan `#03A6FC`, blue `#0464FA`, teal `#02C9AC`, navy `#041B45`, white `#FFFFFF`, black `#000000`, lemon `#FFC93D`, Kids orange `#FB693A` and yellow `#FCCA38` where applicable.
- Core compositions: `mark` (symbol), `stacked`, `horizontal`, `wordmark` (full brand lettering + tagline).
- Each composition has SVG variants named `<brand>-<composition>-white|black|lemon-v1.svg` under [`logos/svg/`](logos/svg/), plus a transparent base under [`vector/`](vector/).
- PNG files are under [`logos/png/`](logos/png/): `512` pixel width for marks only, plus `1024`, `2048`, and `4096` pixel widths for all compositions (preserving viewBox proportions). Transparent and white, black and lemon backgrounds are separate files.

## Source audit

| Composition | Reference SVG | Original artboard | SHA-256 |
| --- | --- | --- | --- |
| mark | [`techtrack-kids-mark-bg-white-v1.svg`](source/techtrack-kids-mark-bg-white-v1.svg) | 0 0 447 423 | `3605dd5f359a0da8734acb4a834f70e224ec0545a7412f903bc9917a188612dc` |
| stacked | [`techtrack-kids-lockup-stacked-bg-white-v1.svg`](source/techtrack-kids-lockup-stacked-bg-white-v1.svg) | 0 0 975 960 | `95aff0d9053966db4333d8857d4a7a4b3b2e97c154d4ac3d4c66509ed9e52317` |
| horizontal | [`techtrack-kids-lockup-horizontal-bg-black-v1.svg`](source/techtrack-kids-lockup-horizontal-bg-black-v1.svg) | 0 0 1434 534 | `770de09f91a7a6457a215e2cf5c3a3d19afe80fa43f1324b3734938e1dd4b47c` |
| wordmark | [`techtrack-kids-wordmark-bg-lemon-v1.svg`](source/techtrack-kids-wordmark-bg-lemon-v1.svg) | 0 0 975 534 | `1e7cb6c0ba11452b3782a155afde3683ef6d25a93bad2a59b6e019df4ea23916` |

Full inventory, SHA-256 hashes of all original images and embedded PNGs, original SVG and image sizes, reconstruction status, and individual SVG/PNG paths: [`brand.json`](brand.json).

## Fidelity and review limitations

The shapes are smoothed silhouettes traced from the original raster image and all letterforms are path outlines (not substitute typefaces). They preserve visible layout, but **cannot exactly reproduce** the designer's hidden Bézier handles, banded/cellular gradient detail, tiny edge anti-aliasing, and some interior cyan/teal shapes of the symbol. Gradients are reconstructed from visible reference colors. Small tagline stroke weight differs from source in comparisons; zoomed inspection and manual designer refinement are still required. The lemon Kids treatment deliberately switches yellow details to the original orange accent for contrast.

Do not publish these as approved originals. Review [`TechTrack_Visual_Contact_Sheet.png`](../../TechTrack_Visual_Contact_Sheet.png), the source-to-vector comparisons, and pass `python validate.py` before requesting owner sign-off. Reproduce by running `python reconstruct.py --root .`, then `python validate.py`.
