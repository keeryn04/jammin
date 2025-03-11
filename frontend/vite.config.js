import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    host: '0.0.0.0',  
    port: 5173,        
    hmr: {
      clientPort: 5173,
    }, 
    watch: {
    usePolling: true,
    },
    proxy: {
    // Proxy API requests to Flask backend on port 5000
    '/api': {
      target: 'http://localhost:5000',  // Flask backend URL
      changeOrigin: true,
      secure: false,
      ws: true, // Enable WebSocket support if needed
    },
    '/spotify': {
      target: 'http://localhost:5000',  // Flask backend URL
      changeOrigin: true,
      secure: false,
      ws: true, // Enable WebSocket support if needed
    }
  }},
  build: {
    rollupOptions: {
      input: '/index.html'
    }
  },
})
