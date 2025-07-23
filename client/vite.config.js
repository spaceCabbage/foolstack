import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '../', '')
  const baseDomain = env.BASE_DOMAIN || 'localhost'
  const isDevelopment = env.ENVIRONMENT === 'development'
  const vuePort = parseInt(env.VUE_PORT) || 5173
  const serverPort = parseInt(env.DJANGO_PORT) || 8000
  const logLevel = env.LOG_LEVEL || 'INFO'
  const serverBaseUrl = isDevelopment
    ? `http://api.${baseDomain}:${serverPort}`
    : `https://api.${baseDomain}`

  return {
    plugins: [vue(), vueDevTools(), tailwindcss()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      host: '0.0.0.0',
      port: vuePort,
      proxy: {
        '/api': {
          target: isDevelopment ? `http://server:${serverPort}` : serverBaseUrl,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(serverBaseUrl),
      'import.meta.env.VITE_LOG_LEVEL': JSON.stringify(logLevel),
    },
  }
})
