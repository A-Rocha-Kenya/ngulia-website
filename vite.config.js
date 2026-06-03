import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: './',
  optimizeDeps: {
    noDiscovery: true,
    include: ['@deck.gl/core', '@deck.gl/layers', '@deck.gl/mapbox', 'earcut', 'mapbox-gl']
  }
})
