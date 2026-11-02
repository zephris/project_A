# Separate Z geometry page

Historical V1/underside-USB reference. USB2 is now on the top side; see the [8 October revision](../../USB2-top-assessment-2026-10-08.md) and the current [native CAD height check](../../heatsink_2026-10-08/usb-top-check.json). The table and diagrams below retain the earlier geometry.

Open `index.html` for the dedicated local page, or view `pcb-z-geometry.png` / `.svg`.
CSV and JSON provide the same dimensions in machine-readable form.

Z=0 is the nominal PCB front seating plane. Positive Z points towards the switches
and display; PCB back is nominally Z=-1.6 mm. The picture places separate feature
sections side-by-side; it is not a continuous physical cross-section through them.

| Feature | Nominal Z extent, mm | Basis / qualification |
|---|---|---|
| PCB | -1.6 to 0 | General thickness 1.6 mm; finished 1.44-1.76 mm under JLCPCB's published +/-10% |
| OEM Choc V1 | 0 to +8 | Housing 5 mm + stem projection 3 mm; top at +5 mm at nominal full stroke. Keycap, pin tails and component tolerance omitted |
| Retention plate | +0.9 to +2.2 | 1.3 mm trial plate; installed height requires actual latch/seating check |
| OLED U5 | +2.0 to +5.7 | 3 mm mounting gap, CAD body -1.0 to +2.7 relative to module mounting reference; long untrimmed pins excluded |
| RP2350 QFN-60 | 0 to +0.85 + s | Package height A=0.80 / 0.85 / 0.90 mm; s is unknown assembled solder stand-off above the PCB |
| USB2 SMD main body | -9.40 to -3.70 | 5.7 mm shell; 2.1 mm elevation above back seating plane; excludes locating pegs |
| Compact dongle trial | -10.55 to -2.55 | 8 mm body centred on nominal mating centre -6.55; body/plug alignment requires sample verification |

Sources: [Kailh OEM drawing](https://www.kailhswitch.com/Content/upload/pdf/202215927/CPG135001D01-16.pdf),
[RP2350 datasheet section 14.1](https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf),
[USB-A manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/b82f44b617887c4bf965ef8115e91ba5.pdf?productCode=C46400),
[JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).
OLED heights come from the exact EasyEDA model documented in `3dmodels/README.md`.

The active SMT connector requires two plastic locating holes, with no recessed body cutout. Its simplified STEP is a fit reference. See `mechanical/USB2-SMD-edge-assessment-2026-10-05.md`.

The KiCad general thickness is 1.600 mm, while the declared copper/dielectric/mask
layer thicknesses sum to **1.647165 mm**. These are source values, not measured
boards. Confirm the JLCPCB-approved stack and consistent thickness convention before
freezing Z hardware. The native STEP export's substrate solid and viewer model
placement include different layer/reference treatment; do not equate its bare-body
bounding box with the finished-board thickness specification.

The MCU top boss must satisfy `Z_contact_face = s + A + compressed thermal pad`.
For illustration only, a 0.5 mm pad at 20% compression gives a 0.40 mm gap, and a
nominal contact-face height of 1.25 mm + s. The pad supplier's compression/force
curve, assembled stand-off and local PCB shape must determine the final gap and
stop height. No MCU clamp force or safe thermal performance is established here.

The user-required layer order is retained: bottom outer plate > lower gasket >
bottom spreader > PCB > upper spreader interwoven with retention plate > upper
gasket > top outer plate. Final plate/carrier thicknesses, foam cuts, gasket travel,
keycap clearance, remaining component heights and total enclosure height remain
unassigned; the drawing does not invent released values for them.

Regenerate with `../build_z_geometry.py`. The XY map was refreshed from the same active PCB revision. Historical packaged maps predate the SMT replacement.
