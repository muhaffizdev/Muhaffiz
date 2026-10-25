"""Muhaffiz SRS/SDS document builder: helpers that emit WordprocessingML and assemble the final .docx
from the university template (SRS-Template.docx). Content lives in ch*.py files."""
import re, os, copy, zipfile, shutil, subprocess, json
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NSMAP_DECL = ('xmlns:w="%s" xmlns:r="%s" '
              'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
              'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
              'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
              'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
              'xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main"') % (W, R)
ns = {'w': W}
TEXT_W = 9026  # A4 text width in twips (11906 - 2*1440)

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------------------------------------------------------- block constructors
def H1(text, key=None, numbered=True): return dict(k='h', lvl=1, text=text, key=key, numbered=numbered)
def H2(text, key=None): return dict(k='h', lvl=2, text=text, key=key, numbered=True)
def H3(text, key=None): return dict(k='h', lvl=3, text=text, key=key, numbered=True)
def P(text, indent=True, keep=False): return dict(k='p', text=text, indent=indent, keep=keep)
def BUL(items): return dict(k='bul', items=items)
def NUM(items): return dict(k='num', items=items)
def TBL(key, caption, headers, rows, widths, align=None, fs=18):
    return dict(k='tbl', key=key, caption=caption, headers=headers, rows=rows, widths=widths, align=align, fs=fs)
def FIG(key, caption, svg=None, png=None, width_in=6.3, land=False): return dict(k='fig', key=key, caption=caption, svg=svg, png=png, width_in=width_in, land=land)
def LAND(mode): return dict(k='sect', mode=mode)
def RAW(el): return dict(k='raw', el=el)
def PAGEBREAK(): return dict(k='pb')
def SPACER(): return dict(k='raw_xml', xml='<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>')

# ---------------------------------------------------------------- registry
class Ctx:
    def __init__(self):
        self.sec = {}      # key -> number text
        self.cap = {}      # key -> ('Table'|'Figure', n)
        self.cite_order = []   # keys in order of first appearance
        self.cite_defs = {}
        self.headings = []     # dicts for TOC
        self.captions = []     # dicts for LoT/LoF
        self.bm = 100
        self.pages = {}        # bookmark -> page label (from previous render)
        self.images = []       # (rid, path, kind)
        self.media_counter = 0
        self.rels = []         # extra relationships (rid, type, target)
        self.docpr = 1000
    def next_bm(self):
        self.bm += 1; return self.bm

def number_blocks(blocks, ctx):
    ch = sec = sub = 0; tb = fg = 0; idx = 0
    for b in blocks:
        if b['k'] == 'h':
            idx += 1
            b['bm'] = '_Toc%06d' % idx
            if b['lvl'] == 1:
                if b['numbered']:
                    ch += 1; sec = sub = 0; b['num'] = 'Chapter %d:' % ch; raw = str(ch)
                else:
                    b['num'] = ''; raw = ''
            elif b['lvl'] == 2:
                sec += 1; sub = 0; b['num'] = '%d.%d' % (ch, sec); raw = b['num']
            else:
                sub += 1; b['num'] = '%d.%d.%d' % (ch, sec, sub); raw = b['num']
            if b.get('key'): ctx.sec[b['key']] = raw
            ctx.headings.append(b)
        elif b['k'] == 'tbl':
            tb += 1; b['n'] = tb; ctx.cap[b['key']] = ('Table', tb); ctx.captions.append(dict(label='Table', n=tb, text=b['caption'], bm='_Toc_cap_%s' % b['key']))
        elif b['k'] == 'fig':
            fg += 1; b['n'] = fg; ctx.cap[b['key']] = ('Figure', fg); ctx.captions.append(dict(label='Figure', n=fg, text=b['caption'], bm='_Toc_cap_%s' % b['key']))

# ---------------------------------------------------------------- run / field helpers
def rpr(bold=False, italic=False, size=None, color=None, extra=''):
    s = ''
    if bold: s += '<w:b/><w:bCs/>'
    if italic: s += '<w:i/><w:iCs/>'
    if color: s += '<w:color w:val="%s"/>' % color
    if size: s += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
    s += extra
    return '<w:rPr>%s</w:rPr>' % s if s else ''

def run(text, **kw):
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr(**kw), esc(text))

def fld(instr, result_xml, rp=''):
    return ('<w:r>%s<w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r>%s<w:instrText xml:space="preserve"> %s </w:instrText></w:r>'
            '<w:r>%s<w:fldChar w:fldCharType="separate"/></w:r>%s'
            '<w:r>%s<w:fldChar w:fldCharType="end"/></w:r>') % (rp, rp, instr, rp, result_xml, rp)

TOKEN = re.compile(r'(\*\*.+?\*\*|//.+?//|\{(?:sec|tbl|fig|cite):[^}]+\})')

def inline(text, ctx, **kw):
    out = []
    for part in TOKEN.split(text):
        if not part: continue
        if part.startswith('**') and part.endswith('**'):
            out.append(inline(part[2:-2], ctx, **dict(kw, bold=True)))
        elif part.startswith('//') and part.endswith('//'):
            out.append(inline(part[2:-2], ctx, **dict(kw, italic=True)))
        elif part.startswith('{sec:'):
            key = part[5:-1]
            if key not in ctx.sec: raise KeyError('unknown section key ' + key)
            out.append(fld('REF _Ref_sec_%s \\r \\h' % key, run(ctx.sec[key], **kw)))
        elif part.startswith('{tbl:') or part.startswith('{fig:'):
            key = part[5:-1]
            if key not in ctx.cap: raise KeyError('unknown caption key ' + key)
            lab, n = ctx.cap[key]
            out.append(fld('REF _Ref_cap_%s \\h' % key, run('%s %d' % (lab, n), **kw)))
        elif part.startswith('{cite:'):
            key = part[6:-1]
            if key not in ctx.cite_order: ctx.cite_order.append(key)
            out.append(run('[%d]' % (ctx.cite_order.index(key) + 1), **kw))
        else:
            out.append(run(part, **kw))
    return ''.join(out)

def para(inner, style=None, ppr=''):
    st = '<w:pStyle w:val="%s"/>' % style if style else ''
    pp = '<w:pPr>%s%s</w:pPr>' % (st, ppr) if (st or ppr) else ''
    return '<w:p>%s%s</w:p>' % (pp, inner)

# ---------------------------------------------------------------- emitters
def bm_wrap(name, inner, ctx):
    i = ctx.next_bm()
    return '<w:bookmarkStart w:id="%d" w:name="%s"/>%s<w:bookmarkEnd w:id="%d"/>' % (i, name, inner, i)

def emit_heading(b, ctx):
    style = 'Heading%d' % b['lvl']
    ppr = ''
    if b['lvl'] == 1 and not b['numbered']:
        ppr = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'
    inner = run(b['text'])
    if b.get('key'): inner = bm_wrap('_Ref_sec_%s' % b['key'], inner, ctx)
    inner = bm_wrap(b['bm'], inner, ctx)
    return para(inner, style, ppr)

def emit_block(b, ctx):
    k = b['k']
    if k == 'h': return emit_heading(b, ctx)
    if k == 'p':
        ppr = '' if b['indent'] else '<w:ind w:firstLine="0"/>'
        if b['keep']: ppr += '<w:keepNext/>'
        return para(inline(b['text'], ctx), 'SRSBody', ppr)
    if k == 'bul' or k == 'num':
        out = []
        numid = 91
        if k == 'num':
            numid = ctx.new_num()
        n_items = len(b['items'])
        for i_, it in enumerate(b['items']):
            last = '<w:spacing w:after="360"/>' if i_ == n_items - 1 else ''
            out.append(para(inline(it, ctx), 'SRSList',
                            '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="%d"/></w:numPr>%s' % (numid, last)))
        return ''.join(out)
    if k == 'tbl': return emit_table(b, ctx)
    if k == 'fig': return emit_figure(b, ctx)
    if k == 'pb': return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    if k == 'sect':
        first = '' if getattr(ctx, 'sect_started', False) else '<w:pgNumType w:start="1"/>'
        if b['mode'] == 'begin_land':
            ctx.sect_started = True
            return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:sectPr><w:footerReference w:type="default" r:id="rId119"/><w:type w:val="nextPage"/><w:pgSz w:w="11906" w:h="16838"/>'
                    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>%s<w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr></w:pPr></w:p>' % first)
        return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:sectPr><w:footerReference w:type="default" r:id="rId119"/><w:type w:val="nextPage"/><w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>'
                '<w:pgMar w:top="1000" w:right="1000" w:bottom="1000" w:left="1000" w:header="708" w:footer="500" w:gutter="0"/><w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr></w:pPr></w:p>')
    if k == 'raw_xml': return b['xml']
    if k == 'refs':
        out = []
        for i, key in enumerate(ctx.cite_order):
            out.append(para(run('[%d]  ' % (i + 1)) + inline(ctx.cite_defs[key], ctx), 'SRSRef'))
        return ''.join(out)
    if k == 'toc': return build_toc(ctx, any(c['label']=='Figure' for c in ctx.captions), any(c['label']=='Table' for c in ctx.captions))
    raise ValueError(k)

def caption_par(label, n, text, key, ctx, keep_next):
    bmid = '_Toc_cap_%s' % key
    lab = bm_wrap('_Ref_cap_%s' % key, run(label + ' ') + fld('SEQ %s \\* ARABIC' % label, run(str(n))), ctx)
    inner = lab + run(': ' + text)
    inner = bm_wrap(bmid, inner, ctx)
    return para(inner, 'Caption', '<w:keepNext/>' if keep_next else '')

def cell_xml(text, w, header, shade, ctx, fs, align=None):
    tcpr = '<w:tcW w:w="%d" w:type="dxa"/>' % w
    if header: tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="1F4E78"/>'
    elif shade: tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="EAF1F8"/>'
    tcpr += '<w:tcMar><w:top w:w="60" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tcMar>'
    tcpr += '<w:vAlign w:val="%s"/>' % ('center' if header else 'top')
    paras = []
    lines = str(text).split('\n') if text != '' else ['']
    for ln in lines:
        kw = dict(size=fs)
        if header: kw.update(bold=True, color='FFFFFF')
        bullet = ln.startswith('• ')
        ppr = ''
        if bullet:
            ppr = '<w:ind w:left="170" w:hanging="170"/>'
        if align == 'center': ppr += '<w:jc w:val="center"/>'
        paras.append(para(inline(ln, ctx, **kw), 'TableText', ppr))
    return '<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % (tcpr, ''.join(paras))

def emit_table(b, ctx):
    tot = sum(b['widths']); widths = [round(w * TEXT_W / tot) for w in b['widths']]
    widths[-1] += TEXT_W - sum(widths)
    fs = 18   # one table font size throughout the document
    out = [caption_par('Table', b['n'], b['caption'], b['key'], ctx, True)]
    grid = ''.join('<w:gridCol w:w="%d"/>' % w for w in widths)
    rows = []
    hdr = ''.join(cell_xml(h, w, True, False, ctx, fs) for h, w in zip(b['headers'], widths))
    rows.append('<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>%s</w:tr>' % hdr)
    for i, r in enumerate(b['rows']):
        assert len(r) == len(widths), (b['key'], r)
        cells = ''.join(cell_xml(c, w, False, i % 2 == 1, ctx, fs) for c, w in zip(r, widths))
        rows.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>' % cells)
    tbl = ('<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/>'
           '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
           '<w:tblGrid>%s</w:tblGrid>%s</w:tbl>') % (TEXT_W, grid, ''.join(rows))
    out.append(tbl)
    out.append('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="12"/><w:szCs w:val="12"/></w:rPr></w:pPr></w:p>')
    return ''.join(out)

def emit_figure(b, ctx):
    rid_png, rid_svg = ctx.add_image(b)
    w, h = png_size(b['png'])
    max_w, max_h = (10.2, 5.7) if b.get('land') else (min(6.3, b['width_in']), 8.3)
    disp_w = min(max_w, max_h * w / h)
    try:
        import re as _re
        head = open(b['svg'], encoding='utf8').read(600) if b.get('svg') else ''
        mw = _re.search(r'width="([\d.]+)', head)
        if mw: disp_w = min(disp_w, float(mw.group(1)) / 96.0 * 1.12)
    except Exception: pass
    cx = int(disp_w * 914400)
    cy = int(cx * h / w)
    ctx.docpr += 1
    ext = ''
    if rid_svg:
        ext = ('<a:extLst><a:ext uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}">'
               '<asvg:svgBlip r:embed="%s"/></a:ext></a:extLst>') % rid_svg
    drawing = ('<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="%d" cy="%d"/>'
               '<wp:docPr id="%d" name="Figure %d" descr="%s"/><wp:cNvGraphicFramePr/>'
               '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
               '<pic:pic><pic:nvPicPr><pic:cNvPr id="%d" name="fig%d.png"/><pic:cNvPicPr/></pic:nvPicPr>'
               '<pic:blipFill><a:blip r:embed="%s">%s</a:blip><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
               '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
               '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>') % (
                   cx, cy, ctx.docpr, b['n'], esc(b['caption']), ctx.docpr, b['n'], rid_png, ext, cx, cy)
    pic = para('<w:r>%s</w:r>' % drawing, None, '<w:keepNext/><w:spacing w:before="120" w:after="60"/><w:jc w:val="center"/>')
    cap = caption_par('Figure', b['n'], b['caption'], b['key'], ctx, False)
    return pic + cap

def png_size(path):
    with open(path, 'rb') as f:
        d = f.read(32)
    from struct import unpack
    return unpack('>II', d[16:24])

# ---------------------------------------------------------------- TOC
def toc_entry_runs(num, title, lvl):
    if lvl == 1:
        txt = (num + ' ' if num else '') + title
        return run(txt)
    return run(num) + '<w:r><w:tab/></w:r>' + run(title)

def build_toc(ctx, with_figs, with_tabs):
    out = []
    out.append('<w:sdt><w:sdtPr><w:id w:val="-1394504381"/><w:docPartObj><w:docPartGallery w:val="Table of Contents"/><w:docPartUnique/></w:docPartObj></w:sdtPr><w:sdtContent>')
    out.append(para(run('Table of Contents'), 'TOCHeading'))
    ents = ctx.headings
    first = True
    for b in ents:
        lvl = b['lvl']
        pg = ctx.pages.get(b['bm'], '')
        tabs = '<w:tabs>%s<w:tab w:val="right" w:leader="dot" w:pos="%d"/></w:tabs>' % (
            '' if lvl == 1 else '<w:tab w:val="left" w:pos="%d"/>' % (700 if lvl == 2 else 1100), TEXT_W)
        inner = ''
        if first:
            inner += ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
                      '<w:r><w:fldChar w:fldCharType="separate"/></w:r>')
            first = False
        link = toc_entry_runs(b['num'], b['text'], lvl) + '<w:r><w:tab/></w:r>' + fld('PAGEREF %s \\h' % b['bm'], run(str(pg)))
        inner += '<w:hyperlink w:anchor="%s" w:history="1">%s</w:hyperlink>' % (b['bm'], link)
        out.append(para(inner, 'TOC%d' % lvl, tabs))
    out.append('<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
    out.append('</w:sdtContent></w:sdt>')
    def lot(label, title, instr):
        items = [c for c in ctx.captions if c['label'] == label]
        res = [para(run(title), 'TOCHeading', '<w:pageBreakBefore/>')]
        first = True
        for c in items:
            pg = ctx.pages.get(c['bm'], '')
            inner = ''
            if first:
                inner += ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> %s </w:instrText></w:r>'
                          '<w:r><w:fldChar w:fldCharType="separate"/></w:r>') % instr
                first = False
            link = run('%s %d: %s' % (label, c['n'], c['text'])) + '<w:r><w:tab/></w:r>' + fld('PAGEREF %s \\h' % c['bm'], run(str(pg)))
            inner += '<w:hyperlink w:anchor="%s" w:history="1">%s</w:hyperlink>' % (c['bm'], link)
            res.append(para(inner, 'TableofFigures', '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="%d"/></w:tabs>' % TEXT_W))
        if items: res.append('<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
        return ''.join(res) if items else ''
    if with_figs: out.append(lot('Figure', 'List of Figures', 'TOC \\h \\z \\c "Figure"'))
    if with_tabs: out.append(lot('Table', 'List of Tables', 'TOC \\h \\z \\c "Table"'))
    return ''.join(out)

# ---------------------------------------------------------------- numbering and styles patches
def patch_numbering(path, ctx_nums):
    t = etree.parse(path); root = t.getroot()
    abstr_xml = []
    # heading multilevel list
    abstr_xml.append('''<w:abstractNum xmlns:w="%s" w:abstractNumId="90"><w:multiLevelType w:val="multilevel"/>
<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:pStyle w:val="Heading1"/><w:suff w:val="space"/><w:lvlText w:val="Chapter %%1:"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="0" w:firstLine="0"/></w:pPr></w:lvl>
<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:pStyle w:val="Heading2"/><w:lvlText w:val="%%1.%%2"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="576" w:hanging="576"/></w:pPr></w:lvl>
<w:lvl w:ilvl="2"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:pStyle w:val="Heading3"/><w:lvlText w:val="%%1.%%2.%%3"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="720"/></w:pPr></w:lvl>
</w:abstractNum>''' % W)
    abstr_xml.append('''<w:abstractNum xmlns:w="%s" w:abstractNumId="91"><w:multiLevelType w:val="hybridMultilevel"/>
<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="567" w:hanging="340"/></w:pPr><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:hint="default"/></w:rPr></w:lvl>
</w:abstractNum>''' % W)
    abstr_xml.append('''<w:abstractNum xmlns:w="%s" w:abstractNumId="92"><w:multiLevelType w:val="hybridMultilevel"/>
<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%%1."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="567" w:hanging="340"/></w:pPr></w:lvl>
</w:abstractNum>''' % W)
    first_num = root.find('w:num', ns)
    for x in abstr_xml:
        el = etree.fromstring(x)
        first_num.addprevious(el)
    def add_num(nid, aid, restart=False):
        n = etree.fromstring('<w:num xmlns:w="%s" w:numId="%d"><w:abstractNumId w:val="%d"/>%s</w:num>' % (
            W, nid, aid, '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride>' if restart else ''))
        root.append(n)
    add_num(90, 90); add_num(91, 91)
    for nid in ctx_nums: add_num(nid, 92, True)
    t.write(path, xml_declaration=True, encoding='UTF-8', standalone=True)

def patch_styles(path):
    s = open(path, encoding='utf8').read()
    TNR = '<w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    def sub_style(sid, new):
        nonlocal s
        pat = re.compile(r'<w:style [^>]*w:styleId="%s"[^>]*>.*?</w:style>' % sid, re.S)
        if pat.search(s): s = pat.sub(lambda m: new, s, count=1)
        else: s = s.replace('</w:styles>', new + '</w:styles>')
    sub_style('Heading1', '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="SRSBody"/><w:qFormat/>'
        '<w:pPr><w:keepNext/><w:pageBreakBefore/><w:numPr><w:numId w:val="90"/></w:numPr><w:spacing w:before="240" w:after="240"/><w:outlineLvl w:val="0"/></w:pPr>'
        '<w:rPr>%s<w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>' % TNR)
    sub_style('Heading2', '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="SRSBody"/><w:qFormat/>'
        '<w:pPr><w:keepNext/><w:numPr><w:ilvl w:val="1"/><w:numId w:val="90"/></w:numPr><w:spacing w:before="280" w:after="140"/><w:outlineLvl w:val="1"/></w:pPr>'
        '<w:rPr>%s<w:b/><w:bCs/><w:color w:val="2E5395"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>' % TNR)
    sub_style('Heading3', '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="SRSBody"/><w:qFormat/>'
        '<w:pPr><w:keepNext/><w:numPr><w:ilvl w:val="2"/><w:numId w:val="90"/></w:numPr><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="2"/></w:pPr>'
        '<w:rPr>%s<w:b/><w:bCs/><w:color w:val="1F4D78"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>' % TNR)
    sub_style('SRSBody', '<w:style w:type="paragraph" w:customStyle="1" w:styleId="SRSBody"><w:name w:val="SRS Body"/><w:basedOn w:val="Normal"/><w:qFormat/>'
        '<w:pPr><w:spacing w:after="360" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="720"/><w:jc w:val="both"/></w:pPr>'
        '<w:rPr>%s<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>' % TNR)
    sub_style('SRSList', '<w:style w:type="paragraph" w:customStyle="1" w:styleId="SRSList"><w:name w:val="SRS List"/><w:basedOn w:val="Normal"/><w:qFormat/>'
        '<w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
        '<w:rPr>%s<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>' % TNR)
    sub_style('TableText', '<w:style w:type="paragraph" w:customStyle="1" w:styleId="TableText"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:qFormat/>'
        '<w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
        '<w:rPr>%s<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>' % TNR)
    sub_style('SRSRef', '<w:style w:type="paragraph" w:customStyle="1" w:styleId="SRSRef"><w:name w:val="SRS Reference"/><w:basedOn w:val="Normal"/><w:qFormat/>'
        '<w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:ind w:left="567" w:hanging="567"/><w:jc w:val="both"/></w:pPr>'
        '<w:rPr>%s<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>' % TNR)
    sub_style('FrontHeading', '<w:style w:type="paragraph" w:customStyle="1" w:styleId="FrontHeading"><w:name w:val="Front Heading"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
        '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="160"/></w:pPr>'
        '<w:rPr>%s<w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>' % TNR)
    sub_style('Caption', '<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:unhideWhenUsed/><w:qFormat/>'
        '<w:pPr><w:keepLines/><w:spacing w:before="120" w:after="100"/><w:jc w:val="center"/></w:pPr>'
        '<w:rPr>%s<w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:style>' % TNR)
    for lvl, ind in ((1, 0), (2, 240), (3, 480)):
        sub_style('TOC%d' % lvl, '<w:style w:type="paragraph" w:styleId="TOC%d"><w:name w:val="toc %d"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:autoRedefine/><w:uiPriority w:val="39"/><w:unhideWhenUsed/>'
            '<w:pPr><w:spacing w:after="60"/><w:ind w:left="%d"/></w:pPr><w:rPr>%s<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>' % (lvl, lvl, ind, TNR))
    sub_style('TableofFigures', '<w:style w:type="paragraph" w:styleId="TableofFigures"><w:name w:val="table of figures"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/>'
        '<w:pPr><w:spacing w:after="60"/></w:pPr><w:rPr>%s<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>' % TNR)
    sub_style('TOCHeading', '<w:style w:type="paragraph" w:styleId="TOCHeading"><w:name w:val="TOC Heading"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:qFormat/>'
        '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="240"/></w:pPr><w:rPr>%s<w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>' % TNR)
    s = re.sub(r'<w:rPrDefault>.*?</w:rPrDefault>', '<w:rPrDefault><w:rPr>%s<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>' % TNR, s, count=1, flags=re.S)
    open(path, 'w', encoding='utf8').write(s)

# ---------------------------------------------------------------- Ctx extensions
def _new_num(self):
    self._num = getattr(self, '_num', 100) + 1
    self.nums.append(self._num)
    return self._num
Ctx.new_num = _new_num
Ctx.nums = []

def _add_image(self, b):
    """Register PNG (+ optional SVG) for a figure; returns (rid_png, rid_svg)."""
    self.media_counter += 1
    n = self.media_counter
    rid_png = 'rIdSrsImg%dp' % n
    self.images.append((rid_png, b['png'], 'png', 'media/srs_fig%d.png' % n))
    rid_svg = None
    if b.get('svg'):
        rid_svg = 'rIdSrsImg%ds' % n
        self.images.append((rid_svg, b['svg'], 'svg', 'media/srs_fig%d.svg' % n))
    return rid_png, rid_svg
Ctx.add_image = _add_image

# ---------------------------------------------------------------- package assembly
def parse_fragment(xml):
    root = etree.fromstring('<w:body %s>%s</w:body>' % (NSMAP_DECL, xml))
    return list(root)

def heading_info(el):
    st = el.find('w:pPr/w:pStyle', ns)
    if st is None: return None
    v = st.get('{%s}val' % W)
    if v in ('Heading1', 'Heading2', 'Heading3'):
        return int(v[-1])
    return None

KEYMAP = {'User Classes and Characteristics': 'users',
          'Design and Implementation Constraints, Assumptions and Dependencies': 'constraints'}

def raw_to_blocks(elements):
    """Turn untouched template elements into blocks; template headings become numbered heading blocks."""
    out = []
    for el in elements:
        lvl = heading_info(el)
        text = ''.join(el.itertext()).strip()
        if lvl and text:
            text = re.sub(r'^Chapter \d+:\s*', '', text)
            text = re.sub(r'^\d+\.\d+(\.\d+)?\s*', '', text)
            out.append(dict(k='h', lvl=lvl, text=text, key=KEYMAP.get(text), numbered=True))
        else:
            out.append(RAW(el))
    return out

def emit_all(blocks, ctx):
    number_blocks(blocks, ctx)
    xml = []
    elems = []
    buf = []
    def flush():
        if buf:
            elems.extend(parse_fragment(''.join(buf))); buf.clear()
    for b in blocks:
        if b['k'] == 'raw':
            flush(); elems.append(copy.deepcopy(b['el']))
        else:
            buf.append(emit_block(b, ctx))
    flush()
    return elems

def write_package(src_dir, out_path, ctx):
    """Zip src_dir into out_path after pruning unreferenced media/embeddings and adding figures."""
    docx = os.path.join(src_dir, 'word', 'document.xml')
    # figures
    rels_path = os.path.join(src_dir, 'word', '_rels', 'document.xml.rels')
    rels = open(rels_path, encoding='utf8').read()
    ct_path = os.path.join(src_dir, '[Content_Types].xml')
    ct = open(ct_path, encoding='utf8').read()
    add = ''
    for rid, path, kind, target in ctx.images:
        dest = os.path.join(src_dir, 'word', target)
        if kind == 'png':
            r = subprocess.run(['convert', path, '-dither', 'None', '-colors', '192', 'PNG8:' + dest], capture_output=True)
            if r.returncode != 0: shutil.copy(path, dest)
        else:
            shutil.copy(path, dest)
        mime = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
        add += '<Relationship Id="%s" Type="%s" Target="%s"/>' % (rid, mime, target)
        ext = 'svg' if kind == 'svg' else 'png'
        if 'Extension="%s"' % ext not in ct:
            ct = ct.replace('<Default ', '<Default Extension="%s" ContentType="%s"/><Default ' % (ext, 'image/svg+xml' if ext == 'svg' else 'image/png'), 1)
    rels = rels.replace('</Relationships>', add + '</Relationships>')
    # prune unreferenced image/ole relationships
    d = open(docx, encoding='utf8').read()
    used = set(re.findall(r'r:(?:id|embed|link|pict)="([^"]+)"', d))
    def keep(m):
        rid = m.group(1); typ = m.group(2)
        if typ.endswith('/image') or typ.endswith('/oleObject'):
            return m.group(0) if rid in used else ''
        return m.group(0)
    rels = re.sub(r'<Relationship Id="([^"]+)" Type="([^"]+)"[^>]*/>', keep, rels)
    open(rels_path, 'w', encoding='utf8').write(rels)
    open(ct_path, 'w', encoding='utf8').write(ct)
    # delete files no relationship points to
    targets = set()
    for root_, _, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.rels'):
                for t in re.findall(r'Target="([^"]+)"', open(os.path.join(root_, f), encoding='utf8').read()):
                    targets.add(os.path.normpath(os.path.join(os.path.dirname(root_), t)))
    for sub in ('media', 'embeddings'):
        base = os.path.join(src_dir, 'word', sub)
        if os.path.isdir(base):
            for f in os.listdir(base):
                if os.path.normpath(os.path.join(base, f)) not in targets:
                    os.remove(os.path.join(base, f))
    if os.path.exists(out_path): os.remove(out_path)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(src_dir, '[Content_Types].xml'), '[Content_Types].xml')
        for root_, _, files in os.walk(src_dir):
            for f in sorted(files):
                full = os.path.join(root_, f)
                arc = os.path.relpath(full, src_dir)
                if arc == '[Content_Types].xml': continue
                z.write(full, arc)

# ---------------------------------------------------------------- page-number lookup from rendered PDF
def pdf_pages(pdf):
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    pages = []
    for i in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), '-layout', pdf, '-'], capture_output=True, text=True).stdout
        pages.append(t)
    return pages

def find_pages(pdf, ctx):
    pages = pdf_pages(pdf)
    norm = lambda s: re.sub(r'\s+', ' ', s).strip()
    # first body page: contains Chapter 1 heading and no dotted TOC leaders
    first = None
    for i, t in enumerate(pages):
        if 'Chapter 1:' in t and t.count('.....') < 3 and 'Table of Contents' not in t:
            first = i; break
    if first is None: return {}
    out = {}
    cur = first
    for b in ctx.headings:
        key = norm(((b['num'] + ' ') if b['num'] else '') + b['text'])[:45]
        for i in range(cur, len(pages)):
            lines = [norm(l) for l in pages[i].split('\n')]
            if any(l.startswith(key) or (b['lvl'] > 1 and norm(b['num'] + ' ' + b['text']).startswith(l) and len(l) > 8 and l.startswith(b['num'])) for l in lines):
                out[b['bm']] = i - first + 1; cur = i; break
    cur = first
    for c in ctx.captions:
        key = '%s %d:' % (c['label'], c['n'])
        for i in range(cur, len(pages)):
            if any(norm(l).startswith(key) for l in pages[i].split('\n')):
                out[c['bm']] = i - first + 1; cur = i; break
    return out
