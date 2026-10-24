"""Swimlane activity diagrams (custom SVG): lanes as columns, nodes on a grid, orthogonal connectors."""
import os, math
from diag3 import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)

def swim(name, lanes, nodes, edges, lw=310, rowh=82, size=12.8):
    n = len(lanes)
    maxrow = max(v[1] for v in nodes.values())
    W = lw * n + 40; H = 70 + rowh * (maxrow + 1) + 30
    c = Canvas(W, H)
    # lanes
    for i, ln in enumerate(lanes):
        x = 20 + i * lw
        c.add('<rect x="%s" y="20" width="%s" height="%s" fill="%s" stroke="#8a9bb0" stroke-width="1.3"/>' % (x, lw, H - 40, '#F8FAFC' if i % 2 == 0 else '#F1F5F9'))
        c.add('<rect x="%s" y="20" width="%s" height="30" fill="#25497A"/>' % (x, lw))
        c.text(x + lw / 2, 36, ln, 13.5, weight='bold', fill='#fff')
    pos = {}
    for id_, v in nodes.items():
        kind, lane, row, label = v[0], v[1] if False else None, None, None
    geo = {}
    for id_, (kind, row, lane, label, *rest) in nodes.items():
        dx = rest[0] if rest else 0
        cx_ = 20 + lane * lw + lw / 2 + dx; cy_ = 72 + row * rowh + 26
        if kind == 'act': w, h = (172 if not rest or len(rest) < 2 else min(rest[1], lw - 36)), 50
        elif kind == 'dec': w, h = 160, 66
        elif kind in ('start', 'end'): w, h = 18, 18
        geo[id_] = (cx_, cy_, w, h, kind)
        if kind == 'act':
            c.node(cx_ - w / 2, cy_ - h / 2, w, h, label, fill=LBLUE, stroke=BLUE, size=size - 0.4, rx=16)
        elif kind == 'dec':
            c.add('<polygon points="%s,%s %s,%s %s,%s %s,%s" fill="#FFF4CC" stroke="#B08900" stroke-width="1.4"/>' % (cx_, cy_ - h / 2, cx_ + w / 2, cy_, cx_, cy_ + h / 2, cx_ - w / 2, cy_))
            c.text(cx_, cy_, label.split('\n'), size - 0.8, fill='#3a2f00')
        elif kind == 'start':
            c.add('<circle cx="%s" cy="%s" r="9" fill="%s"/>' % (cx_, cy_, NAVY))
        elif kind == 'end':
            c.add('<circle cx="%s" cy="%s" r="10" fill="#fff" stroke="%s" stroke-width="2"/><circle cx="%s" cy="%s" r="6" fill="%s"/>' % (cx_, cy_, NAVY, cx_, cy_, NAVY))
    def anchor(id_, side):
        x, y, w, h, k = geo[id_]
        return {'t': (x, y - h / 2), 'b': (x, y + h / 2), 'l': (x - w / 2, y), 'r': (x + w / 2, y)}[side]
    for e in edges:
        a, b, lab, o, i = e[:5]; kw = e[5] if len(e) > 5 else {}
        p, q = anchor(a, o), anchor(b, i)
        cor = kw.get('cor')
        if o == 'b' and i == 't':
            ym = kw.get('ym', (p[1] + q[1]) / 2)
            pts = [p, q] if abs(p[0] - q[0]) < 1 else [p, (p[0], ym), (q[0], ym), q]
        elif o in 'lr' and i in 'lr' and cor is None and abs(p[1] - q[1]) < 1:
            pts = [p, q]
        elif o in 'lr' and i == 't':
            pts = [p, (q[0], p[1]), q]
        elif o == 'b' and i in 'lr':
            pts = [p, (p[0], q[1]), q]
        elif o in 'lr' and i == 'b':
            pts = [p, (q[0], p[1]), q]
        elif o in 'lr' and i in 'lr':
            cx_ = cor if cor is not None else (min(p[0], q[0]) - 60 if o == 'l' else max(p[0], q[0]) + 60)
            pts = [p, (cx_, p[1]), (cx_, q[1]), q]
        elif o == 't' and i == 'b':
            pts = [p, (p[0], p[1] - 20), (cor if cor is not None else p[0] + 100, p[1] - 20), (cor if cor is not None else p[0] + 100, q[1] + 20), (q[0], q[1] + 20), q]
        elif o == 'b' and i == 'b':
            ym = max(p[1], q[1]) + 24
            pts = [p, (p[0], ym), (q[0], ym), q]
        else:
            pts = [p, (q[0], p[1]), q]
        c.conn(pts, lab, dashed=kw.get('dashed', False), lpos=kw.get('lpos', 0.28 if lab else 0.5), loff=kw.get('loff', (0, -9)), size=11.8)
    c.save(os.path.join(OUT, name + '.svg'), os.path.join(OUT, name + '.png'), px_width=2300)

def make():
    swim('activity_onboard', ['Primary User', 'Muhaffiz application'], {
        'st': ('start', 0, 0, ''), 'u1': ('act', 1, 0, 'Open the application'), 'u2': ('act', 2, 0, 'Enter mobile number\nand one-time code'),
        's1': ('act', 3, 1, 'Verify code; create or\nrestore the account', 0, 168), 'u3': ('act', 4, 0, 'Read the consent statement'),
        'd': ('dec', 5, 0, 'Accept?'), 's2': ('act', 6, 1, 'Store consent and time;\nenable feature choices', -88, 168), 's3': ('act', 6, 1, 'Keep microphone features\noff; go to Home', 98, 168),
        'u5': ('act', 7, 0, 'Add at least one trustee'), 'u6': ('act', 8, 0, 'Enter safe and duress phrases;\nspeak three samples each', 0, 200),
        's4': ('act', 9, 1, 'Validate trustee and phrases;\nsave on the device', -30, 190), 's5': ('act', 10, 1, 'Request Android permissions;\nstart services', -30, 190), 's6': ('act', 11, 1, 'Show Home screen', -30, 150), 'en': ('end', 12, 1, '', -30)},
        [('st', 'u1', '', 'b', 't'), ('u1', 'u2', '', 'b', 't'), ('u2', 's1', '', 'r', 't'), ('s1', 'u3', '', 'l', 't'), ('u3', 'd', '', 'b', 't'),
         ('d', 's2', 'yes', 'r', 't', {'lpos': 0.2}), ('d', 's3', 'no', 'r', 't', {'lpos': 0.62, 'loff': (0, -10)}),
         ('s2', 'u5', '', 'l', 't'), ('u5', 'u6', '', 'b', 't'), ('u6', 's4', '', 'r', 't'), ('s4', 's5', '', 'b', 't'), ('s5', 's6', '', 'b', 't'), ('s6', 'en', '', 'b', 't'), ('s3', 'en', '', 'b', 'r')], lw=340)

    swim('activity_child', ['Guardian', 'Muhaffiz', 'Administrator'], {
        'st': ('start', 0, 0, ''), 'g1': ('act', 1, 0, 'Open the report form'), 'g2': ('act', 2, 0, 'Enter child details, photo, last\nseen, contact; confirm guardianship', 0, 210), 'g3': ('act', 3, 0, 'Submit'),
        's1': ('dec', 4, 1, 'Valid?'), 'g4': ('act', 4, 0, 'Correct the entries', 0, 150),
        's3': ('act', 5, 1, 'Store report (active);\nrestrict photo access'), 's4': ('act', 6, 1, 'Alert trustees and helpers\nwithin 5 km'), 's5': ('act', 7, 1, 'Place report in the\nmoderation queue'),
        'a1': ('act', 8, 2, 'Review the report'), 'a2': ('dec', 9, 2, 'False report?'), 'a3': ('act', 10, 2, 'Remove report; may\nsuspend the author', -78, 150), 'a4': ('act', 10, 2, 'Approve: report\nstays active', 78, 150),
        'e2': ('end', 11, 2, '', -78), 'e3': ('end', 11, 2, '', 78), 'st2': ('start', 10, 0, ''), 'g8': ('act', 11, 0, 'Later: mark found, or renew\nbefore 72 hours', 0, 200), 's6': ('act', 12, 1, 'Stop alerts; delete photo;\nset found or expired'), 'en': ('end', 13, 1, '')},
        [('st', 'g1', '', 'b', 't'), ('g1', 'g2', '', 'b', 't'), ('g2', 'g3', '', 'b', 't'), ('g3', 's1', '', 'r', 't'), ('s1', 'g4', 'no', 'l', 'r'), ('g4', 'g2', '', 'l', 'l', {'cor': 40}),
         ('s1', 's3', 'yes', 'b', 't'), ('s3', 's4', '', 'b', 't'), ('s4', 's5', '', 'b', 't'), ('s5', 'a1', '', 'r', 't'), ('a1', 'a2', '', 'b', 't'), ('a2', 'a3', 'yes', 'l', 't', {'lpos': 0.4}), ('a2', 'a4', 'no', 'r', 't', {'lpos': 0.4}),
         ('a3', 'e2', '', 'b', 't'), ('a4', 'e3', '', 'b', 't'), ('st2', 'g8', '', 'b', 't'), ('g8', 's6', '', 'r', 't'), ('s6', 'en', '', 'b', 't')], lw=290)

    swim('activity_report', ['Primary User', 'Application', 'Scheduled function'], {
        'st': ('start', 0, 0, ''), 'u1': ('act', 1, 0, 'Choose category;\nconfirm or move location'), 'u2': ('act', 2, 0, 'Submit'),
        'a1': ('dec', 3, 1, 'Within limits?\n5 per 24 h, no duplicate', 0), 'u9': ('act', 3, 0, 'See rejection message', 0, 160),
        'a3': ('act', 4, 1, 'Write IncidentReport\n(geohash7, time)'), 'b1': ('act', 5, 2, 'Read reports of\nchanged cells'), 'b2': ('act', 6, 2, 'Score = sum of\n0.5 ^ (age / 90 days)'), 'b3': ('act', 7, 2, 'Write CellScore'),
        'b4': ('dec', 8, 2, 'Burst of reports\nin one cell?'), 'b5': ('act', 9, 2, 'Add to moderation queue'), 'u3': ('act', 10, 0, 'Open Danger map; tap a cell'),
        'a4': ('act', 11, 1, 'Read scores; draw cells green\nto red; show zone panel'), 'en': ('end', 12, 0, '')},
        [('st', 'u1', '', 'b', 't'), ('u1', 'u2', '', 'b', 't'), ('u2', 'a1', '', 'r', 't'), ('a1', 'u9', 'no', 'l', 'r'), ('u9', 'en', '', 'l', 'l', {'cor': 40}), ('a1', 'a3', 'yes', 'b', 't'), ('a3', 'b1', 'later', 'r', 't', {'lpos': 0.3}),
         ('b1', 'b2', '', 'b', 't'), ('b2', 'b3', '', 'b', 't'), ('b3', 'b4', '', 'b', 't'), ('b4', 'b5', 'yes', 'b', 't'), ('b4', 'u3', 'no', 'l', 'r', {'cor': 470, 'lpos': 0.15}), ('b5', 'u3', '', 'b', 'r', {'dashed': True}), ('u3', 'a4', '', 'b', 'l'), ('a4', 'en', '', 'b', 'r')], lw=290)

    swim('activity_helper', ['Applicant', 'Application', 'Administrator'], {
        'st': ('start', 0, 0, ''), 'u1': ('act', 1, 0, 'Enter name and phone;\nadd identity document photo'), 'u2': ('act', 2, 0, 'Submit'),
        'a1': ('act', 3, 1, 'Store application (pending);\nrestrict the image'), 'm1': ('act', 4, 2, 'Open the helper review queue'), 'm2': ('act', 5, 2, 'Review the identity photo'), 'm3': ('dec', 6, 2, 'Decision?'),
        'a2': ('act', 7, 1, 'Set Verified Helper;\ndelete the image'), 'a3': ('act', 8, 2, 'Reject; delete the image', 0, 176), 'u3': ('act', 9, 0, 'Receive the result\nnotification'), 'en': ('end', 10, 0, '')},
        [('st', 'u1', '', 'b', 't'), ('u1', 'u2', '', 'b', 't'), ('u2', 'a1', '', 'r', 't'), ('a1', 'm1', '', 'r', 't'), ('m1', 'm2', '', 'b', 't'), ('m2', 'm3', '', 'b', 't'), ('m3', 'a2', 'approve', 'l', 't', {'lpos': 0.3}), ('m3', 'a3', 'reject', 'b', 't'),
         ('a2', 'u3', '', 'b', 'r'), ('a3', 'u3', '', 'l', 't', {'dashed': True}), ('u3', 'en', '', 'b', 't')], lw=290)

    swim('activity_nearhelp', ['Requester', 'Cloud function', 'Verified Helper'], {
        'st': ('start', 0, 0, ''), 'r1': ('act', 1, 0, 'Request nearby help (button, or\nSOS with helpers enabled)', 0, 200), 'r2': ('dec', 2, 0, 'Data connection?'),
        'r3': ('act', 3, 0, 'Show "unavailable";\nqueue the request', 0, 170), 'f1': ('act', 3, 1, 'Find Verified Helpers\nwithin 1 km (geohash)'), 'f2': ('act', 4, 1, 'Send push: distance\nand age, no exact location'),
        'h1': ('act', 5, 2, 'Receive the notification'), 'h2': ('dec', 6, 2, 'Accept?'), 'h3': ('act', 7, 2, 'Close the request'), 'f3': ('act', 7, 1, 'Record acknowledgement;\nreveal exact location\nto this helper'),
        'r4': ('act', 8, 0, 'See that a helper\naccepted', 0, 160), 'en': ('end', 9, 0, '')},
        [('st', 'r1', '', 'b', 't'), ('r1', 'r2', '', 'b', 't'), ('r2', 'r3', 'no', 'b', 't'), ('r2', 'f1', 'yes', 'r', 't', {'lpos': 0.3}), ('f1', 'f2', '', 'b', 't'), ('f2', 'h1', '', 'r', 't'), ('h1', 'h2', '', 'b', 't'),
         ('h2', 'f3', 'yes', 'l', 't', {'lpos': 0.3}), ('h2', 'h3', 'no', 'b', 't'), ('f3', 'r4', '', 'b', 'r'), ('r3', 'en', '', 'l', 'l', {'cor': 30}), ('r4', 'en', '', 'b', 't'), ('h3', 'en', '', 'b', 'b', {'dashed': True})], lw=290)

if __name__ == '__main__': make(); print('ok')
