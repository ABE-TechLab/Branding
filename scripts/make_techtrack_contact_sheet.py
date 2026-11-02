#!/usr/bin/env python3
"""Build a reviewed TechTrack contact sheet without the deferred black-background treatment."""
from pathlib import Path
import io
import cairosvg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CELL_W, CELL_H = 520, 330
BRANDS = ("techtrack", "techtrack-kids")
COMPOSITIONS = ("mark", "stacked", "horizontal", "wordmark")
VARIANTS = ("white", "lemon", "transparent")
BACKGROUNDS = {"white": "#FFFFFF", "lemon": "#FFC93D", "transparent": "#E3E7EB"}

sheet = Image.new("RGB", (CELL_W * len(VARIANTS), CELL_H * len(BRANDS) * len(COMPOSITIONS)), "#E8ECEF")
draw = ImageDraw.Draw(sheet)

for row, (brand, composition) in enumerate((b, c) for b in BRANDS for c in COMPOSITIONS):
    brand_root = ROOT / "brands" / brand
    for col, variant in enumerate(VARIANTS):
        if variant == "transparent":
            svg_path = brand_root / "vector" / composition / f"{brand}-{composition}-master.svg"
        else:
            svg_path = brand_root / "logos" / "reconstructed" / "svg" / f"{brand}-{composition}-{variant}-v1.svg"
        if not svg_path.is_file():
            raise FileNotFoundError(svg_path)
        rendered = cairosvg.svg2png(url=str(svg_path), output_width=450)
        with Image.open(io.BytesIO(rendered)) as source:
            artwork = source.convert("RGBA")
        artwork.thumbnail((CELL_W - 42, CELL_H - 72))
        x0, y0 = col * CELL_W, row * CELL_H
        draw.rectangle((x0 + 8, y0 + 8, x0 + CELL_W - 8, y0 + CELL_H - 8), fill=BACKGROUNDS[variant], outline="#C7CDD2", width=1)
        x = x0 + (CELL_W - artwork.width) // 2
        y = y0 + 48 + (CELL_H - 68 - artwork.height) // 2
        sheet.paste(artwork, (x, y), artwork)
        draw.text((x0 + 18, y0 + 18), f"{brand} · {composition} · {variant}", fill="#17212B")

target = ROOT / "TechTrack_Visual_Contact_Sheet.png"
sheet.save(target, optimize=True)
print(target)
