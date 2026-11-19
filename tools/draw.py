"""Draws entry.png: a one-image front page of the world's news of Wednesday 18 November 2026.

Four illustrated lead stories, then the rest of the day by region. Run offline on the author's machine
(needs Pillow); the result is committed as entry.png and main.py copies it. Every story is an event that
happened or was first reported on 18 November 2026 (see NEWS.md for sources).
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor
W = H = 1024
FONT_DIR = "C:/Windows/Fonts/"
BOLD = FONT_DIR + "arialbd.ttf"
REG = FONT_DIR + "arial.ttf"
HEAVY = FONT_DIR + "impact.ttf"

BG = (12, 19, 34)
PANEL = (26, 38, 62)
INK = (244, 246, 250)
SOFT = (206, 214, 230)
MUTED = (150, 166, 196)
ACCENT = (255, 196, 61)


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


# ---- icon primitives: each icon draws in a 150 x 150 box on its own layer ----
def rect(d, x0, y0, x1, y1, fill):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill)


def ell(d, cx, cy, r, fill, outline=None, width=0):
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill, outline=outline, width=width * S)


def poly(d, pts, fill):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)


def line(d, pts, fill, width):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(width * S), joint="curve")


def star(d, cx, cy, r1, r2, fill, n=8):
    poly(d, [(cx + (r1 if k % 2 == 0 else r2) * math.cos(k * math.pi / n), cy + (r1 if k % 2 == 0 else r2) * math.sin(k * math.pi / n)) for k in range(2 * n)], fill)


def icon_summit(d):
    for i, (c, t) in enumerate([((60, 100, 200), "US"), ((215, 40, 45), "CN"), ((236, 238, 244), "RU")]):
        cx, cy = 28 + i * 47, 62 + (20 if i == 1 else 0)
        ell(d, cx, cy, 25, c)
        d.text((cx * S, cy * S), t, font=font(BOLD, 24), fill=(20, 30, 50) if t == "RU" else (255, 255, 255), anchor="mm")
    line(d, [(28, 94), (75, 112), (122, 94)], ACCENT, 5)
    d.text((75 * S, 136 * S), "APEC", font=font(HEAVY, 30), fill=ACCENT, anchor="mm")


def icon_gulf(d):
    rect(d, 0, 104, 150, 150, (30, 90, 150))
    poly(d, [(0, 104), (60, 92), (150, 100), (150, 104)], (200, 176, 120))
    ell(d, 96, 110, 16, (255, 120, 40))
    star(d, 96, 104, 26, 12, (255, 150, 50))
    ell(d, 96, 104, 8, (255, 230, 140))
    for cx, cy in [(30, 22), (62, 22), (30, 54), (62, 54)]:
        ell(d, cx, cy, 13, None, outline=(220, 224, 236), width=3)
    line(d, [(30, 22), (62, 54)], (220, 224, 236), 6)
    line(d, [(62, 22), (30, 54)], (220, 224, 236), 6)
    ell(d, 46, 38, 8, (180, 186, 200))
    line(d, [(56, 50), (84, 82)], (255, 196, 61), 3)


def icon_gaza(d):
    poly(d, [(62, 8), (92, 18), (60, 138), (40, 130)], (214, 196, 150))
    rect(d, 0, 8, 56, 138, (40, 100, 160))
    for i in range(0, 130, 14):
        line(d, [(112, 12 + i), (112, 20 + i)], (230, 230, 240), 3)
    line(d, [(140, 75), (84, 75)], (235, 60, 60), 10)
    poly(d, [(62, 75), (90, 56), (90, 94)], (235, 60, 60))


def icon_bridge(d):
    rect(d, 0, 95, 150, 150, (30, 90, 150))
    for i in range(4):
        line(d, [(5 + i * 40, 118), (20 + i * 40, 112), (35 + i * 40, 118)], (90, 150, 210), 3)
    for px in (22, 128):
        rect(d, px - 6, 55, px + 6, 100, (150, 156, 170))
    rect(d, 0, 50, 52, 61, (200, 204, 214))
    rect(d, 98, 50, 150, 61, (200, 204, 214))
    poly(d, [(52, 50), (64, 72), (70, 62)], (200, 204, 214))
    poly(d, [(98, 50), (86, 80), (80, 62)], (200, 204, 214))
    star(d, 75, 40, 26, 11, (255, 120, 40))
    ell(d, 75, 40, 8, (255, 226, 120))


def paste_icon(img, fn, x, y, size):
    layer = Image.new("RGBA", (150 * S, 150 * S), (0, 0, 0, 0))
    fn(ImageDraw.Draw(layer))
    layer = layer.resize((size * S, size * S), Image.LANCZOS)
    img.paste(layer, (int(x * S), int(y * S)), layer)


LEADS = [
    ("CHINA", (255, 104, 104), icon_summit, "Trump lands in Shenzhen for APEC; Xi greets him. Summit with Putin set for 19 Nov"),
    ("GULF", (255, 150, 70), icon_gulf, "Iran strikes Kuwait and Bahrain after a US strike on its Qeshm Island; Gulf states condemn"),
    ("GAZA", (96, 214, 150), icon_gaza, "Israel's first ground push in central Gaza since the ceasefire: 3 killed, families flee camps"),
    ("UKRAINE", (88, 166, 255), icon_bridge, "Ukraine hits the Crimea bridge for a 3rd time in 4 days; Russia shuts it to all traffic"),
]

SECTIONS = [
    ("EUROPE", (88, 166, 255), [
        ("Ukraine:", "Russian strikes kill at least 5, four of them in Odesa"),
        ("EU:", "Commission proposes a €45bn loan to keep Ukraine funded and armed"),
        ("Migration:", "five EU states look to Rwanda to take rejected asylum seekers"),
    ]),
    ("MIDDLE EAST", (96, 214, 150), [
        ("Yemen:", "Saudi-led coalition hits 60 Houthi sites as Houthis push towards Aden"),
        ("Israel:", "Eisenkot ally Matan Kahana elected Knesset speaker, a blow to Netanyahu"),
        ("West Bank:", "Israel delays E1 settlement contracts after UK sanctions"),
        ("Iraq:", "six French nationals jailed for life for joining ISIL"),
        ("Lebanon:", "US sanctions a charity it calls a Hezbollah front"),
    ]),
    ("ASIA", (255, 104, 104), [
        ("Shenzhen:", "Xi meets Putin, says they should lead a 'multipolar world'"),
        ("Diplomacy:", "Trump and Putin to hold one-on-one talks in China on Thursday"),
        ("Bangladesh:", "garment wage protests shut 55 factories; about 300 arrests"),
        ("Kashmir:", "Indian troops kill a militant commander in Kulgam"),
        ("Thailand:", "clean-water scramble as arsenic from Myanmar mines taints rivers"),
        ("South Korea:", "AI cheating scandal shakes university entrance exams"),
    ]),
    ("AFRICA", (255, 196, 61), [
        ("Senegal:", "migrant boat capsizes off Yenne, at least one dead"),
        ("DR Congo:", "fighting goes on in the Kivus despite rival peace efforts"),
    ]),
    ("OCEANIA", (120, 220, 230), [
        ("Australia:", "sanctions 3 Israelis and 4 groups over West Bank settlements"),
    ]),
    ("AMERICAS", (140, 160, 255), [
        ("US:", "Hakeem Jeffries formally nominated as the first Black House Speaker"),
        ("Alaska:", "Democrat Mary Peltola flips the last Senate seat to be called"),
        ("Venezuela:", "Hegseth visits Caracas, announces a military partnership"),
        ("US:", "Homeland Security chief grilled over the nationwide flight ground stop"),
        ("Bird flu:", "top US egg producer Cal-Maine culls 1.8 million hens"),
        ("Haiti:", "Salvadoran troops destroy a gang leader's house in Canaan"),
    ]),
    ("BUSINESS · SCIENCE · CULTURE · SPORT", (200, 170, 255), [
        ("Markets:", "Anthropic prices the biggest IPO ever, a reported $107B; trading opens 19 Nov"),
        ("Space:", "Voyager 1 reaches one light-day (~26bn km) from Earth, 49 years after launch"),
        ("Art:", "Van Gogh's Blossoming Chestnut Trees sells for a record $190.4M"),
        ("Football:", "FIFA nominations close; Infantino faces three challengers"),
        ("Cricket:", "Bangladesh's Litton Das sets a Test record of 8 dismissals in an innings"),
        ("Gaming:", "PlayStation network outage on the eve of the GTA VI launch"),
    ]),
]


def wrap_words(d, words, max_w):
    """words: list of (text, font, colour); returns lines of the same tuples."""
    lines, cur, cur_w = [], [], 0
    for word in words:
        if cur and cur_w + d.textlength(word[0], font=word[1]) > max_w * S:
            lines.append(cur)
            cur, cur_w = [], 0
        cur.append(word)
        cur_w += d.textlength(word[0] + " ", font=word[1])
    lines.append(cur)
    return lines


def draw_words(d, lines, x, y, lh):
    for ln in lines:
        tx = x
        for word, fnt, fill in ln:
            d.text((tx * S, y * S), word, font=fnt, fill=fill)
            tx += d.textlength(word + " ", font=fnt) / S
        y += lh
    return y


def count_stories():
    return len(LEADS) + sum(len(items) for _, _, items in SECTIONS)


def main():
    img = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((W // 2 * S, 38 * S), "WEDNESDAY 18 NOVEMBER 2026", font=font(HEAVY, 52), fill=ACCENT, anchor="mm")
    sub = f"THE WORLD'S NEWS IN ONE IMAGE  ·  {count_stories()} STORIES  ·  6 CONTINENTS"
    d.text((W // 2 * S, 86 * S), sub, font=font(BOLD, 21), fill=INK, anchor="mm")
    d.line([(16 * S, 104 * S), ((W - 16) * S, 104 * S)], fill=ACCENT, width=2 * S)

    # four illustrated leads
    lead_f, tag_f = font(BOLD, 18), font(HEAVY, 26)
    cw, ch, y0 = 240, 222, 114
    for i, (tag, colour, icon, text) in enumerate(LEADS):
        x = 16 + i * (cw + 8)
        d.rounded_rectangle([x * S, y0 * S, (x + cw) * S, (y0 + ch) * S], 14 * S, fill=PANEL, outline=colour, width=2 * S)
        paste_icon(img, icon, x + 10, y0 + 10, 92)
        d.text(((x + 112) * S, (y0 + 40) * S), tag, font=tag_f, fill=colour, anchor="lm")
        d.text(((x + 112) * S, (y0 + 72) * S), "LEAD STORY", font=font(BOLD, 13), fill=MUTED, anchor="lm")
        lines = wrap_words(d, [(w, lead_f, INK) for w in text.split()], cw - 22)
        draw_words(d, lines, x + 12, y0 + 110, 22)

    # the rest of the day, by region, in three columns, then a full-width band
    head_f, loc_f, item_f = font(HEAVY, 21), font(BOLD, 16.5), font(REG, 16.5)
    col_w, gap, top, lh = 320, 16, y0 + ch + 16, 19.5
    sections = {name: (colour, items) for name, colour, items in SECTIONS}

    def head(x, y, name, colour):
        d.rectangle([x * S, (y + 4) * S, (x + 5) * S, (y + 23) * S], fill=colour)
        d.text(((x + 12) * S, (y + 14) * S), name, font=head_f, fill=colour, anchor="lm")
        return y + 32

    def item(x, y, loc, text, colour):
        words = [(loc, loc_f, colour)] + [(w, item_f, SOFT) for w in text.split()]
        d.ellipse([(x + 3) * S, (y + 7) * S, (x + 9) * S, (y + 13) * S], fill=colour)
        return draw_words(d, wrap_words(d, words, col_w - 18), x + 15, y, lh) + 7

    bottom = top
    for col, names in enumerate([["EUROPE", "MIDDLE EAST"], ["ASIA", "OCEANIA"], ["AMERICAS", "AFRICA"]]):
        x, y = 16 + col * (col_w + gap), top
        for name in names:
            colour, items = sections[name]
            y = head(x, y, name, colour)
            for loc, text in items:
                y = item(x, y, loc, text, colour)
            y += 8
        print(f"column {col} ends at y={y}")
        bottom = max(bottom, y)

    band = SECTIONS[-1]
    y = head(16, bottom + 2, band[0], band[1])
    d.line([(16 * S, (bottom - 4) * S), ((W - 16) * S, (bottom - 4) * S)], fill=(44, 60, 92), width=S)
    band_items = band[2]
    for r in range(0, len(band_items), 3):  # rows of three; each row starts below the tallest item above it
        row_end = y
        for col, (loc, text) in enumerate(band_items[r:r + 3]):
            row_end = max(row_end, item(16 + col * (col_w + gap), y, loc, text, band[1]))
        y = row_end + 2
    print("band ends at y=", y)

    foot = "Sources: AP · AFP · BBC · CNN · CNBC · PBS · Al Jazeera · The Guardian · Democracy Now · The Daily Star"
    d.text((W // 2 * S, 1010 * S), foot, font=font(BOLD, 13), fill=MUTED, anchor="mm")
    img = img.resize((W, H), Image.LANCZOS)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
