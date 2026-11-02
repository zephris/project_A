# Assembly materials: AliExpress sourcing

Supplier pages checked **9 October 2026**. Prices are AUD before freight; web stock is not a reservation. Use the exact hardware quantities in the [final assembly guide](../../README.md#parts-to-prepare).

**Current preference: source all small parts from AliExpress**, replacing the previous local-first plan. Use the exact specifications below. Search links are procurement routes, not verified seller selections: live prices, stock and Perth arrival estimates could not be checked. No purchases have been made.

Buy small exact-size packs with a few spares; compare delivered totals and postcode-specific delivery estimates. Consolidate with one seller where it reduces freight. Do not assume separate sellers ship together. Keep local acrylic cutting and aluminium machining as separate quote items.

## Primary small-parts procurement

| Part | Required variant / quantity | AliExpress search |
|---|---|---|
| Case columns | 8 × M3 female/female, 12 mm body, AF5; separate from heatsink posts | [12 mm M3 columns](https://www.aliexpress.com/w/wholesale-m3-female-female-standoff-12mm.html) |
| Case washers | 16 × OD7 / ID3.4 / thickness0.50 mm | [M3 0.5 mm washers](https://www.aliexpress.com/w/wholesale-m3-washer-0.5mm.html) |
| Case screws | 16 × M3×6, 90° countersunk | [M3×6 countersunk](https://www.aliexpress.com/w/wholesale-m3-6-countersunk-screw.html) |
| Switch-plate screws | 3 × M3×8 polymer; head ≤ Ø6×2.4 mm | [M3×8 nylon](https://www.aliexpress.com/w/wholesale-m3-8-nylon-screw.html) |
| Screen screws | 4 × M2×8 polymer; head ≤ Ø4×1.6 mm | [M2×8 nylon](https://www.aliexpress.com/w/wholesale-m2-8-nylon-screw.html) |
| Option retainer | 2 × M2×5 pan head ≤ Ø4×1.6 mm; 2 × M2 nuts AF4×1.6 mm | [M2×5 screws](https://www.aliexpress.com/w/wholesale-m2-5-pan-head-screw.html), [M2 nuts](https://www.aliexpress.com/w/wholesale-m2-hex-nut.html) |
| Heatsink hardware | Two M3 and one M2 polymer screw; installed length unresolved. 12 mm blanks only for trimming trials after retention geometry is settled. Nylon nuts require redesigned carriers. | [M3×12 nylon](https://www.aliexpress.com/w/wholesale-m3-12-nylon-screw.html), [M2×12 nylon](https://www.aliexpress.com/w/wholesale-m2-12-nylon-screw.html), [nylon nuts](https://www.aliexpress.com/w/wholesale-nylon-m2-m3-nut.html) |
| Thermal pad | Soft electrically insulating silicone gap pad, 0.5 mm; cut U1 5.5×5.5 mm and U3 3.5×3.5 mm | [0.5 mm thermal pads](https://www.aliexpress.com/w/wholesale-thermal-pad-0.5mm.html) |
| Foam | Seven lower pads from 2 mm cushioning foam; six upper from 1.5 mm; nonconductive | [2 mm EVA](https://www.aliexpress.com/w/wholesale-eva-foam-2mm.html), [1.5 mm foam](https://www.aliexpress.com/w/wholesale-foam-1.5mm.html) |

Verify seller drawings and delivered samples, including screw head dimensions. For pads require identifiable thermal conductivity, insulation and hardness/compression data; an advertised W/m·K number alone does not qualify a product. Avoid conductive graphite/metal pads. Trial thermal-pad compression to 0.4 mm, lower foam to about1.65 mm and upper foam to1.2 mm. Adhesive tape needs its own compression/removal trial. Custom stepped insulating posts and relieved support washers remain custom parts, not catalogue standoffs or arbitrary O-rings.

See the [heatsink hardware audit](heatsink-hardware-options.md) for exact screw and nut order codes, measured nominal grip length and printable alternatives to machined POM. The current tapped rear caps do not establish sufficient thread engagement merely by choosing a stock screw length.

## Local fallback and custom-work references

The following previously researched local sources are retained for comparison or urgent fallback; they are no longer the primary small-parts shopping plan. Prices below were checked on the date above.

| Material / parts | Fallback source / custom-work decision |
|---|---|
| Two TPU USB collars | Use existing unfilled, nonconductive TPU 95A or request a small local print quote for both STLs. [Jaycar Elegoo grey TL6530](https://www.jaycar.com.au/elegoo-tpu-95a-filament-grey-1-75mm-1kg/p/TL6530) lists **$29.95 / 1 kg**; store stock requires selection. Buy a spool only if it beats the print quote or will be used for other projects. |
| 0.5 mm insulating thermal pad | [PLE Minus Pad 8, 120×20×0.5 mm, two pieces](https://www.ple.com.au/Products/645790/Thermal-Grizzly-Minus-Pad-8--120x20-x-05mm-Thermal-Pad-2pcs), **$9**, listed in stock at Osborne Park. Ample for the 5.5×5.5 and 3.5×3.5 chip pads, and cheaper than the $19 large sheet. Confirm collection. Compression still needs a trial. |
| Two 2 mm acrylic covers | Request one combined DXF cutting quote from [CDC Laser Perth](https://cdclaser.com.au/laser-cutting/) or [Acrylic Sheet Sales](https://acrylicsheetsales.com.au/laser-cutting-services/). Ask for offcuts, nested panels and secondary 90° countersinks. Price and lead time require quotes. Do not substitute 3 mm sheet. |
| Seven 2 mm lower and six 1.5 mm upper foam pads | Ask [Foam Sales Perth](https://www.foamsales.com.au/) for small nonconductive cushioning samples/offcuts. [Algeos EVA sheets](https://www.algeos.com.au/eva-foam-sheets/) lists these thickness categories as an online alternative. Exact stock, grade and compression remain unconfirmed. Trial samples before buying a large sheet; 3 mm weatherstrip changes the stack. |
| Case hardware and option-retainer hardware | Take the guide's dimensioned list to [Altronics Northbridge](https://www.altronics.com.au/store-locator/altronics-northbridge) first. A complete matching local kit has not been verified. Bundle missing sizes through [element14 fasteners](https://au.element14.com/c/fasteners-mechanical/fasteners-fixings) or [RS Australia](https://au.rs-online.com/). Confirm dispatch location, Perth ETA and delivered total. |
| Polymer M3×8 and M2×8 screws; measured heatsink screw lengths | Include in the same hardware order and verify head envelopes. [Jaycar M3×12 nylon HP0140](https://www.jaycar.com.au/m3-x-12mm-nylon-screws-pack-of-10/p/HP0140), **$2.95 / 10**, is an economical trial blank that can be shortened to 8 mm and deburred if its head fits. It is not an exact drop-in part. M2 still needs sourcing. |
| Rigid printed parts | Use existing PLA/PETG stock; batch spacer frames, plate, screen mounts and option caps/retainer with one print provider. Request TPU collars within the same job, separately printed in TPU. Preserve all insulating material and dimension requirements. |
| Aluminium heatsink and custom POM mounting parts | Send STEP files together for a small-job machining quote. Ask for offcut material and combined setup/pickup. Ordinary standoffs do not replace the relieved custom stops and retainers. Price and lead time are unconfirmed. |

Exact case hardware: **8 M3 female/female 12 mm AF5 columns; 16 Ø7/Ø3.4/0.50 mm end washers; 16 M3×6 90° countersunk screws**. An untapped or male/female spacer does not substitute. Other screws and nuts must match the guide's head envelopes, not just thread size.

## Readily available foam alternatives

- Lower-pad trial: [Officeworks X-Press It A5 adhesive foam, 2 mm, two sheets](https://www.officeworks.com.au/shop/officeworks/p/x-press-it-a5-adhesive-foam-sheet-white-2mm-2-pack-xpfsa52w). Small pack; price and selected-store stock could not be verified. Measure thickness including any adhesive before fitting.
- Lower-pad trial: [Spotlight Crafters Choice EVA sheets](https://www.spotlightstores.com/en-au/p/crafters-choice-12-pack-eva-foam-sheets/80634972), **$10 / 12 sheets**, each 228×304×2 mm. Click & Collect offered, but Perth store stock needs selection. This confirms nominal thickness, not the required cushioning stiffness; trial compression from 2 mm to about 1.65 mm before using all seven pads.
- Exact-thickness upper-pad trial: [Surepak Stylus foam tape](https://surepak.com.au/collections/double-sided-tape) lists **1.5 mm × 12 mm × 33 m**, **$41.83**. Ask for a sample/short length and Perth availability rather than buying an entire roll for six pads. It is double-sided adhesive: avoid bonding the moving assembly to the fixed case. Any non-stick facing adds thickness and needs allowance. Trial compression to 1.2 mm. A listing is not a qualified gasket material.
- Bunnings Raven RP14 is **6 mm** high, unsuitable for this stack. Jaycar NM2821 lacks a thickness specification and currently lists sold out. Solid insertion rubber and rigid craft foamboard are not cushioning substitutes.

## Thermal tape comparison

[Jaycar NM2790](https://www.jaycar.com.au/thermal-transfer-tape-100x100x0-5mm/p/NM2790) is an actual thermal interface: two 100×100×0.5 mm sheets, **$18.95**, **1.6 W/m·K**. Its [datasheet](https://media.jaycar.com.au/product/resources/NM2790_datasheetMain_69168.pdf) gives Shore A 25 and dielectric breakdown >10 kV/mm; the website's 7 V insulation field conflicts with that data. Confirm supplied-product identity if relying on the insulation rating. The sheet thickness fits the free-state design, but compression to 0.4 mm and removal of the adhesive interface need a trial.

The **$9 PLE 0.5 mm gap pad** remains the lowest verified local purchase here for the current design. Jaycar HP1155 transistor insulators are not specified as a replacement for this compressible gap interface and are not part of the thermal BOM.

AliExpress is now the primary small-parts source. Local quotes remain relevant for acrylic and aluminium. No whole-build cost or completion date is confirmed until exact hardware variants, shipping estimates and custom-work quotes are available.
