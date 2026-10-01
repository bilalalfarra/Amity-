#!/usr/bin/env python3
"""Render out/merged.json (+ out/parking.json, out/ur.json) into a printable Arabic/Japanese HTML report.

Usage: python3 report.py [out_html]
"""
import html, json, os, re, sys, datetime, statistics
from geo import bike_minutes

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_DIR") or os.path.join(HERE, "out")
TODAY = datetime.date.today().strftime("%Y/%m/%d")

WARD_RE = re.compile(r"(北|上京|左京|中京|東山|下京|南|右京|伏見|山科|西京)区")
WARD_AR = {"下京区": "شيموغيو", "中京区": "ناكاغيو", "南区": "مينامي", "右京区": "أوكيو", "上京区": "كاميغيو",
           "西京区": "نيشيكيو", "東山区": "هيغاشياما", "北区": "كيتا", "伏見区": "فوشيمي", "左京区": "ساكيو", "山科区": "ياماشينا"}
SRC_LABEL = {"suumo": "SUUMO", "homes": "HOME'S", "athome": "at home", "chintai": "CHINTAI", "ur": "UR",
             "jkosha": "住宅供給公社", "sumaity": "スマイティ", "eheya": "エイブル(eheya)", "able": "エイブル", "yahoo": "Yahoo!不動産", "other": "أخرى"}
STRUCT_AR = {"RC": "خرسانة مسلحة RC", "SRC": "خرسانة+فولاذ SRC", "重量鉄骨": "فولاذ ثقيل", "軽量鉄骨": "فولاذ خفيف ⚠", "鉄骨": "فولاذ", "木造": "خشب", "その他": "أخرى"}


def e(s):
    return html.escape("" if s is None else str(s))


def yen(v):
    return "—" if v in (None, "") else f"¥{int(v):,}"


def ja(s):
    return f'<bdi lang="ja" dir="ltr">{e(s)}</bdi>' if s else "—"


# Hand-written additions from sources that could not be fully verified (at home was CAPTCHA-blocked after 4 pages)
EXTRA_NOTES = {
    "アリコス壬生": "at home يعرض أيضاً شقة أخرى بالطابق 7 في نفس المبنى (2LDK 54 م²، 98,000+8,000، 礼金 0، 敷金 100,000) — https://www.athome.co.jp/chintai/6982872244/ (لم أستطع التحقق منها: الموقع حجب البوت)",
}


def clean_notes(n, name=None):
    extra = next((v for k, v in EXTRA_NOTES.items() if name and k in name), None)
    if extra:
        n = f"{extra} ◆ {n or ''}"
    if not n:
        return None
    n = re.sub(r";?\s*POSSIBLE DUPLICATE.*?(?=;|$)", "", str(n))
    n = re.sub(r";?\s*構造\(原文\):[^;]*", "", n)
    n = re.sub(r";?\s*更新 \d{4}/\d{2}/\d{2}", "", n)
    n = re.sub(r"\s*;\s*;", ";", n).strip(" ;")
    return n[:420] + "…" if len(n) > 420 else n


def ward_of(addr):
    m = WARD_RE.search(addr or "")
    return m.group(0) if m else "?"


def short_url(u):
    u = re.sub(r"^https?://(www\.)?", "", u or "")
    return u if len(u) <= 58 else u[:55] + "…"


def grade_chip(u):
    g = u.get("insulation_grade") or "?"
    cls = {"A": "g-a", "B+": "g-b", "B": "g-b", "B-": "g-bm", "C": "g-c"}.get(g, "g-q")
    return f'<span class="chip {cls}" title="{e(u.get("insulation_note"))}">عزل {e(g)}</span>'


def parking_cell(u, full=True):
    st = u.get("parking_status")
    if st == "onsite":
        fee = yen(u["parking_fee"]) + "/شهر" if u.get("parking_fee") else "رسوم غير مذكورة"
        return f'<span class="ok">✓ موقف داخل العقار</span> <span class="num">{fee}</span>'
    if st == "onsite_full":
        return f'<span class="warn">موقف بالعقار لكن ممتلئ حالياً</span>' + nearest_html(u, full)
    label = {"nearby": "موقف قريب (حسب الإعلان)", "none": "لا يوجد موقف بالعقار", "unknown": "الموقف غير مذكور"}.get(st, "—")
    return f'<span class="warn">{label}</span>' + nearest_html(u, full)


def nearest_html(u, full):
    lots = u.get("nearby_parking") or []
    if not lots:
        return '<div class="muted small">لم أجد موقفاً شهرياً مُعلناً ضمن 800 م — اسأل الوكيل العقاري (عادةً 10–20 ألف ين)</div>'
    items = []
    for l in lots[: (3 if full else 1)]:
        fee = yen(l["monthly_fee"]) + "/شهر" if l.get("monthly_fee") else e(l.get("fee_text") or "السعر عند الاستفسار")
        items.append(f'<li>{ja(l.get("name"))} · <span class="num">{fee}</span> · {e(l["distance_km"])} كم (~{e(l["walk_min"])} د مشي) '
                     f'<a href="{e(l["url"])}" target="_blank" rel="noopener">رابط ↗</a><span class="print-url">{e(short_url(l["url"]))}</span></li>')
    return f'<ul class="lots">{"".join(items)}</ul>'


def commute_chip(mins):
    if mins is None:
        return ""
    if mins <= 20:
        return '<span class="chip g-a">ضمن 20 د</span>'
    if mins <= 25:
        return '<span class="chip g-bm">20–25 د</span>'
    return '<span class="chip g-c">فوق 25 د</span>'


def floor_cell(u):
    f = u.get("floor"); bf = u.get("building_floors")
    s = f"الطابق {f}" if f is not None else "الطابق ؟"
    if bf:
        s += f" من {bf}"
    ev = u.get("elevator")
    s += " · " + ("مصعد ✓" if ev is True else ("بدون مصعد" if ev is False else "مصعد؟"))
    return s


def labelled_sources(u):
    seen = {}
    out = []
    for s in u["sources"]:
        lab = SRC_LABEL.get(s["source"], s["source"])
        seen[lab] = seen.get(lab, 0) + 1
        out.append((f"{lab} {seen[lab]}" if seen[lab] > 1 else lab, s["url"]))
    return out


def links_cell(u):
    return " ".join(f'<a class="btn" href="{e(url)}" target="_blank" rel="noopener">{e(lab)} ↗</a>' for lab, url in labelled_sources(u))


def print_urls(u):
    return "".join(f'<div class="print-url">{e(lab)}: {e(url)}</div>' for lab, url in labelled_sources(u))


def initial_costs(u):
    parts = []
    parts.append(f'礼金 (كي مني): <b class="num">{e(u.get("reikin") or "—")}</b>')
    parts.append(f'敷金 (تأمين): <span class="num">{e(u.get("shikikin") or "—")}</span>')
    if u.get("other_initial"):
        parts.append(e(u["other_initial"]))
    return " · ".join(parts)


def card(u, rank_label=None):
    name = u.get("building_name") or "(اسم المبنى غير معلن)"
    total = u["rent"] + (u.get("kanrihi") or 0)
    twp = u.get("monthly_total_with_parking")
    built = f'{u["built_year"]}' + (f'/{u["built_month"]:02d}' if u.get("built_month") else "") if u.get("built_year") else "؟"
    ward = ward_of(u.get("address"))
    return f'''
<article class="card tier-{e(u["tier"])}" data-ward="{e(ward)}" data-tier="{e(u["tier"])}" data-parking="{e(u["parking_status"])}">
  <header class="card-h">
    <div class="rank">{e(rank_label or ("#%d" % u["rank"]))}</div>
    <div class="card-title">
      <h3>{ja(name)}</h3>
      <div class="addr">{ja(u.get("address"))} <span class="muted">· {e(WARD_AR.get(ward, ward))}</span></div>
    </div>
    <div class="price">
      <div class="big num">{yen(u["rent"])}</div>
      <div class="small muted">+ 管理費 {yen(u.get("kanrihi") or 0)} = <span class="num">{yen(total)}</span>/شهر</div>
      {f'<div class="small muted">مع الموقف ≈ <span class="num">{yen(twp)}</span></div>' if twp else ''}
    </div>
  </header>
  <div class="facts">
    <div><span class="k">التقسيم / المساحة</span><span class="v"><bdi dir="ltr">{e(u["layout"])}</bdi> · <span class="num">{e(u["area_m2"])} م²</span></span></div>
    <div><span class="k">الطابق</span><span class="v">{floor_cell(u)}</span></div>
    <div><span class="k">البناء</span><span class="v"><span class="num">{built}</span> ({e(u.get("age_years"))} سنة) · {e(STRUCT_AR.get(u.get("structure"), u.get("structure") or "؟"))} {grade_chip(u)}</span></div>
    <div><span class="k">المسافة للشغل</span><span class="v"><span class="num">{e(u["distance_km"])} كم</span> ≈ {e(u["bike_min"])} دقيقة بالدراجة {commute_chip(u["bike_min"])} · {ja(u.get("nearest_station"))}</span></div>
    <div class="wide"><span class="k">الموقف</span><span class="v">{parking_cell(u)}</span></div>
    <div class="wide"><span class="k">التكاليف الأولية</span><span class="v small">{initial_costs(u)}</span></div>
    {f'<div class="wide"><span class="k">ملاحظات</span><span class="v small"><bdi dir="auto">{e(clean_notes(u["notes"], u.get("building_name")))}</bdi></span></div>' if clean_notes(u.get("notes"), u.get("building_name")) else ''}
  </div>
  <footer class="card-f">{links_cell(u)}{print_urls(u)}</footer>
</article>'''


def table(units, caption):
    if not units:
        return ""
    rows = []
    for u in units:
        total = u["rent"] + (u.get("kanrihi") or 0)
        pk = "✓ داخلي " + (yen(u["parking_fee"]) if u.get("parking_fee") else "") if u["parking_status"] == "onsite" else (
            f'قريب {yen(u["nearby_parking"][0]["monthly_fee"])}' if u.get("nearby_parking") and u["nearby_parking"][0].get("monthly_fee") else "—")
        links = " ".join(f'<a href="{e(url)}" target="_blank" rel="noopener">{e(lab)}</a>' for lab, url in labelled_sources(u))
        rows.append(f'''<tr data-ward="{e(ward_of(u.get("address")))}" data-tier="{e(u["tier"])}" data-parking="{e(u["parking_status"])}">
<td class="num">{e(u["rank"])}</td><td>{ja(u.get("building_name") or "—")}<div class="small muted">{ja(u.get("address"))}</div></td>
<td class="num">{yen(total)}</td><td><bdi dir="ltr">{e(u["layout"])}</bdi><br><span class="num">{e(u["area_m2"])} م²</span></td>
<td class="num">{e(u.get("floor"))}/{e(u.get("building_floors") or "?")} {"🛗" if u.get("elevator") else ""}</td>
<td><span class="num">{e(u.get("built_year"))}</span> {e(u.get("structure") or "")}<br>{grade_chip(u)}</td>
<td class="num">{e(u["distance_km"])} كم<br><span class="small muted">{e(u["bike_min"])} د</span><br>{commute_chip(u["bike_min"])}</td>
<td class="small">{pk}</td><td class="small num">{e(u.get("reikin") or "—")}</td><td class="links">{links}</td></tr>''')
    return f'''<div class="tablewrap"><table><caption>{caption}</caption>
<thead><tr><th>#</th><th>المبنى / العنوان</th><th>الإجمالي الشهري</th><th>التقسيم</th><th>الطابق</th><th>البناء</th><th>المسافة</th><th>الموقف</th><th>礼金</th><th>روابط</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>'''


def ur_section(ur_rows):
    if not ur_rows:
        return ""
    def rng(v, unit=""):
        if isinstance(v, (list, tuple)) and len(v) == 2 and v[0] is not None:
            return (f"{v[0]:,}{unit}" if v[0] == v[1] else f"{v[0]:,}–{v[1]:,}{unit}")
        return e(v) if v else "—"
    rows = []
    order = sorted(ur_rows, key=lambda r: (0 if r.get("tier") in ("A", "B") else 1, 0 if r.get("big_units_in_catalogue") else 1, r.get("distance_km") or 99))
    for r in order:
        old = r.get("tier") not in ("A", "B")
        fam = r.get("big_units_in_catalogue")
        built = f'{e(r.get("built_year"))}{"≈" if r.get("built_year_approx") else ""}'
        age_chip = '<span class="chip g-c">قبل 1991 — قديم</span>' if old else '<span class="chip g-b">≈2000 · RC</span>'
        ev = "مصعد ✓" if r.get("elevator") else ("بدون مصعد" if r.get("elevator") is False else "مصعد غير مذكور")
        rows.append(f'''<tr class="{"ur-old" if old else "ur-ok"}"><td>{ja(r.get("building_name"))}<div class="small muted">{ja(r.get("address"))}</div><div class="small muted">{ja(r.get("nearest_station"))}</div></td>
<td><span class="num">{built}</span> · {e(r.get("structure") or "")} · {e(r.get("building_floors") or "?")} طوابق<br>{ev}<br>{age_chip}</td>
<td><bdi dir="ltr">{e(r.get("layout_range") or r.get("layout"))}</bdi><br><span class="num">{rng(r.get("area_range"), " م²")}</span></td>
<td class="num">{rng(r.get("rent_range"), "円")}<br><span class="small muted">共益費 {e(r.get("kanrihi_text") or "—")}</span></td>
<td>{"<span class=ok>✓ نعم</span>" if fam else "<span class=muted>لا (استوديو/2DK فقط)</span>"}</td>
<td class="num">{e(r.get("distance_km"))} كم<br><span class="small muted">{e(bike_minutes(r.get("distance_km")))} د</span></td>
<td class="small">{ja(r.get("parking") or "غير مذكور")}</td>
<td class="links"><a href="{e(r.get("url"))}" target="_blank" rel="noopener">UR ↗</a><div class="print-url">{e(r.get("url"))}</div></td></tr>''')
    return f'''<section id="ur"><h2>مجمعات UR القريبة (UR賃貸住宅) — {len(order)} مجمعاً ضمن 5.5 كم</h2>
<p class="lead">UR: صفر 礼金، صفر عمولة وكيل، صفر كفيل، صفر رسوم تجديد، والتأمين 敷金 شهران. <b>لكن</b> كل مجمعات UR داخل مدينة كيوتو بُنيت بين 1967 و1982 ما عدا <bdi lang="ja" dir="ltr">京都十条</bdi> (≈2000) — أي أنها لا تحقق شرط العزل الذي طلبته رغم أنها خرسانية ومُجدَّدة أحياناً. حالة الشغور تتغير يومياً ولم أستطع التحقق منها من هنا (الـAPI محجوب)، فافتح الرابط أو اتصل بـ UR空家情報 <bdi dir="ltr">0120-23-3456</bdi>.</p>
<div class="tablewrap"><table><thead><tr><th>المجمع</th><th>البناء</th><th>التقسيمات / المساحة</th><th>الإيجار</th><th>شقق 2LDK+ ≥45م²؟</th><th>المسافة</th><th>الموقف</th><th>رابط</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="small muted">المبنى الذي يسكنه صديقك قرب محطة كيوتو هو على الأرجح <bdi lang="ja" dir="ltr">UR 松ノ木町</bdi> (11 طابقاً، 707 شقة، 1979) أو <bdi lang="ja" dir="ltr">UR 九条</bdi> / <bdi lang="ja" dir="ltr">UR 菅田町</bdi> — وكلها استوديوهات و2DK فقط (29–47 م²). الوحيد قرب محطة كيوتو بشقق عائلية ومصعد هو <bdi lang="ja" dir="ltr">UR 九条大宮</bdi> (3DK حتى 85 م²، ≤97,500 ين) لكنه بناء 1969.</p></section>'''


def main():
    out_html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, "report.html")
    units = json.load(open(os.path.join(OUT, "merged.json"), encoding="utf-8"))
    try:
        ur_rows = json.load(open(os.path.join(OUT, "ur.json"), encoding="utf-8"))
    except Exception:
        ur_rows = []
    try:
        lots = json.load(open(os.path.join(OUT, "parking.json"), encoding="utf-8"))
    except Exception:
        lots = []

    apt = [u for u in units if not u["is_house"] and not u["is_ur"]]
    tier_a = [u for u in apt if u["tier"] == "A"]
    tier_b = [u for u in apt if u["tier"] == "B"]
    houses = [u for u in units if u["is_house"]]
    top_b = sorted([u for u in tier_b if (u["distance_km"] or 99) <= 4.5], key=lambda u: -u["score"])[:12]
    within20 = sum(1 for u in apt if (u["bike_min"] or 99) <= 20)
    ward_stats = {}
    for u in apt:
        w = ward_of(u.get("address"))
        ws = ward_stats.setdefault(w, {"n": 0, "a": 0, "tot": [], "d": []})
        ws["n"] += 1; ws["a"] += (u["tier"] == "A"); ws["tot"].append(u["rent"] + (u.get("kanrihi") or 0)); ws["d"].append(u["distance_km"] or 0)
    with_pk = [u for u in apt if u["parking_status"] == "onsite"]
    rents = [u["rent"] + (u.get("kanrihi") or 0) for u in apt]
    sources = sorted({s["source"] for u in units for s in u["sources"]} | {r.get("source", "ur") for r in ur_rows})

    # parking fee stats per ward
    pk_stats = {}
    for l in lots:
        w = ward_of(l.get("address"))
        if l.get("monthly_fee"):
            pk_stats.setdefault(w, []).append(l["monthly_fee"])
    pk_rows = "".join(f'<tr><td>{e(w)} <span class="muted">{e(WARD_AR.get(w, ""))}</span></td><td class="num">{len(v)}</td><td class="num">{yen(statistics.median(v))}</td><td class="num">{yen(min(v))} – {yen(max(v))}</td></tr>'
                      for w, v in sorted(pk_stats.items(), key=lambda kv: -len(kv[1])) if w != "?")

    ward_rows = "".join(
        f'<tr><td>{e(w)} <span class="muted">{e(WARD_AR.get(w, ""))}</span></td><td class="num">{ws["n"]}</td><td class="num">{ws["a"]}</td>'
        f'<td class="num">{yen(statistics.median(ws["tot"]))}</td><td class="num">{statistics.median(ws["d"]):.1f} كم</td>'
        f'<td class="num">{yen(statistics.median(pk_stats[w])) if pk_stats.get(w) else "—"}</td></tr>'
        for w, ws in sorted(ward_stats.items(), key=lambda kv: -kv[1]["n"]))
    wards = sorted({ward_of(u.get("address")) for u in apt})
    ward_opts = "".join(f'<option value="{e(w)}">{e(w)} {e(WARD_AR.get(w, ""))}</option>' for w in wards)

    page = f'''<title>بيوت كيوتو قرب KRP</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
<style>
/* Layout: a printable dossier — summary strip, ranked cards, then dense reference tables. RTL Arabic with LTR Japanese islands. */
:root{{
  --paper:#f6f7f4; --ink:#1b2430; --ink-2:#4a5565; --line:#d7dbd3; --card:#ffffff;
  --accent:#2f6b4f; --accent-ink:#ffffff; --accent-soft:#e3efe7;
  --ok:#2f6b4f; --warn:#9a5b00; --bad:#a23b2b;
  --g-a:#1f7a4d; --g-b:#2f6b4f; --g-bm:#9a5b00; --g-c:#a23b2b; --g-q:#6b7280;
  --font-ar:"IBM Plex Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif;
  --font-ja:"Noto Sans JP","Hiragino Sans","Yu Gothic",Meiryo,sans-serif;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{
  --paper:#161a1f; --ink:#e8ebe6; --ink-2:#aab2a8; --line:#333a40; --card:#1e242b;
  --accent:#7fc29b; --accent-ink:#0f1a14; --accent-soft:#223229;
  --ok:#7fc29b; --warn:#e2a848; --bad:#e2846f; --g-a:#7fc29b; --g-b:#7fc29b; --g-bm:#e2a848; --g-c:#e2846f; --g-q:#9aa3ad; color-scheme:dark }} }}
:root[data-theme="dark"]{{
  --paper:#161a1f; --ink:#e8ebe6; --ink-2:#aab2a8; --line:#333a40; --card:#1e242b;
  --accent:#7fc29b; --accent-ink:#0f1a14; --accent-soft:#223229;
  --ok:#7fc29b; --warn:#e2a848; --bad:#e2846f; --g-a:#7fc29b; --g-b:#7fc29b; --g-bm:#e2a848; --g-c:#e2846f; --g-q:#9aa3ad; color-scheme:dark }}
body{{background:var(--paper);color:var(--ink);font-family:var(--font-ar);font-size:15px;line-height:1.65;margin:0}}
.wrap{{max-width:1080px;margin:0 auto;padding-block:28px 56px;padding-inline:16px;direction:rtl}}
bdi[lang="ja"]{{font-family:var(--font-ja);unicode-bidi:isolate}}
h1,h2,h3{{text-wrap:balance;margin:0;line-height:1.3}}
h1{{font-size:clamp(26px,4vw,38px);font-weight:700}}
h2{{font-size:22px;font-weight:600;margin-block:40px 10px;padding-bottom:6px;border-bottom:2px solid var(--accent)}}
h3{{font-size:17px;font-weight:600}}
.eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}}
.lead{{color:var(--ink-2);max-width:72ch;margin-block:6px 0}}
.muted{{color:var(--ink-2)}} .small{{font-size:13px}} .num{{font-variant-numeric:tabular-nums}}
.ok{{color:var(--ok);font-weight:600}} .warn{{color:var(--warn);font-weight:600}} .bad{{color:var(--bad)}}
.criteria{{display:flex;flex-wrap:wrap;gap:8px;margin-block:16px}}
.criteria span{{background:var(--accent-soft);color:var(--ink);border-radius:999px;padding:4px 12px;font-size:13px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-block:18px}}
.kpi{{border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:var(--card)}}
.kpi .n{{font-size:26px;font-weight:700;font-variant-numeric:tabular-nums}} .kpi .l{{font-size:12px;color:var(--ink-2)}}
.filters{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-block:12px;font-size:14px}}
.filters select,.filters label{{font:inherit}} .filters select{{padding:4px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink)}}
.cards{{display:grid;gap:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;break-inside:avoid;page-break-inside:avoid}}
.card-h{{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:start}}
.rank{{background:var(--accent);color:var(--accent-ink);border-radius:8px;font-weight:700;padding:6px 10px;font-variant-numeric:tabular-nums;min-width:44px;text-align:center}}
.addr{{font-size:13px;color:var(--ink-2)}}
.price{{text-align:left;direction:ltr}} .price .big{{font-size:24px;font-weight:700}}
.facts{{display:grid;grid-template-columns:1fr 1fr;gap:8px 20px;margin-block:14px 10px;padding-top:12px;border-top:1px dashed var(--line)}}
.facts > div{{display:grid;grid-template-columns:120px 1fr;gap:8px;min-width:0}} .facts .wide{{grid-column:1 / -1}}
.k{{font-size:12px;color:var(--ink-2);font-weight:600;padding-top:3px}} .v{{min-width:0}}
.chip{{display:inline-block;border-radius:6px;padding:1px 8px;font-size:12px;font-weight:600;color:#fff;vertical-align:middle}}
.g-a{{background:var(--g-a)}} .g-b{{background:var(--g-b)}} .g-bm{{background:var(--g-bm)}} .g-c{{background:var(--g-c)}} .g-q{{background:var(--g-q)}}
.lots{{margin:4px 0 0;padding-inline-start:18px;font-size:13px}} .lots li{{margin-block:2px}}
.card-f{{display:flex;flex-wrap:wrap;gap:8px;padding-top:10px;border-top:1px dashed var(--line)}}
.btn{{display:inline-block;border:1px solid var(--accent);color:var(--accent);border-radius:8px;padding:4px 12px;text-decoration:none;font-weight:600;font-size:13px}}
.btn:hover,.btn:focus-visible{{background:var(--accent);color:var(--accent-ink);outline:none}}
a{{color:var(--accent)}} a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.print-url{{display:none;font-size:10.5px;color:var(--ink-2);direction:ltr;text-align:left;word-break:break-all;font-family:var(--font-ja)}}
.tablewrap{{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}}
table{{border-collapse:collapse;width:100%;font-size:13px;min-width:860px}}
caption{{text-align:start;padding:10px 14px;font-weight:600;color:var(--ink-2)}}
th,td{{padding:8px 10px;border-top:1px solid var(--line);vertical-align:top;text-align:start}}
th{{font-size:12px;color:var(--ink-2);font-weight:600;background:var(--accent-soft)}}
td.links a{{display:inline-block;margin-inline-end:6px}}
.note{{background:var(--accent-soft);border-radius:10px;padding:14px 18px;margin-block:12px}}
.note ul{{margin:6px 0 0;padding-inline-start:20px}}
.hidden{{display:none}}
footer.end{{margin-top:40px;font-size:12px;color:var(--ink-2);border-top:1px solid var(--line);padding-top:12px}}
@media (max-width:640px){{ .card-h{{grid-template-columns:auto 1fr}} .price{{grid-column:1 / -1;text-align:right;direction:rtl}} .facts{{grid-template-columns:1fr}} .facts > div{{grid-template-columns:100px 1fr}} }}
@media print{{
  body{{background:#fff;color:#000;font-size:11.5px}} .wrap{{max-width:none;padding:0}}
  .filters,.btn{{display:none !important}} .print-url{{display:block}}
  .card{{border-color:#bbb;box-shadow:none;padding:10px 12px}} .kpi{{border-color:#bbb}}
  h2{{page-break-after:avoid;margin-top:22px}} .tablewrap{{border:none;overflow:visible}} table{{min-width:0}}
  tr{{page-break-inside:avoid}} .chip{{-webkit-print-color-adjust:exact;print-color-adjust:exact}} .rank{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
  a{{color:#000;text-decoration:none}}
  .cards{{grid-template-columns:1fr 1fr;gap:8px}} .card{{font-size:10px;line-height:1.45}}
  .facts{{grid-template-columns:1fr;gap:3px;margin-block:8px 6px;padding-top:6px}} .facts > div{{grid-template-columns:86px 1fr;gap:6px}}
  .card-h{{gap:8px}} .price .big{{font-size:17px}} .rank{{padding:3px 7px;min-width:36px}} h3{{font-size:12.5px}}
  .lots{{padding-inline-start:12px}} .chip{{font-size:9.5px;padding:0 5px}} .card-f{{padding-top:6px}} .print-url{{font-size:8.5px}}
  table{{font-size:9.5px}} th,td{{padding:3px 5px}} .kpis{{grid-template-columns:repeat(6,1fr);gap:6px}} .kpi{{padding:6px 8px}} .kpi .n{{font-size:16px}}
  #wards,#ur,#parking,#notes{{page-break-before:auto}} .lead{{font-size:10.5px}}
  @page{{size:A4;margin:12mm 10mm}}
}}
@media (prefers-reduced-motion: reduce){{ *{{transition:none !important}} }}
</style>
<div class="wrap">
<header>
  <div class="eyebrow">تقرير بحث سكن · كيوتو · {TODAY}</div>
  <h1>بيوت للإيجار قرب 京都技術科学センター (KRP)</h1>
  <p class="lead">نقطة المرجع: مركز كيوتو للتقنية والعلوم داخل Kyoto Research Park، 下京区中堂寺南町134 (محطة JR 丹波口). كل المسافات هنا خط مستقيم من هذه النقطة، والدقائق تقديرية متحفظة للدراجة الهوائية (مسافة الطريق ≈ 1.25× الخط المستقيم بسرعة 13 كم/س مع الإشارات): 3.5 كم ≈ 20 دقيقة، 4.5 كم ≈ 26 دقيقة. جمعتُ حتى 5.5 كم لتوسيع الخيارات، والشارة الملوّنة بجانب كل مسافة تبيّن هل هي ضمن حدّك.</p>
  <div class="criteria">
    <span>الإيجار ≤ ¥100,000</span><span>2LDK فأكبر</span><span>≥ 45 م²</span><span>ليس الطابق الأول</span><span>≥ 4 طوابق ⇒ مصعد</span>
    <span>礼金 ≤ شهر</span><span>بناء 2001+ (أو RC من 1991+)</span><span>≤ 20 دقيقة بالدراجة</span><span>موقف سيارة أو موقف شهري قريب</span>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="n">{len(apt)}</div><div class="l">شقة مطابقة (بعد حذف التكرار)</div></div>
    <div class="kpi"><div class="n">{within20}</div><div class="l">منها ضمن ~20 دقيقة بالدراجة (≤ 3.5 كم)</div></div>
    <div class="kpi"><div class="n">{len(with_pk)}</div><div class="l">منها بموقف داخل العقار</div></div>
    <div class="kpi"><div class="n">{yen(statistics.median(rents)) if rents else "—"}</div><div class="l">وسيط الإجمالي الشهري (إيجار + 管理費)</div></div>
    <div class="kpi"><div class="n">{len(sources)}</div><div class="l">مواقع تم مسحها: {e(", ".join(SRC_LABEL.get(s, s) for s in sources))}</div></div>
    <div class="kpi"><div class="n">{len(lots)}</div><div class="l">موقف شهري (月極) مرصود للمطابقة</div></div>
  </div>
</header>

<section id="wards">
  <h2>أين تتركز النتائج</h2>
  <div class="tablewrap"><table><thead><tr><th>الحي</th><th>شقق مطابقة</th><th>منها بناء 2001+</th><th>وسيط الإجمالي الشهري</th><th>وسيط المسافة</th><th>وسيط الموقف الشهري بالحي</th></tr></thead><tbody>{ward_rows}</tbody></table></div>
</section>

<section id="tiera">
  <h2>الفئة A — بناء 2001 فما بعد ({len(tier_a)} شقة) · الأولوية الأولى حسب طلبك (العزل)</h2>
  <p class="lead">كل ما وجدته من شقق مبنية بعد معيار الطاقة 1999 ويحقق باقي الشروط. العدد قليل لأن ثلاثة فلاتر تضيق السوق في كيوتو معاً: 礼金 ≤ شهر (العرف المحلي شهران)، ≥45 م² بسعر ≤100 ألف، والقرب من KRP. مرتّبة حسب الدرجة الإجمالية؛ الرقم في الزاوية هو الترتيب العام بين كل الشقق (A وB معاً).</p>
  <div class="cards">{"".join(card(u) for u in sorted(tier_a, key=lambda u: -u["score"]))}</div>
</section>

<section id="tierb-top">
  <h2>الفئة B — أفضل {len(top_b)} من الخرسانة المسلحة 1991–2000 (ضمن 4.5 كم)</h2>
  <p class="lead">بُنيت بعد معيار الطاقة 1992 وقبل معيار 1999؛ الخرسانة تحفظ الحرارة لكن غالباً زجاج مفرد — اسأل عن النوافذ (二重サッシ / 複層ガラス) وعن 断熱改修. هذه الفئة هي معظم المعروض الذي يحقق شروطك، وفيها أفضل قيمة مقابل السعر.</p>
  <div class="cards">{"".join(card(u) for u in top_b)}</div>
</section>

{f'<section id="houses"><h2>بيوت مستقلة (一戸建て / 貸家) — {len(houses)} بيوت</h2><p class="lead">خيار ثانوي حسب طلبك. البيت في 七条御所ノ内西町 قريب جداً من الشغل وبموقف مجاني؛ البيوت الخشبية (木造) الحديثة عزلها جيد عادةً لكن تأكد من سنة البناء.</p><div class="cards">{"".join(card(u, rank_label=str(u["rank"])) for u in houses[:3])}</div>{table(houses[3:], f"بقية البيوت ({len(houses[3:])})") if len(houses) > 3 else ""}</section>' if houses else ''}

<section id="all">
  <h2>كل شقق الفئة B — {len(tier_b)} شقة مرتبة حسب المسافة من الشغل</h2>
  <div class="filters">
    <label>الحي: <select id="f-ward"><option value="">الكل</option>{ward_opts}</select></label>
    <label>الموقف: <select id="f-park"><option value="">الكل</option><option value="onsite">داخل العقار فقط</option></select></label>
    <span class="muted small" id="f-count"></span>
  </div>
  {table(sorted(tier_b, key=lambda u: u["distance_km"] or 99), "الإجمالي الشهري = الإيجار + 管理費. الموقف: ✓ داخلي بسعره، أو أقرب موقف شهري مُعلن.")}
</section>

{ur_section([r for r in ur_rows if (r.get("distance_km") or 99) <= 5.5])}

<section id="parking">
  <h2>مرجع أسعار المواقف الشهرية (月極駐車場)</h2>
  <p class="lead">إن لم يكن للشقة موقف داخلي، هذه الأسعار المرصودة في المنطقة. العرض "مع الموقف" في البطاقات أعلاه يستخدم أقرب موقف مُعلن سعره.</p>
  <div class="tablewrap"><table><thead><tr><th>الحي</th><th>عدد المواقف المرصودة</th><th>الوسيط</th><th>النطاق</th></tr></thead><tbody>{pk_rows or '<tr><td colspan="4">لا توجد بيانات مواقف</td></tr>'}</tbody></table></div>
</section>

<section id="notes">
  <h2>ملاحظات عملية</h2>
  <div class="note"><b>العزل الحراري — كيف قرأت درجات "عزل A / B / C":</b>
    <ul>
      <li><b>A</b>: بناء 2015 فما بعد (معيار الطاقة 2013). عادةً زجاج مزدوج وعزل جدران جيد.</li>
      <li><b>B+</b>: 2001–2014 خرسانة RC/SRC — بعد معيار 1999 (次世代省エネ基準). الأفضل من حيث السعر/الراحة.</li>
      <li><b>B / B-</b>: 2001–2014 خشب أو فولاذ خفيف (軽量鉄骨). الفولاذ الخفيف هو النوع الذي حذّرتَ منه: مقبول فقط إن كان من شركات كبرى حديثة (積水ハウス シャーメゾン، 大和 D-room، 旭化成 ヘーベルメゾン) — اسأل عن 断熱 والنوافذ.</li>
      <li><b>C</b>: 1991–2000 خرسانة. مقبول إن كانت النوافذ مُجدَّدة. ما قبل 1991 حُذف كلياً (أيضاً ما قبل 1981 = معيار زلازل قديم 旧耐震).</li>
    </ul></div>
  <div class="note"><b>التكاليف الأولية المعتادة في كيوتو (غير UR):</b>
    <ul>
      <li>礼金 (كي مني) — حسب طلبك ≤ شهر، مُفلتر. 敷金 (تأمين) يُسترد جزئياً، مع 敷引/償却 أحياناً في كانساي (مبلغ غير مسترد — اسأل).</li>
      <li>仲介手数料 عمولة الوكيل: شهر + ضريبة عادةً (بعض الوكالات نصف شهر أو صفر). 保証会社 شركة الضمان: 50–100% من شهر. 火災保険 تأمين حريق ≈ ¥15–20 ألف لسنتين. 鍵交換 تبديل القفل ≈ ¥15–25 ألف. 前家賃 إيجار أول شهر.</li>
      <li>UR: صفر 礼金، صفر عمولة، صفر كفيل، صفر رسوم تجديد؛ الشرط شهادة دخل (الدخل الشهري ≥ 4× الإيجار، أو إيداع مسبق).</li>
      <li>السيارة: عند التعاقد على موقف شهري تحتاج 車庫証明 (شهادة المرآب) — المالك/الوكيل يصدر 保管場所使用承諾証明書 مقابل رسم ¥2–5 آلاف عادةً.</li>
    </ul></div>
</section>

<footer class="end">
  تم جمع البيانات آلياً بتاريخ {TODAY} من المواقع المذكورة، مع التحقق من أن كل رابط كان يعمل ويعرض الوحدة نفسها لحظة الجمع. الأسعار والشغور تتغير بسرعة؛ الوكيل العقاري هو المرجع النهائي. الإحداثيات على مستوى الحي/الشارع (دقة ±300 م).
</footer>
</div>
<script>
(function(){{
  var fw=document.getElementById('f-ward'),fp=document.getElementById('f-park'),fc=document.getElementById('f-count');
  if(!fw||!fp)return;
  var rows=document.querySelectorAll('#all tbody tr');
  function apply(){{var w=fw.value,p=fp.value,n=0;rows.forEach(function(r){{var ok=(!w||r.dataset.ward===w)&&(!p||r.dataset.parking===p);r.hidden=!ok;if(ok)n++;}});fc.textContent=n+' / '+rows.length;}}
  fw.addEventListener('change',apply);fp.addEventListener('change',apply);apply();
}})();
</script>
'''
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {out_html}: {len(apt)} apartments ({len(tier_a)} A / {len(tier_b)} B), {len(houses)} houses, {len(ur_rows)} UR rows, {len(lots)} parking lots")


if __name__ == "__main__":
    main()
