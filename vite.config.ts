import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
	plugins: [
		sveltekit(),
		tailwindcss()
	],
	server: {
		fs: {
			strict: false
		},
		watch: {
			ignored: ['**/node_modules/**', '**/.git/**']
		},
		hmr: {
			overlay: false
		}
	},
	optimizeDeps: {
		include: ['highlight.js', 'marked', 'dompurify'],
		exclude: ['@sveltejs/kit', 'svelte']
	},
	build: {
		minify: 'terser',
		sourcemap: false,
		rollupOptions: {
			cache: true,
			output: {
				manualChunks(id) {
					if (id.includes('node_modules')) {
						if (id.includes('svelte')) {
							return 'vendor';
						}
						if (id.includes('highlight.js') && !id.includes('marked')) {
							return 'markdown';
						}
						if (id.includes('dompurify')) {
							return 'utils';
						}
					}
				}
			}
		},
		chunkSizeWarningLimit: 1600,
	},
	define: {
		'process.env.NODE_ENV': '"development"'
	}
});
