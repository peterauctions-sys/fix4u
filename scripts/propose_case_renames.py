#!/usr/bin/env python3
"""Propose `<Case description> for <Device>` names for case and cover titles.

Cases are third-party accessories, so the case brand (hoco., CASE-MATE, Baseus)
may lead the title; the Apple or Samsung model must sit after `for` so the title
reads as "fits this phone" rather than as the phone maker's own product.
"""
from __future__ import annotations

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repairdesk.client import RepairDeskClient

OUT_CSV = "data/case-rename-proposal.csv"

CASE_WORD = re.compile(r"\b(case|cases|cover|covers)\b", re.I)
BRANDS = {"iphone", "ipad", "samsung", "galaxy", "huawei", "hiawei", "meizu", "airpods"}
CASE_BRANDS = ("CASE-MATE", "hoco.")

MODEL_WORDS = {
    "pro", "max", "plus", "mini", "air", "ultra", "edge", "se", "note", "lite",
    "nova", "duo", "galaxy", "tab", "x", "xs", "xr", "5g", "4g", "/", "and", "&",
}

COLOURS = [
    "dark blue", "rose gold", "rosegold", "space grey", "black", "white",
    "blue", "pink", "red", "silver", "gold", "grey", "brown", "purple",
    "orange", "green",
]

# Shop goods that are not phone/tablet cases, plus items already renamed as parts.
EXCLUDE_IDS = {
    "12827944", "13000790", "12998434", "12999796", "12999892", "13000220",
    "12999315", "12998297", "12997829", "12828117", "12827921", "13000104",
    "12999293", "12999152", "12999155", "12999156", "12999159", "13000115",
    "12827527", "12997543", "12997789", "12999020",
    "12997372", "12827596", "12827595", "12827592", "12999541", "12999347",
    "12999360", "12827593", "12828347", "12827904", "12827798", "13001107",
    "12997458", "12998925", "12997459", "12998926", "12997449",
}

PRE_CLEAN = [
    (r"\biPhone\s+iPhone\b", "iPhone"),
    (r"\bHiawei\b", "Huawei"),
    (r"\s+", " "),
]

DEVICE_FIXES = [
    (r"\b[Ii][Pp]hone\b", "iPhone"),
    (r"\b[Ii][Pp]ad\b", "iPad"),
    (r"\bMini\b", "mini"),
    (r"\b(?:PLUS|plus)\b", "Plus"),
    (r"\b(?:MAX|max)\b", "Max"),
    (r"\bpro\b", "Pro"),
    (r"\bedge\b", "Edge"),
    (r"\bXs\b", "XS"),
    (r"\bXr\b", "XR"),
    (r"\bSE2\b", "SE 2"),
    (r"\bSE3\b", "SE 3"),
    (r"\bNote3\b", "Note 3"),
    (r"\bMEIZU\b", "Meizu"),
    (r"\s*/\s*", " / "),
]

SAMSUNG_BARE = re.compile(r"^Samsung\s+(?!Galaxy\b)", re.I)
SAMSUNG_LINE = re.compile(r"^Samsung\s+(?:Note\s*\d|[AMZSJ]\d)", re.I)

# Titles the token rules cannot split cleanly.
MANUAL = {
    "12827574": "Back Covers for iPhone 4 White - Wholesale Lot of 10",
    "12828102": "Bumper Case for iPhone 4 / 4S (Various Colours)",
    "12997755": "iFrogz Case / Cover for iPhone 5 / 5s Black",
    "12997756": "iFrogz Case / Cover for iPhone 5 / 5s Blue",
    "12828031": "Wooden Pattern Case for iPhone 8 / 7 Plus / 6s",
    "12828035": "Drop Resistant Protection Case for iPhone 8",
    "12828033": "Luxury Metal Case with Matt Plastic Round for iPhone 6 Dark Blue",
    "12828099": "Luxury Metal Case with Matt Plastic Round for iPhone 6 Pink",
    "12828097": "Luxury Metal Case with Matt Plastic Round for iPhone 6 Red",
    "12828048": "Luxury Metal Case for iPhone 6 Plus Black",
    "12828085": "Luxury Metal Case for iPhone 6 Plus Dark Blue",
    "12828083": "Luxury Metal Case for iPhone 6 Plus Pink",
    "12828084": "Luxury Metal Case for iPhone 6 Plus Red",
    "12828018": "Luxury Metal Case for iPhone 6 Plus Silver",
    "12828028": "Case for Meizu Note 3",
    "12997790": "Back Case with Ring Holder for Samsung Galaxy S7 Edge",
    "12997791": "Back Case with Ring Holder for Samsung Galaxy S8 Plus",
    "13000040": 'Wallet Case for iPad 10.2" Black',
    "12998076": "Leather Flip Case for iPad Air 1 / iPad Pro 9.7 (2017 / 2018)",
    "12998075": 'Leather Flip Case for iPad Air 10.5" (2019)',
    "12998074": "Leather Flip Case for iPad Air 2 / iPad 9.7 (2017 / 2018)",
    "12998265": "Waterproof Case for iPhone 6 / 6S Plus",
    "12827734": "Waterproof Case for iPhone (Full Protection)",
    "12827735": "Waterproof Heavy Duty Case for iPhone",
    "13001023": "Clear Phone Case for iPhone 14 Pro Max",
    "13001269": "Maxguard Space Tech Armor MagFit Case for iPhone DUO",
    "13001243": "Oxford Leather Case for AirPods 3 Brown",
    "13001244": "Oxford Leather Case for AirPods 3 Blue",
    "12999750": "Anti-Drop Transparent Case for Samsung Galaxy S23 / S23 Plus / S23 Ultra",
    "12999679": "Transparent Case for Samsung Galaxy A90 5G",
    "13001083": "Adventurer Heavy Duty Case for iPhone 16 Black",
    "13001084": "Adventurer Heavy Duty Case for iPhone 16 Pro Black",
    "13001085": "Adventurer Heavy Duty Case for iPhone 16 Pro Max Black",
    "12998002": "Canvas Wallet Case for Samsung Galaxy A20 / A30",
    "12998422": 'Clear Back Case for iPhone 12 mini (5.4")',
    "12998429": 'Clear Back Case for iPhone 12 Pro Max (6.7")',
    "12998426": 'Clear Back Case for iPhone 12 / 12 Pro (6.1")',
    "13000316": "Clear MagSafe Case for iPhone 13 / 14 (Wireless Charging, Anti-Scratch)",
    "12828015": "Clear Case with Standing Holder for iPhone X",
    "12828026": "Motomo Brushed Aluminium Thin Back Case for Samsung Galaxy S5",
}


def model_ish(token: str) -> bool:
    low = token.lower().strip(",")
    if low in MODEL_WORDS:
        return True
    if re.fullmatch(r"\(?[\d\.]+(?:''|\"|\s*inch)?\)?", low):
        return True
    if re.fullmatch(r"[\w\./'\"-]*\d[\w\./'\"-]*", low):
        return True
    if "/" in low and all(p in MODEL_WORDS for p in low.split("/") if p):
        return True
    return False


def split_colour(desc: str) -> tuple[str, str]:
    """Pull a trailing colour off the description so it can follow the device."""
    for colour in COLOURS:
        match = re.search(rf"\s*-?\s*\b{colour}\b\s*$", desc, re.I)
        if match:
            return desc[: match.start()].strip(" -,"), colour.title()
    return desc, ""


def canon_device(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip(" -,/")
    for pattern, repl in DEVICE_FIXES:
        text = re.sub(pattern, repl, text)
    text = re.sub(r"^Galaxy\b", "Samsung Galaxy", text)
    if SAMSUNG_LINE.match(text):
        text = SAMSUNG_BARE.sub("Samsung Galaxy ", text)
    return re.sub(r"\s+", " ", text).strip(" -,/")


def canon_desc(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip(" -,/")
    text = re.sub(r"\bPhone Case\b", "Case", text, flags=re.I)
    text = re.sub(r"\bcases?\b", "Case", text)
    text = re.sub(r"\bcovers?\b", "Cover", text)
    text = re.sub(r"\bWater Proof\b", "Waterproof", text, flags=re.I)
    text = re.sub(r"\bwallet\b", "Wallet", text)
    text = re.sub(r"\btpu\b", "TPU", text, flags=re.I)
    text = re.sub(r"\bjel\b", "Gel", text, flags=re.I)
    text = re.sub(r"\bAnti-drop\b", "Anti-Drop", text)
    text = re.sub(r"\bcard slot\b", "Card Slot", text, flags=re.I)
    text = re.sub(r"\bCase(\s+Case)+\b", "Case", text)
    return re.sub(r"\s+", " ", text).strip(" -,/")


def propose(name: str) -> str | None:
    prefix = ""
    body = name
    for brand in CASE_BRANDS:
        if body.startswith(brand):
            prefix, body = brand + " ", body[len(brand):].strip()
            break

    tokens = body.split()
    start = next(
        (i for i, t in enumerate(tokens) if t.lower().strip(".,") in BRANDS), None
    )
    if start is None:
        return None

    end = start + 1
    while end < len(tokens) and model_ish(tokens[end]):
        end += 1

    device = canon_device(" ".join(tokens[start:end]))
    before = " ".join(tokens[:start])
    after = " ".join(tokens[end:])

    if before.lower().endswith(" for") or before.lower() == "for":
        desc, tail = before[: -len("for")].strip(), after
    elif before:
        desc, tail = before, after
    else:
        desc, tail = after, ""

    desc = canon_desc(desc)
    if not desc or not CASE_WORD.search(f"{desc} {tail}"):
        return None

    desc, colour = split_colour(desc)
    tail = tail.strip(" -,")
    for name in COLOURS:
        tail = re.sub(rf"\b{name}\b", name.title(), tail, flags=re.I)

    out = f"{prefix}{desc} for {device}"
    if tail:
        out += f" {tail}"
    if colour:
        out += f" {colour}"
    return re.sub(r"\s+", " ", out).strip()


def main() -> int:
    client = RepairDeskClient()
    rows = []
    for item in client.iter_inventory():
        item_id = str(item.get("id"))
        name = (item.get("name") or "").strip()
        for pattern, repl in PRE_CLEAN:
            name = re.sub(pattern, repl, name)
        name = name.strip()
        if item_id in EXCLUDE_IDS or not CASE_WORD.search(name):
            continue
        new = MANUAL.get(item_id) or propose(name)
        if new is None or new == name:
            continue
        rows.append((item_id, item.get("sku") or "-", name, new))

    rows.sort(key=lambda r: r[3].lower())
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "sku", "old_name", "proposed_name"])
        writer.writerows(rows)

    for item_id, sku, old, new in rows:
        print(f"{item_id} | {old}\n           -> {new}")
    print(f"\n{len(rows)} proposals -> {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
