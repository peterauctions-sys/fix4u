# FIX4U WordPress Theme

Install and manage this theme from **https://fix4u.co.nz/admin** (WordPress admin).

## Install via wp-admin (recommended)

1. Download `dist/fix4u.zip` from this repository.
2. Open [https://fix4u.co.nz/admin](https://fix4u.co.nz/admin) and log in.
3. Go to **Appearance → Themes → Add New → Upload Theme**.
4. Upload `fix4u.zip` and click **Install Now**, then **Activate**.
5. Go to **Settings → Reading** and set **Your homepage displays** to **A static page** (create/select a Home page if needed). The theme’s `front-page.php` renders the English home layout.
6. Optional Chinese home:
   - Create a Page with slug `zh`.
   - Assign template **FIX4U Chinese Home**.
   - Publish. It will be available at `/zh/`.

## Manage theme content

After activation, use:

| Task | Where in /admin |
|------|-----------------|
| Colors, hero text, phone, email, address, hours, prices | **Appearance → Customize → FIX4U Site Settings** |
| Menus | **Appearance → Menus** (Primary / Chinese / Footer) |
| Theme guide shortcuts | **Appearance → FIX4U Theme** |
| Logged-in footer links | Site footer shows **Admin** + **Customize theme** for editors |

Current live site uses BeTheme. Keep it installed as a fallback until you confirm the new home page.

## Files

- `fix4u/` — theme source (upload as zip root folder name `fix4u`)
- `dist/fix4u.zip` — ready-to-upload package
- `snippets/` — shared HTML/CSS snippets for the live BeTheme shell (e.g. Repair | Shop switcher)
- `snippets/HANDOFF-shop-match-main-site.md` — **give this to the shop agent** to match shop chrome (switcher / header / footer styles + identical company strip) to the main site without changing shop homepage content
