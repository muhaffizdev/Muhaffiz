import os, math
from diag3 import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)
def P(n): return os.path.join(OUT, n + '.svg'), os.path.join(OUT, n + '.png')

def actor(c, x, y, name, ext=False):
    col = '#5b6b7a' if ext else NAVY
    c.add('<circle cx="%s" cy="%s" r="10" fill="#fff" stroke="%s" stroke-width="2"/>' % (x, y - 30, col))
    for a in ((x, y - 20, x, y + 10), (x - 17, y - 10, x + 17, y - 10), (x, y + 10, x - 13, y + 32), (x, y + 10, x + 13, y + 32)):
        c.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % (a + (col,)))
    c.text(x, y + 52, name.split('\n'), 12.8, weight='bold', fill=col, lh=15)

def ucd(name, title, ucs, left, right, links, includes=(), extends=(), gaps=None, ext_actors=(), W=820, rx=140, ry=29, row=76):
    """Single column of use cases inside a system boundary. Actors with 3+ links use a vertical 'bus' with short stubs;
    include relationships between neighbouring use cases are short vertical dashed arrows; extend arrows run on the right side."""
    gaps = gaps or {}
    cxm = 400
    ypos = {}; y = 112
    for k, (uid, lab) in enumerate(ucs):
        if k: y += row + gaps.get(uid, 0)
        ypos[uid] = y
    H0 = int(y + 70)
    bx0, bx1 = 200, 660
    def place(names):
        ys = {}
        for nm in names:
            ls = [ypos[u] for a, u in links if a == nm]
            ys[nm] = sum(ls) / len(ls) if ls else H0 / 2
        last = -999
        for nm in sorted(names, key=lambda k: ys[k]):
            if ys[nm] - last < 135: ys[nm] = last + 135
            last = ys[nm]
        return ys
    ly, ry_ = place(left), place(right)
    H = int(max([H0] + [v + 95 for v in list(ly.values()) + list(ry_.values())]))
    c = Canvas(W, H)
    c.add('<rect x="%s" y="35" width="%s" height="%s" rx="12" fill="%s" fill-opacity="0.55"/>' % (bx0 + 2, bx1 - bx0, H - 52, SHADOW))
    c.add('<rect x="%s" y="32" width="%s" height="%s" rx="12" fill="#FAFCFE" stroke="%s" stroke-width="1.8"/>' % (bx0, bx1 - bx0, H - 52, BLUE))
    c.add('<path d="M%s,44 a12,12 0 0 1 12,-12 h%s a12,12 0 0 1 12,12 v14 h-%s z" fill="#25497A"/>' % (bx0, bx1 - bx0 - 24, bx1 - bx0))
    c.text((bx0 + bx1) / 2, 46, '«system»  ' + title, 13.5, weight='bold', fill='#fff')
    lbus, rbus = 232, 612
    def draw_links(names, ys, side):
        for nm in names:
            ls = sorted(ypos[u] for a, u in links if a == nm)
            ax = 75 + 17 if side == 'l' else W - 75 - 17
            ay = ys[nm] - 10
            ex = cxm - rx if side == 'l' else cxm + rx
            if len(ls) >= 3:
                bx = lbus if side == 'l' else rbus
                c.add('<polyline points="%s,%s %s,%s %s,%s" fill="none" stroke="#40546b" stroke-width="1.4"/>' % (ax, ay, bx, ay, bx, max(min(ay, ls[0]), ls[0]) if False else ay))
                lo, hi = min(ls + [ay]), max(ls + [ay])
                c.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#40546b" stroke-width="1.4"/>' % (bx, lo, bx, hi))
                for yy in ls: c.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#40546b" stroke-width="1.4"/>' % (bx, yy, ex, yy))
            else:
                for yy in ls:
                    c.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#40546b" stroke-width="1.4"/>' % (ax, ay, ex, yy))
    draw_links(left, ly, 'l'); draw_links(right, ry_, 'r')
    for uid, lab in ucs:
        c.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" fill-opacity="0.55"/>' % (cxm + 2, ypos[uid] + 3, rx, ry, SHADOW))
        c.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#EAF1F8" stroke="%s" stroke-width="1.5"/>' % (cxm, ypos[uid], rx, ry, BLUE))
        c.text(cxm, ypos[uid], lab.split('\n'), 13.2, fill='#12202e', lh=16)
    for nm, yy in ly.items(): actor(c, 75, yy, nm, nm in ext_actors)
    for nm, yy in ry_.items(): actor(c, W - 75, yy, nm, nm in ext_actors)
    # include: base -> included, drawn between vertically adjacent use cases
    order = [u[0] for u in ucs]
    for base, inc in includes:
        yb, yi = ypos[base], ypos[inc]
        if abs(order.index(base) - order.index(inc)) == 1:
            sgn = 1 if yi > yb else -1
            p = (cxm + 40, yb + sgn * ry); q = (cxm + 40, yi - sgn * ry)
            c.conn([p, q], '«include»', dashed=True, lpos=0.5, loff=(52, 0), size=11.5)
    for base, ext, lab in extends:
        yb, ye = ypos[base], ypos[ext]
        xo = cxm + rx + 30
        c.conn([(cxm + rx - 4, yb + (8 if ye > yb else -8)), (xo, yb), (xo, ye), (cxm + rx - 6, ye + (-8 if ye > yb else 8))], '«extend»' + ('\n' + lab if lab else ''), dashed=True, lpos=0.5, loff=(0, 0), size=11)
    c.save(*P(name))

def make():
    ucs = [('UC-02', 'UC-02  Handle Automatic\nDistress Alert'), ('UC-01', 'UC-01  Trigger Manual SOS'), ('UC-03', 'UC-03  Trigger SOS by\nVoice Phrase'), ('UC-25', 'UC-25  Escalate to\nAuthorities'),
           ('UC-29', 'UC-29  Acknowledge SOS Alert'), ('UC-24', 'UC-24  Manage Evidence\nRecordings'), ('UC-04', 'UC-04  Manage Trustees'), ('UC-05', 'UC-05  View SOS Event Log'), ('UC-06', 'UC-06  Enrol Safe and\nDuress Phrases')]
    links = [('Primary User', u) for u in ('UC-02', 'UC-01', 'UC-03', 'UC-24', 'UC-04', 'UC-05', 'UC-06')] + [('Trustee', 'UC-29'), ('Trustee', 'UC-01'), ('Verified Helper', 'UC-29'), ('Authority Contact', 'UC-25')]
    ucd('uc_alert', 'Emergency alerting', ucs, ['Primary User'], ['Trustee', 'Verified Helper', 'Authority Contact'], links,
        includes=[('UC-02', 'UC-01'), ('UC-03', 'UC-01')], extends=[('UC-25', 'UC-01', '[no response\nin 3 min]')], gaps={'UC-01': 22, 'UC-03': 22}, ext_actors=('Trustee', 'Verified Helper', 'Authority Contact'))
    ucs = [('UC-07', 'UC-07  Create Circle and\nInvite Member'), ('UC-08', 'UC-08  Share Location and\nView Members'), ('UC-09', 'UC-09  Stop Sharing by\nSafe Phrase'), ('UC-10', 'UC-10  Leave Family Circle'), ('UC-11', 'UC-11  Use Decoy Mode'), ('UC-27', 'UC-27  Change App Disguise')]
    links = [('Primary User', 'UC-07'), ('Primary User', 'UC-11'), ('Primary User', 'UC-27'), ('Family Circle\nMember', 'UC-07'), ('Family Circle\nMember', 'UC-08'), ('Family Circle\nMember', 'UC-09'), ('Family Circle\nMember', 'UC-10')]
    ucd('uc_family', 'Family network and disguise', ucs, ['Primary User'], ['Family Circle\nMember'], links)
    ucs = [('UC-12', 'UC-12  Submit Incident Report'), ('UC-13', 'UC-13  View Danger Heatmap'), ('UC-14', 'UC-14  Register as\nVerified Helper'), ('UC-15', 'UC-15  Request and Respond\nto Nearby Help'), ('UC-23', 'UC-23  File Missing-Child Report'),
           ('UC-16', 'UC-16  Browse Library'), ('UC-17', 'UC-17  Search Library'), ('UC-18', 'UC-18  Call Emergency Service'), ('UC-26', 'UC-26  Navigate to Nearest\nSafe Location')]
    links = [('Primary User', u) for u in ('UC-12', 'UC-13', 'UC-14', 'UC-15', 'UC-16', 'UC-17', 'UC-18', 'UC-26')] + [('Guardian', 'UC-23'), ('Verified Helper', 'UC-15'), ('Verified Helper', 'UC-23'), ('Administrator', 'UC-14')]
    ucd('uc_community', 'Community, library and directory', ucs, ['Primary User', 'Guardian'], ['Verified Helper', 'Administrator'], links, ext_actors=('Verified Helper',))
    ucs = [('UC-19', 'UC-19  Sign Up and Log In'), ('UC-28', 'UC-28  Recover Account'), ('UC-20', 'UC-20  Manage Consent and\nPrivacy Settings'), ('UC-21', 'UC-21  Moderate Reports and\nReview Helpers'), ('UC-22', 'UC-22  Monitor System Health')]
    links = [('Primary User', 'UC-19'), ('Primary User', 'UC-28'), ('Primary User', 'UC-20'), ('Administrator', 'UC-21'), ('Administrator', 'UC-22')]
    ucd('uc_admin', 'Account, consent and administration', ucs, ['Primary User'], ['Administrator'], links, includes=[('UC-28', 'UC-19')], gaps={'UC-28': 22})

def make_all():
    make()
    return {k: (os.path.join(OUT, k + '.svg'), os.path.join(OUT, k + '.png')) for k in ('uc_alert', 'uc_family', 'uc_community', 'uc_admin')}

if __name__ == '__main__': print(make_all())
