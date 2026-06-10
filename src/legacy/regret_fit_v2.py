"""
Refit using only the post-boundary regime n>=18 where regret is monotone non-negative,
and consider asymmetric models (sat_L >= an, sat_L >= n/2 - b*g(n)).
"""
from __future__ import annotations
import json, math
from pathlib import Path

DATA_PATH = Path("/home/user/workspace/erdos872/extended_results.json")


def load_table():
    with DATA_PATH.open() as f:
        d = json.load(f)
    rows = []
    for k, v in d.items():
        n = int(k)
        sat_L = int(v["sat_L"])
        regret = n // 2 - sat_L
        rows.append((n, sat_L, regret))
    rows.sort()
    return rows


def linfit(xs, ys):
    n = len(xs)
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    denom = n * sxx - sx * sx
    if denom == 0:
        return 0.0, sy / n, 0.0
    m = (n * sxy - sx * sy) / denom
    b = (sy - m * sx) / n
    ymean = sy / n
    ss_tot = sum((y - ymean) ** 2 for y in ys)
    ss_res = sum((y - (m * x + b)) ** 2 for x, y in zip(xs, ys))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return m, b, r2


def main():
    rows = load_table()
    rows = [r for r in rows if r[0] >= 18]  # post-boundary
    ns = [r[0] for r in rows]
    sats = [r[1] for r in rows]
    rs = [r[2] for r in rows]

    print("Stable regime (n>=18):")
    print(f"{'n':>3} {'sat_L':>5} {'sat_L/n':>8} {'regret':>6}")
    for n, s, r in rows:
        print(f"{n:>3} {s:>5} {s/n:>8.4f} {r:>6}")

    print()

    # Fit sat_L = a*n + b (linear)
    m, b, r2 = linfit(ns, sats)
    print(f"sat_L = {m:.4f}*n + {b:.4f}  (R^2 = {r2:.4f})")

    # Fit sat_L = a*n directly (no intercept) -- get sat_L / n trend
    # We want a precise asymptotic ratio. Use last 10 points only.
    tail = rows[-10:]
    avg_ratio = sum(r[1] / r[0] for r in tail) / len(tail)
    print(f"Avg sat_L/n on last 10 points (n={tail[0][0]}..{tail[-1][0]}): {avg_ratio:.4f}")

    # Fit regret with linear, then with all the sublinear models again, on stable regime
    print()
    print("Regret fits (stable regime):")
    models = [
        ("linear: c*n", lambda n: n),
        ("log(n)", lambda n: math.log(n)),
        ("sqrt(n)", lambda n: math.sqrt(n)),
        ("n^0.5*log(n)", lambda n: math.sqrt(n) * math.log(n)),
        ("n^0.6", lambda n: n**0.6),
        ("log(n)^2", lambda n: math.log(n)**2),
        ("n / log(n)", lambda n: n / math.log(n)),
    ]
    print(f"{'model':<24} {'slope':>10} {'intercept':>12} {'R^2':>8}")
    for name, f in models:
        xs = [f(n) for n in ns]
        m, b, r2 = linfit(xs, rs)
        print(f"{name:<24} {m:>10.4f} {b:>12.4f} {r2:>8.4f}")

    # Power-law log-log fit on regret >= 1
    pos = [(n, r) for n, r in zip(ns, rs) if r > 0]
    lx = [math.log(n) for n, _ in pos]
    ly = [math.log(r) for _, r in pos]
    m, b, r2 = linfit(lx, ly)
    print(f"\nLog-log fit: log(regret) = {m:.3f}*log(n) + {b:.3f}  (R^2 = {r2:.4f})")
    print(f"  => regret ~ {math.exp(b):.4f} * n^{m:.3f}")

    # Test specific bound forms.
    # Hypothesis H1: sat_L(n) >= ceil(n/2) - C*log2(n).  Find min C.
    print("\nHypothesis: sat_L(n) >= ceil(n/2) - C*log2(n).  Min C that fits:")
    cs = [(n // 2 - s) / math.log2(n) for n, s in zip(ns, sats) if math.log2(n) > 0]
    print(f"  max C across n>=18: {max(cs):.4f}")

    # H2: sat_L >= n/2 - C*sqrt(n)
    cs = [(n // 2 - s) / math.sqrt(n) for n, s in zip(ns, sats)]
    print(f"H2: sat_L(n) >= n/2 - C*sqrt(n).  Min C: {max(cs):.4f}")

    # H3: sat_L >= 0.4 * n (asymptotic)
    cs = [s / n for n, s in zip(ns, sats)]
    print(f"H3: sat_L(n)/n minimum on n>=18: {min(cs):.4f}")

    # H4: sat_L >= n/2 - C * n^0.6
    cs = [(n // 2 - s) / (n**0.6) for n, s in zip(ns, sats)]
    print(f"H4: sat_L(n) >= n/2 - C*n^0.6.  Min C: {max(cs):.4f}")


if __name__ == "__main__":
    main()
