# Notes on Erdős Problem #409: the forest structure of $n \mapsto \varphi(n)+1$

*Working notes, 22 July 2026. Prepared with Claude (Fable 5); every numerical claim below was machine-verified with the included code. The theorems are elementary and some may be folklore, but none are recorded on the problem page (erdosproblems.com/409, last edited 20 Dec 2025). Not peer-reviewed.*

## 0. The problem

Erdős Problem #409 (a problem of Finucane; cf. Guy, *Unsolved Problems in Number Theory*, B41). Let $f(n)=\varphi(n)+1$. Three questions are posed:

**Q1.** How many iterations of $f$ are needed before a prime is reached? (Write $F(n)$ for this count; OEIS A039651. Recorded remarks: $F(n)=o(n)$ trivially; $F(n)=1$ infinitely often (Cambie); "presumably the intended question is good upper bounds.")

**Q2.** Can infinitely many $n$ reach the same prime?

**Q3.** What is the density of $n$ which reach any fixed prime?

Additionally recorded on the discussion thread (checked 22 Jul 2026): (i) a conjecture, referenced to OEIS A229487, that only finitely many integers reach any fixed prime — i.e. Q2 conjecturally *no* and Q3 conjecturally *zero*; (ii) explicit constructed examples with $F(n)=67$ (e.g. $n=2548851069$), all reaching the prime $9005041$. Below: two unconditional theorems — Theorem 2 **proves the recorded finiteness conjecture for a full-density subfamily of primes** ($p\equiv3\bmod4$) — one conditional theorem on Q1, exact certified computations complementing the constructed records, and a quantitative branching analysis that turns out to sit in mild tension with the recorded conjecture.

## 1. Structure

Write $B(p)=\{n\ge 1: \text{the } f\text{-trajectory of } n \text{ contains } p\}$ (the **basin** of the prime $p$).

**Theorem 1.**
(i) $f(1)=f(2)=2$, and $f(n)$ is odd for every $n\ge 3$.
(ii) The fixed points of $f$ are exactly the primes.
(iii) If $n\ge 4$ is composite then $f(n)\le n-\sqrt n+1<n$.
(iv) Every trajectory reaches a prime in finitely many steps; hence $\mathbb{N}=\bigsqcup_p B(p)$ (with $1,2\in B(2)$).
(v) No even number $\ge 4$ is a value of $f$. Hence in the preimage forest, every even number is a leaf.
(vi) If $f(x)=m$ and $x\neq m$, then $x>m$ (so each tree grows strictly upward: no cycles).
(vii) $F(n)\le 5\sqrt n+1$ for all $n\ge 1$.

*Proof.* (i) $\varphi(n)$ is even for $n\ge 3$. (ii) $\varphi(p)+1=p$; conversely $\varphi(n)=n-1$ forces $n$ prime. (iii) The least prime factor $q$ of composite $n$ satisfies $q\le\sqrt n$, so $\varphi(n)\le n-n/q\le n-\sqrt n$. (iv) Immediate from (ii),(iii). (v) By (i), the only even value of $f$ is $2=f(1)=f(2)$. (vi) $\varphi(x)=m-1\le x-1$, with equality iff $x$ prime, in which case $x=m$. (vii) For composite $m\ge 4$, $m-f(m)\ge\sqrt m-1\ge\tfrac12\sqrt m$; so the number of composite iterates in $(x/2,x]$ is at most $(x/2)/(\tfrac12\sqrt{x/2})=\sqrt{2x}$, and summing dyadically, $F(n)\le \sqrt{2n}\,(1-2^{-1/2})^{-1}+O(1)\le 5\sqrt n+1$. $\square$

So the dynamics is a forest: one finite-or-infinite tree per prime, growing strictly upward, with all even numbers as leaves and all branching happening through odd composite nodes. **Q2 asks exactly: is some tree infinite?** Since each vertex has finitely many children ($\varphi(x)=v \Rightarrow x\le 2v^2$), by König's lemma a tree is infinite iff it has arbitrarily long chains, i.e. iff $F$ is unbounded on a single basin.

## 2. The 2-adic gate: Q2 and Q3 for almost all $p\equiv 3 \pmod 4$

**Theorem 2.** Let $p>3$ be a prime with $p\equiv 3\pmod 4$. Then
$$f^{-1}(p)\setminus\{p\}=\{2p\}\;\cup\;\{q^a,\,2q^a:\ q \text{ prime},\ q\equiv 3\ (\mathrm{mod}\ 4),\ a\ge 2,\ q^{a-1}(q-1)=p-1\}.$$
Consequently:
(a) If $p-1$ is **not** of the form $q^{a-1}(q-1)$ with $q\equiv 3\pmod4$ prime and $a\ge 2$ ("non-exceptional"), then $B(p)=\{p,2p\}$: **exactly two integers in all of $\mathbb N$ ever reach $p$.**
(b) The number of exceptional $p\le x$ is at most $\sqrt{2x}+O(x^{1/3}\log x)$.
(c) Since $\#\{p\le x: p\equiv 3\ (4)\}\sim x/(2\log x)$, statement (a) holds for **100% of primes $p\equiv3\pmod4$**. For these primes the answer to Q2 is *no* and to Q3 is *density zero* (indeed, the basin is finite of size 2).

*Proof.* Suppose $f(n)=p$, i.e. $\varphi(n)=p-1\equiv 2\pmod 4$. Write $n=2^b m$ with $m$ odd. Then
$$v_2(\varphi(n))=\max(b-1,0)+\sum_{q\mid m} v_2(q-1),$$
and each term of the sum is $\ge 1$. For this to equal $1$: either $m=1,\ b=2$ (so $n=4$, $\varphi=2$, $p=3$, excluded), or $m=q^a$ is a prime power with $v_2(q-1)=1$ (i.e. $q\equiv3\bmod4$) and $b\le 1$. Then $\varphi(n)=q^{a-1}(q-1)=p-1$; the case $a=1$ forces $q=p$, giving $n\in\{p,2p\}$. This proves the displayed classification. For (a): $2p$ is an even leaf by Theorem 1(v), so the tree stops. For (b): if $a=2$ then $q(q-1)=p-1\le x$ gives $q\le \sqrt{2x}$; for each $a\ge3$, $q^{a-1}\le x$ gives at most $x^{1/(a-1)}$ choices, and summing over $3\le a\le \log_2 x$ gives $O(x^{1/3}\log x)$. (c) follows since $\sqrt x = o(x/\log x)$. $\square$

**Certified verification.** For all $1620+12$ primes $p\equiv3\pmod4$, $3<p<30000$: exactly $1620$ have $B(p)=\{p,2p\}$, and the exceptional set is precisely
$$\{7,\ 19,\ 43,\ 163,\ 487,\ 1459,\ 4423,\ 6163,\ 14407,\ 19183,\ 22651,\ 26407\},$$
matching the $q^{a-1}(q-1)+1$ characterization exactly ($7,19,163,487,1459$ from $q=3$; $43,14407$ from $q=7$; $4423$ from $q=67$; etc.).

*Remark.* Theorem 2 does **not** resolve Q2/Q3 as posed (which quantify over all primes); it resolves them for a full-density subfamily and concentrates the open content entirely on $p\equiv1\pmod4$ (and the sparse exceptional $3\bmod 4$ primes).

## 3. Exact basins (certificates)

Using an inverse-totient solver validated exhaustively (all $v\le 2000$ against brute force over $n \le 8\cdot 10^6$, justified by $n\le 2\varphi(n)^2$, itself machine-checked on the range), **every basin $B(p)$ for every prime $p<30{,}000$ was computed exactly and is finite** (3,245 trees, zero truncations at caps of $4\cdot10^4$ nodes / $10^{12}$ values). Samples:

| $p$ | $B(p)$ |
|---|---|
| 2 | $\{1,2\}$ |
| 3 | $\{3,4,6\}$ |
| 5 | $\{5,8,10,12\}$ |
| 7 | $\{7,9,14,15,16,18,20,24,30\}$ |
| 11 | $\{11,22\}$ |
| 13 | 31 elements, height 4, max 138 |
| 61 | 57 elements, height 8, max 4314 |

Largest tree found: $p=21089$ with $|B|=5557$, height 17, max element 4,431,606. Tallest: $p=23509$, height 20, whose deepest chain is
$$115243\to108449\to98581\to84493\to80029\to79421\to77533\to74141\to73501\to71101\to70273\to60229\to53761\to52273\to48241\to45685\to36545\to29233\to26401\to24833\to23509,$$
machine-verified link by link.

## 4. Q1: a conditional unboundedness theorem, and data

**Theorem 3 (Dickson $\Rightarrow$ $F$ unbounded).** Fix $L\ge1$. For $t\ge1$ with $2^Lt\neq4$ define
$$q_i(t)=3^{i-1}2^{\,L-i+1}\,t-1\ (1\le i\le L),\qquad p(t)=2^{L+1}t-3 .$$
These $L{+}1$ linear forms form an admissible system. If $q_1,\dots,q_L,p$ are simultaneously prime, then with $m_i:=3q_i$ one has $f(m_{i+1})=m_i$ and $f(m_1)=p$, hence $F(3q_L)=L$ exactly. Under Dickson's conjecture this occurs for infinitely many $t$, for every $L$; hence $F$ is unbounded.

*Proof.* Since $q_{i+1}=(3q_i+1)/2$ by construction, $\varphi(3q_{i+1})=2(q_{i+1}-1)=3q_i-1=m_i-1$, using $\gcd(3,q_{i+1})=1$ (guaranteed by $2^Lt\ne 4$, which forces every $q_i>3$); and $\varphi(3q_1)=2(q_1-1)=2^{L+1}t-4=p-1$. Each $m_i$ is composite, so the trajectory of $3q_L$ takes exactly $L$ steps. Admissibility: all forms are odd; mod 3, choose $t\equiv2\ (3)$ for even $L$ and $t\equiv1\ (3)$ for odd $L$; mod $r\ge5$, $t\equiv0$ makes every $q_i\equiv-1$ and $p\equiv-3\not\equiv0$. $\square$

**Verified witnesses** (each trajectory literally iterated and checked): $L=3$: $t=1$, $F(51)=3$, lands on $13$. $L=4$: $t=2$, $F(321)=4$, lands on $61$. $L=5$: $t=2905$, $F(1{,}411{,}827)=5$, lands on $185{,}917$. $L=6$: $t=750155$, $F(1{,}093{,}725{,}987)=6$, lands on $96{,}019{,}837$.

**Data (exact computation of $F(n)$ for all $n\le10^7$).** Record values: $F=38$ at $n=7{,}754{,}613$ (terminal prime $30689$; the full 38-step trajectory is in the code output). Growth of $\max_{n\le 10^k}F$: $4,7,11,18,28,38$ for $k=2,\dots,7$ — strikingly linear in $\log n$. The distribution of $F$ has a geometric tail with ratio $\approx0.76$ per step. Note the trivial bound of Theorem 1(vii), $F(n)\le 5\sqrt n+1$, already improves the recorded "trivial $o(n)$", but the truth appears to be $\Theta(\log n)$:

**Conjecture C1.** $\max_{n\le x}F(n)\asymp\log x$. (Lower-bound mechanism: Theorem 3's chains have top element $\approx 2\cdot3^L t$; an effective form of Dickson/Bateman–Horn with polynomially bounded least solutions would give $\max_{n\le x}F(n)\gg\log x$ unconditionally-modulo-that-hypothesis.)

## 5. Q2 as a multitype branching process

By Theorem 1, a tree grows only through odd composite nodes $m$, whose children are the odd solutions $x$ of $\varphi(x)=m-1$. By the valuation identity in Theorem 2's proof, the fertility of $m$ is governed by its **type** $t=v_2(m-1)$: a child $x$ satisfies $\sum_{q\mid x}v_2(q-1)\ (+2\text{-part}) = t$, so type-1 parents ($m\equiv3\bmod4$) admit only prime-power children (rare), while higher types branch freely.

Measured mean-offspring matrices $M[t][t']$ (random odd $m\sim x$, types capped at 6) give Perron roots
$$\lambda \approx 1.10\ (x=10^4),\quad 1.17\ (10^5),\quad 1.09\ (10^6),\quad 1.17\ (3\cdot10^6),\quad 1.07\ (10^7),$$
with seed-to-seed noise $\pm0.1$ (offspring counts are heavy-tailed: totient multiplicities are unbounded). The matrix has a telling shape: fertile high-type parents pour most of their children into the sterile type-1 class.

So the process is **marginally supercritical** at every measured scale — yet **all 3,245 real trees in range go extinct**. These are compatible: with $\lambda\approx1.1$ and $P(\text{0 children})\approx0.75$–$0.79$, the survival probability per fertile root is small; 810+ type-$\ge3$ roots all dying bounds it at roughly $\lesssim0.4\%$ in this range. Hence:

**On the recorded conjecture.** The problem thread (via OEIS A229487) records the conjecture that every basin is finite. Our Theorem 2 *proves* this for 100% of primes $\equiv3\pmod4$. But the measured $\lambda>1$ means that, if the full conjecture is true, it is true *near criticality* — extinction is not comfortable but marginal, driven by fertile nodes dumping offspring into the sterile type-1 class. The honest alternatives: either $\lambda(x)\to\le1$ (conjecture safe, all basins finite), or $\limsup\lambda(x)>1$ and infinite basins exist but are rare (none below $30{,}000$, per-fertile-root survival $\lesssim0.4\%$ in range). The present data cannot separate these; we consider the reduction of Q2 to the asymptotics of this Perron root the main structural insight, and note it mildly *challenges* the recorded conjecture rather than supporting it.

**Conjecture C3.** Every basin has natural density zero. (Proved above for 100% of primes $\equiv3\bmod4$; open in general. Note it does not follow automatically even if $B(p)$ is infinite.)

## 6. What is actually new here, and what remains open

Already on the thread (not ours): the finiteness/density-zero conjecture (via A229487), and constructed examples with $F=67$. Apparently new here: Theorem 1(vii) ($F\le 5\sqrt n+1$, improving the recorded "trivially $o(n)$"); Theorem 2 with its certified exceptional-set verification — a *proof* of the recorded conjecture for a full-density subfamily of primes ($\equiv3\bmod4$), and as far as we can tell the first proven case of Q2/Q3 in any regime; Theorem 3 (Dickson $\Rightarrow$ $F$ unbounded, explicit admissible systems, verified witnesses to $L=6$); the exhaustive basin atlas to $30{,}000$ and exhaustive $F$-records to $10^7$ (complementing the thread's constructed examples); and the multitype-branching reformulation of Q2 with measured near-critical $\lambda$. The elementary ingredients of Theorem 2 (the 2-adic valuation of $\varphi$, the classification of $\varphi(n)\equiv2\bmod4$) are classical; we make no priority claim beyond "apparently unrecorded for this problem."

Still open: Q2 and Q3 in full (equivalently: is any tree infinite; the fate of $p\equiv1\pmod4$); unconditional unboundedness of $F$; any $F(n)\ll n^{o(1)}$ upper bound.

## 7. Code

`e409.py` (validated $\varphi$-sieve, $F$ DP, exact inverse totient), `basins.py` (exact basin BFS with certificates). All experiments reproducible in minutes on a laptop.
