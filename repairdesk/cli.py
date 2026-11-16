#!/usr/bin/env python3
"""CLI for RepairDesk inventory content updates.

Examples:
  python -m repairdesk.cli list-used
  python -m repairdesk.cli get 12997939
  python -m repairdesk.cli update 12997939 --name "..." --description "..."
  python -m repairdesk.cli sync-used --out data/used-devices.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .client import RepairDeskClient, RepairDeskError


def _print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_list_used(args: argparse.Namespace) -> int:
    client = RepairDeskClient()
    items = client.list_used_devices(in_stock_only=not args.all)
    rows = [
        {
            "id": i.get("id"),
            "name": i.get("name"),
            "stock": i.get("in_stock"),
            "price": i.get("original_price"),
            "sku": i.get("sku"),
            "description": i.get("description") or "",
        }
        for i in items
    ]
    _print_json(rows)
    print(f"\n# {len(rows)} item(s)", file=sys.stderr)
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    client = RepairDeskClient()
    _print_json(client.get_inventory(args.id))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    client = RepairDeskClient()
    result = client.update_inventory_content(
        args.id,
        name=args.name,
        description=args.description,
        notes=args.notes,
        price=args.price,
        in_stock=args.stock,
        sku=args.sku,
    )
    _print_json(result)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    client = RepairDeskClient()
    payload = client.list_inventory(page=args.page, pagesize=args.pagesize, keyword=args.keyword)
    data = payload.get("data") or {}
    items = data.get("inventoryListData") or []
    rows = [
        {
            "id": i.get("id"),
            "name": i.get("name"),
            "stock": i.get("in_stock"),
            "price": i.get("original_price"),
            "sku": i.get("sku"),
        }
        for i in items
    ]
    _print_json({"pagination": data.get("pagination"), "items": rows})
    return 0


def _website_item(item: dict) -> dict:
    prices = item.get("prices") or {}
    retail = item.get("original_price") or prices.get("retail_price") or "0"
    online = prices.get("online_price") or "0"
    try:
        display = float(online) if float(online or 0) > 0 else float(retail or 0)
    except (TypeError, ValueError):
        display = 0.0
    return {
        "id": str(item.get("id")),
        "name": (item.get("name") or "").strip(),
        "sku": item.get("sku") or "",
        "stock": int(float(item.get("in_stock") or 0)),
        "price": display,
        "price_label": f"${display:,.2f}" if display > 0 else "Contact us",
        "description": (item.get("description") or "").strip(),
        "image": item.get("image") or item.get("originalimage") or "",
    }


def cmd_sync_used(args: argparse.Namespace) -> int:
    client = RepairDeskClient()
    items = client.list_used_devices(in_stock_only=True)
    # Skip $0 / contact-only unless --include-unpriced
    website_items = []
    for item in items:
        row = _website_item(item)
        if row["price"] <= 0 and not args.include_unpriced:
            continue
        website_items.append(row)

    out = {
        "source": "repairdesk",
        "store": "FIX4U Auckland",
        "count": len(website_items),
        "items": website_items,
    }
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(website_items)} used devices to {path}", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RepairDesk API tools for FIX4U")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list-used", help="List used / refurbished devices")
    p.add_argument("--all", action="store_true", help="Include out-of-stock items")
    p.set_defaults(func=cmd_list_used)

    p = sub.add_parser("get", help="Get one inventory item by ID")
    p.add_argument("id")
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("update", help="Update inventory content fields")
    p.add_argument("id")
    p.add_argument("--name")
    p.add_argument("--description")
    p.add_argument("--notes")
    p.add_argument("--price", type=float)
    p.add_argument("--stock", type=int)
    p.add_argument("--sku")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("search", help="Search inventory by keyword")
    p.add_argument("keyword")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--pagesize", type=int, default=50)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("sync-used", help="Export in-stock used devices for the website")
    p.add_argument("--out", default="data/used-devices.json")
    p.add_argument("--include-unpriced", action="store_true")
    p.set_defaults(func=cmd_sync_used)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except RepairDeskError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
