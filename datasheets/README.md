# PHBox RGB LED datasheet cache

Downloaded 2026-09-25 for comparison of the candidate LED and the part named by the former PCB footprint. The OPSCO PDF is the design reference for schematic LEDs D1–D20 and the project PCB footprint; confirm that the purchased `SK6805-EC15` is the `-001` variant documented here.

| Cached PDF | Document identity | Source | SHA-256 |
|---|---|---|---|
| `OPSCO_SK6805-EC15-001_C2890035.pdf` | OPSCO SK6805-EC15-001, Rev A/1, dated 2025-08-07; linked by LCSC C2890035, which lists MPN SK6805-EC15 | https://datasheet.lcsc.com/datasheet/pdf/0f4b58ac8908ccf8037b2d7ca0ec1e91.pdf?productCode=C2890035 | `7862e1b38734e98826262766ff7b654292008c626bc265c91798eabcd447df0f` |
| `Newstar_EC15_SK6812.pdf` | Newstar EC15, Rev 02, dated 2018-09-18; manufacturer-authored document mirrored by Datasheet4U | https://datasheet4u.com/pdf/1313775/EC15.pdf | `66dc63d9f50667548e5edd46bea4ba234cb3b60c5637b8106ce58da3026aa4cf` |

The KiCad `LED_SK6812_EC15_1.5x1.5mm` footprint points to `http://www.newstar-ledstrip.com/product/20181119172602110.pdf`, which returned HTTP 404 on 2026-09-25. The cached Newstar PDF is a mirror of a manufacturer-authored EC15 sheet; its document identifies the model as `EC 15`, not a uniquely orderable `SK6812-EC15` manufacturer part number.

For the two design review items: the OPSCO candidate and Newstar EC15 agree on pins 1 DIN, 2 VDD, 3 DOUT, 4 GND and 1.5×1.5×0.65 mm body size. OPSCO's recommended land drawing shows 0.55×0.55 mm pads with 0.40 mm gaps; Newstar's shows 0.60×0.50 mm pads with 0.40 mm gaps. The former embedded PCB footprint had 0.50×0.50 mm pads on 0.90 mm horizontal and vertical pitch. The PCB's 20 LED footprints now use the OPSCO land drawing and orientation, but the exact supplied variant and assembly-process suitability still need confirmation.

| Electrical item | OPSCO SK6805-EC15-001 | Newstar EC15 Rev 02 |
|---|---|---|
| Supply range in sheet | 3.7–5.5 V | 3.5–5.5 V, in an “absolute maximum ratings” table; do not treat this as a recommended range |
| DIN high threshold at 5 V | ≥0.78×VDD = 3.9 V | ≥0.7×VDD = 3.5 V |
| Color byte order | GRB | GRB |
| Reset low interval | ≥200 µs | >80 µs |
| Idle current | 0.5 mA typical | 1 mA typical |
| RGB channel current | 5 mA typical, 6.3 mA listed maximum per channel | Not specified in this sheet; `0.1 Watt` appears in its cover description but does not establish a current limit |

Use the OPSCO sheet, not the Newstar figures, to design around C2890035. In particular, a 3.3 V MCU output falls below both stated 5 V DIN thresholds, and the two parts have different reset requirements. The comparison does not establish interchangeable parts or a production-approved footprint.
