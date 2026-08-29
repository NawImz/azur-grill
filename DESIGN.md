# DESIGN.md — Azur Grill

Système de design de la refonte. Chaque valeur ci-dessous est **mesurée**, pas estimée
à l'œil : les scripts de mesure sont ceux décrits dans `SETUP.md` §7. Rien n'est hérité
d'une session antérieure.

---

## 1. Diagnostic du site actuel — la mesure, pas l'impression

Le brief soupçonne le site existant d'être près du premier look « AI-slop »
(crème dominante + serif à fort contraste + accent terracotta). **Vérifié, c'est le cas
sur les trois axes :**

| Axe | Valeur mesurée dans le dépôt | Verdict |
|---|---|---|
| Fond dominant | `creme #FAF8F4` — hue 40°, sat 37,5 %, lum 96,9 % | **beige chaud dominant** ; la référence AI-slop est `#F4F1EA` (hue 42°) — pratiquement le même point |
| Display | **Fraunces** — serif à très fort contraste | l'ingrédient n°2 du cliché, **et** il duelle avec le wordmark serif du logo (§4.13) |
| Accent | `brique #A6532F` — **hue 18,2°, sat 55,9 %** | **en pleine zone terracotta** (10–28° / sat < 75 %) ; à comparer au `#D97757` d'Anthropic : hue 14,8° |

**Défaut supplémentaire, indépendant du style et plus grave :** `brique` sert de fond aux
boutons « Commander » posés sur les bandes bleues. Contraste mesuré **`#A6532F`
contre `#16098F` = 2,65:1** — sous le seuil **3:1** exigé pour qu'un composant
d'interface soit distinguable de son fond. Cette couleur échoue donc **deux fois** :
esthétiquement (zone interdite) et sur l'accessibilité (WCAG 2.2 AA, composants).
Elle est **supprimée**, pas retouchée.

---

## 2. Palette — cinq valeurs

Les deux bleus ne sont pas des choix : ce sont les valeurs **exactes** du logo, obtenues
par comptage de pixels (`#16098F` couvre 13,1 % de l'image, `#74C0EC` 5,9 %). Elles sont
**verrouillées**.

| Token | Hex | Rôle | Mesures |
|---|---|---|---|
| `nazar` | **`#16098F`** | **Couleur structurante et dominante.** Fonds de section, en-tête, larges aplats. | hue 245,8° · sat 88,2 % · lum 29,8 % |
| `ciel` | **`#74C0EC`** | Accents sur fond bleu, liens, kickers, le nazar décoratif. | **7,14:1 sur `nazar`** — AA texte courant |
| `braise` | **`#FA8B0C`** | Accent chaud unique : appels à l'action, prix mis en avant, la lueur au survol. | hue **32,0°** · sat **96,0 %** · **5,96:1 sur `nazar`** |
| `creme` | **`#F7F5F1`** | **Secondaire** : cartes, surfaces de respiration, texte sur bleu. Jamais le fond général du site. | **13,12:1 avec `nazar`** |
| `encre` | **`#1A1626`** | Texte courant sur surfaces claires. | **16,25:1 sur `creme`** |

### Pourquoi `#FA8B0C` et pas une autre chaude

Sept candidats ont été mesurés contre deux critères durs — sortir de la zone terracotta
(**hue ≥ 28°** *et* **sat ≥ 85 %**) et rester lisible sur le bleu dominant (**≥ 4,5:1**) :

| Candidat | hue | sat | / `nazar` | Verdict |
|---|---|---|---|---|
| `#D97757` (référence AI-slop) | 14,8° | 63,1 % | 4,58 | **rejeté** — zone terracotta |
| `#A6532F` (`brique` actuel) | 18,2° | 55,9 % | **2,65** | **rejeté** — zone terracotta **et** échec AA |
| `#EF7215` | 25,6° | 87,2 % | 4,82 | rejeté — hue encore dans la zone |
| `#F58220` | 27,6° | 91,4 % | 5,51 | limite basse |
| **`#FA8B0C`** | **32,0°** | **96,0 %** | **5,96** | **retenu** |
| `#F5A524` | 37,0° | 91,3 % | 7,00 | lit « or / moutarde » plus que « braise » |

`#FA8B0C` est le point qui s'éloigne franchement de l'argile **sans** basculer dans le
doré : une saturation de 96 % rend la lecture « terre cuite » impossible, et à hue 32° la
couleur reste une flamme, pas un métal.

> **Garde-fou d'emploi.** `braise` sur `creme` ne donne que **2,20:1** : il ne doit
> **jamais** porter du texte sur fond clair. Il est réservé aux fonds bleus et aux
> surfaces pleines — `encre` sur `braise` donne **7,38:1**, largement AA. À vérifier au `grep` avant livraison.

### La crème : légèrement refroidie, et reléguée

Le fond réel du logo est un blanc **froid** (`#FCFEFE`), pas un beige. La crème du dépôt
(`#FAF8F4`, sat 37,5 %) est à un cheveu de la référence AI-slop. Elle est donc désaturée
vers **`#F7F5F1`** — encore perceptiblement crème, mais sortie du beige marqué.

Le levier décisif n'est cependant pas la nuance, c'est la **surface** : le brief impose
que le bleu profond soit dominant. La crème passe de fond général à surface secondaire.
Cible : **≥ 60 % de la hauteur de page en `nazar`**, à mesurer sur la page construite
(échantillonnage de la colonne centrale), pas à l'estime.

---

## 3. Typographie

### Le logo décide à notre place

Le wordmark « AZUR RESTAURANT » est déjà composé dans **un serif à très fort contraste**
(type Didot). Reprendre un serif de la même famille pour le display du site, c'est
mettre deux voix identiques en concurrence — l'erreur §4.13. Le brief interdit par
ailleurs le serif contrasté comme ingrédient du cliché. Les deux raisons convergent :
**le display du site ne sera pas un serif.**

| Rôle | Police | Vérifiée sur npm | Justification |
|---|---|---|---|
| **Display** | **Zilla Slab** | `@fontsource/zilla-slab@5.3.0` | Un slab à empattements francs et **terminaisons chaleureuses** — exactement ce que demande le brief. Présence d'enseigne, lisible en très grand, et une voix **franchement autre** que le Didot du logo : les deux coexistent au lieu de se disputer. |
| **Corps** | **Manrope** | `@fontsource-variable/manrope@5.3.0` | Déjà au projet, neutre, excellente en petit corps. Une seule police de corps, comme demandé. |
| **Prix** | **Zilla Slab**, chiffres tabulaires | — | Pas de troisième police technique : un menu n'est pas un relevé de diagnostic. Les prix restent dans la voix d'affichage, alignés en `tabular-nums`. |

Échelle : conservée de la config actuelle (elle est saine), avec les interlignages
resserrés sur les grandes tailles (1,02–1,1) et ouverts sur le corps (1,6).

---

## 4. Structure — une page, six respirations

| # | Section | Fond | Ce qui doit être vrai |
|---|---|---|---|
| 1 | **En-tête** | `nazar` | Logo, téléphone cliquable, **un** bouton unique. *(Réserver ou Commander : à trancher avec le client — voir `TODO-CLIENT.md`.)* |
| 2 | **Hero** | photo + scrim | La promesse en une phrase. Séquence en tranches (§5). |
| 3 | **La carte** | `creme` sur `nazar` | **6 à 8 plats signature, prix visibles sans un clic.** Lien vers la carte complète. |
| 4 | **Ce qu'on dit de nous** | `nazar` | 4,6/5, avis **réels**, lien vers la fiche Google. |
| 5 | **Le lieu** | `nazar` | Intérieur, devanture, équipe. Traits d'ambiance réels. |
| 6 | **Infos pratiques** | `creme` | Adresse, **plan cliquable** (jamais d'iframe), **statut ouvert/fermé en direct**, téléphone. |

Pied de page minimal : mentions légales, réseaux. Rien d'autre.

**Change majeur imposé par le diagnostic :** la carte quitte les `<details>` fermés.
Huit plats signature en clair, la carte complète (50 plats) derrière un lien assumé.

Espacement : 80 px mobile / 120 px desktop entre sections.

---

## 5. L'animation signature — la broche et la lame

**Une seule idée, menée jusqu'au bout.** Elle vient du geste le plus reconnaissable du
métier : la broche tourne, la lame en tranche de fines lamelles.

### 5.1 À l'arrivée — la coupe

Le hero se révèle par **six bandes verticales** qui se rétractent en séquence rapide,
de gauche à droite, comme une lame qui vient de passer. Une silhouette de broche au
trait, dans le style du logo, tourne **une fois** pendant la séquence, puis disparaît.

| Paramètre | Valeur | Raison |
|---|---|---|
| Bandes | **6** | Assez pour lire « tranches », assez peu pour rester net (le brief autorise 5 à 8). |
| Durée totale | **≤ 900 ms**, décalage 55 ms par bande | Contrainte du brief. Ne se rejoue jamais. |
| Courbe | `cubic-bezier(.22, 1.12, .36, 1)` — **léger dépassement** | Un `ease-out` plat lit « fondu » ; le léger dépassement lit **un geste sûr**, jamais hésitant. |
| Broche | rotation unique, opacité 0 en fin | Un repère narratif, pas une boucle décorative. |

**Photo du hero : `about-pain-maison.webp`.** Trois raisons, dans l'ordre :
1. Elle **est** la promesse — le pain est l'un des trois noms du titre.
2. Elle ne contient **aucun élément typographique**, donc aucun duel avec le titre
   (§4.13). C'est ce qui la fait préférer à `gallery-devanture.webp`, dont l'enseigne au
   néon porte déjà « AZUR RESTAURANT » en gros — cette photo ira en section « Le lieu ».
3. L'alignement répété des pains crée un **rythme horizontal** que les tranches
   verticales viennent épouser : la forme de l'animation rime avec le contenu de l'image.

> ⚠️ **À mesurer à l'assemblage, pas à supposer.** Le haut de cette photo est un
> carrelage **très clair** ; un texte crème y échouerait. Le scrim sera **asymétrique**
> (dense là où le titre se pose, transparent là où les pains respirent) et son opacité
> sera fixée **par échantillonnage pixel du composite réel**, pas par une valeur choisie
> au jugé (§4.10 et §4.11). Le tiers inférieur (sacs, cagettes) est à recadrer.

### 5.2 Au scroll — la même lame, en plus discret

La logique de tranches devient la transition d'entrée de section : **2 à 3 bandes**,
même sens, même courbe. C'est ce qui donne au site sa signature reconnaissable sans
rejouer le geste complet à chaque fois.

> ⚠️ **Piège technique à ne pas rejouer (§4.7).** Le `clip-path` de révélation doit être
> porté par **un enfant** (l'`<img>`, un `<span>` interne), **jamais par l'élément
> observé** par ScrollTrigger : Chromium calcule l'intersection après le clip, donc
> `isIntersecting` reste `false` pour toujours — blocage silencieux, sans erreur console.

### 5.3 Deux motifs secondaires — et rien d'autre

- **Section avis** : le nazar boncuğu pulse **une fois**, doucement, à l'entrée dans le
  viewport. Un œil protecteur qui veille sur la réputation du lieu.
- **Survol d'un plat** : une lueur `braise` discrète sous le prix, comme un reflet de
  braise. **Restreinte à cette seule interaction.**

### 5.4 Le registre « artisan » — matière et gestes

Le mouvement seul ne fait pas une atmosphère : une section d'un aplat parfaitement
uni lit comme un calque d'écran, quelle que soit l'animation posée dessus. Trois
leviers, tous dérivés du même geste :

| Levier | Ce qu'il fait | Où |
|---|---|---|
| **Grain de papier** | un bruit fractal en SVG inline, en `multiply` sur les surfaces claires et en `overlay` sur le bleu — c'est ce qui sépare le papier du calque | toutes les sections |
| **Le trait qui se tire** | la ligne pointillée entre le plat et le prix se dessine de gauche à droite, puis le montant se pose — le geste de la carte écrite à la main | la carte |
| **Le cadre qui respire** | chaque photo est rognée par un cadre ; au survol elle s'agrandit lentement à l'intérieur, avec un voile de braise qui monte | le lieu |

S'y ajoutent, dans le même esprit de retenue : le filet `braise` qui se tire sous
chaque intitulé de section, les étoiles d'un avis qui s'allument l'une après
l'autre, le chiffre de la note qui se pose depuis le bas, et une respiration de
26 s sur la photo du hero — **une seule passe, jamais une boucle**.

Les ombres sont teintées de braise (`--ombre-posee`, `--ombre-levee`) et jamais
noires : une ombre neutre sur une palette chaude a l'air d'un calque, pas d'une
lumière.

### 5.5 Exclu

Particules, curseur personnalisé, parallaxe généralisé, et **toute animation qui boucle
sans avoir été déclenchée** par le scroll ou une interaction.

> **À supprimer en priorité :** le `setInterval` de 200 ms de `ScrollReveal.astro`, qui
> appelle `getBoundingClientRect()` sur 34 éléments en continu (`SETUP.md` §6). Il masque
> un défaut de synchronisation au lieu de le corriger, et rend l'objectif Lighthouse ≥ 95
> inatteignable.

### 5.6 Plancher d'accessibilité

`prefers-reduced-motion: reduce` **coupe tout** : hero directement dans son état final,
sans tranches ni broche. Toutes les animations en `transform` / `opacity` uniquement —
aucune ne bloque l'interaction ni ne décale la mise en page.

---

## 6. Budget — à mesurer, pas à espérer

| Cible | Valeur | Comment elle sera vérifiée |
|---|---|---|
| Lighthouse mobile | ≥ 95 | audit sur le build |
| LCP | ≤ 1,5 s | `fetchpriority="high"` sur l'image du hero ⚠️ **la séquence de tranches ne doit pas retarder la peinture de l'image** — à contrôler, un clip peut déplacer le LCP |
| CLS | ≤ 0,02 | dimensions explicites sur toutes les images |
| JS total | ≤ 60 Ko gzip | GSAP + ScrollTrigger importés **dynamiquement**, Lenis en lerp modéré |
| Images | AVIF + WebP | le jeu `photos-v2` est le seul exploitable (`SETUP.md` §5) |

---

## 7. Ce qui reste à trancher avant l'assemblage

1. **Opacité et forme exactes du scrim du hero** — par mesure sur le composite réel.
2. **Recadrage du hero** — écarter le tiers inférieur encombré ; un crop mobile dédié
   si le cadrage `cover` coupe mal.
3. **Traitement du logo** — l'actif est une affiche photographiée sans canal alpha
   (`SETUP.md` §5). Détourage ou revectorisation du wordmark nécessaire pour l'en-tête.
4. **Bouton unique de l'en-tête** : « Réserver » ou « Commander » — décision client.
