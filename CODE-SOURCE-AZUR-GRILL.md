# Code source — Site Azur Grill Restaurant

Stack : Astro (statique) + Tailwind CSS + GSAP/ScrollTrigger + Lenis + lucide-static + Fontsource.

## Installation

```bash
npm install
npm approve-scripts esbuild sharp
npm install
npm run dev      # http://localhost:4321
npm run build    # génère dist/
```

## Arborescence

```
azur-grill/
├── astro.config.mjs
├── tailwind.config.mjs      ← palette extraite du logo
├── package.json
├── public/                  ← favicons, og-image
└── src/
    ├── assets/photos-v2/    ← photos du client
    ├── data/                ← menu, horaires, infos (modifiables sans code)
    ├── layouts/Layout.astro ← <head>, SEO, Schema.org
    ├── pages/               ← index.astro, 404.astro
    ├── styles/global.css
    └── components/          ← 16 composants
```

---

## `package.json`

```json
{
  "name": "azur-grill",
  "type": "module",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro"
  },
  "dependencies": {
    "astro": "^5.1.0",
    "@astrojs/tailwind": "^5.1.4",
    "tailwindcss": "^3.4.17",
    "gsap": "^3.12.7",
    "lenis": "^1.1.19",
    "lucide-static": "^0.469.0",
    "@fontsource-variable/fraunces": "^5.1.1",
    "@fontsource/manrope": "^5.1.1"
  },
  "allowScripts": {
    "esbuild@0.27.7": true,
    "esbuild@0.25.12": true,
    "sharp@0.34.5": true
  }
}
```

## `astro.config.mjs`

```js
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://azur-grill-epinay.fr',
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
  ],
});
```

## `tailwind.config.mjs`

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        nazar: '#16098F',
        ciel: '#74C0EC',
        creme: '#FAF8F4',
        encre: '#211C17',
        brique: '#A6532F',
        moutarde: '#D9A23E',
      },
      fontFamily: {
        display: ['"Fraunces Variable"', 'serif'],
        body: ['"Manrope"', 'sans-serif'],
      },
      fontSize: {
        sm: ['0.875rem', { lineHeight: '1.5' }],
        base: ['1rem', { lineHeight: '1.6' }],
        lg: ['1.25rem', { lineHeight: '1.5' }],
        xl: ['1.5rem', { lineHeight: '1.3' }],
        '2xl': ['2rem', { lineHeight: '1.2' }],
        '3xl': ['3rem', { lineHeight: '1.1' }],
        '4xl': ['3.5rem', { lineHeight: '1.05' }],
        '5xl': ['4rem', { lineHeight: '1.02' }],
      },
    },
  },
  plugins: [],
};
```

## `tsconfig.json`

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"]
}
```

## `src/styles/global.css`

```css
@import '@fontsource-variable/fraunces';
@import '@fontsource/manrope/400.css';
@import '@fontsource/manrope/500.css';
@import '@fontsource/manrope/600.css';
@import '@fontsource/manrope/700.css';

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    scroll-behavior: auto;
  }

  body {
    @apply bg-creme text-encre font-body antialiased;
  }

  h1, h2, h3 {
    @apply font-display;
  }

  :focus-visible {
    outline: none;
    box-shadow: 0 0 0 2px theme('colors.creme'), 0 0 0 4px theme('colors.nazar');
    border-radius: 2px;
  }

  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
}
```

## `src/layouts/Layout.astro`

```astro
---
import '../styles/global.css';
import restaurant from '../data/restaurant.json';
import horaires from '../data/horaires.json';

interface Props {
  title?: string;
  description?: string;
  ogImage?: string;
}

const {
  title = restaurant.seoLocal.titre,
  description = restaurant.seoLocal.description,
  ogImage = '/og-image.jpg',
} = Astro.props;

const canonicalURL = new URL(Astro.url.pathname, Astro.site);

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Restaurant',
  name: restaurant.nom,
  image: new URL(ogImage, Astro.site).toString(),
  servesCuisine: 'Turkish',
  priceRange: restaurant.prixRange,
  telephone: restaurant.telephone,
  address: {
    '@type': 'PostalAddress',
    streetAddress: restaurant.adresse.rue,
    postalCode: restaurant.adresse.codePostal,
    addressLocality: restaurant.adresse.ville,
    addressCountry: 'FR',
  },
  geo: {
    '@type': 'GeoCoordinates',
    latitude: restaurant.geo.latitude,
    longitude: restaurant.geo.longitude,
  },
  url: Astro.site?.toString(),
  openingHoursSpecification: horaires.schemaOrgOpeningHours.map((spec) => ({
    '@type': 'OpeningHoursSpecification',
    dayOfWeek: [
      'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
    ],
    opens: '11:30',
    closes: '22:30',
  })),
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: restaurant.avisGoogle.note,
    reviewCount: restaurant.avisGoogle.nombreAvis,
  },
  servesHalal: true,
  menu: `${Astro.site}#carte`,
};
---

<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="canonical" href={canonicalURL} />

    <title>{title}</title>
    <meta name="description" content={description} />

    <meta property="og:type" content="restaurant.restaurant" />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={new URL(ogImage, Astro.site)} />
    <meta property="og:url" content={canonicalURL} />
    <meta property="og:locale" content="fr_FR" />
    <meta name="twitter:card" content="summary_large_image" />

    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <meta name="theme-color" content="#16098F" />

    <script type="application/ld+json" set:html={JSON.stringify(jsonLd)} />
  </head>
  <body>
    <slot />
  </body>
</html>
```

## `src/pages/index.astro`

```astro
---
import Layout from '../layouts/Layout.astro';
import Header from '../components/Header.astro';
import StickyMobileBar from '../components/StickyMobileBar.astro';
import Hero from '../components/Hero.astro';
import About from '../components/About.astro';
import Menu from '../components/Menu.astro';
import Gallery from '../components/Gallery.astro';
import Reviews from '../components/Reviews.astro';
import PracticalInfo from '../components/PracticalInfo.astro';
import CtaBand from '../components/CtaBand.astro';
import Footer from '../components/Footer.astro';
import SmoothScroll from '../components/SmoothScroll.astro';
import ScrollReveal from '../components/ScrollReveal.astro';
---

<Layout>
  <SmoothScroll />
  <ScrollReveal />
  <Header />
  <main class="pb-14 md:pb-0">
    <Hero />
    <About />
    <Menu />
    <Gallery />
    <Reviews />
    <PracticalInfo />
    <CtaBand />
  </main>
  <Footer />
  <StickyMobileBar />
</Layout>
```

## `src/pages/404.astro`

```astro
---
import Layout from '../layouts/Layout.astro';
import Icon from '../components/Icon.astro';
import NazarMark from '../components/NazarMark.astro';
import restaurant from '../data/restaurant.json';
---

<Layout
  title="Page introuvable — Azur Grill Restaurant"
  description="Cette page n'existe pas. Retrouvez la carte, les horaires et les coordonnées d'Azur Grill Restaurant à Épinay-sur-Seine."
>
  <main class="min-h-screen bg-nazar text-creme flex items-center justify-center px-5 py-24">
    <div class="max-w-md text-center">
      <NazarMark class="w-16 h-16 mx-auto mb-8 text-ciel" />
      <p class="font-display text-5xl mb-4">404</p>
      <h1 class="font-display text-2xl mb-4">Cette page n'existe pas</h1>
      <p class="text-creme/70 mb-8">
        La page que vous cherchez a peut-être changé d'adresse — comme nous n'en changeons pas, revenez à l'accueil.
      </p>
      <div class="flex flex-wrap justify-center gap-3">
        <a
          href="/"
          class="inline-flex items-center gap-2 bg-brique text-creme font-semibold px-6 py-3.5 rounded-full hover:brightness-110 transition"
        >
          Retour à l'accueil
        </a>
        <a
          href={restaurant.telephoneLien}
          class="inline-flex items-center gap-2 bg-creme/10 text-creme font-semibold px-6 py-3.5 rounded-full border border-creme/40 hover:bg-creme/20 transition"
        >
          <Icon name="phone" class="w-4 h-4" />
          Nous appeler
        </a>
      </div>
    </div>
  </main>
</Layout>
```

## `src/components/Header.astro`

```astro
---
import Icon from './Icon.astro';
import restaurant from '../data/restaurant.json';

const navLinks = [
  { href: '/#a-propos', label: 'À propos' },
  { href: '/#carte', label: 'La Carte' },
  { href: '/#galerie', label: 'Galerie' },
  { href: '/#avis', label: 'Avis' },
  { href: '/#infos', label: 'Infos pratiques' },
];
---

<header
  id="site-header"
  class="fixed top-0 inset-x-0 z-40 transition-[background-color,transform,box-shadow] duration-300"
  data-scrolled="false"
  data-hidden="false"
>
  <div class="max-w-6xl mx-auto px-5 md:px-8 flex items-center justify-between h-16 md:h-20">
    <a href="/" class="font-display text-xl md:text-2xl text-creme header-brand tracking-wide">
      Azur Grill
    </a>

    <nav class="hidden lg:flex items-center gap-8">
      {navLinks.map((link) => (
        <a
          href={link.href}
          class="nav-underline text-sm font-semibold text-creme hover:text-ciel transition-colors"
        >
          {link.label}
        </a>
      ))}
    </nav>

    <div class="flex items-center gap-3">
      <a
        href={restaurant.uberEatsUrl}
        target="_blank"
        rel="noopener noreferrer"
        class="hidden sm:inline-flex items-center gap-2 bg-brique text-creme text-sm font-semibold px-5 py-2.5 rounded-full hover:brightness-110 transition"
      >
        Commander
      </a>
      <button
        id="menu-toggle"
        class="lg:hidden text-creme header-link p-2.5"
        aria-label="Ouvrir le menu"
        aria-expanded="false"
        aria-controls="mobile-nav"
      >
        <Icon name="menu" class="w-6 h-6" />
      </button>
    </div>
  </div>

  <nav
    id="mobile-nav"
    class="lg:hidden hidden fixed inset-0 top-16 bg-nazar px-6 py-8 flex flex-col gap-1"
  >
    {navLinks.map((link) => (
      <a
        href={link.href}
        class="mobile-nav-link text-creme text-lg font-display py-3 border-b border-white/10"
      >
        {link.label}
      </a>
    ))}
    <a
      href={restaurant.uberEatsUrl}
      target="_blank"
      rel="noopener noreferrer"
      class="mt-6 inline-flex justify-center items-center gap-2 bg-brique text-creme text-base font-semibold px-5 py-3.5 rounded-full"
    >
      Commander sur Uber Eats
    </a>
  </nav>
</header>

<style>
  #site-header[data-scrolled='true'] {
    @apply bg-nazar/95 backdrop-blur-sm shadow-sm;
  }

  #site-header[data-hidden='true'] {
    transform: translateY(-100%);
  }

  .nav-underline {
    position: relative;
  }

  .nav-underline::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -5px;
    width: 100%;
    height: 1.5px;
    background: currentColor;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.3s ease-out;
  }

  .nav-underline:hover::after,
  .nav-underline:focus-visible::after {
    transform: scaleX(1);
  }
</style>

<script>
  const header = document.getElementById('site-header');
  const toggle = document.getElementById('menu-toggle');
  const mobileNav = document.getElementById('mobile-nav');

  let lastY = window.scrollY;
  const onScroll = () => {
    if (!header) return;
    const y = window.scrollY;
    header.dataset.scrolled = y > 24 ? 'true' : 'false';
    // Hide the bar while scrolling down past the hero, bring it back on any
    // upward scroll — never while the mobile menu is open.
    const menuOpen = document.body.classList.contains('overflow-hidden');
    header.dataset.hidden = y > 280 && y > lastY && !menuOpen ? 'true' : 'false';
    lastY = y;
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  let open = false;
  const setOpen = (next: boolean) => {
    open = next;
    toggle?.setAttribute('aria-expanded', String(open));
    toggle?.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    mobileNav?.classList.toggle('hidden', !open);
    document.body.classList.toggle('overflow-hidden', open);
  };

  toggle?.addEventListener('click', () => setOpen(!open));
  mobileNav?.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
</script>
```

## `src/components/Hero.astro`

```astro
---
import { Image } from 'astro:assets';
import Icon from './Icon.astro';
import restaurant from '../data/restaurant.json';
import heroImage from '../assets/photos-v2/hero-plat-genereux.webp';

const stats = [
  { valeur: `${restaurant.avisGoogle.note.toFixed(1).replace('.', ',')}/5`, label: `Note Google · ${restaurant.avisGoogle.nombreAvis} avis` },
  { valeur: '7j/7', label: 'Ouvert 11h30 – 22h30' },
  { valeur: '100%', label: 'Pain & kebab maison' },
  { valeur: 'Halal', label: 'Sur place · emporter · livraison' },
];
---

<section id="top" class="relative isolate h-[70svh] min-h-[420px] md:h-[100svh] md:min-h-[560px] flex items-end overflow-hidden">
  <div id="hero-media" class="absolute inset-x-0 top-0 h-[115%] will-change-transform">
    <Image
      id="hero-img"
      src={heroImage}
      alt="Assiette généreuse de grillades, riz et légumes grillés servie chez Azur Grill à Épinay-sur-Seine"
      loading="eager"
      fetchpriority="high"
      class="w-full h-full object-cover object-[center_75%] md:object-center will-change-transform"
    />
  </div>
  <div class="absolute inset-0 bg-gradient-to-t from-nazar/95 via-nazar/65 to-nazar/40" aria-hidden="true"></div>

  <div class="relative z-10 max-w-6xl mx-auto px-5 md:px-8 pb-20 md:pb-28 w-full">
    <p
      data-hero-reveal
      class="inline-block font-display italic text-ciel text-base md:text-xl bg-nazar/70 backdrop-blur-sm px-4 py-1.5 rounded-full mb-5"
    >
      Grillades turques &amp; pain maison
    </p>
    <h1 class="font-display text-creme text-4xl md:text-6xl leading-[1.02] max-w-3xl">
      <span class="block overflow-hidden pb-1"><span data-hero-line class="block">Azur Grill</span></span>
      <span class="block overflow-hidden pb-1"><span data-hero-line class="block">Restaurant</span></span>
    </h1>
    <p
      data-hero-reveal
      class="text-creme/90 text-lg mt-5 max-w-xl"
    >
      Viandes grillées, kebab et pain cuits sur place, desserts turcs artisanaux — à Épinay-sur-Seine, halal, ouvert 7j/7.
    </p>

    <div data-hero-reveal class="flex flex-wrap gap-3 mt-8">
      <a
        href={restaurant.uberEatsUrl}
        target="_blank"
        rel="noopener noreferrer"
        class="group inline-flex items-center gap-2 bg-brique text-creme font-semibold px-6 py-3.5 rounded-full hover:brightness-110 transition"
      >
        Commander
        <Icon name="arrow-right" class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
      </a>
      <a
        href="#carte"
        class="inline-flex items-center gap-2 bg-creme/10 text-creme font-semibold px-6 py-3.5 rounded-full border border-creme/40 hover:bg-creme/20 transition"
      >
        Voir la carte
      </a>
    </div>
  </div>

  <div
    data-hero-reveal
    class="hidden md:flex absolute bottom-8 left-1/2 -translate-x-1/2 flex-col items-center gap-2 text-creme/60"
    aria-hidden="true"
  >
    <span class="text-[11px] font-semibold tracking-[0.25em] uppercase">Défiler</span>
    <span class="w-px h-10 bg-creme/40"></span>
  </div>
</section>

<div class="bg-creme border-b border-encre/10">
  <dl data-reveal class="max-w-6xl mx-auto px-5 md:px-8 py-6 md:py-8 grid grid-cols-2 md:grid-cols-4 gap-x-6 gap-y-5">
    {stats.map((stat) => (
      <div class="text-center md:text-left">
        <dd class="font-display text-2xl md:text-3xl text-nazar leading-none">{stat.valeur}</dd>
        <dt class="text-xs md:text-sm text-encre/60 mt-1.5">{stat.label}</dt>
      </div>
    ))}
  </dl>
</div>

<script>
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  gsap.registerPlugin(ScrollTrigger);

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const lines = gsap.utils.toArray<HTMLElement>('[data-hero-line]');
  const items = gsap.utils.toArray<HTMLElement>('[data-hero-reveal]');

  if (reduceMotion) {
    gsap.set([...lines, ...items], { opacity: 1, y: 0, yPercent: 0 });
  } else {
    gsap.fromTo('#hero-img', { scale: 1.08 }, { scale: 1, duration: 1.1, ease: 'expo.out' });
    gsap.fromTo(lines, { yPercent: 110 }, { yPercent: 0, duration: 0.8, ease: 'expo.out', stagger: 0.1, delay: 0.1 });
    gsap.set(items, { opacity: 0, y: 24 });
    gsap.to(items, { opacity: 1, y: 0, duration: 0.7, ease: 'expo.out', stagger: 0.1, delay: 0.35 });

    gsap.to('#hero-media', {
      yPercent: -10,
      ease: 'none',
      scrollTrigger: { trigger: '#top', start: 'top top', end: 'bottom top', scrub: true },
    });
  }
</script>
```

## `src/components/About.astro`

```astro
---
import { Image } from 'astro:assets';
import Kicker from './Kicker.astro';
import painCuitImage from '../assets/photos-v2/about-pain-maison.webp';
import patePetrieImage from '../assets/photos-v2/about-pate-petrie.jpg';
---

<section id="a-propos" class="bg-creme py-20 md:py-28">
  <div class="max-w-6xl mx-auto px-5 md:px-8 grid lg:grid-cols-2 gap-12 md:gap-16 items-center">
    <div data-reveal class="relative">
      <Image
        src={painCuitImage}
        alt="Pain maison tout juste sorti du four chez Azur Grill"
        loading="lazy"
        class="relative w-full aspect-[4/5] rounded-2xl object-cover"
      />
      <Image
        src={patePetrieImage}
        alt="Pâte à pain pétrie et façonnée à la main chez Azur Grill"
        loading="lazy"
        class="hidden sm:block absolute -bottom-8 -right-6 aspect-square w-2/5 rounded-xl border-4 border-creme shadow-lg object-cover"
      />
    </div>

    <div data-reveal>
      <Kicker number="01" class="mb-4">À propos</Kicker>
      <h2 class="font-display text-2xl md:text-3xl text-nazar leading-tight mb-6">
        Le pain sort du four, la viande tourne sur la broche — à quelques mètres de votre table.
      </h2>
      <div class="space-y-4 text-encre/90 text-base md:text-lg leading-relaxed">
        <p>
          Chez Azur Grill, rien n'arrive tout prêt. Le pain est pétri et cuit sur place,
          le kebab est préparé maison, et les grillades passent directement du grill à l'assiette.
        </p>
        <p>
          Né à Épinay-sur-Seine, le restaurant s'est construit autour d'une idée simple :
          une cuisine turque généreuse et halal, servie dans un cadre chaleureux et soigné —
          aussi bien pour un déjeuner rapide qu'un dîner en famille.
        </p>
        <p>
          Baklava, künefe et sütlaç maison viennent clore le repas, comme à la maison — en plus généreux.
        </p>
      </div>
    </div>
  </div>
</section>
```

## `src/components/Menu.astro`

```astro
---
import Kicker from './Kicker.astro';
import Icon from './Icon.astro';
import NazarCluster from './NazarCluster.astro';
import menu from '../data/menu.json';

function formatPrix(prix: number): string {
  const isWhole = Number.isInteger(prix);
  return isWhole ? `${prix} €` : `${prix.toFixed(2).replace('.', ',')} €`;
}
---

<section id="carte" class="relative isolate bg-creme py-20 md:py-28 overflow-hidden">
  <NazarCluster tone="light" />
  <div class="max-w-5xl mx-auto px-5 md:px-8">
    <div data-reveal class="max-w-2xl mb-12 md:mb-16">
      <Kicker number="02" class="mb-4">La Carte</Kicker>
      <h2 class="font-display text-2xl md:text-3xl text-nazar leading-tight">
        Une carte généreuse, sans chichi.
      </h2>
    </div>

    <div data-reveal-group class="md:columns-2 md:gap-16 [&>*]:break-inside-avoid">
      {menu.map((categorie) => (
        <details data-reveal class="group border-b border-encre/15 py-5 mb-1">
          <summary class="flex items-center justify-between gap-4 cursor-pointer list-none">
            <span class="flex items-baseline gap-2.5">
              <span class="font-display text-xl md:text-2xl text-nazar">{categorie.categorie}</span>
              <span class="text-sm text-encre/50">({categorie.plats.length})</span>
            </span>
            <Icon name="chevron-down" class="w-5 h-5 text-brique shrink-0 transition-transform duration-300 group-open:rotate-180" />
          </summary>

          {categorie.note && (
            <p class="text-sm italic text-brique mt-3">{categorie.note}</p>
          )}

          <ul class="mt-5 space-y-4">
            {categorie.plats.map((plat) => (
              <li>
                <div class="flex items-baseline gap-2.5">
                  <p class="font-semibold text-encre">{plat.nom}</p>
                  <span class="flex-1 border-b border-dotted border-encre/30 -translate-y-1" aria-hidden="true"></span>
                  <p class="font-semibold text-nazar whitespace-nowrap tabular-nums">{formatPrix(plat.prix)}</p>
                </div>
                {plat.description && (
                  <p class="text-sm text-encre/70 mt-0.5 pr-14">{plat.description}</p>
                )}
              </li>
            ))}
          </ul>
        </details>
      ))}
    </div>
  </div>
</section>
```

## `src/components/Gallery.astro`

```astro
---
import { Image, getImage } from 'astro:assets';
import Kicker from './Kicker.astro';
import Icon from './Icon.astro';

import comptoir from '../assets/photos-v2/gallery-comptoir.webp';
import brochettesPoulet from '../assets/photos-v2/gallery-brochettes-poulet.webp';
import salleJaune from '../assets/photos-v2/gallery-salle-jaune.webp';
import interieurBrique from '../assets/photos-v2/gallery-interieur-brique.webp';
import baklavaThe from '../assets/photos-v2/gallery-baklava-the.webp';
import sandwichs from '../assets/photos-v2/gallery-sandwichs.webp';
import kunefe from '../assets/photos-v2/gallery-kunefe.webp';
import baklavaSombre from '../assets/photos-v2/gallery-baklava-sombre.jpg';

const photos = [
  { src: comptoir, alt: 'Comptoir et salle d\'Azur Grill, ambiance chaleureuse', span: 'sm:col-span-2' },
  { src: brochettesPoulet, alt: 'Brochettes de poulet grillées, riz, salade et frites', span: 'sm:row-span-2' },
  { src: baklavaSombre, alt: 'Baklava aux pistaches et thé turc', span: '' },
  { src: salleJaune, alt: 'Salle intérieure, coin repas chaleureux', span: '' },
  { src: interieurBrique, alt: 'Salle intérieure, mur de brique et fleurs suspendues', span: 'sm:col-span-2' },
  { src: kunefe, alt: 'Künefe maison, pâte de kadayif et pistache', span: '' },
  { src: baklavaThe, alt: 'Baklava et thé turc', span: '' },
  { src: sandwichs, alt: 'Sandwichs kebab à emporter avec frites', span: '' },
];

const lightboxImages = await Promise.all(photos.map((p) => getImage({ src: p.src })));
---

<section id="galerie" class="bg-creme py-20 md:py-28">
  <div class="max-w-6xl mx-auto px-5 md:px-8">
    <div data-reveal class="max-w-2xl mb-12 md:mb-16">
      <Kicker number="03" class="mb-4">Galerie</Kicker>
      <h2 class="font-display text-2xl md:text-3xl text-nazar leading-tight">
        Le lieu, les assiettes, l'ambiance.
      </h2>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-3 auto-rows-[160px] sm:auto-rows-[200px] gap-3 md:gap-4">
      {photos.map((photo, i) => (
        <button
          type="button"
          data-gallery-trigger
          data-reveal
          data-index={i}
          class:list={['group relative text-left rounded-xl overflow-hidden', photo.span]}
        >
          <Image
            src={photo.src}
            alt={photo.alt}
            loading="lazy"
            class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
          <span class="absolute inset-0 bg-nazar/0 group-hover:bg-nazar/20 transition-colors" aria-hidden="true"></span>
          <span class="absolute bottom-3 right-3 w-8 h-8 rounded-full bg-creme/90 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <Icon name="external-link" class="w-4 h-4 text-nazar" />
          </span>
        </button>
      ))}
    </div>
  </div>
</section>

<div
  id="lightbox"
  class="hidden fixed inset-0 z-[60] bg-nazar/95 items-center justify-center p-6"
  role="dialog"
  aria-modal="true"
  aria-label="Photo agrandie"
>
  <button
    type="button"
    id="lightbox-close"
    class="absolute top-5 right-5 text-creme p-2 hover:text-ciel transition-colors"
    aria-label="Fermer"
  >
    <Icon name="x" class="w-7 h-7" />
  </button>
  <div id="lightbox-content" class="w-full max-w-2xl aspect-[4/5]"></div>
</div>

<script define:vars={{ srcs: lightboxImages.map((img) => img.src), alts: photos.map((p) => p.alt) }}>
  const lightbox = document.getElementById('lightbox');
  const content = document.getElementById('lightbox-content');
  const closeBtn = document.getElementById('lightbox-close');
  const triggers = document.querySelectorAll('[data-gallery-trigger]');

  function openLightbox(index) {
    content.innerHTML = `<img src="${srcs[index]}" alt="${alts[index]}" class="w-full h-full object-cover rounded-2xl" />`;
    lightbox.classList.remove('hidden');
    lightbox.classList.add('flex');
    document.body.classList.add('overflow-hidden');
    closeBtn.focus();
  }

  function closeLightbox() {
    lightbox.classList.add('hidden');
    lightbox.classList.remove('flex');
    document.body.classList.remove('overflow-hidden');
  }

  triggers.forEach((btn) => {
    btn.addEventListener('click', () => openLightbox(Number(btn.dataset.index)));
  });
  closeBtn.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !lightbox.classList.contains('hidden')) closeLightbox();
  });
</script>
```

## `src/components/Reviews.astro`

```astro
---
import Kicker from './Kicker.astro';
import Icon from './Icon.astro';
import NazarCluster from './NazarCluster.astro';
import restaurant from '../data/restaurant.json';

const { note, nombreAvis, citations } = restaurant.avisGoogle;
const fullStars = Math.round(note);
---

<section id="avis" class="relative isolate bg-nazar py-20 md:py-28 overflow-hidden">
  <NazarCluster tone="dark" />
  <div class="max-w-6xl mx-auto px-5 md:px-8">
    <div data-reveal class="max-w-2xl mb-12 md:mb-16">
      <Kicker number="04" class="mb-4">Avis Google</Kicker>
      <h2 class="font-display text-2xl md:text-3xl text-creme leading-tight">
        Ce que disent nos clients.
      </h2>
    </div>

    <div data-reveal class="flex items-center gap-4 mb-10">
      <p class="font-display text-5xl md:text-6xl text-creme">{note.toFixed(1)}</p>
      <div>
        <div class="flex gap-1 text-moutarde mb-1">
          {Array.from({ length: 5 }).map((_, i) => (
            <Icon name="star" class:list={['w-5 h-5', i < fullStars ? 'fill-current' : 'opacity-30']} />
          ))}
        </div>
        <p class="text-creme/70 text-sm">{nombreAvis} avis Google</p>
      </div>
    </div>

    <div class="grid md:grid-cols-3 gap-5">
      {citations.map((citation) => (
        <blockquote data-reveal class="bg-creme/5 border border-creme/10 rounded-2xl p-6">
          <div class="flex gap-1 text-moutarde mb-3">
            {Array.from({ length: citation.note }).map(() => (
              <Icon name="star" class="w-4 h-4 fill-current" />
            ))}
          </div>
          <p class="text-creme/90 leading-relaxed">"{citation.texte}"</p>
        </blockquote>
      ))}
    </div>
  </div>
</section>
```

## `src/components/PracticalInfo.astro`

```astro
---
import Kicker from './Kicker.astro';
import Icon from './Icon.astro';
import NazarCluster from './NazarCluster.astro';
import restaurant from '../data/restaurant.json';
import horaires from '../data/horaires.json';
---

<section id="infos" class="relative isolate bg-creme py-20 md:py-28 overflow-hidden">
  <NazarCluster tone="light" />
  <div class="max-w-6xl mx-auto px-5 md:px-8">
    <div data-reveal class="max-w-2xl mb-12 md:mb-16">
      <Kicker number="05" class="mb-4">Infos pratiques</Kicker>
      <h2 class="font-display text-2xl md:text-3xl text-nazar leading-tight">
        Nous trouver, nous appeler, commander.
      </h2>
    </div>

    <div class="grid lg:grid-cols-2 gap-10 md:gap-16">
      <div data-reveal>
        <div class="flex items-start gap-3 mb-6">
          <Icon name="map-pin" class="w-5 h-5 text-brique shrink-0 mt-1" />
          <div>
            <p class="font-semibold text-encre">{restaurant.adresse.texte}</p>
            <a
              href={restaurant.googleMapsItineraire}
              target="_blank"
              rel="noopener noreferrer"
              class="text-sm font-semibold text-brique hover:underline"
            >
              Obtenir l'itinéraire
            </a>
          </div>
        </div>

        <div class="flex items-start gap-3 mb-8">
          <Icon name="clock" class="w-5 h-5 text-brique shrink-0 mt-1" />
          <div>
            <p class="font-semibold text-encre">{horaires.texte}</p>
            <p class="text-sm text-encre/70">Sur place, à emporter, livraison Uber Eats</p>
          </div>
        </div>

        <iframe
          src={restaurant.googleMapsEmbed}
          title="Localisation d'Azur Grill Restaurant sur Google Maps"
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          class="w-full aspect-[4/3] rounded-2xl border border-encre/10"
        ></iframe>
      </div>

      <div data-reveal class="bg-nazar rounded-2xl p-6 sm:p-8 md:p-10 flex flex-col justify-center">
        <p class="text-creme/70 text-sm font-semibold uppercase tracking-[0.14em] mb-3">
          Nous appeler
        </p>
        <a
          href={restaurant.telephoneLien}
          class="font-display text-3xl sm:text-4xl lg:text-5xl text-creme hover:text-ciel transition-colors whitespace-nowrap"
        >
          {restaurant.telephone}
        </a>

        <div class="flex flex-wrap gap-3 mt-8">
          <a
            href={restaurant.telephoneLien}
            class="inline-flex items-center gap-2 bg-creme text-nazar font-semibold px-6 py-3.5 rounded-full hover:brightness-95 transition"
          >
            <Icon name="phone" class="w-4 h-4" />
            Appeler
          </a>
          <a
            href={restaurant.uberEatsUrl}
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 bg-brique text-creme font-semibold px-6 py-3.5 rounded-full hover:brightness-110 transition"
          >
            Commander
            <Icon name="external-link" class="w-4 h-4" />
          </a>
        </div>

        <p class="text-creme/60 text-sm mt-6">Halal · Ouvert 7j/7 · 11h30–22h30</p>
      </div>
    </div>
  </div>
</section>
```

## `src/components/CtaBand.astro`

```astro
---
import Icon from './Icon.astro';
import NazarCluster from './NazarCluster.astro';
import restaurant from '../data/restaurant.json';
---

<section class="relative isolate bg-nazar overflow-hidden py-20 md:py-28">
  <NazarCluster tone="dark" />
  <div class="max-w-3xl mx-auto px-5 md:px-8 text-center">
    <p data-reveal class="font-display italic text-ciel text-lg mb-4">On vous attend</p>
    <h2 data-reveal class="font-display text-creme text-3xl md:text-5xl leading-[1.05]">
      Une petite faim&nbsp;?
    </h2>
    <p data-reveal class="text-creme/80 text-lg mt-5 max-w-xl mx-auto">
      Commandez en ligne ou passez nous voir — le grill est déjà chaud.
    </p>

    <div data-reveal class="flex flex-wrap justify-center gap-3 mt-9">
      <a
        href={restaurant.uberEatsUrl}
        target="_blank"
        rel="noopener noreferrer"
        class="group inline-flex items-center gap-2 bg-brique text-creme font-semibold px-7 py-4 rounded-full hover:brightness-110 transition"
      >
        Commander sur Uber Eats
        <Icon name="arrow-right" class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
      </a>
      <a
        href={restaurant.telephoneLien}
        class="inline-flex items-center gap-2 bg-creme text-nazar font-semibold px-7 py-4 rounded-full hover:brightness-95 transition"
      >
        <Icon name="phone" class="w-4 h-4" />
        {restaurant.telephone}
      </a>
    </div>

    <p data-reveal class="text-creme/60 text-sm mt-7">
      {restaurant.adresse.texte} · Ouvert 7j/7 · 11h30 – 22h30
    </p>
  </div>
</section>
```

## `src/components/Footer.astro`

```astro
---
import Icon from './Icon.astro';
import NazarMark from './NazarMark.astro';
import restaurant from '../data/restaurant.json';

const currentYear = new Date().getFullYear();

const planDuSite = [
  { href: '/#a-propos', label: 'À propos' },
  { href: '/#carte', label: 'La Carte' },
  { href: '/#galerie', label: 'Galerie' },
  { href: '/#avis', label: 'Avis' },
  { href: '/#infos', label: 'Infos pratiques' },
];
---

<footer class="relative bg-nazar text-creme/80 overflow-hidden pt-16 pb-10 px-5 md:px-8">
  <NazarMark class="absolute -bottom-24 -right-24 w-96 h-96 text-creme opacity-[0.05]" />

  <div data-reveal class="relative max-w-6xl mx-auto grid sm:grid-cols-3 gap-10 mb-12">
    <div>
      <p class="font-display text-xl text-creme mb-3">Azur Grill Restaurant</p>
      <p class="text-sm leading-relaxed">{restaurant.adresse.texte}</p>
      <a href={restaurant.telephoneLien} class="text-sm hover:text-ciel transition-colors">{restaurant.telephone}</a>
    </div>

    <div>
      <p class="text-sm font-semibold uppercase tracking-[0.14em] text-creme/65 mb-3">Plan du site</p>
      <ul class="space-y-2">
        {planDuSite.map((link) => (
          <li><a href={link.href} class="text-sm hover:text-ciel transition-colors">{link.label}</a></li>
        ))}
      </ul>
    </div>

    <div>
      <p class="text-sm font-semibold uppercase tracking-[0.14em] text-creme/65 mb-3">Suivez-nous</p>
      <a
        href={restaurant.instagram}
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center gap-2 text-sm hover:text-ciel transition-colors"
      >
        <Icon name="instagram" class="w-4 h-4" />
        @azurgrillrestaurant
      </a>
    </div>
  </div>

  <div class="relative max-w-6xl mx-auto pt-6 border-t border-creme/10 text-xs text-creme/65">
    <p>© {currentYear} Azur Grill Restaurant — Tous droits réservés</p>
  </div>
</footer>
```

## `src/components/StickyMobileBar.astro`

```astro
---
import Icon from './Icon.astro';
import restaurant from '../data/restaurant.json';
---

<div
  class="md:hidden fixed bottom-0 inset-x-0 z-50 grid grid-cols-2 bg-nazar text-creme shadow-[0_-4px_16px_rgba(0,0,0,0.18)]"
  style="padding-bottom: env(safe-area-inset-bottom);"
>
  <a
    href={restaurant.telephoneLien}
    class="flex items-center justify-center gap-2 py-3.5 text-sm font-semibold border-r border-white/15 active:bg-white/10"
  >
    <Icon name="phone" class="w-4 h-4" />
    Appeler
  </a>
  <a
    href={restaurant.googleMapsItineraire}
    target="_blank"
    rel="noopener noreferrer"
    class="flex items-center justify-center gap-2 py-3.5 text-sm font-semibold active:bg-white/10"
  >
    <Icon name="map-pin" class="w-4 h-4" />
    Itinéraire
  </a>
</div>
```

## `src/components/ScrollReveal.astro`

```astro
<script>
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  gsap.registerPlugin(ScrollTrigger);

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Grouped reveals: elements inside [data-reveal-group] animate together, in DOM
  // order, off a single trigger on the group. Used where a CSS multi-column or
  // masonry layout would otherwise scatter individual elements' viewport
  // positions out of reading order.
  const groups = gsap.utils.toArray<HTMLElement>('[data-reveal-group]');
  const grouped = new Set<HTMLElement>();

  groups.forEach((group) => {
    const children = gsap.utils.toArray<HTMLElement>(group.querySelectorAll('[data-reveal]'));
    children.forEach((child) => grouped.add(child));

    if (reduceMotion) {
      gsap.set(children, { opacity: 1, y: 0 });
      return;
    }

    gsap.fromTo(
      children,
      { opacity: 0, y: 32 },
      {
        opacity: 1,
        y: 0,
        duration: 0.5,
        ease: 'power2.out',
        stagger: 0.08,
        scrollTrigger: {
          trigger: group,
          start: 'top 85%',
          toggleActions: 'play reverse play reverse',
          fastScrollEnd: true,
        },
      }
    );
  });

  // Individual reveals: everything else, each on its own trigger.
  const items = gsap.utils
    .toArray<HTMLElement>('[data-reveal]')
    .filter((el) => !grouped.has(el));

  if (reduceMotion) {
    gsap.set(items, { opacity: 1, y: 0 });
  } else {
    items.forEach((el) => {
      gsap.fromTo(
        el,
        { opacity: 0, y: 32 },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play reverse play reverse',
            fastScrollEnd: true,
          },
        }
      );
    });
  }

  // Safety net: very fast or repeated direction changes can occasionally leave a
  // tween interrupted mid-transition, out of sync with the element's actual
  // position (a known GSAP ScrollTrigger + smooth-scroll edge case). Rather than
  // trust scroll-driven events to catch every case, poll continuously and snap
  // anything mismatched back in line — cheap enough for this many elements, and
  // guarantees on-screen is always visible / off-screen is always hidden.
  if (!reduceMotion) {
    const allReveals = gsap.utils.toArray<HTMLElement>('[data-reveal]');

    setInterval(() => {
      allReveals.forEach((el) => {
        const rect = el.getBoundingClientRect();
        const onScreen = rect.top < window.innerHeight * 0.85 && rect.bottom > 0;
        const opacity = gsap.getProperty(el, 'opacity') as number;
        if (onScreen && opacity < 0.98) {
          gsap.to(el, { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out', overwrite: true });
        } else if (!onScreen && opacity > 0.02) {
          gsap.to(el, { opacity: 0, y: 32, duration: 0.3, ease: 'power2.out', overwrite: true });
        }
      });
    }, 200);
  }
</script>
```

## `src/components/SmoothScroll.astro`

```astro
<script>
  import gsap from 'gsap';
  import Lenis from 'lenis';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  gsap.registerPlugin(ScrollTrigger);

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!reduceMotion) {
    const lenis = new Lenis({
      duration: 1.1,
      easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    });

    // Keep ScrollTrigger perfectly in sync with Lenis's virtual scroll position —
    // without this, fast scrolling can desync the two and leave scroll-reveal
    // animations stuck mid-transition.
    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {
      lenis.raf(time * 1000);
    });
    gsap.ticker.lagSmoothing(0);
  }
</script>
```

## `src/components/Kicker.astro`

```astro
---
import NazarMark from './NazarMark.astro';

interface Props {
  number?: string;
  class?: string;
}

const { number, class: className = '' } = Astro.props;
---

<span class:list={['inline-flex items-center gap-2 text-sm font-semibold tracking-[0.18em] uppercase text-brique', className]}>
  <NazarMark class="w-4 h-4 text-brique" />
  {number && <span class="font-display italic text-brique/70 normal-case tracking-normal">{number}</span>}
  <slot />
</span>
```

## `src/components/Icon.astro`

```astro
---
interface Props {
  name: string;
  class?: string;
}

const { name, class: className = 'w-5 h-5' } = Astro.props;
const icons = import.meta.glob('/node_modules/lucide-static/icons/*.svg', {
  eager: true,
  query: '?raw',
  import: 'default',
}) as Record<string, string>;

const raw = icons[`/node_modules/lucide-static/icons/${name}.svg`];
if (!raw) throw new Error(`Icon "${name}" not found`);

const svg = raw.replace(/class="[^"]*"/, `class="${className}"`);
---

<Fragment set:html={svg} />
```

## `src/components/NazarMark.astro`

```astro
---
interface Props {
  class?: string;
}

const { class: className = 'w-4 h-4' } = Astro.props;
---

<svg viewBox="0 0 64 64" class={className} aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="32" r="31" fill="none" stroke="currentColor" stroke-width="2.5" />
  <circle cx="32" cy="32" r="21" fill="currentColor" opacity="0.18" />
  <circle cx="32" cy="32" r="12" fill="currentColor" opacity="0.55" />
  <circle cx="32" cy="32" r="5" fill="currentColor" />
</svg>
```

## `src/components/NazarCluster.astro`

```astro
---
interface Props {
  tone?: 'light' | 'dark';
  class?: string;
}

const { tone = 'light', class: className = '' } = Astro.props;

// Echoes the scattered nazar rings in the client's real logo — a handful of
// simple outlined circles at different sizes and heights, never a
// repeated/tiled pattern. Single stroke, single opacity per circle (avoid
// nesting inside components with their own internal opacity layers, which
// compounds into near-invisibility).
const primary = tone === 'dark' ? 'text-ciel' : 'text-nazar';
const accent = tone === 'dark' ? 'text-creme' : 'text-brique';
---

<div class:list={['absolute inset-0 overflow-hidden pointer-events-none -z-10', className]} aria-hidden="true">
  <svg class:list={['absolute top-[6%] -left-10 w-48 h-48 opacity-[0.3]', primary]} viewBox="0 0 64 64">
    <circle cx="32" cy="32" r="28" fill="none" stroke="currentColor" stroke-width="2.5" />
  </svg>
  <svg class:list={['absolute top-[42%] -right-16 w-56 h-56 opacity-[0.22]', primary]} viewBox="0 0 64 64">
    <circle cx="32" cy="32" r="29" fill="none" stroke="currentColor" stroke-width="2" />
  </svg>
  <svg class:list={['absolute bottom-[8%] left-[10%] w-20 h-20 opacity-[0.35]', accent]} viewBox="0 0 64 64">
    <circle cx="32" cy="32" r="27" fill="none" stroke="currentColor" stroke-width="4" />
  </svg>
</div>
```

## `src/data/restaurant.json`

```json
{
  "nom": "Azur Grill Restaurant",
  "cuisine": "Restaurant turc",
  "accroche": "Grillades généreuses, pain et kebab faits maison, à Épinay-sur-Seine.",
  "adresse": {
    "rue": "69 Bd Foch",
    "codePostal": "93800",
    "ville": "Épinay-sur-Seine",
    "pays": "France",
    "texte": "69 Bd Foch, 93800 Épinay-sur-Seine"
  },
  "geo": {
    "latitude": 48.9556,
    "longitude": 2.3111,
    "note": "[À VÉRIFIER] coordonnées approximatives calculées à partir de l'adresse postale"
  },
  "telephone": "01 86 04 22 42",
  "telephoneLien": "tel:+33186042242",
  "halal": true,
  "modes": ["Sur place", "À emporter", "Livraison"],
  "prixMoyen": "10–20 € / pers.",
  "prixRange": "€€",
  "uberEatsUrl": "https://www.ubereats.com/fr/store/azur-grill-restaurant/Ym7axLEcRvSDupKAmCFrxQ",
  "instagram": "https://www.instagram.com/azurgrillrestaurant",
  "googleMapsItineraire": "https://www.google.com/maps/dir/?api=1&destination=69+Bd+Foch+93800+%C3%89pinay-sur-Seine",
  "googleMapsEmbed": "https://www.google.com/maps?q=69+Bd+Foch+93800+%C3%89pinay-sur-Seine&output=embed",
  "avisGoogle": {
    "note": 4.6,
    "nombreAvis": 124,
    "citations": [
      { "texte": "Portions généreuses et viande vraiment fraîche, on sent le fait maison.", "note": 5 },
      { "texte": "Accueil chaleureux, le pain cuit sur place fait toute la différence.", "note": 5 },
      { "texte": "Rapport qualité-prix excellent pour Épinay, on y retourne sans hésiter.", "note": 5 }
    ]
  },
  "seoLocal": {
    "titre": "Azur Grill Restaurant — Restaurant turc halal à Épinay-sur-Seine",
    "description": "Kebab et pain faits maison, viandes grillées, desserts turcs artisanaux. Restaurant turc halal à Épinay-sur-Seine, ouvert 7j/7 de 11h30 à 22h30. Sur place, à emporter ou en livraison.",
    "motsCles": ["restaurant turc Épinay-sur-Seine", "kebab Épinay-sur-Seine", "restaurant halal Épinay-sur-Seine"]
  }
}
```

## `src/data/horaires.json`

```json
{
  "texte": "Ouvert 7j/7 · 11h30 – 22h30",
  "jours": [
    { "jour": "Lundi", "horaire": "11h30 – 22h30" },
    { "jour": "Mardi", "horaire": "11h30 – 22h30" },
    { "jour": "Mercredi", "horaire": "11h30 – 22h30" },
    { "jour": "Jeudi", "horaire": "11h30 – 22h30" },
    { "jour": "Vendredi", "horaire": "11h30 – 22h30" },
    { "jour": "Samedi", "horaire": "11h30 – 22h30" },
    { "jour": "Dimanche", "horaire": "11h30 – 22h30" }
  ],
  "schemaOrgOpeningHours": ["Mo-Su 11:30-22:30"]
}
```

## `src/data/menu.json`

```json
[
  {
    "categorie": "Entrées froides",
    "plats": [
      { "nom": "Houmous", "prix": 3.5, "description": "Purée de pois chiche, tahin, huile d'olive" },
      { "nom": "Ezme", "prix": 3.5, "description": "Tomates, persil, concombre, oignons" },
      { "nom": "Patlican", "prix": 3.5, "description": "Aubergines fumées au grill, huile d'olive, ail, jus de citron" },
      { "nom": "Haydari", "prix": 3.5, "description": "Concombre, yaourt, ail" }
    ]
  },
  {
    "categorie": "Entrées chaudes",
    "plats": [
      { "nom": "Lahmacun", "prix": 3.5, "description": "Pizza turque à la viande hachée" },
      { "nom": "Pide", "prix": 2, "description": "Pain turc nature" }
    ]
  },
  {
    "categorie": "Plats",
    "plats": [
      { "nom": "Döner Kebab", "prix": 13, "description": "Lamelles de veau ou poulet marinées cuites sur broche" },
      { "nom": "Köfte", "prix": 13, "description": "Boulettes de bœuf haché assaisonnées" },
      { "nom": "Brochette de Poulet", "prix": 14, "description": "" },
      { "nom": "Brochette d'Agneau", "prix": 14, "description": "" },
      { "nom": "Adana", "prix": 13.5, "description": "Bœuf haché assaisonné" },
      { "nom": "Côtelettes d'Agneau", "prix": 16, "description": "" },
      { "nom": "Spécialité du Chef", "prix": 20, "description": "Brochette de poulet, brochette d'agneau et adana" },
      { "nom": "Azur", "prix": 16, "description": "Lamelles de veau et 3 köfte" },
      { "nom": "Poulet Curry", "prix": 13, "description": "" },
      { "nom": "Mixte", "prix": 18, "description": "Côtelette, kebab, brochette de poulet, brochette d'agneau, köfte" },
      { "nom": "Vegan", "prix": 9, "description": "Boulgour, frites, crudités" }
    ]
  },
  {
    "categorie": "Sandwichs",
    "note": "Avec frites : +1 €",
    "plats": [
      { "nom": "Döner Kebab", "prix": 8.5, "description": "" },
      { "nom": "Köfte", "prix": 9.5, "description": "" },
      { "nom": "Brochette de Poulet", "prix": 8.5, "description": "" },
      { "nom": "Brochette d'Agneau", "prix": 8.5, "description": "" },
      { "nom": "Adana", "prix": 9.5, "description": "" },
      { "nom": "Kebab Steak", "prix": 9, "description": "" },
      { "nom": "Spécialité du Chef", "prix": 9, "description": "Veau, poivrons, oignons" },
      { "nom": "Poulet Curry avec Köfte ou Kebab", "prix": 9, "description": "" },
      { "nom": "Poulet Curry", "prix": 8.5, "description": "" },
      { "nom": "Kebab Mixte", "prix": 9.5, "description": "Veau et poulet" },
      { "nom": "2 Steaks", "prix": 8.5, "description": "" },
      { "nom": "Merguez", "prix": 8.5, "description": "" },
      { "nom": "Cordon Bleu", "prix": 8.5, "description": "" },
      { "nom": "Americain", "prix": 9, "description": "2 steaks, fromage, œuf" },
      { "nom": "Lahmacun Kebab", "prix": 9, "description": "" }
    ]
  },
  {
    "categorie": "Formules & Burgers",
    "note": "Servis avec frites et boisson",
    "plats": [
      { "nom": "Formule Azur", "prix": 13.5, "description": "Sandwich kebab, cheeseburger, frites et boisson" },
      { "nom": "Chicken Burger", "prix": 7.5, "description": "" },
      { "nom": "Cheese Burger", "prix": 7, "description": "" },
      { "nom": "Double Cheese Burger", "prix": 8.5, "description": "" },
      { "nom": "Nuggets Gourmands", "prix": 7, "description": "6 nuggets, frites, boisson" },
      { "nom": "Menu Enfant", "prix": 5.5, "description": "Steak, nuggets ou hamburger, frites, Capri-Sun et Kinder Surprise" }
    ]
  },
  {
    "categorie": "Desserts",
    "plats": [
      { "nom": "Baklava", "prix": 3, "description": "Pâte croustillante, noix, pistaches d'Antep, sirop" },
      { "nom": "Künefe", "prix": 8.5, "description": "Pâte de kadayif, fromage doux, sirop, glace de Maraş" },
      { "nom": "Tiramisu", "prix": 3.5, "description": "" },
      { "nom": "Tarte au Daim", "prix": 3.5, "description": "" },
      { "nom": "Sütlaç", "prix": 3.5, "description": "Riz au lait vanillé caramélisé" },
      { "nom": "Revani", "prix": 3.5, "description": "Gâteau à la semoule, sirop, pistaches" },
      { "nom": "Trileçe", "prix": 3.5, "description": "Gâteau trois laits, caramel" }
    ]
  },
  {
    "categorie": "Boissons",
    "plats": [
      { "nom": "Sodas", "prix": 1.5, "description": "" },
      { "nom": "Eau", "prix": 1, "description": "" },
      { "nom": "Thé turc", "prix": 1.5, "description": "" },
      { "nom": "Café expresso", "prix": 1.5, "description": "" },
      { "nom": "Café turc", "prix": 5, "description": "Moulu fin, préparé au cezve, non filtré" }
    ]
  }
]
```

## `src/env.d.ts`

```ts
/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />
```

## `public/favicon.svg`

```xml
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="32" r="32" fill="#16098F"/>
  <circle cx="32" cy="32" r="24" fill="#FAF8F4"/>
  <circle cx="32" cy="32" r="17" fill="#74C0EC"/>
  <circle cx="32" cy="32" r="9" fill="#FAF8F4"/>
  <circle cx="32" cy="32" r="4.5" fill="#16098F"/>
</svg>
```

---

## Notes

- **Photos** : non incluses dans ce document (binaires). Elles vivent dans `src/assets/photos-v2/` et sont référencées par les imports en haut des composants Hero, About et Gallery.
- **`PhotoPlaceholder.astro`** existe encore dans le projet mais n_est plus utilisé (il servait avant l_arrivée des vraies photos) — supprimable.
- **Contenu éditable sans toucher au code** : `src/data/menu.json` (carte), `horaires.json`, `restaurant.json` (adresse, téléphone, avis Google, liens).
- **Palette** : définie une seule fois dans `tailwind.config.mjs`, extraite au pixel près du logo client (#16098F nazar, #74C0EC ciel).
