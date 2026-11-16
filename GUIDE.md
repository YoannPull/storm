# Guide — modifier le site STORM

Tout ce qui change souvent (actualités, projets, publications, axes, schémas) se
modifie dans **un seul dossier : `data/`**. Ce sont des fichiers texte. Aucune
connaissance de HTML ou de CSS n'est nécessaire.

```
data/           ← ce que vous modifiez le plus souvent
templates/      ← l'apparence de chaque type de fiche (rarement)
fr/  en/        ← les pages rédigées
assets/css/     ← couleurs, typographie
```

Après chaque modification :

```bash
quarto render                 # édition française  → docs/fr
quarto render --profile en    # édition anglaise   → docs/en
bash build.sh                 # les deux d'un coup
```

`quarto render` sans option construit l'édition française : c'est le profil par
défaut. Chaque rendu se recopie tout seul dans `docs/` — il n'y a pas d'étape
supplémentaire. Ouvrir ensuite `docs/fr/index.html`.

Pour travailler avec rechargement automatique : `quarto preview`.

---

## 1. Les gestes les plus fréquents

### Ajouter une actualité

La page **Actualités** (`/fr/actualites/`, `/en/news/`) et l'accueil réunissent
deux sources, triées par date :

- les **notes techniques** (`fr/notes/*.qmd`) — elles y apparaissent seules,
  rien à faire ;
- tout le reste — publications, interventions, conférences, presse — dans
  **`data/actualites.yml`**.

Pour une intervention, copier ce bloc en haut de `data/actualites.yml` :

```yaml
- type: "intervention"          # publication | intervention | evenement | presse
  title: "Titre de l'intervention"
  title_en: "Talk title"        # facultatif
  qui: "Prénom Nom"             # qui intervient (affiché sous le titre)
  date: "2026-11-20"
  lieu: "Conférence XYZ, Paris"
  lieu_en: "XYZ Conference, Paris"
  path: "https://…"             # lien vers le programme, les slides…
```

Le libellé (« Intervention », « Talk »…) se choisit tout seul selon `type` ;
`etiquette` / `etiquette_en` le remplacent si besoin (« Séminaire »…).
L'accueil montre les cinq plus récentes.

### Ajouter un projet

`data/projets.yml`. Le projet apparaît automatiquement sur la page de son axe.

```yaml
- title: "Nom du projet"
  title_en: "Project name"
  axe: "credit"                     # credit | climat | geopolitique | methodes
  statut: "en-cours"                # a-demarrer | en-cours | relecture | termine
  statut_fr: "En cours"
  statut_en: "In progress"
  horizon: "T3"                     # ou ""
  resume_fr: "Une ou deux phrases."
  resume_en: "One or two sentences."
  equipe: ["Quentin Lajaunie", "Yoann Pull"]
  livrables: ["note", "article"]
  note: "notes/ma-note.html"        # ou "" s'il n'y a pas de note
```

`statut` pilote la couleur de la pastille ; `statut_fr` / `statut_en` sont les
mots affichés. Changer d'axe = changer `axe`, rien d'autre.

### Ajouter une publication

`data/publications.yml`. L'article apparaît sur `/fr/publications/` et sur la
page de son axe, apparié à sa note technique s'il y en a une.

```yaml
- title: "Titre exact de l'article"
  auteurs: ["Christophe Hurlin", "Yoann Pull"]
  date: "2026-06-01"                # le tri se fait là-dessus
  revue: "European Journal of Operational Research"   # "" si working paper
  reference: "361, 27–60"           # ou "arXiv:2608.04469"
  etat: "publie"                    # publie | accepte | soumis | working-paper
  etat_fr: "Publié"
  etat_en: "Published"
  axe: "credit"
  resume_fr: "…"
  resume_en: "…"
  note: "notes/ma-note.html"        # "" si pas de note
  note_titre_fr: "…"
  note_titre_en: "…"
  path: "https://…"                 # lien principal du titre
  liens:
    journal: "https://…"
    arxiv: "https://…"
```

Les clés de `liens` deviennent les libellés des boutons : écrire `arxiv`, `ssrn`,
`pdf`, `code`… donne un bouton portant ce nom.

### Écrire une note

Créer `fr/notes/ma-note.qmd`. L'en-tête suffit : la note apparaît d'elle-même
dans les Actualités, sur l'accueil, dans `/fr/notes/`, le flux RSS et la recherche.

```markdown
---
title: "Titre de la note"
subtitle: "Sous-titre en une ligne"
description: "Deux phrases — c'est ce qui s'affiche dans la liste."
date: 2026-09-08
author:
  - Prénom Nom
  - Autre Personne
categories: [Risque de crédit, Stress testing]
listing:
  - id: schema
    contents: ../../data/schemas.yml
    include:
      id: "mon-schema"
    template: ../../templates/fr/schema.ejs
---

::: {.standfirst}
[En bref]{.lede}
Le paragraphe d'ouverture.
:::

::: {.message}
[Message central]{.label}

L'argument en un paragraphe.
:::

## 1. Première section

Texte…

::: {.why}
[Pourquoi c'est important]{.label}

- **Un point.** Son explication.
- **Un autre.** Son explication.
:::

::: {#schema}
:::

::: {.retenir}
[À retenir pour chaque équipe]{.label}

- **Modélisation.** …
:::

{{< include ../_partenariat.qmd >}}
```

Le bloc `listing` de l'en-tête et le `::: {#schema}` du corps ne sont utiles que
s'il y a un schéma. Le paragraphe de partenariat est écrit une seule fois dans
`fr/_partenariat.qmd` — le modifier là le met à jour dans toutes les notes.

Équations : `$…$` dans le texte, `$$…$$` isolées. KaTeX est servi depuis le site.

### Ajouter un schéma d'architecture

`data/schemas.yml`. On décrit les étapes, **le dessin est calculé tout seul** :
positions, flèches, numéros, largeurs. Il n'y a jamais de SVG à écrire.

```yaml
- title: "Nom du schéma"
  id: "mon-schema"                  # repris dans l'en-tête de la note
  etapes:
    - titre: "PREMIÈRE BRIQUE"
      sous_titre: "ce qu'elle fait"
    - titre: "DEUXIÈME BRIQUE"
      sous_titre: "ce qu'elle fait"
  sorties:                          # facultatif
    - titre: "Sortie"
      sous_titre: "précision"
      queue: true                   # true = encadré ocre (mesure de queue)
  legende_fr: "La légende sous le schéma."
  legende_en: "The caption under the figure."
```

De 2 à 6 étapes passent bien. Sans `sorties`, le schéma est plus compact.

### Ajouter un axe de recherche

1. Ajouter un bloc dans `data/axes.yml`.
2. Créer `fr/recherche/<slug>.qmd` et `en/research/<slug>.qmd` — le plus simple
   est de copier une page d'axe existante et de remplacer `axe: "credit"` par le
   nouveau nom dans les deux blocs `listing`.

---

## 2. Changer l'apparence

### Couleurs et typographie

`assets/css/storm.scss`, bloc `:root` en haut du fichier. La palette vient des
notes techniques du collectif ; l'encre du logo est `#0a2d5a`.

| Variable | Valeur | Rôle |
|---|---|---|
| `--ink` | `#0a2d5a` | logo, titres |
| `--primary` | `#124489` | liens, filets, traits des schémas |
| `--primary-soft` | `#5a7daa` | texte secondaire |
| `--tint` | `#e9eff6` | fond des encadrés |
| `--signal` | `#bd8c42` | accent chaud — queues de distribution (aussi dans le fond animé) |
| `--bg` / `--surface` | `#f7f8fa` / `#ffffff` | fonds (`--bg` doit rester égal à `$body-bg`) |
| `--chart-1…4` | | séries de données |

Changer une valeur ici la change partout, **y compris dans les schémas**. Le site
est volontairement toujours clair (pas de mode sombre) : le fond animé est
dessiné pour un fond clair.

### Fond animé

`partials/after-body.html`, inséré sur toutes les pages. Des densités en
perspective dérivent lentement ; la zone au-delà du quantile à 95 % est ombrée
en or, avec un trait au quantile. Toutes les ~18 s, un épisode de stress balaie
la page : les densités s'élargissent, le quantile s'éloigne, la queue grossit.
Réglages en tête du script : `N` (nombre de lignes), `PERIOD` (durée du cycle),
`alpha` (intensité des traits), `GOLD` (couleur des queues). Le fond reste
immobile pour les visiteurs qui ont désactivé les animations.

`--signal` ne doit jamais servir à du texte : son contraste sur blanc est
insuffisant pour l'accessibilité. Filets, pastilles et marques de graphique
seulement.

### Forme des fiches

`templates/fr/` et `templates/en/` — un fichier par type de fiche :
`actualite`, `projet`, `publication`, `axe`, `note`, `schema`. Tous produisent
des « lignes » (`.item`) : titre, méta, flèche.

Deux règles à respecter :

1. **Le HTML est émis d'un bloc, dans un bloc ```` ```{=html} ````.** Sinon Pandoc
   le réinterprète et casse la mise en page. C'est pour cela que les gabarits
   construisent une chaîne `out` et l'émettent d'un coup.
2. **Une modification de forme se reporte dans les deux langues.** Les gabarits
   `fr/` et `en/` ne diffèrent que par les suffixes de champs (`resume_fr` vs
   `resume_en`) et les libellés.

### Navigation, pied de page, langues

`_quarto-fr.yml` et `_quarto-en.yml`. Les liens sont écrits en absolu
(`/fr/notes/`), ce qui suppose que le site est servi à la racine d'un domaine.
S'il devait vivre dans un sous-dossier, ces liens seraient à revoir.

`_quarto.yml` contient ce qui est commun aux deux éditions : thème, polices,
KaTeX, favicon.

---

## 3. Points d'attention

**Blocs imbriqués.** Un bloc `:::` qui en contient un autre doit avoir *plus* de
deux-points que celui qu'il contient :

```markdown
:::: {.exterieur}

::: {.interieur}
Texte
:::

::::
```

Laisser une ligne vide avant et après chaque `:::`.

**Fichier produit automatiquement.** `data/_notes.yml` est réécrit avant chaque rendu par `scripts/collect.py`. Il existe parce que
Quarto ne sait lire les en-têtes que des fichiers qu’il rend : sans lui, les
listes de l’édition anglaise sortiraient vides. Ne le modifiez jamais à la
main — modifiez la note concernée, il suivra.

**Adresses de contact et domaine.** `storm.example.org` et
`contact@storm.example.org` sont des valeurs d'attente, à remplacer dans
`_quarto-fr.yml`, `_quarto-en.yml`, `fr/a-propos/index.qmd` et
`en/about/index.qmd`.

**Notes en anglais.** Les quatre notes existent en français. Les pages anglaises
les listent en signalant la langue. Pour en traduire une : copier le `.qmd` dans
`en/notes/`, traduire, et retirer le renvoi vers l'édition française dans
`en/notes/index.qmd`.

---

## 4. Mettre en ligne

`docs/` est prêt pour GitHub Pages (branche `main`, dossier `/docs`).
`docs/index.html` redirige vers l'édition française.

Une seule subtilité de construction : Quarto ne sait pas écrire deux éditions
dans un même dossier de sortie — la seconde effacerait la première. Chaque
édition est donc rendue à part (`_site-fr`, `_site-en`), puis recopiée dans
`docs/` par `scripts/assemble.sh`, que Quarto appelle automatiquement après
chaque rendu (clé `post-render` de `_quarto.yml`). Vous n'avez jamais à lancer
ce script vous-même. `_site-fr/` et `_site-en/` sont des dossiers de travail,
ignorés par git.

Après avoir modifié `data/`, pensez à relancer **les deux** rendus si le
changement concerne les deux langues (actualités, projets, publications, axes).

Le site ne fait **aucune requête vers un tiers** au chargement : polices
(Source Serif 4, Source Sans 3, IBM Plex Mono) et KaTeX sont servis depuis
`assets/`. C'est voulu — cela évite la question du transfert de données
personnelles vers Google Fonts, et le site reste complet derrière le réseau
d'une banque.

---

## 5. Équipe (retirée)

Les pages membres ont été retirées du site lors de la refonte. Elles sont
conservées dans `_ancien/equipe-fr/` et `_ancien/team-en/` (Quarto ignore les
dossiers qui commencent par `_`). Une sauvegarde complète du site avant refonte
se trouve dans `../sauvegarde-avant-refonte.tar.gz`.
