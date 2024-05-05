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
          },
        },
      },
      plugins: [],
    }

