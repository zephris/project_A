# Round Choc V2 keycap shortlist

## Selected for the wider candidate

User selection: **SGF MonKeys / generic 20 mm round arcade-style keycaps**.
Use **Choc V2 / Small / Flat / Nekkid, PA12 nylon**, as the named baseline.
The nominal model input is a 20 mm circular plan envelope for each main cap;
the top cover uses 24 mm through-openings, providing 2 mm nominal radial clearance.
The switch centres, 32 mm action pitch and Choc V2 retention apertures stay fixed.
This choice applies to all 16 main controls, not the six custom option plungers.

A generic substitute must fit Kailh Choc V2 with an MX-style cross stem and
must meet the 20.2 mm maximum measured outer/skirt diameter allocation. Check its seating
depth, underside relief and full press in the assembled cover. A generic
20 mm panel-mount arcade pushbutton is not a substitute for these keycaps.
The exact cap underside and mounting depth have not been measured or modeled.
The opening was increased from the initial 22.5 mm proposal after the
[manufacturing tolerance budget](manufacturing-tolerances.md) was added.
No order was placed. Earlier 24 mm and 25.2 mm suggestions below are alternatives,
not the selected geometry.

## Earlier sourcing comparison

Checked 30 October 2026. No order was placed. Prices are GBP before shipping
and applicable tax. Perth delivered prices and arrival dates were not quoted.

| Choice | Exact option | Material | Stock / unit price checked | Suitability |
|---|---|---|---|---|
| [AdditiveArcade low-profile round caps](https://additivearcade.com/products/low-profile-round-choc-v2-3d-printed-button-caps) | Standard / 24 mm, e.g. Black | PLA; translucent options use PETG | Available, £0.85 | Earlier alternative; not selected. Seller explicitly lists MX/Choc V2. This diameter is not a drop-in fit for the current cover allowance. |
| [SGF MonKeys through AdditiveArcade](https://additivearcade.com/products/low-profile-sgf-monkeys-button-caps) | Choc V2 / Small / Flat / Nekkid, 20 mm | PA12 nylon, opaque | Available, £0.83 | Smaller contact surface and more clearance; removes the specific 24 mm SW16/heatsink plan overlap. The current cover would leave a wider gap around it. |

The same SGF listing offers **Choc V2 / Large / Flat / Nekkid, 25.2 mm**, checked
available at £0.93. This is another size choice, but it needs larger cover
openings to retain the intended floating-board clearance and worsens the SW16
projected overlap. It is not a drop-in geometry approval.

The seller advertises dispatch within five working days; that is not an
Australia delivery estimate. Both recommended products can be combined through
the same store, subject to its checkout shipping price. Verify the Choc V2 stem
selection: the SGF page defaults to a Choc V1 variant.

Stock/price were checked against the public product variant data, in addition
to the product descriptions:

- Printed Black / Standard / 24 mm: variant `58243123315069`, available, £0.85.
- SGF Choc V2 / Small / Flat / Nekkid: variant `48649959211295`, available, £0.83.
- SGF Choc V2 / Large / Flat / Nekkid: variant `53536057950589`, available, £0.93.

[NLOFIN's 23 mm molded caps](https://nlofin.shop/products/nlofinleverless-controller-keycaps-replacement-button-caps-4pcs-23mm-arcade-replacement-hitbox-button-caps-for-mechanical-pushbuttons-caps-for-ttc-cherry-akko-switches-caps)
are a possible future candidate, but the official page currently says sold out
and names TTC/Cherry/Akko rather than explicitly guaranteeing Choc V2 clearance.
The indexed AliExpress search did not provide an independently verifiable exact
listing for the required fit. Do not substitute a generic cross-stem cap without
checking its skirt and seating depth.

The selected diameter is recorded in `layout.json` and used by the cover and
layout guide. A vendor-specific underside model is still unavailable. An MX cross
mount and nominal diameter do not prove full-stroke clearance. See the
[button clearance review](button-clearance-review.md).
