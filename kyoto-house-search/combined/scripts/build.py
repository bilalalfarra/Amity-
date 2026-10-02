#!/usr/bin/env python3
"""Combined report: homes near the office (budget ≤ ¥107,000 incl. parking) + homes around UR 松ノ木町.
Reads ../sakyo/out/final.json and ../matsu/out/final.json, adds travel times, draws two maps."""
import base64, datetime, importlib.util, json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
sys.path.insert(0, ROOT)
from travel import travel  # noqa: E402
from make_maps import make_map  # noqa: E402

spec = importlib.util.spec_from_file_location("sb", os.path.join(ROOT, "sakyo", "build_report.py"))
SB = importlib.util.module_from_spec(spec); spec.loader.exec_module(SB)
R, e, ja, yen = SB.R, SB.e, SB.ja, SB.yen
TODAY = datetime.date.today().strftime("%Y/%m/%d")
FRIEND_MAPS = "https://www.google.com/maps/search/?api=1&query=34.975815,135.764618"


def t(u, k):
    v = (u.get("travel") or {}).get(k)
    return f'{v["min"]} د' if v else "—"


def travel_row(u, matsu=False):
    tr = u.get("travel") or {}
    ramp = tr.get("ramp")
    bike = [f'الشغل <b class="num">{t(u, "work")}</b>']
    if matsu:
        bike.append(f'بيت رفيقك <b class="num">{t(u, "friend")}</b>')
    bike += [f'محطة JR 京都 <b class="num">{t(u, "jr")}</b>', f'دوشيشا 今出川 <b class="num">{t(u, "doshisha_imadegawa")}</b>']
    car = []
    if ramp:
        car.append(f'أقرب مدخل طريق سريع لأوساكا ({ja(ramp["label"])}) <b class="num">{ramp["min"]} د</b>')
    car.append(f'دوشيشا 京田辺 <b class="num">{t(u, "doshisha_kyotanabe")}</b>')
    return (f'<div class="wide"><span class="k">المشاوير</span><span class="v small">بالمسكليت: {" · ".join(bike)}'
            f'<br>بالسيارة: {" · ".join(car)}</span></div>')


def card(u, matsu=False):
    h = R.card(u, rank_label=f"#{u['rank']}")
    h = h.replace('<div class="wide"><span class="k">الموقف</span>', travel_row(u, matsu) + '<div class="wide"><span class="k">الموقف</span>', 1)
    if (u.get("monthly_total_with_parking") or 0) > 100000:
        h = h.replace("    </div>\n  </header>", '      <div><span class="chip g-bm">بين 100 و107 ألف</span></div>\n    </div>\n  </header>', 1)
    return h


SB.card = card


def matsu_table(units):
    rows = []
    for u in units:
        pk = u.get("parking_cost")
        pk_txt = ("✓ داخلي " if u.get("parking_cost_src") == "onsite" else "قريب ") + ("مجاني" if pk == 0 else yen(pk))
        ramp = (u.get("travel") or {}).get("ramp")
        links = " ".join(f'<a href="{e(url)}" target="_blank" rel="noopener">{e(lab)}</a>' for lab, url in R.labelled_sources(u))
        rows.append(f'''<tr><td class="num">{e(u["rank"])}</td><td>{ja(u.get("building_name") or "—")}<div class="small muted">{ja(u.get("address"))}</div></td>
<td class="num"><b>{yen(u["monthly_total_with_parking"])}</b><div class="small muted">{yen(u["rent"])} + {yen(u.get("kanrihi") or 0)} + {pk_txt}</div></td>
<td><bdi dir="ltr">{e(u["layout"])}</bdi><br><span class="num">{e(u["area_m2"])} م²</span></td>
<td class="num">{e(u.get("floor") or "—")}/{e(u.get("building_floors") or "?")} {"مصعد" if u.get("elevator") else ""}</td>
<td><span class="num">{e(u.get("built_year"))}</span> {e(u.get("structure") or "")}<br>{R.grade_chip(u)}</td>
<td class="num">{t(u, "friend")}</td><td class="num">{t(u, "work")}</td><td class="num">{t(u, "jr")}</td>
<td class="num">{e(ramp["min"]) + " د" if ramp else "—"}</td><td class="small num">{e(u.get("reikin") or "—")}</td>
<td class="links">{links}<div class="print-url">{e(u["sources"][0]["url"])}</div></td></tr>''')
    return f'''<div class="tablewrap"><table><caption>ملخص سريع — مرتب حسب الأفضلية</caption>
<thead><tr><th>#</th><th>المبنى / العنوان</th><th>الإجمالي مع الكراج</th><th>التقسيم</th><th>الطابق</th><th>البناء</th><th>لبيت رفيقك</th><th>للشغل</th><th>لـJR 京都</th><th>للطريق السريع (سيارة)</th><th>礼金</th><th>روابط</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>'''


def fig(path, alt, legend, caption):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return f'<figure><img src="data:image/png;base64,{b64}" alt="{e(alt)}"><div class="legend">{legend}</div><figcaption class="small muted">{caption}</figcaption></figure>'


def dot(col, label):
    return f'<span><span class="dot" style="background:{col}"></span>{label}</span>'


def main():
    out_html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, "report.html")
    S = json.load(open(os.path.join(ROOT, "sakyo", "out", "final.json"), encoding="utf-8"))
    M = json.load(open(os.path.join(ROOT, "matsu", "out", "final.json"), encoding="utf-8"))
    expired = set(json.load(open(os.path.join(OUT, "expired.json")))) if os.path.exists(os.path.join(OUT, "expired.json")) else set()
    for lst in (S, M):
        for u in lst:
            u["sources"] = [s for s in u["sources"] if s["url"] not in expired]
    S = [u for u in S if u["sources"]]
    M = [u for u in M if u["sources"]]
    s_urls = {s["url"] for u in S for s in u["sources"]}
    M = [u for u in M if not any(s["url"] in s_urls for s in u["sources"])]
    for u in S + M:
        u["travel"] = travel(u.get("lat"), u.get("lon"))
    for u in M:   # show the commute to work on the card, not the distance to the friend's place
        w = u["travel"].get("work")
        if w:
            u["bike_min"], u["distance_km"], u["route_km"] = w["min"], w["km"], w["km"]
    M.sort(key=lambda u: -u["score"])
    for i, u in enumerate(M, 1):
        u["rank"] = f"M{i}"

    near = [u for u in S if u["near"]]
    core = [u for u in S if not u["near"]]
    l1 = [u for u in core if not u["is_house"] and u["reikin_group"] == "le1"]
    l2 = [u for u in core if not u["is_house"] and u["reikin_group"] == "le2"]
    houses = [u for u in core if u["is_house"]]
    for u in S:
        u["_col"] = "near" if u["near"] else ("house" if u["is_house"] else u["reikin_group"])
    for u in M:
        u["_col"] = "matsu"

    work_lm = [(35.023968, 135.773178, "#c0392b", "★")]
    friend_lm = [(34.975815, 135.764618, "#c0392b", "★"), (34.987183, 135.758743, "#111111", "JR"),
                 (34.974926, 135.767303, "#555555", "IC"), (34.965160, 135.755417, "#555555", "IC")]
    p1 = make_map(S, work_lm, os.path.join(OUT, "map_work.png"))
    p2 = make_map(M, friend_lm, os.path.join(OUT, "map_matsu.png"), size=(1200, 820))

    css = re.search(r"<style>.*?</style>", open(os.path.join(ROOT, "sakyo", "out", "report.html"), encoding="utf-8").read(), re.S).group(0)
    lots = json.load(open(os.path.join(ROOT, "sakyo", "out", "parking.json"), encoding="utf-8")) + \
        json.load(open(os.path.join(ROOT, "matsu", "out", "parking.json"), encoding="utf-8"))
    seen, pk_stats = set(), {}
    for l in lots:
        if l.get("url") in seen or not l.get("monthly_fee") or l.get("oversize_vehicle"):
            continue
        seen.add(l["url"])
        pk_stats.setdefault(l.get("ward") or R.ward_of(l.get("address")), []).append(l["monthly_fee"])
    pk_rows = "".join(f'<tr><td>{e(w)} <span class="muted">{e(R.WARD_AR.get(w, ""))}</span></td><td class="num">{len(v)}</td><td class="num">{yen(statistics.median(v))}</td><td class="num">{yen(min(v))} – {yen(max(v))}</td></tr>'
                      for w, v in sorted(pk_stats.items(), key=lambda kv: -len(kv[1])) if w and w != "?" and len(v) >= 5)

    allu = l1 + l2 + near + houses + M
    tot = [u["monthly_total_with_parking"] for u in allu]
    S_lead = "مرتبة حسب درجة بتجمع: قرب الشغل، السعر الكلي مع الكراج، المساحة، العزل، كراج بالبناية، مصعد، و礼金 صفر."
    m_lead = ("هدول البيوت ضمن 15 دقيقة بالمسكليت من بيت رفيقك (UR 松ノ木町). جنب بيته مباشرة (東九条) ما لقيت ولا بيت بيحقق الشروط، لأن معظم البنايات هونيك قديمة أو صغيرة، فأقرب شي بـ東山区 و竹田 و深草 و吉祥院. الشغل من هون بياخد عادةً 25–30 دقيقة بالمسكليت، ومعظم الطريق على ممشى نهر 鴨川 بدون إشارات. بس انتبه: "
              "حاسب الطريق بيحسب أقصر طريق، وما بيعرف إنك بتفضّل ممشى النهر، فالوقت الحقيقي على النهر ممكن يكون أقل أو أكتر بدقايق. "
              "مداخل الطريق السريع 鴨川東 و上鳥羽 (第二京阪 / 阪神高速8号 باتجاه أوساكا) قراب كتير، ومحطة JR 京都 على بعد 10 دقايق تقريباً.")

    page = f'''<title>بيوت كيوتو — الشغل وطريق أوساكا</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
{css}
<div class="wrap">
<header>
  <div class="eyebrow">تقرير بحث سكن · كيوتو · {TODAY} · الإصدار المدموج</div>
  <h1>بيوت قرب الشغل، وبيوت قرب رفيقك بـ南区</h1>
  <div class="office"><div><b>الشغل: <bdi lang="ja" dir="ltr">公益財団法人 京都技術科学センター</bdi></b><br>
    <bdi lang="ja" dir="ltr">〒606-8305 京都市左京区吉田河原町14</bdi> · قطار 京阪 出町柳 بـ7 دقايق مشي</div>
    <div><a class="btn" href="{SB.GMAPS}" target="_blank" rel="noopener">الخريطة ↗</a><div class="print-url">{SB.GMAPS}</div></div></div>
  <div class="office"><div><b>بيت رفيقك: <bdi lang="ja" dir="ltr">UR 松ノ木町</bdi></b><br>
    <bdi lang="ja" dir="ltr">〒601-8023 京都市南区東九条南松ノ木町1-1</bdi> · قريب من نهر 鴨川 ومن مداخل الطريق السريع</div>
    <div><a class="btn" href="{FRIEND_MAPS}" target="_blank" rel="noopener">الخريطة ↗</a><div class="print-url">{FRIEND_MAPS}</div></div></div>
  <p class="lead">هالملف بيجمع كلشي: البيوت قرب الشغل لحد ¥107,000 مع الكراج، وقائمة لحالها للبيوت حول بيت رفيقك. لكل بيت حسبت أوقات المشاوير على طريق حقيقي (OSRM): بالمسكليت للشغل، لمحطة JR 京都، ولجامعة دوشيشا 今出川؛ وبالسيارة لأقرب مدخل طريق سريع باتجاه أوساكا ولجامعة دوشيشا 京田辺. ما بعرف أي حرم جامعي بدكن، فحطيت الاتنين.</p>
  <div class="criteria">
    <span><b>الإيجار + 管理費 + الكراج ≤ ¥107,000</b></span><span>2LDK فأكبر</span><span>≥ 45 م²</span><span>مو الطابق الأول</span>
    <span>من الطابق 4 وفوق لازم مصعد</span><span>بناء 2001+ أو خرسانة 1991+</span><span>礼金 لحد شهرين (مقسومة بقوائم)</span>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="n">{len(l1)}</div><div class="l">قرب الشغل — 礼金 لحد شهر</div></div>
    <div class="kpi"><div class="n">{len(l2)}</div><div class="l">قرب الشغل — 礼金 لحد شهرين</div></div>
    <div class="kpi"><div class="n">{len(near) + len(houses)}</div><div class="l">إضافي: 21–25 د وبيوت مستقلة</div></div>
    <div class="kpi"><div class="n">{len(M)}</div><div class="l">حول بيت رفيقك (松ノ木町)</div></div>
    <div class="kpi"><div class="n">{yen(statistics.median(tot)) if tot else "—"}</div><div class="l">وسيط الإجمالي الشهري مع الكراج</div></div>
  </div>
</header>

<h2 style="border-bottom-width:4px">القسم الأول — قرب الشغل (≤ 20 دقيقة بالمسكليت)</h2>
<section id="map1">{fig(p1, "خريطة الشغل والبيوت القريبة", dot("#c0392b", "★ الشغل") + dot("#2f6b4f", "礼金 لحد شهر") + dot("#b86e00", "礼金 لحد شهرين") + dot("#7a8590", "N = 21–25 د") + dot("#6a4c93", "H = بيت مستقل"), "الرقم على كل نقطة = رقم البيت بالتقرير. الموقع دقيق لحد الحي (±300 م).")}</section>
{SB.section(l1, "list1", f"القائمة 1 — 礼金 لحد شهر ({len(l1)})", S_lead)}
{SB.section(l2, "list2", f"القائمة 2 — 礼金 أكتر من شهر لحد شهرين ({len(l2)})", "نفس الشروط، بس 礼金 بين شهر وشهرين. كتير مالكين بيقبلوا ينزلوه لشهر إذا طلب الوكيل.")}
{SB.section(houses, "houses", f"بيوت مستقلة ({len(houses)})", "بيت مستقل ضمن 20 دقيقة، خيار تاني متل ما طلبت.") if houses else ""}
{SB.section(near, "near", f"خيارات إضافية: 21–25 دقيقة بالمسكليت ({len(near)})", "بيحققوا كل الشروط بس بياخدوا 21–25 دقيقة للشغل، يعني أكتر من حدّك بشوي. عمود 礼金 بيبين القائمة.", max_cards=12) if near else ""}

<h2 style="border-bottom-width:4px">القسم الثاني — حول بيت رفيقك (UR 松ノ木町)</h2>
<section id="matsu"><p class="lead">{m_lead}</p>
{fig(p2, "خريطة البيوت حول UR 松ノ木町", dot("#c0392b", "★ بيت رفيقك") + dot("#111111", "JR = محطة 京都") + dot("#555555", "IC = مدخل طريق سريع (鴨川東 / 上鳥羽)") + dot("#1f5f99", "M = بيت بهالقائمة"), "الرقم على كل نقطة = رقم البيت.")}
{matsu_table(M) if M else '<p class="lead">ما لقيت بيوت بهالشروط حول بيت رفيقك.</p>'}
<div class="cards">{"".join(card(u, matsu=True) for u in M)}</div></section>

<section id="parking"><h2>أسعار الكراجات الشهرية (月極駐車場) حسب الحي</h2>
<p class="lead">إذا البناية ما فيها كراج، حسبت أرخص كراج شهري معلن سعره ضمن 600 م من البيت. بعض الكراجات مليانة وعليها قائمة انتظار، ومكتوبة جنب كل كراج.</p>
<div class="tablewrap"><table><thead><tr><th>الحي</th><th>عدد الكراجات</th><th>الوسيط</th><th>النطاق</th></tr></thead><tbody>{pk_rows}</tbody></table></div></section>
<section id="notes"><h2>ملاحظات</h2>
<div class="note"><b>درجات العزل:</b> A = بناء 2015+ · B+ = 2001–2014 خرسانة · B / B- = 2001–2014 خشب أو حديد خفيف (اسأل عن العزل) · C = 1991–2000 خرسانة (اسأل عن الشبابيك 複層ガラス / 二重サッシ).</div>
<div class="note"><b>الأوقات:</b> بالمسكليت ≈14 كم/س بدون حساب الطلعات (البيوت بالشمال أعلى من الشغل)؛ بالسيارة بدون زحمة. مداخل الطريق السريع المحسوبة: 鴨川西 و鴨川東 و上鳥羽 على 第二京阪 / 阪神高速8号 باتجاه أوساكا.</div>
<div class="note"><b>المصادر:</b> SUUMO، CHINTAI، スマイティ، エイブル، eheya، HOME'S، والكراجات من アットパーキング وタイムズ وPark Direct وp-king وغيرهم. at home حاجب البوتات. كل رابط تفحص.</div>
</section>
<footer class="end">تم الجمع بتاريخ {TODAY}. الأسعار والشواغر بتتغير بسرعة، فتأكد مع الوكيل. الخرائط © OpenStreetMap contributors.</footer>
</div>'''
    open(out_html, "w", encoding="utf-8").write(page)
    print("wrote", out_html, f"l1={len(l1)} l2={len(l2)} near={len(near)} houses={len(houses)} matsu={len(M)}")


if __name__ == "__main__":
    main()
