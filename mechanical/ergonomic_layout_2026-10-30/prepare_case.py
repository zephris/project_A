"""Derive this revision's editable factories from the previous case revision.

Copies only source, a small catalog screw and registration. No old print or STEP
outputs are copied. Read back candidate PCB geometry before calling this script.
"""
from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'sandwich_17mm_2026-10-08'
for folder in ('src','STEP','STL','DXF','reference','imported'):(HERE/folder).mkdir(exist_ok=True)
for src in (OLD/'src').glob('*.py'):shutil.copy2(src,HERE/'src'/src.name)
shutil.copy2(OLD/'imported/ISO10642_M3x6.step',HERE/'imported/ISO10642_M3x6.step')
def replace(path,old,new):
    text=path.read_text()
    assert old in text,(path,old)
    path.write_text(text.replace(old,new))
c=HERE/'src/common.py'
replace(c,"(HEAT/'constraints.json')","(HERE/'constraints.json')")
replace(c,'CAP_HOLE=26.5',"LAYOUT=json.loads((HERE/'layout.json').read_text())\nCAP_DIAMETER=LAYOUT['cap_diameter_assumption_mm']\nCAP_HOLE=LAYOUT['cover_hole_diameter_mm']")
replace(c,'OPTION_X=(217.73218,227.73218,237.73218,250.73218,260.73218,270.73218)\nOPTION_Y=-44.016558',
"# The tact body/actuator is offset from this footprint's pad-1 origin.\nOPTION_FPS={f['ref']:f for f in json.loads((HERE/'constraints.json').read_text())['footprints']}\nOPTION_X=tuple(OPTION_FPS[f'OPSW{i}']['pcb_xy'][0]+2.25 for i in range(1,7))\nOPTION_Y=-(OPTION_FPS['OPSW1']['pcb_xy'][1]-3.25)")
replace(c,"return [(244.23218,-50),(244.23218,-38)]","return [((OPTION_X[2]+OPTION_X[3])/2,OPTION_Y-5),((OPTION_X[2]+OPTION_X[3])/2,OPTION_Y+5)]")
replace(c,"(rect((xmin+xmax)/2,(ymin-80)/2,xmax-xmin,-80-ymin) & board_profile())+tab_profiles()",
"(rect((xmin+xmax)/2,(ymin-80)/2,xmax-xmin,-80-ymin) & board_profile())+tab_profiles()\n    # Closed, supported apertures extend into the former electronics strip.\n    # Their wings clear the screen frame and the existing heatsink.\n    p+=rect(*xy('SW1'),21,20.2,.3)\n    x,y=xy('SW16');p+=rect(x,y-3.0,20.8,27,1)")
replace(c,"p-=rect(100.3,-54,38.4,36.5,2)","p-=rect(*xy('U5'),38.4,36.5,2)")
replace(c,"for x in (217.73218,227.73218,237.73218,250.73218,260.73218,270.73218):\n        p-=rect(x,-44.016558,6.8,8.0,.3)","for x in OPTION_X:\n        p-=rect(x,OPTION_Y,6.8,8.0,.3)")
replace(c,"p-=rect(100.3,-54,30,25,1)","p-=rect(*xy('U5'),30,25,1)")
replace(c,"for x in (143,150,157,164,171,178):p-=rect(x,-65,3,18,1)","# Omit the former X=178 vent: it would merge with the moved SW16 opening.\n    for x in (143,150,157,164,171):p-=rect(x,-65,3,18,1)")
replace(c,"p=rect(100.3,-54,40.4,38.5,2)-rect(100.3,-54,35.9,34.0,0.2)","p=rect(*xy('U5'),40.4,38.5,2)-rect(*xy('U5'),35.9,34.0,0.2)")
replace(c,"p-=rect(100.3,-54,34.6,24.4,0.5)","p-=rect(*xy('U5'),34.6,24.4,0.5)")
replace(c,"p-=rect(100.3,-39.25,13,5)","sx,sy=xy('U5');p-=rect(sx,sy+14.75,13,5)")
replace(c,"s.label='printed_top_spacer_with_foam_capture_pockets';s.color=srgb('#A2B7CF')",
"# Local recesses keep the moved screen frame and retainer bosses clear;\n    # the exterior side wall and the USB seal structures remain closed.\n    s-=solid(rect(*xy('U5'),41.6,39.7,2),3.75,1.95,'screen_frame_float_relief','#999999')\n    for ox,oy in option_mounts():s-=cylinder(ox,oy,8.2,5.0,3.1)\n    s.label='printed_top_spacer_with_foam_capture_pockets';s.color=srgb('#A2B7CF')")
replace(HERE/'src/option_common.py','rect(244.23218,OPTION_Y,67,18,1)','rect((OPTION_X[0]+OPTION_X[-1])/2,OPTION_Y,67,12,1)')
replace(HERE/'src/assembly.py',"HEAT/'reference/board.step'","HERE/'reference/board.step'")
print('Prepared case revision source; prior case sources and print files unchanged.')
