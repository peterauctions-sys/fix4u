# Shop Repair | Shop switcher — deployed

Live: https://shop.fix4u.co.nz/  
Deployed: 2026-08-11 via Woodmart Header Builder (`header_695440` / Header Marketplace 2)

## What changed

1. **Removed** dark top-bar menus (About / FIX4U Repair / Contact Us).
2. **Added** light **Repair | Shop** switcher with **Shop** active (`#1E88E5`), matching main site.
3. Top bar row restyled (light bg, dark text scheme, visible on mobile).
4. Switcher markup + CSS live in Header Builder **Text/HTML** elements (desktop left column + mobile column). CSS is embedded via `<style id="f4u-site-switcher-css">` because Woodmart Custom CSS save via `options.php` returned 403 in this environment.
5. Track Order / logo / search / cart in main + bottom header rows unchanged.

## Canonical snippets

- `wp-theme/snippets/HANDOFF-shop-switcher.md`
- `wp-theme/snippets/site-switcher.shop.html` (class names in handoff use `f4u-*`)
- `wp-theme/snippets/site-switcher.shop.woodmart.css` (CSS actually used on shop)

## Edit later

WoodMart → Header builder → Header Marketplace 2 → Top bar Text/HTML (`f4u-switcher-host`).
