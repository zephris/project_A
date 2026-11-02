# Printed fitment mock kit — unpowered use only

**Layout revision:** these complete-kit print files and the manual below retain the earlier button positions. For the [30 October higher/wider candidate](../../ergonomic_layout_2026-10-30/README.md), use the [new replacement-only A1 stack](../../ergonomic_layout_2026-10-30/REPRINT_A1/README.md) and reuse the unchanged pieces listed there. Do not print this old complete kit as the wider revision.

Follow the **[35-step illustrated assembly manual](output/pdf/PHBox_mock_assembly_manual.pdf)**, with one operation per page, highlighted parts, movement arrows, underside views and fitting checks. The [linked step-by-step version](ASSEMBLY_STEPS.md) lists the exact STL files for each operation. Bench-check the rigid USB collar gauges on the empty surround, then remove them before closing over the coarse USB proxy blocks.

For the Bambu A1 with AMS Lite, use the [single stacked PLA/PETG job](STACK_A1/README.md) for the requested vertical layout, or the [individual PLA print kit](PRINT_A1/README.md) for one part or quarter-section per project. The stack uses PETG support contact layers, PLA backing and the same 105 separate meshes. Both print collars as PLA shape surrogates; use real TPU collars separately for compliance tests.

This is a separate mock kit derived from the current 17 mm sandwich factories. Production files and PCB routing are unchanged. **Never power the board with the plastic heatsink surrogate or rigid thermal-pad gauges installed.** PLA/PETG parts do not reproduce acrylic strength, aluminium heat transfer, POM creep resistance or foam compression.

Use [manifest.json](manifest.json) as the full one-of-each print list, including dimensions, source-coordinate bounds, materials and purpose. Every file is in millimetres and has its intended bed plane at Z=0. [STEP/fitment_kit.step](STEP/fitment_kit.step) and the catalog STL are a laid-out visual inventory, **not a single printable assembly or print bed**.

| Included | Purpose and quantity |
|---|---|
| Top and bottom acrylic surrogate panels | One each, 2 mm nominal, original holes and countersinks |
| Acrylic case posts and washers | Eight 12 mm AF5 column envelopes plus sixteen 0.5 mm washers; these are independent case columns, not heatsink posts |
| Upper/lower spacer, switch plate, screen frame | One each from existing geometry |
| Screen posts and rear caps | Four of each, existing 3 mm seats |
| Switch plate stops and rear caps | H1/H2/H3, one of each |
| Heatsink stops, support washers, rear washers/caps | H5/H7/H12, exact existing envelopes |
| Aluminium heatsink surrogate | One, including thermal bosses and service notch |
| Option caps, retainer and optional fastener gauges | Six caps, one retainer, two screw and two nut envelopes |
| USB collars | A and C, unfilled TPU 95A candidate, same production geometry and print orientation |
| Installed-height support and thermal pad gauges | Individual disconnected pad pieces, rigid geometric gauges only |
| PCB surrogate | Outline, H mounting drills, coarse MCU/flash/USB body envelopes; omits copper, solder, other packages and switch sockets |
| OLED module PCB surrogate | 35.4 × 33.5 mm outline, 1.2 mm nominal substrate and mounting holes; glass/header topography omitted |

The PCB surrogate's square USB body boxes deliberately do not represent usable mating connectors or the USB-C corner contour. Use real connectors/dongles to qualify collar interference and insertion/removal. Use real switches, display and final PCB before approving fitment. The OLED surrogate cannot qualify glass clearance.

## Printing economically

Start with the smallest interfaces: one switch aperture from the existing [switch coupon](../STEP/switch_coupon.step), one option cap, one of each screen/switch/heatsink stop, and both USB collars. Then print the enclosure parts. PLA is sufficient for an unpowered shape mock; PETG is preferable for repeatedly assembled rigid mock parts. These are material candidates, not validated service-life substitutions.

Use 0.1 mm layers where nominal thickness matters: 1.3 mm switch plate, 0.5 mm washer gauges, and the collars' approximately 0.317 mm membrane. Measure actual printed thickness and holes with calipers; adjust slicer hole compensation only after the first coupon. Do not assume a nominal STL produces the specified gap. Start with several perimeters and modest infill for large mock panels, then inspect bridges and disconnected islands in the slicer. Avoid scaling parts to fit a print bed.

The heatsink surrogate is flipped so its broad upper face sits on the bed and its thermal bosses face upward. Bottom acrylic is flipped to place countersinks upward. Option caps are inverted; support may be needed around the small actuator stems. Check supports for spacer pockets, overhangs and nut recesses. Supports must not mar the mating seats. Print the TPU collars separately using the filament manufacturer's profile, never rigid PLA/PETG.

Parts wider than 220 mm also have four `QUARTER` alternatives. Choose the full part **or** all four quarter files, not both. Quarter seams have no added pins, scarf joints or overlap; hold them on a flat reference surface and tape the reverse face temporarily. Quartered assemblies cannot reproduce panel stiffness or retain hardware loads. The manifest records original bounds to identify each section and recover its original location. Some quarters contain separate islands; use a removable brim and keep their placement on the flat jig. Full panel dimensions require roughly a 300 × 200 mm usable bed; quarter pieces are below 220 × 220 mm.

## Fit checks

1. Verify printed panel thickness, post seat heights and washer gauges. Dry-stack the independent acrylic columns: 12 mm body plus two 0.5 mm washers gives the 13 mm inner-face separation.
2. Place the PCB surrogate at its original datum and check outline/H drills against spacer guides, switch/heat mounts and collars. Its raised package boxes are deliberately coarse envelopes. When testing the real board, remove the surrogate entirely.
3. Check the heat service notch and boss alignment using rigid pad-height gauges without force. These gauges cannot determine thermal pad preload; use actual 0.5 mm pads and measured package heights for the final assembly.
4. Install switch/screen mock posts and test frame and option cap seating. Check real switches separately for clip retention, LED windows and cap travel.
5. Close the enclosure only with suitable **real screws** or light temporary external clamps. Mock screws/posts have no threads and are not functional fastening hardware. Do not force screws into pilot bores and treat that as a thread qualification.
6. Use actual foam for board float and damping tests, actual TPU for collar compliance, and actual ports/cables/dongles for insertion and extraction clearance.

The current 2 mm heatsink rear caps have omitted threads. Stock M2/M3 × 10 screws provide only about 0.85 mm engagement; × 12 protrude about 0.85 mm below the existing cap without another stack change. **Heatsink screw selection/retainer redesign remains unresolved.** See [heatsink hardware options](../heatsink-hardware-options.md). Printed stop pilots and cap bores reproduce the design for inspection and must not be called production-ready threads.

## Rebuild and checks

From project root, use the existing `mechanical/heatsink_2026-10-08/.venv/Scripts/python.exe` to run `MOCK_ONLY/src/fitment_kit.py`, with the same CAD cache environment as other mechanical sources. Then run `MOCK_ONLY/check_meshes.py`.

[mesh-check.json](mesh-check.json) records saved-STL triangle parsing, finite coordinates, bed-plane placement, dimensions within 0.05 mm and mesh volume agreement within 3.5% of the native solids. Native geometry validity/positive volume is asserted during generation. These checks do not qualify printability, watertightness, screws, thermal performance or structural strength. The catalog image is in [review/fitment-kit.png](review/fitment-kit.png).
