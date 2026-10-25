# Template Compliance Checklist: Muhaffiz SRS & SDS

**Template:** `Documents/Reference/SRS-Template.docx` (Air University SRS & SDS; its printed pages 1–49).
**Audited document:** `Documents/SRS/Muhaffiz-SRS-SDS.pdf` (206 pages). Page references are **PDF p. (printed p.)**, where printed = PDF − 12 from PDF page 13 onwards.

**Status key:**
- **C**: Compliant.
- **P**: Partially compliant.
- **N**: Non-compliant or missing.
- **NA**: Not applicable or not required.
- **NYA**: Not yet assessable, because it depends on implementation.
- **?**: Unclear whether the template requires it.

The "Finding" column refers to IDs in `audit-report.md`.

## Front matter

| # | Template item | Status | Location | Notes / Finding |
|---|---|---|---|---|
| F1 | Cover: university, document type, project title, version | C | p.1 | Title *Muhaffiz: Offline-First Safety for Women and Children*, v1.0. The former name "Hifazat" is not mentioned (N08) |
| F2 | Cover: student names and registration numbers | C | p.1 | Two members; the template's third line was removed (team of two) |
| F3 | Cover: supervisor and degree line | C | p.1 | Kanwal Batool; BS Software Engineering (2023–2027) |
| F4 | Revision History table ("record every submitted revision") | P | p.2 | Table present but empty (N01) |
| F5 | Application Evaluation and Review History (committee comments and actions) | P | p.2 | Table present but empty; approval of scope changes not recorded (N01, M17) |
| F6 | Approval table (Supervisor, FYP Head) | C | p.2 | Names filled in; signature and date left blank for signing |
| F7 | Table of Contents (generated) | P | pp.3–5 | Generated field; entries 3.2.10–3.2.22 have no space after the number (N03) |
| F8 | List of Figures (generated) | C | pp.6–7 | 68 figures |
| F9 | List of Tables (generated) | C | pp.8–12 | 175 tables |

## Chapter 1: Introduction

| # | Template item | Status | Location | Notes / Finding |
|---|---|---|---|---|
| 1.0 | Chapter Overview | C | p.13 (1) | |
| 1.1 | Purpose: product and intended readers | C | p.13 (1) | Readers listed |
| 1.2 | Scope: In scope, Out of scope, Benefits table | C | pp.14–15 (2–3) | Table 1. Problem statement and objectives absent from the chapter (M16) |
| 1.3 | Modules: ID, name, description, primary actor | P | pp.15–16 (3–4) | Table 2 complete; 21 modules versus 16 in the proposal and 19 in the brief; approval not documented (M17) |
| 1.4 | Definitions, acronyms and abbreviations, alphabetical | P | pp.17–19 (5–7) | Alphabetical; missing terms and OTP expansion (N09) |
| 1.5 | Document overview | C | pp.19–20 (7–8) | Also defines the identifier scheme |
| 1.S | Chapter Summary | C | p.20 (8) | Numbered as 1.6 (X01) |

## Chapter 2: Overall Description and Requirements Elicitation

| # | Template item | Status | Location | Notes / Finding |
|---|---|---|---|---|
| 2.0 | Chapter Overview | C | p.21 (9) | |
| 2.1 | Product perspective (new or replacement; relation to existing systems; context diagram) | P | pp.21–23 (9–11) | Fig. 1 present; no named or cited existing systems (O17) |
| 2.2 | User classes table (description, skills, responsibilities; access level; frequency) | P | p.23 (11) | Table 4 complete; children as users not addressed (O07) |
| 2.3 | Operating environment table, plus OE-n statements | C | p.24 (12) | Table 5, OE-1 to OE-4. Runtime inconsistency (N17); Android feasibility (M11) |
| 2.4a | Constraints CON-n with rationale | C | pp.25–26 (13–14) | CON-1 to CON-12; CON-1 rationale overstated (M11); CON-8 versus Cloud Functions (O22) |
| 2.4b | Assumptions and dependencies table (ID, type, statement, rationale, impact) | C | pp.26–27 (14–15) | AS-1 to AS-9, DEP-1 to DEP-7; no legal-review assumption (O20) |
| 2.5a | Elicitation techniques explained and justified | P | pp.27–29 (15–17) | Survey and interviews described; sample size unverifiable; no questionnaire or sampling description (M14) |
| 2.5b | Stakeholders | C | p.29 (17) | |
| 2.5c | Prioritization method | C | p.29 (17) | High, Medium, Low with Table 9 |
| 2.5d | Validation | C | pp.29–30 (17–18) | Reviews, acceptance criteria, RTM |
| 2.5e | Technique table (technique, stakeholders, purpose, evidence) | C | p.30 (18) | Table 10; "users" in prototyping not evidenced (minor) |
| 2.S | Chapter Summary | C | p.30 (18) | |

## Chapter 3: Software Requirements Specification

| # | Template item | Status | Location | Notes / Finding |
|---|---|---|---|---|
| 3.0 | Chapter Overview | C | p.31 (19) | |
| 3.1 | Functional requirement catalogue (FR ID, module, title, priority, dependencies) | C | pp.31–33 (19–21) | Table 11, 87 FRs; count verified |
| 3.2a | One specification table per FR with all attributes (ID, title, requirement, source, rationale, BR, dependencies, priority, acceptance criteria) | C | pp.34–68 (22–56) | All 87 tables use the full attribute set |
| 3.2b | Responses to valid input, invalid input and error conditions | P | pp.34–68 | Many FRs give no invalid-input or error behaviour (for example FR-02.02, FR-10.03, FR-19.05); contradictions C01, M02, M03 |
| 3.2c | "shall" used for mandatory requirements; IDs kept throughout | C | throughout | Automated check: no references to undefined IDs |
| 3.2d | Use-case diagram(s) | P | pp.69–70 (57–58) | Figs. 2–5; actor and include issues (O16, N18); small text (N06) |
| 3.2e | Use-case specification for each substantial use case (all template fields) | C | pp.71–74 (59–62); App. B pp.192–202 | 29 use cases, all fields present; UC-01 precondition conflict (N12) |
| 3.2f | Use case list | **N in PDF** | p.70 (58) | Table 99 rows lost in the PDF export; present in the `.docx` (M01) |
| 3.3 | Business rules table (BR ID, rule, source, related FR/UC, priority) | C | pp.74–77 (62–65) | 32 rules; BR-02 versus BR-03 contradiction (C01) |
| 3.4a | NFR categories: reliability, usability, performance, security, maintainability, other | C | pp.77–80 (65–68) | 42 NFRs including privacy, safety and robustness |
| 3.4b | Each NFR specific, quantitative, verifiable, with target and verification method | P | pp.77–80 | Reference device undefined (O19); no false-trigger or keyword error-rate targets (O05); latency conflict (M04); PRV-03 subjective (N15) |
| 3.4c | Reliability distinguished from availability | P | pp.77, 80 | Only NFR-AVL-01; no backend availability target |
| 3.5a | User interface requirements (standards, fonts, layout, navigation, messages, localization, accessibility; mockups identified as conceptual or committed) | C | pp.80–81 (68–69) | UI-1 to UI-10; UI-9 states the designs are committed |
| 3.5b | Software interfaces with names and versions | P | pp.81–82 (69–70) | SI-1 to SI-14; few versions given |
| 3.5c | Hardware interfaces | C | p.82 (70) | HI-1 to HI-8 |
| 3.5d | Communications interfaces | C | pp.82–83 (70–71) | CI-1 to CI-7; CI-6 versus UC-25 A3 (M12) |
| 3.5e | Interface table (ID, type, element, data, protocol, error handling) | P | p.83 (71) | Table 113 omits several interfaces (N20); word breaks (N04) |
| 3.S | Chapter Summary | C | p.83 (71) | |

## Chapter 4: System Design

| # | Template item | Status | Location | Notes / Finding |
|---|---|---|---|---|
| 4.0 | Chapter Overview | C | p.84 (72) | |
| 4.1 | Design methodology and process model, justified | C | pp.84–85 (72–73) | Object-oriented design, incremental and risk-driven process |
| 4.2a | Box-and-line architecture view | C | p.86 (74) | Fig. 6; small text (N06) |
| 4.2b | Architecture style | C | p.85 (73) | Layered, event-driven core, backend-as-a-service |
| 4.2c | Decomposition | C | pp.86–87 (74–75) | Table 114 |
| 4.2d | Deployment view | C | p.88 (76) | Fig. 7 |
| 4.2e | Architecture decision records (ADRs) | C | pp.88–89 (76–77) | ADR-01 to ADR-13; citation issue in ADR-04 (O17) |
| 4.3a | Use case diagram | C | in 3.2.22 | Referenced from 4.3 |
| 4.3b | Class diagrams (classes, attributes, operations, multiplicity) | P | pp.91–98 (79–86) | Figs. 8–15; used partly as flow diagrams; multiplicity and auth issues (O16) |
| 4.3c | Sequence diagrams (participants, guards, alternatives) | P | pp.99–112 (87–100) | Figs. 16–29; overlapping labels (N05) and fragment-nesting errors (O16) |
| 4.3d | Activity diagrams (decisions, start/end, swimlanes) | P | pp.113–122 (101–110) | Figs. 30–39; logic defects (O16), onboarding conflict (O06) |
| 4.3e | State diagrams (states, events, guards, initial/final) | P | pp.123–131 (111–119) | Figs. 40–48; Fig. 41 safety contradiction (M07); missing failure paths (O16) |
| 4.3f | Component diagram (provided/required interfaces) | P | p.132 (120) | Fig. 49 has no interfaces (N19) |
| 4.3g | Data flow diagrams | NA | p.90 (78) | Exclusion justified |
| 4.3h | Event-response table (event-driven behaviour) | C | pp.132–133 (120–121) | Table 116; inherits C01 |
| 4.3i | Every model explained, labels readable | P | 4.3 | Explanatory text present; overlaps and sub-6 pt text (N05, N06) |
| 4.4a | Data dictionary, alphabetical, with types | P | pp.134–135 (122–123) | Ordering slip; no methods; missing entities (N10, O09) |
| 4.4b | ER diagram | C | pp.136–139 (124–127) | Figs. 50–53 (crow's-foot notation) |
| 4.4c | Normalization, indexes, constraints | C | pp.139–140 (127–128) | Table 118 |
| 4.4d | Retention, validation, integrity | P | p.133 (121) | Retention incomplete (M13) |
| 4.5a | Screen images | P | pp.142–146 (130–134) | Figs. 55–59 (renderings); decoy hint defect (M10); mockup glitches (N07) |
| 4.5b | Screen objects and actions | C | pp.146–147 (134–135) | |
| 4.5c | Navigation flow | C | p.141 (129) | Fig. 54 |
| 4.5d | Screen table (ID, role, purpose, objects, FR/UC) | C | pp.147–148 (135–136) | Table 119, S-01 to S-26 |
| 4.6 | Security, error-handling and logging design with table | P | pp.148–149 (136–137) | Table 120 present; threat coverage incomplete (M19) |
| 4.7a | Risk table (probability, impact, owner, mitigation, contingency) | C | pp.150–151 (138–139) | RSK-01 to RSK-16; RSK-16 rating (O01); word breaks (N04) |
| 4.7b | Sprint or milestone plan with dependencies | P | p.151 (139) | Milestones and dependencies, no dates (team decision); no effort estimates (O21) |
| 4.S | Chapter Summary | C | pp.151–152 (139–140) | |

## Chapter 5: Implementation and Deployment

| # | Template item | Status | Location | Notes / Finding |
|---|---|---|---|---|
| 5.0 | Chapter Overview | C | p.153 (141) | |
| 5.1 | Algorithms with pseudocode, inputs/outputs, complexity; template examples replaced | P | pp.153–157 (141–145) | A1 to A10 with a parameter table; A1 and A4 defects (O04, O03); A3 and A5 inherit C01 |
| 5.2 | External APIs/SDKs: name, version, purpose, endpoint/function | P | pp.157–158 (145–146) | Versions vague (N14) |
| 5.3 | REST API: route, method, auth, inputs, outputs, status codes, errors, implementation component, related requirements | P | p.159 (147) | Table 135; no implementation components (N14); client-supplied recipients (M19); word breaks (N04) |
| 5.4 | Implemented user interface per subsystem | **NYA / N** | pp.159–168 (147–156) | Design renderings under an "implemented" heading; realistic metrics in Fig. 67 (M15) |
| 5.5a | Environments (development, testing, staging, production) | P | p.168 (156) | Three environments, no staging (acceptable); test numbers not substituted (C02) |
| 5.5b | Server setup | C | p.168 (156) | |
| 5.5c | Environment variables and secrets handling | **N** | not covered | (N14) |
| 5.5d | CI/CD | C | p.168 (156) | |
| 5.5e | Backup and monitoring | C | pp.168–169 (156–157) | |
| 5.5f | Rollback | **N** | not covered | (N14) |
| 5.5g | Deployment diagram | C | p.169 (157) | Refers to Fig. 7 |
| 5.S | Chapter Summary | C | p.169 (157) | |

## Chapter 6: Testing, Evaluation and Conclusion

| # | Template item | Status | Location | Notes / Finding |
|---|---|---|---|---|
| 6.0 | Chapter Overview | C | p.170 (158) | |
| 6.1 | Unit tests (valid, invalid, boundary) with Actual Result and Result | P / NYA | pp.170–171 (158–159) | UT-01 to UT-24 designed; results "-" (not executed); UT-08 encodes C01 |
| 6.2 | Functional tests | P / NYA | pp.172–173 (160–161) | FT-01 to FT-29; FT-25 and FT-18 safety issue (C02) |
| 6.3 | Business-rule tests (decision tables) | P / NYA | pp.174–175 (162–163) | BRT-01 to BRT-32 |
| 6.4 | Integration tests | P / NYA | pp.175–176 (163–164) | IT-01 to IT-14 |
| 6.5 | Non-functional tests | P / NYA | pp.176–178 (164–166) | NF-01 to NF-42; method column filled mechanically (O19) |
| 6.6 | Test summary and defect log | NYA | p.179 (167) | Planned 141, executed 0; defect log empty |
| 6.7 | Requirements traceability matrix (source, design, implementation, test, status) | P | pp.179–187 (167–175) | 55 interface and constraint requirements absent (M18); inaccurate mappings; empty status (O15) |
| 6.8 | Conclusion, limitations, future enhancements | P | pp.187–188 (175–176) | "Realized" claim and undefined BO-1 to BO-6 (M15, M16); Android version error (N13) |
| 6.S | Chapter Summary | C | p.188 (176) | |

## Closing parts and appendices

| # | Template item | Status | Location | Notes / Finding |
|---|---|---|---|---|
| R1 | References in IEEE style, numbered in order of first appearance | P | p.189 (177) | Format and order correct; only 7 entries; [6] misattributed; uncited claims (O17) |
| R2 | Every citation in the list and vice versa | C | throughout | [1] to [7] all cited |
| A1 | Appendix: use case list | C | pp.190–191 (178–179) | Appendix A, Table 145 |
| A2 | Appendix: glossary | C (alternative) | Section 1.4 | Glossary kept in 1.4 and stated as such (p.20) |
| A3 | Appendix: TBD list | C | p.203 (191) | Appendix C, TBD-1 to TBD-8; no legal-review or scope-approval item (O20, M17) |
| A4 | Appendix: sample test data | C | pp.204–205 (192–193) | Appendix D; includes the real numbers 15 and 1122 (C02) |
| A5 | Detailed use cases (Appendix B, as the template suggests) | C | pp.192–202 (180–190) | |
| A6 | Template Appendix D "Diagram Notation Reference" ("Include only notation relevant … Insert the appropriate standard symbol") | ? | not provided | Wording suggests a deliverable; confirm with the supervisor (X03) |
| A7 | Template example appendices (cafeteria, MHCF, Appendices E–G) removed | C | — | No leftover template or example text found |
| A8 | Document Status page | NA (extra) | p.206 (194) | Not in the template; it is the only disclaimer, and it is at the end (M15) |

## Formatting guidelines (template pp.17–18)

| # | Rule | Status | Evidence | Notes / Finding |
|---|---|---|---|---|
| G1 | Each chapter starts on a new page | C | Heading 1 has `pageBreakBefore` | |
| G2 | Each chapter begins with an Overview and ends with a Summary | C | Chapters 1–6 | Summaries numbered (X01) |
| G3 | Times New Roman throughout | **P** | `.docx` styles use Times New Roman; the PDF embeds Liberation Serif, Liberation Sans and DejaVu | Font substitution at export (N02) |
| G4 | Chapter headings 16 pt bold | C | Heading 1: 16 pt bold | Coloured navy (cosmetic) |
| G5 | Section headings 14 pt bold | C | Heading 2: 14 pt bold | |
| G6 | Body 12 pt, justified | C | SRSBody style: 12 pt, justified | Tables use 9 pt text (not specified by the template) |
| G7 | Line spacing 1.5 | C | `line=360` | |
| G8 | 18 pt after each paragraph | C | `after=360` | |
| G9 | First-line indent 1.27 cm | C | `firstLine=720` | |
| G10 | Margins 2.54 cm with page numbers in the footer | C | `pgMar` 1440 on all sides; footer "n \| Page" from p.13 | Front matter unnumbered, as in the template |
| G11 | Built-in Heading 1–3 styles linked to multilevel numbering | C | `numPr` on Heading 1–3 | |
| G12 | Captions inserted automatically; figure captions below, table captions above | C | 243 SEQ fields; placement verified visually | Sequential numbering rather than chapter-based (X02) |
| G13 | Cross-references inserted as fields, never typed | C | 165 REF fields; 0 hand-typed references found in body text | |
| G14 | TOC, List of Figures and List of Tables generated | C | TOC fields present | Spacing defect (N03) |
| G15 | IEEE citations, placed before punctuation | C | for example "lifetime [1]." | |
| G16 | Pre-submission checklist: fonts, spacing and justification consistent | P | | Font substitution in the PDF (N02); table column word breaks (N04) |

## Summary of compliance

- **Missing or non-compliant:** Table 99 rows in the PDF (M01); 5.5 secrets handling and rollback (N14); Times New Roman in the PDF (N02).
- **Not yet assessable:** 5.4 Implemented UI, and the Chapter 6 results, executed counts and defect log. Acceptable before implementation only if clearly labelled (M15).
- **Unclear:** template Appendix D notation reference (X03).
- **Partially compliant:** the empty Revision and Review History tables, the RTM coverage, the component-diagram interfaces and the NFR verifiability details. These are listed above.
- **Compliant:** the overall structure and section order match the template completely, with no reordered or renamed template sections. The extra sections added are the numbered chapter summaries, the 3.2.x module subsections, 4.3.1–4.3.5 and the Document Status page.
