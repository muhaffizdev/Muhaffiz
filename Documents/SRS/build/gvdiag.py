"""Graphviz-based diagram rendering (WASM Graphviz through Node) with one consistent visual style."""
import os, re, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)
FONT = 'Liberation Sans'
NAVY = '#1F3864'; BLUE = '#1F4E78'; TEAL = '#0F5C63'; LBLUE = '#EAF1F8'; LTEAL = '#E3F2EE'; AMBER = '#B08900'; LAMBER = '#FFF4D6'; GREY = '#5b6b7a'; LGREY = '#F2F5F7'

def style(rankdir='TB', extra='', nodesep=0.3, ranksep=0.5, splines='true'):
    return ('graph [rankdir=%s, fontname="%s", fontsize=13, nodesep=%s, ranksep=%s, splines=%s, pad=0.25, compound=true, newrank=true, bgcolor="white" %s];\n'
            'node [shape=box, style="rounded,filled", fillcolor="%s", color="%s", fontname="%s", fontsize=11, penwidth=1.3, margin="0.14,0.07"];\n'
            'edge [color="%s", fontname="%s", fontsize=10, arrowsize=0.8, penwidth=1.2];\n') % (rankdir, FONT, nodesep, ranksep, splines, extra, LBLUE, BLUE, FONT, NAVY, FONT)

def cluster(name, label, body, fill='#FAFCFD', color=TEAL, pen=1.8, fontcolor=None, labeljust='c', style_='rounded,filled'):
    return ('subgraph cluster_%s {\n label=<<B>%s</B>>; style="%s"; fillcolor="%s"; color="%s"; penwidth=%s; fontcolor="%s"; labeljust=%s; fontsize=12; margin=14;\n%s\n}\n'
            % (name, label, style_, fill, color, pen, fontcolor or color, labeljust, body))

def render(name, dot, engine='dot', png_w=2300):
    svgp = os.path.join(OUT, name + '.svg'); pngp = os.path.join(OUT, name + '.png')
    with tempfile.NamedTemporaryFile('w', suffix='.dot', delete=False, encoding='utf8') as f:
        f.write(dot); tmp = f.name
    r = subprocess.run(['node', os.path.join(HERE, 'dot_render.mjs'), tmp, svgp, engine], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0: raise RuntimeError('dot failed for %s: %s' % (name, r.stderr[-800:]))
    s = open(svgp, encoding='utf8').read()
    s = re.sub(r'<!DOCTYPE[^>]*>\s*', '', s); s = re.sub(r'<!--.*?-->\s*', '', s, flags=re.S)
    # Word-friendly: pixel sizes instead of pt
    s = re.sub(r'<svg width="([\d.]+)pt" height="([\d.]+)pt"', lambda m: '<svg width="%dpx" height="%dpx"' % (round(float(m.group(1)) * 4 / 3), round(float(m.group(2)) * 4 / 3)), s)
    open(svgp, 'w', encoding='utf8').write(s)
    subprocess.run(['rsvg-convert', '-w', str(png_w), '-o', pngp, svgp], check=True)
    return svgp, pngp
