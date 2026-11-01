#!/usr/bin/env python3
"""Create fixed-background ABE TechLab logo PNGs from existing adaptive SVGs."""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from PIL import Image

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

SOURCES = {
    "mark": ("public/logos/abe-techlab-mark-adaptive.svg", "mark", True),
    "lockup-stacked": ("public/logos/abe-techlab-lockup-stacked-adaptive.svg", "ink", True),
    "lockup-horizontal": ("public/logos/abe-techlab-lockup-horizontal-adaptive.svg", "ink", True),
    "wordmark": ("public/logos/abe-techlab-wordmark-adaptive.svg", "ink", False),
}
BACKGROUNDS = {
    "white": ("#FFFFFF", "#111111", "#A7E021"),
    "black": ("#000000", "#F9F9F6", "#A7E021"),
    "lemon": ("#A7E021", "#111111", "#F9F9F6"),
}


def render_source(source, selector, bg, ink, accent, has_accent, target):
    raw = source.read_text(encoding="utf-8")
    media = re.compile(
        rf"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*"
        rf"\{{\s*\.{selector}\s*\{{\s*fill\s*:\s*#[0-9a-fA-F]{{6}}\s*;?\s*\}}\s*\}}",
        re.I,
    )
    raw, count = media.subn("", raw, count=1)
    if count != 1:
        raise ValueError(f"{source}: expected one dark-mode color rule")

    base = re.compile(rf"\.{selector}\s*\{{\s*fill\s*:\s*#[0-9a-fA-F]{{6}}\s*;?\s*\}}", re.I)
    raw, count = base.subn(f".{selector}{{fill:{ink}}}", raw, count=1)
    if count != 1:
        raise ValueError(f"{source}: expected one base color rule")

    if has_accent:
        accent_rule = re.compile(r"\.accent\s*\{\s*fill\s*:\s*#[0-9a-fA-F]{6}\s*;?\s*\}", re.I)
        raw, count = accent_rule.subn(f".accent{{fill:{accent}}}", raw, count=1)
        if count != 1:
            raise ValueError(f"{source}: expected one accent rule")

    root = ET.fromstring(raw)
    values = tuple(float(v) for v in re.split(r"[ ,]+", root.attrib["viewBox"].strip()))
    if len(values) != 4 or values[2] <= 0 or values[3] <= 0:
        raise ValueError(f"{source}: invalid viewBox")
    x, y, w, h = values
    style_pos = next((i for i, child in enumerate(list(root)) if child.tag == f"{{{NS}}}style"), None)
    if style_pos is None:
        raise ValueError(f"{source}: missing theme style block")
    root.insert(style_pos + 1, ET.Element(f"{{{NS}}}rect", {
        "x": str(x), "y": str(y), "width": str(w), "height": str(h), "fill": bg
    }))
    svg = ET.tostring(root, encoding="unicode")
    width, height = round(w * 3), round(h * 3)
    rgba_target = target.with_name(target.stem + ".rgba.png")
    cairosvg.svg2png(
        bytestring=svg.encode("utf-8"), write_to=str(rgba_target),
        output_width=width, output_height=height
    )
    with Image.open(rgba_target) as rendered:
        indexed = rendered.convert("RGB").quantize(
            colors=256,
            method=Image.Quantize.FASTOCTREE,
            dither=Image.Dither.NONE,
        )
        # Preserve the exact requested canvas token after palette quantization.
        background_index = indexed.getpixel((0, 0))
        palette = indexed.getpalette()
        background_rgb = tuple(bytes.fromhex(bg.lstrip("#")))
        palette[background_index * 3:background_index * 3 + 3] = list(background_rgb)
        indexed.putpalette(palette)
        indexed.save(target, optimize=True)
    rgba_target.unlink()
    validate(target, (width, height), bg, ink, accent, has_accent)


def validate(path, size, bg, ink, accent, has_accent):
    with Image.open(path) as image:
        image.load()
        if image.format != "PNG" or image.size != size:
            raise ValueError(f"{path}: invalid PNG format or dimensions: {image.format}, {image.size}")
        rgba = image.convert("RGBA")
        if rgba.getchannel("A").getextrema() != (255, 255):
            raise ValueError(f"{path}: background must be fully opaque")
        bg_rgb = tuple(bytes.fromhex(bg[1:]))
        if rgba.getpixel((0, 0))[:3] != bg_rgb:
            raise ValueError(f"{path}: unexpected background color")
        colors = rgba.getcolors(maxcolors=rgba.width * rgba.height)
        if colors is None:
            raise ValueError(f"{path}: could not inspect PNG colors")
        palette = {pixel for _, pixel in colors}

        def present(hex_color):
            rgb = tuple(bytes.fromhex(hex_color[1:]))
            return any(
                max(abs(px[i] - rgb[i]) for i in range(3)) <= 2 and px[3] == 255
                for px in palette
            )

        if not present(ink):
            raise ValueError(f"{path}: foreground color {ink} not found")
        if has_accent and not present(accent):
            raise ValueError(f"{path}: accent color {accent} not found")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path("public/logos"))
    args = parser.parse_args()
    root = args.repo_root.resolve()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    count = 0
    for composition, (source_name, selector, has_accent) in SOURCES.items():
        source = root / source_name
        if not source.is_file():
            raise FileNotFoundError(source)
        for background, (bg, ink, accent) in BACKGROUNDS.items():
            target = out / f"abe-techlab-{composition}-bg-{background}-v1.png"
            render_source(source, selector, bg, ink, accent, has_accent, target)
            with Image.open(target) as image:
                print(f"OK {target} — {image.width}x{image.height}, opaque {background} background")
            count += 1
    if count != 12:
        raise ValueError(f"Expected 12 exports, created {count}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, ET.ParseError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

# Version 1 opaque background exports are separate from transparent PNG assets.
