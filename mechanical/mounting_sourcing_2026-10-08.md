# PHBox mounting and Perth sourcing proposal

Checked 8 October 2026. This is a prototype mounting proposal, not a released enclosure or machining drawing. This proposal itself makes no PCB changes. Use it with [the heatsink candidate](heatsink_2026-10-08/README.md) and [Choc V2 LED fit study](choc_v2_led_fit_2026-10-08/README.md).

Update: the [USB-A top-side revision](USB2-top-assessment-2026-10-08.md) changes the active PCB placement and moves the future dongle bay to the upper edge. The insulating hardware proposal still applies; the current CAD covers remain 26 mm references pending the 15 mm enclosure revision.

## Recommended structure

Keep the **PCB, Choc V2 retention plate, MCU/flash heatsink and OLED on one floating carrier**. Gasket tabs on the carrier rest between upper and lower foam pads on case ledges. Separate fastenezdrs join the outer top and bottom plates outside the PCB. A screw through the PCB into a fixed case spacer would bypass the gasket suspension.

Preserve the intended stack: bottom cover → gasket → bottom thermal relief plate → PCB → top thermal relief plate integrated around the retention plate → upper gasket → top cover. The current CAD includes the MCU/flash top heatsink and outer cover references; the full bottom spreader, carrier, gasket ledges and V2 retention plate remain to be designed. Do not treat the old V1 retention plate as a verified V2 part.

### PCB and gasket mounting

The main PCB holes H1–H7 are **Ø6.4 mm**, not M3 clearance holes. Ordinary Ø5 mm M3 spacers can pass through them. Use custom insulating flanged bushes or equivalent carrier bosses, nominal Ø6.1 pilot with Ø8–10 load-spreading flange, and M3 fasteners. Start the carrier at H1/H3/H4/H6/H2/H7; share H7 with the heatsink's internal fastening rather than stacking a second post there. Preserve H5/H12 for the other heatsink supports. Check each flange against copper, components and retention geometry before committing its size.

Pilot Ø6.1 in a nominal Ø6.4 hole leaves 0.3 mm diametral clearance, not a press fit. Finished-hole tolerance and printed/machined boss tolerance must be checked. The carrier, not the switches' solder joints, should carry mounting loads. PETG can be used for a fit prototype; use dimensionally controlled POM/nylon for the precision thermal stops.

Place gasket tabs on the carrier perimeter, clear of switches, USB connectors and OLED. Start with distributed paired pads and tune their area from assembled deflection; foam compression and spring rate are not established by a generic tape thickness. The earlier concept used 1.5 mm pads per face. Readily obtainable 3 mm foam tape requires different ledges: 20% trial compression would leave **2.4 mm per face**, versus 1.2 mm for the earlier pads. Do not substitute it without changing the stack.

Put damping foam on the covers with clearances around backside sockets, pin ends, thermal contacts and air paths. Keep it clear of components throughout gasket travel. After moving USB-A to the top, the lowest exported feature is the OLED's untrimmed pin tails at Z=−4.5 mm. The current 26 mm cover references therefore leave **7.5 mm** to the bottom-cover inner face at Z=−12 mm. Recalculate that gap for the future 15 mm case; this larger temporary clearance is not available once the bottom cover is raised. Use selective foam/recesses around remaining components.

### Heatsink fastening

Keep three internal supports: M3 at H5/H7 and M2 at H12. Retain the existing **4.00 mm support datum**, established by the POM hard stops; the annular insulating washer sits around the central stop land. Soft washers or O-rings cushion/isolate the support but do not set chip loading. A stock 5 or 6.3 mm spacer is not a replacement.

The current front stop is a 3.50 mm seat plus a 0.50 mm washer, with the central hard-stop land ending at 4.00 mm. H5/H7 use Ø8 flanges and Ø6.1 PCB pilots; H12 uses Ø4.5. Rear retainers/washers are custom too. Have these insulating stops and retainers made with the heatsink, or revise the entire mounting stack to a measured catalog assembly before machining. Do not clamp the aluminium directly onto the PCB or use the chips as mechanical stops.

Use polymer screws. Trial M3×12 or ×15 at H5/H7 and M2×12 at H12, then choose/trim lengths against the actual head washer, rear retainer and thread engagement. These lengths are candidates, not cleared fastener assemblies. Inspect head clearance and prevent screws bottoming out before the hard stops seat. Preserve BOOTSEL/RESET access.

Cut separate **5.5×5.5 mm MCU** and **3.5×3.5 mm flash** pads from a 0.5 mm electrically insulating thermal pad. Thermal Grizzly Minus Pad 8 is a locally stocked candidate, not a validated 20%-compression interface. The manufacturer confirms electrical insulation and 0.5 mm availability, but the required package load/compression must still be established. Measure installed package heights and adjust boss heights to the chosen compressed pad. Do not bridge surrounding passives with one large pad.

### Screen mounting

HS13L03W2C01 has four Ø3 mm mounting holes on a **30.4×28.5 mm pitch**. Matching board holes are at PCB coordinates (85.1,39.75), (85.1,68.25), (115.5,39.75), (115.5,68.25).

Use **four M2.5 nylon screws, 3.0 mm insulating spacers and underside nuts**. The current STEP mounting land is at module-local Z=0 with +3 mm placement, so 3 mm is the starting post height; the long header pins are not a mounting datum. Trim/deburr four 6 mm spacers from the local M2.5 kit to 3 mm and verify flatness/thread engagement, or buy exact 3 mm spacers online. Do not install unmodified 6 mm posts and assume the existing top-cover height still works.

Use compact heads/upper washers, **OD≤5 mm as a candidate limit**, at the corners; check the actual part against the glass. Do not load the glass or rely on the header solder joints. Trial M2.5×10 bolts and trim protrusion after measuring the complete stack. Trim header ends only as needed after soldering, keeping electrical joints intact. The screen mounts to the floating PCB/carrier, not separately to the fixed top cover.

### Outer covers

For the provisional 3 mm top and bottom covers and 20 mm cavity, use **four 20 mm female/female M3 case spacers and eight M3×6 screws**. These are outside the PCB and independent of its gasket suspension. The overall reference stack is **26 mm**, excluding keycaps and screw heads. Brass spacers are acceptable here because they do not touch the PCB/heatsink island.

Alternatively, untapped 20 mm nylon spacers need approximately M3×30 through-bolts and nuts: 3+20+3=26 mm before adding a nut. M3×25 is too short. Exact spacer corner envelopes and screw heads must be incorporated in the case CAD before cutting covers.

## Local shopping shortlist

Prices are AUD as displayed; web stock is not a reservation. Only PLE below exposed an unambiguous Osborne Park stock status. Altronics web availability does not establish Northbridge shelf stock; phone/check collection before travelling.

| Use / quantity for one prototype         | Part and source                                                                                                                          | Availability / adjustment                                                                                                                                                                                                                                                                 |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OLED hardware: 4 screws, 4 nuts, 4 posts | [Altronics H8946 M2.5 nylon kit](https://www.altronics.com.au/product/h8946-m25-nylon-screw-stand-off-set), $29.95                        | Web in stock. Contains 6 mm posts, not 3 mm: shorten or source exact height.                                                                                                                                                                                                              |
| Heatsink M3 screws: 2 plus spares        | [Jaycar HP0140 M3×12 nylon, 10 pack](https://www.jaycar.com.au/m3-x-12mm-nylon-screws-pack-of-10/p/HP0140), $2.95                        | Actual assembled grip/head clearance must be checked.                                                                                                                                                                                                                                     |
| Spare polymer spacers for carrier trials | [Altronics H1339 M3×5 nylon, 8 pack](https://www.altronics.com.au/product/h1339-m3-x-5mm-nylon-tapped-spacer-pk-8), $3.40                | Web in stock. Does not bridge Ø6.4 holes or replace precision stops.                                                                                                                                                                                                                     |
| Four case spacers                        | Altronics H1250 M3×20 tapped metal, 8 pack, $6.95;[catalog](https://www.altronics.com.au/category/spacers-mounts?pagenumber=2)           | Catalog listing; confirm material, through threading and local stock. Add eight M3×6 screws: H2915 polycarbonate, 25 pack, $4.70, in the[Altronics fastener catalog](https://www.altronics.com.au/hardware/bolts-nuts//?prdf=5&size_2=m3-size&srt=2&type_1=polycarbonate-panhead-screws). |
| Alternative case spacers: 4              | [Altronics H1326 M3×20 untapped nylon, 10 pack](https://www.altronics.com.au/product/h1326-m3-x-20mm-untapped-nylon-spacer-pk-10), $4.25 | Web in stock; Ø5 outside/Ø3 nominal bore. Requires long through-bolts and nuts.                                                                                                                                                                                                         |
| Prototype gasket trial                   | [Bunnings Moroday 24×3 mm PE foam tape, 10 m](https://www.bunnings.com.au/moroday-24-x-3mm-x-10m-grey-pe-foam-tape_p0077670), $9.47      | Store stock unconfirmed. Prototype cushioning, not qualified urethane gasket material. Requires new ledge spacing.                                                                                                                                                                        |
| MCU/flash thermal pads                   | [PLE Minus Pad 8, 100×100×0.5 mm](https://www.ple.com.au/products/645562/thermal-grizzly-minus-pad-8-100x100-x-05mm-thermal-pad), $19   | Osborne Park listed in stock. Manufacturer TG-MP8-100-100-05-1R.                                                                                                                                                                                                                          |

Nearest-city priority: [Altronics Northbridge, 174 Roe Street](https://www.altronics.com.au/store-locator/altronics-northbridge), then [Bunnings Homebase Subiaco, 55 Salvado Road](https://www.bunnings.com.au/stores/wa/homebase-subiaco). For other items, [Jaycar Osborne Park, 83–87 Frobisher Street](https://www.jaycar.com.au/stores/osborne_park_jaycarau) and [PLE Osborne Park, Unit 3/3 King Edward Road](https://www.ple.com.au/Contact/OsbornePark).

Manufacturer thermal-pad information: [Minus Pad 8](https://www.thermal-grizzly.com/en/minus-pad-8/s-tg-mp8).

## Online fallback

- **M2 polymer screws:** element14 lists TR Fastenings **TRNSE-1207-M2-12**, order **2472690**, M2×12 nylon 6.6, in its [M2 plastic screw catalog](https://au.element14.com/c/fasteners-mechanical/fasteners-fixings/plastic-fasteners/plastic-screws?thread-size-metric=m2). Pack of 100 was $12.43 including GST; live stock/delivery was not resolved. Ask for the fastest stocked dispatch location before relying on it.
- **RS alternative:** [232-6904 M2×12 nylon screws](https://au.rs-online.com/web/p/machine-screws/2326904), $74.89/100. Listed stock was at another location. [RS delivery guidance](https://au.rs-online.com/web/content/support/all-articles/delivery) for locally stocked items does not establish this item's Perth ETA.
- **Expedited options:** [element14 UK Express](https://au.element14.com/uk-express) advertises eligible UPS Express Saver orders in 3–4 days. Eligibility, stock location and postcode need confirmation. [Core Electronics hardware](https://core-electronics.com.au/hardware.html) offers M2.5 kits with express checkout; its product checkout guidance quotes express from $11 and typically 2+ days, not guaranteed next-day Perth delivery. Local Altronics is preferable for this kit.

## Before committing the hardware

1. Fit the V2 switches/LEDs using the LED study and test physical samples; community STEP geometry is not an OEM tolerance certificate.
2. Design the carrier, V2 retention plate and gasket ledges with the selected spacers/foam; check full travel and connector openings.
3. Measure thermal package tops, PCB thickness and screen mounting land; settle pad load and insulating stop dimensions.
4. Include actual screw heads, washers, nuts and spacer envelopes in CAD and rerun interference checks. Current fit checks covered custom support geometry, not this entire shopping list.
5. Assemble the island first, then float it in the case. Verify screen access, BOOTSEL/RESET access, gasket travel and no chip load change when cover screws tighten.

The design can use ordinary retail fasteners and locally stocked pad material, but **custom carrier geometry and precision insulating stops remain necessary** for the present hole sizes and thermal stack. No fabrication revision is proposed merely to use standard fasteners.
