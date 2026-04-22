# PWA Asset Setup Instructions (2026)

To complete the PWA integration and ensure a "native" feel with perfect branding, you need to generate a specific set of assets. 

## 1. Required Assets
Place these in `client/public/`:

- `favicon.ico`: 32x32 standard icon.
- `apple-touch-icon.png`: 180x180 icon for iOS home screens.
- `mask-icon.svg`: A monochrome SVG icon for Safari pinned tabs.
- `pwa-192x192.png`: 192x192 icon for Android/Chrome.
- `pwa-512x512.png`: 512x512 icon for splash screens.

## 2. Brand Colors
Your current brand background is: `oklch(0.14 0.01 265)`
Use this color for the background of your splash screens and the safe-area padding in your design.

## 3. Generation Tool (Recommended)
Use a modern PWA asset generator (like `pwa-asset-generator` or `vite-pwa` CLI tools) to create these from a single high-resolution source SVG.

Example command for 2026:
```bash
npx pwa-asset-generator logo.svg client/public/ --background "oklch(0.14 0.01 265)" --padding "10%"
```

## 4. Manifest Checklist
The `client/vite.config.js` is already configured with:
- `display_override: ["window-controls-overlay"]` (Desktop edge-to-edge)
- `theme_color` and `background_color` matching your brand.
- Maskable icon support (ensure your `pwa-512x512.png` has enough padding).

## 5. Deployment Note
Prerendering is disabled in favor of a standard SPA with optimized meta-tags (2026 standard for high-performance crawlers). Verify your SEO in production using modern tools.
