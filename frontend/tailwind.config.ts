import type { Config } from "tailwindcss";
const config: Config = { content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}"], theme: { extend: { colors: { ink: "#080D16", panel: "#101927", line: "#1E2B3B", mint: "#4DE0C1" }, boxShadow: { glow: "0 0 50px rgba(77,224,193,.10)" } } }, plugins: [] };
export default config;
