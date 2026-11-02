"""Nonmanufacturing dimension overlay for the saved assembled mounting layout.

Text and leader geometry are inspection aids, never included in physical parts.
Dimensions are measured from saved solids; PCB thickness is explicitly nominal.
"""
import json
from cadgen import step,read_scene,build123d as bd,srgb
from heatsink_common import PROJECT


def measurements():
    scene=read_scene(str(PROJECT/'STEP/heatsink_mounting.step'))
    def bounds(label):
        b=scene.resolve('#'+label).shape().bounding_box()
        return {'min':list(b.min),'max':list(b.max),'size':list(b.size)}
    top=bounds('REFERENCE_top_outer_bezel_3mm_Z8_to11')
    bottom=bounds('REFERENCE_bottom_outer_plate_3mm_Z_minus15_to_minus12')
    heat=bounds('Milled_aluminium_heatsink')
    registration=json.loads((PROJECT/'registration.json').read_text())
    pcb=registration['substrate']['bounds']
    constraints=json.loads((PROJECT/'constraints.json').read_text())
    return {'units':'mm','assembly_sha256':scene.document_hash,
            'enclosure_width':top['size'][0],'enclosure_depth':top['size'][1],
            'overall_height':top['max'][2]-bottom['min'][2],
            'top_plate_thickness':top['size'][2],
            'bottom_plate_thickness':bottom['size'][2],
            'cavity_height':top['min'][2]-bottom['max'][2],
            'pcb_width':pcb[1]-pcb[0],'pcb_depth':pcb[3]-pcb[2],
            'pcb_thickness_nominal':constraints['pcb_thickness_mm'],
            'heatsink_envelope':heat['size'],'heatsink_web_thickness':3.0,
            'heatsink_underside_z':4.0,'heatsink_top_z':heat['max'][2],
            'top':top,'bottom':bottom,
            'scope':'Provisional assembled envelope; excludes keycaps, screws/heads and final walls. Display guides are not machining geometry.'}


def guides(data):
    parts=[]
    def line(a,b):
        direction=bd.Vector(b)-bd.Vector(a)
        axis=bd.Plane(origin=a,z_dir=direction).location
        parts.append(axis*bd.Cylinder(0.12,direction.length,
                     align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN)))
    def text(words,x,y,z,size=4,rotation=0):
        # Lightly extruded faces make labels visible from both sides in STEP viewers.
        glyphs=bd.Text(words,font_size=size,font='Arial',rotation=rotation)
        parts.append(bd.Pos(x,y,z)*bd.extrude(glyphs,0.03))
    mn,mx=data['top']['min'],data['top']['max']
    x0,y0,z0=mn; x1,y1,z1=mx
    z=z1+1
    cx,cy=(x0+x1)/2,(y0+y1)/2
    # Overall width along X, outside the front edge.
    yd=y0-13
    for x in (x0,x1):
        line((x,y0,z),(x,yd-2,z))
        line((x-2,yd-2,z),(x+2,yd+2,z))
    line((x0,yd,z),(x1,yd,z))
    text(f"{data['enclosure_width']:.1f} mm overall",cx,yd-7,z,5)
    # Overall depth along Y, outside the left edge.
    xd=x0-13
    for y in (y0,y1):
        line((x0,y,z),(xd-2,y,z))
        line((xd-2,y-2,z),(xd+2,y+2,z))
    line((xd,y0,z),(xd,y1,z))
    text(f"{data['enclosure_depth']:.1f} mm overall",xd-7,cy,z,5,90)
    # A real vertical dimension is paired with an XY label and leader.
    xh,yh=x1+12,y0-6
    low,high=data['bottom']['min'][2],z1
    line((xh,yh,low),(xh,yh,high))
    for zz in (low,high):
        line((x1,y0,zz),(xh+2,yh,zz))
        line((xh-2,yh,zz-2),(xh+2,yh,zz+2))
    text(f"{data['overall_height']:.1f} mm overall height",x1+52,y0+8,z,4)
    line((xh,yh,high),(x1+18,y0+8,z))
    # Legend sits beyond the back edge, without obscuring the PCB.
    notes=[
        'PROVISIONAL LAYOUT - mm - no keycaps',
        f"PCB outline {data['pcb_width']:.1f} x {data['pcb_depth']:.1f}; thickness {data['pcb_thickness_nominal']:.2f} nominal",
        f"Outer top / bottom plates {data['top_plate_thickness']:.1f} / {data['bottom_plate_thickness']:.1f}; cavity {data['cavity_height']:.1f}",
        f"Heatsink {data['heatsink_envelope'][0]:.1f} x {data['heatsink_envelope'][1]:.1f} x {data['heatsink_envelope'][2]:.1f}; web 3.0",
        'PCB front Z0; heatsink web Z4 to Z7',
    ]
    for i,note in enumerate(notes):
        text(note,cx,y1+10+8*i,z,3.6)
    annotation=bd.Compound(children=parts,label='DIMENSIONS_REFERENCE_ONLY_mm')
    annotation.color=srgb('#36DDE0')
    return annotation


@step(out='../STEP/mounting_dimensions.step')
def mounting_dimensions():
    return guides(measurements())


if __name__=='__main__':
    data=measurements()
    (PROJECT/'dimensions.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('top','bottom')},indent=2),flush=True)
    mounting_dimensions()
