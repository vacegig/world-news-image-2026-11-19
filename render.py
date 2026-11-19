"""Deterministically render the 19-story World in One Picture front page."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ASSETS / "entry.png"
W = H = 1024
S = 2

FONT_SERIF = "/usr/share/fonts/opentype/urw-base35/P052-Roman.otf"
FONT_SERIF_B = "/usr/share/fonts/opentype/urw-base35/P052-Bold.otf"
FONT_SERIF_I = "/usr/share/fonts/opentype/urw-base35/P052-Italic.otf"
FONT_DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
FONT_SANS = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Regular.otf"
FONT_SANS_B = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf"

BG, PAPER, INK = "#F4F0E5", "#FFFDF7", "#171B20"
NAVY, RED, BLUE, GREEN = "#17354F", "#A52C3D", "#386D9E", "#326B54"
OCHRE, MUTED, RULE = "#C18A40", "#6B6A64", "#A8A298"


def render():
    canvas = Image.new("RGB", (W*S, H*S), BG)
    d = ImageDraw.Draw(canvas)
    cache = {}

    def F(size, family="serif"):
        path = {"serif": FONT_SERIF, "serifb": FONT_SERIF_B, "serifi": FONT_SERIF_I,
                "display": FONT_DISPLAY, "sans": FONT_SANS, "sansb": FONT_SANS_B}[family]
        key = (path, round(size*S))
        if key not in cache: cache[key] = ImageFont.truetype(path, key[1])
        return cache[key]

    def box(x1,y1,x2,y2,fill=None,outline=None,width=1):
        d.rectangle(tuple(round(v*S) for v in (x1,y1,x2,y2)), fill=fill, outline=outline,
                    width=max(1,round(width*S)))

    def line(x1,y1,x2,y2,fill=RULE,width=1):
        d.line(tuple(round(v*S) for v in (x1,y1,x2,y2)), fill=fill, width=max(1,round(width*S)))

    def text(x,y,s,size,fill=INK,family="serif",anchor=None):
        d.text((round(x*S),round(y*S)),s,font=F(size,family),fill=fill,anchor=anchor)

    def width(s,size,family="serif"):
        return d.textlength(s,font=F(size,family))/S

    def wrap(s,size,maxw,family="serif"):
        rows=[]; cur=""
        for word in s.split():
            nxt=(cur+" "+word).strip()
            if cur and width(nxt,size,family)>maxw: rows.append(cur); cur=word
            else: cur=nxt
        if cur: rows.append(cur)
        return rows

    def para(x,y,s,maxw,size,fill=INK,family="serif",leading=None,maxlines=20,minimum=None):
        fs=size; rows=wrap(s,fs,maxw,family)
        if minimum is not None:
            while len(rows)>maxlines and fs>minimum:
                fs-=.2; rows=wrap(s,fs,maxw,family)
        if len(rows)>maxlines:
            raise ValueError(f"Text overflow: {s!r} ({len(rows)} lines; max {maxlines})")
        step=leading or fs*1.2
        for i,row in enumerate(rows): text(x,y+i*step,row,fs,fill,family)
        return len(rows)*step,rows,fs

    def fit(s,maxw,size,family="serifb",minimum=9):
        while size>minimum and width(s,size,family)>maxw: size-=.2
        return size

    def image_panel(source, crop, rect, border=True, mode="cover"):
        x1,y1,x2,y2=rect; im=source.crop(crop)
        tw,th=round((x2-x1)*S),round((y2-y1)*S)
        if mode == "stretch":
            im=im.resize((tw,th),Image.Resampling.LANCZOS)
        else:
            scale=max(tw/im.width,th/im.height)
            im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
            left=(im.width-tw)//2; top=(im.height-th)//2
            im=im.crop((left,top,left+tw,top+th))
        canvas.paste(im,(round(x1*S),round(y1*S)))
        if border: box(x1,y1,x2,y2,None,"#77736B",.5)

    # All story artwork below is cropped from the three supplied WebP references.
    ref=Image.open(ASSETS/"reference-1.webp").convert("RGB")
    ref2=Image.open(ASSETS/"reference-2.webp").convert("RGB")
    ref3=Image.open(ASSETS/"reference-3.webp").convert("RGB")

    # Masthead and date.
    text(16,7,"THE WORLD IN ONE PICTURE",15.5,RED,"sansb")
    text(1008,7,"19 STORIES · EVERY ONE FROM THURSDAY 19 NOVEMBER",13.4,NAVY,"sansb","ra")
    line(16,29,1008,29,INK,1.35)
    title="Thursday 19 November 2026"
    text(14,32,title,fit(title,994,59,"display",52),INK,"display")
    subtitle="Three leaders meet in Shenzhen · GTA VI unlocks worldwide · A record IPO starts trading · The World Court rules on the Rohingya"
    para(17,103,subtitle,990,16.2,RED,"serifi",18.8,2,14.5)
    line(16,127,1008,127,INK,.85)

    # Six edition statistics, set in six equal columns.
    stats=[("$81.3bn","raised by Anthropic, the largest IPO on record"),
           ("13 years","since GTA V; its sequel goes on sale today"),
           ("551,864","sat South Korea’s college entrance exam"),
           ("50,000","moved to safety in Odisha before Cyclone Akvan"),
           ("$120bn","adaptation-finance goal still open at COP31"),
           ("700,000+","Rohingya who fled Myanmar in 2017")]
    sx=16; sw=992/6
    for i,(num,desc) in enumerate(stats):
        x=sx+i*sw
        if i: line(x,139,x,199,"#B8B1A5",.65)
        text(x+8,135,num,fit(num,sw-15,23.5,"display",19),RED,"display")
        para(x+8,164,desc,sw-16,12.2,INK,"serif",13.6,3)
    line(16,204,1008,204,INK,.9)

    # Three feature stories. High-resolution, story-matched artwork.
    lead_data=[
        ("1","SHENZHEN, CHINA · DIPLOMACY","Trump, Xi and Putin hold first three-way summit",
         "The US, Chinese and Russian leaders meet together for the first time, on APEC’s last day. Putin backs the draft Shenzhen Declaration.", ref, (14,208,338,325)),
        ("2","WORLDWIDE · GAMES","GTA VI finally goes on sale around the world",
         "Rockstar’s sequel unlocks at midnight local time. New Zealand first, on PS5 and Xbox Series X|S; no PC version yet.", ref, (349,208,674,325)),
        ("3","NEW YORK · MARKETS","Anthropic starts trading on Nasdaq as ANT",
         "Priced at $83, above its $70–78 range; $81.3bn raised, the largest IPO on record, valuing the Claude maker near $1.5tn.", ref2, (14,611,207,678)),
    ]
    margin=16; gap=10; cw=(992-2*gap)/3; y=212; ch=237; art_h=100
    for i,(num,loc,head,deck,im,crop) in enumerate(lead_data):
        x=margin+i*(cw+gap)
        box(x,y,x+cw,y+ch,PAPER,"#55514A",.75)
        image_panel(im,crop,(x+1,y+1,x+cw-1,y+art_h),mode="stretch")
        box(x+1,y+art_h,x+cw-1,y+art_h+19,RED)
        text(x+7,y+art_h+1,f"{num}  {loc}",11.3,"#FFFFFF","sansb")
        hs=16.2
        _,rows,_=para(x+9,y+art_h+25,head,cw-18,hs,INK,"serifb",18.1,3)
        deck_y=y+art_h+28+len(rows)*18.1
        para(x+9,deck_y,deck,cw-18,12.2,INK,"serif",13.3,4)

    # Eight secondary cards, four columns by two rows. Illustrations are selected
    # only from the same story subject in the supplied references.
    cards=[
      ("4","THE HAGUE · LAW","World Court rules on Rohingya genocide","Judgment: The Gambia v Myanmar is read at 10:00; it is final, with no appeal.",ref,(14,463,254,520)),
      ("5","ODISHA, INDIA · STORM","Cyclone Akvan nears India’s east coast","Red alert; 50,000 moved to safety in Odisha. Landfall is expected Friday between Narsapur and Puri.",ref,(265,463,505,520)),
      ("6","ANTALYA, TÜRKİYE · CLIMATE","COP31 enters its last 48 hours","Talks split over money, with a $120bn adaptation goal still in play before Friday’s close.",ref,(516,463,756,520)),
      ("7","SEOUL · EDUCATION","Half a million sit Korea’s Suneung","551,864 take the college exam; flights pause and a nationwide alert checks for hidden phones.",ref,(767,463,1009,520)),
      ("8","WASHINGTON · IRAN WAR","Trump weighs a new Iran offensive, reports say","He also claims, unconfirmed, that Tehran is “looking at” biological weapons; Iran denies seeking them.",ref,(14,651,254,711)),
      ("9","GAZA · WAR","Israeli armour pushes into central Gaza","Tanks and bulldozers move toward Salah al-Din Street; Hamas calls it a ceasefire breach.",ref,(265,651,505,711)),
      ("10","BOGOTÁ · LABOUR","Colombia’s unions strike nationwide","Workers and teachers march against President De la Espriella’s “Economic Rescue” tax bill.",ref3,(416,548,606,587)),
      ("11","CANBERRA · ECONOMY","Australia’s jobless rate rises","Economists warn of recession; the opposition calls it an “economic crisis”.",ref,(767,651,1009,711)),
    ]
    x0=16; y0=462; gapx=10; gapy=6; cardw=(992-3*gapx)/4; cardh=173; artH=45
    for i,(num,loc,head,deck,im,crop) in enumerate(cards):
        col=i%4; row=i//4; x=x0+col*(cardw+gapx); y=y0+row*(cardh+gapy)
        box(x,y,x+cardw,y+cardh,PAPER,"#5B574F",.7)
        image_panel(im,crop,(x+1,y+1,x+cardw-1,y+artH))
        text(x+7,y+artH+5,f"{num}  {loc}",10.7,RED,"sansb")
        hs=16.2
        _,rows,_=para(x+7,y+artH+19,head,cardw-14,hs,INK,"serifb",17.2,3)
        deck_y=y+artH+21+len(rows)*17.2
        para(x+7,deck_y,deck,cardw-14,12.2,INK,"serif",13.1,4)

    # Lower information zone: the locator map and two readable brief columns.
    section_y=819
    text(16,section_y,"WHERE IT HAPPENED",14.2,RED,"sansb")
    text(332,section_y,"ALSO ON THURSDAY 19 NOVEMBER",14.2,RED,"sansb")
    line(16,839,1008,839,INK,.8)
    # Use the reference's original locator map, separated from its tiny caption text.
    box(16,845,314,929,NAVY)
    map_crop=ref.crop((14,856,314,961))
    map_crop=map_crop.resize((200*S,70*S),Image.Resampling.LANCZOS)
    canvas.paste(map_crop,(108*S,846*S))
    text(23,864,"Red = stories 1–11",10.4,"#FFFDF7","sans")
    text(23,879,"Grey = briefs",10.4,"#FFFDF7","sans")

    briefs=[
      ("FLORIDA","Broward schools stay shut after 15 inches of rain."),
      ("MEXICO CITY","Banxico minutes explain its surprise cut."),
      ("LONDON","National Grid debunks a viral AI-made “blackout” post."),
      ("NEW DELHI","Schools reopen as GRAP-III smog curbs are lifted."),
      ("SHENZHEN","Putin backs APEC’s draft Shenzhen Declaration."),
      ("AUCKLAND","New Zealanders are first to play GTA VI, at midnight."),
      ("LONDON","A Taoist temple opens in Chinatown."),
      ("SYDNEY","Data centres may add 39m t of CO₂ a year by 2035."),
    ]
    bx=332; colgap=16; colw=(676-colgap)/2; top=842; brief_fs=12.2
    brief_columns=[briefs[:4],briefs[4:]]
    for col,items in enumerate(brief_columns):
        x=bx+col*(colw+colgap); yy=top
        for place,summary in items:
            prefix=place+" — "
            first_width=colw-width(prefix,brief_fs,"serifb")
            lines=[]; current=""; available=first_width
            for word in summary.split():
                candidate=(current+" "+word).strip()
                if current and width(candidate,brief_fs,"serif")>available:
                    lines.append(current); current=word; available=colw
                else:
                    current=candidate
            if current: lines.append(current)
            text(x,yy,place,brief_fs,RED,"serifb")
            text(x+width(prefix,brief_fs,"serifb"),yy,lines[0],brief_fs,INK,"serif")
            for line_no,content in enumerate(lines[1:],1):
                text(x+4,yy+line_no*13.2,content,brief_fs,INK,"serif")
            yy+=max(14.5,len(lines)*13.2)+1.2

    # Editorial fact check and sourcing footer.
    box(16,940,1008,993,"#FBF6F1",RED,.9)
    datecheck="DATE CHECK — left off on purpose because they broke before Thursday: Voyager 1 reaches one light-day from Earth (18 Nov) · Van Gogh’s record $190.4m sale in New York (18 Nov) · EU proposes a €45bn Ukraine loan (18 Nov) · Saudi all-clear after Houthi alerts (18 Nov) · William and Kate meet Modi (18 Nov) · US strikes on Iran’s Qeshm Island (17 Nov)"
    para(24,943,datecheck,974,12.2,INK,"serif",13.8,3)
    footer="Every story above happened, or was first reported, on Thursday 19 November 2026, in any time zone; claims are attributed, not stated as fact. Sources: AP, Reuters, CNBC, ICJ, IMD, UNFCCC, ABC (Australia), Korea JoongAng Daily, Al Jazeera. Original drawings."
    fs=fit(footer,990,10.5,"sans",9.2)
    text(17,999,footer,fs,INK,"sans")

    final=canvas.resize((W,H),Image.Resampling.LANCZOS)
    final.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save(
        OUT,format="PNG",optimize=True,compress_level=9)
    return OUT


if __name__=="__main__":
    print(render())
