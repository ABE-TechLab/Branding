#!/usr/bin/env python3
"""Generate the unified ABE TechLab product brand library and individual asset pages."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = {
    "abe-techlab": {
        "name": "ABE TechLab", "kind": "Company identity",
        "intro": "The parent-company identity and shared visual foundation for ABE TechLab products.",
        "accent": "#A7E021", "status": "WORKING BRAND ASSETS",
        "compositions": ["mark", "lockup-stacked", "lockup-horizontal", "wordmark"],
        "variants": ["adaptive", "light", "dark"],
        "type": "abe",
        "notes": "The available source contains standalone light and dark mark artwork. The public library also includes working adaptive lockups and wordmark variants. They remain subject to final master-artwork verification.",
    },
    "abemail": {
        "name": "ABEmail", "kind": "Product identity",
        "intro": "The ABEmail identity, rendered directly from its supplied editable vector SVG artwork.",
        "accent": "#72E3AD", "status": "VECTOR SOURCE · REVIEW PENDING",
        "compositions": ["symbol", "stacked", "horizontal", "wordmark"],
        "variants": ["white", "black", "lemon", "light", "dark", "monochrome"],
        "type": "abemail",
        "notes": "ABEmail source files contain real SVG vector paths. The wordmark remains live Inter text; keep Inter available for consistent SVG rendering. PNG exports are rendered from vector source at 4×.",
    },
    "techtrack": {
        "name": "TechTrack", "kind": "Product identity",
        "intro": "Skills Today. Opportunities Tomorrow. The standard TechTrack ecosystem and its original colour system.",
        "accent": "#1264F3", "status": "RASTER SOURCE · VECTOR RECONSTRUCTION PENDING",
        "compositions": ["mark", "stacked", "horizontal", "wordmark"],
        "variants": ["white", "black", "lemon", "transparent"],
        "type": "raster",
        "notes": "The uploaded SVG files wrap embedded PNGs and are not editable vector masters. Current PNG variants preserve the source pixels; 2× exports are interpolation only.",
    },
    "techtrack-kids": {
        "name": "TechTrack Kids", "kind": "Product identity",
        "intro": "Learn. Play. Create. A separate identity for the TechTrack Kids ecosystem, with its own multicolour lettering and palette.",
        "accent": "#885CF6", "status": "RASTER SOURCE · VECTOR RECONSTRUCTION PENDING",
        "compositions": ["mark", "stacked", "horizontal", "wordmark"],
        "variants": ["white", "black", "lemon", "transparent"],
        "type": "raster",
        "notes": "The uploaded SVG files wrap embedded PNGs and are not editable vector masters. The 2× files are interpolated exports, not new vector detail. Yellow accents shift to orange on the lemon background for contrast.",
    },
}

ROOT_CSS = r"""
/* BRAND_LIBRARY_SHELL_START */
:root { --brand-ink:#171816; --brand-muted:#62675f; --brand-line:#dedfd9; --brand-panel:#fff; --brand-canvas:#f4f5f2; --brand-accent:#396b16; }
body { background:var(--brand-canvas); }
.brand-shell { min-height:100vh; display:grid; grid-template-columns:260px minmax(0,1fr); }
.brand-sidebar { position:sticky; top:0; height:100vh; padding:26px 18px 24px; background:#fff; border-right:1px solid var(--brand-line); display:flex; flex-direction:column; gap:26px; z-index:10; }
.brand-sidebar__identity { display:flex; align-items:center; gap:12px; padding:2px 8px 20px; border-bottom:1px solid #e9ebe5; text-decoration:none; color:inherit; }
.brand-sidebar__identity img { width:38px; height:38px; object-fit:contain; }
.brand-sidebar__identity span { display:block; font-weight:760; font-size:14px; letter-spacing:-.02em; color:#171816; }
.brand-sidebar__identity small { display:block; margin-top:3px; color:#788071; font-size:10px; font-weight:700; letter-spacing:.13em; text-transform:uppercase; }
.brand-nav__label { padding:0 10px; margin:0 0 9px; font-size:10px; font-weight:750; letter-spacing:.14em; color:#858b80; text-transform:uppercase; }
.brand-nav { display:grid; gap:5px; }
.brand-nav a { display:flex; align-items:center; gap:11px; min-height:43px; padding:9px 11px; border-radius:9px; color:#4f554a; text-decoration:none; font-size:13px; font-weight:650; transition:background .16s ease,color .16s ease; }
.brand-nav a:hover { background:#f3f5ef; color:#171816; }
.brand-nav a[aria-current="page"] { background:#eff4e9; color:#2e5715; box-shadow:inset 3px 0 0 #A7E021; }
.brand-nav__dot { width:9px; height:9px; flex:none; border-radius:3px; background:#aeb4a8; }
.brand-nav a[aria-current="page"] .brand-nav__dot { background:#6c982f; }
.brand-sidebar__foot { margin-top:auto; padding:15px 10px 0; border-top:1px solid #e9ebe5; color:#83897e; font-size:11px; line-height:1.6; }
.brand-sidebar__foot a { color:#566d43; }
.brand-main { width:100%; min-width:0; max-width:1440px; margin:0 auto; padding:54px clamp(24px,4vw,64px) 76px; }
.brand-main > main { width:100%; max-width:1180px; margin:0 auto; padding:0; }
.brand-mobilebar { display:none; }
.page-kicker { display:flex; align-items:center; gap:9px; color:#71796c; font-size:11px; font-weight:750; letter-spacing:.13em; text-transform:uppercase; }
.page-kicker__line { width:22px; height:1px; background:var(--brand-accent,#A7E021); }
.brand-hero { display:flex; align-items:flex-start; justify-content:space-between; gap:26px; margin:12px 0 32px; }
.brand-hero h1 { margin:0 0 10px; color:#171816; font-size:clamp(34px,4vw,48px); letter-spacing:-.05em; line-height:1.04; }
.brand-hero p { max-width:720px; margin:0; color:#5b6057; font-size:14px; line-height:1.75; }
.brand-badge { flex:none; margin-top:8px; padding:8px 10px; border:1px solid var(--brand-line); border-radius:7px; background:#fff; color:#65705b; font-size:9px; font-weight:800; letter-spacing:.09em; }
.brand-section { margin-top:40px; }
.brand-section__heading { display:flex; align-items:end; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:6px; }
.brand-section h2 { margin:0; color:#20241e; font-size:21px; letter-spacing:-.03em; }
.brand-section__intro { margin:0; max-width:760px; color:#656a62; font-size:13px; line-height:1.65; }
.brand-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:16px; margin-top:20px; }
.brand-card { overflow:hidden; border:1px solid var(--brand-line); border-radius:14px; background:#fff; }
.brand-card__head { padding:17px 18px 8px; }
.brand-card__head h3 { margin:0 0 5px; color:#20241e; font-size:15px; }
.brand-card__head p { margin:0; color:#71786c; font-size:12px; line-height:1.55; }
.brand-card__previews { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:6px; padding:12px 12px 8px; }
.brand-preview { height:118px; display:grid; place-items:center; overflow:hidden; padding:10px; border:1px solid #e4e7df; border-radius:9px; background:#fff; text-decoration:none; }
.brand-preview--black { background:#101311; border-color:#101311; }
.brand-preview--lemon { background:#FFC93D; border-color:#FFC93D; }
.brand-preview--transparent { background-color:#fafbf8; background-image:linear-gradient(45deg,#e8ebe4 25%,transparent 25%),linear-gradient(-45deg,#e8ebe4 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#e8ebe4 75%),linear-gradient(-45deg,transparent 75%,#e8ebe4 75%); background-size:16px 16px; background-position:0 0,0 8px,8px -8px,-8px 0; }
.brand-preview img { display:block; max-width:100%; max-height:100%; width:auto; height:auto; object-fit:contain; }
.brand-preview__caption { display:block; padding:0 12px 13px; color:#7b8176; font-size:10px; }
.brand-card__actions { display:flex; flex-wrap:wrap; gap:8px; padding:9px 16px 17px; }
.brand-link { display:inline-flex; justify-content:center; align-items:center; min-height:33px; padding:7px 10px; border:1px solid #d8ddd1; border-radius:7px; background:#fafbf8; color:#3c5a2c; font-size:11px; font-weight:700; text-decoration:none; }
.brand-link:hover { background:#f0f4ea; text-decoration:none; }
.brand-link--primary { border-color:#dce8cb; background:#eef4e6; color:#315817; }
.brand-note { margin-top:22px; padding:17px 19px; border:1px solid #e0e4d9; border-radius:12px; background:#fbfcf9; color:#62695c; font-size:12px; line-height:1.7; }
.brand-note strong { color:#343c2e; }
.brand-palette { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; margin-top:16px; }
.brand-swatch { overflow:hidden; border:1px solid var(--brand-line); border-radius:11px; background:#fff; }
.brand-swatch__color { height:65px; }
.brand-swatch__meta { padding:11px 12px; }
.brand-swatch__meta strong { display:block; font-size:12px; }
.brand-swatch__meta code { display:block; margin-top:4px; color:#71786c; font-size:11px; }
.asset-crumbs { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:7px 0 24px; color:#8b9187; font-size:12px; }
.asset-crumbs a { color:#5d7650; font-weight:650; text-decoration:none; }
.asset-hero { display:grid; grid-template-columns:minmax(0,1.45fr) minmax(250px,.8fr); gap:20px; margin-top:22px; align-items:stretch; }
.asset-viewer { min-height:360px; display:grid; place-items:center; padding:35px; border:1px solid var(--brand-line); border-radius:15px; background:#fff; }
.asset-viewer--black { background:#101311; border-color:#101311; }
.asset-viewer--lemon { background:#FFC93D; border-color:#FFC93D; }
.asset-viewer--transparent { background-color:#fafbf8; background-image:linear-gradient(45deg,#e8ebe4 25%,transparent 25%),linear-gradient(-45deg,#e8ebe4 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#e8ebe4 75%),linear-gradient(-45deg,transparent 75%,#e8ebe4 75%); background-size:22px 22px; background-position:0 0,0 11px,11px -11px,-11px 0; }
.asset-viewer img { display:block; max-width:100%; max-height:620px; width:auto; height:auto; object-fit:contain; }
.asset-sidebar { padding:22px; border:1px solid var(--brand-line); border-radius:15px; background:#fff; }
.asset-sidebar h2 { margin:0 0 8px; color:#20241e; font-size:18px; letter-spacing:-.03em; }
.asset-sidebar p { margin:0 0 18px; color:#687062; font-size:12px; line-height:1.7; }
.asset-actions { display:grid; gap:9px; }
.asset-actions a { display:flex; align-items:center; justify-content:center; min-height:42px; padding:10px 13px; border:1px solid #d8ddd1; border-radius:8px; color:#354e29; background:#fafbf8; font-size:12px; font-weight:750; text-decoration:none; }
.asset-actions a.primary { color:#fff; border-color:#273b1a; background:#273b1a; }
.asset-actions a:hover { filter:brightness(.97); text-decoration:none; }
.asset-meta { margin-top:20px; padding-top:16px; border-top:1px solid #edf0e9; color:#7b8275; font-size:11px; line-height:1.7; }
.asset-variants { display:flex; flex-wrap:wrap; gap:8px; margin-top:19px; }
.asset-variants a { padding:7px 10px; border:1px solid #dce0d7; border-radius:7px; color:#59664e; font-size:11px; font-weight:700; text-decoration:none; }
.asset-variants a[aria-current="page"] { border-color:#c7d9b0; background:#eff4e9; color:#325717; }
.brand-footer { margin-top:42px; padding-top:17px; border-top:1px solid #e2e5dc; color:#858b7f; font-size:11px; line-height:1.65; }
.brand-main .eyebrow { color:#65705b; }
.brand-main h1 { letter-spacing:-.045em; }
@media(max-width:880px) { .brand-shell{grid-template-columns:220px minmax(0,1fr)} .brand-sidebar{padding:23px 12px} .brand-main{padding:40px 25px 60px} .asset-hero{grid-template-columns:1fr} }
@media(max-width:680px) {
 .brand-shell{display:block}
 .brand-sidebar{position:sticky;top:0;width:100%;height:auto;padding:11px 14px 12px;border-right:0;border-bottom:1px solid var(--brand-line);gap:8px;background:rgba(255,255,255,.97);backdrop-filter:blur(12px)}
 .brand-sidebar__identity{padding:0 3px 9px;border-bottom:0}
 .brand-sidebar__identity img{width:28px;height:28px}
 .brand-sidebar__identity span{font-size:12px}
 .brand-sidebar__identity small{font-size:8px;margin-top:1px}
 .brand-nav__label{display:none}
 .brand-nav{display:flex;gap:5px;overflow-x:auto;padding-bottom:2px}
 .brand-nav a{flex:none;min-height:34px;padding:7px 9px;font-size:11px;white-space:nowrap;background:#f7f8f5}
 .brand-nav a[aria-current="page"]{box-shadow:inset 0 -2px 0 #A7E021}
 .brand-nav__dot{width:7px;height:7px}
 .brand-sidebar__foot{display:none}
 .brand-main{padding:30px 17px 50px}
 .brand-hero{display:block}
 .brand-badge{display:inline-block;margin-top:18px}
 .brand-grid{grid-template-columns:1fr}
 .brand-preview{height:104px}
 .asset-viewer{min-height:240px;padding:20px}
 .asset-sidebar{padding:17px}
}
 /* BRAND_LIBRARY_SHELL_END */
"""

def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))

def shell(content: str, title: str, active: str, description: str = "") -> str:
    nav = []
    for slug, cfg in BRANDS.items():
        current = ' aria-current="page"' if slug == active else ""
        nav.append(
            f'<a href="/brands/{slug}/"{current}><span class="brand-nav__dot" '
            f'style="background:{cfg["accent"]}"></span><span>{esc(cfg["name"])}</span></a>'
        )
    sidebar = f"""
<aside class="brand-sidebar" aria-label="Brand navigation">
  <a class="brand-sidebar__identity" href="/brands/abe-techlab/">
    <img src="/logos/abe-techlab-mark-adaptive.svg" alt="" aria-hidden="true">
    <span>ABE TechLab<small>Brand library</small></span>
  </a>
  <div>
    <p class="brand-nav__label">Company & product brands</p>
    <nav class="brand-nav">{''.join(nav)}</nav>
  </div>
  <div class="brand-sidebar__foot">One source of truth for every brand.<br><a href="https://github.com/ABE-TechLab/Branding">Open Brand Library repository ↗</a></div>
</aside>
"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f4f5f2"><meta name="description" content="{esc(description)}">
<title>{esc(title)} · ABE TechLab Brand Library</title><style>{ROOT_CSS}</style></head>
<body><div class="brand-shell">{sidebar}<div class="brand-main">{content}
<footer class="brand-footer">ABE TechLab Brand Library · Source artwork, derivation method and approval status are recorded per brand. Generated assets do not imply formal approval.</footer>
</div></div></body></html>
"""

def image_path(slug: str, filename: str) -> str:
    if slug == "abe-techlab":
        return f"/logos/{filename}"
    return f"/brands/{slug}/logos/png/{filename}"

def svg_path(slug: str, filename: str) -> str:
    if slug == "abe-techlab":
        return f"/logos/{filename}"
    return f"/brands/{slug}/logos/svg/{filename}"

def asset_route(slug: str, composition: str, variant: str) -> str:
    return f"/brands/{slug}/assets/{composition}/{variant}/"

def filename(slug: str, composition: str, variant: str, fmt: str = "png") -> str | None:
    if slug == "abe-techlab":
        if variant == "adaptive":
            return f"abe-techlab-{composition}-adaptive.svg" if fmt == "svg" else (
                f"abe-techlab-{composition}-light-v1.png"
            )
        suffix = "light-v1.png" if variant == "light" else "dark-v1.png"
        return f"abe-techlab-{composition}-{suffix}" if fmt == "png" else None
    if slug == "abemail":
        base = f"abemail-{composition}"
        if variant in ("white", "black", "lemon"):
            base += f"-bg-{variant}"
        else:
            base += f"-{variant}"
        return f"{base}-v1.{fmt}"
    base = f"{slug}-{composition}"
    if variant == "transparent":
        base += "-transparent"
    else:
        base += f"-bg-{variant}"
    if fmt == "svg":
        return f"{base}-v1.svg" if variant == "transparent" else None
    return f"{base}-v1.png"

def variant_image_url(slug: str, composition: str, variant: str) -> str:
    name = filename(slug, composition, variant, "png")
    if not name:
        raise ValueError(f"No PNG for {slug}/{composition}/{variant}")
    return image_path(slug, name)

def human_variant(variant: str) -> str:
    return {
        "white": "White background", "black": "Black background",
        "lemon": "Lemon background", "transparent": "Transparent background",
        "light": "Light theme", "dark": "Dark theme",
        "monochrome": "Monochrome",
        "adaptive": "Adaptive SVG",
    }[variant]

def composition_title(composition: str) -> str:
    return {
        "mark": "Symbol only", "symbol": "Symbol only",
        "stacked": "Stacked lockup", "lockup-stacked": "Stacked lockup",
        "horizontal": "Horizontal lockup", "lockup-horizontal": "Horizontal lockup",
        "wordmark": "Wordmark only",
    }[composition]

def render_variant_page(slug: str, composition: str, variant: str, cfg: dict, public_root: Path) -> str:
    png_name = filename(slug, composition, variant, "png")
    svg_name = filename(slug, composition, variant, "svg")
    png_url = image_path(slug, png_name) if png_name else None
    svg_url = svg_path(slug, svg_name) if svg_name else None
    if png_url and not (public_root / png_url.lstrip("/")).is_file():
        raise FileNotFoundError(f"Expected public preview image not found: {png_url}")
    if svg_url and not (public_root / svg_url.lstrip("/")).is_file():
        raise FileNotFoundError(f"Expected public SVG not found: {svg_url}")

    bgclass = f"asset-viewer--{variant}" if variant in ("black", "lemon", "transparent") else ""
    theme_note = cfg["notes"]
    title = f'{cfg["name"]} · {composition_title(composition)} · {human_variant(variant)}'
    breadcrumbs = f'<div class="asset-crumbs"><a href="/brands/">Brands</a><span>›</span><a href="/brands/{slug}/">{esc(cfg["name"])}</a><span>›</span><span>{esc(composition_title(composition))}</span><span>›</span><strong>{esc(human_variant(variant))}</strong></div>'
    actions = []
    if png_url:
        actions.append(f'<a class="primary" href="{png_url}" target="_blank" rel="noopener">Open PNG in new tab</a>')
        actions.append(f'<a href="{png_url}" download="{esc(png_name)}">Download PNG</a>')
    if slug in ("techtrack", "techtrack-kids"):
        if variant == "transparent":
            two_x = f"/brands/{slug}/logos/png/{slug}-{composition}-transparent-2x-v1.png"
            if (public_root / two_x.lstrip("/")).is_file():
                actions.append(f'<a href="{two_x}" download>Download 2× PNG</a>')
            if svg_url:
                actions.append(f'<a href="{svg_url}" target="_blank" rel="noopener">Open raster-backed SVG wrapper</a>')
            source_name = {
                "mark": f"{slug}-mark-bg-white-v1.svg",
                "horizontal": f"{slug}-lockup-horizontal-bg-black-v1.svg",
                "stacked": f"{slug}-lockup-stacked-bg-white-v1.svg",
                "wordmark": f"{slug}-lockup-stacked-bg-white-v1.svg",
            }[composition]
            source_url = f"/brands/{slug}/source/{source_name}"
            if (public_root / source_url.lstrip("/")).is_file():
                actions.append(f'<a href="{source_url}" target="_blank" rel="noopener">Open original uploaded SVG reference</a>')
    elif svg_url:
        actions.append(f'<a href="{svg_url}" target="_blank" rel="noopener">Open SVG in new tab</a>')
        actions.append(f'<a href="{svg_url}" download="{esc(svg_name)}">Download SVG</a>')

    variants = []
    for other in cfg["variants"]:
        current = ' aria-current="page"' if other == variant else ""
        variants.append(f'<a href="{asset_route(slug,composition,other)}"{current}>{esc(human_variant(other))}</a>')

    image_markup = f'<img src="{esc(png_url)}" alt="{esc(title)}">' if png_url else ""
    viewer = f'<div class="asset-viewer {bgclass}"><a href="{png_url}" target="_blank" rel="noopener" aria-label="Open full-size image">{image_markup}</a></div>' if png_url else ""
    meta = ""
    if slug == "abemail":
        meta = '<div class="asset-meta">Source: editable SVG vector paths · PNG render scale: 4× · Colour treatment follows the original Concept 1 artwork.</div>'
    elif slug in ("techtrack", "techtrack-kids"):
        meta = '<div class="asset-meta">Source: PNG embedded inside uploaded SVG · 2× variant is interpolated · Not an editable vector master.</div>'
    else:
        meta = '<div class="asset-meta">Source: current ABE TechLab working SVG/PNG assets · Formal master verification remains pending.</div>'

    content = f"""
<div class="page-kicker"><span class="page-kicker__line"></span>{esc(cfg["kind"])} · individual asset</div>
{breadcrumbs}
<div class="brand-hero"><div><h1>{esc(composition_title(composition))}</h1><p>{esc(cfg["name"])} · {esc(human_variant(variant))}. This page provides an in-browser view and separate file access/download controls.</p></div><span class="brand-badge">{esc(cfg["status"])}</span></div>
<div class="asset-hero">{viewer}<aside class="asset-sidebar"><h2>Asset files</h2><p>Preview the artwork here, open the original file in its own browser tab, or download a local copy.</p><div class="asset-actions">{''.join(actions)}</div><div class="asset-meta">Brand: {esc(cfg["name"])}<br>Composition: {esc(composition_title(composition))}<br>Treatment: {esc(human_variant(variant))}</div></aside></div>
<div class="asset-variants" aria-label="Other variants">{''.join(variants)}</div>
<div class="brand-note"><strong>Source and quality:</strong> {esc(theme_note)}</div>
"""
    return shell(content, title, slug, f"View and download {title}.")

def render_brand_page(slug: str, cfg: dict, public_root: Path) -> str:
    composition_cards = []
    for comp in cfg["compositions"]:
        title = composition_title(comp)
        previews = []
        preview_variants = ["white", "black", "lemon"] if cfg["type"] in ("abemail", "raster") else ["adaptive", "light", "dark"]
        for v in preview_variants:
            url = variant_image_url(slug, comp, v)
            if not (public_root / url.lstrip("/")).is_file():
                continue
            vclass = {"black":"brand-preview--black","lemon":"brand-preview--lemon"}.get(v,"")
            target = asset_route(slug,comp,v)
            previews.append(
                f'<a class="brand-preview {vclass}" href="{target}" title="View {esc(title)} · {esc(human_variant(v))}">'
                f'<img loading="lazy" src="{url}" alt="{esc(cfg["name"])} {esc(title)} · {esc(human_variant(v))}"></a>'
            )
        if len(previews) < 3:
            # ABE has no fixed background treatments in its current source family.
            preview_variants = ["light","dark","adaptive"]
            previews = []
            for v in preview_variants:
                url = variant_image_url(slug,comp,v)
                if (public_root / url.lstrip("/")).is_file():
                    vclass = "brand-preview--black" if v=="dark" else ""
                    previews.append(f'<a class="brand-preview {vclass}" href="{asset_route(slug,comp,v)}"><img loading="lazy" src="{url}" alt="{esc(cfg["name"])} {esc(title)} {esc(v)}"></a>')
        extra = []
        if cfg["type"] == "abemail":
            extra = [f'<a class="brand-link" href="{asset_route(slug,comp,v)}">View {esc(human_variant(v))}</a>' for v in ("light","dark","monochrome")]
        elif cfg["type"] == "raster":
            extra = [f'<a class="brand-link" href="{asset_route(slug,comp,v)}">View {esc(human_variant(v))}</a>' for v in ("transparent",)]
        else:
            extra = [f'<a class="brand-link" href="{asset_route(slug,comp,v)}">View {esc(human_variant(v))}</a>' for v in ("adaptive","light","dark")]
        composition_cards.append(f"""
<article class="brand-card"><div class="brand-card__head"><h3>{esc(title)}</h3><p>Open a preview to view the full-size artwork and download options.</p></div>
<div class="brand-card__previews">{''.join(previews)}</div><span class="brand-preview__caption">Select a background preview to open its dedicated asset page.</span>
<div class="brand-card__actions">{''.join(extra)}</div></article>""")

    palettes = {
        "abe-techlab":[("Lime","#A7E021"),("Charcoal","#111111"),("Off-white","#F9F9F6")],
        "abemail":[("Mint green","#72E3AD"),("Deep teal","#0C2E34"),("White","#FFFFFF")],
        "techtrack":[("Navy","#071A3D"),("Electric blue","#1264F3"),("Cyan blue","#1488F0"),("Teal green","#08C9A5"),("Light gray","#F3F6FC")],
        "techtrack-kids":[("Blue","#1264F3"),("Teal","#08C9A5"),("Yellow","#FFC93D"),("Orange","#FF7A45"),("Purple","#885CF6"),("Pink","#FF5C7A")],
    }[slug]
    palette_html = "".join(
        f'<article class="brand-swatch"><div class="brand-swatch__color" style="background:{color}"></div><div class="brand-swatch__meta"><strong>{esc(name)}</strong><code>{color}</code></div></article>'
        for name,color in palettes
    )
    content = f"""
<div class="page-kicker"><span class="page-kicker__line"></span>{esc(cfg["kind"])} · ABE TechLab Brand Library</div>
<div class="brand-hero"><div><h1>{esc(cfg["name"])}</h1><p>{esc(cfg["intro"])}</p></div><span class="brand-badge">{esc(cfg["status"])}</span></div>
<section class="brand-section"><div class="brand-section__heading"><h2>Logo compositions</h2></div><p class="brand-section__intro">Every composition has its own page for viewing the artwork at full size, opening the source image directly, and downloading the PNG or SVG where available.</p>
<div class="brand-grid">{''.join(composition_cards)}</div></section>
<section class="brand-section"><div class="brand-section__heading"><h2>Brand colours</h2></div><p class="brand-section__intro">Working colour tokens used by this identity. Use the source palette and its documented roles when creating new product surfaces.</p><div class="brand-palette">{palette_html}</div></section>
<div class="brand-note"><strong>Source status:</strong> {esc(cfg["notes"])} <a href="https://github.com/ABE-TechLab/Branding/tree/main/brands/{slug}">View brand source and manifest ↗</a></div>
"""
    return shell(content, cfg["name"], slug, cfg["intro"])

def render_directory(public_root: Path) -> str:
    cards=[]
    for slug,cfg in BRANDS.items():
        if slug=="abe-techlab":
            preview="/logos/abe-techlab-mark-adaptive.svg"
        elif slug=="abemail":
            preview="/brands/abemail/logos/png/abemail-horizontal-bg-white-v1.png"
        elif slug=="techtrack":
            preview="/brands/techtrack/logos/png/techtrack-horizontal-bg-white-v1.png"
        else:
            preview="/brands/techtrack-kids/logos/png/techtrack-kids-horizontal-bg-white-v1.png"
        if not (public_root / preview.lstrip("/")).is_file():
            raise FileNotFoundError(preview)
        cards.append(f'<article class="brand-card"><a class="brand-preview" href="/brands/{slug}/"><img src="{preview}" alt="{esc(cfg["name"])}"></a><div class="brand-card__head"><h3>{esc(cfg["name"])}</h3><p>{esc(cfg["intro"])}</p></div><div class="brand-card__actions"><a class="brand-link brand-link--primary" href="/brands/{slug}/">Open brand library</a></div></article>')
    content=f'<div class="page-kicker"><span class="page-kicker__line"></span>Company & product identities</div><div class="brand-hero"><div><h1>Brand library</h1><p>One place to explore ABE TechLab and its connected product identities. Each brand has its own page, palette, logo compositions and viewable individual assets.</p></div></div><div class="brand-grid">{"".join(cards)}</div>'
    return shell(content,"Brand library","", "Browse all ABE TechLab brand identities.")

def wrap_company_page(source_html: str) -> str:
    if "BRAND_LIBRARY_SHELL_START" in source_html:
        start=source_html.index("/* BRAND_LIBRARY_SHELL_START */")
        end=source_html.index("/* BRAND_LIBRARY_SHELL_END */")+len("/* BRAND_LIBRARY_SHELL_END */")
        source_html=source_html[:start]+ROOT_CSS.strip()+"\n"+source_html[end:]
        return source_html
    if "</style>" not in source_html:
        raise ValueError("Company page is missing its inline style block")
    source_html=source_html.replace("</style>",ROOT_CSS+"\n  </style>",1)
    sidebar = """
    <aside class="brand-sidebar" aria-label="Brand navigation">
      <a class="brand-sidebar__identity" href="/brands/abe-techlab/"><img src="/logos/abe-techlab-mark-adaptive.svg" alt=""><span>ABE TechLab<small>Brand library</small></span></a>
      <div><p class="brand-nav__label">Company & product brands</p><nav class="brand-nav">
      <a href="/brands/abe-techlab/" aria-current="page"><span class="brand-nav__dot" style="background:#A7E021"></span><span>ABE TechLab</span></a>
      <a href="/brands/abemail/"><span class="brand-nav__dot" style="background:#72E3AD"></span><span>ABEmail</span></a>
      <a href="/brands/techtrack/"><span class="brand-nav__dot" style="background:#1264F3"></span><span>TechTrack</span></a>
      <a href="/brands/techtrack-kids/"><span class="brand-nav__dot" style="background:#885CF6"></span><span>TechTrack Kids</span></a>
      </nav></div>
      <div class="brand-sidebar__foot">One source of truth for every brand.<br><a href="https://github.com/ABE-TechLab/Branding">Open Brand Library repository ↗</a></div>
    </aside>
"""
    source_html=source_html.replace("<body>\n  <main>", "<body>\n  <div class=\"brand-shell\">"+sidebar+"<div class=\"brand-main\">\n  <main>",1)
    source_html=source_html.replace("</main>\n</body>", "</main></div>\n</div>\n</body>",1)
    if 'href="/brands/abemail/"' not in source_html:
        raise ValueError("Sidebar navigation was not installed in company page")
    dimensions = {
        "mark": None,
        "lockup-stacked": "1560 × 1050",
        "lockup-horizontal": "2040 × 495",
        "wordmark": "1590 × 336",
    }
    for comp in ("mark","lockup-stacked","lockup-horizontal","wordmark"):
        old=f'href="/logos/abe-techlab-{comp}-adaptive.svg">Open adaptive SVG'
        new=f'href="/brands/abe-techlab/assets/{comp}/adaptive/">View asset page'
        source_html=source_html.replace(old,new)
        for theme in ("light","dark"):
            route=f'/brands/abe-techlab/assets/{comp}/{theme}/'
            old_png=f'href="/logos/abe-techlab-{comp}-{theme}-v1.png">Open PNG asset'
            source_html=source_html.replace(old_png,f'href="{route}">View {theme} asset page')
            size=dimensions[comp]
            old_label=(f'href="/logos/abe-techlab-{comp}-{theme}-v1.png">{theme.title()}'
                       + (f' ({size})' if size else ''))
            source_html=source_html.replace(old_label,f'href="{route}">{theme.title()} asset page')
    return source_html

def build(public_root: Path) -> None:
    public_root.mkdir(parents=True,exist_ok=True)
    # Preserve the existing ABE TechLab main page and wrap it in the shared navigation.
    company_file=ROOT/"public"/"index.html"
    company_html=wrap_company_page(company_file.read_text(encoding="utf-8"))
    (public_root/"index.html").write_text(company_html,encoding="utf-8")

    # Alias the parent-company brand page to the existing complete ABE TechLab page.
    abe_dir=public_root/"brands"/"abe-techlab"
    abe_dir.mkdir(parents=True,exist_ok=True)
    (abe_dir/"index.html").write_text(company_html,encoding="utf-8")

    # Build all brand homepages and an individual page for every supported logo variant.
    for slug,cfg in BRANDS.items():
        if slug=="abe-techlab":
            for comp in cfg["compositions"]:
                for variant in cfg["variants"]:
                    route=asset_route(slug,comp,variant).strip("/")
                    target=public_root/route/"index.html"
                    target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_text(render_variant_page(slug,comp,variant,cfg,public_root),encoding="utf-8")
            continue
        brand_dir=public_root/"brands"/slug
        brand_dir.mkdir(parents=True,exist_ok=True)
        (brand_dir/"index.html").write_text(render_brand_page(slug,cfg,public_root),encoding="utf-8")
        for comp in cfg["compositions"]:
            for variant in cfg["variants"]:
                route=asset_route(slug,comp,variant).strip("/")
                target=public_root/route/"index.html"
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text(render_variant_page(slug,comp,variant,cfg,public_root),encoding="utf-8")

    brands_dir=public_root/"brands"
    brands_dir.mkdir(parents=True,exist_ok=True)
    (brands_dir/"index.html").write_text(render_directory(public_root),encoding="utf-8")
    print("Generated shared navigation, 4 brand homepages, and individual logo detail pages.")

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-root",type=Path,default=ROOT/"public")
    args=parser.parse_args()
    target=args.public_root.resolve()
    if target != (ROOT/"public").resolve():
        # Start from the committed static public folder; expected output goes to temp.
        target.mkdir(parents=True,exist_ok=True)
        for path in ("logos",):
            src=ROOT/"public"/path
            dst=target/path
            if src.exists() and not dst.exists():
                shutil.copytree(src,dst)
    build(target)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
