# Progress report — 2026-10-18

| Phase | Status |
| --- | --- |
| 1. Foundation | Original Cocoa HTML and migration inventory retained; static content architecture and validation remain in place. |
| 2. Experience | Homepage, collection search, combined filters, sort, timeline, profile routes, related stories, sharing, themes, and responsive styles remain in place. |
| 3. Content | Phase 3B promoted 20 candidates. There are 54 verified profiles and 46 unpublished candidates. |
| 4. Quality | Content, route, base-path, client-behavior, semantics, and accent-contrast tests pass. Live browser visual and assistive-technology checks remain blocked. |
| 5. Delivery | Review branch carries the Phase 3B work. Draft PR text is updated; deployment remains disabled. |

**Current data:** 54 unique publishable profiles, 115 source citations, 11 portraits with file-specific rights metadata, and 46 unpublished discovery candidates. Every biography is 150–300 words. The 100-profile gate deliberately fails by 46 records.

## Phase 3B research

The 20 additions are Dorothy Vaughan, Ellen Ochoa, Kalpana Chawla, Lise Meitner, Emmy Noether, Rebecca Lee Crumpler, Henrietta Lacks, Nise da Silveira, Fe del Mundo, Rosa Parks, Ella Baker, Dolores Huerta, Desmond Tutu, Rigoberta Menchú, Michelle Bachelet, Qiu Jin, Huda Sha'arawi, Zora Neale Hurston, Faith Ringgold, and Nawal El Saadawi. Their pending IDs became their permanent profile IDs. The batch spans North America (9), Asia (3), Africa (3), Europe (2), South America (2), and Central America (1); Menchú represents a K’iche’ Maya perspective. Each has at least two sources from independent domains, with 45 new citations in all.

### Evidence decisions

- [NASA's astronaut fact book](https://www.nasa.gov/reference/astronaut-fact-book/) gives Kalpana Chawla a 1961 birth date while other published accounts give 1962. Her birth date is null; her verified missions and 2003 death remain recorded.
- Qiu Jin's birth year varies among historical accounts. It is null until a stronger consensus is documented.
- The often repeated claim that Fe del Mundo was the first woman admitted to Harvard Medical School conflicts with [Harvard Library's admission history](https://guides.library.harvard.edu/c.php?g=1108872&p=8085578). The profile makes no such claim.
- Accounts of particular events in Rigoberta Menchú's testimony have been disputed, as discussed in [PMLA](https://www.cambridge.org/core/journals/pmla/article/abs/authoring-ethnicized-subjects-rigoberta-menchu-and-the-performative-production-of-the-subaltern-self/B795BADD23BAF53F524B457A9ACB7E66). Her profile uses independently documented advocacy and identifies the dispute without treating every autobiographical episode as settled.
- The [National Park Service](https://www.nps.gov/people/dr-rebecca-lee-crumpler.htm) reports no surviving photograph of Rebecca Lee Crumpler; her placeholder is intentional. Images of Rosa Parks and several living people also remain placeholders because a specific reusable file was not cleared.

### Portraits

Four new profiles gained checked files: NASA photographs of Vaughan, Ochoa, and Chawla, plus an anonymous early photograph of Noether. Four existing placeholders gained checked historical works: portraits of Ada Lovelace, Harriet Tubman, Madam C. J. Walker, and Bessie Coleman. Exact Commons file pages, creators or attributed creators, rights basis, attribution, and relevant notices are stored with each profile. Large Commons originals use 960-pixel thumbnails where available. This brings the collection from three to eleven rights-reviewed portraits. Potential images with ambiguous authorship or rights, including several other historical subjects, remain unpublished.

## Visual and accessibility audit

Static review covered the homepage, filters, empty state, timeline, profile routes, light and dark themes, responsive breakpoints at 1000/700/400 px, focus rules, reduced-motion rules, labels, alt text, and the GitHub Pages subpath. A real client-script test found that `normalize` was missing from the homepage import, stopping search/filter initialization. An integration test now executes the script and checks combined filters, empty state, clearing, and unknown-date sorting. Null birth dates also exposed an unsafe string operation in build and sort code; both are fixed. Calculated WCAG text contrast for small accent labels was below 4.5:1 in several light and dark contexts; the new theme-specific accent text exceeds 4.5:1 against paper, ivory, and card surfaces, and a regression test enforces it. Large accent headings on light surfaces use the same corrected token.

Browser screenshots and keyboard-only or screen-reader sessions could not run in this sandbox: local HTTP binding failed with `PermissionError: [Errno 1] Operation not permitted`; Chromium headless failed with `setsockopt: Operation not permitted` (exit 133); Firefox headless exited 139. No desktop, tablet, or mobile screenshots or Lighthouse scores are claimed. Runtime focus order, portrait display, and layout at those viewport widths still need a browser review outside this sandbox.

## Link validation and remaining work

All 45 newly cited source pages were opened and read through the web research tool. Indexed pages that returned 403, 500, or only an access challenge were replaced before promotion. The eight newly assigned image URLs also resolved in the web research tool. Direct shell HTTP status checks and in-browser image rendering could not run because DNS resolution failed (`Temporary failure in name resolution`); existing citations and images were not rechecked in this phase. The automated internal-route/base-path test passed. Next steps are a real browser and assistive-technology audit, more image-rights review, and 46 additional verified profiles before the 100-profile gate can pass. Draft PR creation remains permission-blocked; use `docs/draft-pr.md` for manual creation. No deployment was enabled.
