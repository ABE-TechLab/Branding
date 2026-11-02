#!/usr/bin/env python3
"""Validate owner-reviewed TechTrack reconstructions and the black-background exclusion."""
from pathlib import Path
from PIL import Image
import hashlib, json, re, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CHECKS = 0

for brand in ("techtrack", "techtrack-kids"):
    base = ROOT / "brands" / brand
    manifest = json.loads((base / "brand.json").read_text(encoding="utf-8"))
    assert manifest["approval"] == "owner-reviewed-except-black-background"
    assert manifest["status"] == "owner-reviewed-with-exclusions"
    assert manifest["excluded_variants"]["black"]["status"] == "deferred"
    assert "transparent" in manifest["assets"]["mark"]

    for filename, record in manifest["source_inventory"].items():
        source = base / "source" / filename
        assert source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() == record["original_sha256"], source
        CHECKS += 1

    for composition in ("mark", "stacked", "horizontal", "wordmark"):
        master = base / "vector" / composition / f"{brand}-{composition}-master.svg"
        files = [master]
        for background in ("white", "lemon"):
            files.append(base / "logos" / "reconstructed" / "svg" / f"{brand}-{composition}-{background}-v1.svg")

        for path in files:
            source = path.read_text(encoding="utf-8")
            root = ET.fromstring(source)
            assert root.attrib.get("data-provenance") == "vector-reconstructed-from-raster"
            assert root.attrib.get("data-approval") == "owner-reviewed-except-black-background"
            assert len(list(root.iter("{http://www.w3.org/2000/svg}path"))) > 0
            assert "<image" not in source and "base64" not in source and "data:image/" not in source
            assert not re.search(r"<(?:script|foreignObject|iframe)\b|onload\s*=", source, re.I)
            dimensions = manifest["sources"][composition]["embedded_png_dimensions"]
            assert root.attrib["viewBox"].split()[-2:] == [str(value) for value in dimensions]
            CHECKS += 1

        widths = (512, 1024, 2048, 4096) if composition == "mark" else (1024, 2048, 4096)
        for background in ("white", "lemon", "transparent"):
            for width in widths:
                image_path = base / "logos" / "reconstructed" / "png" / f"{brand}-{composition}-{background}-{width}w-v1.png"
                assert image_path.is_file(), image_path
                with Image.open(image_path) as image:
                    image.load()
                    assert image.format == "PNG" and image.width == width, image_path
                    source_width, source_height = manifest["sources"][composition]["embedded_png_dimensions"]
                    assert abs(image.height - (width * source_height / source_width)) <= 0.51, image_path
                    alpha = image.convert("RGBA").getchannel("A")
                    assert alpha.getextrema() == ((0, 255) if background == "transparent" else (255, 255)), (image_path, alpha.getextrema())
                CHECKS += 1

        assert not list((base / "logos" / "reconstructed" / "svg").glob(f"{brand}-{composition}-black-v1.svg"))
        assert not list((base / "logos" / "reconstructed" / "png").glob(f"{brand}-{composition}-black-*w-v1.png"))

print(f"PASS: {CHECKS} source, SVG, export-size and transparency checks.")
print("PASS: no black-background reconstructed variants are generated or listed.")
print("Usage: use the transparent assets on black or dark surfaces.")
