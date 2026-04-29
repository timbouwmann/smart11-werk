"""
build_divi_homepage.py
Genereert een Divi shortcode + JSON voor de Smart11 homepage (homepage-new.html).
Elke sectie van de pagina wordt een echte et_pb_section — bewerkbaar via Divi builder.
"""

import json, base64

V = '_builder_version="4.27.0"'
GOLD = "#DC9600"
DARK = "#0d0d0d"
CARD = "#111111"
TEXT_SEC = "#888888"
FONT = 'Poppins||||||||'

# ── Divi bouw-blokken ───────────────────────────────────────────────────────

def sec(content, bg=DARK, pad="80px||80px||false|false", extra=""):
    return (
        f'[et_pb_section fb_built="1" {V} background_color="{bg}" '
        f'custom_padding="{pad}" {extra}]'
        f'{content}'
        f'[/et_pb_section]'
    )

def row(content, pad="0px||0px||false|false", extra=""):
    return (
        f'[et_pb_row {V} width="100%" max_width="1200px" '
        f'custom_padding="{pad}" column_structure="4_4" {extra}]'
        f'{content}'
        f'[/et_pb_row]'
    )

def row_fullwidth(content, pad="0px||0px||false|false", extra=""):
    """Row zonder max-width beperking — voor code-modules die volle breedte nodig hebben."""
    return (
        f'[et_pb_row {V} width="100%" max_width="100%" make_fullwidth="on" '
        f'custom_padding="{pad}" column_structure="4_4" {extra}]'
        f'{content}'
        f'[/et_pb_row]'
    )

def row_cols(content, structure="1_3,1_3,1_3", pad="0px||0px||false|false", extra=""):
    return (
        f'[et_pb_row {V} width="100%" max_width="1200px" '
        f'custom_padding="{pad}" column_structure="{structure}" {extra}]'
        f'{content}'
        f'[/et_pb_row]'
    )

def col(content, t="4_4", extra=""):
    return f'[et_pb_column type="{t}" {V} {extra}]{content}[/et_pb_column]'

def txt(html, pad="0px||0px||false|false", extra=""):
    return (
        f'[et_pb_text {V} text_font="{FONT}" text_text_color="#FFFFFF" '
        f'custom_padding="{pad}" {extra}]'
        f'{html}'
        f'[/et_pb_text]'
    )

def btn(label, url="#", align="left", extra=""):
    return (
        f'[et_pb_button button_url="{url}" button_text="{label}" '
        f'button_alignment="{align}" custom_button="on" '
        f'button_bg_color="{GOLD}" button_text_color="#000000" '
        f'button_font="Poppins|800|||||||" button_text_size="15px" '
        f'button_border_width="0px" button_border_radius="10px" '
        f'button_letter_spacing="0px" button_use_icon="off" {V} {extra}]'
        f'[/et_pb_button]'
    )

def btn_outline(label, url="#", align="left", extra=""):
    return (
        f'[et_pb_button button_url="{url}" button_text="{label}" '
        f'button_alignment="{align}" custom_button="on" '
        f'button_bg_color="rgba(255,255,255,0.04)" button_text_color="#FFFFFF" '
        f'button_font="Poppins|600|||||||" button_text_size="15px" '
        f'button_border_width="1px" button_border_color="rgba(255,255,255,0.15)" '
        f'button_border_radius="10px" button_use_icon="off" {V} {extra}]'
        f'[/et_pb_button]'
    )

def code(html):
    return f'[et_pb_code {V}]{html}[/et_pb_code]'

def tag(label):
    return (
        f'<p style="font-size:11px;font-weight:800;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:{GOLD};margin:0 0 14px;">{label}</p>'
    )

def h2(text):
    return (
        f'<h2 style="font-size:clamp(30px,4vw,46px);font-weight:900;font-style:italic;'
        f'line-height:1.08;letter-spacing:-0.025em;color:#fff;margin:0 0 16px;">'
        f'{text}</h2>'
    )

def lead(text, max_w="580px"):
    return (
        f'<p style="font-size:17px;color:{TEXT_SEC};line-height:1.75;'
        f'max-width:{max_w};margin:0;">{text}</p>'
    )

# ── 0. Fonts + Global CSS ───────────────────────────────────────────────────
# WordPress strips <style> tags from et_pb_code content — inject via JS instead.
# CSS is base64-encoded so no quoting/escaping issues.

_RAW_CSS = (
    ":root{--gold:#DC9600;--gold-light:#F0AB14;--bg-darkest:#000;--bg-card:#111111;--text-secondary:#888888;}"
    "body{font-family:'Poppins',sans-serif!important;}"

    # Hero
    ".s11-hero-escape{width:100vw;position:relative;left:50%;transform:translateX(-50%);}"
    ".s11-hero{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:100px 24px 60px;overflow:hidden;text-align:center;}"
    ".s11-hero video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;}"
    ".s11-hero-overlay{position:absolute;inset:0;z-index:1;background:linear-gradient(to bottom,rgba(0,0,0,.72) 0%,rgba(0,0,0,.55) 40%,rgba(0,0,0,.75) 75%,rgba(0,0,0,.97) 100%);}"
    ".s11-hero-glow{position:absolute;inset:0;z-index:1;background:radial-gradient(ellipse 70% 45% at 50% 20%,rgba(220,150,0,.18) 0%,transparent 60%);}"
    ".s11-hero-inner{position:relative;z-index:2;max-width:900px;width:100%;}"
    ".s11-badge{display:inline-flex;align-items:center;gap:8px;padding:5px 16px;margin-bottom:28px;background:#DC9600;border-radius:3px;font-size:11px;font-weight:800;color:#000;letter-spacing:.1em;text-transform:uppercase;font-style:italic;}"
    ".s11-h1{font-size:clamp(44px,7.5vw,92px);font-weight:900;line-height:1.02;letter-spacing:-.03em;font-style:italic;color:#fff;margin:0 0 22px;}"
    ".s11-h1 em{color:#DC9600;font-style:normal;}"
    ".s11-sub{font-size:clamp(15px,1.8vw,18px);color:rgba(255,255,255,.65);line-height:1.75;max-width:560px;margin:0 auto 48px;}"
    ".s11-segs{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:840px;margin:0 auto;}"
    ".s11-seg{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);backdrop-filter:blur(16px);border-radius:16px;padding:26px 22px;text-align:left;text-decoration:none;}"
    ".s11-seg:hover{border-color:rgba(220,150,0,.4);}"
    ".s11-seg-icon{width:42px;height:42px;border-radius:10px;background:rgba(220,150,0,.12);border:1px solid rgba(220,150,0,.22);display:flex;align-items:center;justify-content:center;margin-bottom:16px;}"
    ".s11-seg-lbl{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#DC9600;margin-bottom:6px;}"
    ".s11-seg-title{font-size:17px;font-weight:700;color:#fff;margin-bottom:6px;line-height:1.3;}"
    ".s11-seg-desc{font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;margin-bottom:18px;}"
    ".s11-seg-link{font-size:13px;font-weight:700;color:#DC9600;}"
    "@media(max-width:640px){.s11-segs{grid-template-columns:1fr;}}"

    # Gradient cards
    ".gc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;}"
    ".gc{position:relative;border-radius:20px;overflow:hidden;padding:36px;display:flex;flex-direction:column;min-height:400px;border:1px solid transparent;transition:transform .28s ease,box-shadow .28s ease;}"
    ".gc:hover{transform:translateY(-4px) scale(1.02);box-shadow:0 24px 60px rgba(0,0,0,.5);}"
    ".gc--speler{background:linear-gradient(135deg,#1e1100 0%,#111111 65%);border-color:rgba(220,150,0,.2);}"
    ".gc--coach{background:linear-gradient(135deg,#090f1e 0%,#111111 65%);border-color:rgba(59,130,246,.2);}"
    ".gc--club{background:linear-gradient(135deg,#071610 0%,#111111 65%);border-color:rgba(16,185,129,.2);}"
    ".gc-deco{position:absolute;bottom:-12%;right:-8%;width:68%;pointer-events:none;object-fit:cover;opacity:.18;border-radius:12px;transition:transform .38s ease,opacity .38s ease;}"
    ".gc:hover .gc-deco{transform:scale(1.09) rotate(3deg);opacity:.28;}"
    ".gc-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:100px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.1);font-size:12px;font-weight:700;color:rgba(255,255,255,.8);margin-bottom:24px;width:fit-content;}"
    ".gc-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}"
    ".gc-title{font-size:24px;font-weight:900;font-style:italic;color:#fff;line-height:1.2;margin:0 0 8px;}"
    ".gc-desc{font-size:14px;color:rgba(255,255,255,.5);line-height:1.6;margin:0 0 24px;}"
    ".gc-products{display:flex;flex-direction:column;gap:8px;flex:1;margin-bottom:32px;}"
    ".gc-product{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:rgba(255,255,255,.85);}"
    ".gc-pdot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}"
    ".gc-cta{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;color:rgba(255,255,255,.9);text-decoration:none;margin-top:auto;position:relative;z-index:1;}"
    ".gc-cta svg{transition:transform .25s ease;}"
    ".gc-cta:hover{color:#DC9600;}"
    ".gc-cta:hover svg{transform:translateX(4px);}"
    "@media(max-width:900px){.gc-grid{grid-template-columns:1fr;}.gc{min-height:auto;}}"

    # News carousel
    ".nc-carousel{overflow:hidden;margin-bottom:28px;}"
    ".nc-track{display:flex;gap:20px;transition:transform .42s cubic-bezier(.25,.46,.45,.94);}"
    ".nc-card{position:relative;border-radius:16px;overflow:hidden;text-decoration:none;display:block;min-height:300px;flex:0 0 calc((100% - 40px)/3);}"
    ".nc-card:hover{transform:translateY(-3px);}"
    ".nc-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}"
    ".nc-overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.94) 0%,rgba(0,0,0,.55) 55%,rgba(0,0,0,.12) 100%);}"
    ".nc-content{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:22px;}"
    ".nc-meta{font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:8px;}"
    ".nc-title{font-size:16px;font-weight:800;color:#fff;line-height:1.38;margin-bottom:14px;}"
    ".nc-footer{display:flex;align-items:flex-end;justify-content:space-between;gap:8px;}"
    ".nc-date{font-size:12px;font-weight:600;color:rgba(255,255,255,.45);}"
    ".nc-arrow{width:34px;height:34px;border-radius:50%;background:#DC9600;display:flex;align-items:center;justify-content:center;flex-shrink:0;}"
    ".nc-controls{display:flex;align-items:center;justify-content:center;gap:16px;}"
    ".nc-nav{width:38px;height:38px;border-radius:50%;border:1px solid rgba(255,255,255,.08);background:#111;color:#888;display:flex;align-items:center;justify-content:center;cursor:pointer;}"
    ".nc-nav:hover:not(:disabled){border-color:#DC9600;color:#DC9600;}"
    ".nc-nav:disabled{opacity:.3;cursor:default;}"
    ".nc-dots{display:flex;gap:8px;align-items:center;}"
    ".nc-dot{width:8px;height:8px;border-radius:50%;border:none;background:rgba(255,255,255,.18);cursor:pointer;padding:0;}"
    ".nc-dot.active{background:#DC9600;width:22px;border-radius:4px;}"
    "@media(max-width:900px){.nc-card{flex:0 0 calc((100% - 20px)/2);}}"
    "@media(max-width:640px){.nc-card{flex:0 0 100%;}}"

    # Newsletter form
    ".nl-form{display:flex;flex-direction:column;gap:14px;}"
    ".nl-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;}"
    ".nl-input{padding:13px 18px;font-size:14px;font-weight:500;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:10px;color:#fff;font-family:'Poppins',sans-serif;outline:none;width:100%;box-sizing:border-box;}"
    ".nl-input::placeholder{color:#888;}"
    ".nl-input:focus{border-color:rgba(220,150,0,.4);background:rgba(220,150,0,.05);}"
    ".nl-select{padding:13px 18px;font-size:14px;font-weight:500;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:10px;color:#888;font-family:'Poppins',sans-serif;outline:none;width:100%;appearance:none;cursor:pointer;}"
    ".nl-btn{padding:14px 24px;font-size:14px;font-weight:700;color:#000;background:#DC9600;border:none;border-radius:10px;cursor:pointer;font-family:'Poppins',sans-serif;box-shadow:0 6px 20px rgba(220,150,0,.28);}"
    ".nl-btn:hover{background:#F0AB14;}"
    ".nl-note{font-size:12px;color:rgba(255,255,255,.25);text-align:center;}"
    "@media(max-width:600px){.nl-row{grid-template-columns:1fr;}}"
)

_CSS_B64 = base64.b64encode(_RAW_CSS.encode("utf-8")).decode("ascii")

GLOBAL_CSS = (
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">'
    '<script>(function(){'
    'if(document.getElementById("s11css"))return;'
    f'var s=document.createElement("style");s.id="s11css";s.textContent=atob("{_CSS_B64}");'
    'document.head.appendChild(s);'
    '})();</script>'
)

fonts_sec = sec(
    row(col(code(GLOBAL_CSS))),
    pad="0px||0px||false|false"
)

# ── 1. Hero ─────────────────────────────────────────────────────────────────

hero_html = """<div class="s11-hero-escape"><div class="s11-hero">
  <video autoplay muted loop playsinline>
    <source src="/wp-content/uploads/smart11/Frame-1.mp4" type="video/mp4" />
  </video>
  <div class="s11-hero-overlay"></div>
  <div class="s11-hero-glow"></div>
  <div class="s11-hero-inner">
    <div class="s11-badge">
      <svg width="8" height="8" viewBox="0 0 8 8"><circle cx="4" cy="4" r="4" fill="currentColor"/></svg>
      Het analyse-platform voor voetbal
    </div>
    <h1 class="s11-h1">Verhoog je <em>voetbal&shy;intelligentie</em></h1>
    <p class="s11-sub">Smart11 geeft spelers, coaches én clubs de analyse-software en voetbalkennis om écht beter te worden. Van JO15 tot reserve-elftal.</p>
    <div class="s11-segs">
      <a href="#speler" class="s11-seg">
        <div class="s11-seg-icon"><svg width="20" height="20" fill="none" stroke="#DC9600" stroke-width="2" stroke-linecap="round" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M6 20v-2a6 6 0 0 1 12 0v2"/></svg></div>
        <div class="s11-seg-lbl">Ik ben speler</div>
        <div class="s11-seg-title">Analyseer je eigen spel</div>
        <div class="s11-seg-desc">Volg je Game Actions, begrijp je keuzes en zie je groei per wedstrijd.</div>
        <span class="s11-seg-link">Ontdek de app -&gt;</span>
      </a>
      <a href="#coach" class="s11-seg">
        <div class="s11-seg-icon"><svg width="20" height="20" fill="none" stroke="#DC9600" stroke-width="2" stroke-linecap="round" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9l6 6M15 9l-6 6"/></svg></div>
        <div class="s11-seg-lbl">Ik ben coach</div>
        <div class="s11-seg-title">Analyseer sneller, coach beter</div>
        <div class="s11-seg-desc">AI-videoanalyse en spelersfeedback — klaar vóór de volgende training.</div>
        <span class="s11-seg-link">Ontdek SmartCoach -&gt;</span>
      </a>
      <a href="#club" class="s11-seg">
        <div class="s11-seg-icon"><svg width="20" height="20" fill="none" stroke="#DC9600" stroke-width="2" stroke-linecap="round" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div>
        <div class="s11-seg-lbl">Ik ben club</div>
        <div class="s11-seg-title">Eén platform voor de hele club</div>
        <div class="s11-seg-desc">Coaches én spelers op één plek. Schaalbaar van 1 team naar de hele selectie.</div>
        <span class="s11-seg-link">Bekijk Smart11 BASE -&gt;</span>
      </a>
    </div>
  </div>
</div>"""

hero_sec = sec(
    row_fullwidth(col(code(hero_html)), pad="0px||0px||false|false"),
    bg="#000000", pad="0px||0px||false|false"
)

# ── 2. Stats bar ────────────────────────────────────────────────────────────

def stat_col(number, label):
    return col(
        txt(
            f'<div style="text-align:center;padding:36px 16px;">'
            f'<p style="font-size:clamp(30px,3.5vw,44px);font-weight:900;font-style:italic;'
            f'letter-spacing:-.03em;color:{GOLD};line-height:1;margin:0 0 8px;">{number}</p>'
            f'<p style="font-size:13px;font-weight:600;color:{TEXT_SEC};margin:0;line-height:1.4;">{label}</p>'
            f'</div>'
        ),
        "1_4"
    )

stats_sec = sec(
    row_cols(
        stat_col("3.500+", "App-gebruikers") +
        stat_col("200+", "Professionele spelers begeleid") +
        col(
            txt(
                '<div style="text-align:center;padding:36px 16px;">'
                f'<div style="display:inline-flex;align-items:center;gap:8px;padding:6px 14px;'
                f'background:rgba(220,150,0,0.1);border:1px solid rgba(220,150,0,0.2);'
                f'border-radius:6px;font-size:13px;font-weight:700;color:{GOLD};margin-bottom:8px;">'
                f'&#9733; Partner van de KNVB</div>'
                f'<p style="font-size:13px;font-weight:600;color:{TEXT_SEC};margin:0;">Officieel erkend</p>'
                f'</div>'
            ),
            "1_4"
        ) +
        stat_col("1,2M+", "Minuten wedstrijdvideo geanalyseerd"),
        structure="1_4,1_4,1_4,1_4"
    ),
    bg=CARD, pad="0px||0px||false|false",
    extra='border_width_top="1px" border_color_top="rgba(255,255,255,0.08)" border_width_bottom="1px" border_color_bottom="rgba(255,255,255,0.08)"'
)

# ── 3. Wat Smart11 biedt — gradient cards ───────────────────────────────────

gradient_cards_html = """<div class="gc-grid">
  <div class="gc gc--speler" id="speler">
    <img src="/wp-content/uploads/smart11/Smart11_V2-5.jpg" class="gc-deco" alt="" />
    <div class="gc-badge"><span class="gc-dot" style="background:#DC9600;"></span>Ik ben speler</div>
    <h3 class="gc-title">Analyseer je eigen spel</h3>
    <p class="gc-desc">Volg je Game Actions per wedstrijd. Zie je keuzes, begrijp je uitvoering en groei elke week.</p>
    <div class="gc-products">
      <div class="gc-product"><span class="gc-pdot" style="background:#DC9600;"></span>Smart11 App — gratis &amp; Pro</div>
      <div class="gc-product"><span class="gc-pdot" style="background:#DC9600;"></span>Clairence — AI-analyst voor jouw momenten</div>
    </div>
    <a href="#" class="gc-cta">Ontdek de app <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
  </div>
  <div class="gc gc--coach" id="coach">
    <img src="/wp-content/uploads/smart11/Smartcoach-laptop.jpg" class="gc-deco" alt="" />
    <div class="gc-badge"><span class="gc-dot" style="background:#3b82f6;"></span>Ik ben coach</div>
    <h3 class="gc-title">Analyseer sneller, coach beter</h3>
    <p class="gc-desc">AI-videoanalyse en spelersfeedback — klaar vóór de volgende training. Minder nabespreken, meer impact.</p>
    <div class="gc-products">
      <div class="gc-product"><span class="gc-pdot" style="background:#3b82f6;"></span>SmartCoach — voor de individuele coach</div>
      <div class="gc-product"><span class="gc-pdot" style="background:#3b82f6;"></span>Smart11 BASE — volledige teamomgeving</div>
      <div class="gc-product"><span class="gc-pdot" style="background:#3b82f6;"></span>Clairence — samenvattingen per speler in 5 min</div>
    </div>
    <a href="#" class="gc-cta">Ontdek SmartCoach <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
  </div>
  <div class="gc gc--club" id="club">
    <img src="/wp-content/uploads/smart11/Smart11_V2-7.jpg" class="gc-deco" alt="" />
    <div class="gc-badge"><span class="gc-dot" style="background:#10b981;"></span>Ik ben club</div>
    <h3 class="gc-title">Eén platform voor de hele club</h3>
    <p class="gc-desc">Schaalbaar van 1 team naar de volledige selectie. Coaches én spelers op één plek.</p>
    <div class="gc-products">
      <div class="gc-product"><span class="gc-pdot" style="background:#10b981;"></span>Smart11 BASE — centraal clubplatform</div>
      <div class="gc-product"><span class="gc-pdot" style="background:#10b981;"></span>Smart11 Team — analyse per team</div>
      <div class="gc-product"><span class="gc-pdot" style="background:#10b981;"></span>Smart11 Club — voor alle selectieteams</div>
    </div>
    <a href="#" class="gc-cta">Bekijk Smart11 BASE <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
  </div>
</div>"""

tools_header = txt(
    tag("Wat Smart11 biedt") +
    h2("Tools voor <em style='color:#DC9600;font-style:normal;'>elke rol</em>") +
    lead("Van speler tot club — Smart11 heeft voor elke doelgroep de juiste tools om slimmer te worden."),
    pad="0px||48px||false|false"
)

tools_sec = sec(
    row(col(tools_header)) +
    row(col(code(gradient_cards_html))),
    pad="80px||80px||false|false"
)

# ── 4. Voetbalkennis ────────────────────────────────────────────────────────

kennis_sec = sec(
    row_cols(
        col(
            txt(
                tag("Voetbalkennis") +
                h2("Next-level <em style='color:#DC9600;font-style:normal;'>voetbalkennis</em>") +
                lead("Leer van de beste coaches in Nederland. Tactische cursussen en masterclasses die je direct kunt toepassen.") +
                f'<ul style="margin:28px 0 32px;padding:0;list-style:none;display:flex;flex-direction:column;gap:12px;">'
                f'<li style="display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:#fff;"><span style="width:6px;height:6px;border-radius:50%;background:{GOLD};flex-shrink:0;"></span>Smart11 community — cursussen voor coaches &amp; spelers</li>'
                f'<li style="display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:#fff;"><span style="width:6px;height:6px;border-radius:50%;background:{GOLD};flex-shrink:0;"></span>Videobibliotheek — praktijkvoorbeelden uit het veld</li>'
                f'<li style="display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:#fff;"><span style="width:6px;height:6px;border-radius:50%;background:{GOLD};flex-shrink:0;"></span>Smart11 methode — compleet cursuspakket voor coaches <em style="color:{GOLD};">volgens de bewezen Smart11 methode</em></li>'
                f'<li style="display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:#fff;"><span style="width:6px;height:6px;border-radius:50%;background:{GOLD};flex-shrink:0;"></span>Masterclasses — tactische verdieping</li>'
                f'</ul>',
                pad="0px||0px||false|false"
            ) +
            btn_outline("Bekijk het aanbod -&gt;", "#"),
            "1_2"
        ) +
        col(
            f'[et_pb_image src="/wp-content/uploads/smart11/cursus-voetbal-coach.jpg" '
            f'alt="Smart11 voetbalkennis" border_radii="on|16px|16px|16px|16px" {V}]'
            f'[/et_pb_image]',
            "1_2"
        ),
        structure="1_2,1_2",
        pad="0px||0px||false|false"
    ),
    pad="80px||80px||false|false"
)

# ── 5. Hoe het werkt ────────────────────────────────────────────────────────

def step_col(num, title, desc, t="1_3"):
    return col(
        txt(
            f'<div style="background:{CARD};padding:36px 32px;height:100%;">'
            f'<div style="font-size:56px;font-weight:900;font-style:italic;color:rgba(220,150,0,0.14);line-height:1;margin-bottom:20px;">{num}</div>'
            f'<h3 style="font-size:17px;font-weight:700;color:#fff;margin:0 0 10px;line-height:1.35;">{title}</h3>'
            f'<p style="font-size:14px;color:{TEXT_SEC};line-height:1.65;margin:0;">{desc}</p>'
            f'</div>'
        ),
        t
    )

steps_sec = sec(
    row(col(
        txt(
            tag("Hoe het werkt") +
            h2("Van wedstrijd naar <em style='color:#DC9600;font-style:normal;'>verbetering</em>"),
            pad="0px||48px||false|false"
        )
    )) +
    row_cols(
        step_col("01", "Analyseer de wedstrijd met AI",
                 "Upload je wedstrijdvideo. Smart11 identificeert automatisch alle Game Actions — keuzes én uitvoeringen van elke speler.") +
        step_col("02", "Geef spelers directe feedback",
                 "Koppel analyses aan individuele spelers. Zij zien hun eigen momenten, leren van hun keuzes en nemen ownership over hun eigen groei.") +
        step_col("03", "Zie verbetering binnen 2 weken",
                 "Coaches zien al na één trainingsweek dat spelers bewuster spelen. Minder herhalen, meer toepassen — zo werkt echte voetbalintelligentie."),
        structure="1_3,1_3,1_3",
        extra='border_radii="on|16px|16px|16px|16px"'
    ),
    pad="80px||80px||false|false"
)

# ── 6. Nieuws carousel ──────────────────────────────────────────────────────

news_carousel_html = """<div class="nc-carousel"><div class="nc-track" id="ncTrack">
  <a href="https://smart11.ai/en/individuele-videoanalyse-in-het-amateurvoetbal/" class="nc-card" target="_blank">
    <img src="/wp-content/uploads/smart11/videoanalyse-voetbal-ai.jpg" class="nc-bg" alt="" />
    <div class="nc-overlay"></div>
    <div class="nc-content">
      <div class="nc-meta">Voetbalintelligentie</div>
      <div class="nc-title">Individuele ontwikkeling met behulp van videobeelden in het amateurvoetbal</div>
      <div class="nc-footer"><span class="nc-date">1 apr 2026</span><div class="nc-arrow"><svg width="14" height="14" fill="none" stroke="#000" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div></div>
    </div>
  </a>
  <a href="https://smart11.ai/en/van-moeten-naar-willen-hoe-je-spelers-eigenaar-maakt-van-hun-eigen-groei/" class="nc-card" target="_blank">
    <img src="/wp-content/uploads/smart11/Smart11_V2-5.jpg" class="nc-bg" alt="" />
    <div class="nc-overlay"></div>
    <div class="nc-content">
      <div class="nc-meta">Voetbalintelligentie</div>
      <div class="nc-title">Van 'moeten' naar 'willen': hoe je spelers eigenaar maakt van hun eigen groei</div>
      <div class="nc-footer"><span class="nc-date">16 mrt 2026</span><div class="nc-arrow"><svg width="14" height="14" fill="none" stroke="#000" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div></div>
    </div>
  </a>
  <a href="https://smart11.ai/en/eigenaarschap-en-zelfregulatie-bij-fc-twente-heracles-academie/" class="nc-card" target="_blank">
    <img src="/wp-content/uploads/smart11/Smart11_V2-7.jpg" class="nc-bg" alt="" />
    <div class="nc-overlay"></div>
    <div class="nc-content">
      <div class="nc-meta">Use Cases</div>
      <div class="nc-title">Eigenaarschap en zelfregulatie bij FC Twente/Heracles Academie</div>
      <div class="nc-footer"><span class="nc-date">15 jan 2026</span><div class="nc-arrow"><svg width="14" height="14" fill="none" stroke="#000" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div></div>
    </div>
  </a>
  <a href="https://smart11.ai/en/individuele-analyse-voetbal-bouw-een-vaste-structuur/" class="nc-card" target="_blank">
    <img src="/wp-content/uploads/smart11/Smart11_V2-8.jpg" class="nc-bg" alt="" />
    <div class="nc-overlay"></div>
    <div class="nc-content">
      <div class="nc-meta">Voetbalintelligentie</div>
      <div class="nc-title">Zo bouw je een vaste structuur voor individuele analyse zonder dat het je uren kost</div>
      <div class="nc-footer"><span class="nc-date">4 mrt 2026</span><div class="nc-arrow"><svg width="14" height="14" fill="none" stroke="#000" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div></div>
    </div>
  </a>
  <a href="https://smart11.ai/en/van-theorie-naar-praktijk-ons-sneek-stoomt-jeugdtrainers-klaar-dankzij-smart11/" class="nc-card" target="_blank">
    <img src="/wp-content/uploads/smart11/rtc-niek.jpg" class="nc-bg" alt="" />
    <div class="nc-overlay"></div>
    <div class="nc-content">
      <div class="nc-meta">Use Cases</div>
      <div class="nc-title">Van theorie naar praktijk: ONS Sneek stoomt jeugdtrainers klaar dankzij Smart11</div>
      <div class="nc-footer"><span class="nc-date">18 feb 2026</span><div class="nc-arrow"><svg width="14" height="14" fill="none" stroke="#000" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div></div>
    </div>
  </a>
  <a href="https://smart11.ai/en/clairence-is-now-live/" class="nc-card" target="_blank">
    <img src="/wp-content/uploads/smart11/Smartcoach-laptop.jpg" class="nc-bg" alt="" />
    <div class="nc-overlay"></div>
    <div class="nc-content">
      <div class="nc-meta">Smart11 Tips</div>
      <div class="nc-title">Clairence: Smart11's volledig geïntegreerde AI-analyst is nu LIVE!</div>
      <div class="nc-footer"><span class="nc-date">15 dec 2025</span><div class="nc-arrow"><svg width="14" height="14" fill="none" stroke="#000" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div></div>
    </div>
  </a>
</div></div>
<div class="nc-controls">
  <button class="nc-nav" id="ncPrev"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M19 12H5M12 19l-7-7 7-7"/></svg></button>
  <div class="nc-dots" id="ncDots"></div>
  <button class="nc-nav" id="ncNext"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></button>
</div>
<script>
(function(){
  var track=document.getElementById('ncTrack'),cards=track.querySelectorAll('.nc-card'),
  dotsEl=document.getElementById('ncDots'),prev=document.getElementById('ncPrev'),
  next=document.getElementById('ncNext'),total=cards.length,vis=3,cur=0;
  function gv(){return window.innerWidth<640?1:window.innerWidth<900?2:3;}
  function pages(){return Math.ceil(total/vis);}
  function buildDots(){dotsEl.innerHTML='';for(var i=0;i<pages();i++){var d=document.createElement('button');d.className='nc-dot'+(i===cur?' active':'');(function(i){d.addEventListener('click',function(){goTo(i);})})(i);dotsEl.appendChild(d);}}
  function goTo(idx){cur=Math.max(0,Math.min(idx,pages()-1));var gap=20,cw=track.parentElement.offsetWidth/vis-gap*(vis-1)/vis,off=cur*(cw+gap)*vis;track.style.transform='translateX(-'+off+'px)';dotsEl.querySelectorAll('.nc-dot').forEach(function(d,i){d.classList.toggle('active',i===cur);});prev.disabled=cur===0;next.disabled=cur>=pages()-1;}
  function init(){vis=gv();buildDots();goTo(0);}
  prev.addEventListener('click',function(){goTo(cur-1);});
  next.addEventListener('click',function(){goTo(cur+1);});
  window.addEventListener('resize',init);
  init();
})();
</script>"""

_news_h2 = h2('Leer van de <em style="color:#DC9600;font-style:normal;">beste coaches</em>')
news_header_txt = txt(
    '<div style="display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:24px;">'
    '<div>' + tag("Voetbalintelligentie") + _news_h2 + '</div>'
    '<a href="https://smart11.ai/en/blog/" target="_blank" style="display:inline-flex;align-items:center;gap:8px;padding:10px 22px;font-size:13px;font-weight:600;color:#fff;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:10px;text-decoration:none;white-space:nowrap;">Alle artikelen &#8594;</a>'
    '</div>'
    f'<p style="font-size:17px;color:{TEXT_SEC};line-height:1.75;max-width:560px;margin:16px 0 0;">Gratis kennis die je direct op de training kunt toepassen. Elke week nieuw.</p>',
    pad="0px||48px||false|false"
)

news_sec = sec(
    row(col(news_header_txt)) +
    row(col(code(news_carousel_html))),
    pad="80px||80px||false|false"
)

# ── 7. Testimonials ─────────────────────────────────────────────────────────

def t_card(initial, quote, name, role, badge, t="1_3"):
    return col(
        txt(
            f'<div style="background:{CARD};border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:32px 28px;height:100%;">'
            f'<div style="color:{GOLD};font-size:14px;margin-bottom:16px;letter-spacing:2px;">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
            f'<p style="font-size:15px;color:#fff;line-height:1.7;margin-bottom:24px;font-style:italic;">&ldquo;{quote}&rdquo;</p>'
            f'<div style="display:flex;align-items:center;gap:14px;">'
            f'<div style="width:44px;height:44px;border-radius:50%;background:rgba(220,150,0,.15);border:2px solid rgba(220,150,0,.3);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;font-weight:800;color:{GOLD};">{initial}</div>'
            f'<div>'
            f'<div style="font-size:14px;font-weight:700;color:#fff;">{name}</div>'
            f'<div style="font-size:12px;color:{TEXT_SEC};">{role}</div>'
            f'<span style="display:inline-block;margin-top:4px;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:{GOLD};background:rgba(220,150,0,.1);border-radius:4px;padding:2px 8px;">{badge}</span>'
            f'</div></div></div>'
        ),
        t
    )

reviews_sec = sec(
    row(col(
        txt(
            f'<div style="text-align:center;">'
            + tag("Resultaten")
            + h2("Wat coaches en clubs <em style='color:#DC9600;font-style:normal;'>zeggen</em>")
            + '</div>',
            pad="0px||48px||false|false"
        )
    )) +
    row_cols(
        t_card("A", "Smart11 scherpt het bewustzijn van spelers aan. Ze zien een niveau van detail dat anderen simpelweg niet zien.",
               "Alex van der Veen", "Eigenaar — VEENS Voetbal Academie", "Speler &amp; Coach") +
        t_card("F", "Smart11 stimuleert zelfregulatie bij spelers — ze kijken vaker zelfstandig wedstrijdbeelden terug. Precies wat wij willen zien.",
               "Fedrik Houtstra", "Head of Academy — SC Cambuur", "Coach") +
        t_card("Y", "Smart11 geeft spelers krachtige tools om nieuwe inzichten te ontdekken en concrete vervolgstappen te zetten in hun ontwikkeling.",
               "Youri Geurkink", "Coordinator Performance &amp; Science — FC Twente/Heracles Academie", "Club"),
        structure="1_3,1_3,1_3"
    ),
    pad="80px||80px||false|false"
)

# ── 8. Congres ──────────────────────────────────────────────────────────────

congres_sec = sec(
    row_cols(
        col(
            txt(
                tag("Evenement") +
                h2("Smart11 <em style='color:#DC9600;font-style:normal;'>Congres 2026</em>") +
                f'<div style="display:inline-flex;align-items:center;gap:8px;padding:6px 14px;margin:24px 0;background:rgba(220,150,0,.12);border:1px solid rgba(220,150,0,.2);border-radius:6px;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:{GOLD};">&#128197; 30 september 2026</div>' +
                f'<p style="font-size:15px;color:{TEXT_SEC};line-height:1.7;margin:0 0 20px;">Het Smart11 Congres brengt de meest ambitieuze coaches en technisch directeuren van Nederland samen. Tactische sessies, live demo\'s en netwerken op het hoogste niveau.</p>' +
                f'<p style="font-size:14px;font-weight:600;color:rgba(255,255,255,.75);margin:0 0 8px;">&#128205; MAC³PARK Stadion — PEC Zwolle, Zwolle</p>' +
                f'<p style="font-size:14px;font-weight:600;color:rgba(255,255,255,.75);margin:0 0 32px;">&#128101; ~100 coaches &amp; technisch directeuren</p>',
                pad="0px||0px||false|false"
            ) +
            btn("Meld je aan -&gt;", "#"),
            "1_2"
        ) +
        col(
            f'[et_pb_image src="/wp-content/uploads/smart11/Smart11_V2-8.jpg" '
            f'alt="Smart11 Congres 2026" border_radii="on|16px|16px|16px|16px" {V}]'
            f'[/et_pb_image]',
            "1_2"
        ),
        structure="1_2,1_2"
    ),
    bg=CARD, pad="80px||80px||false|false",
    extra='border_width_top="1px" border_color_top="rgba(255,255,255,0.08)" border_width_bottom="1px" border_color_bottom="rgba(255,255,255,0.08)"'
)

# ── 9. Nieuwsbrief ──────────────────────────────────────────────────────────

newsletter_html = f"""<div class="nl-form">
  <div class="nl-row">
    <input class="nl-input" type="text" placeholder="Voornaam" />
    <input class="nl-input" type="email" placeholder="E-mailadres" />
  </div>
  <select class="nl-select">
    <option value="" disabled selected>Ik ben een... (kies jouw rol)</option>
    <option value="coach">Coach</option>
    <option value="speler">Speler</option>
    <option value="club">Club / technisch directeur</option>
  </select>
  <button class="nl-btn">Schrijf me in — gratis -&gt;</button>
  <p class="nl-note">Geen spam. Alleen waardevolle content. Op elk moment uitschrijven.</p>
</div>"""

newsletter_sec = sec(
    row_cols(
        col(
            txt(
                tag("Nieuwsbrief") +
                h2("Wekelijks <em style='color:#DC9600;font-style:normal;'>voetbalintelligentie</em><br>in je inbox") +
                f'<p style="font-size:15px;color:{TEXT_SEC};line-height:1.7;margin:16px 0 0;">Tactische tips, analyse-inzichten en Smart11 nieuws — elke week gratis. Al meer dan 1.200 coaches gingen je voor.</p>',
                pad="0px||0px||false|false"
            ),
            "1_2"
        ) +
        col(code(newsletter_html), "1_2"),
        structure="1_2,1_2"
    ),
    bg=CARD, pad="80px||80px||false|false",
    extra='border_width_top="1px" border_color_top="rgba(255,255,255,0.08)"'
)

# ── 10. Final CTA ───────────────────────────────────────────────────────────

cta_sec = sec(
    row(col(
        txt(
            f'<div style="text-align:center;">'
            + tag("Start vandaag")
            + f'<h2 style="font-size:clamp(32px,4.5vw,52px);font-weight:900;font-style:italic;line-height:1.1;letter-spacing:-.025em;color:#fff;margin:0 0 20px;">Jouw volgende wedstrijd is dit weekend.<br>Wat doe je met de <em style="color:{GOLD};font-style:normal;">analyse</em>?</h2>'
            + lead("Sluit je aan bij meer dan 17 clubs die al slimmer analyseren. Start gratis of plan een demo.", "520px")
            + '</div>',
            pad="0px||48px||false|false"
        ) +
        btn("Start vandaag gratis", "#", "center",
            'button_text_size="16px" custom_padding="20px|56px|20px|56px|true|true"') +
        f'[et_pb_button button_url="#" button_text="Plan een demo -&gt;" button_alignment="center" '
        f'custom_button="on" button_bg_color="rgba(255,255,255,0.04)" button_text_color="#FFFFFF" '
        f'button_font="Poppins|600|||||||" button_text_size="15px" '
        f'button_border_width="1px" button_border_color="rgba(255,255,255,0.15)" '
        f'button_border_radius="10px" button_use_icon="off" {V}][/et_pb_button]' +
        txt(
            f'<p style="font-size:12px;color:rgba(255,255,255,.25);text-align:center;margin:20px 0 0;">Geen creditcard nodig &middot; Gratis te starten &middot; Onboarding inbegrepen</p>'
        )
    )),
    bg="#0f0d00", pad="100px||100px||false|false",
    extra='border_width_top="1px" border_color_top="rgba(220,150,0,0.3)" border_radii="on|0px|0px|0px|0px"'
)

# ── Assemble ────────────────────────────────────────────────────────────────

shortcode = (
    fonts_sec +
    hero_sec +
    stats_sec +
    tools_sec +
    kennis_sec +
    steps_sec +
    news_sec +
    reviews_sec +
    congres_sec +
    newsletter_sec +
    cta_sec
)

out_sc = "Smart11/html_pages/homepage-shortcode.txt"
out_json = "Smart11/html_pages/homepage-divi.json"

with open(out_sc, "w", encoding="utf-8") as f:
    f.write(shortcode)

with open(out_json, "w", encoding="utf-8") as f:
    json.dump({"version": "4.27.0", "data": shortcode}, f, ensure_ascii=False, indent=2)

print(f"Shortcode: {len(shortcode):,} tekens  -&gt;  {out_sc}")
print(f"Divi JSON:                          -&gt;  {out_json}")
print()
print("Stap 1  Kopieer de shortcode uit homepage-shortcode.txt")
print("Stap 2  Ga naar de Divi pagina -&gt; gebruik 'Divi builder' -&gt; plak in 'Portability' -&gt; Import")
print("        OF: plak shortcode direct in een Divi Code module op de pagina.")
print()
print("Afbeeldingen uploaden naar WordPress:")
print("  /wp-content/uploads/smart11/  (maak deze map aan in Media Library)")
print("  Vereiste bestanden:")
print("    Frame-1.mp4")
print("    Smart11_V2-5.jpg  Smart11_V2-7.jpg  Smart11_V2-8.jpg")
print("    Smartcoach-laptop.jpg  cursus-voetbal-coach.jpg")
print("    videoanalyse-voetbal-ai.jpg  rtc-niek.jpg")
