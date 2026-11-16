#!/usr/bin/env python3
"""Rename brand-leading replacement-part titles to the `Part for Device` form.

Genuine brand accessories and whole devices keep their brand-leading titles.
Results are written incrementally so an interrupted run can be resumed.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repairdesk.client import RepairDeskClient, RepairDeskError

RESULTS_JSON = "data/brandleading-rename-results.json"
RESULTS_CSV = "data/brandleading-rename-results.csv"
PLAN_CSV = "data/brandleading-rename-plan.csv"

# Genuine brand accessories / whole devices -> brand stays in front.
SKIP = {
    "12997901": "whole device (refurbished Google speaker)",
    "12998318": "whole device (refurbished Google speaker)",
    "12828017": "genuine Huawei accessory cable",
    "12997917": "genuine Samsung charger",
    "12998314": "genuine Samsung charger",
    "12827811": "whole device (used Galaxy A72)",
    "12828223": "whole device (used Samsung camera)",
    "12827929": "genuine Xiaomi speaker",
    "12828255": "genuine Xiaomi car charger",
    "12997904": "genuine Samsung power pack",
    "12998325": "genuine Samsung power pack",
    "12998651": "whole device (Moto G8)",
    # Apple-branded power accessories: wording depends on whether stock is
    # genuine Apple or aftermarket, so the owner decides before any rename.
    "12827915": "Apple-branded charger - owner to confirm genuine vs aftermarket",
    "12827724": "Apple-branded cable - owner to confirm genuine vs aftermarket",
    "12998403": "Apple-branded charger - owner to confirm genuine vs aftermarket",
}

RENAMES = {
    # Apple
    "12997370": "Battery for MacBook Air A1405 7.6V 6700mAh",
    "12999939": "Charging Port Flex for iPad 6th Gen",
    "12999813": "Rear Camera for iPhone 12",
    "13000489": "Rear Camera for iPhone 12 Pro",
    "13000248": "Rear Camera for iPhone 14",
    "13000249": "Back Housing for iPhone XR Black",
    "12998889": "Back Housing with Frame for iPhone XS",
    "12828268": "Battery for Apple Watch Series 6 44mm",
    # Google
    "12999941": "LCD Screen for Google Pixel 4a 5G",
    "12999940": "LCD Screen for Google Pixel 4a",
    # Huawei
    "12827817": "Screen for Huawei Mate 9 with Frame",
    "12828215": "Screen for Huawei Mate 9 without Frame",
    "12998596": "Battery for Huawei Mate 10 Pro / P20 Pro 3900mAh HB436486ECW",
    "12997860": "Screen for Huawei Nova 2i",
    "12998107": "Back Glass for Huawei Nova 3i",
    "12998067": "Screen for Huawei Nova 3i",
    "12998034": "Screen for Huawei Nova 5T",
    "12998225": "Screen for Huawei Nova 5T",
    "12828180": "Screen for Huawei P10 without Frame",
    "12998136": "Screen for Huawei P20 Lite / Nova 3e",
    "12828131": "Screen for Huawei P9 Lite with Frame",
    "12828208": "Screen for Huawei P9 Lite without Frame",
    "12827826": "Screen for Huawei P9 with Frame",
    "12828234": "Screen for Huawei P9 without Frame",
    "12998091": "Screen for Huawei P10 Plus Black",
    "12998125": "Screen for Huawei P20",
    # LG / Motorola / Nokia / OPPO
    "12827865": "Screen Assembly for LG Nexus 5 Black",
    "12828213": "Screen with Frame for Motorola Moto G2 Black (XT1063 / XT1064 / XT1068)",
    "12827936": "LCD Screen for Nokia N8",
    "12827970": "LCD Screen for Nokia N95 8GB + Free Tools",
    "12827969": "LCD Screen for Nokia N95 Grade A+ + Free Tools",
    "12827978": "Touch Screen Digitizer for Nokia X6 Grade A+",
    "12827781": (
        "OLED Screen Digitizer Assembly for OPPO Reno8 Lite 5G CPH2343 "
        "without Frame Black (Fingerprint Support)"
    ),
    # Samsung
    "12999380": "Motherboard Flex for Samsung Galaxy A31",
    "12827723": "Loud Speaker for Samsung Galaxy Ace S5830",
    "12998330": "Rear Camera for Samsung Galaxy S10 Plus",
    "12828308": "Rear Camera for Samsung Galaxy S2 i9100",
    "12828354": "Earpiece & Headphone Jack Flex for Samsung Galaxy S2 i9100",
    "12827559": "Front Camera for Samsung Galaxy S2 i9100",
    "12828386": "Front Housing Frame for Samsung Galaxy S2 i9100 Black",
    "12828387": "Front Housing Frame for Samsung Galaxy S2 i9100 White (Silver)",
    "12827622": "Home Button & Sensor Ribbon Flex for Samsung Galaxy S2 i9100",
    "12999351": "Rear Camera for Samsung Galaxy S20 FE 4G",
    "12999352": "Rear Camera for Samsung Galaxy S20 FE 5G",
    "12999708": "Rear Camera for Samsung Galaxy S20 Ultra",
    "12999693": "Main Rear Camera for Samsung Galaxy S20 Ultra",
    "12828359": "Rear Camera for Samsung Galaxy S3 i9300",
    "12827616": "Front Camera for Samsung Galaxy S3 i9300",
    "12827890": "Front Housing Frame for Samsung Galaxy S3 i9300 Blue",
    "12828358": "Front Housing Frame for Samsung Galaxy S3 i9300 White",
    "12828338": "Loud Speaker & Headphone Jack for Samsung Galaxy S3 i9300 Black",
    "12828335": "Loud Speaker & Headphone Jack for Samsung Galaxy S3 i9300 White",
    "12828368": "Sensor Ribbon Flex for Samsung Galaxy S3 i9300",
    "12828267": "Front Housing Frame for Samsung Galaxy S3 i9305 Blue",
    "12828318": "Front Housing Frame for Samsung Galaxy S3 i9305 Blue",
    "12828317": "Front Housing Frame for Samsung Galaxy S3 i9305 White",
    "12828333": "Front Housing Frame for Samsung Galaxy S3 i9305 White",
    "12828271": "Rear Camera for Samsung Galaxy S4",
    "12827640": "Front Camera for Samsung Galaxy S4",
    "12828367": "Home Button & Sensor Ribbon Flex for Samsung Galaxy S4",
    "12828324": "Front Housing Frame for Samsung Galaxy S4 i9500 Blue",
    "12827584": "Loud Speaker for Samsung Galaxy S4 i9500 White",
    "12828316": "Loud Speaker for Samsung Galaxy S4 i9505 White",
    "12828391": "Charging Port & Sensor Ribbon Flex for Samsung Galaxy S5 G900F",
    "12828284": "Rear Camera for Samsung Galaxy S6",
    "12828343": "Back Housing for Samsung Galaxy S6",
    "12828345": "Back Housing for Samsung Galaxy S6 Edge",
    "12828253": "Rear Camera for Samsung Galaxy S7",
    "12828328": "Back Housing for Samsung Galaxy S7",
    "12828244": "Rear Camera for Samsung Galaxy S7 Edge",
    "12998140": "Back Housing for Samsung Galaxy S9",
    "12998111": "Back Housing for Samsung Galaxy S9 Plus",
    "12998883": "Volume & Power Button Flex for Samsung Galaxy S9 Plus",
    "13000221": "Main Flex for Samsung Galaxy S20 FE",
    "13000273": "Charging Port Board for Samsung Galaxy S21 Ultra",
    "13000257": "Rear Camera for Samsung Galaxy S21 Ultra",
    "13000274": "Charging Port Board for Samsung Galaxy S22",
    "13000272": "Ear Speaker for Samsung Galaxy S22",
    "13000275": "Charging Port Board for Samsung Galaxy S22 Plus",
    "13000266": "Charging Port Board for Samsung Galaxy S22 Ultra",
    "13000267": "Charging Port Board for Samsung Galaxy S22 Ultra",
    "13000386": "Front Camera for Samsung Galaxy S22 Ultra",
    "13000276": "Charging Port Board for Samsung Galaxy S23",
    "13000277": "Charging Port Board for Samsung Galaxy S23 Plus",
    "13000278": "Charging Port Board for Samsung Galaxy S23 Ultra",
    # Second pass: buttons / sensors / OnePlus
    "12999806": 'Home Button for iPad 10.5"',
    "12997950": "Power Button for Huawei Nova 2i",
    "13000905": "OLED Screen for OnePlus 6T (Fingerprint Sensor OK)",
    "12828389": "Home Button with Fingerprint Sensor for Samsung Galaxy S5 G900F Black",
    "12828388": "Home Button with Fingerprint Sensor for Samsung Galaxy S5 G900F White",
    "12827968": "Home Button with Fingerprint Sensor for Samsung Galaxy S5 G900H Black",
    "12828326": "Home Button with Fingerprint Sensor for Samsung Galaxy S5 G900H White",
    # Third pass: jacks / tablet glass
    "12827673": "Headphone Jack for Samsung Galaxy S5 G900F",
    "12999463": "Headphone Jack for Samsung Galaxy S9",
    "12999651": "DC Power Jack for Samsung NP-RF511 5.5 x 3.0mm",
    "12998866": "Glass for Samsung Galaxy Tab E SM-T560",
}


def load_results() -> dict:
    if os.path.exists(RESULTS_JSON):
        with open(RESULTS_JSON, encoding="utf-8") as fh:
            return {r["id"]: r for r in json.load(fh)}
    return {}


def save_results(results: dict) -> None:
    rows = sorted(results.values(), key=lambda r: r["new_name"].lower())
    with open(RESULTS_JSON, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
    with open(RESULTS_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["id", "sku", "old_name", "new_name", "status", "detail"]
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    dry_run = "--apply" not in sys.argv
    client = RepairDeskClient()

    current = {}
    for item in client.iter_inventory():
        current[str(item.get("id"))] = item

    plan = []
    for item_id, new_name in RENAMES.items():
        item = current.get(item_id)
        if item is None:
            plan.append((item_id, "-", "<missing>", new_name))
            continue
        plan.append((item_id, item.get("sku") or "-", item.get("name") or "", new_name))
    plan.sort(key=lambda r: r[3].lower())

    with open(PLAN_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "sku", "old_name", "new_name"])
        writer.writerows(plan)
    print(f"plan -> {PLAN_CSV} ({len(plan)} renames, {len(SKIP)} kept brand-leading)")

    if dry_run:
        for item_id, sku, old, new in plan:
            print(f"  {item_id} | {sku:12} | {old!r}\n       -> {new!r}")
        print("\ndry run; pass --apply to write")
        return 0

    results = load_results()
    ok = fail = 0
    for index, (item_id, sku, old, new) in enumerate(plan, 1):
        if results.get(item_id, {}).get("status") == "ok":
            ok += 1
            continue
        if old == "<missing>":
            results[item_id] = dict(
                id=item_id, sku=sku, old_name=old, new_name=new,
                status="skipped", detail="item not found in inventory",
            )
            continue

        detail = ""
        status = "fail"
        for attempt in range(5):
            try:
                client.update_inventory_content(item_id, name=new, preserve_pricing=True)
                status, detail = "ok", ""
                break
            except RepairDeskError as exc:
                detail = str(exc)
                if "Too Many Requests" not in detail and "429" not in detail:
                    break
                time.sleep(min(5 * 2 ** attempt, 90))

        results[item_id] = dict(
            id=item_id, sku=sku, old_name=old, new_name=new,
            status=status, detail=detail,
        )
        if status == "ok":
            ok += 1
        else:
            fail += 1
        print(f"[{index}/{len(plan)}] {status:4} {item_id} {new}"
              + (f"  ({detail[:70]})" if detail else ""))
        if index % 10 == 0:
            save_results(results)
        time.sleep(1.1)

    save_results(results)
    print(f"\ndone: {ok} ok, {fail} failed -> {RESULTS_CSV}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
