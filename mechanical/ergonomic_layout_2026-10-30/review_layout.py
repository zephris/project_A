"""Plan-view comparison, a true-size hand-fit sheet, and coordinate/spacing audit."""
from pathlib import Path
import json,math,csv,html
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
cfg=json.loads((HERE/'layout.json').read_text())
CAP=cfg['cap_diameter_assumption_mm']
HOLE=cfg['cover_hole_diameter_mm']
OLD_CAP=24.0
OLD_HOLE=26.5
changes=json.loads((HERE/'checks/placement-changes.json').read_text())['changes']
old={f['ref']:f['old_xy'] for f in changes}
new={f['ref']:f['new_xy'] for f in changes}
fps={f['ref']:f for f in json.loads((HERE/'constraints.json').read_text())['footprints']}
sw=[f'SW{i}' for i in range(1,17)]
actions=sum(cfg['action_rows'],[])
def distance(a,b):return math.hypot(a[0]-b[0],a[1]-b[1])
def minimum(positions,refs):
    return min((distance(positions[a],positions[b]),a,b) for i,a in enumerate(refs) for b in refs[i+1:])
def net(ref):return next(p['net'] for p in fps[ref]['pads'] if p['number']=='1')
box=(42.25718,24.491558,292.65,191.050022)
palette={'old':'#aebdc8','new':'#167c9a','screen':'#c6dfd5','aux':'#e88737'}
with (HERE/'review/button-coordinates.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['Reference','Signal','Old_X_mm','Old_Y_mm','New_X_mm','New_Y_mm','Delta_X_mm','Delta_Y_mm'])
    for ref in sw:w.writerow([ref,net(ref),*old[ref],*new[ref],new[ref][0]-old[ref][0],new[ref][1]-old[ref][1]])
metrics={'minimum_all_button_centres_before_mm':minimum(old,sw),'minimum_all_button_centres_after_mm':minimum(new,sw),
         'minimum_action_centres_before_mm':minimum(old,actions),'minimum_action_centres_after_mm':minimum(new,actions),
         'minimum_cover_web_before_mm':minimum(old,sw)[0]-OLD_HOLE,'minimum_cover_web_after_mm':minimum(new,sw)[0]-HOLE,
         'main_action_horizontal_pitch_mm':32,'row_offset_mm':[-6,34],
         'palm_margin_to_caps_before_mm':box[1]+box[3]-max(old[x][1]+OLD_CAP/2 for x in sw),
         'palm_margin_to_caps_after_mm':box[1]+box[3]-max(new[x][1]+CAP/2 for x in sw),
         'screen_shift_toward_usb_mm':2,'option_shift_toward_usb_mm':3,'option_actuator_datum_correction_mm':.1,
         'keycap_diameter_before_mm':OLD_CAP,'keycap_diameter_assumed_mm':CAP,
         'cover_hole_diameter_mm':HOLE,'keycap_shape_and_hand_fit_not_yet_qualified':True}
(HERE/'checks/layout-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')

def svg_panel(pos,width=292.65,height=191.050022,offset=(0,0),previous=None,cap=CAP,hole=HOLE):
    xmin,ymin=box[:2];ox,oy=offset
    def xy(p):return p[0]-xmin+ox,p[1]-ymin+oy
    def rect(x,y,w,h,fill,r=0):
        x,y=xy((x,y));return f'<rect x="{x:.4f}" y="{y:.4f}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="#536a78" stroke-width=".25"/>'
    out=[rect(xmin,ymin,width,height,'#f5f7f9',10),rect(52.25718,34.491558,272.65,171.050022,'none',5)]
    sx,sy=pos['U5'];out+=[rect(sx-20.2,sy-19.25,40.4,38.5,palette['screen'],2)]
    out+=[rect(121,45,60,34,'#d1d8df',2),rect(185,34.14,14,13,'#a3adb7'),rect(153.46,34,9.94,9,'#a3adb7')]
    for i in range(1,7):
        cx,cy=pos[f'OPSW{i}'];x,y=xy((cx+2.25,cy-3.25))
        out.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#e2bc8c" stroke="#536a78" stroke-width=".25"/>')
    for ref in sw:
        x,y=xy(pos[ref]);color=palette['new'] if ref in actions else palette['aux']
        if previous:
            a,b=xy(previous[ref]);out.append(f'<circle cx="{a}" cy="{b}" r="12" fill="none" stroke="#99aab6" stroke-width=".35" stroke-dasharray="1 1"/>')
            out.append(f'<line x1="{a}" y1="{b}" x2="{x}" y2="{y}" stroke="#99aab6" stroke-width=".4"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{hole/2:g}" fill="none" stroke="{color}" stroke-width=".25" stroke-dasharray="1 1"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{cap/2:g}" fill="{color}" fill-opacity=".18" stroke="{color}" stroke-width=".45"/>')
        out.append(f'<text x="{x}" y="{y-.7}" font-size="3.2" text-anchor="middle" fill="#203849">{ref}</text>')
        out.append(f'<text x="{x}" y="{y+3}" font-size="2.5" text-anchor="middle" fill="#203849">{html.escape(net(ref))}</text>')
    out.append(f'<text x="{ox+8}" y="{oy+8}" font-size="3.6" fill="#203849">USB / screen edge</text>')
    out.append(f'<text x="{ox+85}" y="{oy+184}" font-size="3.5" fill="#203849">Palm space - {cap:g} mm keycaps</text>')
    out.append(f'<path d="M {ox+10} {oy+172} v 3 h 50 v -3" fill="none" stroke="#203849" stroke-width=".4"/>')
    out.append(f'<text x="{ox+35}" y="{oy+170}" font-size="3" text-anchor="middle">50 mm scale check</text>')
    return ''.join(out)
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="292.65mm" height="191.050022mm" viewBox="0 0 292.65 191.050022"><g font-family="Arial">{svg_panel(new)}</g></svg>'
(HERE/'review/hand-fit-template.svg').write_text(svg)
compare=f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="650" viewBox="0 0 620 252"><rect width="620" height="252" fill="white"/><g font-family="Arial"><text x="8" y="15" font-size="8" fill="#203849">BEFORE</text><text x="319" y="15" font-size="8" fill="#203849">HIGHER / WIDER CANDIDATE</text>{svg_panel(old,offset=(8,24),cap=OLD_CAP,hole=OLD_HOLE)}{svg_panel(new,offset=(319,24),previous=old)}<text x="8" y="235" font-size="5" fill="#203849">Blue: main actions. Orange: direction / auxiliary. Dotted grey: previous centres. Dotted coloured: cover holes.</text><text x="8" y="245" font-size="5" fill="#203849">32 mm action-column pitch; curved rows retained. Case height and USB ports unchanged. Trial hand fit before cutting.</text></g></svg>'
(HERE/'review/layout-comparison.svg').write_text(compare)
# Use the local SVG renderer bundled with CAD dependencies if available; fallback
# raster uses the same measured coordinates rather than a synthetic illustration.
im=Image.new('RGB',(1680,730),'white');d=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14);bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
for index,(pos,title) in enumerate(((old,'BEFORE'),(new,'HIGHER / WIDER CANDIDATE'))):
    cap,hole=(OLD_CAP,OLD_HOLE) if index==0 else (CAP,HOLE)
    scale=2.6;origin=(30+index*830,65)
    def pixel(x,y):return origin[0]+(x-box[0])*scale,origin[1]+(y-box[1])*scale
    d.text((origin[0],20),title,fill='#203849',font=bold)
    x,y=pixel(*box[:2]);d.rounded_rectangle((x,y,x+box[2]*scale,y+box[3]*scale),radius=20,fill='#f0f4f6',outline='#6b7c89',width=2)
    for xx,yy,w,h,c in ((pos['U5'][0]-20.2,pos['U5'][1]-19.25,40.4,38.5,'#c6dfd5'),(121,45,60,34,'#ccd5dd'),(185,34.14,14,13,'#8898a5'),(153.46,34,9.94,9,'#8898a5')):
        x,y=pixel(xx,yy);d.rectangle((x,y,x+w*scale,y+h*scale),fill=c)
    for n in range(1,7):
        cx,cy=pos[f'OPSW{n}'];x,y=pixel(cx+2.25,cy-3.25);r=4*scale;d.ellipse((x-r,y-r,x+r,y+r),fill='#e2bc8c')
    for ref in sw:
        x,y=pixel(*pos[ref]);r=cap/2*scale;c='#167c9a' if ref in actions else '#c37732'
        if index:
            a,b=pixel(*old[ref]);old_r=OLD_CAP/2*scale;d.ellipse((a-old_r,b-old_r,a+old_r,b+old_r),outline='#b9c5ce',width=1);d.line((a,b,x,y),fill='#b9c5ce')
        d.ellipse((x-r,y-r,x+r,y+r),fill='#d7e9ee' if ref in actions else '#f5e5d8',outline=c,width=2)
        d.text((x,y-7),ref,anchor='mm',font=font,fill='#203849');d.text((x,y+10),net(ref),anchor='mm',font=font,fill='#203849')
    d.text((origin[0]+220,590),f'{cap:g} mm keycaps / {hole:g} mm cover openings',fill='#203849',font=font)
d.text((30,650),'32 mm horizontal action pitch; curved rows retained. USB / screen edge is at the top.',font=bold,fill='#203849')
d.text((30,690),'The SVG hand-fit template is full size. Print at 100% and check the 50 mm scale bar. This is not cutting artwork.',font=font,fill='#536a78')
im.save(HERE/'review/layout-comparison.png')
print(json.dumps(metrics,indent=2))
