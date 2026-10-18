# Draft pull request: Museum foundation and first 14 reviewed profiles

## Summary

Builds a review-only digital museum foundation from the ten biographies and five categories in the original Cocoa-escaped page. Adds four researched profiles, a responsive editorial site, search and combined filters, profile routes, timeline, source citations, validation, tests, and documentation.

## Content status

- 14 verified publishable profiles; 28 institutional citations.
- 86 discovery candidates are unpublished and unverified.
- One NASA portrait is published with file-level rights and attribution; other portraits use typographic placeholders.
- The required 100-profile milestone remains unmet by 86 profiles. `npm run milestone` fails by design.

## Checks

- `npm run validate` — pass.
- `npm test` — 5 tests pass (routes, base path, filtering, semantics, milestone gate).
- `npm run build` — pass for `/trailblazers-website/`.
- Automated external HEAD checks — all 28 blocked by shell DNS; link status unmeasured.
- Browser screenshots/Lighthouse — blocked by local server and Chromium sandbox restrictions; scores unmeasured.

## Review notes

The original page and image URLs are preserved in `legacy/`. No GitHub Pages workflow or live deployment setting was changed. Do not merge or publish until the 100-profile gate and browser/rights review are complete.
