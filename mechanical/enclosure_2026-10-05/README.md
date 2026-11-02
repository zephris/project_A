# PHBox Choc V1 retention plate — fit candidate

First deliverable for the gasket suspended acrylic/PLA enclosure. See
[DESIGN-PRINCIPLES.md](DESIGN-PRINCIPLES.md) for the required bottom-to-top stack,
thermal interfaces, suspension, foam damping and remaining validation.

## Files

- `candidate/choc-v1-retention-nominal.dxf`: 1:1 millimetre nominal cut contours. No laser kerf or cutter compensation. Intended trial sheet thickness: 1.3 mm.
- `candidate/choc-v1-retention-1p3mm.step`: editable solid at Z=0…1.3 mm.
- `candidate/choc-v1-retention-1p3mm.stl`: flat PLA prototype; use a flat bed and verify dimensional calibration. At this size a large printer bed or segmentation will be required; segmentation joints are not designed here.
- `candidate/choc-v1-fit-coupon-1p2mm.*` and `...-1p3mm.*`: print/cut these first. Left-to-right hole sizes viewed with +Y up: 13.9, 14.0, 14.1, 14.2 mm. The DXF is the common nominal outline for both sheet thicknesses.
- `candidate-preview.png`: dimensioned-coordinate overview of the plate over a simplified PCB outline. Electronics bounding boxes are illustrative, not a collision analysis. Brown areas are eight gasket tabs.
- `candidate-parameters.json`: extracted PCB centres, CAD coordinate mapping, assumptions and source hash.
- `candidate-validation.json`: geometry checks and explicit outstanding fit checks.
- `build_candidate.py`: reproducible CAD generator using project-local CadQuery dependencies in `stage2_work/enclosure_cad_dependencies` and the included KiCad parser.

DXF is the cutting reference. The generated SVG is a visual preview only; its page
scaling is not a machine cutting specification. The STL and STEP export origin is
the lower-left corner of the PCB's bounding rectangle, with +Y towards USB. Z=0 is
the underside of the plate, not PCB front. The initial installed plate-top estimate
is 2.2 mm above PCB front; physical switch seating must confirm that height.

Six circular holes match H1/H2/H3/H7/H8/H9 for clearance/alignment. They are not
instructions to bolt the floating assembly to the outer enclosure. The top service
region has no retention plate, so the other PCB mounting holes are outside this part.
PCB outline corners are R5 at the lower corners; tab and aperture corners are square.

The 14 mm aperture and 1.3 mm thickness need a physical coupon trial. Acrylic at
this thickness and size requires structural support and careful handling; the PLA
sheet is also a fit prototype pending stiffness assessment. A thicker acrylic bezel
or printed carrier can support the thin clip regions in the eventual enclosure.

This is a candidate mechanical package, not the final enclosure manufacturing
release. The PCB, JLCPCB package, bottom/top outer plates, spreaders, screen posts
and final foam patterns are not altered or released by this candidate.
