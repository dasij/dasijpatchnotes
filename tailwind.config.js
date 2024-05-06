/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
      ],
      theme: {
        extend: {
          backgroundImage: {
            'hots-repeat': "url('@/assets/background-hots-bg.jpg')",
            'heroes-page-container': "url('@/assets/heroes_page_background.webp')",
          },
        },
      },
      plugins: [],
    }

