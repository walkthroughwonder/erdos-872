# Erdős #872 Phase 3: Reconciliation with the forum literature

After collecting the full erdosproblems.com/forum/thread/872 (33 posts, Aug 2025 to May 2026), I now have the community's actual state of the art. Several of my Phase 2 conclusions were already known. Others remain partially novel. This document realigns the proof attack.

## Notation alignment (CRITICAL)

The forum and the wiki use `L(n)` for the **Prolonger-first** (== Long-first) game length under optimal play, where the player whose pick adds to A is also Prolonger (both players add). My code uses `sat_L` for the same thing.

When the forum says "the conjecture `L(n) ≥ εn`", that is the **Long-first** version. The `sat_S(n) ~ π(n) + O(1)` result I derived in Phase 2 is the **Short-first** version, which is different and was NOT the headline open question.

## What the community already has (as of 22 May 2026)

1. **Lower bound `L(n) ≥ (1 + o(1)) · n / log n`** (DesmondWeisenberg + Thomas Bloom, 11 Aug 2025). Argument: every prime in `[√n, n]` must have a multiple in any maximal primitive set, and these multiples are distinct. So any terminal `A` has `|A| ≥ π(n) − π(√n) = (1+o(1)) n/log n`.

2. **Refined lower bound `L(n) ≥ (1/8 − o(1)) · n loglog n / log n`** (Om_Buddhdev_sensho + GPT-5.4 Pro, 23 Apr 2026). "Fan capture" via semiprimes `pq ∈ (n/2, n]`.

3. **Refined lower bound `L(n) ≥ (1/2 − o(1)) · n loglog n / log n`** (Jonas Silva + GPT-5.5 Pro, 29 Apr 2026). Dyadic refinement of the fan-capture: H-secure small odd primes, then chains `C_pq = {pq, 2pq, 4pq, …}` for `n/2^(H+1) < pq ≤ n`. Link: [Jonas's PDF on GitHub](https://github.com/jonaslsaa/maths/blob/main/872.pdf).

4. **Upper bound `L(n) < 0.19n`** (Om_Buddhdev_sensho, 23 Apr 2026). Constant `W_4/2 ≤ 0.1897…`, fourth-order Bonferroni on Shortener's odd-prime-prefix strategy. **Has Lean partial formalization** (zero-sorry for the `5n/24` first-hit cover and the `13/36, 5/16` intermediate upper bounds).

5. **Aristotle Lean 4 formalization of the 23/48 upper bound** (Pommeret, 8 May 2026). Uses `IsCRespecting` to restrict Shortener's plays to "odd centers" C, then proves any maximal C-respecting play terminates in `≤ ⌈n/2⌉ − |C|/2` moves. Refined with Aristotle + Claude Opus 4.7. [Lean playground link in the thread](https://www.erdosproblems.com/forum/thread/872). natso26 (21 May 2026) confirms the result "has already been accepted as correct, but the formalization is not complete".

6. **Brenner's exact data up to N=120** (old-bielefelder relaying Frank Brenner, 20 May 2026). Optimal lengths for both starters AND for the two cooperative versions. At N=65: Short-first=20, Long-first=26, π(N)=18, ⌈N/2⌉=33.

7. **Surprising structural observation**: For N ∈ [105, 164], Short's optimal first move is BOTH 2 AND 3 (equi-optimal). For N < 105 move 3 is at most 1 worse than 2. No heuristic explanation yet (old-bielefelder, 21 May 2026).

## What I had right

- The lower-bound argument `min_M |M| = π(n)` for maximal primitive subsets is exactly what DesmondWeisenberg + Bloom established in Aug 2025. My CP-SAT verification (n ∈ [10, 200], optimal proofs) is novel computational confirmation but the *theorem* up to constants was already known.

- My `sat_S(n) − π(n) ∈ {0, 1, 2}` for `n ≤ 78` is **consistent with old-bielefelder's note (20 May 2026)** that "If player SHORT starts, the optimal game length seems to be much nearer to the lower bound `low(N) = π(N)`."

## What I had wrong

- I conjectured `sat_L(n) = π(n) + O(1)`. **Wrong.** My own data shows `sat_L − π` = 1, 2, 4 at n = 9, 21, 35 (growing). The forum has rigorous lower bounds showing `L(n) ≥ Ω(n loglog n / log n)`, far exceeding `π(n) + O(1)`.

- I conflated Short-first and Long-first variants. The Erdős problem statement asks `(1−ε)n/2` style, which is the Long-first quantity in the community's convention. My Phase 2 reframing claimed both conjectures were refuted by `sat_S ~ π(n)`, but the actual open problem is about `sat_L`.

## What is still potentially novel

1. **CP-SAT confirmation that `min_M |M| = π(n)` for n ∈ [10, 200]**, with explicit witnesses. Worth a short note.

2. **`sat_S(n) = π(n) + g(n)` with `g(n) ∈ {0, 1, 2}` for n ≤ 78** via the "Short plays smallest available prime" strategy. This gives an explicit, computable upper bound on Short-first game value. The community has Brenner's data up to N=120 but not, as far as I can see, an explicit strategy.

3. The structural transition points (n=25, n=55) for the gap. n=55 = 5·11 is the first n where 5 has a "free" semiprime above n/2 (since 5·11=55 < 60 = 5·12 and 11 is the first prime > √55).

## Updated proof attack plan

Given that the community's lower bound is `L(n) ≥ Ω(n loglog n / log n)` and the upper bound is `L(n) ≤ 0.19n`, the gap is between `n loglog n / log n` and `0.19n`. Closing this requires either:

- **Improving the upper bound** below `o(n)`. This would refute the weak Erdős conjecture and is the harder direction. Best current candidate: Lean-formalize the Bonferroni argument and try to extend the order to W_k → 0.

- **Improving the lower bound** to `Ω(n / loglog n)` or beyond, eventually to linear. This is the path to a positive resolution (Erdős conjecture proven).

The semiprime/fan-capture lower bound machinery is already at "right-star" plus dyadic refinement (Jonas Silva). The next obvious improvement would be **3-prime chains** `pqr ∈ (n/4, n]` with two free vertices to defend, which extends to `n (loglog n)^{k-1} / log n` for `k` factors (Bloom mentions this in post 16).

The most promising line: **formalize Jonas's dyadic argument in Lean**, then GPT-5.5 Pro tries to extend `H = O(loglog n)` instead of fixed `H = O(1)`, which would give `L(n) ≥ Ω(n (loglog n)^2 / log n)` or possibly a multi-tier improvement.

## Concrete next actions

1. (DONE) Reconfirm `min_M |M| = π(n)` for n ≤ 200 via CP-SAT. ✓
2. (DONE) Confirm `sat_S(n) − π(n) ∈ {0, 1, 2}` for n ≤ 78. ✓
3. (NEW) Reach out to Jonas Silva (GitHub: jonaslsaa) — his note PDF is on his repo. Read carefully.
4. (NEW) Inspect Om_Buddhdev_sensho's full 23 Apr 2026 post claim: `L(n) < 0.19n` AND lower bound `≥ (1/8 − o(1)) n loglog n / log n`, plus the Lean "shield-weight barrier" obstruction (Theorem A).
5. (NEW) Rewrite the GPT-5.5 Pro prompt to attack one of:
   - (a) Upper bound `L(n) ≤ c·n / log n` for some `c < 1`. (Stretch: refute weak conjecture cleanly.)
   - (b) Lower bound `L(n) ≥ Ω(n (loglog n)^2 / log n)` via Jonas's H-securing extended to multiple tiers.
   - (c) The `n=55 ↔ n=25` structural transition phenomenon — explain WHY Short cannot avoid these extra moves.
6. (DONE) Downloaded Buddhdev's 51-page manuscript and Jonas's 5-page note. Read Buddhdev cover-to-key-sections.

## Update 22 May 2026 (afternoon): full manuscript read

After reading Buddhdev's manuscript end to end (sections 1-9 plus Appendix A through Proposition A.3), the picture sharpens.

### Buddhdev's exact statement set

- **Theorem 1.1 (headline upper bound)**: L(n) ≤ (W_4/2 + o(1)) n, where W_4 := 1 − J_1 + J_2 − J_3 + J_4 from the 4th-order Bonferroni truncation at the bj envelope, with W_4/2 ≤ 0.1897123371.
- **Theorem 1.2 (unconditional lower bound)**: L(n) ≥ (1/8 − o(1)) n loglog n / log n. The factor 1/8 splits as (1/2 from Mertens half-saving on A_0) × (1/2 from PNT density of fan primes) × (1/2 from the right-capture Lemma 4.3).
- **Theorem 1.3 / Theorem A (shield-prefix obstruction)**: any shield-prefix proof of |A| ≥ |U_n| − cn through some P ⊆ U_n needs |P| ≥ n^(e^(−2c) − o(1)). For c = 1/2 − ε (i.e., L(n) ≤ εn) this forces |P| ≥ n^(1 − o(1)), so a sublinear prefix cannot prove sublinearity of L. Concretely at c = 0.19, |P| ≥ n^(e^(−0.38)) = n^0.684, so 0.19n requires a polynomial shield.
- **Theorem 1.6 (exact 5/24 first-hit cover)**: zero-sorry Lean. Min number of U_n elements that hit every L_n element by divisibility is (5/24)n + O(1).
- **Theorem 1.7 (intermediates)**: explicit Shortener strategies giving L(n) ≤ (13/36 + o(1)) n and L(n) ≤ (5/16 + o(1)) n. Both Lean-formalized.
- **Theorem 4.7 (conditional T2)**: L(n) ≥ c_δ · n (loglog n)^2 / log n conditional on a restricted safe-edge hypothesis (Definition 4.5).

### The architecture (cleanly)

1. **Shield reduction** (Section 3): for any maximal primitive A ⊆ V_n and any shield prefix P ⊆ A ∩ U_n, |A| ≥ |U_n| − β_n(P), where β_n(P) = max antichain shadow-weight in L_n(P).
2. **Polynomial shield-weight lower bound** (Section 4.1): β_n(P) ≥ ((1/2) log(1/α) − o(1)) n uniformly for |P| ≤ n^α. Proof uses Mertens primes-not-dividing-P estimate and the exchange argument (smallest primes maximize reciprocal mass under a log-budget).
3. **Unconditional fan-capture** (Section 4.2): Prolonger plays a 2-phase strategy. Phase 1 activates odd primes a ≤ n^δ as left-vertices of a bipartite fan with right primes b ∈ J_a := (n/(2a), n/a] ∩ P. Phase 2 uses Lemma 4.3 (max-degree right capture, C + X ≥ |E|/2). Combined: L(n) ≥ |E_0|/2 ≥ (1/8 − o(1)) n loglog n / log n.
4. **0.19n upper bound** (Section 7): Shortener pre-commits an odd-prime prefix; the surviving antichain's odd-part image avoids those primes; 4th-order Bonferroni + prime-sequence comparison (Lemma 7.9, Theorem 7.10) + half-density prime-rounding bridge (Lemma 7.11-7.15) translate from the real-valued envelope sequence (b_j) to actual primes (p_j). The Bonferroni truncation at order 4 with the (1/((h+1) log X)) envelope gives W_4/2 < 0.19.
5. **Three obstructions** (Section 8):
   - **Sherali-Adams barrier** (Prop 8.1): random-set transversal LPs have integrality gap ≥ ℓ−r, so level-r SA cannot prove transversal lower bounds beyond N/(ℓ−r) on these instances.
   - **q-shadow dichotomy** (Prop 8.2): for top-facet packet arguments, σ_q(D) + |B|δ_q > 1 − 4λ_q^2/r. In the regime L ~ h/log h, q ~ 2(log h)^2, separator starvation forces |B| > (e^(−1) − o(1)) h^2: pure expansion cannot supply unlimited fresh separators.
   - **Separator-only limitation** (Prop 8.3): if Sn is odd, |Sn| = o(r_1(n)), H(Sn) = o(1), then separator-only closure leaves n/2 − o(n) upper-half integers legal. So **no separator-only proof class** can prove L(n) = O(n (loglog n)^2 / log n) or even L(n) = o(n).

### What this means for our attack

- The shield-prefix obstruction (Theorem A) means any **static** upper-bound argument via U_n prefix faces a polynomial-prefix lower bound. To push below 0.19n one needs **dynamic** information: the actual game tree, not just the static incidence geometry of low-rank shadows.
- The Sherali-Adams barrier rules out a wide class of LP-based proofs.
- The separator-only limitation rules out any "just play odd primes" Prolonger lower-bound argument from beating n (loglog n)^2 / log n.
- The K_4-fiber refutation (Prop A.2) rules out the *general* safe-edge property in the rank-3 residual game, so any potential-function proof must restrict to the strategy-generated state subspace.

### The decisive target

Given these obstructions, the cleanest line of attack is:

**Target (UB-1)**: improve the unconditional upper bound to L(n) ≤ c n / log n for some constant c. This would refute the weak Erdős conjecture L(n) ≥ εn (showing L(n) = o(n)). The path: extend the Bonferroni truncation beyond order 4, or replace it with a **dynamic** Shortener strategy that tracks lower-half captures alongside the prefix.

**Target (LB-1)**: improve the unconditional lower bound to L(n) ≥ c n (loglog n)^2 / log n by proving the restricted safe-edge hypothesis (Def. 4.5) for the activation/residual strategies in Appendix A. This is exactly what Buddhdev's Theorem 4.7 leaves as the conditional gap.

**Target (LB-2)**: prove the **weak** Erdős conjecture L(n) ≥ εn for some constant ε > 0. This is the wide-open direction.

After weighing: **Target LB-1** is the highest-value tractable target. It requires only the finite combinatorics of the safe-edge hypothesis on a specific reachable subspace, not new asymptotic machinery. Buddhdev's appendix already gives the slot-game framework and the K_4-fiber refutation tells us exactly which states must be avoided. If GPT-5.5 Pro can produce a strategy-invariant Q-monotonicity proof for the Appendix A activation strategy, the conditional T2 theorem becomes unconditional.

**Target UB-1** is also tractable but harder: it requires an idea outside the static Bonferroni envelope.
