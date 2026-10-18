# Trailblazers of History

**Celebrating Women and People of Color Who Changed the World.** This is a static digital museum built for the GitHub Pages project path `/trailblazers-website/`. The collection contains **80 reviewed profiles** with 168 source citations. The 100-profile milestone is **not yet complete**. Another 20 people are listed in a separate, unpublished discovery queue; names on that list are not presented as researched biographies.

## Run locally

Requires Python 3.10+ and Node.js for the JavaScript behavior test. There are no runtime package dependencies.

```sh
npm run validate
npm test
npm run build
BASE_PATH=/ python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

The default build writes `dist/` with `/trailblazers-website/` URLs. Set `BASE_PATH=/` for a local root preview; restore the default build before packaging for GitHub Pages. `npm run milestone` deliberately fails until 100 unique publishable records pass validation.

## Add a profile

Add one object to `content/profiles.json` using the fields described in [content guidelines](docs/content-guidelines.md). Add two independent credible source links, write an original 150–300 word biography, record a review date, and run validation. `content/pending.json` is a research queue and never appears on the public site. Rights-cleared image metadata is optional; null produces a typographic placeholder. Sixteen portraits currently have file-specific rights records. UI components need no edits.

## Browser review

The optional [browser-review workflow](.github/workflows/browser-review.yml) builds and serves the production project path without deploying it. A feature-branch push touching site files or a manual **Run workflow** starts Chromium checks at desktop, tablet, and mobile widths, runs axe accessibility checks, and uploads screenshots, traces, and an HTML report as an artifact. It requests read-only repository permission and no secrets. See [deployment and browser review instructions](docs/deployment.md) for local reproduction. Browser results are pending until the workflow runs in an environment with network and browser support.

## Project state

The original Cocoa HTML is retained in Git history. The decoded source and a profile-by-profile migration inventory are in `legacy/`. The new static architecture, research method, deployment procedure, and current gaps are documented in `docs/`. No deployment workflow is enabled, and the `feature/museum-foundation` branch is intended for review only. The draft PR text is in `docs/draft-pr.md`; automatic PR creation was blocked by the connected app’s permissions. Research decisions and browser-review status are in `docs/progress-report.md`.
