# Project instructions

- Treat `content/profiles.json` as the only publishable collection. Keep unreviewed discovery names in `content/pending.json`.
- Every publishable biography must be original, 150–300 words, and supported by at least two credible sources from independent domains. Define the scope of historical firsts. Use `verification: verified` only after claim review.
- Do not reuse an image until its exact file, creator, source, license, attribution, and required notices have been checked. `image: null` is preferred when rights are unclear.
- Preserve `legacy/recovered-original.html` and `legacy/migration-inventory.json` for migration history.
- Run `npm run validate`, `npm test`, and `npm run build` before a review request. `npm run milestone` is the 100-profile release gate and must not be bypassed.
- Keep GitHub Pages base-path support. Do not enable deployment, publish, merge, or modify live Pages settings without owner approval.
