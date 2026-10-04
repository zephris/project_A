# Fill/via cleanup and focused JLCPCB review — 2026-10-03

## Applied to the main PCB

- Removed 58 remote, untracked GND stitching vias. Retained every via with a nearby ground track, any pad within 3 mm, any non-GND layer-transition via within 3 mm, the perimeter fence, and the MCU/USB power-control clusters. The removed vias include all five illustrated in the user's screenshot. These distance criteria are a conservative layout screening rule, not a measured EMC result.
- Removed one empty +1V1 zone and one obsolete +1V1 zone superseded by the unified core-power pour.
- Consolidated 13 F.Cu +5V and B.Cu +3V3 zone definitions into their existing same-net background pours. Native refill/DRC proves the consolidated candidate remains connected. Front background fill went from 171 contour objects to 2; those earlier contours were not 171 electrically floating islands.
- Raised zones with 0.0254 mm minimum thickness to 0.10 mm (B.Cu zones already use 0.20 mm). This eliminates the two sliver warnings in the stricter clearance trial.
- Moved C40's GND via from (156.45,77.300618) to (156.45,76.55) mm, outside its solder pad, retaining the via UUID and adding two short 0.15 mm F.Cu GND fanout segments. No via centers now lie within SMD solder pads in the native geometry check.
- Strengthened the project hole-to-copper clearance from 0.15 to 0.20 mm and solder-mask-opening-to-other-net-copper clearance from 0 to 0.09 mm. Other project settings remain unchanged.

All 144 footprints/pad geometries/UUIDs/placements are unchanged. Signal routes and power tracks are unchanged. Only one remaining GND via moved; two GND fanout segments were added. There are 319 vias, including 205 GND vias, and 1771 total track/via objects. Both inner GND fills remain single continuous outlines; area is 44788.0646 mm² each after the increased clearance/refill.

## Why power pours remain

The temporary no-background trial broke two LED bypass +5V connections (C20/C35) and three MCU +3V3 network links, plus produced dangling power items. That trial was rejected. The broad pours have functional power connections and are not removable filler. A future conversion of unused area to GND must preserve or reroute those supply links and verify return geometry; do not change the power-pour net label in place.

## Solder mask and exposed +5V

The board contains no non-pad mask graphics or mask zones opening large copper areas. Front/back global via tenting is enabled. The red copper display is not a representation of bare finished copper. Broad +5V copper is covered by solder mask; normal component solder lands remain exposed. Solder mask does not replace mechanical insulation/clearance from the metal enclosure.

For new routing, use localized power distribution and grounded unused-area copper where practical, with suitable stitching; retain the two dedicated inner GND planes. Large power pours are not inherently a manufacturing fault. This is a layout preference and must be evaluated against actual PDN/return paths.

## Focused JLCPCB checks

Profile: four-layer FR-4, 1 oz outer copper, routed board edge, standard tented vias, and a mask color supporting 0.10 mm webs (green/red/yellow/blue/purple). Black/white requires 0.13 mm webs per the current capability table; this report does not approve that different option.

| Item | Board / rule | JLCPCB guide |
|---|---|---|
| Minimum track width | 0.15 mm measured | 0.09 mm multilayer, 1 oz |
| Minimum copper clearance | 0.10 mm rule; zones 0.15/0.1524 mm | 0.09 mm multilayer trace spacing; separate pad rules apply |
| Vias | ≥0.45045 mm diameter, 0.30–0.35 mm drill | Diameter should exceed drill by 0.10 mm, preferably 0.15 mm; preferred minimum drill 0.20 mm |
| Via annulus | ≥0.075075 mm measured | Meets preferred 0.15 mm diameter increase; do not confuse via rule with component PTH annular-ring rules |
| Via tenting | Both sides enabled | Ideally ≤0.40 mm holes; not guaranteed for large holes >0.50 mm |
| Copper to routed edge | ≥0.30 mm enforced and native DRC passes | ≥0.20 mm; V-cut has a different ≥0.40 mm rule |
| Hole-to-copper | ≥0.20 mm strengthened rule | Inner via-hole-to-copper and via-hole-to-track minimum 0.20 mm; component PTH rules are distinct |
| Mask openings to neighbor traces | ≥0.09 mm strengthened rule | ≥0.09 mm |
| Mask web | 0.10 mm | 0.10 mm with listed mask colors; black/white 0.13 mm |
| Via-in-SMD-pad centers | None after C40 repair | Filled/capped process is required for conventional via-in-pad assembly; simple tenting is not plated-over via filling |
| Copper balance | Broad solid outer power fills retained; both inner GND planes continuous | JLCPCB recommends copper in unused areas and avoiding highly unbalanced coverage |

## Sources

- [JLCPCB current capabilities](https://jlcpcb.com/capabilities/pcb-capabilities)
- [JLCPCB via-covering guidance](https://jlcpcb.com/help/article/pcb-via-covering)
- [JLCPCB copper pour basics](https://jlcpcb.com/blog/pcb-copper-pour-basics)
- [JLCPCB solder mask guide](https://jlcpcb.com/blog/basic-design-of-solder-mask)
- [KiCad 10 solder mask and zone documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html)

This is a focused copper/via/mask review, not a whole-board fabrication or EMC sign-off. Exact stackup/impedance, final Gerber/assembly preview and mechanical/hardware release gates remain. Manufacturing and firmware outputs were not regenerated.

## Evidence and recovery

`before/` contains the exact pre-cleanup PCB/project/schematic/rules. `inventory.json`, `trial-removals.json`, `consolidation-removals.json`, `audit.json` and `dfm-measurements.json` record changes. Rejected background-removal and stricter-rule trials are preserved separately. `consolidation-drc.json` and `main-drc.json` report zero violations, unconnected items and schematic parity errors on their exact revisions. Fresh main ERC/netlist checks are recorded alongside them.
