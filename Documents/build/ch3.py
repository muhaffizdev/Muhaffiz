import re
from srslib import *
import fr_common, fr_data1, fr_data2, fr_data3, figs_uc2
from fr_common import FRS, MODNAME
import ch3_data as D

def expand_br(txt):
    out = set()
    for m in re.finditer(r'BR-(\d\d)(?: to BR-(\d\d))?', txt):
        a = int(m.group(1)); z = int(m.group(2) or a)
        out |= {'BR-%02d' % i for i in range(a, z + 1)}
    return out

def fr_spec_table(f):
    req = ''
    if f['u']: req += '**User perspective:** %s\n' % f['u']
    req += '**System perspective:** %s' % f['s']
    rows = [
        ['Identifier', f['id']],
        ['Title', f['title']],
        ['Requirement', req],
        ['Source', f['src']],
        ['Rationale', f['why']],
        ['Business Rule', f['br']],
        ['Dependencies', f['dep']],
        ['Priority', f['pri']],
        ['Acceptance Criteria', '\n'.join('• ' + a for a in f['acc'])],
    ]
    return TBL('fr_' + f['id'].replace('.', '_').replace('-', ''), 'Specification of %s: %s' % (f['id'], f['title']),
               ['Attribute', 'Required Information'], rows, [1.3, 6.1], fs=17)

def uc_spec_table(uid):
    name, actors, mod, frs, br = next((u[1], u[2], u[3], u[4], u[5]) for u in D.UCS if u[0] == uid)
    sp = D.UC_SPECS[uid]
    rows = [
        ['Use Case ID', uid], ['Use Case Name', name], ['Actors', actors], ['Description', sp['desc']], ['Trigger', sp['trigger']],
        ['Preconditions', sp['pre']], ['Postconditions', sp['post']],
        ['Normal Flow', '\n'.join('%d. %s' % (i + 1, t) for i, t in enumerate(sp['flow']))],
        ['Alternative Flows', sp['alt']], ['Exceptions', sp['exc']], ['Business Rules', sp['br']], ['Assumptions', sp['ass']],
    ]
    return TBL('uc_' + uid.replace('-', '').lower(), 'Use case specification %s: %s' % (uid, name), ['Field', 'Description'], rows, [1.3, 6.1], fs=17)

def blocks(ctx):
    figs = figs_uc2.make_all()
    b = []
    b.append(H1('Software Requirements Specification', 'ch3'))
    b.append(P('**Chapter Overview.** This chapter specifies what Muhaffiz shall do. Section {sec:frcat} lists the functional requirements, Section {sec:frspec} specifies each of them and gives the use cases, Section {sec:br} states the business rules, Section {sec:nfr} gives the non-functional requirements and Section {sec:ifc} specifies the external interfaces. Every requirement has a unique identifier, is written with "shall", and has acceptance criteria that can be tested.'))

    # ------------------------------------------------------------ 3.1
    b.append(H2('Functional Requirement Catalogue', 'frcat'))
    b.append(P('The functional requirements are organized by module. The identifier FR-mm.nn names module mm and the requirement nn within it; the requirements of MOD-01 to MOD-19 follow the numbering of the sub-modules 7.1.1 to 7.19.6 of the feature document, so that each can be traced to it. There are %d functional requirements. A requirement has the priority of its module in Section {sec:elicit} unless {tbl:frcatalogue} states otherwise.' % len(FRS)))
    rows = [[f['id'], 'MOD-%02d' % f['mod'], f['title'], f['pri'], f['dep']] for f in FRS]
    b.append(TBL('frcatalogue', 'Functional requirement catalogue', ['FR ID', 'Feature or Module', 'Requirement Title', 'Priority', 'Dependencies'], rows, [0.9, 0.9, 2.5, 0.8, 2.3], fs=17))

    # ------------------------------------------------------------ 3.2
    b.append(H2('Functional Requirement Specification', 'frspec'))
    b.append(P('Each functional requirement is specified in a table with the attributes required by the template. The requirement is stated from the user perspective, where a user acts, and from the system perspective, as the response of the system to a trigger. Valid input, invalid input and error conditions are covered by the system perspective and the acceptance criteria. The acceptance criteria are the conditions that the test cases of Chapter 6 verify.'))
    for m in range(1, 22):
        b.append(H3('MOD-%02d %s' % (m, MODNAME[m]), 'mod%d' % m))
        for f in [x for x in FRS if x['mod'] == m]:
            b.append(fr_spec_table(f))
    b.append(H3('Use case Specification', 'ucspec'))
    b.append(P('The use cases describe the interaction between actors and the system. {fig:uc_alert}, {fig:uc_family}, {fig:uc_community} and {fig:uc_admin} show the use-case diagrams, grouped by function. Actors are linked to the use cases they take part in. An include relationship shows that a use case reuses the steps of another (UC-02 and UC-03 reuse the dispatch steps of UC-01, and UC-28 reuses the sign-in steps of UC-19), and an extend relationship shows an optional continuation (UC-25 extends UC-01 when nobody responds within 3 minutes). {tbl:uclist} lists all %d use cases with their modules, related requirements and business rules. The six use cases that are on the critical path of an alert or that involve a child\'s data are specified in this section; the others are specified in Appendix B.' % len(D.UCS)))
    for key, cap in (('uc_alert', 'Use-case diagram: emergency alerting'), ('uc_family', 'Use-case diagram: family network and disguise'),
                     ('uc_community', 'Use-case diagram: community, library and directory'), ('uc_admin', 'Use-case diagram: account, consent and administration')):
        svg, png = figs[key]
        b.append(FIG(key, cap, svg=svg, png=png, width_in=5.3 if key != 'uc_alert' else 5.2))
    b.append(TBL('uclist', 'Use case list', ['Use Case ID', 'Use Case Name', 'Actors', 'Module', 'Related FRs', 'Business Rules'],
                 [[u[0], u[1], u[2], u[3], u[4], u[5]] for u in D.UCS], [0.8, 1.7, 1.6, 0.7, 1.5, 1.1], fs=16))
    for uid in D.IN_CHAPTER_UCS:
        b.append(uc_spec_table(uid))

    # ------------------------------------------------------------ 3.3
    b.append(H2('Business Rules', 'br'))
    b.append(P('The business rules in {tbl:brs} are the policies, limits and constraints that govern the behaviour of the functional requirements. A functional requirement or use case refers to a rule by its identifier.'))
    br_fr = {}
    for f in FRS:
        for r in expand_br(f['br']): br_fr.setdefault(r, []).append(f['id'])
    br_uc = {}
    for u in D.UCS:
        for r in expand_br(u[5]): br_uc.setdefault(r, []).append(u[0])
    for uid, sp in D.UC_SPECS.items():
        for r in expand_br(sp['br']): br_uc.setdefault(r, [])
        for r in expand_br(sp['br']):
            if uid not in br_uc[r]: br_uc[r].append(uid)
    rows = []
    for bid, rule, why, pri in D.BRS:
        rel = ', '.join(br_fr.get(bid, [])) + ('; ' + ', '.join(sorted(br_uc.get(bid, []))) if br_uc.get(bid) else '')
        rows.append([bid, rule, why, rel, pri])
    b.append(TBL('brs', 'Business rules', ['BR ID', 'Business Rule', 'Source or Rationale', 'Related FR or UC', 'Priority'], rows, [0.7, 3.0, 1.5, 2.1, 0.7], fs=16))

    # ------------------------------------------------------------ 3.4
    b.append(H2('Non-Functional Requirements', 'nfr'))
    b.append(P('The non-functional requirements are specific, quantitative and verifiable. Each has a measurable target and a verification method, and each target is a requirement that Chapter 6 verifies on the reference device and under the stated conditions. They are grouped by quality: reliability, performance, security, privacy, usability, and maintainability with other qualities (compatibility, availability, scalability, safety and robustness).'))
    for cat, rows in D.NFRS.items():
        b.append(TBL('nfr_' + re.sub(r'\W+', '', cat)[:8].lower(), 'Non-functional requirements: ' + cat, ['ID', 'Requirement', 'Measurement or Target', 'Verification Method'],
                     [list(r) for r in rows], [0.9, 2.7, 2.6, 1.6], fs=16))

    # ------------------------------------------------------------ 3.5
    b.append(H2('External Interface Requirements', 'ifc'))
    b.append(P('This section specifies how Muhaffiz communicates with its users and with external software, hardware and communication services. {tbl:ifctable} summarizes the interfaces.'))
    b.append(H3('User Interface Requirements', 'uireq'))
    b.append(BUL([
        'UI-1: The application shall follow Material Design 3 as provided by Flutter, with one colour scheme of dark teal, navy and mint used on all screens.',
        'UI-2: The application shall use the system sans-serif font at 14 sp or larger for body text, the Material icon set, and verb labels on buttons.',
        'UI-3: The application shall be designed for portrait orientation on phone screens from 320 dp wide. The home screen shall show the SOS control, the loud or silent toggle and a status strip with the connectivity tier and the state of detection and voice activation.',
        'UI-4: The application shall provide bottom navigation with Home, Family, Map, Library and More. Help, settings and the privacy summary shall be reachable from More.',
        'UI-5: Every control shall have a content description, and the focus order shall follow the reading order, so that a screen reader can be used.',
        'UI-6: Success messages shall appear as brief messages, errors shall appear next to the field with the next step, and notifications shall use separate Android channels for status, alerts and reminders. In a silent SOS the notification wording shall be neutral.',
        'UI-7: The interface language shall be English, and dates and times shall follow the device locale.',
        'UI-8: Information shall not be conveyed by colour alone; the heatmap shall have a legend with numeric ranges.',
        'UI-9: The screen designs in Section {sec:hmi} are the committed designs of the key screens; other screens follow the same components.',
        'UI-10: The admin website shall be usable on screens 1024 px wide or wider and shall present lists as filterable tables.',
    ]))
    b.append(H3('Software Interfaces', 'swif'))
    b.append(BUL([
        'SI-1: The application and the admin website shall use Firebase Authentication for phone sign-in of users and email-and-password sign-in of administrators.',
        'SI-2: The application shall use Cloud Firestore with offline persistence for circles, locations, reports, helper status and acknowledgements.',
        'SI-3: The system shall use Firebase Cloud Messaging to deliver push notifications to trustees and helpers.',
        'SI-4: The system shall use Cloud Storage for identity images and child photos, protected by storage rules.',
        'SI-5: The system shall use Cloud Functions, called over HTTPS, for email dispatch, the acknowledgement endpoint, heatmap aggregation and scheduled expiry.',
        'SI-6: The application shall use the Google Maps SDK for Android for online maps.',
        'SI-7: The application shall load offline map data for up to three areas from an open map-data source that permits offline storage.',
        'SI-8: The application shall send SMS through the Android SMS manager, called through a platform channel.',
        'SI-9: The application shall prepare WhatsApp messages with the WhatsApp share link through an Android intent.',
        'SI-10: The application shall use the Android Keystore for the evidence encryption key.',
        'SI-11: The application shall run its sound-classification, keyword-spotting and sentence-embedding models with TensorFlow Lite or an equivalent on-device runtime.',
        'SI-12: The application shall use Android WorkManager to retry the outbound queue.',
        'SI-13: The application shall use SQLite as its on-device database.',
        'SI-14: The backend shall call an email delivery service from Cloud Functions.',
    ]))
    b.append(H3('Hardware Interfaces', 'hwif'))
    b.append(BUL([
        'HI-1: The application shall read the microphone as 16 kHz mono audio for detection, voice activation and evidence recording. If the microphone is in use by another application, the affected function shall pause and resume when it is free.',
        'HI-2: The application shall read the accelerometer and gyroscope at 50 Hz or faster during a detection window.',
        'HI-3: The application shall obtain location from the fused location provider (GPS and network).',
        'HI-4: The application shall drive the vibration motor for the 20-second countdown and the 30-second warning.',
        'HI-5: The application shall play the siren through the alarm audio stream of the speaker.',
        'HI-6: The application shall use the telephony hardware to send SMS and place calls.',
        'HI-7: The application shall read the magnetometer, when present, to show compass direction offline.',
        'HI-8: The application shall read photos chosen by the user from the camera or gallery for the helper identity image and the child photo.',
    ]))
    b.append(H3('Communications Interfaces', 'comif'))
    b.append(BUL([
        'CI-1: SOS and escalation messages shall be sent as SMS over the cellular network, in as many message parts as the text needs.',
        'CI-2: Push notifications shall be delivered through Firebase Cloud Messaging.',
        'CI-3: Email alerts shall be sent from Cloud Functions through the email service.',
        'CI-4: WhatsApp messages shall be prepared as a share link for the WhatsApp application.',
        'CI-5: All data between the application, the admin website and the backend shall use HTTPS with TLS 1.2 or later; real-time updates shall use the Firestore real-time channel.',
        'CI-6: Calls shall be placed through the Android dialer.',
        'CI-7: A trustee without the application shall be able to acknowledge an alert through a web page served by Firebase Hosting and linked from the message.',
    ]))
    b.append(TBL('ifctable', 'Summary of external interfaces', ['Interface ID', 'Interface Type', 'External Element', 'Data or Interaction', 'Protocol or Standard', 'Error Handling'], [
        ['SI-1', 'Software', 'Firebase Authentication', 'One-time code sign-in; administrator sign-in', 'HTTPS / Firebase SDK', 'Wrong code rejected; lock after five attempts; offline use of safety functions continues.'],
        ['SI-2', 'Software', 'Cloud Firestore', 'Circles, locations, reports, helper status, acknowledgements', 'Firestore SDK (real-time)', 'Local cache used offline; writes retried on reconnection.'],
        ['SI-3', 'Software', 'Firebase Cloud Messaging', 'Push alerts and help requests', 'FCM over HTTPS', 'Failure logged; other channels continue.'],
        ['SI-4', 'Software', 'Cloud Storage', 'Identity images, child photos', 'HTTPS / Storage SDK', 'Upload retried; deletion confirmed.'],
        ['SI-5', 'Software', 'Cloud Functions', 'Email dispatch, acknowledgement, scheduled jobs', 'HTTPS callable', 'Errors logged and visible in health monitoring.'],
        ['SI-6', 'Software', 'Google Maps SDK', 'Map display, overlays', 'Maps SDK for Android', 'Offline: last data or offline map shown.'],
        ['SI-8', 'Software', 'Android SMS manager', 'SOS and escalation SMS', 'Android API', 'Missing permission prompts; failure queued and retried.'],
        ['SI-9', 'Software', 'WhatsApp', 'Prepared message', 'Share link / intent', 'Application missing: channel skipped.'],
        ['HI-1', 'Hardware', 'Microphone', 'Audio frames for detection, voice, evidence', '16 kHz mono PCM', 'In use elsewhere: pause and resume.'],
        ['HI-2', 'Hardware', 'Accelerometer, gyroscope', 'Motion window', '50 Hz or faster', 'Sensor missing: audio-only rule applies.'],
        ['HI-3', 'Hardware', 'Location provider', 'Position fixes', 'Fused location', 'No fix: cached location used.'],
        ['HI-6', 'Hardware', 'Telephony', 'SMS and calls', 'GSM SMS, voice', 'No signal: queued and retried.'],
        ['CI-3', 'Communication', 'Email service', 'Email alerts', 'HTTPS API', 'Failure logged; other channels continue.'],
        ['CI-7', 'Communication', 'Acknowledgement page', 'Trustee acknowledgement', 'HTTPS (Firebase Hosting)', 'Link opened offline: acknowledgement not recorded.'],
    ], [0.7, 0.9, 1.4, 1.8, 1.4, 2.0], fs=16))

    b.append(H2('Chapter Summary', 'ch3sum'))
    b.append(P('This chapter specified Muhaffiz through %d functional requirements, %d use cases, %d business rules, %d non-functional requirements and the external interface requirements. Each functional requirement has a source, rationale, business rule, dependencies, priority and acceptance criteria. Chapter 4 now translates these requirements into the design of the system.' % (len(FRS), len(D.UCS), len(D.BRS), sum(len(v) for v in D.NFRS.values()))))
    return b
