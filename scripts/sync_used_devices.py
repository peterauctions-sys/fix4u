#!/usr/bin/env python3
"""Sync in-stock used devices from RepairDesk into data/used-devices.json."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from repairdesk.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["sync-used", "--out", str(ROOT / "data" / "used-devices.json")]))
