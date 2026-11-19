# v12: 刘道顺《新旧约圣经全景》整合页 panorama.html
from lib import *
from books import BOOKS,CATS,qmark
from liu_data import LIU,LIU_INTRO
SRC_LIU='刘道顺《新旧约圣经全景》（房角石）'
ERAS=[('🌍','创造·堕落','创1–11','gen','圣经的苗圃：三问——神做了什么？人如何回应？神又怎样做？','#ffcb5c'),
('⛺','族长','创12–50 · 约2100–1800 BC','gen','应许与起誓：后裔、土地、福气','#ff9f43'),
('🌊','出埃及·律法','出–申 · 1446–1406 BC','exo','救赎→圣幕→信心之战→约的更新','#ff6fa5'),
('⚔️','征服·士师','书–得 · 1406–1050 BC','jos','安息的预表；没有王时神已预定一位王','#f472b6'),
('👑','联合王国','撒上–王上11 · 1050–931 BC','2sa','神政王国：大卫之约（撒下7）','#b78cff'),
('💔','分裂王国','王上12–王下 · 931–586 BC','1ki','地上宝座更迭，天上宝座不变；先知是天上之王的使臣','#8b9cff'),
('⛓️','被掳','哀·结·但 · 605–538 BC','eze','锡安之死、荣光离开；至高者在人的国中掌权','#5cc8ff'),
('🧱','归回','拉·尼·斯·该·亚·玛 · 538–430 BC','hag','计划没有中断；后来的荣耀必大过先前','#2dd4bf'),
('🕯️','四百年','玛拉基→施洗约翰','mal','「我曾爱你们」——影儿等待实体','#3ee0a1'),
('✝️','基督','四福音 · AD 前6–30','mat','实体显明：王·仆人·人子·神子；「你们说我是谁？」','#ffd27a'),
('🕊️','教会','徒–犹 · AD 30–95','act','父所应许的圣灵：从耶路撒冷到罗马；教义→「所以，弟兄们」','#7dd3fc'),
('🏙️','成全','启示录','rev','宝座与羔羊：神的帐幕在人间','#fbbf24')]
def eraflow():
    o='<ol class="rhflow loop rv" aria-label="救赎史全景流程（刘道顺）">'
    for i,(ic,t,d,bid,k,col) in enumerate(ERAS):
        o+=f'<li style="--c:{col};--i:{i}"><a href="index.html#b-{bid}"><span class="rn">{i+1}</span><span class="ri">{ic}</span><b>{t}</b><small>{E(d)}</small><span class="rk">{qmark(k,False)}</span></a></li>'
    return o+'</ol>'
def card66(sel,title):
    bs=[b for b in BOOKS if sel(b)]
    o=f'<div class="lgrid rv" aria-label="{E(title)}">'
    for b in bs:
        L=LIU[b['id']]; col=CATS[b['cat']][1]
        o+=(f'<a class="lcard" href="index.html#b-{b["id"]}" style="--c:{col}"><span class="lch">{b["ch"]}</span><b>{E(b["name"])}</b>'
            f'<span class="lt">{qmark(L["t"],False)}</span></a>')
    return o+'</div>'
def chain(items,cls='lchain'):
    return f'<ol class="{cls} rv">'+''.join(f'<li style="--i:{i}"><span class="ce">{ic}</span><b>{E(t)}</b><small>{qmark(d,False)}</small></li>' for i,(ic,t,d) in enumerate(items))+'</ol>'
def rings():
    n=['预知','预定','呼召','称义','荣耀']
    cs=['#ffcb5c','#ff6fa5','#b78cff','#5cc8ff','#3ee0a1']
    g=''.join(f'<circle class="flow" cx="{60+i*70}" cy="60" r="44" fill="none" stroke="{cs[i]}" stroke-width="7"/><text x="{60+i*70}" y="{64 if i%2==0 else 64}" text-anchor="middle" font-size="16" fill="currentColor" font-weight="700">{n[i]}</text>' for i in range(5))
    return f'<figure class="rings loop rv"><svg viewBox="0 0 400 120" role="img" aria-label="罗马书8:29-30 黄金五环">{g}</svg><figcaption class="srcline">「黄金五环」（罗8:29-30）：神一旦拣选、呼召、称义，就必带入荣耀——五环绝不断开（多特信经第五要点：圣徒的坚忍）</figcaption></figure>'
def build():
    I=LIU_INTRO
    c=[f'''<section class="hero reveal"><div class="chips"><span class="chip g">📜 新旧约全景</span><span class="chip">刘道顺 牧师</span><span class="chip">救赎史观点</span><span class="chip">66卷一卷一句</span></div>
<h1>登高远望：<em>先见森林，再看树木</em></h1><p class="lead">{qmark(I["one"],False)}</p>
<p class="srcline">本页为 {SRC_LIU} 全书（序言、序论、66卷全景、先知书序论、书信序论、附录）的要义转述与可视化；引号内短语为原书用语。凡与三项联合信条需要校准之处，均以 🧭 标出。</p></section>''']
    c.append(legend_box())
    c.append(h2('method','🔭','读经法：远观→微观'))
    c.append(h3('far','登高远望：从整体到部分'))
    c.append(chain([('🏔️','远观','整本圣经的主题：神的拯救计划（救赎史）'),('🌳','主干','旧约主题：神应许差遣弥赛亚；新约主题：拿撒勒人耶稣就是那基督'),('🌿','枝节','66卷各卷的主题，以及它们如何一脉相承'),('🔬','微观','各章核心 → 逐节细读')]))
    c.append(co('core','<p>'+qmark(I['ot'],False)+'</p>','刘牧师的方法'))
    c.append(h3('three','三问读每一卷'))
    c.append('<div class="grid g3 rv">'+''.join(f'<div class="card tile" style="--c:{col}"><div class="big">{ic}</div><h4>{t}</h4><p>{qmark(d,False)}</p></div>' for ic,t,d,col in [('🙌','① 神做了什么？','创造、按形象造人、立约——先知道 ==神为我们做了什么==','var(--gold)'),('🙇','② 人如何回应？','不信神的话、背约（何6:7）——~~罪的根在「不信」~~','var(--red)'),('✝️','③ 神又怎样做？','尽管如此，神仍应许「女人的后裔」并信守到底——++恩典++','var(--emer)')])+'</div>')
    c.append(h3('spine','66卷是一本书：圣经的「脊椎」'))
    c.append('<div class="grid g2 rv">'+note('🦴 脊椎与架构','<p>'+qmark(I['spine'],False)+'</p><p>'+qmark(I['key'],False)+'</p>')+note('🧭 改革宗校准','<p>'+rich('这正是改革宗「圣约—救赎史」读经：霍志恒（Vos）的圣经神学、巴文克（Bavinck）称之为**「神的大事」**，里德波斯（Ridderbos）称为**「神的国」**，德格拉夫（De Graaf）称为**「应许与救恩」**。海德堡要理问答第19问：福音是{{HC19|这福音是神首先在伊甸园里亲自启示，后来由族长和众先知宣告}}。',False)+'</p>')+'</div>')
    c.append(h2('flow','🌊','救赎史全景流程'))
    c.append(h3('eras','十二段：一条线串起66卷'))
    c.append(eraflow())
    c.append(co('mnc','<p>'+qmark('口诀：**创·族·出·征，王·分·掳·归，四百年后基督来，教会传到地极，宝座羔羊成全**',False)+'</p>','十二段口诀'))
    c.append(h3('presence','以马内利的轨迹：神住在人中间'))
    c.append(chain([('🌳','伊甸','神与人同住'),('⛰️','西奈','神降临山上，人不可近'),('⛺','圣幕','「使我可以住在他们中间」（出25:8）；荣光充满（出40:34）'),('🏛️','圣殿','火从天降、荣光充满（代下7:1-2）'),('🔥','荣光离开','殿被焚——罪不在建筑，在人心（结10）'),('🧱','第二殿','「后来的荣耀必大过先前的荣耀」（该2:9）'),('✝️','基督','「道成肉身，住在我们中间」＝支搭帐幕（约1:14）'),('🕊️','教会','圣灵充满的不是楼房，而是120人；身子是圣灵的殿（林前6:19）'),('🏙️','新耶路撒冷','「神的帐幕在人间」（启21:3）')],'lchain wide'))
    c.append(h3('renew','约的更新链'))
    c.append(mer('''flowchart LR
A["🤝 亚伯拉罕之约<br/>起誓应许（创22:16）"]-->S["⛰️ 西奈之约<br/>第一代"]-->M["📜 摩押更新<br/>第二代（申29）"]-->J["🪨 示剑更新<br/>约书亚（书24）"]-->N["🧱 归回更新<br/>尼希米（尼9:38）"]-->C["🍷 新约<br/>「我立约的血」（太26:28）"]-->L["🍞 圣餐中常常更新<br/>直等他来（林前11:26）"]
style C fill:#5a4614,stroke:#f5c76b''','刘牧师：申命记的主题是「约的更新」，这条线一直延伸到基督与圣餐'))
    c.append(h3('seeds','两后裔之争：从创3:15到启示录'))
    c.append(chain([('🐍','创3:15','女人的后裔 ⚔️ 蛇的后裔'),('🩸','该隐 × 亚伯','第一次分离与敌对'),('👶','以扫 × 雅各','利百加腹中「两国」（创25:23）'),('⛰️','以东 × 以色列','以扫的山 × 锡安山（俄巴底亚书）'),('📜','哈曼 × 末底改','要灭弥赛亚所出的民族（以斯帖记）'),('👑','希律 × 耶稣','谁是真正的犹太人之王（太2）'),('🐉','龙 × 羔羊','古蛇被扔在火湖里（启20:10）')]))
    c.append(h3('throne','宝座与羔羊：以赛亚书 × 启示录'))
    c.append('<div class="grid g2 rv">'+note('👑 宝座（赛6 · 启4）','<p>'+qmark('乌西雅王崩的那年，以赛亚「见主坐在高高的宝座上」：==看得见的王背后有看不见的王==。约翰在拔摩海岛也先看见宝座。地上的宝座更迭，天上的宝座永不改变（列王纪）。',False)+'</p>')+note('🐑 羔羊（赛53 · 启5）','<p>'+qmark('赛53是旧约的核心：担罪的羔羊。启示录「羔羊」约30次——「有羔羊站立，像是被杀过的」（启5:6）。++颂赞归给坐宝座的和羔羊++（启5:13；7:10）。',False)+'</p>')+'</div>')
    c.append(h2('ot','📗','旧约39卷 · 一卷一句'))
    c.append(co('info','<p>'+qmark(LIU['proph']['t']+'：'+'；'.join(LIU['proph']['p']),False)+'</p>','先知书序论'))
    for k,t in [('law','律法书'),('hist','历史书'),('poet','诗歌智慧书'),('majp','大先知书'),('minp','小先知书')]:
        c.append(h3('ot-'+k,f'{CATS[k][2]} {t}'))
        c.append(card66(lambda b,k=k:b['cat']==k,t))
    c.append(co('core','<p>'+qmark(LIU['otend']['p'][0]+'；'+LIU['mal']['p'][2],False)+'</p>','旧约全景的结论'))
    c.append(h2('nt','📘','新约27卷 · 一卷一句'))
    c.append(co('info','<p>'+qmark('；'.join(LIU['ntpre']['p']),False)+'</p>','新约全景序言'))
    c.append(h3('nt-gosp','✝️ 四福音：四幅肖像，一个问题'))
    c.append('<div class="grid g4 rv">'+''.join(f'<div class="card tile" style="--c:{col}"><div class="big">{ic}</div><h4>{n} · {p}</h4><p>{qmark(d,False)}</p></div>' for ic,n,p,d,col in [('👑','马太','王','亚伯拉罕的后裔、大卫的子孙（1:1）；分割点 16:15','var(--gold)'),('🐂','马可','仆人','舍命作多人的赎价（10:45）；分割点 8:29','var(--red)'),('🧑','路加','人子','寻找拯救失丧的人（19:10）；分割点 9:20','var(--sky)'),('🦅','约翰','神子','太初有道；七神迹＋七「我是」；叫你们信（20:31）','var(--vio)')])+'</div>')
    c.append(co('core','<p>'+qmark('对观福音都在中间位置问==「你们说我是谁？」==：前半见证 **耶稣是谁**（应许的弥赛亚），后半见证 **他为什么来**（十字架与复活）。四福音四侧面，正如利1–5章五种祭共同预表基督。',False)+'</p>','福音书的骨架'))
    c.append(card66(lambda b:b['cat'] in('gosp','acts'),'福音书与使徒行传'))
    c.append(h3('nt-epis','✉️ 书信：先教义，后「所以，弟兄们」'))
    c.append(chain([('🚂','车头＝福音（教义）','神为我们做了什么：坚固信仰'),('🚃','车厢＝伦理（实践）','我们当怎样生活：活出真理'),('⏳','唯一未成就的应许','主的再来（约一3:3）')]))
    c.append(card66(lambda b:b['cat'] in('paul','gen'),'书信'))
    c.append(rings())
    c.append(h3('nt-rev','👑 启示录：创世记的回响'))
    c.append(table(['创世记 1–3','启示录 20–22'],[['起初神创造天地','我又看见一个新天新地（21:1）'],['古蛇引诱人犯罪','那龙就是古蛇……被扔在火湖里（20:2,10）'],['地受咒诅，人必死','以后再没有咒诅；不再有死亡（22:3；21:4）'],['被逐出伊甸，生命树被把守','生命树在城中，叶子医治万民（22:2）'],['那人独居不好','羔羊的婚筵：末后亚当的新妇（19:7）'],['神与人同在园中','神的帐幕在人间（21:3）']],'cmp2'))
    c.append(card66(lambda b:b['cat']=='rev','启示录'))
    c.append(h2('keys','🗝️','十把钥匙：贯穿全书的救赎史主题'))
    K=[('🌱','两后裔','创3:15贯穿全本：诗1两条路、俄巴底亚、以斯帖、希律','gen,psa,oba,est'),('🤝','约的更新','申29、书24、尼9:38 → 基督立约的血','deu,jos,neh'),('⛺','以马内利','圣幕→圣殿→基督→教会→新耶路撒冷','exo,2ch,hag,jhn'),('🏞️','安息','迦南是预表的安息，真安息在基督（来4）','jos,heb'),('👑','神政王国','神是真正的王；王制只是弥赛亚国的预表','1sa,2sa,1ki,dan'),('🩸','代赎','按手转嫁、祭物必死、若不流血罪不得赦','lev,heb'),('📯','耶和华的日子','历史的审判叠合末日审判（复合性）','joe,zep,mal'),('⚖️','因信称义','义人因信得生：哈2:4→罗1:17→宗教改革','hab,rom,gal'),('🕊️','圣灵施行','父定、子成就、灵施行：五旬节与教会','act,eph'),('🐑','宝座与羔羊','赛6+赛53 → 启4–5','isa,rev')]
    c.append(table(['钥匙','要义','代表书卷'],[[f'{ic} <b class="k">{t}</b>',qmark(d,False),' '.join(f'<a href="index.html#b-{x}" class="tag">{[b["name"] for b in BOOKS if b["id"]==x][0]}</a>' for x in bs.split(','))] for ic,t,d,bs in K]))
    c.append(h2('calib','🧭','与三项联合信条的校准'))
    c.append('<p>'+qmark('刘牧师的整体框架（救赎史、基督中心、因信称义、神的主权与护理）与欧陆改革宗高度一致；以下几处做 ;;认信校准;;：',False)+'</p>')
    rows=[]
    for bid in [b['id'] for b in BOOKS]:
        L=LIU[bid]
        if L.get('r'): rows.append([f'<a href="index.html#b-{bid}">{[b["name"] for b in BOOKS if b["id"]==bid][0]}</a>',qmark(L['t'],False),qmark(L['r'],False)])
    c.append(table(['书卷','刘牧师要义','🧭 改革宗校准'],rows))
    c.append(co('conf','<p>'+rich('总原则：一切解释都要「以经解经」，合乎信仰的类比。比利时信条第7条：{{BC7|我们相信，圣经中包含了神全部的旨意}}。',False)+'</p>','认信原则'))
    A=LIU['appx']
    c.append(h2('preach','🎙️','附录：救赎史讲道法'))
    c.append(chain([('🐣','用福音生','先「用福音生了你们」（林前4:15）——每周至少一次见证福音本身'),('🍼','要成长','爱慕纯净的灵奶（彼前2:2）；约一2:12-14 小子·父老·少年人'),('🛡️','成为精兵','穿戴全副军装（弗6:10-13）：教会不是住院部，而是练兵场'),('📯','耶和华的军队','出埃及的乌合之众被称为「耶和华的军队」（出12:41）')]))
    c.append('<div class="grid g2 rv">'+note('⚠️ 今天讲道的三病','<ol><li>'+qmark('**无骨架**：没有脊椎——内部装修有瑕疵可修，架构有问题须重建',False)+'</li><li>'+qmark('**无视历史性**：断章取义 → ~~没有家谱的信仰~~',False)+'</li><li>'+qmark('**使圣经难解**：在基督与众人之间竖墙；圣经的核心是基督',False)+'</li></ol>','hardc')+note('✅ 好讲道的三性','<ol><li>'+qmark('**历史性**：每篇讲道是救赎史中的一个章回',False)+'</li><li>'+qmark('**统一性**：只有一个主题、一个主人公、一位计划和完成者',False)+'</li><li>'+qmark('**渐进性**：从影儿到实体，层层展开',False)+'</li></ol>')+'</div>')
    c.append(co('app','<ul>'+''.join(f'<li>{qmark(x,False)}</li>' for x in ['讲道＝传讲神 ==全备的旨意==（徒20:27）——不是讨人喜欢的话，而是于人有益的话','跪着把经文读 **30遍**，先默想后参考','浓缩成一句：「通过今天的经文，神要说的话就是……」','必须有应用：没有应用的讲道如同流产'])+'</ul>','讲道前的准备'))
    c.append(f'<p class="srcline">资料：{SRC_LIU}；1995 年旧约序言、新约序言（羊圈教会）。本页为要义转述，非原文全文；书卷要义亦见每卷书卡片中的「📜 全景要义」。</p>')
    return page('panorama.html','新旧约全景 · 刘道顺 — 救赎史一卷一句','\n'.join(c))
