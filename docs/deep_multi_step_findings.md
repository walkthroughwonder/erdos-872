# Deep multi-step K_5 activation search (extended budget)

Outcome: **NEG within extended budget**. Depth tripled from 12 to 38 certified safe Maker-only moves. Still zero K_5 pair edges claimed.

## Setup

Ran [multi_step_exact_bounds_deep.py](../src/t2_reachability_code/multi_step_exact_bounds_deep.py), a copy of [multi_step_exact_bounds.py](../src/t2_reachability_code/multi_step_exact_bounds.py) with the budget knobs raised:

- `TIME_BUDGET_SECONDS = 570.0` (was 210.0)
- `MAX_EXPANSIONS = 200000` (was 50000)

Bound backend: same Dusart 2010 explicit bounds ([Dusart arXiv record](https://arxiv.org/abs/1002.0442)), no exact prime-counting backend available in this environment.

Instance witness: n = 10^20, δ = 1/8, Y = 316, 64 small primes, 2016 pair edges, q = 4806305873305829. K_5 primes {101, 103, 107, 109, 113}. All identical to the earlier runs.

## Result

Best-first certified Maker-only search finished at the time budget:

- `status = NEG_NO_POS_WITHIN_BUDGET`
- `wall_clock_seconds = 571.64`
- `expansions = 38`
- `seen_states = 359`
- `steps = 38`
- `captured_vertices = 40`
- `claimed_edges = 38`
- `claimed_k5_edges = 0 / 10`
- `all_k5_certified_safe_at_step = -1`

The greedy prefix that seeded the frontier: `(3, 101), (5, 103)`, both certified safe with margins 1.43 × 10^16 and 1.25 × 10^16, worst replies deletion of vertex 5 and deletion of vertex 7 respectively.

## What changed vs the earlier tightened run

The earlier [multi_step_exact_bounds run](../src/t2_reachability_code/multi_step_exact_bounds.out) reached 12 certified steps in 216 seconds. The deep run reached 38 certified steps in 572 seconds. That is a roughly linear extension in depth per unit time, which suggests the frontier does not blow up quickly (only 359 seen states for 38 expansions).

The initial-state diagnostics are identical: 64 moves certify safe, all ten K_5 pair edges remain certified unsafe as first moves with margin worse than -5.6 × 10^16, and the worst reply for every K_5 first move is still deletion of vertex 3.

## Interpretation

After 38 certified safe moves the search has captured 40 of the 65 small-prime vertices (including 4 of the 5 K_5 vertices as side-effects of moves like `(3, 101)`, `(5, 103)`, `(7, 107)`), and it still has not produced a certified safe K_5 pair activation. The certified frontier remains rich (only 38 of 359 seen states expanded), so the search is still budget-limited rather than exhausted.

This is a materially stronger negative result than the previous 12-step version, but it is not a proof of exclusion. Two limitations remain:

1. It is a Maker-only ordering search, not an adversarial strategy-tree proof. A real Prolonger against a real Shortener may take a different path.
2. The Dusart bounds are conservative. An exact `primecount` backend would further sharpen every interval and may unlock additional certified moves.

## Honest conclusion

The multi-step certified frontier is deep and diverse (38 steps, 359 seen states, no dead end reached), and no K_5 pair activation is certified safe anywhere on the explored frontier. This strengthens the intuition that the vertex-star obstruction persists beyond the initial state, but it is not a structural exclusion theorem.

## Next honest moves

- Run with an exact `primecount` backend to eliminate the Dusart slack.
- Search with a heavier expansion budget (24 hours would explore roughly `24 * 3600 / 15 ≈ 5700` expansions, versus 38 here) to see whether the certified frontier eventually admits a K_5 pair activation, or whether it structurally excludes them.
- Try a lexicographic monovariant as the earlier [monovariant analysis](monovariant_exclusion_analysis.md) suggested.
- Emphasize in any follow-up communication that this is a Maker-only Dusart-bounded certified frontier search, not a two-player adversarial proof.
