# RepairDesk API integration (FIX4U)

Connects this site to [RepairDesk](https://www.repairdesk.co/) so inventory content can be read and updated via the Public API.

## Setup

1. In RepairDesk: **Store → General Settings → Other Information → API** — create an API key.
2. Export the key as an environment variable:

```bash
export REPAIRDESK_API_KEY='your-key'
```

## CLI

```bash
# List in-stock used / refurbished devices
python3 -m repairdesk.cli list-used

# Search inventory
python3 -m repairdesk.cli search "iPhone 11"

# Get one item
python3 -m repairdesk.cli get 12997939

# Update name / description / notes (keeps price & stock unless you pass flags)
python3 -m repairdesk.cli update 12997939 \
  --name "[Pre-owned] iPad Pro 9.7 32GB" \
  --description "Pre-owned Apple iPad Pro 9.7\" 32GB. Tested by FIX4U." \
  --notes "90-day warranty. Unlocked / Wi-Fi."

# Export used devices for the website
python3 -m repairdesk.cli sync-used --out data/used-devices.json
# or:
python3 scripts/sync_used_devices.py
```

## What can be changed

| Resource | Read | Update |
|----------|------|--------|
| Inventory (name, description, notes, price, stock) | yes | `PUT /inventory/{id}` |
| Customers | yes | `PUT /customers/{id}` |
| Tickets | yes | `PUT /ticket/updateticket` |
| Invoices | yes | create/payments |

Base URL: `https://api.repairdesk.co/api/web/v1`  
Docs: https://api-docs.repairdesk.co/

## Website sync

`data/used-devices.json` is loaded by the Used Devices section on `index.html` / `index-zh.html`. Re-run `sync-used` after you change stock or copy in RepairDesk.
