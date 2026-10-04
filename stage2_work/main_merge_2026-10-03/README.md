# PHBox main-project merge — 2026-10-03

The repaired four-layer candidate was promoted into the root `Flatbox-rev8.kicad_pcb` and its matching schematic. Open the root `Flatbox-rev8.kicad_pro` for subsequent work.

## Validation of the merged main files

High confidence, local KiCad 10.0.6 file/connectivity evidence:

- ERC: **0 findings** (`main-erc.json`). Main-project ERC settings were retained.
- DRC: **0 errors / 0 warnings / 0 open connections / 0 schematic parity findings** (`main-drc.json`, after final refill/save).
- All **144 footprints** and **1,843 track/via objects** match the accepted four-layer candidate. All **432 PCB pad entries** match the fresh schematic netlist; footprint schematic UUID paths match (`merge-audit.json`, `main-netlist.xml`).
- Both inner GND layers have one continuous filled outline (~44,839 mm² each), with no inner signal tracks.
- The 76 checked fixed component positions, rotations and sides match the former main board, including action/option switches, MCU, OLED, USB ports, LEDs and MCU support parts.
- Component references, values and sourcing properties match the former main schematic. Its only component-pin net changes are the accepted no-connect declarations on unused U1 SWCLK/SWD pins 24/25. The former main schematic was byte-identical to the candidate's pre-ERC-repair schematic baseline.
- `git diff --check` passes.

## Merged files and settings

The root PCB, schematic and `.kicad_dru` now contain the repaired design. The project imports the candidate's DRC rules/severities and routing net classes. Existing main schematic/ERC, plotting and editor settings remain. `PHBox.kicad_sym` gained only the three matching frozen legacy symbol definitions; existing definitions remain intact. `PHBox_Repair.pretty` and its registration were added; existing library registrations remain. Blank-line whitespace in the schematic was cleaned without changing its circuit.

The .dru permits only the 16 intentional matching action-switch/LED courtyard overlaps. Other reported rules remain enabled. Existing ignored checks are listed in the DRC report, including missing courtyards; their mechanical verification still requires actual part geometry.

## Recovery

`before/` contains the exact previous main PCB/schematic/project/library tables/symbol library/AGENTS.md. `manifest.json` records before/candidate/final hashes and the absent files before promotion. Restore source files from `before/` into the root project if recovery is needed; retaining the new library registration and rule file would not reproduce the former state, so follow the manifest for those additions. Preserve subsequent edits when restoring.

The candidate and separate `stage2_work/Flatbox-rev8.kicad_pcb` were retained. Existing editor-state/autosave files and manufacturing/firmware outputs were preserved.

## Remaining release checks

Confirm the actual JLCPCB stackup/impedance and DFM, mechanical/enclosure/switch/OLED clearances, USB and bypass return geometry, power/current/thermal/startup behavior, RGB waveforms, GP2040-CE configuration and hardware operation. Quilter USB differential-pair PRC remains deferred as previously directed. Complete BOM/CPL/assembly-preview review and manufacturing outputs from the accepted main revision. This merge validation covers KiCad connectivity, library consistency, placements and fills; no new thermal/EMC/SPICE or manufacturing-release review was performed.
