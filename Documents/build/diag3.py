"""Professional-style SVG primitives: panels with title bars, shadowed boxes, orthogonal connectors."""
import math
from diag import Svg, FONT, clip_rect, head_poly

NAVY = '#1F3864'; BLUE = '#1F4E78'; TEAL = '#0F5C63'; LBLUE = '#EAF1F8'; LTEAL = '#E3F2EE'; AMBER = '#B08900'; LAMBER = '#FFF4D6'; GREY = '#5b6b7a'

DEFS = ''
HDR = {'blue': '#25497A', 'teal': '#0F6068', 'amber': '#A07C0A'}
SHADOW = '#c5cfdb'

class Canvas(Svg):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.defs = DEFS

    def panel(self, x, y, w, h, title, kind='blue', hh=26, fill=None, size=13):
        stroke = {'blue': BLUE, 'teal': TEAL, 'amber': AMBER}[kind]
        body = fill or {'blue': '#F7FAFD', 'teal': '#F4FAF8', 'amber': '#FFFBF0'}[kind]
        hc = HDR[kind]
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="8" fill="%s" fill-opacity="0.55"/>' % (x + 2, y + 3, w, h, SHADOW))
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="8" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, w, h, body, stroke))
        self.add('<path d="M%s,%s a8,8 0 0 1 8,-8 h%s a8,8 0 0 1 8,8 v%s h-%s z" fill="%s"/>' % (x, y + 8, w - 16, hh - 8, w, hc))
        self.text(x + w / 2, y + hh / 2 + 1, title, size, weight='bold', fill='#fff')

    def node(self, x, y, w, h, lines, fill='#fff', stroke=BLUE, size=11.5, bold_first=False, rx=6, dash=None):
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" fill-opacity="0.55"/>' % (x + 1.5, y + 2, w, h, rx, SHADOW))
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="1.3"%s/>' % (
            x, y, w, h, rx, fill, stroke, ' stroke-dasharray="%s"' % dash if dash else ''))
        if isinstance(lines, str): lines = lines.split('\n')
        n = len(lines); lh = size * 1.28; y0 = y + h / 2 - (n - 1) * lh / 2
        for i, l in enumerate(lines):
            self.text(x + w / 2, y0 + i * lh, l, size if not (bold_first and i == 0) else size + 0.5, weight='bold' if (bold_first and i == 0) else 'normal', fill='#17212b' if not (bold_first and i == 0) else NAVY)
        return (x, y, w, h)

    def conn(self, pts, label='', dashed=False, both=False, color=NAVY, lpos=0.5, loff=(0, -9), arrow=True, size=10.5):
        pstr = ' '.join('%.1f,%.1f' % p for p in pts)
        dash = ' stroke-dasharray="6,4"' if dashed else ''
        self.add('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.4"%s/>' % (pstr, color, dash))
        if arrow and len(pts) >= 2: self.add(head_poly(pts[-2], pts[-1], color))
        if both and len(pts) >= 2: self.add(head_poly(pts[1], pts[0], color))
        if label:
            segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
            tot = sum(math.dist(a, b) for a, b in segs); tgt = tot * lpos; acc = 0
            for a, b in segs:
                d = math.dist(a, b)
                if acc + d >= tgt and d > 0:
                    f = (tgt - acc) / d; mx = a[0] + (b[0] - a[0]) * f + loff[0]; my = a[1] + (b[1] - a[1]) * f + loff[1]
                    lines = label.split('\n'); w = max(len(l) for l in lines) * size * 0.56 + 8; h = len(lines) * size * 1.25 + 3
                    self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#fff" fill-opacity="0.92"/>' % (mx - w / 2, my - h / 2, w, h))
                    self.text(mx, my, lines, size, fill='#22303c'); break
                acc += d

    def note(self, x, y, w, h, text, size=10.5):
        self.add('<path d="M%s,%s h%s l8,8 v%s h-%s z" fill="#FFF8DC" stroke="#C9B458" stroke-width="1.1"/>' % (x, y, w - 8, h - 8, w))
        self.text(x + w / 2, y + h / 2, text, size)

def cx(b): return b[0] + b[2] / 2
def cy(b): return b[1] + b[3] / 2
def right(b, t=.5): return (b[0] + b[2], b[1] + b[3] * t)
def left(b, t=.5): return (b[0], b[1] + b[3] * t)
def top(b, t=.5): return (b[0] + b[2] * t, b[1])
def bottom(b, t=.5): return (b[0] + b[2] * t, b[1] + b[3])
