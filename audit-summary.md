# Audit Summary: Muhaffiz (Hifazat) SRS & SDS

**Document:** `Documents/Muhaffiz-SRS-SDS.pdf`, Version 1.0, 206 pages (audited 23 October 2026)
**Full findings:** `audit-report.md` (70 findings). **Template checklist:** `template-compliance.md`. **Coverage and limitations:** `review-progress.md`.
**Page convention:** PDF page (printed page); printed = PDF − 12 from PDF page 13 onwards.

## Overall status: **Requires major revision**

The document is detailed, well structured and close to the template in its layout. Identifiers are consistent, and every functional requirement has acceptance criteria and a test. The survey figures are accurate for the 31 responses actually analysed. However, the core safety behaviour contradicts itself in several places, and two of those contradictions involve the features the project claims as its contribution. The test plan would contact real emergency services. The document also presents an unbuilt system, and a survey sample, in ways an evaluation committee is likely to challenge.

None of these issues requires redesigning the product. Most are fixed by deciding one behaviour and propagating it consistently through the requirements, rules, diagrams, algorithms and tests.

| Severity | Count |
|---|---|
| Critical | 2 |
| Major | 19 |
| Moderate | 22 |
| Minor | 20 |
| Observation | 7 |

## The five most important issues to resolve before submission

1. **The duress (silent) SOS contradicts itself** (AUD-C01). BR-03 and FR-01.04 forbid vibration and any visible indication. BR-02, FR-03.04, UC-03, Algorithm A3, Figs. 19 and 33, and UT-08 send the duress phrase through a 20-second vibrating countdown with a full-screen cancel button. Under coercion, that exposes the user and lets the attacker cancel the alert.
2. **The SOS lifecycle is incomplete and inconsistent** (AUD-M04, M05, M06, M07).
   - Latency targets of 1 s, 2 s and 5 s conflict with a design that waits up to about 13 s before the first SMS.
   - Acknowledgements cannot arrive with no data connection, so every offline SOS escalates to the authorities.
   - Nothing specifies how to end an SOS or retract a false alarm.
   - Fig. 41 stops the alarm and the recording as soon as escalation is sent.
3. **Real emergency services and unverified authority channels** (AUD-C02, M12, M11). FT-25 expects SMS to the real Police 15 and Rescue 1122, and the test environment does not substitute numbers. Automatic calls and "share" need user action on Android, and SMS acceptance by 15 and 1122 is unverified. Several background-microphone, boot-restart, lock-screen and indicator assumptions need checking against current Android versions.
4. **Exposure of people's locations and of child data** (AUD-M08, M09, M10, M13).
   - Any helper who accepts sees the requester's exact location; "verified" means only that an administrator looked at an ID photo.
   - Missing-child alerts go out before moderation, based on self-attested guardianship.
   - The decoy screen design prints its own hidden gesture.
   - There is no account deletion and no server-side retention for location and third-party data.
5. **Evidence and claims an evaluator will challenge** (AUD-M14, M15, M16, M17).
   - The survey is reported as n = 73, but only 31 responses were analysed. One source says 109, and no raw data exists beyond the 31.
   - Section 5.4 is titled "Implemented User Interface", and a mockup shows "98.4% SOS delivery".
   - Section 6.8 says the objectives "are realized", yet the objectives BO-1 to BO-6 are never defined.
   - Modules MOD-17 to MOD-21 are committed without documented approval.

**Quick but visible fix:** Table 99 (use case list, PDF p.70) has no rows in the PDF. The `.docx` has all 29, so the PDF export dropped them (AUD-M01).

## Missing template deliverables

- **Section 5.4 Implemented User Interface:** cannot be satisfied before implementation. The current content is design renderings under an "implemented" heading (AUD-M15).
- **Chapter 6 actual results, executed counts and defect log:** structurally present but empty. Not yet assessable, which is acceptable at the SRS stage if labelled clearly.
- **Section 5.5:** secrets and environment-variable handling, and rollback, are not covered (AUD-N14).
- **Revision History and Review History:** present but empty (AUD-N01).
- **Component diagram:** no provided or required interfaces (AUD-N19).
- **Template Appendix D "Diagram Notation Reference":** not produced. It is unclear whether this is required; confirm with the supervisor (AUD-X03).
- **Typography:** the PDF uses substituted fonts (Liberation and DejaVu) instead of Times New Roman (AUD-N02).

## Technical and safety-critical contradictions

| Topic | Conflicting statements |
|---|---|
| Silent or duress SOS | BR-03, FR-01.04 versus BR-02, FR-03.04, FR-02.04, NFR-SAF-01, UC-03, A3, A5, Figs. 19, 33, 40, 55, UT-08; FR-19.03 and HI-4 vibration in silent mode |
| Private opt-out | FR-05.03 ("no event for other members") versus FR-04.02, FR-05.04, FR-05.05, Fig. 20 step 9, Fig. 56 |
| How to stop sharing | UC-09, FR-05.02, BR-11 (voice phrase only) versus BR-09, FR-15.02 (toggle at any time) |
| Dispatch timing | FR-01.01 (1 s), NFR-PER-01 (2 s), NFR-REL-01 (5 s) versus A3, A4, Figs. 17, 30, 32, 40 (fix wait up to 10 s plus probe up to 3 s) |
| Escalation behaviour | Fig. 41 (escalation closes the SOS and stops recording; cancel ends the SOS) versus FR-19.03 and Fig. 31 |
| Offline acknowledgement | FR-19.02 (timer runs offline) versus ADR-13, CI-7, API-03 (acknowledgement needs data) |
| Evidence toggle | RSK-16 ("can be switched off") versus BR-23, FR-15.02, Fig. 59 (no switch) |
| Channels | A4 ("send SMS always") versus FR-01.02 and BR-04 (per-trustee channels) |
| Calls | UC-25 A3 and UC-18 ("system places the call") versus CI-6 ("through the Android dialer") |
| Onboarding | Fig. 35 (declining consent skips the trustee step) versus FR-01.05 (a trustee is mandatory) |
| Shared trigger engine | Figs. 10, 18 and 19 route triggers differently |

## Pages or diagrams that could not be verified

All 206 pages and all 68 figures were inspected, both as text and as rendered images. Nothing was inaccessible. What could not be verified:

- **Raw survey data beyond the 31 analysed responses**, and the open-ended survey answer cited as the source of MOD-21.
- **External facts:** Android platform restrictions, whether Police 15, Rescue 1122 and 1099 accept SMS, current Firebase pricing, and Google Maps and OSM licence terms. No external research was requested.
- **Supervisor or committee approval** of MOD-17 to MOD-21.
- **The 207-page version** mentioned in the audit brief. The available PDF has 206 pages; the older `Documents/Muhaffiz.pdf` has 186.

## Confirmed defects, concerns and recommendations

- **Confirmed defects (most findings)** are shown directly by the document, the PDF render or the `.docx` source. Examples: the Table 99 rows, the contradictions above, the FT-25 test numbers, the decoy hint, the missing deletion requirements, the 55 untraced "shall" statements and the survey-source conflict.
- **Reasonable concerns** depend on facts outside the documents: Android behaviour (M11), authority acceptance (M12), scope approval (M17), helper and child-report abuse risk (M08, M09), Firebase billing (O22), legal review (O20), feasibility of the full scope (O21) and the children-as-users policy (O07).
- **Subjective recommendations** are optional: design alternatives such as pre-moderation, requester confirmation, a configurable decoy code and phrase renaming; extracting a "Dispatch SOS" use case; component interfaces; caption style; and reducing page count.

## Prioritised correction plan

### Phase 1: decisions needed from the team or supervisor (before editing)
1. Duress-phrase behaviour: immediate silent SOS, or a covert countdown (C01).
2. Offline acknowledgement strategy (SMS reply, user-confirmed escalation, or documented limitation) and the end or retract SOS behaviour (M05, M06).
3. How to stop sharing: toggle plus phrase (M03). Missing-child moderation model (M09). Near Help location disclosure (M08).
4. Survey reporting: n = 31 (M14). Scope approval of MOD-17 to MOD-21 (M17).

### Phase 2: mandatory corrections to the SRS
5. Propagate the Phase 1 decisions through the BRs, FRs, UCs, algorithms A3–A5 and A9, Figs. 19, 30–33, 40–43, Table 116 and the tests (C01, M02–M07, O01, O06, O08, O11, O12).
6. Make testing safe: test numbers, a build guard, and revised FT-25 and FT-18 (C02).
7. Add the missing requirements: end or retract SOS, account and data deletion, a retention table, helper location handling, admin MFA, server-derived recipients, server-side rate limits, and a maximum recording duration (M06, M13, M08, M19, O13).
8. Fix the data model gaps and A1 and A4 (O03, O04, O09, O10).
9. Restate integration and platform claims as constraints, assumptions or limitations; present escalation as simulated (M11, M12, O22).
10. Integrity fixes: a status note in the front matter and in Chapters 5 and 6, mockups labelled as illustrative with placeholder metrics, objectives BO-1 to BO-6 added to Chapter 1, the proposal's evaluation plan added (retrieval-quality baseline, pilot study, delivery per tier), the contribution statement and the citations fixed (M15, M16, O17, O18).
11. Traceability: add the 55 interface and constraint requirements to the RTM and correct its mappings (M18, O15). Define the reference device (O19).

### Phase 3: presentation and template polish
12. Re-export the PDF with Times New Roman and check Table 99 and all tables for lost rows (M01, N02).
13. Fill the Revision and Review History tables. Fix the TOC spacing, the column-width word breaks, the diagram overlaps (Fig. 20 first), the mockup glitches, the glossary and the former-name note (N01, N03–N11).
14. Add the 5.5 secrets and rollback text, versions in 5.2, and implementation components in 5.3 (N14).
15. Optional: enlarge small diagram text, reduce duplication and half-empty pages, add component interfaces, and settle the notation appendix with the supervisor (N06, N19, X03, X04).

**Next step:** no changes have been made to the SRS. Corrections will begin only after your approval, starting with the Phase 1 decisions.
