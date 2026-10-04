# Accepted local LX, USB and C42 changes — 2026-10-04

Merged into root Flatbox-rev8.kicad_pcb and .kicad_sch after the user confirmed both editors saved/closed. Root remains the accepted source; early trial boards/reports in this directory are rejected checkpoints, not release files. `pre-edit/` is the recovery checkpoint.

## Accepted changes

- Added named RP2350_LX_copper_cutout rule areas on In1.Cu, In2.Cu and B.Cu. Their small stepped outline covers the LX-side inductor pad and LX corridor, not the neighboring PGND return or the entire regulator. It excludes tracks, vias and zone fills without removing the existing top-layer LX copper/power loop. Native filled-copper queries at L1's LX pad (147.03218,50.816558) changed from GND present to absent on both inner layers. Each inner plane remains one connected filled contour.
- Moved existing C42 on B.Cu from (210,70.5) to (216.6,69.4), rotation 180°. Its +5V pad is now 1.688 mm from U7 IN rather than 6.98 mm. Removed its two old back-side fanouts and the dedicated front-side supply stub/via; added a short IN branch and local ground via. U7 and surrounding power/control routing were not moved or rerouted.
- USB1 keeps its connector, filter, TVS, CC components and protected MCU pair in place. Replaced two local connector-side D− front tracks with a back-side section and two 0.45 mm/0.30 mm vias, eliminating the prior two-via-versus-zero-via imbalance. The original D+ path and reversible connector fanout are unchanged. Existing nearby ground transitions remain. This is a limited full-speed layout improvement, **not** validation of 90 Ω impedance or a claim of ideal pair coupling everywhere.
- Added U8, ST USBLC6-2SC6 (JLCPCB C7519), on B.Cu at (221.1,62.4), with standard Package_TO_SOT_SMD:SOT-23-6 footprint. Pins 1/6 are HD+, 3/4 HD−, 2 GND, 5 USB_HOST_5V. Both channels have actual continuous flow-through PCB copper connecting their two pads; continuity does not depend on the analyzer understanding internal IC connections. Only the connector-side host fanout was replaced; the long host pair and R5/R7 remain unchanged.
- Added C44, 100 nF/16 V X7R Samsung CL05B104KO5NNNC (C1525), on F.Cu opposite U8 at (221.4,61.4), rotation 180°. Short dedicated ground and switched-VBUS vias connect it to U8. Its supply comes from the existing switched output bank, never upstream +5V. This small bypass does not change U7's ILIM, GPIO controls or bulk-capacitor architecture.

## Verification and object scope

Fresh exact-main `main-erc.json` and `main-drc.json`: ERC 0, DRC 0, unconnected 0, schematic parity 0. No rule was disabled or weakened. 146 footprints / 440 numbered PCB pad entries are synchronized. Independent XML-to-pad checks and UUID/physical geometry comparisons are in audit.json. Only existing footprint C42 moved; U8/C44 are the two additions. 18 old copper objects removed, 34 added, **every surviving track/via unchanged**; total 1790→1806. The USB group merely dropped deleted member UUIDs.

Zone refill is included in the accepted board. Both inner planes remain single connected contours; all 29 front and 22 back ground contours have actual plated anchors into both inner planes (`ground-anchors.json`). This does not establish measured EMI/ESD performance. Local bottom-layer layout was visually reviewed in the exported preview; fab-layer annotation overlap is not silkscreen overlap.

Candidates were generated with KiCad 10 pcbnew, then loaded/refilled/checked by KiCad CLI. A quote-aware balanced-form merge applied only changed objects and filled zones, preserving unrelated main forms/UUIDs. Project .pro/.dru and existing libraries were unchanged. Helpers here regenerate **candidates only**; merge_patch.py rejects a main source that differs from its pre-edit checkpoint and must not be rerun blindly after this merge.

## Sources and remaining gates

ST [USBLC6-2 datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), DS4260 Rev 7, confirms the SC6 pinout, SOT-23-6 package, low line capacitance and 100 nF VBUS bypass guidance. [JLCPCB C7519](https://jlcpcb.com/partdetail/STMicroelectronics-USBLC62SC6/C7519) supplied the sourcing identity; availability still needs rechecking before purchase. The PDF was inspected online, but direct download failed twice (HTTP/2 reset and HTTP/1.1 timeout); do not claim a local cached PDF exists.

Regulator cutout follows [RP2350 datasheet §6.3.8](https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf), while retaining the neighboring ground returns. U7 input bypass placement follows the [TPS2553 layout guidance](https://www.ti.com/lit/ds/symlink/tps2553.pdf).

Corrected two transcription errors in the earlier final-review table: RP2350A native USB D+ is pin 52 and D− pin 51; TPS2553 pin 4 is FAULT and pin 5 ILIM. The actual schematic/PCB mappings were already correct and were not changed.

Still required: factory stackup/impedance model or coupon, USB functional/eye/ESD tests, regulator startup/ripple checks, U7 inrush/FAULT behavior, real upstream/suspend-current and thermal measurements, enclosure/assembly clearance (including opposite-side C44/U8), and manufacturing/BOM/firmware release checks. No firmware image, manufacturing outputs, commit or push was produced.
