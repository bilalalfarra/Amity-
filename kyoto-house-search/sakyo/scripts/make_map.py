#!/usr/bin/env python3
"""Static OSM map: office + every kept home, numbered with its rank. -> out/map.png"""
import json, os
from PIL import ImageDraw, ImageFont
from staticmap import StaticMap, CircleMarker
import staticmap.staticmap as sm
from geo import CENTER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
units = json.load(open(os.path.join(OUT, "final.json"), encoding="utf-8"))

COL = {"le1": "#2f6b4f", "le2": "#b86e00", "house": "#6a4c93", "near": "#7a8590"}
m = StaticMap(1200, 900, url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
              headers={"User-Agent": "amity-house-search/1.0 (personal flat search)"})
m.add_marker(CircleMarker((CENTER[1], CENTER[0]), "white", 30))
m.add_marker(CircleMarker((CENTER[1], CENTER[0]), "#c0392b", 24))
pts = []
for u in units:
    if u.get("lat") is None:
        continue
    key = "near" if u["near"] else ("house" if u["is_house"] else u["reikin_group"])
    m.add_marker(CircleMarker((u["lon"], u["lat"]), "white", 22))
    m.add_marker(CircleMarker((u["lon"], u["lat"]), COL[key], 18))
    pts.append((u["lon"], u["lat"], str(u["rank"])))
img = m.render()
d = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)


def px(lon, lat):
    return (m._x_to_px(sm._lon_to_x(lon, m.zoom)), m._y_to_px(sm._lat_to_y(lat, m.zoom)))


seen = {}
for lon, lat, label in pts:
    x, y = px(lon, lat)
    k = (round(x / 6), round(y / 6))          # nudge labels of stacked markers
    off = seen.get(k, 0); seen[k] = off + 1
    d.text((x, y + off * 11), label, fill="white", font=font, anchor="mm")
x, y = px(CENTER[1], CENTER[0])
d.text((x, y), "★", fill="white", font=big, anchor="mm")
d.rectangle([0, img.height - 18, img.width, img.height], fill=(255, 255, 255))
d.text((6, img.height - 9), "© OpenStreetMap contributors", fill=(60, 60, 60), font=font, anchor="lm")
img.save(os.path.join(OUT, "map.png"), optimize=True)
print("map.png", img.size, "zoom", m.zoom, "points", len(pts))
