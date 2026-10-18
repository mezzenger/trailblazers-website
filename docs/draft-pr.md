# Draft pull request: Trailblazers of History release preparation

## Summary

Prepares `feature/museum-foundation` for owner review. The collection contains 100 verified biographies with 211 citations. Phase 4 makes homepage category discovery derive from the full collection and adds accessible placeholder-profile browser coverage. Portraits without cleared files continue to use a typographic initials treatment. This branch does not enable Pages deployment or publication.

## Content and rights

- 100 verified publishable profiles; no pending candidates.
- 211 citations and 16 portraits with file-specific rights metadata.
- The unresolved Olympe de Gouges execution day and Langston Hughes birth year remain qualified in the biographies and progress report.
- Other profiles use typographic placeholders where reusable image rights or identity have not been confirmed.

## Confirmed checks

- Final Phase 4 run [39107535658](https://github.com/mezzenger/trailblazers-website/actions/runs/39107535658) passed all workflow steps on commit `0b9c664e94bcc4481000a7b6994a2623eadd7d94`; 12/12 Playwright checks passed across desktop, tablet, and mobile, including axe checks.
- The browser artifact [12128832691](https://github.com/mezzenger/trailblazers-website/actions/runs/39107535658/artifacts/12128832691) contains screenshots, traces, the HTML report, and URL audit report.
- Final local gates pass: `npm run validate`, `npm test` (10 tests), `npm run build`, and `npm run milestone`.
- Each of two hosted audits covered 243 unique URLs: 201 reachable and 0 confirmed broken; restricted/unavailable responses varied from 29/13 to 30/12 between runs. No unresolved response was classified as broken without a confirming 404/410.
- Local `npm run audit:links` attempted the same set but DNS restrictions made all 243 unavailable locally.
- The artifact ZIP could not be rendered in this environment because DNS resolution for its signed download host failed. Owner visual review is required; no Lighthouse result is claimed.

## Review notes

The 100-profile content milestone is met. Browser automation tests search, combined filters, category navigation, timeline control, keyboard focus, GitHub Pages routing, responsive overflow, placeholder rendering, and axe on representative pages and themes. César Chávez's reported allegations and the recorded historical date disputes remain carefully qualified. GitHub denied draft PR creation to the connected integration (HTTP 403: resource not accessible); create the review draft manually at https://github.com/mezzenger/trailblazers-website/compare/main...feature/museum-foundation?expand=1. Do not merge or publish until the owner has reviewed the screenshot artifact and outstanding restricted/unavailable links.
