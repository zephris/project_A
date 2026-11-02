# Final JLCDFM verification

Completed PCB and SMT analysis for [candidate 630408027919675394](https://jlcdfm.com/viewer?pcbUploadFileId=630408027919675394). BOM matched on the separate matching site: all 35 groups confirmed. Models generated and saved before SMT analysis. USB2 was visually inspected on the bottom side: mating opening faces outside the board edge, four signal leads face the board interior and align with their lands. Accepted CPL is unchanged.

## Confirmed fixes

Production silk-to-pad dangers fell from 66 to 0; silk-to-hole dangers fell from 57 to 0. Final measured clearance is 0.160 mm. Remaining 62 pad-proximity and 16 hole-proximity warnings are below the viewer recommendation but above JLCPCB's published 0.15 mm minimum. Original KiCad artwork remains restored; use the supplied clipped production silk.

U4 now has six exact ST-recommended 0.664 x 0.190 mm paste-only apertures in the source board/library and paste Gerber. This stencil change is verified locally; the SMT geometry checker does not validate stencil aperture processing. Whole-board 100 micrometre stencil approval remains an assembler review.

## Remaining viewer findings

Counts are danger / warning / good. They are not a clean manufacturing release.

| Check | Final counts | Disposition |
|---|---|---|
| PCB pad spacing | 1 / 37 / 36 | Zero-distance pair is two tangent +1V1 via lands; drill gap 0.30 mm. No different-net short. |
| Annular ring | 69 / 31 / 0 | Generic classification differs from via/PTH requirements. Native inventory meets the respective published geometry requirements; obtain CAM disposition. |
| Slot width | 4 / 0 / 0 | OEM USB1 0.60 mm slots meet multilayer capability; viewer uses 0.6096 mm. |
| SMT lead to hole | 9 / 0 / 0 | U1 thermal holes require epoxy filling and copper capping, explicitly including the mapped ComponentDrill holes. Not yet accepted or purchased. |
| SMT pin inner edge | 1 / 0 / 0 | D21 model rounding. |
| SMT pin left / right edge | 36 / 0 / 0 each | D21 oversized generic terminals and sub-micrometre U1/U4/F1 model differences; retain manufacturer land patterns. |
| SMT lead coverage | 0 / 2 / 0 | D21 server model terminal width exceeds ST maximum. Actual-package CAM review required. |
| Component collision | 0 / 0 / 1 | No collision danger. |
| Component spacing | 0 / 0 / 57 | No spacing danger. |
| Component clipped by outline | 0 / 2 / 0 | Intended USB connector mating projection beyond edge. |
| Missing pads / missing pin holes / outer pin edges | 0 / 0 / 0 | No failures. |

See findings-disposition.md for dimensions and source links. Saved final raw snapshots: pcb-dfm-rerun.txt, silk-pad-final-details.txt, smt-dfm-rerun.txt. Screenshots under reference include PCB result, SMT result and USB2 close-up.

Local invariants confirm unchanged component origins/angles, copper pads/nets/drills, tracks and vendor CPL. Native DRC has no copper/connectivity/parity failures, with 70 library-validation notices and two source silk-overlap warnings. This focused DFM review does not constitute full electrical, firmware or hardware qualification.

Before ordering, JLCPCB must confirm the exact nine U1 holes receive epoxy filling and copper capping; ordinary via finish selection may exclude ComponentDrill holes. Capping prevents solder wicking but does not enlarge annular rings or remove drill-based DFM flags. Final stencil, actual-package model discrepancies and legend fragments remain CAM review notes.
