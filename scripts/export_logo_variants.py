#!/usr/bin/env python3
"""Export fixed light/dark PNG derivatives from adaptive SVG logo masters.

This exporter intentionally changes only the `.ink` theme color. It does not
recreate vector geometry, crop the viewBox, or add a background. It is designed
for the adaptive SVG convention used by the ABE Branding library.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable
import xml.etree.ElementTree as ET

import cairosvg
from PIL import Image

DEFAULT_SOURCES = (
    "public/logos/abe-techlab-lockup-stacked-adaptive.svg",
    "public/logos/abe-techlab-lockup-horizontal-adaptive.svg",
    "public/logos/abe-techlab-wordmark-adaptive.svg",
)

LIGHT_INK = "#111111"
DARK_INK = "#F9F9F6"
ACCENT = "#A7E021"


def parse_viewbox(svg_text: str, source: Path) -> tuple[float, float, float, float]:
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        raise ValueError(f"{source}: invalid SVG/XML: {exc}") from exc

    viewbox = root.attrib.get("viewBox")
    if not viewbox:
        raise ValueError(f"{source}: root SVG must have a viewBox")
    try:
        values = tuple(float(v) for v in re.split(r"[ ,]+", viewbox.strip()))
    except ValueError as exc:
        raise ValueError(f"{source}: invalid viewBox {viewbox!r}") from exc
    if len(values) != 4 or values[2] <= 0 or values[3] <= 0:
        raise ValueError(f"{source}: viewBox must contain four values and positive dimensions")
    return values  # type: ignore[return-value]


def fixed_color_svg(svg_text: str, color: str, source: Path) -> str:
    """Pin only the `.ink` fill and remove the adaptive dark override."""
    if "prefers-color-scheme" not in svg_text:
        raise ValueError(f"{source}: expected an adaptive prefers-color-scheme SVG")

    media_pattern = re.compile(
        r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{\s*\.ink\s*\{\s*fill\s*:\s*#[0-9A-Fa-f]{6}\s*;?\s*\}\s*\}",
        re.IGNORECASE,
    )
    updated, media_count = media_pattern.subn("", svg_text, count=1)
    if media_count != 1:
        raise ValueError(f"{source}: unsupported dark-mode CSS; review exporter before proceeding")

    ink_pattern = re.compile(r"\.ink\s*\{\s*fill\s*:\s*#[0-9A-Fa-f]{6}\s*;?\s*\}", re.IGNORECASE)
    updated, ink_count = ink_pattern.subn(f".ink{{fill:{color}}}", updated, count=1)
    if ink_count != 1:
        raise ValueError(f"{source}: expected exactly one default .ink fill rule")

    if ACCENT.lower() not in svg_text.lower():
        raise ValueError(f"{source}: expected brand accent {ACCENT} was not found")
    return updated


def validate_png(path: Path, expected_width: int, expected_height: int, ink: str, expect_accent: bool) -> None:
    try:
        with Image.open(path) as image:
            image.load()
            if image.format != "PNG":
                raise ValueError(f"{path}: output is not PNG")
            if image.size != (expected_width, expected_height):
                raise ValueError(f"{path}: unexpected dimensions {image.size}")
            if image.mode not in {"RGBA", "RGBa", "P"}:
                raise ValueError(f"{path}: expected RGBA or indexed PNG with palette alpha, got {image.mode}")
            rgba = image.convert("RGBA")
            alpha = rgba.getchannel("A")
            if alpha.getextrema()[0] != 0:
                raise ValueError(f"{path}: no fully transparent background pixels found")
            if alpha.getextrema()[1] < 250:
                raise ValueError(f"{path}: image has no fully opaque logo pixels")

            colors = rgba.getcolors(maxcolors=rgba.width * rgba.height)
            if colors is None:
                raise ValueError(f"{path}: unable to inspect output colors")
            palette = {color for _, color in colors}
            expected_rgb = tuple(bytes.fromhex(ink.lstrip("#")))
            if not any(max(abs(rgb[i] - expected_rgb[i]) for i in range(3)) <= 4 and rgb[3] >= 250 for rgb in palette):
                raise ValueError(f"{path}: expected solid ink near {ink} not found")
            if expect_accent:
                accent_rgb = tuple(bytes.fromhex(ACCENT.lstrip("#")))
                if not any(max(abs(rgb[i] - accent_rgb[i]) for i in range(3)) <= 3 and rgb[3] >= 250 for rgb in palette):
                    raise ValueError(f"{path}: expected solid accent near {ACCENT} not found")
    except OSError as exc:
        raise ValueError(f"{path}: PNG could not be decoded: {exc}") from exc


def export_one(source: Path, output_dir: Path, scale: float, palette_colors: int) -> list[Path]:
    svg_text = source.read_text(encoding="utf-8")
    _, _, view_width, view_height = parse_viewbox(svg_text, source)
    width = round(view_width * scale)
    height = round(view_height * scale)
    if width <= 0 or height <= 0:
        raise ValueError(f"{source}: invalid output dimensions at scale {scale}")

    base_name = source.stem.removesuffix("-adaptive")
    outputs: list[Path] = []
    for variant, ink in (("light", LIGHT_INK), ("dark", DARK_INK)):
        target = output_dir / f"{base_name}-{variant}-v1.png"
        rgba_target = target.with_name(target.stem + ".rgba.png")
        raster_svg = fixed_color_svg(svg_text, ink, source)
        cairosvg.svg2png(
            bytestring=raster_svg.encode("utf-8"),
            write_to=str(rgba_target),
            output_width=width,
            output_height=height,
        )
        if palette_colors:
            # Preserve transparent palette alpha while keeping public PNGs compact.
            with Image.open(rgba_target) as rendered:
                rendered.quantize(
                    colors=palette_colors,
                    method=Image.Quantize.FASTOCTREE,
                    dither=Image.Dither.NONE,
                ).save(target, optimize=True)
            rgba_target.unlink()
        else:
            rgba_target.replace(target)

        expect_accent = bool(re.search(r'class=["\']accent["\']', svg_text))
        validate_png(target, width, height, ink, expect_accent)
        outputs.append(target)
        accent_note = f", accent {ACCENT}" if expect_accent else ""
        print(f"OK {target} — {width}×{height}, transparent PNG, ink {ink}{accent_note}")
    return outputs


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", help="Adaptive SVG source; may be supplied more than once")
    parser.add_argument("--output-dir", default="public/logos", help="Output directory (default: public/logos)")
    parser.add_argument("--scale", type=float, default=3.0, help="Pixels per SVG viewBox unit (default: 3)")
    parser.add_argument("--palette-colors", type=int, default=256, help="Indexed PNG palette entries (1–256); use 0 for full RGBA (default: 256)")
    args = parser.parse_args(argv)

    if args.scale <= 0:
        parser.error("--scale must be greater than zero")
    if args.palette_colors < 0 or args.palette_colors > 256 or args.palette_colors == 1:
        parser.error("--palette-colors must be 0 or between 2 and 256")

    sources = [Path(value) for value in (args.source or DEFAULT_SOURCES)]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        for source in sources:
            if not source.is_file():
                raise FileNotFoundError(f"SVG source does not exist: {source}")
            export_one(source, output_dir, args.scale, args.palette_colors)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
