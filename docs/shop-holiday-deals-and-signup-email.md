# Shop: Holiday Deals hide + signup email

Live site: https://shop.fix4u.co.nz/ (WordPress + Woodmart + Elementor). Changes were applied in wp-admin / REST, not in this static repo.

## Holiday Deals — hidden (2026-08-11)

- Homepage Elementor page ID: `17`
- Section container: `d9c6010` (widget `3de30c1`, `wd_products_tabs`, title **Holiday Deals** / description Christmas Deals)
- Visibility: Elementor hide on desktop, tablet, and mobile (`elementor-hidden-*` classes)
- Elementor Files & Data cache cleared after update
- To restore later: edit Home in Elementor → select the Holiday Deals tabs widget/container → Advanced → Responsive → unhide

## Signup / subscription email routing

| Flow | Destination |
|------|-------------|
| WordPress **Administration Email Address** | `info@fix4u.co.nz` (was pending change to `websiteparking123@gmail.com`; pending change cancelled) |
| WooCommerce email **From** address | `info@fix4u.co.nz` |
| WooCommerce **New order** admin recipient | `info@fix4u.co.nz` |
| WooCommerce **New account** email | Sent to the customer; From uses `info@fix4u.co.nz` |
| Footer **Subscribe Newsletter** (MC4WP form “Newsletter form”, form ID `129`) | Intended for Mailchimp audience (double opt-in on). As of 2026-08-11 Mailchimp API reported **not connected** / no audiences — reconnect under **Mailchimp for WP → Mailchimp** if list signup should work |

Default / intended ops inbox for shop admin notifications: **info@fix4u.co.nz**.
