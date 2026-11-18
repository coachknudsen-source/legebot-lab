import numpy as np, pandas as pd, lab
ok = lambda b, m: print(('ok - ' if b else 'FEJL: ') + m)
df = lab.syntetisk('BTC', n=60000)
F = lab.forbered(df)
p = dict(lb=20, stopATR=0.5, tp1R=2.0, volF=1.2, limitATR=0.25)
pd_ = dict(N=20, M=10, stopATR=2.0)
alle = []
for setup in (0, 1, 2, 3):
    ind, ud, pnl, d = lab.simuler(F, setup, pd_ if setup == 3 else p)
    alle.append((setup, ind, ud, pnl))
    print(f"  setup {setup}: {len(ind)} handler, netto {pnl.sum():+.4f}, mindste {pnl.min() if len(pnl) else 0:+.4f}, største {pnl.max() if len(pnl) else 0:+.4f}")
# 1) ingen snyd med fremtiden: afkort data – handler der er lukket før snittet skal være identiske
cut = 40000
F2 = lab.forbered(df.iloc[:cut].copy())
for setup, ind, ud, pnl in alle:
    i2, u2, p2, _ = lab.simuler(F2, setup, pd_ if setup == 3 else p)
    a = [(x, y, round(z, 10)) for x, y, z in zip(ind, ud, pnl) if y < cut - 700]
    b = [(x, y, round(z, 10)) for x, y, z in zip(i2, u2, p2) if y < cut - 700]
    ok(a == b, f'setup {setup}: samme handler når fremtiden fjernes ({len(a)} handler)')
# 2) permutation bevarer fordelingen
rng = np.random.default_rng(1)
P = lab.permuter(df, rng)
rc = np.sort(np.log(df.c / df.o).values); rc2 = np.sort(np.log(P.c / P.o).values)
ok(np.allclose(rc[1:], rc2[1:], atol=1e-9) and abs(np.log(P.c.iloc[-1] / df.c.iloc[-1])) < 1e-6, 'permutation bevarer fordeling og slutkurs')
ok(not np.allclose(P.c.values[:5000], df.c.values[:5000]), 'permutation ændrer rækkefølgen')
ok((P.h >= P[['o', 'c']].max(axis=1) - 1e-9).all() and (P.l <= P[['o', 'c']].min(axis=1) + 1e-9).all(), 'blandede lys er gyldige (høj ≥ åbn/luk ≥ lav)')
# delvis permutation: kun i vinduet
Q = lab.permuter(df, rng, 10000, 20000)
ok(np.allclose(Q.c.values[:10000], df.c.values[:10000]), 'delvis permutation rører ikke data før vinduet')
# 3) risiko: et tab er højst ca. 1 % (+ gebyrer og gap)
tab = np.concatenate([x[3][x[3] < 0] for x in alle])
ok(len(tab) == 0 or tab.min() > -0.02, f'største tab pr. handel {tab.min() if len(tab) else 0:+.4f} (ca. −1 % risiko)')
# 4) regime bruger kun afsluttede timelys
reg_full = F['reg'][:cut - 100]; reg_cut = F2['reg'][:cut - 100]
ok((reg_full == reg_cut).all(), 'regimet ændrer sig ikke, når fremtiden fjernes')
# 5) limit-ordrer: indgang til maker-gebyr, og en ordre der ikke fyldes, giver ingen handel
lab.VENT = 0
i0, _, p0, _ = lab.simuler(F, 0, p)
ok(len(i0) == 0, 'ventetid 0 lys: ingen limit-ordre fyldes')
lab.VENT = 2
