"""Draws entry.png: a one-image summary of the world's news of Wednesday 18 November 2026.

A world map with a numbered pin where each story happened, and a numbered card per story below it.
Run offline on the author's machine (needs Pillow) with the path of Natural Earth's public-domain
ne_110m_land.geojson as its argument; the result is committed as entry.png and main.py copies it.
Every story is an event reported on 18 November 2026 (see NEWS.md for sources).
"""
import json
import sys
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor
W = H = 1024
FONT_DIR = "C:/Windows/Fonts/"
BOLD = FONT_DIR + "arialbd.ttf"
HEAVY = FONT_DIR + "impact.ttf"

BG = (12, 19, 34)
OCEAN = (17, 32, 58)
LAND = (52, 74, 108)
COAST = (86, 112, 150)
PANEL = (26, 38, 62)
INK = (244, 246, 250)
MUTED = (150, 166, 196)
ACCENT = (255, 196, 61)

# map window: equirectangular, longitude -180..180 across the full width, latitude 78N..56S
MAP_Y0, LAT_N, LAT_S = 124, 78.0, -56.0
MAP_H = round(W * (LAT_N - LAT_S) / 360)

# (location, headline, lon, lat, badge offset dx, dy, colour)
STORIES = [
    ("Shenzhen:", "Trump lands for APEC and Xi greets him; Putin arrives too. 3-way summit set for 19 Nov", 114.06, 22.54, 40, 26, (255, 99, 99)),
    ("Crimea:", "Ukraine hits the Kerch bridge for a 3rd time in 4 days; Russia shuts it to traffic", 36.5, 45.3, 6, -42, (88, 166, 255)),
    ("Gaza:", "Israel's first operation in central Gaza since the Oct 2025 ceasefire", 34.4, 31.4, -44, 30, (96, 214, 150)),
    ("Washington:", "House Democrats nominate Hakeem Jeffries for Speaker after midterm wins", -77.0, 38.9, -50, 22, (140, 160, 255)),
    ("New York:", "Anthropic prices the biggest IPO ever, a reported $107B; trading opens 19 Nov", -74.0, 40.7, 34, -34, (110, 230, 160)),
    ("Bangladesh:", "Garment workers' pay protests close 55 factories; about 300 arrests", 90.4, 23.8, -18, 46, (255, 196, 61)),
    ("Haiti:", "Salvadoran troops destroy a gang leader's house in Canaan", -72.2, 18.6, 34, 34, (255, 150, 90)),
    ("Deep space:", "Voyager 1 reaches one light-day from Earth, the first craft to do so", None, None, 0, 0, (200, 170, 255)),
]


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def proj(lon, lat):
    return (lon + 180) / 360 * W, MAP_Y0 + (LAT_N - lat) / (LAT_N - LAT_S) * MAP_H


def sc(pts):
    return [(x * S, y * S) for x, y in pts]


def draw_map(d, geojson_path):
    d.rectangle([0, MAP_Y0 * S, W * S, (MAP_Y0 + MAP_H) * S], fill=OCEAN)
    for lon in range(-150, 180, 30):
        x, _ = proj(lon, 0)
        d.line([(x * S, MAP_Y0 * S), (x * S, (MAP_Y0 + MAP_H) * S)], fill=(24, 42, 72), width=S)
    for lat in (60, 30, 0, -30):
        _, y = proj(0, lat)
        d.line([(0, y * S), (W * S, y * S)], fill=(24, 42, 72), width=S)
    with open(geojson_path, encoding="utf8") as f:
        land = json.load(f)
    for feat in land["features"]:
        g = feat["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = [proj(lon, max(min(lat, LAT_N + 2), LAT_S - 2)) for lon, lat in poly[0]]
            if len(ring) > 2:
                d.polygon(sc(ring), fill=LAND, outline=COAST, width=S)


def badge(d, cx, cy, r, n, colour, size):
    d.ellipse([(cx - r - 2) * S, (cy - r - 2) * S, (cx + r + 2) * S, (cy + r + 2) * S], fill=BG)
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=colour)
    d.text((cx * S, (cy + 1) * S), str(n), font=font(BOLD, size), fill=(14, 20, 34), anchor="mm")


def draw_pins(d):
    for n, (_, _, lon, lat, dx, dy, colour) in enumerate(STORIES, 1):
        if lon is None:  # deep space: over the open Pacific at the right edge, pointing off the map
            bx, by = W - 40, proj(0, 2)[1]
            for k in range(4):
                d.line(sc([(bx + 4 + k * 9, by - 22 - k * 12), (bx + 8 + k * 9, by - 28 - k * 12)]), fill=colour, width=3 * S)
            d.text(((bx - 24) * S, by * S), "Voyager 1", font=font(BOLD, 17), fill=colour, anchor="rm")
            badge(d, bx, by, 17, n, colour, 20)
            continue
        x, y = proj(lon, lat)
        bx, by = x + dx, y + dy
        d.line(sc([(x, y), (bx, by)]), fill=colour, width=3 * S)
        d.ellipse([(x - 6) * S, (y - 6) * S, (x + 6) * S, (y + 6) * S], fill=INK, outline=colour, width=3 * S)
        badge(d, bx, by, 17, n, colour, 20)


def wrap_words(d, words, max_w):
    """words: list of (text, font, colour); returns lines of the same tuples."""
    lines, cur, cur_w = [], [], 0
    for word in words:
        w = d.textlength(word[0] + " ", font=word[1])
        if cur and cur_w + d.textlength(word[0], font=word[1]) > max_w * S:
            lines.append(cur)
            cur, cur_w = [], 0
        cur.append(word)
        cur_w += w
    lines.append(cur)
    return lines


def draw_cards(d):
    loc_f, head_f = font(BOLD, 23), font(BOLD, 23)
    x0, y0, cw, ch, gx, gy = 16, MAP_Y0 + MAP_H + 12, 488, 108, 16, 8
    for i, (loc, text, *_, colour) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x, y = x0 + col * (cw + gx), y0 + row * (ch + gy)
        d.rounded_rectangle([x * S, y * S, (x + cw) * S, (y + ch) * S], 16 * S, fill=PANEL)
        d.rectangle([x * S, (y + 10) * S, (x + 5) * S, (y + ch - 10) * S], fill=colour)
        badge(d, x + 36, y + ch / 2, 21, i + 1, colour, 24)
        words = [(loc, loc_f, colour)] + [(w, head_f, INK) for w in text.split()]
        lines = wrap_words(d, words, cw - 82)
        ty = y + ch / 2 - len(lines) * 27 / 2
        for ln in lines:
            tx = x + 68
            for word, fnt, fill in ln:
                d.text((tx * S, ty * S), word, font=fnt, fill=fill)
                tx += d.textlength(word + " ", font=fnt) / S
            ty += 27


def main(geojson_path):
    img = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(img)
    d.text((W // 2 * S, 40 * S), "WEDNESDAY 18 NOVEMBER 2026", font=font(HEAVY, 54), fill=ACCENT, anchor="mm")
    d.text((W // 2 * S, 94 * S), "THE WORLD'S NEWS IN ONE IMAGE", font=font(BOLD, 26), fill=INK, anchor="mm")
    draw_map(d, geojson_path)
    draw_pins(d)
    draw_cards(d)
    foot = "Reported 18 Nov 2026 · AP · BBC · CNN · PBS · CNBC · Democracy Now · The Daily Star · Map: Natural Earth"
    d.text((W // 2 * S, 1011 * S), foot, font=font(BOLD, 14), fill=MUTED, anchor="mm")
    img = img.resize((W, H), Image.LANCZOS)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main(sys.argv[1])
