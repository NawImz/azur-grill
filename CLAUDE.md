# CLAUDE.md — Template Site Vitrine Restaurant

## Client actuel Azur Grill

- **Nom du restaurant :**
- **Type de cuisine / positionnement :** (ex: bistrot traditionnel, gastro, pizzeria familiale, street food)
- **Adresse / téléphone / horaires :**
- **Couleurs de l'identité existante :** (logo, devanture, menus — si rien n'existe, proposer une palette)
- **Photos disponibles :** (dossier /assets/photos — si photos de mauvaise qualité, le signaler)
- **Lien Google Maps / fiche Google Business :**
- **Réseaux sociaux :**
- **Système de réservation :** (téléphone uniquement / TheFork / Zenchef / formulaire)

---

## Stack imposée (ne jamais en changer sans demande explicite)

- **Framework :** Astro (site statique, performance maximale)
- **Styles :** Tailwind CSS
- **Animations :** GSAP + ScrollTrigger (reveals au scroll), Lenis (smooth scroll)
- **Icônes :** Lucide
- **Polices :** Google Fonts ou Fontsource, maximum 2 familles (1 display + 1 corps)
- **Images :** composant <Image> d'Astro, formats WebP/AVIF, lazy loading partout sauf le hero
- **Déploiement cible :** hébergement statique (Netlify / Vercel / Cloudflare Pages)

Pas de React/Vue sauf si un composant l'exige vraiment (îlot Astro uniquement).
Pas de CMS pour l'instant : contenu dans des fichiers de données (src/data/*.json) pour
que le menu, les horaires et les infos soient modifiables sans toucher au code.

## Direction artistique — règles strictes

**Philosophie : sobre, chaleureux, "agence web haut de gamme". Le héros du site, c'est
le restaurant (ses plats, son lieu, son histoire) — jamais la technique.**

1. **Avant de coder, toujours proposer un mini plan design** : palette (4-6 couleurs
   nommées en hex, tirées de l'identité du resto), paire typographique justifiée,
   concept de layout en une phrase, et UN élément signature mémorable propre à ce
   restaurant. Attendre validation avant d'implémenter.
2. **Palette** : 2-3 couleurs principales maximum + neutres. Dérivée du lieu, de la
   cuisine ou du logo du client. Interdits : dégradés violets/bleus génériques,
   l'esthétique "template IA" (fond crème + serif + accent terracotta par défaut).
   Ces choix ne sont acceptables que s'ils viennent réellement de l'identité du client.
3. **Typographie** : elle porte la personnalité du site. Une display avec du caractère
   (utilisée avec parcimonie : titres uniquement), une sans-serif très lisible pour le
   corps. Échelle typographique cohérente (ex: 14/16/20/24/32/48).
4. **Espace** : généreux. Beaucoup de blanc (ou de sombre), photos plein écran ou
   larges, jamais de mise en page dense.
5. **Photos** : elles font 80% de l'effet. Toujours les mettre en valeur (hero plein
   écran, galerie soignée). Si les photos du client sont faibles, le dire et proposer
   des placeholders élégants en attendant.
6. **Règle Chanel** : avant de livrer, retirer un effet/une décoration. Less is more.

## Animations — règles strictes

- **Autorisé** : fade-in / slide-up subtils au scroll (GSAP ScrollTrigger), parallax
  léger sur le hero, hover élégants (zoom doux sur images, soulignés animés sur liens),
  smooth scroll Lenis, une séquence d'entrée orchestrée sur le hero.
- **Interdit** : particules, 3D, curseurs custom, effets qui bougent en permanence,
  plus de 5 types d'animations différents sur un même site.
- **Toujours** : respecter `prefers-reduced-motion` (désactiver les animations),
  durées courtes (0.4–0.8s), easings naturels (power2.out, expo.out).
- Une animation doit servir la lecture (guider l'œil), jamais impressionner pour rien.

## Structure type du site (sections activables selon le client)

1. **Hero** — photo/vidéo plein écran, nom du resto, phrase d'accroche courte,
   CTA principal "Réserver" + CTA secondaire "Voir la carte"
2. **À propos / Histoire** — 2-3 paragraphes, 1-2 photos, le "pourquoi" du lieu
3. **La carte / Menu** — données dans src/data/menu.json, design lisible,
   prix alignés, catégories claires. Option : PDF téléchargeable en plus.
4. **Galerie** — grille soignée (masonry ou grille éditoriale), lightbox simple
5. **Avis** — 3-4 avis Google sélectionnés, note globale, lien vers la fiche Google
6. **Infos pratiques** — horaires (données dans un JSON), adresse avec carte
   embarquée, parking/accès si pertinent
7. **Contact / Réservation** — téléphone en très gros, bouton de réservation,
   formulaire simple si demandé
8. **Footer** — coordonnées, réseaux sociaux, mentions légales, plan du site

## Non-négociables techniques (checklist avant chaque livraison)

- [ ] **Mobile-first** : conçu d'abord pour mobile (70%+ du trafic resto est mobile)
- [ ] Sur mobile : bouton "Appeler" (lien tel:) et "Itinéraire" (lien Google Maps)
      accessibles en permanence (barre sticky ou header)
- [ ] **Schema.org type Restaurant** en JSON-LD : nom, adresse, téléphone, horaires,
      type de cuisine, fourchette de prix, lien menu, geo — crucial pour Google
- [ ] Meta tags complets : title unique par page, description, Open Graph + image
- [ ] **Lighthouse ≥ 90** sur les 4 scores (Performance, Accessibilité, Best
      Practices, SEO) — vérifier avant livraison
- [ ] Images : WebP/AVIF, dimensions explicites (pas de layout shift), lazy loading
- [ ] Accessibilité : contrastes AA, alt sur toutes les images, navigation clavier,
      focus visible
- [ ] Favicon + apple-touch-icon générés
- [ ] Page 404 personnalisée
- [ ] Aucune erreur console
- [ ] Testé visuellement en 375px, 768px, 1440px

## Workflow de travail

1. Lire ce fichier + la section "Client actuel" + regarder les références visuelles
   fournies (dossier /references s'il existe).
2. Proposer le plan design (palette, typo, layout, élément signature). Attendre OK.
3. Construire section par section, mobile d'abord.
4. **Après chaque section : screenshot desktop + mobile via Playwright MCP,
   s'auto-critiquer comme un directeur artistique exigeant (espacements cohérents ?
   hiérarchie claire ? ça a l'air fait par une agence ou par un dev ?), corriger.**
5. À la fin : dérouler la checklist des non-négociables, corriger, re-screenshot.
6. Ne jamais dire "terminé" sans avoir fait les étapes 4 et 5.

## Ton et contenu

- Textes en français, ton chaleureux mais pas cliché (éviter "une expérience culinaire
  unique", "des produits d'exception" et autres formules creuses).
- Textes courts : les gens viennent voir la carte, les horaires et des photos.
- Boutons explicites : "Réserver une table", "Voir la carte", "Nous appeler" —
  jamais "Cliquez ici" ou "En savoir plus" seul.
- Si une info client manque (horaires, prix...), utiliser un placeholder visible
  [À COMPLÉTER] et me lister toutes les infos manquantes en fin de session.
