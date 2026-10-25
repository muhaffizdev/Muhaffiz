# Review Progress and Limitations

**Audit of:** `Documents/SRS/Muhaffiz-SRS-SDS.pdf` (206 pages) and its source `Documents/SRS/Muhaffiz-SRS-SDS.docx`
**Date:** 23 October 2026 · **Status:** Audit complete. **The SRS was not modified.** Corrections are waiting for approval.

## Sources used, in the order of authority given in the brief

| Rank | Source | File | Used for |
|---|---|---|---|
| 1 | University SRS template | `Documents/Reference/SRS-Template.docx`, converted to PDF (53 rendered pages, printed labels 1–49) and read in full | Required structure, tables and formatting rules |
| 2 | Approved project brief | `Documents/Reference/Hifazat Feature Document.md` (19 modules; 7.17–7.19 "to be confirmed") and `Documents/Reference/Muhaffiz_FYP_Scope_Document-UnUpdated.docx` (proposal; 16 modules, objectives BO-1 to BO-6, evaluation plan) | Scope and confirmed features. **Limitation:** neither file is marked as the approved version. The scope document is labelled "UnUpdated", and `project-context.md` says it is out of date. Both were therefore used, and conflicts between them are reported (AUD-M17) |
| 3 | SRS under audit | `Documents/SRS/Muhaffiz-SRS-SDS.pdf` and `.docx` | Everything audited |
| Context | Decisions and history | `Documents/Notes/project-context.md`, `Documents/Notes/progress.md`, `Documents/Notes/SRS-Checklist.md`, `Documents/Reference/Hifazat Full Chat Record.md` | Identifying source conflicts (survey size, scope approval, interview count) and recomputing the survey figures. Not treated as authority for correctness |
| Not audited | Older build | `Documents/Archive/Muhaffiz-SRS-SDS-old-186p.pdf` (186 pages, 22 Oct 23:56) | Noted only (AUD-X05) |

## Page numbering

**PDF p.N (printed p.M)** is used throughout. Printed = PDF − 12 for PDF pages 13–206. PDF pages 1–12 carry no printed number.

## Coverage record

| PDF pages (printed) | Content | Text read | Rendered images inspected | Done |
|---|---|---|---|---|
| 1–12 | Cover, revision/review/approval tables, TOC, list of figures, list of tables | Yes | pp.1–3 | ✔ |
| 13–20 (1–8) | Chapter 1 | Yes | — | ✔ |
| 21–30 (9–18) | Chapter 2, including Fig. 1 | Yes | p.22 | ✔ |
| 31–68 (19–56) | 3.1 catalogue and all 87 FR specification tables | Yes | — | ✔ |
| 69–74 (57–62) | Use-case diagrams (Figs. 2–5), Table 99, UC-01, 02, 03, 09, 25, 23 | Yes | pp.69, 70 | ✔ |
| 74–83 (62–71) | Business rules, NFRs, external interfaces | Yes | — | ✔ |
| 84–89 (72–77) | 4.1, 4.2 (Figs. 6, 7), ADRs | Yes | pp.86, 88 | ✔ |
| 90–98 (78–86) | Class diagrams (Figs. 8–15) | Yes | pp.91–98 (all) | ✔ |
| 99–112 (87–100) | Sequence diagrams (Figs. 16–29) | Yes | pp.99–112 (all) | ✔ |
| 113–122 (101–110) | Activity diagrams (Figs. 30–39) | Yes | pp.113–122 (all) | ✔ |
| 123–131 (111–119) | State diagrams (Figs. 40–48) | Yes | pp.123–131 (all) | ✔ |
| 132–133 (120–121) | Component diagram (Fig. 49), event-response table | Yes | p.132 | ✔ |
| 133–140 (121–128) | Data design, ER diagrams (Figs. 50–53) | Yes (including the ER text layer) | ER diagrams checked through their text layer and against Table 117 | ✔ (see limitation L6) |
| 141–148 (129–136) | Navigation (Fig. 54), key screens (Figs. 55–59), Table 119 | Yes | pp.141, 142, 143, 145 | ✔ |
| 148–152 (136–140) | Security design, risks, milestones | Yes | p.150 | ✔ |
| 153–169 (141–157) | Algorithms A1–A10, APIs, REST API, 5.4 screens (Figs. 60–68), deployment | Yes | pp.159, 160, 165, 167 | ✔ |
| 170–188 (158–176) | Test tables, test summary, RTM, conclusion | Yes | — | ✔ |
| 189 (177) | References | Yes | — | ✔ |
| 190–205 (178–193) | Appendices A–D | Yes | — | ✔ |
| 206 (194) | Document Status | Yes | — | ✔ |

All 206 pages were read as text. All 68 figures were checked: 57 as rendered images and 11 through their text layer only (see L6). A low-resolution image of every page (100 dpi) was generated, and near-blank pages were detected automatically.

## Automated checks performed

| Check | Method | Result |
|---|---|---|
| Table rows lost in the PDF | Compared every `.docx` table row with the PDF text (raw extraction) | Only Table 99 lost its rows (AUD-M01) |
| Undefined or dangling IDs | Collected every MOD/FR/BR/UC/NFR/CON/AS/DEP/RSK/TBD/API/SD/ADR/test/interface ID referenced and compared with the defined sets | No undefined references; CON-x mostly never referenced again (AUD-M18) |
| FR count | Per-module count | 87, matching the stated total |
| Test count | Per-table count | 24 + 29 + 32 + 14 + 42 = 141, matching Table 142 |
| NFR count | Per-category count | 42, matching the stated total |
| Survey percentages | Recomputed from the 31 coded rows in the chat record | All Table 7 and Table 8 values match |
| Fonts in the PDF | `pdffonts` | Liberation Serif, Liberation Sans, DejaVu; no Times New Roman (AUD-N02) |
| Body and heading styles | Parsed `styles.xml` | Match the template (AUD-X07) |
| Cross-references | Parsed field codes in `document.xml` | 165 REF fields; 0 hand-typed references in body text |
| Captions | SEQ fields | 243 |
| Text beyond the margins | Word bounding boxes | None found |
| Minimum diagram text size | Word bounding-box heights, calibrated against 12 pt body text (box ≈ 1.11 × font size) | Smallest text about 5.0–5.9 pt in several figures (AUD-N06) |
| Leftover template text | Searched for cafeteria, MHCF, Stripe, "[Enter]", "Student Name" | None |
| Terms searched in the full text | account deletion, MFA, legal, Play Store, "end the SOS", BO-1, novel, rollback, secret | Results used in AUD-M06, M13, M16, M19, O18, O20, N14 |

## Limitations and items that could not be verified

| # | Limitation | Effect |
|---|---|---|
| L1 | **No external research** (none was requested). Android platform behaviour (microphone restrictions on background services and at boot, the privacy-indicator version, emergency-call restrictions, lock-screen options), whether Police 15, Rescue 1122 and 1099 accept SMS, Firebase billing for Cloud Functions, Google Maps and OSM licence terms, and Google Play SMS policy were not checked against current sources | The related findings are classified as **reasonable concerns** (M11, M12, O22, N13) and need verification |
| L2 | **Raw survey data beyond the 31 analysed responses is unavailable.** Sources disagree on the total (73 in `project-context.md`, 109 in the chat record) | The total sample size cannot be verified (M14) |
| L3 | **The open-ended survey answer cited as the source of MOD-21** is not in the available materials | Source unverifiable (X06) |
| L4 | **Approval status of MOD-17 to MOD-21** and of the brief itself is not documented in any file | Reported as a source conflict (M17) |
| L5 | **The 207-page version** named in the audit brief was not found; the available PDF has 206 pages | This audit applies to the 206-page PDF of 23 Oct 2026, 01:12 |
| L6 | **ER diagrams (Figs. 50–53, PDF pp.136–139) and the mockups in Figs. 57, 59, 61–64 and 66** were checked through their text layer and against the data dictionary or screen table, without a separate detailed visual pass for every one. The text layers were complete and consistent | Small visual defects in those figures (such as crow's-foot symbol errors or overlaps) may remain undetected |
| L7 | **Rendering environment:** the PDF was rendered on Linux. Word on Windows may lay out the `.docx` differently (fonts, row breaks) | Re-check Table 99 and the column-width issues in the final export tool |
| L8 | **Legal compliance** was not assessed; no legal source was provided | Only the absence of a legal-review item is noted (O20) |
| L9 | **Novelty** was assessed only against the project's own documents, not the research literature | AUD-O18 concerns how the contribution is stated, not whether it is novel |

## Outstanding checks recommended after correction

1. Re-export the PDF and repeat the row-count comparison and the font check.
2. Re-run the ID cross-check after renumbering or adding requirements (end-SOS, deletion, retention, and so on).
3. Verify the Android, emergency-service and Firebase facts listed in L1, and update the constraints and assumptions.
4. Do a full visual pass over the Fig. 41, 43 and 20 redraws and the decoy mockup fix.
5. Obtain and record supervisor approval of the scope (Review History table).

## Unresolved questions for the team

1. Should the duress phrase skip the countdown entirely, or use a covert cancel? (C01)
2. Which offline acknowledgement strategy, if any, is acceptable? (M05)
3. Are minors intended to hold accounts? (O07)
4. Were MOD-17 to MOD-21 approved by the supervisor, and is template Appendix D (notation reference) required? (M17, X03)
5. Does the full export with 73 (or 109) survey responses exist? (M14)
