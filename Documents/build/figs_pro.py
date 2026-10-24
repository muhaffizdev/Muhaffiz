import os
from diag3 import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)
def P(n): return os.path.join(OUT, n + '.svg'), os.path.join(OUT, n + '.png')

def fit_row(c, x0, w, y, h, items, fill, stroke, size=10.2, gap=8):
    tot = sum(wd for _, wd in items) + gap * (len(items) - 1)
    k = min(1.0, (w - 24) / tot)
    x = x0 + (w - tot * k) / 2; out = []
    for lab, wd in items:
        out.append(c.node(x, y, wd * k, h, lab, fill=fill, stroke=stroke, size=size)); x += wd * k + gap * k
    return out

def architecture():
    c = Canvas(910, 1040)
    c.panel(20, 20, 770, 540, 'Android application (Flutter, on-device layer)', 'teal', size=14)
    spec = [
        (60, 'Presentation layer', 'blue', [('Screens and widgets\n(Home, Family, Map, Library, More)', 250), ('Navigation and\nbottom bar', 130), ('State providers\n(Riverpod)', 130), ('Theme and\nstrings', 100)]),
        (148, 'Application layer', 'blue', [('Trigger\nEngine', 100), ('SOS\nOrchestrator', 110), ('Delivery\nManager', 100), ('Escalation\nManager', 104), ('Sharing\nManager', 100), ('Consent\nManager', 100)]),
        (236, 'Domain and data layer (local storage on the device)', 'amber', [('Local repositories\n(SQLite, Drift)', 160), ('Evidence vault\n(AES-256-GCM)', 150), ('Location\ncache', 100), ('Remote repositories\n(Firestore, Storage)', 170)]),
        (324, 'On-device intelligence', 'blue', [('Sound classifier\n(TensorFlow Lite)', 190), ('Keyword spotter\n(offline)', 170), ('Sentence embedder\n(library search)', 190)]),
    ]
    rem = None
    for y, t, kind, items in spec:
        c.panel(40, y, 730, 76, t, kind, hh=20, size=12, fill='#fff' if kind == 'blue' else '#FFFBF0')
        row = fit_row(c, 40, 730, y + 26, 44, items, LBLUE if kind == 'blue' else LAMBER, BLUE if kind == 'blue' else AMBER, size=11.4)
        if t.startswith('Domain'): rem = row[3]
    for y in (136, 224, 312, 400):
        c.conn([(405, y), (405, y + 12)])
    for lab, y in (('events, state', 142), ('domain calls', 230), ('inference requests', 318), ('device capabilities', 406)):
        c.text(425, y, lab, 10.5, anchor='start', italic=True, fill=GREY)
    c.panel(40, 412, 730, 132, 'Platform layer (Kotlin, platform channels)', 'blue', hh=20, size=12, fill='#fff')
    fit_row(c, 40, 730, 438, 44, [('Foreground\nservices', 110), ('Audio and\nmotion sensors', 120), ('Fused\nlocation', 100), ('Android\nKeystore', 100), ('WorkManager', 110), ('Launcher\naliases', 100)], LBLUE, BLUE, size=11.4)
    bottoms = []
    for lab, cxx in (('SMS manager', 120), ('Share intent\n(WhatsApp)', 290), ('Online map\n(Google Maps SDK)', 460), ('Offline map\nrenderer', 630)):
        bottoms.append(c.node(cxx - 70, 490, 140, 46, lab, fill=LBLUE, stroke=BLUE, size=11.4))
    ext = {}
    for lab, cxx in (('Cellular\nSMS network', 120), ('WhatsApp', 290), ('Google Maps\nPlatform', 460), ('Open map-data\nsource', 630)):
        ext[lab] = c.node(cxx - 70, 596, 140, 50, lab, fill=LAMBER, stroke=AMBER, size=11.4)
    for b, lab, e, d in ((bottoms[0], 'SMS', ext['Cellular\nSMS network'], False), (bottoms[1], 'share link', ext['WhatsApp'], False), (bottoms[2], 'map tiles', ext['Google Maps\nPlatform'], False), (bottoms[3], 'region download', ext['Open map-data\nsource'], True)):
        c.conn([bottom(b), top(e)], lab, loff=(34 if len(lab) < 6 else 46, 0), dashed=d, size=10.8)
    # backend and web
    c.panel(20, 706, 300, 120, 'Web front ends', 'teal', size=13)
    c.node(36, 740, 268, 34, ['Admin website  muhaffiz.me', '(Flutter web)'], fill=LTEAL, stroke=TEAL, size=11)
    c.node(36, 782, 268, 34, ['Alert page for trustees', '(Firebase Hosting)'], fill=LTEAL, stroke=TEAL, size=11)
    c.panel(340, 706, 450, 220, 'Firebase backend', 'teal', size=14)
    svc = [('Authentication', 'phone and email sign-in'), ('Cloud Firestore', 'data, listeners, rules'), ('Cloud Messaging', 'push notifications'), ('Cloud Storage', 'photos, identity images'), ('Cloud Functions', 'email, acknowledgements, jobs'), ('Hosting', 'muhaffiz.me, alert page')]
    sn = []
    for k, (a, b) in enumerate(svc):
        r, m = divmod(k, 2)
        sn.append(c.node(354 + m * 220, 744 + r * 58, 206, 50, [a, b], fill=LTEAL, stroke=TEAL, size=11, bold_first=True))
    emailb = c.node(354, 960, 206, 46, 'Email service', fill=LAMBER, stroke=AMBER, size=11.5)
    c.conn([right(rem), (815, rem[1] + 22), (815, sn[1][1] + 25), right(sn[1])], 'HTTPS, real-time', both=True, lpos=0.62, loff=(-0, 0), size=10.8)
    c.conn([(320, 766), (340, 766)], '', both=True)
    c.conn([bottom(sn[4]), (bottom(sn[4])[0], 960)], 'email', loff=(26, 0), size=10.8)
    c.node(20, 850, 300, 90, '', fill='#fff', stroke='#9aa9bd')
    c.text(170, 864, 'Legend', 11.5, weight='bold', fill=NAVY)
    for k, (col, st, lab) in enumerate((('#EAF1F8', BLUE, 'Application layer or component'), ('#FFF4D6', AMBER, 'Local data store or external service'), ('#E3F2EE', TEAL, 'Firebase service or hosted page'))):
        c.add('<rect x="34" y="%d" width="22" height="14" rx="3" fill="%s" stroke="%s"/>' % (876 + k * 20, col, st)); c.text(66, 883 + k * 20, lab, 11, anchor='start')
    c.save(*P('architecture'))

def deployment():
    c = Canvas(900, 1010)
    c.panel(40, 20, 750, 330, '\u00abdevice\u00bb  Android phone (user)', 'blue', size=13.5)
    c.panel(52, 58, 234, 280, '\u00abexecution environment\u00bb', 'blue', hh=22, size=11, fill='#fff')
    for k, t in enumerate([['Muhaffiz application', '(Flutter, Kotlin)'], ['Foreground services', '(detection, voice)'], ['WorkManager', 'notifications'], ['Launcher aliases', 'Android 8.0 and later']]):
        c.node(64, 92 + k * 60, 210, 50, t, fill=LBLUE, size=11.4)
    c.panel(298, 58, 234, 280, '\u00abdata\u00bb  Local storage', 'amber', hh=22, size=11, fill='#FFFBF0')
    for k, t in enumerate([['SQLite database', 'queue, log, library'], ['Encrypted evidence', 'Keystore key'], ['Bundled directory', 'and embeddings'], ['Offline map areas', '(up to three)']]):
        c.node(310, 92 + k * 60, 210, 50, t, fill=LAMBER, stroke=AMBER, size=11.4)
    c.panel(544, 58, 234, 280, '\u00abartifacts\u00bb  Models', 'blue', hh=22, size=11, fill='#fff')
    for k, t in enumerate([['Sound classifier', '(TFLite)'], ['Keyword spotter', '(offline)'], ['Sentence embedder', '(384 values)']]):
        c.node(556, 92 + k * 60, 210, 50, t, fill=LBLUE, size=11.4)
    ext = {}
    for lab, cxx in (('WhatsApp', 150), ('Google Maps\nPlatform', 310), ('Open map-data\nsource', 470), ('Cellular\nSMS network', 650)):
        ext[lab] = c.node(cxx - 70, 410, 140, 54, lab, fill=LAMBER, stroke=AMBER, size=11.5)
    for cxx, lab, key, dsh in ((150, 'share link', 'WhatsApp', False), (310, 'map tiles', 'Google Maps\nPlatform', False), (470, 'region download', 'Open map-data\nsource', True), (650, 'SMS (SOS, escalation)', 'Cellular\nSMS network', False)):
        c.conn([(cxx, 350), (cxx, 410)], lab, loff=(max(36, len(lab) * 3.2), 0), dashed=dsh, size=10.8)
    c.panel(40, 520, 750, 190, '\u00abcloud\u00bb  Firebase (Google)', 'teal', size=13.5)
    svc = [('Authentication', 'users and administrators'), ('Cloud Firestore', 'security rules, indexes'), ('Cloud Messaging', 'push delivery'), ('Cloud Storage', 'storage rules'), ('Cloud Functions', 'email, ack, scheduled jobs'), ('Hosting', 'muhaffiz.me, alert page')]
    for k, (a, b) in enumerate(svc):
        r, m = divmod(k, 3)
        c.node(52 + m * 246, 558 + r * 70, 232, 58, [a, b], fill=LTEAL, stroke=TEAL, size=11.5, bold_first=True)
    c.conn([(40, 185), (36, 185), (36, 615), (40, 615)], 'HTTPS,\nWebSocket', both=True, lpos=0.5, loff=(4, 0), size=10.8)
    c.panel(40, 780, 250, 130, '\u00abdevice\u00bb  Administrator computer', 'blue', size=11.8)
    c.node(52, 814, 226, 40, ['Web browser'], fill=LBLUE, size=11.4)
    c.node(52, 860, 226, 40, ['Admin website  muhaffiz.me'], fill=LTEAL, stroke=TEAL, size=11)
    emailb = c.node(330, 810, 180, 54, 'Email service', fill=LAMBER, stroke=AMBER, size=11.5)
    c.panel(540, 780, 250, 200, '\u00abdevice\u00bb  Trustee phone', 'blue', size=11.8)
    c.node(552, 814, 226, 36, 'SMS application', fill=LBLUE, size=11.4)
    c.node(552, 856, 226, 44, ['WhatsApp, email, push', '(if installed)'], fill=LBLUE, size=11)
    c.node(552, 906, 226, 56, ['Browser: alert page and', 'acknowledgement link'], fill=LTEAL, stroke=TEAL, size=11)
    c.conn([(165, 710), (165, 780)], 'HTTPS', both=True, loff=(30, 0), size=10.8)
    c.conn([(420, 710), (420, 810)], 'email', loff=(26, 0), size=10.8)
    c.conn([(665, 710), (665, 780)], 'push, alert link', loff=(0, 0), size=10.8)
    c.conn([(720, 437), (822, 437), (822, 880), (790, 880)], 'SMS alert', lpos=0.4, loff=(0, 0), size=10.8)
    c.save(*P('deployment'))

def components():
    c = Canvas(930, 940)
    def group(x, y, w, h, title, items, cols, kind='blue'):
        c.panel(x, y, w, h, title, kind, hh=24, size=11.5)
        bw = (w - 24 - 12 * (cols - 1)) / cols
        for k, it in enumerate(items):
            r, m = divmod(k, cols)
            bx = x + 12 + m * (bw + 12); by = y + 38 + r * 46; col = BLUE if kind == 'blue' else TEAL
            c.node(bx, by, bw, 36, it, fill=LBLUE if kind == 'blue' else LTEAL, stroke=col, size=11.5)
            c.add('<rect x="%s" y="%s" width="12" height="6" fill="#fff" stroke="%s" stroke-width="1"/><rect x="%s" y="%s" width="12" height="6" fill="#fff" stroke="%s" stroke-width="1"/>' % (bx - 6, by + 8, col, bx - 6, by + 22, col))
        return (x, y, w, h)
    A = group(20, 20, 390, 150, 'Safety core  (MOD-01, 02, 03, 18, 19)', ['sos_core', 'trigger_engine', 'detection_engine', 'voice_engine', 'evidence_vault', 'escalation'], 3)
    B = group(440, 20, 380, 150, 'Delivery and storage  (MOD-12, 13)', ['delivery_manager', 'sms_gateway', 'offline_store'], 1)
    E = group(20, 230, 390, 150, 'Identity and consent  (MOD-06, 14, 15, 21)', ['auth', 'consent', 'decoy_mode', 'app_disguise'], 2)
    C = group(440, 230, 380, 196, 'Family, community  (MOD-04, 05, 07, 08, 17)', ['family_circle', 'location_sharing', 'heatmap', 'near_help', 'missing_child'], 2)
    K = group(20, 450, 390, 150, 'Knowledge  (MOD-09, 10, 11, 20)', ['library', 'semantic_search', 'directory', 'safe_navigation'], 2)
    F = group(440, 470, 380, 150, 'Backend  (Functions, rules)', ['email_function', 'ack_endpoint', 'scheduled_jobs', 'security_rules'], 2, 'teal')
    G = group(440, 660, 380, 100, 'Admin website  (MOD-16)', ['admin_site'], 1, 'teal')
    c.node(20, 800, 800, 70, ['Shared packages', 'app_shell (navigation, theme, providers)  \u2022  platform_bridge (Kotlin channels)', 'config (thresholds and limits)  \u2022  firebase_client'], fill='#FFFBF0', stroke=AMBER, size=11.2, bold_first=True)
    c.conn([(410, 95), (440, 95)], '\u00abuses\u00bb', loff=(0, -14), size=10.5)
    c.conn([(215, 230), (215, 170)], 'consent, phrase hook', loff=(78, 0), lpos=0.5, size=11)
    c.conn([(630, 230), (630, 170)], 'push, queue', loff=(52, 0), lpos=0.5, size=11)
    c.conn([(820, 95), (836, 95), (836, 545), (820, 545)], '\u00abuses\u00bb HTTPS callable', lpos=0.5, loff=(0, 0), size=10.5)
    c.conn([(630, 660), (630, 620)], 'Firestore, functions', loff=(74, 0), lpos=0.5, size=11)
    c.text(430, 780, 'Arrows show runtime dependencies between package groups.', 10.8, italic=True, fill=GREY)
    c.save(*P('components'))

def navigation():
    c = Canvas(840, 900)
    steps = [('Splash', 20, 20), ('Sign in\n(one-time code)', 290, 20), ('Onboarding\nconsent', 560, 20), ('Phrase\nenrolment', 290, 110), ('Trustee\nsetup', 560, 110)]
    for t, x, y in steps: c.node(x, y, 230, 52, t, fill=LBLUE, size=11.8)
    c.conn([(250, 46), (290, 46)]); c.conn([(520, 46), (560, 46)])
    c.conn([(675, 72), (675, 110)])
    c.conn([(560, 136), (520, 136)])
    c.node(310, 196, 220, 56, ['Home', 'SOS control, status strip, tiles'], fill=LTEAL, stroke=TEAL, size=11.5, bold_first=True)
    c.conn([(405, 162), (405, 196)])
    tabs = {'Family tab': (20, ['Circle members', 'Invite member', 'Stop sharing', 'Last-known view']), 'Map tab': (290, ['Heatmap overlay', 'Zone details', 'Report incident', 'Nearby help']), 'Library tab': (560, ['Browse and filter', 'Search', 'Item view', 'Bookmarks'])}
    c.conn([(420, 252), (420, 284)], arrow=False); c.add('<line x1="135" y1="284" x2="685" y2="284" stroke="%s" stroke-width="1.4"/>' % NAVY)
    for t, (x, items) in tabs.items():
        c.conn([(x + 115, 284), (x + 115, 306)])
        c.panel(x, 306, 230, 30 + len(items) * 42 + 8, t, 'blue', hh=22, size=11.8)
        for k, it in enumerate(items): c.node(x + 12, 342 + k * 42, 206, 34, it, fill='#fff', size=11.4)
    more = ['Trustees', 'Settings and consent', 'Privacy summary', 'Evidence list', 'Directory', 'Safe location', 'Missing-child report', 'Helper registration', 'Escalation settings', 'App disguise']
    c.conn([(530, 224), (826, 224), (826, 566), (800, 566)])
    c.panel(20, 540, 780, 236, 'More tab', 'blue', hh=22, size=11.8)
    for k, it in enumerate(more):
        r, m = divmod(k, 3)
        c.node(32 + m * 256, 576 + r * 46, 240, 36, it, fill='#fff', size=11.4)
    c.node(20, 800, 800, 84, ['Screens reached from outside the tabs', 'SOS, countdown and SOS-active screens open from Home, the lock screen and the automatic and voice triggers.', 'The escalation warning opens after 3 minutes without acknowledgement. The decoy screen replaces the whole application.'], fill='#FFFBF0', stroke=AMBER, size=10.8, bold_first=True)
    c.save(*P('navigation'))

if __name__ == '__main__':
    architecture(); deployment(); components(); navigation(); print('ok')
