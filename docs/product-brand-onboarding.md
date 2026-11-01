# Onboard a Product Brand

This repository is the central source of truth for ABE TechLab and product brand assets. Each product has its own identity record; sharing an organization does not imply sharing a product's logo, palette, typography, or visual language.

## Create a product brand record

1. Create `brands/<product-slug>/` in this repository.
2. Copy [`templates/product-brand-manifest.json`](../templates/product-brand-manifest.json) to `brands/<product-slug>/brand.json` and replace every placeholder with verified product data.
3. Add the original editable master artwork under `source/`. Keep it unchanged and record its originating file, source revision, owner, and license/permission status.
4. Add reviewed SVGs under `logos/svg/`, fixed light/dark PNGs under `logos/png/`, color tokens under `tokens/`, and a short product `README.md`.
5. Keep `status` as `draft` or `review` until the responsible product/brand owner records approval. Do not infer approval from a merged pull request or successful deployment.
6. Review the logo at intended sizes, on both light and dark surfaces, and in the actual product placements. Check both raster and vector files, including transparency and clipping.
7. Publish the approved public assets through the designated production brand host. Record the canonical production origin and exact versioned file paths in the manifest.
8. Update consuming products to reference those stable production paths. Do not embed preview deployment URLs, raw repository file pages, signed URLs, or temporary upload links.

## Product integration rules

- Product repositories should reference this central brand package and must not become a competing source of truth.
- Do not copy brand files into product repositories unless there is a documented build/distribution reason. If copies are required, record the source revision and add a verification/synchronization step.
- Product sites, mailers, documentation, social graphics, and dashboards must use only files listed in the product's current brand manifest.
- Use fixed-color transparent PNGs for email and clients that do not reliably display SVG. Use adaptive SVG only where the target browser and embedding method have been tested.
- If a product needs a new logo composition, create it from the approved master and submit it for human review before publication.

## Approval and release

A product brand is not `approved` merely because source files exist. The manifest must identify the approver and approval date, rights/ownership must be confirmed, the required light/dark variants must pass checks, and each public URL must be reachable anonymously. Keep the previous released version available when publishing a new version so products can migrate without broken references.
