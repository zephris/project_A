# Active USB2 SMD edge revision - 2026-10-05

Historical underside assessment. Superseded by the [8 October top-side revision](USB2-top-assessment-2026-10-08.md); retain the following as evidence for the earlier manufacturing package.

USB2 uses Jing 904-131A2032S10200 / JLCPCB C46400 on B.Cu at (192,47) mm, opening toward negative KiCad Y, to the right of USB-C in front-side coordinates. H12 and all twelve mounting holes remain.

Four signal contacts and both shield lands are SMT. Two plastic locating pegs use 1.3 mm NPTH holes. No recessed body cutout is required. Pin 1 USB_HOST_5V; pin 2 HD-; pin 3 HD+; pin 4 and shield GND. MCU pin mapping and enable circuitry remain unchanged. The PIO host supports full/low speed; this replacement does not add high speed or SuperSpeed.

JLCPCB snapshot: 57 units, extended assembly part on 2026-10-05. Recheck stock and placement preview when ordering. [Part](https://jlcpcb.com/partdetail/47404-904131A2032S10200/C46400). [OEM drawing](https://datasheet.lcsc.com/datasheet/pdf/b82f44b617887c4bf965ef8115e91ba5.pdf?productCode=C46400).

Approximate mating face: KiCad Y=32.5 mm, 2.016558 mm beyond board edge. Main shell nominal Z=-9.4..-3.7 relative to PCB front Z=0 and back Z=-1.6. STEP is a simplified OEM drawing-derived reference; small folds, registration and peg depth need assembled fit verification.

External component keepout: X=181.5..202.5, Y=-17.5..31.5 mm. Socket courtyard handles the interior body. U8 protection and C44 relocated with rebuilt routes; native USB-C connectivity unchanged.

Mayflash [MagicBoots PS4](https://www.mayflash.com/product/MAGPS4.html) and [Xbox One](https://www.mayflash.com/product/MAGONE.html) publish 15 x 15 x 8 mm. Centred 8 mm body assumption gives Z=-10.55..-2.55 and provisional flush bottom datum -10.55. Published dimensions do not establish plug/body centre alignment. PXN N5 dimensions remain unverified. Brook FGC2 is an external passthrough converter excluded from the underside bay. Physical fit does not establish firmware authentication compatibility.

KiCad 10.0.6 DRC: zero violations, unconnected items and schematic parity issues. ERC: zero violations. PCB SHA256: 5b784939d83dc5a2fc575b216f58ee85acac75a75ce2c42e9aacb26c66cb3db0. Native geometry: 146 footprints, 331 round PTH, 4 PTH slots, 116 round NPTH. XY and separate Z references regenerated.

JLCDFM/prototype review only: USB signal integrity, factory stack, assembly rotations and mechanical fit require first-article validation. Final lower carrier and feed ramp remain enclosure work. Guides must allow gasket movement and must not rigidly bypass the floating PCB suspension.
