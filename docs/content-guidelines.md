# Content guidelines

Each publishable record needs `id`, `name`, `born`, `died`, `region`, `place`, `era`, `categories`, `summary`, `biography`, `achievements`, `milestones`, `sources`, `image`, `verification`, and `reviewed`. Dates may be a year, year-month, or full ISO date; use `null` when unknown. Do not turn uncertain dates into exact ones. Use a stable lowercase hyphenated ID. Summaries should be concise, biographies original and 150–300 words, and milestones dated by a defensible year. Sources need a descriptive title and HTTPS URL.

Use `verified` only when major claims, dates, and scoped firsts have been checked against at least two credible sources from independent domains. Mark unresolved claims in research notes, or keep the person in `pending.json`. Do not imply a living person is dead, or use a current title for a former officeholder. Attribute collective accomplishments accurately. Explain the conditions in which a contribution mattered without reducing a person to adversity.

For portraits, `image: null` produces an intentional typographic placeholder. To publish an image object, supply `url`, `creator`, `source`, `license`, and `attribution`; record notices in attribution. Verify the exact image file, not merely the repository or hosting domain. Do not generate realistic portraits and pass them off as historical photographs. Avoid blanket public-domain claims, especially for modern photographs.

## Documentary image gallery

An optional `gallery` array can place multiple documentary images into the biography, after the opening life narrative. Each entry requires `url`, `creator`, `source`, `license`, `attribution`, `caption`, and descriptive `alt`. Use photographs, artifacts, letters, documents and artwork that illuminate a documented milestone—not duplicates added just to increase photo counts. Every file requires individual copyright and identification review; no automatically populated search results. If no cleared source exists, omit the gallery. Portrait image metadata remains a separate `image` field. External image delivery and rights should be checked before publication.
