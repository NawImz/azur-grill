# TODO-CLIENT.md — ce qu'il nous faut d'Azur Grill

Liste des informations et fichiers à obtenir du restaurant. Rien de ce qui suit ne sera
inventé : tant qu'un point n'est pas tranché, le site affiche un marqueur visible
(`À CONFIRMER`, `PLACEHOLDER-AVIS`) plutôt qu'une valeur plausible.

Classé par **coût d'un oubli**, pas par ordre d'importance ressentie.

---

## 🔴 Bloquant — une erreur ici fait perdre des clients

### 1. Les horaires exacts

Trois versions **contradictoires** circulent, dont une déjà en ligne sur le site :

| Source | Horaires |
|---|---|
| Fiche publique | lundi–vendredi **12h–22h30**, fermé le week-end |
| Réseaux du restaurant | lundi–samedi **11h30–23h**, fermé le dimanche |
| **Données du site actuel** | **7j/7 · 11h30–22h30** ← ne correspond à **aucune** des deux |

En attendant, le site affichera **lundi–samedi 11h30–23h, fermé le dimanche**, marqué
`À CONFIRMER`.

> **Pourquoi c'est le point n°1 :** le site calcule un statut **« ouvert / fermé
> maintenant »** en direct. Un horaire faux ne se contente pas d'être faux — il annonce
> « ouvert » à quelqu'un qui va trouver porte close, ou « fermé » à quelqu'un qui
> serait venu. C'est la seule erreur de cette liste qui coûte un client à chaque
> occurrence.

**Il nous faut :** les horaires réels, jour par jour, et l'éventuelle fermeture
hebdomadaire ou coupure méridienne.

### 2. Le nom exact du restaurant

Trois graphies coexistent : le **logo** affiche « AZUR RESTAURANT », le brief dit
« **Azur Grill** », les données du site disent « Azur Grill Restaurant ».

**Il nous faut :** la forme officielle, celle qui ira dans l'en-tête, le titre de la
page et les résultats Google.

### 3. Uber Eats : toujours d'actualité ?

Le site pousse aujourd'hui « **Commander sur Uber Eats** » comme bouton principal, vers
un lien enregistré. Si le restaurant a quitté la plateforme ou changé de prestataire,
ce bouton envoie les clients dans le vide.

**Il nous faut :** confirmation que le lien est actif, ou le nom du service utilisé
aujourd'hui (ou « aucun, on prend les commandes par téléphone »).

### 4. Réserver ou Commander ?

L'en-tête ne portera **qu'un seul** bouton — c'est ce qui lui donne sa force.

**Il nous faut le choix :** pousser la **réservation** sur place, ou la **commande** à
emporter / en livraison ? (Le second bouton restera disponible ailleurs sur la page.)

---

## 🟠 Important — le site fonctionne sans, mais il est moins convaincant

### 5. De vrais avis Google

Les trois avis actuellement affichés sont **des textes rédigés, pas des avis réels**.
L'un d'eux vante même des « portions généreuses » — or c'est le seul point qu'un avis
public a **critiqué**. Ils sont remplacés par des `PLACEHOLDER-AVIS` visibles.

**Il nous faut :** 3 à 4 avis authentiques copiés depuis la fiche Google du restaurant
(capture d'écran suffit), avec le prénom et la note. Directement depuis la fiche
Google — pas depuis un site d'agrégation.

### 6. Des photos en meilleure résolution

État réel du stock, après contrôle fichier par fichier :

| Ce qu'on a | Verdict |
|---|---|
| `assets/photos/` — **96 pixels de large** | inutilisables (vignettes) |
| `photos-enhanced/` — 640 px | dépannage mobile seulement |
| `photos-v2/` — jusqu'à 1360 px | **le seul jeu exploitable**, mais juste pour un grand écran |

**Il nous faut, par ordre d'utilité :**

- 🔥 **La broche qui tourne** — *aucune photo de la broche n'existe aujourd'hui*, alors
  que c'est **le geste sur lequel tout le site est construit** (l'animation signature
  reprend le mouvement de la lame qui tranche). C'est la photo manquante la plus
  importante.
- 🔥 **La sauce blanche maison** — citée dans presque tous les avis, absente du site.
- **L'équipe** — l'accueil est le deuxième argument du restaurant ; il n'y a
  aujourd'hui aucun visage sur le site.
- Les photos d'origine, **non redimensionnées**, sorties du téléphone (viser 2000 px de
  large minimum).

> Deux précisions utiles : la photo servant actuellement d'accueil montre **deux canettes
> Coca-Cola** au premier plan — une marque tierce très visible, qui n'aide ni l'image ni
> le propos « tout est fait ici ». Elle est remplacée par la photo des **pains sortis du
> four**. Et aucune image d'illustration achetée ou générée ne sera utilisée : uniquement
> de vraies photos du restaurant.

### 7. Le logo en fichier propre

Le seul logo disponible est **une affiche photographiée** (fond blanc incrusté, aucune
transparence) en 574 × 1020 px. L'autre fichier fait **96 × 121 px**. Ni l'un ni l'autre
ne peut être posé proprement dans un en-tête.

**Il nous faut :** le fichier d'origine du logo — idéalement vectoriel (`.ai`, `.eps`,
`.svg`, `.pdf`), sinon un PNG à fond transparent en grande taille. À défaut, nous le
redessinons, et il faut nous le dire.

### 8. La carte : à valider, pas à fournir

**Bonne nouvelle : la carte complète est déjà là** — 7 catégories, 50 plats, prix
détaillés. Elle n'est pas à refournir.

**Il nous faut seulement :** une relecture pour confirmer que **les prix sont à jour**,
et l'indication des **8 plats à mettre en avant** (à défaut, nous proposerons une
sélection appuyée sur les avis : döner, pain maison, künefe, côtelettes…).

---

## 🟡 À trancher — décisions, pas informations

### 9. Mentions légales

Obligatoires sur un site professionnel. **Il nous faut :** raison sociale, forme
juridique, SIRET, adresse du siège, nom du responsable de publication.

### 10. Mesure d'audience

Prévu : un outil **sans cookie** (Plausible ou Umami) — donc **aucun bandeau cookie** à
faire accepter aux visiteurs. C'est un gain de simplicité et de conversion. Ces outils
sont payants (quelques euros par mois) ; l'alternative est de ne rien mesurer du tout.

**Il nous faut :** l'accord du client, ou le choix de s'en passer.

### 11. Réseaux et contact

**Il nous faut :** confirmation du compte Instagram
(`@azurgrillrestaurant` est enregistré), l'existence d'un **WhatsApp** professionnel, et
d'une éventuelle page Facebook.

### 12. Adresse exacte sur le plan

Les coordonnées enregistrées sont marquées « approximatives, calculées depuis l'adresse
postale » dans les données. **Il nous faut :** valider que le lien-plan tombe bien sur la
devanture, en l'ouvrant une fois depuis un téléphone.

---

## Ce qui n'est **pas** demandé au client

Pour éviter les allers-retours inutiles : nous n'avons besoin d'aucun texte rédigé,
d'aucun slogan, d'aucune traduction. Les textes du site sont écrits à partir des avis
réels et des faits ci-dessus, puis soumis à validation.
