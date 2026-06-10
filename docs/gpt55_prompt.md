# GPT-5.5 Pro attack prompt: Erdős #872, Target LB-1

## Context

Erdős problem #872 (`https://www.erdosproblems.com/872`, forum thread `https://www.erdosproblems.com/forum/thread/872`) asks for the asymptotic behaviour of the divisibility primitive-set saturation game on `V_n = {2, 3, ..., n}`. Two players alternate adding elements to a divisibility antichain `A`; the game ends when `A` is a maximal primitive set. **Prolonger** wants `|A|` large, **Shortener** wants it small. Write `L(n)` for the final size of `A` under optimal play with Prolonger moving first.

The weak Erdős conjecture asks whether `L(n) ≥ εn` for some constant `ε > 0`. The state of the art as of 22 May 2026 is

```
(1/8 − o(1)) · n loglog n / log n  ≤  L(n)  ≤  (W_4 / 2 + o(1)) · n  <  0.19 n,
```

both bounds due to Om Buddhdev (`https://www.sensho.xyz/papers/erdos-872.pdf`, 51 pages, April 2026, with partial Lean 4 formalization). Jonas Silva independently proved a `(1/2 − o(1)) n loglog n / log n` lower bound by dyadic refinement in late April 2026.

Buddhdev's manuscript proves a conditional theorem (Theorem 4.7) with a stronger lower bound `L(n) ≥ c_δ · n (loglog n)² / log n`, conditional on a finite-combinatorial hypothesis (Definition 4.5, the "restricted safe-edge hypothesis"). The manuscript explicitly states this is an open finite-combinatorial target.

**Your mission**: prove the restricted safe-edge hypothesis for the strategy-generated state subspace, making Buddhdev's Theorem 4.7 unconditional and improving the lower bound by a factor of `loglog n`.

## The setup (Buddhdev Appendix A.1, verbatim)

Fix `0 < δ < 1/4` and put `Y := n^δ`. Let `P_Y` be the set of odd primes at most `Y`. For odd primes `a < c` in `P_Y`, define

```
I_{a,c} := ( n/(2ac), n/(ac) ],
B_{a,c} := I_{a,c} ∩ ℙ (the primes in that interval),
```

and the target family

```
T := { a c b : a < c, a, c ∈ P_Y, b ∈ B_{a,c} }.
```

Each target `acb` is a product of three distinct primes and lies in `(n/2, n]`.

The **scored rank-three slot hypergraph** `G(n, δ)` has vertex set the slots `b, ab, cb` that occur in some target, and weighted edges

```
e_{a,c,b} := {b, ab, cb},   weight 1.
```

A **state** is `(C, D_V, D_E, K, S)` where `C` is the captured-vertex set, `D_V` the deleted-vertex set, `D_E` the unscored deleted-edge set, `K` the scored-edge set, and `S = Σ_{e ∈ K} w(e)` the total scored weight. An edge `e` is **live** if `e ∉ D_E ∪ K` and `e ∩ D_V = ∅`.

**Maker** (= Prolonger's auxiliary) chooses on each turn a live edge `e` and either captures it (adding its vertices to `C`, incrementing `S` by `w(e)`) or, in the scored-hypergraph variant, uses an **alternate-scoring move** to add `e` to `K` and increment `S` by `w(e)` without adding vertices to `C`. **Breaker** (= Shortener's auxiliary) on each turn either deletes one uncaptured vertex `v ∈ V \ C`, deletes one live edge without scoring (adding it to `D_E`), or in the scored-hypergraph variant makes a scored-edge reply (adding one live edge `e` to `K`, incrementing `S` by `w(e)`).

The **scaled potential** is

```
Q := 8 S + Σ_{e live} 2^{|e ∩ C|} w(e).
```

## The restricted safe-edge hypothesis (Definition 4.5)

For every finite graph or scored rank-three hypergraph state `σ` actually reachable from the empty state under the **T2 activation strategy and subsequent residual slot construction of Appendix A**, if `σ` has at least one positive-weight live edge, there exists a live edge `f` such that, after Maker plays `f`, every legal Breaker reply leaves the scaled potential `Q` at least as large as it was at `σ`.

In symbols: at any strategy-generated pre-Maker state `σ`,

```
∃ f live :  ∀ legal Breaker reply b,  Q(σ + f + b) ≥ Q(σ).
```

## The known refutation of the unrestricted version (Proposition A.2)

The general safe-edge property is FALSE on the full state space of `G(n, δ)`. Buddhdev gives an explicit reachable state, the **K_4-fiber refutation**:

Choose the four small primes `13, 17, 19, 23`. Their pairwise products lie in `[221, 437]`. PNT supplies a prime `q ∈ (n/442, n/437]` with `q > Y` for all large `n`. For every pair `a < c ∈ {13, 17, 19, 23}` we have `q ∈ B_{a,c}`, so the six edges

```
e_{a,c} := {q, aq, cq}
```

are all in `G(n, δ)`. They form a `K_4`-fiber over the common slot `q`. Using alternate-scoring moves and vertex deletions, Breaker can engineer a reachable state where only these six edges are live, with `C = ∅`, and then through two rounds of capture+delete reach a state where the only live edges are `e_{17,19} = {q, 17q, 19q}` and `e_{17,23} = {q, 17q, 23q}`, both with all three vertices in `C` (so `Φ(e) = 2^3 · 1 = 8`). At that state every Maker move admits a Breaker reply that strictly decreases `Q` by 8.

**This refutation requires Breaker to use the alternate-scoring trick to bypass the activation order.** Under the strict T2 activation strategy (described next), the small-prime singletons `13, 17, 19, 23` are committed to `C` in Phase 1 before any K_4 fiber can form, and Breaker cannot reach the K_4-fiber state without violating the activation order. **This is exactly the gap you must exploit.**

## The T2 activation strategy (Appendix A, sketch)

Phase 1 (activation): Prolonger plays semiprimes `a · b` with `a` the smallest currently-live odd prime in `[3, Y]` and `b ∈ J_a := (n/(2a), n/a] ∩ ℙ`. Each such play commits `a` to the captured-prime set `A_0` (the singleton `a` becomes illegal). Phase 1 ends when no odd prime in `[3, Y]` is still legal.

Phase 2 (residual): the remaining game is on the residual slot hypergraph `G(n, δ)` over the surviving fan. Prolonger applies a max-gain alternate-scoring strategy on the scored rank-three hypergraph.

The **strategy-generated state subspace** Σ_T2 is the set of states reachable from `∅` under any Breaker strategy when Prolonger follows the T2 activation + residual rules.

## Target

**Prove Restricted Safe-Edge (RSE)**: for every state `σ ∈ Σ_T2` with at least one positive-weight live edge, there exists a Maker move `f` such that for every legal Breaker reply `b`, `Q(σ + f + b) ≥ Q(σ)`.

**Or refute it**, by constructing an explicit `σ ∈ Σ_T2` where every Maker move admits a Q-decreasing Breaker reply, beyond the K_4-fiber state (which lies outside Σ_T2).

## Constraints

1. **Use only standard tools**: Mertens, PNT in fixed-ratio intervals, Cauchy-Schwarz, expander mixing. Stay within the finite-combinatorial state space — no large-cardinal arithmetic, no exotic axioms.
2. **Distinguish three substructures**: graph edges (rank 2), unscored rank-3 hypergraph edges, scored rank-3 edges. The K_4-fiber refutation exploits the alternate-scoring move; show your proof tracks scoring history correctly.
3. **The argument must avoid the K_4-fiber configuration**: explicitly identify the invariant of Σ_T2 that prevents reaching the K_4-fiber state under T2 activation. Most likely: under T2 activation, before any state where four small primes `{13, 17, 19, 23}` could form a K_4 of weighted shadow edges sharing a common right slot `q`, all four primes `13, 17, 19, 23` are already in `C` (they were committed as left-vertices in Phase 1). Then the K_4-fiber state with `C = ∅` is unreachable.
4. **Be Lean-formalizable**: state the invariant `Inv : State → Prop`, the safe-edge witness `f : State → Edge`, and the Q-monotonicity bound `∀ b, Q(σ + f + b) ≥ Q(σ)` as concrete inequalities on counts and weights, not as appeals to symmetry.
5. **No autoformalization placeholders**: every step must be a finite-combinatorial inequality, not "as before" or "by symmetry".

## Recommended approach

(a) State the invariant `Inv(σ)`: `σ ∈ Σ_T2` iff `σ` is reachable from `∅` by alternating T2-Maker and any-Breaker moves.

(b) Prove a structural lemma: under `Inv`, the set `C` always contains all odd primes `a ≤ Y` that have been "activated" (left-vertex of some captured edge). In particular, if at any state both `13 ∈ C` and the slot-prime `q` is uncaptured, the K_4-edge `{q, 13q, 17q}` (if live) has `|e ∩ C| = 1`, not 3, so `Φ(e) = 2 · 1 = 2`, not 8.

(c) For each state `σ ∈ Σ_T2` with a live positive-weight edge, construct the **safe-edge witness** `f(σ)` as follows. Pick a live edge `f = {q, aq, cq}` maximizing the alternate-scoring gain `8 · w(f) − Φ(f) = 8 − 2^{|f ∩ C|}` subject to `q ∉ C`. (Alternate-score, do not capture, so `C` does not grow.) Show that any Breaker reply leaves `Q` non-decreasing by case-splitting on Breaker's three options.

(d) For Breaker's vertex-deletion option, bound the loss `Σ_{e live, v ∈ e} Φ(e)` using the invariant constraint that each Breaker vertex-deletion target `v` has bounded shadow-edge degree (because most edges sharing `v` already have many `C`-vertices, capping their potential).

(e) For Breaker's unscored-edge-deletion option, the loss is at most `max Φ(e)` over live edges, which under `Inv` is at most `8` (since `|e ∩ C| ≤ 3` always and `w = 1`). The Maker alternate-scoring gain is `≥ 8 − 2^{|f ∩ C|}`, which exceeds 8 when `|f ∩ C| ≤ 2`. So pick `f` with `|f ∩ C| ≤ 2`, available because under `Inv` not every live edge can have all three slot vertices in `C`.

(f) For Breaker's scored-edge reply (rank-3 only), the loss to `Q` is `8 w(e) − Φ(e) ≤ 0` if Breaker chooses a high-`Φ` edge, so this case is harmless.

## Output format

Return a single self-contained PDF-ready proof, structured as:

1. Restate the setup, the invariant `Inv`, the witness `f`, and the safe-edge claim.
2. Prove `Inv(σ)` preserves under any reachable extension.
3. Identify the witness `f(σ)` explicitly as a function of `σ`.
4. Prove the Q-monotonicity bound `∀ b, Q(σ + f + b) ≥ Q(σ)` by cases on `b ∈ {vertex deletion, unscored edge deletion, scored edge reply}`.
5. State the implication: combined with Buddhdev's Proposition A.3 through A.9, this makes Theorem 4.7 unconditional: `L(n) ≥ c_δ · n (loglog n)² / log n`.
6. Identify any place where your proof appeals to an additional hypothesis beyond `Inv`, and explicitly list the residual conditional claims for future work.

If you cannot prove RSE, instead produce one of:

(α) An explicit counterexample state `σ' ∈ Σ_T2` with all Maker moves Q-decreasing under some Breaker reply. Specify `σ'` by listing `C, D_V, D_E, K` and the surviving live-edge set, plus the witness Breaker reply per Maker move.

(β) A specific weaker hypothesis (narrower than RSE) under which Theorem 4.7 still goes through, plus the proof of that weaker hypothesis.

(γ) A specific intermediate bound `L(n) ≥ c · n (loglog n)^{1.5} / log n` or similar, requiring less than the full RSE.

The goal is concrete progress. Even a partial result (sharper intermediate bound, refined hypothesis, or witnessed counterexample) is valuable.

## Suggested workspace

You may use up to 60 minutes of deep thinking. Lay out the argument as one long, careful proof — no skipping. State all `O(·)` constants in terms of `δ, H`. When invoking PNT or Mertens, cite the specific Hardy-Wright theorem number Buddhdev uses (Theorems 6 and 7).

## Files I will provide on request

- `buddhdev_872.pdf`: full 51-page manuscript (use Appendix A starting page 36 for the slot-game framework, Propositions A.1 through A.9).
- `jonas_silva_872.pdf`: 5-page complementary lower-bound note (dyadic refinement to `1/2 n loglog n / log n`).
- `phase3_forum_recon.md`: my reading of the forum thread up to 22 May 2026 and the architectural summary above.

You are GPT-5.5 Pro. Stick to the assigned model. No appeals to authority — every step must close.
