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
