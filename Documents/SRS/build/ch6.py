import re
from srslib import *
import fr_common, fr_data1, fr_data2, fr_data3
from fr_common import FRS, MODNAME
import ch3_data as D
import ch6_data as T

IMPL = {1: 'sos_core', 2: 'detection_engine, trigger_engine', 3: 'voice_engine', 4: 'family_circle', 5: 'location_sharing', 6: 'decoy_mode', 7: 'heatmap, scheduled functions',
        8: 'near_help', 9: 'library', 10: 'semantic_search', 11: 'directory', 12: 'delivery_manager, sms_gateway', 13: 'offline_store', 14: 'auth', 15: 'consent',
        16: 'admin_site', 17: 'missing_child', 18: 'evidence_vault', 19: 'escalation', 20: 'safe_navigation', 21: 'app_disguise'}
DESIGN = {1: 'Class diagram SOS core; sequence SOS dispatch', 2: 'Class diagram detection; sequence automatic detection; algorithms A1, A2', 3: 'Class diagram detection; algorithm A5',
          4: 'Class diagram family; state diagram member', 5: 'Sequence stop sharing; state diagram member; algorithm A6', 6: 'Algorithm A5; activity SOS pipeline',
          7: 'Class diagram community; algorithm A7', 8: 'Class diagram community; state diagram helper', 9: 'Data design: LibraryItem', 10: 'Algorithm A8; data design: LibraryItem',
          11: 'Data design: DirectoryEntry', 12: 'Activity tiered delivery; sequence offline queue; algorithm A4', 13: 'Data design: device entities', 14: 'Architecture; security design SD-03',
          15: 'Class diagram detection: ConsentSettings', 16: 'Architecture; security design SD-02', 17: 'State diagram child report; data design', 18: 'Class diagram SOS core: EvidenceRecording; SD-04',
          19: 'Sequence escalation; algorithm A9', 20: 'Algorithm A10', 21: 'Architecture; component diagram'}

def expand_frs(txt):
    out = []
    for m in re.finditer(r'FR-(\d\d)\.(\d\d)(?: to FR-(\d\d)\.(\d\d))?', txt):
        a, n1 = int(m.group(1)), int(m.group(2))
        if m.group(3):
            z, n2 = int(m.group(3)), int(m.group(4))
            for f in FRS:
                if (f['mod'], f['n']) >= (a, n1) and (f['mod'], f['n']) <= (z, n2): out.append(f['id'])
        else: out.append('FR-%02d.%02d' % (a, n1))
    return out

def blank_rows(rows, nblank):
    return [r + [''] * nblank for r in rows]

def blocks(ctx):
    b = []
    b.append(H1('Testing, Evaluation and Conclusion', 'ch6'))
    nf = [(nid, req, tgt, ver) for cat in D.NFRS.values() for (nid, req, tgt, ver) in cat]
    b.append(P('**Chapter Overview.** This chapter defines how the system is verified against its requirements. Sections {sec:unit} to {sec:nft} give the test cases at each level, Section {sec:summary} the test summary and defect log, Section {sec:rtm} the requirements traceability matrix, and Section {sec:conclusion} the conclusion, limitations and future enhancements. Every functional requirement, business rule and non-functional requirement is covered by at least one test case, and the matrix shows which. The columns Actual Result, Observed Result and Result of each table record the outcome of the execution of the test case; a hyphen in these columns means that the test case has not yet been executed.'))
    b.append(P('Tests are executed in the testing environment of Section {sec:deploy}. Where users or helpers are needed for a test, simulated accounts are used and are identified as simulated in the test log. The reference device is a mid-range Android phone running Android 8.0 or later, and its model is recorded in the test log. Timing and battery targets are measured on the reference device.'))

    b.append(H2('Unit Testing', 'unit'))
    b.append(P('Unit tests check individual functions, classes and algorithms with fixed inputs. {tbl:ut} lists test cases UT-01 to UT-%02d.' % len(T.UT)))
    b.append(TBL('ut', 'Unit test cases', ['No.', 'Test Case or Script', 'Input Attribute and Value', 'Expected Result', 'Actual Result', 'Result'],
                 [[u[0], u[1], u[2], u[3], '-', '-'] for u in T.UT], [0.7, 1.5, 2.1, 2.3, 0.8, 0.75], fs=16))

    b.append(H2('Functional Testing', 'func'))
    b.append(P('Each use case is tested through the interface after unit testing. {tbl:ft} lists test cases FT-01 to FT-%02d; the number of a functional test equals the number of its use case.' % len(T.FT)))
    b.append(TBL('ft', 'Functional test cases', ['No.', 'Test Case or Script', 'Input Attribute and Value', 'Expected Result', 'Actual Result', 'Result'],
                 [[f[0], f[1], f[2], f[3], '-', '-'] for f in T.FT], [0.7, 1.4, 2.2, 2.3, 0.8, 0.75], fs=16))

    b.append(H2('Business Rules Testing', 'brtest'))
    b.append(P('The business rules are tested with decision tables: each row gives the conditions of one case of the rule and the expected action. {tbl:brt} lists test cases BRT-01 to BRT-%02d, one for each business rule BR-01 to BR-%02d (the prefix BRT distinguishes a test case from the rule it tests).' % (len(T.BRT), len(T.BRT))))
    rows = []
    for k in range(1, len(T.BRT) + 1):
        cond, act = T.BRT['BR-%02d' % k]
        rows.append(['BRT-%02d' % k, 'BR-%02d' % k, cond, act, '-', '-'])
    b.append(TBL('brt', 'Business rule test cases', ['BR Test ID', 'Related BR', 'Conditions', 'Expected Action', 'Actual Action', 'Result'], rows, [0.8, 0.7, 2.5, 2.3, 0.9, 0.75], fs=16))

    b.append(H2('Integration Testing', 'integ'))
    b.append(P('Integration tests check that modules, services, the database and external systems work together and that the interfaces between them behave as specified. {tbl:it} lists test cases IT-01 to IT-%02d.' % len(T.IT)))
    b.append(TBL('it', 'Integration test cases', ['No.', 'Integrated Component', 'Test Scenario', 'Expected Result', 'Actual Result', 'Result'],
                 [[i[0], i[1], i[2], i[3], '-', '-'] for i in T.IT], [0.7, 1.5, 2.1, 2.3, 0.8, 0.75], fs=16))

    b.append(H2('Non-Functional Testing', 'nft'))
    b.append(P('Each measurable non-functional requirement is verified under the stated environment and workload. {tbl:nf} lists test cases NF-01 to NF-%02d, one for each requirement of Section {sec:nfr}.' % len(nf)))
    rows = [['NF-%02d' % (i + 1), n[0], n[3] + ' (reference device)', n[2], '-', '-'] for i, n in enumerate(nf)]
    b.append(TBL('nf', 'Non-functional test cases', ['NF Test ID', 'Related NFR', 'Method and Environment', 'Target', 'Observed Result', 'Status'], rows, [0.7, 0.9, 1.8, 2.65, 0.9, 0.75], fs=15))

    b.append(H2('Test Summary and Defect Log', 'summary'))
    counts = [('Unit', len(T.UT)), ('Functional', len(T.FT)), ('Business rules', len(T.BRT)), ('Integration', len(T.IT)), ('Non-functional', len(nf))]
    tot = sum(c for _, c in counts)
    rows = [[n, str(c), '0', '0', '0', '0', '-'] for n, c in counts] + [['Total', str(tot), '0', '0', '0', '0', '-']]
    b.append(P('{tbl:summary} summarizes the test cases by type, and {tbl:defects} is the defect log.'))
    b.append(TBL('summary', 'Test summary', ['Test Type', 'Planned', 'Executed', 'Passed', 'Failed', 'Blocked', 'Pass Rate'], rows, [1.6, 0.8, 0.9, 0.8, 0.8, 0.8, 0.9], fs=17))
    b.append(TBL('defects', 'Defect log', ['Defect ID', 'Description', 'Severity', 'Related Test', 'Status', 'Resolution or Rationale'], [['', '', '', '', '', ''] for _ in range(4)], [0.8, 2.6, 0.8, 1.0, 0.8, 2.0], fs=17))

    b.append(H2('Requirements Traceability Matrix', 'rtm'))
    b.append(P('The matrix in {tbl:rtm} traces every functional requirement, business rule and non-functional requirement from its source to the design element, the implementation component and the test cases that verify it. A functional requirement is traced to the functional tests of the use cases that contain it, and to the unit and integration tests that name it. The Status column records the verification status of each requirement.'))
    ft_of = {}
    for u in D.UCS:
        for fid in expand_frs(u[4]): ft_of.setdefault(fid, []).append('FT-%02d' % int(u[0][3:]))
    for t in T.UT:
        for fid in t[4]: ft_of.setdefault(fid, []).append(t[0])
    for t in T.IT:
        for fid in t[4]: ft_of.setdefault(fid, []).append(t[0])
    missing = [f['id'] for f in FRS if f['id'] not in ft_of]
    assert not missing, missing
    rows = []
    for f in FRS:
        rows.append([f['id'], f['src'].split(';')[0], DESIGN[f['mod']], IMPL[f['mod']], ', '.join(sorted(set(ft_of[f['id']]))), ''])
    br_first = {}
    for f in FRS:
        for r in re.findall(r'BR-\d\d', f['br']): br_first.setdefault(r, f['mod'])
    for bid, rule, why, pri in D.BRS:
        m = br_first.get(bid, 1)
        rows.append([bid, 'Business rule: ' + why.rstrip('.'), DESIGN[m], IMPL[m], 'BRT-%02d' % int(bid[3:]), ''])
    nfdesign = {'REL': 'Security design SD-08, SD-09, SD-16', 'PER': 'Algorithms A1 to A10; architecture', 'SEC': 'Security design SD-01 to SD-07', 'PRV': 'Security design SD-05; data design',
                'USA': 'Human interface design', 'MNT': 'Component diagram; configuration', 'CMP': 'Architecture', 'AVL': 'Activity tiered delivery', 'SCL': 'Deployment view', 'SAF': 'Algorithm A3; state diagram SOS', 'ROB': 'Security design SD-06, SD-14, SD-15'}
    for i, n in enumerate(nf):
        rows.append([n[0], 'Non-functional requirements of Chapter 3', nfdesign[n[0].split('-')[1]], 'Cross-cutting', 'NF-%02d' % (i + 1), ''])
    b.append(TBL('rtm', 'Requirements traceability matrix', ['Requirement ID', 'Source', 'Design Element', 'Implementation Component', 'Test Case ID', 'Status'], rows, [0.9, 1.9, 2.1, 1.3, 1.4, 0.6], fs=14))

    b.append(H2('Conclusion, Limitations and Future Enhancements', 'conclusion'))
    b.append(P('**Conclusion.** Muhaffiz brings together in one Android application the functions that a person needs before, during and after an unsafe event: a manual, automatic and voice-triggered SOS through one shared pipeline; delivery that does not depend on a data connection; a family location model that the tracked person controls; a community danger map and verified nearby help; an offline library with search by meaning; evidence recording, escalation and a missing-child report; and an administration website. The six objectives of the project are realized by the following modules: the unified trigger engine and its countdown (BO-1) by MOD-01 to MOD-03; the three-tier delivery (BO-2) by MOD-12 and MOD-13; the bilateral opt-in and unilateral opt-out family model (BO-3) by MOD-04 and MOD-05; on-device detection and voice activation with no audio leaving the phone (BO-4) by MOD-02 and MOD-03; on-device semantic search (BO-5) by MOD-10; and the integrated application (BO-6) by all modules. The requirements, design and tests in this document are traced to one another so that each claim can be checked.'))
    b.append(P('**Limitations.** The following limitations apply.'))
    b.append(BUL([
        'The application runs on Android only.',
        'The sound classifier and the keyword spotter are pre-trained models; their accuracy bounds the accuracy of automatic and voice triggers, and accented speech may reduce it.',
        'WhatsApp messages need the user\'s confirmation, so SMS, push and email are the automatic channels.',
        'SMS needs cellular coverage, and the other channels need a data connection.',
        'Near Help is useful only where verified helpers are present, and its evaluation uses simulated helpers.',
        'Android may stop background services to save battery; the application asks for an exemption but cannot enforce it.',
        'Android 11 and later shows a microphone indicator that an application cannot hide, so evidence recording may be visible during a silent SOS.',
        'Consent based on a switch or a phrase can be defeated by physical coercion; the design reduces but does not remove this risk.',
        'Escalation messages go to numbers that the user configures; the application cannot ensure that an authority receives, accepts or acts on them, and it has no direct integration with official systems.',
        'Offline maps are available for up to three areas, and offline guidance gives distance and direction, not turn-by-turn directions.',
        'Semantic search covers the library only, and the interface is in English.',
    ]))
    b.append(P('**Future enhancements.** The following work is possible after this project: an iOS version; Urdu and other languages for the interface and the phrases; fine-tuning the sound and keyword models on locally collected data; direct integration with official emergency and missing-child systems where they offer one; support for wearables and hardware panic buttons; offline turn-by-turn routing; larger offline map coverage; accessibility improvements for users with visual or hearing impairments; and semantic search across incident reports.'))
    b.append(H2('Chapter Summary', 'ch6sum'))
    b.append(P('This chapter defined %d unit, %d functional, %d business-rule, %d integration and %d non-functional test cases, the test summary and defect log, and a traceability matrix that links every requirement to its design, implementation and tests. It closed with the conclusion, the limitations and the future enhancements of Muhaffiz.' % (len(T.UT), len(T.FT), len(T.BRT), len(T.IT), len(nf))))
    return b
