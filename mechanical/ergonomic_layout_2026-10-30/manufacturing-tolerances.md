# Manufacturing allowances for the selected 20 mm caps

## PCB basis — checked 30 October 2026

[JLCPCB's current rigid-PCB capability table](https://jlcpcb.com/capabilities/Capabilities/)
lists regular routed outlines ±0.2 mm, precision routing ±0.1 mm, drilled-hole
position ±0.075 mm, through-hole diameter +0.13/−0.08 mm, non-plated slots
±0.2 mm, and ±10% thickness for boards at least 1 mm thick. A nominal 1.6 mm
board can therefore finish at 1.44–1.76 mm. The existing order basis is regular
routing. Precision routing is not assumed.

JLCPCB says holes at least 6.3 mm are routed. H4/H6 are 6.4 mm locator openings:
obtain CAM confirmation of their routed profile and position tolerances rather
than assigning the small-drilled-hole diameter tolerance automatically.

## Conditional cap-opening allocation

[tolerance-budget.json](tolerance-budget.json) stores the inputs and their
provenance; [the calculation](checks/tolerance-budget.json) uses worst-case
linear addition rather than a statistical RSS estimate.

The following are **design acceptance targets**, not measured parts, quoted
supplier promises or extra JLCPCB capabilities:

| Interface | Allocation |
|---|---:|
| 6.4 mm routed locator opening | Maximum diameter 6.6 mm; position ±0.2 mm per axis, pending CAM acceptance |
| Printed 5.4 mm guide | Minimum diameter 5.3 mm; position ±0.1 mm per axis |
| Choc V2 switch location | ±0.075 mm per axis allocation, to be confirmed against the switch/plate seating geometry |
| Additional switch/cap seating play | ±0.1 mm per axis |
| Nominal 20 mm cap | Maximum measured outer/skirt diameter 20.2 mm |
| Acrylic opening | Up to 0.2 mm diameter undersize; centre ±0.1 mm per axis |

The maximum locator radial play is (6.6−5.3)/2 = **0.65 mm**. Adding conservative
diagonal position bounds gives **1.463 mm** total lateral allowance. A nominal
24 mm opening, reduced to 23.8 mm, around a 20.2 mm maximum cap leaves
(23.8−20.2)/2−1.463 = **0.337 mm** radial margin. This exceeds the allocated
0.2 mm residual target. The original 22.5 mm proposal would give **−0.413 mm**;
it has been superseded. Minimum acrylic web is now **6.70 mm**.

Do not treat PCB outline error as a second cap-centre error after the guide/hole
location stack: this design locates the board using H4/H6. Outline tolerance is
a separate perimeter-to-spacer fit. A larger opening does not fix guide binding,
a warped board, an oversized cap skirt or a cap that seats incorrectly.

The native selected-cap check covers the saved 24 mm STEP/DXF holes, the
20 mm Z=0–15 mm guard envelopes, and newly added acrylic versus nearby board
components. For that local check only, ±0.16 mm PCB-thickness variation is
conservatively added to ±0.25 mm travel, giving **±0.41 mm Z**. Sampled XY
poses are the nominal centre and ±0.5 mm corners; the analytic budget above
addresses the larger locator allowance. This is not a full case travel check.

## Interfaces still requiring qualification

- The 0.6 mm nominal PCB-to-spacer relief cannot be read as independent ±0.5 mm
  motion plus PCB outline and FDM errors. Check the actual guide/rim constraints
  together; relieve the rim if the intended motion is obstructed. Depaneling
  burrs and rail removal must also be addressed.
- The existing 0.302 mm plate/heatsink gap and SW16's 1.00 mm nominal cap/heatsink
  gap need their own cutting, mounting-hole, fastener-play and cap-skirt budget.
  PCB outline error does not directly change the distance between two
  PCB-mounted parts, but relative mounting/feature errors do.
- Board thickness affects rear retainers, screw engagement and foam compression.
  It does not automatically shift a heatsink referenced to the PCB front face.
  Confirm the finished stack and thermal-pad compression before final milling.
- Acrylic size/thickness, CNC aluminium, FDM shrinkage, SGF/generic cap dimensions,
  screen-module tolerances and THT seating are separate supplier/measurement
  inputs. JLCPCB's PCB capability table does not qualify them.

No entire-assembly tolerance release or fabrication release is implied by the
conditional cap-opening calculation. Measure a first article and fit all caps
through their complete stroke before cutting final enclosure parts.
