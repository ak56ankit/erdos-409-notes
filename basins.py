"""Exact basin computation for f(n)=phi(n)+1 dynamics (Erdos #409).

basin(p) = { n : f-trajectory of n reaches p }.
Structure used (proved separately):
  * f(n) odd for n>=3; f(1)=f(2)=2 -> only even value ever attained is 2.
  * so even m>=4 have no f-preimages: even nodes are leaves.
  * x in f^{-1}(m)  <=>  phi(x)=m-1;  and phi(x)<=x-1 => x>=m, x=m iff m prime.
    Hence children of node m are inv_phi(m-1) minus {m}, all strictly > m: no cycles.
"""
from e409 import inv_phi

def basin(p, node_cap=10**6, val_cap=10**12):
    """Exact basin of prime p. Returns dict with size,height,maxval,nodes(optional),
    truncated flag. Height = max #edges from root p."""
    nodes = {p: 0}
    frontier = [(p, 0)]
    truncated = False
    while frontier:
        m, d = frontier.pop()
        if m - 1 == 0:
            continue
        for x in inv_phi(m - 1):
            if x == m:
                continue  # the root fixed point (m prime) reproduces itself
            if x in nodes:
                continue  # cannot happen (x>m strictly), but be safe
            nodes[x] = d + 1
            if x % 2 == 1:  # odd nodes may have further preimages
                if x > val_cap or len(nodes) > node_cap:
                    truncated = True
                else:
                    frontier.append((x, d + 1))
    return {
        "p": p,
        "size": len(nodes),
        "height": max(nodes.values()),
        "maxval": max(nodes),
        "truncated": truncated,
        "nodes": nodes,
    }

def deepest_chain(p, **kw):
    b = basin(p, **kw)
    nodes = b["nodes"]
    h = b["height"]
    # reconstruct one deepest chain by walking down: node at depth d has f(node)=parent
    # parent of x is phi(x)+1
    from sympy import totient
    x = max((n for n, d in nodes.items() if d == h), key=lambda t: -t)
    chain = [x]
    while x != p:
        x = int(totient(x)) + 1
        chain.append(x)
    return b, chain
