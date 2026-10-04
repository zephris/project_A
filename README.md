# Project PHBox 
An attempt at an ultra-slim hitbox supporting 13/16 buttom layout, per-key lighting and minimum wired latency, all with uncompromising thinness and weight.

## Specifications
- Dimensions: 296*196*16.5mm (Clap shell customisables)
- Processor: RP2350A
- Connetivity: Wired
- Controller modes: X-input mode, Switch mode, PS3 / D-input mode, Keyboard mode
- Switch: Kailh Choc V1 (hotswappable), with compatability for soldered V2s and 5-pin profiles (Will require custom top-plate with 5-pin full-size switches).
- System compatability: Windows/Unix, Switch/Switch 2, PS3, IpadOS, iOS (USB-C based)
- Feature: 
    - OLED screen
    - Programmable key-mapping with GP-2040-CE firmware
    - Per-key RGB lighting and case-lined diffused lighting
    - Foam-lined, gasket-mounted top-plate to reduce force transfer back onto finger
    - USB-C 3.1 connectivity
    - Stealth flush-sitting passthrough port
    - overclocked for sub-1ms input delay
    - CNC'd alluminium lining plate for thermal dissipation

## TODO:

## Current KiCad project

Latest copper/via cleanup and focused JLCPCB checks: [review and recovery record](stage2_work/fill_via_cleanup_2026-10-03/README.md).

Use the root `Flatbox-rev8.kicad_pro`. The accepted PCB has four copper layers with two dedicated inner GND planes. The 2026-10-03 main-project merge passes ERC, DRC and schematic parity with zero findings and zero open connections. Validation evidence, recovery backup and remaining release checks are in [the merge record](stage2_work/main_merge_2026-10-03/README.md). Eight unnecessary routing bridges were subsequently simplified, removing 16 vias; [the bridge record](stage2_work/bridge_simplification_2026-10-03/README.md) contains the latest verification and PCB backup.


Latest power/USB routing repair and exact validation: [2026-10-04 review](stage2_work/direct_power_usb_2026-10-03/README.md).

## Testing this checkpoint on another computer

Use **KiCad 10**, including its standard symbol/footprint libraries. Open the root `Flatbox-rev8.kicad_pro`; do not open an old autosave, backup or fabrication output. Required project-local libraries and the switch 3D model are included. Some inherited optional third-party 3D model references may be unresolved unless their libraries are installed; this is not proof of mechanical clearance.

Latest accepted changes: [LX cutout, USB ESD/routing and C42](stage2_work/lx_usb_c42_2026-10-04/README.md). This checkpoint contains 146 footprints and 440 numbered pad entries. Recorded exact-main ERC, DRC, unconnected and schematic-parity findings are all zero. Rerun these checks after opening the checkout:

```sh
kicad-cli sch erc --format json -o phbox-erc.json Flatbox-rev8.kicad_sch
kicad-cli pcb drc --refill-zones --schematic-parity --format json -o phbox-drc.json Flatbox-rev8.kicad_pcb
kicad-cli sch export netlist --format kicadxml -o phbox-netlist.xml Flatbox-rev8.kicad_sch
```

On macOS, use `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` if it is not on PATH. On Windows, use the executable in the KiCad installation's `bin` directory. Review the reports, not just the command exit status. The committed reports record the originating computer and revision; they do not substitute for a fresh run elsewhere.

**Not a manufacturing or firmware release:** historical `order/`, `production/`, BOM and placement exports are stale. No PHBox-validated UF2 or completed SPICE testbench is included. USB2 is intended for a low-power authenticator dongle, not a general-purpose controller power outlet. Firmware mapping, 50% RGB brightness, authentication, suspend current, upstream power budget, USB/ESD, thermal and enclosure tests remain required. Large local candidates/recovery snapshots are deliberately excluded from Git; AGENTS.md retains their provenance for the original workstation.

## Testing methodology and future release steps

This is a validation roadmap, **not a record of completed hardware tests**. The completed checks are schematic/PCB consistency, ERC, DRC, zone refill and pad-net reconciliation. Simulation, firmware behaviour, physical measurements and manufacturing qualification remain future work.

### Configuration baseline

Record the Git commit, KiCad version, board revision, exact firmware SHA-256, exported firmware settings, host OS/console, dongle model, cable and instruments for every test run. Do not infer firmware settings from the schematic.

| Function | Intended configuration |
|---|---|
| MCU/upstream USB | Embedded RP2350A; USB1 is a USB-C **full-speed USB device**, not a USB 3.1 data link |
| OLED | Winstar WEA012864DWPP3N00003, 128×64 I²C; +3V3 supply; GPIO12 SDA / GPIO13 SCL |
| RGB | GPIO8; GRB; D1–D16 at SW1–SW16, then D17–D20 edge LEDs left-to-right; 20 total |
| Brightness | Provisional maximum 127/255 (~50%), including edge effects; verify on the actual firmware |
| 13-button mode | Disable SW6, SW7, SW16 and LED indices 5, 6, 15; same fully populated PCB as 16-button mode |
| USB2 host data | GPIO20 D+ / GPIO21 D− |
| USB2 power control | GPIO7 EN; GPIO17 active-low FAULT input; default off at reset |

USB2 is current-limited by U7/TPS2553 with 200 kΩ ILIM and two 100 µF output capacitors. Its provisional limit is about 115–159 mA, not a promise that any particular dongle works. Explicitly implement and test startup/fault handling; selecting a GP2040-CE enable pin alone does not establish it.

### 1. Software and design regression checks

- Run the KiCad commands above on the exact checkout being tested; retain JSON reports and a fresh XML netlist. Resolve every new finding or document its physical justification; do not weaken rules to obtain a pass.
- Compare symbol pins, PCB pads and actual copper for MCU power/USB, OLED SDA/SCL, LED DIN/DOUT, U6 orientation, U7 switched output and U8 ESD pinout. ERC/DRC alone cannot identify a mutually consistent but incorrect library pin map.
- Confirm zone fills and the local LX exclusion on In1.Cu/In2.Cu/B.Cu. Preserve the neighboring PGND return and connected inner ground planes.
- Keep all test artifacts under a run-specific directory, with pass/fail criteria, model assumptions, raw data and any unresolved limitations. A prior report does not validate a changed board.

### 2. Automated SPICE tests — planned, not implemented

Use separate simulation schematics/netlists so that test sources and behavioural loads cannot accidentally enter the manufacturing schematic. KiCad uses ngspice; batch runs can be driven by a Python/pytest harness and SPICE `.meas` results. Begin with [TI's unencrypted TPS2553 transient model](https://www.ti.com/product/TPS2553#design-development), verify model-pin mapping and ngspice compatibility, and reproduce its reference test before applying it to PHBox.

| Testbench | Sweeps and measurements |
|---|---|
| USB2 startup | Supply ramp, EN timing, 160/200/240 µF output bank, unloaded and representative dongle loads; output rise time, current and FAULT duration |
| USB2 overload/recovery | Loads below/above the limit; output voltage, limiting and recovery after fault removal |
| Shared +5V supply | Cable/source resistance, RGB pulsed-current loads and host hot-plugging; supply minima and settling |
| 3.3V/OLED supply | Startup and load steps using an appropriate regulator model; rail limits and transient response |
| Bypass/data networks | Effective capacitance, ESR, estimated trace/via R/L/C and suitable driver/input models; impedance, ringing and settling |

Use datasheet bounds and measured loads when available; distinguish typical, worst-case and assumed values. Include MLCC bias effects and component tolerances rather than relying on ideal nominal capacitors. A Monte Carlo sample is not a guaranteed worst-case bound. Setting `.temp` does not simulate enclosure heating or self-heating. PCB parasitics are not automatically extracted accurately merely by opening the board in KiCad.

Define assertions from the actual receiving-device voltage/timing limits and the selected models. Do not claim RP2350 firmware execution, regulator-loop stability, USB compliance or ESD survival from generic behavioural models. The present repository has **no complete SPICE test suite**. See [KiCad's simulator documentation](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#simulator).

### 3. Prototype bring-up and power measurements

1. Inspect assembly, polarity and solder joints; check resistance between each rail and GND before power. Support the OLED mechanically; its electrical leads are not mounting posts.
2. Use a current-limited supply through the intended upstream power path, with RGB and USB2 initially off. Never tie a bench supply to a computer's VBUS without a suitable isolated injection arrangement.
3. Verify +5V, +3V3 and the configured MCU core supply; check startup/ripple with short oscilloscope probe returns. Then enable OLED, RGB and USB2 separately and record their incremental loads.
4. Capture upstream current and rail voltages during enumeration, OLED illumination, all-white RGB at 127/255, animation transitions, dongle hot-plugging and repeated boot cycles. A slow USB meter cannot establish peak current or inrush compliance.
5. Use a controlled electronic load for USB2 overload/recovery testing. Capture U7 IN/OUT, EN and FAULT; distinguish legitimate reservoir charging from a sustained fault. Verify the dongle also starts successfully at the low current-limit corner.
6. Test actual USB suspend/resume, not just user inactivity or black LEDs. The existing ~10 mA typical LED-idle estimate is already above the 2.5 mA USB suspend target; power gating or a verified low-power solution may require a hardware revision.

The provisional 500 mA average-current budget is **not closed by measurement**. RGB PWM peaks, upstream USB power declaration/configuration, cable drop, startup and fuse derating remain checks. Stop on abnormal current, temperature or rail collapse; do not use an uncontrolled wire short as a fault test.

### 4. Firmware and interoperability tests

- Verify each action/option button, simultaneous presses, SOCD behaviour and both 13/16-button modes. Confirm disabled buttons/LEDs stay disabled after reboot.
- Exercise each LED individually and solid red/green/blue to verify index/colour order; verify OLED refresh and button activity together.
- Test enumeration, repeated reconnects and suspend/resume on the intended operating systems, both USB-C cable orientations and representative compliant cables.
- Use a Python/pytest harness with HIDAPI in a supported HID mode for automated report checks. End-to-end input testing needs real button stimulation; software-generated input on the PC does not test the PCB contacts. Do not assume HID tooling tests XInput modes identically.
- Use Wireshark/USBPcap on Windows or usbmon on Linux for PC-side protocol diagnostics. The PC cannot directly capture the USB2 dongle bus behind the MCU; use firmware logs or an inline USB protocol analyzer for that side.
- Test the actual authenticator and target console over extended sessions, including unplug/replug and recovery. Successful PC enumeration is not proof of console authentication or official platform approval.
- Measure physical-input-to-host-report latency with an external stimulus/time reference; USB polling interval alone does not establish end-to-end latency.

Tools: [HIDAPI](https://github.com/libusb/hidapi), [pytest](https://docs.pytest.org/en/stable/), [Wireshark USB capture](https://wiki.wireshark.org/CaptureSetup/USB), [USB-IF protocol/electrical tools](https://www.usb.org/compliancetools). USB3CV can test USB 2.0 devices, but use a dedicated test computer/controller because it takes over the host controller.

### 5. Physical qualification

- Check regulator startup/ripple and core-rail load transients. The LX keepout is a layout improvement, not proof of regulator stability or reduced emissions.
- Test the assembled enclosure at room temperature and the specified **60 °C maximum ambient** until temperatures stabilize. Record fuse, regulator, U7 and MCU temperatures/rail behaviour. Surface temperature is not junction temperature; do not credit the aluminium plate as cooling without verified thermal coupling.
- Obtain factory stackup/impedance data or a coupon; obtain appropriate full-speed USB waveform/eye measurements using a suitable scope, probe and fixture. Packet captures and matched via counts do not establish 90 Ω or electrical compliance.
- Use a competent lab for controlled ESD and applicable emissions/immunity testing of the assembled enclosure and connectors. Do not substitute improvised static shocks for the specified test method.
- Verify actual switch housing/keycap light paths, solder access, OLED standoffs/window, USB insertion clearance, insulating layers, screw/hole clearances and the total enclosure stack. Component bodies/courtyards retain 2.5 mm PCB-edge clearance except USB1 and the four edge LEDs; unresolved mounting-hole exceptions must be explicitly approved.

### 6. Manufacturing and release gate

1. Freeze one reviewed source revision. Manufacture one fully populated 16-button board; 13-button operation is a firmware/mechanical-cover mode, not a reduced BOM.
2. Recheck exact MPN, package, footprint/pinout, polarity, lifecycle and current supplier availability. For JLCPCB, verify each LCSC identity and Basic/Extended status at ordering time. Confirm the SK6805-EC15 purchased variant against the `-001` datasheet; generic substitutes are not automatically acceptable.
3. Agree the four-layer stackup, copper weights, impedance geometry, drill/via limits, soldermask, stencil/reflow process, double-sided assembly and mechanical tolerances with the manufacturer. Review exposed-pad soldering, via treatment, 0402 access, USB2 on B.Cu and opposite-side U8/C44 placement.
4. Regenerate BOM, top/bottom placement files, all four copper-layer Gerbers, masks, silkscreens, Edge.Cuts and plated/non-plated drills **from that same revision**. Inspect them in an independent viewer; verify orientation, mirror conventions, drill alignment and placement datum. Never reuse the historical `order/` or `production/` exports.
5. Review the assembler's BOM/CPL matching and visual assembly preview. Check every polarized IC/diode/capacitor, connector and LED rotation; retain explicit DNP/exclusion and hand-assembly notes. Include OLED mounting hardware and other non-schematic mechanical items separately.
6. Build a small first-article batch and execute the above tests before a larger production run. Clearly distinguish a risk-accepted engineering prototype order from a qualified production release.
7. Archive source commit, tool versions, reports/raw captures, approved parts/alternatives, exact fabrication files, assembly preview, mechanical drawings, firmware image/hash and exported settings for both modes. Attach a release manifest/checksums so the build can be reproduced.

Manufacturing exit requires reviewed electrical/physical checks, proven power/suspend/thermal behaviour, verified mechanical fit, compatible firmware/dongle operation and coherent assembly outputs. Clean ERC/DRC alone is not manufacturing sign-off.
