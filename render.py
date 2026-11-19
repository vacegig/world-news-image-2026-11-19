"""Render the 33-story Image 1 edition with a thumbnail-legible type hierarchy."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "entry.png"
BASE = ROOT / "assets" / "entry-source.webp"
REF2 = ROOT / "assets" / "reference-2.webp"
REF3 = ROOT / "assets" / "reference-3.webp"
W = H = 1024
S = 2

FONT_SERIF = "/usr/share/fonts/opentype/urw-base35/P052-Roman.otf"
FONT_SERIF_B = "/usr/share/fonts/opentype/urw-base35/P052-Bold.otf"
FONT_SERIF_I = "/usr/share/fonts/opentype/urw-base35/P052-Italic.otf"
FONT_DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
FONT_DISPLAY_I = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Italic.ttf"
FONT_SANS = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf"
FONT_SANS_B = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf"

BG = "#F4F0E5"
PAPER = "#FFFDF7"
INK = "#171B20"
NAVY = "#17354F"
RED = "#A52C3D"
BLUE = "#386D9E"
GREEN = "#326B54"
OCHRE = "#C18A40"
MUTED = "#6B6A64"
RULE = "#8C887F"


def render():
    canvas = Image.new("RGB", (W*S, H*S), BG)
    d = ImageDraw.Draw(canvas)
    original = Image.open(BASE).convert("RGB")
    ref2 = Image.open(REF2).convert("RGB")
    ref3 = Image.open(REF3).convert("RGB")
    cache = {}

    def F(size, family="serif"):
        path = {"serif": FONT_SERIF, "serifb": FONT_SERIF_B, "serifi": FONT_SERIF_I,
                "display": FONT_DISPLAY, "displayi": FONT_DISPLAY_I,
                "sans": FONT_SANS, "sansb": FONT_SANS_B}[family]
        key = (path, int(round(size*S)))
        if key not in cache:
            cache[key] = ImageFont.truetype(path, key[1])
        return cache[key]

    def box(x1,y1,x2,y2,fill=None,outline=None,width=1):
        d.rectangle((round(x1*S),round(y1*S),round(x2*S),round(y2*S)),fill=fill,outline=outline,width=max(1,round(width*S)))

    def line(x1,y1,x2,y2,fill=RULE,width=1):
        d.line((round(x1*S),round(y1*S),round(x2*S),round(y2*S)),fill=fill,width=max(1,round(width*S)))

    def text(x,y,s,size,fill=INK,family="serif",anchor=None):
        d.text((round(x*S),round(y*S)),s,font=F(size,family),fill=fill,anchor=anchor)

    def width(s,size,family="serif"):
        return d.textlength(s,font=F(size,family))/S

    def wrap(s,size,maxw,family="serif"):
        rows=[]; cur=""
        for word in s.split():
            t=(cur+" "+word).strip()
            if width(t,size,family)>maxw and cur:
                rows.append(cur); cur=word
            else: cur=t
        if cur: rows.append(cur)
        return rows

    def para(x,y,s,maxw,size,fill=INK,family="serif",leading=None,maxlines=20,fit_min=None):
        fs=size
        rows=wrap(s,fs,maxw,family)
        if fit_min is not None:
            while len(rows)>maxlines and fs>fit_min:
                fs-=.2; rows=wrap(s,fs,maxw,family)
        rows=rows[:maxlines]
        step=leading or fs*1.2
        for i,row in enumerate(rows): text(x,y+i*step,row,fs,fill,family)
        return len(rows)*step, rows, fs

    def fitted(s,maxw,size,family="serifb",minimum=9):
        while size>minimum and width(s,size,family)>maxw: size-=.2
        return size

    def place_crop(source,crop,target,mode="cover"):
        image=source.crop(crop)
        x1,y1,x2,y2=target; tw=round((x2-x1)*S); th=round((y2-y1)*S)
        if mode=="cover":
            scale=max(tw/image.width,th/image.height)
            image=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
            left=(image.width-tw)//2; top=(image.height-th)//2
            image=image.crop((left,top,left+tw,top+th))
        else:
            image=image.resize((tw,th),Image.Resampling.LANCZOS)
        canvas.paste(image,(round(x1*S),round(y1*S)))

    # Quiet paper grain, matching Image 1's ivory identity.
    random.seed(20261119)
    for _ in range(8000):
        x=random.randrange(W*S); y=random.randrange(H*S)
        canvas.putpixel((x,y),(244,240,229) if random.random()<.65 else (248,245,237))
    d=ImageDraw.Draw(canvas)

    # Masthead and date, retaining Image 1's wording and structure.
    text(16,6,"THE WORLD IN ONE DAY",15.2,RED,"sansb")
    text(1008,6,"33 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY",13.2,NAVY,"sansb","ra")
    line(16,29,1008,29,INK,1.2)
    title="Thursday 19 November 2026"
    text(14,32,title,fitted(title,994,57,"display",49),NAVY,"display")
    subtitle="Trump, Xi and Putin share one table · The World Court finds genocide in Myanmar · COP31’s draft drops fossil fuels"
    para(17,96,subtitle,990,17.6,RED,"displayi",20,2,15)
    line(16,122,1008,122,INK,.8)

    # Geographical distribution.
    regions=[("ASIA",7,"#B65C18"),("MIDDLE EAST",3,RED),("EUROPE",7,BLUE),("AFRICA",5,GREEN),
             ("AMERICAS",4,"#6B4BA0"),("OCEANIA",4,"#1A7180"),("GLOBAL",3,"#58626C")]
    total=sum(n for _,n,_ in regions); x=16; barw=992
    for label,count,color in regions:
        ww=barw*count/total
        box(x,128,x+ww-1,153,color)
        labeltext=f"{label} {count}"
        fs=fitted(labeltext,ww-4,13.6,"sansb",10.5)
        text(x+ww/2,140.5,labeltext,fs,"#FFFFFF","sansb","mm")
        x+=ww

    # Six key figures; larger numerals and captions.
    stats=[("3","presidents at one table"),("9–6","World Court genocide vote"),
           ("$120bn","aid goal cut at COP31"),("$81bn","Anthropic’s record IPO"),
           ("109–0","Danish vote on Arctic pact"),("4.9%","Australian jobless rate")]
    sx=16; sw=992/6
    for i,(num,desc) in enumerate(stats):
        x=sx+i*sw
        if i: line(x,159,x,210,"#B4AEA2",.7)
        text(x+8,155,num,fitted(num,sw-16,29,"display",22),RED,"display")
        para(x+8,185,desc,sw-16,12.7,INK,"serifb",14.6,2,11.3)
    line(16,215,1008,215,INK,.9)

    # Feature cards: smaller art panes leave more room for readable copy.
    leads=[
      ("1","SHENZHEN · SUMMIT","Trump, Xi and Putin hold first three-way summit",
       "The US, Chinese and Russian leaders met for 90 minutes and issued a “Declaration on Peace” on nuclear risk and UN reform. — Reuters · AP · Xinhua",(16,202,405,289),original),
      ("2","THE HAGUE · JUSTICE","World Court: Myanmar committed genocide",
       "By 9 votes to 6 the ICJ found Myanmar guilty of genocide against the Rohingya and ordered reparations. — Al Jazeera · UN News",(415,220,707,307),original),
      ("3","ANTALYA · CLIMATE","COP31 draft drops fossil fuels and $120bn aid goal",
       "The slimmer text has no figure for adaptation aid. Talks are due to end on Friday. — Reuters · AFP",(216,429,410,470),ref3)]
    lx=16; ly=221; gap=8; lw=(992-2*gap)/3; lh=226
    for i,(num,loc,head,desc,crop,source) in enumerate(leads):
        x=lx+i*(lw+gap)
        box(x,ly,x+lw,ly+lh,PAPER,"#494B4C",.8)
        box(x,ly,x+lw,ly+17,RED)
        text(x+7,ly+1,f"{num} · {loc}",11.4,"#FFFFFF","sansb")
        place_crop(source,crop,(x+1,ly+18,x+lw-1,ly+92),"stretch")
        hs=fitted(head,lw-18,21.2,"display",17)
        para(x+9,ly+99,head,lw-18,hs,INK,"display",23,3,16.2)
        para(x+9,ly+168,desc,lw-18,13.5,INK,"serif",14.4,4,12.2)

    # Ten story cards. Their original topic-matched art remains; selected panels
    # use matching scenes from the supplied reference graphics.
    stories=[
      ("4","CRIMEA · WAR","Ukraine hits Crimea bridge again","Third strike in a week halts trains to Russia. — Euronews",(535,439,654,487),ref2),
      ("5","RIYADH · WAR","Saudis shoot down Houthi missiles","Debris fell on the capital; no casualties reported. — Reuters",(837,439,974,487),ref2),
      ("6","ODISHA · STORM","Cyclone Akvan nears India’s coast","Over 100,000 in shelters before Friday’s landfall. — IMD",(426,429,604,482),ref3),
      ("7","SEOUL · JUSTICE","Korea’s top court clears ex-PM Han","Han Duck-soo’s martial law conviction is overturned. — AP",(618,460,810,525),original),
      ("8","GREENLAND · SECURITY","Denmark backs Arctic pact with US","Parliament approves the Greenland security deal 109–0. — AP",(817,460,1010,525),original),
      ("9","NEW YORK · MARKETS","Anthropic starts trading on Nasdaq","Its record $81bn share sale was priced at $83. — AP",(14,611,207,678),original),
      ("10","WORLDWIDE · GAMES","GTA VI goes on sale after 13 years","The midnight launch draws rave reviews. — ABC",(214,611,408,678),original),
      ("11","BOGOTÁ · LABOUR","Colombia’s unions hold national strike","Marches in three cities against an economic law. — Infobae",(415,611,610,678),original),
      ("12","NAIROBI · SPORT","Marathon champion banned for doping","Kenya’s Peres Jepchirchir gets three years. — ABC",(617,611,810,678),original),
      ("13","CANBERRA · ECONOMY","Australia’s jobless rate hits 4.9%","Highest since 2021; shares and the dollar slide. — ABC",(818,611,1010,678),original),
    ]
    # Scene-only replacement/crops that contain no unrelated story words.
    art=[]
    crimea=ref2.crop((535,439,654,487))
    riyadh_box=(837,439,974,487)
    riyadh=ref2.crop(riyadh_box)
    riyadh_fill=ref2.getpixel((875,442))
    ImageDraw.Draw(riyadh).ellipse((857-riyadh_box[0]-11,450-riyadh_box[1]-11,
                                    857-riyadh_box[0]+11,450-riyadh_box[1]+11),fill=riyadh_fill)
    # Remove the source panel's 9 marker; keep the matching Riyadh skyline art.
    fill=ref2.getpixel((875,442))
    ImageDraw.Draw(riyadh).ellipse((857-837-11,450-439-11,857-837+11,450-439+11),fill=fill)
    akvan=ref3.crop((426,429,604,482))
    art=[crimea,riyadh,akvan]
    for i,(num,loc,head,desc,crop,source) in enumerate(stories):
        col=i%5; row=i//5; x=16+col*200; y=456+row*140; cw=192; ch=136
        box(x,y,x+cw,y+ch,PAPER,"#55534D",.7)
        if i<3: pane=art[i]
        elif source is original: pane=source.crop(crop)
        else: pane=source.crop(crop)
        # Story 10 gets the matching no-caption night-city/car detail from Image 2.
        if num=="10":
            pane=original.crop(crop)
        place_crop(pane,(0,0,pane.width,pane.height),(x+1,y+1,x+cw-1,y+36))
        # Add image 2's night car strip inside the GTA art window, without its labels.
        if num=="10":
            car=ref2.crop((420,254,710,298)).resize((round((cw-10)*S),round(20*S)),Image.Resampling.LANCZOS)
            canvas.paste(car,(round((x+5)*S),round((y+13)*S)))
        if num=="11":
            crowd=ref2.crop((690,628,814,655)).resize((round((cw-10)*S),round(15*S)),Image.Resampling.LANCZOS)
            canvas.paste(crowd,(round((x+5)*S),round((y+20)*S)))
        tag=f"{num} · {loc}"
        text(x+6,y+39,tag,fitted(tag,cw-12,11.2,"sansb",9.2),RED,"sansb")
        hs=fitted(head,cw-12,16.3,"display",13.4)
        _,rows,_=para(x+6,y+54,head,cw-12,hs,INK,"display",17.5,3,12.7)
        decky=y+54+len(rows)*17.5+1
        para(x+6,decky,desc,cw-12,12.5,INK,"serif",13.7,3,10.8)

    # Lower map and briefs. Four compact columns keep the 20 briefs visible,
    # with larger line spacing than Image 1's original lower block.
    lower_y=744
    text(16,lower_y,"WHERE IT HAPPENED",15.2,NAVY,"sansb")
    text(214,lower_y+1,"numbers match the stories",11.5,MUTED,"serifi")
    text(355,lower_y,"ALSO ON THURSDAY 19 NOVEMBER 2026",15.2,NAVY,"sansb")
    text(775,lower_y+1,"place · what happened · source",11.5,MUTED,"serifi")
    line(16,765,1008,765,INK,.8)
    mapcrop=original.crop((14,781,309,936)).resize((206*S,136*S),Image.Resampling.LANCZOS)
    canvas.paste(mapcrop,(16*S,772*S))
    box(16,772,222,908,None,"#77766F",.6)

    briefs=[
      ("14","Shenzhen","Xi urges ban on all nuclear arms.","Al Jazeera"),
      ("15","APEC","Albanese to Putin: “End your war, end it now.”","ABC"),
      ("16","Seoul","Half a million sit college entrance exam.","Sedaily"),
      ("17","Jakarta","Asset-seizure law passes after 18 years.","Kompas"),
      ("18","Hormuz","Iran says mines set 5 tankers ablaze.","Al Jazeera"),
      ("19","Gaza","Israel ends tank raid past truce line.","BBC"),
      ("20","Krasnodar","Kyiv says it hit two oil refineries.","Euronews"),
      ("21","Brussels","EU delays methane rules two years.","Euronews"),
      ("22","UK","Inquiry: yacht Bayesian was vulnerable to wind.","RNZ"),
      ("23","Zurich","Two rivals to challenge FIFA’s Infantino.","ABC"),
      ("24","Rome","Author Corrado Augias dies at 91.","Euronews"),
      ("25","Mogadishu","Somalia expels UAE ambassador.","Al Jazeera"),
      ("26","Sudan","Court sentences absent RSF chief to death.","AP"),
      ("27","Pretoria","Central bank holds rate at 7.25%.","SABC"),
      ("28","Canaries","Record 11,000 migrants in 15 days.","Africanews"),
      ("29","Florida","Floods shut Broward, Miami schools again.","CBS"),
      ("30","Wellington","Court: pay equity cuts broke rights law.","RNZ"),
      ("31","Tonga","Drought emergency takes effect.","RNZ"),
      ("32","Cook Islands","Cyclone Xavier weakens to category 4.","RNZ"),
      ("33","Space","Red giant seen eating a Sun-sized star.","Nature"),
    ]
    bx=234; bw=774; colgap=12; colw=(bw-colgap)/2; top=772; rows_per=10; rowh=15.2
    badge_colors=[OCHRE,RED]
    for i,(num,place,summary,source) in enumerate(briefs):
        col=i//rows_per; row=i%rows_per; x=bx+col*(colw+colgap); y=top+row*rowh
        color=badge_colors[col]
        d.ellipse((round(x*S),round((y+1)*S),round((x+14)*S),round((y+15)*S)),fill=color)
        text(x+7,y+8,num,8.6,"#FFFFFF","sansb","mm")
        fs=14.0
        rest=f"{summary} {source}"
        while width(place+" ",fs,"serifb")+width(rest,fs,"serif")>colw-23 and fs>11.4:
            fs-=.2
        assert width(place+" ",fs,"serifb")+width(rest,fs,"serif")<=colw-22, f"brief {num} exceeds its column"
        tx=x+19
        text(tx,y,place,fs,RED,"serifb")
        text(tx+width(place+" ",fs,"serifb"),y,rest,fs,INK,"serif")
        line(x+19,y+14.3,x+colw,y+14.3,"#D1CBBF",.35)

    # Date check and footer retain every phrase from Image 1.
    box(16,931,1008,1002,PAPER,RED,.9)
    text(24,935,"DATE CHECK ✓",13.5,GREEN,"sansb")
    datecheck="Every story on this page happened, or was first reported, on Thursday 19 November 2026. LEFT OUT AS OTHER DAYS’ NEWS: 18 NOV: EU’s €45bn Ukraine loan plan · Iran fires on Kuwait and Bahrain · Nvidia results · Jeffries named for US speaker · Carney on China ties 20 NOV: COP31’s scheduled close · Cyclone Akvan’s landfall"
    para(132,934,datecheck,866,12.8,INK,"serif",14.4,4,10.8)
    footer="Claims are attributed, not stated as fact · Pictures and map: original, drawn in code · Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature · 2026-11-19"
    para(18,1006,footer,990,10.8,INK,"serif",12.0,2,9.8)

    final=canvas.resize((W,H),Image.Resampling.LANCZOS)
    final.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save(
        OUT,format="PNG",optimize=True,compress_level=9
    )
    return OUT


if __name__=="__main__":
    print(render())
