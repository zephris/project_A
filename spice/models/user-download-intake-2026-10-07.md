# User-supplied download intake

The following files were verified in Downloads and copied into the project's vendor-model folders. Original downloads were left untouched.

## U3

`vendor/Winbond/w25q128jvsiq.zip` contains `w25q128jvsiq.ibs`. Its declared component is W25Q128JVSIQ, package 8-pin SOIC 208-mil, IBIS3.2 revision1.0, dated2015-06-12. Pins are CS1, IO1/DO2, IO2/WP3, GND4, IO0/DI5, SCK6, IO3/HOLD7, VCC8. It includes package parasitics, clamp curves and input/output model data. This closes the exact U3 IBIS-download gap, but not the missing internal flash SPICE/functional model. Model data remains unqualified for a board-connected signal-integrity bench.

## Samsung

Saved full `vendor/Samsung/Samsung_PSPICE_Precise_Intr_Library.zip` and `Samsung_Component_Library_Install_Guide_for_PSpice.pdf`.

Extracted the following manufacturer base-part models:

- CL05B104KO5NNN: 100nF bank.
- CL05A475MP5NRN: C2/C11/C12/C13, 4.7uF.
- CL05A105KA5NQN: C14/C15, 1uF.

All three precise interactive files contain `**$ENCRYPTED_LIB` and `$CDNENCSTART_ADV2` markers. They are Cadence PSpice-encrypted models and cannot be used directly by KiCad/ngspice. Installing the library following its PSpice guide does not add a decryption capability to KiCad. No attempt was made to decrypt or modify encrypted payloads, and no PSpice installation or global configuration was changed.

Use the existing unencrypted static models in KiCad for their specified 0V-bias/25C comparison, or qualify these interactive models in compatible Cadence PSpice. Ordering-code suffix equivalence and operating conditions still require review. The full Samsung archive also contains other parts which have not been selected for this PCB.

Hashes and status: `user-download-intake-2026-10-07.json`. The new files are archived, not added as runnable board-suite models. Existing runnable benches are unchanged.
