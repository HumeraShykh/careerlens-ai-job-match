/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        sans: ["Plus Jakarta Sans", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Plus Jakarta Sans", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        ink: {
          950: "#152033",
          900: "#1E2B45",
          700: "#44506A",
          500: "#6B7890",
        },
        brand: {
          50: "#EEF3FF",
          100: "#DCE6FF",
          500: "#4F7CFF",
          600: "#3D68F0",
          700: "#3B4FD4",
        },
        teal: {
          500: "#14B8A6",
          600: "#0D9488",
        },
      },
      boxShadow: {
        card: "0 18px 50px -24px rgba(47, 72, 160, 0.4)",
        glow: "0 10px 24px -12px rgba(79, 124, 255, 0.8)",
      },
    },
  },
  plugins: [],
};
