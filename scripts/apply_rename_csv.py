#!/usr/bin/env python3
"""Apply a rename CSV (id, sku, old_name, proposed_name) to RepairDesk inventory.

Rows whose proposed name is `<NO MATCH>` or equal to the current name are
skipped. Results are saved incrementally so an interrupted run can resume.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repairdesk.client import RepairDeskClient, RepairDeskError


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: apply_rename_csv.py <plan.csv> [--apply]")
        return 2
    plan_path = sys.argv[1]
    dry_run = "--apply" not in sys.argv
    stem = os.path.splitext(plan_path)[0].replace("-proposal", "")
    results_json = f"{stem}-results.json"
    results_csv = f"{stem}-results.csv"

    with open(plan_path, encoding="utf-8-sig") as fh:
        plan = [r for r in csv.DictReader(fh) if r["proposed_name"] != "<NO MATCH>"]
    plan = [r for r in plan if r["proposed_name"].strip() != r["old_name"].strip()]
    print(f"{len(plan)} renames to apply from {plan_path}")

    if dry_run:
        print("dry run; pass --apply to write")
        return 0

    results = {}
    if os.path.exists(results_json):
        with open(results_json, encoding="utf-8") as fh:
            results = {r["id"]: r for r in json.load(fh)}

    client = RepairDeskClient()
    ok = fail = 0

    def save() -> None:
        rows = sorted(results.values(), key=lambda r: r["new_name"].lower())
        with open(results_json, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
        with open(results_csv, "w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=["id", "sku", "old_name", "new_name", "status", "detail"]
            )
            writer.writeheader()
            writer.writerows(rows)

    for index, row in enumerate(plan, 1):
        item_id, new = row["id"], row["proposed_name"].strip()
        if results.get(item_id, {}).get("status") == "ok":
            ok += 1
            continue
        detail, status = "", "fail"
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
            id=item_id, sku=row["sku"], old_name=row["old_name"],
            new_name=new, status=status, detail=detail,
        )
        if status == "ok":
            ok += 1
            if index % 25 == 0:
                print(f"[{index}/{len(plan)}] ok   {new}")
        else:
            fail += 1
            print(f"[{index}/{len(plan)}] FAIL {item_id} {new}  ({detail[:80]})")
        if index % 25 == 0:
            save()
        time.sleep(1.1)

    save()
    print(f"\ndone: {ok} ok, {fail} failed -> {results_csv}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
