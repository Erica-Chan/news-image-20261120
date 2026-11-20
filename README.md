# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Erica-Chan/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Erica-Chan/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday, 20 November 2026: the ICJ's genocide ruling against Myanmar, the first Trump–Xi–Putin three-way summit in Shenzhen, Russia's overnight strikes on Kyiv and the airspace incursion over Poland, the Houthi missile that hit Riyadh's tallest tower, Anthropic's Nasdaq debut as markets slid, and the end of Kenya's Ebola outbreak — plus the day's other headlines in the footer strip.

The poster is drawn by `compose_poster.py` (PIL; crisp text over an AI-generated, text-free hero illustration kept as `hero.png`) and shipped as `entry.png`. `main.ts` (Node 22, standard library only) copies it to `/output/entry.png`, so two runs write identical bytes with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=96p1ekwa&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
