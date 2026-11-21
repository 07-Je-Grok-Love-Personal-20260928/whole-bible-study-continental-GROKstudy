# v12.1: 刘道顺《新旧约圣经全景》全文阅读版 — liu.html (目录) + liu-*.html (每篇一页)
# 正文逐字照录（只处理PDF抽取痕迹：换行拼接、页码删除）；标注只用 span/mark/b 包裹，不改动任何字符。
import json,re,os,html as H
from lib import *
import lib
from books import BOOKS,CATS,qmark
from liu_data import LIU
HERE=os.path.dirname(os.path.abspath(__file__))
P=json.load(open(os.path.join(HERE,'data','liu','paras.json')))
REF=open(os.path.join(HERE,'data','liu','ref_norm.txt')).read()
ATTR='刘道顺牧师《新旧约圣经全景》（房角石）'
LIC='经授权转载'
# fix: a lone '〈' that PDF stream order put at the end of the previous paragraph
for i in range(len(P)-1):
    if P[i]['t'].endswith('〈') and '〉' in P[i+1]['t'] and '〈' not in P[i+1]['t']:
        P[i]['t']=P[i]['t'][:-1].rstrip(); P[i+1]['t']='〈'+P[i+1]['t']
BIC={'gen':'🌍','exo':'🌊','lev':'🔥','num':'🏕️','deu':'📜','jos':'⚔️','jdg':'🗡️','rut':'🌾','1sa':'👑','2sa':'🎵','1ki':'🏛️','2ki':'⛓️','1ch':'🧾','2ch':'🕍',
'ezr':'📖','neh':'🧱','est':'👸','job':'🌪️','psa':'🎼','pro':'💡','ecc':'⏳','sng':'🌹','isa':'🕊️','jer':'😢','lam':'🥀','eze':'👁️','dan':'🦁','hos':'💍',
'joe':'🦗','amo':'⚖️','oba':'⛰️','jon':'🐋','mic':'⚖️','nah':'🌩️','hab':'🗼','zep':'📯','hag':'🏗️','zec':'🐎','mal':'✉️','mat':'👑','mrk':'🐂','luk':'🧑',
'jhn':'🦅','act':'🔥','rom':'⚖️','1co':'🏺','2co':'🏺','gal':'🗝️','eph':'🛡️','php':'😊','col':'👑','1th':'🎺','2th':'🎺','1ti':'🧑‍🏫','2ti':'🏃','tit':'🏝️',
'phm':'🤝','heb':'⛪','jas':'🌱','1pe':'🪨','2pe':'🕯️','1jn':'💗','2jn':'💌','3jn':'💌','jud':'🛡️','rev':'🏙️'}
XG={  # 非书卷篇章的重点导读（据原文提炼）
'pre':{'t':'先读**设计图**，再一步步施工','s':'推荐人：远东广播电台台长 金长焕牧师','p':['刘牧师在远东广播电台以**救赎史观点**讲解圣经，整理成书；收听率始终稳居上位','背目录式学习：先掌握**整体结构**，再仔细研究——如熟读设计图后再施工','研经常太片面、太微观：要以==救赎史整体设计图==为前提，再从微观细看'],'x':'本书把救赎史的设计图一目了然地展现在眼前','mn':'先森林，后树木'},
'ot00':{'t':'登高远望：看清从创世记到玛拉基书**神的拯救启示**','s':'1995年8月 · 羊圈教会 刘道顺','p':['讲道人的使命：见证「神的奥秘是如何安排的」（弗3:8-9）','先知道**神为我们做了什么**，再思想我该为神做什么→明白爱与恩典、学会敬畏','断面知识多、脉络不足＝只见树木不见森林；方法：==先远观、后微观==（整体→部分、主干→枝节）'],'x':'追问：圣经整体主题→旧约/新约主题→各卷主题→彼此关系','mn':'登高远望，先林后木'},
'ot01':{'t':'圣经是一部**救赎史**：隐藏的奥秘，核心是基督','s':'影儿（旧约）→实体（新约）','p':['神的拯救计划是隐藏的奥秘：旧约是**影儿**，新约道成肉身**实体**显明（西1:26）','圣经66卷是一位圣灵所著、分不开的**一本书**；从创1:1到启22，神一直在「成就」他的计划（耶33:2）','中心话语如人体的**脊椎**、建筑的**架构**；以马忤斯路上主用的就是救赎史方法（路24:25-27）'],'x':'「给我作见证的就是这经」（约5:39）','mn':'奥秘·影儿·实体·脊椎'},
'ap1':{'t':'教会不是住院部，而是**练兵场**','s':'弗6:10-13 · 出生→成长→精兵','p':['**出生是第一**：先「用福音生」（林前4:15）','**要成长**：爱慕灵奶（彼前2:2），由父老、少年人到成熟','**需要神的精兵**：穿戴全副军装，与执政掌权者争战（弗6:10-13；提后2:3）'],'x':'耶和华的军队为基督争战，元帅是主自己','mn':'生·长·兵'},
'ap2':{'t':'救赎史讲道：**历史性·统一性·渐进性**','s':'提出问题→今日讲道三病→方向','p':['今日讲道三病：**无骨架**（无脊椎）、**无视历史性**（断章取义）、**造成圣经难解**','旧约大主题：神应许差遣弥赛亚；新约大主题：拿撒勒人耶稣就是基督（约5:39）','按圣经原本写作目的讲道：一年讲完66卷中心，为信徒建立**真理的骨架**'],'x':'连小孩子听了也会遇见耶稣、接受耶稣为救主','mn':'三病：无骨·无史·难解'},
'ap3':{'t':'讲道的改革从**讲坛回归圣经**开始','s':'提出问题→以神为中心→历史性→统一性','p':['改革先从牧会者自身：牧者是「神奥秘事的管家」（林前4:1）','**以神为中心**：不以挪亚、亚伯拉罕等人物为中心，基督不是配角','**历史性**：没有历史性的信仰是「没有家谱的信仰」；**统一性**：66卷一个主题'],'x':'耶稣基督理当成为讲道见证的中心','mn':'神本·历史·统一'},
'ap4':{'t':'讲道是传讲**神全备的旨意**','s':'林前2:7 · 讲道是什么→圣灵帮助→救赎史释经→核心→应用','p':['讲道＝作神的代言人：特权与责任（徒20:27）','倚靠**圣灵的帮助**：提早定下经文，常常默想，渴慕圣灵引导','**救赎史释经**：抓住经文核心（浓缩为一句话），最后必须有**应用**'],'x':'讲道「不是用智慧委婉的言语，乃是用圣灵和大能的明证」','mn':'代言·圣灵·核心·应用'},
}
# ------------------------------------------------------------ chaptering
def chapters():
    i=0;n=len(P);CH=[];seg=[0]
    def take(a,b): return P[a:b]
    # cover
    k=next(j for j,p in enumerate(P) if p['t']=='推荐辞')
    cover=P[:k]
    k2=next(j for j,p in enumerate(P) if p['t'].startswith('〈旧约圣经全景目录'))
    pre=P[k:k2]
    k3=next(j for j,p in enumerate(P) if p['role']=='title' and p['t']=='旧')
    toc=P[k2:k3]
    heads=[j for j,p in enumerate(P) if p['role']=='h1' and j>k3]
    k4=next(j for j,p in enumerate(P) if p['role']=='title' and p['t']=='新')
    ap0=next(j for j,p in enumerate(P) if p['role']=='h1' and p['t']=='附录')
    blocks={'cover':cover,'toc':toc,'otdiv':P[k3:k3+6],'ntdiv':P[k4:k4+6]}
    def chap_from(j,end):
        return P[j:end]
    hs=[j for j in heads if j<k4]+[j for j in heads if k4<j<ap0]
    # OT: j in heads < k4 ; NT: k4<j<ap0 ; appendix: ap0 (TOC) then h1s after ap0+5
    ot=[j for j in heads if j<k4]; nt=[j for j in heads if k4<j<ap0]
    apx=[j for j in heads if j>ap0 and not P[j]['t'].startswith('◎')]
    blocks['aptoc']=P[ap0:apx[0]]
    out=[('pre','front',pre)]
    for q,j in enumerate(ot): out.append((f'ot{q:02d}','ot',P[j:(ot[q+1] if q+1<len(ot) else k4)]))
    for q,j in enumerate(nt): out.append((f'nt{q:02d}','nt',P[j:(nt[q+1] if q+1<len(nt) else ap0)]))
    for q,j in enumerate(apx): out.append((f'ap{q+1}','ap',P[j:(apx[q+1] if q+1<len(apx) else n)]))
    return blocks,out
BLK,CHS=chapters()
OTB=[b for b in BOOKS if b['n']<=39]; NTB=[b for b in BOOKS if b['n']>39]
def meta(key,part,ps):
    title=ps[0]['t']; m={'key':key,'part':part,'ps':ps,'title':title,'file':f'liu-{key}.html','p0':ps[0]['page'],'p1':ps[-1]['page']}
    m['chars']=len(re.sub(r'\s','',''.join(p['t'] for p in ps)))
    bid=None
    if part in('ot','nt'):
        nm=re.sub(r'^\d+．','',title).replace('全景','')
        nm={'腓利经书':'腓立比书','腓利比书':'腓立比书','列王记上':'列王纪上','列王记下':'列王纪下','雅歌':'雅歌'}.get(nm,nm)
        b=[x for x in BOOKS if x['name']==nm]
        if b: bid=b[0]['id']
    m['bid']=bid
    if bid: m['ic']=BIC.get(bid,'📖'); m['col']=CATS[[x for x in BOOKS if x['id']==bid][0]['cat']][1]
    else: m['ic']={'pre':'💌','ot00':'🏔️','ot01':'🧭','ot24':'📯','nt00':'🪨','nt06':'✉️','ap1':'🛡️','ap2':'🦴','ap3':'🔨','ap4':'🙏'}.get(key,'📜'); m['col']='var(--gold)'
    gk={'ot24':'proph','nt00':'ntpre','nt06':'epis'}.get(key,bid)
    m['g']=XG.get(key) or (LIU.get(gk) if gk else None)
    if m['g'] is None: raise SystemExit('no guide for '+key+' '+title)
    m['mn']=({'ot24':'责罪·劝悔·警审·慰余','nt00':'影儿→实体，以便以谢','nt06':'先教义，后「所以」'}.get(key) or m['g'].get('mn') or ([x for x in BOOKS if x['id']==bid][0].get('mn') if bid else ''))
    return m
CH=[meta(*c) for c in CHS]
from books import liufile
for _c in CH:
    if _c['bid']: assert liufile([b for b in BOOKS if b['id']==_c['bid']][0])==_c['file'],_c['key']
PARTS=[('front','💌','推荐辞'),('ot','📗','旧约圣经全景'),('nt','📘','新约圣经全景'),('ap','🗂️','附录 · 救赎史讲道法')]
# ------------------------------------------------------------ segments (verbatim units)
SEGS=[]   # (seg id, normalized source text) in PDF order
ORDER={id(p):k for k,p in enumerate(P)}
def segattr(ps):
    """register the paragraphs as one verbatim segment; id = PDF order index of first paragraph"""
    k=ORDER[id(ps[0])]; SEGS.append((k,''.join(p['t'] for p in ps)))
    return f' data-seg="{k}"'
# ------------------------------------------------------------ marking (styling only)
REFP=re.compile(r'（(?:参考|参：|参|比较|见)?\s?(?:[\u4e00-\u9fff]{1,4}\s?)?\d+\s?[：:]\s?\d+[^）（]{0,40}）')
SQ=re.compile(r'“[^“”]{4,220}”(?=\s?（[^）]{0,12}\d+\s?[：:])')
ORD=re.compile(r'^(第[一二三四五六七八九十]+[，、]|首先，|其次，|最后，|结论是|总之，)')
CIRC=re.compile(r'[①②③④⑤⑥⑦⑧⑨⑩]')
KEYW=re.compile(r'主题|核心|中心|一句话|总结|概括|关键')
XW=re.compile(r'见证(了)?基督|预表|女人的后裔|弥赛亚')
TERMS_L=['救赎史','恩典之约','原始福音','女人的后裔','神的国','约的更新','以马内利','神的主权','神的拯救计划','十字架','影儿','实体','圣约','福音','圣灵']
def sentences(t):
    return [(m.start(),m.end()) for m in re.finditer(r'[^。！？]*[。！？]+[”’」]?',t)]
class Marker:
    def __init__(s): s.hy=0; s.ug=0; s.terms=set()
    def ranges(s,t):
        R=[]
        for a,b in sentences(t):
            seg=t[a:b]
            if len(seg.strip())<8 or len(seg)>150: continue
            if s.hy<5 and KEYW.search(seg) and not seg.lstrip().startswith(('默想',)):
                R.append((a+len(seg)-len(seg.lstrip()),b,'<mark class="hy">','</mark>',0)); s.hy+=1
            elif s.ug<4 and XW.search(seg):
                R.append((a+len(seg)-len(seg.lstrip()),b,'<span class="ug">','</span>',0)); s.ug+=1
        for m in SQ.finditer(t): R.append((m.start(),m.end(),'<span class="lsq">','</span>',1))
        for m in REFP.finditer(t): R.append((m.start(),m.end(),'<span class="rf">','</span>',2))
        m=ORD.match(t)
        if m: R.append((0,m.end(),'<b class="k">','</b>',2))
        for m in CIRC.finditer(t): R.append((m.start(),m.end(),'<b class="k">','</b>',3))
        for w in TERMS_L:
            if w in s.terms: continue
            i=t.find(w)
            if i>=0: R.append((i,i+len(w),'<span class="cx">','</span>',4)); s.terms.add(w)
        return R
def render(t,R):
    acc=[]
    for r in sorted(R,key=lambda r:(r[4],r[0])):
        if r[1]<=r[0]: continue
        if all(r[1]<=a[0] or r[0]>=a[1] or (a[0]<=r[0] and r[1]<=a[1]) or (r[0]<=a[0] and a[1]<=r[1]) for a in acc): acc.append(r)
    ev=[]
    for a in acc: ev.append((a[0],0,-(a[1]-a[0]),a[2])); ev.append((a[1],1,(a[1]-a[0]),a[3]))
    ev.sort(key=lambda e:(e[0],-e[1],e[2]))
    # closes before opens at same position; among opens, longer first; among closes, shorter first
    o=[];pos=0
    for p,kind,_,tag in sorted(ev,key=lambda e:(e[0],0 if e[1]==1 else 1,e[2])):
        o.append(H.escape(t[pos:p],quote=False)); o.append(tag); pos=p
    o.append(H.escape(t[pos:],quote=False))
    return ''.join(o)
def mk(t,M): return render(t,M.ranges(t))
# ------------------------------------------------------------ body rendering
ORDM=re.compile(r'^(第[一二三四五六七八九十]+[，、]|首先|其次|最后|总之|那么|结论)')
def label(t,n=20):
    c=re.split(r'(?<=[。？！])',t,1)[0]
    return (c[:n]+'…') if len(c)>n else c
def body(ch):
    ps=ch['ps'][1:]; M=Marker(); o=[]; i=0; nsec=0
    # 默想 split
    mi=None
    for j,p in enumerate(ps):
        if re.search(r'默想\s*(?:\d|[１-９]|$)',p['t']): mi=j;break
    def sec(lbl):
        nonlocal nsec; nsec+=1
        return f'<h3 class="h nonum lsec" data-toc="{E(lbl)}"><span aria-hidden="true">§ {nsec}</span></h3>'
    main=ps if mi is None else ps[:mi]
    j=0
    while j<len(main):
        p=main[j]; t=p['t']
        if p['role']=='h2': o.append(f'<h3 class="h nonum lh2"{segattr([p])}>{E(t)}</h3>'); j+=1; continue
        if p['role']=='h3': o.append(f'<h4 class="h nonum lh3"{segattr([p])}>{E(t)}</h4>'); j+=1; continue
        if p['role']=='small':
            g=[p]; j+=1
            while j<len(main) and main[j]['role']=='small': g.append(main[j]); j+=1
            o.append(f'<blockquote class="lep"{segattr(g)}>'+'<br>'.join(E(x['t']) for x in g)+'</blockquote>'); continue
        # poetry: run of >=2 short indented lines
        if len(t)<=24 and p['x']>68:
            g=[p]; k=j+1
            while k<len(main) and len(main[k]['t'])<=24 and main[k]['x']>68 and main[k]['role']=='p': g.append(main[k]); k+=1
            if len(g)>=2:
                o.append(f'<blockquote class="lpoem"{segattr(g)}>'+''.join(f'<span class="ln">{mk(x["t"],M)}</span>' for x in g)+'</blockquote>'); j=k; continue
        if j>0 and (ORDM.match(t) or ('见证基督' in t[:40]) or t.startswith('弟兄们')) and len(t)>40:
            o.append(sec(label(t)))
        cls='lp'
        if t.startswith('“') and re.search(r'）$',t) and len(t)<200: cls='lp lqp'
        if p['x']>150 and len(t)<40: cls='lp lsig'   # signatures / dates (right-aligned in PDF)
        o.append(f'<p class="{cls}"{segattr([p])}>{mk(t,M)}</p>'); j+=1
    if mi is not None:
        p=ps[mi]; t=p['t']; k=t.index('默想')
        rest=t[k+2:]+''.join(x['t'] for x in ps[mi+1:])
        segk=ORDER[id(p)]
        if k>0:
            pre_t=t[:k]
            o.append(f'<p class="lp" data-seg="{segk}">{mk(pre_t,M)}</p>'); SEGS.append((segk,pre_t))
            segk+=0.5
        items=[x for x in re.split(r'(?=(?<![\d．])(?:\d{1,2}|[１-９])．)',rest) if x.strip()]
        SEGS.append((segk,'默想'+''.join(items)))
        o.append(f'<h3 class="h nonum lmx" id="mx" data-toc="🙏 默想"><span class="lmxw" data-seg="{segk}">默想</span></h3>')
        o.append(f'<ol class="lmq" data-seg="{segk+0.25}">'+''.join(f'<li>{E(x.strip())}</li>' for x in items)+'</ol>')
    return ''.join(o)
# ------------------------------------------------------------ pages
def chip_nav(cur=None,compact=False):
    o='<div class="lnav">'
    for pk,pi,pn in PARTS:
        cs=[c for c in CH if c['part']==pk]
        o+=f'<div class="lnp"><b>{pi} {pn}</b><div class="lnc">'+''.join(f'<a href="{c["file"]}" class="{"on" if c is cur else ""}" title="{E(c["title"])}">{c["ic"]} {E(short(c))}</a>' for c in cs)+'</div></div>'
    return o+'</div>'
def short(c):
    t=re.sub(r'^\d+．','',c['title']).replace('全景','')
    return t if len(t)<=8 else t[:8]+'…'
def guide(c):
    g=c['g']; ps=g.get('p',[])[:5]
    x=g.get('x','')
    lk=''
    if c['bid']: lk=f'<a class="btn" href="index.html#b-{c["bid"]}">📚 本卷13项解读</a><a class="btn" href="panorama.html">📜 全景整合页</a>'
    else: lk='<a class="btn" href="panorama.html">📜 全景整合页</a><a class="btn" href="liu.html">📖 全书目录</a>'
    return (f'<div class="lguide rv" style="--c:{c["col"]}"><div class="lgh"><span class="lgi" aria-hidden="true">{c["ic"]}</span><div><small>一句话主题</small><p class="lgt">{qmark(g["t"],False)}</p></div></div>'
        +(f'<p class="lgs">🧩 {qmark(g["s"],False)}</p>' if g.get('s') else '')
        +'<ol class="lgp">'+''.join(f'<li><span class="lgn">{k+1}</span><span>{qmark(p,False)}</span></li>' for k,p in enumerate(ps))+'</ol>'
        +(f'<p class="lgx">✝️ <b>见证基督</b> {qmark(x,False)}</p>' if x else '')
        +(f'<p class="lgm">🧠 <b>记忆口诀</b> <span class="must">{E(re.sub(r"^[“\"]|[”\"]$","",c["mn"].split("（")[0]))}</span></p>' if c['mn'] else '')
        +f'<div class="lgl">{lk}</div></div>')
def chapter_page(k,c):
    pv=CH[k-1] if k>0 else None; nx=CH[k+1] if k+1<len(CH) else None
    lib.FABNAV[c['file']]=((pv['file'],pv['ic'],short(pv)) if pv else ('liu.html','📖','全书目录'),(nx['file'],nx['ic'],short(nx)) if nx else ('liu.html','📖','全书目录'))
    pn={'front':'卷首','ot':'旧约','nt':'新约','ap':'附录'}[c['part']]
    mins=max(1,round(c['chars']/450))
    hero=(f'<div class="crumb"><a href="index.html">📖 整本圣经</a><i>›</i><a href="liu.html">📖 全景·原文全书</a><i>›</i><span>{pn}</span><i>›</i><b>{c["ic"]} {E(short(c))}</b></div>'
      f'<section class="hero lhero reveal" style="--c:{c["col"]}"><div class="lkick"><span class="lki" aria-hidden="true">{c["ic"]}</span><span>{pn} · 第 {k} / {len(CH)-1} 篇</span><span>原书 第 {c["p0"]}–{c["p1"]} 页</span></div>'
      f'<h1 class="ltitle"{segattr([c["ps"][0]])}>{E(c["title"])}</h1>'
      f'<div class="chips"><span class="chip g">📜 原文逐字</span><span class="chip">✍️ {c["chars"]:,} 字</span><span class="chip">⏱️ 约 {mins} 分钟</span><span class="chip">📄 {len(c["ps"])-1} 段</span></div>'
      f'<p class="srcline">{ATTR} · <b>{LIC}</b> · 正文一字不差照录原书；加粗、底纹、下划线仅为笔记标注，未改动任何文字。</p></section>')
    c_=hero+legend_mini()
    c_+=h2('guide','🧭','重点导读')+guide(c)
    c_+=h2('text','📜','原文全文',f'原文全文（逐字）')+f'<article class="lbody" lang="zh-CN">{body(c)}</article>'
    c_+=('<nav class="pnx lpnx">'+(f'<a href="{pv["file"]}" class="pv"><small>← 上一篇</small><b>{pv["ic"]} {E(pv["title"])}</b></a>' if pv else '<a href="liu.html" class="pv"><small>← 返回</small><b>📖 全书目录</b></a>')
         +(f'<a href="{nx["file"]}" class="nx"><small>下一篇 →</small><b>{nx["ic"]} {E(nx["title"])}</b></a>' if nx else '<a href="liu.html" class="nx"><small>返回 →</small><b>📖 全书目录</b></a>')+'</nav>')
    c_+=f'<details class="dx lall"><summary>📚 全书篇目（{len(CH)} 篇）</summary><div class="in">{chip_nav(c)}</div></details>'
    return page(c['file'],re.sub(r'^\d+．','',c['title'])+' · 刘道顺《新旧约圣经全景》全文',c_,cv=False)
def toc_block():
    """original book TOC (pages 5–8) verbatim; dot leaders → CSS"""
    o=''
    for p in BLK['toc']:
        t=p['t']
        if p['role']=='h1': o+=('</div>' if o else '')+f'<div class="ltocg"><h4 class="h nonum ltoch"{segattr([p])}>{E(t)}</h4>'; continue
        ents=re.findall(r'(.+?)\.{5,}\s?(\d+)\s?',t)
        rest=re.sub(r'(.+?)\.{5,}\s?(\d+)\s?','',t).strip()
        lis=''
        for nm,pg in ents:
            nm=nm.strip(); m=[c for c in CH if c['p0']==int(pg)] or [c for c in CH if c['p0']<=int(pg)<=c['p1']]
            href=m[0]['file'] if m else 'liu.html'
            lis+=f'<li><a href="{href}"><span>{E(nm)}</span><i aria-hidden="true"></i><b>{pg}</b></a></li>'
        if rest: lis+=f'<li class="lrest">{E(rest)}</li>'
        o+=f'<ol class="ltoc"{segattr([p])}>{lis}</ol>'
    return o+('</div>' if '<div class="ltocg">' in o else '')
def index_page():
    cv=BLK['cover']; tot=sum(c['chars'] for c in CH)
    o=(f'<section class="hero lhero reveal"><div class="chips"><span class="chip g">📖 全文阅读版</span><span class="chip">{len(CH)} 篇</span><span class="chip">✍️ 约 {round(len(REF)/10000)} 万字</span><span class="chip">📄 原书 339 页</span><span class="chip">🔒 逐字核对 100%</span></div>'
       f'<div class="lcover"><h1 class="ltitle"{segattr(cv[:1])}>{E(cv[0]["t"])}</h1>'+''.join(f'<p class="lcv"{segattr([x])}>{E(x["t"])}</p>' for x in cv[1:])+'</div>'
       f'<p class="lead">刘道顺牧师以<b class="k">救赎史</b>观点「登高远望」整本圣经：旧约的大主题是<mark class="hy">神应许差遣弥赛亚</mark>，新约的大主题是<mark class="hy">拿撒勒人耶稣就是那基督</mark>。本区收录全书 <b class="k">{len(CH)}</b> 篇全文，每篇开头附「重点导读」。</p>'
       f'<p class="srcline">{ATTR} · <b>{LIC}</b>。正文按原书目录分篇，逐字照录（仅合并PDF换行、删去页码）；构建时自动与原书PDF逐字核对。笔记标注（加粗、底纹、下划线）只是样式，不改动文字。神学立场的校准见 <a href="panorama.html">📜 新旧约全景整合页</a>。</p></section>')
    o+=legend_mini()
    o+=h2('how','🧭','怎样使用这部全文')
    o+=('<div class="grid g3 rv">'+''.join(f'<div class="card tile" style="--c:{col}"><div class="big">{ic}</div><h4>{t}</h4><p>{d}</p></div>' for ic,t,d,col in [
        ('🔭','① 先看重点导读','每篇顶部 3–5 点＋口诀＋见证基督，三十秒抓住骨架','var(--gold)'),
        ('📜','② 再读原文全文','逐字原文；<mark class="hy">黄底</mark>＝主题/核心句，<span class="ug">绿线</span>＝见证基督，<span class="lsq">经文引语</span>','var(--sky)'),
        ('🙏','③ 最后做默想','每篇末尾的默想题，用来复述与应用；右下角 ✦ 可上下篇切换','var(--emer)')])+'</div>')
    for pk,pi,pn in PARTS:
        cs=[c for c in CH if c['part']==pk]
        o+=h2('part-'+pk,pi,pn)
        if pk=='ot': o+=f'<p class="ldiv rv" aria-label="旧约圣经全景"{segattr(BLK["otdiv"])}>'+''.join(f'<span>{E(x["t"])}</span>' for x in BLK['otdiv'])+'</p>'
        if pk=='nt': o+=f'<p class="ldiv rv" aria-label="新约圣经全景"{segattr(BLK["ntdiv"])}>'+''.join(f'<span>{E(x["t"])}</span>' for x in BLK['ntdiv'])+'</p>'
        if pk=='ap': o+=f'<div class="laptoc rv"{segattr(BLK["aptoc"])}>'+''.join(f'<span>{E(x["t"])}</span>' for x in BLK['aptoc'])+'</div>'
        groups=[(None,cs)]
        if pk=='ot': groups=[('律法书 · 历史书',cs[:19]),('诗歌智慧书',cs[19:23]),('先知书',cs[23:])]
        if pk=='nt': groups=[('福音书 · 使徒行传',cs[:6]),('书信',cs[6:27]),('预言',cs[27:])]
        for gn,gc in groups:
            if gn: o+=h3(f'part-{pk}-{gc[0]["key"]}',gn)
            o+='<div class="lcgrid rv">'+''.join(
              f'<a class="lccard" href="{c["file"]}" style="--c:{c["col"]}"><span class="lci" aria-hidden="true">{c["ic"]}</span><span class="lcb"><b>{E(c["title"])}</b><small>{qmark(c["g"]["t"],False)}</small><em>p.{c["p0"]} · {c["chars"]:,}字 · 约{max(1,round(c["chars"]/450))}分钟</em></span></a>' for c in gc)+'</div>'
    o+=h2('origtoc','🗂️','原书目录（原样）')
    o+=f'<div class="ltocw rv">{toc_block()}</div>'
    return page('liu.html','刘道顺《新旧约圣经全景》全文阅读版',o,cv=False)
def build():
    SEGS.clear()
    out={'liu.html':index_page()}
    for k,c in enumerate(CH): out[c['file']]=chapter_page(k,c)
    return out
# ------------------------------------------------------------ verification
class _TP(H.parser.HTMLParser if hasattr(H,'parser') else object): pass
from html.parser import HTMLParser
class SegText(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.stack=[]; s.cur=None; s.out={}; s.depth=0
    def handle_starttag(s,tag,a):
        if tag in('br','img','meta','link','input','hr','wbr','source'): return
        d=dict(a)
        if s.cur is None and 'data-seg' in d: s.cur=d['data-seg']; s.depth=0; s.out.setdefault(s.cur,'')
        if s.cur is not None: s.depth+=1
    def handle_endtag(s,tag):
        if tag in('br','img','meta','link','input','hr','wbr','source'): return
        if s.cur is not None:
            s.depth-=1
            if s.depth==0: s.cur=None
    def handle_data(s,d):
        if s.cur is not None: s.out[s.cur]+=d
def norm(t): return re.sub(r'\s+','',re.sub(r'\.{5,}','',t))
def verify(site):
    got={}
    for f in sorted(os.listdir(site)):
        if f=='liu.html' or f.startswith('liu-'):
            p=SegText(); p.feed(open(os.path.join(site,f),encoding='utf-8').read())
            for k,v in p.out.items():
                if k in got: raise SystemExit(f'LIU VERBATIM: duplicate seg {k} in {f}')
                got[k]=v
    seq=''.join(norm(got[k]) for k in sorted(got,key=float))
    # per chapter
    bad=[]
    for c in CH:
        src=norm(''.join(p['t'] for p in c['ps']))
        ks=[k for k in got if ORDER[id(c['ps'][0])]<=float(k)<=ORDER[id(c['ps'][-1])]+0.9]
        site_t=''.join(norm(got[k]) for k in sorted(ks,key=float))
        if site_t!=src: bad.append(c['key'])
    import difflib
    cov=100.0 if seq==REF else round(100*difflib.SequenceMatcher(None,REF,seq,autojunk=False).ratio(),3)
    print(f'Liu verbatim: chapters {len(CH)}, segs {len(got)}, site chars {len(seq)}, PDF chars {len(REF)}, coverage {cov}%, chapter mismatches {bad}')
    if seq!=REF or bad: raise SystemExit('LIU VERBATIM CHECK FAILED')
    return cov
