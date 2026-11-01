#!/usr/bin/env python3
"""Build reproducible ABEmail, TechTrack and TechTrack Kids logo packages.

ABEmail is path-based SVG artwork with live Inter text and is rendered from
vector source at 4x. The TechTrack SVG uploads are PNG-backed SVG containers;
their embedded PNGs are extracted and background-separated without pretending
that the files are editable vector masters. Those raster-derived exports are
provided at native and 2x dimensions, with the original source resolution
recorded in each brand inventory.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import io
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)

ABEMAIL = {
    "symbol": {
        "dark": "ABEmail_C1_Symbol_Dark.svg",
        "light": "ABEmail_C1_Symbol_Light.svg",
        "monochrome": "ABEmail_C1_Symbol_Monochrome.svg",
    },
    "horizontal": {
        "dark": "ABEmail_C1_Horizontal_Dark.svg",
        "light": "ABEmail_C1_Horizontal_Light.svg",
        "monochrome": "ABEmail_C1_Horizontal_Monochrome.svg",
    },
    "stacked": {
        "dark": "ABEmail_C1_Stacked_Dark.svg",
        "light": "ABEmail_C1_Stacked_Light.svg",
        "monochrome": "ABEmail_C1_Stacked_Monochrome.svg",
    },
}
ABEMAIL_SCALE = 4
ABEMAIL_COLORS = {
    "mint": "#72E3AD",
    "deep_teal": "#0C2E34",
    "white": "#FFFFFF",
    "black_background": "#000000",
    "lemon_background": "#FFC93D",
}

TECHTRACK = {
    "techtrack": {
        "source": "brands/techtrack/source",
        "mark": "techtrack-mark-bg-white-v1.svg",
        "horizontal": "techtrack-lockup-horizontal-bg-black-v1.svg",
        "stacked": "techtrack-lockup-stacked-bg-white-v1.svg",
        "tagline": "Skills Today. Opportunities Tomorrow.",
        "palette": {
            "navy": "#071A3D",
            "electric_blue": "#1264F3",
            "cyan_blue": "#1488F0",
            "teal_green": "#08C9A5",
            "light_gray": "#F3F6FC",
            "white": "#FFFFFF",
        },
        "yellow_to_orange_on_lemon": False,
    },
    "techtrack-kids": {
        "source": "brands/techtrack-kids/source",
        "mark": "techtrack-kids-mark-bg-white-v1.svg",
        "horizontal": "techtrack-kids-lockup-horizontal-bg-black-v1.svg",
        "stacked": "techtrack-kids-lockup-stacked-bg-white-v1.svg",
        "tagline": "Learn. Play. Create.",
        "palette": {
            "blue": "#1264F3",
            "teal": "#08C9A5",
            "yellow": "#FFC93D",
            "orange": "#FF7A45",
            "purple": "#885CF6",
            "pink": "#FF5C7A",
            "light": "#F8FAFF",
        },
        "yellow_to_orange_on_lemon": True,
    },
}
BACKGROUNDS = {
    "white": "#FFFFFF",
    "black": "#000000",
    "lemon": "#FFC93D",
}
DARK_INK = (7, 26, 61)
LIGHT_INK = (248, 250, 255)
ORANGE = (255, 122, 69)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_viewbox(root: ET.Element) -> tuple[float, float, float, float]:
    raw = root.attrib.get("viewBox")
    if not raw:
        width = float(root.attrib.get("width", "0").replace("px", ""))
        height = float(root.attrib.get("height", "0").replace("px", ""))
        raw = f"0 0 {width:g} {height:g}"
    values = tuple(float(v) for v in re.split(r"[ ,]+", raw.strip()))
    if len(values) != 4 or values[2] <= 0 or values[3] <= 0:
        raise ValueError(f"Invalid SVG viewBox: {raw}")
    return values  # type: ignore[return-value]


def svg_render(svg: bytes, width: int, height: int) -> Image.Image:
    rendered = cairosvg.svg2png(bytestring=svg, output_width=width, output_height=height)
    with Image.open(io.BytesIO(rendered)) as image:
        image.load()
        return image.convert("RGBA")


def save_rgba(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True, dpi=(300, 300))
    with Image.open(path) as check:
        check.load()
        if check.format != "PNG" or check.mode != "RGBA" or check.size != image.size:
            raise ValueError(f"PNG validation failed: {path}")
        if check.getchannel("A").getbbox() is None:
            raise ValueError(f"PNG is fully transparent: {path}")


def save_opaque(image: Image.Image, background: str, path: Path) -> None:
    rgb = tuple(bytes.fromhex(background.lstrip("#")))
    canvas = Image.new("RGBA", image.size, (*rgb, 255))
    canvas.alpha_composite(image)
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(path, format="PNG", optimize=True, dpi=(300, 300))
    with Image.open(path) as check:
        check.load()
        if check.format != "PNG" or check.mode != "RGB" or check.size != image.size:
            raise ValueError(f"Opaque PNG validation failed: {path}")
        if check.getpixel((0, 0)) != rgb:
            raise ValueError(f"Incorrect {background} background: {path}")


def add_background_svg(source_svg: bytes, color: str) -> bytes:
    root = ET.fromstring(source_svg)
    x, y, width, height = parse_viewbox(root)
    rect = ET.Element(f"{{{SVG_NS}}}rect", {
        "x": str(x), "y": str(y), "width": str(width), "height": str(height),
        "fill": color,
    })
    root.insert(0, rect)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def crop_text_only(source_svg: bytes) -> bytes:
    root = ET.fromstring(source_svg)
    view_x, view_y, view_w, view_h = parse_viewbox(root)
    text_nodes = [copy.deepcopy(node) for node in list(root) if local_name(node.tag) == "text"]
    if not text_nodes:
        raise ValueError("ABEmail vector source has no editable text wordmark")

    new_root = ET.Element(f"{{{SVG_NS}}}svg", {
        "version": root.attrib.get("version", "1.1"),
        "width": root.attrib.get("width", str(view_w)),
        "height": root.attrib.get("height", str(view_h)),
        "viewBox": f"{view_x:g} {view_y:g} {view_w:g} {view_h:g}",
        "role": "img",
        "aria-label": "ABEmail wordmark",
    })
    title = ET.SubElement(new_root, f"{{{SVG_NS}}}title")
    title.text = "ABEmail wordmark"
    desc = ET.SubElement(new_root, f"{{{SVG_NS}}}desc")
    desc.text = "ABEmail wordmark extracted from the supplied editable SVG text."
    new_root.extend(text_nodes)

    # Render once to get a tight text-only viewBox while preserving live text.
    temp = ET.tostring(new_root, encoding="utf-8")
    preview = svg_render(temp, max(1, round(view_w)), max(1, round(view_h)))
    bounds = preview.getchannel("A").getbbox()
    if not bounds:
        raise ValueError("ABEmail text-only source did not render visible pixels")
    left, top, right, bottom = bounds
    pad = 8
    left, top = max(0, left - pad), max(0, top - pad)
    right, bottom = min(preview.width, right + pad), min(preview.height, bottom + pad)
    new_root.set("viewBox", f"{view_x + left:g} {view_y + top:g} {right-left:g} {bottom-top:g}")
    new_root.set("width", str(right - left))
    new_root.set("height", str(bottom - top))
    return ET.tostring(new_root, encoding="utf-8", xml_declaration=True)


def clear_generated(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def mirror_public(source: Path, destination: Path) -> None:
    # destination is the brand's generated public/logos directory.
    # Replace only that directory; leave index.html and asset-detail pages untouched.
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def render_abemail(package_root: Path, public_root: Path) -> dict:
    source_root = ROOT / "brands" / "abemail" / "source"
    svg_out = package_root / "abemail" / "logos" / "svg"
    png_out = package_root / "abemail" / "logos" / "png"
    clear_generated(svg_out)
    clear_generated(png_out)

    inventory = []
    source_docs = {}
    for composition, themes in ABEMAIL.items():
        for theme, filename in themes.items():
            source = source_root / filename
            if not source.is_file():
                raise FileNotFoundError(source)
            raw = source.read_bytes()
            root = ET.fromstring(raw)
            if root.find(f".//{{{SVG_NS}}}path") is None:
                raise ValueError(f"Expected real vector paths in ABEmail source: {source}")
            if root.find(f".//{{{SVG_NS}}}image") is not None:
                raise ValueError(f"ABEmail SVG unexpectedly embeds a raster image: {source}")
            source_docs[(composition, theme)] = raw

            target_svg = svg_out / f"abemail-{composition}-{theme}-v1.svg"
            target_svg.write_bytes(raw)
            x, y, w, h = parse_viewbox(root)
            width, height = round(w * ABEMAIL_SCALE), round(h * ABEMAIL_SCALE)
            transparent = svg_render(raw, width, height)
            png_name = f"abemail-{composition}-{theme}-v1.png"
            target_png = png_out / png_name
            save_rgba(transparent, target_png)
            inventory.append({
                "composition": composition, "theme": theme,
                "svg": str(target_svg.relative_to(package_root)),
                "transparent_png": str(target_png.relative_to(package_root)),
                "viewBox": root.attrib.get("viewBox"),
                "png_dimensions": list(transparent.size),
                "render_scale": ABEMAIL_SCALE,
                "source": str(source.relative_to(ROOT)),
                "source_sha256": sha256(source),
                "vector_paths": len(root.findall(f".//{{{SVG_NS}}}path")),
                "live_text": len(root.findall(f".//{{{SVG_NS}}}text")),
            })

    # Produce a wordmark-only SVG from the existing editable wordmark text.
    for theme in ("dark", "light", "monochrome"):
        source = source_docs[("horizontal", theme)]
        wordmark_svg = crop_text_only(source)
        target_svg = svg_out / f"abemail-wordmark-{theme}-v1.svg"
        target_svg.write_bytes(wordmark_svg)
        root = ET.fromstring(wordmark_svg)
        _, _, w, h = parse_viewbox(root)
        transparent = svg_render(wordmark_svg, round(w * ABEMAIL_SCALE), round(h * ABEMAIL_SCALE))
        target_png = png_out / f"abemail-wordmark-{theme}-v1.png"
        save_rgba(transparent, target_png)
        inventory.append({
            "composition": "wordmark", "theme": theme,
            "svg": str(target_svg.relative_to(package_root)),
            "transparent_png": str(target_png.relative_to(package_root)),
            "viewBox": root.attrib.get("viewBox"),
            "png_dimensions": list(transparent.size),
            "render_scale": ABEMAIL_SCALE,
            "source": "brands/abemail/source/ABEmail_C1_Horizontal_" + theme.title() + ".svg",
            "source_type": "live-text-extraction-from-vector-source",
            "live_text": 1,
        })

    # Fixed-background family: use light artwork on white/lemon and dark on black.
    for composition in ("symbol", "horizontal", "stacked", "wordmark"):
        for background, color in BACKGROUNDS.items():
            theme = "dark" if background == "black" else "light"
            if composition == "wordmark":
                base_svg = (svg_out / f"abemail-wordmark-{theme}-v1.svg").read_bytes()
            else:
                base_svg = source_docs[(composition, theme)]
            fixed_svg = add_background_svg(base_svg, color)
            target_svg = svg_out / f"abemail-{composition}-bg-{background}-v1.svg"
            target_svg.write_bytes(fixed_svg)
            root = ET.fromstring(fixed_svg)
            _, _, w, h = parse_viewbox(root)
            width, height = round(w * ABEMAIL_SCALE), round(h * ABEMAIL_SCALE)
            image = svg_render(fixed_svg, width, height)
            target_png = png_out / f"abemail-{composition}-bg-{background}-v1.png"
            # Save as fully opaque RGB PNG.
            save_opaque(image, color, target_png)
            inventory.append({
                "composition": composition, "background": background,
                "svg": str(target_svg.relative_to(package_root)),
                "png": str(target_png.relative_to(package_root)),
                "png_dimensions": [width, height],
                "render_scale": ABEMAIL_SCALE,
                "source_theme": theme,
            })

    public_destination = public_root / "abemail"
    mirror_public(package_root / "abemail" / "logos", public_destination / "logos")
    # Publish the original editable SVG sources separately from generated variants.
    mirror_public(source_root, public_destination / "source")
    return {
        "brand": "abemail",
        "source_type": "editable-svg-vector-paths-with-live-inter-font-wordmark",
        "export_scale": ABEMAIL_SCALE,
        "palette": ABEMAIL_COLORS,
        "inventory": inventory,
    }


def extract_embedded_png(source: Path) -> tuple[Image.Image, str]:
    raw = source.read_text(encoding="utf-8")
    match = re.search(r"data:image/png;base64,([^\"']+)", raw)
    if not match:
        raise ValueError(f"TechTrack source SVG has no embedded PNG: {source}")
    encoded = re.sub(r"\s+", "", match.group(1))
    data = base64.b64decode(encoded, validate=True)
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        if image.format != "PNG":
            raise ValueError(f"Embedded payload is not PNG: {source}")
        embedded = image.convert("RGB")
        native_size = embedded.size
    root = ET.fromstring(raw)
    _, _, vw, vh = parse_viewbox(root)
    if round(vw) != native_size[0] or round(vh) != native_size[1]:
        raise ValueError(
            f"{source}: embedded PNG {native_size} differs from SVG viewBox {vw:g}×{vh:g}"
        )
    if len(root.findall(f".//{{{SVG_NS}}}path")) or len(root.findall(f".//{{{SVG_NS}}}text")):
        raise ValueError(f"{source}: expected image-backed SVG wrapper, not vector source")
    return embedded, hashlib.sha256(data).hexdigest()


def background_rgb(name: str) -> tuple[int, int, int]:
    return tuple(bytes.fromhex(BACKGROUNDS[name].lstrip("#")))


def remove_flat_background(image: Image.Image, background: tuple[int, int, int]) -> Image.Image:
    rgb = image.convert("RGB")
    pixels = rgb.load()
    result = Image.new("RGBA", rgb.size, (0, 0, 0, 0))
    out = result.load()
    max_possible = max(max(background), 255 - min(background))
    # For each antialiased pixel, estimate coverage from distance to the flat
    # background and un-composite the source colour to avoid a coloured halo.
    for y in range(rgb.height):
        for x in range(rgb.width):
            p = pixels[x, y]
            delta = max(abs(p[i] - background[i]) for i in range(3))
            if delta <= 3:
                continue
            alpha = min(1.0, delta / max_possible)
            if alpha < 0.035:
                continue
            uncomposited = tuple(
                max(0, min(255, round((p[i] - background[i] * (1 - alpha)) / alpha)))
                for i in range(3)
            )
            out[x, y] = (*uncomposited, round(alpha * 255))
    if result.getchannel("A").getbbox() is None:
        raise ValueError("Background removal left no visible logo pixels")
    return result


def recolor_white_to_navy(image: Image.Image) -> Image.Image:
    out = image.copy()
    pixels = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = pixels[x, y]
            if a and min(r, g, b) > 205 and max(r, g, b) - min(r, g, b) < 50:
                pixels[x, y] = (*DARK_INK, a)
    return out


def recolor_navy_to_light(image: Image.Image) -> Image.Image:
    out = image.copy()
    pixels = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = pixels[x, y]
            if a and r < 38 and g < 55 and b < 105 and b >= r:
                pixels[x, y] = (*LIGHT_INK, a)
    return out


def recolor_yellow_to_orange(image: Image.Image) -> Image.Image:
    out = image.copy()
    pixels = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = pixels[x, y]
            if a and r > 175 and g > 125 and b < 125 and r >= g:
                pixels[x, y] = (*ORANGE, a)
    return out


def crop_wordmark(stacked: Image.Image) -> Image.Image:
    alpha = stacked.getchannel("A")
    threshold = max(4, round(stacked.width * 0.008))
    row_counts = []
    for y in range(stacked.height):
        row_counts.append(sum(1 for value in alpha.crop((0, y, stacked.width, y + 1)).getdata() if value > 32))
    active = [count > threshold for count in row_counts]
    groups: list[tuple[int, int]] = []
    start = None
    for y, is_active in enumerate(active + [False]):
        if is_active and start is None:
            start = y
        elif not is_active and start is not None:
            groups.append((start, y))
            start = None
    candidates = [group for group in groups if group[0] > round(stacked.height * 0.30)]
    if not candidates:
        raise ValueError("Could not locate the wordmark region in stacked source")
    top = candidates[0][0]
    bottom = candidates[-1][1]
    crop = stacked.crop((0, max(0, top - 10), stacked.width, min(stacked.height, bottom + 10)))
    bounds = crop.getchannel("A").getbbox()
    if not bounds:
        raise ValueError("Wordmark crop is empty")
    return crop.crop(bounds)


def write_raster_svg_wrapper(image: Image.Image, target: Path, title: str) -> None:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    root = ET.Element(f"{{{SVG_NS}}}svg", {
        "width": str(image.width), "height": str(image.height),
        "viewBox": f"0 0 {image.width} {image.height}",
        "role": "img", "aria-label": title,
    })
    title_node = ET.SubElement(root, f"{{{SVG_NS}}}title")
    title_node.text = title
    desc = ET.SubElement(root, f"{{{SVG_NS}}}desc")
    desc.text = "Transparent SVG compatibility wrapper containing embedded raster artwork; not an editable vector master."
    ET.SubElement(root, f"{{{SVG_NS}}}image", {
        "x": "0", "y": "0", "width": str(image.width), "height": str(image.height),
        "preserveAspectRatio": "none", f"{{{XLINK_NS}}}href": "data:image/png;base64," + encoded,
    })
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))


def render_techtrack_brand(slug: str, config: dict, package_root: Path, public_root: Path) -> dict:
    source_dir = ROOT / config["source"]
    svg_out = package_root / slug / "logos" / "svg"
    png_out = package_root / slug / "logos" / "png"
    clear_generated(svg_out)
    clear_generated(png_out)

    source_map = {
        "mark": source_dir / config["mark"],
        "horizontal": source_dir / config["horizontal"],
        "stacked": source_dir / config["stacked"],
    }
    extracted: dict[str, Image.Image] = {}
    sources_meta = {}
    for comp, path in source_map.items():
        image, embedded_hash = extract_embedded_png(path)
        suffix = re.search(r"bg-(white|black|lemon)", path.name)
        if not suffix:
            raise ValueError(f"Source filename must declare its background: {path}")
        bg_name = suffix.group(1)
        bg = background_rgb(bg_name)
        corners = [image.getpixel(point) for point in (
            (0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1)
        )]
        if any(max(abs(corners[i][ch] - bg[ch]) for ch in range(3)) > 12 for i in range(4)):
            raise ValueError(f"{path}: canvas corners do not match declared {bg_name} background")
        extracted[comp] = remove_flat_background(image, bg)
        sources_meta[comp] = {
            "source": str(path.relative_to(ROOT)),
            "source_sha256": sha256(path),
            "embedded_png_sha256": embedded_hash,
            "source_dimensions": list(image.size),
            "source_background": bg_name,
            "vector_paths": 0,
            "embedded_raster": True,
        }

    # The horizontal source is supplied with white lettering on black. Recolour
    # that lettering to the brand navy for light surfaces after removing black.
    extracted["horizontal"] = recolor_white_to_navy(extracted["horizontal"])
    extracted["wordmark"] = crop_wordmark(extracted["stacked"])

    logo_names = ("mark", "horizontal", "stacked", "wordmark")
    inventory = []
    for composition in logo_names:
        base = extracted[composition]
        transparent_1x = png_out / f"{slug}-{composition}-transparent-v1.png"
        save_rgba(base, transparent_1x)
        transparent_2x_image = base.resize(
            (base.width * 2, base.height * 2), Image.Resampling.LANCZOS
        )
        transparent_2x = png_out / f"{slug}-{composition}-transparent-2x-v1.png"
        save_rgba(transparent_2x_image, transparent_2x)

        wrapper = svg_out / f"{slug}-{composition}-transparent-v1.svg"
        write_raster_svg_wrapper(base, wrapper, f"{slug} {composition} transparent")

        for background, hex_color in BACKGROUNDS.items():
            if background == "black":
                art = recolor_navy_to_light(base)
            else:
                art = base.copy()
            if background == "lemon" and config["yellow_to_orange_on_lemon"]:
                art = recolor_yellow_to_orange(art)

            target = png_out / f"{slug}-{composition}-bg-{background}-v1.png"
            save_opaque(art, hex_color, target)
            upscaled = art.resize((art.width * 2, art.height * 2), Image.Resampling.LANCZOS)
            target_2x = png_out / f"{slug}-{composition}-bg-{background}-2x-v1.png"
            save_opaque(upscaled, hex_color, target_2x)

            wrapper_bg = svg_out / f"{slug}-{composition}-bg-{background}-v1.svg"
            write_raster_svg_wrapper(
                Image.new("RGBA", (1, 1), (0, 0, 0, 0)), wrapper_bg,
                f"{slug} {composition} {background} source reference"
            )
            # A background-specific SVG is not emitted as a false vector. The
            # original image-backed reference SVG remains in source/.
            wrapper_bg.unlink()

            inventory.append({
                "composition": composition,
                "background": background,
                "png": str(target.relative_to(package_root)),
                "png_2x": str(target_2x.relative_to(package_root)),
                "source_dimensions": list(base.size),
                "export_dimensions_2x": list(upscaled.size),
                "render_method": "2x Lanczos upscale from embedded raster; no new vector detail created",
                "source": sources_meta.get(composition, sources_meta.get("stacked")),
            })

        inventory.append({
            "composition": composition,
            "background": "transparent",
            "png": str(transparent_1x.relative_to(package_root)),
            "png_2x": str(transparent_2x.relative_to(package_root)),
            "svg_wrapper": str(wrapper.relative_to(package_root)),
            "source_dimensions": list(base.size),
            "export_dimensions_2x": list(transparent_2x_image.size),
            "render_method": "background-separated embedded PNG; SVG is a raster-backed wrapper",
            "source": sources_meta.get(composition, sources_meta.get("stacked")),
        })

    # Mirror generated output only; preserve source and documentation directories.
    destination = public_root / slug
    mirror_public(package_root / slug / "logos", destination / "logos")
    # Keep the uploaded, PNG-backed SVG references reachable from individual asset pages.
    mirror_public(source_dir, destination / "source")
    return {
        "brand": slug,
        "source_type": "png-backed-svg-uploads",
        "vector_master_available": False,
        "source_resolution_note": "The uploaded SVGs contain embedded PNGs at the SVG viewBox dimensions. 2x files are interpolation-only; supply original editable vector artwork for true vector-quality scaling.",
        "palette": config["palette"],
        "tagline": config["tagline"],
        "source_files": sources_meta,
        "inventory": inventory,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, default=ROOT / "brands")
    parser.add_argument("--public-root", type=Path, default=ROOT / "public" / "brands")
    parser.add_argument("--inventory-dir", type=Path, default=ROOT / "brands")
    args = parser.parse_args()

    package_root = args.package_root.resolve()
    public_root = args.public_root.resolve()
    inventory_dir = args.inventory_dir.resolve()
    package_root.mkdir(parents=True, exist_ok=True)
    public_root.mkdir(parents=True, exist_ok=True)
    inventory_dir.mkdir(parents=True, exist_ok=True)

    abemail = render_abemail(package_root, public_root)
    results = [abemail]
    for slug, config in TECHTRACK.items():
        results.append(render_techtrack_brand(slug, config, package_root, public_root))

    for result in results:
        slug = result["brand"]
        destination = inventory_dir / slug / "inventory.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Generated {len(result['inventory'])} inventory entries for {slug}")

    print("Completed ABEmail vector exports and TechTrack raster-derived exports.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, ET.ParseError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
