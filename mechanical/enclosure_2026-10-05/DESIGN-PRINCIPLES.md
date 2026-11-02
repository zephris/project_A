> Current switch choice (2026-10-07): OEM Kailh Choc V2, cross (+) stem. Earlier V1 plate dimensions below are historical prototype assumptions and require V2 retention/height verification. See ../model_completion_2026-10-07/README.md.

# PHBox enclosure design principles — 2026-10-05

This document records the user's enclosure requirements and researched techniques.
The Choc V1 retention plate is the first geometry candidate. The complete enclosure,
thermal plates, foam cuts and screen carrier remain to be dimensioned and validated.
The electrical PCB and frozen JLCPCB manufacturing package are unchanged.

## Required stack, from bottom to top

1. Acrylic cut or PLA printed bottom outer plate.
2. Lower suspension gasket, on defined support lands.
3. Bottom aluminium thermal relief/spreader plate, with component reliefs and electrically insulating thermal interface where appropriate.
4. PCB, carried by the gasket suspended internal assembly.
5. Top aluminium thermal relief/spreader plate, interwoven in plan with the Choc V1 switch retention plate.
6. Upper suspension gasket and mounting lands.
7. Acrylic cut or PLA printed top outer plate/bezel.

“Interwoven” means complementary regions of a common floating assembly: a plastic
retention plate in the switch field and a separate metal spreader in the electronics
region, with insulated structural connections as necessary. They need not share one
Z height. An MCU contact boss can sit lower than the main upper spreader. Avoid metal
over the switch clips or any obstruction to switch removal. Local thermal pads are
additional interfaces at the PCB/spreader boundaries; suspension gaskets have a
different purpose and are not a substitute for a qualified thermal interface.

## Suspension and fastening

- Suspend the PCB, switch plate, both spreaders and screen carrier as one internal island between upper and lower gasket supports. The PCB must be supported by that island, not merely left hanging from switch solder joints or hotswap sockets.
- Use discrete, symmetric gasket lands around the perimeter rather than packing the entire underside. Place support near the main button groups; adjust stiffness for reliable gaming inputs without rocking. A highly flexible keyboard feel is not automatically desirable for a fight controller.
- Existing PCB mounting holes are available for insulated fasteners within the island. Do not run rigid case standoffs through them and clamp the PCB to the outer plates: that bypasses the gasket suspension. Screen posts also belong to the floating island.
- Case screws join the outer enclosure around the island. Hard stops between outer case parts set the closed cavity height and gasket compression. Local hard stops within the island independently set the MCU thermal-pad gap. These are two separate load paths.
- Prototype starting point: 1.5 mm soft microcellular urethane gasket pads on each face, with 20% initial compression (1.2 mm installed per pad). This is a design assumption, not a supplier requirement. Choose a specific grade and evaluate its compression-force/deflection curve, pad area and material tolerances before release.
- Start with a 0.5 mm travel budget in each vertical direction and lateral clearance at all moving interfaces. This is a prototype target, not calculated deflection. Verify loaded displacement, return to position, and absence of bottoming under simultaneous button presses. Add cushioned overload stops if needed; stops should not engage during normal use.
- Allow PCB motion at USB-C and USB-A openings. Cable stiffness can also bypass suspension. Provide clearance around connector shells and cable plugs, retain access to boot/reset controls, and avoid using the fixed enclosure to grip the board-mounted connectors.
- The display moves with the PCB. Its protective window/bezel must clear the module at both travel limits. Posts must support the module at its four mounting holes without loading the glass or requiring the electrical header to carry mechanical loads.

Rogers' gasket guide explains why material compression behaviour, flatness, thickness
tolerances, compression set and enclosure creep determine the installed load. Its
sealing examples are useful mechanical guidance; this enclosure is not being claimed
as a water seal. [Rogers design guide](https://tools.rogerscorp.com/documents/993/hpf/poron/industrial/Sealing-Gasketing-Design-Guide.aspx),
[PORON 4701-30 material family](https://www.rogerscorp.com/elastomeric-material-solutions/poron-industrial-polyurethanes/poron-4701-30).

## Foam damping

- Make the damping removable and independently tunable. Begin with 1 mm case foam in the switch region; trial 2 mm only where the closed cavity and suspension travel permit it. Those are prototype trials, not a guaranteed fit.
- Prefer nonconductive, documented foam such as microcellular urethane or a suitable neoprene grade. Exclude conductive/antistatic foam unless its electrical behaviour is deliberately accommodated. Verify the actual supplier's material rather than assuming every black foam is insulating.
- Keep acoustic foam clear of the MCU contact pad, both spreaders' heat rejection surfaces, USB openings, LEDs, sockets, pin tails, connectors and screen posts. Provide component-shaped reliefs rather than compressing foam onto components. A foam-backed PCB can become a rigid tray mount if the cavity is overfilled.
- Where possible, attach case foam to the stationary outer shell and leave a gap beneath the floating assembly at maximum normal travel. If foam touches the island, treat it as an additional spring in the load/deflection assessment.
- Thin optional plate foam may occupy confirmed empty space between retention plate and PCB, with cutouts for switches and every component. Do not put unverified foam under Choc switch bases: raising switches can impair clip engagement or pin/socket insertion. The Choc stack is too shallow to borrow MX foam thicknesses directly.
- Do not promise a particular sound from materials alone. Compare no foam, 1 mm and 2 mm trials with the same switches/keycaps, checking input reliability and gasket motion as well as sound. Omit PE/IXPE switch film from the first candidate; add it only after fit and electrical seating are established.

ZSA recommends checking thickness against the actual enclosure, and describes case
foam and switch pads as different treatments. Its Moonlander example favours about
2 mm over a tight 3 mm insert; those dimensions are not transferred to PHBox as a
verified stack. [ZSA foam installation guide](https://blog.zsa.io/robins-repairs-foam/).
Keychron explicitly notes that its bottom acoustic pad reduces flexibility and can
be removed. That supports a removable, tunable approach here.
[Keychron double gasket and acoustic stack](https://www.keychron.com/collections/new-arrivals/products/keychron-q5-ultra-8k-wireless-custom-mechanical-keyboard).

## Thermal spreaders and outer materials

- Use separate aluminium spreaders inside the acrylic/PLA enclosure, with deburred edges, insulated fasteners and clearance from conductive components. Anodising is not the primary electrical isolation barrier.
- Make the top MCU contact through an electrically insulating, compliant thermal pad. Set its compression with local stops within the floating island, never by tightening the outer enclosure. Pad thickness and force must be selected from actual assembled heights and the selected pad's load curve.
- A bottom spreader is a PCB-to-spreader thermal path; it does not directly contact the MCU die. Solder mask alone is not sufficient protection against metal contact. Reliefs and a qualified insulation/interface layer are needed around underside components and exposed conductors.
- Spreaders must move with the PCB so pad compression does not vary with button presses. A rigid thermal bridge to the outer shell would bypass the gasket mount. If a flexible thermal link is later proposed, assess its added spring force.
- Reserve ventilation or exposed, guarded heat rejection surfaces around the electronics zone. Aluminium enclosed between insulating plastic and acoustic foam is a heat spreader, not a demonstrated heatsink. Cooling performance must be measured or modelled after the full geometry and power budget are available.
- Keep the electronics zone free of acoustic fill. Check PLA temperature/creep and acrylic cracking against the final thermal and mechanical load conditions. Do not rely on a 1.3 mm plastic clip sheet as the sole structural support of the entire controller.

## Choc V1 candidate and validation gates

The first plate uses the actual SW1–SW16 stem centres and existing lower mounting
hole locations. It ends at PCB Y=80 mm, leaving the electronics zone available for
the top spreader and screen carrier. Eight tabs provision upper gasket supports;
the lower carrier and lower gasket lands have not yet been designed.

The manufacturer's drawing gives a 13.8 mm housing width and depicts the flange/latch
geometry. A 14.0 mm square opening and 1.3 mm sheet are candidate choices, not a
manufacturer-specified finished cutout tolerance. Trial coupons include 13.9, 14.0,
14.1 and 14.2 mm holes at 1.2 and 1.3 mm thickness. Start with a coupon from the actual
printing/cutting process, check seating, retention, removal and burrs, then adjust.
[Kailh PG1350 drawing](https://www.kailhswitch.com/Content/upload/pdf/202215927/CPG135001D01-16.pdf).

Before enclosure release: check switch latch height and full seating; retention under
keycap removal; assembled component clearances; stiffness of the large plastic plate;
foam/gasket travel under multi-button loads; display/USB motion clearance; thermal-pad
force; temperature rise; and access for assembly and servicing. The original overall
height target may need to increase to accommodate two spreaders, gaskets and travel.
