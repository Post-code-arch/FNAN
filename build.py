#!/usr/bin/env python3
"""Génère les pages statiques du site FNAN : anglais (racine) et arabe (dossier ar/).

Usage : python3 build.py
Le contenu vit ici, en deux langues : T("anglais", "arabe"). Ne pas éditer les .html générés.
Les textes arabes viennent du copywriting « Architecture du site v3 » ; les chaînes sans source
(libellés d'interface, aperçus de profils) sont à faire relire avant production.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
L = "en"  # langue en cours de génération : "en" | "ar"

SITE = ("National Cultural Festival of Plastic and Visual Arts", "المهرجان الثقافي الوطني للفنون التشكيلية والفنون المرئية")
EDITION = ("Digital Edition", "النسخة الرقمية")
DATES = ("19 — 22 November 2026", "19 — 22 نوفمبر 2026")
IG = "https://www.instagram.com/algeria.visual.arts.festival"
FB = "https://www.facebook.com/share/1N61yh9TeK/"
MAIL = "festivalartsvisuelsalgerie@gmail.com"


def T(en, ar=None):
    """Texte de la langue courante (anglais si pas de version arabe)."""
    return escape(ar if (L == "ar" and ar is not None) else en)


def S(pair):
    return T(pair[0], pair[1])


def A(path):
    """Chemin d'un fichier du site depuis la page courante."""
    return ("../" if L == "ar" else "") + path


PAGES = [
    dict(f="about", nav=("About the Festival", "نبذة عن المهرجان"), title=("About the Festival", "نبذة عن المهرجان"),
         tag=("A space where art meets new expressions.", "ملتقى الفنون والتعبيرات الإبداعية المعاصرة")),
    dict(f="programme", nav=("Programme", "البرنامج"), title=("The Programme", "برنامج المهرجان"),
         tag=("Four ways to explore, create and connect.", "أربعة محاور تجمع بين الاكتشاف والإبداع والتفاعل.")),
    dict(f="artists", nav=("Artists", "الفنانون"), title=("The Artists", "الفنانون"),
         tag=("The artists behind new imaginaries.", "تجارب فنية تعيد تشكيل آفاق الإبداع المعاصر.")),
    dict(f="experts", nav=("Experts", "الخبراء"), title=("The Experts", "الخبراء"),
         tag=("The voices behind the ideas.", "خبرات ورؤى تثري النقاش حول الفن والتكنولوجيا.")),
    dict(f="visit", nav=("Visit the Festival", "زيارة المهرجان"), title=("Visit the Festival", "زيارة المهرجان"),
         tag=("Experience the festival. Discover new perspectives.", "تجربة فنية وثقافية متكاملة.")),
    dict(f="press", nav=("Press & Media", "الصحافة والإعلام"), title=("Press & Media", "الصحافة والإعلام"), tag=None),
]
PG = {p["f"]: p for p in PAGES}

ARROW = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M3 9h12M10 4l5 5-5 5"/></svg>'
ARROW_DL = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M8 2v8M4.5 7 8 10.5 11.5 7M3 13.5h10"/></svg>'


def arch_paths(n=6, active=0, w=120, h=150):
    """Arches emboîtées (SVG). `active` = numéro (1..n) de la couche mise en lumière."""
    out = []
    for i in range(n):
        inset = i * 48 / (n - 1)
        left, right, top = 8 + inset, w - 8 - inset, 6 + inset * 1.25
        r = (right - left) / 2
        cls = f"a{i + 1}" + (" on" if active == i + 1 else "")
        out.append(f'<path class="{cls}" d="M{left:.1f},{h - 2} V{top + r:.1f} A{r:.1f} {r:.1f} 0 0 1 {right:.1f},{top + r:.1f} V{h - 2}"/>')
    return "".join(out)


def link_for(slug, lang):
    """Lien vers la page `slug` dans la langue `lang`, depuis la langue courante."""
    if lang == L:
        return f"{slug}.html"
    return f"ar/{slug}.html" if lang == "ar" else f"../{slug}.html"


def head(title, desc, slug, body_class=""):
    fonts = "Geist+Mono:wght@400;500&family=Syne:wght@400;500;600;700"
    if L == "ar":
        fonts = "Reem+Kufi:wght@400;500;600;700&family=" + fonts
    d = "rtl" if L == "ar" else "ltr"
    return f"""<!doctype html>
<html lang="{L}" dir="{d}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{S(title)}</title>
<meta name="description" content="{S(desc)}">
<meta name="theme-color" content="#050403">
<link rel="icon" type="image/webp" href="{A('assets/logo-mark-small.webp')}">
<link rel="alternate" hreflang="en" href="{link_for(slug, 'en')}">
<link rel="alternate" hreflang="ar" href="{link_for(slug, 'ar')}">
<meta property="og:title" content="{S(title)}">
<meta property="og:description" content="{S(desc)}">
<meta property="og:locale" content="{'ar_DZ' if L == 'ar' else 'en_GB'}">
<meta property="og:image" content="{A('assets/kv.webp')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={fonts}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{A('assets/site.css')}">
</head>
<body class="{body_class}">
"""


def header(slug, current=""):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{p["f"]}.html"{cur if p["f"] == current else ""}>{S(p["nav"])}</a>'
        for p in PAGES[:4]
    )
    press, visit = PG["press"], PG["visit"]
    ar_cur = ' aria-current="true"' if L == "ar" else ""
    en_cur = ' aria-current="true"' if L == "en" else ""
    return f"""<header class="hdr" id="hdr">
  <a class="brand" href="index.html" aria-label="FNAN">
    <img src="{A('assets/logo-mark-small.webp')}" alt="" width="54" height="46">
    <span>FNAN</span>
  </a>
  <nav class="nav" id="nav" aria-label="{T('Main', 'التنقل الرئيسي')}">
    {links}
    <a class="cta mono" href="visit.html"{cur if current == "visit" else ""}>{S(visit['nav'])}</a>
    <a href="press.html"{cur if current == "press" else ""}>{S(press['nav'])}</a>
  </nav>
  <img class="hdr-min" src="{A('assets/logo-culture.webp')}" alt="{T('Ministry of Culture and Arts of Algeria', 'وزارة الثقافة والفنون - الجزائر')}" width="36" height="44">
  <div class="lang mono" role="group" aria-label="Language">
    <a href="{link_for(slug, 'ar')}" hreflang="ar" lang="ar"{ar_cur}>AR</a><span aria-hidden="true">|</span><a href="{link_for(slug, 'en')}" hreflang="en" lang="en"{en_cur}>EN</a>
  </div>
  <button class="burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
</header>
"""


def footer():
    order = ["about", "programme", "artists", "experts", "press", "visit"] if L == "en" else \
            ["about", "programme", "artists", "experts", "visit", "press"]
    if L == "ar":
        explore = "".join(f'<li><a href="{f}.html"><span class="n">0{i + 1}</span> — {S(PG[f]["nav"])}</a></li>'
                          for i, f in enumerate(order))
    else:
        explore = "".join(f'<li><a href="{f}.html">{S(PG[f]["nav"])}</a></li>' for f in order)
    return f"""<footer class="ftr">
  <div class="ftr-top">
    <img class="ftr-mark" src="{A('assets/logo-mark.webp')}" alt="FNAN" width="110" height="92">
    <img class="logo-min" src="{A('assets/logo-culture.webp')}" alt="{T('Ministry of Culture and Arts of Algeria', 'وزارة الثقافة والفنون - الجزائر')}" width="69" height="84">
  </div>
  <div class="ftr-name">{S(SITE)} — {S(EDITION)}</div>
  <div class="ftr-date mono">{T("19–22 November 2026 · Algiers", "19–22 نوفمبر 2026 · الجزائر العاصمة")}</div>
  <div class="ftr-cols">
    <div><h4 class="mono">{T("Explore", "صفحات الموقع")}</h4><ul>{explore}</ul></div>
    <div><h4 class="mono">{T("Follow us", "تابعونا")}</h4><ul>
      <li><a href="{IG}" target="_blank" rel="noopener">{T("Instagram", "إنستغرام")}</a></li><li><a href="{FB}" target="_blank" rel="noopener">{T("Facebook", "فيسبوك")}</a></li></ul></div>
  </div>
  <div class="ftr-bot mono">
    <span><a href="#">{T("Privacy Policy", "سياسة الخصوصية")}</a> · <a href="#">{T("Legal Notice", "الإشعار القانوني")}</a></span>
    <span dir="ltr">© FNAN 2026</span>
  </div>
</footer>
<script src="{A('assets/site.js')}"></script>
</body>
</html>
"""


def pager(idx):
    prev = PAGES[idx - 1] if idx > 0 else None
    nxt = PAGES[idx + 1] if idx < len(PAGES) - 1 else None

    def cell(p, k, n):
        if not p:
            return '<span class="empty"></span>'
        return f'<a href="{p["f"]}.html"><span class="k mono">{T(*k)} · 0{n}</span><span class="t">{S(p["title"])}</span></a>'

    return (f'<nav class="pager" aria-label="{T("Pages", "الصفحات")}">'
            f'{cell(prev, ("Previous", "السابق"), idx)}{cell(nxt, ("Next", "التالي"), idx + 2)}</nav>')


def page_hero(idx):
    p = PAGES[idx]
    lead = f'<p class="lead">{S(p["tag"])}</p>' if p["tag"] else ""
    return f"""<section class="page-hero">
  <p class="num">0{idx + 1} / 0{len(PAGES)}</p>
  <h1>{S(p["title"])}</h1>
  {lead}
  <svg class="page-arch" viewBox="0 0 120 150" aria-hidden="true">{arch_paths(6, idx + 1)}</svg>
</section>
"""


def lst(items):
    return '<ul class="list">' + "".join(f"<li>{T(*i)}</li>" for i in items) + "</ul>"


# ------------------------------------------------------------------ pages
def index():
    layer_links = "".join(
        f'<li><a href="{p["f"]}.html" data-layer="{i + 1}"><span class="n mono">0{i + 1}</span><span class="t mono">{S(p["nav"])}</span></a></li>'
        for i, p in enumerate(PAGES)
    )
    gates = "".join(
        f'<a class="gate rv" href="{p["f"]}.html"><span class="n mono">0{i + 1}</span>'
        f'<span><span class="t">{S(p["title"])}</span><p class="d">{S(p["tag"]) if p["tag"] else ""}</p></span>'
        f'<span class="go">{ARROW}</span></a>'
        for i, p in enumerate(PAGES)
    )
    kv = "assets/kv-rtl.webp" if L == "ar" else "assets/kv.webp"
    return (
        head(("FNAN — " + SITE[0] + " · 19–22 November 2026, Algiers", "FNAN — " + SITE[1] + " · 19–22 نوفمبر 2026، الجزائر"),
             ("FNAN, National Cultural Festival of Plastic and Visual Arts, Digital Edition. 19–22 November 2026, Dar Abd-el-Tif and the National Museum of Fine Arts, Algiers.",
              "المهرجان الثقافي الوطني للفنون التشكيلية والفنون المرئية، النسخة الرقمية. 19–22 نوفمبر 2026، دار عبد اللطيف والمتحف الوطني للفنون الجميلة، الجزائر العاصمة."),
             "index")
        + header("index")
        + f"""<main>
<section class="hero" id="hero" aria-labelledby="hero-title">
  <div class="kv" aria-hidden="true">
    <div class="kv-box">
      <img class="kv-img" src="{A(kv)}" alt="" width="1333" height="2000" fetchpriority="high">
      <!-- Vidéo du KV : déposer assets/kv.mp4 (même cadrage vertical 2:3) et elle remplace l'image (retournée automatiquement en arabe) -->
      <video class="kv-video" id="kv-video" muted loop playsinline autoplay preload="auto" poster="{A(kv)}">
        <source src="{A('assets/kv.mp4')}" type="video/mp4">
      </video>
      <div class="kv-light g"></div><div class="kv-light r"></div>
      <div class="kv-door"></div><div class="kv-sweep"></div>
    </div>
    <div class="kv-shade"></div><div class="kv-dark"></div><div class="kv-fade"></div>
  </div>

  <div class="hero-copy">
    <p class="edition mono">{S(EDITION)}</p>
    <h1 id="hero-title">{S(SITE)}</h1>
    <p class="when">{S(DATES)}</p>
    <p class="where mono">{T("Dar Abd-el-Tif", "دار عبد اللطيف")}<br>{T("National Museum of Fine Arts, Algiers", "المتحف الوطني للفنون الجميلة، الجزائر العاصمة")}</p>
  </div>

  <nav class="layers" id="layers" aria-label="{T("Navigate through the arch layers", "التنقل عبر طبقات القوس")}">
    <svg class="layers-arch" viewBox="0 0 120 150" aria-hidden="true">{arch_paths(6)}</svg>
    <ol>{layer_links}</ol>
  </nav>
  <div class="cue mono" aria-hidden="true">{T("Scroll", "مرّر")}</div>
</section>

<section class="gates" aria-labelledby="gates-title">
  <h2 id="gates-title" class="rv">{T("Walk through the arches.", "اعبروا الأقواس.")}</h2>
  {gates}
</section>
</main>
"""
        + footer()
    )


def about():
    purposes = [
        (("Supporting Algerian Creation", "دعم الإبداع الفني الجزائري"),
         ("Giving visibility to Algerian artists and supporting contemporary artistic expression.", "دعم الفنانين الجزائريين ومرافقة تجاربهم في تطوير أشكال جديدة من التعبير الفني.")),
        (("Building Artistic Bridges", "تطوير أشكال التعبير الفني المعاصر"),
         ("Creating connections between visual arts and digital practices.", "تشجيع التفاعل بين مختلف المجالات الفنية والوسائط المرئية، واستكشاف أساليب جديدة في الإنتاج والتعبير الفني.")),
        (("Encouraging Experimentation", "تشجيع البحث والتطوير الفني"),
         ("Promoting artistic research, experimentation and creative collaborations.", "دعم الممارسات القائمة على البحث والتجريب، وإتاحة المجال أمام الفنانين لاستكشاف تقنيات وأدوات جديدة في تطوير أعمالهم.")),
        (("Making Art Accessible", "تعزيز التفاعل مع التجارب الفنية"),
         ("Making artworks accessible through cultural mediation and encounters with the public.", "تهيئة فضاءات للقاء بين الفنانين والجمهور، وتشجيع المشاركة في الأنشطة والتجارب التي يتيحها البرنامج الفني.")),
    ]
    cards = "".join(
        f'<article class="card rv"><span class="n mono">0{i + 1}</span><h3>{S(t)}</h3><p>{S(d)}</p></article>'
        for i, (t, d) in enumerate(purposes)
    )
    return (
        head(("About the Festival — FNAN", "نبذة عن المهرجان — FNAN"),
             ("The National Festival of Digital Arts brings together visual arts, audiovisual creation and digital practices.",
              "ملتقى الفنون والتعبيرات الإبداعية المعاصرة: فنون بصرية وإبداع سمعي بصري وتعبيرات مرئية."), "about", "inner")
        + header("about", "about") + "<main>" + page_hero(0)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("The National Festival of Digital Arts brings together visual arts, audiovisual creation and digital practices in a space dedicated to artistic exploration and contemporary expression.",
          "يشكّل المهرجان الوطني للفنون التشكيلية والفنون المرئية فضاءً ثقافياً يجمع بين الفنون البصرية والإبداع السمعي البصري والتعبيرات المرئية المعاصرة، ويتيح المجال أمام استكشاف ممارسات فنية جديدة وتطوير أساليب التعبير الإبداعي.")}</p>
    <p>{T("This edition celebrates Algerian artistic creation and the artists exploring new possibilities through image, video, graphic design, light and immersive installations, while maintaining a strong connection with our cultural heritage.",
          "وتحتفي هذه الدورة بتنوّع المشهد الفني الجزائري، من خلال تجارب تستكشف إمكانات الصورة والفيديو والتصميم الغرافيكي والضوء والمنشآت الفنية التفاعلية والغامرة مع مختلف أشكال التعبير الفني المعاصر.")}</p>
  </div>
  <section class="theme rv">
    <p class="label mono">{T("Theme of the Festival", "موضوع المهرجان")}</p>
    <h2>{T("Algerian Imaginaries: creating in the digital age.", "الإبداع في العصر الرقمي")}</h2>
    <p>{T("An exploration of how digital technologies are transforming the ways we create, see and experience art, without distancing us from our cultural heritage.",
          "تسلّط هذه الدورة الضوء على التحولات التي يشهدها الفن في ظل التطور التكنولوجي، وعلى الفرص الجديدة التي تتيحها الوسائط المرئية للفنانين في ابتكار أعمالهم وتقديمها للجمهور، في سياق يعكس تطور الممارسات الفنية والإبداعية.")}</p>
  </section>
  <section>
    <h2 class="sec-title rv">{T("The Festival's Purpose", "أهداف المهرجان")}</h2>
    <div class="cards">{cards}</div>
  </section>
  <p class="rv"><span class="btn mono is-disabled" aria-disabled="true">{T("Download the festival catalogue", "تحميل دليل المهرجان")} {ARROW_DL} <em>{T("Coming soon", "قريباً")}</em></span></p>
</div>
</main>"""
        + pager(0) + footer()
    )


def programme():
    def act(n, title, tag, body):
        return f"""<section class="act rv">
    <div class="head"><span class="n mono">0{n}</span><h2>{S(title)}</h2><p class="tag">{S(tag)}</p></div>
    <div class="body">{body}</div>
  </section>"""

    third = f'<p>{T("It also explores new forms of artistic expression through installations and projection mapping, depending on available technical resources.")}</p>' if L == "en" else ""
    exhibition = (
        f'<p>{T("Discover exclusive artworks and ongoing research exploring the possibilities of contemporary visual and digital creation.", "يقدم المعرض مجموعة من الأعمال الفنية التي تعكس تنوع الممارسات الإبداعية المعاصرة، وتستكشف إمكانات توظيف الوسائط الرقمية في تطوير أشكال جديدة من التعبير الفني.")}</p>'
        f'<p>{T("The exhibition brings together different artistic disciplines, including video, animation, photography, illustration, painting and digital creations.", "وتشمل المشاركات مجالات فنية متعددة، من الفيديو والرسوم المتحركة والتصوير الفوتوغرافي والرسم التوضيحي إلى الفنون التشكيلية والمرئية.")}</p>'
        + third
        + f'<h3>{T("Discover", "يشمل المعرض :")}</h3>'
        + lst([("Exclusive artworks.", "أعمالاً فنية معاصرة."), ("Artistic research processes.", "مشاريع ومسارات بحث فني."),
               ("Digital and audiovisual creations.", "إنتاجات رقمية وسمعية بصرية."), ("Installations and projection mapping.", "منشآت فنية وعروض الإسقاط الضوئي.")])
    )
    residency = (
        f'<p>{T("The creative residency invites artists to develop new artistic proposals through experimentation, research and the exploration of digital tools.", "تتيح الإقامة الفنية للفنانين فرصة تطوير مقترحاتهم الإبداعية ضمن بيئة قائمة على البحث والتجريب واستكشاف الإمكانات التي توفرها الأدوات والتقنيات الرقمية.")}</p>'
        f'<p>{T("The resulting productions may take the form of artworks, audiovisual sequences or ongoing research processes presented to the public.", "وتتوج هذه التجارب بإنتاج أعمال فنية أو محتويات سمعية بصرية، إلى جانب مشاريع بحثية وإبداعية تُعرض ضمن فعاليات المهرجان.")}</p>'
        f'<p>{T("The residency is structured around two formats:", "وتندرج الإقامة الفنية ضمن صيغة مزدوجة:")}</p>'
        '<div class="formats">'
        f'<article class="card"><h3>{T("Supported Creative Residency", "الإقامة الفنية بالمرافقة والدعم")}</h3><p>{T("Four resident artists are welcomed and supported throughout the creative process, developing an artwork from beginning to end.", "استقبال فنانين ومرافقتهم خلال مختلف مراحل إنجاز مشاريعهم الفنية، بدءاً من الفكرة الأولى وصولاً إلى إنتاج العمل النهائي.")}</p></article>'
        f'<article class="card"><h3>{T("Augmented Artworks", "تطوير الأعمال الفنية باستخدام التقنيات الرقمية")}</h3><p>{T("Artists bring existing artworks that are enhanced through digital approaches and presented as part of the exhibition.", "تتيح هذه الصيغة للفنانين فرصة إعادة تقديم أعمالهم الفنية القائمة ضمن مقاربات إبداعية تستثمر الإمكانات الرقمية، من خلال توظيف أدوات وتقنيات تساهم في إثراء الأعمال وتطوير أساليب عرضها.")}</p></article>'
        "</div>"
    )
    talks = (
        f'<p>{T("A space for dialogue and reflection, bringing together different perspectives on the relationship between artistic creation, technology and cultural heritage.", "تجمع اللقاءات والنقاشات فنانين وخبراء ومختصين لفتح حوار حول التحولات التي تشهدها الممارسات الفنية في ظل التطور التكنولوجي، وعلاقة الإبداع المعاصر بالتراث الثقافي.")}</p>'
        f'<p>{T("Through an opening conference and panel discussions, the programme explores several key topics:", "ومن خلال المؤتمر الافتتاحي والجلسات الحوارية، يتناول البرنامج جملة من المحاور، أبرزها:")}</p>'
        + lst([("Digital Arts in Algeria.", "واقع الفنون الرقمية في الجزائر."), ("Artistic Creation with Artificial Intelligence.", "الإبداع الفني في ظل الذكاء الاصطناعي."),
               ("Algerian Heritage and Imaginaries.", "الفن والتكنولوجيا وآفاق الإبداع المعاصر."), ("The Production and Distribution of Digital Artworks.", "آليات إنتاج المشاريع الفنية المرئية.")])
    )
    workshops = (
        f'<p>{T("Practical workshops designed to encourage experimentation, knowledge sharing and the discovery of new creative approaches.", "تندرج الورشات التطبيقية ضمن مسعى المهرجان إلى تشجيع الممارسة الفنية وتبادل المعارف، من خلال إتاحة الفرصة للمشاركين لاكتساب أدوات ومقاربات جديدة في مجال الإبداع الرقمي.")}</p>'
        f'<p>{T("The workshops explore different aspects of contemporary digital creation, including:", "وتتناول هذه الورشات مجموعة من المواضيع، من بينها:")}</p>'
        + lst([("Developing an Artistic Concept.", "تطوير الأفكار الفنية وتحويلها إلى مشاريع إبداعية."), ("Introduction to Projection Mapping.", "التعرف على تقنيات الإسقاط الضوئي وتطبيقاتها الفنية."),
               ("Visual Creation with Artificial Intelligence.", "توظيف الذكاء الاصطناعي في الإبداع البصري."), ("Preparing an Artwork Presentation and Technical Sheet.", "إعداد الملفات التقديمية والبطاقات التقنية للأعمال الفنية.")])
    )
    return (
        head(("The Programme — FNAN", "برنامج المهرجان — FNAN"),
             ("Four ways to explore, create and connect: exhibition, creative residency, talks & meetings and workshops.",
              "أربعة محاور تجمع بين الاكتشاف والإبداع والتفاعل: المعرض الفني، الإقامة الفنية الإبداعية، اللقاءات والنقاشات وورشات العمل."), "programme", "inner")
        + header("programme", "programme") + "<main>" + page_hero(1)
        + f"""<div class="wrap">
  <p class="prose rv"><span class="intro">{T("The festival unfolds through four complementary activities, bringing together artistic discovery, creative experimentation, exchange and knowledge sharing.", "يتضمن برنامج المهرجان أربعة محاور رئيسية، تتكامل فيما بينها لتقديم تجربة فنية وثقافية متنوعة، تشمل المعارض الفنية والإقامات الإبداعية واللقاءات الحوارية والورشات التطبيقية، بما يتيح اكتشاف تجارب جديدة في مجال الفنون الرقمية والتفاعل مع مختلف أشكالها.")}</span></p>
  {act(1, ("Exhibition", "المعرض الفني"), ("A journey through artistic expression.", "فضاء يحتفي بتنوّع التعبيرات الفنية المعاصرة."), exhibition)}
  {act(2, ("Creative Residency", "الإقامة الفنية الإبداعية"), ("Where ideas become new creations.", "مرافقة الفنانين لتطوير مشاريع إبداعية جديدة."), residency)}
  {act(3, ("Talks & Meetings", "اللقاءات والنقاشات"), ("Exchange ideas. Explore new perspectives.", "فضاء للحوار وتبادل الخبرات الفنية :"), talks)}
  {act(4, ("Workshops", "ورشات العمل"), ("Learn. Experiment. Create.", "مساحات للتكوين والتجريب وتبادل الخبرات الفنية."), workshops)}
</div>
</main>"""
        + pager(1) + footer()
    )


def profiles(n, name, lines):
    cards = "".join(
        f'<article class="profile rv"><div class="portrait" aria-hidden="true"></div>'
        f'<h3>{S(name)} {i + 1:02d}</h3>'
        + "".join(f"<p>{T(*ln)}</p>" for ln in lines)
        + f'<span class="soon mono">{T("Profile coming soon", "الملف قريباً")}</span></article>'
        for i in range(n)
    )
    return f'<div class="profiles">{cards}</div>'


def chips(items):
    return "".join(f'<span class="chip">{T(*i)}</span>' for i in items)


def artists():
    en_only = """<section>
    <h2 class="sec-title rv">Artist Profiles</h2>
    <p class="label mono rv">Each artist profile will feature:</p>
    <div class="chips rv"><span class="chip">Artist's name</span><span class="chip">Portrait</span><span class="chip">Biography</span></div>
  </section>"""
    ar_only = '<section><h2 class="sec-title rv">الفنانون المشاركون</h2></section>'
    return (
        head(("The Artists — FNAN", "الفنانون — FNAN"),
             ("Discover the artists exploring new forms of expression through visual arts, audiovisual creation and digital practices.",
              "تجارب فنية تعيد تشكيل آفاق الإبداع المعاصر: الفنانون المشاركون في المهرجان."), "artists", "inner")
        + header("artists", "artists") + "<main>" + page_hero(2)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("Discover the artists exploring new forms of expression through visual arts, audiovisual creation and digital practices.", "يسلط المهرجان الضوء على الفنانين الذين يستكشفون إمكانات التعبير الجديدة من خلال الفنون البصرية والإنتاج السمعي البصري والممارسات المرئية للفنون المرئية.")}</p>
    <p>{T("Through their works and creative approaches, they contribute to a dialogue between artistic heritage, contemporary expression and emerging technologies.", "ومن خلال أعمالهم ومساراتهم الإبداعية، تتجسد رؤى فنية متنوعة تفتح حواراً بين المرجعيات التراثية والتعبيرات المعاصرة والتكنولوجيات الناشئة.")}</p>
  </div>
  {ar_only if L == "ar" else en_only}
  {profiles(8, ("Artist", "فنان"), [("Biography to come.", "النبذة قريباً.")])}
</div>
</main>"""
        + pager(2) + footer()
    )


def experts():
    topics = [("Digital Arts in Algeria", "الفنون المرئية في الجزائر"), ("Artistic Creation with Artificial Intelligence", "الإبداع الفني في ظل الذكاء الاصطناعي"),
              ("Algerian Heritage and Imaginaries", "الهوية والثقافة في الفنون المعاصرة"), ("Production and Distribution of Digital Artworks", "آفاق إنتاج الأعمال الفنية المرئية وتقديمها")]
    fields = [("Expert's name", "اسم الخبير"), ("Portrait", "صورة شخصية"), ("Professional title", "الصفة المهنية"), ("Biography", "نبذة تعريفية"),
              ("Area of expertise", "مجال الخبرة"), ("Associated conference, panel or workshop", "المحاضرة أو الحلقة أو الورشة المرتبطة")]
    fields_block = "" if L == "ar" else f'<p class="label mono rv">Each profile will feature:</p><div class="chips rv">{chips(fields)}</div>'
    return (
        head(("The Experts — FNAN", "الخبراء — FNAN"),
             ("Meet the artists, experts and cultural professionals contributing to the festival's programme.",
              "خبرات ورؤى تثري النقاش حول الفن والتكنولوجيا: الخبراء المشاركون في برنامج المهرجان."), "experts", "inner")
        + header("experts", "experts") + "<main>" + page_hero(3)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("Meet the artists, experts and cultural professionals contributing to the festival's programme through conferences, panel discussions and practical workshops.", "يجمع المهرجان نخبة من الفنانين والخبراء والمهنيين في المجال الثقافي، للمساهمة في إثراء برنامجه من خلال المؤتمرات واللقاءات الحوارية والورشات التطبيقية.")}</p>
    <p>{T("Their perspectives open up conversations around digital creation, artistic experimentation, cultural heritage and the evolving relationship between art and technology.", "وتتيح هذه اللقاءات تبادل المعارف والخبرات وطرح رؤى متعددة حول تطور الفنون المرئية، والتجريب الفني، والتحولات التي تعرفها العلاقة بين الفن والتكنولوجيا.")}</p>
  </div>
  <section>
    <p class="label mono rv">{T("Key topics", "المحاور الرئيسية")}</p>
    <div class="chips rv">{chips(topics)}</div>
  </section>
  <section>
    <h2 class="sec-title rv">{T("Meet the Experts", "تعرّفوا على الخبراء")}</h2>
    {fields_block}
  </section>
  {profiles(6, ("Expert", "خبير"), [("Title and expertise to come.", "الصفة ومجال الخبرة قريباً.")])}
</div>
</main>"""
        + pager(3) + footer()
    )


def visit():
    return (
        head(("Visit the Festival — FNAN", "زيارة المهرجان — FNAN"),
             ("19–22 November 2026 at Dar Abd-el-Tif and the National Museum of Fine Arts of Algiers.",
              "19–22 نوفمبر 2026 في دار عبد اللطيف والمتحف الوطني للفنون الجميلة، الجزائر العاصمة."), "visit", "inner")
        + header("visit", "visit") + "<main>" + page_hero(4)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("Join us for an encounter between visual arts, creative experimentation and digital practices.", "يستقبل المهرجان جمهوره ضمن برنامج يجمع بين الفنون المرئية والتجارب الإبداعية المعاصرة، من خلال عروض فنية ولقاءات وورشات تتيح التعرّف على اتجاهات جديدة في المشهد الفني.")}</p>
    <p>{T("The festival invites visitors to explore artistic works, discover new forms of expression and take part in conversations and creative experiences.", "كما يوفّر فرصة للقاء الفنانين والمتخصصين، وتبادل الأفكار حول التحولات التي يشهدها الإبداع الفني اليوم.")}</p>
  </div>
  <section>
    <h2 class="sec-title rv">{T("Festival Information", "معلومات المهرجان")}</h2>
    <div class="info">
      <article class="card rv"><span class="n mono">{T("Dates", "التواريخ")}</span><p class="big">{T("19 – 22 November 2026", "19 – 22 نوفمبر 2026")}</p></article>
      <article class="card rv"><span class="n mono">{T("Locations", "فضاءات الاحتضان")}</span>
        <p class="big">{T("Dar Abd-el-Tif, Algiers.", "دار عبد اللطيف، الجزائر العاصمة.")}</p>
        <p class="big">{T("National Museum of Fine Arts of Algiers.", "المتحف الوطني للفنون الجميلة، الجزائر العاصمة.")}</p></article>
    </div>
  </section>
  <section class="signature rv">
    <h2>{T("Algerian Imaginaries. Creating in the digital age.", "الإبداع في العصر الرقمي.")}</h2>
    <p>{T("A space to discover, experiment, exchange and imagine new possibilities for artistic creation.", "فضاء للتفاعل وتبادل المعارف وفتح آفاق جديدة أمام الممارسات الفنية المعاصرة.")}</p>
  </section>
</div>
</main>"""
        + pager(4) + footer()
    )


def press():
    def doc(n, title, desc, meta, thumb, href, fname, cta):
        return (
            f'<article class="doc rv"><a class="doc-thumb" href="{A(href)}" target="_blank" rel="noopener" aria-label="{S(title)}">'
            f'<img src="{A(thumb)}" alt="" loading="lazy"></a>'
            f'<div class="doc-body"><span class="n mono">{n}</span><h3>{S(title)}</h3><p>{S(desc)}</p>'
            f'<p class="meta mono">{S(meta)}</p>'
            f'<a class="btn mono" href="{A(href)}" download="{fname}">{S(cta)} {ARROW_DL}</a></div></article>'
        )

    docs = (
        doc("01", ("Press Kit", "الملف الصحفي"),
            ("Discover the festival's vision, concept, theme, objectives, programme, participating artists and speakers, along with all the key information about this edition.",
             "وثيقة تعريفية تتناول رؤية المهرجان وأهدافه وموضوع هذه الدورة، إلى جانب برنامجه الفني ومختلف الأنشطة والمحاور التي يتضمنها."),
            ("PDF · Arabic · 7 pages", "PDF · بالعربية · 7 صفحات"), "assets/press/thumb-dossier.webp", "assets/press/fnan-dossier-de-presse.pdf",
            "FNAN-press-kit.pdf", ("Download the Press kit", "تحميل الملف الصحفي"))
        + doc("02", ("Press Release", "البيان الصحفي"),
              ("Read the festival's official announcements and updates.",
               "البيان الرسمي للمهرجان، المتضمن لأبرز المعلومات والتفاصيل المتعلقة بهذه الدورة، والموجه إلى وسائل الإعلام والجهات الصحفية."),
              ("PDF · Arabic · 1 page", "PDF · بالعربية · صفحة واحدة"), "assets/press/thumb-communique.webp", "assets/press/fnan-communique-de-presse.pdf",
              "FNAN-press-release.pdf", ("Download the Press Release", "تحميل البيان الصحفي"))
        + doc("03", ("Key visual", "الصورة الرسمية للمهرجان"),
              ("The official poster of the festival, for editorial use.", "الملصق الرسمي للمهرجان، للاستخدام الصحفي."),
              ("JPG · 1443 × 2048 px", "JPG · 1443 × 2048 بكسل"), "assets/press/thumb-kv.webp", "assets/press/fnan-key-visual.jpg",
              "FNAN-key-visual.jpg", ("Download the key visual", "تحميل الصورة الرسمية"))
    )
    contact = f"""<article class="card contact rv">
      <span class="n mono">04</span><h3>{T("Press contact", "الاتصال الصحفي")}</h3>
      <p>{T("Communication & Media Unit. For media enquiries, interview requests and coverage coordination.", "خلية الاتصال والإعلام. للاستفسارات الإعلامية وطلبات المقابلات والتنسيق بشأن التغطية الصحفية.")}</p>
      <ul class="clist">
        <li><span class="mono">{T("Email", "البريد الإلكتروني")}</span><a href="mailto:{MAIL}" dir="ltr">{MAIL}</a></li>
        <li><span class="mono">{T("Phone", "الهاتف")}</span><a href="tel:+213553486929" dir="ltr">0553 48 69 29</a></li>
        <li><span class="mono">{T("Social", "صفحات التواصل")}</span><span><a href="{IG}" target="_blank" rel="noopener">{T("Instagram", "إنستغرام")}</a> · <a href="{FB}" target="_blank" rel="noopener">{T("Facebook", "فيسبوك")}</a></span></li>
      </ul>
    </article>"""
    note = "" if L == "ar" else '<p class="note mono rv">The press documents are provided in Arabic.</p>'
    return (
        head(("Press & Media — FNAN", "الصحافة والإعلام — FNAN"),
             ("Press resources for the National Cultural Festival of Plastic and Visual Arts: press kit, press release, key visual and media contact.",
              "الملف الصحفي والبيان الصحفي والصورة الرسمية وبيانات الاتصال الصحفي الخاصة بالمهرجان."), "press", "inner")
        + header("press", "press") + "<main>" + page_hero(5)
        + f"""<div class="wrap">
  <div class="cols prose rv">
    <p>{T("The National Festival of Digital Arts welcomes media professionals and journalists to discover, cover and share the stories shaping this edition.", "يتيح المهرجان الوطني للفنون التشكيلية والفنون الرقمية للصحفيين وممثلي وسائل الإعلام مجموعة من الوثائق الرسمية الخاصة بهذه النسخة، والتعرّف على رؤيته وأهدافه وموضوعه، إلى جانب برنامجه الفني ومختلف الأنشطة المندرجة ضمنه.")}</p>
    <p>{T("This section provides access to the festival's official Press Kit, featuring key information about its vision, concept, programme and participants, as well as its official Press Release, presenting the festival and its key highlights.", "ويضم هذا القسم الملف الصحفي، الذي يقدم عرضاً تعريفياً بالمهرجان ومختلف محاوره، إلى جانب البيان الصحفي الذي يتناول أبرز المعلومات المتعلقة بهذه الدورة.")}</p>
  </div>
  <section>
    {note}
    <div class="docs">{docs}</div>
  </section>
  <section>{contact}</section>
</div>
</main>"""
        + pager(5) + footer()
    )


PAGE_FUNCS = [("index", index), ("about", about), ("programme", programme), ("artists", artists),
              ("experts", experts), ("visit", visit), ("press", press)]

if __name__ == "__main__":
    (ROOT / "ar").mkdir(exist_ok=True)
    for lang in ("en", "ar"):
        L = lang
        for name, fn in PAGE_FUNCS:
            out = ROOT / ("ar" if lang == "ar" else "") / f"{name}.html"
            out.write_text(fn(), encoding="utf-8")
            print("écrit", out.relative_to(ROOT))
