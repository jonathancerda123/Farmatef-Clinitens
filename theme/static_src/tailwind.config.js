module.exports = {
  theme: { extend: {
    colors: {
      brand: {
        50: 'rgb(var(--color-primary-soft) / <alpha-value>)',
        100: '#d3eee6', 200: '#a9dacc', 300: '#76bdab', 400: '#449e8e',
        500: '#138477', 600: 'rgb(var(--color-primary) / <alpha-value>)',
        700: 'rgb(var(--color-primary-hover) / <alpha-value>)',
        800: '#17474e', 900: '#19363c', 950: '#10282d',
      },
    },
  } },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
