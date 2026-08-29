import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://azur-grill-epinay.fr',
  vite: {
    plugins: [tailwindcss()],
  },
});
