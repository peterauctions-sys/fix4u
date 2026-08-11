# Repair | Shop site switcher

Shared top switcher so `fix4u.co.nz` and `shop.fix4u.co.nz` feel like one brand.

## Files

- `site-switcher.css` — shared styles (uses `.bt-a` tokens on main site)
- `site-switcher.repair.html` — main site markup (`Repair` active)
- `site-switcher.shop.html` — shop markup (`Shop` active; for later)

## Main-site behaviour

On BeTheme blank pages that use the `.bt-a` shell:

1. Sticky chrome wraps switcher + floating header.
2. Segmented control: **Repair** | **Shop**.
3. Main site marks Repair as `is-active`; Shop links to `https://shop.fix4u.co.nz/`.
4. Nav “Shop” text link can be removed once the switcher is live (avoids duplicate).

Shop implementation is deferred until shop admin access is available.
