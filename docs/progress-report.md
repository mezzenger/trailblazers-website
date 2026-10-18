# Progress report — 2026-10-18

| Phase | Status |
| --- | --- |
| 1. Foundation | Original Cocoa HTML and migration inventory retained; static content architecture and validation remain in place. |
| 2. Experience | Homepage, collection search, combined filters, sort, timeline, profile routes, related stories, sharing, themes, and responsive styles remain in place. |
| 3. Content | Phase 3D promoted the final 20 candidates; 100 verified profiles now satisfy the 100-profile gate. |
| 4. Quality | Static validation and local automated checks are being run for Phase 3D. The supplied Actions report is inaccessible from this environment; browser and visual sign-off await a reachable run. |
| 5. Delivery | Review branch carries the 100-profile collection and biography-card accessible-name fix. No merge or deployment is authorized. |

**Current data:** 100 unique publishable profiles, 211 source citations, 16 portraits with file-specific rights metadata, and 0 unpublished candidates. Every biography is 150–300 words. The 100-profile gate passes on the validated dataset.

## Phase 3D research and accessibility repair

The final 20 candidates were promoted: Rebecca Masika Katsuva, César Chávez, Marsha P. Johnson, Sylvia Rivera, Angela Davis, Claudette Colvin, Mahatma Gandhi, Golda Meir, Benazir Bhutto, Jacinda Ardern, Olympe de Gouges, Mary Wollstonecraft, Arundhati Roy, Audre Lorde, James Baldwin, Langston Hughes, Gwendolyn Brooks, Alma Thomas, Nina Simone, and Billie Holiday. Their original IDs became public routes. The additions contain 43 citations; combined with the existing collection, the dataset has 100 profiles and 211 citations. No portraits were added because a file-specific, reusable image right was not confirmed for these candidates. Existing typographic placeholders remain; the 16 rights-cleared portraits are unchanged.

- Olympe de Gouges's execution date conflicts between the French National Assembly (6 November 1793) and Library of Congress (3 November 1793). Her record gives only 1793.
- Langston Hughes's birth year is listed as 1901 by the Kansas Historical Society and 1902 by Library of America. His record leaves the birth year blank.
- The profile for César Chávez identifies 2026 allegations reported by Dolores Huerta and other women as allegations and does not present them as adjudicated findings. It also credits Filipino farmworkers and Dolores Huerta in the movement's organizing.
- Marsha P. Johnson and Sylvia Rivera are described as participants in the collective Stonewall uprising; no unsupported “first brick” claim is repeated.
- Claudette Colvin's death date was updated to 13 January 2026 using the Associated Press obituary published by the Los Angeles Times.
- Inaccessible sources encountered during research were replaced where usable independent alternatives were available. Benazir Bhutto's sources use DePauw and the AP obituary reprint; James Baldwin's use Stanford and the Library of Congress.

The reported `label-content-name-mismatch` on biography-card links came from a custom `aria-label` (“Read about [name]”) overriding the longer visible card content. The override was removed, allowing visible link text and portrait alternative text to form the accessible name. A unit regression test asserts that generated biography-card links have no overriding `aria-label`; axe in the browser workflow checks the result. The supplied initial Actions run's logs, axe report, screenshots, and traces could not be fetched from the current environment (GitHub page cache miss and API DNS failure). The other reported accessibility findings therefore remain unknown and are not marked fixed or suppressed.

The browser workflow is configured to run on a feature-branch push touching content, the builder, tests, or workflow. Its new run and screenshots are not confirmed yet. No screenshot, Lighthouse score, or successful browser audit is claimed. Shell network access was restricted, so web-research source access is distinct from a comprehensive HTTP check; existing citations and portrait URLs were not all revalidated during this phase.

## Phase 3C research and rights review

The 26 additions are Mary Jackson, Margaret Hamilton, Annie Easley, Gladys West, Valentina Tereshkova, Sally Ride, Chiaki Mukai, Marie Curie, Sofia Kovalevskaya, Rosalind Franklin, Nettie Stevens, Rita Levi-Montalcini, Virginia Apgar, Florence Nightingale, Clara Barton, Sojourner Truth, Fannie Lou Hamer, Pauli Murray, Bayard Rustin, John Lewis, Steve Biko, Nadia Murad, Indira Gandhi, Chimamanda Ngozi Adichie, Octavia Butler, and Yayoi Kusama. Their existing candidate IDs became permanent public routes. The batch spans Africa, Asia, Europe, and North America across science, medicine, spaceflight, civil rights, government, and the arts. Each has an original 150–300 word biography and at least two opened, independent source pages. This batch adds 53 citations. Sources that returned only access challenges, including several Nobel, UN, and official defense pages, were excluded rather than treated as verification.

- [MIT's 2026 obituary](https://news.mit.edu/2026/margaret-hamilton-computing-pioneer-dies-1007), [the Guardian's Gladys West obituary](https://www.theguardian.com/science/2026/feb/08/gladys-west-obituary), and [the Yayoi Kusama Museum notice](https://yayoikusamamuseum.jp/en/news/news20260827/) support newly recorded 2026 deaths. Their older living-person metadata was not carried forward.
- Sojourner Truth's 1851 Akron speech survives in conflicting reports. The famous refrain appears in a later version, not a verified verbatim transcript; her profile flags that distinction. Her birth is approximate, so `born` remains null.
- Franklin and Gosling's DNA diffraction work is described alongside other laboratories, without assigning the double helix to one person. Stevens's sex-chromosome research acknowledges Wilson's related work and the limits of generalizing from mealworms. Hamilton and West are credited for major team contributions without being called sole inventors.
- Gandhi's Emergency is documented as a suspension of civil rights, with a [Library of Congress account](https://blogs.loc.gov/kluge/2020/07/the-20th-century-transformation-of-the-dalit-movement-in-india/) added alongside her institutional biography. Nadia Murad's profile centers documented advocacy rather than graphic details of abuse. Kusama's artworks remain copyrighted, so her profile uses a placeholder.
- Five file-specific Commons records were checked and added: NASA portraits of Mary Jackson, Annie Easley, and Sally Ride; a nineteenth-century Library of Congress carte de visite of Sojourner Truth; and Henry Hering's National Portrait Gallery photograph of Florence Nightingale. The source page, creator, rights basis, attribution, and applicable notices appear in each record. This raises rights-reviewed portraits from 11 to 16. Other candidates remain placeholders where an authentic reusable file was not confirmed.

## Phase 3C browser-review path

The earlier sandbox failures described below were not retried in the same configuration. A read-only `.github/workflows/browser-review.yml` now builds the normal project-path site and runs Playwright Chromium at 1440×900, 768×1024, and 390×844. Tests exercise collection search and combined filters, empty state, clearing, timeline control, keyboard focus, a biography route, image record link, overflow, and axe accessibility in both themes with reduced motion. Screenshots, traces, and an HTML report are uploaded for 14 days even after test failure. The workflow uses no secrets, deployment API, or Pages permission. The first feature-branch run has not been observed yet, so browser findings, screenshots, and Lighthouse scores remain unreported. A local reproduction command is in `docs/deployment.md`.

At the end of Phase 3C, external-link validation covered that phase's 53 new citation URLs and five new Commons file records. The 20 candidates noted there were subsequently researched and promoted in Phase 3D. Direct shell HTTP sweeps and live browser rendering remain unavailable in this sandbox; the earlier 80-profile collection's citations and portraits were not comprehensively revalidated in Phase 3D.

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

At the end of Phase 3B, all 45 source pages added in that batch had been opened and reviewed. That earlier progress snapshot recorded the remaining 46 profiles and is superseded by Phase 3C and Phase 3D above. No deployment was enabled.
