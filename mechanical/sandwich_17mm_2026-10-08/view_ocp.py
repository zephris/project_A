"""Send maintained saved sandwich geometry to the current VSCode OCP viewer."""
from pathlib import Path
import argparse
from cadgen import read_scene
from ocp_vscode import show,set_port,Camera
HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=3939);p.add_argument('--exploded',action='store_true')
    a=p.parse_args();set_port(a.port)
    scene=read_scene(HERE/'STEP'/('exploded.step' if a.exploded else 'assembly.step'))
    items=[]
    for group in scene.roots[0].children:
        s=scene.resolve(group.ref).shape();s.label=group.label;items.append(s)
    show(*items,names=[s.label for s in items],alphas=[.35 if 'acrylic' in s.label else 1 for s in items],
         reset_camera=Camera.RESET,show_parent=False,zoom=1,
         quaternion=[0.4247082003,0.1759198966,0.3398511430,0.8204732386])
    print('Sandwich assembly sent to OCP',flush=True)

if __name__=='__main__':main()
