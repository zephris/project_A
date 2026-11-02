# USB2 top-side revision — 8 October 2026

USB2, Jing 904-131A2032S10200 / C46400, is now on **F.Cu** at the unchanged PCB position **(192,47) mm**, orientation **180°**. The opening still points toward negative KiCad Y, beside USB-C at the board edge. This replaces the earlier underside arrangement; it is not a new part or a firmware pin-map change.

## Routing and electrical checks

The footprint was flipped left/right, not top/bottom, so the opening stays outward. The mirrored contact positions are:

| Contact | Net | PCB X,Y mm |
|---|---|---|
| 1 | USB_HOST_5V | 195.5,47 |
| 2 | HD- | 193,47 |
| 3 | HD+ | 191,47 |
| 4 | GND | 188.5,47 |
| 5, shell | GND | 199.5,44.3 and 184.5,44.3 |

The connector keeps both Ø1.3 locating holes in their original physical locations (the pair is symmetrical). There is no new body recess, board-outline change or mounting-hole change.

Only the local connector fan-out changed. Native UUID/geometry comparison found **145 other footprints unchanged**, **1,891 retained routing items unchanged**, **12 removed local track segments plus one replaced HD+ via**, and **19 new track segments plus five vias**. Added vias are nominal Ø0.6 / drill Ø0.3, outside the SMT lands; no new via-in-pad process requirement is introduced. U8 ESD protection, C44, the MCU, enable/fault signals and the remainder of the USB-host circuit stay in place.

HD- rejoins its existing back-side route. HD+ uses a short In1.Cu crossing and rejoins its existing In1.Cu route; its former dangling transition via is removed. VBUS uses a short In2.Cu link to the existing local VBUS via. Ground stitching connects the signal return and both shell lands. The local layer crossing accommodates the reversed pin order without moving unrelated option-button routes. The short VBUS link is offset from the new HD+ crossing rather than routed beneath it.

Summed routed segment changes: HD- **+0.566 mm**, HD+ **+2.408 mm**, VBUS **−1.631 mm**, GND **+7.100 mm**. These are copper-length deltas, not unique differential-path lengths. This is a minimal local routing revision, not a claim of impedance tuning, exact length matching, signal-integrity simulation or factory approval. Quilter was not needed for this candidate.

Native KiCad 10 DRC after zone refill: **zero errors, zero unconnected items and zero schematic-parity findings**. Two silk-clearance warnings at R2/C4 and R2/R3 remain, with the same finding UUIDs as the baseline. The sixteen intentional switch/LED courtyard exceptions remain the original project rules; no DRC rules were loosened for USB2.

Evidence and reproducible scripts: [candidate audit](../stage2_work/usb_a_top_2026-10-08/audit.json), [candidate DRC](../stage2_work/usb_a_top_2026-10-08/drc.json), [baseline DRC](../stage2_work/usb_a_top_2026-10-08/baseline-drc.json), [routing delta](../stage2_work/usb_a_top_2026-10-08/routing-delta.json). The original PCB is retained as `stage2_work/usb_a_top_2026-10-08/before.kicad_pcb`. Current source SHA-256: `3f6aadb20eb35b7df2a3d103c082da9fad3d124a0a84a652d2cac04c88c36e6a`.

## Mechanical integration

The top-side arrangement places USB-A and the MCU/flash heatsink on the same side of the PCB. The regenerated native board STEP is [Flatbox-rev8-pcb.step](../Flatbox-rev8-pcb.step); the current [heatsink project](heatsink_2026-10-08/README.md) uses the same regenerated board in its fitted, mounted and exploded assemblies.

The heatsink metal, pad interfaces and insulating supports are unchanged. The outer covers remain the earlier **26 mm envelope references**: this revision does not yet create the target 15 mm enclosure. The exported OLED has long pin tails; lower-profile rear hardware, pin trimming, cover thickness and gasket travel still control the next height reduction. The next enclosure must move the dongle bay/ramp to the upper edge and provide port clearance through the gasket travel range. The historical underside ramp/bay is superseded.

Saved native geometry checks put the USB shell at **Z=2.1..7.8 mm**, the remaining lowest board feature at **−4.5 mm**, and the shell-to-lowest-feature span at **12.3 mm**. The modeled USB geometry has **3.712 mm minimum separation** from the heatsink. All four modeled contacts match the front SMT pads and the outward shell opening passed a void-volume probe. The fitted/mounted assemblies have no nominal board/heatsink/support collision hits. See [USB registration and height check](heatsink_2026-10-08/usb-top-check.json), [heatsink fit checks](heatsink_2026-10-08/fit-check.json) and [mounting checks](heatsink_2026-10-08/mounting-check.json).

The fitted, mounted and exploded saved STEP snapshots were reviewed. These checks exclude an inserted dongle, fastener-head envelopes and loaded gasket travel. The temporary upper bezel is only 0.2 mm above the USB shell at its overlapping edge region; its final port opening must allow assembly tolerances, motion and the dongle body rather than using that nominal gap as design clearance.

The previous manufacturing ZIP, Gerbers and CPL represent **bottom-side USB2**. They are retained as the prior revision and must be regenerated, with the top-side connector orientation visually checked, before ordering this revised board. The existing quote selections do not update themselves when the PCB changes.

No firmware mapping change is required by this placement change because the nets and MCU assignments are unchanged. Firmware operation, real dongle fit, gasket-loaded clearance and USB signal integrity still require hardware validation.
