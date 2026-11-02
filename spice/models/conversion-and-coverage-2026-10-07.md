# Samsung conversion and remaining model coverage

Reviewed 2026-10-07. Research only; no simulator installation, decryption, board edits or new simulation results.

## Samsung / KiCad 10

The three downloaded precise interactive libraries contain `$CDNENCSTART_ADV2` encrypted payloads. Native KiCad/ngspice cannot load them. Renaming files, importing PSpice symbols or enabling ngspice PSpice compatibility does not decrypt them. KiCad's PSpice compatibility is syntax support, not a Cadence execution engine.

Sources: https://docs.kicad.org/10.0/en/eeschema/eeschema.html ; https://ngspice.sourceforge.io/modelparams.html ; https://www.kicad.org/discover/spice/

The supported practical route is Samsung's unencrypted fixed-condition Simple/Precise models. Existing local static models are 0V/25C, so they must not represent powered-board effective capacitance without qualification. Obtain fixed-condition exports at each rail's actual bias and temperature where Samsung's tool offers them, or request those exports from Samsung. Alternatively simulate the interactive library separately in compatible Cadence PSpice. Installation instructions are for PSpice, not KiCad.

Samsung model types: https://weblib.samsungsem.com/resources/file/SPICE_Library_Guide.pdf ; library portal: https://weblib.samsungsem.com/index.do?designSupportTools=Pspice

After obtaining plaintext: preserve original vendor bytes; select the correct base part and conditions; inspect .SUBCKT terminal order; enable PSpice compatibility if needed; repair only demonstrated syntax differences in a separate adapter; test impedance versus frequency and operating conditions against Samsung curves before integrating powered-board benches. Bias-dependent behavioral files additionally require DC-bias sweep and transient checks. Decryption alone would not establish ngspice compatibility or accuracy.

An unofficial candidate exists: author Joe Sylve reported SpiceCrypt v2 support for all six PSpice encryption modes. However https://github.com/jtsylve/spice-crypt returned HTTP404 during this review. Its implementation and operation on these Samsung files could not be verified; no installer, mirror or decryption was used. Treat this as an unavailable, unqualified candidate, not a working project dependency. Primary author statement: https://news.ycombinator.com/item?id=47439949 .

No verified KiCad plugin providing Cadence PSpice execution/encrypted-library support was found. The third-party KiCad SPICE symbol libraries found are symbol/model collections, not replacement engines: https://github.com/ryansturmer/kicad-spice-library . Official addon entry points: https://addons.kicad.org/ ; https://dev-docs.kicad.org/en/addons/index.html . This is a search finding, not proof that no external integration exists.

## Coverage audit

| References / part | Current files and remaining gap |
|---|---|
| U2 TLV73333P | TI plaintext transient model present and used; vendor-header discrepancy and wider qualification remain documented. |
| U6 SN74LV1T34 | TI plaintext SPICE and IBIS present; SPICE used in suite. |
| U7 TPS2553 | TI plaintext model present; documented ngspice XNOR adapter used. |
| U8 USBLC6-2SC6 | ST plaintext PSpice present and used. |
| D21 ESDA7P120-1U1M | ST plaintext PSpice present and used. |
| Samsung 100nF, 1uF, 4.7uF | Plaintext static and encrypted interactive files present; powered bias-aware ngspice coverage remains incomplete. |
| C19/C43 KEMET T520B107M010ATE070 | Exact 5V/25C/100kHz exported RLC file and subcircuit adapter present, staged rather than integrated. |
| U3 W25Q128JVSIQ | Exact IBIS present; no downloaded internal/functional PSpice model. Manufacturer site lists model categories, which alone does not establish an exact available SPICE file. |
| U1 RP2350 | No exact public PSpice file found; retain bounded load approximation. |
| U4 ECMF2-40A100N6 | No exact PSpice or S-parameter file verified; exact product CAD resources are not simulation models. |
| U5 HS13L03W2C01 | No exact PSpice file found; bounded display load remains necessary. |
| D1–D20 SK6805-EC15 | No exact PSpice file found; manufacturer catalogue offers specifications. Use bounded aggregate load. |
| F1 SMD0805-075-12V | No exact electrothermal PSpice file found; resistance approximation cannot establish trip/recovery behavior. |
| Y1 ABM8-272-T3 12MHz | ABM8 family model example found for 16MHz, not an exact substitute. Exact motional parameters remain missing. |
| L1 AOTA-B201610S3R3-101-T | No exact nonlinear PSpice file verified; L/DCR approximation does not cover saturation. |
| C16/C17 Fenghua 0402CG150J500NT | No exact PSpice file found; ideal 15pF C0G approximation remains. These are not Samsung parts. |
| C41 | Exact MPN not selected; no exact supplier model can be chosen. |
| Resistors, switches, connectors | Built-in resistor and contact/parasitic models suffice for present low-frequency benches; individual vendor PSpice files are not required. |

Manufacturer search links and earlier provenance are recorded in additional-downloads-2026-10-07.md. Rechecked exact-part searches did not close the outstanding gaps. Absence from public searches does not establish absence of private vendor models.

Relevant primary sources: https://pip.raspberrypi.com/categories/1214-rp2350 ; https://www.st.com/en/protections-and-emi-filters/ecmf2-40a100n6.html ; https://opscoled.com/index/download/ ; https://www.sealand-pptc.com ; https://abracon.com/parametric/inductors/AOTA-B201610S3R3-101-T ; https://abracon.com/Support/SPICE/Resonators/ABM8-Series%20ParameterTest%20Data_SPICE%20MODEL.pdf ; https://www.winbond.com/hq/support/documentation/?__locale=en ; https://ksim3.kemet.com/capacitor-simulation?pn=T520B107M010ATE070
