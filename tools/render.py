#!/usr/bin/env python3
"""Typeset the dense edition of The Day in Brief for 19 November 2026.

Usage: python3 tools/render.py 2026-11-19 /path/to/entry.png

One page, the whole day, at broadsheet density: a compact masthead, a
lead story beside a dotted world map marked with the day's datelines, a
"day in numbers" band, and twenty-six stories in four columns under
region headers, plus one-line briefs. Every item is drawn from that
day's wire reporting; the tables below are the whole editorial input
and the drawing code adds no facts of its own.

Deterministic: fixed fonts, fixed geometry, no clocks, no randomness,
no network. The same edition renders byte-identically on every run.
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 36
INNER = W - 2 * MARGIN

PAPER = (250, 247, 240)
INK = (26, 24, 20)
BODY = (52, 48, 40)
ACCENT = (150, 30, 30)
RULE = (26, 24, 20)
DIV = (203, 195, 180)
FAINT = (110, 102, 90)
MAPDOT = (168, 158, 140)
BAND = (26, 24, 20)
BANDTXT = (250, 247, 240)
BANDSUB = (206, 198, 182)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"

WEEKDAY = "THURSDAY"
DATELINE = "19 NOVEMBER 2026"

LEAD_KICKER = "SHENZHEN \u00b7 APEC SUMMIT \u00b7 THE LEAD"
LEAD_HEADLINE = "Three nuclear powers, one table in Shenzhen"
LEAD_TEXT = (
    "Trump, Xi and Putin sit down together for the first trilateral "
    "meeting of the three leaders, one hour set aside at the APEC "
    "summit. Trump wants nuclear arms control at the centre; Beijing "
    "resists. Xi met Trump at the airport; Putin attacked sanctions."
)

NUMBERS = [
    ("3", "nuclear powers\nat one table"),
    ("\u20ac45bn", "EU loan proposed\nfor Ukraine"),
    ("1", "light-day: Voyager's\ndistance out"),
    ("$3,735", "gold's low, a\nfourteen-month first"),
    ("96%", "of coral reefs at\nrisk by 2075"),
    ("53", "soldiers killed\nin Yemen"),
]

SECTIONS = {
    "THE GULF": [
        ("Iran fires on Kuwait",
         "Tehran struck US drone and missile sites in Kuwait overnight, "
         "its first attack there since September; Bahrain has intercepted "
         "Iranian attacks three times in a week."),
        ("Houthi rocket kills 53",
         "A Houthi rocket hit a military camp in Yemen, killing at least "
         "53 soldiers of the recognised government."),
        ("Saudi cities stand down",
         "Riyadh says the danger has passed in three southern cities, as "
         "Houthi forces retake the Bab el-Mandeb strait."),
    ],
    "EUROPE": [
        ("EU's \u20ac45bn loan for Ukraine",
         "The Commission proposes borrowing \u20ac45 billion for Kyiv's "
         "budget, repaid once Russia pays reparations."),
        ("Moscow accuses Paris",
         "Lavrov says Russia is aware of French troop deployments to "
         "Ukraine and has formally protested to Paris."),
        ("Finland opens waste repository",
         "Helsinki authorises the world's first disposal facility for "
         "spent nuclear fuel to begin operating."),
        ("Spy suspect held in Germany",
         "A suspected Russian spy is arrested as espionage cases rise; "
         "state leaders press Berlin on energy taxes."),
    ],
    "AMERICAS": [
        ("Jeffries nominated for Speaker",
         "House Democrats nominate Hakeem Jeffries, set to be the first "
         "African-American Speaker; the Senate haul is the party's "
         "largest in nearly seventy years."),
        ("AI cyber threat outruns defences",
         "Senators warn the White House that AI-enabled cyber threats "
         "are outpacing the country's defences."),
        ("Outage hits NSA network",
         "An outage of the NSA's classified internal network disrupted "
         "intelligence staff and forced schedule changes."),
        ("Fed minutes point to hikes",
         "Minutes of the October meeting show most officials expecting "
         "further rate rises if inflation runs as expected."),
    ],
    "SCIENCE & TECH": [
        ("Voyager 1, a light-day out",
         "NASA's probe is believed to have crossed one light-day from "
         "Earth after 49 years; confirmation is due Thursday."),
        ("Nvidia halts H-series for China",
         "H-series shipments to the mainland stop; acting CEO Colette "
         "Kress promises earlier raises at her first all-hands."),
        ("Reefs face near-total risk",
         "An IUCN analysis unveiled in Armenia puts 96% of the world's "
         "coral reefs at extreme risk by 2075."),
    ],
    "ASIA-PACIFIC": [
        ("Xi calls for open trade",
         "At APEC in Shenzhen, Xi urges open trade and wider market "
         "access; Putin attacks Western sanctions as a failure."),
        ("Cyclone Akvan bears down",
         "The Bay of Bengal storm is set to turn very severe and cross "
         "the Andhra Pradesh coast on Friday."),
        ("Bangladesh locks down",
         "Paramilitaries deploy nationwide as protests over Hasina's "
         "planned December return turn to bombs and arson."),
        ("Amazon's $7bn renewables bet",
         "Amazon plans $7 billion of renewable investment in India by "
         "2030; green capacity stands at 299.25 GW."),
    ],
    "MARKETS": [
        ("Gold slides, dollar climbs",
         "Gold falls 3% to $3,735 an ounce, a fourteen-month low; the "
         "dollar touches a nineteen-month high."),
        ("Goldman turns bullish on India",
         "Goldman Sachs upgrades India to overweight, with a December "
         "2027 target of 28,500 for the Nifty."),
        ("JPMorgan's $1bn crypto book",
         "Filings show JPMorgan holding about $981 million in Bitcoin "
         "ETFs and crypto stocks in the third quarter."),
    ],
    "HEALTH": [
        ("US loses measles-free status",
         "After twelve months of continuous transmission, the United "
         "States formally loses measles elimination status."),
        ("WHO: resistance rising",
         "WHO warns antibiotic resistance is climbing in Europe's "
         "hospital bacteria; India opens AMR awareness week."),
    ],
    "SPORT & CULTURE": [
        ("Vice City opens at last",
         "Grand Theft Auto VI begins its global rollout after a "
         "thirteen-year wait \u2014 the industry's biggest launch."),
        ("India edge Pakistan in final",
         "India beat Pakistan 2\u20131 in Dhaka to win the SAFF "
         "Championship; the losers gave a guard of honour."),
    ],
}

BRIEFS = [
    "COP31: the AI pledge in Antalya fails to attract major US tech firms",
    "Anthropic's IPO pricing awaited as Wall Street digests Nvidia",
    "Microsoft in talks to sell AI services to ByteDance, say reports",
    "Pew: Islam on track to be the world's largest religion by 2035",
]

# Coarse dotted world map, one character per dot cell. '#' is land.
MAP_ROWS = [
    "                                                                ",
    "        #######                                                 ",
    "     ###########      ##     ##########  ##################     ",
    "   #############    ####   ############ ####################    ",
    "  ##############    ####  ###############################       ",
    "   ############      ##    #############################        ",
    "    ##########              ##########################          ",
    "     ########                ###  #################             ",
    "      ######                  ##    ##############              ",
    "       #####                        ############                ",
    "       ####                          ##########                 ",
    "       ###                            ########                  ",
    "      ####                             ######                   ",
    "      ###                               ####        ##          ",
    "     ####                               ###        ####         ",
    "     ###                                                ##      ",
    "                                                                ",
]
# (column, row, label) markers on the map grid above.
MARKERS = [(49, 4, "SHENZHEN"), (38, 5, "HORMUZ"), (10, 4, "WASHINGTON"), (31, 3, "BRUSSELS")]

COLUMNS = [
    ["THE GULF", "EUROPE"],
    ["AMERICAS", "SCIENCE & TECH"],
    ["ASIA-PACIFIC", "MARKETS"],
    ["HEALTH", "SPORT & CULTURE"],
]


def wrap(draw, text, font, width):
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
    while size > 9:
        font = ImageFont.truetype(path, size)
        if len(wrap(draw, text, font, width)) <= max_lines:
            return font
        size -= 1
    return ImageFont.truetype(path, size)


def centered(draw, text, font, y, fill):
    x = (W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_masthead(draw):
    y = 20
    kicker_font = ImageFont.truetype(SANS_B, 19)
    centered(draw, "THE DAY IN BRIEF \u00b7 THE WORLD ON ONE PAGE", kicker_font, y, ACCENT)
    y += 28
    title_font = ImageFont.truetype(SERIF_B, 48)
    centered(draw, f"{WEEKDAY} {DATELINE}", title_font, y, INK)
    y += 60
    draw.rectangle([MARGIN, y, W - MARGIN, y + 5], fill=RULE)
    draw.rectangle([MARGIN, y + 9, W - MARGIN, y + 11], fill=RULE)
    return y + 20


def draw_map(draw, x, y, w):
    # Dotted continents with red dateline markers.
    cols = len(MAP_ROWS[0])
    rows = len(MAP_ROWS)
    cell = w / cols
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                cx = x + c * cell + cell / 2
                cy = y + r * cell + cell / 2
                draw.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=MAPDOT)
    label_font = ImageFont.truetype(SANS_B, 10)
    for c, r, label in MARKERS:
        cx = x + c * cell + cell / 2
        cy = y + r * cell + cell / 2
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=ACCENT)
        draw.text((cx + 7, cy - 6), label, font=label_font, fill=ACCENT)
    return y + int(rows * cell)


def draw_lead(draw, top):
    text_w = 600
    kicker_font = ImageFont.truetype(SANS_B, 16)
    draw.text((MARGIN, top), LEAD_KICKER, font=kicker_font, fill=ACCENT)
    headline_font = fit(draw, LEAD_HEADLINE, SERIF_B, 38, text_w, 2)
    y = top + 24
    for line in wrap(draw, LEAD_HEADLINE, headline_font, text_w):
        draw.text((MARGIN, y), line, font=headline_font, fill=INK)
        y += 42
    body_font = ImageFont.truetype(SERIF, 15)
    y += 2
    for line in wrap(draw, LEAD_TEXT, body_font, text_w):
        draw.text((MARGIN, y), line, font=body_font, fill=BODY)
        y += 21
    map_x = MARGIN + text_w + 28
    map_bottom = draw_map(draw, map_x, top + 4, INNER - text_w - 28)
    cap_font = ImageFont.truetype(SANS, 11)
    draw.text((map_x, map_bottom + 4), "WHERE THE DAY HAPPENED", font=cap_font, fill=FAINT)
    bottom = max(y, map_bottom + 22)
    draw.line([MARGIN, bottom + 6, W - MARGIN, bottom + 6], fill=DIV, width=1)
    return bottom + 14


def draw_numbers(draw, top):
    draw.rectangle([MARGIN, top, W - MARGIN, top + 68], fill=BAND)
    head_font = ImageFont.truetype(SANS_B, 11)
    draw.text((MARGIN + 12, top + 5), "THE DAY IN NUMBERS", font=head_font, fill=BANDSUB)
    col_w = INNER / len(NUMBERS)
    big_font = ImageFont.truetype(SERIF_B, 21)
    small_font = ImageFont.truetype(SANS, 9)
    for i, (big, small) in enumerate(NUMBERS):
        x = MARGIN + 12 + i * col_w
        draw.text((x, top + 19), big, font=big_font, fill=BANDTXT)
        for j, line in enumerate(small.split("\n")):
            draw.text((x, top + 45 + j * 11), line, font=small_font, fill=BANDSUB)
    return top + 76


def draw_item(draw, headline, brief, x, y, w):
    head_font = fit(draw, headline, SANS_B, 14, w, 2)
    for line in wrap(draw, headline, head_font, w):
        draw.text((x, y), line, font=head_font, fill=INK)
        y += 15
    brief_font = fit(draw, brief, SERIF, 11, w, 3)
    y += 1
    for line in wrap(draw, brief, brief_font, w):
        draw.text((x, y), line, font=brief_font, fill=BODY)
        y += 12
    return y + 5


def draw_section(draw, title, items, x, y, w):
    head_font = ImageFont.truetype(SANS_B, 13)
    draw.text((x, y), title, font=head_font, fill=ACCENT)
    y += 17
    draw.line([x, y, x + w, y], fill=DIV, width=1)
    y += 5
    for headline, brief in items:
        y = draw_item(draw, headline, brief, x, y, w)
    return y


def draw_grid(draw, top):
    gap = 22
    col_w = (INNER - 3 * gap) // 4
    bottom = top
    for i, section_names in enumerate(COLUMNS):
        x = MARGIN + i * (col_w + gap)
        y = top
        for name in section_names:
            y = draw_section(draw, name, SECTIONS[name], x, y, col_w)
            y += 6
        bottom = max(bottom, y)
        if i < 3:
            vx = x + col_w + gap // 2
            draw.line([vx, top, vx, bottom], fill=DIV, width=1)
    return bottom


def draw_briefs(draw, top):
    head_font = ImageFont.truetype(SANS_B, 13)
    draw.text((MARGIN, top), "IN BRIEF", font=head_font, fill=ACCENT)
    font = ImageFont.truetype(SANS, 12)
    y = top + 20
    x = MARGIN
    for item in BRIEFS:
        text = item + "   \u00b7   "
        width = draw.textlength(text, font=font)
        if x + width > W - MARGIN:
            y += 17
            x = MARGIN
        draw.text((x, y), text, font=font, fill=BODY)
        x += width
    return y + 17


def draw_footer(draw):
    top = H - 34
    draw.rectangle([MARGIN, top, W - MARGIN, top + 2], fill=RULE)
    colophon = "Compiled from the day's wire reporting \u00b7 One page, the whole day \u00b7 No story here is invented; figures as reported that day"
    font = ImageFont.truetype(SANS, 12)
    y = top + 8
    x = (W - draw.textlength(colophon, font=font)) / 2
    draw.text((x, y), colophon, font=font, fill=FAINT)


def main():
    day, out_path = sys.argv[1], sys.argv[2]
    if day != "2026-11-19":
        print("error: this typesetter carries only the 2026-11-19 edition", file=sys.stderr)
        return 1
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    y = draw_numbers(draw, y)
    y = draw_grid(draw, y + 2)
    draw_briefs(draw, y + 4)
    draw_footer(draw)
    page.save(out_path, format="PNG", optimize=True)
    print("wrote", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
