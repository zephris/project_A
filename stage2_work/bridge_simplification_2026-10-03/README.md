# Bridge simplification — 2026-10-03

Reviewed 30 isolated outer-layer via-to-via track chains, including longer detours. Tested same-geometry layer consolidation on a separate candidate with matching project/rules and native zone refill/DRC. Conflicting neighboring chains were resolved before the final trial. USB data routing retained.

Merged eight successful sections into the root PCB, removing 16 signal vias. All track widths, net assignments, endpoint coordinates, and 144 footprint/pad geometries are preserved; only 16 existing track segments changed B.Cu to F.Cu. Both inner GND planes remain one filled outline each; their filled area increased from 44839.4045 to 44846.6328 mm² because removed signal vias no longer require clearance holes.

Recovery: `before.kicad_pcb` is the exact main-board backup immediately before the merge. `inventory.json`, `accepted.json`, `reasons.json`, trial reports, and `audit.json` record inspection and validation. Retained entries failed clearance or connectivity in the attempted consolidation, or conflicted with the better accepted consolidation of neighboring sections; this does not rule out future rerouting with different geometry.

| Net | Layer-hop length (mm) | Result |
|---|---:|---|
| UP2 | 7.337 | Retained: clearance, track_dangling, tracks_crossing, unconnected_items |
| Net-(D17-DIN) | 6.743 | Retained: track_dangling, unconnected_items |
| Net-(D13-DIN) | 1.482 | Retained: track_dangling, unconnected_items |
| UP3 | 7.354 | Retained: clearance, track_dangling, tracks_crossing, unconnected_items |
| SDA | 10.499 | Retained: track_dangling, tracks_crossing, unconnected_items |
| UP2 | 9.276 | Retained: clearance, track_dangling, tracks_crossing, unconnected_items |
| Net-(U4-D+_to_connector) | 3.505 | Retained: clearance, solder_mask_bridge |
| Net-(D17-DIN) | 88.866 | Retained: clearance, shorting_items, tracks_crossing |
| Net-(D17-DIN) | 1.236 | Simplified to F.Cu |
| Net-(D16-DIN) | 113.988 | Retained: clearance, tracks_crossing |
| Net-(D12-DOUT) | 8.582 | Simplified to F.Cu |
| Net-(D13-DIN) | 0.920 | Simplified to F.Cu |
| Net-(D13-DIN) | 1.460 | Simplified to F.Cu |
| SCL | 19.042 | Retained: tracks_crossing |
| UP3 | 9.398 | Retained: shorting_items, track_dangling, tracks_crossing, unconnected_items |
| RGB | 28.285 | Retained: tracks_crossing |
| /LED_BUFFER_Y | 5.402 | Retained: shorting_items, solder_mask_bridge, tracks_crossing |
| SDA | 1.388 | Retained: clearance, tracks_crossing |
| SDA | 18.956 | Retained: clearance, shorting_items, track_dangling, tracks_crossing, unconnected_items |
| Net-(D9-DIN) | 1.226 | Simplified to F.Cu |
| Net-(D9-DOUT) | 0.921 | Simplified to F.Cu |
| OPT2 | 5.837 | Retained: tracks_crossing |
| Net-(D1-DOUT) | 6.236 | Retained: clearance |
| OPT6 | 5.862 | Retained: tracks_crossing |
| OPT5 | 5.862 | Retained: tracks_crossing |
| OPT4 | 5.862 | Retained: tracks_crossing |
| OPT3 | 5.862 | Retained: tracks_crossing |
| /LED_DATA_IN | 6.991 | Retained: tracks_crossing |
| Net-(D5-DIN) | 10.442 | Simplified to F.Cu |
| Net-(D6-DIN) | 1.736 | Simplified to F.Cu |

Final main-project verification: native zone refill/DRC found 0 violations, 0 open items and 0 schematic parity findings. Fresh ERC found 0 violations. Fresh XML netlist matches all 432 fitted PCB pad entries. Main/candidate S-expressions are identical excluding regenerated filled polygons; both main inner GND planes remain one outline with the same area as the candidate. `main-verification.json` records the final main PCB hash. No manufacturing/firmware output was regenerated.
