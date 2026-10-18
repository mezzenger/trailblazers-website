# Draft pull request: Museum foundation and 100 verified profiles

## Summary

Continues the review-only museum on `feature/museum-foundation`. Phase 3D promotes the final 20 researched biographies, completes the 100-profile milestone, and repairs biography-card accessible names by deriving them from visible content. The original Cocoa-escaped page and migration inventory remain in `legacy/`; existing IDs, content, interface behavior, and rights metadata are preserved.

## Content status

- 100 verified publishable profiles with 211 source citations; every profile has at least two sources from independent domains.
- No unpublished candidates remain in the current queue.
- Sixteen portraits have file-specific creator, source, rights basis, and attribution metadata. Other profiles use typographic placeholders.
- Conflicting source dates for Olympe de Gouges and Langston Hughes are documented; their uncertain date components are left blank.

## Checks and browser review

- `npm run validate` — pass; 100 profiles, 211 citations, zero errors.
- `npm test` — pass; 8 tests, including card-link accessible-name regression and milestone boundary coverage.
- `npm run build` — pass; generated all 100 profile routes using `/trailblazers-website/`.
- `npm run milestone` — pass at 100; a 99-profile fixture still fails as required.
- The confirmed biography-card label mismatch is fixed without altering axe rules.
- The initial Actions report could not be retrieved from this environment, so other reported axe failures remain unknown. A feature-branch browser run must be inspected before approval; no screenshots or browser pass are claimed yet.

## Review notes

César Chávez's reported abuse allegations are presented as allegations, with broader organizing credit given to Dolores Huerta and Filipino farmworkers. The Stonewall biographies do not claim a verified first brick. Research disputes and source access limitations are in `docs/progress-report.md`. The branch does not enable Pages deployment or change publication settings. Do not merge or publish before owner review of the browser run and release candidate.
