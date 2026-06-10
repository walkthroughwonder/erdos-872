"""
Consolidate Phase 2 data and rebuild sat_plot.png + phase2_findings.md.

Inputs:
  - extended_results.json (sat_L, sat_S for n=4..42)
  - min_mp_sat_results_*.json (proven min_M = π(n) for n=10..200)
  - short_strategy_upper_*.json (sat_S_upper for n=4..78)
"""
import json
import os
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = "/home/user/workspace/erdos872"

# ---- Load data ----
with open(f"{ROOT}/extended_results.json") as f:
    ext = json.load(f)
# ext keys are stringified ints
ext = {int(k): v for k, v in ext.items()}

min_mp = {}
for p in glob.glob(f"{ROOT}/min_mp_sat_results_*.json"):
    with open(p) as f:
        d = json.load(f)
    for k, v in d.items():
        min_mp[int(k)] = v

short_ub = {}
for p in glob.glob(f"{ROOT}/short_strategy_upper_*.json"):
    with open(p) as f:
        d = json.load(f)
    for k, v in d.items():
        short_ub[int(k)] = v

# ---- Build merged table ----
all_n = sorted(set(ext) | set(min_mp) | set(short_ub))
table = []
for n in all_n:
    row = {"n": n}
    if n in ext:
        row["sat_L"] = ext[n].get("sat_L") or ext[n].get("v_L") or ext[n].get("game_L")
        row["sat_S"] = ext[n].get("sat_S") or ext[n].get("v_S") or ext[n].get("game_S")
    if n in min_mp:
        row["pi_n"] = min_mp[n]["pi_n"]
        row["min_M"] = min_mp[n]["min_M"]
    if n in short_ub:
        row["sat_S_upper"] = short_ub[n]["sat_S_upper"]
        row["pi_n"] = short_ub[n]["pi_n"]
    table.append(row)

# Save merged JSON
with open(f"{ROOT}/phase2_merged.json", "w") as f:
    json.dump(table, f, indent=2)
print(f"Wrote {ROOT}/phase2_merged.json with {len(table)} rows")

# ---- Show first few + last few ----
print("\nFirst rows:")
for r in table[:5]:
    print(" ", r)
print("Last rows:")
for r in table[-5:]:
    print(" ", r)

# ---- Build plot ----
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

ns = [r["n"] for r in table]
pi_n = [r.get("pi_n") for r in table]
sat_L = [r.get("sat_L") for r in table]
sat_S = [r.get("sat_S") for r in table]
min_M = [r.get("min_M") for r in table]
sat_S_ub = [r.get("sat_S_upper") for r in table]

# Panel 1: sat_S, sat_S_upper, π(n), min_M
ax = axes[0, 0]
ax.plot(ns, [v if v is not None else np.nan for v in pi_n], "k-", label="π(n) (theoretical lower bound)", lw=1.5)
ax.plot(ns, [v if v is not None else np.nan for v in min_M], "g.", label="min |M| (CP-SAT optimal)", ms=6)
ax.plot(ns, [v if v is not None else np.nan for v in sat_S], "ro", label="sat_S(n) (exact)", ms=6)
ax.plot(ns, [v if v is not None else np.nan for v in sat_S_ub], "b^", label="sat_S(n) upper bound (Short = smallest prime)", ms=4)
ax.set_xlabel("n")
ax.set_ylabel("size")
ax.set_title("Lower bound min |M| = π(n) and sat_S upper bound vs n")
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, alpha=0.3)

# Panel 2: gap sat_S_upper - π(n)
ax = axes[0, 1]
gap = [(sat_S_ub[i] - pi_n[i]) if sat_S_ub[i] is not None and pi_n[i] is not None else None for i in range(len(ns))]
xs = [n for n, g in zip(ns, gap) if g is not None]
ys = [g for g in gap if g is not None]
ax.step(xs, ys, where="post", color="purple", lw=2)
ax.scatter(xs, ys, color="purple", s=20)
ax.set_xlabel("n")
ax.set_ylabel("sat_S_upper(n) − π(n)")
ax.set_title("Gap: Short=smallest-prime upper bound minus π(n)")
ax.set_yticks([0, 1, 2, 3])
ax.grid(True, alpha=0.3)
# Mark transitions
for trans_n, label in [(25, "n=25"), (55, "n=55")]:
    if trans_n <= max(xs):
        ax.axvline(trans_n, color="gray", ls=":", alpha=0.5)
        ax.text(trans_n, 0.2, label, rotation=90, fontsize=8, va="bottom")

# Panel 3: sat_L behavior
ax = axes[1, 0]
xs_L = [n for n, v in zip(ns, sat_L) if v is not None]
ys_L = [v for v in sat_L if v is not None]
ax.plot(xs_L, ys_L, "go-", label="sat_L(n) (Long-first)", ms=5)
xs_pi = [n for n, v in zip(ns, pi_n) if v is not None]
ys_pi = [v for v in pi_n if v is not None]
ax.plot(xs_pi, ys_pi, "k-", label="π(n) (lower bound)", lw=1)
xs_half = [n for n in ns if n is not None]
ax.plot(xs_half, [n/2 for n in xs_half], "r--", alpha=0.5, label="n/2 (max antichain size)")
# Linear fit
if len(xs_L) >= 5:
    fit_xs = [x for x in xs_L if x >= 18]
    fit_ys = [y for x, y in zip(xs_L, ys_L) if x >= 18]
    if len(fit_xs) >= 5:
        p = np.polyfit(fit_xs, fit_ys, 1)
        ax.plot(xs_L, np.polyval(p, xs_L), "b:", lw=1,
                label=f"linear fit (n>=18): {p[0]:.4f}·n + {p[1]:.2f}")
ax.set_xlabel("n")
ax.set_ylabel("size")
ax.set_title("sat_L(n) and bounds (Long first)")
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, alpha=0.3)

# Panel 4: residual sat_S - π(n) (exact, where available)
ax = axes[1, 1]
xs_e = [n for n, sS, p in zip(ns, sat_S, pi_n) if sS is not None and p is not None]
ys_e = [sS - p for n, sS, p in zip(ns, sat_S, pi_n) if sS is not None and p is not None]
ax.step(xs_e, ys_e, where="post", color="darkred", lw=2, label="sat_S(n) − π(n) (exact)")
xs_u = [n for n, su, p in zip(ns, sat_S_ub, pi_n) if su is not None and p is not None]
ys_u = [su - p for n, su, p in zip(ns, sat_S_ub, pi_n) if su is not None and p is not None]
ax.step(xs_u, ys_u, where="post", color="steelblue", lw=2, alpha=0.6, label="sat_S_upper(n) − π(n)")
ax.set_xlabel("n")
ax.set_ylabel("residual")
ax.set_title("sat_S − π(n) refutes weak Erdős conjecture (would need O(n))")
ax.legend(loc="upper left", fontsize=9)
ax.set_yticks([0, 1, 2, 3])
ax.grid(True, alpha=0.3)

plt.suptitle("Erdős #872 Phase 2: sat_S(n) appears to be π(n) + O(log n)", fontsize=13, y=1.00)
plt.tight_layout()
out = f"{ROOT}/sat_plot.png"
plt.savefig(out, dpi=120, bbox_inches="tight")
print(f"Wrote {out}")
