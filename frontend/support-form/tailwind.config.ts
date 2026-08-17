import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#D1F470',
          hover: '#C3E85F',
        },
        secondary: '#11110D',
        tertiary: '#000000',
        neutral: '#FFFFFF',
        surface: '#F7F7F5',
        border: '#E5E7EB',
        muted: '#6B7280',
        error: '#D92D20',
        overlay: '#11110D',
      },
      fontFamily: {
        sans: ['var(--font-dm-sans)', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        none: '0px',
        sm: '4px',
        DEFAULT: '8px',
        lg: '16px',
        xl: '24px',
        full: '9999px',
      },
      spacing: {
        xs: '2px',
        sm: '12px',
        md: '20px',
        lg: '32px',
        xl: '76px',
        gutter: '24px',
        margin: '32px',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
