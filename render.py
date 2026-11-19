"""Build assets/entry.png from original vector-like shapes (Pillow is build-time only)."""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
im = Image.new('RGB', (W, H), '#f3efe5')
d = ImageDraw.Draw(im)
INK = '#142b36'; MUTED = '#526773'; PAPER = '#f3efe5'; CARD = '#fffdf7'
TEAL = '#3c9a91'; PALE = '#c5e0d8'; RED = '#e65b3f'; GOLD = '#e9b44c'; BLUE = '#356b8c'
fontpath = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
boldpath = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def f(size, bold=False): return ImageFont.truetype(boldpath if bold else fontpath, size)
def text(x,y,s,size=16,color=INK,bold=False): d.text((x,y),s,font=f(size,bold),fill=color)
def wrap(txt, font, maxw):
    words=txt.split(); lines=[]; line=''
    for word in words:
        t=(line+' '+word).strip()
        if d.textlength(t,font=font)>maxw and line: lines.append(line); line=word
        else: line=t
    if line: lines.append(line)
    return lines
def paragraph(x,y,txt,width,size=15,color=INK,leading=19,bold=False):
    ft=f(size,bold)
    for line in wrap(txt,ft,width):
        d.text((x,y),line,font=ft,fill=color); y+=leading
    return y

# Newspaper masthead and date.
d.rectangle((0,0,W,119),fill=INK)
d.rectangle((30,28,39,91),fill=RED)
text(58,26,'THE WORLD, TODAY',34,'#fffdf7',True)
text(60,73,'FIVE DATELINES · ONE DAY',14,'#a9c4c9',True)
d.text((W-35,39),'THURSDAY, 19 NOVEMBER 2026',font=f(19,True),fill='#fffdf7',anchor='ra')

# Central globe: hand-drawn world silhouette, graticule and location pins.
d.rounded_rectangle((32,139,992,477),radius=17,fill='#e2ece7')
# Globe outer field.
d.ellipse((348,152,676,480),fill='#d5e8e1',outline='#7ea99f',width=3)
# Curved latitude/longitude guides.
for box in [(374,199,650,432),(392,163,632,468),(431,154,593,475)]:
    d.ellipse(box,outline='#a6c8be',width=2)
d.arc((360,195,664,435),0,180,fill='#a6c8be',width=2)
d.arc((360,195,664,435),180,360,fill='#a6c8be',width=2)
d.line((350,316,675,316),fill='#a6c8be',width=2)
# Simplified continent silhouettes, positioned to remain recognizable at thumbnail size.
continents=[
 [(389,221),(415,194),(449,189),(464,205),(458,226),(475,238),(467,255),(444,258),(433,278),(415,274),(404,252),(386,245)],
 [(458,285),(477,293),(487,320),(480,340),(493,360),(484,391),(471,420),(457,402),(454,375),(442,352),(446,328)],
 [(505,207),(527,190),(554,194),(564,208),(586,204),(606,219),(597,233),(575,239),(560,255),(539,249),(526,263),(506,252),(491,231)],
 [(531,263),(560,256),(580,270),(589,292),(580,310),(573,335),(559,353),(541,342),(536,317),(522,299)],
 [(596,348),(620,341),(641,353),(636,369),(615,376),(600,365)],
 [(623,260),(633,252),(642,259),(639,271),(629,275)],
]
for p in continents: d.polygon(p,fill=TEAL)
# Highlight the story regions and connect with fine dashed editorial routes.
pins=[(429,241,RED),(546,278,GOLD),(573,294,BLUE),(610,356,RED),(528,235,GOLD)]
for x,y,c in pins:
    d.ellipse((x-8,y-8,x+8,y+8),fill=CARD,outline=c,width=4)
    d.ellipse((x-3,y-3,x+3,y+3),fill=c)
text(59,171,'A WORLD IN',22,INK,True); text(59,197,'FIVE MOVES',22,INK,True)
text(59,239,'SHENZHEN',13,BLUE,True)
paragraph(59,260,'Three powers meet at the APEC summit as Ukraine and Iran shadow the agenda.',190,15,INK,20)
d.line((255,276,401,243),fill=BLUE,width=2)
text(725,171,'SEOUL',13,BLUE,True)
paragraph(725,193,'South Korea’s exports cross $1 trillion for the first time, powered by chip demand.',215,15,INK,20)
d.line((720,250,588,286),fill=BLUE,width=2)
text(725,316,'THE HAGUE',13,RED,True)
paragraph(725,338,'The UN’s top court opens its Rohingya genocide judgment hearing.',215,15,INK,20)
d.line((720,371,449,325),fill=RED,width=2)

# Five restrained news cards with original miniature illustrations.
cards=[
 (32,500,338,720,'01','SHENZHEN · DIPLOMACY','THREE LEADERS\nAT ONE TABLE','Trump, Xi and Putin meet at APEC; nuclear arms and wars in Ukraine and Iran are on the agenda.',BLUE,'leaders'),
 (359,500,665,720,'02','THE HAGUE · JUSTICE','ROHINGYA CASE\nREACHES THE ICJ','The court opens its judgment hearing in The Gambia’s genocide case against Myanmar.',RED,'court'),
 (686,500,992,720,'03','SEOUL · ECONOMY','EXPORTS TOP\n$1 TRILLION','South Korea crosses the milestone for the first time, as semiconductor demand surges.',GOLD,'chips'),
 (32,739,501,977,'04','RIYADH · SECURITY','MISSILE DEBRIS\nDAMAGES TOWER','Saudi-led coalition says debris from a missile threat damaged a building in the capital.',RED,'missile'),
 (523,739,992,977,'05','WELLINGTON · EQUAL PAY','COURT UPHOLDS\nWOMEN’S RIGHTS','New Zealand’s High Court rules the pay-equity overhaul discriminated against women.',BLUE,'court'),
]
for x1,y1,x2,y2,num,kicker,head,body,accent,kind in cards:
    d.rounded_rectangle((x1,y1,x2,y2),radius=14,fill=CARD,outline='#d5d7ce',width=2)
    d.rectangle((x1+1,y1+1,x1+8,y2-1),fill=accent)
    text(x1+22,y1+16,num,13,accent,True)
    text(x1+56,y1+17,kicker,12,MUTED,True)
    # icon medallion
    cx=x2-48; cy=y1+53
    d.ellipse((cx-26,cy-26,cx+26,cy+26),fill='#edf2ed')
    if kind=='leaders':
        for i,col in enumerate((BLUE,RED,GOLD)):
            xx=cx-13+i*13
            d.ellipse((xx-5,cy-15,xx+5,cy-5),fill=col)
            d.rounded_rectangle((xx-7,cy-3,xx+7,cy+14),radius=5,fill=col)
        d.line((cx-18,cy+17,cx+18,cy+17),fill=INK,width=3)
    elif kind=='court':
        d.polygon([(cx-19,cy-7),(cx,cy-18),(cx+19,cy-7)],fill=RED)
        d.line((cx-20,cy-5,cx+20,cy-5),fill=INK,width=3)
        for xx in (cx-13,cx-4,cx+5,cx+14): d.line((xx,cy-3,xx,cy+13),fill=BLUE,width=3)
        d.line((cx-21,cy+15,cx+21,cy+15),fill=INK,width=3)
    elif kind=='chips':
        d.rounded_rectangle((cx-14,cy-14,cx+14,cy+14),radius=3,outline=GOLD,width=4)
        for off in (-9,0,9):
            d.line((cx-20,cy+off,cx-14,cy+off),fill=INK,width=2); d.line((cx+14,cy+off,cx+20,cy+off),fill=INK,width=2)
            d.line((cx+off,cy-20,cx+off,cy-14),fill=INK,width=2); d.line((cx+off,cy+14,cx+off,cy+20),fill=INK,width=2)
    elif kind=='missile':
        d.polygon([(cx-17,cy+12),(cx+9,cy-14),(cx+17,cy-11),(cx+14,cy-3),(cx-12,cy+19)],fill=RED)
        d.polygon([(cx-17,cy+12),(cx-22,cy+21),(cx-12,cy+19)],fill=GOLD)
        d.line((cx+4,cy+10,cx+21,cy+10),fill=INK,width=2)
    else:
        d.ellipse((cx-6,cy-6,cx+6,cy+6),fill=BLUE)
        for a in range(0,360,60):
            ex=cx+int(17*math.cos(math.radians(a))); ey=cy+int(17*math.sin(math.radians(a)))
            d.ellipse((ex-4,ey-4,ex+4,ey+4),fill=GOLD)
            d.line((cx,cy,ex,ey),fill=BLUE,width=2)
    headlines=head.split('\n')
    yy=y1+61
    for ln in headlines:
        text(x1+22,yy,ln,19,INK,True); yy+=23
    paragraph(x1+22,yy+4,body,(x2-x1)-44,14,MUTED,18)

d.line((32,990,992,990),fill='#c7c8bd',width=1)
text(34,994,'WORLD DESK  /  19 NOVEMBER 2026',10,MUTED,True)
text(990,994,'SOURCES: AP · YONHAP',10,MUTED,True)

im.save('assets/entry.png',format='PNG',optimize=True)
