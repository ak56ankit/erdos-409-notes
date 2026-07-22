"""verify.py -- one-command reproduction of every claim in erdos409.pdf.

Usage:
    python verify.py            # full run (F(n) to 10^7; ~1-5 min, ~1-2 GB RAM)
    python verify.py --fast     # lighter run (F(n) to 10^6)
    python verify.py --lambda   # additionally measure the branching Perron root

Run this from the folder containing e409.py and basins.py.
"""
import sys, time
import numpy as np
from sympy import isprime, totient, primerange

from e409 import phi_sieve, inv_phi
from basins import basin, deepest_chain

FAST = "--fast" in sys.argv
DO_LAMBDA = "--lambda" in sys.argv

PASS = 0
FAIL = 0
def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}   {detail}")

t0 = time.time()
print("== 1. Your own theorems, checked against the code ==")
check("inv_phi(10) == [11, 22]          (Task: basin of 11)",
      inv_phi(10) == [11, 22], str(inv_phi(10)))
check("inv_phi(22) == [23, 46]          (your Task 3)",
      inv_phi(22) == [23, 46], str(inv_phi(22)))
check("inv_phi(42) == [43, 49, 86, 98]  (your Task 4)",
      inv_phi(42) == [43, 49, 86, 98], str(inv_phi(42)))

print("== 2. Independent brute-force cross-validation of inv_phi ==")
V = 500
N = 2 * V * V  # n <= 2*phi(n)^2 guarantees completeness of the brute force
phi = phi_sieve(N)
from collections import defaultdict
pre = defaultdict(list)
for n in range(1, N + 1):
    if phi[n] <= V:
        pre[int(phi[n])].append(n)
bad = [v for v in range(1, V + 1) if inv_phi(v) != sorted(pre.get(v, []))]
check(f"inv_phi(v) matches exhaustive enumeration for ALL v <= {V}",
      not bad, f"mismatches at v={bad[:5]}")

print("== 3. Dickson-ladder witnesses, by direct iteration (sympy only) ==")
def F_direct(n):
    steps = 0
    while not isprime(n):
        n = int(totient(n)) + 1
        steps += 1
    return steps, n
for n_start, L_expect, p_expect in [(51, 3, 13), (321, 4, 61),
                                    (1411827, 5, 185917),
                                    (1093725987, 6, 96019837)]:
    L, p = F_direct(n_start)
    check(f"F({n_start}) = {L_expect}, landing on {p_expect}",
          (L, p) == (L_expect, p_expect), f"got F={L}, p={p}")

print("== 4. The height-20 chain above p=23509, link by link ==")
b23509, chain = deepest_chain(23509)
links_ok = all(int(totient(chain[i])) + 1 == chain[i + 1]
               for i in range(len(chain) - 1))
check("every link satisfies f(x) = next", links_ok)
check("chain has 20 steps and ends at 23509",
      len(chain) == 21 and chain[-1] == 23509,
      f"len={len(chain)}, end={chain[-1]}")

print("== 5. Basin sweep: all primes p < 30000 ==")
EXPECT_EXC = {7, 19, 43, 163, 487, 1459, 4423, 6163, 14407, 19183, 22651, 26407}
n_ok = 0
exc = set()
truncated = []
largest = (0, None)   # (size, p)
tallest = (0, None)   # (height, p)
for p in primerange(2, 30000):
    bb = basin(p, node_cap=40000, val_cap=10**12)
    if bb["truncated"]:
        truncated.append(p)
    if bb["size"] > largest[0]:
        largest = (bb["size"], p)
    if bb["height"] > tallest[0]:
        tallest = (bb["height"], p)
    if p % 4 == 3 and p > 3:
        if bb["size"] == 2:
            n_ok += 1
        else:
            exc.add(p)
check("every basin finite (zero truncations)", not truncated, str(truncated[:5]))
check("exactly 1620 primes = 3 mod 4 have basin {p, 2p}",
      n_ok == 1620, f"got {n_ok}")
check("exceptional set is exactly the predicted 12 primes",
      exc == EXPECT_EXC, f"got {sorted(exc)}")
check("largest tree: 5557 elements at p=21089",
      largest == (5557, 21089), str(largest))
check("tallest tree: height 20 at p=23509",
      tallest == (20, 23509), str(tallest))

print("== 6. Exhaustive F(n) records ==")
NF = 10**6 if FAST else 10**7
phiF = phi_sieve(NF)
ispL = (phiF[2:] == np.arange(2, NF + 1) - 1).tolist()
ispL = [False, False] + ispL          # index-aligned: ispL[n] for n>=0
phL = phiF.tolist()
F = [0] * (NF + 1); F[1] = 1
for n in range(4, NF + 1):
    if not ispL[n]:
        F[n] = 1 + F[phL[n] + 1]
Fa = np.array(F, dtype=np.int32)
decade = [int(Fa[:10**k + 1].max()) for k in range(2, (6 if FAST else 7) + 1)]
if FAST:
    check("decade records (10^2..10^6) = [4, 7, 11, 18, 28]",
          decade == [4, 7, 11, 18, 28], str(decade))
else:
    check("decade records (10^2..10^7) = [4, 7, 11, 18, 28, 38]",
          decade == [4, 7, 11, 18, 28, 38], str(decade))
    check("max F on [1,10^7] is 38, attained at n=7754613",
          int(Fa.max()) == 38 and int(Fa.argmax()) == 7754613,
          f"max={int(Fa.max())} at {int(Fa.argmax())}")

if DO_LAMBDA:
    print("== 7. (optional) Branching Perron root at scale 10^5 ==")
    import random
    random.seed()  # fresh seed on purpose: you are measuring, not replaying
    TMAX = 6
    def vtype(n):
        v = 0; n -= 1
        while n % 2 == 0:
            n //= 2; v += 1
        return min(v, TMAX)
    x, R = 10**5, 200
    M = np.zeros((TMAX, TMAX))
    for t in range(1, TMAX + 1):
        cnt = np.zeros(TMAX)
        for _ in range(R):
            while True:
                m = random.randrange(x | 1, 2 * x, 2)
                if vtype(m) == t:
                    break
            for c in inv_phi(m - 1):
                if c % 2 == 1 and c != m:
                    cnt[vtype(c) - 1] += 1
        M[t - 1] = cnt / R
    lam = max(abs(np.linalg.eigvals(M)))
    print(f"  measured Perron root lambda = {lam:.3f}")
    print(f"  (expected band ~0.95-1.35; heavy-tailed noise of +/-0.1 per run is normal;")
    print(f"   outside 0.9-1.4 on repeated runs -> pause and investigate before posting)")

print(f"\n== SUMMARY: {PASS} passed, {FAIL} failed, {time.time()-t0:.0f}s ==")
if FAIL == 0:
    print("ALL PASS. The verification sentence in the PDF is now true on this machine.")
sys.exit(0 if FAIL == 0 else 1)
