> Superseded for current enclosure work by ../model_completion_2026-10-07/PHBox-ChocV2-assembly.step and its README. This export predates the remaining component and V2 model additions.

# STEP export and capacitor-model investigation — 7 October 2026

KiCad 10.0.6 STEP exports are under this folder. Use `PHBox-assembly.step` to retain component identities/assembly structure. Use `PHBox-single-compound.step` as one imported CAD shape for enclosure reference and Boolean operations. The compound contains disconnected solids: it is not a single watertight solid. No artificial bridges or component-envelope infill have been added. `PHBox-fused.step` tests native KiCad `--fuse-shapes`; that switch does not promise a connected board-plus-components solid.

Validation completed: all three exports re-import as valid CAD geometry with 162 solids. Native `--fuse-shapes` did not reduce the solid count for this export. Single-compound round-trip volume agrees within approximately 0.000024 mm3. Generic capacitor model heights are 0.50 mm (0402), 0.80 mm (0603) and 2.10 mm (Kemet B), before assembly stand-off or manufacturer tolerances. Full assembly bounds include protruding module leads; they are not the finished enclosure dimensions.

## Missing capacitors

17 capacitor instances referenced `${KICAD8_3RD_PARTY}/3dmodels/com_github_CDFER_JLCPCB-Kicad-Library/JLCPCB.3dshapes/C_0402.step`, a legacy external plugin location. Other instances used installed KiCad 10 standard models. C41 had no model clause at all. All 44 C references now use project-local STEP files: 0402/1005 metric, 0603/1608 metric for C41 and Kemet B/EIA-3528-21 for C19/C43. All paths exist; the standard library files were copied without modifications. Both Samsung tolerance footprints in PHBox.pretty have matching portable references.

These are generic package models, not supplier-specific maximum-tolerance or soldered-assembly models. In particular, use each capacitor's actual MPN/datasheet for maximum height before machining reliefs. Adding a model for C41 does not change the BOM or decide whether it should be populated; it is absent from the accepted assembly BOM. Confirm the intended assembly variant before treating its model as installed hardware.

Only model clauses changed in the active PCB: exact comparison after stripping model clauses proves every other board datum unchanged. `model-audit.json` records all references and file availability. Original board retained as `board-before-model-fix.kicad_pcb`. Prior manufacturing packages were not regenerated or changed because fabrication/CPL data is unchanged.

## Remaining export omissions

- L1 references a nonexistent AOTA-B201610SR47MT.STEP file; overriding the KiCad version variable cannot create it.
- D21 references nonexistent ST_QFN-2L_1.6x1.0mm.step.
- U4 and D1–D20 have no assigned model.
- H1–H12 are bare mounting holes; omission of screw models is expected.
- Installed Choc switch bodies/keycaps, screws, OLED standoffs and finished solder/pin profiles are not represented by the PCB assembly. Socket models represent sockets only.

Consequently this export is not a complete machining keepout for either heatsink. Preserve explicit relief envelopes for these omitted components until validated model or drawing-derived geometry is added. Generic shapes must not silently stand in for manufacturer maxima.

## Export and coordinate convention

Native command: `kicad-cli pcb export step --force --subst-models --user-origin 0x0mm --define-var KICAD10_3DMODEL_DIR=... --define-var KICAD9_3DMODEL_DIR=... --define-var KICAD7_3DMODEL_DIR=... -o PHBox-assembly.step Flatbox-rev8.kicad_pcb`. Installed library root is `D:/Program Files/share/kicad/3dmodels`. A second export adds `--fuse-shapes`.

STEP uses KiCad's CAD export axes and layer treatment, not the mechanical sheet's Z=0 front-seating datum. Register CAD to actual board front/back faces before using recorded Z heights. Do not assume STEP substrate bounds equal the approved finished-board thickness. `geometry-validation.json` records solid counts, validity and bounds after re-import; it also records capacitor model bounds. `combine.py` flattens the exported solids into a single compound and checks a STEP round trip.

Source of copied capacitor models: installed KiCad 10 standard library, https://gitlab.com/kicad/libraries/kicad-packages3D. License: CC-BY-SA 4.0 with KiCad library exception, https://www.kicad.org/libraries/license/. All source model headers retained. These files have different provenance from existing EasyEDA or OEM models.

## Cleanup — 9 October 2026

The three superseded STEP outputs named above were removed to reduce disk usage. Use the Choc V2 exports in ../model_completion_2026-10-07. Original scripts, model-audit.json and geometry-validation.json remain as historical provenance and verification evidence; combine.py requires regenerating its old inputs before use. These historical generators are not instructions to modify the active PCB.

