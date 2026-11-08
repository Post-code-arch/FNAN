#!/usr/bin/env python3
"""Génère les pages statiques du site FNAN (EN + AR) à la racine du dépôt.

Usage : python3 build.py
Le contenu vit ici (fonction T(en)) ; ne pas éditer les .html générés.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
SITE_EN = "National Cultural Festival of Plastic and Visual Arts"
EDITION_EN = "Digital Edition"
DATES_EN = "19 — 22 November 2026"


def T(en):
    return escape(en)


# (fichier, EN court, AR court, titre de page EN, titre de page AR)
PAGES = [
    ("about", "About the Festival", "About the Festival"),
    ("programme", "Programme", "The Programme"),
    ("artists", "Artists", "The Artists"),
    ("experts", "Experts", "The Experts"),
    ("visit", "Visit the Festival", "Visit the Festival"),
    ("press", "Press & Media", "Press & Media"),
]
TAGLINES = {
    "about": ("A space where art meets new expressions."),
    "programme": ("Four ways to explore, create and connect."),
    "artists": ("The artists behind new imaginaries."),
    "experts": ("The voices behind the ideas."),
    "visit": ("Experience the festival. Discover new perspectives."),
    "press": ("Everything you need to cover the festival."),  # provisoire : texte non fourni
}
ARROW_DL = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M8 2v8M4.5 7 8 10.5 11.5 7M3 13.5h10"/></svg>'
ARROW = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M3 9h12M10 4l5 5-5 5"/></svg>'


def arch_paths(n=6, active=0, w=120, h=150):
    """Arches emboîtées (SVG). `active` = numéro (1..n) de la couche mise en lumière."""
    out = []
    for i in range(n):
        inset = i * 48 / (n - 1)
        left, right, top = 8 + inset, w - 8 - inset, 6 + inset * 1.25
        r = (right - left) / 2
        cls = f"a{i + 1}" + (" on" if active == i + 1 else "")
        out.append(f'<path class="{cls}" d="M{left},{h - 2} V{top + r:.1f} A{r:.1f} {r:.1f} 0 0 1 {right},{top + r:.1f} V{h - 2}"/>')
    return "".join(out)


def head(title_en, desc, body_class=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title_en)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#050403">
<link rel="icon" type="image/webp" href="assets/logo-mark-small.webp">
<meta property="og:title" content="{escape(title_en)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="assets/kv.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Syne:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body class="{body_class}">
"""


def header(current=""):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{f}.html"{cur if f == current else ""}>{T(en)}</a>'
        for f, en, _ in PAGES[:4]
    )
    return f"""<header class="hdr" id="hdr">
  <a class="brand" href="index.html" aria-label="FNAN — home">
    <img src="assets/logo-mark-small.webp" alt="" width="54" height="46">
    <span>FNAN</span>
  </a>
  <nav class="nav" id="nav" aria-label="Main">
    {links}
    <a class="cta mono" href="visit.html"{cur if current == "visit" else ""}>{T("Visit the Festival")}</a>
    <a href="press.html"{cur if current == "press" else ""}>{T("Press & Media")}</a>
  </nav>
  <img class="hdr-min" src="assets/logo-culture.webp" alt="Ministry of Culture and Arts of Algeria" width="36" height="44">
  <button class="burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
</header>
"""


def footer():
    order = ["about", "programme", "artists", "experts", "press", "visit"]
    names = {f: en for f, en, _ in PAGES}
    explore = "".join(f'<li><a href="{f}.html">{T(names[f])}</a></li>' for f in order)
    return f"""<footer class="ftr">
  <div class="ftr-top">
    <div>
      <img class="ftr-mark" src="assets/logo-mark.webp" alt="FNAN" width="110" height="92">
      <div class="ftr-name">{T(SITE_EN)} — {T(EDITION_EN)}</div>
      <div class="ftr-date mono">{T("19–22 November 2026 · Algiers")}</div>
    </div>
    <img class="logo-min" src="assets/logo-culture.webp" alt="Ministry of Culture and Arts of Algeria" width="69" height="84">
  </div>
  <div class="ftr-cols">
    <div><h4 class="mono">{T("Explore")}</h4><ul>{explore}</ul></div>
    <div><h4 class="mono">{T("Follow us")}</h4><ul>
      <li><a href="https://www.instagram.com/algeria.visual.arts.festival" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.facebook.com/share/1N61yh9TeK/" target="_blank" rel="noopener">Facebook</a></li></ul></div>
  </div>
  <div class="ftr-bot mono">
    <span><a href="#">{T("Privacy Policy")}</a> · <a href="#">{T("Legal Notice")}</a></span>
    <span>© FNAN 2026</span>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


def pager(idx):
    prev = PAGES[idx - 1] if idx > 0 else None
    nxt = PAGES[idx + 1] if idx < len(PAGES) - 1 else None

    def cell(p, k_en, n):
        if not p:
            return '<span class="empty"></span>'
        return f'<a href="{p[0]}.html"><span class="k mono">{T(k_en)} · 0{n}</span><span class="t">{T(p[2])}</span></a>'

    return f'<nav class="pager" aria-label="Pages">{cell(prev, "Previous", idx)}{cell(nxt, "Next", idx + 2)}</nav>'


def page_hero(idx):
    f, en, ten = PAGES[idx]
    tl = TAGLINES[f]
    return f"""<section class="page-hero">
  <p class="num">0{idx + 1} / 0{len(PAGES)}</p>
  <h1>{T(ten)}</h1>
  <p class="lead">{T(tl)}</p>
  <svg class="page-arch" viewBox="0 0 120 150" aria-hidden="true">{arch_paths(6, idx + 1)}</svg>
</section>
"""


def lst(items):
    return '<ul class="list">' + "".join(f"<li>{T(e)}</li>" for e in items) + "</ul>"


# ------------------------------------------------------------------ pages
def index():
    layer_links = "".join(
        f'<li><a href="{f}.html" data-layer="{i + 1}"><span class="n mono">0{i + 1}</span><span class="t mono">{T(en)}</span></a></li>'
        for i, (f, en, ten) in enumerate(PAGES)
    )
    gates = "".join(
        f'<a class="gate rv" href="{f}.html"><span class="n mono">0{i + 1}</span>'
        f'<span><span class="t">{T(ten)}</span><p class="d">{T(TAGLINES[f])}</p></span>'
        f'<span class="go">{ARROW}</span></a>'
        for i, (f, en, ten) in enumerate(PAGES)
    )
    return (
        head(f"FNAN — {SITE_EN} · 19–22 November 2026, Algiers",
             "FNAN, National Cultural Festival of Plastic and Visual Arts, Digital Edition. 19–22 November 2026, Dar Abd-el-Tif and the National Museum of Fine Arts, Algiers.")
        + header()
        + f"""<main>
<section class="hero" id="hero" aria-labelledby="hero-title">
  <div class="kv" aria-hidden="true">
    <div class="kv-box">
      <img class="kv-img" src="assets/kv.webp" alt="" width="1333" height="2000" fetchpriority="high">
      <!-- Vidéo du KV : déposer assets/kv.mp4 (même cadrage vertical 2:3) et elle remplace l'image -->
      <video class="kv-video" id="kv-video" muted loop playsinline autoplay preload="auto" poster="assets/kv.webp">
        <source src="assets/kv.mp4" type="video/mp4">
      </video>
      <div class="kv-light g"></div><div class="kv-light r"></div>
      <div class="kv-door"></div><div class="kv-sweep"></div>
    </div>
    <div class="kv-shade"></div><div class="kv-dark"></div><div class="kv-fade"></div>
  </div>

  <div class="hero-copy">
    <p class="edition mono">{T(EDITION_EN)}</p>
    <h1 id="hero-title">{T(SITE_EN)}</h1>
    <p class="when">{T(DATES_EN)}</p>
    <p class="where mono">{T("Dar Abd-el-Tif")}<br>{T("National Museum of Fine Arts, Algiers")}</p>
  </div>

  <nav class="layers" id="layers" aria-label="{escape("Navigate through the arch layers")}">
    <svg class="layers-arch" viewBox="0 0 120 150" aria-hidden="true">{arch_paths(6)}</svg>
    <ol>{layer_links}</ol>
  </nav>
  <div class="cue mono" aria-hidden="true">{T("Scroll")}</div>
</section>

<section class="gates" aria-labelledby="gates-title">
  <h2 id="gates-title" class="rv">{T("Walk through the arches.")}</h2>
  {gates}
</section>
</main>
"""
        + footer()
    )


def about():
    purposes = [
        ("Supporting Algerian Creation", "Giving visibility to Algerian artists and supporting contemporary artistic expression."),
        ("Building Artistic Bridges", "Creating connections between visual arts and digital practices."),
        ("Encouraging Experimentation", "Promoting artistic research, experimentation and creative collaborations."),
        ("Making Art Accessible", "Making artworks accessible through cultural mediation and encounters with the public."),
    ]
    cards = "".join(
        f'<article class="card rv"><span class="n mono">0{i + 1}</span><h3>{T(te)}</h3><p>{T(de)}</p></article>'
        for i, (te, de) in enumerate(purposes)
    )
    return (
        head("About the Festival — FNAN", "The National Festival of Digital Arts brings together visual arts, audiovisual creation and digital practices.", "inner")
        + header("about") + "<main>" + page_hero(0)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("The National Festival of Digital Arts brings together visual arts, audiovisual creation and digital practices in a space dedicated to artistic exploration and contemporary expression.")}</p>
    <p>{T("This edition celebrates Algerian artistic creation and the artists exploring new possibilities through image, video, graphic design, light and immersive installations, while maintaining a strong connection with our cultural heritage.")}</p>
  </div>
  <section class="theme rv">
    <p class="label mono">{T("Theme of the Festival")}</p>
    <h2>{T("Algerian Imaginaries: creating in the digital age.")}</h2>
    <p>{T("An exploration of how digital technologies are transforming the ways we create, see and experience art, without distancing us from our cultural heritage.")}</p>
  </section>
  <section>
    <h2 class="sec-title rv">{T("The Festival's Purpose")}</h2>
    <div class="cards">{cards}</div>
  </section>
</div>
</main>"""
        + pager(0) + footer()
    )


def programme():
    def act(n, te, tage, body):
        return f"""<section class="act rv">
    <div class="head"><span class="n mono">0{n}</span><h2>{T(te)}</h2><p class="tag">{T(tage)}</p></div>
    <div class="body">{body}</div>
  </section>"""

    exhibition = (
        f'<p>{T("Discover exclusive artworks and ongoing research exploring the possibilities of contemporary visual and digital creation.")}</p>'
        f'<p>{T("The exhibition brings together different artistic disciplines, including video, animation, photography, illustration, painting and digital creations.")}</p>'
        f'<p>{T("It also explores new forms of artistic expression through installations and projection mapping, depending on available technical resources.")}</p>'
        f'<h3>{T("Discover")}</h3>'
        + lst([("Exclusive artworks."), ("Artistic research processes."),
               ("Digital and audiovisual creations."), ("Installations and projection mapping.")])
    )
    residency = (
        f'<p>{T("The creative residency invites artists to develop new artistic proposals through experimentation, research and the exploration of digital tools.")}</p>'
        f'<p>{T("The resulting productions may take the form of artworks, audiovisual sequences or ongoing research processes presented to the public.")}</p>'
        f'<p>{T("The residency is structured around two formats:")}</p>'
        '<div class="formats">'
        f'<article class="card"><h3>{T("Supported Creative Residency")}</h3><p>{T("Four resident artists are welcomed and supported throughout the creative process, developing an artwork from beginning to end.")}</p></article>'
        f'<article class="card"><h3>{T("Augmented Artworks")}</h3><p>{T("Artists bring existing artworks that are enhanced through digital approaches and presented as part of the exhibition.")}</p></article>'
        "</div>"
    )
    talks = (
        f'<p>{T("A space for dialogue and reflection, bringing together different perspectives on the relationship between artistic creation, technology and cultural heritage.")}</p>'
        f'<p>{T("Through an opening conference and panel discussions, the programme explores several key topics:")}</p>'
        + lst([("Digital Arts in Algeria."), ("Artistic Creation with Artificial Intelligence."),
               ("Algerian Heritage and Imaginaries."), ("The Production and Distribution of Digital Artworks.")])
    )
    workshops = (
        f'<p>{T("Practical workshops designed to encourage experimentation, knowledge sharing and the discovery of new creative approaches.")}</p>'
        f'<p>{T("The workshops explore different aspects of contemporary digital creation, including:")}</p>'
        + lst([("Developing an Artistic Concept."), ("Introduction to Projection Mapping."),
               ("Visual Creation with Artificial Intelligence."), ("Preparing an Artwork Presentation and Technical Sheet.")])
    )
    return (
        head("The Programme — FNAN", "Four ways to explore, create and connect: exhibition, creative residency, talks & meetings and workshops.", "inner")
        + header("programme") + "<main>" + page_hero(1)
        + f"""<div class="wrap">
  <p class="prose rv"><span style="color:var(--soft);font-size:1.15rem;display:block;max-width:60ch">{T("The festival unfolds through four complementary activities, bringing together artistic discovery, creative experimentation, exchange and knowledge sharing.")}</span></p>
  {act(1, "Exhibition", "A journey through artistic expression.", exhibition)}
  {act(2, "Creative Residency", "Where ideas become new creations.", residency)}
  {act(3, "Talks & Meetings", "Exchange ideas. Explore new perspectives.", talks)}
  {act(4, "Workshops", "Learn. Experiment. Create.", workshops)}
</div>
</main>"""
        + pager(1) + footer()
    )


def profiles(n, name_en, lines):
    cards = "".join(
        f'<article class="profile rv"><div class="portrait" aria-hidden="true"></div>'
        f'<h3>{T(name_en)} {i + 1:02d}</h3>'
        + "".join(f"<p>{T(e)}</p>" for e in lines)
        + f'<span class="soon mono">{T("Profile coming soon")}</span></article>'
        for i in range(n)
    )
    return f'<div class="profiles">{cards}</div>'


def artists():
    return (
        head("The Artists — FNAN", "Discover the artists exploring new forms of expression through visual arts, audiovisual creation and digital practices.", "inner")
        + header("artists") + "<main>" + page_hero(2)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("Discover the artists exploring new forms of expression through visual arts, audiovisual creation and digital practices.")}</p>
    <p>{T("Through their works and creative approaches, they contribute to a dialogue between artistic heritage, contemporary expression and emerging technologies.")}</p>
  </div>
  <section>
    <h2 class="sec-title rv">{T("Artist Profiles")}</h2>
    <p class="label mono rv">{T("Each artist profile will feature:")}</p>
    <div class="chips rv"><span class="chip">{T("Artist's name")}</span><span class="chip">{T("Portrait")}</span><span class="chip">{T("Biography")}</span></div>
  </section>
  {profiles(8, "Artist", [("Biography to come.")])}
</div>
</main>"""
        + pager(2) + footer()
    )


def experts():
    topics = [("Digital Arts in Algeria"), ("Artistic Creation with Artificial Intelligence"),
              ("Algerian Heritage and Imaginaries"), ("Production and Distribution of Digital Artworks")]
    chips = "".join(f'<span class="chip">{T(e)}</span>' for e in topics)
    fields = [("Expert's name"), ("Portrait"), ("Professional title"), ("Biography"),
              ("Area of expertise"), ("Associated conference, panel or workshop")]
    fchips = "".join(f'<span class="chip">{T(e)}</span>' for e in fields)
    return (
        head("The Experts — FNAN", "Meet the artists, experts and cultural professionals contributing to the festival's programme.", "inner")
        + header("experts") + "<main>" + page_hero(3)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("Meet the artists, experts and cultural professionals contributing to the festival's programme through conferences, panel discussions and practical workshops.")}</p>
    <p>{T("Their perspectives open up conversations around digital creation, artistic experimentation, cultural heritage and the evolving relationship between art and technology.")}</p>
  </div>
  <section>
    <p class="label mono rv">{T("Key topics")}</p>
    <div class="chips rv">{chips}</div>
  </section>
  <section>
    <h2 class="sec-title rv">{T("Meet the Experts")}</h2>
    <p class="label mono rv">{T("Each profile will feature:")}</p>
    <div class="chips rv">{fchips}</div>
  </section>
  {profiles(6, "Expert", [("Title and expertise to come.")])}
</div>
</main>"""
        + pager(3) + footer()
    )


def visit():
    return (
        head("Visit the Festival — FNAN", "19–22 November 2026 at Dar Abd-el-Tif and the National Museum of Fine Arts of Algiers.", "inner")
        + header("visit") + "<main>" + page_hero(4)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("Join us for an encounter between visual arts, creative experimentation and digital practices.")}</p>
    <p>{T("The festival invites visitors to explore artistic works, discover new forms of expression and take part in conversations and creative experiences.")}</p>
  </div>
  <section>
    <h2 class="sec-title rv">{T("Festival Information")}</h2>
    <div class="info">
      <article class="card rv"><span class="n mono">{T("Dates")}</span><p class="big">{T("19 – 22 November 2026")}</p></article>
      <article class="card rv"><span class="n mono">{T("Locations")}</span>
        <p class="big">{T("Dar Abd-el-Tif, Algiers.")}</p>
        <p class="big">{T("National Museum of Fine Arts of Algiers.")}</p></article>
    </div>
  </section>
  <section class="signature rv">
    <h2>{T("Algerian Imaginaries. Creating in the digital age.")}</h2>
    <p>{T("A space to discover, experiment, exchange and imagine new possibilities for artistic creation.")}</p>
  </section>
</div>
</main>"""
        + pager(4) + footer()
    )


def press():
    ig = "https://www.instagram.com/algeria.visual.arts.festival"
    fb = "https://www.facebook.com/share/1N61yh9TeK/"
    mail = "festivalartsvisuelsalgerie@gmail.com"

    def doc(n, title, desc, meta, thumb, href, fname, cta):
        return (
            f'<article class="doc rv"><a class="doc-thumb" href="{href}" target="_blank" rel="noopener" aria-label="{escape(title)}">'
            f'<img src="{thumb}" alt="" loading="lazy"></a>'
            f'<div class="doc-body"><span class="n mono">{n}</span><h3>{T(title)}</h3><p>{T(desc)}</p>'
            f'<p class="meta mono">{T(meta)}</p>'
            f'<a class="btn mono" href="{href}" download="{fname}">{T(cta)} {ARROW_DL}</a></div></article>'
        )

    docs = (
        doc("01", "Press kit", "The official presentation of the festival: vision, theme, programme, venues and key facts.",
            "PDF · Arabic · 7 pages", "assets/press/thumb-dossier.webp", "assets/press/fnan-dossier-de-presse.pdf", "FNAN-press-kit.pdf", "Download the press kit")
        + doc("02", "Press release", "The announcement of the first festival edition, 19–22 November 2026.",
              "PDF · Arabic · 1 page", "assets/press/thumb-communique.webp", "assets/press/fnan-communique-de-presse.pdf", "FNAN-press-release.pdf", "Download the press release")
        + doc("03", "Key visual", "The official poster of the festival, for editorial use.",
              "JPG · 1443 × 2048 px", "assets/press/thumb-kv.webp", "assets/press/fnan-key-visual.jpg", "FNAN-key-visual.jpg", "Download the key visual")
    )
    contact = f"""<article class="card contact rv">
      <span class="n mono">04</span><h3>{T("Press contact")}</h3>
      <p>{T("Communication & Media Unit. For media enquiries, interview requests and coverage coordination.")}</p>
      <ul class="clist">
        <li><span class="mono">{T("Email")}</span><a href="mailto:{mail}">{mail}</a></li>
        <li><span class="mono">{T("Phone")}</span><a href="tel:+213553486929">0553 48 69 29</a></li>
        <li><span class="mono">{T("Social")}</span><span><a href="{ig}" target="_blank" rel="noopener">Instagram</a> · <a href="{fb}" target="_blank" rel="noopener">Facebook</a></span></li>
      </ul>
    </article>"""
    return (
        head("Press & Media — FNAN", "Press resources for the National Cultural Festival of Plastic and Visual Arts: press kit, press release, key visual and media contact.", "inner")
        + header("press") + "<main>" + page_hero(5)
        + f"""<div class="wrap">
  <section>
    <h2 class="sec-title rv">{T("Press resources")}</h2>
    <p class="note mono rv">{T("The press documents are provided in Arabic.")}</p>
    <div class="docs">{docs}</div>
  </section>
  <section>{contact}</section>
</div>
</main>"""
        + pager(5) + footer()
    )


if __name__ == "__main__":
    for name, fn in [("index", index), ("about", about), ("programme", programme), ("artists", artists), ("experts", experts), ("visit", visit), ("press", press)]:
        (ROOT / f"{name}.html").write_text(fn(), encoding="utf-8")
        print("écrit", f"{name}.html")
