# Trailblazers of History

**Celebrating Women and People of Color Who Changed the World.** This is a static digital museum built for the GitHub Pages project path `/trailblazers-website/`. The collection contains **100 verified profiles** with 211 source citations. The first 100-profile milestone is complete; the candidate queue is empty pending the next research batch.

## Run locally

Requires Python 3.10+ and Node.js for the JavaScript behavior test. There are no runtime package dependencies.

```sh
npm run validate
npm test
npm run build
npm run audit:links
BASE_PATH=/ python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

The default build writes `dist/` with `/trailblazers-website/` URLs. Set `BASE_PATH=/` for a local root preview; restore the default build before packaging for GitHub Pages. `npm run milestone` deliberately fails until 100 unique publishable records pass validation.

`npm run audit:links` checks all citation, portrait-asset, and portrait-rights URLs in a network-enabled environment. It writes an ignored `external-link-report.json`; access restrictions and network failures are reported separately from confirmed 404/410 links.

## Add a profile

Add one object to `content/profiles.json` using the fields described in [content guidelines](docs/content-guidelines.md). Add two independent credible source links, write an original 150–300 word biography, record a review date, and run validation. `content/pending.json` is a research queue and never appears on the public site. Rights-cleared image metadata is optional; null produces a typographic placeholder. Sixteen portraits currently have file-specific rights records; other profiles use placeholders. UI components need no edits.

## Browser review

The optional [browser-review workflow](.github/workflows/browser-review.yml) builds and serves the production project path without deploying it. A feature-branch push touching site files, tests, documentation, or the workflow starts Chromium checks at desktop, tablet, and mobile widths, runs axe accessibility checks, and uploads screenshots, traces, and an HTML report as an artifact. It requests read-only repository permission and no secrets. It uses Node 22 for compatibility with the current axe package. The category tiles are generated from the collection, and portrait placeholders use initials without synthetic imagery. See [deployment and browser review instructions](docs/deployment.md) for local reproduction. Run `39104859860` passed all 9 browser cases on commit `09ad3dc1e46eff9de221fb37ffba7f50e5ccc8c5`; its artifact is uploaded, but local DNS blocks opening the signed download for pixel-level review. A final browser run is required after release-preparation changes.

## Project state

The original Cocoa HTML is retained in Git history. The decoded source and a profile-by-profile migration inventory are in `legacy/`. The new static architecture, research method, deployment procedure, and current gaps are documented in `docs/`. No deployment workflow is enabled, and the `feature/museum-foundation` branch is intended for review only. The draft PR text is in `docs/draft-pr.md`; automatic PR creation was blocked by the connected app’s permissions. Research decisions and browser-review status are in `docs/progress-report.md`.
