# Reference-case comparison — 9 October 2026

This is a measurement and mechanism study, not a transplanted case or PCB design.
Downloaded source geometry is retained in `reference/port-cases`; reviewed snapshots
are in `review`. The source repositories remain the authority for licences.

## USB surrounds

The [Flatbox Rev 8 case CAD](https://github.com/jfedor2/flatbox/tree/master/hardware-rev8/extras)
contains a rounded USB-C opening split between the case halves. Measured opening:
9.74 × 4.01 mm, corner R1.655. The included HRO shell is 8.94 × 3.21 mm,
R1.255: 0.40 mm nominal clearance per side. Its USB-A opening is 15.8 × 6.8 mm;
the export does not include an identifiable USB-A body, so its shell clearance
is not established. The README fixes the PCB to the case with five M2 screws.

The [Open_Core0 printed frame](https://github.com/OpenStickCommunity/Hardware/tree/main/Boards/GP2040-CE%20Official%20Controllers/Open_Core0/3D%20print%20files)
uses stepped wall openings and a projecting port bay. Horizontal sections at
Z=3 and 4 show a large opening widening from 27 to 31 mm across the wall, and
a smaller opening widening from 13 to 14 mm. These dimensions describe the
downloaded full-frame mesh, not verified connector-part clearances. Neither
reference establishes environmental sealing.

Our foam-mounted PCB needs a motion allowance absent from a fixed PCB case.
The adapted surround uses 2.8 mm-deep printed collars, at Y=−36.4..−33.6,
with 0.20 mm running clearance beyond ±0.50 XY / ±0.25 Z movement:

| Interface | Rigid mating access | Roof |
|---|---|---|
| C2344 USB-A | 15.8 × 6.6, R0.20 | 2 mm top acrylic; collar has side cheeks |
| HRO USB-C | 10.34 × 4.11, R1.455 | Integral contoured printed collar and rear spacer roof |

The native USB-C front shell has R1.255 corners. Its soft collar hole now uses
8.74 × 3.01, R1.155, giving 0.10 mm nominal inward offset around that outline.
The earlier small corner radius left gaps at the rounded shell corners.
The close USB-C roof clears the highest shell pose by 0.20 mm at its centre;
the rear roof has 3.395 mm clearance. USB-A roof clearance is 0.75 mm at upward
travel. Compliant collars close the motion gaps while allowing PCB float.
Rigid collars should not clamp shells or carry insertion force through the foam.

## Option buttons

[Flatbox Rev 8](https://github.com/jfedor2/flatbox/tree/master/hardware-rev8)
offers two distinct mechanisms. Variant A has printed flexure flaps over
6 × 6 × 5 mm tact switches. Variant B uses taller 6 × 6 × 7 mm switches and
silicone caps through 7.5 mm holes. The two downloaded tops were visually
reviewed: A has narrow three-sided flap cuts, B has six round cap holes.

[Open_Core0](https://github.com/OpenStickCommunity/Hardware/tree/main/Boards/GP2040-CE%20Official%20Controllers/Open_Core0)
provides six auxiliary inputs plus two additional auxiliary inputs. Its downloaded
BOM specifies eight Yuandi TS-1095-A11B3-D1 tact switches (C493055), distinct
from its BOOTSEL/RESET switches. The top-insert mesh shows rectangular auxiliary
button surrounds. This supports using individual recessed, guided actuators;
it does not establish a drop-in cap, measured travel or spring force for our H5 parts.

For our acrylic top and moving PCB, retain the six captured plungers: Ø5.6 bodies,
Ø6.2 guides, Ø8 retaining flanges, 1.2 mm nominal exposed height. This applies
the individual-cap approach without switching to H7 tact switches or relocating
PCB pads. Flatbox A's flap concept could be used in a separate printed insert,
but acrylic flexures and copied flap dimensions are unsuitable without material,
stroke and fatigue tests. Silicone caps would need the correct stem fit and height;
the Flatbox B dimensions are not interchangeable with our current stack.

The switch's contact dome supplies tactile snap and restoring force, as described
in [the manufacturer's tactile-switch construction guide](https://www.aratas.com/us-en/products/switches/tactile-switches/tactile-switch_features); no additional
coil springs are included. An auxiliary spring adds cap resistance, not a new
tactile snap, and can reduce the relative prominence of the click. First verify
cap friction, alignment and return at both PCB travel extremes. If a different
feel is wanted, specify a compatible switch with the desired force/travel before
adding a spring. The current exact H5 switch MPN remains unspecified: actuator
height 5 mm and operating stroke 0.35 mm are modelling assumptions.

These conclusions preserve the PCB, acrylic architecture and current cap geometry.
No firmware or GPIO changes are required for a purely mechanical actuator change.
