#!/usr/bin/env python3
"""Compose the visual-first front page for 19 November 2026.

Layout: masthead, one large summit illustration, a bold lead headline,
six short stories in two columns and a numbers strip along the foot.
Run:  python3 tools/compose.py   -> writes entry.png (1024x1024)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
HERO = ROOT / "assets" / "hero.png"
OUT = ROOT / "entry.png"

W = 1024
MARGIN = 28
PAPER = (247, 243, 234)
INK = (26, 24, 20)
ACCENT = (146, 32, 24)
RULE = (26, 24, 20)
BAND = (24, 22, 34)
BAND_TX = (244, 238, 222)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


class Pen:
    """Tiny text helper: wraps, lefts, centres."""

    def __init__(self, draw):
        self.d = draw

    def width(self, text, fnt):
        return self.d.textlength(text, font=fnt)

    def wrap(self, text, fnt, limit):
        words, lines, cur = text.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if self.width(trial, fnt) <= limit:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def block(self, xy, text, fnt, fill, limit, leading):
        x, y = xy
        for line in self.wrap(text, fnt, limit):
            self.d.text((x, y), line, font=fnt, fill=fill)
            y += leading
        return y

    def centred(self, cx, y, text, fnt, fill):
        self.d.text((cx - self.width(text, fnt) / 2, y), text, font=fnt, fill=fill)
        return y + fnt.size


def hero_block(page, draw, pen):
    """Paste the summit illustration, cropped to a wide band."""
    art = Image.open(HERO).convert("RGB")
    target_w = W - 2 * MARGIN
    target_h = 428
    scale = max(target_w / art.width, target_h / art.height)
    art = art.resize((round(art.width * scale), round(art.height * scale)))
    left = (art.width - target_w) // 2
    top = int((art.height - target_h) * 0.35)
    art = art.crop((left, top, left + target_w, top + target_h))
    y = 118
    page.paste(art, (MARGIN, y))
    draw.rectangle([MARGIN, y, MARGIN + target_w, y + target_h], outline=RULE, width=3)
    cap_y = y + target_h + 8
    pen.centred(W / 2, cap_y,
                "Dawn over Shenzhen Bay: three leaders, six flags, one table — the summit that set the day's agenda.",
                font(SERIF_I, 17), (84, 78, 66))
    return cap_y + 30


LEAD = ("THREE FLAGS OVER SHENZHEN",
        "Xi hosts Trump and Putin for a trilateral on trade, chips and the sea lanes — "
        "the first three-way summit of the decade, opened at dawn in Shenzhen.")

STORIES_LEFT = [
    ("Iran shuts Kuwaiti airspace",
     "Tehran closes the skies after strikes on its bases; Gulf flights reroute, oil jumps."),
    ("Rocket kills 53 in Israel",
     "A Houthi long-range strike is the deadliest of the year; the region braces for reply."),
    ("EU agrees €45bn package",
     "Brussels signs off the support deal after a night of haggling among finance chiefs."),
]
STORIES_RIGHT = [
    ("Jeffries holds the gavel",
     "The Speaker survives a leadership challenge in Washington by a handful of votes."),
    ("Voyager crosses 15.5 light-days",
     "Humanity's farthest object phones home across a widening dark; signal still strong."),
    ("Nvidia warns on chip supply",
     "CFO Colette Kress tells analysts tight supply runs into 2027; shares whipsaw."),
]

NUMBERS = "53  DEAD IN THE ROCKET STRIKE      €45BN  EU PACKAGE      $3,735  GOLD      15.5  LIGHT-DAYS TO VOYAGER 1"


def story(pen, x, y, head, body, col_w):
    y = pen.block((x, y), head.upper(), font(SANS_B, 20), ACCENT, col_w, 24)
    y = pen.block((x, y + 2), body, font(SANS, 18), INK, col_w, 23)
    return y + 14


def main():
    page = Image.new("RGB", (W, W), PAPER)
    draw = ImageDraw.Draw(page)
    pen = Pen(draw)

    # Masthead
    pen.centred(W / 2, 16, "THE DAY IN BRIEF", font(SERIF_B, 54), INK)
    draw.line([MARGIN, 92, W - MARGIN, 92], fill=RULE, width=3)
    pen.centred(W / 2, 97, "Thursday 19 November 2026  ·  The world in one page  ·  No. 19",
                font(SERIF, 16), (84, 78, 66))

    y = hero_block(page, draw, pen)

    # Lead headline
    pen.centred(W / 2, y + 2, LEAD[0], font(SERIF_B, 41), INK)
    pen.block((MARGIN + 60, y + 52), LEAD[1], font(SERIF, 19), INK, W - 2 * MARGIN - 120, 25)
    y += 108
    draw.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)

    # Two story columns
    col_w = (W - 2 * MARGIN - 36) // 2
    lx, rx = MARGIN, MARGIN + col_w + 36
    ly = ry = y + 14
    for head, body in STORIES_LEFT:
        ly = story(pen, lx, ly, head, body, col_w)
    for head, body in STORIES_RIGHT:
        ry = story(pen, rx, ry, head, body, col_w)
    mid = MARGIN + col_w + 18
    draw.line([mid, y + 14, mid, max(ly, ry) - 10], fill=(196, 188, 168), width=2)

    # Numbers band
    band_y = 952
    draw.rectangle([0, band_y, W, W], fill=BAND)
    pen.centred(W / 2, band_y + 14, "THE DAY IN NUMBERS", font(SANS_B, 17), (196, 170, 90))
    pen.centred(W / 2, band_y + 40, NUMBERS, font(SANS_B, 16), BAND_TX)

    page.save(OUT, optimize=True)
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
