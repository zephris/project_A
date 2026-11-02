# Additional manufacturer models

Retrieved 2026-10-07. These files are staged for qualification, not yet substituted into the board benches.

| Board references | Saved model | Conditions / provenance |
|---|---|---|
| C19, C43 | vendor/KEMET/T520B107M010ATE070_5V_25C_100kHz.CKT | Exact KEMET part exported from https://ksim3.kemet.com/capacitor-simulation?pn=T520B107M010ATE070 ; one capacitor, 5V bias, 25C, 100kHz center frequency. |
| C2, C11, C12, C13 | vendor/Samsung/CL05A475MP5NRN_Precise_DC0V_25degC_P.lib | Base model for ordering code CL05A475MP5NRNC / C23733; 4.7uF, X5R, 10V, 0402. 0V bias, 25C. |
| C14, C15 | vendor/Samsung/CL05A105KA5NQN_Precise_DC0V_25degC_P.lib | Base model for ordering code CL05A105KA5NQNC / C52923; 1uF, X5R, 25V, 0402. 0V bias, 25C. |

Samsung source: https://weblib.samsungsem.com/resources/file/support/software_library/Samsung_PSPICE_Static_Library.zip . Original library saved locally; extracted model bytes preserved. The stock ordering suffix C is absent from the manufacturer model names. Confirm base-code equivalence and use bias-aware models before relying on powered-board PDN predictions.

KEMET's downloaded CKT contains an RLC network and commented end marker, without an executable subcircuit wrapper. `adapters/T520B107M010ATE070_5V_25C_100kHz.lib` adds a two-terminal `.SUBCKT` wrapper with external nodes 1 and 8. Original exported file remains unchanged. No claim of broadband transient or tolerance qualification is made.

SHA256 records: additional-downloads-2026-10-07.json.

## Account access

The exact U3 candidate W25Q128JVSIQ IBIS listing requires Winbond sign-in. The Winbond registration form was opened visibly for the user: https://www.winbond.com/hq/register/?__locale=en . No account information submitted. IBIS describes IO electrical behavior, not internal flash operation or firmware execution.

## Remaining search results

- U1: Raspberry Pi official product resources and focused RP2350 model search did not expose an exact SPICE/IBIS model: https://pip.raspberrypi.com/categories/1214-rp2350 .
- U4: ST exact product CAD resources list footprints/symbols, no verified SPICE/S-parameter: https://www.st.com/en/protections-and-emi-filters/ecmf2-40a100n6.html .
- U5: Hansheng HS13L03W2C01 exact model not found; manufacturer https://www.hslcm.com was previously unreachable.
- D1–D20: OPSCO manufacturer download catalogue https://opscoled.com/index/download/ lists SK6803/05-EC15 specifications, not a verified SPICE model. The contact form is for a datasheet download, not evidence of an account-gated simulation model.
- F1: SEA&LAND/ALPHA-TOP exact SMD0805-075-12V searches did not find an electrothermal model. Manufacturer https://www.sealand-pptc.com .
- Y1: Abracon publishes ABM8-family SPICE parameter examples, but the example found is 16MHz; board ABM8-272-T3 is 12MHz. It was not substituted: https://abracon.com/Support/SPICE/Resonators/ABM8-Series%20ParameterTest%20Data_SPICE%20MODEL.pdf .
- L1: Exact Abracon AOTA-B201610S3R3-101-T search found datasheet/geometry resources, no verified nonlinear SPICE: https://abracon.com/parametric/inductors/AOTA-B201610S3R3-101-T .
- C16/C17: LCSC C1548 is Fenghua 0402CG150J500NT, not Samsung. Exact SPICE was not verified; retain the ideal 15pF approximation. Source: https://www.lcsc.com/product-detail/C1548.html .
- C41 has no selected exact MPN, so an exact supplier model cannot be selected.

Not found is not proof that private models do not exist. No alternative component or electrical design was substituted, and no supplier was contacted.

Samsung interactive precise library was attempted through direct HTTP and the observed browser download link. Neither completed; bias-dependent library remains unavailable locally. This is a download timeout, not a sign-in requirement.

Superseded download/access status: user subsequently supplied the exact U3 IBIS archive and Samsung precise interactive library plus installation guide. See user-download-intake-2026-10-07.md. The Samsung relevant models are Cadence encrypted.
