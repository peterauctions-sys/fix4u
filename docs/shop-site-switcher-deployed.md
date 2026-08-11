# Shop Repair | Shop switcher — deployed

> Superseded for full chrome match by `docs/shop-chrome-match-main-deployed.md` and `wp-theme/snippets/HANDOFF-shop-match-main-site.md` (centered switcher, `#E3EAF2`, transparent header logo, identical foot-bar).

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

## Main menu cleanup (2026-08-11)

Removed from **Main Product Categories** menu (`menus=114`, header bottom nav):

- Top Deals (`menu-item` 1779)
- Services (`menu-item` 1961)

Remaining top-level: Security, Accessories, Electronic, Parts, Pre-owned Device, Mobile Phones, Track Your Order.

## Logo update (2026-08-11)

- Main site (`fix4u.co.nz`) homepage header/footer already use `fix4u-logo-20260811-real.png` / `-real-on-dark.png`.
- Shop header logo updated to `fix4u-logo-20260811-real.png` (media 28637; on-dark 28636 also uploaded) via Header Builder. Header row is light grey, so the dark-text logo is required (on-dark looked like icon-only).
- Static `index.html` / `index-zh.html` now use `images/fix4u-logo-20260811-real.png`.

## Favicon (2026-08-11)

Shop Site Icon set to new FIX4U mark (stacked colorful X + 4U on black), media `fix4u-favicon-20260811.png`.
Static pages use `images/favicon-32.png` / `images/favicon-192.png` / `images/apple-touch-icon.png`.
