# GP2040-CE power-handling review for PHBox — 2026-10-05

Reviewed latest published release v0.7.12, commit prefix `0014e4a`, downloaded
from the upstream GitHub API. This is source inspection, not a flashed-PHBox
test. Development main and submodule internals were not audited. The project
still has no validated PHBox firmware image/configuration.

## PHBox-specific findings

### USB2 EN is not a managed output in the released implementation

**Hardware revision:** the original 10 kΩ R16 discussed below was replaced by
220 kΩ on 2026-10-05 to support this weak-pull-up implementation without a
firmware patch. See [revision, corner checks and A2 limitations](../stage2_work/usb2_enable_2026-10-05/README.md).
The paragraphs below record the original-board audit.

`lib/PicoPeripherals/peripheral_usb.cpp:22–28` configures enable5v with
`gpio_set_dir(..., GPIO_IN)` and `gpio_pull_up(...)`. It does not actively
drive EN high. PHBox has a 10 kΩ EN pulldown R16, GPIO7 and a TPS2553. A weak
internal pull-up opposing that pulldown must not be assumed to reach a valid
EN voltage. Likely compatibility problem: verify EN voltage or change the
PHBox firmware to an explicitly driven output; keep the reset pulldown.
This is an inference from code and board topology, not a measured failure.

Peripheral USB setup is called at `src/gp2040.cpp:58`, before device
`tud_init` at line 286. No upstream-configured power gate, TPS2553 fault-pin
configuration, current sensing or fault/retry state machine was found in
the application/peripheral power path. `proto/config.proto:125–130` provides
only enabled, dp, enable5v and order for USBOptions. PHBox GPIO17 FAULT_N
therefore requires board-specific logic rather than setting EN alone.

Sources: [USB peripheral implementation](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/lib/PicoPeripherals/peripheral_usb.cpp),
[startup](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/src/gp2040.cpp),
[configuration schema](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/proto/config.proto).

### Brightness maximum does not cover every case-light path

Button RGB uses configured brightnessMaximum through AnimationStation.
`src/addons/neopicoleds.cpp:566–573` zeros the button brightness when suspended.
But case lights are written afterward at lines 603–612. Ambient mode uses
independent brightness parameters (and breath mode uses a 0–1 envelope),
without the button maximum or a suspend check. Linked mode uses a separate
brightness factor; `DimBrightnessTo0` zeros brightnessX, not that factor.
Thus a button Max Brightness of 127 is not a global hard 50% ceiling or
guaranteed case-light suspend blanking in this release. Confirm on hardware;
a PHBox build should clamp and blank the complete final frame for all 20 LEDs.

Sources: [RGB implementation](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/src/addons/neopicoleds.cpp),
[brightness implementation](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/src/animationstation/animationstation.cpp),
[LED configuration](https://gp2040-ce.info/web-configurator/menu-pages/led-configuration/).

### Suspend options exist but do not establish whole-board current

`src/usbdriver.cpp:55–57` sets the suspended flag. RGB blanking is optional;
OLED's optional suspended branch calls its display-driver power command
(`src/addons/display.cpp:145–151,177–182`). These paths do not physically
disconnect LED/OLED supply rails or switch off USB2. The RGB chips' powered
idle current, MCU activity and dongle load still matter. PHBox's documented
20×0.5 mA typical LED idle estimate alone is above 2.5 mA. Measure real suspend
current; board-level power gating may still be required.

Sources: [USB callbacks](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/src/usbdriver.cpp),
[display power handling](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/src/addons/display.cpp).

### Declared power differs by input mode

| Released descriptor | Declared configured current |
|---|---:|
| XInput, PS3/DInput, Switch/Switch Pro, Xbox One | 500 mA |
| Generic HID, keyboard, PS4 descriptor | 100 mA |

The byte value 50 in USB2 bMaxPower means 100 mA. Keyboard's
TUD_CONFIG_DESCRIPTOR explicitly requests 100 mA. Declare and validate the
actual permitted draw for every supported mode, including web configuration;
the laptop port's physical capacity is not a substitute. A descriptor is
a declared requirement, not an automatic current limiter.

Sources: [HID descriptor](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/headers/drivers/hid/HIDDescriptors.h),
[keyboard descriptor](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/headers/drivers/keyboard/KeyboardDescriptors.h),
[XInput descriptor](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/headers/drivers/xinput/XInputDescriptors.h),
[PS4 descriptor](https://github.com/OpenStickCommunity/GP2040-CE/blob/v0.7.12/headers/drivers/ps4/PS4Descriptors.h).

## Upstream reported problems

- [PR #1105](https://github.com/OpenStickCommunity/GP2040-CE/pull/1105): RGB
  remained off after disconnect/reconnect with suspend blanking enabled;
  merged September 2024. Release source clears the suspend flag on mount.
- [PR #1404](https://github.com/OpenStickCommunity/GP2040-CE/pull/1404): USB-host
  startup repair involving reset and a 500 ms delay; merged June 2025 and
  listed in v0.7.12. This is USB stack startup, not evidence of TPS2553
  power sequencing or fault handling.
- [v0.7.11 release warning](https://github.com/OpenStickCommunity/GP2040-CE/releases/tag/v0.7.11):
  PS4/PS5 dongle authentication can be lost during flash-saving actions,
  including LED-setting/turbo changes. Upstream disabled real-time LED saves
  in these modes and recommends changing/saving LEDs in XInput mode.
- [Issue #389](https://github.com/OpenStickCommunity/GP2040-CE/issues/389):
  historical Feather USB-host power-enable problem; closed through #439.
  It explains the option's origin, not validation of PHBox's pulldown/EN path.

The [v0.7.12 release](https://github.com/OpenStickCommunity/GP2040-CE/releases/tag/v0.7.12)
describes RP2350 support as early. The upstream FlatboxRev8 configuration is
not a PHBox-specific firmware definition: it does not set PHBox's EN/FAULT,
OLED/RGB configuration or a full power policy. USB-host enabled startup also
sets the system clock to 120 MHz, so the project's overclocking intent needs
checking against this code path.

Priority before prototype validation: actively driven GPIO7 EN with
configured/suspend/fault policy; final-frame brightness/blanking; per-mode
power descriptors; measured suspend and combined-load current. Then run
dongle start, recovery, flash-save, reconnect and sleep/resume regressions.
