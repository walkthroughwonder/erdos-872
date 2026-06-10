# Erdős #872 — Phase 1 Findings (supersedes Phase 0)

Exact retrograde-DP solve extended to n ∈ [4, 41] (in progress to 44). Optimal-trace extraction, two independent solver implementations cross-verified. Three Long-strategy heuristics benchmarked. Source files in `/home/user/workspace/erdos872/`.

## Headline numbers (n=4..41)

| n  | sat_L | sat_S | ⌊n/2⌋ | sat_L/n | regret |
|----|-------|-------|-------|---------|--------|
| 20 |   9   |  8    | 10    | 0.450   |  1     |
| 25 |  11   | 10    | 12    | 0.440   |  1     |
| 30 |  13   | 11    | 15    | 0.433   |  2     |
| 35 |  15   | 12    | 17    | 0.429   |  2     |
| 40 |  16   | 13    | 20    | 0.400   |  4     |
| 41 |  17   | 14    | 20    | 0.415   |  3     |

Full table at `extended_results.json`.

## Result 1 (corrected): the strong conjecture is likely FALSE

The original Phase 0 hypothesis was `sat_L(n) = n/2 - o(n)`. Extended data refutes this.

- `sat_L(n)/n` drifts downward across the range: 0.500 at n=10, 0.450 at n=20, 0.433 at n=30, 0.415 at n=41.
- Linear regression of `sat_L(n)` on `n` over n ∈ [18, 41]: `sat_L ≈ 0.367·n + 1.93`, R² = 0.974. This is a tighter fit than any sublinear regret model.
- Best sublinear-regret fits (log n, sqrt(n), n^0.6) all sit at R² ∈ [0.69, 0.72] — essentially indistinguishable, and clearly worse than the linear fit.
- Interpretation: the regret may itself be linear (slope ~0.13), in which case `sat_L(n) ~ c·n` for some `c ∈ [0.37, 0.42]` strictly less than 1/2.

If this asymptotic holds, the strong Erdős conjecture is FALSE and the weak one is true with ε = c.

## Result 2: Short's actual strategy (refutes Phase 0 hypothesis)

Phase 0 hypothesized that Short steals upper-half primes from the core C = (n/2, n]. Trace extraction shows this is wrong.

- Short plays small integers d ∈ [2, √n] (often d ∈ {4, 7, 13}).
- Each such move kills ⌊n/d⌋ multiples of d, many of which lie in C.
- Sample at n=30: Short plays 4, 7, 13. Playing 7 kills {14, 21, 28} ⊂ C. Playing 13 kills {26} ⊂ C. Playing 4 kills {8, 12, 16, 20, 24, 28}, of which {16, 20, 24, 28} ⊂ C. Net: only 7 of 15 elements of C end up in A.

This means the original pairing-strategy idea ("pair small primes with their 6p multiples") cannot succeed. The cumulative loss from small-divisor moves is at least Σ_{d=2}^{√n} n/d = Ω(n log log n) in the worst case — superlinear in any sublinear `o(n)` budget.

## Result 3: Long strategy benchmarking

| n  | optimal | v1 gap | v2 gap | v4 gap |
|----|---------|--------|--------|--------|
| 20 |   9     |   0    |   1    |   1    |
| 25 |  11     |   1    |   1    |   1    |
| 28 |  12     |   2    |   1    |   1    |
| 30 |  13     |   2    |   1    |   1    |
| 33 |  14     |   2    |   1    |   0    |
| 35 |  15     |   3    |   2    |   0    |
| 38 |  16     |   3    |   2    |   ?    |

- v1 (open with 6, greedy upper-half): gap grows from 0 to 3 across n ∈ [10, 38].
- v2 (open with 6, then most-threatened upper-half element): gap ∈ {0, 1, 2} across the range, max 2.
- v4 (v2 framework with 1-ply lookahead at each Long-turn): gap ∈ {0, 1} for n ∈ [10, 35], hits 0 at several n.

**v4 is the operational benchmark.** It is a simple, fully specified strategy that achieves `sat_L(n) - 1` empirically. If we can prove a matching lower bound on v4's performance, we get `sat_L(n) ≥ G_{v4}(n) ≥ ?`, an explicit function of n.

## The corrected conjecture

**Conjecture (revised).** `sat_L(n) ≥ n/e + O(1)` where `e = 2.718...`. Asymptotic ratio `sat_L(n)/n → c` for some constant `c ∈ [1/e, 1/2)`.

The `1/e ≈ 0.368` constant matches the linear regression slope of 0.367 to three decimals. This is consistent with a heuristic from the divisibility-poset structure: integers in `[2, n]` have Dickman-density of having no prime factor ≤ √n equal to ρ(2) ≈ 0.307; and the expected proportion of "safely-claimable" core elements after both players spend O(√n) moves is roughly 1/e if Short's small-divisor coverage is asymptotically optimal.

(This last paragraph is hand-wavy; the precise heuristic needs work. But the empirical 0.367 number is striking enough to warrant attention as the target constant.)

## Three proof-strategy frames

Frame 1 (pairing — likely WRONG): Long pairs small primes with composite responses. Refuted by the multiplicity of Short's small-divisor coverage.

Frame 2 (potential function): Track Φ(state) = # live core elements + α·(# live small primes). Show that Long can keep ΔΦ bounded under Short's best play, and that the game length equals Φ(start) - Φ(end).

Frame 3 (bipartite matching — most promising): Define bipartite graph G_n with left = damaging-move set [2, n/2], right = core C = (n/2, n], edges by divisibility. Short's moves correspond to removing left vertices (taking their entire right-neighborhood out of contention for A); Long's moves correspond to claiming right vertices (committing them to A). The game value equals the size of the maximum **anti-matching** Long can preserve, which by König-Egerváry duality equals |C| - (min vertex cover of an adversarial subgraph). Computing the asymptotic of this min vertex cover is the proof obligation.

## Lean 4 skeleton

Written to `Erdos872.lean`. Includes:
- `Board`, `play`, `valueLong`, `valueShort` definitions
- `satL`, `satS` derived
- Conjecture types: weak (`∃ ε. sat_L ≥ εn`), strong (`∀ ε. sat_L ≥ (1-ε)n/2`)
- Lemma stubs: `upper_half_primitive`, `long_reservoir_count`
- Theorem target: `satL_lower_bound_weak`
- Strategy spec: `strategy_v4`, conjecture `v4_gap_bound`

Several `sorry`'s remain; the structure is ready for Aristotle handoff.

## Recommended next step

1. Let solver finish to n=44 to confirm the asymptotic-ratio drift (in particular: is the 0.400 at n=40 the floor, or does it continue downward?).
2. Submit the updated GPT-5.5 Pro prompt with the corrected hypothesis (target: prove sat_L ≥ n/e).
3. In parallel, formalize the bipartite-matching framing (Frame 3) more carefully and seed it as a fallback prompt.
4. If Frame 3 yields a clean theorem, hand the lemma list to Aristotle for Lean 4 proofs.

## Files

- `solver_fast.py` — fast solver (memo + move ordering, alpha-beta removed for soundness)
- `solver_naive.py` — ground-truth verification solver
- `trace_extract.py` — optimal-PV extractor (revealed Short's small-divisor strategy)
- `strategy_test.py` — tests v1 and v2 strategies
- `strategy_v3.py` — v3 (was worse than v2; documented)
- `strategy_v4.py` — v4 with 1-ply lookahead, current best
- `regret_fit.py`, `regret_fit_v2.py` — growth-rate fitting
- `gpt55_prompt.md` — updated single-shot prompt for GPT-5.5 Pro
- `Erdos872.lean` — Lean 4 skeleton, ready for Aristotle
- `extended_results.json` — full sat_L, sat_S table through last completed n
- `overnight.log` — solver process log
- `sat_plot.png` — chart (stale, Phase 0; will be regenerated)
