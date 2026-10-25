from srslib import *
import figs_pro, gv_uml, gv_beh, figs_seq, swim, figs_ui, os
import fr_common
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams')
def F(name): return (os.path.join(OUT, name + '.svg'), os.path.join(OUT, name + '.png'))
def land_fig(key, cap):
    return [FIG(key, cap, svg=F(key)[0], png=F(key)[1])]
def land_group(items):
    return [FIG(k, c, svg=F(k)[0], png=F(k)[1]) for k, c in items]

def blocks(ctx):
    figs_pro.architecture(); figs_pro.deployment(); figs_pro.components(); figs_pro.navigation(); gv_uml.make(); gv_beh.make(); figs_seq.make(); swim.make(); figs_ui.make()
    b = []
    b.append(H1('System Design', 'ch4'))
    b.append(P('**Chapter Overview.** This chapter translates the requirements of Chapter 3 into a design. Section {sec:method} gives the design methodology and process model, Section {sec:arch} the architecture, Section {sec:models} the design models, Section {sec:data} the data design, Section {sec:hmi} the human interface design, Section {sec:secdesign} the security, error-handling and logging design, and Section {sec:risk} the risk analysis and the milestone plan.'))

    # ------------------------------------------------------------ 4.1
    b.append(H2('Design Methodology and Software Process Model', 'method'))
    b.append(P('Muhaffiz is designed with an object-oriented method. The domain is expressed as classes with clear responsibilities (Section {sec:models}), behaviour is described with use cases, sequence, activity and state models, and the structure follows a layered architecture in which a small event-driven core handles triggers. This follows the practice described for software design descriptions {cite:ieee1016} and for object-oriented systems {cite:sommerville}. Object orientation suits the product because its central problem, that many different triggers must lead to one consistent behaviour, maps directly to a shared set of classes (TriggerEngine, SosOrchestrator and DeliveryManager).'))
    b.append(P('The software process is incremental and iterative, organized in short sprints that group into milestones. Each milestone delivers a working increment that is built on the previous one. The order of milestones is risk-driven: the modules whose feasibility is least certain, namely distress detection, offline voice activation and offline delivery, are built early so that problems are found while there is still time to change the approach. A team of two with a fixed academic schedule benefits from this: scope can be reduced late by dropping low-priority modules (Section {sec:elicit}) without disturbing the core. Section {sec:risk} gives the milestones and the risks.'))
    b.append(P('The design follows five principles that come from the objectives of the project.'))
    b.append(BUL([
        '**Privacy by design:** sensitive audio is processed and discarded on the device; the backend receives only what a feature needs.',
        '**Offline first:** the path that gets an alert out never depends on the backend; SMS and the local queue are on that path.',
        '**One trigger pipeline:** manual, automatic and voice triggers, the opt-out and the decoy all pass through shared components.',
        '**Fail safe:** a failing channel, model or sensor disables only itself, and manual SOS stays available.',
        '**Configuration over code:** thresholds, timers and limits are held in one configuration so that they can be tuned during evaluation.',
    ]))

    # ------------------------------------------------------------ 4.2
    b.append(H2('Architectural Design', 'arch'))
    b.append(P('**Architecture style.** Muhaffiz combines three styles. The Android application uses a layered architecture (presentation, application, domain and data, and platform layers) so that screens do not depend on platform details. Inside the application, the triggers, the delivery pipeline and the escalation timers are event-driven: detectors publish events and managers react to them. The application and the admin website use a backend-as-a-service architecture, in which Firebase provides authentication, data, messaging, storage and server-side functions. {fig:architecture} shows the main parts and their connections.'))
    b += land_fig('architecture', 'Architecture of Muhaffiz (box-and-line view)')
    b.append(P('**Decomposition.** {tbl:decomp} maps the modules to the packages of the application and to the backend, and states what each package is responsible for.'))
    b.append(TBL('decomp', 'Decomposition of the system into packages', ['Package', 'Responsibility', 'Modules', 'Main interface'], [
        ['sos_core', 'Runs the SOS from start to close; owns the SOS event and its state.', 'MOD-01', 'start(trigger, mode), cancel(), complete()'],
        ['trigger_engine', 'Receives manual, automatic and voice triggers and applies the countdown rule.', 'MOD-01, 02, 03', 'onManual(), onAutomatic(), onVoice()'],
        ['detection_engine', 'Monitors sound level, classifies bursts, reads motion sensors and applies the fusion rule.', 'MOD-02', 'start(), stop(), events'],
        ['voice_engine', 'Offline keyword spotting for the safe and duress phrases; context-aware delivery of detections.', 'MOD-03', 'start(), stop(), setContext(), events'],
        ['evidence_vault', 'Records and encrypts audio; lists, exports and deletes recordings.', 'MOD-18', 'startRecording(), list(), export()'],
        ['escalation', 'Tracks acknowledgements, runs the timers, composes and sends the escalation message.', 'MOD-19', 'onDispatched(), onAcknowledged()'],
        ['delivery_manager, sms_gateway, offline_store', 'Detects the connectivity tier, sends on each channel, queues and retries; holds the local database and cache.', 'MOD-12, 13', 'dispatch(), flush(), cache API'],
        ['family_circle, location_sharing', 'Circles, invitations, movement-based location publication, opt-out and last-known display.', 'MOD-04, 05', 'invite(), publish(), stopSharing()'],
        ['heatmap, near_help, missing_child', 'Incident reports and cell scores, helper registration and requests, missing-child reports.', 'MOD-07, 08, 17', 'submitReport(), broadcast(), file()'],
        ['library, semantic_search, directory, safe_navigation', 'Bundled content, on-device search, emergency directory, nearest safe location.', 'MOD-09, 10, 11, 20', 'search(), nearest(), call()'],
        ['auth, consent, decoy_mode, app_disguise', 'Sign-in and sessions, consent and toggles, decoy screen, launcher appearance.', 'MOD-06, 14, 15, 21', 'signIn(), toggle(), setAppearance()'],
        ['Cloud Functions', 'Email dispatch, acknowledgement endpoint, heatmap aggregation, expiry and clean-up jobs.', 'MOD-01, 07, 17, 19', 'HTTPS callable (Section {sec:rest})'],
        ['admin_site', 'Administrator sign-in, overview, moderation, helper review and health monitoring.', 'MOD-16', 'Firestore and Functions calls'],
    ], [1.6, 3.2, 1.0, 1.8], fs=16))
    b.append(P('**Deployment view.** {fig:deployment} shows where the parts run. The phone holds the application, the local database, the encrypted evidence and the on-device models. Firebase hosts the backend and the two web pages (the admin website and the alert page). Trustees reach the alert page and receive SMS, push, email and WhatsApp messages. Section {sec:deploy} gives the environments and the deployment procedure.'))
    b += land_fig('deployment', 'Deployment view of Muhaffiz')
    b.append(P('**Architecture decision records.** {tbl:adr} records the main decisions, the alternatives considered and the reasons.'))
    b.append(TBL('adr', 'Architecture decision records', ['ADR', 'Decision', 'Alternatives considered', 'Rationale and consequence'], [
        ['ADR-01', 'Flutter for the user interface, with Kotlin platform channels for services, SMS, sensors and launcher aliases.', 'Native Kotlin; React Native.', 'One code base for a two-person team; native code is limited to the parts Flutter cannot reach.'],
        ['ADR-02', 'Firebase as the backend platform.', 'Supabase; Cloudflare Workers and D1.', 'Phone authentication, real-time listeners, offline cache and push messaging come in one platform within free-tier limits.'],
        ['ADR-03', 'A pre-trained audio-event classifier of the YAMNet class, run with TensorFlow Lite on the phone {cite:hershey2017}.', 'Cloud inference; training a custom model.', 'Keeps audio on the device and needs no training data or GPU. Accuracy is bounded by the pre-trained model and is evaluated (NFR-SAF-02).'],
        ['ADR-04', 'An open-source, offline keyword-spotting engine (the sherpa-onnx keyword spotter) for the two phrases {cite:sainath2015}.', 'Picovoice Porcupine; openWakeWord; Vosk grammar mode.', 'Needs no network, account or access key (CON-7) and accepts a phrase typed as text. Accuracy on local accents is evaluated; the alternatives remain as fallbacks.'],
        ['ADR-05', 'A compact sentence-embedding model of the MiniLM class with embeddings computed before release {cite:reimers2019}.', 'Keyword search only; hosted embedding service.', 'Search by meaning with no network call. The keyword fallback covers model failure.'],
        ['ADR-06', 'SMS through the Android SMS manager; WhatsApp through a share link that the user confirms.', 'WhatsApp Business API.', 'SMS needs no data. WhatsApp cannot be sent without user interaction, and the Business API needs paid, approved templates.'],
        ['ADR-07', 'SQLite through Drift for local data, with WorkManager for queue retries.', 'Key-value storage only.', 'A durable queue and relational queries survive restarts.'],
        ['ADR-08', 'AES-256-GCM encryption of evidence with a Keystore key; files in private storage, excluded from backup.', 'Plain files; cloud storage.', 'Evidence stays on the device and unreadable by other applications.'],
        ['ADR-09', 'Geohash cells of precision 7, aggregated by a scheduled Cloud Function.', 'PostGIS on a relational backend.', 'Works on Firestore without a second backend; cell queries are simple.'],
        ['ADR-10', 'Google Maps SDK for online maps; open map data for offline areas.', 'Google Maps only; open maps only.', 'Google\'s terms do not allow storing its tiles; open data can be stored for up to three areas.'],
        ['ADR-11', 'Riverpod for state management.', 'Bloc; Provider.', 'Testable, compile-safe providers fit the modular packages.'],
        ['ADR-12', 'The admin website is a separate Flutter web build on muhaffiz.me.', 'A page inside the user application; a separate JavaScript stack.', 'Separation from the user application (CON-11) with shared models and one language.'],
        ['ADR-13', 'Trustees without the application acknowledge through a hosted alert page linked in the message.', 'SMS reply parsing.', 'A link can be tracked reliably; SMS replies cannot be read without extra permissions.'],
    ], [0.85, 2.4, 1.5, 2.85], fs=16))

    # ------------------------------------------------------------ 4.3
    b.append(H2('Design Models', 'models'))
    b.append(P('Muhaffiz is an object-oriented, partly event-driven system, so the models are chosen to explain structure, interaction and behaviour. The use-case diagrams are in Section {sec:ucspec}. This section gives class diagrams for the main domains, system-sequence and detailed-sequence diagrams for the critical interactions, activity diagrams for workflows, state diagrams for entities with state-dependent behaviour, a component diagram, and an event-response table for the background behaviour. Data-flow diagrams are not used, because the system is not designed as a data-processing pipeline.'))
    b.append(H3('Class diagrams', 'classes'))
    b.append(P('The class diagrams are grouped by domain. {fig:class_core} shows the SOS core and its delivery: the SosOrchestrator creates a SosEvent for every SOS; the event has one ChannelDelivery for each trustee and channel; the DeliveryManager creates the deliveries, learns the tier from the ConnectivityMonitor and holds undelivered deliveries in the OutboundQueue. {fig:class_evidence} shows evidence and escalation: the EvidenceVault keeps the EvidenceRecordings of events, and the EscalationManager monitors an event, collects its Acknowledgements and, if needed, sends the escalation message to the AuthorityNumbers and logs it in EscalationRecords.'))
    b.append(FIG('class_core', 'Class diagram: SOS core and delivery', svg=F('class_core')[0], png=F('class_core')[1], width_in=6.3))
    b.append(FIG('class_evidence', 'Class diagram: evidence and escalation', svg=F('class_evidence')[0], png=F('class_evidence')[1], width_in=6.3))
    b.append(P('{fig:class_detect} shows detection: the AudioMonitor passes a burst to the SoundClassifier; the FusionRule combines the score with the MotionAnalyzer result and starts the CountdownController, which on expiry hands over to the TriggerEngine, and the TriggerEngine starts the SosOrchestrator. {fig:class_voice} shows voice and consent: the KeywordSpotter uses the PhraseProfile and sends detected phrases to the TriggerEngine, to the SharingManager (stop-sharing context) and to DecoyMode; the ConsentSettings enable the monitor and the spotter.'))
    b.append(FIG('class_detect', 'Class diagram: distress detection', svg=F('class_detect')[0], png=F('class_detect')[1], width_in=6.3))
    b.append(FIG('class_voice', 'Class diagram: voice activation, consent and decoy', svg=F('class_voice')[0], png=F('class_voice')[1], width_in=6.3))
    b.append(P('{fig:class_family} shows the family network: an Account creates Circles and has Memberships, a Circle issues Invitations, and a Membership shares a LocationShare under the control of the SharingManager. {fig:class_community} shows the community classes: Accounts submit IncidentReports that are counted in CellScores, apply to become a HelperProfile, create and answer HelpRequests, and file MissingChildReports.'))
    b.append(FIG('class_family', 'Class diagram: family network', svg=F('class_family')[0], png=F('class_family')[1], width_in=6.3))
    b.append(FIG('class_community', 'Class diagram: community', svg=F('class_community')[0], png=F('class_community')[1], width_in=6.3))
    b.append(P('{fig:class_knowledge} shows the knowledge classes: SemanticSearch ranks LibraryItems with a SentenceEmbedder and falls back to KeywordSearch, Bookmarks mark items, and the SafeLocationFinder chooses a DirectoryEntry. {fig:class_admin} shows identity and administration: the AuthService opens a session, AppDisguise changes the launcher appearance, and an AdminUser reviews the ModerationQueue, which records AdminDecisions.'))
    b.append(FIG('class_knowledge', 'Class diagram: library, search and directory', svg=F('class_knowledge')[0], png=F('class_knowledge')[1], width_in=6.3))
    b.append(FIG('class_admin', 'Class diagram: identity, disguise and administration', svg=F('class_admin')[0], png=F('class_admin')[1], width_in=6.3))
    b.append(H3('System-sequence and detailed-sequence diagrams', 'sequences'))
    b.append(P('{fig:seq_ssd_sos} is the system-sequence diagram of the manual SOS (UC-01): it treats Muhaffiz as one unit and shows only the exchange with the user, the trustee and a helper. The detailed-sequence diagrams then show how the components cooperate. {fig:seq_dispatch} shows the dispatch of an SOS. {fig:seq_auto} shows automatic detection (UC-02) with its cancel path, and {fig:seq_voice} the voice trigger (UC-03). {fig:seq_optout} shows the stop-sharing by safe phrase (UC-09), including that no message reaches other members. {fig:seq_escalate} shows the escalation (UC-25), and {fig:seq_queue} the retry of the outbound queue. {fig:seq_invite} shows the invitation and acceptance of a circle member (UC-07), {fig:seq_nearhelp} the nearby-help request (UC-15), {fig:seq_child} the missing-child report (UC-23), {fig:seq_search} the semantic search (UC-17), {fig:seq_helper} the helper verification (UC-14), {fig:seq_report} the incident report and heatmap (UC-12, UC-13), and {fig:seq_signin} the sign-in (UC-19).'))
    for k, cap in (('seq_ssd_sos', 'System-sequence diagram: manual SOS (UC-01)'), ('seq_dispatch', 'Detailed sequence: SOS dispatch'), ('seq_auto', 'Detailed sequence: automatic distress detection (UC-02)'), ('seq_voice', 'Detailed sequence: voice-triggered SOS (UC-03)'),
                   ('seq_optout', 'Detailed sequence: stop sharing by safe phrase (UC-09)'), ('seq_escalate', 'Detailed sequence: escalation to authorities (UC-25)'), ('seq_queue', 'Detailed sequence: offline queue and retry'),
                   ('seq_invite', 'Detailed sequence: circle invitation (UC-07)'), ('seq_nearhelp', 'Detailed sequence: nearby help (UC-15)'), ('seq_child', 'Detailed sequence: missing-child report (UC-23)'),
                   ('seq_search', 'Detailed sequence: semantic library search (UC-17)'), ('seq_helper', 'Detailed sequence: helper verification (UC-14)'), ('seq_report', 'Detailed sequence: incident report and heatmap (UC-12, UC-13)'), ('seq_signin', 'Detailed sequence: sign-in (UC-19)')):
        b.append(FIG(k, cap, svg=F(k)[0], png=F(k)[1], width_in=6.3))
    b.append(H3('Activity diagrams', 'activities'))
    b.append(P('{fig:activity_sos_a} shows the first phase of an SOS, from the trigger to the dispatch, with the work that runs in parallel after the SOS starts, and {fig:activity_sos_b} the response phase with the acknowledgement check and the escalation. {fig:activity_tier} shows the tiered delivery and its queue. {fig:activity_voice} shows how a detected phrase is handled in its context, and {fig:activity_search} the semantic search with its fallback. Four workflows involve several parties and are drawn with swimlanes: {fig:activity_onboard} the onboarding and consent, {fig:activity_child} the missing-child report with moderation, {fig:activity_report} the incident report and the heatmap aggregation, {fig:activity_helper} the helper verification and {fig:activity_nearhelp} the nearby help.'))
    for k, cap, w in (('activity_sos_a', 'Activity diagram: SOS pipeline, trigger and dispatch', 5.4), ('activity_sos_b', 'Activity diagram: SOS pipeline, response and escalation', 5.4), ('activity_tier', 'Activity diagram: tiered delivery and retry', 5.4), ('activity_voice', 'Activity diagram: phrase handling in context', 5.8), ('activity_search', 'Activity diagram: semantic search with fallback', 5.0),
                      ('activity_onboard', 'Activity diagram with swimlanes: onboarding and consent', 5.6), ('activity_child', 'Activity diagram with swimlanes: missing-child report', 6.3), ('activity_report', 'Activity diagram with swimlanes: incident report and heatmap', 6.3),
                      ('activity_helper', 'Activity diagram with swimlanes: helper verification', 6.3), ('activity_nearhelp', 'Activity diagram with swimlanes: nearby help', 6.3)):
        b.append(FIG(k, cap, svg=F(k)[0], png=F(k)[1], width_in=w))
    b.append(H3('State diagrams', 'states'))
    b.append(P('{fig:state_sos_a} shows the first part of the life of an SOS event (trigger, countdown, dispatch) and {fig:state_sos_b} the second part (response, escalation, close), with the actions performed on entering each state. {fig:state_countdown} shows the confirmation countdown. {fig:state_share} shows a circle member, including the stopped state in which others see only the last location, and {fig:state_invite} the invitation. {fig:state_child} shows a missing-child report, {fig:state_helper} a helper application, {fig:state_tier} the connectivity tier, and {fig:state_evidence} an evidence recording.'))
    for k, cap, w in (('state_sos_a', 'State diagram: SOS event, trigger and dispatch', 5.2), ('state_sos_b', 'State diagram: SOS event, response and escalation', 5.2), ('state_countdown', 'State diagram: confirmation countdown', 5.2), ('state_share', 'State diagram: circle member and sharing', 5.4), ('state_invite', 'State diagram: circle invitation', 4.6),
                      ('state_child', 'State diagram: missing-child report', 6.0), ('state_helper', 'State diagram: Verified Helper application', 5.2), ('state_tier', 'State diagram: connectivity tier', 5.6), ('state_evidence', 'State diagram: evidence recording', 4.8)):
        b.append(FIG(k, cap, svg=F(k)[0], png=F(k)[1], width_in=w))
    b.append(H3('Component diagram and event-response table', 'components'))
    b.append(P('{fig:components} shows the packages grouped by function and the runtime dependencies between the groups. The safety core depends on delivery and storage, which depends on the backend functions; identity and consent control the safety core; the family and community group uses delivery for push and queueing; and the knowledge group uses bundled data.'))
    b += land_fig('components', 'Component diagram')
    b.append(P('The detection, delivery and escalation behaviour is driven by events in the background, so {tbl:events} lists the important events, the state of the system when they occur and the response.'))
    b.append(TBL('events', 'Event-response table', ['Event', 'System State', 'Response'], [
        ['Sound level rises suddenly above the ambient level', 'Detection on; monitoring', 'Classify the buffered burst; read motion; apply the fusion rule (FR-02.02, FR-02.03).'],
        ['Fusion rule satisfied', 'Monitoring', 'Start the 20-second countdown: vibration and a cancel control (FR-02.04).'],
        ['User cancels during the countdown (swipe, spoken or typed safe phrase)', 'Countdown', 'Stop the vibration, send nothing, resume monitoring.'],
        ['Countdown ends with no cancel', 'Countdown', 'Start the SOS with trigger "automatic" or "voice".'],
        ['Safe phrase detected', 'Voice on; no stop-sharing screen open', 'Start the countdown and then the SOS (FR-03.04); during a countdown with spoken cancel enabled, cancel it (FR-03.05).'],
        ['Safe phrase detected', 'Stop-sharing screen open', 'Unlock the sharing toggle; start no SOS; sharing stops when the toggle is switched off (FR-05.02).'],
        ['Duress phrase detected', 'Voice on', 'Start the silent countdown (no vibration, no indication), then a silent SOS; show the decoy screen (FR-03.04, FR-06.01).'],
        ['Connectivity tier changes', 'Any', 'Update the status strip; flush the queue if the tier is 2 or 3 (FR-12.01, FR-12.03).'],
        ['Fresh location fix not obtained in 10 seconds', 'SOS starting', 'Use the cached location and state its age (FR-13.01).'],
        ['Acknowledgement received', 'SOS active; timer running', 'Record it, stop the timer, show it (FR-19.01).'],
        ['3-minute timer expires with no acknowledgement', 'SOS active', 'Start the 30-second warning (FR-19.03).'],
        ['Warning ends with no cancel', 'Escalation warning', 'Send the escalation message and log it (FR-19.05, FR-19.06).'],
        ['Device restarts', 'Detection or voice enabled', 'Restart the services and the queue worker (NFR-REL-03).'],
        ['72 hours pass without renewal', 'Missing-child report active', 'Set "expired", delete the photo, stop alerts (FR-17.03).'],
    ], [2.6, 1.9, 3.5]))

    # ------------------------------------------------------------ 4.4
    b.append(H2('Data Design', 'data'))
    b.append(P('The information domain is divided into data held on the server in Cloud Firestore and data held only on the device. Firestore holds what must be shared between users: accounts, trustees, circles, memberships, invitations, shared locations, reports and cell scores, helper profiles and requests, acknowledgements, missing-child reports and administrator decisions. The device holds what must stay private or work offline: the SOS events and their deliveries, the outbound queue, the evidence recordings and their keys, the escalation records, the bundled library and directory, bookmarks and settings. Retention follows the rules of Chapter 3: evidence is deleted after the retention period (BR-23), heatmap reports older than 12 months are removed (NFR-PRV-02), photos are deleted when no longer needed (BR-26), and identity images are deleted after review (BR-18).'))
    b.append(P('**Data dictionary.** {tbl:dict} lists the entities in alphabetical order with their storage, attributes and meaning. Two further entities, the consent record and the authority numbers, are stored on the device as settings and are not drawn in the entity-relationship diagram.'))
    dd = [
     ('Acknowledgement', 'Server', 'id: string; sosId: string; source: enum(trustee, helper); at: timestamp', 'A confirmation by a trustee or a helper that they have seen the alert.'),
     ('Account', 'Server', 'uid: string; phone: string; name: string; messageTemplate: string(160); defaultMode: enum; createdAt: timestamp', 'A registered user.'),
     ('AdminDecision', 'Server', 'id: string; adminUid: string; target: string; decision: enum; at: timestamp', 'A logged moderation or review decision.'),
     ('AuthorityNumber', 'Device', 'number: string; channel: enum(sms, call, share)', 'A configured authority number for escalation.'),
     ('Bookmark', 'Device', 'itemId: string; createdAt: timestamp', 'A bookmarked library item.'),
     ('CellScore', 'Server', 'geohash7: string; counts: map(category to int); score: double; updatedAt: timestamp', 'The aggregated, weighted report score of one cell.'),
     ('ChannelDelivery', 'Device', 'id: string; sosId: string; trusteeId: string; channel: enum; status: enum; attempts: int; lastAttempt: timestamp', 'The delivery of one SOS message on one channel to one trustee.'),
     ('Circle', 'Server', 'id: string; createdBy: string; createdAt: timestamp', 'A family circle.'),
     ('ConsentRecord', 'Device', 'micDetection: bool; voiceActivation: bool; locationSharing: bool; acceptedAt: timestamp', 'The user\'s consent and toggles.'),
     ('DirectoryEntry', 'Device (bundled)', 'id: string; name: string; category: enum; phone: string; lat, lng: double?', 'A hospital, police station, helpline or emergency number.'),
     ('EscalationRecord', 'Device', 'id: string; sosId: string; number: string; channel: enum; status: enum; at: timestamp', 'One escalation message and its delivery.'),
     ('EvidenceRecording', 'Device', 'id: string; sosId: string; startedAt: timestamp; duration: int; trigger: enum; encryptedPath: string', 'An encrypted audio recording made after an SOS.'),
     ('HelperProfile', 'Server', 'uid: string; status: enum(pending, verified, rejected, revoked); verifiedAt: timestamp', 'The helper status of a user.'),
     ('HelpRequest', 'Server', 'id: string; uid: string; geohash: string; radius: int; status: string; createdAt: timestamp', 'A request for nearby help.'),
     ('IncidentReport', 'Server', 'id: string; uid: string; category: enum; note: string(280)?; geohash7: string; createdAt: timestamp; status: enum', 'A user report of an unsafe incident.'),
     ('Invitation', 'Server', 'id: string; circleId: string; toPhone: string; status: enum; expiresAt: timestamp', 'An invitation to a circle.'),
     ('LibraryItem', 'Device (bundled)', 'id: string; title: string; category: enum; summary: string; body: string; embedding: float[384]', 'A library article, video or link and its search embedding.'),
     ('Membership', 'Server', 'id: string; circleId: string; uid: string; state: enum; sharing: bool; lastShared: (lat, lng, time)', 'The membership of a user in a circle and its sharing state.'),
     ('MissingChildReport', 'Server', 'id: string; guardianUid: string; childName: string; age: int; photoRef: string; description: string; lastSeen: (place, time); status: enum; expiresAt: timestamp', 'A missing-child report.'),
     ('QueueItem', 'Device', 'id: string; deliveryId: string; payload: blob; dueAt: timestamp', 'An outbound message waiting to be sent or retried.'),
     ('SosEvent', 'Device', 'id: string; startedAt: timestamp; trigger: enum; mode: enum; location: (lat, lng); locationAge: int; status: enum', 'One SOS from start to close.'),
     ('Trustee', 'Server and device', 'id: string; uid: string; name: string; phone: string; email: string?; channels: set', 'A contact who receives alerts.'),
    ]
    b.append(TBL('dict', 'Data dictionary', ['Entity', 'Storage', 'Attributes (name: type)', 'Description'], [list(d) for d in dd], [1.3, 0.9, 3.6, 2.2], fs=16))
    b.append(P('**ER diagrams.** {fig:er_users}, {fig:er_community}, {fig:er_device} and {fig:er_content} show the entities. The first two show the entities held on the server in Cloud Firestore (accounts, trustees, circles and administrator decisions; then community data), and the last two the entities held on the device (SOS data, then bundled content and settings). Crow\'s-foot notation shows the cardinality of each relationship, and foreign keys (FK) name the related entity.'))
    for k, cap in (('er_users', 'Entity-relationship diagram: server data, accounts and circles'), ('er_community', 'Entity-relationship diagram: server data, community'), ('er_device', 'Entity-relationship diagram: device data, SOS records'), ('er_content', 'Entity-relationship diagram: device data, bundled content and settings')):
        b.append(FIG(k, cap, svg=F(k)[0], png=F(k)[1], width_in=6.3))
    b.append(P('**Normalization, indexes and constraints.** The device database is relational and is kept in third normal form: a delivery refers to its SOS event and trustee by key, and a queue item refers to its delivery. The server data is document-oriented and is deliberately denormalized where a screen needs it in one read, for example the member\'s last shared location is stored inside the membership. {tbl:indexes} lists the indexes and the constraints that protect integrity.'))
    b.append(TBL('indexes', 'Indexes and constraints', ['Store', 'Index or Constraint', 'Purpose'], [
        ['Firestore', 'Index on Membership (circleId, state)', 'List the members of a circle and their state.'],
        ['Firestore', 'Index on IncidentReport (geohash7, createdAt)', 'Load the reports of a cell and apply the 12-month limit.'],
        ['Firestore', 'Index on HelperProfile (status) and geohash of the last position', 'Find verified helpers within a radius.'],
        ['Firestore', 'Index on MissingChildReport (status, lastSeen geohash)', 'Find active reports near a place.'],
        ['Firestore', 'Index on Acknowledgement (sosId, at)', 'Read the acknowledgements of one SOS.'],
        ['Firestore rules', 'Account.phone is unique; (circleId, uid) is unique; age is between 0 and 17; enumerated values only', 'Integrity of server data.'],
        ['Firestore rules', 'A user reads another user\'s location only under BR-10 to BR-14 and BR-32; only administrators read identity images', 'Confidentiality (NFR-SEC-03, NFR-SEC-06).'],
        ['SQLite', 'Index on ChannelDelivery (sosId); index on QueueItem (dueAt); index on LibraryItem (category)', 'Fast log, retry and library queries.'],
        ['SQLite', 'Foreign keys with delete cascade: deliveries and queue items are deleted with their SOS event', 'No orphan rows.'],
    ], [1.0, 4.2, 2.8], fs=16))

    # ------------------------------------------------------------ 4.5
    b.append(H2('Human Interface Design', 'hmi'))
    b.append(P('The interface is designed so that the most important action, the SOS, is available at once, and so that every protective feature is easy to reach but not obvious to a bystander. A new user passes through sign-in, consent, trustee setup and phrase enrolment, and then reaches the Home screen, from which the main areas are reached by the bottom navigation. {fig:navigation} shows the navigation flow, and {tbl:screens} lists the screens with their purpose, objects, actions and related requirements.'))
    b += land_fig('navigation', 'Navigation flow of the application')
    b.append(P('**Screen images.** {fig:ui_k1} to {fig:ui_k5} show the key screens from the user\'s perspective: the Home, countdown and SOS-active screens, the family map, the danger map and the library search, and the decoy, stop-sharing, trustee and settings screens. The other screens are shown in Section {sec:implui}.'))
    b += land_group([('ui_k1', 'Key screens: Home and countdown'), ('ui_k2', 'Key screens: SOS active and family map'), ('ui_k3', 'Key screens: danger map and library search'), ('ui_k4', 'Key screens: decoy and stop sharing'), ('ui_k5', 'Key screens: trustees and settings')])
    b.append(P('**Screen objects and actions.** On the Home screen the large red SOS control starts an SOS when it is held for one second, the Loud and Silent switch selects the SOS mode, the status strip shows the connectivity tier and the state of detection and voice activation, and four tiles open the trustees, the evidence list, the directory and the safe-location guidance. On the countdown screen a ring shows the seconds left and a large button and the swipe, the spoken safe phrase or the typed safe phrase cancel the alert, as set in the settings; a loud countdown vibrates and makes no sound, and a silent countdown shows nothing. On the SOS-active screen a red banner shows that an SOS is active, a card for each trustee shows the delivery status per channel, a card shows the nearby helpers, and the Stop alarm and Evidence buttons act on the siren and the recording. The family map shows each member as a marker, a live member in green and a member who has stopped sharing in grey with the label "Not live", and a button opens the stop-sharing screen. The danger map shows green-to-red cells with a legend, and a tap on a cell opens a panel with the category counts. The library search screen has a field for a question in the user\'s words, category chips, an offline indicator, and result cards with a relevance bar. The decoy screen is a calculator that works normally; a two-second hold on the equals key opens the real application. The stop-sharing screen asks for the safe phrase, shows that the phone is listening, unlocks the sharing toggle when the phrase is recognised and states that nobody else is notified. The trustee screen lists trustees with a chip for each enabled channel.'))
    scr = [
     ['S-01 Sign-in', 'Primary User', 'Verify the phone number', 'Number field, send code, code field, verify', 'FR-14.01, UC-19'],
     ['S-02 Onboarding consent', 'Primary User', 'Obtain informed consent', 'Consent text, agree box, accept, not now', 'FR-15.01, FR-18.05, UC-20'],
     ['S-03 Trustees', 'Primary User', 'Manage trustees and channels', 'Trustee cards, channel chips, add, edit, remove', 'FR-01.05, UC-04'],
     ['S-04 Phrase enrolment', 'Primary User', 'Enrol the safe and duress phrases', 'Phrase fields, sample progress, record', 'FR-03.01, FR-03.02, UC-06'],
     ['S-05 Home', 'Primary User', 'Start an SOS; see status', 'SOS control, mode switch, status strip, tiles, navigation', 'FR-01.01, FR-01.04, FR-12.01, UC-01'],
     ['S-06 Countdown', 'Primary User', 'Cancel an automatic or voice alert', 'Ring, seconds, cancel button', 'FR-02.04, FR-03.04, UC-02, UC-03'],
     ['S-07 SOS active', 'Primary User', 'Follow the SOS', 'Banner, delivery cards, helper card, stop alarm, evidence', 'FR-01.02, FR-01.03, FR-01.06, FR-19.01'],
     ['S-08 Family circle', 'Family Circle Member', 'See members; invite; stop sharing', 'Map, member cards, invite, stop-sharing button', 'FR-04.01, FR-04.02, FR-05.04, UC-07, UC-08'],
     ['S-09 Stop sharing', 'Family Circle Member', 'Stop sharing by safe phrase', 'Prompt, listening indicator, cancel, leave link', 'FR-05.02, FR-05.03, UC-09, UC-10'],
     ['S-10 Danger map', 'Primary User', 'View the heatmap', 'Map, cells, legend, zone panel, report button', 'FR-07.04, UC-13'],
     ['S-11 Incident report', 'Primary User', 'Report an incident', 'Category chips, location pin, note, submit', 'FR-07.01, UC-12'],
     ['S-12 Nearby help', 'Primary User; Verified Helper', 'Request or answer help', 'Request card, accept, decline, offline notice', 'FR-08.02 to FR-08.04, UC-15'],
     ['S-13 Helper registration', 'Primary User', 'Apply to become a helper', 'Name, phone, identity photo, submit, status', 'FR-08.01, UC-14'],
     ['S-14 Library', 'Primary User', 'Browse and search', 'Search field, chips, result cards, bookmark', 'FR-09.01 to FR-10.05, UC-16, UC-17'],
     ['S-15 Missing-child report', 'Guardian', 'File a report', 'Child fields, photo, guardian box, submit', 'FR-17.01, UC-23'],
     ['S-16 Evidence list', 'Primary User', 'Manage recordings', 'Recording cards, export, delete, retention note', 'FR-18.03, FR-18.04, UC-24'],
     ['S-17 Directory', 'Primary User', 'Call an emergency service', 'Entry cards, call buttons', 'FR-11.01 to FR-11.03, UC-18'],
     ['S-18 Safe location', 'Primary User', 'Get guidance to the nearest safe place', 'Map, route line, distance card, open directions', 'FR-20.01 to FR-20.03, UC-26'],
     ['S-19 Escalation warning', 'Primary User', 'Cancel an escalation', 'Seconds, cancel button', 'FR-19.03, UC-25'],
     ['S-20 Escalation settings', 'Primary User', 'Set authority numbers and channels', 'Number cards, change, add', 'FR-19.04, UC-25'],
     ['S-21 Settings and consent', 'Primary User', 'Change toggles and defaults', 'Switches, retention', 'FR-15.02, FR-14.03, UC-20'],
     ['S-22 Privacy summary', 'Primary User', 'See what is stored and where', 'Three data cards', 'FR-15.03, UC-20'],
     ['S-23 App disguise', 'Primary User', 'Choose an appearance', 'Option cards, apply', 'FR-21.01, FR-21.02, UC-27'],
     ['S-24 Decoy', 'Primary User', 'Show a neutral screen', 'Calculator keys, hidden hold', 'FR-06.01, FR-06.02, UC-11'],
     ['S-25 Admin overview', 'Administrator', 'See users, queues and delivery', 'Metric tiles, charts, bars', 'FR-16.01, FR-16.04, UC-22'],
     ['S-26 Moderation queue', 'Administrator', 'Decide on flagged items', 'Table, approve, remove, reject', 'FR-16.02, FR-16.03, UC-21'],
    ]
    b.append(TBL('screens', 'Screens of the application and the admin website', ['Screen ID and Name', 'User or Role', 'Purpose', 'Main Objects and Actions', 'Related FR or UC'], scr, [1.4, 1.2, 1.6, 2.4, 1.6], fs=16))

    # ------------------------------------------------------------ 4.6
    b.append(H2('Security, Error Handling and Logging Design', 'secdesign'))
    b.append(P('**Authentication and authorization.** Users authenticate with a one-time code sent to their phone number; administrators authenticate with email and password and hold an administrator role (FR-14.01, FR-16.05). Authorization is enforced on the server by Firestore and Storage rules, so that a client cannot read data it is not entitled to even if it is modified. **Input validation** is applied on the device and again by the rules and the functions. **Sensitive data** is handled by keeping audio on the device, encrypting evidence, deleting identity images and photos after use, and masking phone numbers in the admin website.'))
    b.append(P('**Error handling.** A failure is handled where it occurs and isolated from the safety path: a failed channel is logged and queued, a failed model disables only its feature, a missing permission produces a prompt, and a full storage stops only the recording. User messages state the problem and the next step in at most two sentences (NFR-USA-06). **Logging.** The device keeps an SOS event log and an escalation log for the user, and a technical log at three levels (error, warning, information) that holds no audio, no transcript and no location trace. The backend logs function errors and delivery outcomes without user identities for the health monitoring of FR-16.04. Administrator decisions are logged with the administrator and the time. Logs on the device are private to the application, and server logs are readable only by administrators and the developers; technical logs are kept for 30 days. {tbl:secdesign} lists the main threats, failures and events with their handling.'))
    sec = [
     ['SD-01', 'A user tries to read another user\'s location', 'Firestore rules allow reads only under BR-10 to BR-14 and BR-32.', 'Denied requests counted in the backend log.', 'NFR-SEC-03, BR-32'],
     ['SD-02', 'A non-administrator opens the admin website', 'Role check on sign-in and in every rule; access denied.', 'Denied attempt logged.', 'FR-16.05, NFR-SEC-04'],
     ['SD-03', 'A one-time code is guessed', 'Lock for 10 minutes after five wrong codes; code expiry.', 'Lock events logged.', 'FR-14.01'],
     ['SD-04', 'An evidence file is copied from the device', 'AES-256-GCM encryption; key in the Keystore; private storage; no backup.', 'No log of file content.', 'FR-18.02, NFR-SEC-02'],
     ['SD-05', 'Audio would leave the device', 'The detection and voice packages have no network access; tests inspect traffic.', 'Test alert if traffic appears.', 'FR-02.05, NFR-SEC-05'],
     ['SD-06', 'A model file is missing or corrupt', 'Disable the feature, tell the user, keep manual SOS.', 'Warning logged on the device.', 'NFR-ROB-01'],
     ['SD-07', 'The SMS permission is missing', 'Prompt (loud mode) and use other channels.', 'Event logged with the missing permission.', 'FR-12.02, UC-01 E1'],
     ['SD-08', 'No data connection', 'Use SMS; queue the other channels; retry later.', 'Delivery status in the SOS log.', 'FR-12.03, BR-05'],
     ['SD-09', 'The monitoring service is stopped by the system', 'Restart by the system and after reboot; onboarding explains battery settings.', 'Restart logged.', 'FR-02.01, NFR-REL-03'],
     ['SD-10', 'A report spam or malicious flagging of an area', 'Rate limits, near-duplicate check, burst detection and moderation.', 'Moderation queue entry.', 'FR-07.05, BR-15'],
     ['SD-11', 'A person pretends to be a helper', 'Identity check by an administrator before approval; revocation.', 'Decision logged.', 'FR-08.01, FR-16.03, BR-18'],
     ['SD-12', 'A false missing-child report', 'Immediate review queue, removal, author suspension, rate limit.', 'Decision logged.', 'FR-17.05, BR-27'],
     ['SD-13', 'A child photo or identity image is exposed', 'Storage rules; deletion on found, expiry or decision.', 'Deletion logged.', 'FR-17.06, NFR-SEC-06'],
     ['SD-14', 'Malformed or oversized input', 'Validation on the device, in the rules and in the functions.', 'Rejected input counted.', 'NFR-ROB-02'],
     ['SD-15', 'Low storage during an SOS', 'Stop the recording; continue the SOS.', 'Entry in the SOS log.', 'NFR-ROB-03'],
     ['SD-16', 'The application is killed during an SOS', 'The queue and the SOS state are stored in SQLite and resumed at start.', 'Resume logged.', 'NFR-REL-02'],
     ['SD-17', 'A function or the backend fails', 'The safety path does not call the backend; functions are retried; errors are shown to administrators.', 'Function error log.', 'NFR-AVL-01, FR-16.04'],
     ['SD-18', 'The phone is forced open by another person', 'Decoy screen and app disguise; duress phrase.', 'No visible log entry.', 'FR-06.01, FR-21.01, BR-28'],
    ]
    b.append(TBL('secdesign', 'Security, error handling and logging design', ['Design ID', 'Threat, Failure or Event', 'Control or Handling Strategy', 'Log or Alert', 'Related Requirement'], sec, [0.7, 2.0, 2.8, 1.4, 1.4], fs=16))

    # ------------------------------------------------------------ 4.7
    b.append(H2('Risk Analysis and Sprint Plan', 'risk'))
    b.append(P('{tbl:risks} lists the risks with their probability and impact (High, Medium or Low), their mitigation or contingency, and the owner. Muhammad Shamoil owns the detection, voice, search, SOS front end, decoy, consent, evidence, escalation and disguise modules and the interface design; Ali Raza owns the backend, family, location, heatmap, Near Help, missing-child, delivery, navigation, authentication and admin modules and the deployment.'))
    risks = [
     ['RSK-01', 'The pre-trained sound classifier produces too many false alarms or misses.', 'Medium', 'High', 'Confirm-or-cancel countdown; fusion with motion; evaluate on labelled clips and tune thresholds; manual SOS is the primary path.', 'M. Shamoil'],
     ['RSK-02', 'The keyword spotter is unreliable for local accents or Urdu phrases.', 'Medium', 'High', 'Test with team and volunteer voices; use the sensitivity set at enrolment; fall back to openWakeWord or Vosk; manual SOS remains.', 'M. Shamoil'],
     ['RSK-03', 'Android stops background services to save battery.', 'High', 'High', 'Foreground services; request battery-optimisation exemption in onboarding; restart logic; test on several manufacturers.', 'M. Shamoil'],
     ['RSK-04', 'Battery use of monitoring is too high.', 'Medium', 'Medium', 'Spike gate keeps classification rare; measure against NFR-PER-10; reduce sampling if needed.', 'M. Shamoil'],
     ['RSK-05', 'SMS cannot be sent because of permission policy or carrier limits.', 'Medium', 'High', 'Request the permission clearly; test on several carriers; provide the other channels and the queue.', 'A. Raza'],
     ['RSK-06', 'WhatsApp cannot send without the user.', 'High', 'Low', 'Treated as user-confirmed; SMS, push and email are the automatic channels (BR-04).', 'A. Raza'],
     ['RSK-07', 'Near Help is not useful because few helpers are nearby.', 'High', 'Medium', 'Evaluate with simulated helpers and label them as such; fall back to trustees by SMS.', 'A. Raza'],
     ['RSK-08', 'Authorities do not act on, or accept, escalation messages.', 'Medium', 'High', 'Describe the hand-off precisely; let the user choose channels; confirm numbers before use (Appendix C).', 'M. Shamoil'],
     ['RSK-09', 'Privacy or consent concerns about listening.', 'Medium', 'High', 'Explicit consent, on-device processing, no audio storage, privacy summary, tests that inspect traffic and storage.', 'M. Shamoil'],
     ['RSK-10', 'Coercion defeats the consent model despite the safeguards.', 'Medium', 'Medium', 'Document the limit; use the safe phrase, the decoy and the last-known display; do not claim it is solved.', 'A. Raza'],
     ['RSK-11', 'Firebase free-tier limits are exceeded.', 'Low', 'Medium', 'Quota calculation; movement-based updates; scheduled aggregation; reduce listener scope.', 'A. Raza'],
     ['RSK-12', 'False or abusive reports and helper applications.', 'Medium', 'Medium', 'Rate limits, moderation queue, identity review, revocation.', 'A. Raza'],
     ['RSK-13', 'The schedule is too short for all 21 modules.', 'Medium', 'High', 'Build in priority order; the Low modules (MOD-20, MOD-21) are dropped first, then Medium modules, without touching the core.', 'Both'],
     ['RSK-14', 'Offline map data licence or size is a problem.', 'Medium', 'Low', 'Limit to three areas; choose a source that permits storage; guidance works with distance and direction alone.', 'A. Raza'],
     ['RSK-15', 'A device or Android version behaves differently.', 'Medium', 'Medium', 'Test on at least three device models; isolate platform code in the platform layer.', 'Both'],
     ['RSK-16', 'The microphone indicator of Android reveals recording in a silent SOS.', 'High', 'Low', 'Cannot be hidden; documented as a limitation; evidence can be switched off in the settings.', 'M. Shamoil'],
    ]
    b.append(TBL('risks', 'Risk analysis', ['Risk ID', 'Risk', 'Probability', 'Impact', 'Mitigation or Contingency', 'Owner'], risks, [0.7, 2.2, 0.8, 0.7, 2.9, 0.8], fs=16))
    b.append(P('{tbl:milestones} lists the milestones in the order in which they are built. The plan uses milestones and not calendar dates; the dependencies show why the order is fixed.'))
    ms = [
     ['M1 Foundation', 'Project skeleton, theme, navigation, local database, authentication, consent flow, configuration', 'MOD-14, MOD-15, MOD-13', 'Running application with sign-in, onboarding and settings', 'None', 'Scheduled'],
     ['M2 Core SOS and delivery', 'Manual SOS, trustees, dispatch on all channels, loud and silent modes, tiers, queue and retry, event log', 'MOD-01, MOD-12, MOD-13', 'Working SOS delivered by SMS at Tier 1 and by all channels at Tiers 2 and 3', 'M1', 'Scheduled'],
     ['M3 Detection and voice', 'Monitoring service, classifier, fusion, countdown, keyword spotting, phrase enrolment, shared hook', 'MOD-02, MOD-03', 'Automatic and voice SOS with cancel', 'M2', 'Scheduled'],
     ['M4 Family network and decoy', 'Circles, invitations, movement-based sharing, opt-out, last-known display, decoy', 'MOD-04, MOD-05, MOD-06', 'Family map with duress-aware sharing; decoy screen', 'M1, M3', 'Scheduled'],
     ['M5 Community and admin', 'Incident reports, geohash aggregation, heatmap, helper registration, Near Help, admin site', 'MOD-07, MOD-08, MOD-16', 'Heatmap, nearby help and moderation', 'M2', 'Scheduled'],
     ['M6 Knowledge', 'Library, semantic search, directory, safe-location guidance, offline maps', 'MOD-09, MOD-10, MOD-11, MOD-20', 'Offline library with search; directory; guidance', 'M1', 'Scheduled'],
     ['M7 Follow-through', 'Evidence recording, escalation, missing-child report, app disguise', 'MOD-17, MOD-18, MOD-19, MOD-21', 'Evidence, escalation, missing-child alerts, disguise', 'M2, M5', 'Scheduled'],
     ['M8 Evaluation and hardening', 'Test execution, detection and search evaluation, fixes, documentation', 'All modules', 'Test results, evaluation, final documents', 'M1 to M7', 'Scheduled'],
    ]
    b.append(TBL('milestones', 'Milestone plan', ['Sprint or Milestone', 'Objectives', 'Requirements or Modules', 'Deliverables', 'Dependencies', 'Status'], ms, [1.2, 2.5, 1.2, 2.0, 0.7, 0.8], fs=16))
    b.append(H2('Chapter Summary', 'ch4sum'))
    b.append(P('This chapter chose an object-oriented, layered and partly event-driven design built in risk-driven milestones, recorded the main architecture decisions, presented the class, sequence, activity, state and component models, the data design with the entity-relationship diagram, the screens and their navigation, the security, error-handling and logging design, and the risks and milestones. Chapter 5 now describes the algorithms, external components, backend interfaces, user interface and deployment that realize this design.'))
    return b
