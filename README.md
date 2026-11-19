# The Day in Brief — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/0xnici/day-in-brief-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/0xnici/day-in-brief-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One page, the whole day: a dense broadsheet front page that sums up the
world news of **Thursday 19 November 2026** in a single 1024×1024 image —
a lead story, a dotted world map of the day's datelines, a day-in-numbers
band, twenty-six stories in four columns, and an in-brief strip.

![The Day in Brief — Thursday 19 November 2026](entry.png)

## The front page

- **The lead · Shenzhen** — Trump, Xi and Putin hold the first trilateral
  meeting of the three leaders at the APEC summit, nuclear arms control
  on Trump's agenda, Beijing resisting.
- **The Gulf** — Iran fires on US sites in Kuwait; a Houthi rocket kills
  53 soldiers in Yemen; Saudi cities stand down.
- **Europe** — the €45 billion EU loan for Ukraine, Moscow's protest to
  Paris, Finland's nuclear-waste first, a spy arrest in Germany.
- **Americas** — Jeffries nominated for Speaker, senators warn on AI
  cyber threats, an NSA network outage, Fed minutes pointing to hikes.
- **Science & tech** — Voyager 1 a light-day out, Nvidia halts H-series
  shipments to China, 96% of coral reefs at risk by 2075.
- **Asia-Pacific** — Xi's open-trade call, Cyclone Akvan, Bangladesh's
  lockdown, Amazon's $7 billion India renewables bet.
- **Markets** — gold's fourteen-month low, Goldman's India upgrade,
  JPMorgan's $981 million crypto book.
- **Health, sport & culture** — the US loses measles-free status, WHO on
  antibiotic resistance, GTA VI's rollout, India's SAFF final win.

Every story comes from the day's wire reporting; no story is invented,
and figures are as reported that day.

## Run it

```sh
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` is standard library only and needs no network: it delivers the
committed `entry.png` to the output directory and verifies the copy byte
for byte before reporting success.

## Visual edition (v3)

The standing entry is a visual-first front page: a large summit
illustration (`assets/hero.png`) under the masthead, one bold lead
headline, six short stories and the numbers band, composed by
`tools/compose.py`:

```sh
python3 tools/compose.py   # writes entry.png
```

## Rebuild the page

```sh
python3 tools/render.py 2026-11-19 entry.png
```

The typesetter (`tools/render.py`, Pillow + DejaVu fonts) is
deterministic: the same edition renders byte-identically on every run.
Its `CONTENT` table is the whole editorial input — masthead, six story
panels, the also-today strip and the colophon.

## Licence

MIT — see `LICENSE`.
