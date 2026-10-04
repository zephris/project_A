# Direct power traces and moved USB-C repairs — 2026-10-04

## Accepted main revision

The power and USB-C workers edited separate candidates, then a third worker reviewed current/voltage-drop margins, actual copper connectivity and ground contours. Root reviewed the object deltas, combined the repairs, ran native checks, and promoted only the accepted PCB to `Flatbox-rev8.kicad_pcb`. Existing dirty files are preserved. The user confirmed PCB editor saved and closed; native Codex subagents explicitly authorized for this task.

- Broad F.Cu +5V and B.Cu +3V3 backgrounds replaced by GND. Local regulator/core and useful local power copper remain.
- Fifteen 0.30mm LED bypass branches added, including C20 and C35. C26 already had copper. Three 0.60mm +5V joins, two 0.50mm +3V3 joins, and a short MCU 0.15mm escape followed by 0.25mm connection added. One orphan +3V3 zone and 17 old track/via objects removed; no new vias.
- USB1 remains at the user's moved location (158.432180,38.843118), rotation180. Its VBUS, CC, reversible data and GND/shield fanouts reconnected by changing 25 existing tracks. VBUS stem/D21 cathode0.60mm; D21 ground0.50mm. No footprint placement or pad changes.
- 144 footprints unchanged; 432 checked pads match fresh XML; 1,826 track/via objects. All surviving unrelated copper matches baseline, with precisely the two workers' accepted changes.
- Both inner GND planes remain one continuous outline,44790.72595mm² each; no inner signal tracks. Outer GND has29 front/21back contours. Every contour has an actual plated GND anchor to both inner planes, checked by filled-polygon intersections. No floating contour was accepted. Always-remove-islands enabled.

## Final validation and evidence

Exact main native KiCad10.0.6: **ERC0; DRC0 errors/0warnings; opens0; schematic parity0**. Zone refill/save completed. `git diff --check` passes. No DRC rules/severities changed for these repairs.

- `main-drc.json`, `main-erc.json`, `merged-netlist.xml`, `main-audit.json`: final checks.
- `merge-deltas.json`, `power/power-audit.json`, `usb/usb-audit.json`: complete UUID/geometry deltas.
- `usb/merged-manual-trace.json`: actual USB1 pad-to-protection/CC trace paths and GND plane intersections.
- `current_review/native-power-connectivity.json`: actual copper continuity for LED/bypass, MCU/flash/OLED, and isolated host output.
- `current_review/ground-anchors.json`: actual anchors for all50 outer GND contours.
- `current_review/current-sizing.md`: current sizing assumptions, calculations and primary sources.
- `pre-merge-main/`: exact main source backup. `baseline/`: starting candidate with moved USB1 and stale routing. Workers/merged are isolated review files, not the main project to edit next.

Current screen assumes35µm outer copper: provisional average stress~473mA; simultaneous planning peak~662mA. New traces pass conservative thermal/drop screening, but this does not close upstream USB500mA compliance. Firmware power sequencing/brightness, actual current waveforms, fuse temperature and regulator/OLED/dongle loading need hardware tests. Inherited USB pair asymmetry/impedance remains deferred; connector mating/enclosure fit, factory stackup and assembly checks remain. No manufacturing outputs, firmware, commit or push made in this task.

A one-run1:15AM Perth resume automation was created as a usage-limit fallback. It checks whether this work is already complete and takes no further action if so.
