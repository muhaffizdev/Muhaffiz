from srslib import *
import fig_context

def blocks(ctx):
    svg, png = fig_context.make()
    b = []
    b.append(H1('Overall Description and Requirements Elicitation', 'ch2'))
    b.append(P('**Chapter Overview.** This chapter places Muhaffiz in its context and explains where its requirements come from. Section {sec:perspective} describes the origin of the product and its relationship to existing systems, Section {sec:users} identifies the user classes, Section {sec:env} states the operating environment, Section {sec:constraints} lists the constraints, assumptions and dependencies, and Section {sec:elicit} explains how requirements were identified, prioritized and validated.'))

    # ------------------------------------------------------------ 2.1
    b.append(H2('Product Perspective', 'perspective'))
    b.append(P('Muhaffiz is a new, self-contained product. It does not replace or extend an earlier system. It was conceived to address a safety gap that is large and well documented: worldwide, about one in three women experience physical or sexual violence in their lifetime {cite:who2021}. A person in danger needs to raise an alarm quickly, discreetly and in places where a data connection cannot be relied on, and a person who is being monitored by someone else needs a way to stop that monitoring safely.'))
    b.append(P('People currently combine general-purpose tools to do this. In the survey described in Section {sec:elicit}, the most common tool was WhatsApp live location (61% of the 73 respondents), followed by the phone\'s built-in emergency SOS (19%); 29% used nothing, and only 3% had ever used a dedicated safety application. The most common reason for not using a safety application was that it needs internet (71%). Muhaffiz does not compete with the national emergency helplines. It complements them: it can alert a person\'s own contacts first, and it hands a message to a helpline number when the contacts do not respond.'))
    b.append(P('The product consists of three parts. The **Android application** contains the on-device layer, which works without any network: sound-based distress detection, offline voice activation, SOS triggering, SMS dispatch, the offline library and its search, the local cache and the evidence recorder. The **Firebase backend** is the cloud coordination layer: authentication, family-circle synchronisation, the heatmap and Near Help data, push messaging, storage, and server-side functions for channels that cannot run on the phone, such as email. The **admin website** at muhaffiz.me lets administrators moderate reports and review helpers. {fig:context} shows the system as one unit and its interfaces with people and external services.'))
    b.append(FIG('context', 'Context diagram of Muhaffiz', svg=svg, png=png, width_in=6.2))
    b.append(P('The external entities and their interfaces are as follows.'))
    b.append(BUL([
        '**Primary User:** operates the application; sends SOS commands, settings, incident reports and searches, and receives alerts, map data and library results.',
        '**Family Circle Member:** shares location with, and views the sharing status of, other members of a circle.',
        '**Verified Helper:** receives nearby help requests and replies with accept or decline.',
        '**Trustee:** receives the SOS alert and may acknowledge it.',
        '**Authority Contact:** receives the escalation message when nobody has responded.',
        '**Administrator:** moderates reports, approves or revokes helpers, and monitors system health through the admin website.',
        '**Google Maps Platform:** supplies the map and tiles used by the heatmap, the family map and navigation.',
        '**Email provider:** carries the email copy of an SOS and returns delivery status.',
        '**WhatsApp:** receives the SOS share request on the user\'s phone.',
        '**Cellular SMS network:** carries SMS alerts, which need no data connection.',
    ]))

    # ------------------------------------------------------------ 2.2
    b.append(H2('User Classes and Characteristics', 'users'))
    b.append(P('{tbl:userclasses} lists every user class and external actor. Access level and frequency of use are given in the description.'))
    b.append(TBL('userclasses', 'User classes and external actors', ['User Class or Actor', 'Description', 'Expected Skills', 'Main Responsibilities or Interactions'], [
        ['Primary User', 'A registered person who uses Muhaffiz for personal safety. Authenticated by phone number. Full access to the user modules. Daily background use, with occasional active use.',
         'Basic smartphone use. No technical or security knowledge.', 'Configures trustees, phrases and privacy toggles; triggers or cancels SOS; reports incidents; uses the library, directory and navigation.'],
        ['Guardian', 'A Primary User who acts for a child. Same access as a Primary User, with additional access to the missing-child report.',
         'Basic smartphone use.', 'Files and updates a missing-child report; manages the child-related contacts.'],
        ['Family Circle Member', 'A Primary User who has joined a family circle. Access is limited to the circle they belong to. Continuous use while sharing.',
         'Basic smartphone use.', 'Accepts invitations; shares location; stops sharing by safe phrase; views other members\' status.'],
        ['Trustee', 'A contact chosen by a Primary User to receive SOS alerts. May have no account and no app, in which case alerts arrive by SMS, WhatsApp or email. Rare use, at the time of an alert.',
         'Reading a message and following a map link.', 'Receives alerts; may acknowledge an alert.'],
        ['Verified Helper', 'A Primary User who has passed an identity check and agreed to respond to nearby requests. Occasional use.',
         'Basic smartphone use.', 'Registers for verification; accepts or declines requests.'],
        ['Administrator', 'A member of the project team with access to the admin website. Daily or weekly use. Authenticated separately from the application.',
         'Web browser use; understanding of moderation rules.', 'Reviews flagged reports and missing-child reports; approves or revokes helpers; monitors delivery success and errors.'],
        ['Authority Contact (external)', 'An emergency service number configured for escalation. Not a user of Muhaffiz.',
         'Not applicable.', 'Receives the escalation message sent as SMS, call or share.'],
    ], [1.2, 2.6, 1.5, 2.4]))

    # ------------------------------------------------------------ 2.3
    b.append(H2('Operating Environment', 'env'))
    b.append(P('{tbl:env} gives the hardware, software, network and hosting environment in which Muhaffiz operates.'))
    b.append(TBL('env', 'Operating environment', ['Environment Item', 'Specification or Version', 'Purpose'], [
        ['Client operating system', 'Android 8.0 (API level 26) or later', 'Foreground services, notification channels and runtime permissions used by the safety engines.'],
        ['Client framework', 'Flutter (stable channel) with Dart; Android platform channels written in Kotlin', 'Single code base for the user interface, with platform channels for SMS, foreground services and launcher-icon switching.'],
        ['Client hardware', 'Smartphone with microphone, accelerometer, gyroscope, GPS receiver, speaker, vibration motor and SIM card; Google Play services', 'Sensing, alarm, vibration countdown, SMS delivery, push messaging and maps.'],
        ['Network', 'Cellular network (SMS, voice, data) and Wi-Fi', 'SOS must be deliverable by SMS without a data connection; other channels need data.'],
        ['Backend platform', 'Google Firebase: Authentication, Cloud Firestore, Cloud Messaging, Cloud Storage, Cloud Functions, Hosting', 'Identity, synchronisation, push, file storage, server-side functions and web hosting.'],
        ['Admin website', 'Flutter web build served by Firebase Hosting on the muhaffiz.me domain; current versions of Chrome, Edge, Firefox and Safari on desktop', 'Administrator access to moderation, helper review and monitoring.'],
        ['Maps', 'Google Maps SDK for Android', 'Heatmap overlay, family map and navigation display.'],
        ['Offline map data', 'Open map data (OpenStreetMap-derived) downloaded for up to three user-selected areas and stored on the device', 'Map display for frequent areas and safe-location guidance with no connection.'],
        ['On-device intelligence', 'TensorFlow Lite runtime; pre-trained models for sound classification, keyword spotting and sentence embedding, bundled with the application', 'Distress detection, voice activation and semantic search without a network.'],
        ['On-device storage', 'SQLite database; encrypted files protected by a key held in the Android Keystore', 'Offline library, cache, outbound queue and evidence recordings.'],
        ['Geography and language', 'Pakistan; English user interface', 'Target users and emergency numbers.'],
    ], [1.5, 3.2, 3.0]))
    b.append(BUL([
        'OE-1: The application shall operate correctly on Android 8.0 (API level 26) and later on phones that provide the sensors and radios listed in {tbl:env}.',
        'OE-2: The SOS dispatch by SMS shall operate with no data connection when cellular coverage is present.',
        'OE-3: The voice-activation, distress-detection, library, search, directory and evidence functions shall operate with no network connection.',
        'OE-4: The admin website shall operate correctly on the current versions of Chrome, Edge, Firefox and Safari on desktop computers.',
    ]))

    # ------------------------------------------------------------ 2.4
    b.append(H2('Design and Implementation Constraints, Assumptions and Dependencies', 'constraints'))
    b.append(P('The following constraints restrict the design and implementation. Each is followed by its rationale.'))
    b.append(BUL([
        'CON-1: The user application shall run on Android only. //Rationale:// Android permits the foreground services, background audio and SMS capability that the safety engines need; iOS restricts them.',
        'CON-2: The user application shall be built with Flutter and Dart, using Android platform channels where a native capability is required. //Rationale:// one code base is practical for a two-person team.',
        'CON-3: The backend shall use Firebase services. //Rationale:// they provide phone authentication, real-time synchronisation, push messaging and offline caching as one managed platform.',
        'CON-4: Machine-learning components shall use existing pre-trained models; no model shall be trained from scratch. //Rationale:// the project has no labelled incident data or GPU infrastructure.',
        'CON-5: Audio processed by the distress-detection and voice engines shall not be stored or transmitted off the device. //Rationale:// privacy and the consent given by the user.',
        'CON-6: Evidence recordings shall be stored only on the device, in encrypted form. //Rationale:// recordings are sensitive and are meant for the user to present later.',
        'CON-7: The voice-activation engine shall be open source or otherwise usable with no network access, account or access key. //Rationale:// voice activation must work fully offline.',
        'CON-8: Third-party services and components shall be used within their free tiers or free licences. //Rationale:// the project has no budget for paid services.',
        'CON-9: Microphone, location, SMS, notification and recording features shall run only after the user has granted the corresponding Android permission and has given consent in the application. //Rationale:// Android permission rules and the privacy principles of the product.',
        'CON-10: The user interface shall be in English. //Rationale:// approved project scope.',
        'CON-11: The admin website shall be served from its own domain, muhaffiz.me, and shall be separate from the user application. //Rationale:// administrative functions must not be reachable from the user application.',
        'CON-12: The system shall be completed within the final year project schedule by a team of two. //Rationale:// academic schedule and team size.',
    ]))
    b.append(P('{tbl:assume} states the assumptions, which are believed true but not guaranteed, and the external dependencies on which the project relies.'))
    b.append(TBL('assume', 'Assumptions and dependencies', ['ID', 'Type', 'Statement', 'Rationale or Source', 'Impact if Invalid'], [
        ['AS-1', 'Assumption', 'Users\' phones have a microphone, motion sensors, GPS, a vibration motor and a SIM card.', 'Typical of current Android smartphones.', 'Detection, countdown or SMS delivery is unavailable on the affected phone.'],
        ['AS-2', 'Assumption', 'Cellular coverage is available when an SOS is sent.', 'SMS needs the cellular network, not data.', 'The alert stays in the outbound queue until coverage returns.'],
        ['AS-3', 'Assumption', 'Users grant the required permissions and exclude the application from battery optimisation.', 'Android may stop background services otherwise.', 'Background detection and voice activation stop silently.'],
        ['AS-4', 'Assumption', 'A pre-trained sound classifier distinguishes distress sounds from other loud sounds well enough for a confirm-or-cancel design.', 'The 20-second cancel step limits the cost of an error.', 'False alarms or missed detections increase; manual SOS remains available.'],
        ['AS-5', 'Assumption', 'The keyword-spotting engine recognises the phrases users choose, including with local accents.', 'Phrases are user-chosen and short.', 'Voice triggers are unreliable; manual SOS remains available.'],
        ['AS-6', 'Assumption', 'Emergency numbers such as Police 15 and Rescue 1122 accept calls and text messages from the public.', 'Published public numbers.', 'Escalation messages are delivered but may not be acted on.'],
        ['AS-7', 'Assumption', 'At least one of a trustee\'s channels (SMS, WhatsApp, email, push) is reachable at alert time.', 'Trustees are chosen by the user.', 'The alert is not seen; escalation to authorities applies.'],
        ['AS-8', 'Assumption', 'Incident reports and helper registrations are submitted in good faith, and abuse is caught by rate limits and moderation.', 'Crowd-sourced data needs moderation.', 'The heatmap or helper list becomes unreliable.'],
        ['AS-9', 'Assumption', 'Library content is curated by the project team from reputable sources.', 'Curated, bundled content.', 'Library guidance is inaccurate.'],
        ['DEP-1', 'Dependency', 'Availability of Firebase services (Authentication, Firestore, Cloud Messaging, Storage, Functions, Hosting).', 'Chosen backend platform.', 'Synchronised features and push are unavailable; on-device and SMS functions continue.'],
        ['DEP-2', 'Dependency', 'Google Maps Platform and Google Play services on the phone.', 'Map display and push delivery.', 'Maps and push are unavailable; SMS and call functions continue.'],
        ['DEP-3', 'Dependency', 'WhatsApp installed on the user\'s phone for share-based dispatch.', 'WhatsApp is one dispatch channel.', 'The WhatsApp channel is skipped; other channels continue.'],
        ['DEP-4', 'Dependency', 'An email delivery service reachable from Cloud Functions.', 'Email is a dispatch channel.', 'The email channel fails; other channels continue.'],
        ['DEP-5', 'Dependency', 'Pre-trained models and their licences: sound classifier, keyword spotter and sentence embedder.', 'CON-4 and CON-7.', 'The affected on-device function cannot be delivered.'],
        ['DEP-6', 'Dependency', 'The cellular operators and the emergency services that receive escalation messages.', 'External recipients.', 'Escalation depends on their acceptance and response.'],
        ['DEP-7', 'Dependency', 'An open map-data source that permits offline storage.', 'Offline maps need data that may be stored on the device.', 'Offline map display is unavailable; online maps and distance guidance continue.'],
    ], [0.6, 1.2, 2.9, 1.9, 2.3], fs=17))

    # ------------------------------------------------------------ 2.5
    b.append(H2('Requirement Identifying Techniques', 'elicit'))
    b.append(P('**Elicitation.** Requirements were identified from five sources: analysis of the approved project scope document and the feature document; a review of existing safety applications and emergency helplines to see which features already exist; a questionnaire survey; semi-structured interviews; and use-case analysis by the project team. The survey received 73 responses, and the percentages quoted in this document are percentages of these 73 respondents. Survey figures state interest, not adoption.'))
    b.append(TBL('survey1', 'Survey: current practice and barriers (n = 73)', ['Finding', 'Result'], [
        ['Worry about the safety of a woman or child "often" or "almost every time"', '87%'],
        ['Has used a dedicated safety application', '3%'],
        ['Has used WhatsApp live location', '61%'],
        ['Has used the phone\'s built-in emergency SOS', '19%'],
        ['Has used nothing', '29%'],
        ['Barrier: the application needs internet', '71%'],
        ['Barriers: privacy, too slow or complicated, lack of trust, do not know a good one (each)', '39%'],
        ['Barrier: battery use', '19%'],
        ['Barrier: someone could force me to share my location', '13%'],
        ['Would use an application like this (for self, for a family member, or both)', '87%'],
        ['Would install it for a woman or child in the family', '58%'],
    ], [5.2, 2.2]))
    b.append(TBL('survey2', 'Survey: respondents likely or very likely to use each feature (n = 73)', ['Feature described in the survey', 'Likely or very likely', 'Related module'], [
        ['Decoy screen that hides the application when forced to unlock the phone', '87%', 'MOD-06'],
        ['Map of areas reported as unsafe', '84%', 'MOD-07'],
        ['One-tap list of nearby hospitals and helplines', '84%', 'MOD-11'],
        ['SOS sent to authorities', '81%', 'MOD-19'],
        ['Audio recording kept on the device as evidence while an SOS is active', '77%', 'MOD-18'],
        ['Missing-child report to verified users', '77%', 'MOD-17'],
        ['One-tap direction to the nearest safe area', '77%', 'MOD-20'],
        ['SOS button that sends live location, by SMS when there is no internet', '74%', 'MOD-01, MOD-12'],
        ['Family location map where everyone must agree and anyone can stop privately', '68%', 'MOD-04, MOD-05'],
        ['Safety tips searchable in your own words, even offline', '68%', 'MOD-09, MOD-10'],
        ['Secret phrase to call for help without touching the phone', '58%', 'MOD-03'],
        ['Alerting verified application users nearby', '58%', 'MOD-08'],
        ['Phone senses screaming or distress and sends an alert unless cancelled within 20 seconds', '55%', 'MOD-02'],
    ], [5.0, 1.4, 1.5]))
    b.append(P('The interviews were held with a high-school student, a working woman, a medical (MBBS) student and a male university student. {tbl:survey1} and {tbl:survey2} and the interviews led to the following requirements decisions.'))
    b.append(BUL([
        'Internet dependence was the most common barrier (71%). This supports the offline-first design of MOD-12 and MOD-13 and the requirement that voice, detection, library and search work with no network.',
        'The decoy screen was the most favoured feature (87%) and was named by a medical student as one of the most valuable. This supports MOD-06 and MOD-21.',
        'Audio evidence was accepted by interviewees as a trade-off for proof in front of authorities, while the high-school student considered video a privacy breach. This supports audio-only recording in MOD-18 and the exclusion of video recording.',
        '13% of the survey respondents named the risk of being forced to share their location as a barrier. This supports the consent rules of MOD-04 and MOD-05.',
        'An interviewee said that trust in how applications handle personal data is a concern. This supports on-device processing, the consent flow of MOD-15 and the child-data rules of MOD-17.',
        'A male university student asked for directions to the nearest safe location that work offline. This, with the survey item, is the source of MOD-20.',
        'One survey respondent suggested disguising the application by changing its icon and name. This is the source of MOD-21.',
        'Automatic detection received the lowest stated interest (55%), and only 6% chose it as the single most important feature. It is therefore designed as an assistance that always asks for confirmation (the 20-second cancel step), with manual SOS as the primary path.',
    ]))
    b.append(P('**Stakeholders.** The stakeholders are the Primary Users and Guardians for whom the system is built, the family circle members and trustees who receive its information, the verified helpers and administrators who operate its community functions, the emergency services that receive escalation messages, the supervisor, who guides and approves the work, the evaluation committee, and the two developers. Their interests are reflected in the user classes of Section {sec:users}.'))
    b.append(P('**Prioritization.** Requirements are prioritized High, Medium or Low. A module is High when it is on the critical path of getting an alert out or protects the user from coercion, so that without it the purpose of the product fails. A module is Medium when it adds significant value but the core alert still works without it. A module is Low when it is an enhancement. The ranking considered the survey interest in {tbl:survey2}, the dependencies between modules, and the technical risk. A requirement inherits the priority of its module in {tbl:priority} unless Section {sec:frcat} states otherwise.'))
    prio = [
        ['High', 'MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06, MOD-12, MOD-13, MOD-14, MOD-15', 'Core alert path, offline delivery, identity and consent, and the duress-protection features that distinguish the product.'],
        ['Medium', 'MOD-07, MOD-08, MOD-09, MOD-10, MOD-11, MOD-16, MOD-17, MOD-18, MOD-19', 'Community, information and follow-through features; the admin dashboard is needed to moderate MOD-07, MOD-08 and MOD-17.'],
        ['Low', 'MOD-20, MOD-21', 'Enhancements that depend on other modules (the directory and the settings).'],
    ]
    b.append(TBL('priority', 'Module priorities', ['Priority', 'Modules', 'Basis'], prio, [0.9, 3.4, 3.6]))
    b.append(P('**Validation.** Requirements are written to be unique, clear, feasible, testable and traceable {cite:iso29148}. Each functional requirement carries acceptance criteria that are verified by the test cases of Chapter 6, and each requirement is traced to its source, design element and test in the traceability matrix. The specification is reviewed by the supervisor and the evaluation committee, and the screen designs of Section {sec:hmi} are used to confirm user-interface flows. {tbl:techniques} summarizes the techniques.'))
    b.append(TBL('techniques', 'Requirement identification techniques', ['Technique', 'Stakeholders or Source', 'Purpose', 'Evidence or Output'], [
        ['Document analysis', 'Approved project scope document; feature document', 'Define modules and sub-modules', 'Modules MOD-01 to MOD-21 (Section {sec:modules})'],
        ['Review of existing systems', 'Publicly available safety applications and national helplines', 'Identify what exists and the gaps', 'Product perspective (Section {sec:perspective})'],
        ['Questionnaire survey', 'Survey respondents (73 responses)', 'Measure current practice, barriers and interest by feature', '{tbl:survey1} and {tbl:survey2}'],
        ['Semi-structured interviews', 'High-school student, working woman, MBBS student, male university student', 'Explore reactions, privacy concerns and missing features', 'Requirements decisions listed above; MOD-20 and MOD-21'],
        ['Use cases', 'Project team and supervisor', 'Describe actor and system interaction', 'Chapter 3 and Appendices A and B'],
        ['Event-response tables', 'Project team', 'Specify background behaviour of detection, delivery and escalation', 'Section {sec:models}'],
        ['Storyboarding and prototyping', 'Project team; users', 'Confirm screen flows', 'Screen designs, Section {sec:hmi}'],
        ['Prioritization (High, Medium, Low)', 'Project team and supervisor', 'Order the work', '{tbl:priority}'],
    ], [1.5, 2.2, 2.2, 1.9]))

    b.append(H2('Chapter Summary', 'ch2sum'))
    b.append(P('This chapter described Muhaffiz as a new product made of an Android application, a Firebase backend and an admin website, and showed its interfaces in a context diagram. It identified seven user classes, fixed the operating environment, listed twelve constraints, nine assumptions and seven dependencies, and explained how requirements were elicited from documents, a survey and interviews, prioritized and validated. Chapter 3 now specifies the requirements in detail.'))
    return b
