"""README illustrations: annotate reviewed CAD render; draw functional mount sections.

Run after rendering STEP/exploded.step to review/exploded.png at 1400 x 2000.
Callout anchors are reviewed image coordinates, not manufacturing dimensions.
"""
from pathlib import Path
import textwrap
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
OUT=HERE/'review'
INK='#233746';BLUE='#176D91';TEAL='#348979';GOLD='#D9BE75';GREY='#8C8A80'
def font(size,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',size)
def text(d,xy,s,size=30,bold=False,fill=INK):d.text(xy,s,font=font(size,bold),fill=fill)
def lines(d,xy,s,width=46,size=30):
    x,y=xy
    for row in textwrap.wrap(s,width=width):text(d,(x,y),row,size);y+=size+9
    return y
def box(d,xy,fill):d.rectangle(xy,fill=fill,outline=INK,width=3)
def arrow(d,a,b,color=BLUE):
    d.line([a,b],fill=color,width=5)
    x,y=b;d.polygon([(x,y),(x-11,y-18),(x+11,y-18)],fill=color)

def exploded_guide():
    raw=Image.open(OUT/'exploded.png').convert('RGB')
    assert raw.size==(1400,2000),'Render exploded.step at 1400 x 2000 before annotating'
    im=Image.new('RGB',(2400,2150),raw.getpixel((0,0)));d=ImageDraw.Draw(im)
    text(d,(80,60),'PHBox | Assembly map',64,True)
    text(d,(82,143),'Current 17 mm sandwich case - keycaps excluded',34)
    art=raw.resize((1200,1714));im.paste(art,(65,250))
    # Anchor fractions relative to the raw reviewed exploded render.
    anchors=[(.72,.25),(.61,.435),(.762,.416),(.50,.34),(.72,.581),(.755,.651),(.46,.754),(.62,.873),(.534,.944)]
    entries=[
      ('A','Top acrylic + option caps','2 mm acrylic. Captured caps and the M2 retainer are installed from below; check free return.'),
      ('B','Upper spacer + TPU collars','Printed perimeter and port surrounds. USB-A roof is acrylic; USB-C roof is printed.'),
      ('C','Upper foam capture pads','Six pads hold switch-plate tabs softly beneath the upper spacer. Tune preload by foam grade.'),
      ('D','Heatsink + OLED frame','Heatsink: insulating mounts at H5/H7/H12, separate MCU/flash pads. OLED: four corner posts and frame.'),
      ('E','Choc V2 retention plate','1.30 mm plate on three insulating mounts at H1/H2/H3. Fit switches and verify their latches.'),
      ('F','PCB and attached parts','This moving assembly floats on foam. H4/H6 are loose locating guides, not rigid case clamps.'),
      ('G','Lower support foam','Seven relieved pads from 2 mm stock. Keep foam off components, sockets and solder tails.'),
      ('H','Lower spacer / carrier','Supports the foam pads and closes the lower perimeter. Columns remain outside the PCB.'),
      ('I','Bottom acrylic','2 mm panel. Eight M3 columns join both covers: 12 mm spacer + 0.50 mm washer at each end.'),
    ]
    for i,((letter,title,body),(ax,ay)) in enumerate(zip(entries,anchors)):
        x=65+int(ax*1200);y=250+int(ay*1714)
        if letter in ('C','G','H'):
            tx,ty=x,y
            dx,dy={'C':(-40,35),'G':(-65,25),'H':(-60,20)}[letter]
            x+=dx;y+=dy
            d.line([(x,y),(tx,ty)],fill=BLUE,width=4)
            d.ellipse((tx-5,ty-5,tx+5,ty+5),fill=BLUE)
        d.ellipse((x-28,y-28,x+28,y+28),fill=BLUE,outline='white',width=4)
        d.text((x,y),letter,font=font(30,True),fill='white',anchor='mm')
        yy=235+i*190
        d.ellipse((1390,yy,1452,yy+62),fill=BLUE)
        d.text((1421,yy+31),letter,font=font(30,True),fill='white',anchor='mm')
        text(d,(1480,yy+2),title,35,True)
        lines(d,(1480,yy+55),body,width=49,size=29)
    d.line((80,1990,2320,1990),fill='#A6B8C4',width=3)
    text(d,(85,2020),'Build lower case -> fit PCB assembly -> prepare top cover -> close gently -> test',32,True)
    text(d,(85,2075),'Exploded spacing is for identification only. Use the README for actual installed heights and screw specifications.',27)
    im.save(OUT/'assembly-exploded-guide.png')

def mount_sections():
    im=Image.new('RGB',(2400,1220),'#F3F7FB');d=ImageDraw.Draw(im)
    text(d,(70,45),'Mounting details | Read with the exploded assembly map',52,True)
    text(d,(72,118),'Functional sections - not to scale; hardware and thermal-pad fit require a physical trial.',29)
    for x in (60,850,1640):d.rounded_rectangle((x,190,x+740,1130),radius=18,fill='white',outline='#B9CBD8',width=3)
    text(d,(85,217),'1  Fixed case column',37,True)
    box(d,(150,380,700,420),'#B4D8E4');box(d,(150,775,700,815),'#B4D8E4')
    box(d,(210,420,305,775),'#A2B7CF')
    box(d,(360,448,455,747),GOLD)
    box(d,(340,420,475,448),'#C4C9CC');box(d,(340,747,475,775),'#C4C9CC')
    d.line((408,390,408,488),fill=INK,width=9);d.line((408,710,408,805),fill=INK,width=9)
    d.polygon([(387,380),(429,380),(408,405)],fill='#C4C9CC',outline=INK)
    d.polygon([(387,815),(429,815),(408,790)],fill='#C4C9CC',outline=INK)
    text(d,(495,433),'End washer',26);text(d,(495,545),'12 mm M3',28,True);text(d,(495,582),'column',28)
    text(d,(175,320),'Top acrylic - M3 screw',28);text(d,(175,856),'Bottom acrylic - M3 screw',28)
    lines(d,(95,938),'Eight columns clamp covers and spacer walls. They do not pass through the PCB.',width=38,size=29)

    text(d,(875,217),'2  Insulated heatsink mount',37,True)
    box(d,(945,398,1515,448),'#9AABB5');box(d,(952,448,1078,502),'#9AABB5')
    box(d,(952,502,1078,522),'#7562A0');box(d,(960,522,1070,565),INK)
    box(d,(918,565,1540,594),TEAL)
    box(d,(1300,500,1430,565),'#D7C395');box(d,(1282,478,1448,500),'#7562A0')
    box(d,(1340,448,1390,478),'#D7C395')
    box(d,(1300,594,1430,613),'#7562A0');box(d,(1300,613,1430,678),'#D7C395')
    d.line((1365,370,1365,658),fill=INK,width=8)
    box(d,(1340,374,1390,398),INK)
    text(d,(955,340),'Aluminium',29,True);text(d,(1100,503),'Thermal pad',24)
    text(d,(965,692),'Chip',26);text(d,(1225,720),'Insulating stop',26)
    text(d,(985,797),'Polymer screw + rear retainer',27)
    lines(d,(885,938),'The hard stop sets height. Support washers insulate the plate; pads contact U1 and U3 separately.',width=38,size=29)

    text(d,(1665,217),'3  Captured option cap',37,True)
    box(d,(1730,447,1940,495),'#B4D8E4');box(d,(2010,447,2240,495),'#B4D8E4')
    box(d,(1947,383,2003,590),GOLD);box(d,(1905,505,2045,525),GOLD)
    box(d,(1800,555,1940,590),'#A2B7CF');box(d,(2010,555,2185,590),'#A2B7CF')
    box(d,(1966,590,1985,645),GOLD)
    box(d,(1908,670,2040,714),INK);box(d,(1730,714,2240,744),TEAL)
    box(d,(1960,645,1988,670),'#C4C9CC')
    d.arc((1937,672,2011,698),180,360,fill='#C4C9CC',width=4)
    arrow(d,(2200,356),(2200,426))
    text(d,(1740,319),'Press; switch dome returns cap',27)
    text(d,(1745,794),'Flange captured beneath acrylic',27)
    text(d,(1745,839),'Retainer guides; cap slides freely',27)
    lines(d,(1675,938),'No added coil spring. Check release and return across PCB movement; avoid constant switch preload.',width=38,size=29)
    im.save(OUT/'assembly-mounting-details.png')

if __name__=='__main__':exploded_guide();mount_sections()

