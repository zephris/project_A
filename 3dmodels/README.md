# Kailh Choc hot-swap socket model

Source: https://github.com/perigoso/keyswitch-kicad-library
Pinned revision: `9edbd5ea3f5f4e36cbdfaefdf3d8b5c28277a416`

`SW_Hotswap_Kailh_Choc_V1.step` is the upstream `.stp` file renamed without modifying its contents. Its WRL counterpart is also included. Upstream declares the library dual licensed under MIT and CC-BY-SA 4.0; copies are included alongside these assets. Credit: Rafael Silva (perigoso) and contributors to keyswitch-kicad-library.

This is the socket body model, not the installed switch or keycap. Its matching upstream `SW_Hotswap_Kailh_Choc_V1V2` footprint has exactly the same pads and NPTH geometry as the existing PHBox optical variant. The replacement project-local footprint retains PHBox optical silkscreen adaptations and references `${KIPRJMOD}/3dmodels/SW_Hotswap_Kailh_Choc_V1.step`, with upstream zero offset/rotation and unit scale. All SW1–SW16 PCB instances and schematic footprint properties use `PHBox_Repair:SW_Hotswap_Kailh_Choc_V1V2_3D_Optical`.

Model visualization does not establish switch-housing, keycap or enclosure fit; those release checks remain.
