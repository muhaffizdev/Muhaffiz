"""Professional UML sequence diagrams (custom SVG): lifelines, activations, numbered messages, combined fragments, notes."""
import os, math
from diag3 import *
from diag import head_poly
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)

def wrap(t, n):
    out = []
    for part in t.split('\n'):
        words = part.split(' '); cur = ''
        for w in words:
            if len(cur) + len(w) + 1 > n and cur: out.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        out.append(cur)
    return out

def actor_icon(c, x, y, col=NAVY):
    c.add('<circle cx="%s" cy="%s" r="7" fill="#fff" stroke="%s" stroke-width="1.6"/>' % (x, y - 15, col))
    for a in ((x, y - 8, x, y + 8), (x - 11, y - 3, x + 11, y - 3), (x, y + 8, x - 8, y + 21), (x, y + 8, x + 8, y + 21)):
        c.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % (a + (col,)))

def sequence(name, parts, steps, colw=140, size=13, numbered=True, rowh=42):
    """parts: [(label, kind)] kind in actor|obj|ext|db ; steps:
       ('m', i, j, text[, 'ret'|'async'])  ('self', i, text)  ('note', i, j, text)  ('act', i, a, b)
       ('frame', kind, [(guard, first_step, last_step), ...])  step indexes refer to positions in `steps` counting only m/self/note rows."""
    n = len(parts)
    W = colw * n + 40 + (int(colw * 0.9) if any(s[0] == 'self' and s[1] == n - 1 for s in steps) else 0)
    X = lambda i: 20 + colw * i + colw / 2
    # vertical layout
    rows = [s for s in steps if s[0] in ('m', 'self', 'note', 'gap')]
    starts = set()
    for f in steps:
        if f[0] == 'frame':
            for _, a, b in f[2]: starts.add(a)
    ys = []; y = 128
    for ri, s in enumerate(rows):
        if s[0] == 'note': h = rowh + (size + 3) * len(wrap(s[-1], int(max(1, (abs(s[2] - s[1]) + 1)) * colw / (size * 0.58)))) + 18
        elif s[0] == 'm':
            span = abs(s[2] - s[1]); lines = wrap(s[3], max(12, int(span * colw / (size * 0.56))))
            h = rowh + (size + 2) * (len(lines) - 1)
        elif s[0] == 'self': h = rowh + 8 + (size + 2) * (len(wrap(s[2], int(colw / (size * 0.56)))) - 1)
        else: h = rowh * 0.5
        if ri in starts: h += 28
        y += h; ys.append(y)
    H = int(y + 70)
    c = Canvas(W, H)
    # lifelines
    for i in range(n):
        c.add('<line x1="%s" y1="92" x2="%s" y2="%s" stroke="#8a9bb0" stroke-width="1.2" stroke-dasharray="6,5"/>' % (X(i), X(i), H - 24))
    # frames (draw below messages)
    frames = [s for s in steps if s[0] == 'frame']
    for f in frames:
        kind, secs = f[1], f[2]
        y0 = ys[secs[0][1]] - rowh * 0.95; y1 = ys[secs[-1][2]] + rowh * 0.6
        c.add('<rect x="10" y="%.1f" width="%d" height="%.1f" fill="none" stroke="#7d8da3" stroke-width="1.3"/>' % (y0, W - 20, y1 - y0))
        tw = len(kind) * 9 + 24
        c.add('<path d="M10,%.1f h%d v14 l-8,8 h-%d z" fill="#DDE7F3" stroke="#7d8da3" stroke-width="1.3"/>' % (y0, tw, tw - 8))
        c.text(10 + tw / 2 - 2, y0 + 10, kind, size - 1.5, weight='bold')
        for k, (guard, a, b) in enumerate(secs):
            ya = ys[a] - rowh * 0.95
            if k > 0:
                c.add('<line x1="10" y1="%.1f" x2="%d" y2="%.1f" stroke="#7d8da3" stroke-width="1.2" stroke-dasharray="7,4"/>' % (ya, W - 10, ya))
            c.text(max(10 + tw + 10, X(0) + 12) if k == 0 else X(0) + 12, (y0 + 10) if k == 0 else ya + 12, '[' + guard + ']', size - 1.8, anchor='start', fill='#33475c', italic=True)
    # activations
    for s in steps:
        if s[0] == 'act':
            _, i, a, b = s
            c.add('<rect x="%s" y="%.1f" width="10" height="%.1f" fill="#DCE9F5" stroke="%s" stroke-width="1.2"/>' % (X(i) - 5, ys[a] - 10, ys[b] - ys[a] + 20, BLUE))
    # participants
    for i, (lab, kind) in enumerate(parts):
        bw = colw - 24; bx = X(i) - bw / 2
        if kind == 'actor':
            actor_icon(c, X(i), 42); c.text(X(i), 80, lab.split('\n'), size - 0.5, weight='bold', fill=NAVY)
        else:
            fill, st = {'obj': (LBLUE, BLUE), 'ext': (LAMBER, AMBER), 'db': (LTEAL, TEAL)}[kind]
            c.node(bx, 18, bw, 62, lab, fill=fill, stroke=st, size=size - 0.8, bold_first=False)
    # messages
    num = 0
    for s, y in zip(rows, ys):
        if s[0] == 'm':
            _, i, j, t = s[:4]; kind = s[4] if len(s) > 4 else 'sync'
            num += 1; lab = ('%d  ' % num if numbered else '') + t
            dash = ' stroke-dasharray="6,4"' if kind == 'ret' else ''
            xa = X(i) + (5 if j > i else -5); xb = X(j) + (-5 if j > i else 5)
            col = NAVY if kind != 'ret' else GREY
            c.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4"%s/>' % (xa, y, xb, y, col, dash))
            c.add(head_poly((xa, y), (xb, y), col))
            span = abs(j - i); lines = wrap(lab, max(12, int(span * colw / (size * 0.56))))
            mx = (xa + xb) / 2
            for k, ln in enumerate(lines):
                c.text(mx, y - 9 - (len(lines) - 1 - k) * (size + 1.5), ln, size, fill='#17212b', italic=(kind == 'ret'))
        elif s[0] == 'self':
            _, i, t = s; num += 1
            x0 = X(i) + 5
            c.add('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="1.4"/>' % (x0, y - 8, x0 + 34, y - 8, x0 + 34, y + 8, x0, y + 8, NAVY))
            c.add(head_poly((x0 + 34, y + 8), (x0, y + 8), NAVY))
            c.text(x0 + 40, y, wrap('%d  %s' % (num, t) if numbered else t, int(colw * 1.0 / (size * 0.56))), size, anchor='start')
        elif s[0] == 'note':
            _, i, j, t = s
            lines = wrap(t, int((abs(j - i) + 1) * colw / (size * 0.58))); w = (abs(j - i) + 1) * colw - 30; x = X(min(i, j)) - colw / 2 + 15
            h = (size + 3) * len(lines) + 8
            c.add('<path d="M%.1f,%.1f h%.1f l9,9 v%.1f h-%.1f z" fill="#FFF8DC" stroke="#C9B458" stroke-width="1.1"/>' % (x, y - h / 2, w - 9, h - 9, w))
            c.text(x + w / 2, y, lines, size - 1.2, lh=size + 2)
    c.save(os.path.join(OUT, name + '.svg'), os.path.join(OUT, name + '.png'), px_width=2300)
