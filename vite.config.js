import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "path";

export default defineConfig({
  plugins: [tailwindcss()],
  base: "/static/",
  root: resolve(__dirname, "./"),
  build: {
    outDir: resolve(__dirname, "./static"),
    emptyOutDir: true,
    manifest: "true",
    rollupOptions: {
      input: {
        index: resolve(__dirname, "./assets/main.js"),
        style: resolve(__dirname, "./assets/style.css"),
      },
      output: {
        entryFileNames: "[name]-[hash].js",
        chunkFileNames: "[name]-[hash].js",
        assetFileNames: "[name]-[hash][extname]",
      },
    },
    assetsDir: "",
  },
});
