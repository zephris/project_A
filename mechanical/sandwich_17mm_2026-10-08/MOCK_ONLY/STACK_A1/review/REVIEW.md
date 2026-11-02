# Geometry, assembly and stacked-print review

Reviewed 23 October 2026. File checks only; no physical print or load qualification.

## Saved geometry and layout

- 105 source components: 24 quarter-panel sections and 81 smaller models, including 19 optional gauges/envelopes. Native files retain 105 named parts inside one assembly container. No meshes were fused or resized.
- Watertight input mesh: **True**; 105 bodies, 120,832 triangles. Millimetre scale confirmed by `dfam-facts.json`.
- Envelope: **[244.8, 243.7, 44.95] mm**; minimum overlapping-footprint separation **1.000 mm**. Source hashes and native positions checked; maximum native-position error 3.2e-06 mm.
- Every elevated part has positive PETG interface extrusion in its footprint directly below its first model layer. This checks support presence, not full-area contact coverage or release force. Process settings select PETG on both top and bottom interfaces.
- [Every print group](tier-contact-sheet.png), [stack heights](stack-heights.png) and [complete numbered file index](part-index.csv). Independent columns can have different start heights; T-numbers identify groups rather than separate build plates.
- Exact toolpath support volume: **228.9 cm³**, counting support, transition and interface extrusion, excluding purge/prime tower. Filament diameter is 1.75 mm. DfAM's prism volume is only an upper bound and is not the sliced support consumption.

## Placement optimization

Three panel columns share the A1 bed. Each rises independently, eliminating height imposed by the tallest member of a common tier. Same-quarter bottom/top spacers share XY and rotation so their perimeter walls overlap. Broad panels sit below open frames. Small parts use low side pockets. The prime tower has a reserved region. Separators are 1 mm instead of 2 mm; each has two 0.10 mm PETG contact layers at each model-facing surface, with sparse PLA scaffold between.

| Candidate | Total PLA + PETG incl. purge/tower | Estimated time | AMS changes |
|---|---:|---:|---:|
| Earlier two-column layout | 1181.3 g | 81.7 h | 226 |
| Three across, common tier heights | 1198.8 g | 81.7 h | 252 |
| Independent columns, matched spacers | 830.7 g | 55.6 h | 160 |

Combined layout and parameter reduction against the earlier PETG layout: **29.7% total filament and 32.0% time**. The final row includes the later profile tuning described in [TUNING.md](TUNING.md); it is not solely a placement comparison. This is the best of the sliced candidates, not proof of a global minimum. The single stacked job remains slower and uses more material than printing parts separately.

## Assembly checks

Nine current CAD checks completed with exit 0; outputs are preserved alongside `assembly-review.json`:

| Check | Result and scope |
|---|---|
| Main saved STEP assembly | No board, rigid-part, screw-head or hard-travel collisions in the modeled cases; board float ±0.50 mm XY / ±0.25 mm Z. |
| Option caps | 864 pair tests, no collisions; generic H5 actuator, assumed 0.35 mm actuation. Actual switch part remains unspecified. |
| USB surround integration | Floors, sidewalls, retaining lips and roof material present. USB-A roof belongs to acrylic; USB-C roof belongs to spacer. |
| USB seals | Nine board-edge poses checked without rigid board overlap. Outer 0.2 mm interference is intentional for real TPU. |
| Port roofs | USB-A roof 2 mm; upward-travel shell clearance 0.75 mm. USB-C front roof clearance 0.20 mm in tested pose. |
| Plug/finger access | 1,116 rigid-pair tests without collisions for stated gauges. Dongle assumes 2 mm body setback; the zero-setback control collides with the acrylic roof. |
| Cut profiles | Seven DXFs in mm, zero audit errors. |
| Collar meshes | Both valid single solids; thin membrane and TPU compliance require a trial. |
| Corrected mating sources | No overlaps at switch plate/heatsink, switch plate/top spacer, screen frame/actual module, internal mount pieces or countersunk case head. |

The production layer order remains top acrylic → upper spacer/internal parts → PCB → foam → lower spacer → bottom acrylic, nominal 17 mm excluding keycaps. Reconstruct quartered pieces using the original `../manifest.json` coordinate bounds, on a flat jig. Seams have no joining pins; temporary rear-face tape cannot reproduce full-panel stiffness.

**Open fitment concerns:** heatsink rear retainers are 2 mm thick and omit threads in the mock. M2/M3 ×10 screws have about 0.85 mm engagement, while ×12 protrude about 0.85 mm; fastening needs the real-hardware trial or the documented retainer redesign. The PCB mock omits most real parts/solder; OLED glass/header and actual dongle overmold geometry are not qualified. Rigid PLA collars/foam/pad gauges test shape only. No structural, thermal or seal rating is implied.

## Conservative FDM feature review

Compared to the CAD plugin's [FDM process-limit table](FDM-process-limits.md): 1.2 mm supported wall / 1.6 mm unsupported wall, 45° self-support angle. `wall-thickness-by-part.json` maps measured bodies to their actual named part, matched by bounds.

**41 bodies fall below the conservative 1.2 mm supported-wall guide at p05**, including deliberately thin washers, gauges, screen frame or cap features. 5 additional bodies have a sampled minimum below 1.2 mm but p05 above it. These are not blanket printability passes. Representative part measurements follow (min / p05 mm):

- `option_retainer_M2_nut_envelope_2_SURROGATE.stl`: 1.002 / 1.034.
- `rear_insulating_washer_H12.stl`: 0.500 / 0.500.
- `insulating_support_washer_H12.stl`: 0.500 / 0.500.
- `custom_POM_stop_H12.stl`: 0.500 / 1.149.
- `printed_screen_stop_4_3mm.stl`: 0.250 / 0.250.
- `acrylic_case_washer_8_top_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_8_bottom_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_7_top_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_7_bottom_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_6_top_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_6_bottom_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_5_top_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_5_bottom_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_4_top_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_4_bottom_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_3_top_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_3_bottom_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_2_top_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_2_bottom_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `acrylic_case_washer_1_top_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `OPSW6_captive_cap_H5_trial.stl`: 0.600 / 0.600.
- `OPSW5_captive_cap_H5_trial.stl`: 0.600 / 0.600.
- `OPSW4_captive_cap_H5_trial.stl`: 0.600 / 0.600.
- `OPSW3_captive_cap_H5_trial.stl`: 0.600 / 0.600.
- `OPSW2_captive_cap_H5_trial.stl`: 0.600 / 0.600.
- `pad_9_1_INSTALLED_HEIGHT_GAUGE.stl`: 0.450 / 0.450.
- `option_retainer_M2_nut_envelope_1_SURROGATE.stl`: 1.002 / 1.018.
- `printed_screen_stop_3_3mm.stl`: 0.250 / 0.250.
- `printed_screen_stop_2_3mm.stl`: 0.250 / 0.250.
- `printed_screen_stop_1_3mm.stl`: 0.250 / 0.250.
- `OPSW1_captive_cap_H5_trial.stl`: 0.600 / 0.600.
- `rear_insulating_washer_H7.stl`: 0.500 / 0.500.
- `rear_insulating_washer_H5.stl`: 0.500 / 0.500.
- `insulating_support_washer_H7.stl`: 0.500 / 0.500.
- `insulating_support_washer_H5.stl`: 0.500 / 0.500.
- `option_retainer.stl`: 1.000 / 1.000.
- `pad_8_1_INSTALLED_HEIGHT_GAUGE.stl`: 0.450 / 0.450.
- `acrylic_case_washer_1_bottom_0p5_SURROGATE.stl`: 0.500 / 0.500.
- `USB_A_collar.stl`: 0.316 / 0.316.
- `USB_C_collar.stl`: 0.316 / 0.316.
- `screen_frame.stl`: 1.000 / 1.000.

For a generic robust FDM part, thicken a supported wall to at least 1.2 mm (1.6 mm if unsupported). Applying that to a 0.50 mm washer or exact mounting interface would change the fitment test, so the dimensions were preserved. Use the existing individual fine-nozzle files when thin details fail the 0.4 mm trial; treat them as geometry gauges rather than functional hardware. Small-hole diameters, minimum positive feature and bridge span are not exhaustively measured by this tool.

The axis-orientation study offers much less down-facing area on edge but raises build height to about 245 mm and puts broad panels on narrow edges. That changes the requested horizontal stack, reduces bed anchoring and risks panel accuracy; retain the horizontal layout. Support angle findings are addressed with generated supports, not by calling those overhangs self-supporting.

## Online techniques and limits

- [Prusa support guide](https://help.prusa3d.com/article/support-material_1698): denser interfaces support surfaces while sparse backing limits material; supports need permission to start on earlier parts in a vertical stack. Normal supports were chosen for stable stacked structures.
- [Bambu Studio configuration source](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp): explicit support/interface filament assignments and flushing matrix. Here PETG is only the release interface; PLA forms the support scaffold. All model parts remain PLA. Purging into objects, infill or support is disabled, with 800 mm³ flush each direction and a prime tower. This is a conservative starting value requiring filament-specific confirmation, not a manufacturer-guaranteed setting.
- [Bambu Studio issue #11540](https://github.com/bambulab/BambuStudio/issues/11540): installed 2.7.1.62 has a reported zero-gap interface/bridge classification issue for the inverse material pairing. This slice also uses Bridge features on supported first layers. Dimensional surface quality therefore still needs the supplied separation trial; software success alone does not clear it. No automatic application update was installed.
- The final independent file inspection receipt for A1 / 0.4 mm / textured PEI / PLA + PETG is in `file-inspection.json`. Tuned print temperatures are PLA 220 °C / PETG 245 °C, with a 245 °C material-change flush; the maximum nozzle command in the inspected file is 245 °C. Bed temperature is 65 °C. The receipt does not establish physical printer readiness or authorize dispatch.
- PLA/PETG contact is deliberately weak. Dense PETG with zero nominal top/bottom contact gap is a trial choice for release and lower-face finish. PETG dryness, the actual spool profiles and purge sufficiency determine success. Use gentle top-down removal and keep each thin model supported while peeling. Do not assume PETG is water soluble.
