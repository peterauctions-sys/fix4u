#!/usr/bin/env python3
"""Generate per-model screen repair manuals on fix4u.co.nz from one.nz phone list."""
from __future__ import annotations

import base64
import io
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CTX = ssl.create_default_context()
BASE = "https://fix4u.co.nz"
CAT_REPAIR = 4
SHELL_PATH = Path("/tmp/rm_shell_3254.html")
STATE_PATH = Path("/tmp/rm_generate_state.json")
COVER_DIR = Path("/tmp/rm_covers")

IMG_BENCH = f"{BASE}/wp-content/uploads/2026/07/fix4u-home-v2-phone-repair.png"
IMG_CRACK = f"{BASE}/wp-content/uploads/2023/05/istockphoto-1409158612-612x612-1.jpg"
IMG_PRO = f"{BASE}/wp-content/uploads/2026/08/fix4u-hero-professional-repair.jpg"
IMG_PHONE = f"{BASE}/wp-content/uploads/2024/12/Phone-Repair.png"
IMG_SAM = f"{BASE}/wp-content/uploads/2015/02/phone_repair_samsung.jpg"

BRAND_COLORS = {
    "Apple": ("#1C1C1E", "#F5F5F7", "#0A84FF"),
    "Samsung": ("#1428A0", "#F7F9FC", "#00B3E3"),
    "OPPO": ("#1A1A1A", "#F4F7F5", "#00A862"),
    "Motorola": ("#0B1C2C", "#F3F6FA", "#EBB300"),
    "Huawei": ("#CF0A2C", "#FFF7F8", "#1A1A1A"),
    "Doro": ("#003366", "#F5F8FC", "#F36C00"),
    "MobiWire": ("#222222", "#F6F6F6", "#E53935"),
    "One NZ": ("#000000", "#F5F5F5", "#00E5A8"),
}


@dataclass
class Model:
    brand: str
    name: str  # full display e.g. iPhone 16 Pro
    title_name: str  # without brand prefix for Apple "iPhone 16 Pro"
    slug: str
    source: str


def auth_headers(content_type: str | None = None) -> dict:
    user = os.environ["WORDPRESS_ADMIN_USER"]
    app = os.environ["WORDPRESS_APPLICATION_PASSWORD"]
    token = base64.b64encode(f"{user}:{app}".encode()).decode()
    h = {
        "Authorization": f"Basic {token}",
        "User-Agent": "Mozilla/5.0 CursorAgent",
        "Accept": "*/*",
    }
    if content_type:
        h["Content-Type"] = content_type
    return h


def http_json(method: str, path: str, data: dict | None = None, timeout: int = 90):
    body = None
    headers = auth_headers("application/json" if data is not None else None)
    if data is not None:
        body = json.dumps(data).encode()
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace")
            return r.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"{method} {path} -> {e.code}: {err[:500]}") from e


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html",
        },
    )
    with urllib.request.urlopen(req, context=CTX, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def slugify(text: str) -> str:
    s = text.lower()
    s = s.replace("&", " and ")
    s = s.replace("+", " plus ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def load_one_nz_models() -> list[Model]:
    brand_map = [
        ("apple", "Apple", r'alt="(Apple iPhone [^"]+)"'),
        ("samsung", "Samsung", r'alt="(Samsung (?!logo)[^"]+)"'),
        ("oppo", "OPPO", r'alt="(OPPO (?!logo)[^"]+)"'),
        ("motorola", "Motorola", r'alt="(Motorola (?!logo)[^"]+)"'),
        ("huawei", "Huawei", r'alt="(Huawei (?!logo)[^"]+)"'),
        ("doro", "Doro", r'alt="(Doro (?!logo)[^"]+)"'),
        ("mobiwire", "MobiWire", r'alt="(MobiWire [^"]+)"'),
        ("one-nz", "One NZ", r'alt="(One NZ [^"]+)"'),
    ]
    models: list[Model] = []
    seen = set()
    for path, brand, pat in brand_map:
        html = fetch_html(f"https://userguide.one.nz/{path}/?type=phone")
        names = sorted(set(re.findall(pat, html)))
        for full in names:
            if "logo" in full.lower():
                continue
            # title without duplicated brand for Apple/Samsung naming
            title_name = full
            if brand == "Apple" and full.startswith("Apple "):
                title_name = full[len("Apple ") :]
            slug_base = slugify(title_name if brand == "Apple" else full)
            slug = f"{slug_base}-screen-repair-manual"
            key = slug
            if key in seen:
                continue
            seen.add(key)
            models.append(
                Model(
                    brand=brand,
                    name=full if brand != "Apple" else title_name,
                    title_name=title_name,
                    slug=slug,
                    source="one.nz",
                )
            )

    # iPhone 7 / 7 Plus not on one.nz phone guides — still common in NZ
    extras = [
        ("Apple", "iPhone 7"),
        ("Apple", "iPhone 7 Plus"),
    ]
    for brand, title_name in extras:
        slug = f"{slugify(title_name)}-screen-repair-manual"
        if slug in seen:
            continue
        seen.add(slug)
        models.append(
            Model(
                brand=brand,
                name=title_name,
                title_name=title_name,
                slug=slug,
                source="fix4u-extra",
            )
        )

    # Prefer newer first within brand for listing dates
    def sort_key(m: Model):
        return (m.brand, m.title_name.lower())

    return sorted(models, key=sort_key)


def model_notes(m: Model) -> tuple[str, str, list[str]]:
    """Return (models_covered_blurb, when_extra, tips)."""
    t = m.title_name
    brand = m.brand
    tips = []
    if brand == "Apple":
        if any(x in t for x in ("X", "11", "12", "13", "14", "15", "16", "17", "Air")):
            tips.append("We check Face ID / True Tone options and explain part grades before work starts.")
        if "SE" in t or t in ("iPhone 7", "iPhone 7 Plus", "iPhone 8", "iPhone 8 Plus"):
            tips.append("Touch ID path and home-button function are verified after assembly.")
        if "Pro Max" in t or "Plus" in t or "Air" in t:
            tips.append("Larger panels need careful frame alignment — we test for light bleed and uneven touch.")
        if "17" in t or "16" in t:
            tips.append("Latest-generation adhesives and connectors are handled on an ESD-safe bench.")
        covered = f"This guide is specifically for the <strong>{t}</strong> — not mixed with Plus/Pro siblings."
    elif brand == "Samsung":
        if "Z Flip" in t or "Z Fold" in t:
            covered = f"Foldables need hinge-aware handling. This manual covers <strong>{t}</strong> screen/cover glass repair pathways at FIX4U."
            tips.append("We inspect the hinge and inner/cover display before quoting.")
        elif "Note" in t:
            covered = f"Dedicated notes for the <strong>{t}</strong>, including S Pen cut-out / digitizer checks where relevant."
        elif "Xcover" in t or "XCover" in t:
            covered = f"Rugged <strong>{t}</strong> repairs — we reseal correctly after screen work where the design allows."
        else:
            covered = f"Model-specific screen repair notes for the <strong>{t}</strong>."
        tips.append("Samsung ultrasonic fingerprint / Always On Display behaviour is tested after replacement when the model supports it.")
    elif brand == "OPPO":
        covered = f"OPPO screen repair process for the <strong>{t}</strong>."
        tips.append("We verify in-display fingerprint and charging after the new assembly is fitted.")
    elif brand == "Motorola":
        covered = f"Motorola screen repair notes for the <strong>{t}</strong>."
        tips.append("Frame clips and water-resistance adhesives vary by Moto/Edge model — we match the assembly carefully.")
    elif brand == "Huawei":
        covered = f"Huawei screen repair notes for the <strong>{t}</strong>."
        tips.append("We confirm model variant (global/NZ) before ordering parts.")
    else:
        covered = f"Screen repair overview for the <strong>{t}</strong>."
        tips.append("We confirm the exact variant in-store before quoting.")
    when = [
        "Cracked or shattered front glass",
        "Dead touch zones, ghost touch, or unresponsive display",
        "Black screen, coloured lines, or bleeding pixels after a drop",
        "Dim / flickering backlight or display burn after impact",
    ]
    return covered, when, tips


def article_html(m: Model, cover_url: str, date_label: str) -> str:
    covered, when, tips = model_notes(m)
    title = f"{m.title_name} Screen Repair Manual"
    tips_html = "".join(f"<li>{t}</li>" for t in tips)
    when_html = "".join(f"<li>{w}</li>" for w in when)
    brand_line = m.brand if m.brand != "Apple" else "Apple iPhone"
    secondary = IMG_SAM if m.brand == "Samsung" else IMG_CRACK
    body = f"""
<p>This FIX4U repair manual explains how we approach cracked or faulty screens on the <strong>{m.title_name}</strong> ({brand_line}) at our Rosedale, Auckland workshop. It is written for customers who want a clear process — not a full DIY teardown guide.</p>

<h2>Model covered</h2>
<p>{covered}</p>

<h2>When you need a screen repair</h2>
<ul>
{when_html}
</ul>
<img src="{secondary}" alt="Cracked {m.title_name} screen before repair at FIX4U Auckland" style="margin:12px 0 18px;">

<h2>What we check on the {m.title_name}</h2>
<ul>
{tips_html}
<li>Frame bends, battery swelling, and liquid indicators before opening.</li>
<li>Cameras, earpiece, loudspeaker, and charging after the new screen is fitted.</li>
</ul>

<h2>Repair process at FIX4U</h2>
<ol>
<li><strong>Check-in &amp; backup reminder</strong> — we confirm the exact {m.title_name} variant and ask you to back up if possible.</li>
<li><strong>Free diagnosis</strong> — inspect display damage, chassis, biometric path, and battery condition.</li>
<li><strong>Quote first</strong> — clear pricing and part options; work starts only after you approve.</li>
<li><strong>Screen replacement</strong> — controlled heat/adhesive release, new assembly fitted, connectors reseated on an ESD-safe bench.</li>
<li><strong>Function tests</strong> — display, touch, proximity, audio, cameras, and biometrics as applicable to this model.</li>
<li><strong>Handover</strong> — device cleaned, warranty explained (repairs: 3 months).</li>
</ol>
<img src="{IMG_BENCH}" alt="{m.title_name} screen repair on the FIX4U workbench" style="margin:12px 0 18px;">

<h2>Parts &amp; warranty</h2>
<p>We explain part grade options in plain language before work begins. Repair workmanship is covered for <strong>3 months</strong>. Product sales carry a separate 12‑month warranty.</p>

<h2>DIY warning</h2>
<p>Incorrect heat, prying, or connector force can permanently damage biometrics or the logic board on a {m.title_name}. If you are unsure, stop and book in-store help at FIX4U.</p>

<p><a class="btn btn-primary" href="https://fix4u.co.nz/contact-us-fix4u/book-repair/">Book {m.title_name} screen repair</a> · WhatsApp <a href="https://wa.me/6421885501" target="_blank" rel="noopener">+64 21 885 501</a> · Rosedale, Auckland · Serving North Shore customers with phones commonly sold by NZ carriers including One NZ.</p>
"""
    return f"""<section class="rm-article">
  <div class="wrap-article">
    <p class="rm-back"><a href="https://fix4u.co.nz/repair-manual/">← Back to Repair Manual</a></p>
    <h1 class="rm-title">{title}</h1>
    <div class="rm-meta">Repair Manual · {date_label} · {m.brand}</div>
    <div class="rm-feat"><img src="{cover_url}" alt="{title} — FIX4U Auckland"></div>
    <div class="rm-body">
{body}
    </div>
  </div>
</section>
"""


def build_content(shell: str, m: Model, cover_url: str, date_label: str) -> str:
    article = article_html(m, cover_url, date_label)
    # Replace existing article section
    new_shell, n = re.subn(
        r"(?is)<section class=\"rm-article\">[\s\S]*?</section>",
        article,
        shell,
        count=1,
    )
    if n != 1:
        raise RuntimeError(f"Could not splice article for {m.slug}")
    # Ensure title string leftover not needed — shell title only in article
    return new_shell


def make_cover(m: Model) -> Path:
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    bg, fg, accent = BRAND_COLORS.get(m.brand, ("#263238", "#F5F7FA", "#1E88E5"))
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    # atmosphere bars
    draw.rectangle([0, 0, w, 12], fill=accent)
    draw.rectangle([0, h - 90, w, h], fill="#0E1620" if bg != "#F5F5F7" else "#E8EEF5")
    try:
        font_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        font_md = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
    except OSError:
        font_lg = font_md = font_sm = ImageFont.load_default()

    draw.text((64, 80), "FIX4U", font=font_md, fill=accent)
    draw.text((64, 140), "Screen Repair Manual", font=font_sm, fill=fg)
    # wrap title
    title = m.title_name
    draw.text((64, 220), title, font=font_lg, fill=fg)
    draw.text((64, 340), "Auckland · Rosedale · Diagnosis → Quote → Repair → Warranty", font=font_sm, fill=fg)
    draw.text((64, h - 58), "fix4u.co.nz/repair-manual/", font=font_sm, fill="#90A4AE")
    # accent device block
    draw.rounded_rectangle([820, 120, 1120, 520], radius=36, outline=accent, width=6)
    draw.rounded_rectangle([860, 170, 1080, 470], radius=24, fill=accent)
    path = COVER_DIR / f"{m.slug}.jpg"
    img.save(path, "JPEG", quality=88)
    return path


def upload_media(path: Path, alt: str, title: str) -> tuple[int, str]:
    boundary = "----Fix4uBoundary7MA4YWxkTrZu0gW"
    filename = path.name
    file_bytes = path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + file_bytes + (
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="alt_text"\r\n\r\n{alt}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="title"\r\n\r\n{title}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="caption"\r\n\r\n{alt}\r\n'
        f"--{boundary}--\r\n"
    ).encode()
    headers = auth_headers()
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    req = urllib.request.Request(f"{BASE}/wp-json/wp/v2/media", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, context=CTX, timeout=120) as r:
        data = json.loads(r.read().decode())
    return data["id"], data["source_url"]


def excerpt_for(m: Model) -> str:
    return (
        f"{m.title_name} screen repair manual from FIX4U Auckland — diagnosis, quote, "
        f"replacement steps, testing and 3‑month repair warranty. Serving North Shore & One NZ handset users."
    )


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"created": {}, "covers": {}, "trashed_series": False}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


def existing_slugs() -> dict[str, int]:
    out = {}
    page = 1
    while True:
        status, data = http_json(
            "GET",
            f"/wp-json/wp/v2/posts?per_page=100&page={page}&categories={CAT_REPAIR}"
            f"&status=publish,draft,private,future&_fields=id,slug",
        )
        if not data:
            break
        for p in data:
            out[p["slug"]] = p["id"]
        if len(data) < 100:
            break
        page += 1
    return out


SERIES_SLUGS = [
    "iphone-16-series-screen-repair-manual",
    "iphone-15-series-screen-repair-manual",
    "iphone-14-series-screen-repair-manual",
    "iphone-13-series-screen-repair-manual",
    "iphone-12-series-screen-repair-manual",
    "iphone-11-series-screen-repair-manual",
    "iphone-x-xs-xr-screen-repair-manual",
    "iphone-se-2nd-3rd-screen-repair-manual",
    "iphone-8-8-plus-screen-repair-manual",
    "iphone-7-7-plus-screen-repair-manual",
]


def trash_series(state: dict) -> None:
    if state.get("trashed_series"):
        return
    for slug in SERIES_SLUGS:
        try:
            status, posts = http_json("GET", f"/wp-json/wp/v2/posts?slug={slug}&status=publish,draft&_fields=id,slug")
            for p in posts:
                http_json("DELETE", f"/wp-json/wp/v2/posts/{p['id']}?force=false")
                print("trashed series", slug, p["id"])
        except Exception as e:
            print("trash fail", slug, e)
    state["trashed_series"] = True
    save_state(state)


def card_html(m: Model, link: str, cover_url: str, date_label: str) -> str:
    title = f"{m.title_name} Screen Repair Manual"
    return f"""
      <article class="blog-card" data-brand="{m.brand}">
        <a href="{link}" aria-label="{title}"><div class="thumb"><img src="{cover_url}" alt="{title}" loading="lazy"></div></a>
        <div class="body">
          <div class="date">{date_label} · {m.brand}</div>
          <h2><a href="{link}">{title}</a></h2>
          <p>{m.title_name} screen repair process at FIX4U Auckland — diagnosis, quote, replacement and warranty.</p>
          <p><a class="more" href="{link}">Read manual →</a></p>
        </div>
      </article>
"""


def update_listing(models: list[Model], created: dict, covers: dict) -> None:
    status, page = http_json("GET", "/wp-json/wp/v2/pages/2782?context=edit&_fields=content")
    raw = page["content"]["raw"]

    # Group models
    order = ["Apple", "Samsung", "OPPO", "Motorola", "Huawei", "Doro", "MobiWire", "One NZ"]
    groups: dict[str, list[Model]] = {b: [] for b in order}
    for m in models:
        groups.setdefault(m.brand, []).append(m)

    sections = ['<!-- NEW_MANUALS_PER_MODEL_2026 -->']
    for brand in order:
        items = groups.get(brand) or []
        if not items:
            continue
        # newest-ish first for Apple/Samsung by sorting reverse title with heuristics
        items = sorted(items, key=lambda x: x.title_name.lower(), reverse=True)
        sections.append(f'<h2 class="rm-brand-heading" style="grid-column:1/-1;margin:28px 0 8px;font-family:Outfit,sans-serif;font-size:1.35rem;color:#263238;">{brand} screen repair manuals</h2>')
        sections.append(f'<p style="grid-column:1/-1;margin:0 0 8px;color:#546E7A;">Model-by-model guides for {brand} phones commonly used in New Zealand (including devices supported in One NZ user guides).</p>')
        for m in items:
            info = created.get(m.slug)
            if not info:
                continue
            cover = covers.get(m.slug, {}).get("url") or IMG_PRO
            sections.append(card_html(m, info["link"], cover, info.get("date_label", "2026")))

    block = "\n".join(sections)

    # Replace from NEW_MANUALS marker through end of blog-grid cards before closing wrap
    if "<!-- NEW_MANUALS_2026 -->" in raw:
        start = raw.find("<!-- NEW_MANUALS_2026 -->")
    elif "<!-- NEW_MANUALS_PER_MODEL_2026 -->" in raw:
        start = raw.find("<!-- NEW_MANUALS_PER_MODEL_2026 -->")
    else:
        start = raw.find('<div class="wrap blog-grid">')
        if start != -1:
            start = raw.find(">", start) + 1

    end = raw.find("</div>", raw.find('<div class="wrap blog-grid">'))
    # find closing of blog-grid: after last article before section end — use marker end
    # Safer: replace between marker and `</div>\n    </section>` following grid
    m = re.search(
        r'(?is)(<div class="wrap blog-grid">)([\s\S]*?)(</div>\s*</section>)',
        raw,
    )
    if not m:
        raise RuntimeError("listing blog-grid not found")
    new_raw = raw[: m.start(2)] + "\n" + block + "\n    " + raw[m.start(3) :]

    # inject brand heading CSS once
    css = """
/* FIX4U_RM_BRAND_HEADINGS */
.bt-a .rm-brand-heading { letter-spacing: -0.02em; }
.bt-a .blog-grid { align-items: stretch; }
"""
    if "FIX4U_RM_BRAND_HEADINGS" not in new_raw:
        new_raw = new_raw.replace("</style>", css + "\n</style>", 1)

    # Update hero copy if present
    new_raw = re.sub(
        r'(?is)(<h1[^>]*>)(.*?)(</h1>)',
        lambda mo: mo.group(0)
        if "Repair Manual" not in mo.group(2) and "repair manual" not in mo.group(2).lower()
        else f"{mo.group(1)}Repair Manual{mo.group(3)}",
        new_raw,
        count=1,
    )

    http_json("POST", "/wp-json/wp/v2/pages/2782", {"content": new_raw})
    print("listing updated, cards:", sum(1 for s in sections if "blog-card" in s))


def main():
    if not SHELL_PATH.exists():
        raise SystemExit("Missing shell template — fetch post 3254 first")
    shell = SHELL_PATH.read_text()
    state = load_state()
    models = load_one_nz_models()
    print("models total", len(models))
    for brand in sorted({m.brand for m in models}):
        print(" ", brand, sum(1 for m in models if m.brand == brand))

    existing = existing_slugs()
    print("existing repair-manual posts", len(existing))

    # Create covers + posts
    # Stagger dates newest first overall
    base_day = datetime(2026, 8, 11, tzinfo=timezone.utc)
    created = state.setdefault("created", {})
    covers = state.setdefault("covers", {})

    # Process Apple first then others
    brand_order = ["Apple", "Samsung", "OPPO", "Motorola", "Huawei", "Doro", "MobiWire", "One NZ"]
    ordered = []
    for b in brand_order:
        # reverse so newer-looking names get later dates? Actually assign newer dates to newer models
        group = [m for m in models if m.brand == b]
        group = sorted(group, key=lambda x: x.title_name.lower(), reverse=True)
        ordered.extend(group)

    for idx, m in enumerate(ordered):
        if m.slug in created and created[m.slug].get("id"):
            print("skip exists state", m.slug)
            continue
        if m.slug in existing and m.slug not in SERIES_SLUGS:
            # already on site
            status, posts = http_json("GET", f"/wp-json/wp/v2/posts/{existing[m.slug]}?context=edit&_fields=id,link,slug")
            created[m.slug] = {
                "id": posts["id"],
                "link": posts["link"],
                "date_label": "2026",
            }
            save_state(state)
            print("tracked existing", m.slug)
            continue

        # cover
        if m.slug not in covers:
            path = make_cover(m)
            mid, url = upload_media(path, f"{m.title_name} screen repair manual — FIX4U Auckland", f"{m.title_name} Screen Repair Manual")
            covers[m.slug] = {"id": mid, "url": url}
            save_state(state)
            print("uploaded cover", m.slug, mid)
            time.sleep(0.2)
        cover_url = covers[m.slug]["url"]
        cover_id = covers[m.slug]["id"]

        # date: spread backwards from Aug 2026
        day_offset = idx  # one per day-ish but keep in 2025-2026
        # keep within ~4 months
        from datetime import timedelta

        dt = base_day - timedelta(hours=idx * 3)
        date_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
        date_label = dt.strftime("%d %b %Y").lstrip("0")

        content = build_content(shell, m, cover_url, date_label)
        title = f"{m.title_name} Screen Repair Manual"
        payload = {
            "title": title,
            "slug": m.slug,
            "status": "publish",
            "categories": [CAT_REPAIR],
            "excerpt": excerpt_for(m),
            "content": content,
            "featured_media": cover_id,
            "date": date_iso,
        }
        try:
            status, post = http_json("POST", "/wp-json/wp/v2/posts", payload)
        except RuntimeError as e:
            if "已存在" in str(e) or "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                print("duplicate slug, fetching", m.slug)
                status, posts = http_json("GET", f"/wp-json/wp/v2/posts?slug={m.slug}&_fields=id,link,slug")
                post = posts[0]
            else:
                print("ERROR create", m.slug, e)
                save_state(state)
                raise
        created[m.slug] = {
            "id": post["id"],
            "link": post.get("link") or f"{BASE}/{m.slug}/",
            "date_label": date_label,
            "brand": m.brand,
            "title": title,
        }
        save_state(state)
        print("created", post["id"], m.slug)
        time.sleep(0.25)

    trash_series(state)
    update_listing(models, created, covers)
    print("DONE created", len(created), "of", len(models))


if __name__ == "__main__":
    main()
