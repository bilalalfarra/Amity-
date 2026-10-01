#!/usr/bin/env python3
"""One detailed printable report for the corrected workplace (左京区吉田河原町14).
Reuses the helpers of ../report.py; reads out/final.json, out/parking.json, out/map.png."""
import base64, datetime, importlib.util, json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
spec = importlib.util.spec_from_file_location("base_report", os.path.join(HERE, "..", "report.py"))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
e, ja, yen, ward_of, WARD_AR, STRUCT_AR = R.e, R.ja, R.yen, R.ward_of, R.WARD_AR, R.STRUCT_AR
TODAY = datetime.date.today().strftime("%Y/%m/%d")
GMAPS = "https://www.google.com/maps/search/?api=1&query=35.023968,135.773178"
OSM = "https://www.openstreetmap.org/?mlat=35.0240&mlon=135.7732#map=16/35.0240/135.7732"
WARD_AR.setdefault("左京区", "ساكيو")


def avail(a):
    if not a:
        return ""
    a = str(a)
    if re.search(r"(契約可|空きあり|空有|募集中)", a):
        return ' <span class="ok small">متاح</span>'
    if re.search(r"(満車|空き待ち)", a):
        return ' <span class="warn small">ممتلئ — قائمة انتظار</span>'
    return ' <span class="muted small">اسأل عن التوفر</span>'


def lot_li(l):
    fee = yen(l["monthly_fee"]) + "/شهر" if l.get("monthly_fee") else "السعر عند الاستفسار"
    return (f'<li>{ja(l.get("name"))} · <span class="num">{fee}</span> · {int(l["distance_km"]*1000)} م (~{l["walk_min"]} د مشي){avail(l.get("availability"))} '
            f'<a href="{e(l["url"])}" target="_blank" rel="noopener">رابط ↗</a><span class="print-url">{e(l["url"])}</span></li>')


def parking_cell(u, full=True):
    src, pk = u.get("parking_cost_src"), u.get("parking_cost")
    if src == "onsite":
        return f'<span class="ok">✓ موقف داخل العقار</span> <span class="num">{"مجاني" if pk == 0 else yen(pk) + "/شهر"}</span>'
    lots = u.get("nearby_parking") or []
    if src == "listing_nearby":
        head = f'<span class="warn">موقف قريب حسب الإعلان</span> <span class="num">{yen(pk)}/شهر</span> — <span class="small">{ja(u.get("parking"))}</span>'
    else:
        st = u.get("parking_status")
        why = {"onsite_full": "موقف العقار ممتلئ حالياً", "onsite_nofee": "موقف العقار بدون سعر معلن",
               "none": "لا يوجد موقف بالعقار"}.get(st, "الموقف غير مذكور بالإعلان")
        head = f'<span class="warn">{why}</span> → حسبت أرخص موقف شهري قريب: <span class="num">{yen(pk)}/شهر</span>'
    return head + (f'<ul class="lots">{"".join(lot_li(l) for l in lots)}</ul>' if lots else "")


R.parking_cell = parking_cell


def card(u):
    return R.card(u, rank_label=f"#{u['rank']}")


def table(units, caption):
    rows = []
    for u in units:
        pk = u.get("parking_cost")
        pk_txt = ("✓ داخلي " if u.get("parking_cost_src") == "onsite" else "قريب ") + ("مجاني" if pk == 0 else yen(pk))
        links = " ".join(f'<a href="{e(url)}" target="_blank" rel="noopener">{e(lab)}</a>' for lab, url in R.labelled_sources(u))
        rows.append(f'''<tr><td class="num">{e(u["rank"])}</td><td>{ja(u.get("building_name") or "—")}<div class="small muted">{ja(u.get("address"))}</div></td>
<td class="num"><b>{yen(u["monthly_total_with_parking"])}</b><div class="small muted">{yen(u["rent"])} + {yen(u.get("kanrihi") or 0)} + {pk_txt}</div></td>
<td><bdi dir="ltr">{e(u["layout"])}</bdi><br><span class="num">{e(u["area_m2"])} م²</span></td>
<td class="num">{e(u.get("floor") or "—")}/{e(u.get("building_floors") or "?")} {"مصعد" if u.get("elevator") else ""}</td>
<td><span class="num">{e(u.get("built_year"))}</span> {e(u.get("structure") or "")}<br>{R.grade_chip(u)}</td>
<td class="num">{e(u["bike_min"])} د<br><span class="small muted">{e(u["route_km"])} كم</span></td>
<td class="small num">{e(u.get("reikin") or "—")}</td><td class="links">{links}<div class="print-url">{e(u["sources"][0]["url"])}</div></td></tr>''')
    return f'''<div class="tablewrap"><table><caption>{caption}</caption>
<thead><tr><th>#</th><th>المبنى / العنوان</th><th>الإجمالي الشهري مع الموقف</th><th>التقسيم</th><th>الطابق</th><th>البناء</th><th>بالمسكليت</th><th>礼金</th><th>روابط</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>'''


def section(units, sid, title, lead, max_cards=40):
    if not units:
        return f'<section id="{sid}"><h2>{title}</h2><p class="lead">ما لقيت ولا بيت بهالشروط.</p></section>'
    cards = "".join(card(u) for u in units[:max_cards])
    rest = table(units[max_cards:], f"البقية ({len(units) - max_cards})") if len(units) > max_cards else ""
    return f'<section id="{sid}"><h2>{title}</h2><p class="lead">{lead}</p>{table(units, "ملخص سريع — مرتب حسب الأفضلية")}<div class="cards">{cards}</div>{rest}</section>'


def main():
    out_html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, "report.html")
    units = json.load(open(os.path.join(OUT, "final.json"), encoding="utf-8"))
    lots = json.load(open(os.path.join(OUT, "parking.json"), encoding="utf-8"))
    near = [u for u in units if u["near"]]
    units = [u for u in units if not u["near"]]
    l1 = [u for u in units if not u["is_house"] and u["reikin_group"] == "le1"]
    l2 = [u for u in units if not u["is_house"] and u["reikin_group"] == "le2"]
    houses = [u for u in units if u["is_house"]]
    apts = l1 + l2
    css = re.search(r"<style>.*?</style>", open(os.path.join(HERE, "..", "out", "report.html"), encoding="utf-8").read(), re.S).group(0)
    css = css.replace("</style>", ".office{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin-block:14px}"
                      ".office b{font-size:16px} figure{margin:16px 0} figure img{width:100%;height:auto;border:1px solid var(--line);border-radius:10px}"
                      ".legend{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;margin-top:6px} .dot{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:middle;margin-inline-end:4px}"
                      "@media (max-width:640px){.office{grid-template-columns:1fr}} @media print{figure{page-break-inside:avoid}}</style>")
    map_html = ""
    mp = os.path.join(OUT, "map.png")
    if os.path.exists(mp):
        b64 = base64.b64encode(open(mp, "rb").read()).decode()
        map_html = f'''<figure><img src="data:image/png;base64,{b64}" alt="خريطة الشغل وكل البيوت المقترحة">
<div class="legend"><span><span class="dot" style="background:#c0392b"></span>★ الشغل</span><span><span class="dot" style="background:#2f6b4f"></span>القائمة 1 (礼金 ≤ شهر)</span>
<span><span class="dot" style="background:#b86e00"></span>القائمة 2 (礼金 1–2 شهر)</span><span><span class="dot" style="background:#6a4c93"></span>بيت مستقل</span><span><span class="dot" style="background:#7a8590"></span>N = خيار إضافي 21–25 د</span></div>
<figcaption class="small muted">الرقم على كل نقطة = رقم البيت بالتقرير. الموقع دقيق لحد الحي (±300 م).</figcaption></figure>'''

    tot = [u["monthly_total_with_parking"] for u in apts]
    pk_stats = {}
    for l in lots:
        if l.get("monthly_fee") and not l.get("oversize_vehicle"):
            pk_stats.setdefault(l.get("ward") or ward_of(l.get("address")), []).append(l["monthly_fee"])
    pk_rows = "".join(f'<tr><td>{e(w)} <span class="muted">{e(WARD_AR.get(w, ""))}</span></td><td class="num">{len(v)}</td><td class="num">{yen(statistics.median(v))}</td><td class="num">{yen(min(v))} – {yen(max(v))}</td></tr>'
                      for w, v in sorted(pk_stats.items(), key=lambda kv: -len(kv[1])) if w and w != "?" and len(v) >= 3)

    page = f'''<title>بيوت قرب شغلي — ساكيو</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
{css}
<div class="wrap">
<header>
  <div class="eyebrow">تقرير بحث سكن · كيوتو · {TODAY} · نسخة مصححة</div>
  <h1>بيوت للإيجار قرب 京都技術科学センター</h1>
  <div class="office"><div><b><bdi lang="ja" dir="ltr">公益財団法人 京都技術科学センター</bdi></b><br>
    <bdi lang="ja" dir="ltr">〒606-8305 京都市左京区吉田河原町14</bdi> · <bdi dir="ltr">075-771-6117</bdi><br>
    <span class="small muted">قطار 京阪 出町柳 بـ7 دقايق مشي · باص 川端一条 بدقيقتين</span></div>
    <div><a class="btn" href="{GMAPS}" target="_blank" rel="noopener">Google Maps ↗</a> <a class="btn" href="{OSM}" target="_blank" rel="noopener">OpenStreetMap ↗</a>
    <div class="print-url">{GMAPS}</div></div></div>
  <p class="lead">هالتقرير بيحلّ محل التقريرين القدام، لأنهم كانوا محسوبين من مكان غلط (Kyoto Research Park). <b>وقت المسكليت هون محسوب من طريق فعلي</b> بين كل بيت والشغل (OSRM، ملف الدراجات، ≈14 كم/س). الطلعات ما محسوبة، فالبيوت اللي بالشمال (北区 / 岩倉) ممكن تاخد بالرجعة دقيقتين أو تلاتة زيادة.</p>
  <div class="criteria">
    <span><b>الإيجار + 管理費 + الكراج ≤ ¥100,000</b></span><span>≤ 20 دقيقة بالمسكليت</span><span>2LDK فأكبر</span><span>≥ 45 م²</span>
    <span>مو الطابق الأول</span><span>من الطابق 4 وفوق لازم مصعد</span><span>بناء 2001+ أو خرسانة 1991+</span><span>قائمة 1: 礼金 ≤ شهر</span><span>قائمة 2: 礼金 حتى شهرين</span>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="n">{len(l1)}</div><div class="l">القائمة 1 — 礼金 لحد شهر</div></div>
    <div class="kpi"><div class="n">{len(l2)}</div><div class="l">القائمة 2 — 礼金 لحد شهرين</div></div>
    <div class="kpi"><div class="n">{len(near)}</div><div class="l">خيارات إضافية 21–25 د</div></div>
    <div class="kpi"><div class="n">{sum(1 for u in apts if u.get("parking_cost_src") == "onsite")}</div><div class="l">شقق فيها كراج بالبناية</div></div>
    <div class="kpi"><div class="n">{yen(statistics.median(tot)) if tot else "—"}</div><div class="l">وسيط الإجمالي الشهري مع الكراج</div></div>
  </div>
</header>
<section id="map"><h2>الخريطة</h2>{map_html}</section>
{section(l1, "list1", f"القائمة 1 — 礼金 لحد شهر ({len(l1)})", "مرتبة حسب درجة بتجمع: قرب الشغل، السعر الكلي مع الكراج، المساحة، العزل (سنة البناء ونوع الهيكل)، كراج بالبناية، مصعد، و礼金 صفر.")}
{section(l2, "list2", f"القائمة 2 — 礼金 أكتر من شهر لحد شهرين ({len(l2)})", "نفس الشروط بالضبط، بس 礼金 فيها بين شهر وشهرين. 礼金 ما بيرجع، بس كتير مالكين بيقبلوا ينزلوه لشهر إذا طلب الوكيل، اسأل قبل ما تقرر.")}
{section(houses, "houses", f"بيوت مستقلة ({len(houses)})", "خيار تاني متل ما طلبت. البيوت المستقلة باليابان غالباً خشب، فتأكد من العزل.") if houses else ""}
{section(near, "near", f"خيارات إضافية: 21–25 دقيقة بالمسكليت ({len(near)})", "هدول بيحققوا كل الشروط وإجماليهم مع الكراج ≤ ¥100,000، بس بياخدوا بين 21 و25 دقيقة بالمسكليت، يعني أكتر من حدّك بشوي. حطيتهم لحالهم لأن القائمتين فوق صغار. عمود 礼金 بيبيّن إذا البيت من القائمة 1 أو 2.", max_cards=12) if near else ""}
<section id="parking"><h2>أسعار الكراجات الشهرية (月極駐車場) بالمنطقة</h2>
<p class="lead">إذا البناية ما فيها كراج، حسبت أرخص كراج شهري معلن سعره ضمن 600 م من البيت. انتبه: بعض الكراجات مليانة وعليها قائمة انتظار، ومكتوبة بجانب كل كراج.</p>
<div class="tablewrap"><table><thead><tr><th>الحي</th><th>عدد الكراجات</th><th>الوسيط</th><th>النطاق</th></tr></thead><tbody>{pk_rows}</tbody></table></div></section>
<section id="notes"><h2>ملاحظات</h2>
<div class="note"><b>درجات العزل:</b><ul>
<li><b>A</b>: بناء 2015 وطالع (معيار الطاقة 2013).</li><li><b>B+</b>: 2001–2014 خرسانة RC/SRC (بعد معيار 1999).</li>
<li><b>B / B-</b>: 2001–2014 خشب أو حديد خفيف (軽量鉄骨). الحديد الخفيف لازم تسأل عن عزله.</li>
<li><b>C</b>: 1991–2000 خرسانة. اسأل عن الشبابيك (複層ガラス / 二重サッシ).</li></ul></div>
<div class="note"><b>تكاليف الدخول المعتادة:</b><ul>
<li>敷金 (تأمين، بيرجع جزء منه) · 仲介手数料 (عمولة الوكيل، عادةً شهر + ضريبة) · 保証会社 (شركة ضمان، 50–100% من شهر) · 火災保険 (تأمين حريق) · 鍵交換 (تبديل القفل).</li>
<li>للسيارة لازمك 車庫証明، والمالك بيعطيك 保管場所使用承諾証明書.</li></ul></div>
<div class="note"><b>المصادر:</b> SUUMO، CHINTAI، スマイティ، エイブル، eheya، HOME'S، والكراجات من アットパーキング وタイムズ وPark Direct وp-king وغيرهم. at home حاجب البوتات فما استعملته. كل رابط تفحص وقت الجمع.</div>
</section>
<footer class="end">تم الجمع بتاريخ {TODAY}. الأسعار والشواغر بتتغير بسرعة، فتأكد مع الوكيل. الخريطة © OpenStreetMap contributors.</footer>
</div>'''
    open(out_html, "w", encoding="utf-8").write(page)
    print("wrote", out_html, f"l1={len(l1)} l2={len(l2)} houses={len(houses)}")


if __name__ == "__main__":
    main()
