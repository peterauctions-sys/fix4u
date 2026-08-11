# Shop chrome matched to main site — deployed

Live shop: https://shop.fix4u.co.nz/  
Live main: https://fix4u.co.nz/  
Handoff: `wp-theme/snippets/HANDOFF-shop-match-main-site.md`  
Deployed: 2026-08-11 via Woodmart Header Builder + Theme Settings + Customizer Additional CSS

## Scope completed

| Zone | Result |
|------|--------|
| Site switcher | Centered Repair \| Shop only; strip `#E3EAF2`; Shop active; no Parts/Contact |
| Header | Transparent/flat rows; logo `fix4u-logo-header-transparent-v2.png` @ ~56px; shop menus/cart kept |
| Homepage content | Unchanged (product grids / Holiday Deals still hidden) |
| Footer columns | Shop widgets kept; shell restyled `#1B2832` |
| Bottom company strip | Identical to main (Cebel address, 0800, support@, WeChat, WhatsApp, hours, ©) |

## Where it lives on shop

1. **Header Builder** `header_695440` (Header Marketplace 2)
   - Top-bar text elements → centered switcher HTML (`f4u-site-switcher`)
   - Desktop/mobile logos → media `28643` transparent header v2
   - Top-bar bg `#E3EAF2`; general/header-bottom transparent
2. **Customizer Additional CSS** — `/* FIX4U_CHROME_MATCH */ … /* /FIX4U_CHROME_MATCH */`
3. **Theme Settings → Footer → Copyrights** — `.f4u-foot-bar` HTML (byte-match main)
4. **Theme Settings → Custom CSS** — `/* FIX4U_FOOTBAR_VISIBLE */` so copyrights column shows the strip

## Canonical assets

- Header logo: `https://shop.fix4u.co.nz/wp-content/uploads/2026/08/fix4u-logo-header-transparent-v2.png`
- Footer on-dark (main): `https://fix4u.co.nz/wp-content/uploads/2026/08/fix4u-logo-20260811-real-on-dark.png`

## Edit later

- Switcher/logo: WoodMart → Header builder → Header Marketplace 2
- Foot strip text: Theme settings → Footer → Copyrights text
- Chrome CSS: Appearance → Customize → Additional CSS (`FIX4U_CHROME_MATCH` block)
