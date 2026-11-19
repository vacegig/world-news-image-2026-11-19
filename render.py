"""Deterministic newspaper front page renderer."""
from PIL import Image, ImageDraw, ImageFont
import math, random

S=3; W=H=1024
BG='#F5F2E9'; INK='#1C2025'; NAVY='#17354C'; RED='#A72F43'; BLUE='#386D9D'; GREEN='#367658'; OCHRE='#C28A42'; GREY='#87877F'; PANEL='#FBFAF5'; RULE='#C9C5BA'; WHITE='#fffefa'
im=Image.new('RGB',(W*S,H*S),BG); d=ImageDraw.Draw(im)
serif='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'; serif_b='/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'; italic='/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf'; sans='/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf'; sans_b='/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf'
def P(v): return round(v*S)
def F(size,face='sans'):
    return ImageFont.truetype({'sans':sans,'bold':sans_b,'serif':serif,'serifb':serif_b,'italic':italic}[face],P(size))
def text(x,y,t,size=9,color=INK,face='sans',anchor=None): d.text((P(x),P(y)),t,font=F(size,face),fill=color,anchor=anchor)
def line(x1,y1,x2,y2,color=RULE,w=.6): d.line((P(x1),P(y1),P(x2),P(y2)),fill=color,width=max(1,P(w)))
def rect(box,fill=None,outline=None,w=.6): d.rectangle(tuple(P(v) for v in box),fill=fill,outline=outline,width=max(1,P(w)))
def ellipse(box,fill=None,outline=None,w=.7): d.ellipse(tuple(P(v) for v in box),fill=fill,outline=outline,width=max(1,P(w)))
def poly(points,fill,outline=None): d.polygon([(P(x),P(y)) for x,y in points],fill=fill)
def wrap(s, ft, maxw):
    words=s.split(); out=[]; cur=''
    for word in words:
        test=(cur+' '+word).strip()
        if d.textlength(test,font=ft)>P(maxw) and cur: out.append(cur); cur=word
        else: cur=test
    if cur: out.append(cur)
    return out
def para(x,y,s,w,size,color,leading=None,face='sans',maxlines=99):
    ft=F(size,face); rows=wrap(s,ft,w)[:maxlines]; step=leading or size*1.22
    for i,row in enumerate(rows): d.text((P(x),P(y+i*step)),row,font=ft,fill=color)
    return len(rows)*step
def fit(s,maxw,size,face='serifb',minimum=7):
    while size>minimum and d.textlength(s,font=F(size,face))>P(maxw): size-=.2
    return size

# restrained paper grain
random.seed(19)
for _ in range(2100):
    x=random.randrange(W*S); y=random.randrange(H*S)
    im.putpixel((x,y),(232,229,219) if random.random()<.5 else (249,247,240))
d=ImageDraw.Draw(im)

# masthead
text(28,14,'THE WORLD IN ONE DAY',22,INK,'serifb')
text(996,22,"THURSDAY'S NEWS · ONE PAGE · 36 STORIES",8.4,NAVY,'bold','ra')
line(28,43,996,43,INK,1.1)
text(28,47,'Thursday 19 November 2026',31,INK,'serifb')
text(29,83,'Three leaders meet in Shenzhen · A court rules on Myanmar · The biggest IPO ever debuts',10,INK,'italic')
line(28,104,996,104,INK,.9)

# distribution strip
regions=[('EUROPE',6,BLUE),('THE AMERICAS',11,RED),('ASIA-PACIFIC',6,GREEN),('MIDEAST',5,OCHRE),('AFRICA',3,NAVY),('OCEANIA',3,GREY),('WORLD',2,INK)]
total=sum(n for _,n,_ in regions); x=28; avail=968
for lab,n,col in regions:
    width=avail*n/total
    rect((x,111,x+width-1,132),col)
    label=f'{lab}  {n}'; sz=fit(label,width-8,8,'bold',6.2)
    text(x+width/2,121,label,sz,WHITE,'bold','mm'); x+=width

# six statistical blocks
stats=[('$81.3bn','raised by Anthropic — the largest IPO on record'),('15.9m','GTA VI pre-orders banked before release day'),('200,000','evacuated ahead of Cyclone Akvan'),('$120bn','a year of adaptation finance unresolved at COP31'),('730,000','Rohingya who fled in 2017 — the ICJ case'),('16bn miles','Voyager 1 from Earth — one light-day out')]
sw=968/6
for i,(num,desc) in enumerate(stats):
    sx=28+i*sw
    if i: line(sx,139,sx,190,RULE,.55)
    text(sx+8,138,num,17,RED,'serifb')
    para(sx+8,161,desc,sw-17,7.1,INK,8.2,'sans',3)
line(28,194,996,194,INK,.65)

# original vector illustrations in a consistent editorial style
def illustration(kind,x,y,w,h):
    rect((x,y,x+w,y+h),NAVY)
    # paper-like framed color fields and horizon
    if kind=='summit':
        # skyline / diplomatic flags
        for j,(xx,ww,hh,col) in enumerate([(x+8,25,25,'#274b61'),(x+38,18,37,'#31566a'),(x+w-34,20,30,'#274b61')]): rect((xx,y+h-hh,xx+ww,y+h),col)
        line(x+10,y+h-19,x+w-10,y+h-19,'#b7c0b7',.8)
        for j,col in enumerate((BLUE,RED,WHITE)):
            xx=x+22+j*29; line(xx,y+11,xx,y+h-18,'#e6dfca',.8); rect((xx,y+12,xx+15,y+20),col)
        # meeting table and silhouettes
        ellipse((x+w/2-27,y+h-28,x+w/2+27,y+h-12),OCHRE)
        for j,col in enumerate((BLUE,RED,GREEN)):
            xx=x+w/2-16+j*16; ellipse((xx-3,y+17,xx+3,y+23),col); rect((xx-4,y+24,xx+4,y+h-23),col)
        ellipse((x+8,y+8,x+22,y+22),None,'#a3b3b1',.7)
    elif kind=='games':
        rect((x,y,x+w,y+h),'#654f50'); rect((x,y+h*.52,x+w,y+h),'#c98253')
        ellipse((x+w*.65,y+6,x+w*.87,y+28),'#e7bd78')
        # city skyline and palm silhouettes
        for j,(xx,ww,hh) in enumerate([(x+4,17,22),(x+26,14,31),(x+46,20,25),(x+w-42,15,35),(x+w-22,18,22)]): rect((xx,y+h-hh,xx+ww,y+h),NAVY)
        line(x+4,y+h-10,x+w-4,y+h-10,'#f2d5a6',.8)
        for xx in (x+18,x+w-18):
            line(xx,y+h-10,xx+3,y+18,'#182e3b',1.3)
            for dx in (-12,-7,5,11): line(xx+3,y+20,xx+dx,y+12,'#182e3b',1.4)
        ellipse((x+8,y+7,x+22,y+21),None,'#f2d5a6',.8)
    else:
        rect((x,y,x+w,y+h),'#223f50')
        # financial grid and rising graph
        for j in range(1,5): line(x+5,y+j*h/5,x+w-5,y+j*h/5,'#395366',.5)
        for j in range(1,7): line(x+j*w/7,y+5,x+j*w/7,y+h-5,'#304c5c',.4)
        pts=[(x+8,y+h-12),(x+25,y+h-21),(x+42,y+h-18),(x+59,y+h-32),(x+76,y+h-29),(x+94,y+13)]
        d.line([(P(a),P(b)) for a,b in pts],fill=OCHRE,width=P(2))
        for xx,yy in pts[1::2]: ellipse((xx-2,yy-2,xx+2,yy+2),RED)
        text(x+w-8,y+4,'ANT',8,WHITE,'bold','ra')

leads=[
('1','SHENZHEN · SUMMIT','Trump, Xi and Putin hold first three-way summit','The three nuclear powers meet at APEC in Shenzhen; arms control and the Iran war top the agenda.','summit'),
('2','NEW YORK · GAMES','GTA VI arrives after a 13-year wait','Rockstar’s sequel unlocks at midnight in each country, New Zealand first; 15.9m pre-orders banked. $79.99 on PS5 and Xbox, no PC yet. Leave requests jumped.','games'),
('3','NASDAQ · MARKETS','Anthropic debuts in the biggest IPO on record','Priced at $83, above its range, the Claude maker raised $81.3bn and is valued near $1.5tn. Thursday’s first trades set the real price. Up to a fifth went to retail.','markets')]
cw=(968-16)/3
for i,(num,loc,head,desc,kind) in enumerate(leads):
    x=28+i*(cw+8); y=201
    rect((x,y,x+cw,y+141),PANEL,RULE,.7)
    text(x+8,y+6,num,11,RED,'serifb'); text(x+25,y+8,loc,7.4,NAVY,'bold')
    illustration(kind,x+8,y+24,88,52)
    tx=x+104; tw=cw-112
    para(tx,y+25,head,tw,fit(head,tw,12,'serifb',9),INK,13,'serifb',3)
    para(tx,y+65,desc,tw,7.35,INK,9,'sans',7)

# secondary 4–13 in a two-row five-column grid
secondary=[
('4','THE HAGUE · LAW','World Court rules on Myanmar’s Rohingya case','The ICJ reads its judgment in The Gambia’s case over the 2017 campaign.','court'),
('5','ANTALYA · CLIMATE','COP31 enters its final 48 hours','Ministers take over the text in Antalya; “phase out” and the $120bn adaptation fund are still open.','climate'),
('6','ODISHA · STORM','Akvan bears down as 200,000 flee the coast','Red alerts in 11 districts, schools shut. Landfall near Puri due Friday.','storm'),
('7','KYIV · WAR','Left off the agenda, Ukraine watches Shenzhen','The war will not be raised at the summit, the White House says; Kyiv fears being carved up.','ukraine'),
('8','SHENZHEN · TRADE','APEC leaders adopt the Shenzhen Declaration','Twenty-one economies back digital trade and an Asia-Pacific community roadmap.','trade'),
('9','FLORIDA · WEATHER','Flooded Florida braces for still more rain','A foot of rain in hours in Hollywood; 300 rescue calls in a night. Schools shut Thursday.','florida'),
('10','SCIENCE · GEOLOGY','Earth’s missing billion years are explained','A Nature study blames mantle currents and ancient ice sheets for the erasure.','earth'),
('11','PARIS · POLITICS','Mélenchon could win, says France’s justice minister','The hard-left leader is a plausible president, the minister concedes.','france'),
('12','JAZAN · GULF','Saudi Arabia says danger has passed in three cities','The all-clear follows southern alerts after a Houthi missile was downed.','gulf'),
('13','BENGHAZI · CRIME','Cocaine and millions of pills seized in eastern Libya',"Officials display one of the country's biggest drug hauls, seized in the east.",'crime')]
colors=[BLUE,GREEN,OCHRE,BLUE,RED,GREY,GREEN,BLUE,OCHRE,RED]
def mini_art(x,y,w,h,k,col):
    # bespoke miniature scene, restrained to a shared single-line illustration language
    rect((x,y,x+w,y+h), '#e8e4d9')
    if k in ('court','france','trade'):
        # facade and columns, flag / trade lines
        rect((x+5,y+10,x+w-5,y+h-5),'#d5d0c4')
        poly([(x+4,y+11),(x+w/2,y+3),(x+w-4,y+11)],col)
        for xx in (x+10,x+20,x+30,x+40): rect((xx,y+13,xx+4,y+h-6),PANEL)
        line(x+4,y+h-4,x+w-4,y+h-4,NAVY,.8)
        if k=='france':
            rect((x+w-18,y+5,x+w-12,y+h-6),BLUE); rect((x+w-12,y+5,x+w-6,y+h-6),WHITE); rect((x+w-6,y+5,x+w,y+h-6),RED)
    elif k in ('climate','storm','florida'):
        # weather systems and landscape
        line(x+3,y+h-8,x+w-3,y+h-8,GREEN,1)
        if k=='climate': ellipse((x+w-19,y+4,x+w-7,y+16),OCHRE)
        else:
            for j in range(3): ellipse((x+6+j*10,y+7,x+21+j*10,y+19),GREY)
            for xx in (x+11,x+25,x+39): line(xx,y+19,xx-2,y+25,BLUE,1)
        if k=='storm':
            d.arc((P(x+14),P(y+3),P(x+40),P(y+h-1)),180,520,fill=BLUE,width=P(1.3))
        if k=='florida': line(x+4,y+h-5,x+w-3,y+h-5,BLUE,1.4)
    elif k in ('ukraine','gulf'):
        rect((x+5,y+5,x+w-5,y+h-5),'#ded8c9')
        if k=='ukraine': rect((x+7,y+8,x+w-7,y+15),BLUE); rect((x+7,y+15,x+w-7,y+22),'#d9b24e');
        else:
            for xx in (x+12,x+25,x+38): rect((xx,y+13,xx+6,y+h-5),OCHRE)
            poly([(x+8,y+13),(x+28,y+4),(x+47,y+13)],NAVY)
    elif k=='earth':
        for j,colr in enumerate((NAVY,BLUE,OCHRE,RED)):
            ellipse((x+5+j*4,y+5+j*3,x+w-5-j*4,y+h-4-j*3),None,colr,1)
    elif k=='crime':
        # abstract evidence silhouettes, no sensational detail
        for j in range(4):
            rect((x+8+j*10,y+7,x+14+j*10,y+h-7),None,RED,.8)
            line(x+7+j*10,y+10,x+15+j*10,y+10,NAVY,.7)

sec_x=28; sec_y=351; gap=6; scw=(968-4*gap)/5; sh=82
for i,(num,loc,head,desc,kind) in enumerate(secondary):
    col=i%5; row=i//5; x=sec_x+col*(scw+gap); y=sec_y+row*(sh+5)
    rect((x,y,x+scw,y+sh),PANEL,RULE,.55)
    text(x+5,y+4,num,9.2,RED,'serifb'); text(x+20,y+6,loc,6.1,NAVY,'bold')
    mini_art(x+5,y+19,48,31,kind,colors[i])
    para(x+58,y+19,head,scw-63,fit(head,scw-63,8.2,'serifb',6.2),INK,8.7,'serifb',3)
    para(x+5,y+53,desc,scw-10,6.55,INK,7.6,'sans',4)

# lower atlas: recognizable hand-drawn world map and 23 sequential briefs
lower_y=526
text(28,lower_y,'WHERE IT HAPPENED',9.2,NAVY,'bold')
text(284,lower_y,'ALSO ON THURSDAY 19 NOVEMBER — 23 MORE STORIES',9.2,NAVY,'bold')
line(28,lower_y+14,996,lower_y+14,INK,.65)
mx,my,mw,mh=28,lower_y+21,242,326
rect((mx,my,mx+mw,my+mh),NAVY)
# Mollweide-like grid
for frac in (.25,.5,.75):
    yy=my+mh*frac; line(mx+7,yy,mx+mw-7,yy,'#496273',.45)
for frac in (.25,.5,.75):
    xx=mx+mw*frac; d.arc((P(xx-mw*.16),P(my+5),P(xx+mw*.16),P(my+mh-5)),270,90,fill='#496273',width=P(.45))
# simplified, recognizable continental silhouettes
def map_poly(coords): poly([(mx+a*mw,my+b*mh) for a,b in coords],'#d8cfb4')
map_poly([(.08,.20),(.14,.12),(.25,.10),(.32,.16),(.29,.21),(.34,.25),(.30,.31),(.26,.33),(.23,.41),(.18,.39),(.16,.33),(.12,.31),(.10,.25)])
map_poly([(.28,.43),(.34,.42),(.37,.48),(.34,.55),(.35,.61),(.31,.72),(.28,.81),(.26,.73),(.25,.64),(.23,.56),(.25,.49)])
map_poly([(.44,.18),(.51,.14),(.60,.15),(.64,.19),(.73,.18),(.79,.23),(.78,.28),(.69,.30),(.65,.34),(.58,.33),(.55,.38),(.49,.34),(.46,.29),(.42,.27)])
map_poly([(.53,.37),(.60,.35),(.68,.40),(.70,.48),(.67,.54),(.65,.62),(.60,.71),(.56,.68),(.54,.60),(.50,.53),(.51,.45)])
map_poly([(.74,.69),(.80,.67),(.86,.71),(.85,.77),(.78,.79),(.73,.75)])
map_poly([(.82,.39),(.86,.35),(.89,.39),(.87,.45),(.84,.47)])
map_poly([(.86,.68),(.91,.65),(.95,.68),(.96,.77),(.91,.81),(.87,.78)])
# story markers; approximate global placements for lead & secondary stories
pts=[(.59,.25),(.54,.31),(.61,.25),(.51,.25),(.66,.27),(.70,.44),(.39,.32),(.64,.28),(.18,.25),(.80,.44),(.49,.25),(.69,.33),(.70,.52)]
for i,(a,b) in enumerate(pts,1):
    xx,yy=mx+a*mw,my+b*mh; ellipse((xx-5,yy-5,xx+5,yy+5),RED,WHITE,.6); text(xx,yy,str(i),5.2,WHITE,'bold','mm')
for j,(a,b) in enumerate([(.10,.53),(.20,.70),(.12,.82),(.37,.58),(.39,.73),(.45,.31),(.46,.61),(.48,.76),(.52,.27),(.57,.52),(.63,.59),(.71,.57),(.76,.63),(.79,.50),(.82,.27),(.86,.55),(.90,.28),(.33,.27),(.23,.28),(.57,.82),(.70,.21),(.30,.18),(.66,.75)]):
    xx,yy=mx+a*mw,my+b*mh; ellipse((xx-1.7,yy-1.7,xx+1.7,yy+1.7),'#c5c3bb')
legend='Red numbers mark stories 1–13; grey dots mark the briefs below. Positions are approximate.'
para(mx+7,my+mh-35,legend,mw-14,6.1,WHITE,7.1,'sans',4)

briefs=[
'GAZA — Israeli tanks cross the Yellow Line in a rare raid; Hamas calls it a truce breach.',
'CRIMEA — Bridge attacked again; traffic halted, Russian officials say.',
'LONDON — Van Gogh sells for a record $190.4m after a row over its Nazi history.',
'MEXICO CITY — Banxico minutes: board cut rates to 6.25% on a 3–2 vote.',
'CANBERRA — Australia sanctions West Bank settlers, three people and four groups.',
'MOGADISHU — Somalia accuses the UAE of secret military bases on its soil.',
'FRANKFURT — Deutsche Bank handled $582m in Epstein-linked deals, the FT reports.',
'WASHINGTON — Senators warn AI cyber threats are outpacing defenses.',
'OTTAWA — Carney: Canada rethinks China ties, seeking the right US deal.',
'NEW DELHI — Modi meets the Prince and Princess of Wales.',
'TOKYO — India and Japan review defence ties at their 2+2 dialogue.',
'BENGALURU — Amazon pledges $7bn for renewables in India by 2030.',
'SYDNEY — DuckDuckGo’s 133 puts England in charge of the third ODI.',
'AUCKLAND — New Zealand plays first as GTA VI unlocks at local midnight.',
'BAGHDAD — Six French ISIL members jailed for life in Iraq.',
'NAIROBI — Kenya floods kill six as Ruto gives his State of the Nation address.',
'CARACAS — Hegseth signs a US–Venezuela military deal.',
'WASHINGTON — Navarro: no “forever war” in the Gulf.',
'MANAMA — Bapco refinery back on its feet after the attacks.',
'RIYADH — Gulf leaders urge Trump not to strike Iran.',
'WASHINGTON — Liu Yunping becomes the first Asian-American House Democratic chair.',
'SACRAMENTO — California braces for an atmospheric river; flood advisories out.',
'LA PAZ — Bolivia declares an El Niño emergency; 78,000 families hit.'
]
bx=284; bw=712; colgap=9; colw=(bw-colgap*2)/3; by=my+3; bottom=my+mh-3
for i,s in enumerate(briefs):
    col=i//8; row=i%8; x=bx+col*(colw+colgap); y=by+row*39.35
    # number in compact burgundy square, exact numbering maintained
    text(x,y+1,str(i+14),6.2,RED,'bold')
    lines=para(x+18,y,s,colw-18,6.55,INK,7.65,'sans',5)
    line(x+18,min(y+lines+2,bottom),x+colw,min(y+lines+2,bottom),RULE,.35)

# date-check and publication footer
datecheck="DATE CHECK — FIRST REPORTED WEDNESDAY 18 NOV, SO NOT ON THIS PAGE AS NEWS: the Iranian drone interceptions · the EU's proposed €45bn loan for Ukraine · the House Democrats’ 251–11 vote nominating Hakeem Jeffries · Voyager 1 crossing one light-day, at 10:16 GMT Wednesday · Peltola’s Alaska win · Pew’s projection that Islam becomes the largest religion by 2035 · the first COP31 draft (Monday)."
rect((28,878,996,958),PANEL,RED,.8)
para(37,884,datecheck,950,8.6,INK,10.2,'sans',9)
line(28,965,996,965,INK,.7)
footer='Every story here happened, or was first reported, on Thursday 19 November 2026. Disputed claims are attributed, not stated as fact. Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, NASA, ICJ, Pew. Original drawings. The World in One Day — 19 November 2026.'
para(28,972,footer,968,7.1,INK,8.5,'sans',5)

im.resize((W,H),Image.Resampling.LANCZOS).save('assets/entry.png',format='PNG',optimize=True,compress_level=9)
