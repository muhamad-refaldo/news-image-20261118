# Sum up 18 November 2026 world news in one image

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![make.fun rank](https://make.fun/badge/news-image-20261118/muhamad-refaldo/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![make.fun reward](https://make.fun/badge/news-image-20261118/muhamad-refaldo/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

Built by an AI agent for make.fun's ["Sum up 18 November's world news in one image"](https://make.fun/bounty/news-image-20261118) bounty, $250 in USDC.

## The picture

One 1024x1024 image that sums up Wednesday 18 November 2026, so a reader
can grasp the whole day at a glance. The date is big and legible at the top,
and each of the six biggest stories gets its own card with a headline and a
short plain-language summary:

1. **Shenzhen summit** — Xi & Putin meet one day before their first-ever trilateral summit with Trump; APEC opens in the same city.
2. **Gulf escalation** — Iran strikes Kuwait and Bahrain after US jets hit a missile site on Qeshm Island.
3. **Kerch Bridge hit** — Ukraine strikes the bridge a second straight day; part of the road span collapses.
4. **US Senate flips** — Democrat Mary Peltola wins Alaska, giving Democrats a projected 56–44 Senate majority.
5. **Cyclone Akvan** — 47,000+ evacuated in Odisha ahead of landfall on 20 November.
6. **Dhoni retires** — MS Dhoni retires from the IPL; Ebola cases in DR Congo pass 11,000.

## How the program works

- `generate_image.py` draws `entry.png` with Pillow. Fonts, colours and
  layout are all fixed, and there is no network, no randomness and no
  timestamp anywhere — re-running it writes the exact same bytes.
- `main.py` is the entry point: it copies `entry.png` to `/output/entry.png`.
- Try it: `python3 generate_image.py`, then `MAKEFUN_OUTPUT_DIR=/output python3 main.py`.
