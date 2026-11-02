"""Illustrated, file-linked mock assembly manual from the actual saved STL meshes.

Does not rebuild CAD, change geometry, slice, upload or contact a printer.
"""
from pathlib import Path
import json, math, re, struct, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/pdf'
ART=ROOT/'review/manual'
INK='#203849'; ORANGE='#E88737'; BLUE='#167C9A'; GREY='#D5DFE5'; MUTED='#586F7D'
WHITE='#FFFFFF'; PALE='#F0F5F7'
W,H=841.89,595.28
MANIFEST=json.loads((ROOT/'manifest.json').read_text())['files']
ENTRIES={Path(e['file']).stem:e for e in MANIFEST}
MESH={}


def keys(prefix):return sorted(k for k in ENTRIES if k.startswith(prefix))
GROUPS={
 'B01':('Bottom panel quarters',keys('bottom_acrylic_SURROGATE_QUARTER_')),
 'W01':('Lower case washers',[k for k in keys('acrylic_case_washer_') if '_bottom_' in k]),
 'C01':('12 mm case posts',keys('acrylic_case_post_')),
 'B02':('Lower spacer quarters',keys('bottom_spacer_QUARTER_')),
 'F01':('Lower height gauges',keys('pad_1_')),
 'P01':('PCB surrogate quarters',keys('PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_')),
 'M01':('Switch-plate front stops',keys('insulating_plate_stop_')),
 'M02':('Switch-plate rear caps',keys('insulating_plate_rear_')),
 'P02':('Switch-plate quarters',keys('switch_plate_QUARTER_')),
 'H01':('Heatsink front stops',keys('custom_POM_stop_')),
 'H02':('Heatsink support washers',keys('insulating_support_washer_')),
 'H03':('Heatsink rear washers',keys('rear_insulating_washer_')),
 'H04':('Heatsink rear retainers',keys('custom_POM_retainer_')),
 'T01':('MCU + flash height gauges',keys('pad_8_')+keys('pad_9_')),
 'H05':('Heatsink surrogate',['aluminium_heatsink_SURROGATE']),
 'S01':('Screen front posts',keys('printed_screen_stop_')),
 'S02':('Screen rear caps',keys('printed_screen_rear_')),
 'S03':('OLED PCB surrogate',['OLED_MODULE_PCB_SURROGATE']),
 'S04':('Screen retaining frame',['screen_frame']),
 'L01':('Top panel quarters',keys('top_acrylic_SURROGATE_QUARTER_')),
 'O01':('Option-button caps',keys('OPSW')),
 'O02':('Option-cap retainer',['option_retainer']),
 'O03':('Optional screw/nut gauges',keys('option_retainer_M2')),
 'L02':('Upper spacer quarters',keys('top_spacer_QUARTER_')),
 'U01':('USB-A collar gauge',['USB_A_collar']),
 'U02':('USB-C collar gauge',['USB_C_collar']),
 'F02':('Upper height gauges',[k for n in range(2,8) for k in keys(f'pad_{n}_')]),
 'W02':('Upper case washers',[k for k in keys('acrylic_case_washer_') if '_top_' in k]),
}
all_grouped=[k for _,ks in GROUPS.values() for k in ks]
assert len(all_grouped)==105 and len(set(all_grouped))==105


def mesh(key):
    if key not in MESH:
        e=ENTRIES[key];raw=(ROOT/e['file']).read_bytes();n=struct.unpack_from('<I',raw,80)[0]
        assert len(raw)==84+50*n
        dt=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')])
        faces=np.frombuffer(raw,dt,count=n,offset=84)['v'].astype(float)
        lo,hi=np.array(e['raw_bounds_mm'])
        if key.startswith('USB_'):
            # print_part() rotates the installed collar -90 deg about X,
            # then normalizes it. Restore its actual port-seat transform.
            kind=key[4];width=20.4 if kind=='A' else 18.4
            x=192.0 if kind=='A' else 158.43218
            floor=-1.1 if kind=='A' else -3.645
            p=faces.copy();faces[:,:,0]=p[:,:,0]+x-width/2
            faces[:,:,1]=-33.6-p[:,:,2];faces[:,:,2]=p[:,:,1]+floor-.2
        elif e['flip_X_180']:
            faces[:,:,0]+=lo[0];faces[:,:,1]=hi[1]-faces[:,:,1];faces[:,:,2]=hi[2]-faces[:,:,2]
        else:faces+=lo
        b=np.array([faces.reshape(-1,3).min(axis=0),faces.reshape(-1,3).max(axis=0)])
        if not key.startswith('USB_'):assert abs(b-np.array(e['raw_bounds_mm'])).max()<.051,key
        MESH[key]=faces
    return MESH[key]


def frame(view):
    eye=np.array([1.,1.,-1.35 if view=='under' else 1.35])
    if view=='top':eye=np.array([0.,0.,1.])
    eye/=np.linalg.norm(eye)
    right=np.array([1.,-1.,0.])/math.sqrt(2) if view!='top' else np.array([1.,0.,0.])
    up=np.cross(right,eye)
    if view=='under':up=-up;right=-right
    return right,up,eye


def render(path,old,new,view='iso',float_parts=True,focus=None,caption=None,reverse_arrows=False):
    width,height=(1450,880) if focus is None else (620,520)
    image=Image.new('RGB',(width,height),WHITE);draw=ImageDraw.Draw(image)
    right,up,eye=frame(view);old=list(dict.fromkeys(old));new=list(dict.fromkeys(new))
    old=[k for k in old if k not in new]
    chunks=[];arrow_world=[];labels=[]
    for key in old+new:
        faces=mesh(key).copy()
        active=key in new
        if active and float_parts:
            delta=np.array([0.,0.,-17. if view=='under' else 24.])
            if key.startswith('USB_'):delta=np.array([0.,12.,0.])
            original=faces.reshape(-1,3).mean(axis=0)
            faces+=delta
            arrow_world.append((original,original+delta) if reverse_arrows else (original+delta,original))
        if active and len(new)<=8:
            match=re.search(r'_QUARTER_([1-4])$',key) or re.search(r'_(H\d+)$',key)
            label=('Q'+match.group(1) if '_QUARTER_' in key else match.group(1)) if match else None
            if key.startswith('USB_'):label='USB '+key[4]
            if label:labels.append((faces.reshape(-1,3).mean(axis=0),label))
        chunks.append((key,faces,active))
    if not chunks:return
    if focus is None:
        points=np.concatenate([f.reshape(-1,3) for _,f,_ in chunks])
    else:
        centre=np.array(focus)
        points=np.array([centre+np.array([a,b,c]) for a in (-24,24) for b in (-24,24) for c in (-14,26)])
    px=points@right;py=points@up
    scale=min((width-70)/(px.max()-px.min()),(height-60)/(py.max()-py.min()))
    cx=(px.min()+px.max())/2;cy=(py.min()+py.max())/2
    def project(p):
        return np.column_stack(((p@right-cx)*scale+width/2,height/2-(p@up-cy)*scale))
    triangles=[];depths=[];colours=[]
    light=np.array([-.3,.25,1.]);light/=np.linalg.norm(light)
    for key,faces,active in chunks:
        normals=np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0])
        lengths=np.linalg.norm(normals,axis=1);normals/=np.maximum(lengths[:,None],1e-12)
        visible=normals@eye>1e-6
        faces=faces[visible];normals=normals[visible]
        projected=project(faces.reshape(-1,3)).reshape(-1,3,2)
        shade=np.clip(.66+.34*np.maximum(0,normals@light),.5,1)
        base=np.array([232,135,55]) if active else np.array([208,220,227])
        colors=(shade[:,None]*base).astype(int)
        triangles.extend(projected);depths.extend(faces.mean(axis=1)@eye);colours.extend(map(tuple,colors))
    for i in np.argsort(depths):
        draw.polygon([tuple(v) for v in triangles[i]],fill=colours[i])
    for a,b in arrow_world[::max(1,len(arrow_world)//4)]:
        pa,pb=project(np.array([a,b]));direction=pb-pa;length=np.linalg.norm(direction)
        if length<12:continue
        direction/=length;perp=np.array([-direction[1],direction[0]])
        draw.line([tuple(pa),tuple(pb)],fill=BLUE,width=5)
        draw.polygon([tuple(pb),tuple(pb-direction*19+perp*8),tuple(pb-direction*19-perp*8)],fill=BLUE)
    label_font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',24)
    for p,label in labels:
        x,y=project(np.array([p]))[0]
        if not (10<x<width-90 and 10<y<height-35):continue
        box=draw.textbbox((x+10,y-20),label,font=label_font)
        draw.rectangle((box[0]-3,box[1]-2,box[2]+3,box[3]+2),fill=WHITE)
        draw.text((x+10,y-20),label,font=label_font,fill=BLUE)
    if caption:
        ft=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
        draw.text((16,height-33),caption,font=ft,fill=INK)
    image.save(path)


def group_keys(codes):return [k for code in codes for k in GROUPS[code][1]]


# A step changes one named group or places one completed subassembly.
# Collars are checked on an empty surround, then removed: the rigid PCB's
# coarse USB blocks do not reproduce usable mating connectors.
STEPS=[
 ('A','Join the bottom panel',['B01'],'lower','iso','Keep the four cut faces together on a flat jig. Put the countersinks on the outside, facing down.','Q3 / Q4 face the USB edge; Q1 / Q2 face the opposite edge.'),
 ('A','Place the lower washers',['W01'],'lower','iso','Place one lower 0.5 mm washer at each of the eight case-column positions.','Count 8. Keep washers flat; do not put them under the PCB.'),
 ('A','Stand the case posts on the washers',['C01'],'lower','iso','Place the eight 12 mm posts on their lower washers. Hold them temporarily if needed.','Printed 2.5 mm bores are unthreaded. Do not drive M3 screws into them.'),
 ('A','Place the lower spacer quarters',['B02'],'lower','iso','Place Q1-Q4 around the case posts. Align the butt seams and the board-support ledges.','Keep seam tape away from washer seats, foam ledges and guides.'),
 ('A','Place the seven lower height gauges',['F01'],'lower','iso','Place the seven rigid lower gauges on their relieved support ledges.','For a floating-board test, use real foam instead. Do not stack foam on these gauges.'),
 ('B','Join the PCB surrogate quarters',['P01'],'board','iso','On a separate flat jig, join the four PCB quarters with the raised package boxes facing up.','The USB blocks identify the USB edge. This is not a working PCB.'),
 ('B','Fit the switch-plate front stops',['M01'],'board','iso','Place the three front stops at H1, H2 and H3. Seat their locating pilots in the board holes.','These are the three 3 mm switch-plate seats, not the case columns.'),
 ('B','Position the switch-plate rear caps',['M02'],'board','under','View from underneath: place a matching rear cap at H1, H2 and H3. Hold it temporarily.','No threads are modeled. Use tape or gentle external support; do not force a screw.'),
 ('B','Place the switch-plate quarters',['P02'],'board','iso','Align all four switch-plate quarters on the three front stops. Keep their cut edges together.','The nominal plate is 1.30 mm thick. Test real switches off the PCB surrogate.'),
 ('B','Position the heatsink front stops',['H01'],'board','iso','Place the heatsink stops at H5, H7 and H12. Match the smaller H12 stop to H12.','H5/H7 use the larger stop. Do not swap them with the switch-plate stops.'),
 ('B','Add the heatsink support washers',['H02'],'board','iso','Place each support washer on its matching recessed heatsink-stop seat.','Match H5, H7 and H12. Keep the thermal contact bosses clear.'),
 ('B','Position the heatsink rear washers',['H03'],'board','under','View from underneath: place the three relieved rear washers at H5, H7 and H12.','They are rear washers, not the front support washers.'),
 ('B','Position the heatsink rear retainers',['H04'],'board','under','Place each retainer behind its matching rear washer. Hold the stack temporarily.','Retainers are threadless proxies. Final heatsink screw lengths remain unresolved.'),
 ('B','Place the two thermal height gauges',['T01'],'board','iso','Place the larger gauge on the MCU envelope and the smaller gauge on the flash envelope.','Rigid gauges only: use either these or real thermal pads, never both.'),
 ('B','Lower the heatsink surrogate',['H05'],'board','iso','Turn the printed heatsink so its thermal bosses face down. Lower it onto the stops and gauges.','The notch faces BOOTSEL/RESET. Never power the board with this plastic heatsink.'),
 ('B','Fit the four screen front posts',['S01'],'board','iso','Place the four screen posts in their PCB mounting holes, with the 3 mm seating faces upward.','Use the four small screen posts. The switch-plate stops are larger.'),
 ('B','Position the four screen rear caps',['S02'],'board','under','View from underneath: place one screen rear cap at each of the four screen-post holes.','Temporarily hold the caps. They do not provide tested threaded retention.'),
 ('B','Place the OLED PCB surrogate',['S03'],'board','iso','Place the OLED board surrogate on its four screen posts and align all four corner holes.','This model omits the display glass, header and pin tails.'),
 ('B','Place the screen retaining frame',['S04'],'board','iso','Place the frame above the OLED board, aligning the four corner mounting positions.','The ears retain PCB corners. Do not use a real display glass surface as a clamping seat.'),
 ('C','Join the top panel quarters',['L01'],'top','iso','On a separate flat jig, join the top-panel quarters. Keep countersinks on the outside face.','Do not attach the top panel to the lower case yet.'),
 ('C','Insert the six option caps',['O01'],'top','under','From below the top panel, insert the six guided cap bodies upward through their openings.','The wide retaining flanges stay beneath the panel. Contact tips point toward the PCB.'),
 ('C','Place the option-cap retainer',['O02'],'top','under','Place the retainer beneath the cap flanges. Align its guides and the two mounting positions.','Check free guided sliding. The PCB surrogate has no switch springs or actuators.'),
 ('C','Check the optional fastener envelopes',['O03'],'top','under','If printed, position the two screw and two nut envelopes to inspect the retainer clearances.','These four items are visual gauges, not functional fasteners. Remove them if necessary.'),
 ('C','Position the upper spacer quarters',['L02'],'upper','iso','Place all four upper-spacer quarters on the empty lower case, aligning the seams and port surrounds.','Keep the PCB unit on its separate jig. The next two checks need the empty surrounds.'),
 ('C','Bench-check the USB-A collar',['U01'],'upper','iso','With the PCB absent, offer the USB-A collar gauge to the USB-A surround. Do not force it.','PLA checks shape only. Its rigid opening must not be forced over the coarse USB block.'),
 ('C','Bench-check the USB-C collar',['U02'],'upper','iso','With the PCB absent, offer the USB-C collar gauge to its smaller contoured surround.','Inspect the thin membrane and rear relief. Rigid PLA cannot test a soft seal.'),
 ('C','Set the rigid collars aside',[],'upper','iso','Remove both rigid collar gauges before fitting this spacer over the PCB surrogate.','The square USB proxy blocks cannot qualify collar or plug fit. Use real TPU and connectors later.'),
 ('C','Lift off the upper spacer',[],'lift_upper','iso','Lift the empty upper-spacer unit off the lower case and set it aside. Keep its quarter positions together.','Leave both rigid collars out. The lower case must be open for the PCB unit.'),
 ('D','Lower the completed PCB unit',[],'join_board','iso','Lower the completed PCB/switch-plate/heatsink/screen unit into the lower case.','Align the loose H4/H6 guides. Keep case posts outside the PCB; do not clamp through it.'),
 ('D','Place the six upper height gauges',['F02'],'final','iso','Place one upper gauge on each of the six switch-plate capture tabs.','For compliance tests, replace these with real upper foam. Do not stack the two.'),
 ('D','Lower the completed upper spacer',[],'join_upper','iso','Lower the prepared upper spacer over the case posts and internal unit. Leave the rigid collars aside.','Watch the port hoods and option area. No part should need to bend or be forced into place.'),
 ('D','Add the eight upper washers',['W02'],'final','iso','Place one upper 0.5 mm washer on each of the eight case posts.','Each case column has a lower washer, a 12 mm post and an upper washer.'),
 ('D','Lower the prepared top panel',[],'join_top','iso','Lower the top-panel/cap/retainer subassembly onto the upper washers and spacer.','Watch the cap tips and screen frame. Caps will not spring-return on the PCB surrogate.'),
 ('D','Hold the mock together lightly',[],'final','iso','Use light external clamps or temporary tape to keep the panels seated for inspection.','Hold at the outer case columns, not across the PCB. Printed fasteners are not functional.'),
 ('D','Check the assembled mock',[],'final','iso','Measure the closed height and inspect every seam, mounting seat, cap guide and port opening.','Nominal case: 292.6 x 191 x 17 mm, excluding keycaps. This is a geometry trial only.'),
]


def scene_steps():
    states={name:[] for name in ('lower','board','top','upper','final')}
    result=[]
    for index,(phase,title,codes,where,view,instruction,check) in enumerate(STEPS,1):
        new=group_keys(codes)
        if where=='join_board':
            old=states['lower'][:];new=states['board'][:];states['final']=old+new
        elif where=='join_upper':
            old=states['final'][:];new=[k for k in states['upper'] if not k.startswith('USB_')];states['final']+=new
        elif where=='join_top':
            old=states['final'][:];new=states['top'][:];states['final']+=new
        elif where=='lift_upper':
            old=states['lower'][:];new=states['upper'][:]
        else:
            if index==27:
                old=states['lower']+states['upper'];new=['USB_A_collar','USB_C_collar']
                states['upper']=[k for k in states['upper'] if not k.startswith('USB_')]
            else:
                old=states[where][:]
                if where=='upper':old=states['lower']+old
                states[where]+=new
        result.append(dict(number=index,phase=phase,title=title,codes=codes,old=old,new=new,view=view,
                           instruction=instruction,check=check,float_parts=index not in (1,6,20,34,35),
                           reverse_arrows=where=='lift_upper' or index==27))
    assert len(set(states['final']))==103  # Two rigid collars deliberately stay out.
    return result


def wrap(c,text,x,y,width,font='Regular',size=11,leading=15,color=INK):
    c.setFont(font,size);c.setFillColor(HexColor(color))
    words=text.split();line='';lines=[]
    for word in words:
        test=(line+' '+word).strip()
        if pdfmetrics.stringWidth(test,font,size)>width and line:lines.append(line);line=word
        else:line=test
    if line:lines.append(line)
    for line in lines:c.drawString(x,y,line);y-=leading
    return y


def footer(c,page):
    c.setStrokeColor(HexColor('#CAD8DF'));c.line(30,28,W-30,28)
    c.setFillColor(HexColor(MUTED));c.setFont('Regular',8)
    c.drawString(32,15,'PHBox mock kit | 26 October 2026 | UNPOWERED | Colours identify actions, not materials')
    c.drawRightString(W-32,15,str(page))


def header(c,label,title,subtitle=''):
    c.setFillColor(HexColor(BLUE));c.roundRect(30,H-77,55,50,8,fill=1,stroke=0)
    c.setFillColor(HexColor(WHITE));c.setFont('Bold',25);c.drawCentredString(57,H-61,label)
    y=H-48
    size=23
    while pdfmetrics.stringWidth(title,'Bold',size)>W-145:size-=.5
    c.setFont('Bold',size);c.setFillColor(HexColor(INK));c.drawString(102,y,title)
    if subtitle:c.setFont('Regular',10);c.setFillColor(HexColor(MUTED));c.drawString(103,y-21,subtitle)


def create():
    OUT.mkdir(parents=True,exist_ok=True);ART.mkdir(parents=True,exist_ok=True)
    pdfmetrics.registerFont(TTFont('Regular','C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Bold','C:/Windows/Fonts/arialbd.ttf'))
    pdfmetrics.registerFont(TTFont('Mono','C:/Windows/Fonts/consola.ttf'))
    steps=scene_steps()
    for s in steps:
        main=ART/f'step-{s["number"]:02d}.png'
        render(main,s['old'],s['new'],s['view'],s['float_parts'],reverse_arrows=s['reverse_arrows'])
        s['image']=main
        if s['new'] and not s['title'].startswith(('Join','Lower the completed','Lower the prepared')):
            focus=mesh(s['new'][0]).reshape(-1,3).mean(axis=0)
            detail=ART/f'step-{s["number"]:02d}-detail.png'
            render(detail,s['old'],s['new'],s['view'],s['float_parts'],focus=focus,reverse_arrows=s['reverse_arrows'])
            s['detail']=detail
    # Cover uses the assembled mock geometry, not the production metal/glass model.
    final=steps[-1]['old']
    render(ART/'assembled-mock.png',[],final,float_parts=False)
    dest=OUT/'PHBox_mock_assembly_manual.pdf'
    c=canvas.Canvas(str(dest),pagesize=(W,H))
    c.setTitle('PHBox - Printed Mock Assembly Manual')
    c.setAuthor('PHBox project')
    c.setSubject(f'{len(steps)} illustrated operations for the unpowered A1 fitment mock')
    page=1
    c.setFillColor(HexColor(BLUE));c.rect(0,H-150,W,150,fill=1,stroke=0)
    c.setFillColor(HexColor(WHITE));c.setFont('Bold',37);c.drawString(36,H-65,'PHBox')
    c.setFont('Regular',24);c.drawString(36,H-106,'Printed mock assembly manual')
    c.drawImage(str(ART/'assembled-mock.png'),40,100,500,315,preserveAspectRatio=True,anchor='c',mask='auto')
    wrap(c,f'{len(steps)} small steps',575,390,225,font='Bold',size=23,leading=27)
    wrap(c,'A1 / AMS Lite fitment kit\n292.6 x 191 x 17 mm case\nKeycaps excluded',575,345,225,size=12,leading=18)
    y=wrap(c,'UNPOWERED ONLY',575,244,225,font='Bold',size=16,color=ORANGE)
    wrap(c,'Plastic heatsink, rigid pad gauges, threadless posts and simplified PCB/display models are for geometry checks.',575,y-12,225,size=11,leading=16)
    c.setFillColor(HexColor(PALE));c.roundRect(32,48,W-64,44,7,fill=1,stroke=0)
    wrap(c,'Build the lower case. Prepare the PCB unit and cover separately. Then close gently and inspect.',45,74,W-95,font='Bold',size=13)
    footer(c,page);c.showPage();page+=1
    header(c,'!','Before you start','Read this page before fitting any parts')
    blocks=[('UNPACK AND SORT','After printing and cooling, separate supported layers from the top down. Support thin panels while peeling interfaces. Remove brims and sort the small pieces by the part key at the back.'),
            ('ORANGE = CURRENT OPERATION','Grey parts are already in that subassembly. Blue arrows show the movement direction. Insets enlarge the first fitting position.'),
            ('DO NOT USE PRINT-BED POSITIONS','The stacked print layout is not the assembly layout. This manual restores the source CAD positions and orientations.'),
            ('QUARTER MAP: USB EDGE UP','Top row: Q3 | Q4. Bottom row: Q1 | Q2. Join only matching part families. There are no added joining pins. Use a flat jig and thin temporary tape away from seats.'),
            ('NO WORKING THREADS','Printed case columns, rear caps, screws and nuts are shape proxies. Use temporary holding or external clamps. Do not force real screws into pilot bores.'),
            ('GAUGE OR REAL MATERIAL','Use rigid height gauges for a dry geometry stack, or actual foam/thermal pads for their respective trials. Never put real foam/pads on top of the corresponding rigid gauges.'),
            ('NO ELECTRICAL OR SPRING TEST','The PCB surrogate has no switch sockets, button actuators or usable USB receptacles. Test real switches off the surrogate; do not force their pins into it. Caps will not spring-return here.'),
            ('COLLARS STAY OUT OF THE FINAL RIGID MOCK','Bench-check PLA collars on the empty surround, then set them aside. Use real TPU and actual connector geometry later for compliance and plug tests.')]
    y=H-110
    for title,body in blocks:
        c.setFillColor(HexColor(ORANGE));c.circle(41,y-1,4,fill=1,stroke=0)
        y=wrap(c,title,55,y,W-100,font='Bold',size=11,leading=14)
        y=wrap(c,body,55,y-3,W-100,size=10.5,leading=14)-15
    footer(c,page);c.showPage();page+=1
    phases={'A':'LOWER CASE','B':'PCB SUBASSEMBLY - SEPARATE JIG','C':'TOP / UPPER-SPACER SUBASSEMBLIES','D':'BRING THE SUBASSEMBLIES TOGETHER'}
    for s in steps:
        c.bookmarkPage(f'step{s["number"]}');c.addOutlineEntry(f'{s["number"]:02d}  {s["title"]}',f'step{s["number"]}',0)
        header(c,f'{s["number"]:02d}',s['title'],phases[s['phase']] + (' | UNDERSIDE VIEW' if s['view']=='under' else ''))
        c.setFillColor(HexColor(PALE));c.roundRect(32,H-169,W-64,65,6,fill=1,stroke=0)
        c.setFillColor(HexColor(MUTED));c.setFont('Bold',9);c.drawString(45,H-122,'PARTS FOR THIS STEP')
        if s['codes']:
            codes='   +   '.join(f'{code}  x{len(GROUPS[code][1])}  {GROUPS[code][0]}' for code in s['codes'])
        else:
            codes={'join_board':'Completed PCB unit x1 + lower-case unit x1','join_upper':'Completed upper-spacer unit x1',
                   'join_top':'Prepared top-panel unit x1','lift_upper':'Empty upper-spacer unit x1; keep its four quarters together'}.get(STEPS[s['number']-1][3],
                        'Temporary external clamps / thin tape' if s['title'].startswith('Hold the mock') else
                        'Both rigid collar gauges' if s['number']==27 else 'Assembled mock + calipers / ruler')
        wrap(c,codes,45,H-144,W-95,font='Bold',size=12,leading=15)
        mainw=565 if 'detail' in s else W-64
        c.drawImage(str(s['image']),32,117,mainw,300,preserveAspectRatio=True,anchor='c',mask='auto')
        if 'detail' in s:
            c.setStrokeColor(HexColor('#CAD8DF'));c.roundRect(610,184,198,215,6,fill=0,stroke=1)
            c.drawImage(str(s['detail']),615,198,188,170,preserveAspectRatio=True,anchor='c',mask='auto')
            c.setFillColor(HexColor(BLUE));c.setFont('Bold',9);c.drawString(622,382,'ENLARGED FITTING POSITION')
            wrap(c,'Orange identifies the parts handled in this step.',621,194,175,size=8,leading=10)
        y=wrap(c,s['instruction'],37,103,W-74,font='Bold',size=12.5,leading=17)
        wrap(c,'CHECK: '+s['check'],37,y-7,W-74,size=10.5,leading=14,color=BLUE)
        footer(c,page);c.showPage();page+=1
    # File keys in the appendix map every printed item, with exact source names
    # and quantities in a companion Markdown guide.
    groups=list(GROUPS.items())
    for begin in (0,14):
        header(c,'KEY','Find your parts',f'Part codes {begin+1}-{min(begin+14,len(groups))} | all filenames are under MOCK_ONLY/STL/')
        y=H-110
        for code,(name,ks) in groups[begin:begin+14]:
            c.setFillColor(HexColor(BLUE));c.setFont('Bold',11);c.drawString(34,y,code)
            c.setFillColor(HexColor(INK));c.setFont('Bold',10);c.drawString(83,y,f'x{len(ks)}  {name}')
            if code=='W01':pattern='acrylic_case_washer_*_bottom_0p5_SURROGATE.stl'
            elif code=='W02':pattern='acrylic_case_washer_*_top_0p5_SURROGATE.stl'
            elif code=='F01':pattern='pad_1_1.stl through pad_1_7.stl'
            elif code=='F02':pattern='pad_2_1.stl through pad_7_1.stl'
            elif code=='T01':pattern='pad_8_1.stl + pad_9_1.stl'
            elif len(ks)==1:pattern=ks[0]+'.stl'
            else:
                import os
                pattern=os.path.commonprefix(ks)+'*.stl'
            wrap(c,pattern,83,y-14,W-118,font='Mono',size=8,leading=10,color=MUTED)
            y-=31
        footer(c,page);c.showPage();page+=1
    c.save()
    # Linked text instructions are useful on a phone and expose exact filenames.
    md=['# PHBox printed mock: illustrated assembly','',
        '[Open the illustrated PDF](output/pdf/PHBox_mock_assembly_manual.pdf).',
        '', 'Use the printed mock unpowered. Rigid collar gauges are removed before closing over the coarse USB blocks. Printed fastener models have no functional threads.','']
    for s in steps:
        md += [f'## {s["number"]:02d}. {s["title"]}', '',s['instruction'],'', '**Check:** '+s['check'],'',
               f'![Step {s["number"]:02d}](review/manual/step-{s["number"]:02d}.png)','']
        for code in s['codes']:
            name,ks=GROUPS[code]
            md += [f'**{code}: {name}, {len(ks)} pieces**','']
            md += [f'- [{key}.stl](STL/{key}.stl)' for key in ks]
            md += ['']
    md += ['## Source and limits','',
           'Illustrations use the saved mock-kit STL meshes and manifest source-coordinate bounds. Collars are restored from their documented print rotation. Orange means the current operation; grey means earlier parts, not a material specification.',
           '', 'The PCB surrogate omits copper, solder, sockets and most components; the OLED surrogate omits glass/header details. Foam movement, real pad preload, threaded retention, actual cable/dongle fit and heat transfer require their separate real-part trials. No CAD geometry or print file was changed.']
    (ROOT/'ASSEMBLY_STEPS.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    data={'steps':len(steps),'pdf_pages':page-1,'printed_items_mapped':len(all_grouped),'final_rigid_mock_parts':103,
          'collars_excluded_from_final_rigid_mock':True,'source_geometry_changed':False,
          'step_files':[{k:s[k] for k in ('number','title','codes','instruction','check')} for s in steps]}
    (OUT/'manual-checks.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps({'pdf':str(dest),'steps':len(steps),'pages':page-1,'items_mapped':len(all_grouped)},indent=2))


if __name__=='__main__':create()
