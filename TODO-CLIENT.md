# TODO-CLIENT.md — tout ce qui manque

Inventaire établi par scan du code et des données, pas de mémoire. Rien de ce qui
suit n'est inventé sur le site : tant qu'un point n'est pas tranché, un marqueur
visible (`À CONFIRMER`, `PLACEHOLDER`) le signale à l'écran.

Classé par **coût d'un oubli**, pas par ordre d'importance ressentie.

---

## 🔴 Ce qui coûte un client à chaque fois

### 1. Les horaires exacts

Trois versions contradictoires circulent, dont une encore dans les données :

| Source | Horaires |
|---|---|
| Fiche publique | lundi–vendredi **12h–22h30**, fermé le week-end |
| Réseaux du restaurant | lundi–samedi **11h30–23h**, fermé le dimanche |
| Données avant correction | 7j/7 · 11h30–22h30 ← ne correspondait à **aucune** des deux |

Valeur provisoire affichée : **lundi–samedi 11h30–23h, fermé le dimanche**, marquée
`À CONFIRMER` sous le tableau.

> **Pourquoi c'est le point n°1 :** le site calcule un statut **« ouvert / fermé
> maintenant »** en direct, à l'heure de Paris. Un horaire faux n'est pas seulement
> faux — il annonce « ouvert » à quelqu'un qui va trouver porte close. C'est la
> seule erreur de cette liste qui coûte un client à chaque occurrence.

**Il nous faut :** les horaires réels jour par jour, et l'éventuelle coupure entre
le service du midi et celui du soir.

### 2. Le lien de commande

Le bouton principal du site — en-tête, hero, infos pratiques — pointe vers un lien
Uber Eats enregistré dont **l'activité n'a pas été vérifiée**. S'il est mort, chaque
clic sur le bouton le plus visible du site part dans le vide.

**Il nous faut :** confirmation que le lien fonctionne, ou le nom du service utilisé
aujourd'hui, ou « aucun, uniquement par téléphone ». *(Le lien n'existe qu'à un seul
endroit dans les données : le changer est une ligne.)*

### 3. Le nom officiel

Trois graphies coexistent : le **logo** affiche « AZUR RESTAURANT » — c'est celle
retenue partout sur le site depuis votre validation — le brief disait « Azur Grill »,
et les données portent encore « Azur Grill Restaurant » comme nom complet.

**Il nous faut :** la forme officielle, celle qui ira dans les résultats Google et
sur la fiche.

---

## 🟠 Ce qui empêche de convaincre

### 4. De vrais avis Google

Les trois avis affichés sont des **`PLACEHOLDER` visibles**, avec un bandeau
d'avertissement. Les textes qui figuraient avant n'étaient pas des avis réels : l'un
vantait même des « portions généreuses », or c'est le seul point qu'un avis public
ait critiqué.

**Il nous faut :** 3 à 4 avis authentiques copiés depuis la fiche Google (une capture
d'écran suffit), avec le prénom et la note. Depuis la fiche Google elle-même, pas
depuis un site d'agrégation.

### 5. Les photos manquantes

Trois sujets absents, par ordre d'utilité :

- 🔥 **La broche qui tourne.** *Aucune photo n'existe*, alors que c'est le geste sur
  lequel **tout le site est construit** — l'animation signature reprend le mouvement
  de la lame qui tranche, et le premier mot du titre est « la broche ». C'est la
  photo manquante la plus importante du projet.
- 🔥 **La sauce blanche maison.** Citée dans presque tous les avis, nommée dans le
  titre du site, invisible nulle part.
- **L'équipe.** L'accueil est le deuxième argument du restaurant ; il n'y a
  aujourd'hui aucun visage sur le site.

### 6. Les photos en meilleure résolution

La photo des pains que vous avez fournie (896 × 1195) a remplacé l'ancienne et le
hero est net. **Les autres restent limitées** :

| Photo | Résolution | État |
|---|---|---|
| Pains (hero) | 896 → agrandie à 1792 | correcte, l'original du téléphone gagnerait encore |
| Pâte pétrie | **640 × 1138** | faible |
| Devanture de nuit | **765 × 1020** | faible |
| Baklava, künefe | **765 × 1020** | faible |
| Salle brique, comptoir | 1360 | correctes |

**Il nous faut :** ces photos telles qu'elles sortent du téléphone, **sans
redimensionnement ni envoi compressé** (viser 2000 px de large minimum).

### 7. Le logo en fichier propre

Le seul logo disponible est **une affiche photographiée** : fond blanc incrusté,
aucune transparence, 574 × 1020. Il ne peut pas être posé proprement dans l'en-tête.
Le nom y est donc actuellement composé en typographie, au plus près du wordmark.

**Il nous faut :** le fichier d'origine — vectoriel de préférence (`.ai`, `.eps`,
`.svg`, `.pdf`), sinon un PNG à fond transparent en grande taille. À défaut, nous le
redessinons : il faut nous le dire.

### 8. La carte : à valider, pas à fournir

**La carte complète est déjà là** — 7 catégories, 50 plats, prix détaillés. Elle
n'est pas à refournir.

**Il nous faut seulement :** une relecture confirmant que **les prix sont à jour**,
et l'accord sur les **8 plats mis en avant** en page d'accueil : Lahmacun 3,50 €,
Döner Kebab 13 €, Adana 13,50 €, Côtelettes d'Agneau 16 €, Spécialité du Chef 20 €,
Sandwich Döner 8,50 €, Baklava 3 €, Künefe 8,50 €.

---

## 🟡 Décisions, pas informations

### 9. Mesure d'audience

Prévu : un outil **sans cookie** (Plausible ou Umami) — donc **aucun bandeau cookie**
à faire accepter. Un obstacle de moins entre le visiteur et le numéro de téléphone.
Ces outils coûtent quelques euros par mois ; l'alternative est de ne rien mesurer.

**Il nous faut :** l'accord, ou le choix de s'en passer.

### 10. Réseaux et contact

**Il nous faut :** confirmation du compte Instagram (`@azurgrillrestaurant` est
enregistré), l'existence d'un **WhatsApp professionnel**, et d'une page Facebook.

### 11. L'adresse sur le plan

Les coordonnées enregistrées sont marquées « approximatives, déduites de l'adresse
postale ». **Il nous faut :** ouvrir une fois le lien d'itinéraire depuis un
téléphone et confirmer qu'il tombe bien sur la devanture.

---

## ⚙️ Ce qui reste à faire de notre côté

Pas des demandes au client — des points ouverts côté technique :

- **Hébergement et mise en ligne.** Le site est prêt (statique, sans étape de build
  particulière) mais n'est pas déployé, et aucun nom de domaine n'est réservé.
- **Audit Lighthouse.** Impossible à exécuter dans l'environnement de développement :
  l'objectif « ≥ 95 » n'est **ni atteint ni manqué, il n'est pas mesuré**. À faire sur
  l'hébergement réel, où les chiffres auront un sens.
- **Un seul navigateur testé** (Chromium). Safari et Firefox restent à vérifier.
- **Aucun test sur un vrai téléphone**, ni au toucher.
- **Mentions légales** — retirées à votre demande. À signaler tout de même : elles
  sont obligatoires pour un site professionnel en France. Le bloc se remet en une
  ligne le jour où vous le souhaitez.

---

## Ce qui n'est **pas** demandé

Pour éviter les allers-retours : aucun texte rédigé, aucun slogan, aucune traduction
n'est attendu de votre part. Les textes du site sont écrits à partir des avis réels
et des faits ci-dessus, puis soumis à validation.
