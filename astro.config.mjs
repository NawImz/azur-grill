import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

/*
  Deux destinations possibles, d'ou la configuration par variables :

  - GitHub Pages, en previsualisation : servi sous /azur-grill/, donc `base`
    doit etre renseigne sinon tous les chemins pointent hors du site.
  - Le domaine definitif du restaurant, le jour venu : `base` disparait et
    seul `site` change.

  Les liens internes passent par src/lib/url.ts, qui lit BASE_URL : rien
  d'autre n'a besoin de bouger d'une destination a l'autre.
*/
const SITE = process.env.SITE_URL ?? 'https://azur-grill-epinay.fr';
const BASE = process.env.BASE_PATH ?? undefined;

export default defineConfig({
  site: SITE,
  base: BASE,
  vite: {
    plugins: [tailwindcss()],
  },
});
