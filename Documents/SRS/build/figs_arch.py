import os
from diag2 import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)
def P(n): return os.path.join(OUT, n + '.svg'), os.path.join(OUT, n + '.png')

def architecture():
    s = Svg(980, 700)
    s.box(15, 15, 520, 540, '', fill='#F7FBFC', stroke=PRIMARY, rx=10)
    s.text(275, 34, 'Android application (Flutter, on-device layer)', 14, weight='bold', fill=PRIMARY)
    layers = [
        (55, 'Presentation layer', 'Screens and widgets, navigation, state providers (Riverpod)'),
        (140, 'Application layer', 'Trigger engine, SOS orchestrator, delivery manager,\nescalation manager, sharing manager, consent manager'),
        (225, 'Domain and data layer', 'Repositories for the local database (SQLite), cache and encrypted\nevidence files; remote repositories (Firestore, Storage, Functions)'),
        (310, 'On-device intelligence', 'Sound classifier (TFLite) \u2022 Keyword spotter \u2022\nSentence embedder (library search)'),
        (395, 'Platform layer (Kotlin, platform channels)', 'Foreground services \u2022 SMS manager \u2022 audio and sensors \u2022 Keystore \u2022\nWorkManager \u2022 launcher aliases \u2022 notifications'),
    ]
    for y, t, d in layers:
        s.box(35, y, 480, 78, '', fill='#EAF1F8', stroke='#1F4E78', rx=8)
        s.text(275, y + 18, t, 13, weight='bold', fill='#1F3864'); s.text(275, y + 48, d, 11.5)
    for y in (133, 218, 303, 388): s.line((275, y), (275, y + 7), arrow=False)
    s.box(580, 15, 230, 330, '', fill='#F7FBFC', stroke=PRIMARY, rx=10)
    s.text(695, 34, 'Firebase backend', 14, weight='bold', fill=PRIMARY)
    for i, t in enumerate(['Authentication', 'Cloud Firestore', 'Cloud Messaging (FCM)', 'Cloud Storage', 'Cloud Functions', 'Hosting']):
        s.box(598, 50 + i * 47, 194, 38, t, fill='#EAF1F8', size=12)
    s.box(580, 385, 230, 70, 'Admin website\nmuhaffiz.me (Flutter web)', fill='#EAF1F8', stroke=PRIMARY, size=12.5, weight='bold')
    s.box(580, 480, 230, 55, 'Alert page for trustees\n(Firebase Hosting)', fill='#EAF1F8', size=11.5)
    s.box(850, 237, 115, 52, 'Email service', fill='#FFF7E0', stroke='#B08900', size=12)
    ex = [(35, 'Cellular\nSMS network'), (155, 'WhatsApp'), (275, 'Google Maps\nPlatform'), (395, 'Open map-data\nsource')]
    for x, t in ex: s.box(x, 610, 105, 52, t, fill='#FFF7E0', stroke='#B08900', size=11.5)
    arrow(s, [(515, 264), (580, 264)], 'HTTPS,\nreal-time', toff=(0, -22))
    arrow(s, [(792, 263), (850, 263)], '', )
    arrow(s, [(695, 385), (695, 345)], '')
    arrow(s, [(695, 480), (695, 455)], '', )
    for (x, t), lab in zip(ex, ['SMS', 'share link', 'map display', 'download']):
        arrow(s, [(x + 52, 473), (x + 52, 610)], lab, toff=(0, 0), tpos=0.5)
    s.text(275, 585, 'Local storage: SQLite, encrypted evidence, bundled content and models, offline maps', 10.5, italic=True)
    s.save(*P('architecture'))

def deployment():
    s = Svg(860, 600)
    def node(x, y, w, h, title, kind='device'):
        s.add('<rect x="%s" y="%s" width="%s" height="%s" fill="#F7FBFC" stroke="%s" stroke-width="1.8"/>' % (x, y, w, h, PRIMARY))
        s.add('<polygon points="%s,%s %s,%s %s,%s %s,%s" fill="#DCEFEA" stroke="%s" stroke-width="1.2"/>' % (x, y, x + 10, y - 9, x + w + 10, y - 9, x + w, y, PRIMARY))
        s.add('<polygon points="%s,%s %s,%s %s,%s %s,%s" fill="#DCEFEA" stroke="%s" stroke-width="1.2"/>' % (x + w, y, x + w + 10, y - 9, x + w + 10, y + h - 9, x + w, y + h, PRIMARY))
        s.text(x + w / 2, y + 16, '«%s»' % kind, 10.5, fill='#555'); s.text(x + w / 2, y + 32, title, 12.5, weight='bold')
    node(20, 60, 270, 300, 'Android phone (user)')
    for i, t in enumerate(['Muhaffiz application\n(Flutter, Kotlin services)', 'Local database (SQLite)\nlibrary, directory, queue, log', 'Encrypted evidence files\n(Keystore key)', 'On-device models\n(classifier, keyword, embedder)']):
        s.box(40, 105 + i * 62, 230, 52, t, fill='#fff', size=11)
    node(350, 40, 300, 360, 'Firebase (Google cloud)', 'cloud')
    for i, t in enumerate(['Authentication', 'Cloud Firestore + security rules', 'Cloud Messaging', 'Cloud Storage + storage rules', 'Cloud Functions (HTTPS)', 'Hosting: muhaffiz.me (admin),\nalert page for trustees']):
        s.box(370, 90 + i * 49, 260, 42, t, fill='#fff', size=11)
    node(710, 60, 140, 110, 'Admin computer', 'device'); s.box(722, 105, 116, 50, 'Web browser', fill='#fff', size=11)
    node(710, 230, 140, 110, 'Trustee phone', 'device'); s.box(722, 275, 116, 50, 'SMS, browser,\nWhatsApp', fill='#fff', size=10.5)
    s.box(20, 450, 150, 56, 'Cellular SMS network', fill='#FFF7E0', size=11.5); s.box(190, 450, 150, 56, 'WhatsApp', fill='#FFF7E0', size=11.5)
    s.box(360, 450, 150, 56, 'Email service', fill='#FFF7E0', size=11.5); s.box(530, 450, 150, 56, 'Open map-data source', fill='#FFF7E0', size=11.5)
    s.box(700, 450, 150, 56, 'Google Maps\nPlatform', fill='#FFF7E0', size=11.5)
    arrow(s, [(290, 200), (350, 200)], 'HTTPS /\nreal-time', toff=(0, -22))
    arrow(s, [(650, 125), (710, 110)], 'HTTPS', toff=(0, -12))
    arrow(s, [(650, 270), (710, 280)], 'push, link', toff=(0, 16))
    arrow(s, [(95, 360), (95, 450)], 'SMS', toff=(18, 0))
    arrow(s, [(240, 360), (265, 450)], 'share', toff=(22, 0))
    arrow(s, [(500, 400), (435, 450)], 'email', toff=(22, 0), tpos=0.6)
    arrow(s, [(200, 360), (580, 450)], 'map data (online)', dashed=True, tpos=0.58, toff=(0, 14))
    arrow(s, [(240, 360), (770, 450)], '', dashed=True)
    s.text(430, 560, 'The phone also reaches the Google Maps Platform directly for online map display.', 11, italic=True)
    s.save(*P('deployment'))

def components():
    s = Svg(900, 620)
    def grp(x, y, w, h, t, items, cols=1):
        s.box(x, y, w, h, '', fill='#F7FBFC', stroke=PRIMARY, rx=8)
        s.text(x + w / 2, y + 17, t, 12.5, weight='bold', fill=PRIMARY)
        bw = (w - 20 - (cols - 1) * 8) / cols
        for i, it in enumerate(items):
            r, c = divmod(i, cols)
            s.box(x + 10 + c * (bw + 8), y + 34 + r * 38, bw, 30, it, fill='#EAF1F8', size=11, rx=4)
        return (x, y, w, h)
    A = grp(15, 15, 270, 175, 'Safety core (MOD-01, 02, 03, 18, 19)', ['sos_core', 'trigger_engine', 'detection_engine', 'voice_engine', 'evidence_vault', 'escalation'], 2)
    B = grp(335, 15, 230, 175, 'Delivery and storage (MOD-12, 13)', ['delivery_manager', 'sms_gateway', 'offline_store'], 1)
    F = grp(615, 15, 270, 175, 'Backend functions (MOD-16 support)', ['email_function', 'ack_endpoint', 'scheduled_jobs', 'security_rules'], 1)
    E = grp(15, 245, 270, 135, 'Identity and consent (MOD-06, 14, 15, 21)', ['auth', 'consent', 'decoy_mode', 'app_disguise'], 2)
    C = grp(335, 245, 230, 220, 'Family, community (MOD-04, 05, 07, 08, 17)', ['family_circle', 'location_sharing', 'heatmap', 'near_help', 'missing_child'], 1)
    G = grp(615, 245, 270, 80, 'Admin website (MOD-16)', ['admin_site'], 1)
    D = grp(15, 410, 270, 135, 'Knowledge (MOD-09, 10, 11, 20)', ['library', 'semantic_search', 'directory', 'safe_navigation'], 2)
    s.box(335, 500, 550, 45, 'Shared: app_shell \u2022 platform_bridge (Kotlin channels) \u2022 config (thresholds) \u2022 firebase_client', fill='#FFF7E0', stroke='#B08900', size=11.5)
    arrow(s, [(285, 100), (335, 100)], '\u00abuses\u00bb', toff=(0, -12))
    arrow(s, [(565, 100), (615, 100)], '\u00abuses\u00bb', toff=(0, -12))
    arrow(s, [(450, 245), (450, 190)], '\u00abuses\u00bb', toff=(-30, 0))
    arrow(s, [(150, 245), (150, 190)], '\u00abuses\u00bb', toff=(-30, 0))
    arrow(s, [(750, 245), (750, 190)], '\u00abuses\u00bb', toff=(-30, 0))
    arrow(s, [(285, 300), (335, 300)], '', dashed=True)
    arrow(s, [(150, 410), (150, 380)], '', dashed=True)
    s.text(450, 575, 'Solid arrows: runtime dependency between packages. Dashed arrows: shared data or settings.', 11, italic=True)
    s.save(*P('components'))

def navigation():
    s = Svg(940, 560)
    def b(x, y, w, t, fill='#EAF1F8', size=11.5): s.box(x, y, w, 36, t, fill=fill, size=size, rx=6)
    b(15, 20, 110, 'Splash'); b(150, 20, 130, 'Sign in (code)'); b(305, 20, 150, 'Onboarding consent'); b(480, 20, 150, 'Trustee setup'); b(655, 20, 150, 'Phrase enrolment')
    for a, c in ((125, 150), (280, 305), (455, 480), (630, 655)): s.line((a, 38), (c, 38))
    s.poly([(730, 56), (730, 100), (470, 100), (470, 130)], arrow=True)
    b(395, 130, 150, 'Home (SOS)', fill=MINT, size=12.5)
    tabs = [('Family', 20), ('Map', 205), ('Library', 390), ('More', 600)]
    s.line((470, 166), (470, 195), arrow=False); s.line((95, 195), (680, 195), arrow=False)
    for t, x in tabs:
        cx = x + 75
        s.line((cx, 195), (cx, 225)); b(x, 225, 150, t, fill='#DCE9F5', size=12)
    ch = {'Family': ['Circle members', 'Invite member', 'Stop sharing', 'Last-known view'],
          'Map': ['Heatmap overlay', 'Report incident', 'Zone details', 'Nearby help'],
          'Library': ['Browse and filter', 'Search', 'Item view', 'Bookmarks']}
    for t, x in tabs[:3]:
        for i, c in enumerate(ch[t]):
            b(x + 15, 280 + i * 44, 135, c, size=10.5); s.line((x + 8, 261), (x + 8, 298 + i * 44), arrow=False); s.line((x + 8, 298 + i * 44), (x + 15, 298 + i * 44), arrow=False)
    more = ['Trustees', 'Settings and consent', 'Privacy summary', 'Evidence list', 'Directory', 'Safe location', 'Missing-child report', 'Helper registration', 'Escalation settings', 'Disguise and decoy']
    for i, c in enumerate(more):
        col, r = divmod(i, 5); x = 600 + col * 170 if col else 600
        xx = 615 if col == 0 else 785
        b(xx, 280 + r * 44, 150, c, size=10.5)
        s.line((608 + (0 if col == 0 else 170), 261), (608 + (0 if col == 0 else 170), 298 + r * 44), arrow=False)
        s.line((608 + (0 if col == 0 else 170), 298 + r * 44), (xx, 298 + r * 44), arrow=False)
        s.box(15, 508, 910, 40, 'SOS, countdown and SOS-active screens are reachable from Home, the lock screen, and the automatic and voice triggers.', fill='#FFF7E0', stroke='#B08900', size=12)
    s.save(*P('navigation'))

def make():
    architecture(); deployment(); components(); navigation()
if __name__ == '__main__': make(); print('ok')
