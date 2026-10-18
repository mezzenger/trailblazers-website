# Deployment (review only)

No Pages workflow or live setting is enabled by this branch. Do not publish without the owner's explicit approval. The repository name requires the project subpath `/trailblazers-website/`, which is the default in `scripts/build.py`.

Before any authorized deployment, run `npm run validate`, `npm test`, `npm run build`, and `npm run milestone`. The milestone command is currently expected to fail because only 14 of 100 records are verified. Inspect `dist/index.html`, `dist/people/`, and `dist/.nojekyll`; test on desktop and mobile browsers; then configure an approved GitHub Pages artifact upload from `dist/` or use an approved `gh-pages` branch. Do not deploy the old root `index.html`; it is intentionally replaced by the generated result in `dist/`.

For local preview: `BASE_PATH=/ python3 scripts/build.py` and `python3 -m http.server 8000 --directory dist`, then visit `http://localhost:8000/`. Rebuild without `BASE_PATH` for the project URL.
