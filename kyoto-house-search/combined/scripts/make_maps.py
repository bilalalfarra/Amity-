#!/usr/bin/env python3
"""Two static OSM maps for the combined report: around the office, and around UR 松ノ木町."""
import json, os
from PIL import ImageDraw, ImageFont
from staticmap import StaticMap, CircleMarker
import staticmap.staticmap as sm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
BIG = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
COL = {"le1": "#2f6b4f", "le2": "#b86e00", "house": "#6a4c93", "near": "#7a8590", "matsu": "#1f5f99"}


def make_map(units, landmarks, path, size=(1200, 860)):
    """landmarks: list of (lat, lon, colour, label)"""
    m = StaticMap(*size, url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                  headers={"User-Agent": "amity-house-search/1.0 (personal flat search)"})
    for lat, lon, col, _ in landmarks:
        m.add_marker(CircleMarker((lon, lat), "white", 30))
        m.add_marker(CircleMarker((lon, lat), col, 24))
    pts = []
    for u in units:
        if u.get("lat") is None:
            continue
        m.add_marker(CircleMarker((u["lon"], u["lat"]), "white", 24))
        m.add_marker(CircleMarker((u["lon"], u["lat"]), COL[u["_col"]], 20))
        pts.append((u["lon"], u["lat"], str(u["rank"])))
    img = m.render()
    d = ImageDraw.Draw(img)

    def px(lon, lat):
        return (m._x_to_px(sm._lon_to_x(lon, m.zoom)), m._y_to_px(sm._lat_to_y(lat, m.zoom)))

    seen = {}
    for lon, lat, label in pts:
        x, y = px(lon, lat)
        k = (round(x / 7), round(y / 7))
        off = seen.get(k, 0); seen[k] = off + 1
        d.text((x, y + off * 12), label, fill="white", font=FONT, anchor="mm")
    for lat, lon, col, label in landmarks:
        x, y = px(lon, lat)
        d.text((x, y), label, fill="white", font=BIG, anchor="mm")
    d.rectangle([0, img.height - 18, img.width, img.height], fill=(255, 255, 255))
    d.text((6, img.height - 9), "© OpenStreetMap contributors", fill=(60, 60, 60), font=FONT, anchor="lm")
    img.save(path, optimize=True)
    return path
