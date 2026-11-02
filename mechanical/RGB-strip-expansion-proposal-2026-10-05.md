# Optional 5V addressable case-light connector

Recommended topology: D20 DOUT -> source damping resistor -> connector DATA -> strip DIN; protected board 5V -> separately current-limited strip branch -> connector 5V; board GND -> connector GND. D20 pad 3 is currently explicitly unconnected. A schematic revision must remove that no-connect and route it to the connector; no spare MCU GPIO is needed for a serial extension.

Use a keyed three-position wire-to-board connector with a hand-solderable footprint if it will be fitted after assembly. Label 5V / DATA / GND on both assembly drawings and silkscreen, and supply a matching crimped harness. JST PH 2.0 mm is a possible family; exact JLCPCB MPN, orientation and stocked mating harness remain to be selected. There is no universal RGB-strip pin order. Place the connector where soldering access and cable strain relief are available, clear of switch bodies, screen posts, heat spreaders and gasket travel.

Provide a selectable source resistor footprint (initial engineering value 220-330 ohm, verify with chosen strip/cable); local bypass and optional bulk-capacitor footprint at strip power entry. Select capacitance against current-limit soft start and USB inrush, not a generic large-capacitor recipe. For a longer cable, use a 5V-compatible data buffer and suitable ESD protection; avoid loading D20 output with an unverified long harness. Plug/unplug with power removed unless hot-plug behavior is explicitly designed and tested.

Existing chain contains 20 LEDs. Append the strip as indices 20 onward when all existing indices 0-19 remain allocated. GP2040-CE Case RGB LEDs offers Ambient (independent case effects) and Linked modes; configure starting index and strip LED count. Same serial protocol and compatible color format are required. Stock firmware is sufficient for this supported case-LED topology.

Laptop USB power is already shared by controller, OLED, 20 board LEDs and USB authentication dongle. Strip capacity is NOT yet established: allowable strip current = accepted upstream USB budget - worst-case board/dongle current - margin. Max Brightness is not a hardware current limiter or a solution to powered idle/suspend current. Choose strip MPN and LED count before sizing the branch limit, copper, connector and fuse. Do not feed the strip from the 3.3V regulator or the limited USB_HOST_5V dongle rail. If separately powered, keep grounds common, isolate its 5V from laptop USB, and prevent data-line back-power into either unpowered side.

The current source and DFM release do not include this connector. For a retrofit to an already assembled board, a small daughterboard and strain-relieved soldered harness can access 5V/GND and D20 DOUT, but that tiny LED pad is fragile. Adding the connector footprint before fabrication is preferable.

Source: https://gp2040-ce.info/web-configurator/menu-pages/led-configuration/ ; active KiCad D20 pad/net inspection.
