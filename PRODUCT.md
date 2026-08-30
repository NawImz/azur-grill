# PRODUCT.md — Azur Grill

Écrit avant la première ligne de composant, comme l'exige `CLAUDE.md` §2 Phase 1.
Rédigé à partir du brief de refonte et des faits vérifiés dans `SETUP.md` — rien n'est
hérité d'une session antérieure.

## 1. Ce qu'est ce site, et la double contrainte

Un site vitrine **une page** pour un restaurant turc halal d'Épinay-sur-Seine.

Il sert **deux publics à la fois**, et c'est ce qui le rend particulier :

1. **Le client du quartier** qui cherche une adresse, un horaire, un numéro ou la carte.
   Son besoin est utilitaire et pressé.
2. **Le prospect de Nawfal** — un autre restaurateur à qui ce site sera montré sur un
   téléphone, **en trente secondes**, pour emporter une décision commerciale.

Ces deux publics ne s'opposent pas, ils convergent : ce qui impressionne un prospect,
c'est précisément de voir un site qui **répond instantanément** aux questions du client
du quartier. Chaque bonne pratique doit donc être non seulement présente mais
**repérable et nommable en quelques secondes** : appeler en un geste, voir la note et
de vrais avis, ouvrir le plan, savoir si c'est ouvert **maintenant**.

Le site actuel fait le travail mais ne surprend personne. Il n'échoue pas — il ne se
distingue pas.

## 2. Les faits (vérifiés — ne pas réinventer)

- **Azur Grill** — 69 Boulevard Foch, 93800 Épinay-sur-Seine. Cuisine turque, halal.
- Téléphone : **01 86 04 22 42**.
- **4,6/5 sur plus de 110 avis Google.**
- Horaires : **lundi–samedi 11h30–23h, fermé le dimanche**, à afficher marqué
  **`À CONFIRMER`**. Les sources publiques se contredisent (une fiche annonce
  lundi–vendredi 12h–22h30 week-end fermé ; les réseaux du restaurant annoncent
  lundi–samedi 11h30–23h). **C'est la première chose à faire valider.**
  ⚠️ Les données du dépôt affichent aujourd'hui « 7j/7 · 11h30–22h30 », ce qui ne
  correspond à **aucune** des deux sources : à corriger, pas à propager.
- Services confirmés : sur place, à emporter, livraison, traiteur, groupes, menu enfant,
  paiement sans contact, Edenred/Ticket Restaurant, accès fauteuil roulant,
  stationnement rue, réservation possible, service tardif.
- **Carte complète déjà disponible dans le dépôt** : 7 catégories, 50 plats, prix réels
  (`src/data/menu.json`). Ce n'est pas un manque — c'est un actif à mieux exploiter.

### Identité verrouillée

Motif **nazar boncuğu** (l'œil turc protecteur) et palette bleu profond + crème.
Valeurs échantillonnées sur le logo réel : **`#16098F`** et **`#74C0EC`** (voir
`DESIGN.md`). Le logo existant est une **affiche photographiée**, pas un logo détouré —
son wordmark « AZUR RESTAURANT » est composé dans un **serif à fort contraste**, ce qui
a une conséquence directe sur la typographie du site (voir `DESIGN.md` §2).

## 3. Registre et personnalité

**Registre : `brand`** — le site doit produire une impression avant de délivrer une
information, sans jamais retarder l'information.

Quatre traits, dans cet ordre :

1. **Fait ici.** Le trait central. Ce n'est pas une revendication d'« authenticité »,
   c'est un fait matériel constaté : la broche, le pain et la sauce blanche sont
   préparés sur place.
2. **Chaleureux.** L'accueil revient dans presque chaque avis. C'est le second pilier,
   jamais un décor.
3. **Sûr de lui, jamais tapageur.** Une adresse qui n'a pas besoin d'en faire trop.
   Cela vaut aussi pour le mouvement : un geste net, pas une démonstration.
4. **De quartier, et fier de l'être.** Plusieurs clients disent que l'endroit a comblé
   un manque à Épinay. C'est un ancrage, pas une limite.

## 4. La promesse — variantes et arbitrage

Ligne directrice du brief : *tout est fait ici, de la broche à la sauce, par une équipe
qui vous connaît.* Quatre variantes courtes, puis un choix net :

| # | Variante | Verdict |
|---|---|---|
| A | **« La broche, le pain, la sauce. Tout est fait ici. »** | **retenue** |
| B | « Rien n'arrive tout prêt. » | Frappe fort mais se définit par la négative — on retient ce que le restaurant *n'est pas*. |
| C | « De la broche à la sauce, tout sort de notre cuisine. » | Juste, mais « notre cuisine » est une formule que n'importe quel restaurant peut signer. |
| D | « Tout est fait ici. Même la sauce blanche. » | Très mémorable — la sauce blanche est le détail improbable que les avis citent. **Gardée comme alternative** si le client trouve A trop sobre. |

**Retenue : A — « La broche, le pain, la sauce. Tout est fait ici. »**
Trois noms concrets, un rythme ternaire, et la promesse en chute. Elle nomme exactement
les trois choses que les avis réels citent en premier, dans leur ordre d'apparition.
Elle échoue au test « un autre restaurant turc pourrait-il signer ça ? » — et c'est
précisément ce qu'on cherche : la plupart ne le peuvent pas, parce que la plupart ne
font pas leur pain.

Second pilier, en appui et jamais en titre : **l'accueil** — « Et une équipe qui finit
par connaître votre commande. »

## 5. Ce sur quoi la promesse ne doit PAS reposer

- ❌ **La générosité des portions.** Invérifiable, et **déjà contestée une fois** dans
  un avis public sur une commande à emporter. Le site actuel s'appuie dessus
  (« Une carte généreuse », « Portions généreuses… », « hero-plat-genereux ») :
  **à retirer**, c'est une promesse fragile.
- ❌ **« Cuisine authentique », « saveurs d'ailleurs », « voyage gustatif »** — les
  formules que n'importe quel restaurant peut signer.
- ❌ Toute affirmation de prix ou d'horaire non tirée de `src/data/`.

## 6. Anti-références

- **Les trois looks « AI-slop »** décrits dans `SKILL.md`, et particulièrement le
  premier : fond crème dominant + serif à fort contraste + accent terracotta ~`#D97757`.
  **Le site actuel est très près de ce piège** (voir la mesure dans `DESIGN.md` §1).
- **Le site de kebab générique** : dégradés rouge/noir, flammes, photos de stock.
- **La collection d'effets.** Une seule idée d'animation, exécutée jusqu'au bout,
  vaut mieux que dix effets corrects (`DESIGN.md` §3).
- **La carte cachée derrière des accordéons fermés** — le défaut actuel : sept clics
  avant de voir un seul prix.
- **L'iframe Google Maps intégrée** : lourde, et déjà une requête échouée en console.

## 7. Principes de conception

1. **Aucune information de base derrière un clic.** Adresse, horaires, téléphone, prix
   des plats signature : visibles sans interaction.
2. **Une seule page, six sections, pas plus** : en-tête, hero, la carte, ce qu'on dit de
   nous, le lieu, infos pratiques.
3. **Une donnée, une source.** Téléphone, horaires, carte, avis viennent de `src/data/` ;
   aucune valeur en dur dans un composant.
4. **Le bleu structure, la crème respire.** Le bleu profond est la couleur dominante ;
   la crème est secondaire.
5. **Chaque animation doit avoir une raison narrative**, sinon elle saute.
6. **Ce qui n'est pas vérifié est marqué comme tel** — `À CONFIRMER`, `PLACEHOLDER-AVIS` —
   jamais inventé pour faire joli.

## 8. Accessibilité — plancher non négociable

- **WCAG 2.2 AA** : ≥ 4,5:1 pour le texte courant, ≥ 3:1 pour le grand texte et les
  composants, **mesuré par échantillonnage pixel** sur le rendu composite, jamais par
  calcul token contre token.
- **`prefers-reduced-motion: reduce`** coupe tout : le hero s'affiche directement dans
  son état final, sans séquence de tranches ni rotation de broche.
- Navigation clavier complète, focus visible sur fond clair **comme** sur fond bleu.
- Cibles tactiles ≥ 44 × 44 px.
- Le téléphone est un lien `tel:` réel, jamais une image.
- Les photos de plats portent une description utile, pas le nom du fichier.

## 9. Ce que ce site fait de différent (les trente secondes de Nawfal)

À tenir en une phrase chacun, et à démontrer à l'écran :

1. **On sait si c'est ouvert maintenant** — statut calculé en direct, pas un tableau
   d'horaires à déchiffrer.
2. **On appelle en un geste** — le numéro est un lien, présent en permanence sur mobile.
3. **Les prix sont visibles sans cliquer** — huit plats signature, prix affichés.
4. **Les avis sont réels et vérifiables** — note, extraits, lien vers la fiche Google.
5. **Le plan s'ouvre dans l'app de navigation** — un lien, pas une iframe qui alourdit.
6. **Aucun bandeau cookie** — mesure d'audience sans cookie, donc rien à accepter.
7. **Une signature visuelle qu'on ne voit nulle part ailleurs** — la révélation en
   tranches (`DESIGN.md` §3).
