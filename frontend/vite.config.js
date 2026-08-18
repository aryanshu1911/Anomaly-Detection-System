import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // All /api/* requests are forwarded to the FastAPI backend.
      // The /api prefix is stripped before forwarding, so:
      //   /api/alerts  →  http://127.0.0.1:8000/alerts
      //   /api/alerts/ALT-XXXX  →  http://127.0.0.1:8000/alerts/ALT-XXXX
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
