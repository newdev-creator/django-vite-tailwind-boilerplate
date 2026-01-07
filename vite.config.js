import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "path";

export default defineConfig({
  plugins: [tailwindcss()],
  base: "/static/",
  root: resolve(__dirname, "./src"),
  build: {
    outDir: resolve(__dirname, "./src/static"),
    emptyOutDir: false,
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        index: resolve(__dirname, "./src/assets/index.js"),
        style: resolve(__dirname, "./src/assets/style.css"),
      },
      output: {
        entryFileNames: `js/[name]-bundle.js`,
        assetFileNames: `css/[name].css`,
      },
    },
  },
});
