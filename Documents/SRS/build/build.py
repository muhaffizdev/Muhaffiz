import sys, os, shutil, zipfile, subprocess, copy, importlib
sys.path.insert(0, os.path.dirname(__file__))
from srslib import *

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(HERE)   # Documents/SRS
TEMPLATE = os.path.join(DOCS, '..', 'Reference', 'SRS-Template.docx')
WORK = os.environ.get('SRS_WORK', '/tmp/srs_work')
OUT = os.path.join(DOCS, 'Muhaffiz-SRS-SDS.docx')

TITLE = 'Muhaffiz: Offline-First Safety for Women and Children'
CHAPTERS = {}   # chapter number -> module name, if written
for n in range(1, 7):
    if os.path.exists(os.path.join(HERE, 'ch%d.py' % n)):
        CHAPTERS[n] = 'ch%d' % n

def set_text(p, text):
    ts = p.findall('.//w:t', ns)
    ts[0].text = text
    ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    for t in ts[1:]:
        r = t.getparent(); r.getparent().remove(r)

def is_blank(el):
    if etree.QName(el).localname != 'p': return False
    if ''.join(el.itertext()).strip(): return False
    if el.findall('.//w:sectPr', ns) or el.findall('.//w:drawing', ns) or el.findall('.//w:object', ns): return False
    return True

def clear_enter(tbl):
    for t in tbl.findall('.//w:t', ns):
        if t.text and t.text.strip() == '[Enter]': t.text = ''

def front_matter(body):
    B = list(body)
    p = lambda i: B[i]
    set_text(p(4), TITLE)
    # students
    for i, (name, num) in ((7, ('Muhammad Shamoil', '232025')), (8, ('Ali Raza', '232047'))):
        ts = p(i).findall('.//w:t', ns)
        ts[0].text = name + '      '; ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        ts[1].text = num
        r = ts[2].getparent(); r.getparent().remove(r)
    # numbers: make plain (the template italic 'xxxx' run is removed)
    body.remove(p(9))       # third student line removed
    ts = p(11).findall('.//w:t', ns); ts[-1].text = 'Kanwal Batool'
    ts = p(14).findall('.//w:t', ns); ts[0].text = 'Bachelor of Science in Software Engineering (2023-2027)'
    for t in ts[1:]: t.text = ''
    # front-matter headings
    for i in (15, 20, 25):
        st = p(i).find('w:pPr/w:pStyle', ns); st.set('{%s}val' % W, 'FrontHeading')
    for i in (16, 21): body.remove(p(i))
    for i in (18, 23): clear_enter(p(i))
    for i in (18, 23, 26):
        for r in p(i).findall('.//w:r', ns):
            rpr = r.find('w:rPr', ns)
            if rpr is None:
                rpr = etree.SubElement(r, '{%s}rPr' % W); r.insert(0, rpr)
            for tag in ('sz', 'szCs'):
                e = rpr.find('w:%s' % tag, ns)
                if e is None: e = etree.SubElement(rpr, '{%s}%s' % (W, tag))
                e.set('{%s}val' % W, '18')
            f = rpr.find('w:rFonts', ns)
            if f is None:
                f = etree.Element('{%s}rFonts' % W); rpr.insert(0, f)
            for a in ('ascii', 'hAnsi', 'cs'): f.set('{%s}%s' % (W, a), 'Times New Roman')
    # approval table: supervisor name
    tbl = p(26)
    cells = tbl.findall('.//w:tr', ns)[1].findall('w:tc', ns)
    for t in cells[1].findall('.//w:t', ns):
        if t.text and t.text.strip() == '[Enter]': t.text = 'Kanwal Batool'
    B2 = list(body)
    return B2

def set_props(work):
    import re
    p = os.path.join(work, 'docProps', 'core.xml')
    if os.path.exists(p):
        s = open(p, encoding='utf8').read()
        s = re.sub(r'<dc:title>.*?</dc:title>|<dc:title/>', '<dc:title>%s: SRS and SDS</dc:title>' % TITLE, s) if '<dc:title' in s else s.replace('</cp:coreProperties>', '<dc:title>%s: SRS and SDS</dc:title></cp:coreProperties>' % TITLE)
        s = re.sub(r'<dc:creator>.*?</dc:creator>|<dc:creator/>', '<dc:creator>Muhammad Shamoil, Ali Raza</dc:creator>', s)
        s = re.sub(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>|<cp:lastModifiedBy/>', '<cp:lastModifiedBy>Muhammad Shamoil</cp:lastModifiedBy>', s)
        open(p, 'w', encoding='utf8').write(s)

def build(pages=None):
    if os.path.exists(WORK): shutil.rmtree(WORK)
    os.makedirs(WORK)
    with zipfile.ZipFile(TEMPLATE) as z: z.extractall(WORK)
    ctx = Ctx(); ctx.nums = []
    ctx.pages = pages or {}
    doc_path = os.path.join(WORK, 'word', 'document.xml')
    tree = etree.parse(doc_path); root = tree.getroot()
    body = root.find('w:body', ns)
    orig = list(body)
    final_sect = orig[-1]
    idx = {i: orig[i] for i in range(len(orig))}
    # keep references to the chapter ranges before front-matter edits (which remove elements)
    rng = {1: (46, 109), 2: (109, 155), 3: (155, 212), 4: (212, 280), 5: (280, 321), 6: (321, 390)}
    chap_els = {n: [idx[i] for i in range(a, b_)] for n, (a, b_) in rng.items()}
    refs_el = idx[390]
    sect45 = idx[45]
    front = front_matter(body)   # edits in place
    front_els = [e for e in front if e in set(idx[i] for i in range(0, 32))]
    blocks = [RAW(e) for e in front_els if e is not None]
    blocks.append(dict(k='toc'))
    blocks.append(RAW(sect45))
    mods = {}
    for n in range(1, 7):
        if n in CHAPTERS:
            m = importlib.import_module(CHAPTERS[n]); importlib.reload(m)
            blocks += m.blocks(ctx)
        else:
            els = [e for e in chap_els[n] if not is_blank(e)]
            blocks += raw_to_blocks(els)
    blocks.append(H1('References', 'refs', numbered=False))
    import refs; importlib.reload(refs)
    ctx.cite_defs = refs.DEFS
    blocks.append(dict(k='refs'))
    import ch_end; importlib.reload(ch_end)
    blocks += ch_end.blocks(ctx)
    # emit
    elems = emit_all(blocks, ctx)
    for el in list(body): body.remove(el)
    for el in elems: body.append(el)
    if getattr(ctx, 'sect_started', False):
        pn = final_sect.find('w:pgNumType', ns)
        if pn is not None: final_sect.remove(pn)
    body.append(final_sect)
    tree.write(doc_path, xml_declaration=True, encoding='UTF-8', standalone=True)
    patch_styles(os.path.join(WORK, 'word', 'styles.xml'))
    patch_numbering(os.path.join(WORK, 'word', 'numbering.xml'), ctx.nums)
    set_props(WORK)
    write_package(WORK, OUT, ctx)
    return ctx

def render(out_docx, outdir):
    soffice = '/home/shamoil/.config/Claude/local-agent-mode-sessions/skills-plugin/5171dce9-e27b-4924-a547-b705c8d490da/553cb02d-fcb0-4d59-be5c-7272162dcefa/skills/docx/scripts/office/soffice.py'
    os.makedirs(outdir, exist_ok=True)
    subprocess.run(['python3', soffice, '--headless', '--convert-to', 'pdf', '--outdir', outdir, out_docx],
                   capture_output=True, timeout=600)
    return os.path.join(outdir, os.path.basename(out_docx).replace('.docx', '.pdf'))

if __name__ == '__main__':
    rdir = os.environ.get('SRS_RENDER', '/tmp/srs_render')
    ctx = build()
    pdf = render(OUT, rdir)
    pg = find_pages(pdf, ctx)
    ctx = build(pg)
    pdf = render(OUT, rdir)
    print('headings', len(ctx.headings), 'captions', len(ctx.captions), 'pages found', len(pg))
