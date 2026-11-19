"""Deterministic Pillow artwork for THE WORLD — 24 HOURS IN FOCUS."""
from PIL import Image, ImageDraw, ImageFont
import math

S=2; W=H=1024
im=Image.new('RGB',(W*S,H*S),'#071722'); d=ImageDraw.Draw(im)
NAVY='#071722'; PANEL='#0d2431'; PANEL2='#102b39'; IVORY='#f4f0e4'; MUTED='#a8bac2'; DIM='#58717c'; CYAN='#59d6e5'; AMBER='#f2b84b'; CORAL='#ff7168'; TEAL='#2d7b78'; WHITE='#fffdf7'
sans='/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf'
serif='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
serifbold='/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'
def P(v): return int(v*S)
def font(size,bold=False,display=False):
    path=serifbold if (bold and display) else (serif if display else sans)
    return ImageFont.truetype(path,P(size))
def txt(x,y,t,size,color=IVORY,bold=False,display=False,anchor=None):
    d.text((P(x),P(y)),t,font=font(size,bold,display),fill=color,anchor=anchor)
def line(points,fill,width=1): d.line([(P(x),P(y)) for x,y in points],fill=fill,width=P(width))
def rr(box,r,fill,outline=None,width=1): d.rounded_rectangle(tuple(P(v) for v in box),radius=P(r),fill=fill,outline=outline,width=P(width))
def ellipse(box,fill=None,outline=None,width=1): d.ellipse(tuple(P(v) for v in box),fill=fill,outline=outline,width=P(width))
def polygon(points,fill): d.polygon([(P(x),P(y)) for x,y in points],fill=fill)
def wrap(text,fontobj,max_width):
    out=[]; cur=''
    for word in text.split():
        test=(cur+' '+word).strip()
        if d.textlength(test,font=fontobj)>P(max_width) and cur: out.append(cur); cur=word
        else: cur=test
    if cur: out.append(cur)
    return out
def paragraph(x,y,text,width,size,color,leading=15,maxlines=2,bold=False):
    ft=font(size,bold); lines=wrap(text,ft,width)[:maxlines]
    for i,l in enumerate(lines): d.text((P(x),P(y+i*leading)),l,font=ft,fill=color)
    return y+len(lines)*leading

# Fine atlas grain and frame
for y in range(8,1016,32): line([(24,y),(1000,y)],'#0a1d28',1)
line([(32,18),(992,18)],CYAN,2)
txt(34,29,'THE WORLD',40,IVORY,True,True)
txt(36,74,'24 HOURS IN FOCUS  /  GLOBAL DESK',12,CYAN,True)
txt(990,37,'THURSDAY',12,MUTED,True,anchor='ra')
txt(990,55,'19 NOVEMBER',20,IVORY,True,anchor='ra')
txt(990,80,'2026  ·  UTC DAY',11,AMBER,True,anchor='ra')
line([(32,104),(992,104)],'#29414c',1)
txt(35,116,'A summit without guarantees, a landmark court ruling and fresh pressure on fragile fronts.',17,IVORY,False,True)
txt(36,143,'5 REGIONS',10,CYAN,True); txt(122,143,'15 VERIFIED DEVELOPMENTS',10,MUTED,True)
for i,(lab,col) in enumerate([('EUROPE',AMBER),('MIDEAST',CORAL),('ASIA-PAC',CYAN),('OCEANIA',AMBER),('SOUTH ASIA',MUTED)]):
    x=709+i*55; ellipse((x,147,x+5,152),col); txt(x+8,142,lab,8,MUTED,True)

# Central globe, drawn as a clean atlas sphere with simplified continents.
cx,cy,r=512,337,171
ellipse((cx-r,cy-r,cx+r,cy+r),'#0c2a39','#316879',2)
for rw in (55,110,160):
    d.ellipse((P(cx-rw),P(cy-r),P(cx+rw),P(cy+r)),outline='#245263',width=P(1))
for hh in (52,105):
    d.arc((P(cx-r),P(cy-hh),P(cx+r),P(cy+hh)),0,360,fill='#245263',width=P(1))
line([(cx-r,cy),(cx+r,cy)],'#245263',1)
# recognizable continental silhouettes, stylized rather than cartographic detail
polygon([(374,265),(392,237),(425,218),(454,224),(469,241),(457,254),(471,269),(453,283),(437,280),(427,300),(406,303),(400,286),(383,286)],'#287775')
polygon([(438,307),(461,309),(478,327),(470,350),(481,371),(468,396),(459,431),(445,419),(440,390),(430,368),(432,341)],'#287775')
polygon([(498,244),(519,227),(545,229),(559,242),(579,239),(600,254),(596,269),(576,272),(562,288),(540,284),(528,300),(506,287),(489,269)],'#287775')
polygon([(530,296),(557,286),(581,300),(592,323),(581,340),(574,368),(559,391),(544,381),(540,352),(523,332)],'#287775')
polygon([(603,394),(622,388),(642,401),(637,416),(617,421),(604,411)],'#287775')
polygon([(628,309),(637,298),(646,304),(643,319),(634,323)],'#287775')
polygon([(663,380),(682,365),(697,370),(700,391),(685,405),(670,400)],'#287775')
# pins and distinct route arcs to lead-story callouts
pins=[(543,267,CYAN),(558,321,CORAL),(585,273,AMBER),(580,332,CORAL),(615,271,CYAN),(635,403,AMBER)]
for x,y,c in pins:
    ellipse((x-7,y-7,x+7,y+7),NAVY,c,2); ellipse((x-2,y-2,x+2,y+2),c)
line([(543,267),(377,231),(352,231)],CYAN,1); line([(558,321),(375,387),(351,387)],CORAL,1)
line([(585,273),(647,226),(672,226)],AMBER,1); line([(580,332),(650,373),(672,373)],CORAL,1)
line([(615,271),(665,266)],CYAN,1); line([(635,403),(660,431)],AMBER,1)
# globe framing labels
txt(52,205,'EUROPE / UKRAINE',9,CYAN,True); txt(52,220,'ICJ ruling · bridge attack',10,IVORY)
txt(52,365,'MIDDLE EAST',9,CORAL,True); txt(52,380,'Gaza · Riyadh',10,IVORY)
txt(684,205,'ASIA-PACIFIC',9,CYAN,True); txt(684,220,'Shenzhen · Seoul',10,IVORY)
txt(684,355,'SOUTH ASIA',9,CORAL,True); txt(684,370,'Cyclone Akvan',10,IVORY)
txt(684,419,'OCEANIA',9,AMBER,True); txt(684,434,'Wellington · Australia',10,IVORY)
txt(512,493,'A DAY OF POWER, LAW & WEATHER',10,MUTED,True,anchor='mm')

# Six lead stories with bespoke vector marks and careful source-status cues.
stories=[
 ('SHENZHEN · DIPLOMACY','THREE LEADERS MEET','Trump, Xi and Putin hold their first trilateral talks; no agreement announced.',CYAN,'summit'),
 ('THE HAGUE · JUSTICE','ICJ FINDS ROHINGYA GENOCIDE','Court finds Myanmar responsible for genocide in The Gambia case.',CORAL,'court'),
 ('SEOUL · ECONOMY','EXPORTS PASS $1 TRILLION','South Korea reaches the mark for the first time, powered by chip demand.',AMBER,'chip'),
 ('ODISHA · CYCLONE','47,000 EVACUATED','Authorities move residents before Akvan; landfall was forecast for Friday.',CORAL,'storm'),
 ('CENTRAL GAZA · CONFLICT','ISRAEL SAYS RAID ENDED','Military says its tank operation concluded; the account is attributed.',CORAL,'tank'),
 ('WELLINGTON · EQUALITY','COURT REJECTS PAY OVERHAUL','New Zealand High Court says the government’s changes violated women’s rights.',CYAN,'scale'),
]
def icon(x,y,kind,c):
    # icon base is an open dark medallion with restrained luminous strokes
    ellipse((x-21,y-21,x+21,y+21),'#153442','#315967',1)
    if kind=='summit':
        for j,col in enumerate((CYAN,AMBER,CORAL)):
            xx=x-10+j*10; ellipse((xx-4,y-12,xx+4,y-4),col); rr((xx-6,y-2,xx+6,y+12),4,col)
        line([(x-16,y+15),(x+16,y+15)],IVORY,2)
    elif kind=='court':
        polygon([(x-15,y-7),(x,y-16),(x+15,y-7)],c); line([(x-16,y-5),(x+16,y-5)],IVORY,2)
        for dx in (-10,0,10): line([(x+dx,y-3),(x+dx,y+11)],c,3)
        line([(x-17,y+13),(x+17,y+13)],IVORY,2)
    elif kind=='chip':
        rr((x-10,y-10,x+10,y+10),2,None,c,2)
        for q in (-6,0,6): line([(x-15,y+q),(x-10,y+q)],c,2); line([(x+10,y+q),(x+15,y+q)],c,2); line([(x+q,y-15),(x+q,y-10)],c,2); line([(x+q,y+10),(x+q,y+15)],c,2)
    elif kind=='storm':
        line([(x-14,y-7),(x-5,y-13),(x+3,y-9),(x+11,y-15)],c,3); line([(x-14,y+1),(x-4,y-4),(x+6,y),(x+15,y-5)],IVORY,2)
        line([(x-6,y+7),(x-10,y+14)],AMBER,2); line([(x+4,y+7),(x,y+14)],AMBER,2)
    elif kind=='tank':
        rr((x-13,y-7,x+11,y+5),2,c); line([(x-17,y+7),(x+14,y+7)],IVORY,3); ellipse((x-12,y+6,x-5,y+13),AMBER); ellipse((x+3,y+6,x+10,y+13),AMBER); line([(x+5,y-9),(x+17,y-13)],c,3)
    elif kind=='scale':
        line([(x,y-14),(x,y+13)],IVORY,2); line([(x-14,y-7),(x+14,y-7)],c,2); line([(x-10,y-7),(x-15,y+5),(x-4,y+5),(x-10,y-7)],c,2); line([(x+10,y-7),(x+5,y+5),(x+16,y+5),(x+10,y-7)],c,2); line([(x-9,y+14),(x+9,y+14)],IVORY,2)

for idx,(kicker,head,body,accent,kind) in enumerate(stories):
    col=idx%3; row=idx//3; x=32+col*322; y=510+row*113; w=306; h=103
    rr((x,y,x+w,y+h),10,PANEL,'#203d49',1); rr((x,y,x+4,y+h),2,accent)
    txt(x+14,y+10,kicker,9,accent,True); icon(x+w-31,y+44,kind,accent)
    sz=15
    while sz>11 and d.textlength(head,font=font(sz,True,True))>P(w-66): sz-=1
    d.text((P(x+14),P(y+30)),head,font=font(sz,True,True),fill=IVORY)
    paragraph(x+14,y+55,body,w-66,10,MUTED,13,3)

# Nine compact developments, each reported or taking place on November 19.
txt(34,741,'THE WIDER DISPATCH',11,CYAN,True)
line([(186,750),(990,750)],'#29414c',1)
briefs=[
 ('CRIMEA','Russian-installed governor says another attack halted traffic; damage check ongoing.',CORAL),
 ('RIYADH','Saudi-led coalition says missile debris damaged a Riyadh building.',CORAL),
 ('AUSTRALIA','October jobs fell; unemployment hit 4.9%, highest since 2021.',AMBER),
 ('SEOUL','Emergency alerts exposed 22 phones not surrendered at exam start, Yonhap reports.',CYAN),
 ('APEC · SHENZHEN','Leaders adopt a declaration on trade, connectivity and innovation.',AMBER),
 ('JAPAN · RUSSIA','Japan says Takaichi raised a detained national and business concerns with Putin.',CYAN),
 ('UK · CYBERSECURITY','FCA says October reports hit a five-year high; regulators propose new guidance.',CORAL),
 ('GLOBAL ECONOMY','IMF chief says energy shocks and AI demand add to inflation pressure.',CYAN),
 ('ANTALYA · COP31','Negotiations continued Nov. 19; the conference was due to close Friday.',AMBER),
]
for i,(loc,body,accent) in enumerate(briefs):
    col=i%3; row=i//3; x=34+col*322; y=763+row*54
    ellipse((x,y+3,x+6,y+9),accent); txt(x+13,y,loc,9,accent,True)
    paragraph(x+13,y+16,body,286,9,IVORY,11,2)

# Context strip uses verified facts attached to the reported developments.
line([(32,930),(992,930)],'#29414c',1)
facts=[('$1T','Korea exports'),('47K+','Odisha evacuated'),('4.9%','Australia jobless'),('10,000','Rohingya killed¹')]
for i,(num,label) in enumerate(facts):
    x=42+i*237
    if i: line([(x-14,941),(x-14,976)],'#29414c',1)
    txt(x,936,num,20,AMBER if i in (0,1) else CYAN,True,True)
    txt(x,961,label,9,MUTED,True)
txt(32,985,'¹ ICJ stated evidence showed ~10,000 killed in 2017 operations. 19 NOV 2026 · SOURCES: AP · REUTERS · YONHAP · IMD · UN',8,DIM,True)
txt(992,1001,'DEVELOPING: claims attributed; forecasts are not outcomes.',8,MUTED,False,anchor='ra')

im.resize((W,H),Image.Resampling.LANCZOS).save('assets/entry.png',format='PNG',optimize=True,compress_level=9)
