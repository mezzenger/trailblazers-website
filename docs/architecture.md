# Architecture

This is a dependency-free static site. The source repository was a single Cocoa-escaped HTML file; adding a framework would require a package install for a small collection with no server needs. `scripts/build.py` generates the home page, one canonical path per person (`people/<id>/`), and a 404 page from structured JSON. `public/styles.css` holds design tokens and responsive rules. `public/app.js` controls the theme, collection UI, timeline range, and share action. Pure search and sorting functions live in `public/filter-core.mjs` and are exercised from Node in tests.

All profile content is in `content/profiles.json`. The generated cards embed the same records used to build the detail pages, so search and filters cannot drift from the published collection. The build escapes content before putting it into HTML or attributes. `content/pending.json` is never loaded by the builder. Related stories are ranked by shared categories, then name. Trailblazer of the Day is stable for a calendar day based on the build date; rebuilding daily rotates it.

The default base path is `/trailblazers-website/`. `BASE_PATH=/` builds root paths for local preview. `dist/` is ignored and contains only generated artifacts. The site has no backend, tracking, cookies, or paid API. Google Fonts are an optional enhancement; Georgia and Arial are local fallbacks.
