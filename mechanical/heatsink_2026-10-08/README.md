# PHBox MCU and flash aluminium heatsink candidate

Prototype design for **milled 6061-T6 aluminium**, using the current Choc V2 PCB.
The native reference PCB now includes the [9 October C2344 revision](../USB2-C2344-assessment-2026-10-09.md). The heatsink/support geometry is unchanged. This folder's older fitted/mounted exports and26 mm outer-cover references predate C2344; use the [17 mm foam sandwich candidate](../sandwich_17mm_2026-10-08/README.md) for the current integrated assembly.
The stepped underside transfers heat from **U1 RP2350A** and **U3 W25Q128JVSIQ**
through two electrically insulating thermal pads. **SW19 BOOTSEL and SW20 RESET**
have an open-sided service notch. The design does not change PCB fabrication files.

Open [plate STEP](STEP/heatsink_plate.step) for machining geometry and
[fitted assembly STEP](STEP/heatsink_fit.step) for placement, thermal pads and
custom insulating stops. The latter contains reference PCB geometry and is not a
single part to mill. Parametric source is in [src](src/heatsink_common.py).

## Geometry and interfaces

All dimensions are mm. X follows KiCad X; CAD Y is **minus KiCad Y**; Z=0 is the
front component seating plane. The freshly exported STEP puts that plane at
native Z=1.601204, independently measured at U1's metal leads. The dielectric
substrate top at 1.516203 is **not** the seating datum; see [registration](registration.json).

| Feature | Candidate dimension |
|---|---|
| Overall aluminium envelope | 60.0 × 52.9 × 5.7 |
| Main spreader | X=121..181, PCB Y=45..79 |
| Main web / installed Z | 3.0 thick; underside Z=4.0, top Z=7.0 |
| BOOTSEL/RESET notch | Open left; tool outline X=115..136.5, PCB Y=60..75; R3 corners |
| MCU boss | 6 × 6, R0.5 exterior corners; contact face Z=1.30 |
| Flash boss | 4 × 4, R0.5 exterior corners; contact face Z=2.61 |
| MCU / flash pad cuts | 5.5 × 5.5 / 3.5 × 3.5 |
| Thermal pad starting assumption | 0.50 free thickness, 0.40 installed; 20% compression |
| Mounting support stack | 3.50 POM seat + 0.50 installed insulating washer; central hard-stop land ends at Z=4.0 |
| Aluminium volume / estimated mass | 6342.08 mm³ / 17.12 g at assumed density 2.70 g/cm³ |

| Existing hole | KiCad X, Y | Plate bore | Intended internal fastening |
|---|---|---|---|
| H5 | 173.03218, 43.916558 | Ø3.4 | Polymer M3; custom POM stop, Ø8 flange, Ø6.1 pilot |
| H7 | 143.53218, 86.316558 | Ø3.4 | Polymer M3; same stop |
| H12 | 146.93218, 43.916558 | Ø2.4 | Polymer M2; custom POM stop, Ø4.5 flange, no pilot |

The plate now rests on **0.50 mm insulating support washers** at all three holes.
Washers are custom annuli: **Ø8 / Ø4.6** at H5/H7 and **Ø4.5 / Ø3.4** at H12.
They occupy Z=3.50..4.00. Central POM stop lands, respectively Ø4.4 and Ø3.2,
also end at Z=4.00 and prevent soft interfaces from changing the thermal-pad gaps.
The aluminium geometry and thermal mass are unchanged.

An insulating O-ring can replace an annular washer only after its free section,
installed compression, radial expansion and load curve fit the available seat.
Keep the central hard stops: O-rings alone must not set plate height or allow
chip-pad loading to vary with screw torque. **The current assembly models flat
washers, not a selected O-ring product**; the small H12 seat especially needs a
specific ring-size check. These support interfaces remain part of the floating island.

The stop bores are Ø3.4 for H5/H7 and Ø2.2 for H12. H5/H7 pilots extend 1.9 below
the front datum; use relieved insulating rear washers to clear them. Screw lengths,
head projection, rear washers/nuts and polymer-fastener strength remain to be selected.
The represented stops and washers are **custom geometry**, not verified catalog parts.

## Thermal mass

From the saved aluminium STEP, `V = 6342.078 mm³ = 6.342078 cm³`.
At assumed 6061-T6 density `2.70 g/cm³`, `m = 17.12361 g`.
Using specific heat `c_p = 0.896 J/(g·K)`, the lumped plate thermal capacity is:

**`C = m × c_p = 15.34276 J/K ≈ 15.34 J/°C`.**

That is **153.43 J for a uniform 10°C rise**, or **306.86 J for 20°C**.
As a hypothetical adiabatic example, a constant 1 W deposited entirely in the plate
would raise it by **3.91°C/min** and take **153 s** for a 10°C rise. This assumes
uniform temperature and no cooling; it is not the board's measured power or an
MCU junction-temperature prediction. Steady-state cooling depends on pad/contact
resistance, heat spreading, exposed area and enclosure airflow.

The specific heat approximation is supported by the
[Argonne National Laboratory report, section 4](https://publications.anl.gov/anlpubs/2011/06/70320.pdf),
which proposes 0.896 J/g-K for 6061-T6. This is a room-temperature engineering
estimate; material properties vary with temperature. PCB, pads, washers, posts
and fasteners are excluded. Recalculate with [thermal_mass.py](thermal_mass.py);
machine-readable output: [thermal-mass.json](thermal-mass.json).

## Pad selection and assembly

The package-top assumptions are **0.90 for U1** and **2.21 for U3**. These use
the current model tops (0.85 / 2.16) plus an unmeasured 0.05 solder allowance.
Therefore the fitted CAD shows a **0.45 gap**, while the intended soldered assembly
has a **0.40 gap**. The exact gap must be measured before machining contact heights.
For each chip, set `contact face = measured package top + supplier-approved compressed pad`.
Do not substitute one thick sheet spanning both devices or their adjacent passives.

Specify a compliant, electrically insulating pad with documented dielectric strength,
thickness tolerance and pressure/compression curve. The 0.50 thickness and 20%
compression above are prototype assumptions, **not a qualified product specification**.
[Laird's manufacturer brochure](https://www.laird.com/sites/default/files/2022-02/THR-BRO-THERMINTERFACE_Eng_20211103_v2.pdf)
lists pad families with 0.50 mm thickness options. Verify the current exact grade and
compression force before procurement; a high conductivity rating alone is insufficient.
For comparison, Henkel describes
[TGP 3000ULM](https://next.henkel-adhesives.com/us/en/products/thermal-management-materials/central-pdp.html/bergquist-gap-pad-tgp-3000ulm/120324IB.html)
as an electrically insulating, low-stress interface family, but no 0.50 mm variant
has been qualified here. A thicker pad requires different boss heights.

1. Trial the plate outline and post locations with a nonmetal fit print or template.
2. Measure both installed package tops and local PCB flatness. Choose the actual pad.
3. Adjust each contact-face parameter and the stops to establish the approved gap.
4. Cut pads to the specified small footprints, centred on package bodies and clear of leads.
5. Secure the plate through insulating stops and polymer hardware. Tighten to the stops,
   not against the chips; verify pad load and PCB bending rather than assuming the stops
   alone prove safe pressure. Use insulating rear hardware and maintain electrical clearance.
6. Check boot/reset actuation, switch/cap removal, USB plugging and gasket travel.

The plate and posts move with the **floating PCB/island**. Attach no rigid thermal
bridge to the acrylic/PLA outer plates. Preserve the existing bottom plate → gasket →
bottom spreader → PCB → upper spreader/retention plate → gasket → top plate principle.
The main web ends at PCB Y=79. The **H7 mounting tongue extends to Y=91.316558**,
into the earlier retention plate's mounting region. Give the final Choc V2 retention
plate a complementary relief there, or verify separation in Z; its old V1 installed
height is not a released V2 interface. Where an intermediate carrier crosses a stop,
provide clearance around the Ø8 POM flange (start with Ø8.5) rather than trapping it
in the existing Ø6.4 PCB hole. The PCB drill remains unchanged.
The OLED carrier remains independent; no screen-post relocation is proposed.

Keep the electronics zone free of damping foam. Provide ventilation above the plate
and clearance to the stationary enclosure at both suspension travel limits. Required
enclosure inner Z is at least `7 + fastener projection + 0.5 upward travel + clearance`;
use at least 0.5 clearance as a prototype budget. Exact keycaps, fastener heads, gasket
deflection and the full outer enclosure remain unqualified. A sealed plastic/foam
enclosure can trap heat despite this spreader; temperature reduction is not yet established.

## CNC notes and design review

Starting stock **65 × 58 × 8 aluminium 6061-T6** is a proposed blank, with machinist
approval of fixturing and allowances. Suggested process: establish the flat top and
mount bores, flip onto a fixture, remove underside material leaving the two bosses,
then finish the outline and deburr. This is a two-sided 3-axis milling proposal;
no threads, undercuts or deep closed pockets are required.

- Use the flat top as machining datum A. MCU and flash contact faces are respectively
  **5.70 and 4.39 below A**; the general underside is 3.00 below A.
- Request **±0.05 on contact-face offsets and stop height**, contact-face flatness 0.05
  and Ra ≤1.6 µm as proposed drawing requirements. The shop must accept them; they
  have not been measured on a physical part. Other outline dimensions may start at
  ±0.10. Reconcile drill/placement tolerances and hole pitch before ordering.
- Planar outline junctions have R1.5, outer corners generally R2 and notch tool R3.
  A Ø3 end mill geometrically fits R1.5 junctions. Cutter reach, holder access and
  workholding are not verified. Boss exterior R0.5 does not require a Ø1 cutter.
- Remove burrs; specify a light edge break away from pad faces. Edge breaks are a
  machining note, not modeled geometry. Mask thermal contact faces if anodising;
  anodising does not replace the thermal pads and insulating mounting hardware.

Rules were reviewed against [Protolabs Network's CNC design guide](https://www.hubs.com/knowledge-base/how-design-parts-cnc-machining/)
and [Protolabs milling guidelines](https://www.protolabs.com/services/cnc-machining/cnc-milling/design-guidelines/),
accessed 8 October 2026. Their tool-access, internal-radius and tolerance guidance
informs the design; it does not establish the chosen shop's capability. In particular,
±0.05 is tighter than Protolabs' cited typical automated ±0.13 and needs explicit acceptance.

## Validation and rebuild

[Fit-check results](fit-check.json) verify the saved plate STEP is one valid solid;
zero overlap with 50 nearby board occurrences and the mounting supports; three correctly
located through bores; both pads touch their respective bosses without penetration.
Each button's footprint envelope plus **1.5 service margin** is clear; the remaining
clearance to those expanded zones is **1.367 BOOTSEL / 1.343 RESET**. The open notch
also provides a lateral approach. Actual fingertip reach depends on the final case.

The final underside and fitted-board snapshots were visually reviewed: the bosses are
on the underside, the open notch exposes both buttons, and the plate avoids the OLED
and USB-C shell. The saved assembly's plate matches the separate machining STEP in
volume exactly. These checks cover
nominal exported models, not maximum supplier dimensions, solder variation, tolerance
stack-up, fastener heads, strength, contact force or thermal performance. The MCU and
flash remain electronically unchanged. **Candidate for fit/thermal trials; not a released
machining drawing or proven cooling solution.**

Rebuild from the repository root using KiCad 10 Python for `extract_constraints.py`,
then native KiCad STEP export, `inspect_reference.py`, `src/heatsink_plate.py`,
`src/heatsink_fit.py` and `checks/check_fit.py` with the local virtual environment.
See [build.ps1](build.ps1). Runtime pin: [requirements.txt](requirements.txt).
`.venv`, renderer downloads and `.cache` are ignored rebuildable dependencies.
Reference export is tied to the source hash in [constraints.json](constraints.json).
Retain the existing vendor/community model licences when redistributing the fitted assembly.

## OCP CAD Viewer in VSCode

### PCB mounting and separate enclosure plates

[Mounting layout](STEP/heatsink_mounting.step) adds the current Choc V2 hitbox CAD
below the heatsink, rear insulating washers and custom POM retaining caps at
H5/H7/H12. The caps are a **proposed tapped-retainer arrangement**; screw heads,
threads and exact screw lengths are not represented. H5/H7 require polymer M3
fasteners and H12 requires polymer M2. The rear washers clear the existing stop
pilots. Washer Z=-2.15..-1.65 and retainer Z=-4.15..-2.15 are nominal trial values:
adjust the washer seat to the measured finished PCB back surface before assembly.
The reference back seating datum is -1.601204, so this trial leaves 0.049 mm.

The two blue outer parts are **enclosure layout references**, separate from the
aluminium heatsink: 3 mm bottom plate at Z=-15..-12 and 3 mm top bezel at Z=8..11.
They extend 8 mm beyond the PCB outline. The open bezel clears the PCB outline
by 1.4 mm per side, exposing the controls and electronics for this review. Four
20 mm cavity-height spacers are outside the PCB and join the outer plates only.
They do not pass through PCB mounting holes. These heights and outline are new
provisional assumptions, not dimensions taken from a finished enclosure design.

The mounting load path is heatsink → insulating washer/hard stop → PCB → rear
insulating washer/retainer. The island must then be supported by a separate gasket
carrier between the outer plates. **Gaskets and their carrier, bottom thermal
spreader, V2 switch retention plate, keycaps, display support and final port/wall
details remain separate design work and are not modeled by these shell envelopes.**
Do not reuse the historical V1 retention plate or clamp this PCB rigidly to the
outer case. Nothing here changes the PCB or the aluminium machining solid.

[Exploded layout](STEP/heatsink_mounting_exploded.step) separates these layers for
inspection; its offsets are presentation-only. [Mounting checks](mounting-check.json)
record saved nominal geometry tests; they do not qualify gasket deflection or
fastener force. The STEP parts catalog was searched for `nylon M3 screw` and
`nylon M2 screw`: both returned zero candidates. Nylon-insert locknuts were
excluded because their metal bodies do not supply the intended insulating mount.
No catalog fastener has been selected.

Run `view_ocp.py --mounting` for the assembled layout with translucent shell
references, or `view_ocp.py --exploded` to inspect the layer order. Individual
PCB, washer, retainer and outer-plate groups can be hidden in the OCP tree.

The assembled OCP view includes a cyan **reference dimension overlay**. Overall
provisional enclosure size is **288.6 × 187.0 × 26.0 mm**, excluding keycaps and
unmodeled hardware. The PCB outline is **272.6 × 171.0 mm**, with **1.60 mm nominal
finished thickness**; the exported substrate thickness is a different datum.
Both outer plates are **3.0 mm**, with **20.0 mm internal cavity height**. The
heatsink envelope is **60.0 × 52.9 × 5.7 mm**, with a **3.0 mm web at Z=4..7**.
The overlay measures the saved mounting solids and records values and source hash
in [dimensions.json](dimensions.json). Text and dimension lines are contained in
[mounting_dimensions.step](STEP/mounting_dimensions.step), a **nonmanufacturing
reference layer**; none are added to the aluminium machining STEP or PCB.
Use `--no-dimensions` or hide the Dimensions group to suppress them. The exploded
view omits installed-size dimensions because its offsets are presentation-only.

OCP CAD Viewer extension 4.1.0 is installed. The matching Python client is pinned
in the local CAD environment. [view_ocp.py](view_ocp.py) displays the saved plate;
add `--assembly` for the PCB, pads and support washers, or `--supports` for a
focused view of the plate, pads, hard stops and washers. Opening this Python file
triggers the extension's standard autostart.

Select `mechanical/heatsink_2026-10-08/.venv/Scripts/python.exe` with **Python:
Select Interpreter**, then use **OCP CAD Viewer: Open viewer**. The workspace
default now points there; an existing explicit interpreter selection may need
to be changed manually. Run the script with that interpreter once the viewer
is open; pass `--port` if several windows have registered OCP viewers.
# Current connector reference

The active PCB/reference STEP now uses C2344. Use the
[17 mm sandwich assembly](../sandwich_17mm_2026-10-08/README.md) for current
PCB/connector/enclosure fit. The older fitted/mounted STEP views and their checks
below predate this connector replacement; the aluminium plate, pads and stops
are unchanged. Current pin registration is recorded in `usb-top-check.json` and
[the C2344 assessment](../USB2-C2344-assessment-2026-10-09.md).
