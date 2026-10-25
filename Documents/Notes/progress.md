# Progress

## Done
- Topic approved by supervisor; pitch deck built (by user); survey n = 73 (see project-context.md).
- Context read: Feature Document, Full Chat Record, old Scope Document, SRS template.

## Current stage
SRS & SDS (Documents/Reference/SRS-Template.docx), filled chapter by chapter. Waiting for the user's detailed prompt. Do not start before then.

## SRS chapters
- [~] Front matter (cover, empty revision/review tables, approval, TOC, List of Tables) - built, awaiting review
- [~] Ch 1 Introduction - built (build/ch1.py), awaiting review
- [x] Ch 2 Overall Description & Elicitation - built (build/ch2.py), awaiting review
- [x] Ch 3 Software Requirements Specification - built (build/ch3.py, ch3_data.py, fr_data1-3.py), awaiting review
- [~] Ch 4 System Design - built (ch4.py, figs_*.py)
- [~] Ch 5 Implementation & Deployment - built (ch5.py)
- [~] Ch 6 Testing, Evaluation & Conclusion - built (ch6.py, ch6_data.py)
- [~] References, Appendices A-D, Document Status page - built (refs.py, ch_end.py)

## Parked
- Scope document corrections (not needed for SRS).
- WBS/Gantt, mockups in scope document.

## Build system (Documents/SRS/build/)
- `python3 build.py` regenerates Muhaffiz-SRS-SDS.docx from SRS-Template.docx + chapter modules ch1.py ... ch6.py (chapters without a module stay as template placeholders). srslib.py holds table/heading/caption/TOC helpers. Set SRS_WORK and SRS_RENDER env vars to scratch dirs.
- Writing a chapter = create chN.py with blocks(ctx) using H1/H2/P/BUL/NUM/TBL/FIG helpers; {sec:key}, {tbl:key}, {fig:key}, {cite:key} tokens become auto fields.
- Validate with the docx skill's validate.py (needs a defusedxml shim).

## Open items flagged to user after Ch1
- MOD-20 "Safe-Location Navigation" and MOD-21 "App Disguise": names and the "Safe Location" definition (bundled-directory places such as police stations, hospitals) are Claude's proposal; confirm.
- MOD-17..21 confirmed by the user as fully approved and part of the system (2026-10-23); Section 1.5 says so.
- Appendices planned: A use case list, B detailed use cases, C TBD list, D sample test data; glossary stays in 1.4 (reconcile glossary after all chapters).
- Ch5.4 (implemented UI) and Ch6 actual results cannot be filled before implementation.

## Agreed approach (user decision, 2026-10-22)
- Body written in plain present tense as a built system, no hedging; ONE accurate "Document Status" disclaimer page after the last appendix, nowhere else.
- Claude does NOT invent: test results/pass rates/defects, accuracy or timing figures, "implemented" statuses, screenshots of a running app. Chapter 6 = full test cases with Actual/Observed Result and executed counts left empty.
- Interviews: cite four; MBBS entry in the record was "(x2)" - wording avoids a count of participants.
- Survey: n = 73; percentages from first 31 (re-verified from the chat record).
- Web searches were declined by the user; do not run WebSearch unless asked. Keyword-spotting engine name (e.g. sherpa-onnx) still unverified - keep generic until Ch5.
- Section references typed as plain text in ch2 for later chapters (3.1, 4.3, 4.5): convert to {sec:key} fields once those chapters exist.
- Glossary (1.4) must be reconciled with terms used in Ch3-6 at the end.

## Chapter 3 decisions needing user confirmation (made by Claude)
- WhatsApp cannot send without the user's tap: BR-04 makes it user-confirmed and not used in silent SOS (Feature Doc 7.1.2 said all channels at once).
- Google Maps ToS does not allow storing tiles: offline maps use open (OSM-derived) map data for up to 3 areas (FR-13.02, SI-7, OE row, DEP-7 added to Ch2).
- FR-16.05 (admin authentication) added; MOD-20 has 3 FRs, MOD-21 has 3 FRs.
- Parameter values chosen: SOS hold 1 s; countdown 20 s; no-response timer 3 min; escalation warning 30 s; fix wait 10 s; helper radius 1 km; missing-child alert radius 5 km and expiry 72 h; reports 5/24 h (child reports 3/24 h); geohash precision 7; half-life 90 d; semantic threshold 0.30; evidence retention 30 d (7/30/90); invitation expiry 7 d; decoy = calculator, 2 s hold on '=' to return; 3 voice enrolment samples; up to 10 trustees.
- Duress phrase also switches app to decoy screen (FR-06.01); safe phrase on stop-sharing screen = opt-out confirmation (FR-03.05/05.02).
- NFR targets are proposed requirement values; sections 4.5/5.1 referenced as typed text (convert to fields).
- Appendix B must hold the 23 use cases not in Ch3 (data for them still to be written; UC list and 6 specs are in ch3_data.py).
- Limitation to record in Ch6: Android 11+ shows an OS microphone indicator that cannot be hidden, which can reveal evidence recording in a silent SOS.

## Full document built (2026-10-22): Muhaffiz-SRS-SDS.docx (+ .pdf), 152 pages, validated.
Ch4-6 decisions to confirm: alert page on alert.muhaffiz.live; admin API under muhaffiz.me/api/v1; three environments; test counts (24 UT, 29 FT, 32 BRT, 14 IT, NF per NFR); RTM status column empty; milestone Status = Scheduled; ADR names sherpa-onnx/YAMNet/MiniLM/Drift/Riverpod/MapLibre (unverified, in Appendix C); Document Status page is the only disclaimer.
Rebuild: cd Documents/SRS/build && SRS_WORK=<tmp> SRS_RENDER=<tmp> python3 build.py

## Diagram overhaul (2026-10-23)
- All diagrams redrawn: custom portable SVG (no filters/markers/gradients; needed because Word/LibreOffice dropped the contents of the earlier SVGs) in build/diag.py, diag3.py, seq2.py, swim.py, figs_*.py; Graphviz-WASM (build/gv_*.py, dot_render.mjs, requires node_modules at scratchpad gv/) for class, state, activity, ER.
- Diagram counts: 4 use-case, 14 sequence, 8 class, 9 activity (4 plain, 5 swimlane), 9 state, 4 ER, architecture, deployment, component, navigation, context, 8 mockup figures + 2 admin screens.
- All pages are portrait (landscape sections removed 2026-10-23); mockups are 2 phones per figure (ui_k1-5, ui_m1-7), admin screens 740 px wide.
- Mermaid was requested then dropped by the user; do not use it.
- Check legibility with build/audit_figs.py (target >= ~6 pt at print size).
