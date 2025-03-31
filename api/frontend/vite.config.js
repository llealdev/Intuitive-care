import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url' // Mais moderno que 'path'

export default defineConfig({
  plugins: [vue()],
  publicDir: 'public',
  server: {
    host: true, // Expõe para a rede local (ex: acessível via IP)
    port: 5000,
    strictPort: true,
    open: false, // Melhor para prod (evita abrir navegador automaticamente)
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)), // Padrão ESM
      '@components': fileURLToPath(new URL('./src/components', import.meta.url)) // Exemplo de alias extra
    }
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    assetsInlineLimit: 4096, // Arquivos < 4KB viram base64
    chunkSizeWarningLimit: 1000, // Ajusta limite de warnings
    rollupOptions: {
      output: {
        manualChunks: {
          // Separa bibliotecas em chunks (melhora caching)
          vue: ['vue', 'vue-router', 'pinia'],
          axios: ['axios']
        }
      }
    }
  },
  optimizeDeps: {
    include: ['vue', 'vue-router'] // Pré-empacota dependências
  }
})