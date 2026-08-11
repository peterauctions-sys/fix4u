#!/usr/bin/env python3
"""Brand folders (4-col) + rebuild iPhone 16 family manuals from iFixit (logo-scrubbed images)."""
from __future__ import annotations

import base64
import html as htmlmod
import io
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CTX = ssl.create_default_context()
BASE = "https://fix4u.co.nz"
CAT_REPAIR = 4
PAGE_RM = 2782
STATE_PATH = Path("/tmp/rm_generate_state.json")
IFIXIT_STATE = Path("/tmp/iphone16_ifixit_state.json")
COVER_DIR = Path("/tmp/rm_brand_covers")
IMG_DIR = Path("/tmp/ifixit_scrubbed")

BRANDS = [
    ("Apple", "apple", "iPhone screen repair manuals"),
    ("Samsung", "samsung", "Galaxy & Samsung phone screen repair manuals"),
    ("OPPO", "oppo", "OPPO phone screen repair manuals"),
    ("Motorola", "motorola", "Motorola phone screen repair manuals"),
    ("Huawei", "huawei", "Huawei phone screen repair manuals"),
    ("Doro", "doro", "Doro phone screen repair manuals"),
    ("MobiWire", "mobiwire", "MobiWire phone screen repair manuals"),
    ("One NZ", "one-nz", "One NZ handset screen repair manuals"),
]

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

IPHONE16_GUIDES = {
    "iphone-16-screen-repair-manual": {
        "guide_id": 177288,
        "json": "/tmp/ifixit_iphone-16.json",
        "title_name": "iPhone 16",
        "post_id": 3366,
    },
    "iphone-16-plus-screen-repair-manual": {
        "guide_id": 177847,
        "json": "/tmp/ifixit_iphone-16-plus.json",
        "title_name": "iPhone 16 Plus",
        "post_id": 3364,
    },
    "iphone-16-pro-screen-repair-manual": {
        "guide_id": 180298,
        "json": "/tmp/ifixit_iphone-16-pro.json",
        "title_name": "iPhone 16 Pro",
        "post_id": 3362,
    },
    "iphone-16-pro-max-screen-repair-manual": {
        "guide_id": 178634,
        "json": "/tmp/ifixit_iphone-16-pro-max.json",
        "title_name": "iPhone 16 Pro Max",
        "post_id": 3360,
    },
    "iphone-16e-screen-repair-manual": {
        "guide_id": 186614,
        "json": "/tmp/ifixit_iphone-16e.json",
        "title_name": "iPhone 16e",
        "post_id": 3358,
    },
}

# Prefer these step-title keywords in order for illustrated procedure
STEP_PICK_PATTERNS = [
    r"before you begin|prepare",
    r"tape over",
    r"pentalobe",
    r"heat the bottom|create a gap|suction",
    r"insert an opening pick|slice the bottom",
    r"screen information",
    r"prop up the screen|swing open",
    r"connector cover|cover screws|remove the covers",
    r"disconnect the screen",
    r"remove the screen",
    r"ambient light sensor|front sensor",
    r"install the ambient|install the front sensor|place the ambient|press the ambient",
    r"remove the (screen )?adhesive|remove the old adhesive",
    r"orient the adhesive|apply the (replacement )?adhesive|apply the adhesive",
    r"connect the screen",
    r"install the cover|cover the connectors",
    r"place the screen|install the screen onto the frame",
    r"heat the screen|press the (back glass|screen)",
    r"install the pentalobe",
]


def auth_headers(content_type: str | None = None) -> dict:
    token = base64.b64encode(
        f"{os.environ['WORDPRESS_ADMIN_USER']}:{os.environ['WORDPRESS_APPLICATION_PASSWORD']}".encode()
    ).decode()
    h = {"Authorization": f"Basic {token}", "User-Agent": "Mozilla/5.0 CursorAgent", "Accept": "*/*"}
    if content_type:
        h["Content-Type"] = content_type
    return h


def http_json(method: str, path: str, data: dict | None = None, timeout: int = 60):
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
        raise RuntimeError(f"{method} {path} -> {e.code}: {err[:600]}") from e


def log(msg: str) -> None:
    print(msg, flush=True)


def upload_media(path: Path, alt: str, title: str) -> tuple[int, str]:
    boundary = "----Fix4uBoundaryBrandFolders"
    file_bytes = path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + file_bytes + (
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="alt_text"\r\n\r\n{alt}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="title"\r\n\r\n{title}\r\n'
        f"--{boundary}--\r\n"
    ).encode()
    headers = auth_headers()
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    headers["Content-Disposition"] = f'attachment; filename="{path.name}"'
    req = urllib.request.Request(f"{BASE}/wp-json/wp/v2/media", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
        data = json.loads(r.read().decode())
    return data["id"], data["source_url"]


def scrub_ifixit_logo(img: Image.Image) -> Image.Image:
    """Remove common bottom/corner watermarks; keep photo content."""
    img = img.convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img)
    # Sample background near bottom-right interior
    sample = img.getpixel((max(0, w - 30), max(0, h - 30)))
    # Cover thin bottom strip + bottom-right badge area (where logos often sit)
    draw.rectangle([0, h - max(18, h // 45), w, h], fill=sample)
    draw.rectangle([w - max(160, w // 8), h - max(70, h // 14), w, h], fill=sample)
    # Soft top-left badge area sometimes used
    tl = img.getpixel((20, 20))
    # only scrub TL if very light (white bg) and small dark cluster — skip aggressive crop
    return img


def download_scrub_upload(url: str, filename: str, alt: str) -> str:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 FIX4U"})
    with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
        img = Image.open(io.BytesIO(r.read()))
    img = scrub_ifixit_logo(img)
    path = IMG_DIR / filename
    img.save(path, "JPEG", quality=88)
    _id, src = upload_media(path, alt, alt)
    time.sleep(0.15)
    return src


def step_text(step: dict) -> str:
    bits = []
    for line in step.get("lines") or []:
        t = line.get("text_rendered") or line.get("text") or ""
        t = re.sub(r"<[^>]+>", "", t)
        t = htmlmod.unescape(t).strip()
        if t:
            bits.append(t)
    return " ".join(bits)


def step_image_url(step: dict) -> str | None:
    media = step.get("media") or {}
    if media.get("type") != "image":
        return None
    data = media.get("data") or []
    if not data:
        return None
    d = data[0]
    return d.get("huge") or d.get("large") or d.get("medium") or d.get("standard")


def pick_steps(guide: dict) -> list[dict]:
    steps = guide.get("steps") or []
    picked = []
    used = set()
    for pat in STEP_PICK_PATTERNS:
        rx = re.compile(pat, re.I)
        for idx, s in enumerate(steps):
            if idx in used:
                continue
            title = (s.get("title") or "").strip() or f"Step {idx+1}"
            blob = title + " " + step_text(s)[:120]
            if rx.search(blob):
                picked.append(s)
                used.add(idx)
                break
    # Ensure at least one clearly titled Install / Place the screen step
    has_install = any(
        re.search(r"place the screen|install the screen|install the pentalobe", (s.get("title") or ""), re.I)
        for s in picked
    )
    if not has_install:
        for idx, s in enumerate(steps):
            if idx in used:
                continue
            if re.search(r"place the screen|install the screen onto", (s.get("title") or ""), re.I):
                picked.append(s)
                break
    return picked


def rewrite_for_fix4u(text: str, model: str) -> str:
    t = text
    replacements = [
        (r"\biFixit\b", "FIX4U"),
        (r"this guide", "this FIX4U workshop procedure"),
        (r"your iPhone", f"the {model}"),
        (r"your phone", f"the {model}"),
    ]
    for a, b in replacements:
        t = re.sub(a, b, t, flags=re.I)
    # Keep practical length
    if len(t) > 520:
        t = t[:500].rsplit(" ", 1)[0] + "…"
    return t


def build_iphone16_article(meta: dict, guide: dict, image_map: dict[str, str], cover_url: str) -> str:
    model = meta["title_name"]
    title = f"{model} Screen Replacement Manual"
    picked = pick_steps(guide)
    # Split into Disassembly / Transfer / Install
    dis_html = []
    xfer_html = []
    install_html = []
    for i, s in enumerate(picked, 1):
        stitle = (s.get("title") or f"Step {i}").strip()
        body = rewrite_for_fix4u(step_text(s), model)
        img_url = image_map.get(str(s.get("stepid")))
        block = f"<h3>{i}. {htmlmod.escape(stitle)}</h3>\n<p>{htmlmod.escape(body)}</p>\n"
        if img_url:
            block += (
                f'<img src="{img_url}" alt="{htmlmod.escape(model)} — {htmlmod.escape(stitle)} (logo-free)" '
                f'style="margin:10px 0 18px;border-radius:12px;width:100%;max-width:860px;height:auto;">\n'
            )
        low = stitle.lower()
        if any(k in low for k in ["adhesive", "connect the screen", "place the screen", "install the screen", "install the pentalobe", "heat the screen", "press the", "cover the connector", "install the cover"]):
            if any(k in low for k in ["remove the screen adhesive", "remove the old adhesive", "orient", "apply the"]):
                install_html.append(block)
            elif "ambient" in low or "front sensor" in low:
                # install sensor onto new screen is transfer/install hybrid
                if "install" in low or "place the ambient" in low or "press the ambient" in low:
                    xfer_html.append(block)
                else:
                    xfer_html.append(block)
            else:
                install_html.append(block)
        elif any(k in low for k in ["ambient", "front sensor"]):
            xfer_html.append(block)
        else:
            dis_html.append(block)

    src_note = (
        f'<p class="rm-source" style="font-size:.85rem;color:#546E7A;">Procedure adapted for FIX4U workshop use from the public '
        f'<a href="https://www.ifixit.com/Guide/{meta["guide_id"]}" target="_blank" rel="noopener">iFixit {model} Screen Replacement</a> '
        f"guide. Photos scrubbed of third-party logos. Not a substitute for trained technician work — book in-store for warranty-backed repair.</p>"
    )

    return f"""<section class="rm-article">
  <div class="wrap-article">
    <p class="rm-back"><a href="https://fix4u.co.nz/repair-manual/apple/">← Apple repair manuals</a> · <a href="https://fix4u.co.nz/repair-manual/">All brands</a></p>
    <h1 class="rm-title">{htmlmod.escape(title)}</h1>
    <div class="rm-meta">Repair Manual · Apple · Screen replacement · Updated from iFixit procedure</div>
    <div class="rm-feat"><img src="{cover_url}" alt="{htmlmod.escape(title)} — FIX4U Auckland"></div>
    <div class="rm-body">
<p>This FIX4U manual walks through <strong>{htmlmod.escape(model)} screen replacement</strong> the way we approach it in our Rosedale workshop — based on the current public iFixit tear-down sequence, rewritten for customers and technicians. It includes a clear <strong>Install</strong> section (adhesive, reconnect, seat the new screen, and pentalobe screws).</p>
<p><strong>Safety:</strong> drain battery below ~25% before opening. On iPhone 16-class devices the battery often cannot be disconnected first — avoid metal tools near connectors. Soften adhesive with controlled heat only.</p>
{src_note}

<h2>1) Prepare &amp; open (disassembly)</h2>
{''.join(dis_html) or '<p>Open the {model} carefully after heating the adhesive perimeter and removing the bottom pentalobe screws.</p>'}

<h2>2) Transfer parts to the new screen</h2>
<p>Move the ambient light / front sensor hardware from the old assembly to the new {htmlmod.escape(model)} screen when the replacement part requires it.</p>
{''.join(xfer_html) or '<p>Transfer and seat the ambient light sensor (and related front sensors on some models) onto the new display before final install.</p>'}

<h2>3) Install the new screen</h2>
<p>This is the installation phase: clean old adhesive, apply new waterproofing adhesive, reconnect display flexes, test, then seat and screw the {htmlmod.escape(model)} screen.</p>
{''.join(install_html) or '<p>Apply new adhesive, connect the screen, place/install the assembly onto the frame, press the perimeter, and install the pentalobe screws.</p>'}

<h2>4) Calibrate &amp; handover</h2>
<ol>
<li>Power on and check display, touch, True Tone / auto-brightness behaviour, Face ID path, earpiece and cameras.</li>
<li>For genuine Apple screens: <strong>Settings → General → About → Parts &amp; Service History → Restart &amp; Finish Repair</strong> (Repair Assistant) when available.</li>
<li>Explain FIX4U repair warranty (3 months) and return the device cleaned.</li>
</ol>

<p><a class="btn btn-primary" href="https://fix4u.co.nz/contact-us-fix4u/book-repair/">Book {htmlmod.escape(model)} screen repair</a> · WhatsApp <a href="https://wa.me/6421885501" target="_blank" rel="noopener">+64 21 885 501</a> · Rosedale, Auckland</p>
    </div>
  </div>
</section>
"""


FOUR_COL_CSS = """
/* FIX4U_RM_FOUR_COL */
.bt-a .blog-grid,
.bt-a .rm-folder-grid {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 22px !important;
  padding: 18px 0 56px !important;
}
@media (max-width: 1100px) {
  .bt-a .blog-grid,
  .bt-a .rm-folder-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
}
@media (max-width: 640px) {
  .bt-a .blog-grid,
  .bt-a .rm-folder-grid { grid-template-columns: 1fr !important; }
}
.bt-a .rm-brand-heading,
.bt-a .rm-folder-intro { grid-column: 1 / -1; }
.bt-a .folder-card .thumb { aspect-ratio: 16/10; background: #EEF5FC; }
.bt-a .folder-card .thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
"""


def make_brand_cover(brand: str, slug: str) -> Path:
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    bg, fg, accent = BRAND_COLORS.get(brand, ("#263238", "#F5F7FA", "#1E88E5"))
    img = Image.new("RGB", (1200, 750), bg)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 1200, 14], fill=accent)
    try:
        font_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_md = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except OSError:
        font_lg = font_md = ImageFont.load_default()
    draw.text((64, 120), "FIX4U", font=font_md, fill=accent)
    draw.text((64, 200), brand, font=font_lg, fill=fg)
    draw.text((64, 320), "Repair manuals folder", font=font_md, fill=fg)
    draw.text((64, 400), "Screen replacement guides by model", font=font_md, fill=fg)
    path = COVER_DIR / f"brand-{slug}.jpg"
    img.save(path, "JPEG", quality=88)
    return path


def ensure_categories(state: dict) -> dict:
    cats = state.setdefault("brand_cats", {})
    # list children of repair-manual
    status, existing = http_json("GET", f"/wp-json/wp/v2/categories?parent={CAT_REPAIR}&per_page=100")
    by_slug = {c["slug"]: c for c in existing}
    for brand, slug, desc in BRANDS:
        if slug in cats and cats[slug].get("id"):
            continue
        if slug in by_slug:
            cats[slug] = {"id": by_slug[slug]["id"], "name": brand}
            continue
        _s, created = http_json(
            "POST",
            "/wp-json/wp/v2/categories",
            {"name": brand, "slug": slug, "parent": CAT_REPAIR, "description": desc},
        )
        cats[slug] = {"id": created["id"], "name": brand}
        print("created category", brand, created["id"])
    state["brand_cats"] = cats
    return cats


def assign_posts_to_brand_cats(state: dict, cats: dict) -> None:
    created = json.loads(STATE_PATH.read_text()).get("created", {})
    brand_to_slug = {b: s for b, s, _ in BRANDS}
    n = 0
    for slug, info in created.items():
        brand = info.get("brand")
        bslug = brand_to_slug.get(brand)
        if not bslug or bslug not in cats:
            continue
        key = f"cat_assigned_{info['id']}"
        if state.get(key):
            continue
        cat_ids = [CAT_REPAIR, cats[bslug]["id"]]
        try:
            http_json("POST", f"/wp-json/wp/v2/posts/{info['id']}", {"categories": cat_ids}, timeout=25)
            state[key] = True
            n += 1
            if n % 10 == 0:
                save_state(state)
                log(f"categorized {n}…")
        except Exception as e:
            log(f"cat fail {info['id']} {e}")
            continue
        time.sleep(0.05)
    save_state(state)
    log(f"categorized total new {n}")


def folder_card(brand: str, link: str, cover: str, count: int, blurb: str) -> str:
    return f"""
      <article class="blog-card folder-card" data-brand="{htmlmod.escape(brand)}">
        <a href="{link}" aria-label="{htmlmod.escape(brand)} repair manuals">
          <div class="thumb"><img src="{cover}" alt="{htmlmod.escape(brand)} repair manuals folder" loading="lazy"></div>
        </a>
        <div class="body">
          <div class="date">Brand folder · {count} manuals</div>
          <h2><a href="{link}">{htmlmod.escape(brand)}</a></h2>
          <p>{htmlmod.escape(blurb)}</p>
          <p><a class="more" href="{link}">Open folder →</a></p>
        </div>
      </article>
"""


def model_card(title: str, link: str, cover: str, date_label: str, brand: str) -> str:
    return f"""
      <article class="blog-card" data-brand="{htmlmod.escape(brand)}">
        <a href="{link}" aria-label="{htmlmod.escape(title)}"><div class="thumb"><img src="{cover}" alt="{htmlmod.escape(title)}" loading="lazy"></div></a>
        <div class="body">
          <div class="date">{htmlmod.escape(date_label)} · {htmlmod.escape(brand)}</div>
          <h2><a href="{link}">{htmlmod.escape(title)}</a></h2>
          <p>Screen repair / replacement process at FIX4U Auckland.</p>
          <p><a class="more" href="{link}">Read manual →</a></p>
        </div>
      </article>
"""


def get_listing_shell() -> str:
    _s, page = http_json("GET", f"/wp-json/wp/v2/pages/{PAGE_RM}?context=edit&_fields=content")
    return page["content"]["raw"]


def inject_four_col(css_host: str) -> str:
    raw = css_host
    # force replace existing blog-grid 3-col rule if present
    raw = re.sub(
        r"(?is)\.blog-grid\s*\{[^}]*grid-template-columns:\s*repeat\(3[^}]*\}",
        ".blog-grid { /* superseded by FIX4U_RM_FOUR_COL */ }",
        raw,
        count=1,
    )
    if "FIX4U_RM_FOUR_COL" not in raw:
        raw = raw.replace("</style>", FOUR_COL_CSS + "\n</style>", 1)
    else:
        # refresh block
        raw = re.sub(r"(?is)/\* FIX4U_RM_FOUR_COL \*/[\s\S]*?(?=/\*|</style>)", FOUR_COL_CSS + "\n", raw, count=1)
    return raw


def update_main_listing(state: dict, brand_pages: dict, covers: dict, counts: dict) -> None:
    raw = get_listing_shell()
    raw = inject_four_col(raw)
    cards = ['<!-- BRAND_FOLDERS_2026 -->']
    blurbs = {b: d for b, _s, d in BRANDS}
    for brand, slug, _d in BRANDS:
        info = brand_pages[slug]
        cover = covers[slug]
        cards.append(folder_card(brand, info["link"], cover, counts.get(brand, 0), blurbs[brand]))
    block = "\n".join(cards)
    m = re.search(r'(?is)(<div class="wrap blog-grid">)([\s\S]*?)(</div>\s*</section>)', raw)
    if not m:
        raise RuntimeError("blog-grid not found on listing")
    raw = raw[: m.start(2)] + "\n" + block + "\n    " + raw[m.start(3) :]
    # hero blurb
    raw = re.sub(
        r"(?is)(<h1>Repair Manual</h1>\s*<p>)([^<]+)(</p>)",
        r"\1Browse by brand folder — Apple, Samsung, OPPO and more. Each folder lists model screen-repair manuals four across.\3",
        raw,
        count=1,
    )
    http_json("POST", f"/wp-json/wp/v2/pages/{PAGE_RM}", {"content": raw})
    print("main listing updated")


def build_brand_page_content(shell: str, brand: str, slug: str, cards_html: str) -> str:
    raw = inject_four_col(shell)
    # Hero under page banner (Repair Manual listing shell)
    raw = re.sub(
        r"(?is)(<div class=\"wrap\">\s*)<h1>[^<]*</h1>\s*<p>[^<]*</p>",
        f'\\1<h1>{htmlmod.escape(brand)} Repair Manuals</h1>\n      <p>Screen replacement manuals for {htmlmod.escape(brand)} — four per row. Select a model to open the full FIX4U procedure.</p>',
        raw,
        count=1,
    )
    block = f"""<!-- BRAND_MODELS_{slug} -->
    <p class="rm-folder-intro" style="grid-column:1/-1;margin:0 0 4px;"><a href="https://fix4u.co.nz/repair-manual/">← All brand folders</a></p>
    <h2 class="rm-brand-heading" style="margin:8px 0 4px;font-family:Outfit,sans-serif;">{htmlmod.escape(brand)} models</h2>
{cards_html}
"""
    m = re.search(r'(?is)(<div class="wrap blog-grid">)([\s\S]*?)(</div>\s*</section>)', raw)
    if not m:
        raise RuntimeError("blog-grid missing in shell")
    raw = raw[: m.start(2)] + "\n" + block + "\n    " + raw[m.start(3) :]
    return raw


def ensure_brand_pages(state: dict) -> tuple[dict, dict, dict]:
    created = json.loads(STATE_PATH.read_text()).get("created", {})
    covers_models = json.loads(STATE_PATH.read_text()).get("covers", {})
    shell = get_listing_shell()
    brand_pages = state.setdefault("brand_pages", {})
    brand_covers = state.setdefault("brand_covers", {})
    counts: dict[str, int] = {}

    for brand, slug, desc in BRANDS:
        models = [(k, v) for k, v in created.items() if v.get("brand") == brand]
        counts[brand] = len(models)
        if slug not in brand_covers:
            path = make_brand_cover(brand, slug)
            mid, url = upload_media(path, f"{brand} repair manuals — FIX4U", f"{brand} Repair Manuals")
            brand_covers[slug] = {"id": mid, "url": url}
            state["brand_covers"] = brand_covers
            save_state(state)
            print("brand cover", slug, mid)

        # cards
        cards = []
        # sort: iphone 16 family first-ish then alpha reverse
        def sort_key(item):
            k, v = item
            return (0 if "iphone-16" in k else 1, v.get("title", k).lower())

        for mslug, info in sorted(models, key=sort_key):
            cover = covers_models.get(mslug, {}).get("url") or brand_covers[slug]["url"]
            cards.append(
                model_card(
                    info.get("title") or mslug,
                    info.get("link") or f"{BASE}/{mslug}/",
                    cover,
                    info.get("date_label", "2026"),
                    brand,
                )
            )
        content = build_brand_page_content(shell, brand, slug, "\n".join(cards))
        payload = {
            "title": f"{brand} Repair Manuals",
            "slug": slug,
            "status": "publish",
            "parent": PAGE_RM,
            "template": "template-blank.php",
            "content": content,
            "excerpt": desc,
        }
        if slug in brand_pages and brand_pages[slug].get("id"):
            pid = brand_pages[slug]["id"]
            _s, page = http_json("POST", f"/wp-json/wp/v2/pages/{pid}", payload)
            brand_pages[slug] = {"id": page["id"], "link": page.get("link") or f"{BASE}/repair-manual/{slug}/"}
            print("updated brand page", slug, pid)
        else:
            # find existing by slug+parent
            _s, found = http_json("GET", f"/wp-json/wp/v2/pages?slug={slug}&parent={PAGE_RM}&_fields=id,link,slug")
            if found:
                pid = found[0]["id"]
                _s, page = http_json("POST", f"/wp-json/wp/v2/pages/{pid}", payload)
            else:
                _s, page = http_json("POST", "/wp-json/wp/v2/pages", payload)
            brand_pages[slug] = {"id": page["id"], "link": page.get("link") or f"{BASE}/repair-manual/{slug}/"}
            print("created brand page", slug, page["id"])
        state["brand_pages"] = brand_pages
        save_state(state)
        time.sleep(0.2)

    return brand_pages, {s: brand_covers[s]["url"] for _, s, _ in BRANDS}, counts


def save_state(state: dict) -> None:
    IFIXIT_STATE.write_text(json.dumps(state, indent=2))


def load_state() -> dict:
    if IFIXIT_STATE.exists():
        return json.loads(IFIXIT_STATE.read_text())
    return {}


def rebuild_iphone16(state: dict) -> None:
    img_state = state.setdefault("iphone16_images", {})
    # ensure guide json present
    for slug, meta in IPHONE16_GUIDES.items():
        path = Path(meta["json"])
        if not path.exists():
            gid = meta["guide_id"]
            req = urllib.request.Request(
                f"https://www.ifixit.com/api/2.0/guides/{gid}",
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
                path.write_text(r.read().decode())
            print("downloaded guide", slug)

        guide = json.loads(path.read_text())
        picked = pick_steps(guide)
        print(slug, "picked steps", len(picked), [p.get("title") for p in picked])

        image_map = img_state.setdefault(slug, {})
        for s in picked:
            sid = str(s.get("stepid"))
            if sid in image_map and image_map[sid].startswith("http"):
                continue
            url = step_image_url(s)
            if not url:
                continue
            title = (s.get("title") or "step").strip()
            fname = f"{slug}-{sid}.jpg"
            alt = f"{meta['title_name']} {title} — FIX4U"
            try:
                src = download_scrub_upload(url, fname, alt)
                image_map[sid] = src
                save_state(state)
                print("  uploaded step img", sid, title[:40])
            except Exception as e:
                print("  img fail", sid, e)

        # cover: first available image or existing featured
        cover = next(iter(image_map.values()), None)
        if not cover:
            cover = f"{BASE}/wp-content/uploads/2026/08/fix4u-hero-professional-repair.jpg"

        article = build_iphone16_article(meta, guide, image_map, cover)
        # splice into existing post shell
        _s, post = http_json("GET", f"/wp-json/wp/v2/posts/{meta['post_id']}?context=edit&_fields=content,featured_media")
        shell = post["content"]["raw"]
        new_shell, n = re.subn(
            r'(?is)<section class="rm-article">[\s\S]*?</section>',
            article,
            shell,
            count=1,
        )
        if n != 1:
            raise RuntimeError(f"article splice failed for {slug}")
        payload = {
            "title": f"{meta['title_name']} Screen Replacement Manual",
            "content": new_shell,
            "excerpt": (
                f"{meta['title_name']} screen replacement manual for FIX4U Auckland — disassembly, "
                f"sensor transfer, install (adhesive + seat screen + pentalobe), and calibration. "
                f"Procedure adapted from iFixit with logo-free photos."
            ),
        }
        http_json("POST", f"/wp-json/wp/v2/posts/{meta['post_id']}", payload)
        # update title in generate state
        gen = json.loads(STATE_PATH.read_text())
        if slug in gen.get("created", {}):
            gen["created"][slug]["title"] = payload["title"]
            STATE_PATH.write_text(json.dumps(gen, indent=2))
        print("updated manual", slug, meta["post_id"])
        time.sleep(0.2)


def main():
    state = load_state()
    log("=== categories ===")
    cats = ensure_categories(state)
    save_state(state)
    log("=== brand pages (before listing rewrite) ===")
    brand_pages, covers, counts = ensure_brand_pages(state)
    log("=== main listing ===")
    update_main_listing(state, brand_pages, covers, counts)
    save_state(state)
    log("=== iphone 16 ifixit rebuild ===")
    rebuild_iphone16(state)
    save_state(state)
    log("=== assign posts to brand cats (best-effort) ===")
    assign_posts_to_brand_cats(state, cats)
    save_state(state)
    log("DONE")


if __name__ == "__main__":
    main()
