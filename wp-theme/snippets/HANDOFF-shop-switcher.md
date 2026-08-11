# Handoff: Repair | Shop switcher for shop.fix4u.co.nz

> **Superseded for full chrome match.**  
> Use **`HANDOFF-shop-match-main-site.md`** for switcher + header + footer company strip.  
> This file remains as a shorter switcher-only note (some colors below are outdated vs live `#E3EAF2` strip).

Main site (`fix4u.co.nz`) already has this switcher live. Mirror it on the shop (Woodmart) with **Shop** active.

Source agent: https://cursor.com/agents/bc-968985d2-dd55-44ae-9f65-7de3608192aa  
Shop agent (has shop wp-admin as `ai-shop`): https://cursor.com/agents/bc-1e9755b5-6f7f-48f9-882f-eefbe851197c

## Goal

Replace / sit above the current shop dark top bar with the **same** Repair | Shop segmented control as the main site, so both feel like one brand.

- Shop site: **Shop** = active (blue)
- Repair links to `https://fix4u.co.nz/`
- Do not break existing Contact Us / Track Order / category nav work already done on shop

## Live reference

https://fix4u.co.nz/ — look at the very top bar

Repo snippets (canonical):

- `wp-theme/snippets/site-switcher.css`
- `wp-theme/snippets/site-switcher.shop.html`
- `wp-theme/snippets/README-site-switcher.md`

## Colors (hex — do not rely on main-site CSS vars)

| Role | Value |
|------|--------|
| Top bar background | `rgba(245,247,250,0.94)` |
| Top bar border bottom | `#E3E8EE` |
| Segment shell bg | `#FFFFFF` |
| Segment shell border | `#E3E8EE` |
| Segment shell shadow | `0 1px 2px rgba(38,50,56,0.04)` |
| Inactive text | `#546E7A` |
| Inactive hover text | `#1565C0` |
| Inactive hover bg | `#F5F9FC` |
| **Active bg** | `#1E88E5` |
| **Active text** | `#FFFFFF` |
| Active hover bg | `#1565C0` |
| Left label | `#90A4AE` |
| Contact text | `#546E7A` |
| Contact hover | `#1E88E5` |

Fonts: Manrope (already on shop). Content width: `min(1400px, calc(100% - 40px))` (shop already 1400).

Sizes: bar min-height 38px; segment radius **10px** (not pill); button radius **8px**; button min-width 78px; padding 6px 14px.

## Shop HTML

```html
<div class="f4u-site-switcher" data-site="shop">
  <div class="f4u-switcher-wrap">
    <span class="f4u-switcher-label">Parts &amp; accessories</span>
    <nav class="f4u-switcher-seg" aria-label="FIX4U site">
      <a href="https://fix4u.co.nz/">Repair</a>
      <a class="is-active" href="https://shop.fix4u.co.nz/" aria-current="page">Shop</a>
    </nav>
    <a class="f4u-switcher-contact" href="https://fix4u.co.nz/contact-page/">Contact</a>
  </div>
</div>
```

## Shop CSS (paste into Additional CSS or header custom HTML)

```css
.f4u-site-switcher {
  background: rgba(245, 247, 250, 0.94);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid #E3E8EE;
  font-family: "Manrope", "Segoe UI", sans-serif;
  position: relative;
  z-index: 100;
}
.f4u-switcher-wrap {
  width: min(1400px, calc(100% - 40px));
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-height: 38px;
  padding: 4px 0;
}
.f4u-switcher-label {
  font-size: 0.72rem;
  font-weight: 600;
  color: #90A4AE;
  letter-spacing: 0.02em;
  min-width: 9em;
}
.f4u-switcher-seg {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 3px;
  border-radius: 10px;
  background: #fff;
  border: 1px solid #E3E8EE;
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
.f4u-switcher-contact {
  font-size: 0.78rem;
  font-weight: 600;
  color: #546E7A;
  min-width: 9em;
  text-align: right;
  text-decoration: none;
}
.f4u-switcher-contact:hover { color: #1E88E5; }
@media (max-width: 720px) {
  .f4u-switcher-label,
  .f4u-switcher-contact { display: none; }
  .f4u-switcher-wrap { justify-content: center; }
}
```

## Implementation notes for Woodmart

1. Prefer Header Builder top row / custom HTML block, or Additional CSS + HTML injection.
2. Prefer **replacing** the old dark top-bar strip rather than stacking two bars.
3. Keep Contact reachable (switcher already has Contact; shop top-bar Contact can stay or be deduped — your call, don’t delete without checking).
4. Proven path on shop: Customizer Additional CSS + cookie login / Application Password REST (theme option sliders alone were unreliable).
5. After deploy: hard refresh shop homepage; compare side-by-side with https://fix4u.co.nz/

## Acceptance

- [ ] Top of shop shows Repair | Shop with Shop blue-active
- [ ] Repair opens fix4u.co.nz
- [ ] Colors/fonts/radius match main site switcher
- [ ] Width aligns to 1400 content column
- [ ] Mobile hides label + Contact, centers segment
