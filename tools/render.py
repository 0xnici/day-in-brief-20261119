#!/usr/bin/env python3
"""Typeset one edition of The Day in Brief as a 1024x1024 front page.

Usage: python3 tools/render.py 2026-11-19 /path/to/entry.png

The page is a broadsheet in miniature: a masthead with the weekday and
date in large serif type over a double rule, six story panels in two
columns, an "also today" strip, and a colophon. Every story is drawn
from that day's wire reporting; the CONTENT table below is the whole
editorial input, and the drawing code never invents a fact of its own.

Deterministic by construction: fixed fonts, fixed geometry, no clocks,
no randomness, no network. The same edition renders byte-identically
on every run.
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 46

PAPER = (250, 247, 240)
INK = (26, 24, 20)
BODY = (52, 48, 40)
ACCENT = (150, 30, 30)
RULE = (26, 24, 20)
DIV = (198, 190, 175)
FAINT = (110, 102, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"

CONTENT = {
    "2026-11-19": {
        "weekday": "THURSDAY",
        "dateline": "19 NOVEMBER 2026",
        "stories": [
            (
                "SHENZHEN · APEC SUMMIT",
                "Three nuclear powers, one table",
                "Trump, Xi and Putin meet in Shenzhen for the first trilateral "
                "of the three leaders, one hour set aside at the APEC summit. "
                "Trump presses nuclear arms control; Beijing resists. Xi met "
                "Trump at the airport; Putin opened with a handshake.",
            ),
            (
                "THE GULF",
                "Iran fires on Kuwait as the war widens",
                "Iran struck US drone and missile sites in Kuwait overnight, "
                "its first attack there since September, after US forces hit "
                "Qeshm Island. Bahrain says it has now intercepted Iranian "
                "attacks three times in a week.",
            ),
            (
                "WASHINGTON",
                "Jeffries nominated for Speaker",
                "House Democrats nominate Hakeem Jeffries, who would be the "
                "first African-American Speaker of the House, as the party "
                "takes the chamber after the midterms. Its Senate haul is the "
                "largest in nearly seventy years.",
            ),
            (
                "NVIDIA",
                "A new chief, and pay comes first",
                "Acting chief executive Colette Kress, in the job since Jensen "
                "Huang's resignation, used her first all-hands to promise "
                "earlier pay raises and larger stock grants. The chipmaker has "
                "halted H-series shipments to mainland China.",
            ),
            (
                "DEEP SPACE",
                "Voyager 1, one light-day from home",
                "After almost fifty years in flight, NASA's Voyager 1 is "
                "believed to have crossed one light-day from Earth: its "
                "signals now take a full day to arrive. NASA is to confirm "
                "the milestone at a briefing on Thursday.",
            ),
            (
                "BRUSSELS",
                "EU proposes \u20ac45bn loan for Ukraine",
                "The European Commission proposes a \u20ac45 billion loan to "
                "keep Kyiv's budget afloat, to be repaid once Russia pays "
                "reparations for the war. The plan now goes to EU leaders, "
                "with Ukraine's finances strained by the long war.",
            ),
        ],
        "also": (
            "GTA VI begins its global rollout after a thirteen-year wait \u00b7 "
            "Fed minutes point to further rate hikes \u00b7 Cyclone Akvan "
            "strengthens toward the Andhra coast \u00b7 Gold falls 3% to a "
            "fourteen-month low as the dollar hits a nineteen-month high \u00b7 "
            "Bangladesh deploys paramilitaries over Hasina's planned return \u00b7 "
            "Pew: Islam on track to be the world's largest religion by 2035"
        ),
    },
}


def wrap(draw, text, font, width):
    # Greedy word wrap: keep adding words while the line still fits.
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit(draw, text, path, size, width, max_lines):
    # Shrink the font from `size` down until the wrapped text fits the box.
    while size > 10:
        font = ImageFont.truetype(path, size)
        if len(wrap(draw, text, font, width)) <= max_lines:
            return font
        size -= 1
    return ImageFont.truetype(path, size)


def centered(draw, text, font, y, fill):
    # One line of text centred on the page width at height y.
    x = (W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_masthead(draw, edition):
    # Kicker, weekday and date stacked in large type, closed by the
    # double rule every newspaper front page carries. Returns the y
    # coordinate the story grid starts at.
    y = 34
    kicker_font = ImageFont.truetype(SANS_B, 23)
    centered(draw, "THE DAY IN BRIEF \u00b7 THE WORLD ON ONE PAGE", kicker_font, y, ACCENT)
    y += 40
    weekday_font = ImageFont.truetype(SERIF_B, 44)
    centered(draw, edition["weekday"], weekday_font, y, INK)
    y += 54
    dateline_font = ImageFont.truetype(SERIF_B, 63)
    centered(draw, edition["dateline"], dateline_font, y, INK)
    y += 84
    draw.rectangle([MARGIN, y, W - MARGIN, y + 5], fill=RULE)
    draw.rectangle([MARGIN, y + 9, W - MARGIN, y + 11], fill=RULE)
    return y + 26


def draw_story_panel(draw, story, cx, cy, col_w, row_h, index):
    # One panel: accent kicker, a fitted serif headline, a fitted brief,
    # then the hairline dividers that separate it from its neighbours.
    kicker, headline, brief = story
    kicker_font = ImageFont.truetype(SANS_B, 19)
    draw.text((cx, cy), kicker, font=kicker_font, fill=ACCENT)

    headline_font = fit(draw, headline, SERIF_B, 29, col_w, 2)
    y = cy + 30
    for line in wrap(draw, headline, headline_font, col_w):
        draw.text((cx, y), line, font=headline_font, fill=INK)
        y += 34

    brief_font = fit(draw, brief, SERIF, 20, col_w, 4)
    y += 2
    for line in wrap(draw, brief, brief_font, col_w):
        draw.text((cx, y), line, font=brief_font, fill=BODY)
        y += 25

    gap = 26
    if index % 2 == 0 and index < 5:
        divider_x = cx + col_w + gap // 2
        draw.line([divider_x, cy + 2, divider_x, cy + row_h - 18], fill=DIV, width=1)
    if index < 4:
        draw.line([cx, cy + row_h - 8, cx + col_w, cy + row_h - 8], fill=DIV, width=1)


def draw_story_grid(draw, edition, top):
    # Six panels in two columns and three rows over a fixed grid height.
    gap = 26
    inner = W - 2 * MARGIN
    col_w = (inner - gap) // 2
    grid_h = 600
    row_h = grid_h // 3
    for index, story in enumerate(edition["stories"]):
        cx = MARGIN + (index % 2) * (col_w + gap)
        cy = top + (index // 2) * row_h
        draw_story_panel(draw, story, cx, cy, col_w, row_h, index)
    return top + grid_h


def draw_closing_strip(draw, edition, grid_bottom):
    # The "also today" strip under a heavy rule, and the colophon that
    # closes the page: sources, and the promise nothing here is invented.
    inner = W - 2 * MARGIN
    y = grid_bottom + 10
    draw.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=RULE)
    y += 14
    strip_font = ImageFont.truetype(SANS_B, 19)
    draw.text((MARGIN, y), "ALSO TODAY", font=strip_font, fill=ACCENT)
    y += 28
    also_font = fit(draw, edition["also"], SANS, 19, inner, 3)
    for line in wrap(draw, edition["also"], also_font, inner):
        draw.text((MARGIN, y), line, font=also_font, fill=INK)
        y += 25
    y += 8
    draw.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=RULE)
    y += 10
    colophon = "Compiled from the day's wire reporting \u00b7 One page, the whole day \u00b7 No story here is invented; figures as reported that day"
    colophon_font = ImageFont.truetype(SANS, 16)
    centered(draw, colophon, colophon_font, y, FAINT)


def main():
    day, out_path = sys.argv[1], sys.argv[2]
    edition = CONTENT[day]
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    grid_top = draw_masthead(draw, edition)
    grid_bottom = draw_story_grid(draw, edition, grid_top)
    draw_closing_strip(draw, edition, grid_bottom)
    page.save(out_path, format="PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
