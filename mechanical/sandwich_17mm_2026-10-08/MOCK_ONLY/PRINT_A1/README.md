# Bambu A1 PLA mock kit â€” one part per file

Updated 18 October 2026. **Every project and sliced file contains one mock part or one quarter-section.** Each physical component is a separate top-level model with its own name; no assembly wrapper combines them. Printer: Bambu Lab A1, 256 Ã— 256 mm, AMS Lite, PLA. Nothing has been sent to a printer.

Download `A1_PLA_fitment_kit.zip`. `parts/<part-name>.3mf` is an editable unsliced project; `sliced/<part-name>.gcode.3mf` is its validated Bambu Studio slice. Print each required file once. Identical repeated mounts retain separate numbered filenames so the full assembly quantity is explicit.

## Oversized parts

Six full parts exceed the usable A1 bed: PCB surrogate, top acrylic surrogate, bottom acrylic surrogate, top spacer, bottom spacer and switch plate. Each is divided into **four quarter-sections**, with a separate file for every section. No full-size alternatives are in this package. The largest section is 146.3 Ã— 95.5 mm. There is no scaling.

Quarter seams have no interlocking joints. Reconstruct each original part on a flat jig, using the [source manifest](../manifest.json) bounds to identify the original section positions; tape the reverse faces temporarily. Some sections have disconnected islands belonging to that same original part: preserve their positions on the jig. They cannot reproduce full-panel stiffness or support fastening loads.

## Print order and direct file links

### 1. Initial dimension trial â€” 0.4 mm nozzle

Print these small parts first, then measure holes, seats and option-cap travel. Do not print a second copy when these names appear in step 3.

- [screen_frame.gcode.3mf](sliced/screen_frame.gcode.3mf) â€” [editable screen_frame.3mf](parts/screen_frame.3mf).
- [printed_screen_stop_1_3mm.gcode.3mf](sliced/printed_screen_stop_1_3mm.gcode.3mf) â€” [editable printed_screen_stop_1_3mm.3mf](parts/printed_screen_stop_1_3mm.3mf).
- [OPSW1_captive_cap_H5_trial.gcode.3mf](sliced/OPSW1_captive_cap_H5_trial.gcode.3mf) â€” [editable OPSW1_captive_cap_H5_trial.3mf](parts/OPSW1_captive_cap_H5_trial.3mf).

Check a real Choc V2 switch with [switch_coupon.step](../../STEP/switch_coupon.step) before printing the full switch-plate sections. This separate STEP coupon must be imported and sliced; it is not pre-sliced in this package.

### 2. Simple panel, PCB and case-column surrogates â€” 0.6 mm nozzle

| Print filename (sliced) | Editable project | PLA | Estimated time |
|---|---|---:|---:|
| [PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_1.gcode.3mf](sliced/PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_1.gcode.3mf) | [PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_1.3mf](parts/PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_1.3mf) | 21.13 g | 39 min |
| [PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_2.gcode.3mf](sliced/PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_2.gcode.3mf) | [PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_2.3mf](parts/PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_2.3mf) | 21.17 g | 39 min |
| [PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_3.gcode.3mf](sliced/PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_3.gcode.3mf) | [PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_3.3mf](parts/PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_3.3mf) | 21.48 g | 44 min |
| [PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_4.gcode.3mf](sliced/PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_4.gcode.3mf) | [PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_4.3mf](parts/PCB_SELECTED_ENVELOPES_SURROGATE_QUARTER_4.3mf) | 21.49 g | 43 min |
| [top_acrylic_SURROGATE_QUARTER_1.gcode.3mf](sliced/top_acrylic_SURROGATE_QUARTER_1.gcode.3mf) | [top_acrylic_SURROGATE_QUARTER_1.3mf](parts/top_acrylic_SURROGATE_QUARTER_1.3mf) | 21.97 g | 42 min |
| [top_acrylic_SURROGATE_QUARTER_2.gcode.3mf](sliced/top_acrylic_SURROGATE_QUARTER_2.gcode.3mf) | [top_acrylic_SURROGATE_QUARTER_2.3mf](parts/top_acrylic_SURROGATE_QUARTER_2.3mf) | 20.47 g | 40 min |
| [top_acrylic_SURROGATE_QUARTER_3.gcode.3mf](sliced/top_acrylic_SURROGATE_QUARTER_3.gcode.3mf) | [top_acrylic_SURROGATE_QUARTER_3.3mf](parts/top_acrylic_SURROGATE_QUARTER_3.3mf) | 21.68 g | 43 min |
| [top_acrylic_SURROGATE_QUARTER_4.gcode.3mf](sliced/top_acrylic_SURROGATE_QUARTER_4.gcode.3mf) | [top_acrylic_SURROGATE_QUARTER_4.3mf](parts/top_acrylic_SURROGATE_QUARTER_4.3mf) | 21.50 g | 42 min |
| [bottom_acrylic_SURROGATE_QUARTER_1.gcode.3mf](sliced/bottom_acrylic_SURROGATE_QUARTER_1.gcode.3mf) | [bottom_acrylic_SURROGATE_QUARTER_1.3mf](parts/bottom_acrylic_SURROGATE_QUARTER_1.3mf) | 25.80 g | 46 min |
| [bottom_acrylic_SURROGATE_QUARTER_2.gcode.3mf](sliced/bottom_acrylic_SURROGATE_QUARTER_2.gcode.3mf) | [bottom_acrylic_SURROGATE_QUARTER_2.3mf](parts/bottom_acrylic_SURROGATE_QUARTER_2.3mf) | 25.83 g | 46 min |
| [bottom_acrylic_SURROGATE_QUARTER_3.gcode.3mf](sliced/bottom_acrylic_SURROGATE_QUARTER_3.gcode.3mf) | [bottom_acrylic_SURROGATE_QUARTER_3.3mf](parts/bottom_acrylic_SURROGATE_QUARTER_3.3mf) | 25.82 g | 46 min |
| [bottom_acrylic_SURROGATE_QUARTER_4.gcode.3mf](sliced/bottom_acrylic_SURROGATE_QUARTER_4.gcode.3mf) | [bottom_acrylic_SURROGATE_QUARTER_4.3mf](parts/bottom_acrylic_SURROGATE_QUARTER_4.3mf) | 25.79 g | 46 min |
| [acrylic_case_post_1_12mm_AF5_SURROGATE.gcode.3mf](sliced/acrylic_case_post_1_12mm_AF5_SURROGATE.gcode.3mf) | [acrylic_case_post_1_12mm_AF5_SURROGATE.3mf](parts/acrylic_case_post_1_12mm_AF5_SURROGATE.3mf) | 0.38 g | 12 min |
| [acrylic_case_post_2_12mm_AF5_SURROGATE.gcode.3mf](sliced/acrylic_case_post_2_12mm_AF5_SURROGATE.gcode.3mf) | [acrylic_case_post_2_12mm_AF5_SURROGATE.3mf](parts/acrylic_case_post_2_12mm_AF5_SURROGATE.3mf) | 0.38 g | 12 min |
| [acrylic_case_post_3_12mm_AF5_SURROGATE.gcode.3mf](sliced/acrylic_case_post_3_12mm_AF5_SURROGATE.gcode.3mf) | [acrylic_case_post_3_12mm_AF5_SURROGATE.3mf](parts/acrylic_case_post_3_12mm_AF5_SURROGATE.3mf) | 0.38 g | 12 min |
| [acrylic_case_post_4_12mm_AF5_SURROGATE.gcode.3mf](sliced/acrylic_case_post_4_12mm_AF5_SURROGATE.gcode.3mf) | [acrylic_case_post_4_12mm_AF5_SURROGATE.3mf](parts/acrylic_case_post_4_12mm_AF5_SURROGATE.3mf) | 0.38 g | 12 min |
| [acrylic_case_post_5_12mm_AF5_SURROGATE.gcode.3mf](sliced/acrylic_case_post_5_12mm_AF5_SURROGATE.gcode.3mf) | [acrylic_case_post_5_12mm_AF5_SURROGATE.3mf](parts/acrylic_case_post_5_12mm_AF5_SURROGATE.3mf) | 0.38 g | 12 min |
| [acrylic_case_post_6_12mm_AF5_SURROGATE.gcode.3mf](sliced/acrylic_case_post_6_12mm_AF5_SURROGATE.gcode.3mf) | [acrylic_case_post_6_12mm_AF5_SURROGATE.3mf](parts/acrylic_case_post_6_12mm_AF5_SURROGATE.3mf) | 0.38 g | 12 min |
| [acrylic_case_post_7_12mm_AF5_SURROGATE.gcode.3mf](sliced/acrylic_case_post_7_12mm_AF5_SURROGATE.gcode.3mf) | [acrylic_case_post_7_12mm_AF5_SURROGATE.3mf](parts/acrylic_case_post_7_12mm_AF5_SURROGATE.3mf) | 0.38 g | 12 min |
| [acrylic_case_post_8_12mm_AF5_SURROGATE.gcode.3mf](sliced/acrylic_case_post_8_12mm_AF5_SURROGATE.gcode.3mf) | [acrylic_case_post_8_12mm_AF5_SURROGATE.3mf](parts/acrylic_case_post_8_12mm_AF5_SURROGATE.3mf) | 0.38 g | 12 min |

### 3. Spacers, switch plate, heatsink and mounting parts â€” 0.4 mm nozzle

| Print filename (sliced) | Editable project | PLA | Estimated time |
|---|---|---:|---:|
| [top_spacer_QUARTER_1.gcode.3mf](sliced/top_spacer_QUARTER_1.gcode.3mf) | [top_spacer_QUARTER_1.3mf](parts/top_spacer_QUARTER_1.3mf) | 10.75 g | 31 min |
| [top_spacer_QUARTER_2.gcode.3mf](sliced/top_spacer_QUARTER_2.gcode.3mf) | [top_spacer_QUARTER_2.3mf](parts/top_spacer_QUARTER_2.3mf) | 10.76 g | 31 min |
| [top_spacer_QUARTER_3.gcode.3mf](sliced/top_spacer_QUARTER_3.gcode.3mf) | [top_spacer_QUARTER_3.3mf](parts/top_spacer_QUARTER_3.3mf) | 10.52 g | 33 min |
| [top_spacer_QUARTER_4.gcode.3mf](sliced/top_spacer_QUARTER_4.gcode.3mf) | [top_spacer_QUARTER_4.3mf](parts/top_spacer_QUARTER_4.3mf) | 9.58 g | 30 min |
| [bottom_spacer_QUARTER_1.gcode.3mf](sliced/bottom_spacer_QUARTER_1.gcode.3mf) | [bottom_spacer_QUARTER_1.3mf](parts/bottom_spacer_QUARTER_1.3mf) | 23.91 g | 50 min |
| [bottom_spacer_QUARTER_2.gcode.3mf](sliced/bottom_spacer_QUARTER_2.gcode.3mf) | [bottom_spacer_QUARTER_2.3mf](parts/bottom_spacer_QUARTER_2.3mf) | 22.82 g | 49 min |
| [bottom_spacer_QUARTER_3.gcode.3mf](sliced/bottom_spacer_QUARTER_3.gcode.3mf) | [bottom_spacer_QUARTER_3.3mf](parts/bottom_spacer_QUARTER_3.3mf) | 15.85 g | 40 min |
| [bottom_spacer_QUARTER_4.gcode.3mf](sliced/bottom_spacer_QUARTER_4.gcode.3mf) | [bottom_spacer_QUARTER_4.3mf](parts/bottom_spacer_QUARTER_4.3mf) | 21.89 g | 50 min |
| [OLED_MODULE_PCB_SURROGATE.gcode.3mf](sliced/OLED_MODULE_PCB_SURROGATE.gcode.3mf) | [OLED_MODULE_PCB_SURROGATE.3mf](parts/OLED_MODULE_PCB_SURROGATE.3mf) | 1.81 g | 12 min |
| [switch_plate_QUARTER_1.gcode.3mf](sliced/switch_plate_QUARTER_1.gcode.3mf) | [switch_plate_QUARTER_1.3mf](parts/switch_plate_QUARTER_1.3mf) | 12.74 g | 35 min |
| [switch_plate_QUARTER_2.gcode.3mf](sliced/switch_plate_QUARTER_2.gcode.3mf) | [switch_plate_QUARTER_2.3mf](parts/switch_plate_QUARTER_2.3mf) | 12.58 g | 34 min |
| [switch_plate_QUARTER_3.gcode.3mf](sliced/switch_plate_QUARTER_3.gcode.3mf) | [switch_plate_QUARTER_3.3mf](parts/switch_plate_QUARTER_3.3mf) | 12.94 g | 37 min |
| [switch_plate_QUARTER_4.gcode.3mf](sliced/switch_plate_QUARTER_4.gcode.3mf) | [switch_plate_QUARTER_4.3mf](parts/switch_plate_QUARTER_4.3mf) | 12.31 g | 37 min |
| [screen_frame.gcode.3mf](sliced/screen_frame.gcode.3mf) | [screen_frame.3mf](parts/screen_frame.3mf) | 0.61 g | 10 min |
| [aluminium_heatsink_SURROGATE.gcode.3mf](sliced/aluminium_heatsink_SURROGATE.gcode.3mf) | [aluminium_heatsink_SURROGATE.3mf](parts/aluminium_heatsink_SURROGATE.3mf) | 4.79 g | 24 min |
| [printed_screen_stop_1_3mm.gcode.3mf](sliced/printed_screen_stop_1_3mm.gcode.3mf) | [printed_screen_stop_1_3mm.3mf](parts/printed_screen_stop_1_3mm.3mf) | 0.15 g | 9 min |
| [printed_screen_rear_tapped_cap_1_M2.gcode.3mf](sliced/printed_screen_rear_tapped_cap_1_M2.gcode.3mf) | [printed_screen_rear_tapped_cap_1_M2.3mf](parts/printed_screen_rear_tapped_cap_1_M2.3mf) | 0.09 g | 8 min |
| [printed_screen_stop_2_3mm.gcode.3mf](sliced/printed_screen_stop_2_3mm.gcode.3mf) | [printed_screen_stop_2_3mm.3mf](parts/printed_screen_stop_2_3mm.3mf) | 0.15 g | 9 min |
| [printed_screen_rear_tapped_cap_2_M2.gcode.3mf](sliced/printed_screen_rear_tapped_cap_2_M2.gcode.3mf) | [printed_screen_rear_tapped_cap_2_M2.3mf](parts/printed_screen_rear_tapped_cap_2_M2.3mf) | 0.09 g | 8 min |
| [printed_screen_stop_3_3mm.gcode.3mf](sliced/printed_screen_stop_3_3mm.gcode.3mf) | [printed_screen_stop_3_3mm.3mf](parts/printed_screen_stop_3_3mm.3mf) | 0.15 g | 9 min |
| [printed_screen_rear_tapped_cap_3_M2.gcode.3mf](sliced/printed_screen_rear_tapped_cap_3_M2.gcode.3mf) | [printed_screen_rear_tapped_cap_3_M2.3mf](parts/printed_screen_rear_tapped_cap_3_M2.3mf) | 0.09 g | 8 min |
| [printed_screen_stop_4_3mm.gcode.3mf](sliced/printed_screen_stop_4_3mm.gcode.3mf) | [printed_screen_stop_4_3mm.3mf](parts/printed_screen_stop_4_3mm.3mf) | 0.15 g | 9 min |
| [printed_screen_rear_tapped_cap_4_M2.gcode.3mf](sliced/printed_screen_rear_tapped_cap_4_M2.gcode.3mf) | [printed_screen_rear_tapped_cap_4_M2.3mf](parts/printed_screen_rear_tapped_cap_4_M2.3mf) | 0.09 g | 8 min |
| [insulating_plate_stop_H1.gcode.3mf](sliced/insulating_plate_stop_H1.gcode.3mf) | [insulating_plate_stop_H1.3mf](parts/insulating_plate_stop_H1.3mf) | 0.32 g | 12 min |
| [insulating_plate_rear_tapped_cap_H1.gcode.3mf](sliced/insulating_plate_rear_tapped_cap_H1.gcode.3mf) | [insulating_plate_rear_tapped_cap_H1.3mf](parts/insulating_plate_rear_tapped_cap_H1.3mf) | 0.17 g | 9 min |
| [insulating_plate_stop_H2.gcode.3mf](sliced/insulating_plate_stop_H2.gcode.3mf) | [insulating_plate_stop_H2.3mf](parts/insulating_plate_stop_H2.3mf) | 0.32 g | 12 min |
| [insulating_plate_rear_tapped_cap_H2.gcode.3mf](sliced/insulating_plate_rear_tapped_cap_H2.gcode.3mf) | [insulating_plate_rear_tapped_cap_H2.3mf](parts/insulating_plate_rear_tapped_cap_H2.3mf) | 0.17 g | 9 min |
| [insulating_plate_stop_H3.gcode.3mf](sliced/insulating_plate_stop_H3.gcode.3mf) | [insulating_plate_stop_H3.3mf](parts/insulating_plate_stop_H3.3mf) | 0.32 g | 12 min |
| [insulating_plate_rear_tapped_cap_H3.gcode.3mf](sliced/insulating_plate_rear_tapped_cap_H3.gcode.3mf) | [insulating_plate_rear_tapped_cap_H3.3mf](parts/insulating_plate_rear_tapped_cap_H3.3mf) | 0.17 g | 9 min |
| [custom_POM_stop_H5.gcode.3mf](sliced/custom_POM_stop_H5.gcode.3mf) | [custom_POM_stop_H5.3mf](parts/custom_POM_stop_H5.3mf) | 0.37 g | 13 min |
| [custom_POM_stop_H7.gcode.3mf](sliced/custom_POM_stop_H7.gcode.3mf) | [custom_POM_stop_H7.3mf](parts/custom_POM_stop_H7.3mf) | 0.37 g | 13 min |
| [custom_POM_stop_H12.gcode.3mf](sliced/custom_POM_stop_H12.gcode.3mf) | [custom_POM_stop_H12.3mf](parts/custom_POM_stop_H12.3mf) | 0.12 g | 9 min |
| [insulating_support_washer_H5.gcode.3mf](sliced/insulating_support_washer_H5.gcode.3mf) | [insulating_support_washer_H5.3mf](parts/insulating_support_washer_H5.3mf) | 0.09 g | 7 min |
| [insulating_support_washer_H7.gcode.3mf](sliced/insulating_support_washer_H7.gcode.3mf) | [insulating_support_washer_H7.3mf](parts/insulating_support_washer_H7.3mf) | 0.09 g | 7 min |
| [insulating_support_washer_H12.gcode.3mf](sliced/insulating_support_washer_H12.gcode.3mf) | [insulating_support_washer_H12.3mf](parts/insulating_support_washer_H12.3mf) | 0.08 g | 7 min |
| [rear_insulating_washer_H5.gcode.3mf](sliced/rear_insulating_washer_H5.gcode.3mf) | [rear_insulating_washer_H5.3mf](parts/rear_insulating_washer_H5.3mf) | 0.08 g | 7 min |
| [custom_POM_retainer_thread_not_modeled_H5.gcode.3mf](sliced/custom_POM_retainer_thread_not_modeled_H5.gcode.3mf) | [custom_POM_retainer_thread_not_modeled_H5.3mf](parts/custom_POM_retainer_thread_not_modeled_H5.3mf) | 0.17 g | 9 min |
| [rear_insulating_washer_H7.gcode.3mf](sliced/rear_insulating_washer_H7.gcode.3mf) | [rear_insulating_washer_H7.3mf](parts/rear_insulating_washer_H7.3mf) | 0.08 g | 7 min |
| [custom_POM_retainer_thread_not_modeled_H7.gcode.3mf](sliced/custom_POM_retainer_thread_not_modeled_H7.gcode.3mf) | [custom_POM_retainer_thread_not_modeled_H7.3mf](parts/custom_POM_retainer_thread_not_modeled_H7.3mf) | 0.17 g | 9 min |
| [rear_insulating_washer_H12.gcode.3mf](sliced/rear_insulating_washer_H12.gcode.3mf) | [rear_insulating_washer_H12.3mf](parts/rear_insulating_washer_H12.3mf) | 0.08 g | 7 min |
| [custom_POM_retainer_thread_not_modeled_H12.gcode.3mf](sliced/custom_POM_retainer_thread_not_modeled_H12.gcode.3mf) | [custom_POM_retainer_thread_not_modeled_H12.3mf](parts/custom_POM_retainer_thread_not_modeled_H12.3mf) | 0.10 g | 8 min |
| [OPSW1_captive_cap_H5_trial.gcode.3mf](sliced/OPSW1_captive_cap_H5_trial.gcode.3mf) | [OPSW1_captive_cap_H5_trial.3mf](parts/OPSW1_captive_cap_H5_trial.3mf) | 0.39 g | 14 min |
| [OPSW2_captive_cap_H5_trial.gcode.3mf](sliced/OPSW2_captive_cap_H5_trial.gcode.3mf) | [OPSW2_captive_cap_H5_trial.3mf](parts/OPSW2_captive_cap_H5_trial.3mf) | 0.39 g | 14 min |
| [OPSW3_captive_cap_H5_trial.gcode.3mf](sliced/OPSW3_captive_cap_H5_trial.gcode.3mf) | [OPSW3_captive_cap_H5_trial.3mf](parts/OPSW3_captive_cap_H5_trial.3mf) | 0.39 g | 14 min |
| [OPSW4_captive_cap_H5_trial.gcode.3mf](sliced/OPSW4_captive_cap_H5_trial.gcode.3mf) | [OPSW4_captive_cap_H5_trial.3mf](parts/OPSW4_captive_cap_H5_trial.3mf) | 0.39 g | 14 min |
| [OPSW5_captive_cap_H5_trial.gcode.3mf](sliced/OPSW5_captive_cap_H5_trial.gcode.3mf) | [OPSW5_captive_cap_H5_trial.3mf](parts/OPSW5_captive_cap_H5_trial.3mf) | 0.39 g | 14 min |
| [OPSW6_captive_cap_H5_trial.gcode.3mf](sliced/OPSW6_captive_cap_H5_trial.gcode.3mf) | [OPSW6_captive_cap_H5_trial.3mf](parts/OPSW6_captive_cap_H5_trial.3mf) | 0.39 g | 14 min |
| [option_retainer.gcode.3mf](sliced/option_retainer.gcode.3mf) | [option_retainer.3mf](parts/option_retainer.3mf) | 1.48 g | 16 min |
| [acrylic_case_washer_1_bottom_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_1_bottom_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_1_bottom_0p5_SURROGATE.3mf](parts/acrylic_case_washer_1_bottom_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_1_top_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_1_top_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_1_top_0p5_SURROGATE.3mf](parts/acrylic_case_washer_1_top_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_2_bottom_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_2_bottom_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_2_bottom_0p5_SURROGATE.3mf](parts/acrylic_case_washer_2_bottom_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_2_top_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_2_top_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_2_top_0p5_SURROGATE.3mf](parts/acrylic_case_washer_2_top_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_3_bottom_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_3_bottom_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_3_bottom_0p5_SURROGATE.3mf](parts/acrylic_case_washer_3_bottom_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_3_top_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_3_top_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_3_top_0p5_SURROGATE.3mf](parts/acrylic_case_washer_3_top_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_4_bottom_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_4_bottom_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_4_bottom_0p5_SURROGATE.3mf](parts/acrylic_case_washer_4_bottom_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_4_top_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_4_top_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_4_top_0p5_SURROGATE.3mf](parts/acrylic_case_washer_4_top_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_5_bottom_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_5_bottom_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_5_bottom_0p5_SURROGATE.3mf](parts/acrylic_case_washer_5_bottom_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_5_top_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_5_top_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_5_top_0p5_SURROGATE.3mf](parts/acrylic_case_washer_5_top_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_6_bottom_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_6_bottom_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_6_bottom_0p5_SURROGATE.3mf](parts/acrylic_case_washer_6_bottom_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_6_top_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_6_top_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_6_top_0p5_SURROGATE.3mf](parts/acrylic_case_washer_6_top_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_7_bottom_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_7_bottom_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_7_bottom_0p5_SURROGATE.3mf](parts/acrylic_case_washer_7_bottom_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_7_top_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_7_top_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_7_top_0p5_SURROGATE.3mf](parts/acrylic_case_washer_7_top_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_8_bottom_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_8_bottom_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_8_bottom_0p5_SURROGATE.3mf](parts/acrylic_case_washer_8_bottom_0p5_SURROGATE.3mf) | 0.09 g | 7 min |
| [acrylic_case_washer_8_top_0p5_SURROGATE.gcode.3mf](sliced/acrylic_case_washer_8_top_0p5_SURROGATE.gcode.3mf) | [acrylic_case_washer_8_top_0p5_SURROGATE.3mf](parts/acrylic_case_washer_8_top_0p5_SURROGATE.3mf) | 0.09 g | 7 min |

### 4. PLA collar shape surrogates â€” 0.2 mm nozzle

| Print filename (sliced) | Editable project | PLA | Estimated time |
|---|---|---:|---:|
| [USB_A_collar.gcode.3mf](sliced/USB_A_collar.gcode.3mf) | [USB_A_collar.3mf](parts/USB_A_collar.3mf) | 0.26 g | 12 min |
| [USB_C_collar.gcode.3mf](sliced/USB_C_collar.gcode.3mf) | [USB_C_collar.3mf](parts/USB_C_collar.3mf) | 0.35 g | 13 min |

### 5. Optional height gauges and fastener envelopes â€” 0.2 mm nozzle

| Print filename (sliced) | Editable project | PLA | Estimated time |
|---|---|---:|---:|
| [option_retainer_M2x5_pan_screw_envelope_1_SURROGATE.gcode.3mf](sliced/option_retainer_M2x5_pan_screw_envelope_1_SURROGATE.gcode.3mf) | [option_retainer_M2x5_pan_screw_envelope_1_SURROGATE.3mf](parts/option_retainer_M2x5_pan_screw_envelope_1_SURROGATE.3mf) | 0.11 g | 16 min |
| [option_retainer_M2_nut_envelope_1_SURROGATE.gcode.3mf](sliced/option_retainer_M2_nut_envelope_1_SURROGATE.gcode.3mf) | [option_retainer_M2_nut_envelope_1_SURROGATE.3mf](parts/option_retainer_M2_nut_envelope_1_SURROGATE.3mf) | 0.09 g | 11 min |
| [option_retainer_M2x5_pan_screw_envelope_2_SURROGATE.gcode.3mf](sliced/option_retainer_M2x5_pan_screw_envelope_2_SURROGATE.gcode.3mf) | [option_retainer_M2x5_pan_screw_envelope_2_SURROGATE.3mf](parts/option_retainer_M2x5_pan_screw_envelope_2_SURROGATE.3mf) | 0.11 g | 16 min |
| [option_retainer_M2_nut_envelope_2_SURROGATE.gcode.3mf](sliced/option_retainer_M2_nut_envelope_2_SURROGATE.gcode.3mf) | [option_retainer_M2_nut_envelope_2_SURROGATE.3mf](parts/option_retainer_M2_nut_envelope_2_SURROGATE.3mf) | 0.09 g | 11 min |
| [pad_1_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_1_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_1_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_1_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.28 g | 14 min |
| [pad_1_2_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_1_2_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_1_2_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_1_2_INSTALLED_HEIGHT_GAUGE.3mf) | 0.29 g | 14 min |
| [pad_1_3_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_1_3_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_1_3_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_1_3_INSTALLED_HEIGHT_GAUGE.3mf) | 0.29 g | 14 min |
| [pad_1_4_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_1_4_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_1_4_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_1_4_INSTALLED_HEIGHT_GAUGE.3mf) | 0.29 g | 14 min |
| [pad_1_5_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_1_5_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_1_5_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_1_5_INSTALLED_HEIGHT_GAUGE.3mf) | 0.29 g | 14 min |
| [pad_1_6_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_1_6_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_1_6_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_1_6_INSTALLED_HEIGHT_GAUGE.3mf) | 0.29 g | 14 min |
| [pad_1_7_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_1_7_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_1_7_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_1_7_INSTALLED_HEIGHT_GAUGE.3mf) | 0.47 g | 17 min |
| [pad_2_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_2_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_2_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_2_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.25 g | 13 min |
| [pad_3_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_3_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_3_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_3_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.25 g | 13 min |
| [pad_4_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_4_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_4_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_4_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.25 g | 13 min |
| [pad_5_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_5_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_5_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_5_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.25 g | 13 min |
| [pad_6_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_6_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_6_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_6_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.23 g | 12 min |
| [pad_7_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_7_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_7_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_7_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.23 g | 12 min |
| [pad_8_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_8_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_8_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_8_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.08 g | 9 min |
| [pad_9_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf](sliced/pad_9_1_INSTALLED_HEIGHT_GAUGE.gcode.3mf) | [pad_9_1_INSTALLED_HEIGHT_GAUGE.3mf](parts/pad_9_1_INSTALLED_HEIGHT_GAUGE.3mf) | 0.07 g | 9 min |

## Settings and estimates

**Required: 86 separate prints, about 471 g / 26.6 hours.** All optional gauges included: 105 separate prints, 475 g / 30.7 hours. Individual printing adds startup and handling compared with the previous grouped kit. Estimates include slicer startup, supports and brims, but exclude nozzle changes, cooling/removal, manual handling and failures.

- 0.6 mm simple surrogates and 0.4 mm spacers/case posts: 0.20 mm layers, two walls, two top/bottom shells and 5% rectilinear infill.
- 0.4 mm detail parts: 0.10 mm layers, two walls, three top/bottom shells and 8% infill.
- 0.2 mm collar surrogates: 0.10 mm layers. Optional gauges/envelopes: 0.05 mm layers including the first layer.
- Generic PLA profiles; Textured PEI Plate; 220 Â°C nozzle / 65 Â°C bed. Match the physical bed and actual PLA in Bambu Studio and re-slice if different. Match the installed nozzle to each file before printing. The 0.2 mm profile uses its dedicated flow limit.
- One PLA colour/AMS slot, zero in-print filament changes and no prime tower. Automatic bed-only supports where detected; 3 mm brims for large/simple parts, 2 mm for details. Gauges disable supports.

## Fitment limits

The collars are **PLA shape surrogates**, not compliant seals. Test insertion force and sealing with the real TPU95A collars separately. [Bambu A1 documentation](https://cdn1.bambulab.com/documentation/quick-start-f507128172bdf/Quick%20start%20guide%20-%20A1%20combo-EN.pdf) cautions against feeding ordinary flexible TPU through AMS Lite.

Printed threads are omitted. Use real fasteners for closed fit trials. Clip-on heatsink posts have not been implemented. The heatsink retention design still needs qualification. **Do not power a board with the plastic heatsink or rigid thermal-pad gauges fitted.** Use real electronics, foam and thermal pads to qualify topography and compression.

Layer quantisation and printer calibration affect fit: measure actual heights, bores and mating shoulders. A successful slice does not establish strength, adhesion or dimensional accuracy. Quarter pieces must remain temporary unpowered mock sections.

## Verification and rebuilding

[print-plan.json](print-plan.json) maps every file to its source STL. [print-check.json](print-check.json) verifies 105 separate files, one source part per file, source hashes, independent build objects, native slicer object/part counts, mesh dimensions, bed placement, no scaling, successful A1 slices, matching nozzle/PLA settings, no slicer warnings, no prime tower and no filament changes. The [preview sheet](review/part-overview.png) shows the first 24 individual files; every sliced project also contains its own preview.

Rebuild with the existing project Python environment: `prepare_prints.py`, `slice_plates.py`, then `check_and_package.py`. The scripts use installed Bambu Studio at `D:/Bambu Studio`; adjust that path on another computer. All slicing runs locally and does not contact a printer. Successful slice records are retained in `slice-results.json`; disposable `jobs/` scratch copies and build logs can be removed after validation.
