# PHBox project guide

This repository is a KiCad hardware project for PHBox, a slim wired leverless controller. Use `README.md` for product intent and the KiCad schematic and PCB as the current implementation. The design takes its RP2350 controller foundation from Flatbox Rev 8; its enclosure target is inspired by the Haute42 T13/T16 form factor.

## Design constraints

- Target enclosure envelope: 296 × 196 × 16.5 mm. This is an **outer enclosure target**, not the PCB outline. Verify the PCB, mounting points, ports, switch caps, OLED, and top plate against a shared mechanical drawing before fabrication.
- Support 13-button and 16-button layouts with an explicit population or variant plan. Every fitted button needs a unique reference, documented GPIO assignment, and firmware action.
- Use an RP2350A, wired USB-C device connection, and GP2040-CE-compatible firmware configuration. The RP2350's native USB interface is full speed; do not describe the board as USB 3.1 capable because it uses a USB-C connector.
- Design for Kailh Choc V1 hot-swap sockets. Treat soldered Choc V2 and 5-pin full-size switches as separate, mechanically verified assembly options; the latter requires a different top plate.
- Keep the enclosure slim and light while allowing the gasket-mounted, foam-lined top plate and aluminum lining plate. Confirm stack height and clearances with actual component and switch dimensions.
- Budget USB input and protection, OLED, all RGB LEDs, and any pass-through or USB host load together. Verify current limits, power distribution, and thermal behavior before choosing the fuse and power path.
- Treat controller modes, platform compatibility, and sub-1 ms latency as firmware and system validation targets, not properties established by the PCB alone.

## Desired features

- OLED status display and configurable button mapping through GP2040-CE.
- Individually addressable RGB lighting at each action button, plus diffused case-edge lighting. Each LED's data output must feed the next LED's data input on a distinct net.
- Flush-mounted pass-through/USB host port, if supported by the selected firmware and power budget.
- Foam-lined, gasket-mounted top plate and CNC aluminum lining plate.
- Wired modes targeted in the README: XInput, Switch, PS3/DirectInput, and keyboard. Confirm each mode and intended host platform on hardware.
- Target host platforms are Windows, Unix, Switch/Switch 2, PS3, iPadOS, and USB-C iOS devices; document the required mode and any compatibility limits per platform.
- Overclocking and sub-1 ms input delay are performance goals. Establish a baseline, test stability and USB behavior, and measure end-to-end latency before making either claim.

## Four-phase workflow

### 1. Schematics

- Finalize the 13/16-button variant plan and GPIO-to-action table.
- Add every fitted PCB part to the schematic, including OLED, RGB LEDs, LED level shifting, decoupling, connectors, and protection.
- Assign exact manufacturer parts, package variants, pinouts, ratings, and unique references. Check critical connections against manufacturer datasheets.
- Document the USB power tree, expected worst-case load, and firmware pin configuration.

**Exit condition:** the schematic represents the intended assembled board and its variants, with no unresolved pinout or power-budget questions.

### 2. PCB design

- Update the PCB from the schematic and reconcile all footprints, values, references, and pad-to-net assignments.
- Fit the board and controls to the mechanical drawing; check case walls, mounting holes, USB connector insertion, OLED opening, switch travel, and total height.
- Route USB, power, controls, and a true serial RGB data chain. Review return paths, decoupling placement, copper fills, and assembly access.
- Use unique references for all components and add assembly fiducials where required by the manufacturer.

**Exit condition:** the PCB and schematic describe the same populated design and the mechanical fit is documented.

### 3. ERC and DRC checks

- Run KiCad ERC and DRC on the exact schematic and PCB revision to be manufactured.
- Resolve all errors, inspect warnings, and record any intentional exclusions with reasons.
- Check schematic-to-PCB synchronization, duplicate references, pad numbers, unrouted nets, board outline, clearances, and zone fills.
- Re-run checks after any electrical or layout change; validate the button map, RGB chain, OLED interface, and USB power path manually.

**Exit condition:** no unexplained ERC/DRC findings or schematic-to-PCB mismatches remain.

### 4. BOM generation and manufacturing

- Populate manufacturer part numbers, quantities, approved alternatives, and fitted/not-fitted status for each variant.
- Export the BOM, placement files, Gerbers, and drill files from the checked revision.
- Review the fabrication layers, board dimensions, drill data, assembly preview, component orientation, and enclosure/top-plate drawings together.
- Archive the exact production outputs and firmware configuration used for the build.

**Exit condition:** an assembler can build each variant from the released files without guessing part identity, placement, or firmware mapping.

## Current known gaps

The PCB is approximately 272.6 × 171.0 mm, distinct from the enclosure target. Neither the current board nor the checked-in `order/` outputs are a release. Maintain the following decisions and status when continuing work.

### Decisions and implemented state

- The 16 action switches are `SW1`–`SW16`. Their schematic footprint selection follows the existing PCB Kailh Choc V1/V2 hot-swap geometry. The six option switches are `OPSW1`–`OPSW6`, not additional `SW` references. The switch references, five previously incorrect PCB GPIO values, and schematic paths were reconciled; keep their physical switch positions and documented GPIO assignments intact.
- The OLED is the existing I²C `HS91L02W2C01` module (`U5`), not a replacement SPI display. It appears with `R12`/`R13` (4.7 kΩ pull-ups to +3V3) under a separate “OLED status display (I2C)” schematic heading. The schematic labels connect U5 pin 1 to GND, pin 2 to +5V, pin 3 to SCL/GPIO12, and pin 4 to SDA/GPIO13. Its PCB footprint already exists. Confirm the exact module supply and I²C logic thresholds against its manufacturer documentation; do not interpret the analyzer's 5V/3.3V warning alone as proof of damage.
- `USB1` is the upstream USB-C device port. `USB2` is the single downstream USB-A port; there is no duplicate downstream schematic symbol. `USB2` uses project footprint `Type-A:C2763302` on B.Cu. Pins 1–4 have short B.Cu extensions to the prior +5V, HD−, HD+, and GND traces, respectively. `C19` is already B.Cu. The host data-line resistors `R5` and `R7` remain on F.Cu: their HD+ and HD− traces each change to B.Cu through an existing plated through-hole via (0.35 mm drill). Boot/reset switches `SW19`/`SW20` use `SW:C318884` on the PCB. The former schematic-only QSPI chip-select pull-up `R9` was intentionally removed.
- Retain all 20 PCB RGB LEDs. The agreed serial order is the LEDs at `SW1`–`SW16`, then the four top-edge LEDs from left to right; the first LED is to receive data from the existing buffer/series resistor. This is a design decision, **not an implemented chain**.

### Unresolved electrical and layout work

- The 20 RGB LEDs, 17 nearby capacitors, buffer, and series resistor remain unannotated PCB hardware absent from the schematic. All LED data input/output pads still share `DOUT` (163 tracks were observed on that net), so the intended chain is electrically invalid. Select a buffer with a verified pinout and 3.3V-input/5V-output behavior, add all parts to the schematic with unique references, split the LED data nets, then physically reroute and check every hop. Budget worst-case LED current against the upstream 500 mA fuse and all other loads.
- `USB2` VBUS and the 100 µF `C19` are tied directly to the fused upstream +5V rail. No separate downstream power switch or current limit is shown. Decide the permissible host load, inrush strategy, and fault isolation before claiming USB pass-through support. Verify USB2's new four-hole mechanical pattern, enclosure opening, and routing clearances. The host data pins are on GPIO20/21 via `R5`/`R7`; firmware must explicitly support that PIO-USB arrangement.
- The OLED has no separately shown local supply decoupler, and no project datasheet cache currently supports a verified module-level voltage/interface claim. Inspect the actual module circuitry and PCB placement before choosing a decoupling or level-shifting change.
- KiCad ERC last reported 49 violations. These include the missing `PCM_Switch_Keyboard_Hotswap_Kailh` footprint-library registration for 16 switches, power-pin-driver flags, off-grid endpoints, library-symbol mismatches, and a conflicting `FLASH_SS`/`QSPI_SS` label pair. The Type-C D+/D− “input not driven” results appear to be symbol-type artifacts because each receptacle pair is connected; triage rather than suppress them blindly. The KiCad CLI PCB DRC has exited with code 134, so no clean DRC result exists. The board analyzer also found split copper islands; refill zones and rerun checks.
- Schematic MPN and datasheet coverage is sparse. Do not claim pin-level verification, cost, stock, or manufacturing readiness without part-specific evidence. Existing Gerbers and drill files in `order/` predate these changes and must be regenerated only after synchronization, ERC/DRC, and mechanical checks pass.

### Next work sequence

1. Complete the RGB schematic and serial-chain PCB routing, including a verified driver, power distribution, and annotation.
2. Resolve USB host power/inrush and OLED supply/decoupling questions; verify the exact purchased parts and footprint pinouts.
3. Repair library links, consolidate flash net names, run ERC, refill zones, and obtain a working PCB DRC. Reconcile schematic-to-PCB and review all findings before generating new manufacturing outputs.
