# Lumina studio showcase

The interactive study moved from the personal portfolio to EdenTV. The scene is a React/Three.js demonstration of visual styles and design principles, separate from the framework-independent @xlumina/system package.

Build from this directory with `npm ci && npm run build`. Commit the source, lockfile, and generated `assets/lumina` files together. The static entry page is `pages/lumina.html`; run `python3 scripts/build_documents.py` from the repository root after page changes to refresh canonical metadata and the sitemap. Only static assets are deployed, never this source directory or node_modules.
