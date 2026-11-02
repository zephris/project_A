"""OEM dimensioned reference, not exact vendor CAD; units mm, F seating Z=0."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'stage2_work/enclosure_cad_dependencies'))
import cadquery as cq
def block(x,y,z,w,l,h):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
def main():
    # OEM 7.80 total above SMT seating, 5.70 main body -> elevated body base 2.10.
    # Y registration to recommended pad/peg drawing; fine shell details omitted.
    shell=block(0,-7.7,2.1,13.1,13.6,5.7).cut(block(0,-8.0,2.4,12.5,14,5.1))
    back=block(0,-1.6,2.4,12.2,1.4,5.1)
    tongue=block(0,-8,4.1,11.6,11,.85)
    a=cq.Assembly(name='USB_A_904_131A2032S10200_OEM_REFERENCE')
    a.add(shell,name='shell',color=cq.Color(.75,.76,.78));a.add(back.union(tongue),name='insulator',color=cq.Color(.2,.2,.19))
    for i,x in enumerate([-3.5,-1,1,3.5]):a.add(block(x,0,0,.6,2.5,.25),name=f'SMT_contact_{i+1}',color=cq.Color(.8,.65,.3))
    for i,x in enumerate([-7.5,7.5]):
        foot=block(x,-2.7,0,3,5.4,.25).union(block(x,-2.7,.25,.3,5.4,2.15))
        a.add(foot,name=f'SMT_shell_{i}',color=cq.Color(.75,.76,.78))
    for i,x in enumerate([-2.5,2.5]):a.add(cq.Workplane('XY').circle(.6).extrude(1.2).translate((x,-4.4,-1.2)),name=f'locating_peg_{i}',color=cq.Color(.2,.2,.19))
    a.save(str(ROOT/'3dmodels/USB_A_904-131A2032S10200_reference.step'))
    print('10 reference solids; two locating pegs only enter PCB; shell and contacts fully SMT.')
if __name__=='__main__':main()
