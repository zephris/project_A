"""Open this script in VSCode, then run it with the CAD project interpreter.

The ocp_vscode import triggers the installed extension's normal autostart.
The script sends saved geometry; it does not rebuild or alter the CAD models.
"""
from pathlib import Path
import argparse
from cadgen import read_step
from ocp_vscode import show, set_port, Camera
import sys

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--assembly',action='store_true',help='Show PCB, pads and insulating mounting washers')
    parser.add_argument('--supports',action='store_true',help='Focus on plate, thermal pads, hard stops and washers')
    parser.add_argument('--mounting',action='store_true',help='Show PCB, mounting stack and separate outer plate references')
    parser.add_argument('--exploded',action='store_true',help='Explode the mounting layout for inspection')
    parser.add_argument('--no-dimensions',action='store_true',help='Hide the reference measurement overlay')
    parser.add_argument('--port',type=int,help='Use the registered port of this VSCode window')
    args=parser.parse_args()
    if args.port:
        set_port(args.port)
    if args.mounting or args.exploded:
        from cadgen import read_scene
        name='heatsink_mounting_exploded.step' if args.exploded else 'heatsink_mounting.step'
        scene=read_scene(str(HERE/'STEP'/name))
        groups=scene.roots[0].children
        parts=[]
        for group in groups:
            part=scene.resolve(group.ref).shape()
            part.label=group.label
            parts.append(part)
        alphas=[0.20 if p.label.startswith('REFERENCE_') else 1.0 for p in parts]
        colors=[getattr(p,'color',None) for p in parts]
        if not args.exploded and not args.no_dimensions:
            annotation=read_step(str(HERE/'STEP'/'mounting_dimensions.step'))
            annotation.label='Dimensions_REFERENCE_ONLY_mm'
            parts.append(annotation)
            alphas.append(1.0)
            colors.append('#36DDE0')
        show(*parts,names=[p.label for p in parts],alphas=alphas,
             colors=colors,
             reset_camera=Camera.RESET,show_parent=False,zoom=1,
             quaternion=[0.4247082003,0.1759198966,0.3398511430,0.8204732386])
        return
    name='heatsink_fit.step' if args.assembly else 'heatsink_plate.step'
    geometry=read_step(str(HERE/'STEP'/name))
    if args.supports:
        sys.path.insert(0,str(HERE/'src'))
        from heatsink_common import make_pads, make_stops, make_support_washers
        parts=[geometry,*make_pads(),*make_stops(),*make_support_washers()]
        show(*parts,names=['Aluminium heatsink',*[p.label for p in parts[1:]]],
             reset_camera=Camera.RESET,show_parent=False,zoom=5)
        return
    show(geometry,names=['PHBox fitted heatsink' if args.assembly else 'PHBox aluminium heatsink'],
         reset_camera=Camera.RESET,show_parent=False,zoom=3)

if __name__=='__main__':
    main()
