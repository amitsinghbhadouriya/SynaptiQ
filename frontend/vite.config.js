import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// `base: './'` keeps asset URLs relative, so the same build works when Streamlit serves it as a
// custom component (under /component/...) and when FastAPI serves it at the site root.
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    chunkSizeWarningLimit: 4000,
    rollupOptions: {
      output: {
        manualChunks: {
          plotly: ['plotly.js-basic-dist-min'],
          three: ['three'],
          gsap: ['gsap']
        }
      }
    }
  },
  server: {
    port: 5173,
    proxy: { '/api': 'http://127.0.0.1:8000' }
  }
});

