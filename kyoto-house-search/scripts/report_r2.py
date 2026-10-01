#!/usr/bin/env python3
"""Build the separate '礼金 up to 2 months' report from out_r2/merged.json by running report.py
and swapping the wording that differs from the main report."""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
out_html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out_r2", "report_reikin2.html")
env = dict(os.environ, OUT_DIR=os.path.join(HERE, "out_r2"))
subprocess.run([sys.executable, os.path.join(HERE, "report.py"), out_html], check=True, env=env)

h = open(out_html, encoding="utf-8").read()
MAIN = "https://claude.ai/artifact/TcyLUeGgkPgdFPxbtnS7yQ"
subs = [
    ("<title>بيوت كيوتو قرب KRP</title>", "<title>بيوت كيوتو — 礼金 شهرين</title>"),
    ("تقرير بحث سكن · كيوتو ·", "ملحق: 礼金 أكثر من شهر حتى شهرين · كيوتو ·"),
    ("<h1>بيوت للإيجار قرب 京都技術科学センター (KRP)</h1>",
     "<h1>بيوت إضافية قرب KRP — 礼金 حتى شهرين</h1>"
     f'<p class="lead"><b>هذا ملحق منفصل.</b> كل الشقق هنا 礼金 فيها أكثر من شهر وحتى شهرين، وغير موجودة في '
     f'<a href="{MAIN}" target="_blank" rel="noopener">التقرير الأساسي</a>. باقي الشروط نفسها تماماً. '
     'كلفة الدخول أعلى بشهر إيجار تقريباً (礼金 لا يُسترد)، لكن كثيراً ما يقبل المالك تخفيضه إلى شهر إن طلب الوكيل — اسأل.</p>'),
    ("<span>礼金 ≤ شهر</span>", "<span>1 شهر &lt; 礼金 ≤ شهرين</span>"),
    ("الأولوية الأولى حسب طلبك (العزل)", "الأفضل من ناحية العزل"),
    ("العدد قليل لأن ثلاثة فلاتر تضيق السوق في كيوتو معاً: 礼金 ≤ شهر (العرف المحلي شهران)، ≥45 م² بسعر ≤100 ألف، والقرب من KRP. ", ""),
    ("礼金 (كي مني) — حسب طلبك ≤ شهر، مُفلتر.", "礼金 (كي مني) — في هذا الملحق بين شهر وشهرين، وهو مبلغ لا يُسترد؛ فاوض عليه."),
    ("شقة مطابقة (بعد حذف التكرار)", "شقة إضافية (غير موجودة في التقرير الأساسي)"),
]
for a, b in subs:
    if a in h:
        h = h.replace(a, b)
    else:
        print("!! not found:", a[:60])
# no UR section in this addendum (UR has no 礼金)
h = re.sub(r'<section id="ur">.*?</section>', "", h, flags=re.S)
open(out_html, "w", encoding="utf-8").write(h)
print("wrote", out_html)
