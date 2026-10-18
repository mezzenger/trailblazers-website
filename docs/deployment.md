# Deployment (review only)

No Pages workflow or live setting is enabled by this branch. Do not publish without the owner's explicit approval. The repository name requires the project subpath `/trailblazers-website/`, which is the default in `scripts/build.py`.

Before any authorized deployment, run `npm run validate`, `npm test`, `npm run build`, and `npm run milestone`. The 100-profile gate passes only when 100 unique verified records satisfy the content schema; the current collection has reached 100. Inspect `dist/index.html`, `dist/people/`, and `dist/.nojekyll`; test on desktop and mobile browsers; then configure an approved GitHub Pages artifact upload from `dist/` or use an approved `gh-pages` branch. Do not deploy the old root `index.html`; it is intentionally replaced by the generated result in `dist/`.

For local preview: `BASE_PATH=/ python3 scripts/build.py` and `python3 -m http.server 8000 --directory dist`, then visit `http://localhost:8000/`. Rebuild without `BASE_PATH` for the project URL.

## Review-only browser checks

`.github/workflows/browser-review.yml` is a separate, optional review job on the feature branch. It never uploads a Pages artifact or changes publication settings. It builds the default project-path output, serves a copy at `/trailblazers-website/`, checks collection behavior and profile routing in Chromium at desktop, tablet, and mobile sizes, runs axe checks in both themes, and uploads screenshot, trace, and HTML-report artifacts for 14 days. Open **Actions → Browser review (no deployment) → Run workflow** on `feature/museum-foundation`, or inspect the run triggered by a site-file push. Download the `browser-review-<run ID>` artifact even if the test step fails. A workflow-file push may need a token with workflow permission; an owner can add the workflow file through GitHub if that permission is unavailable. No workflow run or screenshots are claimed until the Actions run completes.

The Phase 3D review trigger is a feature-branch push that changes content, the builder, tests, or the workflow. Download its artifact even on failure. Do not describe a queued run as passed. If the repository Actions page or API is inaccessible, record that limitation and resume review when it is reachable. No workflow run or screenshots are claimed until the Actions run completes.

For local reproduction on a machine with browser and loopback access:

```sh
npm run build
npm install --no-save --package-lock=false --ignore-scripts @playwright/test@1.64.0 @axe-core/playwright@4.14.0
npx playwright install chromium
npx playwright test --config=playwright.config.mjs
```

The browser server stages `dist/` under `.browser-preview/trailblazers-website/` before testing, so this checks the production URL shape. The temporary files, screenshots, and report are ignored by Git.
