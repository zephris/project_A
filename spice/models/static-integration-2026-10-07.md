# Static model integration

The generator now includes Samsung 4.7uF, 1uF and the selected C41 candidate in dedicated small-signal impedance benches, alongside the existing 100nF comparison. The exact KEMET C19/C43 export is integrated as two parallel subcircuits in a separate bank impedance bench. These files are copied into generated KiCad projects, and their hashes are checked by the batch runner. Manufacturer originals are preserved.

Samsung files describe 0V DC bias and 25C. They are integrated for those conditions, not substituted into energized-rail startup/load-step tests. KEMET describes 5V/25C with a 100kHz fitting center; broadband transient substitution remains unqualified. No encrypted interactive models are used.

All 14 nominal benches executed in KiCad's ngspice46 DLL with every requested measurement present. Source/model checks passed. Execution success is not hardware qualification.

| New bench | Impedance at 100kHz | Impedance at 1MHz |
|---|---:|---:|
| Samsung 4.7uF | 0.545171 ohm | 0.0541563 ohm |
| Samsung 1uF 0402 | 2.01408 ohm | 0.205716 ohm |
| C41 candidate 1uF 0603 | 2.03737 ohm | 0.207877 ohm |
| KEMET C19+C43 bank | 0.0139134 ohm | Not requested outside center-frequency qualification |

Real vendor capacitor networks differ from ideal nominal capacitors even at zero DC bias because capacitance/impedance depends on frequency. These results do not establish capacitance at 3.3V. The KEMET bank result improves the previous estimated ESR comparison but does not qualify the complete switched rail.

## C41 selection

Schematic: 1u/10V/X7R across +3V3 and GND at the display supply. PCB: Capacitor_SMD:C_0603_1608Metric. Selected candidate: Samsung CL10B105KA8NNNC, JLCPCB C29936, 1uF, 25V, X7R, +/-10%, 0603. Higher voltage rating satisfies the original 10V requirement; package and nominal capacitance match. No routing or footprint change is needed. Its Samsung base-part static model CL10B105KA8NNN was extracted from the previously downloaded manufacturer archive, retaining original bytes. Ordering suffix equivalence and capacitance at actual bias remain qualification items.

JLCPCB lists it for Economic/Standard SMT assembly as an Extended part. The retrieved listing showed stock, but quantity must be rechecked at ordering: https://jlcpcb.com/partdetail/30690-CL10B105KA8NNNC/C29936 . This is a part selection, not a regenerated manufacturing release; schematic/PCB metadata and existing BOM packages remain unchanged.

## Remaining component search

Renewed exact-part/manufacturer searches did not find additional downloadable PSpice files for U1 RP2350, U3 internal flash behavior, U4 ECMF2-40A100N6, U5 HS13L03W2C01, SK6805-EC15 LEDs, F1 SMD0805-075-12V, L1 AOTA-B201610S3R3-101-T, or Fenghua 0402CG150J500NT. Y1 still only has a different-frequency ABM8-family example, not an exact 12MHz model. U3's downloaded IBIS remains available for IO electrical analysis. No family substitutes were labelled as exact models. Public search absence does not exclude private vendor models.

Sources and earlier coverage: conversion-and-coverage-2026-10-07.md and additional-downloads-2026-10-07.md. Model hashes, C41 selection and new measurements: static-integration-2026-10-07.json. Full execution report: ../results/static-integration-2026-10-07/report.json.

## Assembly selection update

C41 is subsequently assigned C29936 in source metadata and included in the current manufacturing BOM/CPL. The candidate status above records the original integration stage; the selected part is now assigned. No copper or simulation topology changed.
