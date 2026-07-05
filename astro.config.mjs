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
