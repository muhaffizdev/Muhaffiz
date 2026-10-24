import os
from diag2 import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)
def P(n): return os.path.join(OUT, n + '.svg'), os.path.join(OUT, n + '.png')

def home(p):
    p.text(125, 40, 'Muhaffiz', 15, weight='bold', fill=PRIMARY); p.status_strip(52)
    p.s.add('<circle cx="%s" cy="%s" r="86" fill="#fde9e9"/><circle cx="%s" cy="%s" r="72" fill="%s"/>' % (p.X + 125, p.Y + 195, p.X + 125, p.Y + 195, RED))
    p.text(125, 195, 'SOS', 40, weight='bold', fill='#fff'); p.text(125, 295, 'Press and hold for 1 second', 10, fill='#555')
    p.rect(30, 312, 190, 34, fill='#eceff1', rx=17); p.rect(33, 315, 92, 28, fill=PRIMARY, rx=14); p.text(79, 329, 'Loud', 11, weight='bold', fill='#fff'); p.text(173, 329, 'Silent', 11, fill='#444')
    for i, t in enumerate(['Trustees', 'Evidence', 'Directory', 'Safe place']):
        x = 12 + i * 58; p.rect(x, 368, 52, 52, fill=MINT, rx=10); p.text(x + 26, 394, t, 8.5, weight='bold', fill=DARK)
    p.nav(0)

def countdown(p):
    p.rect(0, 20, p.w, p.h - 20, fill=DARK, rx=0)
    p.text(125, 70, 'Possible distress detected', 13, weight='bold', fill='#fff'); p.text(125, 92, 'Sending SOS unless you cancel.', 9, fill='#b7d3d0')
    p.s.add('<circle cx="%s" cy="%s" r="72" fill="none" stroke="#2c4a50" stroke-width="12"/><circle cx="%s" cy="%s" r="72" fill="none" stroke="%s" stroke-width="12" stroke-dasharray="135 318" transform="rotate(-90 %s %s)"/>' % (p.X + 125, p.Y + 215, p.X + 125, p.Y + 215, MINT, p.X + 125, p.Y + 215))
    p.text(125, 212, '14', 48, weight='bold', fill='#fff'); p.text(125, 245, 'seconds', 11, fill='#b7d3d0')
    p.button(25, 350, 200, 54, "I'm okay, cancel", fill=MINT, tf=DARK, size=14); p.text(125, 430, 'Swipe, or say or type your safe phrase.', 9.5, fill='#b7d3d0')

def sos_active(p):
    p.rect(0, 20, p.w, 56, fill=RED, rx=0); p.text(125, 40, 'SOS active', 15, weight='bold', fill='#fff'); p.text(125, 62, 'Alarm playing • Recording • 3:00 left', 9.5, fill='#fff')
    p.card(12, 88, 226, 98, ['Ayesha (sister)', 'SMS  ✓ sent     Push  ✓ sent', 'Email  • queued     WhatsApp  confirm'], size=10)
    p.card(12, 194, 226, 70, ['Bilal (friend)', 'SMS  ✓ sent     Push  ✓ sent'], size=10)
    p.card(12, 272, 226, 52, ['Nearby helpers', '2 notified • 1 accepted (450 m)'], size=10, fill=MINT)
    p.card(12, 332, 226, 48, ['Evidence recording', 'Stored on this phone only'], size=10)
    p.button(12, 396, 108, 44, 'Stop alarm', fill=RED); p.button(130, 396, 108, 44, 'Evidence', fill=PRIMARY)
    p.text(125, 458, 'Escalation to authorities if nobody responds', 9, fill='#555')

def family(p):
    p.appbar('Family circle', back=False)
    p.map(0, 60, 250, 230, markers=[(.3, .35, '#2e7d32', 'Ayesha (live)'), (.65, .6, '#9e9e9e', 'Bilal'), (.5, .25, PRIMARY, 'You')])
    p.card(12, 296, 226, 40, ['Ayesha • Sharing', 'Updated 1 min ago'], size=10)
    p.card(12, 342, 226, 40, ['Bilal • Last known location', 'Not live • 3 h ago'], size=10, fill='#f2f2f2')
    p.button(12, 392, 226, 34, 'Stop sharing my location', fill='#fff', tf=RED); p.rect(12, 392, 226, 34, fill='none', stroke=RED, rx=10)
    p.button(12, 434, 226, 0, '')
    p.nav(1)

def heat(p):
    p.appbar('Danger map', back=False)
    cells = [(1, 1, '#66bb6a'), (2, 1, '#9ccc65'), (3, 1, '#d4e157'), (2, 2, '#ffca28'), (3, 2, '#ff9800'), (4, 2, '#ff7043'), (3, 3, '#e53935'), (4, 3, '#ff7043'), (2, 3, '#ffa726'), (1, 4, '#66bb6a'), (5, 3, '#d4e157')]
    p.map(0, 60, 250, 250, cells=cells, markers=[(.5, .55, PRIMARY, 'You')])
    for k, col in enumerate(['#66bb6a', '#9ccc65', '#d4e157', '#ffca28', '#ff9800', '#ff7043', '#e53935']): p.rect(12 + k * 32.3, 318, 32.3, 14, fill=col, rx=0)
    p.text(24, 342, 'Lower', 9, anchor='start'); p.text(226, 342, 'Higher', 9, anchor='end')
    p.card(12, 352, 226, 56, ['Zone: 15 reports', 'Harassment 7 • Felt unsafe 5 • Theft 3', 'Reporters are never shown'], size=9.5)
    p.button(150, 416, 88, 32, '+ Report', fill=RED, size=11); p.nav(2)

def library(p):
    p.appbar('Library', back=False); p.field(12, 70, 226, 'Search in your own words', 'help a friend after harassment')
    p.rect(12, 108, 70, 18, fill=MINT, rx=9); p.text(47, 117, 'Offline', 9, weight='bold', fill=DARK)
    x = 12
    for i, c in enumerate(['All', 'Prevention', 'After care']): x += p.chip(x, 134, c, i == 0) + 6
    for i, (t, r) in enumerate([('Supporting someone after an assault', .92), ('What to do after harassment', .81), ('Talking to a friend in distress', .64)]):
        y = 168 + i * 82; p.card(12, y, 226, 72, [t, 'Article • After-incident care'], size=10); p.rect(22, y + 52, 150, 7, fill='#e0e0e0', rx=3); p.rect(22, y + 52, 150 * r, 7, fill=PRIMARY, rx=3)
        p.text(178, y + 56, '%d%% match' % (r * 100), 8.5, anchor='start')
    p.nav(3)

def decoy(p):
    p.rect(0, 20, p.w, p.h - 20, fill='#1b1b1b', rx=0); p.text(235, 78, '0', 44, anchor='end', fill='#fff')
    keys = [['C', '±', '%', '÷'], ['7', '8', '9', '×'], ['4', '5', '6', '−'], ['1', '2', '3', '+'], ['0', '0', '.', '=']]
    for r, row in enumerate(keys):
        for c, k in enumerate(row):
            op = c == 3; p.s.add('<circle cx="%s" cy="%s" r="25" fill="%s"/>' % (p.X + 36 + c * 59, p.Y + 160 + r * 62, '#ff9f0a' if op else '#333')); p.text(36 + c * 59, 160 + r * 62, k, 16, fill='#fff')
    p.text(125, 480, 'Hold = for 2 seconds to open the real app', 8.5, fill='#666')

def stop_share(p):
    p.appbar('Stop sharing'); p.text(125, 100, 'Say your safe phrase to unlock,', 13, weight='bold', fill=DARK); p.text(125, 118, 'then switch sharing off.', 11)
    p.s.add('<circle cx="%s" cy="%s" r="46" fill="%s"/><circle cx="%s" cy="%s" r="64" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 5"/>' % (p.X + 125, p.Y + 235, PRIMARY, p.X + 125, p.Y + 235, MINT))
    p.text(125, 235, 'Listening', 12, weight='bold', fill='#fff'); p.text(125, 330, 'Nobody else is notified.', 11, weight='bold'); p.text(125, 348, 'They will see your last location,', 10); p.text(125, 362, 'marked "Not live".', 10)
    p.rect(25, 382, 200, 40, fill='#f7f9fa', stroke='#e0e6e8', rx=8); p.text(37, 402, 'Share my location', 11, anchor='start'); p.switch(185, 394, True); p.button(25, 428, 200, 30, 'Cancel', fill='#eceff1', tf='#333'); p.text(125, 476, 'Leave the circle instead', 10.5, fill=PRIMARY)

def trustees(p):
    p.appbar('Trustees')
    for i, (n, ch) in enumerate([('Ayesha (sister)', ['SMS', 'Push', 'Email']), ('Bilal (friend)', ['SMS', 'WhatsApp']), ('Mother', ['SMS'])]):
        y = 72 + i * 86; p.card(12, y, 226, 76, [n, '+92 3xx xxxxxxx'], size=10.5); x = 22
        for c in ch: x += p.chip(x, y + 46, c, True) + 5
    p.button(12, 340, 226, 40, '+ Add trustee', fill=PRIMARY); p.text(125, 400, 'Up to 10 trustees. At least one is required.', 9.5, fill='#555')

def settings(p):
    p.appbar('Settings and consent')
    rows = [('Microphone detection', True), ('Voice activation', True), ('Location sharing', True), ('Silent as default SOS', False), ('Decoy Mode', False), ('Alert nearby helpers', True)]
    for i, (t, on) in enumerate(rows):
        y = 74 + i * 46; p.rect(12, y, 226, 40, fill='#f7f9fa', stroke='#e0e6e8', rx=8); p.text(24, y + 20, t, 11, anchor='start'); p.switch(196, y + 12, on)
    p.card(12, 352, 226, 40, ['Evidence retention', '30 days (7, 30 or 90)'], size=10); p.card(12, 398, 226, 40, ['Countdown cancel', 'Swipe, spoken or typed phrase'], size=10); p.text(125, 458, 'Each switch works on its own and takes effect at once.', 9, fill='#555')

def privacy(p):
    p.appbar('Privacy summary')
    for i, (t, d) in enumerate([('On our servers', 'Profile, trustees, circles, shared locations, reports, helper status'), ('Only on your phone', 'Audio buffers, evidence recordings, library, models, event log'), ('Sent during an SOS', 'Location and message to your trustees, helpers and authority numbers')]):
        y = 72 + i * 110; p.card(12, y, 226, 100, [t, d[:34], d[34:68], d[68:]], size=10, fill=MINT if i == 1 else '#F4F8F8')
    p.text(125, 420, 'No audio from detection or voice ever leaves the phone.', 9.5, weight='bold')

def consent(p):
    p.appbar('Before you start', back=False)
    for i, t in enumerate(['Microphone: the app listens for distress sounds and', 'your safe phrases. This happens only on your phone.', 'No audio is stored by these features.', 'Location: shared only as you choose.', 'Evidence: audio is recorded only after an SOS', 'starts, and stays on your phone.']): p.text(14, 84 + i * 24, t, 9.5, anchor='start')
    p.rect(14, 250, 18, 18, fill='#fff', stroke=PRIMARY, rx=3); p.text(40, 259, 'I understand and agree', 11, anchor='start')
    p.button(14, 300, 222, 40, 'Accept and continue', fill=PRIMARY); p.button(14, 348, 222, 36, 'Not now (features stay off)', fill='#eceff1', tf='#333')

def signin(p):
    p.text(125, 80, 'Muhaffiz', 20, weight='bold', fill=PRIMARY); p.text(125, 104, 'Sign in with your phone number', 11)
    p.field(20, 140, 210, 'Mobile number', '+92 3xx xxxxxxx'); p.button(20, 186, 210, 38, 'Send code', fill=PRIMARY)
    p.field(20, 250, 210, 'One-time code', '4 8 2 9 1 0'); p.button(20, 296, 210, 38, 'Verify and continue', fill=PRIMARY); p.text(125, 360, 'Wrong code five times locks sending for 10 minutes.', 8.5, fill='#555')

def phrases(p):
    p.appbar('Safe and duress phrases')
    p.field(12, 72, 226, 'Safe phrase (loud SOS)', 'blue lantern tonight'); p.card(12, 112, 226, 40, ['Samples 3 of 3 recognised', 'Sensitivity set'], size=10, fill=MINT)
    p.field(12, 168, 226, 'Duress phrase (silent SOS)', 'the kettle is ready'); p.card(12, 208, 226, 40, ['Samples 2 of 3 recognised', 'Say it once more'], size=10)
    p.button(12, 268, 226, 40, 'Record sample', fill=PRIMARY); p.text(125, 332, 'Phrases are 2 to 5 words and must be different.', 9.5, fill='#555')

def report(p):
    p.appbar('Report an incident'); x = 12
    for i, c in enumerate(['Harassment', 'Theft', 'Felt unsafe']): x += p.chip(x, 72, c, i == 0) + 5
    p.map(12, 104, 226, 120, markers=[(.5, .5, RED, '')]); p.text(125, 238, 'Location filled in. Drag the pin to edit.', 9.5)
    p.field(12, 254, 226, 'Note (optional, 280 characters)', 'Followed near the market'); p.button(12, 306, 226, 40, 'Submit report', fill=RED); p.text(125, 366, 'Reports are anonymous. Up to 5 in 24 hours.', 9.5, fill='#555')

def nearhelp(p):
    p.appbar('Nearby help', back=False); p.text(125, 84, 'Help request', 14, weight='bold', fill=RED)
    p.card(12, 100, 226, 96, ['Someone needs help', 'About 450 m away', 'Requested 2 min ago', 'Exact location shown after you accept'], size=10.5)
    p.button(12, 210, 108, 44, 'Decline', fill='#eceff1', tf='#333'); p.button(130, 210, 108, 44, 'Accept', fill=PRIMARY)
    p.card(12, 290, 226, 62, ['Offline view', 'Unavailable: no connection', 'Requests are sent when you are online'], size=10, fill='#f2f2f2')

def helperreg(p):
    p.appbar('Become a Verified Helper'); p.field(12, 74, 226, 'Full name', 'Sara Khan'); p.field(12, 116, 226, 'Phone number', '+92 3xx xxxxxxx')
    p.rect(12, 160, 226, 90, fill='#f7f9fa', stroke='#90a4ae', rx=8); p.text(125, 205, 'Photo of identity document', 11, fill='#607d8b')
    p.button(12, 264, 226, 40, 'Submit for review', fill=PRIMARY); p.card(12, 318, 226, 46, ['Status: pending review', 'The photo is deleted after the decision'], size=9.5, fill=MINT)

def child(p):
    p.appbar('Missing-child report'); p.field(12, 70, 110, 'Name', 'Hamza'); p.field(128, 70, 110, 'Age', '7')
    p.rect(12, 112, 70, 70, fill='#f7f9fa', stroke='#90a4ae', rx=8); p.text(47, 147, 'Photo', 10, fill='#607d8b'); p.field(90, 112, 148, 'Last seen (place)', 'Saddar bazaar'); p.field(90, 150, 148, 'Last seen (time)', 'Today 5:10 pm')
    p.field(12, 192, 226, 'Description', 'Red shirt, blue school bag'); p.field(12, 232, 226, 'Guardian contact', '+92 3xx xxxxxxx')
    p.rect(12, 276, 16, 16, fill='#fff', stroke=PRIMARY, rx=3); p.text(34, 284, 'I am the child\'s guardian', 10.5, anchor='start')
    p.button(12, 308, 226, 40, 'Submit and alert', fill=RED)

def evidence(p):
    p.appbar('Evidence recordings')
    for i, (t, d, tr) in enumerate([('Today 17:42', '12 min 08 s', 'voice'), ('Mon 21:15', '3 min 40 s', 'manual'), ('Sun 08:02', '6 min 12 s', 'automatic')]):
        y = 72 + i * 92; p.card(12, y, 226, 84, [t + ' • ' + d, 'Trigger: ' + tr, 'Location saved'], size=10)
        p.button(110, y + 50, 56, 26, 'Export', fill=PRIMARY, size=9); p.button(172, y + 50, 56, 26, 'Delete', fill=RED, size=9)
    p.text(125, 360, 'Stored encrypted on this phone. Deleted after 30 days.', 9.5, fill='#555')

def directory(p):
    p.appbar('Emergency services')
    for i, (n, d) in enumerate([('Rescue 1122', 'Emergency rescue'), ('Police 15', 'Police helpline'), ('Women\'s helpline', 'Support line'), ('General Hospital', '1.2 km • Hospital'), ('Police Station Saddar', '1.8 km • Police')]):
        y = 72 + i * 62; p.card(12, y, 226, 54, [n, d], size=10.5); p.button(184, y + 12, 46, 30, 'Call', fill=PRIMARY, size=10)
    p.text(125, 400, 'Nearest facilities first when location is available.', 9, fill='#555')

def safeplace(p):
    p.appbar('Nearest safe location'); p.map(0, 60, 250, 250, markers=[(.25, .75, PRIMARY, 'You'), (.75, .25, '#2e7d32', 'Hospital')])
    p.s.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="3" stroke-dasharray="6 4"/>' % (p.X + 62, p.Y + 247, p.X + 188, p.Y + 122, PRIMARY))
    p.card(12, 318, 226, 62, ['General Hospital', '850 m north-east', 'Works without a connection'], size=10); p.button(12, 392, 226, 38, 'Open directions (online)', fill=PRIMARY)

def warning(p):
    p.rect(0, 20, p.w, p.h - 20, fill=DARK, rx=0); p.text(125, 80, 'Nobody has responded', 14, weight='bold', fill='#fff'); p.text(125, 102, 'Alerting authorities in', 11, fill='#b7d3d0')
    p.text(125, 190, '22', 56, weight='bold', fill='#fff'); p.text(125, 225, 'seconds', 11, fill='#b7d3d0')
    p.button(25, 300, 200, 52, 'Cancel escalation', fill=MINT, tf=DARK, size=14); p.text(125, 380, 'Police 15, Rescue 1122 (by SMS)', 10, fill='#b7d3d0')

def authsettings(p):
    p.appbar('Escalation settings')
    for i, (n, c) in enumerate([('Police 15', 'SMS'), ('Rescue 1122', 'SMS')]):
        y = 74 + i * 62; p.card(12, y, 226, 54, [n, 'Channel: ' + c], size=10.5); p.button(176, y + 14, 54, 26, 'Change', fill=PRIMARY, size=9)
    p.button(12, 206, 226, 38, '+ Add number', fill='#eceff1', tf=PRIMARY); p.card(12, 260, 226, 70, ['Timing', 'Wait 3 minutes, then a 30 s warning', 'with one-tap cancel'], size=10)

def disguise(p):
    p.appbar('App disguise'); p.text(125, 86, 'Choose how the app looks on the home screen', 10.5)
    for i, n in enumerate(['Original (Muhaffiz)', 'Calculator', 'Notes', 'Clock']):
        y = 104 + i * 62; p.card(12, y, 226, 54, [n, 'Icon and name change'], size=10.5, fill=MINT if i == 2 else '#F4F8F8')
        p.s.add('<circle cx="%s" cy="%s" r="9" fill="%s" stroke="%s"/>' % (p.X + 216, p.Y + y + 27, PRIMARY if i == 2 else '#fff', PRIMARY))
    p.text(125, 366, 'Some launchers show the change only after refresh.', 9, fill='#555'); p.button(12, 384, 226, 36, 'Apply', fill=PRIMARY)

def admin_dash(s):
    s.add('<rect x="6" y="36" width="150" height="478" fill="#10262B"/>')
    for i, tt in enumerate(['Overview', 'Moderation queue', 'Helper review', 'Health', 'Sign out']):
        s.text(20, 70 + i * 40, tt, 12.8, anchor='start', fill='#fff' if i == 0 else '#9fb9b6', weight='bold' if i == 0 else 'normal')
    s.text(176, 66, 'Overview', 18, anchor='start', weight='bold', fill=DARK)
    for i, (n, v) in enumerate([('Registered users', '1,240'), ('Helpers pending', '7'), ('Reports to review', '12'), ('SOS delivery, 7 days', '98.4%')]):
        x = 176 + i * 140; s.add('<rect x="%d" y="86" width="130" height="76" rx="8" fill="#EAF1F8" stroke="#1F4E78"/>' % x); s.text(x + 10, 108, n, 11.5, anchor='start'); s.text(x + 10, 140, v, 21, anchor='start', weight='bold', fill=PRIMARY)
    s.text(176, 194, 'Registrations per day', 13, anchor='start', weight='bold')
    for i, h in enumerate([30, 44, 38, 60, 52, 70, 64, 48, 58, 76]): s.add('<rect x="%d" y="%d" width="24" height="%d" fill="%s"/>' % (182 + i * 36, 300 - h, h, PRIMARY))
    s.text(176, 336, 'Delivery success by channel', 13, anchor='start', weight='bold')
    for i, (c_, v) in enumerate([('SMS', 99), ('Push', 97), ('Email', 95)]):
        y = 366 + i * 30; s.text(176, y, c_, 12, anchor='start'); s.add('<rect x="236" y="%d" width="400" height="14" fill="#e0e0e0" rx="7"/><rect x="236" y="%d" width="%d" height="14" fill="%s" rx="7"/>' % (y - 7, y - 7, 4 * v, PRIMARY)); s.text(646, y, '%d%%' % v, 12, anchor='start')
    s.text(176, 470, 'Phone numbers are shown masked.', 12, anchor='start', italic=True)

def admin_queue(s):
    s.add('<rect x="6" y="36" width="150" height="478" fill="#10262B"/>')
    for i, tt in enumerate(['Overview', 'Moderation queue', 'Helper review', 'Health', 'Sign out']):
        s.text(20, 70 + i * 40, tt, 12.8, anchor='start', fill='#fff' if i == 1 else '#9fb9b6', weight='bold' if i == 1 else 'normal')
    s.text(176, 66, 'Moderation queue', 18, anchor='start', weight='bold', fill=DARK)
    hdr = ['Type', 'Content', 'Flag reason', 'Decision']; xs = [176, 256, 436, 566]
    s.add('<rect x="170" y="86" width="560" height="30" fill="#1F4E78"/>')
    for x, h in zip(xs, hdr): s.text(x, 101, h, 12.5, anchor='start', fill='#fff', weight='bold')
    rows = [('Heatmap', 'Theft, Saddar market', 'Burst of reports', 'Approve | Remove'), ('Child', 'Hamza, 7, Saddar', 'Every report', 'Approve | Remove'), ('Heatmap', 'Harassment, Gulberg', 'Near-duplicate', 'Approve | Remove'), ('Helper', 'Sara Khan, ID photo', 'Pending check', 'Approve | Reject')]
    for i, r in enumerate(rows):
        y = 116 + i * 50; s.add('<rect x="170" y="%d" width="560" height="50" fill="%s" stroke="#d6dde2"/>' % (y, '#EAF1F8' if i % 2 else '#fff'))
        for x, v in zip(xs, r): s.text(x, y + 25, v, 11.8, anchor='start')
    s.text(176, 360, 'Every decision is logged with the administrator and the time.', 12, anchor='start', italic=True)

KEY = [(home, 'Home screen'), (countdown, 'Countdown screen'), (sos_active, 'SOS active screen'), (family, 'Family map screen'), (heat, 'Danger map screen'), (library, 'Library search screen'),
       (decoy, 'Decoy screen'), (stop_share, 'Stop-sharing screen'), (trustees, 'Trustee screen'), (settings, 'Settings and consent toggles')]
REST = [(privacy, 'Privacy summary'), (consent, 'Onboarding consent'), (signin, 'Sign-in screen'), (phrases, 'Phrase enrolment'), (report, 'Incident report form'), (nearhelp, 'Nearby help screen'),
        (helperreg, 'Helper registration'), (child, 'Missing-child report form'), (evidence, 'Evidence list'), (directory, 'Emergency services directory'), (safeplace, 'Safe-location guidance'),
        (warning, 'Escalation warning'), (authsettings, 'Escalation settings'), (disguise, 'App disguise settings')]

def make():
    out = {'key': [], 'rest': []}
    for grp, items, pre in (('key', KEY, 'ui_k'), ('rest', REST, 'ui_m')):
        for n in range(0, len(items), 2):
            pair = items[n:n + 2]
            key = '%s%d' % (pre, n // 2 + 1)
            phones(*P(key), [b for b, _ in pair], [t for _, t in pair])
            cap = ('Key screens: ' if grp == 'key' else 'Screens: ') + ' and '.join(t.lower() if k else t for k, (_, t) in enumerate(pair))
            out[grp].append((key, cap))
    browser(*P('admin_overview'), 'overview', admin_dash, 740, 520)
    browser(*P('admin_queue'), 'moderation', admin_queue, 740, 520)
    return out
if __name__ == '__main__': print(make())
