"""Tiny SVG diagram helper (no external layout engine): boxes, ellipses, arrows with labels."""
import math, subprocess, os

FONT = "Liberation Sans, Arial, Helvetica, sans-serif"

def head_poly(p, q, color='#1F3864', size=9):
    """Filled arrowhead at q for a segment p->q, as a plain polygon (portable: no SVG markers)."""
    dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    bx, by = q[0] - ux * size, q[1] - uy * size
    nx, ny = -uy * size * 0.42, ux * size * 0.42
    return '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (q[0], q[1], bx + nx, by + ny, bx - nx, by - ny, color)

class Svg:
    def __init__(self, w, h, bg='#ffffff'):
        self.w, self.h = w, h
        self.items = []
        self.defs = ''
        self.bg = bg
    def add(self, s): self.items.append(s)
    def text(self, x, y, lines, size=13, anchor='middle', weight='normal', fill='#111', italic=False, lh=None):
        if isinstance(lines, str): lines = lines.split('\n')
        lh = lh or size * 1.25
        y0 = y - (len(lines) - 1) * lh / 2 + size * 0.34
        out = []
        for i, ln in enumerate(lines):
            ln = ln.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            out.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s"%s>%s</text>' % (
                x, y0 + i * lh, FONT, size, anchor, weight, fill, ' font-style="italic"' if italic else '', ln))
        self.add(''.join(out))
    def box(self, x, y, w, h, lines, fill='#EAF1F8', stroke='#1F4E78', size=13, weight='normal', rx=8, dash=None, tfill='#111'):
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="1.6"%s/>' % (
            x, y, w, h, rx, fill, stroke, ' stroke-dasharray="%s"' % dash if dash else ''))
        if lines: self.text(x + w / 2, y + h / 2, lines, size, weight=weight, fill=tfill)
    def ellipse(self, cx, cy, rx, ry, lines, fill='#1F4E78', stroke='#10294A', size=15, tfill='#fff', weight='bold'):
        self.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (cx, cy, rx, ry, fill, stroke))
        self.text(cx, cy, lines, size, weight=weight, fill=tfill)
    def line(self, p, q, arrow=True, both=False, color='#1F3864', dash=None, width=1.5):
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (
            p[0], p[1], q[0], q[1], color, width, ' stroke-dasharray="%s"' % dash if dash else ''))
        if arrow: self.add(head_poly(p, q, color))
        if both: self.add(head_poly(q, p, color))
    def poly(self, pts, arrow=True, color='#1F3864', dash=None, width=1.5):
        s = ' '.join('%.1f,%.1f' % p for p in pts)
        self.add('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (s, color, width, ' stroke-dasharray="%s"' % dash if dash else ''))
        if arrow and len(pts) >= 2: self.add(head_poly(pts[-2], pts[-1], color))
    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
                '<rect width="%d" height="%d" fill="%s"/>%s</svg>') % (self.w, self.h, self.w, self.h, self.w, self.h, self.bg, ''.join(self.items))
    def save(self, path_svg, path_png, px_width=2000):
        open(path_svg, 'w', encoding='utf8').write(self.svg())
        subprocess.run(['rsvg-convert', '-w', str(px_width), '-o', path_png, path_svg], check=True)

def clip_rect(cx, cy, w, h, tx, ty):
    """point on rectangle (centre cx,cy size w,h) boundary towards (tx,ty)"""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0: return cx, cy
    sx = (w / 2) / abs(dx) if dx else 1e9
    sy = (h / 2) / abs(dy) if dy else 1e9
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s

def clip_ellipse(cx, cy, rx, ry, tx, ty):
    dx, dy = tx - cx, ty - cy
    k = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx * k, cy + dy * k

def flow(svg, ent, ell, out_label, in_label, off=9, lab_off=None, size=12.5, t_out=0.5, t_in=0.5):
    """Two parallel arrows between an entity box ent=(cx,cy,w,h) and an ellipse ell=(cx,cy,rx,ry).
    out_label: flow entity -> system, in_label: system -> entity (either may be None)."""
    ex, ey, ew, eh = ent; cx, cy, rx, ry = ell
    p = clip_rect(ex, ey, ew, eh, cx, cy)
    q = clip_ellipse(cx, cy, rx, ry, ex, ey)
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    both = out_label and in_label
    o = off if both else 0
    def lo(txt):
        if lab_off is not None: return lab_off
        n = len(txt.split('\n')); sign = 1
        return o + 10 + n * size * 0.7
    if out_label:
        a = (p[0] + nx * o, p[1] + ny * o); b = (q[0] + nx * o, q[1] + ny * o)
        svg.line(a, b)
        mx, my = a[0] + (b[0] - a[0]) * t_out, a[1] + (b[1] - a[1]) * t_out
        svg.add('<g>')
        label(svg, mx + nx * lo(out_label), my + ny * lo(out_label), out_label, size)
        svg.add('</g>')
    if in_label:
        a = (q[0] - nx * o, q[1] - ny * o); b = (p[0] - nx * o, p[1] - ny * o)
        svg.line(a, b)
        mx, my = a[0] + (b[0] - a[0]) * t_in, a[1] + (b[1] - a[1]) * t_in
        label(svg, mx - nx * lo(in_label), my - ny * lo(in_label), in_label, size)

def label(svg, x, y, text, size=11):
    lines = text.split('\n')
    wmax = max(len(l) for l in lines) * size * 0.54 + 6
    hh = len(lines) * size * 1.25 + 2
    svg.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff" fill-opacity="0.88"/>' % (x - wmax / 2, y - hh / 2, wmax, hh))
    svg.text(x, y, lines, size, fill='#1a1a1a')

# ---------------------------------------------------------------- use-case diagram
def actor(svg, x, y, name, size=13):
    svg.add('<circle cx="%s" cy="%s" r="9" fill="#fff" stroke="#1F3864" stroke-width="1.8"/>' % (x, y - 26))
    svg.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#1F3864" stroke-width="1.8"/>' % (x, y - 17, x, y + 8))
    svg.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#1F3864" stroke-width="1.8"/>' % (x - 15, y - 8, x + 15, y - 8))
    svg.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#1F3864" stroke-width="1.8"/>' % (x, y + 8, x - 12, y + 28))
    svg.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#1F3864" stroke-width="1.8"/>' % (x, y + 8, x + 12, y + 28))
    svg.text(x, y + 46, name, size, weight='bold')

def usecase_diagram(path_svg, path_png, system_name, ucs, left, right, links, W=800, row=64, rx=150, ry=25):
    """ucs: list of (id, label with \\n); left/right: list of actor names; links: list of (actor, uc id)."""
    n = len(ucs)
    ypos = {uid: 105 + i * row for i, (uid, lab) in enumerate(ucs)}
    H0 = 100 + n * row + 30
    def place(names):
        ys = {}
        for nm in names:
            ls = [ypos[u] for a, u in links if a == nm]
            ys[nm] = sum(ls) / len(ls) if ls else H0 / 2
        last = -999
        for nm in sorted(names, key=lambda k: ys[k]):
            if ys[nm] - last < 125: ys[nm] = last + 125
            last = ys[nm]
        return ys
    ly = place(left); ry_ = place(right)
    H = int(max([H0] + [y + 75 for y in list(ly.values()) + list(ry_.values())]))
    s = Svg(W, H)
    bx0, bx1 = 215, W - 215
    s.add('<rect x="%s" y="40" width="%s" height="%s" rx="10" fill="#fafcff" stroke="#1F4E78" stroke-width="1.8"/>' % (bx0, bx1 - bx0, H - 60))
    s.text((bx0 + bx1) / 2, 58, system_name, 14, weight='bold', fill='#1F3864')
    cx = W / 2
    for a, u in links:
        if a in ly: ax, ay = 85 + 15, ly[a] - 8
        else: ax, ay = W - 85 - 15, ry_[a] - 8
        q = clip_ellipse(cx, ypos[u], rx, ry, ax, ay)
        s.line((ax, ay), q, arrow=False, width=1.2, color='#3a5a85')
    for uid, lab in ucs:
        s.ellipse(cx, ypos[uid], rx, ry, lab, fill='#EAF1F8', stroke='#1F4E78', size=12.5, tfill='#111', weight='normal')
    for nm, y in ly.items(): actor(s, 85, y, nm)
    for nm, y in ry_.items(): actor(s, W - 85, y, nm)
    s.save(path_svg, path_png)
    return H
