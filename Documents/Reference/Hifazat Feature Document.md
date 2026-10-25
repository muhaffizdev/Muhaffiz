# Hifazat: Feature Document

## Modules

### Core Safety & Emergency Response

#### 7.1 SOS Alert System

- 7.1.1 Manual SOS button on the home screen and a lock-screen quick action, sized for one-handed use under stress.
- 7.1.2 Multi-channel dispatch: live GPS and a preset message sent at once by WhatsApp, in-app push (Firebase Cloud Messaging), email and SMS. SMS works with no data.
- 7.1.3 Loud alarm: a high-volume siren to attract attention.
- 7.1.4 Silent mode: no sound and no visible alerting, while dispatch continues in the background.
- 7.1.5 Trustee management: add, edit and remove contacts, with a channel preference for each.
- 7.1.6 SOS event log: time, location, trigger method (manual, automatic, voice) and delivery status per channel.

#### 7.2 Automatic Danger Detection Engine

- 7.2.1 Ambient monitoring as a low-power foreground service that stays dormant until a sudden loud sound.
- 7.2.2 On-device sound classifier (TensorFlow Lite) that labels a short burst as distress (screaming, shouting) or not, with no transcription and no stored audio.
- 7.2.3 Motion fusion: accelerometer and gyroscope signals (a sudden drop, struggle movement) are combined with the audio result to cut false alarms.
- 7.2.4 Confirmation countdown: 20 seconds of mild vibration with a one-tap cancel. If not cancelled, the SOS fires (7.1). If cancelled, nothing happens.
- 7.2.5 On-device guarantee: nothing produced by this module ever leaves the phone.

#### 7.3 Voice Activation & Safe-Phrase Engine

- 7.3.1 Safe-phrase enrollment for a normal (loud) SOS.
- 7.3.2 A second, different duress phrase that fires a silent SOS.
- 7.3.3 Offline keyword spotting (for example Picovoice Porcupine), with no network and no cloud transcription.
- 7.3.4 Voice-triggered SOS through the same dispatch and confirmation pipeline as automatic detection.
- 7.3.5 Shared hook so the same engine confirms the family-map opt-out (7.5) and supports Decoy Mode (7.6).

### Family Safety Network

#### 7.4 Family Circle Management

- 7.4.1 Circle creation and invitations that need both people to accept before any sharing starts.
- 7.4.2 Member list showing each person’s sharing status and last update time.
- 7.4.3 Leave a circle entirely, which is separate from pausing sharing.

#### 7.5 Location Sharing & Privacy Controls

- 7.5.1 Location updates on significant movement rather than constant GPS, to save battery.
- 7.5.2 Opt-out by spoken safe phrase (7.3), with no approval from anyone.
- 7.5.3 Private confirmation shown only to the person who opted out. Other members get no “opted out” message.
- 7.5.4 Last-known-location display: after someone stops sharing, others see only their last location with a timestamp, clearly marked as not live.
- 7.5.5 Real-time sharing status through Firestore listeners, so hidden or silent tracking is not possible.

#### 7.6 Decoy Mode

- 7.6.1 A neutral, unrelated-looking screen replaces the app if someone forces the user to unlock the phone.
- 7.6.2 A hidden gesture returns the real user to the actual app.
- 7.6.3 SOS, voice triggers and location updates keep working underneath the decoy screen.

### Community Safety Intelligence

#### 7.7 Danger Heatmap

- 7.7.1 Incident report form: location (auto-filled, editable), category (harassment, theft, felt unsafe) and an optional note.
- 7.7.2 Geohash grid that groups reports into fixed-size cells.
- 7.7.3 Recency weighting, so older reports count for less.
- 7.7.4 Map overlay (Google Maps) coloured from green to red by weighted density. Tapping a zone shows report categories and counts without identifying reporters.
- 7.7.5 Rate limits and abuse checks to stop spam or malicious flagging of an area.

#### 7.8 Near Help

- 7.8.1 Verified-helper registration with an identity check.
- 7.8.2 Help requests broadcast to verified users within a set radius.
- 7.8.3 Accept or decline screen for responders.
- 7.8.4 Clear “unavailable, no connection” state offline instead of failing silently.

### Safety Knowledge Library

#### 7.9 Content Library Management

- 7.9.1 Curated articles, videos and links on prevention and post-trauma care, by category.
- 7.9.2 Content bundled with the app so it works with no internet.
- 7.9.3 Browsing with category filters and bookmarks.

#### 7.10 Semantic Search Engine

- 7.10.1 Content embeddings computed ahead of time and shipped with the app.
- 7.10.2 The user’s query is converted to an embedding on the device with a compact sentence-embedding model.
- 7.10.3 Cosine-similarity ranking against the bundled embeddings, with no network call.
- 7.10.4 Keyword-search fallback when the model is unavailable or confidence is low.
- 7.10.5 Ranked result cards with a relevance indicator, plus open and bookmark actions.

### Post-Incident Support

#### 7.11 Emergency Services Directory

- 7.11.1 Localized directory of hospitals, helplines and emergency numbers, including Rescue 1122 and women’s helplines.
- 7.11.2 One-tap call from any entry.
- 7.11.3 Nearest facilities first when location is available.

### Offline Reliability & Sync

#### 7.12 Tiered Delivery System

- 7.12.1 Connectivity detection that sorts the phone into three tiers: no connection, any connection, good connection.
- 7.12.2 SMS delivery that works at Tier 1 with zero data.
- 7.12.3 Queue and retry: anything created offline is sent automatically over WhatsApp, email, push and Near Help when a connection returns.

#### 7.13 Offline Data Caching

- 7.13.1 Last-known-location cache, used if a fresh GPS fix is not available when SOS fires.
- 7.13.2 On-device database for library content, map tiles for frequent areas, and pending outbound alerts.

### Identity, Consent & Privacy

#### 7.14 Authentication & Account Management

- 7.14.1 Phone-number sign-up and login (Firebase Authentication).
- 7.14.2 Secure session handling with automatic re-authentication.
- 7.14.3 Profile and settings: name, emergency message template, linked trustees.
- 7.14.4 Account recovery for lost devices.

#### 7.15 Consent & Privacy Controls

- 7.15.1 Onboarding consent that says plainly what the detection and voice engines listen for and that processing stays on the device.
- 7.15.2 Separate toggles for microphone detection, location sharing and voice activation, changeable at any time.
- 7.15.3 In-app privacy summary: what is stored, what stays on the device, what reaches the backend.

### Admin & Platform Operations (Internal)

#### 7.16 Admin Dashboard

- 7.16.1 User overview: registrations and verification status.
- 7.16.2 Moderation queue for flagged heatmap reports.
- 7.16.3 Review queue for approving or revoking Near Help helpers.
- 7.16.4 Health monitoring: delivery success by channel and backend errors.

### New modules (sub-modules to be confirmed)

#### 7.17 Missing-Child Report

- 7.17.1 Report form: child’s name, age, photo, description, last-seen place and time, and the guardian’s contact.
- 7.17.2 Alert to the guardian’s trusted contacts and to verified users nearby.
- 7.17.3 Status handling: active, found, expired.
- 7.17.4 Hand-off to official channels such as the Zainab Alert helpline (1099, to be re-verified before use), as a call or share action, because no direct integration has been confirmed.
- 7.17.5 Moderation and abuse prevention: admin review of reports and handling of false reports.
- 7.17.6 Child-data privacy: limited photo visibility and removal when the child is found.

#### 7.18 Evidence Recording on SOS

- 7.18.1 Recording starts automatically when SOS fires, however it was triggered.
- 7.18.2 Encrypted on-device storage. Nothing is uploaded.
- 7.18.3 Evidence list with time, location and trigger details for each recording.
- 7.18.4 User controls: stop, delete, export, and automatic deletion after a set period.
- 7.18.5 Disclosure in the onboarding consent (7.15), stating that recording begins only after an SOS fires.

#### 7.19 Escalation to Authorities

- 7.19.1 Response tracking: acknowledgements from trustees and nearby helpers are detected.
- 7.19.2 No-response timer, with the duration still to be decided.
- 7.19.3 Warning countdown with a cancel option before escalation, to limit false alarms.
- 7.19.4 Authority channel settings: which numbers and channels are used (for example police 15 and Rescue 1122), sent as SMS, call or share.
- 7.19.5 Escalation message: location, time, trigger type and whether evidence exists.
- 7.19.6 Escalation log.

## Novel contributions

Six design choices set Hifazat apart. Individual pieces such as offline SMS SOS exist in other apps, so the novelty lies in this combination and in the consent and duress model, built for Pakistan.

1. **Duress-aware family sharing (7.4, 7.5).** Both people must agree to join. Anyone can leave alone and privately by speaking a safe phrase. Others never see an “opted out” notice, only a timestamped last location, and there is no hidden tracking mode.
2. **One shared trigger engine (7.1, 7.2, 7.3, 7.5, 7.6).** Manual SOS, automatic detection, voice phrases, the safe-phrase opt-out and decoy mode all run through one engine, so every duress-sensitive action behaves the same way.
3. **Two spoken phrases (7.3).** One phrase fires a loud SOS and a different one fires a silent SOS, both recognised offline on the phone.
4. **Cancel-or-send safeguard (7.2).** Detected distress starts 20 seconds of silent vibration. One tap cancels it, otherwise the SOS fires. Detection itself stores no audio.
5. **Intelligence that stays on the phone (7.2, 7.3, 7.10).** Danger-sound detection, voice recognition and the library’s semantic search all run on the device, and no audio is sent anywhere.
6. **An SOS that follows through (7.18, 7.19).** After an SOS the phone records audio kept only on the device as evidence, and if nobody responds the alert is escalated to the authorities.
