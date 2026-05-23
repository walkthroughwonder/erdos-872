# v3 strategy critique for Erdős #872

## Section 1: Manuscript citation audit

### High-level correction

The requested phrase "Buddhdev Section 3 (slot-game definitions)" is itself incorrect. Section 3 of the manuscript is the shield-reduction argument, not the slot-game setup. The slot-game definitions used by the T2 conditional argument are in Section 4.3 and Appendix A.1, especially the paragraph "Auxiliary slot game and potential" before Proposition A.1.

### References in `v3_proposition_a9_refinement.md`

- **Line 5: residual slot hypergraph after activation. PARTLY CORRECT.** Buddhdev does define a residual scored rank-three slot hypergraph after activation. However, the actual residual edge is `e_{a,c,b} = {b, ab, cb}`. The v3 sketch's `V={q} cup B` and edge form `{a_e b_e, a'_e b'_e, q}` is only the special case of fixing a large prime `q=b`, not the general residual hypergraph.

- **Line 8: "fiber over a pair `{a,a'}`" and slot-disjoint fibers. INCORRECT / MISFORMALIZED.** Proposition A.2's `K_4` fiber is over a common large slot `q`, with six edges indexed by the six pairs among `{13,17,19,23}`. In that geometry, two edges such as `{q,13q,17q}` and `{q,13q,19q}` share two vertices (`q` and `13q`), not merely `q`. Thus the sketch's claimed pair-fiber decomposition is not Buddhdev's obstruction geometry and its "different fibers share at most q" assertion is false for the natural `q`-fiber.

- **Line 9: state tuple `(C_sigma, D_V, D_E, K, S_sigma)`. PARTLY CORRECT.** Appendix A.1 gives captured vertices `C`, deleted vertices `D_V`, unscored deleted edges `D_E`, scored edges `K`, and score `S`. But the code adds a separate `captured_edges` set, and the near-trap predicate uses ordinary-capture counts. That information is not explicitly part of Buddhdev's stated tuple.

- **Line 10: `Phi_sigma(f) in {0,2,4,8}` and deleted-vertex clause. INCORRECT.** Buddhdev's scaled potential is `Q := 8S + sum_{e live} 2^{|e cap C|} w(e)`. For a unit-weight live rank-3 edge, `Phi` is `1,2,4,8`, not `{0,2,4,8}`. Deleted vertices are handled by the definition of "live"; there is no extra "captured vertex incident to a deleted vertex" clause in Appendix A.1.

- **Line 11: `Q_sigma = sum Phi*w`; Prop A.3 asks for `S_final >= M/8`. HALF INCORRECT.** Proposition A.3 indeed gives the final one-eighth bound. But Buddhdev's potential includes the score term `8S`; it is not just the sum over live edge potentials. Also `Phi` already includes the weight in Buddhdev's notation (`Phi(e)=2^{|e cap C|}w(e)`), so multiplying again by `w_sigma(f)` double-counts if read literally.

- **Line 28: Proposition A.2 K4 refutation. MOSTLY CORRECT, but the near-trap parameters are not Buddhdev terminology.** Proposition A.2 is exactly a `K_4`-fiber refutation using small primes `{13,17,19,23}` and a common large prime `q` in `(n/442,n/437]`. It reaches a state with two remaining live edges, both with `Phi=8`, after two Maker captures and two Breaker edge deletions. Buddhdev does not define `c_phi` or `Tau_phi`; those are v3 inventions.

- **Line 53: "items imply Proposition A.3 ... and Theorem 4.7 unconditionally." INCORRECT AS STATED.** Proposition A.3 requires full-round nondecrease of Buddhdev's `Q`, not a bound of `Q_after >= Q_before - 8 w_max`. A per-round loss bound does not imply `S_fin >= M/8` unless an additional summable accounting argument is proved. The line also omits the exact activation/residual hypotheses of Proposition A.9.

- **Line 65: "Buddhdev Lemma 4.4 (max-degree right capture)." INCORRECT.** The maximum-degree right-capture lemma is Lemma 4.3, not Lemma 4.4. Theorem 4.4 is the unconditional fan-capture lower bound. More importantly, Lemma 4.3 is a bipartite fan lemma, not a rank-3 slot-game bound on arbitrary vertex-deletion losses after a max-`Delta_Q` capture.

- **Lines 72-76: Section 8 warning attributed to Buddhdev. INCORRECTLY ATTRIBUTED.** Section 8 contains three obstruction results: Sherali-Adams transversal barrier, q-shadow covering dichotomy, and separator-only limitation. It does not state the v3-specific warning that "any potential-function proof must restrict to the strategy-generated state subspace." That warning is in Section 4.3 / Remark 4.6 and Appendix A around Proposition A.2/A.3, not Section 8.

- **Line 86: "Item (ii) follows from standard slot-game amortization." UNSUPPORTED.** Proposition A.3's proof is simple monotonicity of `Q`, not a hidden amortization converting a negative per-round bound into `M/8`. The v3 text has not supplied the missing summation.

### References in `forum_post_draft.md`

- **Line 9: Definition 4.5, Theorem 4.7, Proposition A.9. CORRECT.** Definition 4.5 is the restricted safe-edge hypothesis; Theorem 4.7 is the conditional T2 lower bound; Proposition A.9 is the conditional T2 lower-bound assembly.

- **Line 9: Proposition A.2 refutes unrestricted version via `K_4` over `{13,17,19,23}` and common `q`. CORRECT.** This matches Proposition A.2.

- **Line 15: rank-2 activation game is Proposition A.6. CORRECT BUT SLIGHTLY OVERSTATED.** Proposition A.6 is the activation-stage potential argument conditional on the restricted safe-edge hypothesis for activation graph states. It is not an unconditional rank-2 RSE theorem.

- **Line 30: two-round K4 sequence. CORRECT IN SUBSTANCE.** It matches the sequence in Proposition A.2 up to relabeling: capture one edge, delete an adjacent edge, capture the complementary edge, delete another edge, leaving two `Phi=8` live edges.

- **Line 72: `S_fin >= M/8` bound of Proposition A.3. CORRECT AS A REFERENCE, NOT AS EVIDENCE.** Proposition A.3 gives `M/8` only under restricted safe-edge monotonicity. The listed computations do not prove that hypothesis for v3.

- **Line 83: Proposition A.9 could be strengthened by specifying residual strategy. PARTLY CORRECT.** Proposition A.9 does not currently specify v3; it assumes RSE for the generated activation and residual states. A strengthened Proposition A.9 would need both a precise strategy and a proof that its generated states satisfy Proposition A.3's safe-edge condition.

- **Line 95: proof would make Theorem 4.7 unconditional. TOO STRONG AS WRITTEN.** A proof of nonempty safe-capture-or-score plus a per-round `Q change >=0` for the actual v3 move on the actual Buddhdev state space would be relevant. But the current forum statement does not match the code, the code does not check chosen-v3 safety, and a counterexample exists for `[5,4]` at the initial state.

## Section 2: Near-trap predicate well-definedness

The near-trap predicate is not well-defined relative to Buddhdev's public state without adding extra history.

- `k_phi(sigma)` is well-defined if `phi` is a legitimate set of edges, because `K` is part of Buddhdev's state.
- `dv_phi(sigma)` is well-defined once a fiber support is defined, because `D_V` is part of the state.
- `Tau_phi(sigma)` is well-defined from `C`, `D_V`, `D_E`, `K`, and the live-edge incidence relation, provided `Phi` is corrected to Buddhdev's `2^{|e cap C|}w(e)` and provided captured edges are also removed from live somehow.
- `c_phi(sigma)` is **not** well-defined in Buddhdev's stated tuple. The sketch writes `|{e in phi : e in C_sigma}|`, but `C_sigma` is a vertex set, not an edge set. The Python implementation silently adds `captured_edges`, which is not part of the manuscript state tuple.

There is also a more serious fiber-definition problem. The v3 sketch defines fibers over small-prime pairs `{a,a'}`. Buddhdev's Proposition A.2 obstruction is a large-prime `q` fiber containing all pair edges among four small primes. If one uses the v3 pair-fiber definition, the K4 obstruction is not even inside one fiber; if one uses the actual `q`-fiber definition, different edges share more than `q` and the sketch's slot-disjoint assumption fails.

The classification is computable from the Python state and does not use future information. But it is computable only because the implementation's state is richer than Buddhdev's stated state and because the implementation adopts a different fiber model.

A further internal inconsistency: the forum says the near-trap condition `max Phi >= 4` is "equivalently" no post-capture `Phi == 8`. That equivalence is false. A first capture in a `K_4` or `K_5` fiber creates adjacent live edges with `Phi=4` but no `Phi=8`.

## Section 3: Counterexample attempts

### Executive counterexample

I found a concrete counterexample to the operational v3 claim on a configuration explicitly in the Monte Carlo list.

Configuration `[5,4]`, initial state, unit weights:

1. The initial state has 16 live edges and `Q0=16` under the code's `Q=8S+sum Phi`.
2. `raw_rse(initial)` is true: there exists a safe ordinary capture, e.g. `('capture', 0)`.
3. v3 does **not** choose that capture. Because its near-trap predicate marks every first ordinary capture in the `K_5` fiber unsafe (`max_phi` becomes 4), it plays `SAFE_SCORE` on edge 0.
4. After Maker's score, `Q=23`.
5. Shortener deletes the shared `q` vertex of the `K_5` fiber. This kills the nine remaining live edges in that fiber. The resulting `Q=14`.
6. Full-round change is `14-16=-2`, contradicting the forum post's proposed per-round `Q change >= 0` for the chosen v3 move.

A stronger version uses a single `[7]` fiber. In the initial state, v3 again scores one edge, then Shortener deletes the shared `q`; `Q` goes from 21 to 28 to 8, a full-round change of `-13`, which is less than `-8*w_max` for unit weights. This directly breaks the `8*w_max` per-round bound proposed in the v3 sketch.

I saved the reproducer as `/home/user/workspace/erdos872/v3_counterexample_attempt.py`.

### Configurations tried

- `[4]`: v3 scores initially; Shortener deleting `q` gives positive full-round delta `+2`. No counterexample to monotonicity, but it already shows the claimed "safe capture nonempty when all fibers fresh" is false.
- `[5]`: v3 scores initially; Shortener deletes `q`; full-round delta `-2`. Counterexample to nonnegative chosen-v3 Q monotonicity.
- `[6]`: v3 scores initially; Shortener deletes `q`; full-round delta `-7`. Still within `-8`, but not nonnegative.
- `[7]`: v3 scores initially; Shortener deletes `q`; full-round delta `-13`. Counterexample to the proposed `-8*w_max` bound.
- `[8]`: same pattern; full-round delta `-20`.
- `[5,2]`: v3 captures the `[2]` fiber; Shortener deletes the `q` of the untouched `[5]` fiber; full-round delta `-3`. This is structurally the same cross-fiber issue.
- `[5,4]`: v3 scores initially; Shortener deletes the `q` of the `[5]` fiber; full-round delta `-2`. This is one of the supposedly Monte-Carlo-tested configurations.
- Tested enumerated initial configurations `[4,2]`, `[4,3]`, `[4,4]`, `[3,3,3]`, `[4,3,2]`, `[3,3]`, `[3,2,2]`, `[2,2,2,2]`; their first v3 move does not immediately decrease `Q`, but this is not enough to validate the strategy.

### Why the tests missed this

The exhaustive and Monte Carlo scripts do **not** check that the v3-chosen move is safe. They check `raw_rse(s)`, which asks whether there exists some Maker move preserving `Q` against all Shortener replies. At the `[5,4]` initial state, `raw_rse` is true because an ordinary capture is safe, while v3 chooses a score move that is unsafe. Thus the reported "0 RSE failures" is evidence about the reachable state set, not about the v3 policy.

## Section 4: Q-monotonicity sketch audit

### Gap 1: tightening from `16 w_max` to `8 w_max`

**Verdict: FUNDAMENTAL for the stated v3.**

The `[7]` initial-state counterexample gives a full-round change of `-13` with `w_max=1`. That directly violates the proposed `-8*w_max` lower bound. The failure mechanism is not a constant-factor bookkeeping issue: v3's overbroad near-trap predicate forces scoring, and scoring leaves a high-degree shared `q` vertex available for Shortener deletion. For a single `K_k` fiber, v3's first score has gain `+7`, while deleting `q` removes `C(k,2)-1` unit-potential live edges. The full-round delta is `8 - C(k,2)`, which is below `-8` for `k>=7` and tends to `-infinity` with `k`.

### Gap 2: cross-fiber interaction through shared `q`

**Verdict: FUNDAMENTAL / MISFORMALIZED.**

There are two separate problems.

First, the code's multi-fiber model uses disjoint large-prime fibers. That excludes cross-fiber sharing by construction. It therefore cannot validate the sketch's claim about shared `q` interactions.

Second, in the actual K4 obstruction, edges sharing a large prime `q` also share side slots such as `13q` when the small-prime pairs overlap. The statement "fibers share only `q`" is not true for the natural large-prime fiber. If instead fibers are defined by small-prime pairs, then the K4 obstruction is spread across multiple pair-fibers, so a fiber-local near-trap predicate does not describe the obstruction it is supposed to avoid.

The line "Shortener can delete `q`, but this kills all live edges in one shot, and the resulting `Delta_Q` is <= 8M" is not a per-round RSE argument. Deleting `q` can erase a large amount of live potential immediately; the `[5]`, `[5,4]`, and `[7]` initial-state examples show this directly.

### Gap 3: SAFE_CAPTURE non-emptiness

**Verdict: FUNDAMENTAL for the stated near-trap predicate; LOOSE-SKETCH only if the predicate is changed.**

The claim at the end of the sketch says that if every fiber has `c_phi=0`, any max-`Delta_Q` live edge is a SAFE_CAPTURE because near-trap requires `c_phi>=1`. That is wrong because the predicate is evaluated after the proposed capture. In a fresh `K_4` fiber, after any first capture, `c_phi=1` and adjacent live edges have `Phi=4`; therefore the code classifies the move as near-trap and unsafe. The same happens in `K_5`, `K_6`, etc.

This is not a subtle induction gap. It is a direct quantifier/time-index error: pre-capture `c=0` does not prevent post-capture `c=1`.

## Section 5: Lean skeleton audit

The Lean skeleton does not state a meaningful v3 theorem.

- `SlotState` contains only `fibers : List Nat`; it has no live edges, vertices, weights, `C`, `D_V`, `D_E`, `K`, score, potential, or legal move relation.
- `inNearTrap`, `isSafeCapture`, `isSafeScore`, `strategy_v3`, and `reachableV3` are all `sorry` placeholders.
- `strategy_v3_invariant` is literally `∀ s0 s, s ∈ reachableV3 s0 → True`. This is vacuous.
- `v3_implies_T2_unconditional` assumes the vacuous invariant and concludes the full conditional T2 lower bound using `sorry`. There is no formal bridge from v3 to Buddhdev's Definition 4.5, Proposition A.3, or Proposition A.9.
- The theorem's comment says the `M/8` final score bound is "verified computationally for all tested configs," but Proposition A.3 is not a finite-config statement; it is a conditional theorem requiring safe-edge monotonicity at every generated state.

Bottom line: the Lean file is a naming scaffold, not a formalization of the v3 strategy or its invariant.

## Section 6: Monte Carlo evidence audit

The Monte Carlo evidence buys much less credence than the forum draft says.

### What is actually sampled

`k4_avoidance_v3_sampled.py` samples one v3 trajectory at a time and chooses Shortener replies uniformly at random from `breaker_moves`. This is not adversarial Shortener. It does not bias toward worst-case vertex deletions, and it does not check whether v3's chosen move is safe.

At every visited state it calls `raw_rse(s, edges)`. That checks existence of some safe Maker move, not whether `strategy_v3(s, edges)` is that move. The `[5,4]` initial state proves the distinction matters: `raw_rse` passes, but v3's selected score move allows `Q` to fall.

### Coverage

For `[5,4]`, the draft reports 158,992 state visits over 20,000 trials. I ran a capped BFS under v3 and reached 1,000,008 distinct states with a frontier of 868,422 still open by depth 4. A smaller capped run already had this depth histogram:

```text
{0: 1, 1: 41, 2: 1120, 3: 22855, 4: 269256, 5: 6736}  (cap hit at 300,009 states)
```

Thus the Monte Carlo visits are at most about 16% of even the first 1,000,008 known distinct reachable states, and the true fraction is lower because trial visits include duplicates and because the BFS frontier was still enormous. The crude labelled state-space upper bound for `[5,4]` is about `7.6e14`, though that upper bound includes unreachable states.

### Depth distribution

The reported `[5,4]` average is `158,992 / 20,000 ≈ 7.95` checked states per trajectory. That is shallow relative to the branching already visible by depth 4.

### Honest assessment

The 486k visits are not evidence that v3 is adversarially safe. They are random-path evidence that the state set reached by v3 often has some safe move. Since the checker does not test v3's selected move, the evidence does not support the forum's central claim.

## Section 7: K_k-signature accounting

"v3 eliminates K_k-sig" is not rigorously equivalent to "v3 eliminates RSE failures."

- The baseline data itself disproves equivalence: `[3,3,3]` has 576 baseline RSE failures and 0 K-sig hits. `[4,3]` has 686 failures but only 320 K-sig hits. `[4,4]` has 30,808 failures but 12,320 K-sig hits.
- The signature code records `(len(C_f), len(D_E_f), len(D_V_f), len(captured_f), sorted live phis, f)` and ignores `K_f` even though scored edges affect the strategic geometry. This is a coarse local signature, not an isomorphism type or proof certificate.
- The signature database is generated from isolated single-fiber failures for the tested fiber sizes. It does not cover larger `K_k` fibers; the `[5]` and `[7]` initial-state failures above are not the original K4 signature.
- v3's reported `0` K-sig hits means only that no reached state matched those compressed isolated-fiber signatures. It does not show that every possible RSE failure mode is gone.

The forum post should not say or imply that K-sig elimination equals RSE elimination. At most it can say that one particular family of compressed local K4-like signatures disappeared in the tested state sets.

## Section 8: Executive summary and recommendation

**Recommendation: (A) v3 has a real flaw / counterexample. Do not post the current claim.**

The central flaw is that the computational checks validate the wrong predicate. They test `raw_rse(s)` (there exists a safe move from state `s`) rather than "the move selected by v3 is safe." On `[5,4]`, one of the configurations advertised in the Monte Carlo evidence, the initial state already passes `raw_rse` but v3 chooses a score move after which Shortener deletes the shared `q` vertex and makes `Q` drop.

There is an even stronger single-fiber `[7]` counterexample to the proposed `Q_after >= Q_before - 8*w_max` bound: v3 scores one edge, Shortener deletes `q`, and the full-round change is `-13` with unit weights.

The analytical sketch also has serious misformalizations: wrong fiber decomposition, wrong potential definition, a type error in `c_phi`, an incorrect citation to Lemma 4.4, an unsupported Section 8 attribution, and a false nonempty-SAFE_CAPTURE claim caused by evaluating a post-capture predicate using pre-capture intuition.

Closest honest forum claim, if revised drastically:

> I implemented a trap-aware heuristic and checked that, on several small disjoint-large-prime fiber configurations, every v3-reachable state still has some raw RSE move. However, the current strategy-selection rule is not proved safe and in fact fails on larger fibers unless the near-trap predicate and move-selection criterion are changed. I am looking for a correct local invariant or counterexamples.

The current draft's claim that v3 makes Theorem 4.7 plausibly unconditional is not defensible.
