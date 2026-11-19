"""High-resolution editorial rebuild of the supplied 33-story front page."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random

ROOT=Path(__file__).resolve().parent
SRC=Image.open(ROOT/'assets'/'entry-source.webp').convert('RGB')
W,H,S=1024,1024,3
BG='#F5F0E3'; PAPER='#FBF8EF'; INK='#17191C'; NAVY='#17354C'; RED='#A72F43'; BLUE='#386D9D'; GREEN='#367658'; OCHRE='#C28A42'; MUTED='#6E716F'; RULE='#9E988C'; WHITE='#FFFEF8'
im=Image.new('RGB',(W*S,H*S),BG); d=ImageDraw.Draw(im)
serif='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
serifb='/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'
ital='/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf'
sans='/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf'
sansb='/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf'
def P(x): return round(x*S)
def F(size,kind='serif'):
    return ImageFont.truetype({'serif':serif,'bold':serifb,'italic':ital,'sans':sans,'sansb':sansb}[kind],P(size))
def text(x,y,s,size,color=INK,kind='serif',anchor=None):
    d.text((P(x),P(y)),s,font=F(size,kind),fill=color,anchor=anchor)
def line(x1,y1,x2,y2,color=RULE,width=.6):
    d.line((P(x1),P(y1),P(x2),P(y2)),fill=color,width=max(1,P(width)))
def rect(box,fill=None,outline=None,width=.6):
    d.rectangle(tuple(P(x) for x in box),fill=fill,outline=outline,width=max(1,P(width)))
def ellipse(box,fill=None,outline=None,width=.6):
    d.ellipse(tuple(P(x) for x in box),fill=fill,outline=outline,width=max(1,P(width)))
def poly(points,fill): d.polygon([(P(x),P(y)) for x,y in points],fill=fill)
def wrap(s,font,maxw):
    out=[]; cur=''
    for word in s.split():
        test=(cur+' '+word).strip()
        if d.textlength(test,font=font)>P(maxw) and cur: out.append(cur); cur=word
        else: cur=test
    if cur: out.append(cur)
    return out
def para(x,y,s,w,size,color=INK,leading=None,kind='serif',maxlines=99):
    font=F(size,kind); rows=wrap(s,font,w)[:maxlines]; step=leading or size*1.2
    for i,row in enumerate(rows): d.text((P(x),P(y+i*step)),row,font=font,fill=color)
    return len(rows)*step
def fit(s,w,size,kind='bold',minimum=7):
    while size>minimum and d.textlength(s,font=F(size,kind))>P(w): size-=.2
    return size

# Fine warm paper grain, kept subtle beneath all text and artwork.
random.seed(20261119)
for _ in range(10000):
    x=random.randrange(W*S); y=random.randrange(H*S)
    im.putpixel((x,y),(231,224,209) if random.random()<.36 else (250,247,239))
d=ImageDraw.Draw(im)
for _ in range(420):
    x=random.randrange(W*S); y=random.randrange(H*S); n=random.randrange(3,18)
    d.line((x,y,min(W*S-1,x+n),y),fill='#eee7d9',width=1)

def art(box,x,y,w,h,focus=(.5,.5)):
    crop=SRC.crop(box)
    out=crop.resize((P(w),P(h)),Image.Resampling.LANCZOS)
    im.paste(out,(P(x),P(y)))
    return ImageDraw.Draw(im)
def lead_climate(x,y,w,h):
    rect((x,y,x+w,y+h),'#176A68')
    ellipse((x+18,y+10,x+104,y+h-8),'#245B8C','#172D4A',1.2)
    poly([(x+42,y+23),(x+53,y+18),(x+66,y+25),(x+58,y+34),(x+46,y+33)],'#4B986C')
    poly([(x+69,y+47),(x+84,y+42),(x+91,y+54),(x+80,y+63),(x+70,y+58)],'#4B986C')
    ellipse((x+57,y+37,x+64,y+43),'#4B986C')
    # Temperature column and a clean, unlettered draft panel.
    rect((x+116,y+12,x+130,y+h-16),PAPER,'#24394C',1)
    rect((x+121,y+25,x+125,y+h-18),RED)
    ellipse((x+114,y+h-25,x+132,y+h-7),RED,'#24394C',1)
    rect((x+152,y+8,x+w-7,y+h-7),'#FBF8EF','#24394C',.8)
    for yy in (y+21,y+33,y+57,y+69): line(x+163,yy,x+w-18,yy,'#8E9693',.8)
    line(x+162,y+45,x+w-17,y+45,RED,2)
    line(x+164,y+49,x+w-20,y+41,NAVY,1.1)

def secondary_scene(x,y,w,h,kind):
    # A single crisp, caption-free editorial illustration for each compact card.
    if kind=='bridge':
        rect((x,y,x+w,y+h),'#E6C98D'); rect((x,y+h*.55,x+w,y+h),'#286084')
        line(x,y+h*.48,x+w,y+h*.48,NAVY,2)
        d.arc((P(x+18),P(y+h*.18),P(x+w*.7),P(y+h*1.05)),180,360,fill=NAVY,width=P(2))
        line(x+20,y+h*.48,x+20,y+h*.72,NAVY,1); line(x+w*.68,y+h*.48,x+w*.68,y+h*.72,NAVY,1)
        ellipse((x+w*.8,y+5,x+w*.8+12,y+17),RED,OCHRE,1)
        for dx,dy in ((-8,0),(8,0),(0,-8),(0,8)): line(x+w*.8+6,y+11,x+w*.8+6+dx,y+11+dy,OCHRE,1)
    elif kind=='war':
        rect((x,y,x+w,y+h),'#172A45')
        for j,(xx,ww,hh) in enumerate(((.04,.12,.45),(.2,.13,.68),(.38,.11,.5),(.55,.14,.78),(.77,.15,.58))):
            rect((x+w*xx,y+h*(1-hh),x+w*(xx+ww),y+h),'#334B68')
            for wy in range(int(y+h*(1-hh)+4),int(y+h-3),9): rect((x+w*xx+4,wy,x+w*xx+7,wy+3),OCHRE)
        d.line([(P(x+8),P(y+5)),(P(x+w*.36),P(y+h*.44)),(P(x+w*.8),P(y+h*.27))],fill='#E4B969',width=P(1.1))
        ellipse((x+w*.78,y+h*.18,x+w*.78+9,y+h*.18+9),RED,OCHRE,1)
    elif kind=='cyclone':
        rect((x,y,x+w,y+h),'#91C2D1'); rect((x,y+h*.63,x+w,y+h),'#337D91')
        for r in (10,17,24): d.arc((P(x+w*.49-r),P(y+h*.48-r),P(x+w*.49+r),P(y+h*.48+r)),20,325,fill=WHITE,width=P(1.5))
        ellipse((x+w*.49-2,y+h*.48-2,x+w*.49+2,y+h*.48+2),NAVY)
        line(x+10,y+h*.78,x+w-10,y+h*.78,'#B8D5D4',.6)
    elif kind=='justice':
        rect((x,y,x+w,y+h),'#E7D8B8')
        rect((x+12,y+7,x+40,y+h-5),NAVY); rect((x+22,y+7,x+30,y+h-5),WHITE)
        line(x+w*.62,y+8,x+w*.62,y+h-7,NAVY,1.5)
        line(x+w*.45,y+15,x+w*.79,y+15,OCHRE,1.5)
        line(x+w*.52,y+16,x+w*.45,y+27,NAVY,1); line(x+w*.74,y+16,x+w*.81,y+27,NAVY,1)
        line(x+w*.40,y+28,x+w*.5,y+28,OCHRE,2); line(x+w*.77,y+28,x+w*.87,y+28,OCHRE,2)
        poly([(x+w*.58,y+11),(x+w*.66,y+11),(x+w*.62,y+5)],RED)
    elif kind=='arctic':
        rect((x,y,x+w,y+h),'#A9D1DC')
        poly([(x,y+h*.76),(x+w*.2,y+h*.18),(x+w*.34,y+h*.7),(x+w*.52,y+h*.1),(x+w*.72,y+h*.73),(x+w*.86,y+h*.29),(x+w,y+h*.68),(x+w,y+h),(x,y+h)],'#EFF0E5')
        rect((x+12,y+7,x+36,y+19),'#224D83'); rect((x+23,y+7,x+27,y+19),WHITE); rect((x+12,y+12,x+36,y+15),WHITE)
        line(x+w*.75,y+h-2,x+w*.75,y+8,NAVY,.8); ellipse((x+w*.75-3,y+4,x+w*.75+3,y+10),OCHRE)
    elif kind=='markets':
        rect((x,y,x+w,y+h),'#123D3A')
        for j in range(1,4): line(x+5,y+j*h/4,x+w-5,y+j*h/4,'#32635B',.5)
        for i,bh in enumerate((8,13,10,18,16,24,21,31)):
            xx=x+10+i*20; rect((xx,y+h-bh-2,xx+8,y+h-2),'#D3A83D' if i>4 else '#427F73')
        pts=[(x+7,y+h-12),(x+34,y+h-17),(x+57,y+h-15),(x+80,y+h-25),(x+108,y+h-22),(x+132,y+h-34),(x+w-9,y+7)]
        d.line([(P(a),P(b)) for a,b in pts],fill=WHITE,width=P(1.5))
    elif kind=='games':
        rect((x,y,x+w,y+h),'#402253')
        ellipse((x+26,y+6,x+w-26,y+h-4),'#F6E7D4','#232338',1)
        rect((x+48,y+16,x+78,y+22),NAVY); rect((x+60,y+8,x+66,y+30),NAVY)
        for cx,cy,c in ((x+w*.68,y+13,OCHRE),(x+w*.76,y+22,RED),(x+w*.83,y+12,BLUE),(x+w*.73,y+31,GREEN)):
            ellipse((cx-3,cy-3,cx+3,cy+3),c)
        line(x+w*.48,y+4,x+w*.48,y+h-4,'#B68BCE',.7)
    elif kind=='labour':
        rect((x,y,x+w,y+h),'#E8D6AE')
        rect((x+5,y+7,x+w-5,y+22),'#D8C49B',NAVY,.7)
        for j,c in enumerate(('#A74B3E','#2B6987','#D29A3A','#4E7A59','#7B4C8E')):
            xx=x+16+j*31; ellipse((xx,y+19,xx+8,y+27),c); rect((xx+2,y+26,xx+6,y+h-3),c)
        line(x+8,y+h-4,x+w-8,y+h-4,NAVY,1)
    elif kind=='sport':
        rect((x,y,x+w,y+h),'#D9C99E'); rect((x,y+h*.72,x+w,y+h),'#4D5C4A')
        ellipse((x+w*.32,y+6,x+w*.32+10,y+16),NAVY)
        line(x+w*.34,y+16,x+w*.43,y+25,NAVY,2); line(x+w*.39,y+19,x+w*.28,y+26,NAVY,1.6)
        line(x+w*.42,y+25,x+w*.5,y+33,NAVY,1.6); line(x+w*.42,y+25,x+w*.34,y+33,NAVY,1.6)
        ellipse((x+w*.73,y+5,x+w*.73+24,y+29),None,RED,1.8); line(x+w*.73+3,y+26,x+w*.73+21,y+8,RED,1.8)
    else: # economy
        rect((x,y,x+w,y+h),'#1E354A')
        for i,hg in enumerate((13,19,17,28,25,35,32,23)):
            xx=x+8+i*20; rect((xx,y+h-hg,xx+10,y+h-2),'#D5AA45' if i<5 else '#567D8B')
        pts=[(x+5,y+12),(x+35,y+10),(x+65,y+14),(x+95,y+16),(x+125,y+22),(x+w-8,y+29)]
        d.line([(P(a),P(b)) for a,b in pts],fill='#C8554C',width=P(1.6))

# Masthead and headline
text(15,5,'THE WORLD IN ONE DAY',13,RED,'sansb')
text(1009,5,'33 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY',10,NAVY,'sansb','ra')
line(14,22,1010,22,NAVY,1.1)
text(14,23,'Thursday 19 November 2026',43,NAVY,'bold')
text(15,72,'Trump, Xi and Putin share one table · The World Court finds genocide in Myanmar · COP31’s draft drops fossil fuels',11.7,RED,'italic')
line(14,95,1010,95,INK,.8)

# Proportional regional bar, with the reference's category palette.
regions=[('ASIA',7,'#B64D14'),('MIDDLE EAST',3,RED),('EUROPE',7,'#2857A4'),('AFRICA',5,'#2D8058'),('AMERICAS',4,'#7642A0'),('OCEANIA',4,'#13798A'),('GLOBAL',3,'#526070')]
total=sum(v for _,v,_ in regions); x=14; avail=996
for label,n,color in regions:
    w=avail*n/total
    rect((x,101,x+w-1,122),color)
    fs=fit(f'{label} {n}',w-6,8.5,'sansb',6.3)
    text(x+w/2,111.5,f'{label} {n}',fs,WHITE,'sansb','mm')
    x+=w

# Six figures from the supplied image.
stats=[('3','presidents at one table'),('9–6','World Court genocide vote'),('$120bn','aid goal cut at COP31'),('$81bn','Anthropic’s record IPO'),('109–0','Danish vote on Arctic pact'),('4.9%','Australian jobless rate')]
sw=996/6
for i,(number,caption) in enumerate(stats):
    x=14+i*sw
    if i: line(x,128,x,169,'#B7B0A3',.55)
    text(x+7,125,number,21,RED,'bold')
    para(x+7,148,caption,sw-13,8.2,INK,9.1,'sansb',2)
line(14,174,1010,174,INK,.7)

# Three lead stories. The artwork is cropped from the supplied image; all copy is re-typeset.
leads=[
('1','SHENZHEN · SUMMIT','Trump, Xi and Putin hold first three-way summit','The US, Chinese and Russian leaders met for 90 minutes and issued a “Declaration on Peace” on nuclear risk and UN reform. — Reuters · AP · Xinhua',(14,204,406,283)),
('2','THE HAGUE · JUSTICE','World Court: Myanmar committed genocide','By 9 votes to 6 the ICJ found Myanmar guilty of genocide against the Rohingya and ordered reparations. — Al Jazeera · UN News',(414,220,708,310)),
('3','ANTALYA · CLIMATE','COP31 draft drops fossil fuels and $120bn aid goal','The slimmer text has no figure for adaptation aid. Talks are due to end on Friday. — Reuters · AFP',(715,178,1008,312))]
lead_x=14; lead_y=181; lead_gap=8; lead_w=(996-2*lead_gap)/3; lead_h=231
for i,(num,loc,headline,deck,box) in enumerate(leads):
    x=lead_x+i*(lead_w+lead_gap); y=lead_y
    rect((x,y,x+lead_w,y+lead_h),PAPER,'#8F877A',.7)
    rect((x,y,x+lead_w,y+15),RED)
    text(x+5,y+1,f'{num}  {loc}',7.7,WHITE,'sansb')
    if i==2: lead_climate(x+1,y+16,lead_w-2,97)
    else: art(box,x+1,y+16,lead_w-2,97,(.5,.48))
    para(x+7,y+117,headline,lead_w-14,15.8,INK,17.2,'bold',3)
    para(x+7,y+170,deck,lead_w-14,9.4,INK,10.7,'serif',5)

# Secondary stories 4–13 in a compact two-row, five-column grid.
secondary=[
('4','CRIMEA · WAR','Ukraine hits Crimea bridge again','Third strike in a week halts trains to Russia. — Euronews',(14,460,208,537)),
('5','RIYADH · WAR','Saudis shoot down Houthi missiles','Debris fell on the capital; no casualties reported. — Reuters',(214,460,414,537)),
('6','ODISHA · STORM','Cyclone Akvan nears India’s coast','Over 100,000 in shelters before Friday’s landfall. — IMD',(417,460,611,537)),
('7','SEOUL · JUSTICE','Korea’s top court clears ex-PM Han','Han Duck-soo’s martial law conviction is overturned. — AP',(615,460,817,537)),
('8','GREENLAND · SECURITY','Denmark backs Arctic pact with US','Parliament approves the Greenland security deal 109–0. — AP',(817,460,1008,537)),
('9','NEW YORK · MARKETS','Anthropic starts trading on Nasdaq','Its record $81bn share sale was priced at $83. — AP',(14,611,208,677)),
('10','WORLDWIDE · GAMES','GTA VI goes on sale after 13 years','The midnight launch draws rave reviews. — ABC',(214,611,414,677)),
('11','BOGOTÁ · LABOUR','Colombia’s unions hold national strike','Marches in three cities against an economic law. — Infobae',(417,611,611,677)),
('12','NAIROBI · SPORT','Marathon champion banned for doping','Kenya’s Peres Jepchirchir gets three years. — ABC',(613,611,817,677)),
('13','CANBERRA · ECONOMY','Australia’s jobless rate hits 4.9%','Highest since 2021; shares and the dollar slide. — ABC',(817,611,1008,677))]
sec_y=418; sec_gap=5; sec_w=(996-4*sec_gap)/5; sec_h=87
scene_kinds={4:'bridge',5:'war',6:'cyclone',7:'justice',8:'arctic',9:'markets',10:'games',11:'labour',12:'sport',13:'economy'}
for i,(num,loc,headline,deck,box) in enumerate(secondary):
    col=i%5; row=i//5; x=14+col*(sec_w+sec_gap); y=sec_y+row*(sec_h+4)
    rect((x,y,x+sec_w,y+sec_h),PAPER,'#928A7D',.55)
    rect((x,y,x+sec_w,y+12),RED)
    fs=fit(f'{num}  {loc}',sec_w-7,7.15,'sansb',5.8)
    text(x+4,y+1,f'{num}  {loc}',fs,WHITE,'sansb')
    secondary_scene(x+1,y+13,sec_w-2,34,scene_kinds[int(num)])
    para(x+5,y+49,headline,sec_w-10,9.4,INK,9.6,'bold',2)
    para(x+5,y+69,deck,sec_w-10,7.6,INK,8.1,'serif',3)

# Locate map panel reused from the supplied art, with its 1–13 markers and grey dots.
lower_y=603
rect((14,lower_y,304,lower_y+17),NAVY)
rect((312,lower_y,1010,lower_y+17),NAVY)
text(20,lower_y+1,'WHERE IT HAPPENED',10.8,WHITE,'sansb')
text(318,lower_y+1,'ALSO ON THURSDAY 19 NOVEMBER 2026',10.8,WHITE,'sansb')
text(856,lower_y+2,'place · what happened · source',7.8,'#E9E1D2','italic')
map_crop=SRC.crop((14,783,309,936)).resize((P(286),P(148)),Image.Resampling.LANCZOS)
im.paste(map_crop,(P(14),P(623)))
line(14,773,300,773,'#BDB5A7',.5)
text(17,775,'numbers match the stories',7.8,MUTED,'italic')

briefs=[
('14','Shenzhen','Xi urges ban on all nuclear arms.','Al Jazeera'),
('15','APEC','Albanese to Putin: “End your war, end it now.”','ABC'),
('16','Seoul','Half a million sit college entrance exam.','Sedaily'),
('17','Jakarta','Asset-seizure law passes after 18 years.','Kompas'),
('18','Hormuz','Iran says mines set 5 tankers ablaze.','Al Jazeera'),
('19','Gaza','Israel ends tank raid past truce line.','BBC'),
('20','Krasnodar','Kyiv says it hit two oil refineries.','Euronews'),
('21','Brussels','EU delays methane rules two years.','Euronews'),
('22','UK Inquiry:','yacht Bayesian was vulnerable to wind.','RNZ'),
('23','Zurich','Two rivals to challenge FIFA’s Infantino.','ABC'),
('24','Rome','Author Corrado Augias dies at 91.','Euronews'),
('25','Mogadishu','Somalia expels UAE ambassador.','Al Jazeera'),
('26','Sudan','Court sentences absent RSF chief to death.','AP'),
('27','Pretoria','Central bank holds rate at 7.25%.','SABC'),
('28','Canaries','Record 11,000 migrants in 15 days.','Africanews'),
('29','Florida','Floods shut Broward, Miami schools again.','CBS'),
('30','Wellington','Court: pay equity cuts broke rights law.','RNZ'),
('31','Tonga','Drought emergency takes effect.','RNZ'),
('32','Cook Islands','Cyclone Xavier weakens to category 4.','RNZ'),
('33','Space','Red giant seen eating a Sun-sized star.','Nature')]
brief_x=312; brief_w=698; col_gap=8; col_w=(brief_w-col_gap)/2; brief_y=622; row_h=23.3
def draw_brief(x,y,n,place,summary,source):
    color=('#B64D14','#A72F43','#2C8058','#2857A4')[(int(n)-14)//5%4]
    ellipse((x,y+1,x+12,y+13),color)
    text(x+6,y+7,str(n),8.0,WHITE,'sansb','mm')
    px=x+17; place_font=F(9.3,'bold'); body_font=F(9.2,'serif')
    text(px,y,place,9.3,INK,'bold')
    start=px+d.textlength(place,font=place_font)+3
    first_w=x+col_w-start-3
    remaining=(summary+' '+source).split(); rows=[]; current=''; width=first_w
    for word in remaining:
        test=(current+' '+word).strip()
        if d.textlength(test,font=body_font)>P(width) and current:
            rows.append(current); current=word; width=col_w-17
        else: current=test
    if current: rows.append(current)
    for j,row in enumerate(rows[:2]):
        d.text((P(start if j==0 else px),P(y+j*10.1)),row,font=body_font,fill=INK)
    line(x, y+21.7,x+col_w-3,y+21.7,'#D8D1C4',.35)
for i,(n,place,summary,source) in enumerate(briefs):
    col=0 if i<10 else 1; row=i%10
    draw_brief(brief_x+col*(col_w+col_gap),brief_y+row*row_h,n,place,summary,source)

# Full-width date check and publication note.
datecheck=("Every story on this page happened, or was first reported, on Thursday 19 November 2026. "
"LEFT OUT AS OTHER DAYS’ NEWS: 18 NOV: EU’s €45bn Ukraine loan plan · Iran fires on Kuwait and Bahrain · Nvidia results · Jeffries named for US speaker · Carney on China ties  "
"20 NOV: COP31’s scheduled close · Cyclone Akvan’s landfall")
rect((14,854,1010,954),PAPER,'#9E5F4E',.8)
text(23,864,'DATE CHECK ✓',11, '#397A5E','sansb')
para(111,863,datecheck,890,9.0,INK,10.3,'sans',5)
line(14,963,1010,963,INK,.7)
footer='Claims are attributed, not stated as fact · Pictures and map: original, drawn in code · Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature · 2026-11-19'
para(40,969,footer,944,8.0,INK,8.8,'serif',3)

im.resize((W,H),Image.Resampling.LANCZOS).save(ROOT/'assets'/'entry.png',format='PNG',optimize=True,compress_level=9)
