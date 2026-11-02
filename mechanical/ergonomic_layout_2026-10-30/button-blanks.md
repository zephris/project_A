# Removable blanks for unused main buttons

Prototype for the current **24 mm faceplate openings**, nominal **2 mm acrylic**.
Print one plug for each unused main button. This part is not for the six small
option-button holes and does not fit the older 26.5 mm cover openings.

| Feature | Dimension |
|---|---:|
| Visible circular flange | Ø25.8 mm |
| Rise above faceplate | 1.6 mm |
| Depth below faceplate top | 2.8 mm |
| Overall height / supplied print height | 4.4 mm |
| Opposed fingernail grooves | 6 mm wide × 0.4 mm high, open at the lower rim |
| Material above grooves | 1.2 mm |
| Curved clip wall / vertical height | 1.6 / 1.9 mm |
| Isolating clearance above the flexible arms | 0.5 mm |
| Intended hole diameter range | 23.8–24.2 mm |
| Intended acrylic thickness range | 1.8–2.2 mm |

The initial 0.8 mm rise target was increased to 1.6 mm so the grooves retain a
1.2 mm upper lip. Two opposed curved cantilevers provide a longer flexure than
short straight snap legs while keeping the part shallow. Their release ramps
allow the plug to be pulled out rather than permanently locked in place.
[Formlabs' snap-fit design guide](https://formlabs.com/blog/designing-3d-printed-snap-fit-enclosures/)
supports using an extended cantilever path and physical fit iteration. It does
not qualify this plug's force or fatigue life.

## Files

- [button_blank.stl](STL/button_blank.stl): one plug, face-down and at Z=0 for printing.
- [button_blank.step](STEP/button_blank.step): the same print-oriented part for CAD editing.
- [button_blank_coupon.stl](STL/button_blank_coupon.stl): optional single test strip,
  100 × 36 × 2 mm; holes are 23.8 / 24.0 / 24.2 mm from left to right.
- [button_blank_coupon.step](STEP/button_blank_coupon.step): coupon CAD.
- [button_blank_fit.step](STEP/button_blank_fit.step): installed example in the
  centre hole of the coupon; this assembly is for inspection, not printing.
- [Editable dimensions](button-blank-spec.json), [native check](checks/button-blank.json),
  [mesh measurements](checks/button-blank-dfam.json) and
  [orientation comparison](checks/button-blank-orientations.json).

The main PCB, faceplate, spacer, heatsink and switch-plate files are unchanged by
this accessory. Print files for the plugs are separate from the older mock kit.
The current complete-case STEP still has the previously documented stale cover;
use the separate fit example above to inspect the plug.

## Fit and removal

1. Remove the **keycap** from the unused main switch. The Choc V2 switch can
   remain installed if its actual height and the case stack match the checked
   envelope. Do not push the plug over a keycap.
2. Clear all support from beneath the two curved arms. Each arm must flex
   independently; support left in the 0.5 mm gap prevents the snap from working.
3. Orient the **two grooves left/right**, so the clip arcs lie front/back.
   Keep within ±10° of that orientation or its 180° equivalent. This matters
   especially for SW16 beside the heatsink; arbitrary rotation is not qualified.
4. Press the plug evenly into the hole until the flange rests on the acrylic.
   Measure an undersized printed/mock hole rather than forcing the clips into it.
   Test first on the coupon or an offcut of the actual acrylic.
5. Hook fingernails into both side grooves and lift evenly. The release ramps
   retract the clips. Avoid levering a metal screwdriver against the acrylic edge.
6. Check that fitting the blank has not actuated the switch, and that PCB float
   remains free. Refit a keycap after removing the blank to restore the button.

## Printing

Use **unfilled PETG** for the intended repeated-removal prototype. PLA is a
shape/fit trial; do not infer repeated clip life from a successful first snap.
[Bambu's filament guide](https://cdn1.bambulab.com/filament/FilamentGuide-EN-2.pdf)
is the material-selection reference; use the profile matching the actual PETG
spool rather than guessing Basic versus HF.

The supplied orientation puts the cosmetic face on the bed, with clips upward.
Use a 0.4 mm nozzle and 0.10 mm layers for the shallow grooves; 0.20 mm layers
are a faster trial after confirming groove resolution. Four perimeters and
solid infill are reasonable starting settings for this small part. Avoid a brim
touching the removal grooves, or trim it completely.

Local support is needed below the curved cantilevers. With AMS Lite, use PLA
as a removable support interface for the PETG part, then verify clean separation
on one sample. Do not let support or a purge layer bond the arms to the roof.
This is a geometry/print recommendation, not a supplied or validated sliced job.

The exact STL is one watertight body. The fact-only tool measures minimum
sampled wall 1.2 mm and p05 1.595 mm; the minimum is at the supported removal lip.
Compare with the installed DfAM guide's FDM supported-wall limit of 1.2 mm.
Unsupported clip-wall qualification is separate: nominal radial thickness is
1.6 mm, but the pooled thickness percentiles do not isolate the arms. Do not
claim a fatigue or unsupported-wall qualification from that pooled result.

The current orientation has 46.13 mm² of down-facing area below the 45° limit
(3.2% of total area). The six-orientation comparison gives no useful improvement:
the best side pose reduces it only to 45.73 mm² and raises build height from
4.4 to 25.8 mm. The support-volume figure, 113.9 mm³, is a coarse prism estimate,
not actual slicer consumption. Support removal, snap force and repeated cycles
still need a printed first article.

## Tolerances and limits

The acrylic and print ranges above are acceptance targets, not JLCPCB PCB
capabilities. JLCPCB's PCB allowances remain in the separate
[manufacturing-tolerance review](manufacturing-tolerances.md). The plug locates
to its own acrylic opening; PCB guide clearance must not be counted as plug-to-hole
clearance. It matters separately for the switch and heatsink moving underneath.

The rigid pilot radius is 11.65 mm, leaving 0.15 mm radial clearance at the
smallest hole after the allocated +0.1 mm printed-radius error. The clip ridge
radius is 12.35 mm: estimated insertion deflection can reach 0.55 mm with the
opposite tolerance stack. Even the small ridge / large hole combination retains
0.15 mm nominal radial engagement. The curved-arm strain estimate is only a
straight-beam proxy, not FEA or a guaranteed permissible material strain.

No press force, pull-out force, accidental-press load, gasket preload or cycle
life is qualified. Test one plug, actual acrylic and an installed switch before
printing a full set. The coupon checks size only and does not reproduce acrylic
stiffness or edge brittleness.

## Checks completed

The saved STEP is valid and one solid; the saved STL is watertight and one
connected body. Native checks cover nine hole/thickness combinations; only
the free-state latch ridges intersect the panel, as required for their snap fit.
There are no rigid-body panel intersections outside those ridges.

Switch/socket checks passed at 54 sampled rotated/displaced poses, including
the 1.463 mm allocated radial offset and ±0.41 mm Z allowance. The roof leaves
**0.590 mm** above the modeled unpressed stem at the upper Z allowance. The
two exact PCB-selected STEP models were loaded individually to avoid a
memory-heavy complete-board import; their stem height matches the independently
measured saved-board height of 8.600 mm.

All 16 positions clear the modeled heatsink, screen frame, posts and hardware
at the stated sampled ±0.5 mm XY / ±0.41 mm Z poses and ±10° plug orientation.
Nominal minimum gaps include **2.214 mm** to the screen frame at SW1 and
**2.600 mm** to the heatsink at SW16. These sampled checks are not a continuous
swept-envelope or manufacturing tolerance proof. The plug, coupon and installed
example were each rendered and visually reviewed.

The local CAD Viewer did not become ready during this attempt. File-open
requests were queued in Codex; that does not confirm they are visible. The
saved STEP/STL files, reviewed renders and native check report are available
through the links above.
