"""CityRateBook SEO config. INDEXABLE gates robots meta and sitemap for the whole site.
City pages also need to pass the thin-page gate (3+ local data points, 2+ local factors, 300+ non-template words)."""
import os, re, shutil, sys
INDEXABLE = False
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT); import seo
LOGOS = "/workspace/atulit-logos/cityratebook"

def hook(ctx):
    p, s, paths = ctx["path"], ctx["soup"], ctx["paths"]
    seg = p.strip("/").split("/") if p else []
    h1 = ctx["h1"]
    if p == "": return dict(titles=["Local Home Service Price Guides (2026 Estimates)", "Local Home Service Price Guides"])
    if len(seg) == 3 and seg[1] == "cost":
        g = s.find("meta", attrs={"name": "x-index-gate"})
        ok = bool(g and "pass=True" in g["content"])
        svc, city = seg[0], seg[2]
        rel = [f"{svc}/cost/", f"cities/{city}/"] + [q for q in paths if q.startswith(f"{svc}/cost/") and q.count("/") == 3 and q != p] + [q for q in paths if q.endswith(f"/cost/{city}/") and q != p] + ["methodology/"]
        nm, cy = h1.split(" Cost in ")[0], h1.split(" Cost in ")[1].replace(" (2026 Estimates)", "")
        return dict(titles=[h1, h1.replace(" (2026 Estimates)", " (2026)"), h1.replace(" (2026 Estimates)", "")], index=ok, related=rel[:8],
                    desc=f"{nm} cost in {cy}: estimate ranges by job type, local labor, permit and seasonal factors, with sources and the date we last checked.")
    if len(seg) == 2 and seg[1] == "cost":
        nm = h1.split(" Cost")[0]
        return dict(titles=[h1], desc=f"How much do {nm.lower()} cost? National estimate ranges by job type, the factors that move the price, and city guides, with sources and dates.")
    if seg[0] == "cities" and len(seg) == 2:
        return dict(titles=[h1, h1.replace(" (2026 Estimates)", " (2026)")])
    return dict(titles=[h1])

def build():
    for a, b in [("option-b-icon.svg", "favicon.svg"), ("option-b-icon-512.png", "option-b-icon-512.png")]:
        shutil.copy(f"{LOGOS}/{a}", f"{ROOT}/img/brand/{b}")
    shutil.copy(f"{ROOT}/img/brand/option-b-icon-32.png", f"{ROOT}/img/brand/favicon-32.png")
    shutil.copy(f"{ROOT}/img/brand/option-b-icon-180.png", f"{ROOT}/img/brand/apple-touch-icon.png")
    site = seo.Site(ROOT, "CityRateBook", "cityratebook.com", "service-price-guide-prototype", INDEXABLE, "Oct 13, 2026", "2026-10-13",
        "Local service price guides. Funded by matched quote requests and sponsored partner links, never by what a price says.",
        f"{LOGOS}/option-b-wordmark-1200.png", "img/brand/option-b-icon-512.png",
        ["Estimates from cited sources, not quotes.", "Last checked Oct 13, 2026.", "From CityRateBook.", "Ranges with sources.", "Free local quotes."], hook)
    return seo.run(site)
if __name__ == "__main__": build()
