# Handoff: Match shop.fix4u.co.nz chrome to main site (fix4u.co.nz)

**Audience:** Shop admin agent (Woodmart / `ai-shop`)  
**Source / main-site agent:** https://cursor.com/agents/bc-968985d2-dd55-44ae-9f65-7de3608192aa  
**Shop agent:** https://cursor.com/agents/bc-1e9755b5-6f7f-48f9-882f-eefbe851197c  
**Live design reference:** https://fix4u.co.nz/  
**Shop target:** https://shop.fix4u.co.nz/

Main site design is **done**. Your job is to make the shop’s **chrome** match the main site. Do **not** rewrite shop homepage product content or shop footer link lists — only align look & shared company strip.

---

## Scope (read carefully)

| Zone | Change? | Rule |
|------|---------|------|
| **Site switcher** (very top) | **Yes — match exactly** | Same height, colors, segment control, centering. Shop = active. |
| **Header** | **Yes — style match** | Same colors, fonts, logo size, spacing, flat header (no white floating card). **Keep shop’s own menus / Woo actions.** |
| **Homepage main content** | **No** | Do not replace Woodmart/home product sections with main-site hero/services. |
| **Footer link columns / newsletter content** | **No content rewrite** | Keep shop’s own links/widgets. Restyle colors, fonts, spacing, grid rhythm to match main footer. |
| **Footer bottom company strip** (`.foot-bar` / company info) | **Yes — identical** | Same text, same order, same links, same hours, same styling. Pixel-level match to main. |

---

## Design tokens (Scheme A — use hex, not CSS vars from main)

| Token | Value | Use |
|-------|--------|-----|
| Primary | `#1E88E5` | Active switcher, CTA, links hover |
| Primary deep | `#1565C0` | Active hover / emphasis |
| Teal | `#26A69A` | Accent (optional) |
| Page / soft bg | `#F5F7FA` | Page canvas behind header |
| Switcher strip bg | `#E3EAF2` | Full-width top bar |
| Switcher border | `#D5DEE8` | Switcher bottom border |
| Ink | `#263238` | Headings / strong text |
| Text | `#546E7A` | Body / inactive nav |
| Muted | `#90A4AE` | Meta / foot-bar text |
| Border | `#E3E8EE` | Dividers / segment border |
| White | `#FFFFFF` | Segment shell, header text on dark |
| Footer bg | `#1B2832` | Full-bleed footer |
| Footer link | `#CFD8DC` | Footer anchors |
| Footer body | `#B0BEC5` | Footer paragraph tone |

**Fonts (load both):**

- Body / UI: `"Manrope", "Segoe UI", sans-serif`
- Headings: `"Outfit", sans-serif`

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
```

**Content width:** `min(1400px, calc(100% - 40px))` centered (`margin-left/right: auto`).

**Logos (canonical — use these URLs):**

| Placement | URL |
|-----------|-----|
| Header (light / transparent) | `https://fix4u.co.nz/wp-content/uploads/2026/08/fix4u-logo-header-transparent-v2.png` |
| Footer (on dark) | `https://fix4u.co.nz/wp-content/uploads/2026/08/fix4u-logo-20260811-real-on-dark.png` |

Header logo height: **56px**. Footer logo height: **56px**.

---

## 1) Site switcher — must match main site

### Live look (main)

- Full-bleed cool strip `#E3EAF2`, border-bottom `#D5DEE8`
- Row height ~**52px** (min-height **40px**, padding **6px 0**)
- Repair | Shop segment **centered** in the strip (no left label, no Contact link)
- Segment: white shell, radius **10px**, border `#C9D6E3` / `#E3E8EE`, shadow `0 1px 2px rgba(38,50,56,.04)`
- Buttons: min-width **78px**, padding **6px 14px**, radius **8px**, font **0.78rem / 700**
- On shop: **Shop** = `.is-active` (bg `#1E88E5`, text `#fff`)
- Repair → `https://fix4u.co.nz/`
- Shop → `https://shop.fix4u.co.nz/`

### HTML (shop)

```html
<div class="f4u-site-switcher" data-site="shop">
  <div class="f4u-switcher-wrap">
    <nav class="f4u-switcher-seg" aria-label="FIX4U site">
      <a href="https://fix4u.co.nz/">Repair</a>
      <a class="is-active" href="https://shop.fix4u.co.nz/" aria-current="page">Shop</a>
    </nav>
  </div>
</div>
```

### CSS (shop — paste Additional CSS / custom HTML)

```css
.f4u-site-switcher {
  width: 100%;
  background: #E3EAF2;
  border-bottom: 1px solid #D5DEE8;
  font-family: "Manrope", "Segoe UI", sans-serif;
  position: relative;
  z-index: 1000;
}
.f4u-switcher-wrap {
  width: min(1400px, calc(100% - 40px));
  max-width: min(1400px, calc(100% - 40px));
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 6px 0;
  box-sizing: border-box;
}
.f4u-switcher-seg {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 3px;
  border-radius: 10px;
  background: #FFFFFF;
  border: 1px solid #C9D6E3;
  box-shadow: 0 1px 2px rgba(38, 50, 56, 0.04);
}
.f4u-switcher-seg a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 78px;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 700;
  color: #546E7A;
  text-decoration: none;
  transition: background 0.18s ease, color 0.18s ease;
}
.f4u-switcher-seg a:hover {
  color: #1565C0;
  background: #F5F9FC;
}
.f4u-switcher-seg a.is-active {
  background: #1E88E5;
  color: #fff;
}
.f4u-switcher-seg a.is-active:hover {
  background: #1565C0;
  color: #fff;
}
```

### Switcher acceptance

- [ ] Strip bg `#E3EAF2`, height ≈ main (~52px)
- [ ] Segment centered; Shop blue-active
- [ ] No second old dark top bar stacked above/below (replace or hide Woodmart top bar)
- [ ] Side-by-side with https://fix4u.co.nz/ looks the same

Repo mirrors: `site-switcher.shop.html`, `site-switcher.css` (keep in sync with this handoff).

---

## 2) Header — same look, shop keeps its own menu

### Match

- Transparent / flat header over soft page bg `#F5F7FA` (**no** floating white card, no heavy shadow card)
- Content row width `min(1400px, calc(100% - 40px))`, centered
- Logo: transparent header PNG, height **56px**
- Nav text: ink/primary system — inactive `#546E7A`, hover/active `#1E88E5` / `#1565C0`
- Primary CTA button (if present): bg `#1E88E5`, hover `#1565C0`, white text, font Manrope 700
- Row min-height ~**72px**, comfortable gap (~24px)
- Fonts: Manrope for nav; Outfit optional for any wordmark text

### Do not match / do not replace

- Main-site menu labels (HOME / OUR SERVICES / …)
- Keep shop categories, cart, account, search, Track Order, etc.

### Suggested shop header CSS direction

```css
/* Align Woodmart header chrome to main — adjust selectors to theme */
body {
  font-family: "Manrope", "Segoe UI", sans-serif;
  color: #546E7A;
  background: #F5F7FA;
}
.whb-header,
.whb-main-header,
.wd-header {
  background: transparent !important;
  box-shadow: none !important;
  border: 0 !important;
}
.whb-header .whb-row,
.wd-header .container {
  width: min(1400px, calc(100% - 40px)) !important;
  max-width: min(1400px, calc(100% - 40px)) !important;
  margin-left: auto !important;
  margin-right: auto !important;
}
.wd-nav > li > a,
.menu-item a {
  font-family: "Manrope", "Segoe UI", sans-serif;
  font-weight: 700;
  color: #546E7A !important;
}
.wd-nav > li > a:hover,
.wd-nav > li.current-menu-item > a {
  color: #1E88E5 !important;
}
/* Logo */
.site-logo img,
.wd-logo img {
  height: 56px !important;
  width: auto !important;
}
```

Tune selectors after inspecting shop DOM. Goal: visual parity with main header chrome, not cloning main HTML.

### Header acceptance

- [ ] Logo 56px transparent asset
- [ ] No white floating card around header
- [ ] Colors/fonts match tokens
- [ ] Shop menus/cart still work
- [ ] Width aligns to 1400 column

---

## 3) Homepage content — do not change

Leave Woodmart homepage builders / product grids / banners as they are.  
Only chrome above/below may change. Do **not** paste main-site `.hero` / services sections into shop home.

---

## 4) Footer — restyle shell; keep shop content; clone bottom company strip

### A) Footer shell (style match)

```css
/* Footer shell — match main site */
.f4u-sitefoot,
footer.footer-container,
.wd-footer {
  background: #1B2832 !important;
  color: #B0BEC5 !important;
  font-family: "Manrope", "Segoe UI", sans-serif;
  padding-top: 48px;
}
.f4u-sitefoot a,
.wd-footer a {
  color: #CFD8DC !important;
  text-decoration: none;
}
.f4u-sitefoot a:hover,
.wd-footer a:hover {
  color: #FFFFFF !important;
}
.f4u-sitefoot h4,
.wd-footer .widget-title {
  color: #FFFFFF !important;
  font-family: "Outfit", sans-serif;
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 700;
}
/* Inner columns width */
.f4u-foot-inner,
.wd-footer .container {
  width: min(1400px, calc(100% - 40px)) !important;
  max-width: min(1400px, calc(100% - 40px)) !important;
  margin-left: auto !important;
  margin-right: auto !important;
}
```

Keep shop’s own column links / widgets. Only make them **look** like main (type, colors, spacing).

Footer logo on dark:

`https://fix4u.co.nz/wp-content/uploads/2026/08/fix4u-logo-20260811-real-on-dark.png` (height 56px).

### B) Bottom company info — **must be identical** to main

Replace / inject this strip at the very bottom of the shop footer (below shop widgets). **Do not rewrite the wording.**

```html
<div class="f4u-foot-bar">
  <div class="f4u-foot-meta">
    <span><a href="https://www.google.com/maps/search/?api=1&query=Unit+D,+1+Cebel+Place,+Rosedale,+Auckland" target="_blank" rel="noopener">Unit D, 1 Cebel Place, Rosedale, Auckland</a></span>
    <span>Phone <a href="tel:0800800349">0800 800 349</a></span>
    <span>Email <a href="mailto:support@fix4u.co.nz">support@fix4u.co.nz</a></span>
    <span>WeChat: fix4urepair</span>
    <span><a href="https://wa.me/6421885501" target="_blank" rel="noopener">WhatsApp: +64 21 885 501</a></span>
    <span>Hours Mon–Fri 9:30am–5:30pm · Sat/Sun Closed</span>
  </div>
  <div>© FIX4U · All rights reserved</div>
</div>
```

```css
.f4u-foot-bar {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 10px;
  padding: 20px 0 24px;
  font-size: 0.82rem;
  color: #90A4AE;
  font-family: "Manrope", "Segoe UI", sans-serif;
  width: min(1400px, calc(100% - 40px));
  max-width: min(1400px, calc(100% - 40px));
  margin: 0 auto;
  box-sizing: border-box;
}
.f4u-foot-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 14px 18px;
  text-align: center;
}
.f4u-foot-bar a {
  color: #CFD8DC;
  text-decoration: none;
}
.f4u-foot-bar a:hover {
  color: #FFFFFF;
}
```

**Hard rules for this strip**

- Hours: **Mon–Fri 9:30am–5:30pm · Sat/Sun Closed** (not 8:30 / not open Sat)
- Email shown: `support@fix4u.co.nz`
- WeChat: `fix4urepair`
- WhatsApp: `+64 21 885 501` → `https://wa.me/6421885501`
- Centered column layout (not space-between)

### Footer acceptance

- [ ] Footer bg `#1B2832`, fonts/colors match
- [ ] Shop column content unchanged (only styled)
- [ ] Bottom company strip text **byte-for-byte** matches main
- [ ] Full-bleed dark footer (edge to edge), inner content 1400

---

## 5) Implementation tips (Woodmart)

1. Prefer **Customizer → Additional CSS** + Header Builder / custom HTML block for switcher + foot-bar.
2. Prefer **replacing** the old dark shop top bar rather than stacking two bars.
3. Theme option “sliders” alone are unreliable; cookie/REST Application Password path used before on shop.
4. After deploy: hard refresh shop; compare side-by-side with https://fix4u.co.nz/ at 1440px width.
5. Do not switch themes without approval. Do not delete shop content without asking.

---

## 6) Final acceptance checklist

- [ ] Site switcher: identical height/color/segment to main; Shop active
- [ ] Header: same colors/fonts/logo size/flat treatment; shop menus preserved
- [ ] Homepage content: unchanged
- [ ] Footer columns: shop content kept; colors/fonts/spacing match main
- [ ] Bottom company info: completely identical to main (address, phone, email, WeChat, WhatsApp, hours, ©)
- [ ] Fonts Manrope + Outfit loaded
- [ ] Content width 1400 rhythm consistent

---

## Related repo files

- `wp-theme/snippets/site-switcher.css`
- `wp-theme/snippets/site-switcher.shop.html`
- `wp-theme/snippets/site-switcher.repair.html`
- `wp-theme/snippets/header-flat.css`
- `wp-theme/snippets/HANDOFF-shop-switcher.md` (older switcher-only note — **this file supersedes it for full chrome match**)
