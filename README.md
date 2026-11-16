# Site STORM

Site de la team STORM — *Quantitative Risk Collective*, la team de
recherche quantitative de Square Management. Deux éditions (française et anglaise) construites avec
[Quarto](https://quarto.org).

## Construire

```bash
quarto render                 # édition française  → docs/fr
quarto render --profile en    # édition anglaise   → docs/en
bash build.sh                 # les deux d'un coup

quarto preview                # aperçu avec rechargement automatique
```

`quarto render` sans option construit l'édition française (profil par défaut).
Chaque rendu se recopie tout seul dans `docs/`.

## Modifier

**→ voir [GUIDE.md](GUIDE.md).** Actualités, projets, publications, axes et schémas
se modifient dans `data/`, sans toucher au HTML.

## Structure

```
data/           actualités, projets, publications, axes, schémas ← le contenu vivant
                (_notes.yml est produit automatiquement)
templates/      gabarits fr/ et en/ — la forme des fiches
assets/
  brand/        logos STORM (Square Research Center retiré)
  css/          storm.scss (système de design) + fonts.css
  fonts/        Source Serif 4, Source Sans 3, IBM Plex Mono
  katex/        KaTeX auto-hébergé
partials/       after-body.html — fond animé (distributions en mouvement)
fr/  en/        pages rédigées
_quarto.yml     réglages communs
_quarto-fr.yml  navigation et langue — édition française
_quarto-en.yml  navigation et langue — édition anglaise
scripts/        collect.py (avant rendu) + assemble.sh (après) — appelés par Quarto
build.sh        raccourci : rend les deux éditions
docs/           site construit (GitHub Pages)
```

Aucune requête vers un tiers au chargement : polices et KaTeX sont servis depuis
le site.

## Reste à faire

- Domaine et adresse de contact réels
- Traduction anglaise des quatre notes techniques
