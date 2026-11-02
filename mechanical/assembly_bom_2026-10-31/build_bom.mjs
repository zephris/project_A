import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const output = path.join(root, 'outputs/01a10a60-ef4e-79f2-86e5-a64bb6e3f512');
const current = 'mechanical/ergonomic_layout_2026-10-30/';
const old = 'mechanical/sandwich_17mm_2026-10-08/';
const heat = 'mechanical/heatsink_2026-10-08/';
const suppliers = {
  jlc: {name:'JLCPCB', area:'China, shipped', purpose:'PCB, assembly and matching electronic parts', url:'https://jlcpcb.com/', availability:'Quote after wider-layout routing and new manufacturing exports. Electronic stock not reverified.', pack:null, price:null, currency:'', note:'No current fabrication release. Do not reuse the October 6 USB2 BOM/CPL.'},
  ple: {name:'PLE Computers', area:'Bentley / Osborne Park / other Perth stores', purpose:'0.5 mm thermal gap-pad stock', url:'https://www.ple.com.au/products/645790/thermal-grizzly-minus-pad-8-120x20-x-05mm-thermal-pad-2pcs', availability:'Listing: Bentley, Cockburn and Wangara in stock. Osborne Park about 1 business day.', pack:2, price:9, currency:'AUD', note:'PLE-645790, TG-MP8-120-20-05-2R. Two 120×20×0.5 mm strips. Buy one pack for both chips; check compression.'},
  multifix: {name:'Multi-Fix WA', area:'Unit 6, 29 O’Malley St, Osborne Park', purpose:'Local small-pack M3 case screws and dimensioned washers', url:'https://www.multifixwa.com.au/products/screws-and-fasteners/screws-and-fasteners/', availability:'Supplier inquiry only. Catalog lists M2.5–M10 metal-thread screws; exact sizes/stock not confirmed.', pack:null, price:null, currency:'', note:'Ask for 16 M3×6 90° countersunk screws and 16 Ø7/Ø3.4/0.50 mm washers. M2 is outside listed range.'},
  searle: {name:'Searle Fasteners', area:'Unit 1/26 Ernest Clark Rd, Canning Vale', purpose:'Consolidated exact-size fastener inquiry, including M2 and polymer hardware', url:'https://searlefasteners.com.au/', availability:'Supplier inquiry only. Specific M2, polymer and head-envelope matches not confirmed.', pack:null, price:null, currency:'', note:'Request small quantities with drawings. Do not substitute metal internal screws for specified insulating screws without review.'},
  altronics: {name:'Altronics Northbridge', area:'Northbridge, Perth', purpose:'Local case-column alternative', url:'https://www.altronics.com.au/category/spacers-mounts?pagenumber=3', availability:'H1348 listed, 8-pack M3×12 nylon tapped spacers. Northbridge shelf stock not verified.', pack:8, price:3.75, currency:'AUD', note:'Conditional alternative only. Check body diameter/AF, female threads and loaded 12 mm height; CAD references brass AF5 columns.'},
  rs: {name:'RS Australia', area:'Australian online delivery, dispatch origin unconfirmed', purpose:'Exact nominal metal case-column fallback', url:'https://au.rs-online.com/web/p/standoffs/0222402', availability:'RS 222-402 listing says in stock. Perth delivery date must be checked.', pack:50, price:50.65, currency:'AUD', note:'M3 female/female, 12 mm, brass, AF5. Pack of 50 is poor value for eight; ask local suppliers first. Price includes GST.'},
  element14: {name:'element14 Australia', area:'Australian online delivery', purpose:'Traceable M2 polymer fastener fallback', url:'https://au.element14.com/c/fasteners-mechanical/fasteners-fixings/plastic-fasteners/plastic-screws?thread-size-metric=m2', availability:'TRNSE-1207-M2-8 / 2472697 listed, pack 100. Live price/availability unavailable.', pack:100, price:null, currency:'', note:'Screen screws only if head ≤Ø4×1.6 mm. Consolidate other M2 hardware in one order; request exact drawings.'},
  cdc: {name:'CDC Laser / Acrylic Sheet Sales', area:'Unit 1/43 Baretta Rd, Wangara', purpose:'2 mm acrylic covers, cut and finished to CAD', url:'https://acrylicsheetsales.com.au/acrylic-sheets/', availability:'Local cutting service and 2 mm stock range listed. Finished-pair price/lead time require quote.', pack:null, price:null, currency:'', note:'Quote one top and one bottom, 2.0 mm cast acrylic. Ask whether 90° countersinks can be completed; laser cutting alone does not make them.'},
  enex: {name:'Enex Engineering', area:'Malaga, Perth', purpose:'Custom CNC aluminium heatsink and retention-plate inquiry', url:'https://enexengineering.com.au/', availability:'CNC milling and 6061 listed. No minimum order advertised. Specific parts, price and lead time unquoted.', pack:null, price:null, currency:'', note:'Request one 6061-T6 heatsink plus one 1.30 mm aluminium switch plate. Confirm thin-plate fixturing/material tolerance. Plastic mounts need separate capability confirmation.'},
  foam: {name:'Foam Sales', area:'50–52 Catalano Circuit, Canning Vale', purpose:'Small samples/offcuts of real cushioning foam', url:'https://www.foamsales.com.au/pages/contact', availability:'Local foam supplier confirmed. Exact 2.0/1.5 mm grade, stock and compression curve require inquiry.', pack:null, price:null, currency:'', note:'Seven 2 mm lower pads and six 1.5 mm upper pads. Ask for nonconductive, non-carbon-filled foam; verify force and compression in assembly.'},
  jaycar: {name:'Jaycar', area:'Perth stores; choose branch before travel', purpose:'TPU material and hardware trial blanks', url:'https://www.jaycar.com.au/elegoo-tpu-95a-filament-grey-1-75mm-1kg/p/TL6530', availability:'TL6530 grey TPU 95A listed. Local branch stock requires selection.', pack:1, price:29.95, currency:'AUD', note:'1 kg spool. Avoid buying a whole spool only for two seals if a local print service can supply them for less. Feed ordinary TPU outside AMS Lite.'},
  additive: {name:'AdditiveArcade', area:'United Kingdom, shipped to Australia', purpose:'Selected SGF MonKeys caps', url:'https://additivearcade.com/products/low-profile-sgf-monkeys-button-caps', availability:'Product lists stock and Choc V2/Small options. Exact Flat/Nekkid variant quantity and Perth freight require checkout check.', pack:1, price:null, currency:'', note:'Buy 16 nominal 20 mm caps: 13 installed plus 3 spares with blanks fitted. Displayed pricing varies by option. No exact Perth stock verified.'},
  keebart: {name:'Keebart', area:'Germany, international delivery', purpose:'Original Kailh Choc V2 Red switch fallback', url:'https://www.keebart.com/de/produkte/choc-switches-v2?country=DE', availability:'Original Red/Brown/Blue variants and 10-packs listed. Confirm Red stock and Perth delivery before buying.', pack:10, price:4.90, currency:'EUR', note:'Two packs supply 16 installed plus 4 spares. Displayed price includes German VAT, not an Australian landed quote. Reference part CPG135301D01.'},
  keebz: {name:'Keebz N Cables', area:'Leederville click-and-collect, online only', purpose:'Optional local inquiry for original Choc V2 Red', url:'https://www.keebzncables.com/pages/frequently-asked-questions', availability:'Perth pickup confirmed. No exact selected Choc V2 stock listing found.', pack:null, price:null, currency:'', note:'Ask before relying on local supply. Do not replace with Choc V1, MX or a different low-profile family just because it has a cross stem.'},
  self: {name:'Own Bambu A1 / existing filament', area:'On hand', purpose:'Rigid custom parts and blanking-plug trials', url:'', availability:'Bambu PLA and PETG already owned. Final service material and joint durability still need qualification.', pack:null, price:null, currency:'', note:'Full-size 292.6 mm parts exceed the 256 mm bed. Existing quartered PLA kit is a fit mock; finished section joints require a service build decision.'}
};
const rows=[];
function add(section,id,qty,unit,part,spec,provider,action,notes='',cad='',extraSource='') {
  rows.push({section,id,qty,unit,part,spec,provider,action,notes,cad,source:[suppliers[provider].url,extraSource].filter(Boolean).join('\n')});
}

add('1. PCB and fitted electronics','E01',1,'assembly','Assembled wider-layout PCB','Current ergonomic KiCad candidate; complete semiconductor, passive, RGB LED, protection and USB population.','jlc','HOLD: finish routing','22 unconnected items in the saved audit tied to the current board hash. Generate fresh Gerbers/BOM/CPL after routing and DRC. Old exports use the superseded USB-A.','mechanical/ergonomic_layout_2026-10-30/pcb/PHBox-ergonomic.kicad_pcb');
add('1. PCB and fitted electronics','E02',1,'module','SH1106 OLED HS13L03W2C01','U5, JLC C7465997; 1.3 inch 128×64; PCB 35.4×33.5 mm, mount pitch 30.4×28.5 mm.','jlc','Confirm PCBA inclusion','Included within E01 if assembled by JLCPCB. Otherwise purchase exactly one separately. A generic OLED is not mechanically equivalent.');
add('1. PCB and fitted electronics','E03',16,'ea','Kailh Choc hot-swap sockets','SW1–SW16 socket footprint; exact socket MPN and assembly coverage must be selected for this footprint.','jlc','HOLD: select exact socket','Current footprint properties have blank LCSC fields. Count within E01 if supplied by assembler. These are sockets, not the 16 physical Choc V2 switches.');
add('1. PCB and fitted electronics','E04',6,'ea','Option tactile switches','OPSW1–OPSW6, through-hole 6 mm body; CAD assumes 5 mm actuator height above the PCB.','jlc','HOLD: choose MPN/height','Blank LCSC/MPN in current PCB. Verify footprint lead pitch and actual actuator height against plungers, then add to refreshed electronic BOM. Include in E01 once selected. No extra return springs.');

add('2. Main controls and blanking plugs','C01',16,'ea','Original Kailh Choc V2 Red switches','CPG135301D01, MX-style cross stem; retain original V2 housing/LED-window geometry.','keebart','Confirm Red stock + shipping','Try Keebz N Cables in Leederville first; exact stock is not verified. Online fallback: buy two packs of 10 (4 spares). Do not substitute different Choc V2 variants without fit review.', '', 'https://www.kailh.net/products/kailh-choc-v2-low-profile-switch-set');
add('2. Main controls and blanking plugs','C02',13,'ea fitted','SGF MonKeys 20 mm caps','Choc V2 / Small / Flat / Nekkid. Ø24 mm acrylic openings.','additive','Confirm exact variant','Suggested purchase: 16 caps, 13 installed + 3 spares. Use all 16 if the three plugs are removed. Custom PETG caps are an authorized fallback if exact supply or delivery is impractical; no new cap model is supplied by this BOM.');
add('2. Main controls and blanking plugs','C03',3,'ea','Clip-on blanking plugs','Current Ø24 mm opening / 2 mm acrylic design; Ø25.8 mm head, nominal 1.6 mm face rise, side removal grooves.','self','Print PLA trial','Latest requested plug material is PLA. Keep switches under blanks only if a full-travel fit trial confirms no unwanted preload/actuation. Repeated-use latch life unqualified.',current+'STL/button_blank.stl');

add('3. Enclosure, foam and port seals','X01',1,'ea','Top acrylic cover','2.0 mm cast acrylic; current 20 mm cap layout, Ø24 mm openings, integrated USB-A roof.','cdc','Quote + trial coupon','Eight Ø3.4 mm case holes, 90° Ø6.7 mm countersinks, nominal 1.65 mm depth. Thin remaining land requires a drilling/countersinking trial.',current+'DXF/top_acrylic.dxf');
add('3. Enclosure, foam and port seals','X02',1,'ea','Bottom acrylic cover','2.0 mm cast acrylic; matching current individual STEP geometry.','cdc','Quote + trial coupon','Same eight case-hole countersinks. No regenerated bottom cutting DXF is present in the current folder; quote from STEP. Do not scale to compensate.',current+'STEP/bottom_acrylic.step');
add('3. Enclosure, foam and port seals','X03',1,'assembly','Upper spacer/frame','Current geometry includes option/display reliefs, USB surrounds and lower USB-C roof.','self','Custom fabrication','Use current STEP/STL, not the stale combined assembly STEP. Full part exceeds A1 bed; print qualified sections or commission a larger build. PLA stack files are mock-only.',current+'STEP/top_spacer.step');
add('3. Enclosure, foam and port seals','X04',1,'assembly','Lower spacer/carrier','Current relieved carrier clears moved sockets and solder tails.','self','Custom fabrication','Full part exceeds A1 bed. Final service material and any sectional joint must be qualified; reuse old mock parts only as specified in the replacement guide.',current+'STEP/bottom_spacer.step');
add('3. Enclosure, foam and port seals','X05',1,'ea','Choc V2 retention plate','1.30 mm aluminium; sixteen 14.10 mm square apertures, capture tabs and clearance reliefs.','enex','Quote + real-switch trial','Confirm 1.30 mm finished thickness, aperture corner/tool access, deburring and latch retention. A printed plate in the mock kit is not the aluminium production part.',current+'DXF/switch_plate.dxf');
add('3. Enclosure, foam and port seals','X06',7,'cut pads','Lower cushioning foam','2.0 mm free stock, nominal 1.6488 mm installed. Nonconductive compressible foam.','foam','Quote samples + compression trial','Cut all seven profiles from current DXF; pads 1/7 changed. Foam must clear reliefs and leave PCB movement free. Do not replace with rigid printed height gauges.',current+'DXF/foam.dxf');
add('3. Enclosure, foam and port seals','X07',6,'cut pads','Upper capture foam','1.5 mm free stock, nominal 1.2 mm installed; four 7×18 and two 19×6 mm pads.','foam','Quote samples + compression trial','Capture the plate tabs without excessive preload. Do not use conductive/carbon-filled ESD foam. Exact grade and force remain unqualified.',current+'DXF/upper_foam.dxf');
add('3. Enclosure, foam and port seals','X08',1,'ea','USB-A compliant collar','Unfilled nonconductive TPU 95A; current rear PCB relief and thin face membrane.','self','Print TPU + trial','Use real TPU, not the PLA mock surrogate. Acrylic supplies the connector roof. Buy material locally only if not already available.',old+'STL/usb_a_collar.stl',suppliers.jaycar.url);
add('3. Enclosure, foam and port seals','X09',1,'ea','USB-C compliant collar','Unfilled nonconductive TPU 95A; current shell relief.','self','Print TPU + trial','Spacer supplies USB-C roof. Collars must seal gaps while allowing intended PCB travel. No ingress rating is established.',old+'STL/usb_c_collar.stl',suppliers.jaycar.url);

add('4. Outer case hardware','H01',8,'ea','Rigid case columns','M3 female/female, 12.0 mm body, AF5; brass reference.','multifix','Local exact-size inquiry','RS 222-402 is a nominal matching shipped fallback (50-pack). Altronics H1348 nylon is cheaper/local but conditional on body size, loaded height and thread arrangement. Do not silently substitute.',current+'STEP/case_hardware.step',suppliers.rs.url+'\n'+suppliers.altronics.url);
add('4. Outer case hardware','H02',16,'ea','Case-column end washers','OD7.0 / ID3.4 / 0.50 mm thick; one at each end of eight columns.','multifix','Local exact-size inquiry','Thickness controls the 13 mm cavity: 12 + 2×0.5 mm. Generic M3 washer labels do not guarantee these dimensions.');
add('4. Outer case hardware','H03',16,'ea','Case-cover screws','M3×6, 90° countersunk; head must fit Ø6.7 mm recess.','multifix','Local exact-size inquiry','Eight top + eight bottom. Verify actual head height and thread engagement. Tighten gently against rigid columns, not against the floating PCB.');

add('5. Switch plate and display mounts','P01',3,'ea','Insulating switch-plate posts','Custom H1/H2/H3 stepped supports; 3.0 mm seat height, Ø6.1 pilots, Ø3.4 screw clearance.','self','Custom + joint qualification','Current models are printed/tapped trial geometry. Machined POM is an alternative; ordinary catalog standoffs do not reproduce these shoulders. Confirm actual PCB thickness.',current+'STEP/mounts.step');
add('5. Switch plate and display mounts','P02',3,'ea','Switch-plate rear retainers','Custom insulating rear caps matched to P01; tapped/pilot fit per CAD.','self','Custom + joint qualification','Printed pilots are not qualified threads. Confirm torque/pullout and underside clearance; get a local plastics-machining quote if print trials fail.',current+'STEP/mounts.step');
add('5. Switch plate and display mounts','P03',3,'ea','Switch-plate polymer screws','M3×8, insulating nylon/polymer, head ≤Ø6×2.4 mm.','searle','Exact-size inquiry','Request head drawing. Jaycar HP0140 M3×12 blanks may be trimmed for a fit trial only after head and finished length checks.','', 'https://www.jaycar.com.au/m3-x-12mm-nylon-screws-pack-of-10/p/HP0140');
add('5. Switch plate and display mounts','D01',1,'ea','OLED retaining frame','Current custom 40.4×38.5 mm body / 1 mm web, corner ears and reliefs.','self','Custom + trial','Retain display PCB edges, never preload the glass. Use current relocated frame.',current+'STEP/screen_frame.step');
add('5. Switch plate and display mounts','D02',4,'ea','Insulating OLED posts','Custom 3.0 mm seat height, Ø4.8 body / Ø2.7 pilot / Ø2.2 M2 clearance.','self','Custom + joint qualification','Positions follow the current OLED. These are not generic 3 mm cylindrical spacers.',current+'STEP/mounts.step');
add('5. Switch plate and display mounts','D03',4,'ea','OLED rear retainers','Custom insulating tapped caps matched to D02.','self','Custom + joint qualification','Check pilot depth, real PCB thickness and thread/pullout strength before loading the screen.',current+'STEP/mounts.step');
add('5. Switch plate and display mounts','D04',4,'ea','OLED polymer screws','M2×8, head ≤Ø4×1.6 mm.','searle','Exact-size inquiry','Local supply preferred. Shipped fallback: element14 2472697, TRNSE-1207-M2-8, if head drawing matches. No verified local shelf match.', '',suppliers.element14.url);

add('6. Option-button hardware','O01',6,'ea','Captive option plungers','Custom guided caps at the six actual actuator centres.','self','Print + actuator trial','No separate springs. Stroke, rest height and freedom depend on selecting the 5 mm-height tactile switches in E04.',current+'STL/option_caps.stl');
add('6. Option-button hardware','O02',1,'ea','Option-button retainer','Current 67×12 mm body, locating bosses, total width including bosses about 17 mm.','self','Print current revision','Use current relocated version; old retainer obstructed the revised placement.',current+'STL/option_retainer.stl');
add('6. Option-button hardware','O03',2,'ea','Option-retainer screws','M2×5 pan head; head ≤Ø4×1.6 mm.','searle','Exact-size inquiry','Check drawing against counters/recesses; do not automatically replace with longer screws.');
add('6. Option-button hardware','O04',2,'ea','Option-retainer nuts','M2 hex, AF4.0×1.6 mm target; pockets AF4.4, depth 1.7 mm.','searle','Sample/drawing fit check','Nut dimensions vary. Verify delivered corners, AF and thickness before final fitting.');

add('7. MCU and flash thermal assembly','T01',1,'ea','Milled aluminium heatsink','6061-T6, 3 mm web, about 60×34 mm body plus tabs, notch and underside contact bosses.','enex','Quote current STEP','One upper MCU/flash plate only. Preserve BOOTSEL/RESET keepout. This is not a uniform flat blank; machine the bosses and mounting geometry.',heat+'STEP/heatsink_plate.step');
add('7. MCU and flash thermal assembly','T02',1,'cut pad','U1 MCU thermal pad','Electrically insulating thermal gap pad, 5.5×5.5 mm; 0.50 mm free thickness.','ple','Buy 1 shared pack','Cut this and T03 from one PLE-645790 pack. Nominal installed 0.40 mm is a trial assumption; confirm contact without bending PCB or overloading chip.');
add('7. MCU and flash thermal assembly','T03',1,'cut pad','U3 flash thermal pad','Same material, 3.5×3.5 mm; 0.50 mm free thickness.','ple','Included in T02 pack','Do not buy a second pack. Plain electrical-insulator washers are not thermal gap pads. Adhesive thermal tape is a different compliance/bonding choice.');
add('7. MCU and flash thermal assembly','T04',3,'ea','Heatsink insulating hard stops','Custom H5/H7 M3 and H12 M2 stepped stops; positive land sets heatsink underside at nominal Z=4 mm.','self','Custom + joint qualification','Rigid insulating parts, not TPU. POM machining is an option; PETG trial requires thermal/preload checks. Ordinary catalog posts do not reproduce the pilots/lands.',heat+'src/heatsink_common.py');
add('7. MCU and flash thermal assembly','T05',3,'ea','Heatsink support washers','Custom insulating washer profiles, nominal installed thickness 0.50 mm.','self','Custom + preload trial','Use flat support washers represented in current CAD. O-rings are an alternative only after requalifying compressed height/force, not additional required parts.',heat+'src/heatsink_common.py');
add('7. MCU and flash thermal assembly','T06',3,'ea','Heatsink rear insulating washers','Custom 0.50 mm washers with PCB pilot reliefs.','self','Custom + fit check','Separate from the three upper support washers and the sixteen outer case washers.',heat+'src/heatsink_mounting.py');
add('7. MCU and flash thermal assembly','T07',3,'ea','Heatsink rear tapped retainers','Custom insulating caps; current nominal threaded depth only 2 mm.','self','HOLD: qualify rear retention','A stock-nut capture-carrier redesign is only proposed, not implemented. Do not buy nuts or treat printed pilot holes as qualified loaded threads.',heat+'src/heatsink_mounting.py');
add('7. MCU and flash thermal assembly','T08',2,'ea','Heatsink M3 polymer screws','H5/H7, insulating; final under-head length unresolved.','searle','HOLD: length + engagement','Current nominal grip 9.15 mm: M3×10 engages only 0.85 mm, ×12 protrudes 0.85 mm. Do not finalize purchase until retention and actual stack are settled.');
add('7. MCU and flash thermal assembly','T09',1,'ea','Heatsink M2 polymer screw','H12, insulating; final under-head length unresolved.','searle','HOLD: length + engagement','Same retention issue as T08. A trimmed ~11 mm trial is not a strength/tolerance qualification.');

add('8. External connection and material stock','A01',1,'ea','Laptop-to-board USB data cable','USB-A→USB-C or USB-C→USB-C for the actual laptop; USB 2.0 data-capable, not charge-only.','jaycar','Reuse first; check overmold fit','Choose a slim overmold within the case USB-C cable gauge (13×8 mm). Local cable catalog does not establish overmold dimensions. Cable stock/price depend on chosen part.', '', 'https://www.jaycar.com.au/computing-communication/cables-adaptors/usb/c/3CB');
add('8. External connection and material stock','A02',1,'shared stock','PLA / PETG rigid-part material','Use existing Bambu spools for trials; three requested blanking plugs are PLA.','self','On hand; no new purchase','PETG custom 20 mm keycaps may be modeled if exact SGF supply/delivery is impractical. No fit-qualified printable keycap model is included yet. Mock print support/purge masses are not installed BOM mass.');
add('8. External connection and material stock','A03',1,'shared stock','TPU 95A for both collars','Only the two collars require TPU. Unfilled, nonconductive, 1.75 mm.','jaycar','Buy only if needed','TL6530 is a local catalog option at $29.95 per 1 kg; branch stock unverified. A small local TPU print may cost less. Use an external spool rather than AMS Lite.');

// Verify every CAD file supplied as an order reference exists.
for (const r of rows) if(r.cad) await fs.access(path.join(root,r.cad));
await fs.mkdir(output,{recursive:true});
await fs.mkdir(path.join(here,'review'),{recursive:true});
const abs = p => path.join(root,p).replaceAll('\\','/');
const sourceMD=r=>`[${suppliers[r.provider].name}](${suppliers[r.provider].url || 'https://bambulab.com/en-au/a1'})`;
const esc=s=>String(s??'').replaceAll('|','/').replaceAll('\n',' ');

let md = `# PHBox final-assembly BOM\n\nPrepared 31 October 2026 for **one wider-layout unit**, approximately **292.6 × 191 × 17 mm**, excluding keycaps. Procurement preference: **Perth pickup first**, Australian shipped exact parts next, international only for unavailable exact parts. No orders or supplier inquiries have been sent.\n\n`;
md += `This is a parts list for the intended finished assembly. **The current wider PCB is not ready to fabricate**: its hash-linked audit records 22 unconnected items. Heatsink screw length/retention, option-switch actuator height and socket MPN are unresolved. Hold the affected orders below. The October 6 Gerbers/BOM/CPL predate the present top-side C2344 USB-A and wider layout.\n\n`;
md += `Quantities are installed quantities unless stated. Assumed configuration: **16 Choc V2 switches, 13 fitted 20 mm caps and 3 PLA blanking plugs**. Buy 16 caps if you want three spares or the option of exposing all controls. Confirm blanks do not preload any switches retained underneath.\n\n`;
md += `The assembled-PCB row includes all fitted board electronics. The OLED, sockets and tactile switches are broken out to make sourcing visible, **not to add duplicate purchases**. If JLCPCB cannot supply/fit an item, purchase only the omitted quantity for hand assembly. Current USB1 is HRO-TYPE-C-31-M-12 / C165948; USB2 is Jing 902-131A1021D10100 / C2344, top-side through-hole. BOOTSEL/RESET use the existing board switches. RGB-strip expansion is not part of the saved design.\n\n`;
md += `## BOM by assembly\n\n`;
for (const section of [...new Set(rows.map(r=>r.section))]) {
  md += `### ${section}\n\n| ID | Qty | Part / specification | Preferred provider | Order status / fit requirement |\n|---|---:|---|---|---|\n`;
  for (const r of rows.filter(r=>r.section===section)) {
    const cad=r.cad?` [CAD/source](<${abs(r.cad)}>)`:'';
    md += `| ${r.id} | ${r.qty} ${r.unit} | **${esc(r.part)}**. ${esc(r.spec)}${cad} | ${sourceMD(r)} | **${esc(r.action)}**. ${esc(r.notes)} |\n`;
  }
  md+='\n';
}
md += `## Perth-first shopping plan\n\n| Supplier / pickup area | What to request | Availability and pricing basis |\n|---|---|---|\n`;
for(const id of ['ple','multifix','searle','altronics','cdc','enex','foam','jaycar','keebz']) {
  const s=suppliers[id];
  md+=`| [${s.name}](${s.url}) — ${s.area} | ${s.purpose} | ${s.availability} ${s.price!==null?`Listed ${s.currency} ${s.price.toFixed(2)} per ${s.pack===1?'pack/spool':`${s.pack}-piece pack`}. `:''}${s.note} |\n`;
}
md+=`\nCatalog availability was checked online on 31 October 2026. A listing is not a branch reservation or a supplier acceptance of the CAD. Prices are indicative, before freight unless stated. There is **no reliable complete assembly total** until the custom parts and held hardware are quoted.\n\n`;
md+=`### Shipped fallbacks\n\n`;
for (const id of ['rs','element14','keebart','additive']) {const s=suppliers[id];md+=`- [${s.name}](${s.url}) (${s.area}): ${s.purpose}. ${s.availability} ${s.price!==null?`Listing ${s.currency} ${s.price.toFixed(2)} / ${s.pack} pieces. `:''}${s.note}\n`;}
md+=`\n### PETG keycap fallback\n\nSGF MonKeys remain the selected purchased cap. Custom PETG caps are authorized if exact supply or shipping proves impractical. A replacement would keep a nominal Ø20 mm top, the original Choc V2 cross-stem interface, compatible underside and seating depth, and clearance through the full press beside the screen/heatsink. Print one stem-fit coupon and one cap first. No new PETG cap geometry is delivered in this BOM, and a generic MX cap is not automatically equivalent.\n\n`;
md+=`## Fabrication and assembly notes\n\n- Layer order: top acrylic → upper spacer/plate/heatsink/screen → PCB → real foam → lower spacer → bottom acrylic. PCB and its attachments remain a floating foam-supported island.\n- Use **individual current parts** linked above. The combined current assembly STEP still contains the earlier top cover; it is not cutting artwork. Top DXF is regenerated; bottom cover is supplied as STEP. DXF profiles use millimetres and zero kerf compensation. Have the shop compensate once.\n- Covers are **2.0 mm cast acrylic**. Obtain a countersinking coupon before machining their 1.65 mm-deep countersinks. Do not substitute thicker sheet without revising the stack.\n- The switch plate is **1.30 mm aluminium** and the heatsink is **milled 6061-T6 with contact bosses**. Neither is replaced by a plastic mock. There is one upper heatsink in the current design, with no lower aluminium plate.\n- All stepped insulating posts, rear caps and relieved washers are custom geometry. Printed pilot holes and nominal CAD fits are not thread-strength validation. The existing plan permits printed prototypes; POM machining is an alternative. Ask a local plastics workshop for capability and a quote if printed joints fail qualification.\n- Foam is real cushioning stock, not the rigid height gauges. Request small offcuts/samples rather than large rolls. Thermal interface pieces must be electrically insulating **thermal gap pads**; plain insulating washers are not a substitute.\n- Case columns are separate from the insulating heatsink stops. O-rings are only an alternative to support washers after compressed-height testing; do not add them to the current stack.\n- Standard A1 bed is smaller than the full-width panels. The supplied quartered PLA jobs are fit mocks. For a finished build, qualify section joints or quote a larger printer; do not treat an old mock stack as a final-material print job.\n- Optional console authentication dongles depend on the target platform and are excluded from the base BOM. A laptop USB data cable is included. Additional LEDs, a bottom heatsink and extra option-button springs are excluded.\n\n`;
md+=`## Files\n\n- [Editable assembly BOM workbook](<${abs('outputs/01a10a60-ef4e-79f2-86e5-a64bb6e3f512/PHBox-final-assembly-BOM.xlsx')}>)\n- [Flat CSV](BOM.csv)\n- [Current ergonomic candidate](../ergonomic_layout_2026-10-30/README.md)\n- [Existing assembly sequence](../sandwich_17mm_2026-10-08/README.md) — use the newer part geometry above.\n- [Heatsink hardware audit](../sandwich_17mm_2026-10-08/heatsink-hardware-options.md) — its older AliExpress-first preference is superseded by this Perth-first BOM.\n`;
await fs.writeFile(path.join(here,'README.md'),md);
const csvQuote = s=>'"'+String(s??'').replaceAll('"','""')+'"';
const csvRows=[['Section','ID','Installed quantity','Unit','Part','Specification','Preferred supplier','Order status','Fit / purchasing notes','CAD / project source','Supplier sources']];
for(const r of rows) csvRows.push([r.section,r.id,r.qty,r.unit,r.part,r.spec,suppliers[r.provider].name,r.action,r.notes,r.cad?abs(r.cad):'',r.source]);
await fs.writeFile(path.join(here,'BOM.csv'),'\uFEFF'+csvRows.map(r=>r.map(csvQuote).join(',')).join('\r\n')+'\r\n');

const wb=Workbook.create();
const bom=wb.worksheets.add('Assembly BOM');
const shop=wb.worksheets.add('Buying guide');
const palette={ink:'#203849',pale:'#E7EDF2',amber:'#FFF0CB',line:'#B5C1CB'};
function base(s,cols,last) {
  s.showGridLines=false;s.tabColor=palette.ink;
  s.getRange(`A1:${cols}${last}`).format.font={name:'Arial',size:10,color:palette.ink};
  s.getRange(`A1:${cols}${last}`).format.verticalAlignment='center';
  s.getRange('A2').format.font={name:'Arial',size:14,bold:true};
  s.getRange(`A2:${cols}2`).format.borders={bottom:{style:'thin',color:palette.line}};
  s.getRange(`A1:${cols}${last}`).format.rowHeight=24;
}
base(bom,'K',rows.length+30);
bom.getRange('A2').values=[['PHBox final-assembly BOM']];
bom.getRange('A3').values=[['One wider-layout unit. Prepared 31 October 2026. Perth suppliers first.']];
bom.getRange('A4').values=[['HOLD PCB order: 22 unconnected items in the current hash-linked audit. Old manufacturing exports are stale.']];
bom.getRange('A5').values=[['16 switches. Fit 13 caps + 3 PLA plugs. Buy 16 caps for 3 spares. OLED/sockets/tactiles counted within PCBA if fitted.']];
bom.getRange('A4').format.font={name:'Arial',size:10,bold:true,color:'#9C4D00'};
bom.getRange('A7:G7').values=[['ID','Installed qty','Unit','Part','Specification','Preferred provider','Order action']];
bom.getRange('I7:K7').values=[['Fit and purchasing notes','Supplier source','CAD / project source']];
bom.getRange('A7:G7').format={fill:palette.ink,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',wrapText:true};
bom.getRange('I7:K7').format.font={name:'Arial',size:10,bold:true};
bom.freezePanes.freezeRows(7);bom.freezePanes.freezeColumns(4);
for(const [col,width] of Object.entries({A:7,B:12,C:12,D:32,E:66,F:23,G:31,H:3,I:112,J:105,K:125})) bom.getRange(`${col}7:${col}${rows.length+30}`).format.columnWidth=width;
let rn=8;const itemRows=[];const sectionRows=[];
for(const section of [...new Set(rows.map(r=>r.section))]) {
  sectionRows.push(rn);
  bom.getRange(`A${rn}:G${rn}`).format={fill:palette.pale,font:{name:'Arial',size:10,bold:true,color:palette.ink},borders:{bottom:{style:'thin',color:palette.line}}};
  bom.getRange(`D${rn}`).values=[[section]];
  bom.getRange(`A${rn}:G${rn}`).format.rowHeight=27;rn++;
  for(const r of rows.filter(r=>r.section===section)) {
    bom.getRange(`A${rn}:G${rn}`).values=[[r.id,r.qty,r.unit,r.part,r.spec,suppliers[r.provider].name,r.action]];
    bom.getRange(`I${rn}:K${rn}`).values=[[r.notes,r.source,r.cad?'Project CAD: '+r.cad:'']];
    bom.getRange(`A${rn}:G${rn}`).format.wrapText=true;
    bom.getRange(`I${rn}:K${rn}`).format.wrapText=true;
    bom.getRange(`A${rn}:K${rn}`).format.rowHeight=66;
    bom.getRange(`B${rn}`).setNumberFormat('0');
    bom.getRange(`B${rn}`).format.horizontalAlignment='right';
    itemRows.push({id:r.id,row:rn});rn++;
  }
}
bom.getRange(`G8:G${rn-1}`).conditionalFormats.add('beginsWith',{text:'HOLD',format:{fill:palette.amber,font:{bold:true,color:'#9C4D00'}}});

base(shop,'J',40);shop.tabColor='#687F91';
shop.getRange('A2').values=[['Suppliers and buying quantities']];
shop.getRange('A3').values=[['Checked 31 October 2026. Listed prices are pack prices. Quotes and shipping are not included.']];
shop.getRange('A4').values=[['No complete cost total: custom machining, acrylic, exact fasteners and foam remain unquoted.']];
shop.getRange('A6:G6').values=[['Supplier','Area / pickup','Purpose','Pack qty','Pack price','Currency','Availability / action']];
shop.getRange('I6:J6').values=[['Buying notes','Source']];
shop.getRange('A6:G6').format={fill:palette.ink,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',wrapText:true};
shop.getRange('I6:J6').format.font={name:'Arial',size:10,bold:true};
const order=['ple','multifix','searle','altronics','cdc','enex','foam','jaycar','keebz','rs','element14','keebart','additive','jlc','self'];
for(const [col,width] of Object.entries({A:29,B:42,C:51,D:10,E:12,F:10,G:76,H:3,I:122,J:118})) shop.getRange(`${col}6:${col}24`).format.columnWidth=width;
shop.freezePanes.freezeRows(6);shop.freezePanes.freezeColumns(1);
order.forEach((id,i)=>{const s=suppliers[id],row=i+7;
  shop.getRange(`A${row}:G${row}`).values=[[s.name,s.area,s.purpose,s.pack,s.price,s.currency,s.availability]];
  shop.getRange(`I${row}:J${row}`).values=[[s.note,s.url]];
  shop.getRange(`A${row}:G${row}`).format.wrapText=true;
  shop.getRange(`I${row}:J${row}`).format.wrapText=true;
  shop.getRange(`A${row}:J${row}`).format.rowHeight=72;
  shop.getRange(`D${row}`).setNumberFormat('0');shop.getRange(`E${row}`).setNumberFormat('0.00');
  shop.getRange(`D${row}:E${row}`).format.horizontalAlignment='right';
});

wb.recalculate();
const check=await wb.inspect({kind:'table',range:'Assembly BOM!A7:G14',include:'values,formulas',tableMaxRows:8,tableMaxCols:7,maxChars:2300});
console.log(check.ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},summary:'Final error scan',maxChars:1000});
console.log(errors.ndjson);
// Review both sheets, and the hardware/thermal region at normal reading scale.
for(const [name,sheet,range] of [['assembly-top','Assembly BOM','A1:G16'],['assembly-hardware','Assembly BOM','A28:G45'],['assembly-thermal','Assembly BOM',`A${itemRows.find(x=>x.id==='T01').row-1}:G${itemRows.find(x=>x.id==='A03').row}`],['suppliers','Buying guide','A1:G14'],['thermal-notes','Assembly BOM','I45:K53'],['shipped-suppliers','Buying guide','A15:G21']]) {
  const png=await wb.render({sheetName:sheet,range,scale:1,format:'png'});
  await fs.writeFile(path.join(here,`review/${name}.png`),new Uint8Array(await png.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(path.join(output,'PHBox-final-assembly-BOM.xlsx'));
await fs.writeFile(path.join(here,'review/verification.json'),JSON.stringify({date:'2026-10-31',rows:rows.length,sections:[...new Set(rows.map(r=>r.section))],itemRows,workbook:path.join(output,'PHBox-final-assembly-BOM.xlsx'),cadReferencesVerified:true},null,2));
console.log(JSON.stringify({bomLines:rows.length,sections:new Set(rows.map(r=>r.section)).size,workbook:path.join(output,'PHBox-final-assembly-BOM.xlsx')}));
