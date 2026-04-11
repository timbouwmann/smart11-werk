"""
Smart11 BASE — Advertentie Visual Generator v2
- Gebruikt het echte logo PNG
- Foto's uit brand_assets/foto's/
- Brand-accurate paint splashes (angular/jagged brushstroke style)
- Layout exact op basis van bestaande Smart11 social posts
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os, random

# --- Paths ---
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ASSETS      = os.path.join(os.path.dirname(SCRIPT_DIR), "brand_assets")
FONT_BOLD   = os.path.join(ASSETS, "font", "Poppins-ExtraBold.ttf")
FONT_REG    = os.path.join(ASSETS, "font", "Poppins-Regular.ttf")
LOGO_PATH   = os.path.join(ASSETS, "logo", "T2024010_SMART11_LOGO_WIT_GEEL_RGB (1).png")
PHOTOS      = [os.path.join(ASSETS, "foto's", f)
               for f in ["Smart11_V2-5.jpg","Smart11_V2-6.jpg",
                          "Smart11_V2-7.jpg","Smart11_V2-8.jpg"]]

# --- Brand Colors ---
BG          = (22, 22, 22)
GOLD        = (212, 158, 10)      # exact amber uit logo
RED         = (210, 30, 10)
WHITE       = (255, 255, 255)
GRAY        = (170, 170, 170)
DARK_GRAY   = (60, 60, 60)
COL_L_BG    = (32, 28, 28)
COL_R_BG    = (28, 30, 24)
CTA_FG      = (18, 14, 0)

W, H = 1080, 1350


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


# ── Paint Splash ──────────────────────────────────────────────────────────────

def paint_splash(draw, cx, cy, size, color, seed=1):
    """
    Simulate the angular, jagged brushstroke-style paint splash
    visible in Smart11's brand assets.
    """
    rng = random.Random(seed)
    r, g, b = color

    def blob(ox, oy, rad, pts, alpha, s):
        rng2 = random.Random(s)
        points = []
        for i in range(pts):
            angle = 2 * math.pi * i / pts + rng2.uniform(-0.15, 0.15)
            dist  = rad * rng2.uniform(0.5, 1.0)
            # every 3rd point punches outward for the spiky look
            if i % 3 == 0:
                dist *= rng2.uniform(1.2, 1.6)
            points.append((ox + dist * math.cos(angle),
                            oy + dist * math.sin(angle)))
        draw.polygon(points, fill=(r, g, b, int(255 * alpha)))

    # main splash body
    blob(cx, cy, size,        24, 0.55, seed)
    blob(cx, cy, size * 0.7,  18, 0.35, seed + 1)
    # secondary drips around center
    for i in range(5):
        angle  = rng.uniform(0, 2 * math.pi)
        dist   = size * rng.uniform(0.55, 0.90)
        bx, by = cx + dist * math.cos(angle), cy + dist * math.sin(angle)
        blob(bx, by, size * rng.uniform(0.18, 0.32), 12, 0.30, seed + 10 + i)


# ── Helpers ───────────────────────────────────────────────────────────────────

def wrap(text, fnt, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rounded_rect(draw, x1, y1, x2, y2, r, fill):
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    for ex, ey in [(x1,y1),(x2-2*r,y1),(x1,y2-2*r),(x2-2*r,y2-2*r)]:
        draw.ellipse([ex, ey, ex+2*r, ey+2*r], fill=fill)


def check_icon(draw, cx, cy, rad, color):
    draw.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], fill=color)
    s, w = rad * 0.52, max(2, int(rad * 0.22))
    p = [(cx-s*0.6, cy), (cx-s*0.1, cy+s*0.55), (cx+s*0.65, cy-s*0.55)]
    draw.line([p[0],p[1]], fill=WHITE, width=w)
    draw.line([p[1],p[2]], fill=WHITE, width=w)


def x_icon(draw, cx, cy, rad, color):
    draw.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], fill=color)
    s, w = rad * 0.5, max(2, int(rad * 0.22))
    draw.line([(cx-s, cy-s),(cx+s, cy+s)], fill=WHITE, width=w)
    draw.line([(cx+s, cy-s),(cx-s, cy+s)], fill=WHITE, width=w)


def load_photo(path, target_w, target_h):
    """Load, darken slightly, and crop photo to target size (center-crop)."""
    img = Image.open(path).convert("RGB")
    # maintain aspect ratio, fill target box
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    # center crop
    left = (new_w - target_w) // 2
    top  = (new_h - target_h) // 2
    img  = img.crop((left, top, left + target_w, top + target_h))
    # slight darken for contrast
    img = ImageEnhance.Brightness(img).enhance(0.78)
    return img


def load_logo(target_w):
    """Load logo PNG and scale to target width."""
    logo = Image.open(LOGO_PATH).convert("RGBA")
    ratio = target_w / logo.width
    new_h = int(logo.height * ratio)
    return logo.resize((target_w, new_h), Image.LANCZOS)


# ── Main Generator ────────────────────────────────────────────────────────────

def create_visual(filename,
                  headline_white, headline_gold, subkop,
                  traditional_items, smart11_items, cta_text,
                  photo_left_idx=2, photo_right_idx=3):

    img  = Image.new("RGBA", (W, H), BG + (255,))
    draw = ImageDraw.Draw(img, "RGBA")

    # ── Paint splashes ──
    paint_splash(draw, -40, -40,  210, GOLD, seed=7)
    paint_splash(draw,  60,  50,   90, GOLD, seed=42)
    paint_splash(draw, W+40, H+40, 230, GOLD, seed=13)
    paint_splash(draw, W-60, H-50,  95, GOLD, seed=77)

    # ── Logo (top-center) ──
    logo    = load_logo(220)
    logo_x  = (W - logo.width) // 2
    logo_y  = 38
    img.paste(logo, (logo_x, logo_y), logo)

    # ── Auto-scale headline font ──
    pad     = 56
    max_hw  = W - 2 * pad
    h_size  = 74
    while h_size > 38:
        f_h = font(FONT_BOLD, h_size)
        bw = draw.textbbox((0,0), headline_white, font=f_h)[2]
        bg = draw.textbbox((0,0), headline_gold,  font=f_h)[2]
        if max(bw, bg) <= max_hw:
            break
        h_size -= 2

    f_head = font(FONT_BOLD, h_size)
    f_sub  = font(FONT_REG,  31)
    f_ch   = font(FONT_BOLD, 29)
    f_item = font(FONT_REG,  29)
    f_cta  = font(FONT_BOLD, 28)

    # ── Headline ──
    hy = logo_y + logo.height + 22
    draw.text((pad, hy), headline_white, font=f_head, fill=WHITE)
    b1 = draw.textbbox((pad, hy), headline_white, font=f_head)
    hy2 = b1[3] + 8
    draw.text((pad, hy2), headline_gold, font=f_head, fill=GOLD)
    b2 = draw.textbbox((pad, hy2), headline_gold, font=f_head)

    # ── Subkop ──
    sy = b2[3] + 16
    for line in wrap(subkop, f_sub, max_hw, draw):
        draw.text((pad, sy), line, font=f_sub, fill=GRAY)
        sy = draw.textbbox((pad, sy), line, font=f_sub)[3] + 5

    # ── Photos (side by side) ──
    PHOTO_H = 295
    photo_y = sy + 22
    photo_w = (W - 2 * pad - 12) // 2   # 12px gap

    ph_l = load_photo(PHOTOS[photo_left_idx],  photo_w, PHOTO_H)
    ph_r = load_photo(PHOTOS[photo_right_idx], photo_w, PHOTO_H)

    # convert to RGBA for pasting
    ph_l_rgba = ph_l.convert("RGBA")
    ph_r_rgba = ph_r.convert("RGBA")

    img.paste(ph_l_rgba, (pad, photo_y), ph_l_rgba)
    img.paste(ph_r_rgba, (pad + photo_w + 12, photo_y), ph_r_rgba)

    # thin gold border around photos
    draw.rectangle([pad-2, photo_y-2, pad+photo_w+2, photo_y+PHOTO_H+2],
                   outline=GOLD, width=2)
    draw.rectangle([pad+photo_w+10, photo_y-2,
                    pad+photo_w*2+14, photo_y+PHOTO_H+2],
                   outline=GOLD, width=2)

    # ── Divider ──
    div_y = photo_y + PHOTO_H + 22
    draw.rectangle([pad, div_y, W-pad, div_y+2], fill=DARK_GRAY)

    # ── Two-column comparison ──
    col_top = div_y + 20
    col_w   = (W - 2*pad - 16) // 2
    lx      = pad
    rx      = pad + col_w + 16

    # Subtle column backgrounds
    rounded_rect(draw, lx-8, col_top-8, lx+col_w+8, col_top+310, 10, COL_L_BG)
    rounded_rect(draw, rx-8, col_top-8, rx+col_w+8, col_top+310, 10, COL_R_BG)

    # Column headers
    draw.text((lx+10, col_top+10), "TRADITIONEEL", font=f_ch, fill=GRAY)
    draw.text((rx+10, col_top+10), "SMART 11 BASE", font=f_ch, fill=GOLD)

    bl = draw.textbbox((lx+10, col_top+10), "TRADITIONEEL", font=f_ch)
    br = draw.textbbox((rx+10, col_top+10), "SMART 11 BASE", font=f_ch)
    draw.rectangle([lx+10, bl[3]+4, bl[2], bl[3]+6], fill=DARK_GRAY)
    draw.rectangle([rx+10, br[3]+4, br[2], br[3]+6], fill=GOLD)

    # Items
    iy_l = bl[3] + 20
    iy_r = br[3] + 20
    ir   = 15
    ix   = 42
    mw   = col_w - ix - 10

    for item in traditional_items:
        x_icon(draw, lx+10+ir, iy_l+ir+2, ir, RED)
        ty = iy_l
        for line in wrap(item, f_item, mw, draw):
            draw.text((lx+10+ix, ty), line, font=f_item, fill=WHITE)
            ty = draw.textbbox((lx+10+ix, ty), line, font=f_item)[3] + 4
        iy_l = ty + 16

    for item in smart11_items:
        check_icon(draw, rx+10+ir, iy_r+ir+2, ir, GOLD)
        ty = iy_r
        for line in wrap(item, f_item, mw, draw):
            draw.text((rx+10+ix, ty), line, font=f_item, fill=WHITE)
            ty = draw.textbbox((rx+10+ix, ty), line, font=f_item)[3] + 4
        iy_r = ty + 16

    # ── CTA Button ──
    cta_y  = H - 118
    cta_h  = 68
    rounded_rect(draw, pad, cta_y, W-pad, cta_y+cta_h, 34, GOLD)
    cb = draw.textbbox((0,0), cta_text, font=f_cta)
    ctx = (W - (cb[2]-cb[0])) // 2
    cty = cta_y + (cta_h - (cb[3]-cb[1])) // 2 - 3
    draw.text((ctx, cty), cta_text, font=f_cta, fill=CTA_FG)

    # ── Save ──
    out = img.convert("RGB")
    path = os.path.join(SCRIPT_DIR, filename)
    out.save(path, "PNG", quality=95)
    print(f"OK {filename}")
    return path


# ── Generate all 4 ────────────────────────────────────────────────────────────

create_visual(
    "visual-1-feedback.png",
    headline_white = "JE LEGT HET ELKE WEEK UIT.",
    headline_gold  = "HIJ DOET HET TOCH ANDERS.",
    subkop         = "Verbale feedback verdwijnt. Spelers onthouden wat ze zelf zien.",
    traditional_items = [
        "Feedback uitleggen, hopen dat het landt",
        "Volgende week dezelfde correctie",
        "Speler heeft geen eigenaarschap",
    ],
    smart11_items = [
        "Speler bekijkt zijn eigen beelden",
        "Fout zelf zien = écht begrijpen",
        "Eigenaarschap over eigen ontwikkeling",
    ],
    cta_text        = "LAAT SPELERS ZICHZELF ZIEN — 14 DAGEN GRATIS >",
    photo_left_idx  = 2,   # V2-7 controlling
    photo_right_idx = 3,   # V2-8 running
)

create_visual(
    "visual-2-tijd.png",
    headline_white = "90 MINUTEN.",
    headline_gold  = "KNIPPEN KOST JE DE HELFT.",
    subkop         = "Je tijd is schaars. Verspil hem niet aan technisch gedoe.",
    traditional_items = [
        "Beelden zoeken en knippen: 45 min",
        "Notities schrijven en versturen",
        "Geen tijd voor echte feedback",
    ],
    smart11_items = [
        "Beelden direct in één omgeving",
        "Analyse klaar in 30 minuten",
        "Meer tijd voor training en coaching",
    ],
    cta_text        = "STOP MET KNIPPEN — BEGIN VANDAAG GRATIS >",
    photo_left_idx  = 0,   # V2-5 jumping
    photo_right_idx = 1,   # V2-6 heading
)

create_visual(
    "visual-3-nabespreking.png",
    headline_white = "JE PRAAT.",
    headline_gold  = "ZE KNIKKEN. ZATERDAG VERGETEN.",
    subkop         = "20 minuten praten werkt niet. Spelers leren van wat ze zelf zien.",
    traditional_items = [
        "Coach praat, spelers luisteren passief",
        "Feedback verdwijnt na 48 uur",
        "Nabespreking = één richting",
    ],
    smart11_items = [
        "Spelers zien hun eigen beelden",
        "Persoonlijke clips blijven hangen",
        "Nabespreking wordt een gesprek",
    ],
    cta_text        = "GEEF FEEDBACK DIE ÉCHT BEKLIJFT — 14 DAGEN GRATIS >",
    photo_left_idx  = 2,   # V2-7
    photo_right_idx = 1,   # V2-6
)

create_visual(
    "visual-4-losse-clips.png",
    headline_white = "LOSSE CLIPS. LOSSE CHATS.",
    headline_gold  = "NERGENS EEN LIJN.",
    subkop         = "Je werkt hard. Maar zonder structuur gaat al die tijd verloren.",
    traditional_items = [
        "Video's verspreid via WhatsApp en mail",
        "Feedback zonder opvolging",
        "Geen overzicht wie écht groeit",
    ],
    smart11_items = [
        "Één omgeving voor video, feedback en thema's",
        "Opvolging per speler bijgehouden",
        "Direct zien wie zich ontwikkelt",
    ],
    cta_text        = "ALLES IN ÉÉN TEAMOMGEVING — 14 DAGEN GRATIS >",
    photo_left_idx  = 0,   # V2-5
    photo_right_idx = 3,   # V2-8
)

print("\nKlaar — 4 visuals gegenereerd.")
