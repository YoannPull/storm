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

### Projets internes

`data/projets.yml` n'est plus affiché sur le site (choix de la refonte : le site
reste général, les articles et les notes portent le détail). Le fichier est
conservé pour mémoire.

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

### Modifier l'expertise (méthodes et applications)

- **Page Expertise** : `fr/expertise/index.qmd` et `en/expertise/index.qmd`.
  Chaque méthode et chaque application y est un bloc court (titre + une
  phrase), avec un identifiant (`id="credit"`…) qui sert de lien.
- **Cartes et lignes de l'accueil** : `data/axes.yml` (`groupe: "methode"` ou
  `"application"`). Le champ `path` pointe vers la section de la page Expertise.

Les anciennes pages détaillées (une par axe) sont rangées dans
`_ancien/recherche-fr/` et `_ancien/research-en/`.

---

## 2. Changer l'apparence

### Couleurs et typographie

`assets/css/storm.scss`, bloc `:root` en haut du fichier. Le site est **noir**
(refonte 2026), avec un seul accent : le bleu STORM, éclairci pour rester lisible
sur noir. Le bas du fichier (« THÈME NOIR — ajustements ») contient les réglages
propres au thème noir et les styles des animations.

| Variable | Valeur | Rôle |
|---|---|---|
| `--ink` | `#ffffff` | titres |
| `--body` | `#c7ccd3` | texte courant |
| `--primary` | `#7aa9ff` | liens, petits libellés |
| `--signal` | `#4d8dff` | bleu STORM — queues, extrêmes, ruptures |
| `--tint` | `#0b1424` | fond des encadrés |
| `--bg` / `--surface` | `#000000` / `#0a0b0c` | fonds (`--bg` doit rester égal à `$body-bg`) |

Changer une valeur ici la change partout, y compris dans les schémas.

### Animations

Tout est dans `partials/after-body.html`, inséré sur toutes les pages.

- **Horizon de densité** (accueil) : une grande densité en poussière derrière
  le titre, la queue au-delà du quantile à 95 % en bleu. Elle ne s'affiche que
  sur une page qui contient un bloc `.home-hero`.
- **Animations de méthodes** : à placer dans n'importe quelle page avec

  ```markdown
  ::: {.storm-anim data-anim="credit"}

  :::
  ```

  `credit` = stress test de crédit (trois onglets), `rst` = reverse stress test
  (seuil → exploration → point de rupture → voisinage → sélection),
  `jeffreys` = test de calibration de Jeffreys, `eprocess` = surveillance en
  continu d'un modèle (e-processus). Les textes suivent la langue de la page.
  Les valeurs sont illustratives.
- Elles sont actuellement sur l'accueil et sur la page Expertise (sections
  « Stress testing » et « Validation et suivi des modèles », chacune avec son
  sélecteur), et dans les notes « Stress tests de crédit » et « Reverse stress
  testing ». Chacune démarre quand elle entre à l'écran.
- Un sélecteur (`.anim-switch`) pilote les animations de son bloc
  `.anim-group`.

Toutes les animations restent immobiles pour les visiteurs qui ont désactivé
les animations dans leur système.

### Forme des fiches

`templates/fr/` et `templates/en/` — un fichier par type de fiche :
`actualite`, `projet`, `publication`, `axe`, `note`, `schema`. Ils produisent
des « lignes » (`.item`) ; `axe` produit des cartes pour les méthodes.

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

**Adresses de contact et domaine.** Les contacts sont dans `fr/a-propos/index.qmd` et `en/about/index.qmd` (section « Travailler avec nous »). L'adresse du site (`site-url`, utilisée pour le flux RSS et le plan du site) est dans `_quarto-fr.yml` et `_quarto-en.yml` : `https://yoannpull.github.io/storm/`.

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
