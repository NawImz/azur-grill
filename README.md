# Azur Grill — site vitrine

Site une page du restaurant **Azur Grill**, 69 boulevard Foch, 93800 Épinay-sur-Seine.
Cuisine turque halal. Astro 5 + Tailwind v4 + GSAP + Lenis.

**Préversion en ligne : https://nawimz.github.io/azur-grill/**

> Préversion publique de travail, pas l'adresse définitive. Le jour où le
> restaurant prend son domaine, seules les variables `SITE_URL` et `BASE_PATH`
> du build changent — les liens internes passent par `src/lib/url.ts` et
> suivent automatiquement.

---

## Ce que ce site fait de différent

*Les trente secondes, face à un prospect. Chaque point est visible à l'écran, pas
seulement vrai dans le code.*

**1. On sait si c'est ouvert, maintenant.**
Pas un tableau d'horaires à déchiffrer : un statut calculé en direct — « Ouvert jusqu'à
23h00 », « Fermé — ouvre à 11h30 ». Et il est calculé **à l'heure de Paris**, jamais à
celle du téléphone du visiteur : sans cela, un client en voyage lirait « ouvert » à tort.

**2. On appelle en un geste.**
Le numéro est un lien `tel:` dans l'en-tête, dans les infos pratiques, et dans une barre
fixe toujours présente en bas de l'écran mobile. Jamais une image, jamais à recopier.

**3. Les prix sont visibles sans cliquer.**
Huit plats signature avec leur prix, en clair, dès la section carte. La carte complète —
50 plats — est à un lien. *(La version précédente cachait tout derrière sept accordéons
fermés : il fallait sept clics pour voir un seul prix.)*

**4. Les avis sont vérifiables.**
La note, des extraits, et un lien vers la fiche Google. Ce qui n'est pas encore
authentifié est marqué `PLACEHOLDER` **à l'écran** — le site ne prétend jamais qu'un
texte rédigé est un avis client.

**5. Le plan s'ouvre dans l'application de navigation.**
Un lien d'itinéraire, pas une carte intégrée : une iframe Google Maps pèse plusieurs
centaines de kilo-octets et échouait déjà en console sur la version précédente.

**6. Aucun bandeau cookie.**
La mesure d'audience prévue est sans cookie — donc rien à faire accepter au visiteur.
Un obstacle de moins entre lui et le numéro de téléphone.

**7. Une signature visuelle qu'on ne voit pas ailleurs.**
À l'arrivée, la page se révèle par six bandes verticales qui se rétractent de gauche à
droite, comme une lame qui vient de trancher la broche — le geste du métier, pas un
effet de catalogue. Moins de 900 ms, jamais rejoué. La même coupe, en plus discret,
introduit chaque section. Et tout disparaît si le visiteur a demandé moins d'animations.

**8. Ça se charge tout de suite.**
51 Ko de JavaScript, 0,000 de décalage de mise en page, images en AVIF et WebP. La
séquence d'entrée est en CSS pur : le premier écran ne dépend d'aucun script.

---

## Démarrer

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # -> dist/
```

## Structure

```
src/
  data/          restaurant.json · menu.json · horaires.json  <- source unique
  components/    Header Hero Menu Reviews Lieu PracticalInfo Footer
                 SliceReveal (révélations) · Broche · NazarMark
  pages/         index.astro · carte.astro · 404.astro
  styles/        global.css   <- tokens @theme (palette, typo, courbe)
```

**Une donnée, un endroit.** Téléphone, horaires, adresse et carte vivent dans
`src/data/`. Vérifié par `grep` : zéro occurrence en dur ailleurs. Changer un horaire,
c'est éditer une ligne de JSON.

## Documents du projet

| Fichier | Contenu |
|---|---|
| `CLAUDE.md` | La méthode de travail, et son adaptation à ce dépôt |
| `SETUP.md` | État vérifié de l'environnement, et ses limites |
| `PRODUCT.md` | Public, promesse, registre, anti-références |
| `DESIGN.md` | Palette et typographie, tranchées par mesure |
| `TODO-CLIENT.md` | **Ce qu'il reste à obtenir du restaurant** |
| `RAPPORT-QA.md` | Vérification chiffrée, et ce qui n'a pas été vérifié |

## Avant la mise en ligne

Le site est complet et vérifié, mais **trois points attendent le restaurant** — les
détails sont dans `TODO-CLIENT.md` :

1. **Les horaires exacts** — trois sources se contredisent. C'est la seule erreur qui
   coûte un client à chaque fois qu'elle se produit.
2. **De vrais avis Google** — les emplacements sont marqués sur le site.
3. **Le lien de commande** — à confirmer comme actif.

## Déploiement

Chaque poussée déclenche `.github/workflows/pages.yml`, qui construit le site et
le publie sur GitHub Pages. Le build reçoit deux variables :

| Variable | Préversion Pages | Domaine définitif |
|---|---|---|
| `SITE_URL` | `https://nawimz.github.io` | le domaine du restaurant |
| `BASE_PATH` | `/azur-grill` | *(vide)* |

Rien d'autre ne distingue les deux destinations.
