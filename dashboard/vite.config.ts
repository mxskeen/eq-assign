import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@traces': path.resolve(__dirname, '../traces')
    }
  },
  server: {
    fs: {
      allow: ['..']
    }
  }
})
