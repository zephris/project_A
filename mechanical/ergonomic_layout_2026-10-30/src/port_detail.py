"""Saved-artifact close-up; crop faces are presentation sections, not case openings."""
from pathlib import Path
import json
from cadgen import step,read_step,read_scene,build123d as bd
from common import HEAT
HERE=Path(__file__).resolve().parents[1]

@step(out='../STEP/port_detail.step')
def port_detail():
    window=bd.Pos(181.5,-37,1.5)*bd.Box(73,28,19)
    items=[]
    for name in ('top_acrylic','bottom_acrylic','top_spacer','bottom_spacer','port_seals'):
        solids=[]
        for s in read_step(HERE/'STEP'/f'{name}.step').solids():
            cut=s.intersect(window)
            if cut is None:continue
            if hasattr(cut,'solids'):solids.extend(cut.solids())
            else:
                for item in cut:solids.extend(item.solids())
        items.append(bd.Compound(children=solids,label=name+'_presentation_crop'))
    scene=read_scene(HEAT/'reference/board.step')
    z=json.loads((HEAT/'registration.json').read_text())['front_z_native_mm']
    shell=next(n for n in scene.leaves() if n.label=='C2344_shell_OEM_reference')
    for ref,label in ((shell.ref.rsplit('.',1)[0],'USB_A_C2344'),(str(HEAT/'reference/board.step')+'#o1.26.1','USB_C_HRO')):
        p=scene.resolve(ref).shape().moved(bd.Location((0,0,-z)))
        p.label=label;items.append(p)
    return bd.Compound(children=items,label='port_detail_sectioned_case_not_fabrication')

if __name__=='__main__':port_detail()
