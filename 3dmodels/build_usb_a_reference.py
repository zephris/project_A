"""Datasheet-derived USB2 visualization; not a manufacturer-issued production model.
All units mm, footprint front-side frame with +Y up and PCB seating plane Z=0.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'stage2_work/enclosure_cad_dependencies'))
import cadquery as cq

def block(x,y,z,w,l,h):
    return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))

def main():
    # Overall main shell dimensions from the C2763302 manufacturer drawing.
    # Longitudinal placement is registered to the existing footprint's reference
    # outline; it remains approximate pending an exact vendor STEP/model.
    rear=4.647; front=rear-11.0; bottom=-2.10; top=3.62
    outside=block(0,(rear+front)/2,bottom,13.10,11.0,5.72)
    inside=block(0,(rear+front)/2-.3,bottom+.3,12.50,11.2,5.12)
    shell=outside.cut(inside)
    # Rear electrically insulating insert and the USB-A tongue. Detailed springs
    # and folded shell features are deliberately omitted.
    housing=block(0,rear-.8,.30,12.1,1.6,2.65)
    tongue=block(0,(front+rear-1.2)/2,.3,11.6,7.6,.9)
    # Accurate pad registrations, simplified shell legs and contact tails.
    legs=[]
    for x in [-7.85,7.85]:
        for y,length in [(2.647,1.12),(-4.253,1.50)]:
            bridge=block((1 if x>0 else -1)*7.2,y,0,1.6,length,.30)
            leg=block(x,y,-2.64,.3,length,2.94)
            legs.extend([bridge,leg])
    contacts=[]
    for x in [-3.5,-1,1,3.5]:
        tail=block(x,4.253,0,.60,1.50,.25)
        finger=block(x,(front+rear)/2,1.20,.60,6.5,.25)
        contacts.extend([tail,finger])
    a=cq.Assembly(name='USB_A_905_761A203S10200_DATASHEET_REFERENCE')
    a.add(shell,name='shell_reference',color=cq.Color(.72,.73,.75))
    a.add(housing.union(tongue),name='insulator_reference',color=cq.Color(.12,.12,.13))
    for i,l in enumerate(legs): a.add(l,name=f'shell_leg_{i}',color=cq.Color(.72,.73,.75))
    for i,c in enumerate(contacts): a.add(c,name=f'contact_{i}',color=cq.Color(.85,.68,.28))
    dest=ROOT/'3dmodels/USB_A_905-761A203S10200_reference.step'
    a.save(str(dest))
    imported=cq.importers.importStep(str(dest))
    assert all(s.isValid() for s in imported.solids().vals())
    print('Wrote',dest,'valid solids',len(imported.solids().vals()))

if __name__=='__main__': main()
