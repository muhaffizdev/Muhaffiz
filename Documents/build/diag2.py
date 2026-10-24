"""Additional diagram helpers: sequence, class, state/graph, mockup phones."""
import math
from diag import *

PRIMARY = '#0F5C63'; DARK = '#10262B'; MINT = '#CDEDE4'; RED = '#C62828'; AMBER = '#F2A900'; GREY = '#E6EAEC'

# ---------------------------------------------------------------- sequence diagram
def sequence(path_svg, path_png, parts, steps, colw=130, top=20, rowh=34, size=11.5):
    """parts: list of names (\\n allowed). steps: ('m', i, j, text[, dashed]) | ('n', i, text) | ('f', label, startstep, endstep) | ('gap',)"""
    W = colw * len(parts) + 40
    x = lambda i: 20 + colw * i + colw / 2
    y = top + 52
    ys = []
    for st in steps:
        if st[0] == 'gap': y += rowh * 0.5; ys.append(y); continue
        y += rowh * (1.3 if st[0] == 'n' else 1); ys.append(y)
    H = int(y + 50)
    s = Svg(W, H)
    for i, p in enumerate(parts):
        s.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#7a8da8" stroke-width="1.2" stroke-dasharray="5,4"/>' % (x(i), top + 40, x(i), H - 15))
    # frames first
    for st, yy in zip(steps, ys):
        pass
    for k, st in enumerate(steps):
        if st[0] == 'f':
            a, b = st[2], st[3]
            y0 = ys[a] - rowh * 0.65; y1 = ys[b] + rowh * 0.45
            s.add('<rect x="12" y="%.1f" width="%d" height="%.1f" fill="none" stroke="#9aa9bd" stroke-width="1.2"/>' % (y0, W - 24, y1 - y0))
            s.add('<rect x="12" y="%.1f" width="%d" height="17" fill="#dfe8f3" stroke="#9aa9bd" stroke-width="1.2"/>' % (y0, 28 + len(st[1]) * 6.2))
            s.text(20, y0 + 8.5, st[1], 11, anchor='start', weight='bold')
    for i, p in enumerate(parts):
        s.box(x(i) - colw / 2 + 8, top, colw - 16, 40, p, size=size, weight='bold', rx=5)
    for st, yy in zip(steps, ys):
        if st[0] == 'm':
            a, b, t = st[1], st[2], st[3]
            dashed = len(st) > 4 and st[4]
            if a == b:
                s.poly([(x(a), yy - 8), (x(a) + 38, yy - 8), (x(a) + 38, yy + 8), (x(a), yy + 8)], arrow=True, dash='4,3' if dashed else None)
                s.text(x(a) + 44, yy, t, size, anchor='start')
            else:
                s.line((x(a), yy), (x(b), yy), dash='5,3' if dashed else None, width=1.4)
                mx = (x(a) + x(b)) / 2
                lines = t.split('\n')
                label(s, mx, yy - 9 - (len(lines) - 1) * 7, t, size - 0.5)
        elif st[0] == 'n':
            i, t = st[1], st[2]
            w = max(len(l) for l in t.split('\n')) * 6.0 + 14
            nx = max(8, x(i) - w / 2)
            s.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff8dc" stroke="#c9b458"/>' % (nx, yy - 15, w, 15 * len(t.split('\n')) + 4))
            s.text(nx + w / 2, yy - 15 + (15 * len(t.split('\n')) + 4) / 2, t, 10.5, lh=13)
    s.save(path_svg, path_png)

# ---------------------------------------------------------------- class diagram
def class_box(s, x, y, w, name, attrs, ops, size=11.5):
    lh = 15
    hn = 24; ha = max(len(attrs), 1) * lh + 8; ho = max(len(ops), 1) * lh + 8
    s.add('<rect x="%s" y="%s" width="%s" height="%s" fill="#fff" stroke="#1F4E78" stroke-width="1.5"/>' % (x, y, w, hn + ha + ho))
    s.add('<rect x="%s" y="%s" width="%s" height="%s" fill="#DCE9F5" stroke="#1F4E78" stroke-width="1.5"/>' % (x, y, w, hn))
    s.text(x + w / 2, y + hn / 2, name, size + 0.5, weight='bold')
    s.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#1F4E78" stroke-width="1.2"/>' % (x, y + hn + ha, x + w, y + hn + ha))
    for i, a in enumerate(attrs): s.text(x + 6, y + hn + 12 + i * lh, a, size - 1, anchor='start')
    for i, o in enumerate(ops): s.text(x + 6, y + hn + ha + 12 + i * lh, o, size - 1, anchor='start')
    return (x, y, w, hn + ha + ho)

def anchor(box, side, t=0.5):
    x, y, w, h = box
    if side == 'l': return (x, y + h * t)
    if side == 'r': return (x + w, y + h * t)
    if side == 't': return (x + w * t, y)
    return (x + w * t, y + h)

def assoc(s, p, q, lab_p='', lab_q='', mid='', via=None, arrow=False, dashed=False, diamond=False, size=11):
    pts = [p] + (via or []) + [q]
    s.poly(pts, arrow=arrow, dash='5,3' if dashed else None, width=1.3)
    def put(pt, other, t, off=12):
        if not t: return
        dx, dy = other[0] - pt[0], other[1] - pt[1]; L = math.hypot(dx, dy) or 1
        s.text(pt[0] + dx / L * 14 + (-dy / L) * 9, pt[1] + dy / L * 14 + (dx / L) * 9, t, size)
    put(p, pts[1], lab_p); put(q, pts[-2], lab_q)
    if mid:
        a, b = pts[len(pts) // 2 - 1], pts[len(pts) // 2]
        label(s, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 8, mid, size - 0.5)

# ---------------------------------------------------------------- state / activity helpers
def state(s, x, y, w, h, text, fill='#EAF1F8', size=12, stroke='#1F4E78', rx=14):
    s.box(x, y, w, h, text, fill=fill, stroke=stroke, size=size, rx=rx)
    return (x, y, w, h)

def dot(s, cx, cy, r=8):
    s.add('<circle cx="%s" cy="%s" r="%s" fill="#1F3864"/>' % (cx, cy, r))
def final(s, cx, cy, r=10):
    s.add('<circle cx="%s" cy="%s" r="%s" fill="#fff" stroke="#1F3864" stroke-width="1.8"/><circle cx="%s" cy="%s" r="%s" fill="#1F3864"/>' % (cx, cy, r, cx, cy, r - 4))
def diamond(s, cx, cy, w=60, h=38, text='', size=11):
    s.add('<polygon points="%s,%s %s,%s %s,%s %s,%s" fill="#FFF4CC" stroke="#B08900" stroke-width="1.5"/>' % (cx, cy - h / 2, cx + w / 2, cy, cx, cy + h / 2, cx - w / 2, cy))
    if text: s.text(cx, cy, text, size)

def arrow(s, pts, text='', size=11, dashed=False, tpos=0.5, toff=(0, -9)):
    s.poly(pts, arrow=True, dash='5,3' if dashed else None, width=1.4)
    if text:
        # label on segment containing tpos of total length
        segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        tot = sum(math.dist(a, b) for a, b in segs); acc = 0; target = tot * tpos
        for a, b in segs:
            d = math.dist(a, b)
            if acc + d >= target:
                f = (target - acc) / d if d else 0
                label(s, a[0] + (b[0] - a[0]) * f + toff[0], a[1] + (b[1] - a[1]) * f + toff[1], text, size - 0.5); break
            acc += d

# ---------------------------------------------------------------- mockup phone widgets
class Ph:
    def __init__(self, s, ox, oy, w=250, h=500, title=''):
        self.s, self.ox, self.oy, self.w, self.h = s, ox, oy, w, h
        s.add('<rect x="%s" y="%s" width="%s" height="%s" rx="26" fill="#1c2a33"/>' % (ox, oy, w + 16, h + 16))
        s.add('<rect x="%s" y="%s" width="%s" height="%s" rx="19" fill="#ffffff"/>' % (ox + 8, oy + 8, w, h))
        s.add('<rect x="%s" y="%s" width="%s" height="20" rx="0" fill="#f1f4f5"/>' % (ox + 8, oy + 8, w))
        s.text(ox + 24, oy + 18, '9:41', 9.5, anchor='start', weight='bold', fill='#333')
        s.text(ox + w - 12, oy + 18, '●●●  T2', 8.5, anchor='end', fill='#333')
        self.X = ox + 8; self.Y = oy + 8
    def rect(self, x, y, w, h, fill='#fff', stroke=None, rx=6, sw=1):
        self.s.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>' % (self.X + x, self.Y + y, w, h, rx, fill, (' stroke="%s" stroke-width="%s"' % (stroke, sw)) if stroke else ''))
    def text(self, x, y, t, size=11, anchor='middle', weight='normal', fill='#222'):
        self.s.text(self.X + x, self.Y + y, t, size, anchor=anchor, weight=weight, fill=fill)
    def appbar(self, title, back=True):
        self.rect(0, 20, self.w, 40, fill=PRIMARY, rx=0)
        self.text(34 if back else 14, 40, ('←  ' if back else '') + title, 12.5, anchor='start', weight='bold', fill='#fff')
    def button(self, x, y, w, h, label, fill=PRIMARY, tf='#fff', size=11.5, rx=10):
        self.rect(x, y, w, h, fill=fill, rx=rx); self.text(x + w / 2, y + h / 2, label, size, weight='bold', fill=tf)
    def card(self, x, y, w, h, lines, size=10.5, fill='#F4F8F8', align='start', bold_first=True):
        self.rect(x, y, w, h, fill=fill, stroke='#cfd8dc', rx=8)
        n = len(lines); lh = min(15, (h - 10) / max(n, 1))
        for i, l in enumerate(lines):
            self.text(x + 10 if align == 'start' else x + w / 2, y + 12 + i * lh, l, size, anchor=align, weight='bold' if (i == 0 and bold_first) else 'normal')
    def field(self, x, y, w, label, val=''):
        self.rect(x, y, w, 32, fill='#fff', stroke='#90a4ae', rx=6)
        self.text(x + 8, y + 10, label, 8.5, anchor='start', fill='#607d8b')
        self.text(x + 8, y + 23, val, 10.5, anchor='start')
    def switch(self, x, y, on=True):
        self.rect(x, y, 34, 17, fill=PRIMARY if on else '#b0bec5', rx=9)
        self.s.add('<circle cx="%s" cy="%s" r="7" fill="#fff"/>' % (self.X + x + (25 if on else 9), self.Y + y + 8.5))
    def chip(self, x, y, label, on=False):
        w = len(label) * 6.2 + 16
        self.rect(x, y, w, 22, fill=MINT if on else '#eceff1', stroke=PRIMARY if on else None, rx=11); self.text(x + w / 2, y + 11, label, 9.5)
        return w
    def nav(self, active=0):
        self.rect(0, self.h - 44, self.w, 44, fill='#f4f7f7', rx=0)
        labs = ['Home', 'Family', 'Map', 'Library', 'More']
        for i, l in enumerate(labs):
            cx = self.w / 10 + i * self.w / 5
            self.s.add('<circle cx="%s" cy="%s" r="8" fill="%s"/>' % (self.X + cx, self.Y + self.h - 30, PRIMARY if i == active else '#b0bec5'))
            self.text(cx, self.h - 13, l, 8.5, weight='bold' if i == active else 'normal', fill=PRIMARY if i == active else '#555')
    def status_strip(self, y=68):
        self.rect(10, y, self.w - 20, 24, fill=MINT, rx=12)
        self.text(self.w / 2, y + 12, 'Tier 3  •  Detection on  •  Voice on', 9.5, fill=DARK)
    def map(self, x, y, w, h, cells=None, markers=None):
        self.rect(x, y, w, h, fill='#dfeee9', stroke='#c3d6cf', rx=6)
        for i in range(1, 6):
            self.s.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#c9ddd5" stroke-width="1"/>' % (self.X + x, self.Y + y + h * i / 6, self.X + x + w, self.Y + y + h * i / 6))
            self.s.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#c9ddd5" stroke-width="1"/>' % (self.X + x + w * i / 6, self.Y + y, self.X + x + w * i / 6, self.Y + y + h))
        for (cx, cy, c) in (cells or []):
            self.s.add('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" fill-opacity="0.55"/>' % (self.X + x + cx * w / 6, self.Y + y + cy * h / 6, w / 6, h / 6, c))
        for (mx, my, c, t) in (markers or []):
            self.s.add('<circle cx="%s" cy="%s" r="8" fill="%s" stroke="#fff" stroke-width="2"/>' % (self.X + x + mx * w, self.Y + y + my * h, c))
            if t: self.text(x + mx * w, y + my * h + 20, t, 9, weight='bold')

def phones(path_svg, path_png, builders, titles, ph_w=250, ph_h=500, gap=22):
    n = len(builders)
    W = n * (ph_w + 16) + (n + 1) * gap
    H = ph_h + 16 + 56
    s = Svg(W, H)
    for i, (b, t) in enumerate(zip(builders, titles)):
        ox = gap + i * (ph_w + 16 + gap)
        p = Ph(s, ox, 8, ph_w, ph_h)
        b(p)
        s.text(ox + (ph_w + 16) / 2, ph_h + 16 + 28, t, 13, weight='bold', fill=DARK)
    s.save(path_svg, path_png)

def browser(path_svg, path_png, title, builder, W=860, H=470):
    s = Svg(W, H)
    s.add('<rect x="6" y="6" width="%d" height="%d" rx="10" fill="#fff" stroke="#9aa9bd" stroke-width="2"/>' % (W - 12, H - 12))
    s.add('<rect x="6" y="6" width="%d" height="30" rx="10" fill="#e8edf2"/>' % (W - 12))
    for i, c in enumerate(('#e57373', '#ffd54f', '#81c784')): s.add('<circle cx="%d" cy="21" r="5" fill="%s"/>' % (24 + i * 16, c))
    s.add('<rect x="100" y="12" width="420" height="18" rx="9" fill="#fff" stroke="#c5ced8"/>')
    s.text(112, 21, 'https://muhaffiz.me/' + title, 10.5, anchor='start', fill='#444')
    builder(s)
    s.save(path_svg, path_png)
