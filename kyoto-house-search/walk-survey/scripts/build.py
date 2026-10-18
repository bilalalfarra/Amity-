#!/usr/bin/env python3
"""Printable price survey of homes within a 10-minute walk of the office, grouped by all-in monthly price band
and split by key money (礼金) yes / no. Reads out/final.json, out/parking.json."""
import base64, datetime, importlib.util, json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
spec = importlib.util.spec_from_file_location("base_report", os.path.join(ROOT, "report.py"))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.path.insert(0, os.path.join(ROOT, "combo"))
import make_maps  # noqa: E402
BANDS = [(0, 100_000, "≤ 100 ألف"), (100_001, 130_000, "100–130 ألف"), (130_001, 160_000, "130–160 ألف"),
         (160_001, 200_000, "160–200 ألف"), (200_001, 10**9, "فوق 200 ألف")]  # same as finalize.py

e, ja, yen = R.e, R.ja, R.yen
R.SRC_LABEL.update({"yahoo": "Yahoo!不動産", "kyotolife": "京都ライフ", "eretz": "エリッツ", "chouei": "長栄",
                    "flat": "フラットエージェンシー", "housemate": "ハウスメイト", "other": "وكالة محلية"})
TODAY = datetime.date.today().strftime("%Y/%m/%d")
GMAPS = "https://www.google.com/maps/search/?api=1&query=35.023968,135.773178"
BAND_COL = ["#2f6b4f", "#1f5f99", "#b86e00", "#a23b2b", "#6a4c93"]


def avail(a):
    a = str(a or "")
    if re.search(r"(契約可|空きあり|空有|募集中)", a):
        return '<span class="ok">متاح</span>'
    if re.search(r"(満車|空き待ち)", a):
        return '<span class="warn">ممتلئ</span>'
    return '<span class="muted">اسأل</span>'


def parking_txt(u):
    src, pk = u["parking_cost_src"], u["parking_cost"]
    if src == "onsite":
        return f'<span class="ok">✓ بالبناية</span> {"مجاني" if pk == 0 else yen(pk)}'
    if src == "listing_nearby":
        return f'قريب (حسب الإعلان) {yen(pk)}'
    if src == "lot" and u["nearby_parking"]:
        l = u["nearby_parking"][0]
        return (f'كراج شهري {yen(pk)} · {int(l["distance_km"]*1000)} م {avail(l.get("availability"))}'
                f'<br><a href="{e(l["url"])}" target="_blank" rel="noopener">رابط الكراج</a>')
    return f'<span class="warn">تقديري {yen(pk)}</span> (ما لقيت كراج بسعر معلن ضمن 500 م)'


def row(u):
    links = " ".join(f'<a href="{e(url)}" target="_blank" rel="noopener">{e(lab)}</a>' for lab, url in R.labelled_sources(u))
    ev = "مصعد" if u.get("elevator") else ""
    kind = "بيت" if u.get("is_house") else ""
    return f'''<tr><td class="num">{u["rank"]}</td>
<td>{ja(u.get("building_name") or "—")} <span class="small">{kind}</span><div class="small muted">{ja(u.get("address"))}</div></td>
<td class="num"><b>{yen(u["monthly_total_with_parking"])}</b><div class="small muted">{yen(u["rent"])} + {yen(u.get("kanrihi") or 0)} + كراج</div>{('<div class="small warn">نفس البيت عند وكالة تانية: ' + ", ".join(yen(x) for x in u["rents_seen"] if x != u["rent"]) + '</div>') if len(u.get("rents_seen") or []) > 1 else ""}</td>
<td><bdi dir="ltr">{e(u["layout"])}</bdi><br><span class="num">{e(u["area_m2"])} م²</span></td>
<td class="num">{yen(u["yen_per_m2"])}</td>
<td class="num">{e(u.get("floor") or "—")}/{e(u.get("building_floors") or "?")} {ev}</td>
<td><span class="num">{e(u.get("built_year") or "؟")}</span> {e(u.get("structure") or "")}<br>{R.grade_chip(u)}</td>
<td class="num">{e(max(1, u["walk_min"]))} د{'<div class="small muted">تقريبي</div>' if (u.get("geo_rank", 2) <= 1) else ""}</td>
<td class="small num">礼 {e(u.get("reikin") or "—")}<br>敷 {e(u.get("shikikin") or "—")}</td>
<td class="small">{parking_txt(u)}</td>
<td class="links">{links}<div class="print-url">{e(u["sources"][0]["url"])}</div></td></tr>'''


def table(units, caption):
    if not units:
        return f'<p class="lead muted">{caption}: ما في.</p>'
    return f'''<div class="tablewrap"><table><caption>{caption}</caption>
<thead><tr><th>#</th><th>المبنى / العنوان</th><th>الإجمالي بالشهر مع الكراج</th><th>التقسيم</th><th>ين/م²</th><th>الطابق</th><th>البناء / العزل</th><th>مشي</th><th>礼金 / 敷金</th><th>الكراج</th><th>روابط</th></tr></thead>
<tbody>{"".join(row(u) for u in units)}</tbody></table></div>'''


def main():
    out_html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, "report.html")
    ALL = json.load(open(os.path.join(OUT, "final.json"), encoding="utf-8"))
    U = [u for u in ALL if not u["near"]]
    N = [u for u in ALL if u["near"]]
    css = re.search(r"<style>.*?</style>", open(os.path.join(ROOT, "sakyo", "out", "report.html"), encoding="utf-8").read(), re.S).group(0)
    css = css.replace("table{", "table{font-size:12.5px;", 1)

    for u in ALL:
        u["_col"] = f"b{u['band']}"
    for i, c in enumerate(BAND_COL):
        make_maps.COL[f"b{i}"] = c
    mp = make_maps.make_map(ALL, [(35.023968, 135.773178, "#c0392b", "★")], os.path.join(OUT, "map.png"), size=(1200, 900))
    b64 = base64.b64encode(open(mp, "rb").read()).decode()
    legend = "".join(f'<span><span class="dot" style="background:{BAND_COL[i]}"></span>{lab}</span>' for i, (_, _, lab) in enumerate(BANDS))

    summary_rows, sections = [], []
    for i, (lo, hi, lab) in enumerate(BANDS):
        band = [u for u in U if u["band"] == i]
        no_r = [u for u in band if not u["has_reikin"]]
        yes_r = [u for u in band if u["has_reikin"]]
        if band:
            areas = [u["area_m2"] for u in band]
            summary_rows.append(f'<tr><td><span class="dot" style="background:{BAND_COL[i]}"></span> {lab}</td><td class="num">{len(no_r)}</td><td class="num">{len(yes_r)}</td>'
                                f'<td class="num">{min(areas):.0f}–{max(areas):.0f} م²</td><td class="num">{yen(statistics.median(u["monthly_total_with_parking"] for u in band))}</td>'
                                f'<td class="num">{yen(statistics.median(u["yen_per_m2"] for u in band))}</td></tr>')
        else:
            summary_rows.append(f'<tr><td>{lab}</td><td class="num">0</td><td class="num">0</td><td>—</td><td>—</td><td>—</td></tr>')
        sections.append(f'''<section id="band{i}"><h2><span class="dot" style="background:{BAND_COL[i]};width:14px;height:14px"></span> {lab} بالشهر (مع الكراج) — {len(band)}</h2>
{table(no_r, f"بدون 礼金 ({len(no_r)})")}
{table(yes_r, f"مع 礼金 ({len(yes_r)})")}</section>''')

    near_summary = "".join(
        f'<tr><td><span class="dot" style="background:{BAND_COL[i]}"></span> {lab}</td><td class="num">{sum(1 for u in N if u["band"] == i and not u["has_reikin"])}</td>'
        f'<td class="num">{sum(1 for u in N if u["band"] == i and u["has_reikin"])}</td>'
        f'<td class="num">{yen(statistics.median([u["monthly_total_with_parking"] for u in N if u["band"] == i])) if any(u["band"] == i for u in N) else "—"}</td></tr>'
        for i, (_, _, lab) in enumerate(BANDS))
    totals = [u["monthly_total_with_parking"] for u in U]
    onsite = sum(1 for u in U if u["parking_cost_src"] == "onsite")
    est = sum(1 for u in U if u["parking_cost_src"] == "estimate")
    page = f'''<title>أسعار البيوت حول الشغل</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
{css}
<div class="wrap">
<header>
  <div class="eyebrow">مسح أسعار · كيوتو · {TODAY}</div>
  <h1>شو بتكلّف البيوت على بعد 10 دقايق مشي من الشغل</h1>
  <div class="office"><div><b><bdi lang="ja" dir="ltr">京都技術科学センター</bdi></b> · <bdi lang="ja" dir="ltr">京都市左京区吉田河原町14</bdi></div>
    <div><a class="btn" href="{GMAPS}" target="_blank" rel="noopener">الخريطة ↗</a></div></div>
  <p class="lead">هاد مسح لفهم الأسعار، مش قائمة اختيار. الشروط الوحيدة: 2LDK أو أكبر، 45 م² أو أكتر، والبيت على بعد 10 دقايق مشي أو أقل (محسوبة على شوارع حقيقية). ما في حد للسعر ولا لـ礼金، ولا لعمر البناية أو الطابق. السعر بكل جدول هو <b>الإيجار + 管理費 + الكراج</b>: كراج البناية إذا في، وإلا أرخص كراج شهري معلن ضمن 500 م، وإذا ما في ولا واحد بحط سعر تقديري (وسيط المنطقة) ومكتوب جنبه "تقديري".</p>
  <div class="kpis">
    <div class="kpi"><div class="n">{len(U)}</div><div class="l">بيت وشقة ضمن 10 د مشي</div></div>
    <div class="kpi"><div class="n">{yen(min(totals)) if totals else "—"}</div><div class="l">أرخص إجمالي مع الكراج</div></div>
    <div class="kpi"><div class="n">{yen(statistics.median(totals)) if totals else "—"}</div><div class="l">الوسيط</div></div>
    <div class="kpi"><div class="n">{onsite}</div><div class="l">فيهم كراج بالبناية</div></div>
    <div class="kpi"><div class="n">{est}</div><div class="l">سعر الكراج تقديري</div></div>
  </div>
</header>
<section id="summary"><h2>الملخص حسب السعر</h2>
<div class="tablewrap"><table><thead><tr><th>الإجمالي بالشهر مع الكراج</th><th>بدون 礼金</th><th>مع 礼金</th><th>المساحات</th><th>وسيط الإجمالي</th><th>وسيط ين/م² (الإيجار بس)</th></tr></thead>
<tbody>{"".join(summary_rows)}</tbody></table></div></section>
<section id="map"><h2>الخريطة</h2><figure><img src="data:image/png;base64,{b64}" alt="خريطة البيوت حول الشغل"><div class="legend"><span><span class="dot" style="background:#c0392b"></span>★ الشغل</span>{legend}</div>
<figcaption class="small muted">الرقم على كل نقطة = رقم البيت بالجداول (N = 11–15 دقيقة). الموقع دقيق لحد الحي (±300 م). © OpenStreetMap contributors</figcaption></figure></section>
{"".join(sections)}
<section id="near"><h2>للمقارنة: بيوت على بعد 11–15 دقيقة مشي ({len(N)})</h2>
<p class="lead">أبعد شوي من حدّك، بس بتعطي صورة أوضح عن الأسعار بالمنطقة. نفس طريقة الحساب، ومرتبة حسب الإجمالي مع الكراج.</p>
<div class="tablewrap"><table><thead><tr><th>السعر</th><th>بدون 礼金</th><th>مع 礼金</th><th>وسيط الإجمالي</th></tr></thead><tbody>{near_summary}</tbody></table></div>
{table(N, "كل البيوت 11–15 دقيقة مشي")}</section>
<section id="notes"><h2>ملاحظات</h2>
<div class="note"><b>العزل:</b> A = بناء 2015+ · B+ = 2001–2014 خرسانة · B / B- = 2001–2014 خشب أو حديد خفيف · C = 1991–2000 خرسانة · D = أقدم أو خشب/حديد قبل 2001. هالمرة ما شلت البنايات القديمة لأنك طلبت فكرة عامة عن الأسعار.</div>
<div class="note"><b>المصادر:</b> SUUMO وCHINTAI وスマイティ وエイブル وeheya وHOME'S للبيوت، وアットパーキング وPark Direct وp-king وタイムズ وغيرهم للكراجات. الإعلان نفسه ممكن ينعرض عند أكتر من وكالة، فدمجتهم بسطر واحد مع كل الروابط. الأسعار بتتغير، فتأكد مع الوكيل.</div>
</section>
<footer class="end">تم الجمع بتاريخ {TODAY}.</footer>
</div>'''
    open(out_html, "w", encoding="utf-8").write(page)
    print("wrote", out_html, len(U), "units")


if __name__ == "__main__":
    main()
