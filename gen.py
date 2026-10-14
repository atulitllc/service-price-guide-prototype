import os,json,re
R=os.path.dirname(os.path.abspath(__file__)); D="Oct 13, 2026"; BR="CityRateBook"
import sys; sys.path.insert(0,R)
from atulit_gfx import icon,flogo,hero,THEME_HEAD,toggle,CREDIT,install_css
SI={"plumbers":"wrench","electricians":"zap","movers":"truck","house-cleaners":"sparkles","pet-sitters":"paw-print","hvac":"thermometer","handyman":"hammer","painters":"paintbrush"}
S={ # slug:(name,unit,lo,hi,mid,jobs,factors,icon,color)
"plumbers":("Plumbers","per job",150,450,275,[("Fix a leaky faucet",125,250),("Unclog a drain",150,350),("Replace a toilet",350,800),("Water heater install",1200,3200),("Repipe a bathroom",1500,4500)],["Emergency or after-hours calls","Pipe access behind walls or floors","Fixture and part quality","Permit needs for gas or water heaters"],"PL","#2563eb"),
"electricians":("Electricians","per job",160,520,310,[("Replace an outlet",120,260),("Install a ceiling fan",180,450),("Add a dedicated circuit",350,900),("EV charger install",800,2200),("Panel upgrade to 200A",1800,4500)],["Panel capacity and age","Wire runs through finished walls","Permit and inspection fees","Licensed master vs journeyman rates"],"EL","#d97706"),
"movers":("Movers","per move",400,1800,950,[("Studio, local",350,800),("2 bedroom, local",800,1900),("3 bedroom, local",1300,2800),("Packing service add on",300,1200),("Long distance, 2 bedroom",2800,6500)],["Distance and stairs","Crew size and hours","Peak season and weekends","Packing materials"],"MV","#7c3aed"),
"house-cleaners":("House cleaners","per visit",120,300,190,[("Standard clean, 1 bed",90,160),("Standard clean, 3 bed",150,260),("Deep clean, 3 bed",250,480),("Move out clean",280,550),("Recurring biweekly",110,220)],["Home size and condition","Deep vs standard clean","Recurring discount","Supplies included"],"HC","#0891b2"),
"pet-sitters":("Pet sitters","per visit",20,45,30,[("30 min drop in",18,35),("Dog walk, 30 min",18,32),("Overnight stay",60,120),("Multiple pets add on",5,15),("Holiday rate",30,60)],["Number of pets","Visit length","Holidays","Medication needs"],"PS","#16a34a"),
"hvac":("HVAC","per job",200,700,420,[("Tune up",90,200),("Diagnose and repair",200,700),("Replace a thermostat",150,450),("Furnace replacement",3500,7500),("Central AC replacement",5000,11000)],["System size in tons or BTU","Efficiency rating (SEER2)","Ductwork condition","Seasonal demand"],"HV","#dc2626"),
"handyman":("Handyman","per hour",60,120,85,[("Mount a TV",100,250),("Assemble furniture",80,200),("Patch drywall",120,350),("Hang doors",150,400),("Half day of small jobs",250,500)],["Hourly minimums","Materials","Travel fee","Job mix"],"HM","#ea580c"),
"painters":("Painters","per room",350,900,600,[("Accent wall",200,450),("Bedroom, walls only",350,800),("Kitchen cabinets",2500,6500),("Interior, 2,000 sq ft",4000,9000),("Exterior, 1 story",3000,7500)],["Wall prep and repairs","Ceiling height","Paint grade","Trim and doors"],"PT","#db2777"),
}
C={ # slug:(name,state,mult,labor,permits,season,points)
"boston-ma":("Boston","MA",1.28,"Union scale and Massachusetts licensing keep hourly trade rates high, often $95 to $160 for licensed work.","Massachusetts requires licensed plumbers and electricians for most work, and Boston Inspectional Services issues permits for water heaters, panels, and new circuits.","Winter brings heating calls and frozen pipe emergencies; September 1 lease turnover drives moving and cleaning demand.","older triple deckers with tight access and knob and tube wiring"),
"austin-tx":("Austin","TX",1.04,"A fast growing metro with many new contractors; licensed trade rates commonly run $80 to $130 per hour.","Texas licenses plumbers (TSBPE) and electricians (TDLR); the City of Austin requires permits for water heaters, HVAC changeouts, and panel work.","Summer heat makes June to September peak AC season, with longer waits for HVAC repairs.","newer suburban builds with attic HVAC and slab plumbing"),
"denver-co":("Denver","CO",1.12,"Rates sit above national averages, about $85 to $140 per hour for licensed trades.","Colorado licenses plumbers and electricians through DORA; Denver Community Planning and Development requires permits for most mechanical work.","Cold snaps lift furnace and pipe calls in winter, while spring hail season ties up roofers and handymen.","altitude adjusted furnace sizing and 1950s ranch homes"),
}
CS=["plumbers","electricians","hvac"]
def esc(s):return s.replace("&","&amp;").replace("<","&lt;")
def m(x):return f"${x:,.0f}"
CSS=open("/dev/null").read()
def page(path,title,desc,body,crumbs,extra_ld=[],gate=None):
    depth=path.count("/"); rel="../"*depth
    url="https://cityratebook.com/"+path
    bl={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":"https://cityratebook.com/"+u} for i,(n,u) in enumerate(crumbs)]}
    org={"@context":"https://schema.org","@type":"Organization","name":BR+" by Atulit","url":"https://cityratebook.com/","logo":"https://cityratebook.com/img/brand/option-b-icon-512.png"}
    lds="".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in [bl,org]+extra_ld)
    gm=f'<meta name="x-index-gate" content="{gate}">' if gate else ""
    cr="".join((f'<a href="{rel}{u}">{esc(n)}</a><span>/</span>' if i<len(crumbs)-1 else f'<b>{esc(n)}</b>') for i,(n,u) in enumerate(crumbs))
    h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | {BR}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="noindex, nofollow">{THEME_HEAD}{gm}
<link rel="canonical" href="{url}"><link rel="icon" href="{rel}img/brand/option-b-icon.svg" type="image/svg+xml"><link rel="icon" href="{rel}img/brand/option-b-icon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="{rel}img/brand/option-b-icon-180.png"><link rel="stylesheet" href="{rel}assets/site.css">{lds}</head><body>
<div class="banner">Prototype. Figures come from BLS wage data and HomeAdvisor cost guides, with sources on each page. Estimates, not quotes. Nothing you enter is sent.</div>
<header class="top"><div class="wrap nav"><a class="logo" href="{rel}"><img src="{rel}img/brand/option-b-wordmark.svg" alt="CityRateBook" height="30"></a>
<nav><a href="{rel}#services">{icon("wrench",16)}Services</a><a href="{rel}#cities">{icon("map-pin",16)}Cities</a><a href="{rel}methodology/">{icon("calculator",16)}How we estimate</a><a class="btn sm" href="{rel}plumbers/cost/boston-ma/#quote">{icon("receipt",16)}Get quotes</a>{toggle()}</nav></div></header>
<main>{'' if path=='' else f'<div class="wrap crumbs">{cr}</div>'}{body}</main>
<footer><div class="wrap fgrid"><div><a class="logo" href="{rel}"><img src="{rel}img/brand/option-b-wordmark.svg" alt="CityRateBook" height="28"></a><p>Local service price guides. Funded by matched quote requests and sponsored partner links, never by what a price says.</p><p class="muted">Last updated {D}</p><p class="muted credit">{CREDIT}</p></div>
<div><b>Guides</b>{''.join(f'<a href="{rel}{k}/cost/">{v[0]}</a>' for k,v in list(S.items())[:4])}</div><div><b>Cities</b>{''.join(f'<a href="{rel}cities/{k}/">{v[0]}, {v[1]}</a>' for k,v in C.items())}</div>
<div><b>Company</b><a href="{rel}about/">About</a><a href="{rel}methodology/">How we estimate</a><a href="{rel}privacy/">Privacy</a></div></div></footer>
<script src="{rel}assets/site.js"></script></body></html>'''
    assert "\u2013" not in h and "\u2014" not in h, path
    os.makedirs(f"{R}/{path}",exist_ok=True); open(f"{R}/{path}index.html","w").write(h)
def tile(k,size=""):return f'<span class="tile {size}" style="--c:{S[k][8]}" title="{S[k][0]}">{icon(SI[k],30 if size=="lg" else 21)}</span>'
def est(rel,src="Sources"):return f'<span class="est">Estimate, last checked {D} · <a href="{rel}methodology/">{src}</a></span>'
def bar(lo,hi,mid,scale_lo,scale_hi,label="Typical range",nat=None):
    p=lambda x:max(0,min(100,(x-scale_lo)/(scale_hi-scale_lo)*100))
    n=f'<div class="nat" style="left:{p(nat[0])}%;width:{p(nat[1])-p(nat[0])}%"><i>National</i></div>' if nat else ""
    return f'''<div class="rbar"><div class="track">{n}<div class="fill" style="left:{p(lo)}%;width:{p(hi)-p(lo)}%"></div><div class="mid" style="left:{p(mid)}%"><em>{m(mid)} median</em></div></div>
<div class="ends"><span>{m(scale_lo)}</span><span>{label}: <b>{m(lo)} to {m(hi)}</b></span><span>{m(scale_hi)}</span></div></div>'''
def table(jobs,mult,rel):
    rows="".join(f"<tr><td>{j}</td><td><b>{m(a*mult)} to {m(b*mult)}</b></td></tr>" for j,a,b in jobs)
    return f'<div class="tablebox"><table><thead><tr><th>Job type</th><th>Estimate</th></tr></thead><tbody>{rows}</tbody></table>{est(rel)}</div>'
def faq(qs):
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qs]}
    return '<section class="faq"><h2>Frequently asked questions</h2>'+"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in qs)+"</section>",ld
def quote(rel,svc="",city=""):
    opts="".join(f'<option value="{k}"{" selected" if k==svc else ""}>{v[0]}</option>' for k,v in S.items())
    return f'''<section class="quote" id="quote"><div class="qhead"><h2>Get up to 3 local quotes</h2><p>Free, about a minute. Prototype only: saved in your browser, nothing is sent.</p>
<ol class="steps"><li class="on">Service</li><li>Timing</li><li>Details</li><li>Contact</li></ol></div>
<form class="qform" novalidate data-city="{city}">
<fieldset class="step on"><label>Service<select name="service">{opts}</select></label><label>ZIP code<input name="zip" inputmode="numeric" maxlength="5" placeholder="e.g. 02118" required pattern="[0-9]{{5}}"></label></fieldset>
<fieldset class="step"><legend>When do you need it?</legend><div class="chips">{''.join(f'<label><input type="radio" name="timing" value="{t}"{" checked" if i==1 else ""}><span>{t}</span></label>' for i,t in enumerate(["Urgent, within 48 hours","Within 2 weeks","Within a month","Just planning"]))}</div></fieldset>
<fieldset class="step"><label>Describe the job<textarea name="details" rows="4" placeholder="e.g. Kitchen sink drains slowly, about 10 year old house"></textarea></label></fieldset>
<fieldset class="step"><label>Name<input name="name" required autocomplete="name"></label><label>Email<input name="email" type="email" required autocomplete="email"></label><label>Phone (optional)<input name="phone" type="tel" autocomplete="tel"></label>
<label class="consent"><input type="checkbox" name="consent" required><span>I agree to be contacted by up to 3 pros.</span></label>
<p class="legal">We collect your service, ZIP, timing, details, and contact info and share them only with up to 3 matched providers. By checking the box and submitting, you agree that those providers may contact you by email, and if you add a phone number, by call or text, including automated means, at the number provided. Consent is not a condition of purchase. Message and data rates may apply; reply STOP to opt out. See our <a href="{rel}privacy/">Privacy policy</a>.</p></fieldset>
<p class="err" role="alert"></p>
<div class="qnav"><button type="button" class="btn ghost back" hidden>Back</button><button type="button" class="btn next">Continue</button></div></form>
<div class="success" hidden><div class="check">✓</div><h3>Request saved</h3><p>In the real product, up to 3 local pros would reach out. In this prototype, your request is stored in this browser only (localStorage) and was not sent anywhere.</p><button class="btn ghost again" type="button">Start a new request</button></div></section>'''

# ===== Real data (fetched Oct 13, 2026) =====
BLS=json.load(open(f"{R}/data/bls_oews.json"))
BLS_URL="https://www.bls.gov/oes/"; BLS_API="https://api.bls.gov/publicAPI/v2/timeseries/data/"
SOC={"plumbers":("47-2152","Plumbers, pipefitters and steamfitters"),"electricians":("47-2111","Electricians"),"hvac":("49-9021","Heating, AC and refrigeration mechanics and installers"),"painters":("47-2141","Painters, construction and maintenance"),"house-cleaners":("37-2012","Maids and housekeeping cleaners"),"movers":("53-7062","Laborers and freight, stock and material movers, hand"),"pet-sitters":("39-2021","Animal caretakers"),"handyman":("49-9071","Maintenance and repair workers, general")}
# HomeAdvisor national cost guides, read Oct 13, 2026 (pages say Updated Jun 19, 2026)
HA={"plumbers":("https://www.homeadvisor.com/cost/plumbing/hire-a-plumber/",182,501,"Average $341. Hourly rates $45 to $200. Trip fees $50 to $300."),
"electricians":("https://www.homeadvisor.com/cost/electrical/hire-an-electrician/",163,538,"Average $351. Licensed electricians charge $50 to $130 per hour, plus a $100 to $200 service call fee."),
"hvac":("https://www.homeadvisor.com/cost/heating-and-cooling/repair-an-hvac-system/",130,2000,"HVAC repair. Labor alone runs $100 to $250 per hour."),
"house-cleaners":("https://www.homeadvisor.com/cost/cleaning-services/hire-a-maid-service/",118,238,"Average $176. Independent cleaners charge $12 to $25 per hour; cleaning companies $25 to $80 per hour."),
"handyman":("https://www.homeadvisor.com/cost/handyman/hire-a-handyman/",164,647,"Handyperson rates run $50 to $150 per hour.")}
CITY_ORDER=list(C)
def w(x):return f"${x:,.2f}"
def bls(area,k): return BLS["data"][area][k]
def pts(area,k): return [x for x in ("p10","median","p90") if bls(area,k)[x]["value"]]
def wagebox(area,k,rel,label):
    b=bls(area,k); yr=b["median"]["year"]
    return f'''<div class="cmp"><div><small>10th percentile</small><b>{w(b["p10"]["value"])}/hr</b></div><div><small>Median</small><b>{w(b["median"]["value"])}/hr</b></div><div><small>90th percentile</small><b>{w(b["p90"]["value"])}/hr</b></div></div>
<p class="muted small">{label}. What workers in this job earn per hour (SOC {SOC[k][0]}, {SOC[k][1]}), not what you pay. Company rates add overhead, insurance and travel. Source: <a href="{BLS_URL}" rel="nofollow">BLS OEWS</a>, May {yr} data, series {b["median"]["series"]}, fetched {D}.</p>'''
def hab(k,rel):
    if k not in HA: return '<p class="muted">We have not found a free, citable national job cost guide for this service yet, so we show no job price.</p>'
    u,lo,hi,n=HA[k]; avg={"plumbers":341,"electricians":351,"house-cleaners":176}.get(k)
    b=bar(lo,hi,avg or lo,0,round(hi*1.4),"National normal range").replace(f"{m(avg or lo)} median",f"{m(avg or lo)} average")
    if not avg: b=re.sub(r'<div class="mid"[^>]*><em>[^<]*</em></div>','',b)
    return f'''{b}<p class="small">{n}</p><span class="est">Estimate, national. Source: <a href="{u}" rel="nofollow">HomeAdvisor cost guide</a> (updated Jun 19, 2026), checked {D}</span>'''
# HOME
rel=""
body=f'''<section class="hero"><div class="wrap hs"><div><span class="kicker">{icon("badge-check",15)} Real sources · last checked {D}</span><h1>Know what it should cost<br><span class="grad">before you call a pro.</span></h1>
<p class="lede">National job cost ranges from published cost guides, plus what local workers earn from US Bureau of Labor Statistics data. Every figure links to its source.</p>
<div class="stats"><div><b>{len(S)}</b>services</div><div><b>{len(C)}</b>cities</div><div><b>{len(HA)}</b>national cost guides</div></div></div><div>{hero("cityratebook")}</div></div></section>
<section class="wrap" id="services"><div class="sh"><h2 class="secdeco" style="--c:#14532D"><span class="ibadge soft">{icon("wrench",20)}</span>Services</h2><a href="methodology/">How we estimate</a></div><div class="grid4">
{''.join(f'<a class="card svc" href="{k}/cost/">{tile(k)}<h3>{v[0]}</h3><p class="rng">{icon("dollar-sign",16,"ic pr")}{(m(HA[k][1])+" to "+m(HA[k][2])) if k in HA else "Median wage "+w(bls("national",k)["median"]["value"])+"/hr"}</p><span class="est">{icon("badge-check",13)} {"Estimate, HomeAdvisor" if k in HA else "BLS wage data"}, {D}</span></a>' for k,v in S.items())}</div></section>
<section class="wrap" id="cities"><div class="sh"><h2 class="secdeco" style="--c:#D9A21B"><span class="ibadge soft">{icon("map-pin",20)}</span>Cities</h2></div><div class="grid3">
{''.join(f'<a class="card city" href="cities/{k}/"><div class="cimg c{i}">{icon("building-2",64,"ic sky")}<b>{v[1]}</b></div><h3>{v[0]}, {v[1]}</h3><p>{icon("map-pin",15)} Local wage data for {len(S)} trades</p></a>' for i,(k,v) in enumerate(C.items()))}</div></section>
<section class="wrap how"><div><span class="ibadge lg" style="--c:#14532D">{icon("scale",30)}</span><h2>Ranges, not guesses</h2><p>We only publish figures we can cite. Job prices are national estimates from published cost guides. Local figures are BLS wage data for the workers who do the job. Where we have no source, we show nothing.</p><a class="btn ghost" href="methodology/">Read our methodology</a></div></section>'''
page("","Local service price guides","Home service cost ranges and local wage data, with sources.",body,[("Home","")])
# SERVICE HUBS
for k,v in S.items():
    rel="../../"; name=v[0]
    qs=[(f"How much do {name.lower()} cost?",(f"HomeAdvisor's national normal range is {m(HA[k][1])} to {m(HA[k][2])} (checked {D})." if k in HA else "We have not found a free, citable national job cost guide for this service yet.")),
        ("Are these quotes?","No. They are estimates from cited sources. Local quotes vary with the job.")]
    fh,fld=faq(qs)
    il={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"https://cityratebook.com/{k}/cost/{c}/","name":f"{name} cost in {C[c][0]}"} for i,c in enumerate(C)]}
    cities="".join(f'<a class="card city sm" href="{c}/"><h3>{C[c][0]}, {C[c][1]}</h3><p>Median wage {w(bls(c,k)["median"]["value"])}/hr</p></a>' for c in C)
    body=f'''<section class="wrap phead">{tile(k,"lg")}<div><h1>{name} Cost (2026 Estimates)</h1><p class="lede">How much do {name.lower()} cost? National figures from cited sources, checked {D}.</p></div></section>
<section class="wrap two"><div class="panel"><h3>National job cost</h3>{hab(k,rel)}</div><div class="panel"><h3>What workers earn nationally</h3>{wagebox("national",k,rel,"United States")}</div></section>
<section class="wrap"><h2>{name} by city</h2><div class="grid3">{cities}</div></section>
<section class="wrap">{fh}</section><section class="wrap">{quote(rel,k)}</section>'''
    page(f"{k}/cost/",f"{name} Cost (2026 Estimates)",f"{name} national cost range and wage data, with sources.",body,[("Home",""),(f"{name} cost",f"{k}/cost/")],[fld,il])
# CITY x SERVICE
gates=[]
import shutil
for c in C:
    for k in S:
        if os.path.isdir(f"{R}/{k}/cost/{c}") and k not in S: shutil.rmtree(f"{R}/{k}/cost/{c}")
for k in S:
  for c,cv in C.items():
    rel="../../../"; name=S[k][0]; cn,st=cv[0],cv[1]
    P=pts(c,k); ok=len(P)>=3
    bl,bn=bls(c,k)["median"]["value"],bls("national",k)["median"]["value"]; diff=round((bl/bn-1)*100)
    qs=[(f"How much do {name.lower()} earn in {cn}?",f"BLS May {bls(c,k)['median']['year']} data puts the median hourly wage at {w(bl)}, {abs(diff)}% {'above' if diff>=0 else 'below'} the national median of {w(bn)}."),
        (f"How much will a {name.lower()[:-1] if name.endswith('s') else name.lower()} job cost in {cn}?","We do not have a free, citable local job price source yet. "+(f"The national HomeAdvisor normal range is {m(HA[k][1])} to {m(HA[k][2])}." if k in HA else ""))]
    fh,fld=faq(qs)
    body=f'''<section class="wrap phead">{tile(k,"lg")}<div><span class="kicker">{cn}, {st}</span><h1>{name} Cost in {cn}, {st} (2026 Estimates)</h1><p class="lede">Local wage data from BLS, plus the national job cost range. Checked {D}.</p></div></section>
<section class="wrap two"><div class="panel"><h3>What {name.lower()} earn in the {cn} metro</h3>{wagebox(c,k,rel,cn+" metro area")}<div class="cmp"><div><small>{cn} median</small><b>{w(bl)}/hr</b></div><div><small>National median</small><b>{w(bn)}/hr</b></div><div><small>Difference</small><b class="{'up' if diff>=0 else 'down'}">{'+' if diff>=0 else ''}{diff}%</b></div></div></div>
<div class="panel"><h3>National job cost</h3>{hab(k,rel)}<p class="gate">Index gate: {len(P)} local data points (BLS wage percentiles). {"Meets the 3 point minimum" if ok else "Below 3, noindex"}. Prototype stays noindex.</p></div></section>
<section class="wrap">{fh}</section><section class="wrap">{quote(rel,k,c)}</section>'''
    gates.append((f"{k}/{c}",len(P),ok))
    page(f"{k}/cost/{c}/",f"{name} Cost in {cn}, {st} (2026 Estimates)",f"{name} wages in {cn} from BLS, plus national cost range.",body,[("Home",""),(f"{name} cost",f"{k}/cost/"),(f"{cn}, {st}",f"{k}/cost/{c}/")],[fld],gate=f"points={len(P)};pass={ok}")
# CITY HUBS
for c,cv in C.items():
    rel="../../"; cn,st=cv[:2]
    il={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"name":S[k][0],"url":f"https://cityratebook.com/{k}/cost/{c}/"} for i,k in enumerate(S)]}
    cards="".join(f'<a class="card svc" href="{rel}{k}/cost/{c}/">{tile(k)}<h3>{v[0]}</h3><p class="rng">{w(bls(c,k)["median"]["value"])}/hr <small>median wage</small></p><span class="est">BLS OEWS May {bls(c,k)["median"]["year"]}</span></a>' for k,v in S.items())
    body=f'''<section class="wrap phead"><span class="tile lg" style="--c:#0f172a">{st}</span><div><h1>Home Service Costs in {cn}, {st} (2026 Estimates)</h1><p class="lede">Median hourly wages for home service workers in the {cn} metro area, from <a href="{BLS_URL}" rel="nofollow">BLS OEWS</a>. Checked {D}.</p></div></section>
<section class="wrap"><div class="grid4">{cards}</div></section><section class="wrap">{quote(rel,"",c)}</section>'''
    page(f"cities/{c}/",f"Home Service Costs in {cn}, {st} (2026 Estimates)",f"Home service wage data for {cn}.",body,[("Home",""),("Cities","cities/"),(f"{cn}, {st}",f"cities/{c}/")],[il])
# STATIC
rel="../"
page("methodology/","Methodology: How We Estimate Prices","Methodology and sources.",f'''<section class="wrap prose"><h1>Methodology: How We Estimate Prices</h1><p class="est">Last checked {D}</p>
<p>We publish only figures we can cite, each with a link and a check date.</p><h2>Sources</h2><ul class="sources">
<li><b>US Bureau of Labor Statistics, OEWS (May 2025 data).</b> Hourly wage 10th percentile, median and 90th percentile, nationally and for the Boston, Austin and Denver metro areas, pulled from the free <a href="{BLS_API}" rel="nofollow">BLS public API</a>. These are worker wages, not customer prices. <a href="{BLS_URL}" rel="nofollow">bls.gov/oes</a></li>
<li><b>HomeAdvisor cost guides</b> for plumbers, electricians, HVAC repair, house cleaning and handyman work. National ranges only, labeled Estimate, with attribution. {"".join(f'<a href="{v[0]}" rel="nofollow">{k}</a> ' for k,v in HA.items())}</li></ul>
<h2>Index rule</h2><p>A city page needs at least 3 real local data points before it can be indexed. Today every city page has 3 local BLS wage points. The whole prototype stays noindex.</p>
<h2>Gaps</h2><p>We have no free, citable local job price data for any city, and no national job cost guide yet for movers, painters or pet sitters.</p></section>''',[("Home",""),("Methodology","methodology/")])

page("privacy/","Privacy","Privacy policy.",f'''<section class="wrap prose"><h1>Privacy policy</h1><p class="est">Last updated {D} · prototype draft</p><h2>What we collect</h2><p>When you request quotes: service, ZIP, timing, job details, name, email and optional phone.</p><h2>Who we share it with</h2><p>Up to 3 matched local service providers, only after you check the consent box.</p><h2>Calls and texts</h2><p>If you give a phone number and consent, matched providers may call or text you, including by automated means. Consent is not a condition of purchase. Reply STOP to opt out.</p><h2>This prototype</h2><p>Nothing is sent. Requests are stored in your browser's localStorage and you can clear them anytime.</p><button class="btn ghost" onclick="localStorage.removeItem('rw_quotes');this.textContent='Cleared'">Clear my saved requests</button></section>''',[("Home",""),("Privacy","privacy/")])
page("about/","About","About.",f'''<section class="wrap prose"><h1>About {BR}</h1><p class="est">Last updated {D}</p><p>{BR} by Atulit publishes local price information for everyday home services, using only figures we can cite.</p><h2>How we are funded</h2><p>Planned: matched quote requests and clearly labeled affiliate partners. No ads.</p></section>''',[("Home",""),("About","about/")])
# cities hub
cl="".join(f'<a class="card city sm" href="{c}/"><h3>{v[0]}, {v[1]}</h3><p>Home service cost estimates</p></a>' for c,v in C.items())
page("cities/","Home Service Costs by City (2026 Estimates)","Cities.",f'<section class="wrap phead"><div><h1>Home Service Costs by City (2026 Estimates)</h1><p class="lede">Pick a city to see local estimate ranges for home services, with sources and the date we last checked.</p></div></section><section class="wrap"><div class="grid3">{cl}</div></section>',[("Home",""),("Cities","cities/")])
json.dump({g[0]:g[2] for g in gates},open(R+"/.index-gate.json","w"))
print("INDEX GATE", sum(g[2] for g in gates), "of", len(gates))
install_css(f"{R}/assets/site.css",""".hs{display:grid;grid-template-columns:1.15fr 1fr;gap:30px;align-items:center}.kicker .ic{vertical-align:-.15em}
.nav nav a .ic{width:16px;height:16px}.nav nav .btn .ic{opacity:1}.thm{margin-left:0}
.rng{display:flex;align-items:center;gap:4px}.rng .ic.pr{color:#D9A21B}.est .ic{color:#16a34a;vertical-align:-.15em}
.cimg{position:relative;overflow:hidden}.cimg .sky{position:absolute;right:10px;top:10px;opacity:.28;color:#fff;width:84px;height:84px}
.card.city p .ic{color:#D9A21B}.how .ibadge{margin-bottom:6px}.credit{font-size:12px}.credit a{display:inline!important;text-decoration:underline}
@media(max-width:820px){.hs{grid-template-columns:1fr}.hs .hero-gfx{max-width:320px}}
html[data-theme=dark] .banner{background:#1a1e26;color:#cbd5e1}
""")
import sys; sys.path.insert(0,R); import seo_site; seo_site.build()
