from pathlib import Path
import sys
sys.path.insert(0,'stage2_work/enclosure_cad_dependencies')
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
s=cq.importers.importStep('mechanical/model_completion_2026-10-07/SW_Kailh_Choc_V2_red.step').val()
fig,ax=plt.subplots(figsize=(7,7))
for solid in s.Solids():
 v,t=solid.tessellate(.07)
 points=[(p.x,p.y) for p in v if p.z < -1.6]
 if points:ax.scatter(*zip(*points),s=3)
for x,y in [(0,5.9),(5,3.8),(-5,-5.15),(0,0)]:ax.add_patch(plt.Circle((x,y),.65,fill=False,color='red'));ax.text(x,y,f'{x},{y}')
ax.set_aspect('equal');ax.grid();ax.set_xlim(-8,8);ax.set_ylim(-8,8);fig.savefig('mechanical/model_completion_2026-10-07/v2-pin-registration.png')
