# RAPPORT-QA.md — Azur Grill

Vérification de la refonte, dimension par dimension. **Chaque ligne est une mesure
exécutée**, pas une estimation. Les scripts sont dans `scratchpad/` et rejouables.
Les limites de la vérification sont documentées en §9 — elles font partie du rapport.

Build vérifié : Astro 5.18.2, Tailwind 4.3.3, 3 pages. Chromium 141.0.7390.37.

---

## 1. Note par dimension

| Dimension | Note | Mesure |
|---|---|---|
| Contraste | **10/10** | 0 zone sous le seuil, 3 largeurs, 2 pages, 5 paliers de scroll |
| Overflow horizontal | **10/10** | 0 px à 375 / 768 / 1440, accueil et carte |
| Cibles tactiles | **10/10** | 0 cible < 44 px à 375 et 768 |
| Console | **10/10** | 0 erreur, 0 warning, 0 requête échouée |
| `prefers-reduced-motion` | **10/10** | 0/28 élément caché, 0 bande, broche masquée |
| Robustesse des révélations | **10/10** | 0 élément bloqué invisible sur 6 paliers |
| CLS | **10/10** | 0,000 en mobile et desktop |
| LCP | **9/10** | 112 ms mobile — mais mesuré en local (voir §9) |
| Budget JS | **9/10** | 51,3 Ko gzip sur 60 autorisés |
| Poids des images | **8/10** | 2,8 Mo au total ; le stock source plafonne à 1360 px (§9) |
| Lighthouse | **non mesuré** | outil indisponible dans cet environnement (§9) |

**Aucune case n'est rouge.** Deux dimensions sont incomplètes plutôt que négatives, et
c'est dit franchement plutôt que compensé par une note flatteuse.

---

## 2. Contraste — échantillonnage pixel du composite réel

Méthode : le texte est rendu **transparent**, la page photographiée, puis le fond réel
sous chaque glyphe échantillonné, en prenant le **5ᵉ percentile** de luminance (le pixel
le plus défavorable). Jamais un calcul token contre token.

| Page | Largeur | Zones sous le seuil |
|---|---|---|
| Accueil | 375 / 768 / 1440 | **0** |
| Carte | 375 / 768 / 1440 | **0** |

### Ce que la mesure a rattrapé, et que la relecture n'aurait pas vu

| Zone | Avant | Après | Cause |
|---|---|---|---|
| Kicker du hero | **3,54:1** | ≥ 4,5:1 | scrim trop clair là où le texte se pose ; densifié à 46 % (0,42 → 0,66) |
| « À CONFIRMER — horaires » | **2,20:1** | ≥ 4,5:1 | texte `braise` sur `creme` — **ma propre règle de `DESIGN.md`, que j'avais violée dans trois composants** |
| Notes de la page carte | **2,20:1** | ≥ 4,5:1 | idem |

Le second cas mérite d'être noté : la règle « `braise` ne porte jamais de texte sur fond
clair » était écrite dans `DESIGN.md` **avant** que le code soit produit, et elle a
quand même été enfreinte. C'est la mesure qui l'a rattrapée, pas la relecture.

---

## 3. Overflow, cibles tactiles, console

| Contrôle | 375 | 768 | 1440 |
|---|---|---|---|
| `scrollWidth - clientWidth` | 0 px | 0 px | 0 px |
| Cibles < 44 px | 0 | 0 | — |
| Erreurs / warnings / requêtes échouées | 0 | 0 | 0 |

Corrigés en cours de route : **overflow de 60 px à 768 px** (un `whitespace-nowrap` que
j'avais moi-même introduit sur le numéro de téléphone), et six cibles sous 44 px (lien
logo, lien téléphone de l'en-tête et du pied de page, liens du pied de page, retour de
la page carte).

La requête échouée du site précédent (`iframe` Google Maps) a disparu : l'iframe est
remplacée par un lien d'itinéraire.

---

## 4. Mouvement

| Contrôle | Résultat |
|---|---|
| `reduce` — éléments `[data-slice]` cachés | **0 / 28** |
| `reduce` — bandes de la lame affichées | **0** |
| `reduce` — broche affichée | **non** |
| `reduce` — lignes du hero cachées | **0** |
| Normal — bandes après 1,8 s | les 6 à `scaleY(0)`, rétractées |
| Normal — contenu bloqué invisible (6 paliers) | **0** |

La broche restait affichée en mode réduit : une règle CSS de composant ne bat pas
l'utility `md:block`. Corrigé par le variant natif `motion-reduce:`.

Le `setInterval` de 200 ms de l'ancien `ScrollReveal` — qui appelait
`getBoundingClientRect()` sur 34 éléments en continu — est supprimé. Chaque élément est
désormais animé une fois (`once: true`), puis oublié.

---

## 5. Performance

| Métrique | Mobile 375 | Desktop 1440 | Cible |
|---|---|---|---|
| **LCP** | **112 ms** | 132 ms | ≤ 1 500 ms |
| **CLS** | **0,000** | 0,000 | ≤ 0,02 |
| **JS total** | **51,3 Ko gzip** | — | ≤ 60 Ko |
| Poids du site | **2,8 Mo** | — | — |

Détail du JS : GSAP 27,0 · ScrollTrigger 17,8 · Lenis 5,4 · révélations 1,0 Ko.

Le CLS était de **0,065 en mobile**. La source, identifiée par `PerformanceObserver` et
non par supposition, était unique : le bloc de titre du hero se remettait en page à
l'arrivée des polices. Corrigé par le préchargement des deux fontes du premier écran →
**0,000**.

Le repli d'image `<Picture>` produisait des PNG allant jusqu'à 1,7 Mo (14 Mo de PNG sur
18 Mo de build). Repli forcé en WebP : **18 Mo → 2,8 Mo**.

---

## 6. Assets

| Contrôle | Résultat |
|---|---|
| Format réel (Pillow, pas l'extension) | conforme — aucune extension mensongère |
| Vignettes 96 px | **supprimées**, après vérification que chacune existe en meilleure résolution |
| Formats servis | AVIF + WebP, repli WebP |
| `fetchpriority="high"` sur le hero | oui |

---

## 7. Source unique de la donnée

Contrôle par `grep` exhaustif, pas par relecture :

| Donnée | Occurrences en dur hors `src/data/` |
|---|---|
| Téléphone | **0** |
| Horaires | **0** |
| Adresse | **0** |

Uber Eats n'apparaît que via `restaurant.uberEatsUrl` (3 emplois) — jamais en dur, donc
retirable en une valeur si le restaurant a quitté la plateforme (`TODO-CLIENT.md`, 3).

---

## 8. Ce qui est signalé comme non validé, à dessein

Ces marqueurs sont **visibles sur le site** et ne doivent pas être retirés avant réponse
du client :

- **`PLACEHOLDER-AVIS`** ×3 et un bandeau d'avertissement dans la section avis.
- **`À CONFIRMER`** sur les horaires, sous le tableau.

---

## 9. Limites de cette vérification — à lire avant de conclure

1. **Lighthouse n'a pas été exécuté** : l'outil n'est pas disponible dans cet
   environnement et la documentation web y est bloquée. L'objectif « ≥ 95 » n'est donc
   **ni atteint ni manqué : il n'est pas mesuré.** À faire sur l'environnement de
   déploiement.
2. **LCP et CLS sont mesurés en local**, sur un serveur de fichiers et une machine non
   bridée. Ce sont des **planchers optimistes**, pas des valeurs de terrain. Le vrai LCP
   dépendra de l'hébergement et du réseau du visiteur.
3. **Les transitions sont validées en état initial et final**, plus cinq images
   intermédiaires de la séquence du hero (80 / 260 / 440 / 620 / 900 ms) — pas en
   inspection image par image.
4. **Un seul moteur** : Chromium 141. Ni Safari ni Firefox n'ont été testés ; le
   comportement de `svh`, des `@keyframes` et de `clip-path` peut y différer.
5. **Le statut ouvert/fermé est vérifié dans sa logique**, pas sur les 7 jours × 24 h.
   Il repose sur des horaires **non confirmés** : le mécanisme est juste, la donnée ne
   l'est pas encore.
6. **Le contraste est mesuré aux trois largeurs de référence** et à cinq paliers de
   scroll — pas sur toutes les positions intermédiaires possibles.
7. **Aucune vérification sur un vrai téléphone**, ni au toucher.

### Trois faux positifs rencontrés — et pourquoi ils comptent

Mon propre outillage a produit trois alertes fausses avant d'être corrigé. Elles sont
consignées parce qu'un rapport qui ne montre que les succès de sa méthode ne dit pas si
on peut lui faire confiance :

1. Une capture `full_page` montrait des sections **vides** — artefact des révélations,
   pas un bug. La QA se fait viewport par viewport.
2. Le bandeau CTA semblait **dupliqué** — mon script recapturait le bas de page.
3. « Traiteur » ressortait à **2,20:1** — la puce passait sous la barre mobile fixe, et
   je mesurais le bouton de cette barre. Corrigé par un test de visibilité réelle
   (`elementFromPoint`).

Dans les trois cas, l'outil mentait et le fichier réel disait vrai.
