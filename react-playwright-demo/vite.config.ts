import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load environment variables
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react()],
    server: {
      port: 8081,
      strictPort: false, // Allow fallback to next available port
      host: true
    },
    define: {
      // Make environment variables available to the app
      'import.meta.env.VITE_APP_ENV': JSON.stringify(env.VITE_APP_ENV || mode),
    },
    build: {
      // Environment-specific build optimizations
      minify: mode === 'production' ? 'esbuild' : false,
      sourcemap: mode !== 'production',
      rollupOptions: {
        output: {
          // Add environment suffix to build files in non-production
          entryFileNames: mode === 'production' 
            ? 'assets/[name]-[hash].js' 
            : `assets/[name]-${mode}-[hash].js`,
          chunkFileNames: mode === 'production' 
            ? 'assets/[name]-[hash].js' 
            : `assets/[name]-${mode}-[hash].js`,
          assetFileNames: mode === 'production' 
            ? 'assets/[name]-[hash].[ext]' 
            : `assets/[name]-${mode}-[hash].[ext]`,
        },
      },
    },
  }
})
