# PHBox PCB mechanical map and tolerance reference

Extracted from the active `Flatbox-rev8.kicad_pcb` with KiCad 10.0.6 on 2026-10-05.
The source PCB and existing manufacturing packages were not changed.

## Geometry and coordinate system

Nominal outline: **272.600 x 171.000 mm**, with **R5.000 at all four corners**.
Nominal thickness: **1.600 mm**, four copper layers. Dimensions come from the
Edge.Cuts centreline; its 0.05 mm stroke width is not added to the finished board.

The coordinate origin is the lower-left corner of the outline's bounding rectangle,
which is outside the material at the rounded corner. X increases right, Y towards
the USB-C edge. KiCad absolute coordinates map as follows:

```
X_CAD = X_KiCad - 52.282180
Y_CAD = 205.516558 - Y_KiCad
Z_CAD = 0 at the PCB front surface
PCB nominal thickness extends from Z=-1.600 to Z=0
```

This is a convenient enclosure reference, not a supplier-agreed inspection datum.
Drawing coordinate decimals describe nominal CAD positions, not manufacturing accuracy.
The previous retention plate CAD uses the same XY origin, but its Z=0 is its own
underside. Position that part separately when building the assembly.

Included geometry: 12 mounting holes, four OLED mounting holes, 16 switch centres,
116 round NPTH holes, 331 round PTH holes/vias and four PTH slots: **451 total**.
Component anchors and rotations are included in JSON, with front/back side identified.
An anchor is not an assembled body extent or a tolerance for component placement.

## Current JLCPCB values and planning assumptions

The current rigid-PCB capabilities page publishes regular routed dimensions at
**+/-0.2 mm**, optional precision routing at **+/-0.1 mm**, thickness at **+/-10%**
for this board, drilled-hole position at **+/-0.075 mm**, through-hole/plated-slot
sizes at **+0.13/-0.08 mm**, and non-plated slot sizes at **+/-0.2 mm**.
Holes at least 6.3 mm are CNC routed. Thus H1-H7, nominal 6.4 mm, use routing.
[JLCPCB current capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).

For the regular-routing option, overall nominal-dimension ranges are 272.4-272.8 mm
and 170.8-171.2 mm. Finished thickness spans 1.44-1.76 mm. These are not a guarantee
of local flatness, component height or hole-to-edge registration.

The older [capabilities URL](https://jlcpcb.com/capabilities/Capabilities) and cached
search results give hole position as +/-0.05 mm; this map uses the current page's
larger +/-0.075 mm. No special press-fit or precision-routing option is assumed.

Two additional allowances are explicitly **engineering planning assumptions**:

- Independently allow each board edge to move 0.2 mm outwards. This gives a conservative 273.0 x 171.4 mm bounding box. It is separate from the published overall dimension range, and must not be read as another supplier guarantee or added twice to the same calculation.
- Allow round NPTH diameters +/-0.2 mm until JLCPCB confirms the exact process. The current page does not separately state a round-NPTH diameter tolerance. Its non-plated-slot tolerance is not proof of the same guarantee for round holes. Planning ranges are H1-H7: 6.2-6.6 mm; H8-H12: 2.0-2.4 mm; OLED: 2.8-3.2 mm. CNC-routed hole position relative to drilled holes must also be confirmed; no +/-0.075 mm guarantee is assigned to the routed holes.

No ISO positional tolerance, true-position diameter, radial tolerance zone or process
capability distribution is inferred from the published +/- position number. The
factory needs to confirm its datum and whether this is per-axis or radial before
designing a precision locating fit. Component placement and OEM component tolerances
are separate from board machining tolerances.

## OEM Kailh Choc V1 assumptions

Switch centres SW1-SW16 are extracted from the native board, checked against the
central 5.05 mm NPTH and used at the PCB's zero-degree orientation. The manufacturer's
PG1350 drawing shows a **13.8 mm housing plan**, **15.0 mm maximum flange plan**, a
**5.0 mm housing height**, **3.0 mm stem projection** and **3.0 mm nominal full travel**.
The rest-height envelope is therefore **8.0 mm above the PCB seating plane**.
The supplied OEM drawing is a 20 gf variant; its operating force is not being assumed
for the user's unspecified Choc V1 spring variant.
[Kailh PG1350 drawing](https://www.kailhswitch.com/Content/upload/pdf/202215927/CPG135001D01-16.pdf).

The switch STEP file contains conservative **15 x 15 x 8 mm boxes**, not a detailed
housing model. They include the resting stem in the same full-width bounding box;
they do not include keycaps, underside pins, latch shape, insertion motion or an OEM
dimensional tolerance. Keycap apertures must be designed from the actual keycaps.

The manufacturer's example uses a 3.4 mm central PCB hole around its 3.2 mm post.
The current combined V1/V2 footprint has a larger 5.05 mm central hole, so that hole
alone should not be treated as a close-fit V1 locator. Plate clips and the remaining
alignment features matter. The existing 14 mm retention apertures and 1.2/1.3 mm
coupons remain fit candidates; this machining map does not certify their engagement.

## Consequences for the floating enclosure

- Use internal insulated mounting hardware and fixed supports within the floating carrier, rather than a rigid bolt pattern between PCB and outer case.
- H8-H12 have only 0.2 mm nominal diametral clearance for a 2 mm shank. Under the unconfirmed +/-0.2 mm NPTH planning range that can become zero clearance. Do not rely on these holes as a guaranteed tight M2 assembly fit before confirming the factory limits.
- H1-H7 are nominal M6 clearance holes, but routed-hole registration is not established. Avoid treating all seven as simultaneous precision pin locations. Clearance bushings, slots in the carrier and a controlled locating scheme can avoid overconstraint while retaining the unchanged PCB.
- For a two-feature fit, relative position uncertainty accumulates from both parts. If the published +/-0.075 mm were confirmed per axis, two independently varying PCB drilled-hole centres could differ by 0.15 mm per axis; mating-plate machining/printing errors add separately. This is a conditional stack calculation, not JLCPCB's definition of true position.
- Enclosure clearance must include the board edge allowance, mating-part tolerance, intended gasket movement and a residual noncontact gap. For example: 0.2 mm edge planning allowance + 0.1 mm pocket error + 0.5 mm lateral motion + 0.2 mm residual gap = 1.0 mm nominal clearance per side, or a 274.6 x 173.0 mm nominal bounding pocket. This is a design example, not an exported enclosure or a guaranteed JLC machining tolerance for acrylic/PLA. Corner radii must also clear the board.
- The 0.32 mm finished-thickness span must enter the vertical stack calculation. Reference the upper thermal contact to local PCB-front supports where practical rather than making thermal-pad compression depend on nominal full-board thickness.
- PCB bow/twist and assembled component-height variation require separate allowances. A generic PCB acceptance limit does not establish flatness near the MCU. Check local gap and load rather than flattening the PCB through the MCU pad.

## Files and reproducibility

- `pcb-geometry-map.png` / `.svg`: drawing with mounting-hole coordinates, OEM switch plan envelopes and tolerance notes. The map is a scaled illustration; do not cut from the rendered image.
- `pcb-outline-only.dxf`: 1:1 mm nominal outline, one closed eight-segment contour.
- `pcb-geometry-nominal-reference.dxf`: nominal outline, all holes/slots, plus named reference layers. `SWITCH_OEM_ENVELOPE`, `REF_*` and `PLANNING_EDGE_ENVELOPE` are reference-only, not PCB milling instructions.
- `pcb-bare-nominal-all-holes.step`: valid nominal bare-board solid, all holes/slots included; no copper, soldermask or component geometry.
- `oem-choc-v1-rest-envelopes.step`: 16 conservative OEM switch bounding volumes in the same coordinate system.
- `mounting-and-screen-holes.csv`, `switch-centres-oem-choc-v1.csv`, `all-holes.csv`: nominal coordinate inventories with clearly marked tolerance status.
- `geometry-and-tolerances.json`, `native-geometry.json`, `validation.json`: machine-readable geometry, source hash and checks.

Regenerate by running `../extract_native_geometry.py` with KiCad 10's Python, then
`../build_geometry_map.py` with the bundled Python and project-local CadQuery libraries.
The geometry is derived read-only. The reference exports are not replacements for
the frozen PCB Gerber and drill manufacturing package.
