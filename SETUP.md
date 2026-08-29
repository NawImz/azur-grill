# SETUP.md — État vérifié de l'environnement

Relevé fait au début de la session de refonte. **Tout ce qui suit a été exécuté et
observé**, pas supposé. Les points marqués « limite » sont des contraintes réelles
de cet environnement, à connaître avant de promettre quoi que ce soit.

## 1. Environnement d'exécution

| Élément | État vérifié | Commande |
|---|---|---|
| OS | Linux 6.18, conteneur éphémère distant | `uname` |
| Node | v22.22.2 | `node --version` |
| npm | 10.9.7 | `npm --version` |
| Python | 3.11.15 | `python3 --version` |
| Pillow | 12.3.0 — **installé par cette session** | `pip install Pillow` |
| Playwright (Python) | 1.x — **installé par cette session** | `pip install playwright` |
| Chromium | 141.0.7390.37, préinstallé | lancé et piloté avec succès |

> **Le conteneur est éphémère.** Rien n'est conservé hors de ce qui est committé et
> poussé. `node_modules/`, Pillow et Playwright seront à réinstaller à la session
> suivante.

### Playwright : le piège de version

`pip install playwright` installe un client qui attend le build Chromium **1234** ;
l'image fournit le build **1194**. Un `p.chromium.launch()` nu échoue donc avec
`Executable doesn't exist…`. **Ne pas lancer `playwright install`** (interdit dans cet
environnement et inutile). La forme qui marche, vérifiée :

```python
p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
```

## 2. Skills et plugins réellement disponibles

Le `CLAUDE.md` hérité nommait cinq skills. **Aucune n'existe dans cet environnement** —
vérifié via l'inventaire des skills activées et des plugins (liste de plugins vide) :

| Skill citée par la méthode | État réel | Substitut retenu |
|---|---|---|
| `impeccable` | **absente** | Passe de polish menue à la main, grille du §4 de `CLAUDE.md` appliquée point par point |
| `emil-design-eng` | **absente** | Chaque animation justifiée par écrit dans `DESIGN.md` (rôle narratif, durée, easing) |
| `ui-ux-pro-max` | **absente** | Décisions de palette/typo tranchées par **mesure** (voir §4) et consignées dans `DESIGN.md` |
| `webapp-testing` | **absente** | Pipeline Playwright autogéré — `scratchpad/shoot.py`, déjà écrit et fonctionnel |
| `find-skills` | **absente** | — |

Skills réellement présentes et pertinentes : `code-review`, `simplify`,
`security-review`, `run`, `artifact-design`. Le fichier `SKILL.md` à la racine du dépôt
est une copie de la skill Anthropic **`frontend-design`** : c'est la source de la liste
des trois looks « AI-slop » que le brief de refonte cite (dont le crème + serif
contrasté + terracotta ~#D97757). Il est conservé comme référence de direction
artistique.

**Conséquence à assumer franchement : aucune skill de design n'a été invoquée, parce
qu'aucune n'est installée.** Le niveau d'exigence qu'elles décrivent est appliqué à la
main, avec les moyens vérifiés ci-dessus.

## 3. Documentation en ligne — limite réelle

| Source | HTTP | Conséquence |
|---|---|---|
| `docs.astro.build` | **000** (bloqué) | inaccessible |
| `tailwindcss.com/docs` | **000** (bloqué) | inaccessible |
| `gsap.com/docs` | **000** (bloqué) | inaccessible |
| registre **npm** | OK | versions et paquets vérifiables |

La politique réseau de l'environnement bloque la documentation web. **Aucune API ne
sera donc écrite « de mémoire » sans contrôle** : la vérification se fera contre les
paquets réellement installés dans `node_modules/` (types TypeScript, README, dist).
C'est plus lent que la doc en ligne, mais c'est une source de vérité, pas un souvenir.

## 4. État réel du projet

### Stack installée (versions constatées, pas celles espérées)

| Paquet | Installé | Cible du brief | Écart |
|---|---|---|---|
| `astro` | **5.18.2** | Astro 5 | conforme |
| `tailwindcss` | **3.4.19** | **Tailwind v4** (`@theme`) | **migration nécessaire** |
| `@astrojs/tailwind` | 5.1.5 | — | à **retirer** (intégration v3 ; v4 passe par `@tailwindcss/vite`) |
| `gsap` | 3.15.0 | GSAP + ScrollTrigger | conforme |
| `lenis` | 1.3.25 | Lenis | conforme |

`tailwindcss@4.3.3` et `@tailwindcss/vite@4.3.3` sont disponibles sur npm (vérifié).

`npm install` puis `npx astro build` : **build vert**, 2 pages, 11 images optimisées.

### Polices — disponibilité vérifiée sur npm

`@fontsource/zilla-slab@5.3.0`, `@fontsource-variable/bricolage-grotesque@5.3.0`,
`@fontsource-variable/manrope@5.3.0`, `@fontsource-variable/outfit@5.3.0` — toutes
présentes. Le choix retenu est argumenté dans `DESIGN.md`.

## 5. Assets — format réel, pas l'extension

Contrôle systématique via Pillow (leçon §4.4 de `CLAUDE.md`). Aucune extension
mensongère détectée, mais **un problème de résolution bien plus grave** :

| Dossier | Contenu réel | Verdict |
|---|---|---|
| `assets/photos/` + `src/assets/photos/` | JPEG **96 px de large** (96×161, 96×69…) | **vignettes inutilisables** — doublon mort à supprimer |
| `src/assets/photos-enhanced/` | JPEG progressifs 640 px de large | dépannage mobile seulement |
| `src/assets/photos-v2/` | WEBP/JPEG, **jusqu'à 1360×1020** | **seul jeu exploitable** (1,9 Mo) |

`src/assets/photos-v2/logo-officiel.webp` — 574×1020, **mode RGB, sans canal alpha** :
ce n'est pas un logo détouré mais **une affiche photographiée** (wordmark « AZUR
RESTAURANT » en serif à fort contraste, entouré de nazars sur fond blanc). Un détourage
ou une revectorisation sera nécessaire pour l'utiliser en en-tête. `assets/photos/logo.png`
fait **96×121** — inutilisable.

### Couleurs de marque — échantillonnées, pas devinées

Comptage exact des pixels de `logo-officiel.webp` :

| Rôle | Hex | Part de l'image | Statut |
|---|---|---|---|
| Bleu nazar | **`#16098F`** | 13,1 % | **verrouillé** — valeur exacte du logo |
| Bleu ciel | **`#74C0EC`** | 5,9 % | **verrouillé** — valeur exacte du logo |
| Fond | `#FCFEFE` | 48,4 % | blanc **froid**, pas un crème chaud |
| Noir | `#170C14` / `#000000` | 2,3 % | pupilles |

Les valeurs `nazar` et `ciel` du `tailwind.config.mjs` hérité sont donc **exactes** et
sont conservées. En revanche `brique #A6532F` et `moutarde #D9A23E` sont des ajouts
sans fondement dans le logo — voir le verdict mesuré dans `DESIGN.md`.

## 6. État du site existant — mesuré

Build servi localement et piloté sous Chromium :

- **Overflow horizontal : 0 px** à 375 et 1440. Conforme.
- **Console : une requête échouée** — l'`iframe` Google Maps (`output=embed`). Le brief
  proscrit l'iframe intégrée ; elle sera remplacée par un lien-plan cliquable.
- **Reveals au scroll : aucun élément bloqué invisible.** 34 éléments `[data-reveal]`
  testés à six paliers de scroll, en `no-preference` **et** en `reduce` : 0 invisible
  dans le viewport à chaque palier.

> **Deux faux positifs évités, à retenir pour la QA.**
> 1. Une capture `full_page` de ce site montre des sections **vides** : les éléments hors
>    viewport sont volontairement à `opacity: 0` et le `toggleActions: play reverse` les
>    y ramène. Ce n'est **pas** un bug du site — c'est un artefact de la capture. Toute QA
>    visuelle doit se faire **viewport par viewport**, jamais en `full_page`.
> 2. Le bandeau « Une petite faim ? » semblait dupliqué sur la planche assemblée :
>    `grep` sur le HTML construit en donne **une seule occurrence**. C'était mon script
>    qui recapturait le même écran une fois le bas de page atteint (scroll non borné).
>
> Dans les deux cas, l'outil mentait et le fichier réel disait vrai (§4.2 de `CLAUDE.md`).

### Dette réelle constatée dans le code

- `src/components/ScrollReveal.astro` porte un **`setInterval` de 200 ms** qui appelle
  `getBoundingClientRect()` sur les 34 éléments en boucle, indéfiniment. C'est un
  « filet de sécurité » qui masque un problème de synchronisation au lieu de le
  corriger, et un layout-thrashing permanent — incompatible avec l'objectif
  Lighthouse ≥ 95.
- `src/components/Menu.astro` rend la carte en `<details>` **fermés par défaut** :
  au chargement, la section carte n'affiche **aucun plat et aucun prix**, seulement sept
  intitulés de catégorie. Pour un site destiné à être montré trente secondes sur un
  téléphone, c'est le défaut le plus coûteux du site actuel.

## 7. Outillage QA écrit dans cette session

- `scratchpad/shoot.py` — `ThreadingHTTPServer` éphémère + Chromium : largeur, hauteur,
  section, clic, `--reduced-motion`, relevé de l'overflow et des erreurs console.
- `scratchpad/shoot-sections.py` — planche-contact **viewport par viewport** (le seul
  mode de capture fiable ici, voir §6).
- `scratchpad/diag-reveal.py` — contrôle qu'aucun élément animé ne reste invisible.
- `scratchpad/qa.py` — **reste à écrire** : contraste par échantillonnage pixel
  (round-trip canvas pour les fonds unis, texte rendu transparent + `Range.getClientRects()`
  pour les composites), cibles tactiles, console. À produire avant toute livraison.
