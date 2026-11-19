"""Draws entry.png: a one-image summary of the world's news of Wednesday 18 November 2026.

Run offline on the author's machine (needs Pillow); the result is committed as entry.png and main.py copies it.
Every story below is an event reported on 18 November 2026 (see NEWS.md for sources).
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor
W = H = 1024
FONT_DIR = "C:/Windows/Fonts/"
BOLD = FONT_DIR + "arialbd.ttf"
HEAVY = FONT_DIR + "impact.ttf"

BG = (14, 22, 40)
PANEL = (27, 40, 66)
INK = (244, 246, 250)
MUTED = (160, 176, 205)
ACCENT = (255, 196, 61)


def font(path, size):
    return ImageFont.truetype(path, size * S)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w * S:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def box(d, x, y, w, h, fill, r=18, outline=None, width=0):
    d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], r * S, fill=fill, outline=outline, width=width * S)


def rect(d, x0, y0, x1, y1, fill):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill)


def ell(d, cx, cy, rx, ry, fill, outline=None, width=0):
    d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=fill, outline=outline, width=width * S)


def poly(d, pts, fill):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)


def line(d, pts, fill, width):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(width * S), joint="curve")


# ---- icons, each drawn in a 150 x 150 square whose top-left corner is (ox, oy) ----
def icon_bridge(d, ox, oy):
    rect(d, ox, oy + 95, ox + 150, oy + 150, (30, 90, 150))
    for i in range(4):
        line(d, [(ox + 5 + i * 40, oy + 118), (ox + 20 + i * 40, oy + 112), (ox + 35 + i * 40, oy + 118)], (90, 150, 210), 3)
    for px in (ox + 22, ox + 128):
        rect(d, px - 5, oy + 55, px + 5, oy + 100, (150, 156, 170))
    rect(d, ox, oy + 50, ox + 52, oy + 60, (200, 204, 214))
    rect(d, ox + 98, oy + 50, ox + 150, oy + 60, (200, 204, 214))
    poly(d, [(ox + 52, oy + 50), (ox + 64, oy + 70), (ox + 70, oy + 62)], (200, 204, 214))
    poly(d, [(ox + 98, oy + 50), (ox + 86, oy + 78), (ox + 80, oy + 62)], (200, 204, 214))
    star = []
    for k in range(16):
        ang = k * math.pi / 8
        rad = 24 if k % 2 == 0 else 11
        star.append((ox + 75 + rad * math.cos(ang), oy + 42 + rad * math.sin(ang)))
    poly(d, star, (255, 120, 40))
    ell(d, ox + 75, oy + 42, 8, 8, (255, 226, 120))


def icon_summit(d, ox, oy):
    cols = [((60, 100, 200), "US"), ((215, 40, 45), "CN"), ((236, 238, 244), "RU")]
    f = font(BOLD, 26)
    for i, (c, t) in enumerate(cols):
        cx = ox + 25 + i * 50
        cy = oy + 50 + (18 if i == 1 else 0)
        ell(d, cx, cy, 24, 24, c)
        fill = (20, 30, 50) if t == "RU" else (255, 255, 255)
        d.text((cx * S, cy * S), t, font=f, fill=fill, anchor="mm")
    line(d, [(ox + 25, oy + 78), (ox + 75, oy + 96), (ox + 125, oy + 78)], ACCENT, 4)
    d.text(((ox + 75) * S, (oy + 124) * S), "APEC", font=font(HEAVY, 30), fill=ACCENT, anchor="mm")
    d.text(((ox + 75) * S, (oy + 148) * S), "SHENZHEN", font=font(BOLD, 14), fill=MUTED, anchor="mm")


def icon_gaza(d, ox, oy):
    poly(d, [(ox + 62, oy + 8), (ox + 92, oy + 18), (ox + 60, oy + 138), (ox + 40, oy + 130)], (214, 196, 150))
    rect(d, ox, oy + 8, ox + 56, oy + 138, (40, 100, 160))
    for i in range(0, 130, 14):
        line(d, [(ox + 112, oy + 12 + i), (ox + 112, oy + 20 + i)], (230, 230, 240), 3)
    line(d, [(ox + 128, oy + 75), (ox + 82, oy + 75)], (235, 60, 60), 9)
    poly(d, [(ox + 62, oy + 75), (ox + 88, oy + 58), (ox + 88, oy + 92)], (235, 60, 60))


def icon_bangladesh(d, ox, oy):
    rect(d, ox + 6, oy + 20, ox + 144, oy + 96, (0, 106, 78))
    ell(d, ox + 70, oy + 58, 24, 24, (244, 42, 65))
    rect(d, ox + 6, oy + 20, ox + 12, oy + 140, (190, 190, 200))
    rect(d, ox + 14, oy + 108, ox + 130, oy + 142, (95, 104, 125))
    for i in range(4):
        poly(d, [(ox + 14 + i * 29, oy + 108), (ox + 14 + i * 29, oy + 94), (ox + 43 + i * 29, oy + 108)], (95, 104, 125))
    rect(d, ox + 112, oy + 94, ox + 122, oy + 112, (95, 104, 125))
    for i in range(5):
        rect(d, ox + 24 + i * 22, oy + 118, ox + 34 + i * 22, oy + 128, (255, 214, 120))


def icon_art(d, ox, oy):
    box(d, ox + 8, oy + 8, 134, 134, (200, 150, 40), r=6)
    rect(d, ox + 20, oy + 20, ox + 130, oy + 130, (84, 160, 220))
    rect(d, ox + 20, oy + 108, ox + 130, oy + 130, (92, 150, 70))
    rect(d, ox + 70, oy + 70, ox + 80, oy + 112, (92, 62, 40))
    for cx, cy, r in [(75, 58, 26), (52, 70, 18), (98, 70, 18), (75, 40, 16)]:
        ell(d, ox + cx, oy + cy, r, r, (240, 244, 240))
    for cx, cy in [(60, 50), (88, 54), (74, 34), (48, 72), (102, 74), (70, 66)]:
        ell(d, ox + cx, oy + cy, 5, 5, (240, 150, 175))


def icon_voyager(d, ox, oy):
    ell(d, ox + 24, oy + 100, 20, 20, (60, 140, 230))
    poly(d, [(ox + 12, oy + 96), (ox + 26, oy + 88), (ox + 30, oy + 104), (ox + 18, oy + 110)], (70, 170, 90))
    for i in range(0, 70, 12):
        line(d, [(ox + 48 + i, oy + 70 - i * 0.55), (ox + 54 + i, oy + 67 - i * 0.55)], MUTED, 3)
    ell(d, ox + 108, oy + 34, 24, 8, None, outline=(235, 238, 245), width=4)
    d.arc([(ox + 84) * S, (oy + 14) * S, (ox + 132) * S, (oy + 54) * S], 200, 340, fill=(235, 238, 245), width=5 * S)
    rect(d, ox + 102, oy + 38, ox + 114, oy + 54, (200, 205, 215))
    line(d, [(ox + 108, oy + 54), (ox + 128, oy + 72)], (200, 205, 215), 4)
    for sx, sy in [(10, 20), (46, 12), (120, 118), (86, 132), (140, 90), (22, 52)]:
        ell(d, ox + sx, oy + sy, 2.5, 2.5, (255, 255, 255))


def icon_capitol(d, ox, oy):
    rect(d, ox + 8, oy + 122, ox + 142, oy + 140, (214, 218, 228))
    rect(d, ox + 20, oy + 70, ox + 130, oy + 122, (236, 238, 246))
    for i in range(6):
        rect(d, ox + 26 + i * 18, oy + 74, ox + 34 + i * 18, oy + 118, (176, 182, 200))
    poly(d, [(ox + 14, oy + 70), (ox + 75, oy + 44), (ox + 136, oy + 70)], (214, 218, 228))
    d.pieslice([(ox + 42) * S, (oy + 8) * S, (ox + 108) * S, (oy + 74) * S], 180, 360, fill=(244, 246, 252))
    rect(d, ox + 72, oy + 0, ox + 78, oy + 14, (200, 204, 214))
    poly(d, [(ox + 78, oy + 0), (ox + 98, oy + 5), (ox + 78, oy + 10)], (80, 130, 255))


def icon_ipo(d, ox, oy):
    box(d, ox + 6, oy + 14, 138, 112, (16, 26, 46), r=10)
    for i in range(1, 4):
        line(d, [(ox + 14, oy + 14 + i * 28), (ox + 136, oy + 14 + i * 28)], (40, 56, 90), 2)
    pts = [(ox + 16, oy + 108), (ox + 44, oy + 92), (ox + 64, oy + 98), (ox + 92, oy + 62), (ox + 112, oy + 52), (ox + 134, oy + 24)]
    line(d, pts, (90, 230, 140), 6)
    poly(d, [(ox + 140, oy + 16), (ox + 120, oy + 20), (ox + 134, oy + 36)], (90, 230, 140))
    d.text(((ox + 75) * S, (oy + 138) * S), "IPO", font=font(HEAVY, 26), fill=ACCENT, anchor="mm")


HERO = ("CHINA · APEC", (255, 110, 110), "Trump lands in Shenzhen for APEC and Xi greets him on the tarmac; Putin arrives too. First-ever three-way summit is set for 19 Nov", icon_summit)

STORIES = [
    ("UKRAINE", (80, 160, 255), "Crimea bridge hit for the 3rd time in 4 days; Russia shuts it to all traffic", icon_bridge),
    ("GAZA", (110, 210, 150), "Israel opens its first operation in central Gaza since the Oct 2025 ceasefire", icon_gaza),
    ("US", (130, 160, 255), "House Democrats nominate Hakeem Jeffries for Speaker after midterm wins", icon_capitol),
    ("MARKETS", (110, 230, 160), "Anthropic prices the biggest IPO ever, a reported $107B; trading starts 19 Nov", icon_ipo),
    ("BANGLADESH", (240, 200, 90), "Garment workers block a highway over pay; 55 factories shut, ~300 arrests", icon_bangladesh),
    ("SPACE", (190, 170, 255), "Voyager 1 reaches one light-day from Earth, a first for a human-made object", icon_voyager),
]


def main():
    img = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(img)
    for i in range(0, W, 32):  # faint grid
        line(d, [(i, 0), (i, H)], (18, 28, 50), 1)
        line(d, [(0, i), (W, i)], (18, 28, 50), 1)

    d.text((W // 2 * S, 52 * S), "WORLD NEWS IN ONE IMAGE", font=font(HEAVY, 62), fill=INK, anchor="mm")
    box(d, 222, 94, 580, 52, ACCENT, r=26)
    d.text((W // 2 * S, 121 * S), "WEDNESDAY 18 NOVEMBER 2026", font=font(BOLD, 34), fill=(20, 24, 40), anchor="mm")

    tag_f, head_f, hero_f = font(HEAVY, 28), font(BOLD, 25), font(BOLD, 33)
    x0, y0, full_w = 28, 160, 968
    # hero: the day's biggest story, across the full width
    tag, color, text, icon = HERO
    box(d, x0, y0, full_w, 196, PANEL, r=20, outline=color, width=3)
    d.text(((x0 + 26) * S, (y0 + 30) * S), tag, font=font(HEAVY, 30), fill=color, anchor="lm")
    icon(d, x0 + 24, y0 + 34)
    ty = y0 + 56
    for ln in wrap(d, text, hero_f, full_w - 220):
        d.text(((x0 + 196) * S, ty * S), ln, font=hero_f, fill=INK)
        ty += 42

    pw, ph, gx, gy = 484, 200, 20, 10
    y1 = y0 + 196 + 10
    for idx, (tag, color, text, icon) in enumerate(STORIES):
        col, row = idx % 2, idx // 2
        x, y = x0 + col * (pw + gx), y1 + row * (ph + gy)
        box(d, x, y, pw, ph, PANEL, r=20)
        rect(d, x + 18, y + 14, x + 24, y + 44, color)
        d.text(((x + 34) * S, (y + 30) * S), tag, font=tag_f, fill=color, anchor="lm")
        icon(d, x + 14, y + 44)
        ty = y + 56
        for ln in wrap(d, text, head_f, pw - 196):
            d.text(((x + 172) * S, ty * S), ln, font=head_f, fill=INK)
            ty += 31

    foot = "Reported 18 Nov 2026 · AP · BBC · CNN · PBS · Democracy Now · The Daily Star"
    d.text((W // 2 * S, 1004 * S), foot, font=font(BOLD, 17), fill=MUTED, anchor="mm")

    img = img.resize((W, H), Image.LANCZOS)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
