#!/usr/bin/env python3
"""Rebuild the banner's artwork and typefaces from the original Canva PDF.

The original export (``source.pdf``, 850 x 2000 mm) stores its artwork as
Adobe-style inverted CMYK JPEGs plus separate soft masks, and its typefaces as
subsetted TrueType fonts with Identity-H encoding and no ``cmap`` table.

Running this script regenerates everything ``banner.html`` needs:

    assets/opera_face.png   assets/mountain_a.png   assets/mountain_b.png
    assets/square.png       assets/masks/mask_RC.png
    fonts/web/*.ttf         (subset fonts with a usable cmap)

Usage:  python3 extract_assets.py [source.pdf]
"""

from __future__ import annotations

import os
import re
import sys

import pikepdf
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from PIL import Image, ImageChops

import numpy as np

Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "assets", "_raw")

# Height in px each asset is downsampled to, sized for 150 dpi at the
# dimensions used in banner.html.
TARGET_HEIGHT = {
    "opera_face.png": 4300,
    "mountain_a.png": 2150,
    "mountain_b.png": 1900,
    "square.png": 700,
}


def extract_images(pdf_path: str) -> None:
    os.makedirs(RAW, exist_ok=True)
    os.system(f'pdfimages -all -p "{pdf_path}" "{RAW}/img"')


def compose(base: str, mask: str, out: str) -> Image.Image:
    """Combine an inverted-CMYK image with its soft mask into a trimmed RGBA PNG."""
    im = Image.open(os.path.join(RAW, base))
    if im.mode == "CMYK":
        im = ImageChops.invert(im)
    im = im.convert("RGBA")

    m = Image.open(os.path.join(RAW, mask)).convert("L")
    if m.size != im.size:
        m = m.resize(im.size, Image.LANCZOS)
    im.putalpha(m)

    bbox = im.getchannel("A").getbbox()
    if bbox:
        im = im.crop(bbox)

    target = TARGET_HEIGHT.get(os.path.basename(out))
    if target and im.height > target:
        im = im.resize((round(im.width * target / im.height), target), Image.LANCZOS)

    im.save(out, optimize=True)
    print("wrote", os.path.relpath(out, HERE), im.size)
    return im


def slice_masks(sheet: Image.Image, out_dir: str, keep: set[str]) -> None:
    """Cut the 4x3 opera-mask sheet into individual transparent PNGs."""
    os.makedirs(out_dir, exist_ok=True)
    alpha = np.array(sheet.getchannel("A"))

    def bands(projection, floor=2, min_len=60):
        out, start = [], None
        for i, v in enumerate(projection):
            if v > floor and start is None:
                start = i
            elif v <= floor and start is not None:
                out.append((start, i))
                start = None
        if start is not None:
            out.append((start, len(projection)))
        return [b for b in out if b[1] - b[0] > min_len]

    cols = bands((alpha > 8).sum(axis=0))
    rows = bands((alpha > 8).sum(axis=1))

    for ri, (y0, y1) in enumerate(rows):
        for ci, (x0, x1) in enumerate(cols):
            name = f"mask_{ri}{ci}.png"
            if keep and name not in keep:
                continue
            tile = sheet.crop((x0, y0, x1, y1))
            bbox = tile.getchannel("A").getbbox()
            if not bbox:
                continue
            tile = tile.crop(bbox)
            if tile.height > 950:
                tile = tile.resize((round(tile.width * 950 / tile.height), 950), Image.LANCZOS)
            tile.save(os.path.join(out_dir, name), optimize=True)
            print("wrote", name, tile.size)


def parse_tounicode(data: str) -> dict[int, str]:
    mapping: dict[int, str] = {}
    for blk in re.findall(r"beginbfchar(.*?)endbfchar", data, re.S):
        for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            mapping[int(src, 16)] = "".join(
                chr(int(dst[i:i + 4], 16)) for i in range(0, len(dst), 4)
            )
    for blk in re.findall(r"beginbfrange(.*?)endbfrange", data, re.S):
        for lo, hi, dst in re.findall(
            r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk
        ):
            base = int(dst, 16)
            for k in range(int(lo, 16), int(hi, 16) + 1):
                mapping[k] = chr(base + (k - int(lo, 16)))
    return mapping


def extract_fonts(pdf: pikepdf.Pdf) -> None:
    """Pull the subset typefaces out of the PDF and give them a real cmap."""
    out_dir = os.path.join(HERE, "fonts", "web")
    os.makedirs(out_dir, exist_ok=True)
    tmp_dir = os.path.join(HERE, "fonts", "_raw")
    os.makedirs(tmp_dir, exist_ok=True)

    for page in pdf.pages:
        for _, font in page.get("/Resources", {}).get("/Font", {}).items():
            name = str(font.get("/BaseFont", "")).lstrip("/").replace("+", "_")
            descendants = font.get("/DescendantFonts")
            desc = descendants[0].get("/FontDescriptor") if descendants else font.get("/FontDescriptor")
            if not desc or "/FontFile2" not in desc or "/ToUnicode" not in font:
                continue

            raw = os.path.join(tmp_dir, f"{name}.ttf")
            with open(raw, "wb") as fh:
                fh.write(bytes(desc["/FontFile2"].read_bytes()))

            cid2uni = parse_tounicode(bytes(font["/ToUnicode"].read_bytes()).decode("latin-1"))
            ttf = TTFont(raw)
            order = set(ttf.getGlyphOrder())
            uni2glyph = {
                ord(s): f"glyph{cid:05d}"
                for cid, s in cid2uni.items()
                if len(s) == 1 and f"glyph{cid:05d}" in order
            }
            if not uni2glyph:
                continue

            cmap = newTable("cmap")
            cmap.tableVersion = 0
            sub4 = CmapSubtable.newSubtable(4)
            sub4.platformID, sub4.platEncID, sub4.language = 3, 1, 0
            sub4.cmap = {k: v for k, v in uni2glyph.items() if k <= 0xFFFF}
            sub12 = CmapSubtable.newSubtable(12)
            sub12.platformID, sub12.platEncID, sub12.language = 3, 10, 0
            sub12.format, sub12.reserved, sub12.length, sub12.nGroups = 12, 0, 0, 0
            sub12.cmap = dict(uni2glyph)
            cmap.tables = [sub4, sub12]
            ttf["cmap"] = cmap

            dest = os.path.join(out_dir, f"{name}.ttf")
            ttf.save(dest)
            chars = "".join(sorted({c for s in cid2uni.values() for c in s}))
            print("font", name, "->", chars)


def main() -> int:
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "source.pdf")
    if not os.path.exists(pdf_path):
        print(f"missing {pdf_path} — see README.md")
        return 1

    extract_images(pdf_path)
    assets = os.path.join(HERE, "assets")
    os.makedirs(assets, exist_ok=True)

    compose("img-001-000.jpg", "img-001-001.jpg", os.path.join(assets, "mountain_a.png"))
    compose("img-001-002.jpg", "img-001-003.jpg", os.path.join(assets, "mountain_b.png"))
    compose("img-001-004.jpg", "img-001-005.jpg", os.path.join(assets, "square.png"))
    compose("img-001-014.jpg", "img-001-015.png", os.path.join(assets, "opera_face.png"))

    sheet = compose("img-001-006.jpg", "img-001-007.png", os.path.join(RAW, "_sheet.png"))
    slice_masks(
        sheet,
        os.path.join(assets, "masks"),
        keep={"mask_01.png", "mask_02.png", "mask_03.png", "mask_10.png", "mask_11.png"},
    )

    extract_fonts(pikepdf.open(pdf_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
