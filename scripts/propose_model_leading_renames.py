#!/usr/bin/env python3
"""Propose `Part for Device` names for part titles that lead with a device model.

These lead with a trademarked model name (`iPhone 11 Back Camera`) rather than a
brand, so they carry the same "reads like an Apple product" risk as the
brand-leading titles. Accessories, tools and whole devices are excluded.
"""
from __future__ import annotations

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repairdesk.client import RepairDeskClient

OUT_CSV = "data/model-leading-rename-proposal.csv"

MODEL_LEAD = re.compile(r"^\s*(iphone|ipad|galaxy)\b", re.I)

# Shop accessories, retail cables/cases and tools - not replacement parts.
EXCLUDE_IDS = {
    "12827663", "12828080", "12828034", "12827581", "12827580",
    "12828252", "12998627", "12997807", "13000316",
}

# Ordered longest-first so multi-word parts win over their single-word prefixes.
PARTS = [
    "Home Button Fingerprint Sensor Flex with Plastic Home Button",
    "Home Button Fingerprint Sensor Flex",
    "Home Button Control Board", "Home Button Control Flex",
    "Home Button Extender Cable", "Home Button with Flex", "Home Button",
    "Power Volume Silent Headphone Jack Flex", "Power Volume Silent Control Flex",
    "Power Volume Vibrate Flex", "Power Volume Flex",
    "Volume Silent Headphone Jack Flex", "Volume & Power Flex",
    "Power Button and Flash Flex", "Power Button Control Flex",
    "Power Button Flex Cable", "Power Button", "Volume Button Control Flex",
    "Dual Rear Camera lens Cover", "Rear Camera Lens Cover", "Rear Main Camera",
    "Rear Camera", "Back Camera", "Front Camera Assembly",
    "Front Camera Sensor Flex", "Front Camera Flex", "Front Camera",
    "Main Camera", "Camera Lens", "camera lens",
    "Back Housing with Parts", "Back Housing",
    "Charging Dock Flex Cable", "Charging Dock Flex", "Charging Dock",
    "Charging Port Flex Cable", "Charging Port Flex", "Charging Port",
    "Charger Port Flex", "chargingport replacment",
    "Wireless Charging Antenna", "Wireless Charging Pad Flex",
    "Wireless Charging pad flex", "Wireless Charger Pad Flex",
    "wireless charging pad",
    "Front Earpiece and Sensor Flex", "Earspeaker Assembly Flex",
    "Earpiece Speaker", "Ear Speaker with cable", "Earspeaker Flex", "Earpiece",
    "Loud Speaker / Wifi Antenna Replacement", "Loud Speaker",
    "Charging Port with Speaker", "Charging Port and Microphone",
    "Charging Port Microphone",
    "Headphone Jack", "Audio Control Cable and Brackets",
    "Screen Assembly", "Touch Glass", "LCD (Retina)", "LCD", "Screen",
    "Battery", "Vibrator", "Proximity Sensor", "Bluetooth Antenna",
    "WiFi Antenna Signal Flex", "WiFi Antenna Flex", "3G Antenna",
    "Flash light Flex", "flash light  flex", "flash light flex",
    "Glass Protector", "front camera flex",
]

# Real parts the part dictionary cannot split automatically.
MANUAL = {
    "12827596": "Back Cover for iPhone 4 Black",
    "12827595": "Back Cover for iPhone 4S Black",
    "12827592": "Back Cover for iPhone 4S White",
    "12827599": "SIM Card Tray for iPhone 4 / 4S",
    "12827647": "SIM Card Tray for iPhone 6",
    "12827648": "SIM Card Tray for iPhone 6 Plus",
    "12827675": "SIM Card Tray for iPhone 6S",
    "12827677": "SIM Card Tray for iPhone 6S Plus",
    "13000045": "SIM Card Tray for iPhone XR Black",
    "12998240": "Logic Board with Touch ID for iPhone 7 (256GB)",
    "12999946": "Logic Board for iPhone XR",
}

PART_CANON = {
    "back camera": "Rear Camera",
    "main camera": "Main Rear Camera",
    "camera lens": "Camera Glass Lens",
    "dual rear camera lens cover": "Rear Camera Lens Cover",
    "earpiece": "Ear Speaker",
    "earpiece speaker": "Ear Speaker",
    "earspeaker flex": "Ear Speaker Flex",
    "earspeaker assembly flex": "Ear Speaker Assembly Flex",
    "ear speaker with cable": "Ear Speaker with Cable",
    "front earpiece and sensor flex": "Ear Speaker & Sensor Flex",
    "charger port flex": "Charging Port Flex",
    "chargingport replacment": "Charging Port",
    "charging port with speaker": "Charging Port with Loud Speaker",
    "charging port and microphone": "Charging Port with Microphone",
    "charging port microphone": "Charging Port with Microphone",
    "wireless charger pad flex": "Wireless Charging Pad Flex",
    "wireless charging pad flex": "Wireless Charging Pad Flex",
    "wireless charging pad": "Wireless Charging Pad",
    "flash light flex": "Flash Light Flex",
    "flash light  flex": "Flash Light Flex",
    "front camera flex": "Front Camera Flex",
    "lcd": "LCD Screen",
    "lcd (retina)": "LCD Screen (Retina)",
    "loud speaker / wifi antenna replacement": "Loud Speaker / WiFi Antenna",
    "3g antenna": "3G Antenna",
    "wifi antenna flex": "WiFi Antenna Flex",
    "wifi antenna signal flex": "WiFi Antenna Signal Flex",
    "home button fingerprint sensor flex with plastic home button":
        "Home Button with Fingerprint Sensor Flex & Plastic Button",
    "home button fingerprint sensor flex": "Home Button with Fingerprint Sensor Flex",
    "home button with flex": "Home Button with Flex",
    "volume & power flex": "Volume & Power Button Flex",
    "power volume vibrate flex": "Power / Volume / Vibrate Flex",
    "power volume flex": "Power / Volume Flex",
    "power volume silent control flex": "Power / Volume / Silent Control Flex",
    "power volume silent headphone jack flex": "Power / Volume / Silent & Headphone Jack Flex",
    "volume silent headphone jack flex": "Volume / Silent & Headphone Jack Flex",
    "power button and flash flex": "Power Button & Flash Flex",
    "audio control cable and brackets": "Audio Control Cable with Brackets",
    "back housing with parts": "Back Housing with Parts",
}


def canon_device(text: str) -> str:
    text = re.sub(r"\s*/\s*", " / ", re.sub(r"\s+", " ", text)).strip(" -/,")
    text = re.sub(r"^iphone\b", "iPhone", text, flags=re.I)
    text = re.sub(r"^ipad\b", "iPad", text, flags=re.I)
    text = re.sub(r"^galaxy\b", "Samsung Galaxy", text, flags=re.I)
    text = re.sub(r"\bipad\b", "iPad", text, flags=re.I)
    text = re.sub(r"\biphone\b", "iPhone", text, flags=re.I)
    text = re.sub(r"\bmini\b", "mini", text)
    text = re.sub(r"\bplus\b", "Plus", text, flags=re.I)
    text = re.sub(r"\bpro\b", "Pro", text, flags=re.I)
    text = re.sub(r"\bmax\b", "Max", text, flags=re.I)
    text = re.sub(r"\bair\b", "Air", text, flags=re.I)
    text = re.sub(r"\bse\b", "SE", text, flags=re.I)
    text = re.sub(r"\bgen\b", "Gen", text, flags=re.I)
    text = re.sub(r"\b(\d+)s\b", lambda m: m.group(1) + "S", text)
    text = re.sub(r"\bxr\b", "XR", text, flags=re.I)
    text = re.sub(r"\bxs\b", "XS", text, flags=re.I)
    return text.strip()


COLOURS = [
    "rose gold", "space grey", "space gray", "golden", "silver", "black",
    "white", "grey", "gray", "gold", "blue", "red", "green", "purple",
]


def canon_tail(text: str) -> str:
    for colour in COLOURS:
        text = re.sub(
            rf"\b{colour}\b",
            colour.title(),
            text,
            flags=re.I,
        )
    return text


def split_name(name: str):
    best = None
    for part in PARTS:
        index = name.lower().find(part.lower())
        if index <= 0:
            continue
        if best is None or index < best[0] or (index == best[0] and len(part) > len(best[1])):
            best = (index, part)
    if best is None:
        return None
    index, part = best
    device = canon_device(name[:index])
    tail = canon_tail(re.sub(r"\s+", " ", name[index + len(part):]).strip(" -,"))
    part_name = PART_CANON.get(part.lower(), part)
    return part_name, device, tail


def main() -> int:
    client = RepairDeskClient()
    rows = []
    for item in client.iter_inventory():
        item_id = str(item.get("id"))
        name = (item.get("name") or "").strip()
        if item_id in EXCLUDE_IDS or not MODEL_LEAD.match(name):
            continue
        if item_id in MANUAL:
            rows.append((item_id, item.get("sku") or "-", name, MANUAL[item_id]))
            continue
        split = split_name(name)
        if split is None:
            rows.append((item_id, item.get("sku") or "-", name, "<NO MATCH>"))
            continue
        part_name, device, tail = split
        new = f"{part_name} for {device}"
        if tail:
            new += f" {tail}"
        rows.append((item_id, item.get("sku") or "-", name, re.sub(r"\s+", " ", new).strip()))

    rows.sort(key=lambda r: r[3].lower())
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "sku", "old_name", "proposed_name"])
        writer.writerows(rows)

    for item_id, sku, old, new in rows:
        print(f"{item_id} | {old}\n           -> {new}")
    print(f"\n{len(rows)} proposals -> {OUT_CSV}")
    print("unmatched:", sum(1 for r in rows if r[3] == "<NO MATCH>"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
