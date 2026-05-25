# v4 findings: repair attempt and structural obstruction

Artifacts:

- Ground-truth manuscript setup: `/home/user/workspace/erdos872/buddhdev_setup_audit.md`
- v4 verifier/strategy code: `/home/user/workspace/erdos872/k4_avoidance_v4.py`
- Combined computational results: `/home/user/workspace/erdos872/v4_combined_results.json`
- Concrete K5 obstruction path: `/home/user/workspace/erdos872/v4_k5_bad_path.txt`

## 1. Corrected Buddhdev setup

See `/home/user/workspace/erdos872/buddhdev_setup_audit.md`. The essential corrections are:

- The residual edge is \(e_{a,c,b}=\{b,ab,cb\}\), not an abstract edge with a non-slot small-prime vertex.
- The manuscript state tuple is \((C,D_V,D_E,K,S)\).
- The potential is
  \[
  Q=8S+\sum_{e\ live}\Phi(e),\qquad \Phi(e)=2^{|e\cap C|}w(e).
  \]
- An edge is live iff it is not in \(D_E\cup K\) and contains no deleted vertex.
- Proposition A.3 requires full-round nondecrease of \(Q\) from the pre-Maker state for the chosen Maker move, against every legal Breaker reply. It is not enough that `raw_rse` exists at the state, and it is not enough to bound losses by \(8w_{max}\) without a separate summation proof.

## 2. Structural diagnosis of the q-deletion attack

### (a) Does Definition 4.5 require monotonicity against deletion of q?

Yes, unless \(q\) has already been captured before Shortener's reply. Definition 4.5 quantifies over every legal Breaker reply after Maker plays the selected live edge. In the residual slot model, \(q\) is the slot \(b\) in \(e_{a,c,b}=\{b,ab,cb\}\). Proposition A.5 says playing \(b\) deletes exactly the residual targets whose hyperedges contain that slot. Thus if Maker scores an edge, or plays in a different fiber, and \(q\notin C\), Shortener's deletion of \(q\) is a legal vertex deletion that must be included in the worst-case reply set.

There is no prior activation commitment that puts \(q\) into \(C\). Activation of the pair \((a,c)\) makes \(a,c,ac\) unavailable in the original divisibility game; it does not capture residual slot vertices \(q,aq,cq\).

### (b) Does Lemma 4.3 already imply a Maker counter-move?

No, not in the residual rank-three game. Lemma 4.3 is a bipartite fan lemma where Maker directly captures a right vertex of maximum live degree. In the residual rank-three slot hypergraph, Maker's ordinary move is edge capture, not vertex-only capture. However, in a single \(q\)-fiber every residual edge contains \(q\), so ordinary capture of any live edge in that fiber captures \(q\) before Shortener's reply. Therefore Maker can protect that particular \(q\) by ordinary edge capture, but Lemma 4.3 is not the reason; it is just the slot-game move rule.

### (c) Is q-deletion structural?

The precise statement is conditional:

> If \(q\notin C\) and Maker's chosen move does not capture an edge containing \(q\), then Shortener can delete \(q\) and remove every live edge in that \(q\)-fiber in one legal reply. No strategy local to other fibers can prevent that reply.

This refutes v3's first-score defense. In a fresh unit-weight \(K_k\) fiber, scoring one edge raises \(Q\) by 7 but leaves \(q\) uncaptured; deleting \(q\) removes \(\binom{k}{2}-1\) remaining unit-potential live edges, giving full-round delta \(8-\binom{k}{2}\). This is negative for \(k\ge5\), and unboundedly bad as \(k\) grows.

But q-deletion is not an absolute obstruction to every local response: ordinary capture of any live edge in the same \(q\)-fiber captures \(q\), making deletion of \(q\) illegal in the immediately following Shortener reply. The deeper obstruction found by v4 is different: after q is captured, Shortener can still force high-\(\Phi\) edge-deletion traps in isolated \(K_5\) fibers.

### (d) Is the shared vertex in `multi_fiber_rse.py` Buddhdev's q?

Yes for a large-prime fiber. In `multi_fiber_rse.py`, an edge has form `((fi,0),(fi,p_i),(fi,p_j))`; `(fi,0)` is the large-prime slot \(q=b\), and `(fi,p)` is the side slot \(pq\). This matches Buddhdev's Proposition A.2 geometry for a single fiber over common \(q\). It is not the small prime \(a\), and it is not an activation-stage vertex. The simplification in `multi_fiber_rse.py` is that different fibers have disjoint large-prime slots; the actual Proposition A.2 obstruction is already present in one such fiber.

## 3. v4 strategy specification and what failed

Two v4 variants were implemented in `/home/user/workspace/erdos872/k4_avoidance_v4.py`.

### v4-greedy one-step max-min

At a pre-Maker state \(\sigma\), compute for every legal Maker move \(m\)

\[
\Delta_{worst}(m)=\min_{b\ legal\ reply}\bigl(Q(\sigma+m+b)-Q(\sigma)\bigr).
\]

Choose the move maximizing \(\Delta_{worst}\). This checks the chosen move, not `raw_rse`.

This fixes the immediate q-deletion examples: at the initial states [5], [7], and [5,4], it chooses ordinary capture of a \(q\)-fiber edge, not scoring, and the worst-case full-round deltas are respectively 16, 31, and 16. See `/home/user/workspace/erdos872/v4_initial_onestep.jsonl`.

However, v4-greedy walks into Buddhdev's K4 two-\(\Phi=8\) trap. On the exact `{13,17,19,23}` q-fiber, it has 32 reachable pre-Maker states with no nonnegative chosen move; the first is exactly the Proposition A.2 state with two live \(\Phi=8\) edges.

### v4-synthesized finite safety strategy

I then implemented a stronger finite safety strategy. A state is winning if it is terminal, or if Maker has a legal move with immediate \(\Delta_{worst}\ge0\) and every Shortener reply reaches a winning state. This is a backward safety-game synthesis over the finite slot state graph.

This strategy avoids the K4 trap and works on several small configurations, but it fails on the isolated K5 q-fiber. Therefore there is no repaired v4 of this local per-round-Q-monotone kind for arbitrary K_k fibers.

## 4. v4 verification table

All rows below check the chosen v4 move's worst-case full-round delta, not raw RSE existence.

| Configuration | v4 variant | Exhausted? | States seen | Checked pre-Maker states | Min chosen delta | States with no nonnegative move | Min terminal S | M/8 | S_fin >= M/8? | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Buddhdev K4 q-fiber `{13,17,19,23}` | synthesized | yes | 195 | 97 | 0 | 0 | 1 | 0.75 | yes | Safety synthesis avoids Prop A.2 trap by scoring/deferring. |
| [4,2] | synthesized | yes | 1,240 | 790 | 0 | 0 | 2 | 0.875 | yes | Full exhaustive pass. |
| [4,3] | synthesized | yes | 7,473 | 4,514 | 0 | 0 | 2 | 1.125 | yes | Full exhaustive pass. |
| [3,3,3] | synthesized | yes | 5,872 | 3,269 | 0 | 0 | 3 | 1.125 | yes | Full exhaustive pass. |
| [5] | synthesized | yes | 6,416 | 4,068 | -8 | 3,774 | 4 | 1.25 | yes | Counterexample to per-round monotonicity; see below. |
| [7] | one-step initial only | n/a | n/a | initial | 31 | n/a | n/a | 2.625 | n/a | Initial q-deletion fixed; full synthesis did not finish before timeout. |
| [5,4] | one-step initial only | n/a | n/a | initial | 16 | n/a | n/a | 2.0 | n/a | Initial q-deletion fixed; full synthesis did not finish before timeout. |
| [4,4] | one-step initial only | n/a | n/a | initial | 10 | n/a | n/a | 1.5 | n/a | Full synthesis timed out. |
| [4,3,2] | one-step initial only | n/a | n/a | initial | 10 | n/a | n/a | 1.25 | n/a | Full synthesis timed out. |

The synthesized [5] counterexample is not merely a greedy-choice error. The safety-game solver searched for any strategy preserving \(\Delta_{worst}\ge0\) forever and found the initial K5 state losing. A concrete reachable losing state is:

```text
C=[q,1q,2q,4q,5q], D_V=[3q], D_E=[e_{1,4}], S=2,
live edges e_{1,5}, e_{2,4}, e_{2,5}, all with Phi=8, Q=40.
```

At that state, Maker can capture or score only one live \(\Phi=8\) edge. Either move changes \(Q\) by \(8-8=0\), and Shortener deletes another remaining \(\Phi=8\) edge, making the full-round delta \(-8\). See `/home/user/workspace/erdos872/v4_k5_bad_path.txt` for the path:

1. Maker captures \(e_{1,2}\); Shortener deletes side vertex \(3q\).  \(Q:10\to38\to26\), delta +16.
2. Maker captures \(e_{4,5}\); Shortener deletes \(e_{1,4}\). \(Q:26\to48\to40\), delta +14.
3. The next state has three live \(\Phi=8\) edges and no nonnegative Maker move.

## 5. What does and does not survive

Survives:

- The critique's immediate q-deletion attack on v3 is real.
- The repair “capture q first by ordinary edge capture” defeats the immediate q-deletion reply in [5], [7], and [5,4].
- The exact Buddhdev K4 Proposition A.2 fiber is avoidable by a non-greedy finite safety strategy in isolation.
- The synthesized safety strategy gives exhaustive positive results on [4,2], [4,3], and [3,3,3].

Does not survive:

- A universal local per-round-Q-monotone residual strategy for arbitrary isolated \(K_k\) q-fibers. The isolated K5 q-fiber is already a counterexample.
- The idea that q-deletion is the only issue. After q is captured, Shortener can force a high-\(\Phi\) edge-deletion obstruction.
- Any claim that Theorem 4.7 becomes unconditional from these computations. Proposition A.9 remains conditional on a restricted safe-edge hypothesis for the actual T2-generated residual states.

## 6. Suggested forum post claim

Do not post a proof claim. A defensible negative/diagnostic claim is:

> I repaired the immediate q-deletion bug in v3 by checking the chosen move's worst-case full-round \(Q\) delta. The repair captures an edge containing the large-prime slot \(q\) rather than scoring first, so the initial [5], [7], and [5,4] q-deletion counterexamples disappear. However, an exhaustive finite safety-game check shows that no local strategy maintaining per-round \(Q\)-monotonicity exists even for the isolated unit-weight K5 q-fiber: Shortener can force a state with three live \(\Phi=8\) edges, after which every Maker move allows a \(-8\) edge-deletion reply. Thus a local residual repair is insufficient; any path to Buddhdev's conditional T2 theorem must use a genuine T2-generated-state invariant or global inter-fiber/activation compensation, not arbitrary q-fiber local monotonicity.

## 7. T2 reachability

Outcome: **reduced to manuscript clarification, not proved reachable or unreachable**.

The T2 reachability question for the isolated unit K5 q-fiber cannot be decided from the manuscript as written. Proposition A.6 says that during activation Prolonger chooses "a safe edge supplied by" the restricted safe-edge hypothesis, but it does not specify a canonical selector among safe edges or prove a q-fiber invariant such as K5-freeness. Proposition A.2 explicitly distinguishes reachability under some legal play from reachability under the specific Proposition A.9 strategies, so this missing selector matters.

I verified a concrete arithmetic incidence witness: for `n = 10^20`, `delta = 1/8`, small primes `{101,103,107,109,113}`, and `q = 4806305873305829`, all ten targets `p_i p_j q` remain live after a legal partial sequence of securing plays if the activation selector secures the ten clique pairs and Shortener avoids q. Independent scripts verify the interval conditions, legality, survival, and K5 slot incidence. This is not a full reachability proof, because the missing steps are to certify that those ten pair choices are safe edges in the full activation graph states and that the later completion of activation does not attach extra residual q-edges. See `/home/user/workspace/erdos872/t2_reachability_proof.md` and `/home/user/workspace/erdos872/t2_reachability_code/`.
