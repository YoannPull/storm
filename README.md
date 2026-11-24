# STORM website

Website of **STORM** — *Quantitative Risk Collective*, the quantitative research
team of [Square Management](https://www.square-management.com).

Live at **<https://squaremanagement-storm.com>** (GitHub Pages, French and
English editions), built with [Quarto](https://quarto.org).

## Build and publish

```bash
bash build.sh                 # builds both editions into docs/
quarto preview                # local preview with live reload (French edition)

git add .
git commit -m "Describe the change"
git push                      # GitHub Pages republishes docs/ within a minute or two
```

`quarto render` alone builds the French edition (default profile);
`quarto render --profile en` builds the English one. Each render copies itself
into `docs/` (see `scripts/assemble.sh`), which also writes `docs/CNAME`
(custom domain), `docs/.nojekyll` and `docs/favicon.ico`.

After publishing, reload with **Cmd + Shift + R** to bypass the browser cache.

**Clean URLs.** After each render, `scripts/clean_urls.py` rewrites internal
links so they no longer show `index.html` or `.html`
(`/fr/expertise/` instead of `/fr/expertise/index.html`). As a consequence,
opening `docs/fr/index.html` straight from the disk no longer lets you click
from page to page; preview locally with `python3 -m http.server -d docs`
(then <http://localhost:8000>) or `quarto preview`.

## Editing content

**→ See [GUIDE.md](GUIDE.md)** (in French) for step-by-step instructions.
Most content lives in `data/` and never requires touching HTML:

| What | Where |
|---|---|
| News items (talks, publications, visits…) | `data/actualites.yml` — technical notes appear automatically |
| Research papers | `data/publications.yml` |
| Method and application cards (homepage) | `data/axes.yml` |
| Architecture diagrams in notes | `data/schemas.yml` |
| Technical notes | `fr/notes/*.qmd` (French only for now) |
| Expertise page | `fr/expertise/index.qmd`, `en/expertise/index.qmd` |
| About page and contacts | `fr/a-propos/index.qmd`, `en/about/index.qmd` |
| Page not found (404) | `scripts/404.html` (copied to `docs/404.html` at each build) |
| Link-preview images (LinkedIn, X…) | `assets/brand/og-storm-fr.png`, `og-storm-en.png` (1200×630), set in `_quarto-fr.yml` / `_quarto-en.yml` |
| Navigation and footer | `_quarto-fr.yml`, `_quarto-en.yml` |

`data/_notes.yml` is generated before each build by `scripts/collect.py`; do
not edit it by hand. Projects in `data/projets.yml` marked
`rubrique: "recherche-en-cours"` appear under **Research in progress** on the Publications page.

## Site structure

| Page | French | English |
|---|---|---|
| Home | `/fr/` | `/en/` |
| Expertise (methods and applications) | `/fr/expertise/` | `/en/expertise/` |
| News | `/fr/actualites/` | `/en/news/` |
| Publications (papers and technical notes) | `/fr/publications/` | `/en/publications/` |
| About and contact | `/fr/a-propos/` | `/en/about/` |

## Design

- **Black theme**, a single accent colour (STORM blue `#4d8dff`), Source Sans 3
  for headings, Source Serif 4 for text, IBM Plex Mono for labels.
- **Theme files:** `assets/css/storm.scss` (tokens and base styles, compiled by
  Quarto) and `assets/css/storm-dark.css` (black-theme adjustments, homepage,
  Expertise page — plain CSS, loaded after the theme).
- **Animations:** `partials/after-body.html`, included on every page, holds
  their code *and* styles (so they are never stale in the browser cache).
  Texts for each language are grouped at the top of each animation's code.
  - the density "horizon" behind the homepage hero;
  - `credit` — credit stress test, played in three automatic phases
    (standard practice → STORM approach → your models);
  - `rst` — reverse stress test (threshold → exploration → breaking point →
    neighbourhood → selection);
  - `jeffreys` — Jeffreys calibration test on a low-default portfolio;
  - `eprocess` — continuous monitoring: one data stream watched by two alarm
    lanes on the same time axis, classic test (false alarms in red) vs
    anytime-valid approach (one blue alert after the mean shift), then bars
    for 200 simulated streams (in-house method, not yet published). Data are simulated in the browser from a fixed `seed`,
    so the figures are the same at every visit;
  - `tfm` — a pretrained tabular model estimating one-year default risk from
    prior borrower outcomes and a new loan file.

  To place one in a page:

  ```markdown
  ::: {.storm-anim data-anim="credit"}

  :::
  ```

  Each animation starts when it scrolls into view, pauses when it leaves,
  and stays still for visitors who disabled animations. Texts follow the page
  language.

Fonts and KaTeX are self-hosted. The only third-party request is the
visitor-statistics script (Cloudflare Web Analytics, cookieless), at the end of
`partials/after-body.html` and in `scripts/404.html`; dashboard in Cloudflare →
Analytics & Logs → Web Analytics.

## Repository layout

```
data/           news, publications, method/application cards, diagrams
templates/      listing templates, fr/ and en/
assets/
  brand/        STORM logos and favicons
  css/          storm.scss + storm-dark.css + fonts.css
  fonts/        self-hosted fonts
  katex/        self-hosted KaTeX
partials/       after-body.html — animations (code and styles)
fr/  en/        pages (French and English editions)
_quarto.yml     shared settings
_quarto-fr.yml  French navigation, footer, site URL
_quarto-en.yml  English navigation, footer, site URL
scripts/        collect.py (before render), assemble.sh + clean_urls.py (after render)
build.sh        builds both editions
docs/           built site, served by GitHub Pages (branch main, folder /docs)
_ancien/        old pages (team, former research pages) — not published, not in git
```

## Hosting

- **GitHub Pages:** repository `YoannPull/storm`, branch `main`, folder `/docs`.
- **Domain:** `squaremanagement-storm.com`, registered with Cloudflare. DNS
  records `@` and `www` point to `yoannpull.github.io` with proxy **off**
  (grey cloud, "DNS only"). MX/TXT records for iCloud email must not be
  changed.
- **HTTPS:** certificate issued by GitHub; tick *Enforce HTTPS* in
  Settings → Pages once available.

## To do

- English translations of the four technical notes
