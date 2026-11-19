#!/usr/bin/env python3
"""Generate entry.png v3 - 1024x1024 poster of world news, 18 Nov 2026.
Deterministic: no network, no random, no timestamps, fixed fonts/colours.
Run: python3 generate_image.py  -> writes entry.png next to this file.

v3 is a poster, not a newspaper: one lead story on top, then five
picture-led cards. Headlines are short enough to read at a glance and
every card's picture is drawn big and simple, so the day's stories are
clear from the pictures and the headlines alone. Same six stories and
same facts as v1/v2, only the composition, the pictures and the wording
of the short summaries are new.
"""
from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PAPER = (247, 243, 232)
DARK = (15, 32, 64)
AMBER = (201, 162, 39)
BLACK = (22, 22, 22)
GREY = (88, 88, 88)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
EDGE = (218, 212, 198)

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def typeface(px, bold=True):
    return ImageFont.truetype(BOLD_PATH if bold else REG_PATH, px)


def split_text(text, face, width, limit):
    """Greedy word wrap, at most `limit` lines, each within `width` px."""
    out = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if face.getlength(trial) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
            if len(out) >= limit:
                break
    if current and len(out) < limit:
        out.append(current)
    return out


def rounded(d, box, radius, fill, outline=None):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline,
                        width=1 if outline else 0)


# ---------------------------------------------------------------- pictures
# Every picture is drawn from lines, arcs and rectangles in white on a
# coloured panel. No photos, no copied artwork.

def pic_towers(d, cx, cy, s):
    """Three towers with a flag on the tallest one."""
    ground = cy + s * 0.40
    d.line([(cx - s * 0.78, ground), (cx + s * 0.78, ground)],
           fill=WHITE, width=7)
    for shift, tall in ((-0.60, 0.66), (-0.14, 0.95), (0.34, 0.74)):
        left = cx + shift * s
        right = left + s * 0.26
        top = ground - tall * s
        d.rectangle([left, top, right, ground], fill=WHITE)
        for row in range(3):
            wy = top + s * 0.10 + row * s * 0.17
            if wy < ground - s * 0.05:
                d.rectangle([left + s * 0.05, wy, right - s * 0.05,
                             wy + s * 0.05], fill=DARK)
    tip = cx + 0.26 * s
    d.line([(tip, cy - s * 0.55), (tip, cy - s * 0.95)], fill=WHITE, width=5)
    d.polygon([(tip, cy - s * 0.95), (tip + s * 0.30, cy - s * 0.86),
               (tip, cy - s * 0.77)], fill=AMBER)


def pic_fire(d, cx, cy, s):
    """Flame over waves: a teardrop silhouette with an inner flame."""
    tip = (cx + s * 0.10, cy - s * 0.62)
    outline = [
        (cx - s * 0.34, cy + s * 0.30),
        (cx - s * 0.40, cy - s * 0.02),
        (cx - s * 0.22, cy - s * 0.34),
        tip,
        (cx + s * 0.30, cy - s * 0.28),
        (cx + s * 0.40, cy + s * 0.02),
        (cx + s * 0.34, cy + s * 0.30),
    ]
    d.polygon(outline, fill=WHITE)
    inner = [
        (cx - s * 0.14, cy + s * 0.22),
        (cx - s * 0.17, cy - s * 0.02),
        (cx + s * 0.02, cy - s * 0.26),
        (cx + s * 0.15, cy - s * 0.06),
        (cx + s * 0.17, cy + s * 0.22),
    ]
    d.polygon(inner, fill=AMBER)
    for dy, wide in ((0.44, 0.55), (0.58, 0.68)):
        d.arc([cx - wide * s, cy + dy * s, cx + wide * s, cy + (dy + 0.20) * s],
              start=180, end=360, fill=WHITE, width=6)


def pic_broken_bridge(d, cx, cy, s):
    """A bridge deck snapped in the middle, the right half tilted down."""
    deck = cy - s * 0.16
    gap = s * 0.12
    d.line([(cx - s * 0.78, deck), (cx - gap, deck)], fill=WHITE, width=9)
    d.line([(cx + gap, deck), (cx + s * 0.78, deck + s * 0.26)],
           fill=WHITE, width=9)
    for px in (-0.58, 0.58):
        x = cx + px * s
        top = deck if px < 0 else deck + s * 0.20
        d.line([(x, top), (x, deck + s * 0.42)], fill=WHITE, width=8)
    d.line([(cx - s * 0.10, deck + s * 0.22), (cx + s * 0.16, deck + s * 0.34)],
           fill=AMBER, width=9)
    for dy in (0.62, 0.74):
        d.arc([cx - s * 0.60, cy + dy * s, cx + s * 0.60,
               cy + (dy + 0.16) * s], start=180, end=360, fill=WHITE, width=6)


def pic_dome(d, cx, cy, s):
    """Capitol dome with a flag, and a check mark."""
    d.arc([cx - s * 0.44, cy - s * 0.58, cx + s * 0.44, cy + s * 0.10],
          start=180, end=360, fill=WHITE, width=7)
    d.rectangle([cx - s * 0.44, cy - s * 0.12, cx + s * 0.44, cy + s * 0.02],
                fill=WHITE)
    for shift in (-0.30, -0.10, 0.10, 0.30):
        x = cx + shift * s
        d.rectangle([x - s * 0.05, cy + s * 0.06, x + s * 0.05, cy + s * 0.34],
                    fill=WHITE)
    d.rectangle([cx - s * 0.55, cy + s * 0.34, cx + s * 0.55, cy + s * 0.44],
                fill=WHITE)
    pole = cx + s * 0.02
    d.line([(pole, cy - s * 0.58), (pole, cy - s * 0.92)], fill=WHITE, width=5)
    d.polygon([(pole, cy - s * 0.92), (pole + s * 0.26, cy - s * 0.84),
               (pole, cy - s * 0.76)], fill=AMBER)
    d.line([(cx + s * 0.42, cy + s * 0.42), (cx + s * 0.58, cy + s * 0.60),
            (cx + s * 0.92, cy + s * 0.18)], fill=AMBER, width=8)


def pic_storm(d, cx, cy, s):
    """Cyclone spiral with a calm eye."""
    for k, r in enumerate((0.78, 0.58, 0.38)):
        box = [cx - r * s, cy - r * s, cx + r * s, cy + r * s]
        d.arc(box, start=40 + k * 55, end=330 + k * 55, fill=WHITE, width=7)
    d.ellipse([cx - s * 0.10, cy - s * 0.10, cx + s * 0.10, cy + s * 0.10],
              fill=AMBER)
    d.line([(cx - s * 0.95, cy + s * 0.62), (cx - s * 0.55, cy + s * 0.62)],
           fill=WHITE, width=6)
    d.line([(cx + s * 0.45, cy + s * 0.78), (cx + s * 0.95, cy + s * 0.78)],
           fill=WHITE, width=6)


def pic_stumps(d, cx, cy, s):
    """Three cricket stumps with bails, and the ball beside them."""
    for shift in (-0.34, -0.02, 0.30):
        x = cx + shift * s
        d.rectangle([x - s * 0.07, cy - s * 0.42, x + s * 0.07, cy + s * 0.48],
                    fill=WHITE)
    d.rectangle([cx - s * 0.36, cy - s * 0.54, cx - s * 0.02, cy - s * 0.44],
                fill=WHITE)
    d.rectangle([cx + s * 0.02, cy - s * 0.54, cx + s * 0.36, cy - s * 0.44],
                fill=WHITE)
    d.line([(cx - s * 0.70, cy + s * 0.58), (cx + s * 0.30, cy + s * 0.58)],
           fill=WHITE, width=6)
    ball = (cx + s * 0.62, cy + s * 0.30)
    d.ellipse([ball[0] - s * 0.17, ball[1] - s * 0.17, ball[0] + s * 0.17,
               ball[1] + s * 0.17], fill=(198, 52, 52))


# ---------------------------------------------------------------- stories
# Same six stories and same facts as v1/v2.

ITEMS = [
    dict(num="01", tag="LEAD STORY  •  SHENZHEN SUMMIT",
         head="Xi & Putin meet before Trump",
         body=("Xi Jinping and Vladimir Putin meet in Shenzhen, one day "
               "before their first-ever trilateral summit with Donald "
               "Trump. APEC opens in the same city."),
         colour=DARK, pic=pic_towers, hero=True),
    dict(num="02", tag="GULF ESCALATION",
         head="Iran strikes Kuwait & Bahrain",
         body=("Iran strikes Kuwait and Bahrain after US jets hit a "
               "missile site on Qeshm Island."),
         colour=(140, 47, 47), pic=pic_fire),
    dict(num="03", tag="KERCH BRIDGE HIT",
         head="Ukraine hits Kerch Bridge",
         body=("Ukraine hits the Kerch Bridge again. A road span "
               "collapses, cutting the link to Crimea."),
         colour=(31, 92, 61), pic=pic_broken_bridge),
    dict(num="04", tag="US SENATE FLIPS",
         head="Democrats take the Senate",
         body=("Mary Peltola beats Dan Sullivan in Alaska. Democrats "
               "take a 56–44 majority."),
         colour=(75, 46, 107), pic=pic_dome),
    dict(num="05", tag="CYCLONE AKVAN",
         head="47,000 flee Cyclone Akvan",
         body=("Cyclone Akvan bears down on India's east coast. 47,000 "
               "evacuated in Odisha."),
         colour=(15, 95, 107), pic=pic_storm),
    dict(num="06", tag="DHONI RETIRES",
         head="Captain Cool bows out",
         body=("MS Dhoni retires from the IPL, ending one of cricket's "
               "great careers. Ebola cases in DR Congo pass 11,000."),
         colour=(122, 74, 31), pic=pic_stumps),
]


def draw_story_card(d, item, x, y, w, h, pic_w, hero=False):
    """One picture-led card: coloured picture panel left, words right."""
    rounded(d, [x, y, x + w, y + h], 14, PANEL, EDGE)
    d.rounded_rectangle([x, y, x + pic_w, y + h], radius=14, fill=item["colour"])
    d.rectangle([x + pic_w - 14, y, x + pic_w, y + h], fill=item["colour"])
    item["pic"](d, x + pic_w // 2, y + h // 2, 92 if hero else 78)
    tx = x + pic_w + 20
    tw = w - pic_w - 40
    kick = typeface(21 if hero else 19)
    d.text((tx, y + 16), item["tag"], font=kick, fill=item["colour"])
    head_lines = split_text(item["head"], typeface(38 if hero else 29),
                            tw, 2)
    hy = y + 46 if hero else y + 44
    for line in head_lines:
        d.text((tx, hy), line, font=typeface(38 if hero else 29), fill=BLACK)
        hy += 44 if hero else 34
    body_lines = split_text(item["body"], typeface(20 if hero else 18, False),
                            tw, 3)
    by = hy + 6
    for line in body_lines:
        d.text((tx, by), line, font=typeface(20 if hero else 18, False),
               fill=GREY)
        by += 26 if hero else 23


def build():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    d = ImageDraw.Draw(img)

    # Header.
    d.rectangle([0, 0, CANVAS, 148], fill=DARK)
    d.text((28, 16), "WORLD NEWS  •  IN ONE IMAGE", font=typeface(25),
           fill=AMBER)
    d.text((28, 48), "18 NOVEMBER 2026", font=typeface(62), fill=WHITE)
    d.text((28, 116), "Wednesday  •  Six stories that shaped the world that day",
           font=typeface(20, False), fill=(205, 210, 225))
    badge = [CANVAS - 208, 26, CANVAS - 28, 122]
    d.rounded_rectangle(badge, radius=12, outline=AMBER, width=3)
    d.text((CANVAS - 190, 38), "18 NOV", font=typeface(34), fill=WHITE)
    d.text((CANVAS - 178, 78), "2026", font=typeface(28), fill=AMBER)
    d.rectangle([0, 148, CANVAS, 154], fill=AMBER)

    margin = 24
    col_w = (CANVAS - margin * 2 - 16) // 2
    lead = ITEMS[0]
    draw_story_card(d, lead, margin, 170, CANVAS - margin * 2, 196, 288,
                    hero=True)
    y = 382
    for row in (ITEMS[1:3], ITEMS[3:5]):
        for i, item in enumerate(row):
            draw_story_card(d, item, margin + i * (col_w + 16), y, col_w,
                            208, 140)
        y += 224
    draw_story_card(d, ITEMS[5], margin, y, CANVAS - margin * 2, 148, 168)

    # Footer.
    d.rectangle([0, CANVAS - 44, CANVAS, CANVAS], fill=DARK)
    d.text((28, CANVAS - 32),
           "Summarised from reports published on 18 November 2026  •  "
           "No single story tells the whole day",
           font=typeface(18, False), fill=(205, 210, 225))
    return img


if __name__ == "__main__":
    build().save("entry.png", "PNG")
