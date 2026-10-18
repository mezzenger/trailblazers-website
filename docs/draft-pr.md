# Draft pull request: Trailblazers of History release preparation

## Summary

Prepares `feature/museum-foundation` for owner review. The collection contains 100 verified biographies with 211 citations. Phase 4 makes homepage category discovery derive from the full collection and adds accessible placeholder-profile browser coverage. Portraits without cleared files continue to use a typographic initials treatment. This branch does not enable Pages deployment or publication.

## Content and rights

- 100 verified publishable profiles; no pending candidates.
- 211 citations and 16 portraits with file-specific rights metadata.
- The unresolved Olympe de Gouges execution day and Langston Hughes birth year remain qualified in the biographies and progress report.
- Other profiles use typographic placeholders where reusable image rights or identity have not been confirmed.

## Confirmed checks

- Phase 3D run [39104859860](https://github.com/mezzenger/trailblazers-website/actions/runs/39104859860) passed 9/9 Playwright cases at commit `09ad3dc1e46eff9de221fb37ffba7f50e5ccc8c5`; the test artifact is available from that run.
- Phase 4 adds category coverage and placeholder-route checks. Final local gates and browser workflow are pending on the release-preparation commit.
- Final local gates pass: `npm run validate`, `npm test` (10 tests), `npm run build`, and `npm run milestone`.
- Local `npm run audit:links` attempted 243 unique URLs; all were unavailable because this sandbox cannot resolve external hosts. No link was labeled broken from that restricted run. The hosted workflow performs the meaningful link check and uploads its per-URL report.
- The artifact screenshots could not be opened in this sandbox because DNS resolution for the signed download host failed. Owner visual review is required; no Lighthouse result is claimed.

## Review notes

The 100-profile content milestone is met. Browser automation tests search, combined filters, category navigation, timeline control, keyboard focus, GitHub Pages routing, responsive overflow, placeholder rendering, and axe on representative pages and themes. The 211 URLs have not all received a current live availability check; coverage and classifications are documented in `docs/progress-report.md`. César Chávez's reported allegations and the recorded historical date disputes remain carefully qualified. Do not merge or publish until the final browser run passes and the owner has reviewed the screenshot artifact and outstanding link/image issues.
