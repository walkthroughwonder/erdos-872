# Forum post draft: trap-aware refinement of the residual strategy in Erdős #872

Target venue: [erdosproblems.com/forum/thread/872](https://www.erdosproblems.com/forum/thread/872)

Posting handle: Ero23 (Edwin Rosero, May 23 2026)

## Body

Following [Om Buddhdev's manuscript](https://www.sensho.xyz/papers/erdos-872.pdf) (Apr 2026) and [Jonas Silva's note](https://github.com/jonaslsaa/maths/blob/main/872.pdf) (Apr 2026), the residual safe-edge hypothesis (Definition 4.5, used in Theorem 4.7 and Proposition A.9) remains open. Buddhdev's Proposition A.2 refutes the unrestricted version via a `K_4` fiber over four small primes `{13, 17, 19, 23}` and a common large prime `q`. The conditional T2 lower bound `L(n) >= c_delta n (log log n)^2 / log n` rests on whether the strategy-generated states avoid this refutation.

I have run an exhaustive finite-state enumeration on small multi-fiber rank-3 slot hypergraphs and on the rank-2 activation graph, and want to report three observations that may help close the gap.

### 1. Activation RSE holds in all tested cases

The rank-2 activation game (Proposition A.6) is the smaller of the two restricted hypothesis components. I built a finite-state enumerator that walks every reachable pre-Prolonger state under any Shortener strategy, then checks raw RSE at each.

  - `k = 3`: 7 non-terminal reachable states, 100 percent RSE pass.
  - `k = 4`: 169 non-terminal reachable states, 100 percent RSE pass.
  - `k = 5`: 12661 non-terminal reachable states, 100 percent RSE pass.

I also stress-tested with non-uniform initial token weights (uniform 1, uniform 2, uniform 3, a Mertens-decay pattern `(8, 6, 4, 5, 3, 2)`, a lopsided `(10, 1, 1, 1, 1, 1)`, and a two-heavy `(5, 5, 1, 1, 1, 1)`). All pass at 100 percent. This is computational support for the activation half of Buddhdev's restricted hypothesis at small `k`.

### 2. The residual RSE fails on isolated `K_4` fibers as Buddhdev predicted

In the rank-3 hypergraph game over a single fiber on `k` small primes (so `1 + k` slot vertices and `C(k, 2)` rank-3 hyperedges), the `K_4` case fails:

  - `k = 3`: 28 non-terminal reachable states, 100 percent RSE pass (and 100 percent under the dominant-capture certificate too).
  - `k = 4`: 1819 non-terminal reachable states, 216 RSE violations (11.87 percent). All violations share signature: 0 vertex deletions, exactly 2 ordinary captures, exactly 2 live edges remaining with combined potentials `(4, 8)` or `(8, 8)`.

Under any of three local Maker strategies (max-gain capture, dominant-capture, one-step lookahead), Shortener forces the violation in two rounds. The pattern is exactly Proposition A.2 reached by a different sequence: Maker captures `e_{1,2}`, Shortener edge-deletes `e_{1,3}`; Maker captures `e_{3,4}`, Shortener edge-deletes `e_{1,4}`; the remaining two live edges share all five captured slots and have `Phi = 8`. Shortener wins the next round.

### 3. A trap-aware refinement of the residual strategy makes RSE hold

I define a refinement of the residual Maker strategy that yields 100 percent RSE on every multi-fiber configuration tested. Call it strategy `v3`.

At every pre-Maker state `sigma`, for each live edge `f` in fiber `phi`:

  - mark `f` as a SAFE CAPTURE if after Maker's ordinary capture of `f` the fiber `phi` does NOT enter a near-trap state. The "near-trap" predicate is: post-capture, the fiber has `0` vertex deletions, `0` scored edges, `>= 1` ordinary capture (including this one), and `>= 1` live edge with `Phi >= 4`. Equivalently, no live edge has post-capture `Phi == 8`.
  - mark `f` as a SAFE SCORE if Maker plays alternate-scoring on `f`. Score is always safe because it removes `f` from live without changing any other edge's `Phi`.
  - mark `f` as UNSAFE if ordinary capture creates `Phi == 8` or otherwise triggers the near-trap predicate.

Maker then plays the SAFE CAPTURE with maximum `Q` gain. If no safe capture exists, Maker plays the SAFE SCORE with maximum `Q` gain. UNSAFE captures are never chosen if any safe move exists.

The intuition: the `K_4` failure is gated on reaching a "two-captures, no deletions" geometry. Strategy `v3` never enters that geometry because the second capture in any fiber is forbidden when it would create a `Phi == 8` live edge, and alternate-scoring is always available as a substitute.

### 4. Computational results

I checked `v3` on every reachable pre-Maker state under any Shortener strategy across eight multi-fiber configurations. For each, baseline `max_gain` Maker is included for comparison.

```
Config [4, 2]:     baseline 74 failures (32 K_k-sig hits),    v3: 0 / 0.
Config [4, 3]:     baseline 686 failures (320 K_k-sig hits),  v3: 0 / 0.
Config [4, 4]:     baseline 30808 failures (12320 K_k-sig),   v3: 0 / 0.
Config [3, 3, 3]:  baseline 576 failures (0 K_k-sig hits),    v3: 0 / 0.
Config [4, 3, 2]:  baseline 5008 failures (2128 K_k-sig),     v3: 0 / 0.
Config [3, 3]:     baseline 0 failures,                       v3: 0 / 0.
Config [3, 2, 2]:  baseline 0 failures,                       v3: 0 / 0.
Config [2, 2, 2, 2]: baseline 0 failures,                     v3: 0 / 0.
```

Larger configurations like `[5, 4]` and `[4, 4, 2]` exceed our enumeration budget of 8 million pre-Maker states; the smaller cases above are exhaustive.

Under `v3` against an adversarial Shortener, the achieved final score `S_fin` exceeds the `M/8` bound of Proposition A.3 in every case:

```
Config [4, 2]: |E| = 7, S_fin = 1 >= M/8 = 0.875.
Config [4, 3]: |E| = 9, S_fin = 2 >= M/8 = 1.125.
Config [4, 4]: |E| = 12, S_fin = 2 >= M/8 = 1.5.
Config [3, 3, 3]: |E| = 9, S_fin = 3 >= M/8 = 1.125.
```

### 5. Proposed refinement of Proposition A.9

If the above pattern extends to all `k` and all fiber multiplicities, Proposition A.9 could be strengthened by specifying the residual strategy as follows:

> Prolonger plays, at each pre-Prolonger state, an ordinary-capture move that does NOT cause any fiber to enter the near-trap state (no vertex deletion, no scored edge in fiber, no post-capture live edge with `Phi == 8`). Among such SAFE captures, Prolonger chooses one with maximum `Q` gain. If no safe capture exists, Prolonger plays an alternate-scoring move on a max-gain live edge.

The restricted safe-edge hypothesis applied to this refined strategy's state space appears to hold computationally for all small fiber configurations tested.

### Open mathematical question

The computational evidence is consistent across all tested configurations, but is not a proof. The remaining task is:

**Prove**: for the strategy `v3` above and any fiber configuration `(k_1, k_2, ..., k_F)` with `k_i >= 2` and disjoint slot supports, at every reachable pre-Maker state with at least one positive-weight live edge, the SAFE-CAPTURE-or-SAFE-SCORE set is nonempty AND the chosen `v3` move yields a per-round `Q` change `>= 0` under any Shortener reply.

A proof of this would make Theorem 4.7 of Buddhdev unconditional, improving the unconditional lower bound on `L(n)` from `(1/8 - o(1)) n loglog n / log n` to `c_delta n (loglog n)^2 / log n`.

### Code and data

All scripts and result files are at [github.com/walkthroughwonder/erdos-872](https://github.com/walkthroughwonder/erdos-872). Key files: `src/activation_rank2_rse.py`, `src/fiber_rse_check.py`, `src/multi_fiber_rse.py`, `src/k4_avoidance_v3.py`, plus JSON output for each enumeration in `results/`. The Lean 4 skeleton in `lean/Erdos872.lean` states the refined hypothesis but does not yet contain a proof.

I welcome any expert who can either prove the strategy invariant or construct a counterexample state outside the multi-fiber configurations I have tested. Buddhdev and Silva: would be great to hear if this resonates with what you have been thinking.

(Edwin Rosero, GitHub: [walkthroughwonder](https://github.com/walkthroughwonder), May 23 2026)
