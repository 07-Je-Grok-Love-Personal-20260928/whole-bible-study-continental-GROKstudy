"""v12.1: extract 刘道顺《新旧约圣经全景》 PDF -> paragraphs (verbatim chars, stream order) with roles.
Uses PyMuPDF rawdict (chars + positions). Only extraction artifacts are changed: PDF line wraps joined,
printed page numbers dropped, whitespace normalised. Reference for verification: pdftotext -raw."""
import pymupdf,json,re,os,sys,subprocess
PDF='/home/box/agent-data/agents/1037332c-f4cc-4d3b-81d0-215f4395bf06/attachments/7a2ed880b4ca378f0e88fb4fc9f4b943e5673632c083b46084f24d6b25e7451f.pdf'
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','liu')
def chars():
    d=pymupdf.open(PDF)
    for pi,p in enumerate(d):
        H=p.rect.height
        for b in p.get_text('rawdict')['blocks']:
            for l in b.get('lines',[]):
                for s in l['spans']:
                    txt=''.join(c['c'] for c in s['chars']).strip()
                    # printed page number: small Times digits at page bottom
                    if txt.isdigit() and s['size']<9.5 and s['bbox'][1]>H-60: continue
                    for c in s['chars']:
                        yield pi+1,c['c'],c['bbox'],c['origin'],s['font'],round(s['size'],1)
def role(font,size):
    if size>=30: return 'title'
    if size>=15: return 'big'
    if size>=13.5: return 'h1'
    if 'SimHei' in font and size>=11.5: return 'h2'
    if 'SimHei' in font and size>=10: return 'h3'
    if size<9.5: return 'small'
    return 'p'
def paragraphs():
    paras=[];cur=None;py=None;ppage=None
    for pg,c,bb,org,font,size in chars():
        if c.isspace() and cur is None: continue
        r=role(font,size) if not c.isspace() else None
        newline = ppage!=pg or (py is not None and org[1]>py+6) or (py is not None and org[1]<py-30)
        brk=False
        if cur is None: brk=True
        elif newline and not c.isspace():
            gap=org[1]-py if ppage==pg else 0
            if bb[0]>68: brk=True              # first-line indent / centred / right-aligned line
            elif gap>24: brk=True              # blank line between paragraphs
            elif r and r!=cur['role'] and (r!='p' or cur['role'] in('h1','h2','big','title')): brk=True
            elif ppage!=pg and r in('h1','h2','h3','title','big'): brk=True
        elif r and cur and r!=cur['role'] and r in('h1','h2','title','big') and cur['role'] not in('h1','h2','title','big') : brk=True
        if c=='〈' and cur and cur['role']=='p': brk=True
        if newline and not c.isspace(): py=org[1]; ppage=pg
        elif py is None: py=org[1]; ppage=pg
        if brk:
            if c.isspace(): continue
            cur={'role':r,'page':pg,'x':round(bb[0]),'t':'','roles':{}}; paras.append(cur)
        cur['t']+=c
        if r: cur['roles'][r]=cur['roles'].get(r,0)+1
        if newline and c.isspace(): pass
        if newline: cur['t']=cur['t'][:-1]+'\n'+c if len(cur['t'])>1 else cur['t']
    for p in paras:
        p['role']=max(p['roles'],key=p['roles'].get); del p['roles']
        p['t']=clean(p['t'])
    return [p for p in paras if p['t']]
CJK=r'[\u2E80-\u9FFF\u3000-\u303F\uFF00-\uFFEF\u2014\u2018-\u201F\u2026\u00B7]'
def clean(t):
    t=t.replace('\u00a0',' ').replace('\u3000',' ')
    t=re.sub(r'[ \t]*\n[ \t\n]*','\n',t).strip()
    t=re.sub(r'(?<=%s)\n(?=%s)'%(CJK,CJK),'',t)     # CJK wrap: join without space
    t=re.sub(r'\n',' ',t)                            # other wraps: single space
    t=re.sub(r' {2,}',' ',t)
    return t.strip()
ARTIFACTS='\u06e8'   # p.224: stray Arabic combining mark (renders as a dotted circle) — a typesetting glitch, not text
def norm(t): return re.sub(r'\s+','',re.sub(r'\.{5,}','',t)).translate({ord(c):None for c in ARTIFACTS})
def reference():
    raw=subprocess.run(['pdftotext','-raw',PDF,'-'],capture_output=True,text=True).stdout.split('\f')
    out=[]
    for i,pg in enumerate(raw[:-1] if raw[-1].strip()=='' else raw):
        ls=pg.split('\n')
        # drop printed page number line (= page index) wherever pdftotext put it
        for k,l in enumerate(ls):
            if l.strip()==str(i+1): ls[k]='';break
        out.append('\n'.join(ls))
    return out
if __name__=='__main__':
    P=paragraphs()
    os.makedirs(OUT,exist_ok=True)
    json.dump(P,open(os.path.join(OUT,'paras.json'),'w'),ensure_ascii=False,indent=0)
    open(os.path.join(OUT,'ref_norm.txt'),'w').write(norm(''.join(reference())))
    ref=norm(''.join(reference())); got=norm(''.join(p['t'] for p in P))
    print('paras',len(P),'ref chars',len(ref),'got',len(got),'equal',ref==got)
    if ref!=got:
        import difflib
        sm=difflib.SequenceMatcher(None,ref,got,autojunk=False)
        for op in sm.get_opcodes():
            if op[0]!='equal': print(op[0],repr(ref[op[1]-10:op[2]+10]),'|',repr(got[op[3]-10:op[4]+10]))
