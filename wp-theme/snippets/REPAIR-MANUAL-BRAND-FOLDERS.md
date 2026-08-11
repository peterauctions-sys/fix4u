# Repair Manual — brand folders + 4-column grids

## Structure

**Repair Manual home** → brand folders (4 per row) → model manuals (4 per row)

| Brand folder | URL |
|--------------|-----|
| Apple | https://fix4u.co.nz/repair-manual/apple/ |
| Samsung | https://fix4u.co.nz/repair-manual/samsung/ |
| OPPO | https://fix4u.co.nz/repair-manual/oppo/ |
| Motorola | https://fix4u.co.nz/repair-manual/motorola/ |
| Huawei | https://fix4u.co.nz/repair-manual/huawei/ |
| Doro | https://fix4u.co.nz/repair-manual/doro/ |
| MobiWire | https://fix4u.co.nz/repair-manual/mobiwire/ |
| One NZ | https://fix4u.co.nz/repair-manual/one-nz/ |

Home: https://fix4u.co.nz/repair-manual/

CSS marker: `FIX4U_RM_FOUR_COL` (`repeat(4, …)` desktop → 2 → 1 responsive).

WordPress: brand pages are **child pages** of Repair Manual (`parent=2782`, blank template). Brand **categories** also exist under Repair Manual (Apple, Samsung, …).

## iPhone 16 family — iFixit-based screen replacement

Rebuilt with disassembly → transfer → **Install** → calibrate:

| Model | URL | iFixit guide |
|-------|-----|--------------|
| iPhone 16 | /iphone-16-screen-repair-manual/ | 177288 |
| iPhone 16 Plus | /iphone-16-plus-screen-repair-manual/ | 177847 |
| iPhone 16 Pro | /iphone-16-pro-screen-repair-manual/ | 180298 |
| iPhone 16 Pro Max | /iphone-16-pro-max-screen-repair-manual/ | 178634 |
| iPhone 16e | /iphone-16e-screen-repair-manual/ | 186614 |

- Step photos downloaded from iFixit CDN, **logo/watermark strip scrubbed**, re-uploaded to FIX4U media.
- Explicit **Install** section includes adhesive, reconnect, **Place / Install the screen**, heat/press, pentalobe screws.
- Credit link to the public iFixit guide retained on each page.

Script: `scripts/repair_manual_brand_folders_iphone16.py`
