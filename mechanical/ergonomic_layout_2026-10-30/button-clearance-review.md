# Button-to-component confirmation

Checked the saved wider-candidate PCB STEP against its matching screen, heatsink
and mounting geometry on 30 October 2026. The PCB hash matches the prior fit
report. The selected cap diameter has subsequently changed to 20 mm and the
top acrylic openings to 24 mm. No PCB, screen or heatsink positions changed.

**The modeled switch bodies clear, but main-keycap clearance through a complete
press is not yet confirmed.**

## Selected 20 mm cap revision

The user selected SGF MonKeys / generic 20 mm round Choc V2-compatible caps.
The named baseline is SGF MonKeys Choc V2 / Small / Flat / Nekkid. The case now
uses 24 mm through-openings. Nominal radial clearance is 2 mm. The
[conditional worst-case budget](checks/tolerance-budget.json) retains 0.337 mm
after the specified locator, manufacturing and cap acceptance allowances.
Supplier acceptance and physical measurements are still required.

The 20 mm envelope removes the historical SW16 projection overlap described
below. The selected-cap report is [selected-caps.json](checks/selected-caps.json).
Its native guards span Z=0–15 mm to avoid relying on an invented cap underside.
The named part's stem, seating depth, maximum skirt diameter and actuation
still need a purchased-part fit trial. The guard is not a vendor STEP model.
The measured guard gaps are **1.00 mm from SW16 to the heatsink** and
**2.55 mm from SW1 to the screen frame**, before their own mounting and
manufacturing variation. These are nominal distances, not guaranteed gaps.

## What passes

The [direct check](checks/button-interference.json) selects both the switch and
hot-swap socket occurrences for all 16 main buttons, plus the six option tact
switches and BOOTSEL/RESET. It compares them with the screen module, frame,
posts/rear caps, screw-head envelopes, heatsink/supports and other modeled PCB
components. There are **zero positive-volume button-body intersections**.
Own switch/socket mating parts are treated as one assembly; nearby RGB LEDs,
resistors and capacitors are not arbitrarily exempted.

| Relevant interface | Nominal clearance |
|---|---:|
| SW1 switch/socket assembly to screen frame | 5.23 mm, native distance |
| SW1 switch/socket assembly to screen posts/rear caps | 8.10 mm, native distance |
| SW1 switch/socket assembly to screen screw-head envelopes | 8.83 mm, native distance |
| SW16 switch/socket assembly to heatsink | 3.69 mm, native distance |
| Assumed 24 mm SW1 keycap footprint to screen frame | At least 0.55 mm, conservative plan-envelope bound |

Far-away objects use conservative bounding-box separation; close interfaces
above use exact native distances. Overlapping boxes are checked with native
solid intersections. This is additional to the earlier case/board travel and
option-cap checks; it is not a physical tolerance qualification.

## Historical 24 mm concern and alternatives

The former **24 mm round footprint at SW16 (LS)** extended about **1 mm over the heatsink
in plan view**. A cap whose underside stays high enough throughout the press
could clear it. A low skirt could touch it. The conservative vertical guard
intersects approximately 19.35 mm³ of the modeled heatsink; this guard is not
the actual cap and therefore does not prove an actual collision.

The web top is nominally Z=7 mm relative to the PCB front datum. The guard's
conservative bounding box gives a sufficient underside height of approximately
Z=7.1 mm; neither number includes a manufacturing clearance allowance. The
chosen cap's shape, mounting depth and full-stroke position must be checked.

A 20 mm cap, now selected, removes this particular projected overlap. Alternatively, moving
SW16 2 mm right would put a 24 mm footprint's left edge at X=182 mm, 1 mm past
the heatsink's nominal X=181 mm edge, but that is a proposal requiring the PCB,
case opening and neighboring socket/component clearances to be updated and
checked. No switch movement was needed for the selected 20 mm cap.

The existing 0.302 mm plate/heatsink gap at H7 is a separate plate interface,
not a switch collision. Its cutting tolerance and the existing threaded
retainer concerns remain prototype checks.

See the [keycap shortlist](keycap-shortlist.md) before choosing the cap envelope.
