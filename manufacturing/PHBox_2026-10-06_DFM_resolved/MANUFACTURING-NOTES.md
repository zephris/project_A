# Required fabrication and assembly instructions

These instructions accompany the current PHBox Gerbers, drill files, BOM and CPL. They are requirements for the retained U1/U4 design, not confirmation that a manufacturing option has already been selected or accepted.

## Fabrication — U1 exposed pad

Apply **epoxy filling and copper capping (POFV)** to the nine Ø0.35 mm plated thermal holes underneath **U1 RP2350A exposed GND pad 61**, producing a flat solderable top surface. Retain the thermal holes, exposed copper and existing four rounded paste windows. Do not substitute solder-mask tenting, ordinary ink plugging, or extra solder paste.

These holes are encoded as footprint through-hole pads and exported as **ComponentDrill**, so automatic treatment of ordinary ViaDrill objects may omit them. Identify them using `reference/U1-hole-identification.csv` and `reference/U1-hole-map.png`. The current drill tool is T4C0.350, nine holes; T3C0.350 is a different set of ordinary vias. Coordinates and component identity take precedence over tool numbers if files are regenerated.

Gerber/drill-origin coordinates in mm: all nine combinations of X = −23.907320, −22.532320, −21.157320 and Y = 38.508442, 37.133442, 35.758442. Excellon rounds to 0.001 mm.

Obtain explicit CAM confirmation that these nine ComponentDrill holes receive filling and copper capping. Preserve functional component through-holes and plated slots elsewhere. Confirm the quoted four-layer fabrication and assembly service combination and review production files before release. If this process is unavailable, return the design for review rather than manufacturing the open-hole variant.

## Stencil and assembly — U4

For **U4 ECMF2-40A100N6**, use ST DS13913 Rev 4 Figure 32: six **0.664 × 0.190 mm** paste apertures, centred on the existing copper-pad centres in local footprint coordinates, with a **100 µm stencil**. This requires an anisotropic reduction from the 0.700 × 0.200 mm copper lands. Account for the footprint's native KiCad 90° rotation when generating the stencil.

The supplied paste Gerber now includes these six exact U4 apertures, implemented as separate paste-only pads in the board and project footprint. Supply/confirm the final stencil artwork and the 100 µm stencil plan. A global stencil thickness change is not approved for all other components by this note; review the complete stencil with the assembler.

Preserve accepted CPL U1=0°, U4=0°, USB2=180°, U8=90°. Orient U4 using the manufacturer pin-1 mark, not text orientation. Review U1's hidden exposed-pad solder joint with appropriate X-ray inspection for solder starvation, bridging and voiding, and confirm the inspection plan for the actual order.

## DFM disposition and remaining review items

### Annular rings — separate via and component-hole requirements

Retain the current annular-ring copper geometry. The board has four copper layers and nominal 35 µm outer copper (1 oz). All 296 ordinary vias have nominal radial rings of at least 0.075 mm, meeting JLCPCB's preferred via diameter-minus-hole difference of 0.15 mm (minimum 0.10 mm). Actual component insertion holes have rings of at least 0.20 mm: USB1 plated slots 0.20 mm, U5 header 0.40 mm, and OPSW1–6 0.45 mm. They meet the multilayer 1 oz component-PTH recommendation of 0.20 mm (absolute minimum 0.15 mm).

JLCDFM's generic annular-ring flags must be reviewed by hole class; do not lower the component-PTH rule globally or enlarge every via to satisfy it. Its displayed results are capped, so individual server flags have not all been mapped to native coordinates. The complete native inventory and representative flagged via sizes support this disposition; see `validation/annular-ring-review.md` and `validation/annular-ring-native-audit.json`.

U1's nine 0.60 mm land / 0.35 mm drill thermal holes have 0.125 mm nominal radial rings. Treat them as thermal via-in-pad holes despite their ComponentDrill export, and apply the filling/capping instructions above. Obtain CAM confirmation of the annular-ring disposition and exact U1 hole treatment before fabrication. Reassess these limits if ordering 2 oz outer copper or changing the fabrication process. These nominal measurements do not certify finished rings after production tolerances.

Sources: [JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities), [JLCPCB POFV requirements](https://jlcpcb.com/news/free-via-in-pad-6-20-layer-pcbs-pofv).

U1/U4 rounded 0.00 mm lateral entries do not justify part translation or copper enlargement. Manufacturer land dimensions match the current copper. U4's four tiny negative model margins are reproduced; the precise server count split for U1 remains unverified. Retained drilled artwork may still trigger U1 hole checks even after a POFV order instruction, so record the accepted manufacturing disposition rather than claiming the Gerber checker understands the process.

The no-via-in-pad candidate from the investigation is **not adopted**: it changes direct plane-ground and thermal paths. The incorrect QFN-56 visual model is replaced locally by the project-local RP2350A model from Raspberry Pi's official R4-S1 reference design; this model-only correction does not alter the manufacturing copper, drill, stencil or placement files.

F1 uses its corrected manufacturer land pattern. Its remaining lateral margins of approximately -0.0000112 mm are numerical model precision. D21's generic model has 0.900024 mm-wide terminals, exceeding ST's 0.85 mm package maximum; the board's ST-recommended lands are retained. Review D21 against the actual manufacturer's package rather than enlarging copper to match this model.

The isolated 0 mm PCB pad-spacing entry is now correlated to two tangent 0.60 mm ordinary via lands on +1V1 at board coordinates (144.832180, 52.716558) and (144.832180, 52.116558). Their 0.30 mm drill-edge spacing meets the 0.20 mm via-hole requirement. This same-net copper union is intentional.

Production silk is clearance-clipped around exposed solder-mask openings and via lands by an additional 0.160 mm. Retain the restored source artwork and silk over mask-covered traces. Use the supplied production silk Gerbers; direct ordinary re-export from the source does not reproduce this manufacturing clipping. Confirm final legend artwork and legibility during production-file review.

See `validation/findings-disposition.md` and the fresh rerun for the complete classification. These instructions do not establish CAM acceptance or authorize an order. Use the separate BOM matching page and visually inspect USB2 orientation before SMT analysis.

Sources: [U1/U4 investigation](reference/U1-U4-investigation.md), [JLCPCB via filling/capping](https://jlcpcb.com/help/article/pcb-via-covering), [ST ECMF2 datasheet](https://www.st.com/resource/en/datasheet/ecmf2-40a100n6.pdf), [Raspberry Pi official reference files](https://pip.raspberrypi.com/documents/RP-010328-CA).
