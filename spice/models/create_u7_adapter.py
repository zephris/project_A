"""Create an attributed ngspice derivative; never edit TI's original."""
from pathlib import Path
import hashlib
root = Path(__file__).resolve().parent
source = root/'vendor/TPS2553/SLVM425A/TPS2553_PSPICE_TRANS/tps2553_trans.lib'
old = 'E_ABMGATE  YINT 0 VALUE {{IF(V(A) > {VTHRESH}  ^  \n+ V(B) > {VTHRESH},{VSS},{VDD})}}'
new = 'E_ABMGATE YINT 0 VALUE {IF(V(A)>{VTHRESH},IF(V(B)>{VTHRESH},{VDD},{VSS}),IF(V(B)>{VTHRESH},{VSS},{VDD}))}'
text = source.read_text()
assert text.count(old) == 1
out = root/'adapters/TPS2553_TRANS_ngspice.lib'
out.parent.mkdir(exist_ok=True)
out.write_text('* PHBox ngspice compatibility derivative, 2026-10-07.\n'
 '* Original TI file SHA256: '+hashlib.sha256(source.read_bytes()).hexdigest()+'\n'
 '* Only XNOR2_BASIC_GEN XOR expression rewritten as nested IFs.\n'
 '* Original vendor copyright/disclaimer follows; no other model changes.\n'+text.replace(old,new))
print(out)
