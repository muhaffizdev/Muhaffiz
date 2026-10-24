import re, glob, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams')
LAND = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else set()
def audit():
    out = []
    for f in sorted(glob.glob(os.path.join(D, '*.svg'))):
        s = open(f, encoding='utf8').read()
        tag = re.search(r'<svg[^>]*>', s).group(0)
        mw = re.search(r'width="([\d.]+)', tag); mh = re.search(r'height="([\d.]+)', tag)
        if not (mw and mh): continue
        w, h = float(mw.group(1)), float(mh.group(1))
        name = os.path.basename(f)[:-4]
        land = name in LAND
        max_w, max_h = (10.2, 5.7) if land else (6.3, 8.3)
        disp_w = min(max_w, max_h * w / h)
        scale = disp_w * 96 / w  # display px per svg px at 96 dpi
        fs = [float(x) for x in re.findall(r'font-size="([\d.]+)', s)]
        fs += [float(x) * 4 / 3 for x in re.findall(r'font-size="([\d.]+)pt', s)] if False else []
        if not fs: continue
        fs.sort(); p10 = fs[max(0, len(fs) // 10)]; med = fs[len(fs) // 2]
        # graphviz svg is in pt with viewBox scaled: font-size attribute is in user units (pt); our px conversion changed width only
        k = 0.75 if 'viewBox' not in tag or 'xmlns:xlink' not in tag else 1.0
        out.append((name, int(w), int(h), round(disp_w, 1), round(p10 * k * scale, 1), round(med * k * scale, 1), 'L' if land else 'P'))
    return out
if __name__ == '__main__':
    for r in audit(): print(r)
