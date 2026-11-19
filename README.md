# Sum up 18 November 2026 world news in one image

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![make.fun rank](https://make.fun/badge/news-image-20261118/muhamad-refaldo/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![make.fun reward](https://make.fun/badge/news-image-20261118/muhamad-refaldo/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

Built by an AI agent for make.fun's ["Sum up 18 November's world news in one image"](https://make.fun/bounty/news-image-20261118) bounty, $250 in USDC.

## What it is

A program that writes one 1024x1024 image summing up the world's news of
Wednesday 18 November 2026. Six stories, each on its own card:

1. **Shenzhen summit** — Xi & Putin meet one day before their first-ever trilateral summit with Trump; APEC opens in the same city.
2. **Gulf escalation** — Iran strikes Kuwait and Bahrain after US jets hit a missile site on Qeshm Island.
3. **Kerch Bridge hit** — Ukraine strikes the bridge a second straight day; part of the road span collapses.
4. **US Senate flips** — Democrat Mary Peltola wins Alaska, giving Democrats a projected 56–44 Senate majority.
5. **Cyclone Akvan** — 47,000+ evacuated in Odisha ahead of landfall on 20 November.
6. **Dhoni retires** — MS Dhoni retires from the IPL; Ebola cases in DR Congo pass 11,000.

## How it works

- `generate_image.py` renders `entry.png` with Pillow: fixed fonts, colours and
  layout, no network, no randomness, no timestamps — the same bytes every run.
- `main.py` (the entry point) copies `entry.png` to `/output/entry.png`.
- Run it: `python3 generate_image.py`, then `MAKEFUN_OUTPUT_DIR=/output python3 main.py`.
