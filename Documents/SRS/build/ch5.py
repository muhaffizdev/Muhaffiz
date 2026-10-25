from srslib import *
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams')
def F(name): return (os.path.join(OUT, name + '.svg'), os.path.join(OUT, name + '.png'))
def land_group(items):
    return [FIG(k, c, svg=F(k)[0], png=F(k)[1]) for k, c in items]
NB = ' '
def ind(n): return NB * (4 * n)

def algo(key, title, inp, out, lines, cx):
    rows = [['**Input:** ' + inp], ['**Output:** ' + out]]
    for i, (lv, t) in enumerate(lines, 1):
        rows.append(['%d:%s%s' % (i, NB * 3, ind(lv) + t)])
    rows.append(['**Complexity:** ' + cx])
    return TBL(key, 'Algorithm: ' + title, ['Algorithm: ' + title], rows, [1.0], fs=17)

def blocks(ctx):
    b = []
    b.append(H1('Implementation and Deployment', 'ch5'))
    b.append(P('**Chapter Overview.** This chapter describes how the design is realized. Section {sec:algorithms} gives the core algorithms with pseudocode, Section {sec:apis} lists the external APIs and SDKs, Section {sec:rest} specifies the interfaces of the project backend, Section {sec:implui} presents the user interface of each subsystem, and Section {sec:deploy} describes the deployment. Source code is not reproduced.'))

    # ------------------------------------------------------------ 5.1
    b.append(H2('Algorithms', 'algorithms'))
    b.append(P('The core behaviour of Muhaffiz is implemented by ten algorithms: the sound-level gate, the distress decision with fusion, the trigger and SOS pipeline, the tiered dispatch with retry, the phrase handling in context, the movement-based location publication, the heatmap cell score, the semantic search, the escalation timer, and the nearest safe location. Their constants are held in one configuration (NFR-MNT-02) and are listed in {tbl:params}; the values are the defaults that the evaluation of Chapter 6 may tune.'))
    params = [
     ['T_amb', 'Window for the rolling ambient sound level', '10 s', 'FR-02.01'],
     ['D_spike', 'Rise above the ambient level that counts as a sudden loud sound, for at least two consecutive 30 ms frames', '15 dB', 'FR-02.01'],
     ['T_buf', 'Length of the in-memory audio burst passed to the classifier', '2 s', 'FR-02.02'],
     ['θ_audio', 'Distress score at or above which the audio result counts as distress', '0.60', 'FR-02.03'],
     ['θ_high', 'Distress score at or above which the audio result alone satisfies the fusion rule', '0.85', 'FR-02.03'],
     ['W_motion', 'Motion window around the burst (2 s before to 3 s after)', '5 s', 'FR-02.03'],
     ['A_dev, G_rot', 'Motion anomaly: acceleration deviation from gravity, or rotation rate', '15 m/s²; 6 rad/s', 'FR-02.03'],
     ['T_count', 'Confirmation countdown', '20 s', 'FR-02.04, BR-02'],
     ['T_confirm', 'Time allowed for the safe phrase on the stop-sharing screen', '15 s', 'FR-05.02'],
     ['T_fix', 'Wait for a fresh location fix at SOS start', '10 s', 'FR-13.01, BR-06'],
     ['D_min', 'Movement that triggers a location publication', '50 m', 'FR-05.01'],
     ['T_probe, T_good', 'Backend probe timeout; round-trip time for Tier 3', '3 s; 1 s', 'FR-12.01'],
     ['B0, B_max', 'First retry delay and maximum delay (doubling)', '15 s; 15 min', 'FR-12.03'],
     ['P_geo, H', 'Geohash precision; report half-life', '7; 90 days', 'FR-07.02, FR-07.03'],
     ['τ_sim, K', 'Similarity threshold for semantic results; number of results', '0.30; 10', 'FR-10.04, FR-10.05'],
     ['T_ack, T_warn', 'No-response timer; warning countdown', '180 s; 30 s', 'FR-19.02, FR-19.03'],
     ['R_help, R_child', 'Helper radius; missing-child alert radius', '1 km; 5 km', 'FR-08.02, FR-17.02'],
    ]
    b.append(TBL('params', 'Algorithm parameters and default values', ['Parameter', 'Meaning', 'Default', 'Related'], params, [1.0, 4.0, 1.1, 1.3], fs=17))
    b.append(algo('alg1', 'sound-level gate (A1)', 'a stream of 30 ms audio frames', 'a burst of T_buf seconds when a sudden loud sound occurs, otherwise nothing', [
        (0, 'ambient ← 0; ring ← empty buffer of T_buf seconds; run ← 0'),
        (0, 'for each frame f from the microphone do:'),
        (1, 'level ← decibelLevel(f); push f into ring; discard the oldest frame'),
        (1, 'if level > ambient + D_spike then run ← run + 1 else run ← 0'),
        (1, 'if run ≥ 2 then'),
        (2, 'emit burst(copy of ring); run ← 0; clear ring'),
        (1, 'else if run = 0 then'),
        (2, 'ambient ← slidingMean(ambient, level, T_amb)'),
        (0, 'end for'),
        (0, 'all frames and the ring exist in memory only'),
    ], 'O(1) time per frame; O(T_buf) memory.'))
    b.append(algo('alg2', 'distress decision with fusion (A2)', 'a burst from A1; the motion window', 'a countdown request, or no action', [
        (0, 'score ← classifier.score(burst)          // distress probability, no transcript'),
        (0, 'discard burst'),
        (0, 'if score < θ_audio then return none'),
        (0, 'motion ← motionAnomaly(window W_motion, A_dev, G_rot)'),
        (0, 'if motionSensorsAvailable = false then ok ← (score ≥ θ_high)'),
        (0, 'else ok ← (motion = true) or (score ≥ θ_high)'),
        (0, 'if ok = false then return none'),
        (0, 'return countdown(T_count, trigger = automatic)'),
    ], 'O(1) per burst after the classifier inference, which is a fixed-size neural-network pass.'))
    b.append(algo('alg3', 'trigger arbitration and SOS pipeline (A3)', 'a trigger t (manual, automatic or voice) and a mode m', 'an SOS event with dispatch, evidence and timers started', [
        (0, 'if t = manual then goto start'),
        (0, 'show countdown for T_count (vibration if m = loud; none if m = silent)'),
        (0, 'if user cancels within T_count by an enabled method then return   // nothing is sent'),
        (0, 'start:'),
        (1, 'event ← new SosEvent(t, m, now)'),
        (1, 'location ← fix within T_fix, else cachedLocation with its age'),
        (1, 'in parallel do:'),
        (2, 'evidence.start(event)'),
        (2, 'escalation.start(event, T_ack)'),
        (2, 'if m = loud then playSiren() else stayQuiet()'),
        (2, 'delivery.dispatch(event, location)               // see A4'),
        (1, 'log(event)'),
    ], 'O(c) for c trustee-channel pairs.'))
    b.append(algo('alg4', 'tiered dispatch and queue retry (A4)', 'an event, a location and the trustee list', 'delivery statuses; undelivered messages queued', [
        (0, 'tier ← detectTier(T_probe, T_good)'),
        (0, 'for each trustee u do:'),
        (1, 'channels ← u.channels, or {sms} if empty'),
        (1, 'send SMS(u)                                      // always, uses no data'),
        (1, 'if tier ≥ 2 then'),
        (2, 'for each channel c in {push, email} ∩ channels do send(c, u)'),
        (1, 'else enqueue({push, email, nearHelp}, u)'),
        (1, 'if whatsapp ∈ channels and m = loud then offerWhatsapp(u)'),
        (0, 'on result r of any send: if r = failed then enqueue(message) else markSent(message)'),
        (0, 'on tier change to ≥ 2: delay ← B0; for each queued item q do try send(q);'),
        (1, 'if failed then reschedule(q, min(2 × delay, B_max)) else markDelivered(q)'),
    ], 'O(c) per dispatch; each retry round is O(q) for q queued items.'))
    b.append(algo('alg5', 'phrase handling in context (A5)', 'a phrase detection p ∈ {safe, duress} and the current context', 'an action', [
        (0, 'if context = countdown and p = safe and cancelBySpeech then'),
        (1, 'countdown.cancel(); return                          // nothing is sent'),
        (0, 'if context = stopSharingScreen and p = safe then'),
        (1, 'toggle.unlock(); return                             // sharing stops when the toggle is switched off'),
        (0, 'if p = safe then return trigger(voice, defaultMode)    // A3 with countdown'),
        (0, 'if p = duress then'),
        (1, 'decoy.show(); return trigger(voice, silent)'),
        (0, 'if context = stopSharingScreen and no phrase within T_confirm then closeScreen()'),
    ], 'O(1) per detection.'))
    b.append(algo('alg6', 'movement-based location publication (A6)', 'location updates and the member\'s sharing flag', 'published locations', [
        (0, 'last ← null'),
        (0, 'for each location update x do:'),
        (1, 'if sharing = false then continue'),
        (1, 'if last = null or distance(last, x) > D_min then'),
        (2, 'publish(x, now); last ← x'),
        (0, 'on stopSharing(): sharing ← false; freeze(last)      // others see last, "Not live"'),
    ], 'O(1) per update.'))
    b.append(algo('alg7', 'heatmap cell score (A7)', 'the reports R of a cell', 'the score of the cell and its category counts', [
        (0, 'score ← 0; counts ← empty map'),
        (0, 'for each report r in R do:'),
        (1, 'age ← now − r.createdAt (in days)'),
        (1, 'score ← score + 0.5 ^ (age / H)'),
        (1, 'counts[r.category] ← counts[r.category] + 1'),
        (0, 'return (score, counts)                               // colour = scale(score)'),
    ], 'O(n) per cell for n reports; run by a scheduled function per changed cell.'))
    b.append(algo('alg8', 'semantic search with keyword fallback (A8)', 'a query string q and the bundled embeddings E', 'a ranked list of at most K items', [
        (0, 'if embedder.available = false then return keywordSearch(q)'),
        (0, 'v ← embedder.embed(q)                               // on device, 384 values'),
        (0, 'for each item i do: sim[i] ← dot(v, E[i]) / (norm(v) × norm(E[i]))'),
        (0, 'sort items by sim descending; top ← first K items'),
        (0, 'if sim[top[0]] < τ_sim then return keywordSearch(q)'),
        (0, 'return top with relevance = sim'),
    ], 'O(N·d) for N items and d = 384; embedding the query is one model pass.'))
    b.append(algo('alg9', 'escalation timer (A9)', 'an SOS event and the authority numbers', 'an escalation message, a cancellation or an acknowledgement', [
        (0, 'wait up to T_ack for an acknowledgement'),
        (0, 'if acknowledgement received then stop; return'),
        (0, 'show warning for T_warn with one-tap cancel'),
        (0, 'if cancelled then log("cancelled"); return'),
        (0, 'msg ← compose(name, callback, location and age, time, trigger, evidenceExists)'),
        (0, 'for each number n do: send(msg, n.channel); log(n, status)'),
    ], 'O(a) for a authority numbers.'))
    b.append(algo('alg10', 'nearest safe location (A10)', 'a position p and the directory entries with coordinates', 'the nearest entry, its distance and its bearing', [
        (0, 'best ← null'),
        (0, 'for each entry e of category hospital or police do:'),
        (1, 'd ← haversine(p, e.position)'),
        (1, 'if best = null or d < best.d then best ← (e, d)'),
        (0, 'bearing ← initialBearing(p, best.e.position)       // degrees from north'),
        (0, 'return (best.e, best.d, bearing)'),
    ], 'O(n) for n entries.'))

    # ------------------------------------------------------------ 5.2
    b.append(H2('External APIs/SDKs', 'apis'))
    b.append(P('{tbl:sdks} lists the third-party APIs and SDKs. Versions are pinned in the dependency lock files of the project; the table gives the major version or the family.'))
    b.append(TBL('sdks', 'External APIs and SDKs', ['Name and Version', 'Description', 'Purpose of Usage', 'Endpoint, Function or Module'], [
        ['Flutter 3.x (stable) and Dart 3.x', 'Cross-platform UI toolkit and language.', 'User application and admin website.', 'All screens and packages.'],
        ['Firebase Authentication (FlutterFire, current stable)', 'Identity service.', 'Phone sign-in and administrator sign-in.', 'verifyPhoneNumber, signInWithEmail.'],
        ['Cloud Firestore (FlutterFire)', 'Real-time document database with offline cache.', 'Shared data and acknowledgements.', 'collection, snapshots, transactions.'],
        ['Firebase Cloud Messaging', 'Push delivery.', 'Alerts and help requests.', 'send by token; topic by geohash.'],
        ['Cloud Storage for Firebase', 'File storage with rules.', 'Identity images and child photos.', 'putFile, getDownloadURL, delete.'],
        ['Cloud Functions for Firebase (Node.js)', 'Server-side functions.', 'Email, acknowledgement, scheduled jobs.', 'HTTPS callable; scheduled; Firestore triggers.'],
        ['Firebase Hosting', 'Static and dynamic web hosting.', 'Admin website and alert page.', 'Custom domains, rewrites to functions.'],
        ['Google Maps SDK for Android 18.x', 'Interactive maps.', 'Heatmap, family map and online guidance.', 'GoogleMap, Polygon, Marker.'],
        ['Open map data and an open-source map renderer (for example MapLibre)', 'Offline map areas.', 'Maps without a connection.', 'Region download; offline style.'],
        ['TensorFlow Lite 2.x', 'On-device inference runtime.', 'Sound classification; embedding.', 'Interpreter.run.'],
        ['YAMNet-class audio-event model', 'Pre-trained sound classifier {cite:hershey2017}.', 'Distress sound score.', 'Input 0.975 s frames; class scores.'],
        ['sherpa-onnx keyword spotter', 'Open-source offline keyword spotting {cite:sainath2015}.', 'Safe and duress phrases.', 'Keyword spotter with a typed phrase.'],
        ['MiniLM-class sentence-embedding model (384 dimensions)', 'Sentence embeddings {cite:reimers2019}.', 'Semantic library search.', 'embed(text).'],
        ['Drift on SQLite', 'Local relational database.', 'Queue, log, library, directory.', 'Tables and DAOs.'],
        ['Riverpod 2.x', 'State management.', 'Providers for all modules.', 'Provider, Notifier.'],
        ['Android WorkManager 2.x', 'Persistent background work.', 'Queue retries; expiry jobs.', 'OneTimeWorkRequest.'],
        ['Android SmsManager (API 26 and later)', 'SMS sending.', 'SOS and escalation SMS.', 'sendMultipartTextMessage.'],
        ['Android Keystore', 'Hardware-backed key storage.', 'Evidence key.', 'KeyGenerator AES-256.'],
        ['Fused Location Provider', 'Location source.', 'Fixes and movement.', 'requestLocationUpdates.'],
        ['Email delivery service (to be selected, Appendix C)', 'Transactional email.', 'Email alerts.', 'HTTPS API called from a function.'],
    ], [2.0, 1.9, 1.8, 2.3], fs=16))

    # ------------------------------------------------------------ 5.3
    b.append(H2('REST API Specification', 'rest'))
    b.append(P('The project backend exposes the HTTPS interfaces in {tbl:rest}. The alert page and the interfaces used by it are served from the alert subdomain through Firebase Hosting rewrites (alert.muhaffiz.live); the administrator interfaces are served from muhaffiz.me under the path /api/v1. Requests and responses use JSON, except the alert page, which is HTML. Scheduled functions, which have no HTTP interface, compute the cell scores, expire missing-child reports and invitations, and remove reports older than 12 months.'))
    b.append(TBL('rest', 'Project backend interfaces', ['API ID', 'Method', 'Endpoint', 'Purpose', 'Authentication', 'Request', 'Success Response', 'Errors'], [
        ['API-01', 'POST', '/v1/alerts/email', 'Send the email copy of an SOS (FR-01.02).', 'User ID token', '{sosId, recipients[], text, lat, lng, time}', '202 {accepted}', '400 invalid; 401; 429 rate; 502 provider'],
        ['API-02', 'POST', '/v1/alerts/push', 'Push an SOS to trustees who have the application.', 'User ID token', '{sosId, phones[], text, lat, lng}', '202 {sent}', '400; 401; 429'],
        ['API-03', 'GET', '/alert/{token}', 'Show the alert page with location and time.', 'Unguessable token', '-', '200 HTML', '404 unknown; 410 expired'],
        ['API-04', 'POST', '/alert/{token}/ack', 'Record a trustee acknowledgement (FR-19.01).', 'Unguessable token', '{name?}', '200 {recorded}', '404; 409 duplicate; 410'],
        ['API-05', 'POST', '/v1/help-requests', 'Create a help request and notify helpers in the radius (FR-08.02).', 'User ID token', '{lat, lng}', '201 {id, notified}', '400; 401; 429'],
        ['API-06', 'GET', '/v1/heatmap/cells', 'Return cell scores for the viewport (FR-07.04).', 'User ID token', '?bbox=...', '200 [{geohash7, score, counts}]', '400; 401'],
        ['API-07', 'POST', '/api/v1/admin/reports/{id}/decision', 'Decide on a flagged report (FR-16.02).', 'Administrator token', '{decision, suspendAuthor?}', '200 {status}', '403; 404; 409'],
        ['API-08', 'POST', '/api/v1/admin/helpers/{uid}/decision', 'Approve, reject or revoke a helper (FR-16.03).', 'Administrator token', '{decision}', '200 {status}', '403; 404; 409'],
        ['API-09', 'GET', '/api/v1/admin/metrics', 'Return delivery success and errors (FR-16.04).', 'Administrator token', '?from&to', '200 {byChannel, errors[]}', '403; 400'],
    ], [0.6, 0.5, 1.6, 1.8, 0.8, 1.2, 1.0, 1.1], fs=15))

    # ------------------------------------------------------------ 5.4
    b.append(H2('Implemented User Interface', 'implui'))
    b.append(P('This section presents the interface of each subsystem that is not shown in Section {sec:hmi}. The mobile application is shown in {fig:ui_m1} to {fig:ui_m7}, and the admin website in {fig:admin_overview} and {fig:admin_queue}.'))
    b += land_group([('ui_m1', 'Mobile application: privacy summary and consent'), ('ui_m2', 'Mobile application: sign-in and phrase enrolment'), ('ui_m3', 'Mobile application: incident report and nearby help'), ('ui_m4', 'Mobile application: helper registration and missing-child report'), ('ui_m5', 'Mobile application: evidence and directory'), ('ui_m6', 'Mobile application: safe-location guidance and escalation warning'), ('ui_m7', 'Mobile application: escalation settings and app disguise')])
    b.append(P('The onboarding screens collect the consent and prepare the safety features: the consent screen states what the microphone is used for and that processing stays on the phone; the sign-in screen verifies the phone number; the phrase screen enrols the safe and the duress phrase with three spoken samples each. The settings screen holds one switch for each sensor-based feature, and the privacy summary lists where data are kept. The incident form takes a category, a location that can be adjusted on the map and an optional note. The nearby-help screen shows a request with distance and age and the accept and decline buttons, and states plainly when it is unavailable offline. The evidence list shows each recording with export and delete actions, the directory offers a call button for each service, and the safe-location screen shows the nearest hospital or police station with its distance and direction. The escalation warning counts down from 30 seconds with a single cancel button.'))
    b += land_group([('admin_overview', 'Admin website: overview'), ('admin_queue', 'Admin website: moderation queue')])
    b.append(P('The admin website has a side menu with the overview, the moderation queue, the helper review and the health pages. The overview shows registration counts, pending helpers, items to review and the delivery success by channel, with phone numbers masked. The moderation queue lists flagged heatmap reports, missing-child reports and helper applications with the decision buttons; every decision is logged.'))

    # ------------------------------------------------------------ 5.5
    b.append(H2('Deployment', 'deploy'))
    b.append(P('**Environments.** {tbl:envs} describes the three environments. The deployment view in {fig:deployment} shows where each part runs in production.'))
    b.append(TBL('envs', 'Deployment environments', ['Environment', 'Purpose', 'Backend', 'Data', 'Access'], [
        ['Development', 'Daily work on each package', 'Firebase Local Emulator Suite and a development project', 'Generated test data', 'The two developers'],
        ['Testing', 'Execution of the test plan on devices', 'A separate test Firebase project', 'Seeded accounts, reports and helpers, labelled as simulated', 'Developers and test users'],
        ['Production', 'The system as used', 'The production Firebase project with muhaffiz.me and alert.muhaffiz.live', 'Real user data under the privacy rules', 'Users; administrators'],
    ], [1.1, 1.6, 2.2, 1.8, 1.3]))
    b.append(P('**Server setup.** The Firebase projects are created with Authentication (phone and email providers), Cloud Firestore in native mode with the security rules and indexes of Section {sec:data}, Cloud Storage with its rules, Cloud Functions in a single region, Cloud Messaging and Hosting. The custom domains are connected to Firebase Hosting through DNS records: muhaffiz.me serves the admin website and alert.muhaffiz.live serves the alert page; HTTPS certificates are provisioned by the platform. Administrator accounts are created by the project owner and given the administrator role claim.'))
    b.append(P('**CI/CD.** Source code is kept in a Git repository. On each push a pipeline analyses the code, runs the unit tests and the rule tests against the emulator, and builds the application package. A tagged release additionally deploys the rules, indexes, functions and hosting to the target project with the Firebase command line, and produces a signed installable package of the application for test users.'))
    b.append(P('**Backup and monitoring.** Server data are exported with the Firebase command line before each release. Evidence recordings are deliberately excluded from every backup, because they exist only on the device (BR-23). Monitoring uses the usage dashboards of the platform for quota, a crash-reporting service for the application, and the Health page of the admin website for delivery success and backend errors (FR-16.04). **Deployment diagram.** {fig:deployment} is the deployment diagram of the system.'))
    b.append(H2('Chapter Summary', 'ch5sum'))
    b.append(P('This chapter gave the default parameters and the pseudocode of ten core algorithms, the third-party APIs and SDKs, the nine backend interfaces, the screens of the application and the admin website, and the environments, setup, pipeline and monitoring used for deployment. Chapter 6 now defines how the system is tested and evaluated.'))
    return b
