# Repair Manuals — per-model (One NZ aligned)

Updated live on https://fix4u.co.nz/repair-manual/

## What changed

Previously iPhone manuals were **series-combined** (e.g. iPhone 7 / 7 Plus). Those 10 series posts were moved to trash and replaced with **one SEO page per model**.

## Coverage (137 manuals)

Source of model list: [One NZ user guides — phones](https://userguide.one.nz/?type=phone) manufacturers:

| Brand | Count | Notes |
|-------|------:|-------|
| Apple iPhone | 39 | All One NZ iPhone guides + **iPhone 7 / 7 Plus** (still common in NZ, not on One NZ guide list) |
| Samsung | 69 | Full One NZ Samsung phone list (S / A / Z / Note / XCover, etc.) |
| OPPO | 15 | One NZ OPPO phones |
| Huawei | 7 | One NZ Huawei phones |
| Motorola | 3 | Edge / Moto G |
| Doro | 2 | |
| MobiWire | 1 | Dakota |
| One NZ | 1 | Smart P12 |

Google Pixel is **not** listed under One NZ phone manufacturers on the user-guide hub (brands present: Apple, Samsung, OPPO, Motorola, Huawei, Doro, MobiWire, One NZ).

## Page pattern (SEO)

Each post:

- Slug: `{model}-screen-repair-manual`
- Title / H1: `{Model} Screen Repair Manual`
- Category: Repair Manual
- Unique excerpt mentioning model + FIX4U Auckland / North Shore
- Unique cover image (branded 1200×630 JPEG in Media Library)
- In-article images with model-specific `alt` text
- H2 structure: Model covered → When you need repair → What we check → Process → Parts & warranty → DIY warning
- CTA to book repair / WhatsApp

Generator (idempotent state in `/tmp/rm_generate_state.json`):

`scripts/generate_repair_manuals.py`

## Examples

- https://fix4u.co.nz/iphone-7-screen-repair-manual/
- https://fix4u.co.nz/iphone-7-plus-screen-repair-manual/
- https://fix4u.co.nz/iphone-17-pro-max-screen-repair-manual/
- https://fix4u.co.nz/iphone-air-screen-repair-manual/
- https://fix4u.co.nz/samsung-galaxy-s26-ultra-screen-repair-manual/
- https://fix4u.co.nz/samsung-galaxy-z-fold7-screen-repair-manual/
- https://fix4u.co.nz/oppo-find-x9-pro-5g-screen-repair-manual/

## Listing

https://fix4u.co.nz/repair-manual/ — brand folders (4 per row); see `REPAIR-MANUAL-BRAND-FOLDERS.md`.
