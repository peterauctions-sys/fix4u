# Screen inventory rename (third-party safe naming)

## What changed in RepairDesk

### Pass 1 — TFT → RHD + Screen naming
- **292** inventory items updated successfully
- **6** skipped (tools / cracked-for-sell / whole refurbished device — not screen parts)

| Pattern | Example |
|---|---|
| TFT screens | `Apple iPhone 15 TFT Screen` → `RHD Screen for iPhone 15` |
| Generic screens | `Apple iPhone 16 Screen` → `Screen for iPhone 16` |
| OLED / LCD grade kept | `OLED Screen for iPhone 16 Pro` |
| Brand prefix removed from front | No more leading `Apple … Screen` / `Samsung … Screen` |

Results: `screen-rename-results.csv` / `.json`

### Pass 2 — Remaining glass / brand-leading titles
- **83 / 83** updated

| Issue | Example fix |
|---|---|
| Brand-leading back glass | `Apple iPhone 12 Back Glass` → `Back Glass for iPhone 12` |
| Touch / camera glass | `Touch Glass for iPad …`, `Camera Glass Lens for Samsung Galaxy …` |
| Screen protectors | `Screen Protector for Samsung Galaxy A13` |
| Cracked-for-parts wording | `… Org. Cracked Screen for Sell` → `Cracked Screen for Parts — …` |

Results: `screen-ip-fix-results.csv` / `.json`

### Pass 3 — Restore OEM grade marker
OEM / Original / Org. / Orginal are **product grade labels** in this shop. For every screen/glass item that previously had those markers, **OEM was put back** (Original/Org → OEM).

- **39 / 39** updated
- Examples: `OEM Screen for iPhone 12 Pro`, `OEM LCD Screen for iPhone 11`, `OEM Screen Assembly for MacBook Air …`

Results: `screen-oem-restore-results.csv` / `.json`

## Naming rules used (for third-party repair)

1. Prefer **`{Grade} Screen for {device}`** (or Back Glass / Touch Glass / Camera Glass Lens).
2. **TFT → RHD** (aftermarket grade).
3. **OEM** kept when the item was OEM / Original / Org grade (product differentiation).
4. Do **not** lead with Apple / Samsung as if the brand sells the part.
5. Empty descriptions were filled with a short compatible-repair note where applied.

## Remaining infringement / wording risks (not all auto-fixed)

These still appear in inventory and are worth a manual review. Device model names (iPhone, Galaxy) are normally fine for compatibility (“for iPhone 16”); the risk is implying **official / original** supply.

| Risk type | Examples still in stock | Suggested action |
|---|---|---|
| **Genuine Apple** accessories | MagSafe adapter, MacBook battery titled “Genuine Apple …” | Rename to `Compatible … for MacBook` unless truly Apple OEM stock |
| **OEM** chargers / earphones / batteries | `OEM Power Adapter for Apple MacBook…`, `OEM Earpod…` | Drop “OEM” or mark only if verified OEM |
| **Original** laptop parts / brand “Original Series” | HP/Dell/Asus “Original …” batteries; hoco “Original Series” | Keep brand product line names; drop “Original” on non-OEM laptop parts |
| **Whole refurbished device** | `Apple iPad 5 Retina Display 32GB … Refurb` | OK as device listing; do not treat as a screen part |
| Website / invoices / quotes | Customer-facing text may still say TFT / OEM | Align website and RepairDesk ticket templates with the same wording |

## Manual RepairDesk UI still needed (devices, not inventory)

API cannot rename/delete **device models**. See:

- `devices-to-delete.md` — duplicate / junk models
- `apple-ipad-mac-replace.csv` — iPad / MacBook model rename map
