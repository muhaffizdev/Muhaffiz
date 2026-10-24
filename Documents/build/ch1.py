from srslib import *

TITLE = 'Muhaffiz: Offline-First Safety for Women and Children'

MODULES = [
 ('MOD-01', 'SOS Alert System',
  'Manual SOS trigger on the home screen and as a lock-screen quick action; simultaneous dispatch of live location and a preset message by WhatsApp, in-app push, email and SMS; loud alarm and silent mode; trustee management; SOS event log.',
  'Primary User; Trustee (recipient)'),
 ('MOD-02', 'Automatic Danger Detection Engine',
  'Low-power background monitoring that stays dormant until a sudden loud sound; on-device classification of distress sounds; fusion with motion sensors; 20-second countdown before the SOS fires, cancelled by the swipe, the spoken safe phrase or the typed safe phrase as the user chooses. No audio leaves the phone.',
  'Primary User'),
 ('MOD-03', 'Voice Activation and Safe-Phrase Engine',
  'Fully offline keyword spotting. A safe phrase fires a loud SOS and a different duress phrase fires a silent SOS; the same engine confirms the family-sharing opt-out and supports Decoy Mode.',
  'Primary User'),
 ('MOD-04', 'Family Circle Management',
  'Creation of a family circle; invitations that both people must accept; member list with each person\'s sharing status and last update time; leaving a circle, which is separate from pausing sharing.',
  'Primary User; Family Circle Member'),
 ('MOD-05', 'Location Sharing and Privacy Controls',
  'Location updates on significant movement; opt-out by spoken safe phrase without anyone\'s approval; private confirmation shown only to the person who opted out; timestamped last-known location marked as not live; real-time sharing status.',
  'Family Circle Member'),
 ('MOD-06', 'Decoy Mode',
  'A neutral, unrelated-looking screen replaces the app when the user is forced to unlock the phone; a hidden gesture returns to the real app; SOS, voice triggers and location updates continue underneath.',
  'Primary User'),
 ('MOD-07', 'Danger Heatmap',
  'Incident report form (category, auto-filled editable location, optional note); geohash grid; recency weighting; Google Maps overlay from green to red; zone details without identifying reporters; rate limits and abuse checks.',
  'Primary User; Administrator (moderation)'),
 ('MOD-08', 'Near Help',
  'Verified-helper registration with an identity check; help requests broadcast to verified users within a set radius; accept or decline screen; clear "unavailable, no connection" state when offline.',
  'Primary User; Verified Helper'),
 ('MOD-09', 'Content Library Management',
  'Curated articles, videos and links on prevention and post-trauma care, grouped by category, bundled with the app for offline use; browsing with category filters and bookmarks.',
  'Primary User'),
 ('MOD-10', 'Semantic Search Engine',
  'On-device search of the library by meaning: pre-computed content embeddings, query embedding on the phone, cosine-similarity ranking, keyword-search fallback and ranked result cards.',
  'Primary User'),
 ('MOD-11', 'Emergency Services Directory',
  'Localized directory of hospitals, police stations, helplines and emergency numbers (including Rescue 1122 and women\'s helplines) with one-tap calling and nearest-first ordering when location is available.',
  'Primary User'),
 ('MOD-12', 'Tiered Delivery System',
  'Detection of connectivity as Tier 1 (no connection), Tier 2 (any connection) or Tier 3 (good connection); SMS delivery that works at Tier 1; automatic queue and retry of alerts created offline.',
  'Primary User (system service)'),
 ('MOD-13', 'Offline Data Caching',
  'Last-known-location cache used when no fresh GPS fix is available at SOS time; on-device database for library content, map tiles for frequent areas and pending outbound alerts.',
  'Primary User (system service)'),
 ('MOD-14', 'Authentication and Account Management',
  'Phone-number sign-up and login; secure session handling with automatic re-authentication; profile and settings (name, emergency message template, linked trustees); account recovery for lost devices.',
  'Primary User'),
 ('MOD-15', 'Consent and Privacy Controls',
  'Onboarding consent explaining what the detection and voice engines listen for; separate toggles for microphone detection, location sharing and voice activation; in-app privacy summary.',
  'Primary User'),
 ('MOD-16', 'Admin Dashboard',
  'Separate website for administrators: user overview, moderation queue for flagged heatmap reports, review queue for approving or revoking Near Help helpers, and monitoring of delivery success and backend errors.',
  'Administrator'),
 ('MOD-17', 'Missing-Child Report',
  'Report form (name, age, photo, description, last-seen place and time, guardian contact); alert to the guardian\'s trusted contacts and nearby verified users; active, found and expired status handling; hand-off to official channels; moderation and child-data privacy.',
  'Primary User (Guardian); Administrator'),
 ('MOD-18', 'Evidence Recording on SOS',
  'Audio recording that starts automatically when an SOS fires; encrypted storage on the device only; evidence list with time, location and trigger; user controls to stop, delete, export and auto-delete.',
  'Primary User'),
 ('MOD-19', 'Escalation to Authorities',
  'Tracking of trustee and helper acknowledgements; 3-minute no-response timer; 30-second warning countdown with cancel; escalation message to configured authority numbers (SMS, call or share); escalation log.',
  'Primary User; Authority Contact (recipient)'),
 ('MOD-20', 'Safe-Location Navigation',
  'One-tap directions from the current position to the nearest safe location, designed to work from data stored on the device when there is no connection.',
  'Primary User'),
 ('MOD-21', 'App Disguise',
  'Option to change the app\'s launcher icon and name to a neutral appearance so that it does not reveal itself as a safety application.',
  'Primary User'),
]

DEFS = [
 ('Accelerometer', 'A phone sensor that measures acceleration. It is combined with the gyroscope to recognise a sudden drop or struggle movement.'),
 ('Administrator', 'A member of the Muhaffiz team authorised to use the web-based Admin Dashboard (MOD-16).'),
 ('Android', 'The mobile operating system on which the Muhaffiz application runs.'),
 ('API', 'Application Programming Interface: a defined way for one software component to request services from another.'),
 ('Authority Contact', 'A phone number of an official emergency service, for example Police 15 or Rescue 1122, configured to receive escalation messages (MOD-19).'),
 ('Bilateral Opt-in', 'The rule that sharing between two people starts only after both have explicitly accepted.'),
 ('Cosine Similarity', 'A measure of how alike two vectors are, based on the angle between them. It is used to rank search results against a query.'),
 ('Decoy Mode', 'A mode in which the application shows a neutral, unrelated-looking screen instead of its real interface while safety functions continue in the background (MOD-06).'),
 ('Duress', 'A situation in which a person is forced or threatened into acting against their will.'),
 ('Duress Phrase', 'A spoken phrase, chosen by the user and different from the safe phrase, that fires a silent SOS.'),
 ('Embedding', 'A numeric vector that represents the meaning of a piece of text, produced by a language model.'),
 ('Evidence Recording', 'Audio recorded on the device after an SOS fires and stored there in encrypted form (MOD-18).'),
 ('FCM', 'Firebase Cloud Messaging: the Google service that delivers push notifications to Android devices.'),
 ('Firebase', 'The Google backend platform used for authentication, database, messaging, storage and hosting.'),
 ('Firestore', 'Cloud Firestore: the Firebase document database, which supports real-time listeners and a local offline cache.'),
 ('Flutter', 'The Google user-interface toolkit, programmed in Dart, used to build the Android application.'),
 ('Foreground Service', 'An Android service that runs with a visible notification so that the operating system does not stop it. Muhaffiz uses one for monitoring.'),
 ('FR', 'Functional Requirement.'),
 ('FYP', 'Final Year Project.'),
 ('Geohash', 'A short string that identifies a rectangular geographic cell. It is used to group nearby points into fixed-size cells.'),
 ('GPS', 'Global Positioning System: satellite-based positioning used to obtain the phone\'s location.'),
 ('Gyroscope', 'A phone sensor that measures rotation.'),
 ('Heatmap', 'A map overlay that colours each area from green to red according to the recency-weighted density of incident reports (MOD-07).'),
 ('Incident Report', 'A user-submitted record of an unsafe event, with a location, a category and an optional note.'),
 ('Keyword Spotting', 'Recognition of specific words or phrases in audio without transcribing general speech.'),
 ('Last-Known Location', 'The most recent location a person shared before they stopped sharing. It is shown with a timestamp and is marked as not live.'),
 ('Near Help', 'The module that sends a help request to Verified Helpers within a set radius (MOD-08).'),
 ('NFR', 'Non-Functional Requirement.'),
 ('Offline-first', 'A design approach in which critical functions work without a data connection and remote synchronisation happens when a connection returns.'),
 ('On-device Processing', 'Computation carried out on the user\'s phone, with no audio or analysis result sent to a server.'),
 ('Primary User', 'A registered person who uses Muhaffiz for their own safety or, as a guardian, for the safety of a child.'),
 ('Rescue 1122', 'An emergency rescue helpline operating in Pakistan.'),
 ('Safe Location', 'A place from the application\'s bundled directory, such as a police station or hospital, to which a user can be directed in an emergency (MOD-20).'),
 ('Safe Phrase', 'A spoken phrase, chosen by the user, that fires a loud SOS and confirms an opt-out from family location sharing.'),
 ('SDS', 'Software Design Specification.'),
 ('SMS', 'Short Message Service: text messaging over the cellular network, which does not need a data connection.'),
 ('SOS', 'An emergency alert sent from the application to the user\'s trustees and, where applicable, to other recipients.'),
 ('SRS', 'Software Requirements Specification.'),
 ('Tier 1, Tier 2, Tier 3', 'The three connectivity levels used by delivery: Tier 1 is no data connection, Tier 2 is any data connection, Tier 3 is a good data connection (MOD-12).'),
 ('TensorFlow Lite (TFLite)', 'A lightweight runtime for running machine-learning models on mobile devices.'),
 ('Trustee', 'A contact chosen by a Primary User to receive SOS alerts. A trustee may or may not have the application installed.'),
 ('Unilateral Opt-out', 'The rule that a person can stop sharing their location at any time without anyone\'s approval.'),
 ('Verified Helper', 'A registered user who has passed an identity check and agreed to respond to Near Help requests.'),
 ('WhatsApp', 'A messaging application used by Muhaffiz as one SOS dispatch channel.'),
 ('Acknowledgement', 'A confirmation by a trustee or a helper that they have seen an alert; it stops the no-response timer.'),
 ('ADR', 'Architecture decision record: a short record of a design decision, the alternatives and the reasons.'),
 ('AES-256-GCM', 'An authenticated encryption method with a 256-bit key, used for evidence recordings.'),
 ('Alert Page', 'A web page, served by Firebase Hosting and linked in an SOS message, where a trustee can see the alert and acknowledge it.'),
 ('Android Keystore', 'The Android facility that holds cryptographic keys so that they cannot be read by other applications.'),
 ('CI/CD', 'Continuous integration and continuous delivery: automatic building, testing and deployment of the software.'),
 ('Cloud Functions', 'Server-side functions of Firebase that run in response to requests, events or schedules.'),
 ('Fusion Rule', 'The rule that combines the audio distress score with the motion result to decide whether to start the confirmation countdown.'),
 ('HTTPS and TLS', 'The secure web protocol and the encryption protocol (Transport Layer Security) that protects data in transit.'),
 ('Moderation Queue', 'The list of flagged reports and applications that an administrator reviews.'),
 ('OTP (One-Time Code)', 'A single-use code sent by SMS to verify a phone number.'),
 ('Outbound Queue', 'The on-device list of messages that could not yet be delivered and are retried.'),
 ('Platform Channel', 'The Flutter mechanism by which Dart code calls native Android (Kotlin) code.'),
 ('SQLite', 'A small relational database that runs inside the application.'),
 ('UI', 'User interface.'),
 ('WorkManager', 'The Android component that runs persistent background work, such as retrying the outbound queue.'),
 ('YAMNet', 'A pre-trained audio-event classification model that runs with TensorFlow Lite.'),
]
DEFS.sort(key=lambda d: d[0].lower())

def blocks(ctx):
    b = []
    b.append(H1('Introduction', 'ch1'))
    b.append(P('**Chapter Overview.** This chapter introduces the Muhaffiz software product and the people who will read and use this document. It states the purpose of the document and its readers (Section {sec:purpose}), the scope and boundaries of the project (Section {sec:scope}), the twenty-one modules of the system (Section {sec:modules}), the terminology used throughout (Section {sec:defs}) and the organization of the remaining chapters and appendices (Section {sec:overview}).'))

    b.append(H2('Purpose', 'purpose'))
    b.append(P('This document is the combined Software Requirements Specification (SRS) and Software Design Specification (SDS), version 1.0, for **%s**. Muhaffiz (from the Urdu word for "guardian") is an Android application, supported by a cloud backend and a separate web-based administration site, that helps a person call for help, be detected as being in distress, share their location with family under privacy safeguards, and reach safety information and emergency contacts, including when no data connection is available.' % TITLE))
    b.append(P('The document defines what the system shall do (the requirements) and how it will be structured to do it (the design). Every requirement has a unique identifier that is kept unchanged in the design, implementation and test documentation, so that each statement can be traced from its source to its verification. The document is written to be read by the following groups.'))
    b.append(BUL([
        '**Supervisor and evaluation committee:** to judge whether the scope is complete, coherent and achievable within a Final Year Project.',
        '**Developers:** to implement the system without having to guess intended behaviour.',
        '**Testers:** to derive test cases from the requirements, business rules and acceptance criteria.',
        '**Project managers:** to plan milestones, assign work and manage risk.',
        '**Users and stakeholders:** to confirm that the user-visible behaviour matches their needs and privacy expectations.',
        '**Documentation writers:** to prepare user and administrator guidance consistent with the specified behaviour.',
    ]))

    b.append(H2('Scope', 'scope'))
    b.append(P('Muhaffiz is an Android application for women and children, with a supporting cloud backend and an administration website. It is designed around three principles: an emergency alert must be able to leave the phone without a data connection; sensitive signals, namely microphone audio and voice phrases, are processed only on the phone; and every action that someone might be forced to perform is protected against coercion. The application provides a manual, automatic and voice-triggered SOS; family location sharing with consent rules that the tracked person controls; a community danger map; verified nearby helpers; an offline safety library with on-device semantic search; a directory of emergency services; evidence recording and escalation after an SOS; and a missing-child report. {tbl:scope} states what is committed for this project, what is excluded, and the expected benefits, so that committed work can be distinguished from possible future work.'))
    b.append(TBL('scope', 'Scope of the Muhaffiz project', ['Scope Category', 'Description'], [
        ['In Scope',
         '• An Android application, built with Flutter, that implements the twenty-one modules MOD-01 to MOD-21 listed in Section {sec:modules}.\n'
         '• A Firebase backend for authentication, data synchronisation, push messaging and storage, and server-side functions for channels that cannot run on the phone.\n'
         '• A separate administration website on its own domain (muhaffiz.me) that implements MOD-16.\n'
         '• On-device machine-learning components that use existing pre-trained models: distress-sound classification, keyword spotting and sentence embedding.\n'
         '• SOS delivery by WhatsApp, in-app push, email and SMS, with SMS usable without a data connection.\n'
         '• Verification of the system as described in Chapter 6.'],
        ['Out of Scope',
         '• Versions of the user application for iOS, desktop or the web.\n'
         '• Training any machine-learning model from scratch, and any GPU infrastructure.\n'
         '• Uploading, storing or transmitting raw audio from the detection and voice engines, and any video recording.\n'
         '• Direct system-to-system integration with police, emergency-service dispatch or government missing-child systems. Muhaffiz hands off by SMS, call or share to numbers and channels that are configured.\n'
         '• Any guarantee that an authority receives, accepts or acts on a message.\n'
         '• User-interface languages other than English.\n'
         '• Wearable devices and dedicated panic-button hardware.\n'
         '• Payments, advertising and any other monetisation.\n'
         '• The content of the promotional website (muhaffiz.live).'],
        ['Benefits',
         '• **For users:** an alert path that does not depend on a data connection (SMS still needs cellular coverage); hands-free and discreet ways to trigger help; microphone audio kept on the phone; control over who can see their location and a private way to stop sharing; safety information and emergency contacts available offline; audio evidence kept on the phone for later use.\n'
         '• **For communities:** a shared picture of areas reported as unsafe and a way to reach verified people nearby.\n'
         '• **For the project:** a demonstration of on-device machine learning, offline-first delivery and privacy-by-design combined in one system, with behaviour that can be measured and tested.'],
    ], [1.2, 6.2]))
    b.append(P('Where demonstration data or simulated users are needed to evaluate a module, for example for the heatmap or Near Help, they shall be identified as simulated in Chapter 6 and shall not be presented as real usage.'))

    b.append(H2('Modules', 'modules'))
    b.append(P('The functionality of Muhaffiz is divided into twenty-one modules. Each module has a persistent identifier of the form MOD-nn, which is used in the requirement catalogue, the design models and the test cases. {tbl:modules} lists the modules with their primary actors; the actors are described in Section {sec:users}.'))
    b.append(TBL('modules', 'Modules of Muhaffiz', ['Module ID', 'Module Name', 'Description', 'Primary Actor or User'],
                 [list(m) for m in MODULES], [0.9, 1.6, 4.4, 1.5]))

    b.append(H2('Definitions, Acronyms and Abbreviations', 'defs'))
    b.append(P('{tbl:defs} defines the domain-specific terms, acronyms and abbreviations used in this document. The entries are in alphabetical order.'))
    b.append(TBL('defs', 'Definitions, acronyms and abbreviations', ['Term or Acronym', 'Definition'],
                 [[t, d] for t, d in DEFS], [1.8, 5.6]))

    b.append(H2('Document Overview', 'overview'))
    b.append(P('The remainder of this document is organized as follows.'))
    b.append(BUL([
        '**Chapter 2: Overall Description and Requirements Elicitation** places Muhaffiz in context, identifies the user classes, the operating environment, the constraints, assumptions and dependencies, and explains how the requirements were identified, prioritized and validated.',
        '**Chapter 3: Software Requirements Specification** gives the functional requirement catalogue and the specification of each functional requirement, the use cases, the business rules, the non-functional requirements and the external interface requirements.',
        '**Chapter 4: System Design** presents the design methodology, the architecture, the design models, the data design, the human interface design, the security, error-handling and logging design, and the risk analysis and milestone plan.',
        '**Chapter 5: Implementation and Deployment** describes the core algorithms, the external APIs and SDKs, the interfaces of the backend, the user interface and the deployment arrangement.',
        '**Chapter 6: Testing, Evaluation and Conclusion** defines the test cases at each level, the traceability matrix, and the conclusion with limitations and future enhancements.',
        '**References** lists the sources cited in IEEE style.',
        '**Appendix A** lists all use cases, **Appendix B** gives the detailed specifications of the use cases not given in Chapter 3, **Appendix C** lists items still to be determined, and **Appendix D** gives sample test data. The glossary is in Section {sec:defs} and is not repeated.',
    ]))
    b.append(P('Identifiers follow a fixed scheme: modules MOD-nn, functional requirements FR-nn.nn (the first number is the module), use cases UC-nn, business rules BR-nn, non-functional requirements NFR-xxx-nn, constraints CON-n, assumptions AS-n, dependencies DEP-n, and risks RSK-nn. Modules MOD-01 to MOD-16 keep the order of modules 7.1 to 7.16 of the approved project scope document; MOD-17 to MOD-21 were added after that document was written and are approved parts of the system.'))

    b.append(H2('Chapter Summary', 'ch1sum'))
    b.append(P('This chapter introduced Muhaffiz as an offline-first, on-device and coercion-aware safety application for women and children, defined the committed and excluded scope, listed the twenty-one modules, and fixed the terminology and identifier scheme. Chapter 2 now describes the context in which the system operates and how its requirements were identified.'))
    return b
