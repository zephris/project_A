"""Register the native STEP front datum and inventory electronics for fit checks."""
from pathlib import Path
import json
from cadgen import read_scene

HERE=Path(__file__).resolve().parent
scene=read_scene(str(HERE/'reference/board.step'))
source=json.loads((HERE/'constraints.json').read_text())
u1=next(f for f in source['footprints'] if f['ref']=='U1')
ux,uy=u1['pcb_xy']; uy=-uy
parts=[]
for leaf in scene.leaves():
    shape=scene.resolve(leaf.ref).shape()
    bb=shape.bounding_box()
    mn,mx=bb.min,bb.max
    if bb.size.X>250 and bb.size.Y>150:
        substrate={'ref':leaf.ref,'label':leaf.label,'bounds':[mn.X,mx.X,mn.Y,mx.Y,mn.Z,mx.Z]}
    if leaf.label=='Pins' and abs((mn.X+mx.X)/2-ux)<0.1 and abs((mn.Y+mx.Y)/2-uy)<0.1:
        front=mn.Z
        seating_ref=leaf.ref
    # Record only geometry near the new plate, reducing later checks.
    if mx.X>=119 and mn.X<=184 and mx.Y>=-93 and mn.Y<=-37:
        parts.append({'ref':leaf.ref,'label':leaf.label,
                      'bounds':[mn.X,mx.X,mn.Y,mx.Y,mn.Z,mx.Z]})
data={'front_z_native_mm':front,'substrate':substrate,'nearby_parts':parts,
      'front_datum_basis':'MCU metal-lead seating plane, not dielectric substrate top',
      'front_datum_ref':seating_ref,
      'coordinate_transform':'native X,Y retained; subtract front_z_native_mm from Z',
      'reference_step_sha256':scene.document_hash}
(HERE/'registration.json').write_text(json.dumps(data,indent=2)+'\n')
print('Front seating datum:',front,'substrate top:',substrate['bounds'][5],'nearby occurrences:',len(parts))
