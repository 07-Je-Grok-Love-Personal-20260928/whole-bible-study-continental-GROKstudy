import re
from lib import *
CATS={'law':('律法书','var(--law)','⚖️'),'hist':('历史书','var(--hist)','🏛️'),'poet':('诗歌智慧书','var(--poet)','🎼'),'majp':('大先知书','var(--majp)','🔥'),'minp':('小先知书','var(--minp)','📯'),'gosp':('福音书','var(--gosp)','✝️'),'acts':('教会历史','var(--acts)','🕊️'),'paul':('保罗书信','var(--paul)','✉️'),'gen':('普通书信','var(--gen)','📨'),'rev':('预言书','var(--rev)','👑')}
def _chipcut(s,n):
    """v5: short chip text — cut at a clause boundary, never mid-parenthesis."""
    import re as _re
    t=_re.split(r'[（(，,；;。]',s)[0].strip() or s
    return t if len(t)<=n else t[:n-1]+'…'

def parse(fn):
    out=[]
    for blk in open(fn).read().split('@@')[1:]:
        lines=blk.strip().split('\n'); h=lines[0].split('|')
        b={'n':int(h[0]),'id':h[1],'name':h[2],'en':h[3],'cat':h[4],'ch':int(h[5]),'kv':[]}
        for ln in lines[1:]:
            if ':' not in ln: continue
            k,v=ln.split(':',1); v=v.strip()
            if k=='kv': t,r=v.split('##'); b['kv'].append((t.strip(),r.strip()))
            else: b[k]=v
        for k in ['one','au','dt','bg','why','ol','core','xc','cov','hard','app','mn','cf']: assert k in b,(b['name'],k)
        out.append(b)
    return out
import os
_D=os.path.dirname(os.path.abspath(__file__))
BOOKS=parse(os.path.join(_D,'books_ot1.txt'))+parse(os.path.join(_D,'books_ot2.txt'))+parse(os.path.join(_D,'books_nt.txt'))
assert [b['n'] for b in BOOKS]==list(range(1,67)),[b['n'] for b in BOOKS]
def _kw(k):
    """v11.2: header keyword never ends with 之书/的书 (救赎之书→救赎)"""
    return re.sub(r'[之的]书(”?)(（[上下]）)?$',r'\1\2',k)
for _b in BOOKS:
    if '：' in _b['one']:
        _k,_r=_b['one'].split('：',1); _b['one']=_kw(_k)+'：'+_r
    assert not re.match(r'^[^：]*[之的]书”?(（[上下]）)?：',_b['one']),_b['one']
V2={}
for _l in open(os.path.join(_D,'books_v2.txt')):
    _id,_r=_l.rstrip('\n').split('|',1); _k,_t=_r.split('|trap:'); V2[_id]={'key':[x.strip() for x in re.split(r'\s*\|\s*',_k.replace('key:','',1).strip()) if x.strip()],'trap':_t.strip()}
def qmark(t,auto=True): return rich(t,auto)
PAL=['#ffcb5c','#ff6fa5','#b78cff','#5cc8ff','#3ee0a1','#ff9f43','#2dd4bf','#f472b6']
RNG=re.compile(r'^\s*(\d+)(?::(\d+))?(?:\s*[–-]\s*(\d+)(?::(\d+))?)?\s*(.*)$')
def _au(a):
    a=re.split(r'[（(；;]',a)[0]
    a=re.sub(r'^(犹太)?传统[：:]','',a).replace('为主','').strip()
    if a.startswith('不详'): return '不详'
    p=re.split(r'[、，,]',a)
    a=p[0]+('等' if len(p)>1 and p[1].strip() else '')
    return a[:8]
_DTO={58:'主后70年前',19:'主前约1440–450',34:'主前约650',18:'族长时代',8:'主前约1150'}
def _dt(n,d):
    if n in _DTO: return _DTO[n]
    d=d.split('；')[0]
    m=re.search(r'(约)?(主[前后])(约)?(\d+)(?:\s*[–-]\s*约?(\d+))?',d)
    if not m: return d[:10]
    ap=bool(m.group(1) or m.group(3) or '左右' in d or '前后' in d[m.end():m.end()+4])
    return m.group(2)+('约' if ap else '')+m.group(4)+('–'+m.group(5) if m.group(5) else '')
def mnp(m):
    mm=re.match(r'^(“[^”]+”)\s*（(.*)）$',m)
    if mm: return f'<p class="mn"><span class="mnq">{E(mm.group(1))}</span><span class="mnx">{E(mm.group(2))}</span></p>'
    return f'<p class="mn"><span class="mnq">{E(m)}</span></p>'
def sbar(b):
    items=[x.strip() for x in b['ol'].split('|')]; segs=[]
    for it in items:
        m=RNG.match(re.sub(r'^卷\S+\s+','',it))
        if not m: return ''
        c1=int(m.group(1)); v1=int(m.group(2) or 1); e=m.group(3); segs.append([c1+(v1-1)/60,int(e) if e else c1,m.group(5)])
    verse_mode=b['ch']==1
    tot=(max(s_[1] for s_ in segs) if verse_mode else b['ch'])+1
    if not verse_mode and segs[0][0]>1.5: return ''
    w=[]
    for i,sg in enumerate(segs):
        nx=segs[i+1][0] if i+1<len(segs) else tot
        w.append(max(nx-sg[0],.35))
    T=sum(w); sp=''; lg=''
    for i,(sg,ww) in enumerate(zip(segs,w)):
        col=PAL[i%len(PAL)]; lab=re.split(r'[：:（(，,、；;—]',sg[2])[0].strip()[:8]
        rng=' '.join(items[i].split(' ')[:2]) if items[i].startswith('卷') else items[i].split(' ')[0]
        rs=re.sub(r'^卷\S+\s+','',rng); f=ww/T
        def fit(W):
            seg=f*W
            if len(lab)*11.5+12<=seg: return ''
            if len(rs)*6.0+6<=seg: return 'n'
            return 'x'
        cls=' '.join(c for c in (('p'+fit(310)) if fit(310) else '',('w'+fit(620)) if fit(620) else '') if c)
        sp+=f'<span class="{cls}" style="flex:{f*100:.2f} 1 0;background:{col};transition-delay:{i*.08:.2f}s" title="{E(items[i])}"><b class="l">{E(lab)}</b><b class="r">{E(rs)}</b></span>'
        txt=items[i][len(rng):].strip() if items[i].startswith(rng) else items[i]
        lg+=f'<li><i style="background:{col}"></i><b class="rg">{E(rs if not items[i].startswith("卷") else rng)}</b><span>{qmark(txt,False)}</span></li>'
    return f'<div class="sbar" role="img" aria-label="{E(b["name"])}结构图">{sp}</div><ol class="sleg2">{lg}</ol>'
V4={}
for _l in open(os.path.join(_D,'books_v4.txt')):
    _m=re.match(r'^(\w+)\|前因：(.*?)\s*\|\s*后果：(.*?)\|文学：(.*)$',_l.rstrip('\n'))
    V4[_m.group(1)]={'pre':_m.group(2).strip(),'post':_m.group(3).strip(),'lit':_m.group(4).strip()}
_USED=set()
import json as _json
try: BKH=_json.load(open(os.path.join(_D,'data','bkh.json')))
except Exception: BKH={}
def confline(b):
    for c in [x.strip() for x in b['cf'].split(',')]:
        k=c if not c.startswith('DT') else 'DT'+c[2:].replace('.','_')
        if k not in SRC or k in _USED: continue
        t=re.sub(r'^答：','',SRC[k][0].strip())
        cl=re.split(r'[。；？！]',t)[0].strip()
        if 10<=len(cl)<=80 and '“' not in cl and '\n' not in cl:
            _USED.add(k); return co('conf','<p>'+rich('{{'+k+'|'+cl+'}}',False)+'</p>','认信一句（逐字）')
    # fallback (v8): any sentence/clause of the linked articles, 10–80 chars, even if the key was already used elsewhere
    for c in [x.strip() for x in b['cf'].split(',')]:
        k=c if not c.startswith('DT') else 'DT'+c[2:].replace('.','_')
        if k not in SRC: continue
        t=re.sub(r'^答：','',SRC[k][0].strip())
        for cl in re.split(r'[。；？！\n]',t):
            cl=cl.strip()
            if 10<=len(cl)<=80 and '“' not in cl and '”' not in cl and '（' not in cl:
                return co('conf','<p>'+rich('{{'+k+'|'+cl+'}}',False)+'</p>','认信一句（逐字）')
    return ''
def v4strip(b):
    """v11.2: 前因 / 后果 in one compact two-row (wide: two-column) card; middle box removed"""
    x=V4[b['id']]
    return (f'<div class="causal2"><div class="cz pre"><b>⏮️ 前因</b><span>{rich(x["pre"])}</span></div>'
            f'<div class="cz post"><b>⏭️ 后果</b><span>{rich(x["post"])}</span></div></div>')
_DR=re.compile(r'(记事|事件)?(在)?约?主[前后]约?\d+(?:\s*[–-]\s*约?\d+)?年?(左右|前后)?')
_DTX={4:'记事38年多；成书于摩押平原',19:'最早为诗90（摩西）；约主前450年前后编辑完成',34:'主前663年底比斯（挪亚们）陷落（3:8）之后、612年尼尼微陷落之前'}
def dtx(b):
    """v11.2: the part of 'dt' NOT already shown by the header date chip"""
    if b['n'] in _DTX: return _DTX[b['n']]
    d=b['dt']; m=_DR.search(d); r=d
    if m and m.start()<=3: r=(d[:m.start()]+d[m.end():]).strip()
    r=re.sub(r'^[；，、代前]','',r).strip()
    mm=re.match(r'^（([^）]*)）(.*)$',r)
    if mm: r=mm.group(1)+('；' if mm.group(2) and not mm.group(2).startswith(('；','成书')) else '')+mm.group(2)
    return re.sub(r'^[；，、]','',r).strip()
def bgnote(b):
    """v11.2: author/date block removed (dup of header chips); unique facts folded here"""
    a=b['au']; ax=a if len(a)>len(_au(a))+1 else ''; d=dtx(b)
    if not ax and not d: return ''
    return '<p class="bgnote">'+(f'<span>✍️ {qmark(ax,False)}</span>' if ax else '')+(f'<span>🕰️ {qmark(d,False)}</span>' if d else '')+'</p>'
def liubox(b):
    """v12: 刘道顺《新旧约圣经全景》要义 — same 5-part block on all 66 cards"""
    from liu_data import LIU
    L=LIU[b['id']]; i=b['id']
    st=''.join(f'<span>{qmark(x.strip(),False)}</span>' for x in L['s'].split('｜'))
    KC=lambda t:re.sub(r'((?:核心|中心)章\s?(?:是)?第?\s?\d+(?:[–-]\d+)?章|钥节\s?\d+:\d+(?:-\d+)?)',r'<<\1>>',t)
    ps=''.join(f'<li>{qmark(KC(p))}</li>' for p in L['p'])
    r=co('info','<p>'+qmark(L['r'],False)+'</p>','🧭 改革宗校准') if L.get('r') else ''
    return (f'<div class="box span2 liu"><h4 class="h" id="b-{i}-liu">📜 全景要义 · 刘道顺</h4>'
            f'<p class="lth"><mark class="hy">{qmark(L["t"],False)}</mark></p><div class="lst">{st}</div><ol class="lps">{ps}</ol>'
            f'{co("xc","<p>"+qmark(L["x"],False)+"</p>","见证基督")}{r}'
            f'<p class="srcline">要义转述自 刘道顺《新旧约圣经全景》 · <a href="panorama.html">全景页 →</a></p></div>')
def card(b):
    import xref as _XF
    cl,col,ic=CATS[b['cat']]; x=V2[b['id']]; i=b['id']
    ol=''.join(f'<li>{qmark(re.sub(r"^(\S+)",r"**\1**",x_.strip(),count=1),False)}</li>' for x_ in b['ol'].split('|'))
    app=''.join(f'<li>{qmark(x_.strip())}</li>' for x_ in b['app'].split('|'))
    kv=''.join((f'<blockquote class="v must"><span class="star">★ 必背</span><span class="vt">{E(t)}</span><cite>— {E(r)}（和合本）</cite></blockquote>' if j==0 else verse(E(t),E(r))) for j,(t,r) in enumerate(b['kv']))
    cf=b['cf'].split(',')
    chips=''.join(f'<span class="tag" style="color:var(--vio)">{conflabel(s_)}</span>' for s_ in cf)
    test='旧约' if b['n']<=39 else '新约'
    one=re.sub(r'^([^：]{2,14})：',r'**\1**：',b['one'],count=1)
    core=re.sub(r'(“[^”{}]{4,60}”)',r'==\1==',b['core'],count=1)
    keys=''.join(f'<li>{qmark(k,False)}</li>' for k in x['key'])
    H=lambda k,t:f'<h4 class="h" id="b-{i}-{k}">{t}</h4>'
    ph=BKH.get(i,{})
    return f'''<article class="bk" id="bk-{i}" data-cat="{b['cat']}" data-t="{'ot' if b['n']<=39 else 'nt'}" style="--c:{col};--phd:{ph.get('d',1500)}px;--pht:{ph.get('t',2100)}px;--phm:{ph.get('m',3000)}px;--pfd:{ph.get('D',1700)}px;--pft:{ph.get('T',2300)}px;--pfm:{ph.get('M',3300)}px">
<header><div class="bhd"><div class="no">{b['n']}</div><h3 class="h" id="b-{i}" data-num="{b['n']}" data-toc="{E(b['name'])}">{ic} {b['name']}<small>{b['en']} · {b['ch']}章</small></h3>
</div><div class="chips bchips"><span class="chip" style="border-color:{col};color:{col}">{cl}</span><span class="chip">{test}第{b['n'] if b['n']<=39 else b['n']-39}卷</span><span class="chip" title="{E(b['au'])}">✍️ {E(_au(b['au']))}</span><span class="chip" title="{E(b['dt'].split('；')[0])}">🕰️ {E(_dt(b['n'],b['dt']))}</span></div>
<div class="one">💡 {qmark(one)}</div></header>
<div class="body" data-lazy><template>
{v4strip(b)}
<div class="bgrid">
<div class="box span2">{H('ol','🧩 结构大纲 · 结构图')}{sbar(b) or '<ol class="outline">'+ol+'</ol>'}</div>
{liubox(b)}
<div class="box">{H('bg','🏺 真实背景 · 受众')}<p>{qmark(b['bg'])}</p>{bgnote(b)}</div>
<div class="box">{H('why','🎯 为什么写')}<p>{qmark(b['why'])}</p></div>
<div class="box">{H('core','💎 核心信息 · 基督中心')}<p class="sideb">{qmark(core)}</p>{co('xc','<p>'+qmark(b['xc'])+'</p>','基督')}</div>
<div class="box">{H('cov','🤝 圣约位置')}<p>{qmark(b['cov'])}</p></div>
<div class="box">{H('lit','📐 文学视角 · 写了什么')}<p>{qmark(V4[b['id']]['lit'])}</p>{confline(b)}</div>
<div class="box">{H('kv','📖 关键经文')}{kv}</div>
<div class="box">{H('hard','⚠️ 难点 · 易错')}{co('hardc','<p>'+qmark(b['hard'])+'</p>','难点辨析')}{co('trap','<p>'+qmark(x['trap'],False)+'</p>','易错点')}</div>
<div class="box">{H('app','🌱 应用')}{co('app','<ul>'+app+'</ul>','教牧应用')}</div>
<div class="box">{H('key','🧠 核心三要点 · 记忆口诀')}{co('core','<ol>'+keys+'</ol>','核心三要点')}{co('mnc',mnp(b['mn']),'记忆口诀')}</div>
<div class="box">{H('rel','🔗 相关书卷 · 跨卷连接')}{_XF.chips(i) or '<p class="srcline">（本数据集暂无）</p>'}<p class="srcline">全部 {len(_XF.XR)} 条精选连接与弧线图 → <a href="compare.html#xref">跨卷连接网络</a></p></div>
</div>
<details class="dx" style="margin-top:10px"><summary>📚 认信连接（三项联合信条原文，逐字引自 ccifellowship.org）{chips}</summary><div class="in">{confref(b['cf'])}</div></details>
</template></div></article>'''
def canon_grid(sel=None):
    out=[]
    for b in BOOKS:
        if sel and not sel(b): continue
        cl,col,ic=CATS[b['cat']]; pg='ot.html' if b['n']<=39 else 'nt.html'
        out.append(f'<a href="{pg}#b-{b["id"]}" style="--c:{col}" title="{b["name"]}：{E(b["one"][:40])}">{b["name"].replace("书","") if len(b["name"])>4 else b["name"]}<small>{b["ch"]}章</small></a>')
    return '<div class="canon">'+''.join(out)+'</div>'
def legend(keys):
    return '<div class="legend">'+''.join(f'<span style="--c:{CATS[k][1]}"><i></i>{CATS[k][2]} {CATS[k][0]}</span>' for k in keys)+'</div>'
