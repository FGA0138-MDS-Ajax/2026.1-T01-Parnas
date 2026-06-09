import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
      },
      '/auth': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
      },
      '/company': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  test: {
    globals: true,            // describe/it/expect sem precisar importar
    environment: 'jsdom',     // DOM simulado pra renderizar componentes React
    setupFiles: './src/test/setup.js', // matchers do jest-dom (toBeInTheDocument...)
    css: true,                // não quebra ao importar .css nos componentes
  },
});