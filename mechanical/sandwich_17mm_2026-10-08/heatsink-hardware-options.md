# Heatsink hardware and printable mounting alternatives

Audit: 9 October 2026. This is a procurement/design assessment, not approval of a new loaded heatsink mount. The current 17 mm sandwich is the governing assembly; the older 26 mm mounting illustration is not the case specification.

## Fit requirements found in the current CAD

The heatsink web spans Z=4..7 mm. Each stop has a 3.5 mm outer shoulder plus a raised 0.5 mm central hard land, setting the underside to Z=4. The outer support washer is 0.5 mm installed. H5/H7 stops have Ø8 outer shoulders, Ø6.1 locating pilots and Ø3.4 screw clearance. H12 is Ø4.5 outside with Ø2.2 clearance. These stepped stops are not ordinary cylindrical catalogue standoffs.

Rear retaining washers span Z=-2.15..-1.65; the current tapped retainers span Z=-4.15..-2.15, giving only 2 mm nominal thread depth. The cap pilots are Ø2.5 for M3 and Ø1.6 for M2, with threads absent from CAD. Without a washer beneath the top screw head, grip to the first rear thread is **9.15 mm**:

| Under-head screw length | Engagement / projection in current nominal retainer |
|---|---|
| 10 mm | 0.85 mm engagement; not a qualified plastic joint |
| 11 mm trimmed | 1.85 mm engagement; 0.15 mm short of the rear face, before tolerances |
| 12 mm | Passes all 2 mm of nominal threads, then projects 0.85 mm below the cap |

Adding a 0.5 mm top washer changes grip to 9.65 mm: a 12 mm screw then projects 0.35 mm below the current cap. Neither case establishes safe thread strength or rear component/foam clearance. The covers have local heatsink fastener reliefs; confirm actual head diameters against those openings and the allowed PCB motion. Do not buy 10 mm screws assuming their name alone establishes fit.

## Primary sourcing: AliExpress

Source small parts through the [AliExpress procurement list](materials.md). Seller stock, dimensions, price and Perth delivery dates are unverified. This sourcing change does not alter stepped-stop geometry or settle screw length. Measure delivered nuts before finalising PETG capture pockets, and verify screw head envelopes.

## Local fallback and manufacturer references

Prices are AUD including GST where quoted, before freight. Shelf stock and Perth delivery dates are unconfirmed unless stated otherwise.

| Purpose | Part / source | Decision |
|---|---|---|
| Two M3 heatsink screw trial blanks | [Jaycar HP0140, M3×12 nylon, ten pack](https://www.jaycar.com.au/m3-x-12mm-nylon-screws-pack-of-10/p/HP0140), $2.95 | Local small-pack fallback. Measure heads; use length trimming only after the rear retention arrangement is settled. |
| M3 screw with traceable manufacturer family | TR Fastenings TRNSE-1207-M3-12, element14 **2472706**; [manufacturer nylon fastener catalogue](https://www.farnell.com/datasheets/2815412.pdf), [order-code index](https://www.farnell.com/datasheets/3959548.pdf) | Nylon 6.6, ISO 1207 cheese head. Availability/price not verified; obtain current quote. Manufacturer warns critical dimensions must be confirmed. |
| H12 M2 screw trial blank | TR Fastenings TRNSE-1207-M2-12, element14 **2472690**, same catalogue/index | 12 mm version is a trimming candidate, not a confirmed installed length. The 8 mm version **2472697** is for current screen mounts, not this heatsink grip. |
| M2 alternative | [RS PRO 527-915, M2×12 nylon](https://au.rs-online.com/web/p/machine-screws/0527915), listed $35.40 / 100 | Poor one-board value; listing says remaining stock is at another location. Confirm quote and ETA rather than relying on it for rapid local supply. |
| Stock M3 rear nuts for proposed redesign | [Jaycar HP0146 nylon M3 nuts, ten pack](https://www.jaycar.com.au/3mm-nylon-nuts-pack-of-10/p/HP0146), $2.95 | Useful stock alternative to tapped custom caps. Actual AF, thickness and corners must be measured before modelling capture pockets. |
| Stock M2 rear nut for proposed redesign | TR Fastenings TRNNE 34814 M2, element14 **2472685**; [order-code index](https://www.farnell.com/datasheets/3959548.pdf) | Source the exact drawing/sample; nominal M2 alone does not establish its capture-pocket size. |
| Acrylic case columns, separate from heatsink | [RS PRO 222-402](https://au.rs-online.com/web/p/standoffs/0222402): M3 female/female, 12 mm, AF5, brass; $50.65 / 50 listed | Exact nominal body/thread match to case columns, but expensive for eight pieces and not an insulating heatsink post. Stock listed ready to ship; Perth ETA still requires confirmation. |
| Cheaper local case-column candidate | Altronics **H1348**, M3×12 tapped nylon, eight pack, $3.75 in [catalogue](https://www.altronics.com.au/category/spacers-mounts?pagenumber=3) | Threaded arrangement, body diameter and dimensions must be confirmed. Not an automatic AF5 drop-in; nylon case-column compression also needs trial. Call Northbridge before travelling. |

The search found no verified stock part that duplicates the stepped heatsink stop. Ordinary 4/5 mm posts do not reproduce its shoulder, pilot and support-washer land. Keep custom adapters if using stock components. Consolidate M2 items into the screen/option hardware order; do not buy a large assortment merely to obtain one screw.

## More manufacturing-friendly alternatives

| Part / process | Assessment |
|---|---|
| **PETG shoulder stops + stock nylon nuts in printed capture carriers** | Recommended low-cost prototype direction. Print clearance bores and accessible hex pockets instead of tiny printed/tapped threads. Keep positive hard lands at Z=4, the insulating shoulder and the PCB pilot. Redesign carrier thickness and screw length together, and check nut corners against rear parts/foam. No functional redesign has been qualified yet. |
| PETG copies of current tapped caps | Good dimensional mock-ups; only 2 mm thread depth is a poor basis for repeated fastening. Do not treat a pilot hole or printed thread as proof of joint strength. |
| Stock nylon spacer + washers | Readily available, but needs a custom shoulder/pilot adapter and a measured stack. Washer piles accumulate tolerances and do not positively locate the large PCB hole. Less attractive than one calibrated printed stop for this prototype. |
| SLS/MJF unfilled PA12 | Quote as a consolidated batch of all insulating posts/retainers if outsourcing. More expensive than home FDM; fine bores, nut pockets, accuracy and service temperature still need provider validation. |
| Machined POM | Retain as the option for controlled shoulder heights and a repeatable finished part. Flatten/simplify the mounting design and use through-fasteners with stock nuts to remove tapping operations where possible. |
| **TPU** | Keep for USB collars and optional compliant support washers only, with a separate rigid hard stop. Do not use it for height-setting posts, nut carriers or threaded rear retainers: their intended function requires stable dimensions under clamp load. |

These are engineering recommendations, not material qualification. [Prusa's PETG guidance](https://help.prusa3d.com/article/petg_2059) supports its use for mechanical holders and clamps; it does not certify sustained preload beside this heatsink. Use unfilled material, low fastening preload, calibrated shoulder heights and a thermal/creep trial with the actual aluminium plate. Avoid conductive/carbon-filled filament around the PCB. TPU flexibility is useful where compliance is intended, not as a substitute for the hard lands.

For a first fitment mock, print the existing geometry and compare it to real screws/nuts. For an operational PETG mount, first settle the rear nut/carrier geometry, check all hardware at the PCB travel extremes, measure installed thermal-pad compression, then trial temperature and loosening. The mock aluminium plate and printed PCB/component surrogates must remain unpowered.
