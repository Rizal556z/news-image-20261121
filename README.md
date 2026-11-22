# news-image-20261121 — World News, Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Rizal556z/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Rizal556z/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for the [make.fun bounty "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121) — $100 pot, top 50 share.

## The image

A dense one-page news poster for **Saturday, 21 November 2026** — "ONE DAY
OF WORLD NEWS, ONE PICTURE", 33 stories — leading with Russia's
double-tap ballistic strike on Kryvyi Rih (a boy of 7 and a woman of 20
killed, 60 wounded), the COP31 climate talks running into overtime in
Antalya with fossil fuels missing from the draft deal, and Mexico's
capture of cartel boss "El Chapo Isidro" with US intelligence help,
with a numbers strip (60 wounded, Nasdaq −5.28%, S&P 500 −3.7%, $4tn
wiped, 6.7 quake, 13 dead in Manipur), a 10-story grid, a UTC timeline,
a "Where it happened" world map with region counts, and a numbered list
of stories 14–33 below them. V2 is denser than v1: it adds the map and
fills the two gaps in v1's list (items 18 and 27). Round 2 redraws the
same poster with a program (see below): every grid item 4–13 now has
its own header, including the missing item 8, the numbers strip drops
the stray "-.7%" cell, and two verified stories join the grid — Iran
striking Bahrain and Denmark expelling the Russian envoy.

## How it works

`draw_poster.py` draws `entry.png` (1024x1024 JPEG) with Pillow:
all 33 headlines, the UTC timeline, the numbers strip, the map and
the 14–33 list are written in that file, so re-running it writes
identical bytes. `main.py` (Python 3, pure standard library, no
network) then verifies the poster is a genuine 1024x1024 JPEG and
copies it byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`.

```sh
python3 draw_poster.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
