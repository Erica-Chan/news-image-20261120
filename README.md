# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Erica-Chan/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Erica-Chan/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday, 20 November 2026: 36 stories across 7 regions. Top story: the ICJ's genocide ruling against Myanmar. Four illustrated leads: Cyclone Akvan's landfall in India, the first Trump–Xi–Putin summit in Shenzhen, Russia's strikes on Kyiv's bridges, and COP31's final-day deadlock in Antalya — plus a world map, a by-the-numbers strip and a date check. The day's other stories run as one-line briefs under region headers: Europe, Middle East, Asia & Pacific, Africa, Americas, Markets & Tech, Culture & Science.

The poster is drawn by `compose_poster.py` (PIL; crisp text over an AI-generated, text-free hero illustration kept as `hero.png`) and shipped as `entry.png`. `main.ts` (Node 22, standard library only) copies it to `/output/entry.png`, so two runs write identical bytes with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=96p1ekwa&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
