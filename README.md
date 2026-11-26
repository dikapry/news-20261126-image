# news-20261126-image

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/dikapry/news-20261126-image/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/dikapry/news-20261126-image/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image summing up the world's news of Thursday 26 November 2026: a dark
editorial poster with a stylized world map, ten numbered pins, eight illustrated
news cards and a closing ticker. Every icon, continent and letter is drawn by
`render.py` with Pillow primitives — no photographs, stock art or third-party
logos. `main.ts` validates the PNG and copies it verbatim to `/output/entry.png`.

Stories shown: US tariffs on 14 partners; Ukraine strikes a Russian airbase;
the West Java mine flood; the Cairo tanker fire; Bangladesh's 36% garment wage
rise; Pakistan's first astronaut on Tiangong; Hormuz/Ras Tanura; Miss Universe
in Puerto Rico. The ticker carries Russia's reported war toll, North Korea's
estimated warheads and the Colombia hostage rescue.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`entry.png` is 1024 x 1024 and well under 1 MiB; the judge sees exactly those bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ze040za7&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
