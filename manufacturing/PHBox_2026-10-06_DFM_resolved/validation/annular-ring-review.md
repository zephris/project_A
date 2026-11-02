# Annular-ring investigation — 6 October 2026

No annular-ring copper enlargement is required by the published fabrication rules for the current nominal geometry. Confidence is high for native geometry and published rules, medium for attribution of every server flag because JLCDFM limits displayed results.

JLCDFM reports 69 Danger and 31 Warning entries, using a generic roughly 0.10/0.15 mm PTH annular-ring rule. The details explicitly warn that vias may be misidentified as through-hole component pads. The inspected layer says 125 results with only the first 50 displayed; the visible 0.07/0.08, 0.10 and 0.12 mm values match ordinary-via geometries. Its `r11.811` and `r17.7362` object labels correspond to approximately 0.300 and 0.45045 mm aperture diameters in mil, despite the r prefix. Do not interpret these as physical radii or assume the summary is an exhaustive hole census.

Native board audit of all 296 vias:

| Via land / drill mm | Nominal radial ring mm | Count |
|---|---:|---:|
| 0.450 / 0.300 | 0.075 | 4 |
| 0.45045 / 0.30030 | 0.075075 | 123 |
| 0.500 / 0.300 | 0.100 | 1 |
| 0.600 / 0.300 | 0.150 | 43 |
| 0.600 / 0.350 | 0.125 | 125 |

[JLCPCB current capabilities](https://jlcpcb.com/capabilities/pcb-capabilities) require via diameter at least 0.10 mm larger than drill, with 0.15 mm preferred. This is a diametral difference: nominal radial rings are 0.05 mm minimum and 0.075 mm preferred. Every ordinary via meets the preferred difference. Applying the generic 0.10/0.15 mm component-PTH rule to all these vias creates conservative/misclassified flags. Native nominal geometry is not a claim about finished copper after drilling and etching.

Actual component PTH copper rings: USB1 plated slots 0.20 mm minimum on both axes; U5 OLED header 0.40 mm; option switches OPSW1–6 0.45 mm. Drills are centred (zero offsets). These meet the published multilayer 1 oz PTH absolute minimum 0.15 mm and recommendation 0.20 mm. This assessment assumes the intended 1 oz fabrication; a different copper weight needs review.

U1's nine footprint-encoded thermal holes have 0.60 mm land / 0.35 mm drill, giving a nominal 0.125 mm ring. They are thermal via-in-pad objects, not component-lead insertion holes. [JLCPCB POFV requirements](https://jlcpcb.com/news/free-via-in-pad-6-20-layer-pcbs-pofv) specify 0.05 mm minimum / 0.075 mm preferred radial ring and 0.2–0.5 mm drill. They meet those ring/drill limits. Retain the exact-hole manufacturing note and require CAM acceptance of filled-and-capped treatment for the nine ComponentDrill objects. Do not blanket-waive them as ordinary PTHs or omit their solder-wicking concern.

No board changes or rule disabling were performed for this investigation. Enlarging the vias solely to clear the generic report would alter surrounding copper clearance unnecessarily. Engineering/CAM disposition of the rule interpretation is still required before fabrication.

Evidence: annular-ring-native-audit.json, annular-ring-details.txt, reference/annular-ring-review.png. Full server row-to-native-coordinate matching was not available due the display cap; the complete native hole inventory and representative server diameter/ring classes were checked.
