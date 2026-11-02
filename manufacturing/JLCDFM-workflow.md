# JLCDFM workflow

User instruction, 6 October 2026: always use the separate BOM matching site for BOM/CPL uploads, rather than the viewer's BOM match button.

After uploading Gerbers, use https://jlcdfm.com/bomMatch?pcbUploadFileId=UPLOAD_ID with the actual viewer upload ID. Upload the current BOM and CPL, process them, confirm all expected part groups, continue to Component Placements and Save & Close. Return to the corresponding viewer, allow models to load, visually check placement and connector orientation, then run SMT DFM. Empty model lists and zero counters before file loading are not a pass.
