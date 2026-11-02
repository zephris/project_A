* One representative 100n branch, not extracted whole-board PDN.
.param c_eff=100n esr=0.05 esl=1n
Itest 0 pdn AC 1
Rleak pdn 0 1G
Lesl pdn n1 {esl}
Resr n1 n2 {esr}
Ceff n2 0 {c_eff}
