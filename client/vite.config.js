import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '../', 'VITE_')
  const vuePort = parseInt(env.VITE_PORT) || 5173

  return {
    plugins: [
      vue(), 
      vueDevTools(), 
      tailwindcss(),
      VitePWA({
        registerType: 'prompt', // Inline update prompts for mobile-first
        includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
        manifest: {
          name: 'Foolstack',
          short_name: 'Foolstack',
          theme_color: 'oklch(0.14 0.01 265)',
          background_color: 'oklch(0.14 0.01 265)',
          display: 'standalone',
          display_override: ['window-controls-overlay'],
          shortcuts: [
            {
              name: "Dashboard",
              url: "/",
              icons: [{ src: "pwa-192x192.png", sizes: "192x192" }]
            }
          ],
          icons: [
            { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },
            { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' },
            { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' }
          ]
        },
        workbox: {
          globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
          // Enable navigation preload
          navigationPreload: true,
          runtimeCaching: [
            {
              // Necessary when navigationPreload is true
              urlPattern: ({ request }) => request.mode === 'navigate',
              handler: 'NetworkFirst',
              options: {
                cacheName: 'navigations',
                networkTimeoutSeconds: 10,
              },
            },
            // Cache Google Fonts
            {
              urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
              handler: 'CacheFirst',
              options: {
                cacheName: 'google-fonts-cache',
                expiration: { maxEntries: 10, maxAgeSeconds: 60 * 60 * 24 * 365 },
                cacheableResponse: { statuses: [0, 200] }
              }
            },
            {
              urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
              handler: 'CacheFirst',
              options: {
                cacheName: 'gstatic-fonts-cache',
                expiration: { maxEntries: 20, maxAgeSeconds: 60 * 60 * 24 * 365 },
                cacheableResponse: { statuses: [0, 200] }
              }
            }
          ]
        }
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      host: '0.0.0.0',
      port: vuePort,
    },
  }
})
