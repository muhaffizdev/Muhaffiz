import os
from diag3 import *
from diag import clip_rect, clip_ellipse
import math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)

def _unused(): pass
def flow(c, ent, ell, out_label, in_label, off=10, size=12.8, t_out=0.5, t_in=0.5):
    ex, ey, ew, eh = ent; cx, cy, rx, ry = ell
    p = clip_rect(ex, ey, ew, eh, cx, cy); q = clip_ellipse(cx, cy, rx, ry, ex, ey)
    dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    both = out_label and in_label; o = off if both else 0
    def lab(txt, a, b, t, sign):
        lines = txt.split('\n'); n = len(lines)
        mx, my = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        d = o + 12 + n * size * 0.62
        w = max(len(l) for l in lines) * size * 0.55 + 8; h = n * size * 1.25 + 3
        x, y = mx + sign * nx * d, my + sign * ny * d
        c.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#fff" fill-opacity="0.9"/>' % (x - w / 2, y - h / 2, w, h)); c.text(x, y, lines, size, fill='#1a1a1a')
    if out_label:
        a = (p[0] + nx * o, p[1] + ny * o); b = (q[0] + nx * o, q[1] + ny * o); c.line(a, b); lab(out_label, a, b, t_out, 1)
    if in_label:
        a = (q[0] - nx * o, q[1] - ny * o); b = (p[0] - nx * o, p[1] - ny * o); c.line(a, b); lab(in_label, a, b, t_in, -1)

def make():
    W, H = 820, 660
    c = Canvas(W, H)
    cx, cy, rx, ry = 410, 330, 128, 82
    c.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" fill-opacity="0.55"/>' % (cx + 3, cy + 4, rx, ry, SHADOW))
    c.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#244777" stroke="#10294A" stroke-width="2"/>' % (cx, cy, rx, ry))
    c.text(cx, cy - 22, 'Muhaffiz', 20, weight='bold', fill='#fff')
    c.text(cx, cy + 16, ['Android application,', 'Firebase backend,', 'admin website'], 13, fill='#E3ECF8', lh=16)
    BW, BH = 160, 54
    ents = {'user': (90, 95, 'Primary User', False), 'family': (90, 330, 'Family Circle\nMember', False), 'helper': (90, 565, 'Verified Helper', False),
            'admin': (730, 95, 'Administrator', False), 'maps': (730, 330, 'Google Maps\nPlatform', True), 'email': (730, 565, 'Email Provider', True),
            'auth': (265, 36, 'Authority Contact', False), 'trust': (555, 36, 'Trustee', False), 'wa': (320, 624, 'WhatsApp', True), 'sms': (570, 624, 'Cellular SMS\nNetwork', True)}
    for k, (x, y, t, ext) in ents.items():
        c.node(x - BW / 2, y - BH / 2, BW, BH, t, fill=LAMBER if ext else LBLUE, stroke=AMBER if ext else BLUE, size=13.5, bold_first=False)
    E = lambda k: (ents[k][0], ents[k][1], BW, BH); ell = (cx, cy, rx, ry)
    flow(c, E('user'), ell, 'SOS trigger, settings,\nreports, searches', 'alerts, map,\nlibrary results', t_out=0.4, t_in=0.55)
    flow(c, E('family'), ell, 'location,\nopt-out', "members' status")
    flow(c, E('helper'), ell, 'accept /\ndecline', 'help\nrequests', t_out=0.45, t_in=0.55)
    flow(c, E('admin'), ell, 'approvals,\nmoderation', 'reports, queues,\nsystem health', t_out=0.4, t_in=0.55)
    flow(c, E('maps'), ell, 'map tiles', 'map requests')
    flow(c, E('email'), ell, 'delivery\nstatus', 'email alerts', t_out=0.45, t_in=0.55)
    flow(c, E('auth'), ell, None, 'escalation\nmessage')
    flow(c, E('trust'), ell, 'acknowledgement', 'SOS alert', t_out=0.4, t_in=0.55)
    flow(c, E('wa'), ell, None, 'SOS share link')
    flow(c, E('sms'), ell, None, 'SMS alert')
    c.node(20, 20, 0, 0, '')
    c.save(os.path.join(OUT, 'context.svg'), os.path.join(OUT, 'context.png'), px_width=2300)
    return os.path.join(OUT, 'context.svg'), os.path.join(OUT, 'context.png')

if __name__ == '__main__': print(make())
