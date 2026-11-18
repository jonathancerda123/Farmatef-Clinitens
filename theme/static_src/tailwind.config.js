module.exports = {
  theme: { extend: {
    colors: {
      brand: {
        50: 'rgb(var(--color-primary-soft) / <alpha-value>)',
        100: '#d2eeee', 200: '#a9dddd', 300: '#6ec9cc', 400: '#0cb3b7',
        500: '#098386', 600: 'rgb(var(--color-primary) / <alpha-value>)',
        700: 'rgb(var(--color-primary-hover) / <alpha-value>)',
        800: 'rgb(var(--color-navigation) / <alpha-value>)',
        900: 'rgb(var(--color-ink) / <alpha-value>)', 950: '#202727',
      },
    },
  } },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
