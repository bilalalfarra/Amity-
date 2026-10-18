#!/usr/bin/env python3
"""Refined, printable report: price bands (rent ≤ 140k), detached houses 1980+ within walking distance,
apartments within ~3 km by bike, a separate list for high key money, and parking options for chosen homes."""
import base64, datetime, importlib.util, json, os, re, statistics, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
spec = importlib.util.spec_from_file_location("base_report", os.path.join(ROOT, "report.py"))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.path.insert(0, os.path.join(ROOT, "combo"))
import make_maps  # noqa: E402

e, ja, yen = R.e, R.ja, R.yen
R.SRC_LABEL.update({"yahoo": "Yahoo!不動産", "kyotolife": "京都ライフ", "eretz": "エリッツ", "chouei": "長栄",
                    "flat": "フラットエージェンシー", "housemate": "ハウスメイト", "other": "وكالة محلية"})
TODAY = datetime.date.today().strftime("%Y/%m/%d")
BANDS = [(0, 100_000, "≤ 100 ألف"), (100_001, 130_000, "100–130 ألف"), (130_001, 160_000, "130–160 ألف"),
         (160_001, 10**9, "فوق 160 ألف")]  # same as finalize.py
BAND_COL = ["#2f6b4f", "#1f5f99", "#b86e00", "#a23b2b"]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
# homes the user asked about, matched by text in name/address + area
FOCUS = [("بيت 7 / بيت 11 بالتقرير السابق (نفس البيت)", "吉田中阿達町", 66.7),
         ("N2 بالتقرير السابق — ファーストコート今出川北", "大北小路東町", 60.32),
         ("N4 بالتقرير السابق — ベルメゾン鴨川", "出水町", 48.6)]


def avail(a):
    a = str(a or "")
    if re.search(r"(契約可|空きあり|空き有|空有|募集中)", a):
        return '<span class="ok">متاح</span>'
    if re.search(r"(満車|空き待ち|空無|空車なし)", a):
        return '<span class="warn">ممتلئ / انتظار</span>'
    return '<span class="muted">اسأل</span>'


def live_availability(url):
    """Re-read a parking lot page now and pull that lot's own availability field (not the site's FAQ text)."""
    try:
        html = subprocess.run(["curl", "-sS", "-L", "--max-time", "20", "-A", UA, url], capture_output=True, text=True).stdout
    except Exception:
        return None
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    t = re.sub(r"<[^>]+>", "|", t)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"(\| ?)+", "|", t)
    for pat in (r"初期費用\|(契約可|空き待ち可)\|",                       # Park Direct: the lot's own row
                r"空き状況\|([^|]{0,8}(?:空き|満車|問合|待ち|契約可)[^|]{0,8})\|",  # p-king / at-parking style field
                r"\|(契約可|空き待ち可|空きあり|空き有り|満車)\|"):
        m = re.search(pat, t)
        if m:
            return m.group(1).strip()
    return None


def parking_txt(u):
    src, pk = u["parking_cost_src"], u["parking_cost"]
    if src == "onsite":
        return f'<span class="ok">✓ بالبناية</span> {"مجاني" if pk == 0 else yen(pk)}'
    if src == "listing_nearby":
        return f'قريب (حسب الإعلان) {yen(pk)} — {ja(u.get("parking"))}'
    l = min(u["nearby_parking"], key=lambda x: x["monthly_fee"])
    return (f'كراج شهري {yen(pk)} · {int(l["distance_km"]*1000)} م {avail(l.get("availability"))}'
            f'<br><a href="{e(l["url"])}" target="_blank" rel="noopener">رابط الكراج</a>')


def row(u):
    links = " ".join(f'<a href="{e(url)}" target="_blank" rel="noopener">{e(lab)}</a>' for lab, url in R.labelled_sources(u))
    other = ('<div class="small warn">نفس البيت عند وكالة تانية: ' + ", ".join(yen(x) for x in u["rents_seen"] if x != u["rent"]) + '</div>') if len(u.get("rents_seen") or []) > 1 else ""
    fixed = '<div class="small warn">صلّحت موقعه يدوياً</div>' if u.get("location_fixed") else ""
    approx = '<div class="small muted">تقريبي</div>' if u.get("geo_rank", 2) <= 1 else ""
    return f'''<tr><td class="num">{u["rank"]}</td>
<td>{ja(u.get("building_name") or "—")} <span class="small">{"بيت مستقل" if u.get("is_house") else ""}</span><div class="small muted">{ja(u.get("address"))}</div>{fixed}</td>
<td class="num"><b>{yen(u["monthly_total_with_parking"])}</b><div class="small muted">{yen(u["rent"])} + {yen(u.get("kanrihi") or 0)} + كراج</div>{other}</td>
<td><bdi dir="ltr">{e(u["layout"])}</bdi>{('<div class="small muted">إعلان تاني: <bdi dir="ltr">' + e(u["layout_alt"]) + '</bdi></div>') if u.get("layout_alt") else ""}<span class="num">{e(u["area_m2"])} م²</span></td>
<td class="num">{e(u.get("floor") or "—")}/{e(u.get("building_floors") or "?")} {"مصعد" if u.get("elevator") else ""}</td>
<td><span class="num">{e(u.get("built_year") or "؟")}</span> {e(u.get("structure") or "")}<br>{R.grade_chip(u)}</td>
<td class="num">{e(u["dist_label"])}<div class="small muted">{e(u["bike_km"])} كم</div>{approx}</td>
<td class="small num">礼 {e(u.get("reikin") or "—")}<br>敷 {e(u.get("shikikin") or "—")}</td>
<td class="small">{parking_txt(u)}</td>
<td class="links">{links}<div class="print-url">{e(u["sources"][0]["url"])}</div></td></tr>'''


def table(units, caption):
    if not units:
        return f'<p class="lead muted">{caption}: ما في.</p>'
    return f'''<div class="tablewrap"><table><caption>{caption}</caption>
<thead><tr><th>#</th><th>المبنى / العنوان</th><th>الإجمالي بالشهر مع الكراج</th><th>التقسيم</th><th>الطابق</th><th>البناء / العزل</th><th>للشغل</th><th>礼金 / 敷金</th><th>الكراج</th><th>روابط</th></tr></thead>
<tbody>{"".join(row(u) for u in units)}</tbody></table></div>'''


def focus_section(U):
    blocks = []
    for title, key, area in FOCUS:
        hits = [u for u in U if key in str(u.get("address") or "") and abs((u.get("area_m2") or 0) - area) < 0.7]
        if not hits:
            blocks.append(f'<h3>{e(title)}</h3><p class="lead muted">ما عاد موجود بالبيانات الجديدة (يمكن تأجّر).</p>')
            continue
        u = hits[0]
        lots = sorted(u["nearby_parking"], key=lambda l: (l["distance_km"]))[:8]
        rows = []
        for l in lots:
            live = live_availability(l["url"])
            rows.append(f'<tr><td>{ja(l.get("name"))}</td><td class="num">{yen(l["monthly_fee"])}</td><td class="num">{int(l["distance_km"]*1000)} م · ~{l["walk_min"]} د</td>'
                        f'<td>{avail(live or l.get("availability"))}<div class="small muted">{ja(live or l.get("availability") or "")}</div></td>'
                        f'<td class="links"><a href="{e(l["url"])}" target="_blank" rel="noopener">رابط</a><div class="print-url">{e(l["url"])}</div></td></tr>')
        listing = f'الإعلان نفسه بيقول عن الكراج: {ja(u.get("parking") or "—")}'
        blocks.append(f'''<h3>{e(title)} — رقمه هلّق #{u["rank"]}</h3>
<p class="small">{ja(u.get("address"))} · {listing}</p>
<div class="tablewrap"><table><thead><tr><th>الكراج</th><th>بالشهر</th><th>البعد عن البيت</th><th>متاح؟ (فحصته اليوم)</th><th>رابط</th></tr></thead>
<tbody>{"".join(rows) or '<tr><td colspan="5">ما لقيت كراج بسعر معلن ضمن 500 م</td></tr>'}</tbody></table></div>''')
    return "".join(blocks)


def main():
    out_html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, "report.html")
    ALL = json.load(open(os.path.join(OUT, "final.json"), encoding="utf-8"))
    U = [u for u in ALL if not u["reikin_over"]]
    X = [u for u in ALL if u["reikin_over"]]
    css = re.search(r"<style>.*?</style>", open(os.path.join(ROOT, "sakyo", "out", "report.html"), encoding="utf-8").read(), re.S).group(0)
    css = css.replace("table{", "table{font-size:12.5px;", 1).replace("</style>", "h3{margin-block:22px 6px;font-size:16px}</style>")

    for u in ALL:
        u["_col"] = f"b{u['band']}"
    for i, c in enumerate(BAND_COL):
        make_maps.COL[f"b{i}"] = c
    mp = make_maps.make_map(U, [(35.023968, 135.773178, "#c0392b", "★")], os.path.join(OUT, "map.png"), size=(1200, 950))
    b64 = base64.b64encode(open(mp, "rb").read()).decode()
    legend = "".join(f'<span><span class="dot" style="background:{BAND_COL[i]}"></span>{lab}</span>' for i, (_, _, lab) in enumerate(BANDS))

    summary_rows, sections = [], []
    for i, (lo, hi, lab) in enumerate(BANDS):
        band = [u for u in U if u["band"] == i]
        no_r = [u for u in band if not u["has_reikin"]]
        yes_r = [u for u in band if u["has_reikin"]]
        apts = sum(1 for u in band if not u["is_house"])
        areas = [u["area_m2"] for u in band]
        area_txt = f"{min(areas):.0f}–{max(areas):.0f} م²" if areas else "—"
        summary_rows.append(f'<tr><td><span class="dot" style="background:{BAND_COL[i]}"></span> {lab}</td><td class="num">{len(no_r)}</td><td class="num">{len(yes_r)}</td>'
                            f'<td class="num">{apts} شقة · {len(band) - apts} بيت</td><td class="num">{area_txt}</td></tr>')
        sections.append(f'''<section id="band{i}"><h2><span class="dot" style="background:{BAND_COL[i]};width:14px;height:14px"></span> {lab} بالشهر (مع الكراج) — {len(band)}</h2>
{table(no_r, f"بدون 礼金 ({len(no_r)})")}
{table(yes_r, f"مع 礼金 لحد شهرين ({len(yes_r)})")}</section>''')

    page = f'''<title>بيوت حول الشغل — منقّحة</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
{css}
<div class="wrap">
<header>
  <div class="eyebrow">بحث سكن · كيوتو · {TODAY} · بعد التنقيح</div>
  <h1>بيوت وشقق حول 京都技術科学センター</h1>
  <p class="lead">الشروط: 2LDK أو أكبر، 45 م² أو أكتر، <b>الإيجار لحد 140 ألف</b> (بدون 管理費)، والكراج محسوب بالإجمالي. <b>الشقق</b> لحد حوالي 3 كم بالمسكليت (أي عمر). <b>البيوت المستقلة</b> ضمن 15 دقيقة مشي وبس اللي مبنية من 1980 وطالع. اللي 礼金 فيها <b>أكتر من شهرين أو أكتر من 250 ألف</b> بقائمة لحالها بالآخر. المسافات على طرق حقيقية (مشي أو مسكليت).</p>
  <div class="kpis">
    <div class="kpi"><div class="n">{len(U)}</div><div class="l">خيار بالقائمة الأساسية</div></div>
    <div class="kpi"><div class="n">{sum(1 for u in U if not u["has_reikin"])}</div><div class="l">منهن بدون 礼金</div></div>
    <div class="kpi"><div class="n">{sum(1 for u in U if u["parking_cost_src"] == "onsite")}</div><div class="l">فيهن كراج بالبناية</div></div>
    <div class="kpi"><div class="n">{yen(statistics.median([u["monthly_total_with_parking"] for u in U])) if U else "—"}</div><div class="l">وسيط الإجمالي مع الكراج</div></div>
    <div class="kpi"><div class="n">{len(X)}</div><div class="l">بقائمة 礼金 العالي</div></div>
  </div>
</header>
<section id="focus"><h2>كراجات للبيوت اللي سألت عنها</h2>
<p class="lead">أقرب الكراجات الشهرية بسعر معلن ضمن 500 م من كل بيت. رجعت فتحت صفحة كل كراج اليوم لأشوف إذا في محل، بس كتير مواقع بتكتب "اسأل" بدل ما تقول.</p>
{focus_section(ALL)}</section>
<section id="summary"><h2>الملخص حسب السعر</h2>
<div class="tablewrap"><table><thead><tr><th>الإجمالي بالشهر مع الكراج</th><th>بدون 礼金</th><th>مع 礼金</th><th>شقق / بيوت</th><th>المساحات</th></tr></thead>
<tbody>{"".join(summary_rows)}</tbody></table></div></section>
<section id="map"><h2>الخريطة</h2><figure><img src="data:image/png;base64,{b64}" alt="خريطة الخيارات حول الشغل"><div class="legend"><span><span class="dot" style="background:#c0392b"></span>★ الشغل</span>{legend}</div>
<figcaption class="small muted">الرقم على كل نقطة = رقم البيت بالجداول. © OpenStreetMap contributors</figcaption></figure></section>
{"".join(sections)}
<section id="reikin"><h2>قائمة تانية: 礼金 أكتر من شهرين أو أكتر من 250 ألف ({len(X)})</h2>
<p class="lead">بيحققوا باقي الشروط، بس 礼金 فيهن عالي. حطيتهن لحالهن متل ما طلبت، ومرتبين حسب الإجمالي مع الكراج.</p>
{table(X, "礼金 عالي")}</section>
<section id="notes"><h2>ملاحظات</h2>
<div class="note"><b>العزل:</b> A = بناء 2015+ · B+ = 2001–2014 خرسانة · B / B- = 2001–2014 خشب أو حديد خفيف · C = 1991–2000 خرسانة · D = أقدم. الشقق القديمة ضليت متل ما طلبت، بس انتبه للعزل والشبابيك.</div>
<div class="note"><b>المصادر:</b> SUUMO، HOME'S، CHINTAI، スマイティ، エイブル، eheya، Yahoo!不動産، 京都ライフ، フラットエージェンシー وغيرهم للبيوت، وアットパーキング وPark Direct وp-king وタイムズ وغيرهم للكراجات. الإعلان المكرر بين المواقع بسطر واحد مع كل الروابط.</div>
</section>
<footer class="end">تم الجمع بتاريخ {TODAY}.</footer>
</div>'''
    open(out_html, "w", encoding="utf-8").write(page)
    print("wrote", out_html, len(U), "main +", len(X), "high-reikin")


if __name__ == "__main__":
    main()
