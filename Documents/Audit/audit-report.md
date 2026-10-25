# Independent Audit Report: Muhaffiz (Hifazat) SRS & SDS

| Item | Value |
|---|---|
| Document audited | `Documents/SRS/Muhaffiz-SRS-SDS.pdf` (206 pages, generated 23 Oct 2026 01:12 from `Muhaffiz-SRS-SDS.docx`) |
| Title on cover | *Muhaffiz: Offline-First Safety for Women and Children*, Version 1.0 |
| Template | `Documents/Reference/SRS-Template.docx` (Air University SRS & SDS template) |
| Project brief | `Documents/Reference/Hifazat Feature Document.md` (19 modules) and `Documents/Reference/Muhaffiz_FYP_Scope_Document-UnUpdated.docx` (proposal, 16 modules) |
| Supporting context | `Documents/Notes/project-context.md`, `Documents/Notes/progress.md`, `Documents/Reference/Hifazat Full Chat Record.md` |
| Audit date | 23 October 2026 |
| Status of original SRS | Not modified |

## How to read this report

**Page references.** Every location is given as **PDF p.N (printed p.M)**. PDF page numbers are the viewer's page index (1 to 206). The printed numbers are the footer labels, which start at 1 on PDF page 13, so printed = PDF − 12. Pages 1–12 (cover, history tables, table of contents, list of figures, list of tables) have no printed number.

**Severity.**

| Severity | Meaning |
|---|---|
| Critical | Safety-critical contradiction or instruction that could cause real-world harm; must be fixed before submission |
| Major | Defect that affects correctness, feasibility, traceability, template compliance or academic integrity in a way an evaluator is likely to challenge; should be fixed before submission |
| Moderate | Defect or gap that weakens quality but does not block evaluation |
| Minor | Editorial, formatting or local inconsistency |
| Observation | Not a defect: context, optional improvement or a positive note |

**Classification.** Each finding is tagged as one of:

- **Confirmed defect:** demonstrable from the document text, the rendered PDF or the source `.docx`.
- **Reasonable concern:** a likely problem that depends on external facts (Android platform behaviour, service policies, approvals) that this audit could not verify, because no external research was requested.
- **Subjective recommendation:** a design or presentation choice the team may reasonably decline.

**Mandatory / optional.** "Mandatory" means the correction is needed for internal consistency, template compliance, safety or integrity. "Optional" means it would improve the document but is not required.

**Independence note.** The project files (`progress.md`) record that this SRS was drafted with AI assistance in earlier sessions. This audit did not rely on those notes for correctness. They were used only to identify source conflicts, and every finding was checked against the document itself.

## Findings count

| Severity | Count |
|---|---|
| Critical | 2 |
| Major | 19 |
| Moderate | 22 |
| Minor | 20 |
| Observation | 7 |
| **Total** | **70** |

---

# 1. Critical findings

### AUD-C01 Silent (duress) SOS contradicts itself across rules, requirements, algorithms and screens
- **Severity:** Critical · **Category:** Requirements consistency / Safety · **Classification:** Confirmed defect · **Mandatory**
- **Location:** BR-02 and BR-03, PDF p.75 (printed p.63); FR-01.04, PDF p.35 (23); FR-02.04, PDF p.38 (26); FR-03.04 and FR-03.05, PDF p.40 (28); FR-06.01, PDF p.44 (32); UC-03 steps 3 and 6, PDF p.72 (60); NFR-SAF-01, PDF p.80 (68); Table 116, PDF p.133 (121); Fig. 19, PDF p.102 (90); Fig. 33, PDF p.116 (104); Fig. 40, PDF p.123 (111); Fig. 55 countdown screen, PDF p.142 (130); Algorithms A3 and A5, PDF pp.154–156 (142–144); UT-08, PDF p.171 (159); FR-19.03 and HI-4, PDF pp.65, 82 (53, 70).
- **What is wrong:** BR-03 and FR-01.04 say a silent SOS (including one started by the duress phrase) "shall play no sound, shall not vibrate, shall show no SOS indication on the screen". FR-03.04, BR-02, UC-03, A3, Fig. 19, Fig. 33 and UT-08 route the duress phrase through the 20-second countdown, which vibrates and shows a full-screen "Possible distress detected … I'm okay, cancel" screen (Fig. 55). NFR-SAF-01 requires the countdown for every voice SOS. FR-19.03 and HI-4 then add a vibrating 30-second escalation warning "in silent mode", which BR-03 forbids. The decoy timing also conflicts: A5 shows the decoy before the countdown, while UC-03 step 6, Fig. 19 and Fig. 33 show it after the SOS starts.
- **Why it matters:** The duress phrase is one of the six claimed novel contributions. Under coercion, 20 seconds of vibration and a visible cancel screen can expose the user, and the attacker can simply tap "cancel". An implementer cannot satisfy both rule sets, and the tests (UT-08, FT-03, BRT-03) would pass or fail depending on which rule they read.
- **Evidence:** BR-03: "A silent SOS (silent default mode or duress phrase) produces no sound, vibration, visible alert". BR-02: "Automatic and voice triggers start a 20-second vibration-only countdown". UT-08 expected result: "decoy shown and silent SOS countdown starts".
- **Recommended correction:** Decide one behaviour for the duress path and apply it everywhere. A typical option is that the duress phrase starts an immediate silent SOS with no vibration and no countdown screen, and the decoy appears at once. If a cancel window is kept, it should be covert (no vibration, cancelled through the hidden decoy gesture). Then update BR-02, BR-03, FR-01.04, FR-02.04, FR-03.04, NFR-SAF-01 (exclude the duress phrase), FR-19.03, HI-4, A3, A5, Figs. 19, 30, 33 and 40, Table 116, UT-08, FT-03 and BRT-02/03.

### AUD-C02 The test plan would send real SOS messages and calls to Police 15 and Rescue 1122
- **Severity:** Critical · **Category:** Testing / Safety / Ethics · **Classification:** Confirmed defect · **Mandatory**
- **Location:** FT-25, PDF p.173 (161); FT-18, PDF p.173 (161); FR-19.04 defaults, PDF p.65 (53); Table 175 sample directory, PDF p.204 (192); test environment, Table 136, PDF p.168 (156); Chapter 6 introduction, PDF p.170 (158).
- **What is wrong:** FT-25's expected result is a "message to Police 15 and Rescue 1122 by SMS if not cancelled". FT-18 taps "Call" on directory entries, and the sample directory contains the real numbers 1122 and 15. Nothing in Section 5.5 or Chapter 6 requires substitute numbers in the testing environment.
- **Why it matters:** Running the test plan as written would send false emergency messages or calls to real emergency services. That could divert responders and is likely to breach the services' terms of use.
- **Recommended correction:** State in Chapter 6 and Section 5.5 that all authority and helpline numbers in development and testing builds are replaced by team-controlled numbers. Add a build-time guard that blocks 15, 1122, 1099 and 112 outside production. Change FT-25 and FT-18 to use test numbers, and add a test that verifies the guard.

---

# 2. Major findings

## 2.1 Template compliance and layout

### AUD-M01 Table 99 "Use case list" has no rows in the PDF
- **Severity:** Major · **Category:** Template / Layout · **Classification:** Confirmed defect · **Mandatory**
- **Location:** Section 3.2.22, PDF p.70 (58).
- **What is wrong:** Only the header row (Use Case ID, Name, Actors, Module, Related FRs, Business Rules) is rendered, and Table 100 starts on the next page. The source `.docx` contains all 30 rows (header plus UC-01 to UC-29), so the rows were lost in the PDF export. The text of the missing rows (for example "FR-01.01 to FR-01.04") appears nowhere in the PDF. An automated comparison found no other table with missing rows.
- **Why it matters:** The table that maps use cases to modules, requirements and rules is visibly empty in the submission copy.
- **Recommended correction:** Re-export the PDF, for example after allowing rows to break across pages or removing "keep with next" on the caption and header, and check p.70 again. Comparing table row counts between the `.docx` and the PDF before submission would catch any recurrence.

## 2.2 Requirements quality and SOS lifecycle

### AUD-M02 The "private" opt-out is visible to other circle members, but the requirements say it is not
- **Severity:** Major · **Category:** Requirements consistency / Privacy · **Classification:** Confirmed defect · **Mandatory**
- **Location:** FR-05.03, PDF pp.42–43 (30–31); FR-04.02, PDF p.41 (29); FR-05.04 and FR-05.05, PDF pp.43–44 (31–32); BR-11 to BR-13, PDF p.75 (63); Fig. 20 step 9, PDF p.103 (91); Fig. 43, PDF p.126 (114); Fig. 56, PDF p.143 (131); Fig. 58, PDF p.145 (133).
- **What is wrong:** FR-05.03's acceptance criterion says "Other members' devices show no event when sharing stops". FR-04.02 shows each member's status ("sharing or stopped") in real time. FR-05.05 propagates "each sharing change" within NFR-PER-04 (5 s), FR-05.04 labels the marker "Not live", Fig. 20 step 9 sends a listener update to the other member's device, and Fig. 56 shows "Bilal • Last known location, Not live • 3 h ago". The source brief has the same tension (Feature Document 7.5.3 versus 7.5.4 and 7.5.5).
- **Why it matters:** The opt-out is meant to be duress-resistant. Users and evaluators will read "no event" as "undetectable", but a watcher sees the state change within seconds. The stop-sharing screen (Fig. 58) is accurate ("They will see your last location, marked 'Not live'"), so the requirement text, not the design, is wrong.
- **Recommended correction:** Reword FR-05.03 and BR-11 to say that no notification, message or push is generated, but the member's status changes to "Not live" for others. Fix the acceptance criterion to match. Add an explicit limitation and risk (RSK-10) that a watcher can detect a stop.

### AUD-M03 Stopping location sharing requires voice activation, which contradicts the location toggle
- **Severity:** Major · **Category:** Requirements consistency / Privacy · **Classification:** Confirmed defect · **Mandatory**
- **Location:** UC-09 preconditions and E1, PDF pp.72–73 (60–61); FR-05.02, PDF p.42 (30); BR-11, PDF p.75 (63); BR-09, PDF p.75 (63); FR-15.02, PDF p.57 (45); Fig. 43, PDF p.126 (114); Fig. 58, PDF p.145 (133); Fig. 59 settings, PDF p.146 (134).
- **What is wrong:** UC-09 requires "voice activation is on and the safe phrase is enrolled". If the voice engine is unavailable, the only option offered is to leave the circle. Fig. 43 has only one path to "Stopped" (the safe phrase), and the stop-sharing screen offers only the phrase or Cancel. BR-09 and FR-15.02, however, give location sharing its own toggle that "can be changed at any time and takes effect immediately", and Fig. 59 shows that toggle.
- **Why it matters:** The two mechanisms disagree. As written, a person who does not want always-on microphone listening cannot pause sharing without leaving the circle, which undermines the unconditional opt-out the product promises.
- **Recommended correction:** Specify both paths: a standard non-voice "Stop sharing" control (the FR-15.02 toggle) and the safe phrase as an optional discreet path, both with the same private-confirmation behaviour. Update UC-09, BR-11, FR-05.02, Fig. 43 and Fig. 58.

### AUD-M04 SOS dispatch latency targets contradict the designed dispatch sequence
- **Severity:** Major · **Category:** Requirements consistency / Performance · **Classification:** Confirmed defect · **Mandatory**
- **Location:** FR-01.01 acceptance criterion, PDF p.34 (22); NFR-PER-01, PDF p.78 (66); NFR-REL-01, PDF p.77 (65); FT-01, PDF p.172 (160); UC-01 steps 3–6, PDF p.71 (59); Fig. 17 step 1, PDF p.100 (88); Fig. 30, PDF p.113 (101); Fig. 32, PDF p.115 (103); Fig. 40, PDF p.123 (111); A3 line 6 and A4 line 1, PDF p.155 (143); Table 123, PDF p.153 (141).
- **What is wrong:** Three different targets apply to the same event: dispatch within 1 s (FR-01.01, FT-01), first channel within 2 s (NFR-PER-01) and SMS within 5 s (NFR-REL-01). Every design artefact obtains the location before dispatch, waiting up to T_fix = 10 s, then probes the backend for up to T_probe = 3 s. The worst case is about 13 s before the first SMS.
- **Why it matters:** These are the most important timing requirements in a safety application. As specified, the design cannot meet them, and the tests will disagree with each other.
- **Recommended correction:** Either dispatch immediately with the cached location (and its age) and send a follow-up when a fresh fix arrives, or relax the targets explicitly. Align FR-01.01, NFR-PER-01, NFR-REL-01, FT-01, A3, A4 and the diagrams on one number. Also decide whether the tier probe may block SMS, which it should not, since SMS needs no data.

### AUD-M05 Acknowledgements cannot arrive offline, so every offline SOS escalates to the authorities
- **Severity:** Major · **Category:** Requirements / Design / Safety · **Classification:** Confirmed defect · **Mandatory**
- **Location:** FR-19.01 and FR-19.02, PDF p.64 (52); ADR-13, PDF p.89 (77); CI-7, PDF p.83 (71); API-03 and API-04, PDF p.159 (147); NFR-AVL-01, PDF p.80 (68); Fig. 21, PDF p.104 (92); data dictionary, PDF p.134 (122); UC-29 E1, PDF p.202 (190).
- **What is wrong:** Acknowledgements arrive only through Firestore listeners or the hosted alert page (`/alert/{token}`). ADR-13 rejects SMS-reply parsing. At Tier 1 the phone has no data, so it cannot receive any acknowledgement, and the 3-minute timer (FR-19.02) "shall still run". A trustee who receives only the SMS and has no data cannot acknowledge either (CI-7: "Link opened offline: acknowledgement not recorded"). The alert-page token must exist on the server, yet the Tier-1 SMS path makes no backend call (NFR-AVL-01), and no API or entity creates a server-side alert record. The `Acknowledgement` entity references `sosId`, but `SosEvent` is stored on the device only.
- **Why it matters:** In the scenario the product is designed for (no data), every SOS escalates to Police 15 and Rescue 1122 after 3.5 minutes, even when trustees saw the SMS. The acknowledgement link in such an SMS would also return 404. This creates systematic false escalations and undermines the claimed follow-through.
- **Recommended correction:** Specify (a) how and when the server-side alert record and token are created, for example on first connectivity, and what the SMS contains if no token exists yet; (b) an offline acknowledgement path, such as an SMS reply keyword or a missed-call-back, stating the permission trade-off; or (c) a rule that escalation at Tier 1 requires the user's confirmation. Add a server-side alert entity to the data model and tests for the offline case.

### AUD-M06 There is no requirement to end an active SOS or retract a false alarm
- **Severity:** Major · **Category:** Requirements completeness / Safety · **Classification:** Confirmed defect · **Mandatory**
- **Location:** Fig. 31, PDF p.114 (102), "User ends the SOS"; Fig. 41, PDF p.124 (112); Table 114 `complete()`, PDF p.86 (74); Fig. 56 SOS-active screen, PDF p.143 (131); FR-01.01, PDF p.34 (22).
- **What is wrong:** No FR, UC, BR or screen control specifies how an SOS ends, whether trustees and helpers receive an "I am safe / false alarm" follow-up, or what happens to the escalation timer and the recording. The SOS-active screen offers only "Stop alarm" and "Evidence". A manual SOS has no countdown, and a lock-screen tap starts one immediately, so accidental activation cannot be undone.
- **Why it matters:** The brief asks for handling of false alarms, cancellation and accidental activation. Without a retraction path, every accidental SOS alarms all trustees and escalates to the authorities unless someone acknowledges it.
- **Recommended correction:** Add requirements, a use case and tests for ending or cancelling an active SOS. These should cover the follow-up message to all recipients, stopping the escalation timer, what happens to the recording, and protection against a coerced cancel, for example a cancel that requires the real PIN and reports a duress cancel as still active.

### AUD-M07 The SOS state machine ends the SOS, and stops recording, as soon as escalation is sent
- **Severity:** Major · **Category:** Diagram / Safety · **Classification:** Confirmed defect · **Mandatory**
- **Location:** Fig. 41, PDF p.124 (112); compare FR-19.03, PDF p.65 (53), and Fig. 31, PDF p.114 (102).
- **What is wrong:** "Escalated" moves to "Closed" on "message sent or queued", and the entry action of Closed is "stop alarm and recording". "User cancels warning" also moves to Closed, which ends the whole SOS, whereas FR-19.03 and Fig. 31 cancel only the escalation and keep the SOS active. "Awaiting response" has no "user ends the SOS" transition.
- **Why it matters:** The escalated state is the most serious case (nobody has responded), yet the model stops the siren and evidence recording at that moment. The diagram contradicts the written requirements.
- **Recommended correction:** After "Escalated", return to an active state (for example "Escalated, awaiting response") that keeps the alarm and recording running. Make "user cancels warning" return to "Awaiting response" or "Active". Add user-end transitions from every active state.

## 2.3 Safety, privacy and security

### AUD-M08 Near Help reveals the requester's exact location to any helper who accepts; helper location handling is unspecified
- **Severity:** Major · **Category:** Safety / Privacy · **Classification:** Confirmed defect (missing specification) and reasonable concern (risk)
- **Location:** FR-08.01 to FR-08.03, PDF pp.47–48 (35–36); BR-18 and BR-19, PDF p.76 (64); UC-15, PDF p.197 (185); Fig. 24, PDF p.107 (95); Fig. 39, PDF p.122 (110); Table 118, PDF p.140 (128); TBD-7, PDF p.203 (191).
- **What is wrong:** When a helper accepts, the system "shall show the requester's exact location to that helper". Any number of helpers can accept, the requester does not confirm, the requester is not shown who the helper is, and there is no function to report or block a helper. "Verified" means only that an administrator looked at a photo of an identity document (TBD-7), with no authenticity check. Matching helpers "within 1 km" requires the server to know helpers' current positions, but no requirement covers how helper locations are collected, consented to, updated or retained. `HelperProfile` has no location attribute, even though Table 118 indexes "the geohash of the last position".
- **Why it matters:** A person in distress could disclose their exact position to an impostor or a stalker who passed a photo check. Continuous tracking of helpers is itself a privacy issue that is not consented to or specified.
- **Recommended correction (mandatory):** Specify helper location collection, consent, update frequency and retention. State the limits of "verified" in the SRS and the consent text. **(Optional, design choice):** add requester confirmation or a cap on the number of accepting helpers, show helper identity to the requester, and add a report-helper function.

### AUD-M09 Missing-child alerts are broadcast before any moderation, and child data retention is incomplete
- **Severity:** Major · **Category:** Safety / Privacy (child data) · **Classification:** Confirmed defect (inconsistency) and reasonable concern (abuse risk)
- **Location:** FR-17.01, FR-17.02, FR-17.05 and FR-17.06, PDF pp.60–62 (48–50); BR-27, PDF p.77 (65); SD-12, PDF p.149 (137); Fig. 25, PDF p.108 (96); Fig. 36, PDF p.119 (107); data dictionary, PDF p.134 (122).
- **What is wrong:** FR-17.05 says "publish a report immediately, place every report in the moderation queue". BR-27 says "Every report is reviewed", and SD-12 calls this an "immediate review queue", although review comes after the broadcast. Guardianship is self-attested (a tick box). The alert carries the description, last-seen place and time, and the guardian's phone number to every verified helper within 5 km. Only the photo is deleted when a report is found or expires; the child's name, age, description and last-seen data stay on the server with no retention rule.
- **Why it matters:** A false report can be used to locate a child or a parent who has fled, for example in a custody dispute, or to harass someone. The SRS does not discuss this risk, and child data is kept indefinitely.
- **Recommended correction (mandatory):** Make the moderation statements consistent, add an explicit risk and retention rule for all child-report fields, and state what helpers may do with the data. **(Optional, design choice):** pre-moderation before broadcast, a smaller radius, or less data in the broadcast.

### AUD-M10 The decoy screen design prints the hidden re-entry gesture on the screen
- **Severity:** Major · **Category:** UI design / Safety · **Classification:** Confirmed defect · **Mandatory**
- **Location:** Fig. 58 decoy screen, PDF p.145 (133); FR-06.01 and FR-06.02, PDF p.44 (32); UI-9, PDF p.81 (69).
- **What is wrong:** The calculator shows the line "Hold = for 2 seconds to open the real app" inside the phone frame. UI-9 makes Section 4.5 the committed design. FR-06.01 requires that the decoy "contain no reference to safety", and FR-06.02 requires that "no other action shall reveal it". The gesture is also fixed and documented publicly, so anyone who knows Muhaffiz knows how to get past the decoy.
- **Why it matters:** The decoy exists for the moment when someone forces the user to unlock the phone, and the design tells that person how to defeat it.
- **Recommended correction:** Remove the hint from the screen (if it is an annotation, move it into the caption). **Optional:** let the user set the re-entry code, for example a calculation that evaluates to a secret number.

### AUD-M11 Several requirements assume Android background behaviour that recent versions restrict
- **Severity:** Major · **Category:** Feasibility · **Classification:** Reasonable concern (Android platform behaviour not verified against current documentation in this audit) · **Mandatory to address**
- **Location:** FR-02.01 restart after reboot, PDF pp.36–37 (24–25); NFR-REL-03, PDF p.77 (65); Table 116 "Device restarts", PDF p.133 (121); FR-01.04 and FR-06.03 "without any visible sign", PDF pp.35, 45 (23, 33); FR-18.01 recording within 1 s from background triggers, PDF p.62 (50); FR-01.01 lock-screen action, PDF p.34 (22); OE-1 (Android 8.0+), PDF p.24 (12); CON-1 rationale, PDF p.25 (13); Limitations, PDF p.188 (176); RSK-16, PDF p.151 (139).
- **What is wrong:**
  - Microphone use from a foreground service started in the background, and starting a microphone-type foreground service at boot, are restricted on recent Android versions.
  - A foreground service must show a notification.
  - The microphone privacy indicator cannot be hidden. The SRS attributes it to Android 11; as far as this audit knows it arrived in Android 12.
  - Android has no third-party lock-screen widgets, so the "lock-screen SOS action" needs a defined mechanism (for example a Quick Settings tile or a notification action) and its locked-device behaviour.
  - CON-1 says Android "permits … background audio", which overstates the platform.
- **Why it matters:** Automatic detection, voice activation, the silent SOS and the lock-screen trigger are core features. If the acceptance criteria cannot be met on current Android versions, the evaluation cannot pass them.
- **Recommended correction:** Verify each behaviour against current Android documentation and record the findings as constraints. Specify the lock-screen mechanism, adjust the acceptance criteria (for example "restarts when the user next unlocks" where a boot start is not allowed), raise RSK-16 impact from Low to High, and correct the Android version in the limitations.

### AUD-M12 Escalation to authorities is specified as a working channel, but the call and share channels need user action and SMS acceptance is unverified
- **Severity:** Major · **Category:** Feasibility / External integration · **Classification:** Reasonable concern · **Mandatory to clarify**
- **Location:** FR-19.04 and FR-19.05, PDF p.65 (53); UC-25 A3 "the system places the call", PDF p.73 (61); UC-18 step 4, PDF p.198 (186); FR-11.02, PDF p.52 (40); CI-6 "Calls shall be placed through the Android dialer", PDF p.82 (70); AS-6, PDF p.26 (14); TBD-1, PDF p.203 (191); Fig. 65, PDF p.165 (153).
- **What is wrong:**
  - UC-25 A3 has the system place a call automatically after the timer expires, when the user may be incapacitated. CI-6 says calls go "through the Android dialer". To this audit's knowledge, Android does not let ordinary apps place calls to emergency numbers directly; it opens the dialer, which needs a user tap.
  - The "share" channel always needs user interaction.
  - Whether Police 15 and Rescue 1122 accept SMS is an open assumption (AS-6, TBD-1), yet SMS is the default channel and the UI says "Alerting authorities … (by SMS)".
  - The approved scope document excluded "automated dispatch integration with government emergency systems". The SRS correctly excludes direct integration, but FR-19 reads as a functioning dispatch.
- **Why it matters:** Follow-through is novel contribution 6. An evaluator will ask whether escalation reaches anyone. For an FYP it has to be presented as a simulated or unverified channel unless acceptance is confirmed.
- **Recommended correction:** Make UC-25, UC-18 and FR-11.02 consistent with CI-6 (dialer, user action). State in FR-19 and the limitations that escalation is demonstrated with test numbers and that real acceptance is unverified. Keep TBD-1 open until it is confirmed.

### AUD-M13 Account deletion and server-side data retention are not specified
- **Severity:** Major · **Category:** Privacy / Data design · **Classification:** Confirmed defect (missing requirements) · **Mandatory**
- **Location:** Section 4.4 retention paragraph, PDF p.133 (121); NFR-PRV-02, PDF p.79 (67); Table 117, PDF pp.134–135 (122–123); 4.6 logging, PDF p.148 (136).
- **What is wrong:** No requirement lets a user delete their account or their server data. A search of the full text finds no account-deletion requirement. Retention is defined only for evidence, heatmap reports (12 months), photos, identity images and technical logs (30 days). There is no retention rule for `Membership.lastShared` locations, `HelpRequest` (whose coordinates are sent to the server), acknowledgements, invitations (third-party phone numbers), trustee records (third parties' names, phones and emails, uploaded to the server without their knowledge), missing-child text fields, `AdminDecision` audit records, alert-page data or messaging tokens.
- **Why it matters:** The brief asks for retention, deletion and data minimisation. Location and third-party contact data are the most sensitive data the server holds.
- **Recommended correction:** Add a requirement for account and data deletion (including what happens to circles, reports and helper status), and a retention table covering every server entity and log. Decide whether trustees are told they were added.

### AUD-M19 Security design gaps: admin authentication, client-controlled recipients, client-side limits, number takeover, unprotected device data
- **Severity:** Major · **Category:** Security · **Classification:** Confirmed defect (missing controls) and reasonable concern
- **Location:** FR-16.05, PDF p.59 (47); API-01 and API-02, PDF p.159 (147); Fig. 28 step 2, PDF p.111 (99); Fig. 37, PDF p.120 (108); FR-14.01 and FR-14.04, PDF pp.55–56 (43–44); Table 120, PDF p.149 (137); Fig. 11 `PhraseProfile`, PDF p.94 (82).
- **What is wrong:**
  - (a) Administrators, who can see identity-document images and child photos, sign in with email and password only, with no second factor. **Mandatory.**
  - (b) `POST /v1/alerts/email` and `/v1/alerts/push` accept `recipients[]` and `phones[]` from the client, so any signed-in user could send alert emails or pushes to arbitrary addresses and numbers. Recipients should come from the server-side trustee list. **Mandatory.**
  - (c) Report rate limits are drawn as client-side checks in Figs. 28 and 37, while the rules in Table 118 do not enforce them. **Mandatory:** state server-side enforcement.
  - (d) Identity rests on a phone-number one-time code alone. SIM swap or a recycled number would give an attacker the victim's circles and live locations. **Optional:** a risk entry and mitigation.
  - (e) The safe and duress phrases, the SOS log with locations and the trustee list are stored unencrypted on the device and readable by anyone who obtains the unlocked phone. **Optional.**
  - (f) There are no abuse controls for invitations or user blocking. **Optional.**
- **Why it matters:** These are the most likely attacks on a safety application. Table 120 does not list them.
- **Recommended correction:** As marked per item above, and add rows to Table 120 for each.

## 2.4 Academic quality, scope and traceability

### AUD-M14 The survey sample size cannot be verified and conflicts across sources
- **Severity:** Major · **Category:** Academic integrity / Evidence · **Classification:** Confirmed source conflict; unverifiable claim · **Mandatory**
- **Location:** Section 2.5, PDF p.27 (15); Tables 7–8, PDF pp.27–28 (15–16); Table 10, PDF p.30 (18); Document Status, PDF p.206 (194).
- **What is wrong:** The SRS states "The survey received 73 responses … the distribution across all 73 responses was found to be nearly identical". The chat record (Exchange 24) records the user saying the survey had "109 responses, so we will kind of scale them", and the advice given then was to report n = 31. `project-context.md` says "n = 73 … raw 73 data lost". Only 31 responses are available. Recomputed from those 31 rows, every percentage in Tables 7 and 8 matches (for example 22/31 = 71%, 27/31 = 87%, 17/31 = 55%), so the figures are honest for n = 31. The claim about 73 cannot be substantiated, and the 109 figure contradicts it. The SRS also does not give the questionnaire, the sampling method or the respondent population (the form had no gender or age question), or say that three responses were self-contradictory.
- **Why it matters:** Reporting a larger sample than was analysed, with no raw data, is a common reason evaluation committees reject evidence.
- **Recommended correction:** Report the analysed sample as n = 31. Mention a larger total only if the raw export exists, and remove "nearly identical" unless it can be shown. Add the questionnaire and a short limitations note (convenience sample, no demographics, stated interest rather than adoption) as an appendix or in 2.5.

### AUD-M15 The unbuilt system is presented as implemented, and mockups contain realistic performance figures
- **Severity:** Major · **Category:** Academic integrity / Template · **Classification:** Confirmed defect · **Mandatory**
- **Location:** Section 5.4 "Implemented User Interface", PDF p.159 (147); Figs. 60–68, PDF pp.160–167 (148–155); Fig. 67, PDF p.167 (155); Section 6.8 Conclusion, PDF p.187 (175); Document Status, PDF p.206 (194).
- **What is wrong:** Section 5.4 is titled "Implemented User Interface" and its captions read "Mobile application: …". The admin overview mockup shows "Registered users 1,240", "SOS delivery, 7 days 98.4%" and "SMS 99% / Push 97% / Email 95%". Section 6.8 says the six objectives "are realized by the following modules". The only statement that nothing is implemented is the Document Status page after the last appendix.
- **Why it matters:** A reader who does not reach page 206 will take these as implementation evidence and measured delivery rates. The template's Section 5.4 requires implemented screens, which cannot exist at this stage.
- **Recommended correction:** Move a short status statement to the front matter and to the start of Chapters 5 and 6. Retitle 5.4 or mark it "design renderings, not yet implemented". Label the mockups as illustrative and replace realistic metrics with placeholders. Change "are realized" to "are designed to be realized".

### AUD-M16 Project objectives BO-1 to BO-6 and the approved evaluation plan are missing from the SRS
- **Severity:** Major · **Category:** Traceability / Academic quality · **Classification:** Confirmed defect · **Mandatory**
- **Location:** Section 6.8, PDF p.187 (175) (the only mention of BO-1 to BO-6); Chapter 1, PDF pp.13–20 (1–8); compare scope document §3 (objectives) and §9 (evaluation method).
- **What is wrong:**
  - BO-1 to BO-6 are cited but never defined in the SRS, and Chapter 1 has no problem statement or objectives.
  - The approved proposal commits to three evaluations:
    - detection precision and recall: covered by NFR-SAF-02;
    - semantic search compared against a keyword baseline: no requirement or test (IT-13 "returns relevant items" is not measurable);
    - a pilot study with 15–20 participants: only NFR-USA-02, with at least 5 participants.
  - The proposal also commits to demonstrating delivery across all three tiers. The SRS measures only the hand-off to the device's SMS service (NFR-REL-01), not delivery, and not Tiers 2 and 3.
- **Why it matters:** The proposal names "design and evaluation" as the engineering contribution, but the SRS drops two of the three evaluations and does not state the objectives it claims to meet.
- **Recommended correction:** Add a problem statement and objectives (BO-1 to BO-6) to Chapter 1, or reference them explicitly. Add measurable requirements and tests for the retrieval-quality comparison, the pilot study and delivery success per tier.

### AUD-M17 The scope exceeds the approved brief, and approval of modules MOD-17 to MOD-21 is not documented
- **Severity:** Major · **Category:** Scope / Source conflict · **Classification:** Reasonable concern (approval status unknown) · **Mandatory to resolve**
- **Location:** Table 1 and Table 2, PDF pp.14–16 (2–4); Section 1.5, PDF p.20 (8); Table 9, PDF p.29 (17).
- **What is wrong:** The Feature Document marks 7.17 to 7.19 as "sub-modules to be confirmed", and the chat record (Exchange 25) lists directions to the nearest safe area and app disguise as "candidates … not decided". The scope document has 16 modules and calls the post-incident module "a directory, not an automated dispatch mechanism". The SRS commits to 21 modules. `project-context.md` records that the user decided to add them, but no source shows supervisor or committee approval, and `progress.md` lists the MOD-20 and MOD-21 names as unconfirmed.
- **Why it matters:** Committing unapproved scope in a formal SRS invites the question of whether the approved project changed. It also adds load to an already large plan (see AUD-O21).
- **Recommended correction:** Record the approval in the Review History table, or mark MOD-17 to MOD-21 (or at least MOD-20 and MOD-21) as provisional or stretch modules until approval is given.

### AUD-M18 Fifty-five "shall" statements outside Chapter 3.2 are never traced or tested
- **Severity:** Major · **Category:** Traceability · **Classification:** Confirmed defect · **Mandatory**
- **Location:** OE-1 to OE-4, PDF p.24 (12); CON-1 to CON-12, PDF pp.25–26 (13–14); UI-1 to UI-10, SI-1 to SI-14, HI-1 to HI-8 and CI-1 to CI-7, PDF pp.80–83 (68–71); RTM, PDF pp.179–187 (167–175).
- **What is wrong:** None of these 55 identifiers appears in the RTM or in any test case. Most CON identifiers are never referenced again (an automated ID cross-check found CON-1 to CON-3, CON-5, CON-6, CON-8 to CON-10 and CON-12 mentioned only where they are defined).
- **Why it matters:** The template requires that "no mandatory requirement should remain without design and test evidence".
- **Recommended correction:** Add these requirements to the RTM with at least an inspection or test method, or reword the ones that are not verifiable requirements as notes.

---

# 3. Moderate findings

### AUD-O01 The SRS says evidence recording can be switched off, but no switch exists
- **Moderate · Requirements consistency · Confirmed defect · Mandatory**
- **Location:** RSK-16, PDF p.151 (139); BR-23, PDF p.76 (64); FR-18.01, PDF p.62 (50); FR-15.02, PDF p.57 (45); Fig. 59, PDF p.146 (134).
- **Problem:** RSK-16 says "evidence can be switched off in the settings". BR-23 says recording starts on every SOS, FR-15.02 lists only three toggles, and the settings mockup has no evidence switch. RSK-16 also rates the impact of the visible microphone indicator as Low, although it can reveal a silent SOS to a coercer.
- **Correction:** Either add an FR and a toggle for evidence recording, or remove the claim from RSK-16. Raise the impact rating.

### AUD-O02 Consent rules are undefined for circles with more than two members
- **Moderate · Requirements ambiguity · Confirmed defect · Mandatory**
- **Location:** FR-04.01 "Sharing between the two people", PDF p.41 (29); BR-10, PDF p.75 (63); Fig. 12 (Circle has 2..* Memberships), PDF p.95 (83); Fig. 23 note, PDF p.106 (94).
- **Problem:** It is not stated whether accepting an invitation means consenting to share with every existing member, or whether existing members consent to a newcomer seeing them. "Bilateral" is defined only for pairs.
- **Correction:** Define consent per member pair or per circle, and state what a new member can see on joining.

### AUD-O03 The delivery and retry algorithm contradicts the channel rules; delivery confirmation, duplicates and expiry are undefined
- **Moderate · Algorithm / Reliability · Confirmed defect · Mandatory**
- **Location:** A4, PDF p.155 (143); FR-01.02 and FR-12.03, PDF pp.34, 53–54 (22, 41–42); BR-04 and BR-05, PDF p.75 (63); UT-07, PDF p.171 (159); Fig. 32, PDF p.115 (103); FR-08.04, PDF p.48 (36).
- **Problem:**
  - A4 line 4 sends SMS to every trustee "always", whatever the trustee's channel preference, contrary to FR-01.02 and BR-04.
  - `nearHelp` is queued inside the per-trustee loop, so it is queued once per trustee.
  - WhatsApp is offered at Tier 1, when there is no data.
  - The mode `m` is used but is not an input.
  - The first retry delay is min(2 × B0) = 30 s, while UT-07 and Fig. 32 expect 15 s, and `delay` is never doubled per item.
  - "Delivered" is undefined per channel: FCM accepting a message, the SMS service accepting it, and a provider accepting an email are not delivery confirmations.
  - There is no duplicate suppression, maximum retry count or message expiry, so a queued SOS or help request can be sent hours later (FR-08.04, FR-12.03).
- **Correction:** Fix A4. Define a delivery status for each channel, idempotency keys, and the maximum age of queued messages.

### AUD-O04 The sound-level gate passes the wrong audio to the classifier
- **Moderate · Algorithm · Confirmed defect · Mandatory**
- **Location:** A1, PDF p.154 (142); Table 123 (T_buf = 2 s, two 30 ms frames), PDF p.153 (141).
- **Problem:** The ring buffer holds the 2 s before the spike, and the burst is emitted after only two loud frames, so the classifier receives about 1.94 s of ambient audio and 60 ms of the event. The ring is then cleared, so a continuing scream produces repeated short bursts. The ambient level starts at 0, so the behaviour at start-up depends on the dB scale used.
- **Correction:** Capture a window centred on or following the onset (for example continue buffering for T_buf after the spike), add a refractory period, and define the initial ambient value and the dB reference.

### AUD-O05 No targets for false countdowns or keyword false accepts and rejects
- **Moderate · NFR completeness · Confirmed gap · Recommended**
- **Location:** NFR-SAF-02 and NFR-PER-03, PDF pp.78–80 (66–68); RSK-01 and RSK-02, PDF p.150 (138).
- **Problem:** Precision and recall on a 100-clip test set do not measure how often the countdown starts in daily life. The voice engine has a latency target but no false-accept or false-reject rate.
- **Correction:** Add, for example, false countdowns per hour of real ambient audio in the soak test, and keyword-spotting false-accept and false-reject rates for enrolled speakers.

### AUD-O06 The onboarding flow contradicts the trustee and consent rules
- **Moderate · Diagram / Requirements consistency · Confirmed defect · Mandatory**
- **Location:** Fig. 35, PDF p.118 (106); FR-01.05 "Onboarding cannot finish without one trustee", PDF p.36 (24); BR-09, PDF p.75 (63); UC-06 preconditions, PDF p.193 (181).
- **Problem:** Declining consent goes straight to Home with no trustee added. Phrase enrolment is mandatory on the accept path even if voice activation is not wanted. Consent is one all-or-nothing decision, whereas BR-09 gives separate per-feature consent.
- **Correction:** Align Fig. 35, FR-01.05, BR-09 and UC-06.

### AUD-O07 Children as direct users are not addressed
- **Moderate · Stakeholders / Privacy · Reasonable concern · Recommended**
- **Location:** Section 2.2, PDF p.23 (11); glossary "Primary User", PDF p.18 (6).
- **Problem:** The product is "for women and children", but no user class, minimum age, guardian consent or handling of a minor's location in circles is defined. Children appear only as the subject of a missing-child report.
- **Correction:** State whether minors may hold accounts. If they may, define age limits, guardian consent and the special rules that apply. If they may not, say that children are protected through guardians' accounts.

### AUD-O08 The shared trigger engine, a claimed novel contribution, is modelled inconsistently
- **Moderate · Design consistency · Confirmed defect · Mandatory**
- **Location:** Fig. 10, PDF p.93 (81); Fig. 18, PDF p.101 (89); Fig. 19, PDF p.102 (90); A3, PDF pp.154–155; Table 114, PDF pp.86–87 (74–75).
- **Problem:** In Fig. 10 the countdown expires into TriggerEngine, which starts SosOrchestrator. In Fig. 18 the countdown starts the "SOS Controller" directly and TriggerEngine does not appear. In Fig. 19 TriggerEngine starts the countdown. The same component is called SosOrchestrator (class diagrams), SOS Controller (sequence diagrams) and sos_core (packages).
- **Correction:** Use one flow and one set of names in all models.

### AUD-O09 The data model is missing entities and attributes that the requirements use
- **Moderate · Data design · Confirmed defect · Mandatory**
- **Location:** Table 117 and Figs. 50–53, PDF pp.134–139 (122–127); Table 118, PDF p.140 (128).
- **Problem:** The data model has none of the following:
  - helper location;
  - the exact location in a help request (it holds only a geohash) that is revealed on accept;
  - the guardian contact and a last-seen geohash in the missing-child report, although Table 118 indexes the latter;
  - coordinates in incident reports, which BR-15's "within 100 m" duplicate check needs;
  - a server-side alert or token entity;
  - messaging tokens;
  - the phrase profile and the location cache.
  
  The server-side Acknowledgement references the device-only SosEvent.
- **Correction:** Add the missing entities and attributes, or change the requirements that rely on them.

### AUD-O10 There is no mechanism for sending invitation SMS to people without an account
- **Moderate · Architecture gap · Confirmed defect · Mandatory**
- **Location:** Fig. 23 step 4, PDF p.106 (94); UC-07 E1, PDF p.193 (181).
- **Problem:** "SMS if there is no account" needs either a server-side SMS provider, which is not in the architecture, dependencies or Table 134, or an SMS sent from the inviter's phone, which is not specified. The diagram also sends the message to the "Invitee application", which a person without an account does not have.
- **Correction:** Specify the mechanism, or use a share link instead.

### AUD-O11 Overloading the safe phrase creates disclosure and context risks, and one branch is missing
- **Moderate · Design / Safety · Confirmed gap and subjective concern · Mandatory (missing branch); optional (renaming)**
- **Location:** FR-03.05 and FR-05.02, PDF pp.40–42 (28–30); Fig. 33, PDF p.116 (104); glossary "Safe Phrase", PDF p.18 (6).
- **Problem:** Opting out means saying the loud-SOS phrase aloud, which teaches it to anyone nearby. Saying it outside the stop-sharing screen starts an SOS countdown. Fig. 33 has no branch for the duress phrase when the stop-sharing screen is open. The name "safe phrase" for a phrase that fires an SOS is also counter-intuitive.
- **Correction:** Add the missing branch. Consider a separate opt-out phrase or a non-voice opt-out, and consider renaming the phrases (for example "SOS phrase" and "duress phrase").

### AUD-O12 A single tap on the lock-screen action dispatches an SOS with no safeguard
- **Moderate · Safety / Usability · Confirmed defect (with AUD-M06) · Mandatory**
- **Location:** FR-01.01, PDF p.34 (22); NFR-USA-01, PDF p.79 (67).
- **Problem:** The home-screen control needs a 1 s hold, but the lock-screen action dispatches on one tap with no hold and no countdown. That invites pocket activation, and there is no way to retract it (AUD-M06).
- **Correction:** Require a hold or double action from the lock screen, or a short cancellable delay, and add retraction.

### AUD-O13 Evidence recording has no maximum duration, and microphone sharing between features is unspecified
- **Moderate · Requirements completeness · Confirmed gap · Mandatory**
- **Location:** FR-18.01 and FR-18.04, PDF pp.62–63 (50–51); Fig. 48, PDF p.131 (119); HI-1, PDF p.82 (70).
- **Problem:** Recording continues until the user stops it, the SOS ends (an action not defined, see AUD-M06) or storage fills. When the voice or detection engine holds the microphone, FR-18.01 says recording is skipped ("microphone is in use"), which could happen on the voice-trigger path itself. Fig. 48 shows "encryption finished" after a stream that was already being encrypted while it was written.
- **Correction:** Define a maximum duration and segmenting, the hand-over of the microphone from the spotter to the recorder, and one encryption model. **Optional:** record an integrity hash for exported files.

### AUD-O14 Heatmap abuse prevention is weak
- **Moderate · Security / Data quality · Reasonable concern · Recommended**
- **Location:** FR-07.01 and FR-07.05, PDF pp.45–47 (33–35); BR-15 and BR-17, PDF p.76 (64).
- **Problem:**
  - The report location can be dragged anywhere, so reports need not come from the reporter's own location.
  - Limits apply per account only, so several accounts can be used to flood an area.
  - The limit checks are drawn on the client side.
  - There is no function for users to flag a report.
  - The 280-character free-text note can carry names or defamatory content, but it is reviewed only when a burst of reports triggers moderation.
- **Correction:** Add server-side checks, a maximum distance between the device and the reported location, a user flagging function, and moderation of free-text notes.

### AUD-O15 RTM design and test mappings are inaccurate or generic
- **Moderate · Traceability · Confirmed defect · Mandatory**
- **Location:** RTM, PDF pp.179–187 (167–175).
- **Problem:**
  - FR-01.04 (silent mode) is traced only to FT-01, which tests loud mode.
  - FR-14.02 is traced to FT-19, which does not test token expiry or an offline SOS.
  - FR-03.x and FR-15.x point to "Class diagram detection", but those classes are in Fig. 11.
  - FR-18.x point to "Class diagram SOS core", but EvidenceRecording is in Fig. 9.
  - BR-23 (evidence) points to "auth; SD-03" instead of evidence_vault and SD-04.
  - BR-09 points to detection_engine.
  - All NFR rows use generic design elements ("Algorithms A1 to A10; architecture").
  - The Status column is empty in every row.
- **Correction:** Correct the mappings, add tests that actually exercise each acceptance criterion, and fill the Status column with "Planned".

### AUD-O16 Diagram logic and notation defects
- **Moderate · Diagrams · Confirmed defects · Mandatory for items that contradict text; optional for notation-only items**

| Figure (PDF p./printed p.) | Defect |
|---|---|
| Fig. 2 (69/57) | Primary User's bus line associates them with UC-29 Acknowledge SOS Alert; Verified Helper not linked to UC-01 although the UC-01 specification lists it |
| Fig. 4 (70/58) | Guardian not shown as a specialisation of Primary User; UC-23 actors Trustee and Administrator missing |
| Fig. 12 (95/83) | Circle–Membership multiplicity 2..* conflicts with creating a circle before anyone accepts |
| Fig. 15 (98/86) | AuthService models only phone codes; administrators use email and password |
| Fig. 17 (100/88) | `alt` with one operand (should be `opt`); WhatsApp and Near Help omitted |
| Fig. 21 (104/92) | Second `alt` not nested in the [timer expires] operand |
| Fig. 22 (105/93) | `alt` drawn after the `loop` instead of inside it |
| Fig. 25 (108/96), Fig. 36 (119/107) | 72-hour expiry drawn as a Guardian action instead of a timer event |
| Fig. 26 (109/97) | `alt` guard uses a similarity value computed inside the operand |
| Fig. 30 (113/101) | "Hold SOS 1 s" after "Trigger received"; join waits for actions that never finish (siren, recording); activity-final node used as a continuation |
| Fig. 32 (115/103) | No path for SMS failure at Tier 1 |
| Fig. 33 (116/104) | No branch for the duress phrase when the stop-sharing screen is open |
| Fig. 37 (120/108) | Scheduled function's "no" branch flows into a user action |
| Fig. 39 (122/110) | Helper decline "Close the request" (should dismiss only for that helper) |
| Fig. 40 (123/111) | Idle state belongs to the device, not the SOS event; no failure states; no second trigger; no user end during Active, Dispatching or Awaiting |
| Fig. 42 (125/113) | Expired goes to final, so the controller never returns to Idle; no manual trigger during the countdown |
| Fig. 43 (126/114) | "Stopped" drawn outside the "Member of the circle" composite; Sharing box overflows the composite; no Sharing → Left circle transition |
| Fig. 46 (129/117) | No self-withdrawal by a helper |
| Fig. 47 (130/118) | Entry actions ("send SMS only") describe policy, not actions on entering the state |
| Fig. 48 (131/119) | Streaming encryption versus "encryption finished"; no failure path |

### AUD-O17 Citation and evidence quality is weak
- **Moderate · Academic quality · Confirmed defect · Mandatory**
- **Location:** References, PDF p.189 (177); ADR-04, ADR-06 and ADR-10, PDF p.89 (77); Table 134, PDF p.157 (145); Section 2.1, PDF p.21 (9); Section 2.5, PDF p.27 (15).
- **Problem:**
  - Reference [6] (Sainath and Parada, 2015) is cited for "the sherpa-onnx keyword spotter", but the paper does not describe that tool.
  - These claims have no source: Google Maps terms forbid storing tiles (ADR-10); the WhatsApp Business API needs paid templates (ADR-06); the Android capability claims (CON-1, limitations); the emergency numbers 15, 1122 and 1099.
  - Section 2.5 lists a "review of existing safety applications", but no application is named or cited. The proposal's related-work table (bSafe, Noonlight, Life360, SafeCity) is gone.
  - There are only seven references in total.
- **Correction:** Cite the actual tool documentation, the platform documentation and official sources for the numbers, and restore a short related-work comparison.

### AUD-O18 The novel contribution is not stated or distinguished from standard features
- **Moderate · Academic quality · Confirmed gap · Recommended**
- **Location:** Whole document; the only mention is the BR-01 rationale "Novel contribution: one shared trigger engine", PDF p.74 (62).
- **Problem:** The Feature Document lists six specific contributions and says not to claim first-of-its-kind. The SRS states none of them, so an evaluator cannot tell standard features (SOS button, directory, library) from the claimed contribution (duress-aware consent, shared trigger engine, two phrases, offline follow-through).
- **Correction:** Add a short contribution statement in Section 1.2 or 2.1, worded as a combination and design contribution, not as novelty of individual features.

### AUD-O19 The reference device is undefined, and test methods are appended mechanically
- **Moderate · Verifiability · Confirmed defect · Mandatory**
- **Location:** Chapter 6 introduction, PDF p.170 (158); Table 141, PDF pp.176–178 (164–166).
- **Problem:** The NFR timing and battery targets depend on a "mid-range Android phone running Android 8.0 or later", with the model to be recorded later. "(reference device)" is appended to every NF method, including security-rule unit tests, documentation review and a load test of 100 concurrent users.
- **Correction:** Name the reference device or its minimum specification and Android version before testing. Give each NF test a realistic environment.

### AUD-O20 Legal and regulatory review is not identified
- **Moderate · Constraints · Reasonable concern · Recommended (no legal claim is made here)**
- **Location:** Section 2.4, PDF pp.25–27 (13–15); Appendix C, PDF p.203 (191).
- **Problem:** The SRS makes no legal claims, which is appropriate, but it records no assumption or TBD item for checking the law on recording third parties' audio, processing children's data, handling identity documents, messaging emergency services, or data protection in Pakistan.
- **Correction:** Add an assumption or dependency and a TBD item for legal review. Do not make compliance claims without a source.

### AUD-O21 The full scope may not be feasible for two developers, and the milestone plan gives no effort estimates
- **Moderate · Feasibility · Reasonable concern · Optional**
- **Location:** Table 2, PDF pp.15–16 (3–4); Table 122, PDF p.151 (139); RSK-13, PDF p.150 (138).
- **Problem:** The scope is 21 modules, 87 FRs, 42 NFRs, 141 test cases, an admin web application, a hosted alert page, two map stacks (Google Maps online, MapLibre/OSM offline), three on-device models and Cloud Functions. The milestone plan has dependencies but no durations or effort figures, so feasibility cannot be judged. RSK-13 does acknowledge the risk.
- **Correction:** Add effort estimates per milestone, and mark which modules are the minimum viable scope and which are stretch goals.

### AUD-O22 The free-tier constraint may conflict with Firebase Cloud Functions billing
- **Moderate · Constraints / Feasibility · Reasonable concern (verify current Firebase pricing) · Mandatory to verify**
- **Location:** CON-8, PDF p.25 (13); ADR-02, PDF p.89 (77); NFR-SCL-01, PDF p.80 (68); RSK-11, PDF p.150 (138).
- **Problem:** Email dispatch, acknowledgements and scheduled jobs all depend on Cloud Functions. To this audit's knowledge, deploying Cloud Functions requires the pay-as-you-go plan with a billing account, even if usage stays within the free quota. The email provider is also still TBD (TBD-2).
- **Correction:** Verify, then either state that a billing account is needed (with usage kept within free quotas) or change CON-8.

---

# 4. Minor findings

| ID | Category | Location (PDF p./printed p.) | Problem | Correction | Mandatory? |
|---|---|---|---|---|---|
| AUD-N01 | Template | Revision and review history, p.2 | Both tables are empty. The template says to "record every submitted revision" and scope-evaluation comments | Add the v1.0 row and any scope-evaluation comments with actions | Mandatory |
| AUD-N02 | Template / Typography | Whole PDF (pdffonts) | The PDF embeds Liberation Serif, Liberation Sans and DejaVu, not Times New Roman, because the export machine substituted fonts. The `.docx` specifies Times New Roman | Export from a machine with Times New Roman installed, or embed it | Mandatory if the PDF is submitted |
| AUD-N03 | Layout | TOC, p.3 | Entries 3.2.10 to 3.2.22 have no space between number and title ("3.2.10MOD-10") | Widen the TOC level-3 tab stop | Mandatory |
| AUD-N04 | Layout | Table 135 p.159 ("POS T", "Authent ication", "API-0 1"); Table 121 pp.150–151 ("Probabil ity", "Mediu m"); Table 122 p.151 ("Schedule d"); Table 117 p.134 ("Acknowledgeme nt"); Table 145 pp.190–191 ("MOD-0 1"); RTM pp.179–187 ("Requirem ent", "Statu s"); Table 113 p.83 ("Interfa ce") | Columns too narrow, so words break mid-word | Widen the columns or abbreviate the headers | Mandatory |
| AUD-N05 | Diagram legibility | Fig. 20 p.103 (the guard "[no phrase within 15 s]" overprints message 10 and is illegible); Figs. 18, 19, 21, 24, 25, 29 (labels overlap guards or dividers); Fig. 8 ("holds0..*", "1..10" overlapping lines) | Overlapping text | Move the labels | Mandatory for Fig. 20; optional for the others |
| AUD-N06 | Diagram legibility | Figs. 2–5 (p.69–70), 6 (p.86), 7 (p.88), 28 (p.111), 49 (p.132): smallest text about 5.0–5.4 pt; Figs. 36–39, 43, 54 about 5.8–5.9 pt (estimated from PDF text boxes, box height ÷ 1.11) | Below a common 6 pt print minimum. The figures are vector, so they are readable on screen | Enlarge the figures or split them | Optional |
| AUD-N07 | Mockups | Fig. 55 p.142 (status bar "T2" but strip says "Tier 3"); Fig. 58 p.145 (two "0" keys); Fig. 60 p.160 ("your trust / ees", line starting ", library", bottom line clipped "o audio …") | Inconsistent or broken mockup text | Fix the mockups | Mandatory for the clipped text |
| AUD-N08 | Consistency with sources | Cover p.1; Section 1.5 p.20 | The approved proposal and brief are titled "Hifazat", but the SRS never mentions the former name | Add one sentence in 1.1 or 1.5: "formerly titled Hifazat" | Mandatory |
| AUD-N09 | Glossary | Section 1.4, pp.17–19 | OTP is defined as "One-Time Code" (standard: One-Time Password). Missing terms: Drift, Riverpod, MapLibre, OpenStreetMap, MiniLM, sherpa-onnx, ONNX, PK/FK, ER, dp/sp, Material Design, Haversine, REST, JSON, DAO | Add the terms and correct OTP | Mandatory |
| AUD-N10 | Data design | Table 117, p.134 | Not strictly alphabetical (Acknowledgement listed before Account). The template asks for methods and parameters in an OO data dictionary | Reorder; optionally add operations | Mandatory (order) |
| AUD-N11 | Source attribution | FR-20.01 to FR-20.03 pp.66–67 ("Interview and survey; interview …"); FR-21.x pp.67–68 and RTM p.183 (an interview listed as the source, although the source is one survey comment); Section 2.5 p.28 ("a medical (MBBS) student", whereas the chat record says "MBBS Student(x2)") | Duplicated or inaccurate sources | Correct the sources; say "an interview with two MBBS students" | Mandatory |
| AUD-N12 | Use cases | UC-01 p.71 | The precondition "SMS permission is granted" contradicts exception E1 (permission missing). The timer starts at step 4, before dispatch, whereas FR-19.02 starts it "when dispatched" | Align them | Mandatory |
| AUD-N13 | Accuracy | Limitations p.188; RSK-16 p.151 | Microphone indicator attributed to "Android 11 and later". To this audit's knowledge it arrived in Android 12 | Verify and correct | Mandatory after verification |
| AUD-N14 | Template (Ch. 5) | Section 5.5 pp.168–169; Table 134 pp.157–158; Table 135 p.159 | 5.5 does not cover secrets or environment-variable handling (for example Maps and email API keys) or rollback, both listed in the template. Library versions are vague ("current stable", "2.x"). The REST table does not reference implementation components as the template asks | Add these items | Mandatory |
| AUD-N15 | Testability | FR-15.03 p.57; NFR-PRV-03 p.79; IT-13 p.176; FR-10.03 p.51 | Acceptance criteria such as "summary matches the behaviour", "returns relevant items" and "item whose meaning matches" are not objectively testable | Give a checklist or a labelled relevance set | Mandatory |
| AUD-N16 | Ambiguity | FR-14.03 p.55 (rationale "short enough for one SMS", although the message also carries name, coordinates, link and time); FR-07.04 p.46, A7 and UI-8 (colour thresholds undefined); FR-12.01 p.53 ("slow"/"fast" defined only in Table 123 and Fig. 47) | Imprecise wording | Define the values or reference Table 123 | Optional |
| AUD-N17 | Consistency | Table 5 p.24 ("TensorFlow Lite runtime" for all models) versus ADR-04 and Table 134 (sherpa-onnx uses an ONNX runtime); Table 134 FCM "topic by geohash" versus the Firestore geohash query in Fig. 24 | Runtime and messaging mechanisms inconsistent | Align them | Mandatory |
| AUD-N18 | Use-case model | Section 3.2.22 p.68; Fig. 2 p.69 | UC-02 and UC-03 «include» "Trigger Manual SOS". Reuse of the dispatch steps would be better modelled by extracting a "Dispatch SOS" use case | Extract a shared use case | Optional |
| AUD-N19 | Template (4.3) | Fig. 49 p.132 | The component diagram shows package groups with no provided or required interfaces, which the template's model table asks for | Add the interfaces | Optional |
| AUD-N20 | Interfaces | Table 113 p.83 | The summary table omits SI-7, SI-10 to SI-14, HI-4, HI-5, HI-7, HI-8, CI-1, CI-2 and CI-4 to CI-6 | Complete it or call it a selection | Optional |

---

# 5. Observations

| ID | Observation |
|---|---|
| AUD-X01 | The chapter overviews and summaries are numbered as sections (1.6, 2.6, 3.6, 4.8, 5.6, 6.9). The template treats them as unnumbered parts of each chapter. Acceptable, but it adds headings that are not in the template. |
| AUD-X02 | Captions are numbered sequentially ("Figure 1", "Table 1"), while the template's example uses chapter-based numbering ("Fig. 4.1", "Table 6.2"). The template's wording is "for example", so this is not a defect. |
| AUD-X03 | Template Appendix D (Diagram Notation Reference) says "Include only notation relevant to diagrams used in the project. Insert the appropriate standard symbol". The SRS has no notation appendix. It is unclear whether this is a required deliverable or an example; confirm with the supervisor. |
| AUD-X04 | There is duplication and page inflation. Table 99 repeats Table 145. Business rules restate FR text (for example BR-16 equals FR-07.03). About 40 diagram pages are half empty, and PDF pp.152 and 205 carry only a few lines. Tightening the layout could reduce the length noticeably without losing content. |
| AUD-X05 | The PDF has 206 pages, not the 207 stated in the audit brief. `Documents/Archive/Muhaffiz-SRS-SDS-old-186p.pdf` is an older 186-page build (22 Oct 23:56); make sure the correct file is submitted. |
| AUD-X06 | The source for MOD-21 ("one survey respondent suggested … changing its icon and name") cannot be verified from the available materials: the open-ended survey answers are not in the chat record. |
| AUD-X07 | **Strengths verified by this audit:** identifiers are unique and consistent, and an automated check found no references to undefined IDs. All 87 FRs use the full template attribute set with acceptance criteria. Survey percentages match the 31 analysed responses exactly. Cross-references are real fields (165 REF fields, 0 hand-typed references found) and captions use SEQ fields. Body text matches the template (Times New Roman 12 pt, justified, 1.5 spacing, 18 pt after, 1.27 cm first-line indent, 2.54 cm margins). Every chapter starts on a new page with an overview and a summary. Limitations are stated candidly (WhatsApp needs confirmation, the microphone indicator, coercion, the limits of escalation). No template placeholder or example text remains. The out-of-scope list correctly excludes direct integration with authorities. |

---

# 6. Distinction between confirmed defects, concerns and recommendations

- **Confirmed defects** (demonstrable from the documents): AUD-C01, C02; M01–M07, M09 (inconsistency), M10, M13–M16, M18, M19 (a–c); O01–O04, O06, O08–O10, O12, O13, O15–O17, O19; all Minor findings except N13 (which needs verification).
- **Reasonable concerns** (depend on facts outside the documents): AUD-M08 (risk part), M09 (abuse risk), M11, M12, M17, M19 (d–f); O05, O07, O14, O20, O21, O22; N13.
- **Subjective recommendations** (may be declined): the design alternatives in M08 and M09, the configurable decoy code in M10, phrase renaming in O11, splitting the scope in O21, and AUD-N18, N19, X01–X04.
