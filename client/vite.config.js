import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'
export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
  envDir: path.resolve(__dirname, '..'),
})