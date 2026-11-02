#!/usr/bin/env python3
"""Assert every generated brand page uses the exact same shared navigation and width rules."""
from pathlib import Path
import argparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-root", type=Path, default=ROOT / "public")
    args = parser.parse_args()
    public_root = args.public_root.resolve()
    pages = [public_root / "index.html"]
    brands = public_root / "brands"
    if brands.exists():
        pages.extend(sorted(brands.rglob("index.html")))
    pages = [path for path in pages if path.is_file()]
    if not pages:
        raise SystemExit("No generated brand pages found")

    canonical_sidebar = None
    canonical_css = None
    failures = []
    for path in pages:
        html = path.read_text(encoding="utf-8")
        sidebars = re.findall(r'<aside class="brand-sidebar"[^>]*>.*?</aside>', html, re.S)
        if len(sidebars) != 1:
            failures.append(f"{path}: expected one sidebar, found {len(sidebars)}")
            continue

        sidebar = re.sub(r' aria-current="page"', "", sidebars[0])
        if canonical_sidebar is None:
            canonical_sidebar = sidebar
        elif sidebar != canonical_sidebar:
            failures.append(f"{path}: navigation markup differs from the shared component")

        if len(re.findall(r' aria-current="page"', sidebars[0])) > 1:
            failures.append(f"{path}: multiple active brand links")

        css_blocks = re.findall(
            r'/\* BRAND_LIBRARY_SHELL_START \*/.*?/\* BRAND_LIBRARY_SHELL_END \*/',
            html,
            re.S,
        )
        if len(css_blocks) != 1:
            failures.append(f"{path}: expected one shared navigation/layout CSS block")
        elif canonical_css is None:
            canonical_css = css_blocks[0]
        elif css_blocks[0] != canonical_css:
            failures.append(f"{path}: shared navigation/layout CSS differs")

    required_css = (
        "--brand-sidebar-width:260px",
        "grid-template-columns:var(--brand-sidebar-width)",
        "width:var(--brand-sidebar-width)",
        ":root{--brand-sidebar-width:220px}",
    )
    for token in required_css:
        if canonical_css is None or token not in canonical_css:
            failures.append(f"shared CSS is missing fixed-width rule: {token}")

    expected_links = (
        '/brands/abe-techlab/',
        '/brands/abemail/',
        '/brands/techtrack/',
        '/brands/techtrack-kids/',
    )
    if canonical_sidebar:
        for link in expected_links:
            if f'href="{link}"' not in canonical_sidebar:
                failures.append(f"shared navigation is missing {link}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"PASS: {len(pages)} pages use identical shared navigation markup and sidebar width rules.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
