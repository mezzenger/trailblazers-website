# Draft pull request: Museum foundation and 34 reviewed profiles

## Summary

Builds a review-only digital museum foundation from the ten biographies and five categories in the original Cocoa-escaped page. Phase 3A adds 20 researched profiles to the existing 14, with a responsive editorial site, search and combined filters, profile routes, timeline, source citations, validation, tests, and documentation.

## Content status

- 34 verified publishable profiles; 70 source citations.
- 66 discovery candidates are unpublished and unverified.
- Three government portraits have file-level rights and attribution records; other portraits use typographic placeholders.
- The required 100-profile milestone remains unmet by 66 profiles. `npm run milestone` fails by design.

## Checks

- `npm run validate` — pass.
- `npm test` — 5 tests pass (routes, base path, filtering, semantics, milestone gate).
- `npm run build` — pass for `/trailblazers-website/`.
- All 42 new source pages opened in the web research tool; direct shell HTTP status checks blocked by DNS.
- Browser screenshots/Lighthouse — not run in Phase 3A; scores unmeasured.

## Review notes

The original page and image URLs are preserved in `legacy/`. Historical ambiguities and source-access limits are recorded in `docs/progress-report.md`. No GitHub Pages workflow or live deployment setting was changed. Do not merge or publish until the 100-profile gate and browser/rights review are complete.
