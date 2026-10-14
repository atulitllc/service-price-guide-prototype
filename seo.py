"""Shared SEO post-build step for Atulit static prototypes.
Run after the site's HTML exists. Idempotent. Driven by site config (seo_site.py)."""
import os, re, json, html as H
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Comment
from PIL import Image

DROP_TYPES = {"Organization", "WebSite", "BreadcrumbList", "AggregateRating", "Review", "Product"}

def norm(s): return re.sub(r"\s+", " ", (s or "")).strip()

class Site:
    def __init__(self, root, brand, apex, repo, indexable, updated, updated_iso, disclosure,
                 og_logo, org_logo, fillers, hook=None, about_tpl="about/", extra_pages=None):
        self.__dict__.update(locals()); del self.__dict__["self"]
        self.origin = "https://" + apex

def rel(path): return "../" * path.count("/")

def pages_of(root):
    out = []
    for d, ds, fs in os.walk(root):
        ds[:] = [x for x in ds if not x.startswith(".")]
        if "index.html" in fs:
            p = os.path.relpath(d, root)
            out.append("" if p == "." else p.replace(os.sep, "/") + "/")
    return sorted(out)

def load(root, path):
    return BeautifulSoup(open(os.path.join(root, path, "index.html"), encoding="utf-8").read(), "html.parser")

def save(root, path, soup, name="index.html"):
    os.makedirs(os.path.join(root, path), exist_ok=True)
    s = str(soup)
    if not s.lower().startswith("<!doctype"): s = "<!doctype html>" + s
    open(os.path.join(root, path, name), "w", encoding="utf-8").write(s)

def h1_text(soup):
    h = soup.find("h1"); return norm(h.get_text(" ")) if h else ""

def crumbs_el(soup):
    return soup.find(attrs={"aria-label": "Breadcrumb"}) or soup.find(class_=re.compile(r"crumb"))

def between_header_footer(soup):
    body = soup.body; hd = body.find("header", recursive=False) or body.find("header")
    ft = body.find("footer")
    nodes, on = [], False
    for c in list(body.children):
        if c is hd: on = True; continue
        if c is ft: break
        if on and getattr(c, 'name', None): nodes.append(c)
    return hd, ft, nodes

def make_page_from(site, path, title, body_html):
    """Clone the about/ page shell (header, footer, head) for a new depth-1 page."""
    soup = load(site.root, site.about_tpl)
    hd, ft, nodes = between_header_footer(soup)
    for n in nodes: n.extract()
    new = BeautifulSoup(f'<main class="wrap w seo-page" data-seo="page"><nav class="crumbs crumb" aria-label="Breadcrumb"><a href="../">Home</a> <span>/</span> <span aria-current="page">{H.escape(title)}</span></nav>{body_html}</main>', "html.parser")
    ft.insert_before(new)
    for s in soup.find_all("script", type="application/ld+json"): s.decompose()
    m = soup.new_tag("meta", attrs={"name": "seo-generated", "content": "1"}); soup.head.append(m)
    return soup

def visible_text(soup):
    s = BeautifulSoup(str(soup.body), "html.parser")
    for t in s(["script", "style", "noscript"]): t.decompose()
    return norm(s.get_text(" ")).lower()

def fit_desc(base, fillers, lo=140, hi=160):
    base = norm(base).replace("\u2014", ",").replace("\u2013", "-")
    if len(base) > hi:
        sents = re.split(r"(?<=[.!?])\s+", base); acc = ""
        for s in sents:
            if len((acc + " " + s).strip()) <= hi: acc = (acc + " " + s).strip()
            else: break
        if len(acc) < 60:
            acc = base[:hi - 1].rsplit(" ", 1)[0].rstrip(",;:") + "."
        base = acc
    if base and base[-1] not in ".!?": base += "."
    for f in fillers:
        if len(base) >= lo: break
        if len(base) + 1 + len(f) <= hi: base = (base + " " + f).strip()
    i = 0
    while len(base) < lo and i < 3:  # last resort, still true statements
        for f in fillers:
            if f not in base and len(base) + 1 + len(f) <= hi: base += " " + f
        i += 1
    return base

def pick_title(cands, brand, maxlen=60):
    for c in cands:
        if len(f"{c} | {brand}") <= maxlen: return f"{c} | {brand}"
    return f"{cands[-1]} | {brand}"

def img_size(fp):
    try:
        if fp.endswith(".svg"):
            t = open(fp).read(3000)
            m = re.search(r'viewBox="\s*[\d.-]+[ ,]+[\d.-]+[ ,]+([\d.]+)[ ,]+([\d.]+)', t)
            if m: return float(m.group(1)), float(m.group(2))
            return None
        with Image.open(fp) as im: return im.size
    except Exception: return None

def fix_images(site, path, soup):
    for img in soup.find_all("img"):
        if not img.get("alt") and img.get("alt") != "":
            img["alt"] = ""
        src = (img.get("src") or "").split("?")[0]
        if src and not src.startswith(("http", "data:")) and not (img.get("width") and img.get("height")):
            sz = img_size(os.path.normpath(os.path.join(site.root, path, src)))
            if sz:
                w, h = sz
                if img.get("height") and not img.get("width"):
                    hh = float(img["height"]); img["width"] = str(round(hh * w / h))
                elif img.get("width") and not img.get("height"):
                    ww = float(img["width"]); img["height"] = str(round(ww * h / w))
                else: img["width"], img["height"] = str(round(w)), str(round(h))
        if img.find_parent("header") and not img.find_parent("main"): img["loading"] = "eager"  # above-the-fold logo
        elif img.get("loading") != "eager": img["loading"] = "lazy"
        img["decoding"] = "async"

def run(site):
    root = site.root; hook = site.hook or (lambda ctx: {})
    # 1. standard pages
    std = {
      "privacy/": ("Privacy policy", f"<h1>Privacy policy</h1><p>Last updated {site.updated}.</p><p>{site.brand} is a prototype by Atulit LLC. It has no user accounts, no analytics and no advertising trackers.</p><p>Some features save small preferences or form entries in your browser's local storage. That data stays on your device and is never sent to us. You can clear it at any time in your browser settings.</p><p>Outbound links, including affiliate links marked sponsored, take you to other sites with their own privacy policies.</p><p>Questions: see our <a href=\"../contact/\">contact page</a>.</p>"),
      "contact/": ("Contact", f"<h1>Contact {H.escape(site.brand)}</h1><p>Last updated {site.updated}.</p><p>{site.brand} is run by Atulit LLC. This is an early prototype and a public contact inbox is not set up yet.</p><p>When it is, the address will be listed here. Until then, you can read <a href=\"../about/\">about us</a> and our <a href=\"../privacy/\">privacy policy</a>.</p>"),
    }
    for p, (t, b) in std.items():
        f = os.path.join(root, p, "index.html")
        if not os.path.exists(f) or 'name="seo-generated"' in open(f).read():
            save(root, p, make_page_from(site, p, t, b))
    for p, (t, b) in (site.extra_pages or {}).items():
        save(root, p, make_page_from(site, p, t, b))
    paths = pages_of(root)
    soups = {p: load(root, p) for p in paths}
    ctxs = {}
    for p, s in soups.items():
        ctx = dict(path=p, soup=s, h1=h1_text(s), site=site, soups=soups, paths=paths)
        ctxs[p] = ctx
    metas = {p: hook(ctxs[p]) or {} for p in paths}   # hook may edit soup content
    for p in paths: ctxs[p]["h1"] = h1_text(soups[p])
    titles = {p: metas[p].get("h1") or ctxs[p]["h1"] for p in paths}
    descs_seen = {}
    report = []
    for p in paths:
        s, m = soups[p], metas[p]
        head = s.head
        topic = m.get("topic") or titles[p] or site.brand
        if m.get("h1") and s.find("h1"):
            s.find("h1").clear(); s.find("h1").append(m["h1"]); titles[p] = m["h1"]
        h1s = s.find_all("h1")
        for extra in h1s[1:]: extra.name = "h2"
        # remove old tags
        for t in head.find_all("meta"):
            if t.get("name") in ("robots", "description", "twitter:card", "twitter:title", "twitter:description", "twitter:image") or (t.get("property") or "").startswith("og:"):
                t.decompose()
        for t in head.find_all("link", rel=True):
            if "canonical" in t["rel"]: t.decompose()
        if not s.html.get("lang"): s.html["lang"] = "en"
        if not head.find("meta", charset=True): head.insert(0, s.new_tag("meta", charset="utf-8"))
        if not head.find("meta", attrs={"name": "viewport"}):
            head.insert(1, s.new_tag("meta", attrs={"name": "viewport", "content": "width=device-width,initial-scale=1"}))
        title = pick_title(m.get("titles") or [topic], site.brand)
        if not head.title: head.append(s.new_tag("title"))
        head.title.string = title
        lede = ""
        main = s.find("main") or s.body
        for para in main.find_all("p"):
            if para.find_parent(class_=re.compile("sample|crumb|banner")): continue
            tx = norm(para.get_text(" "))
            if len(tx.split()) >= 8 and not tx.startswith("Last updated"): lede = tx; break
        base = m.get("desc") or lede or topic
        if m.get("desc_prefix"): base = m["desc_prefix"] + " " + base
        d = fit_desc(base, m.get("fillers") or site.fillers)
        if d in descs_seen:
            d = fit_desc(topic + ". " + base, m.get("fillers") or site.fillers)
        descs_seen[d] = p
        canon = site.origin + "/" + (m.get("canonical", p))
        page_index = m.get("index", True)
        robots = "index,follow" if (site.indexable and page_index) else "noindex,follow"
        tags = [("meta", {"name": "description", "content": d}), ("meta", {"name": "robots", "content": robots}),
                ("link", {"rel": "canonical", "href": canon}),
                ("meta", {"property": "og:type", "content": "website" if p == "" else "article" if m.get("article") else "website"}),
                ("meta", {"property": "og:site_name", "content": site.brand}),
                ("meta", {"property": "og:title", "content": title}), ("meta", {"property": "og:description", "content": d}),
                ("meta", {"property": "og:url", "content": canon}), ("meta", {"property": "og:image", "content": site.origin + "/img/og.png"}),
                ("meta", {"property": "og:image:width", "content": "1200"}), ("meta", {"property": "og:image:height", "content": "630"}),
                ("meta", {"property": "og:image:alt", "content": site.brand + " logo"}),
                ("meta", {"name": "twitter:card", "content": "summary_large_image"}), ("meta", {"name": "twitter:title", "content": title}),
                ("meta", {"name": "twitter:description", "content": d}), ("meta", {"name": "twitter:image", "content": site.origin + "/img/og.png"})]
        anchor = head.title
        for name, attrs in tags:
            t = s.new_tag(name, attrs=attrs); anchor.insert_after(t); anchor = t
        # icons
        r = rel(p)
        for t in head.find_all("link", rel=True):
            if set(t["rel"]) & {"icon", "apple-touch-icon"}: t.decompose()
        for a in [{"rel": "icon", "href": r + "img/brand/favicon.svg", "type": "image/svg+xml"}, {"rel": "icon", "href": r + "img/brand/favicon-32.png", "sizes": "32x32"},
                  {"rel": "apple-touch-icon", "href": r + "img/brand/apple-touch-icon.png", "sizes": "180x180"}]:
            anchor.insert_after(s.new_tag("link", attrs=a))
        # schema
        text = visible_text(s)
        keep = []
        for sc in s.find_all("script", type="application/ld+json"):
            try: data = json.loads(sc.string or "")
            except Exception: data = []
            sc.decompose()
            for x in (data if isinstance(data, list) else [data]):
                ty = x.get("@type")
                if ty in DROP_TYPES: continue
                if ty == "FAQPage":
                    x["mainEntity"] = [q for q in x.get("mainEntity", []) if norm(q["name"]).lower() in text and norm(BeautifulSoup(q["acceptedAnswer"]["text"], "html.parser").get_text()).lower() in text]
                    if not x["mainEntity"]: continue
                if ty == "HowTo" and not all(norm(st["text"]).lower() in text for st in x.get("step", [])): continue
                if ty == "ItemList":
                    for it in x.get("itemListElement", []):
                        if it.get("url"): it["url"] = it["url"].replace("https://atulitllc.github.io/" + site.repo + "/", site.origin + "/")
                    if not all(norm(it.get("name", "")).lower() in text for it in x.get("itemListElement", [])): continue
                if m.get("schema_filter") and not m["schema_filter"](x): continue
                keep.append(x)
        keep += m.get("schema_add", [])
        if p == "":
            keep = [{"@context": "https://schema.org", "@type": "WebSite", "name": site.brand, "url": site.origin + "/"},
                    {"@context": "https://schema.org", "@type": "Organization", "name": site.brand, "url": site.origin + "/", "logo": site.origin + "/" + site.org_logo}] + keep
        else:
            ce = crumbs_el(s)
            if ce is None:
                main0 = s.find("main") or between_header_footer(s)[2][0]
                ce = BeautifulSoup(f'<nav class="crumbs crumb" aria-label="Breadcrumb" data-seo="crumbs"><a href="{r}">Home</a> <span>/</span> <span aria-current="page">{H.escape(titles[p])}</span></nav>', "html.parser").nav
                main0.insert(0, ce)
            items = []
            for a in ce.find_all(["a", "span", "b"]):
                if a.name == "a":
                    tgt = urlparse(urljoin("https://x/" + p, a["href"])).path.lstrip("/")
                    if tgt.endswith("index.html"): tgt = tgt[:-10]
                    items.append((norm(a.get_text(" ")), site.origin + "/" + tgt))
                elif a.get("aria-current") or a.name == "b" or (a is ce.find_all(["a", "span", "b"])[-1] and norm(a.get_text()) not in ("/", "")):
                    items.append((norm(a.get_text(" ")), canon))
            items = [i for i in items if i[0] and i[0] != "/"]
            keep = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}] + keep
        for x in keep:
            x.setdefault("@context", "https://schema.org")
            sc = s.new_tag("script", type="application/ld+json"); sc.string = json.dumps(x, ensure_ascii=False); head.append(sc)
        # related links
        for old in s.find_all(attrs={"data-seo": "related"}): old.decompose()
        relp = m.get("related")
        if relp:
            lis = "".join(f'<li><a href="{r}{q}">{H.escape(titles.get(q) or q)}</a></li>' for q in relp[:8] if q in soups)
            blk = BeautifulSoup(f'<section class="seo-related" data-seo="related" style="margin:28px 0"><h2>Related</h2><ul style="columns:2;padding-left:18px;line-height:1.9">{lis}</ul></section>', "html.parser")
            (s.find("main") or between_header_footer(s)[2][-1]).append(blk)
        # footer disclosure + updated date
        for old in s.find_all(attrs={"data-seo": "foot"}): old.decompose()
        ft = s.find("footer")
        if ft:
            ftxt = norm(ft.get_text(" "))
            bits = []
            if site.disclosure[:40] not in ftxt: bits.append(site.disclosure)
            if "Last updated" not in ftxt: bits.append(f"Last updated {m.get('updated', site.updated)}.")
            if bits:
                tgt = ft.find(class_=re.compile("wrap|w$")) or ft
                tgt.append(BeautifulSoup(f'<p class="seo-foot" data-seo="foot" style="font-size:13px;color:#6b7280;margin-top:12px">{" ".join(bits)} <a href="{r}privacy/">Privacy</a> · <a href="{r}contact/">Contact</a></p>', "html.parser"))
            elif not ft.find("a", href=re.compile(r"contact/$")):
                tgt = ft.find(class_=re.compile("wrap|w$")) or ft
                tgt.append(BeautifulSoup(f'<p class="seo-foot" data-seo="foot" style="font-size:13px;color:#6b7280;margin-top:12px"><a href="{r}privacy/">Privacy</a> · <a href="{r}contact/">Contact</a></p>', "html.parser"))
        fix_images(site, p, s)
        # dash check in text
        for t in s.find_all(string=True):
            if isinstance(t, Comment) or t.parent.name in ("script", "style"): continue
            if "\u2014" in t or "\u2013" in t: t.replace_with(t.replace("\u2014", ",").replace("\u2013", "-"))
        save(root, p, s)
        report.append(dict(path=p, title=title, tl=len(title), dl=len(d), index=page_index, lastmod=m.get("lastmod", site.updated_iso), h1=len(s.find_all("h1"))))
    # 404
    s = load(root, site.about_tpl)
    hd, ft, nodes = between_header_footer(s)
    for n in nodes: n.extract()
    ft.insert_before(BeautifulSoup(f'<main class="wrap w seo-page" style="padding:48px 0"><h1>Page not found</h1><p>Sorry, this page does not exist or has moved.</p><p><a href="../">Go to the {H.escape(site.brand)} home page</a> · <a href="../about/">About</a> · <a href="../contact/">Contact</a></p></main>', "html.parser"))
    for t in s.find_all("script", type="application/ld+json"): t.decompose()
    for t in s.head.find_all("link", rel=True):
        if "canonical" in t["rel"]: t.decompose()
    for t in s.head.find_all("meta"):
        if t.get("name") in ("robots", "description", "seo-generated") or (t.get("property") or "").startswith(("og:",)) or (t.get("name") or "").startswith("twitter:"): t.decompose()
    s.head.title.string = f"Page not found | {site.brand}"
    s.head.title.insert_after(s.new_tag("meta", attrs={"name": "robots", "content": "noindex,follow"}))
    base = BeautifulSoup(f"<script>document.write('<base href=\"'+(location.hostname.endsWith('github.io')?'/{site.repo}/':'/')+'about/\">')</script>", "html.parser")
    s.head.insert(0, base)
    s.head.insert(0, s.new_tag("meta", charset="utf-8"))
    for t in s.head.find_all("meta", charset=True)[1:]: t.decompose()
    save(root, "", s, "404.html")
    # robots + sitemap (gated on INDEXABLE)
    open(os.path.join(root, "robots.txt"), "w").write("User-agent: *\nAllow: /\n" + (f"\nSitemap: {site.origin}/sitemap.xml\n" if site.indexable else ""))
    sm = os.path.join(root, "sitemap.xml")
    entries = [r_ for r_ in report if r_["index"]]
    if site.indexable:
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{site.origin}/{e['path']}</loc><lastmod>{e['lastmod']}</lastmod></url>\n" for e in entries) + "</urlset>\n"
        open(sm, "w").write(xml)
    elif os.path.exists(sm): os.remove(sm)
    # og image + icons
    os.makedirs(os.path.join(root, "img/brand"), exist_ok=True)
    og = Image.new("RGB", (1200, 630), "white")
    lg = Image.open(site.og_logo).convert("RGBA"); lg.thumbnail((960, 320))
    og.paste(lg, ((1200 - lg.width) // 2, (630 - lg.height) // 2), lg)
    og.save(os.path.join(root, "img/og.png"), optimize=True)
    print(f"[{site.brand}] pages={len(report)} indexable_candidates={len(entries)} sitemap={'written' if site.indexable else 'not written (INDEXABLE=False)'}")
    bad = [r_ for r_ in report if not (140 <= r_["dl"] <= 160) or r_["tl"] > 66 or r_["h1"] != 1]
    for b in bad: print("  CHECK", b)
    titles_all = [r_["title"] for r_ in report]
    dup = {t for t in titles_all if titles_all.count(t) > 1}
    if dup: print("  DUP TITLES", dup)
    return report
