"""Regenerate sat plot with extended data through whatever n the solver reached."""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

DATA = Path("/home/user/workspace/erdos872/extended_results.json")
OUT = Path("/home/user/workspace/erdos872/sat_plot.png")

with DATA.open() as f:
    d = json.load(f)
rows = sorted([(int(k), v) for k, v in d.items()])
ns = [r[0] for r in rows]
sat_L = [r[1]["sat_L"] for r in rows]
sat_S = [r[1]["sat_S"] for r in rows]
half = [n // 2 for n in ns]
ratio_L = [s / n for n, s in zip(ns, sat_L)]
ratio_S = [s / n for n, s in zip(ns, sat_S)]
regret = [n // 2 - s for n, s in zip(ns, sat_L)]

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

ax = axes[0, 0]
ax.plot(ns, sat_L, "o-", label="sat_L (Long first)", color="#1f77b4")
ax.plot(ns, sat_S, "s-", label="sat_S (Short first)", color="#ff7f0e")
ax.plot(ns, half, "--", label="⌊n/2⌋ (max primitive)", color="gray", alpha=0.6)
ax.plot(ns, [n / math.e for n in ns], ":", label="n/e ≈ 0.368n", color="green", alpha=0.7)
ax.set_xlabel("n")
ax.set_ylabel("game length")
ax.set_title("sat_L(n), sat_S(n) vs n")
ax.legend()
ax.grid(alpha=0.3)

ax = axes[0, 1]
ax.plot(ns, ratio_L, "o-", label="sat_L / n", color="#1f77b4")
ax.plot(ns, ratio_S, "s-", label="sat_S / n", color="#ff7f0e")
ax.axhline(0.5, color="gray", linestyle="--", alpha=0.5, label="1/2")
ax.axhline(1 / math.e, color="green", linestyle=":", alpha=0.7, label="1/e")
ax.set_xlabel("n")
ax.set_ylabel("ratio")
ax.set_title("sat ratios — drift toward 1/e?")
ax.legend()
ax.grid(alpha=0.3)
ax.set_ylim(0.30, 0.65)

ax = axes[1, 0]
ax.plot(ns, regret, "o-", color="#d62728")
ax.set_xlabel("n")
ax.set_ylabel("⌊n/2⌋ - sat_L(n)")
ax.set_title("regret growth")
ax.grid(alpha=0.3)
# Overlay candidate fits
import numpy as np
ns_arr = np.array([n for n in ns if n >= 18])
re_arr = np.array([n // 2 - sat_L[i] for i, n in enumerate(ns) if n >= 18])
xs = np.log(ns_arr)
m, b = np.polyfit(xs, re_arr, 1)
ax.plot(ns_arr, m * np.log(ns_arr) + b, "--", color="purple", label=f"{m:.2f}·log(n) + {b:.2f}")
xs2 = np.array(ns_arr) ** 0.5
m2, b2 = np.polyfit(xs2, re_arr, 1)
ax.plot(ns_arr, m2 * xs2 + b2, ":", color="orange", label=f"{m2:.2f}·√n + {b2:.2f}")
m3, b3 = np.polyfit(ns_arr, re_arr, 1)
ax.plot(ns_arr, m3 * ns_arr + b3, "-.", color="black", label=f"{m3:.3f}·n + {b3:.2f} (linear)")
ax.legend()

ax = axes[1, 1]
# Plot the linear sat_L fit
ns_arr2 = np.array(ns)
sl_arr = np.array(sat_L)
mask = ns_arr2 >= 18
m4, b4 = np.polyfit(ns_arr2[mask], sl_arr[mask], 1)
ax.plot(ns, sat_L, "o", color="#1f77b4", label="sat_L data")
ax.plot(ns_arr2, m4 * ns_arr2 + b4, "--", color="red", label=f"linear fit (n≥18): {m4:.3f}·n + {b4:.2f}")
ax.plot(ns, [n / math.e for n in ns], ":", color="green", label="n/e")
ax.plot(ns, [n / 2 for n in ns], "--", color="gray", alpha=0.5, label="n/2")
ax.set_xlabel("n")
ax.set_ylabel("sat_L")
ax.set_title(f"Linear fit suggests sat_L ~ {m4:.3f}·n")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUT, dpi=140)
print(f"saved: {OUT}")
print(f"data points: {len(ns)} (n = {ns[0]}..{ns[-1]})")
print(f"linear sat_L fit slope: {m4:.4f}, 1/e = {1/math.e:.4f}")
