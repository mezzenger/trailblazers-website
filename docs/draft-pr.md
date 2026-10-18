# Draft pull request: Museum foundation and 54 reviewed profiles

## Summary

Continues the review-only digital museum on `feature/museum-foundation`. Phase 3B promotes 20 researched biographies from the unpublished queue, adds eight file-reviewed portraits (including four on existing profiles), and fixes search initialization, unknown-date handling, and contrast issues found during a static accessibility review. The original Cocoa-escaped page and migration inventory remain in `legacy/`.

## Content status

- 54 verified publishable profiles; 115 source citations from at least two independent domains per profile.
- 46 discovery candidates remain unpublished.
- Eleven portraits have file-specific creator, source, rights basis, and attribution metadata; other profiles use typographic placeholders.
- The 100-profile milestone remains unmet by 46 records; `npm run milestone` must fail until the researched collection reaches 100.

## Checks

- `npm run validate` — pass, zero schema/content errors.
- `npm test` — seven tests pass, including internal routes, base path, live client-script filter behavior, unknown dates, semantics, contrast, and milestone enforcement.
- `npm run build` — pass for `/trailblazers-website/`.
- All 45 new citation pages opened in the web research tool. The eight newly assigned image URLs resolved in the web research tool. Automated external HTTP status and browser image-rendering checks were blocked by DNS and browser restrictions; existing citations were not rechecked.
- Browser screenshots and Lighthouse scores are unavailable: loopback HTTP binding was denied; Chromium headless failed with a sandbox socket error and Firefox headless exited 139. Desktop, tablet, mobile, keyboard-only, and screen-reader checks remain for a browser-capable environment.

## Review notes

Birth-date and testimony disputes, the Fe del Mundo Harvard claim, portrait decisions, and remaining quality work are documented in `docs/progress-report.md`. No GitHub Pages workflow or publication setting changed. Do not merge or publish until the 100-profile gate and live browser/rights review are complete.
