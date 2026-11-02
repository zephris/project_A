# USB2 C2344 replacement — 9 October 2026

USB2 now uses **Jing 902-131A1021D10100 / JLCPCB C2344**, a right-angle
through-hole USB 2.0 Type-A receptacle, on the top side at **(192,47),180°**.
The contact row stays in its existing location. Firmware pin assignments, host
VBUS limiting, ESD protection and data/power nets are unchanged.

The [OEM drawing](https://datasheet.lcsc.com/datasheet/pdf/b37ecd4a181075ec1f8259176f7b6687.pdf?productCode=C2344)
specifies four Ø0.9 contact holes, two Ø2.1 shell holes,7 mm contact span with
2 mm inner pitch, and14 mm shell-hole span. Shell holes are2.71 mm ahead of the
contact row. The drawing's10.15 mm face-to-shell datum gives12.86 mm from face
to contact row. Nominal mating face is therefore KiCadY34.14; shell height is
7 mm above the PCB and terminal projection reaches3.7 mm below it. The footprint
uses Ø1.7 contact lands and Ø3.2 shell lands, with pad1 square for identification.
Both shell lands are pad5/GND to preserve the schematic symbol's shield mapping.

| Contact | Net | PCB X,Y mm |
|---|---|---|
| 1 | USB_HOST_5V |195.5,47|
| 2 | HD− |193,47|
| 3 | HD+ |191,47|
| 4 | GND |188.5,47|
| 5, shell | GND |185,44.29 and199,44.29|

The new plated rear VBUS land conflicted with a nearby enable-trace bend. Only
two existing **USB_HOST_EN** B.Cu segments were replaced with three segments,
moving that bend0.3 mm sideways. The USB data and power fan-outs are unchanged.
Native audit confirms145 other footprints, all retained routing items and the
board outline unchanged. The previous locating holes disappear; the connector
now has six plated through holes and needs no board cutout.

Final KiCad10 DRC: **zero errors, zero unconnected items and zero schematic-parity
findings**. The same two R2/C4 and R2/R3 silkscreen-clearance warnings remain.
Evidence and reproducible scripts are in
[`stage2_work/usb_c2344_2026-10-09`](../stage2_work/usb_c2344_2026-10-09).

The user's images showed a questionable floating SMT reference. The first view
obscured its open cavity; the later perspective showed the cavity exists. C2344's
linked EasyEDA STEP was downloaded and inspected, but its pin/body registration
does not closely match the OEM drawing. It is retained as evidence and **not used**
as an accurate fit model. The selected STEP is an explicitly simplified,
**drawing-derived reference**, built by `connector_model.py`: Z0 seating surfaces,
four aligned through-board contacts, two shell pins, an open insertion gap and
separate plastic/shell bodies. It omits small folds, spring retention, exact
contact bends and fine plastic detail; it is not manufacturer tooling CAD.
Saved native checks match all four contact centers and both shell pins to the
new holes, show no insertion-gap obstruction and3.8 mm separation from the heatsink.
Inspect actual samples and solder joints before production use.

The native board STEP and current17 mm sandwich assembly are regenerated around
this part. The enclosure keeps its292.6×191 mm plan boundary and six captured
option-button caps. See the [mechanical candidate](sandwich_17mm_2026-10-08/README.md)
for final gauge checks and physical-trial limitations.

[JLCPCB](https://jlcpcb.com/partdetail/2720-902131A1021D10100/C2344) lists C2344 for
**wave soldering**, rather than SMT reflow placement. Request factory review of
selective/wave or manual soldering on this mixed, two-sided assembly; nearby
bottom-side parts must be protected. This is a process-review requirement, not
confirmation that whole-board wave soldering is suitable. Existing manufacturing
Gerbers/BOM/CPL and quote selections remain older revisions: regenerate and
visually approve the replacement's orientation and through holes before ordering.
No order was submitted.
