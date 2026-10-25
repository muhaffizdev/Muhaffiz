# Muhafiz: Project Context

(Formerly Hifazat. Name is Muhafiz / Muhaffiz; treat the older name as the same project.)

## Basics
- Final Year Project, BS Software Engineering (2023-2027), Air University, Islamabad.
- Team: Muhammad Shamoil (232025), Ali Raza (232047). No third member; remove the third-name line from the SRS template.
- Supervisor: Kanwal Batool. FYP Head (template): Dr. Farhad.
- Topic switched from ClipSeeker (semantic stock-media search). Supervisor has approved the new topic. Now writing the SRS & SDS.

## Product
Android-only safety app for women and children, aimed at Pakistan. Flutter (Dart), Firebase (Auth phone login, Firestore, FCM, Storage), TensorFlow Lite sound classifier, Picovoice Porcupine keyword spotting, Google Maps, on-device sentence-embedding model for library search.
Principles: offline-first (SMS at zero connectivity), on-device intelligence (no audio leaves the phone), duress-aware consent.
Engineering contribution = system design + evaluation, not training new models.

## Modules (all 19 are in scope; follow Hifazat Feature Document.md, it is the latest source)
7.1 SOS Alert; 7.2 Automatic Danger Detection; 7.3 Voice Activation & Safe-Phrase; 7.4 Family Circle; 7.5 Location Sharing & Privacy; 7.6 Decoy Mode; 7.7 Danger Heatmap; 7.8 Near Help; 7.9 Content Library; 7.10 Semantic Search; 7.11 Emergency Services Directory; 7.12 Tiered Delivery; 7.13 Offline Caching; 7.14 Authentication; 7.15 Consent & Privacy; 7.16 Admin Dashboard; 7.17 Missing-Child Report; 7.18 Evidence Recording on SOS; 7.19 Escalation to Authorities.
7.17-7.19 sub-modules are still "to be confirmed"; open items: no-response timer length, which authority channels are accepted, Zainab Alert 1099 to be re-verified.

## Key design rules (from the chat record)
- Family sharing: opt-in bilateral; opt-out unilateral via spoken safe phrase; private confirmation to the opter only; others see last-known location with timestamp marked not live; no hidden tracking.
- Auto-detection: volume-spike gate -> TFLite classify -> motion fusion -> 20 s mild vibration, one-tap cancel, else SOS fires. No transcript, no stored audio.
- Two phrases: loud SOS phrase and silent/duress SOS phrase. One shared trigger engine under SOS, detection, voice, opt-out and decoy.
- Evidence audio stays on-device, encrypted; recording starts only after SOS fires; disclosed in consent.
- Do NOT claim "first of its kind". Offline SMS SOS apps exist. Novelty = combination + consent/duress model, for Pakistan.

## Evidence (for SRS elicitation sections)
- Survey: cite n = 73. Percentages come from the first 31 responses analysed; the full 73 mirrored them (user's check; raw 73 data lost). Phrase it that way.
- 31-response figures: 87% worry often/almost always; 1 of 31 had used a dedicated safety app; 61% use WhatsApp live location; 29% use nothing; top barrier "needs internet" 71%; speed, trust, privacy, "don't know a good one" 39% each; 87% would use it, 58% for family; likely/very likely: decoy 87%, unsafe-areas map 84%, hospital list 84%, escalation 81%, audio evidence 77%, missing-child report 77%, SOS button 74%, secret phrase 58%, auto-detection 55%.
- Interviews (4 groups): high-school student (audio-only evidence ok, video would breach privacy); working woman (auto-detect appealing, would pay minimal fee); two MBBS students (decoy + alert, trust concerns about apps mishandling data, accept recording trade-off); male university student (would install for family, wants directions to nearest safe place, ideally offline).
- Candidate features from survey, NOT decided: one-tap directions to nearest safe area; app disguise (icon/name change).

## Known caveats
- Scope document is out of date and parked for now (16 modules only; 243-day vs 78-day Phase 3 arithmetic error; unverified bSafe/Noonlight "needs data" claim). Do not rely on it for numbers.
- Timeline: assume the existing two-semester plan unless told otherwise.

## Decisions made for the SRS (confirmed by user)
- Spelling: "Muhaffiz" (two f's) everywhere in the SRS.
- 7.19 no-response timer: 3 minutes, then 30 s warning countdown with cancel; SMS to configurable authority numbers (Police 15, Rescue 1122 default). Authority acceptance is an unverified external assumption.
- 7.17-7.19 sub-modules from the Feature Document are included. Candidate features (directions to nearest safe area, app disguise) are ADDED as modules too (user said "add them"); number them 7.20 and 7.21 and confirm sub-modules with the user before writing.
- 4.7 uses milestones, not real dates.
- Fill the SRS chapter by chapter. Build the actual .docx (no Markdown). Claude makes all diagrams and mockups. Ask, do not assume; document goes to the FYP board.
- Interviews: DECIDED to keep the 4 real interviews (cite four). Never invent more.
- Domains: promotion website muhaffiz.live; admin website muhaffiz.me (separate web app, not part of the Flutter app).
- Official title (confirmed): "Muhaffiz: Offline-First Safety for Women and Children".
- Voice activation must be fully offline: replace Porcupine (needs an online AccessKey check) with open-source on-device keyword spotting. Candidate: sherpa-onnx keyword spotter (Apache-2.0, Flutter plugin, open-vocabulary, phrase typed as text, no training or key). Alternatives: openWakeWord, Vosk grammar mode. Verify before Chapter 5.
- Other architecture picks (delegated to Claude): Riverpod, Drift/SQLite, YAMNet via TFLite, MiniLM-class embeddings, Google Maps SDK, Android SmsManager via platform channel, Cloud Functions for email, AES-256 evidence with Android Keystore.

## SRS work rules
- Template: Documents/Reference/SRS-Template.docx (SRS & SDS, 6 chapters + appendices). Filled chapter by chapter, only when the user gives a detailed prompt.
- Template formatting: Times New Roman; H1 16 pt bold, H2 14 pt bold, body 12 pt justified, 1.5 line spacing, 18 pt after paragraphs, 1.27 cm first-line indent, 2.54 cm margins, page numbers in footer, built-in heading styles, auto captions (figure below, table above), IEEE citations, every chapter starts on a new page with a Chapter Overview and ends with a Chapter Summary.
