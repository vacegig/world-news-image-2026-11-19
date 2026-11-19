"""Deterministic newspaper front page renderer."""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math, random

S=3; W=H=1024
BG='#F6F0E2'; INK='#171717'; NAVY='#173A56'; RED='#A72F43'; BLUE='#386D9D'; GREEN='#367658'; OCHRE='#C28A42'; GREY='#87877F'; PANEL='#FBF8EF'; RULE='#a9a49a'; WHITE='#fffefa'
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
for _ in range(9000):
    x=random.randrange(W*S); y=random.randrange(H*S)
    im.putpixel((x,y),(230,221,202) if random.random()<.35 else (250,246,236))
d=ImageDraw.Draw(im)
for _ in range(520):
    x=random.randrange(W*S); y=random.randrange(H*S); length=random.randrange(3,19)
    d.line((x,y,min(W*S-1,x+length),y),fill='#eee7d8',width=1)

# masthead
text(28,7,'THE WORLD IN ONE DAY',25,NAVY,'serifb')
line(506,9,506,37,NAVY,1)
text(996,13,"THURSDAY'S NEWS · ONE PAGE · 36 STORIES",12,RED,'serifb','ra')
line(22,44,1002,44,RED,1.3)
line(22,47,1002,47,NAVY,.6)
text(28,47,'Thursday 19 November 2026',43,INK,'serifb')
text(28,96,'Three leaders meet in Shenzhen · A court rules on Myanmar · The biggest IPO ever debuts',13,INK,'italic')
line(22,122,1002,122,INK,.9)

# distribution strip
regions=[('EUROPE',6,NAVY),('THE AMERICAS',11,RED),('ASIA-PACIFIC',6,BLUE),('MIDEAST',5,GREEN),('AFRICA',3,OCHRE),('OCEANIA',3,'#26798B'),('WORLD',2,GREY)]
total=sum(n for _,n,_ in regions); x=28; avail=968
for lab,n,col in regions:
    width=avail*n/total
    rect((x,130,x+width-1,158),col)
    sz=fit(lab,width-8,10.5,'serifb',8)
    # category and count sit on two centered lines, matching the reference page.
    text(x+width/2,137,lab,sz,WHITE,'serifb','mm')
    text(x+width/2,151,str(n),sz,WHITE,'serifb','mm'); x+=width

# six statistical blocks
stats=[('$81.3bn','raised by Anthropic — the largest IPO on record'),('15.9m','GTA VI pre-orders banked before release day'),('200,000','evacuated ahead of Cyclone Akvan'),('$120bn','a year of adaptation finance unresolved at COP31'),('730,000','Rohingya who fled in 2017 — the ICJ case'),('16bn miles','Voyager 1 from Earth — one light-day out')]
sw=968/6
for i,(num,desc) in enumerate(stats):
    sx=28+i*sw
    if i: line(sx,165,sx,218,RULE,.7)
    text(sx+8,163,num,23,RED,'serifb')
    para(sx+8,190,desc,sw-17,8.5,INK,9.3,'serifb',3)
line(22,222,1002,222,INK,.8)

# original vector illustrations in a consistent editorial style
def illustration(kind,x,y,w,h):
    rect((x,y,x+w,y+h),NAVY)
    if kind=='summit':
        # Dusk skyline, diplomatic flags and three anonymous seated silhouettes.
        rect((x,y,x+w,y+h),'#c9c2ad')
        rect((x,y+h*.62,x+w,y+h),NAVY)
        ellipse((x+w*.69,y+6,x+w*.85,y+22),OCHRE)
        skyline=[(x+2,12,22),(x+17,10,29),(x+30,14,19),(x+w-29,11,26),(x+w-15,13,18)]
        for xx,ww,hh in skyline:
            rect((xx,y+h*.62-hh,xx+ww,y+h*.62),'#52616a')
            for wy in range(int(y+h*.62-hh+4),int(y+h*.62-3),6):
                for wx in range(int(xx+3),int(xx+ww-2),5): rect((wx,wy,wx+1.4,wy+2),OCHRE)
        # three distinct flags, with recognizable national color arrangements
        fx=x+6; fy=y+5
        for j in range(3): line(fx+j*20,fy,fx+j*20,fy+15,'#354650',.7)
        # United States
        rect((fx+1,fy+2,fx+15,fy+10),WHITE)
        for k in (0,2,4,6): rect((fx+1,fy+2+k,fx+15,fy+3+k),RED)
        rect((fx+1,fy+2,fx+7,fy+6),BLUE)
        # China
        rect((fx+21,fy+2,fx+35,fy+10),RED); ellipse((fx+24,fy+4,fx+27,fy+7),OCHRE)
        # Russia
        rect((fx+41,fy+2,fx+55,fy+10),WHITE); rect((fx+41,fy+5,fx+55,fy+8),BLUE); rect((fx+41,fy+8,fx+55,fy+10),RED)
        # anonymous leaders behind a shared conference table
        for j,col in enumerate((BLUE,'#3b4d59',GREEN)):
            cx=x+w*.36+j*15
            ellipse((cx-3,y+27,cx+3,y+33),col)
            poly([(cx-6,y+34),(cx+6,y+34),(cx+8,y+h*.83),(cx-8,y+h*.83)],col)
        ellipse((x+w*.27,y+h*.73,x+w*.78,y+h*.92),OCHRE)
        line(x+5,y+h-5,x+w-5,y+h-5,'#e1d4b7',.65)
    elif kind=='games':
        # Sunset over a coastal city, palms and a quiet boulevard.
        rect((x,y,x+w,y+h),'#6d5050')
        rect((x,y+h*.43,x+w,y+h*.72),'#c68159')
        rect((x,y+h*.72,x+w,y+h),'#243d49')
        ellipse((x+w*.68,y+7,x+w*.88,y+27),'#e7bd78')
        # distant ridge and layered city blocks
        poly([(x,y+h*.66),(x+18,y+h*.49),(x+34,y+h*.62),(x+51,y+h*.45),(x+69,y+h*.61),(x+w,y+h*.50),(x+w,y+h*.75),(x,y+h*.75)],'#8c665b')
        for xx,ww,hh in [(x+3,15,19),(x+21,12,29),(x+37,18,22),(x+59,13,34),(x+75,17,23)]:
            rect((xx,y+h*.74-hh,xx+ww,y+h*.74),NAVY)
            for wy in range(int(y+h*.74-hh+4),int(y+h*.74-3),7):
                for wx in range(int(xx+3),int(xx+ww-2),5): rect((wx,wy,wx+1.5,wy+2),OCHRE)
        # palms frame the skyline
        for px in (x+17,x+w-13):
            line(px,y+h-7,px+2,y+20,'#172d39',1.3)
            for dx,dy in [(-13,-3),(-10,-10),(-4,-13),(5,-12),(11,-6),(13,0)]:
                line(px+2,y+21,px+dx,y+21+dy,'#172d39',1.3)
        line(x+5,y+h-5,x+w-5,y+h-5,'#c88f63',.8)
        line(x+25,y+h-9,x+w-18,y+h-9,'#52626a',.6)
    else:
        # Restrained market terminal: fine grid, plotted area and a rising price trace.
        rect((x,y,x+w,y+h),'#152e40')
        for j in range(1,5): line(x+5,y+j*h/5,x+w-5,y+j*h/5,'#355064',.55)
        for j in range(1,8): line(x+j*w/8,y+5,x+j*w/8,y+h-5,'#2c4658',.4)
        pts=[(x+7,y+h-12),(x+20,y+h-20),(x+32,y+h-17),(x+44,y+h-29),(x+57,y+h-24),(x+70,y+h-36),(x+84,y+h-33),(x+w-8,y+15)]
        poly(pts+[(x+w-8,y+h-6),(x+7,y+h-6)],'#24495a')
        d.line([(P(a),P(b)) for a,b in pts],fill=OCHRE,width=P(1.8))
        for j,(xx,yy) in enumerate(pts[1:-1]):
            ellipse((xx-1.8,yy-1.8,xx+1.8,yy+1.8),RED if j%2 else WHITE)
        # quiet trading bars in the lower band
        for j,bh in enumerate((5,9,7,13,10,16,14,21)):
            xx=x+9+j*10; rect((xx,y+h-5-bh,xx+4,y+h-5),BLUE if j<5 else OCHRE)
        text(x+w-6,y+4,'ANT',8.2,WHITE,'bold','ra')

leads=[
('1','SHENZHEN · SUMMIT','Trump, Xi and Putin hold first three-way summit','The three nuclear powers meet at APEC in Shenzhen; arms control and the Iran war top the agenda.','lead_shenzhen'),
('2','NEW YORK · GAMES','GTA VI arrives after a 13-year wait','Rockstar’s sequel unlocks at midnight in each country, New Zealand first; 15.9m pre-orders banked. $79.99 on PS5 and Xbox, no PC yet. Leave requests jumped.','lead_gta'),
('3','NASDAQ · MARKETS','Anthropic debuts in the biggest IPO on record','Priced at $83, above its range, the Claude maker raised $81.3bn and is valued near $1.5tn. Thursday’s first trades set the real price. Up to a fifth went to retail.','lead_ipo')]
cw=(968-16)/3
def photo(name,x,y,w,h):
    src=Image.open(f'assets/{name}.png').convert('RGB')
    crop=ImageOps.fit(src,(P(w),P(h)),method=Image.Resampling.LANCZOS,centering=(.5,.5))
    im.paste(crop,(P(x),P(y)))
    return ImageDraw.Draw(im)
for i,(num,loc,head,desc,asset) in enumerate(leads):
    x=28+i*(cw+8); y=229; h=188
    rect((x,y,x+cw,y+h),PANEL,'#887f73',.75)
    rect((x,y,x+cw,y+19),RED)
    text(x+8,y+2,f'{num}. {loc}',10.1,WHITE,'serifb')
    photo(asset,x+1,y+20,cw-2,88)
    para(x+7,y+112,head,cw-14,fit(head,cw-14,14.1,'serifb',12),INK,15.5,'serifb',3)
    para(x+7,y+150,desc,cw-14,8.3,INK,9.4,'serif',4)

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

sec_x=28; sec_y=426; gap=5; scw=(968-4*gap)/5; sh=76
photo_assets={4:'brief_hague',6:'brief_cyclone',7:'brief_kyiv',9:'brief_florida',10:'brief_earth'}
def wide_art(x,y,w,h,kind):
    rect((x,y,x+w,y+h),'#d8ddda')
    if kind=='climate':
        rect((x,y+h*.54,x+w,y+h),'#3e7484')
        ellipse((x+w*.77,y+3,x+w*.86,y+12),OCHRE)
        poly([(x,y+h*.7),(x+w*.2,y+h*.48),(x+w*.42,y+h*.68),(x+w*.65,y+h*.45),(x+w,y+h*.63),(x+w,y+h),(x,y+h)],'#4b7a61')
        ellipse((x+11,y+5,x+26,y+20),None,WHITE,1.1); ellipse((x+14,y+8,x+23,y+17),None,WHITE,.6)
    elif kind=='trade':
        rect((x,y+h*.55,x+w,y+h),'#b8b8a8')
        poly([(x+8,y+h*.59),(x+w/2,y+3),(x+w-8,y+h*.59)],NAVY)
        for xx in (x+w*.2,x+w*.38,x+w*.56,x+w*.74): rect((xx,y+h*.58,xx+5,y+h*.95),'#f5efe0')
        for j,col in enumerate((RED,BLUE,GREEN,OCHRE)):
            xx=x+18+j*16; line(xx,y+2,xx,y+h*.62,NAVY,.5); rect((xx,y+3,xx+8,y+8),col)
    elif kind=='france':
        rect((x,y,x+w/3,y+h),NAVY); rect((x+w/3,y,x+2*w/3,y+h),WHITE); rect((x+2*w/3,y,x+w,y+h),RED)
        for j in range(4):
            xx=x+12+j*34; line(xx,y+h,xx+1,y+4,'#d7cfbb',.7); ellipse((xx-2,y+2,xx+4,y+8),OCHRE)
    elif kind=='gulf':
        rect((x,y+h*.62,x+w,y+h),OCHRE)
        poly([(x,y+h*.65),(x+w*.26,y+h*.37),(x+w*.52,y+h*.6),(x+w*.77,y+h*.32),(x+w,y+h*.55),(x+w,y+h),(x,y+h)],'#c4a56d')
        rect((x+w*.67,y+8,x+w*.7,y+h*.69),NAVY); poly([(x+w*.62,y+11),(x+w*.685,y+2),(x+w*.75,y+11)],NAVY)
        ellipse((x+w*.12,y+4,x+w*.22,y+14),OCHRE)
    elif kind=='crime':
        rect((x,y+h*.68,x+w,y+h),'#73675a')
        for j in range(6):
            xx=x+17+j*25; ellipse((xx,y+8+(j%2)*3,xx+9,y+18+(j%2)*3),'#e8e1d0',RED,.5)
        line(x+8,y+h*.68,x+w-8,y+h*.68,RED,1)
for i,(num,loc,head,desc,kind) in enumerate(secondary):
    col=i%5; row=i//5; x=sec_x+col*(scw+gap); y=sec_y+row*(sh+4)
    rect((x,y,x+scw,y+sh),PANEL,'#938a7c',.6)
    rect((x,y,x+scw,y+14),RED)
    text(x+5,y+1,f'{num}. {loc}',7.1,WHITE,'serifb')
    asset=photo_assets.get(int(num))
    if asset: photo(asset,x+1,y+15,scw-2,22)
    else: wide_art(x+1,y+15,scw-2,22,kind)
    para(x+5,y+39,head,scw-10,fit(head,scw-10,8.7,'serifb',7.2),INK,8.8,'serifb',2)
    para(x+5,y+56,desc,scw-10,6.5,INK,7.1,'serif',3)

# lower atlas: recognizable hand-drawn world map and 23 sequential briefs
lower_y=589
rect((22,lower_y,310,lower_y+22),NAVY)
rect((326,lower_y,1002,lower_y+22),NAVY)
text(29,lower_y+3,'WHERE IT HAPPENED',12,WHITE,'serifb')
text(334,lower_y+3,'ALSO ON THURSDAY 19 NOVEMBER — 23 MORE STORIES',12,WHITE,'serifb')
mx,my,mw,mh=28,615,280,244
rect((mx,my,mx+mw,my+mh),'#f8f3e7','#aaa295',.6)
# Quiet graticule on a warm paper map panel.
for frac in (.25,.5,.75):
    yy=my+mh*frac; line(mx+5,yy,mx+mw-5,yy,'#d8d2c5',.45)
for frac in (.25,.5,.75):
    xx=mx+mw*frac; d.arc((P(xx-mw*.16),P(my+5),P(xx+mw*.16),P(my+mh-5)),270,90,fill='#d8d2c5',width=P(.45))
# simplified, recognizable continental silhouettes
def map_poly(coords): poly([(mx+a*mw,my+b*mh) for a,b in coords],'#477fa2')
map_poly([(.035,.20),(.06,.16),(.10,.17),(.12,.20),(.10,.23),(.07,.24)]) # Aleutian edge
map_poly([(.075,.22),(.09,.18),(.12,.15),(.16,.14),(.19,.15),(.22,.16),(.26,.17),(.29,.20),(.32,.22),(.34,.25),(.32,.28),(.35,.31),(.33,.34),(.30,.36),(.28,.40),(.26,.43),(.23,.41),(.22,.38),(.19,.37),(.17,.34),(.15,.32),(.13,.30),(.11,.27),(.09,.26)])
map_poly([(.34,.13),(.38,.12),(.40,.15),(.39,.20),(.37,.23),(.35,.20)]) # Greenland
map_poly([(.26,.40),(.29,.42),(.31,.44),(.33,.43),(.35,.46),(.37,.49),(.36,.52),(.34,.54),(.35,.58),(.33,.62),(.32,.67),(.30,.72),(.29,.78),(.27,.83),(.25,.79),(.24,.73),(.23,.68),(.22,.62),(.22,.57),(.23,.53),(.24,.49),(.25,.45)])
map_poly([(.405,.25),(.42,.21),(.45,.19),(.47,.20),(.49,.18),(.51,.16),(.54,.17),(.56,.19),(.59,.18),(.61,.20),(.65,.19),(.68,.21),(.72,.20),(.76,.22),(.79,.24),(.82,.27),(.83,.30),(.80,.32),(.77,.31),(.74,.33),(.71,.32),(.68,.34),(.64,.33),(.61,.35),(.58,.34),(.55,.36),(.52,.34),(.50,.32),(.47,.33),(.45,.31),(.43,.29),(.41,.28)])
map_poly([(.50,.37),(.53,.35),(.56,.36),(.59,.37),(.62,.38),(.65,.40),(.68,.43),(.69,.47),(.68,.50),(.66,.53),(.66,.57),(.64,.61),(.63,.65),(.60,.70),(.58,.72),(.56,.68),(.55,.64),(.53,.60),(.52,.56),(.50,.53),(.49,.49),(.48,.45),(.49,.41)])
map_poly([(.61,.36),(.64,.35),(.66,.37),(.68,.40),(.67,.43),(.65,.45),(.63,.42)]) # Arabian peninsula
map_poly([(.65,.38),(.67,.37),(.69,.39),(.70,.42),(.69,.45),(.68,.48),(.66,.47),(.65,.44)]) # India
map_poly([(.70,.43),(.73,.43),(.76,.45),(.78,.48),(.76,.50),(.74,.49),(.72,.47)]) # mainland southeast Asia
map_poly([(.79,.43),(.81,.41),(.83,.42),(.84,.45),(.82,.47),(.80,.46)]) # Japan
map_poly([(.75,.51),(.78,.50),(.81,.52),(.84,.53),(.87,.55),(.84,.57),(.80,.56),(.77,.54)]) # Indonesia
map_poly([(.74,.68),(.77,.66),(.81,.67),(.85,.70),(.87,.74),(.86,.78),(.83,.80),(.79,.79),(.76,.77),(.73,.74)])
map_poly([(.88,.64),(.90,.62),(.91,.65),(.90,.69),(.88,.68)]) # New Guinea
map_poly([(.70,.58),(.71,.56),(.72,.58),(.71,.61)]) # Madagascar
map_poly([(.68,.49),(.69,.48),(.70,.50),(.69,.52)]) # Sri Lanka
# story markers; approximate global placements for lead & secondary stories
pts=[(.60,.21),(.17,.26),(.20,.31),(.49,.23),(.62,.30),(.72,.44),(.57,.23),(.68,.26),(.17,.36),(.52,.52),(.45,.24),(.65,.41),(.56,.38)]
for i,(a,b) in enumerate(pts,1):
    xx,yy=mx+a*mw,my+b*mh; ellipse((xx-5,yy-5,xx+5,yy+5),RED,WHITE,.7); text(xx,yy,str(i),5.2,WHITE,'bold','mm')
for j,(a,b) in enumerate([(.10,.53),(.20,.70),(.12,.82),(.37,.58),(.39,.73),(.45,.31),(.46,.61),(.48,.76),(.52,.27),(.57,.52),(.63,.59),(.71,.57),(.76,.63),(.79,.50),(.82,.27),(.86,.55),(.90,.28),(.33,.27),(.23,.28),(.57,.82),(.70,.21),(.30,.18),(.66,.75)]):
    xx,yy=mx+a*mw,my+b*mh; ellipse((xx-1.7,yy-1.7,xx+1.7,yy+1.7),'#8b8a82')
legend='Red numbers mark stories 1–13; grey dots mark the briefs below. Positions are approximate.'
para(mx+3,my+mh+3,legend,mw-6,7.1,INK,8.0,'serif',2)

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
bx=326; bw=676; colgap=8; colw=(bw-colgap*2)/3; by=my+3; bottom=my+mh-3
for i,s in enumerate(briefs):
    col=i//8; row=i%8; x=bx+col*(colw+colgap); y=by+row*30.4
    text(x,y+1,str(i+14),7.2,RED,'serifb')
    lines=para(x+20,y,s,colw-20,8.8,INK,9.8,'serif',3)
    line(x+18,min(y+lines+2,bottom),x+colw,min(y+lines+2,bottom),RULE,.35)

# date-check and publication footer
datecheck="DATE CHECK — FIRST REPORTED WEDNESDAY 18 NOV, SO NOT ON THIS PAGE AS NEWS: the Iranian drone interceptions · the EU's proposed €45bn loan for Ukraine · the House Democrats’ 251–11 vote nominating Hakeem Jeffries · Voyager 1 crossing one light-day, at 10:16 GMT Wednesday · Peltola’s Alaska win · Pew’s projection that Islam becomes the largest religion by 2035 · the first COP31 draft (Monday)."
rect((22,885,1002,965),PANEL,RED,.8)
text(34,913,'DATE CHECK',13,RED,'serifb')
line(201,893,201,957,RED,.7)
para(216,891,datecheck.replace('DATE CHECK',''),770,9.0,INK,10.5,'serif',6)
line(22,972,1002,972,INK,.8)
footer='Every story here happened, or was first reported, on Thursday 19 November 2026. Disputed claims are attributed, not stated as fact. Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, NASA, ICJ, Pew. Original drawings. The World in One Day — 19 November 2026.'
for j,row in enumerate(wrap(footer,F(8.5,'italic'),900)):
    text(512,978+j*10,row,8.5,INK,'italic','mt')

im.resize((W,H),Image.Resampling.LANCZOS).save('assets/entry.png',format='PNG',optimize=True,compress_level=9)
