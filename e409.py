"""Erdos Problem #409 toolkit: f(n) = phi(n)+1 dynamics."""
import numpy as np
from sympy import isprime

def phi_sieve(N):
    phi = np.arange(N + 1, dtype=np.int64)
    for i in range(2, N + 1):
        if phi[i] == i:  # i prime
            phi[i::i] -= phi[i::i] // i
    return phi

def F_counts(N, phi):
    """F[n] = # iterations of f(n)=phi(n)+1 to reach a prime (0 if n prime).
    Convention: F[1] = 1 (1 -> 2). Uses f(n) < n for composite n>=4."""
    F = np.zeros(N + 1, dtype=np.int32)
    isp = np.zeros(N + 1, dtype=bool)
    isp[2:] = phi[2:] == np.arange(2, N + 1) - 1  # phi(p)=p-1 iff prime
    F[1] = 1
    for n in range(4, N + 1):
        if not isp[n]:
            F[n] = 1 + F[phi[n] + 1]
    return F, isp

def divisors_of(v):
    ds = []
    i = 1
    while i * i <= v:
        if v % i == 0:
            ds.append(i)
            if i != v // i:
                ds.append(v // i)
        i += 1
    return sorted(ds)

def inv_phi(v):
    """Exact list of all n>=1 with phi(n)=v. Standard recursive algorithm."""
    if v == 1:
        return [1, 2]
    if v % 2 == 1:
        return []
    ds = divisors_of(v)
    ps = [d + 1 for d in ds if isprime(d + 1)]
    ps.sort(reverse=True)  # largest primes first
    res = []
    def dfs(i, rem, cur):
        if rem == 1:
            res.append(cur)          # n itself
            if cur % 2 == 1:
                res.append(2 * cur)  # phi(2n)=phi(n) for odd n
            return
        for j in range(i, len(ps)):
            p = ps[j]
            pm1 = p - 1
            if pm1 > rem:
                continue
            if p == 2:
                # only exponents a>=2 here (a=1, i.e. factor 2^1, is handled
                # by the 2*cur emission above); contribution 2^{a-1}, a>=2
                r2 = rem
                pk = 2
                while r2 % 2 == 0:
                    r2 //= 2
                    pk *= 2
                    dfs(j + 1, r2, cur * pk)
                continue
            if rem % pm1:
                continue
            r2 = rem // pm1
            pk = p
            while True:
                dfs(j + 1, r2, cur * pk)
                if r2 % p:
                    break
                r2 //= p
                pk *= p
    dfs(0, v, 1)
    return sorted(set(res))

if __name__ == "__main__":
    N = 2 * 10**6
    phi = phi_sieve(N)
    # sanity: phi values
    assert phi[1] == 1 and phi[2] == 1 and phi[9] == 6 and phi[10] == 4
    # classical bound check: n <= 2*phi(n)^2 for all n>=1 (verify on range)
    ns = np.arange(1, N + 1)
    assert np.all(ns <= 2 * phi[1:] ** 2), "phi lower bound violated!"
    print("phi(n) >= sqrt(n/2) verified for all n <=", N)
    # validate inv_phi against brute force for v <= 1000 (needs n <= 2v^2 <= 2e6)
    from collections import defaultdict
    pre = defaultdict(list)
    for n in range(1, N + 1):
        if phi[n] <= 1000:
            pre[int(phi[n])].append(n)
    bad = 0
    for v in range(1, 1001):
        a = inv_phi(v)
        b = sorted(pre.get(v, []))
        if a != b:
            bad += 1
            print("MISMATCH v=", v, a[:8], b[:8])
    print("inv_phi validated exactly for all v <= 1000; mismatches:", bad)
