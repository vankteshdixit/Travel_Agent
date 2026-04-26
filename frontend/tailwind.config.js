/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#020617",
        secondary: "#0f172a",
        card: "rgba(255,255,255,0.08)",
        accent: "#38bdf8",
        accentDark: "#0ea5e9",
        success: "#22c55e",
        danger: "#ef4444",
        warning: "#f59e0b",
      },

      boxShadow: {
        glow: "0 0 30px rgba(56,189,248,0.25)",
        card: "0 8px 32px rgba(0,0,0,0.35)",
      },

      borderRadius: {
        xl2: "1.25rem",
      },

      backdropBlur: {
        xs: "2px",
      },

      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },

      backgroundImage: {
        hero: "linear-gradient(135deg, #020617 0%, #0f172a 45%, #082f49 100%)",
      },

      animation: {
        float: "float 5s ease-in-out infinite",
        pulseSlow: "pulse 3s infinite",
      },

      keyframes: {
        float: {
          "0%, 100%": {
            transform: "translateY(0px)",
          },
          "50%": {
            transform: "translateY(-10px)",
          },
        },
      },
    },
  },
  plugins: [],
}