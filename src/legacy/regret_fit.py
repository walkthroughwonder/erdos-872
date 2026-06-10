"""
Fit candidate growth rates to regret(n) = floor(n/2) - sat_L(n).

Candidates:
  R(n) ~ c1 * log(n) + c0           (logarithmic)
  R(n) ~ c1 * sqrt(n) + c0          (square root)
  R(n) ~ c1 * n**0.6 + c0           (sub-linear power)
  R(n) ~ c1 * (log n)**2 + c0       (poly-log)

Uses least-squares on the full extended table from extended_results.json.
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
    """Return (slope, intercept, R^2) for y = slope*x + intercept."""
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
    # Restrict to n >= 10 to skip noise from tiny boards
    rows = [r for r in rows if r[0] >= 10]
    ns = [r[0] for r in rows]
    rs = [r[2] for r in rows]

    print("Extended data (n=10..40):")
    print(f"{'n':>3} {'floor(n/2)':>10} {'sat_L':>5} {'regret':>6}")
    for n, s, r in rows:
        print(f"{n:>3} {n//2:>10} {s:>5} {r:>6}")

    print()
    print("=" * 60)

    fits = []
    # log(n)
    xs = [math.log(n) for n in ns]
    m, b, r2 = linfit(xs, rs)
    fits.append(("c*log(n) + b", m, b, r2))

    # sqrt(n)
    xs = [math.sqrt(n) for n in ns]
    m, b, r2 = linfit(xs, rs)
    fits.append(("c*sqrt(n) + b", m, b, r2))

    # n^0.6
    xs = [n ** 0.6 for n in ns]
    m, b, r2 = linfit(xs, rs)
    fits.append(("c*n^0.6 + b", m, b, r2))

    # (log n)^2
    xs = [math.log(n) ** 2 for n in ns]
    m, b, r2 = linfit(xs, rs)
    fits.append(("c*log(n)^2 + b", m, b, r2))

    # n^0.5 * log(n) (occurs in primitive-set theory)
    xs = [math.sqrt(n) * math.log(n) for n in ns]
    m, b, r2 = linfit(xs, rs)
    fits.append(("c*sqrt(n)*log(n) + b", m, b, r2))

    # log-log fit: log(regret) ~ a * log(n) + b  -> regret ~ exp(b) * n**a
    # Use rows with regret > 0
    rows_pos = [(n, r) for n, r in zip(ns, rs) if r > 0]
    if rows_pos:
        lx = [math.log(n) for n, _ in rows_pos]
        ly = [math.log(r) for _, r in rows_pos]
        m, b, r2 = linfit(lx, ly)
        fits.append((f"power: c*n^a (a={m:.3f})", math.exp(b), m, r2))

    print("Fit comparison (sorted by R^2 descending):")
    print(f"{'model':<32} {'slope':>10} {'intercept':>12} {'R^2':>8}")
    for name, m, b, r2 in sorted(fits, key=lambda x: -x[3]):
        print(f"{name:<32} {m:>10.4f} {b:>12.4f} {r2:>8.4f}")

    # Predictions at n=44, 50, 100 using best logarithmic fit
    log_fit = next(f for f in fits if f[0] == "c*log(n) + b")
    m, b, _ = log_fit[1], log_fit[2], log_fit[3]
    print()
    print("Extrapolations under c*log(n) + b model:")
    for N in [44, 50, 100, 1000]:
        pred = m * math.log(N) + b
        print(f"  n={N}: predicted regret={pred:.2f}, predicted sat_L={N//2 - pred:.2f}")


if __name__ == "__main__":
    main()
