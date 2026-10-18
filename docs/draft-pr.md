# Draft pull request: Museum foundation and 80 reviewed profiles

## Summary

Continues the review-only museum on `feature/museum-foundation`. Phase 3C promotes 26 researched biographies from the unpublished queue and adds five file-reviewed portraits. The original Cocoa-escaped page and migration inventory remain in `legacy/`; existing IDs, content, interface behavior, and rights records are preserved.

## Content status

- 80 verified publishable profiles; 168 source citations from at least two independent domains per profile.
- 20 discovery candidates remain unpublished.
- Sixteen portraits have file-specific creator, source, rights basis, and attribution metadata; other profiles use typographic placeholders.
- The 100-profile milestone remains unmet by 20 records; `npm run milestone` must continue to fail until those records are researched and validated.

## Checks and browser review

- `npm run validate` — pass, zero schema/content errors.
- `npm test` — seven tests cover internal routes, base path, client-script filters, unknown dates, semantics, contrast, and milestone enforcement.
- `npm run build` — produces `/trailblazers-website/` output.
- New citation pages were opened and read in web research; automated external HTTP sweeps and live image rendering remain unavailable in this sandbox.
- `.github/workflows/browser-review.yml` runs review-only Chromium checks and axe at desktop, tablet, and mobile sizes and uploads screenshots/reports. The first Actions run is pending; no browser screenshots or Lighthouse scores are claimed here.

## Review notes

Existing disputes about Kalpana Chawla's and Qiu Jin's birth years, Fe del Mundo's Harvard claim, and Rigoberta Menchú's testimony remain documented in `docs/progress-report.md`. Phase 3C also distinguishes the competing versions of Sojourner Truth's Akron speech, avoids assigning the whole DNA model to one researcher, and records the Emergency in Indira Gandhi's biography. Margaret Hamilton, Gladys West, and Yayoi Kusama have 2026 death records checked against current sources. No Pages deployment workflow or publication setting changed. Do not merge or publish until the 100-profile gate and live browser/rights review are complete.
