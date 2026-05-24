# K_5 q-fiber forced-loss walkthrough

Step-by-step verification of `src/v4_k5_bad_path.py` against Buddhdev (Appendix A.1).
Each step quotes the manuscript rule applied, then explains the resulting state.

## Setup

The fiber is `K_5` over a single shared large-prime slot `q` and five side slots `{1q, 2q, 3q, 4q, 5q}`. The ten rank-3 edges are `e_{i,j} = {q, iq, jq}` for `1 <= i < j <= 5`. All weights are 1.

```
vertices: q, 1q, 2q, 3q, 4q, 5q     (6 slots)
edges:    e_{i,j} = {q, iq, jq}     (10 edges, all weight 1)
```

## Manuscript rules in play

Quoting Appendix A.1 verbatim:

**State tuple**: `(C, D_V, D_E, K, S)` where `C` is the captured-vertex set, `D_V` deleted vertices, `D_E` unscored deleted edges, `K` scored edges, `S` total scored weight.

**Live edge**: `e` is live iff `e not in D_E cup K` and `e` contains no deleted vertex.

**Potential**: `Q = 8 S + sum over live e of Phi(e)`, where `Phi(e) = 2^|e cap C| w(e)`.

**Maker moves**:
- Ordinary capture: pick a live edge `f`, add its vertices to `C`, add its weight `w(f)` to `S`. (See note A below about whether `f` is also removed from live.)
- Alternate-scoring: pick a live edge `f`, add `f` to `K`, add `w(f)` to `S`. (Vertices are NOT added to `C`.)

**Breaker moves**:
- Vertex deletion: pick `v in V \ C` (an uncaptured vertex), add `v` to `D_V`.
- Edge deletion: pick a live edge `e`, add `e` to `D_E`.
- Scored-edge reply (scored-hypergraph variant only): add a live edge to `K`, increment `S` by its weight.

**Note A (captured-edges ambiguity)**: the manuscript does not explicitly say ordinary capture removes `f` from the live set. But the proof of Proposition A.3 requires `Q_fin = 8 S_fin` at termination (no live edges remain), so the captured edge must leave live somehow. We treat ordinary capture as equivalent to also placing `f` into the "removed from live" bookkeeping (a captured-edges set, or equivalently into `K`). Every step below works under this reading.

## Step 0: initial state

```
C = {}, D_V = {}, D_E = {}, K = {}, S = 0
captured-edges = {}
```

All 10 edges are live. For each, `|e cap C| = 0`, so `Phi(e) = 2^0 * 1 = 1`. Thus

```
Q_0 = 8*0 + 10*1 = 10.
```

**Verification**: `Q_0 = 10` matches the reproducer output. Correct.

## Step 1a: Maker captures e_{1, 2}

Rule applied: ordinary capture. Add `{q, 1q, 2q}` to `C`. Add `w(e_{1,2}) = 1` to `S`. Remove `e_{1,2}` from live (per Note A).

```
C = {q, 1q, 2q}
S = 1
captured-edges = {e_{1,2}}
```

For each remaining live edge, compute `|e cap C|`:
- `e_{1,3} = {q, 1q, 3q}`: cap with `C` = `{q, 1q}`, size 2, `Phi = 4`
- `e_{1,4} = {q, 1q, 4q}`: `{q, 1q}`, size 2, `Phi = 4`
- `e_{1,5}`: `{q, 1q}`, size 2, `Phi = 4`
- `e_{2,3}`: `{q, 2q}`, size 2, `Phi = 4`
- `e_{2,4}`: `{q, 2q}`, size 2, `Phi = 4`
- `e_{2,5}`: `{q, 2q}`, size 2, `Phi = 4`
- `e_{3,4} = {q, 3q, 4q}`: cap = `{q}`, size 1, `Phi = 2`
- `e_{3,5}`: `{q}`, size 1, `Phi = 2`
- `e_{4,5}`: `{q}`, size 1, `Phi = 2`

Sum of Phi over 9 live edges: `6*4 + 3*2 = 30`.

```
Q (post-Maker, pre-Shortener) = 8*1 + 30 = 38.
```

**Verification**: matches reproducer output.

## Step 1b: Shortener deletes vertex 3q

Rule applied: vertex deletion. `3q` is not in `C` (only `q, 1q, 2q` are), so it is a legal target. Add `3q` to `D_V`.

```
D_V = {3q}
```

This kills every edge containing `3q`: `e_{1,3}, e_{2,3}, e_{3,4}, e_{3,5}` (4 edges). Remove them from live.

Remaining live edges (5):
- `e_{1,4}`: still Phi = 4
- `e_{1,5}`: still Phi = 4
- `e_{2,4}`: still Phi = 4
- `e_{2,5}`: still Phi = 4
- `e_{4,5}`: Phi = 2

Sum = `4*4 + 1*2 = 18`.

```
Q (post-round 1) = 8*1 + 18 = 26.
```

**Verification**: matches reproducer. Round-1 full delta = `26 - 10 = +16`. Maker is ahead, no problem yet.

## Step 2a: Maker captures e_{4, 5}

Rule applied: ordinary capture of live edge `{q, 4q, 5q}`. `q` already in `C`; add `4q, 5q`. `S` becomes 2. Remove `e_{4, 5}` from live.

```
C = {q, 1q, 2q, 4q, 5q}
S = 2
captured-edges = {e_{1,2}, e_{4,5}}
```

Recompute Phi on remaining live edges:
- `e_{1,4} = {q, 1q, 4q}`: all three in `C`, `Phi = 8`
- `e_{1,5} = {q, 1q, 5q}`: all three in `C`, `Phi = 8`
- `e_{2,4}`: all three in `C`, `Phi = 8`
- `e_{2,5}`: all three in `C`, `Phi = 8`

Sum = `4 * 8 = 32`.

```
Q (post-Maker) = 8*2 + 32 = 48.
```

**Verification**: matches reproducer.

## Step 2b: Shortener edge-deletes e_{1, 4}

Rule applied: edge deletion. `e_{1, 4}` is live, so legal. Add to `D_E`.

```
D_E = {e_{1,4}}
```

Remaining live: `{e_{1,5}, e_{2,4}, e_{2,5}}`, each with `Phi = 8`. Sum = 24.

```
Q (post-round 2) = 8*2 + 24 = 40.
```

**Verification**: matches reproducer. Round-2 full delta = `40 - 26 = +14`. Still nondecreasing.

## Step 3: the trap state

```
state: C = {q, 1q, 2q, 4q, 5q}, D_V = {3q}, D_E = {e_{1,4}}, K = {},
       captured-edges = {e_{1,2}, e_{4,5}}, S = 2,
       live = {e_{1,5}, e_{2,4}, e_{2,5}}, all Phi = 8,
       Q = 40.
```

Now I enumerate every legal Maker move and the worst Shortener reply.

**Maker option A**: ordinary-capture e_{1,5}.
- Vertices added to C: none new (all already in C).
- S becomes 3, e_{1,5} removed from live.
- Post-Maker: live = `{e_{2,4}, e_{2,5}}`, both `Phi = 8`.
- Q post-Maker = `8*3 + 2*8 = 40`.
- Shortener can edge-delete e_{2,4}: remaining live `{e_{2,5}}` with `Phi = 8`. Q = `24 + 8 = 32`.
- Full-round delta = `32 - 40 = -8`.

**Maker option B**: ordinary-capture e_{2,4}. Symmetric to A. Round delta = -8.

**Maker option C**: ordinary-capture e_{2,5}. Symmetric. Round delta = -8.

**Maker option D**: alternate-score e_{1,5}.
- e_{1,5} moves to K. S becomes 3. C unchanged.
- Post-Maker: live = `{e_{2,4}, e_{2,5}}`, still Phi = 8 each (C unchanged).
- Q post-Maker = `8*3 + 16 = 40`.
- Shortener edge-deletes e_{2,4}. Live = `{e_{2,5}}`, Phi = 8. Q = `24 + 8 = 32`.
- Round delta = -8.

**Maker option E**: alternate-score e_{2,4}. Symmetric to D. Round delta = -8.

**Maker option F**: alternate-score e_{2,5}. Symmetric. Round delta = -8.

**No other Maker moves are legal**: the only live edges are these three, and Maker's only options at any state are ordinary capture or alternate-score on a live edge.

**Every Maker move results in worst-case round delta = -8.**

## Why this is a structural proof

The safety-game synthesizer searches over the *entire* reachable state graph by backward induction. A state is declared "safe" if Maker has a move with worst-case round delta `>= 0` leading only to safe states. The synthesizer found 3774 of 4068 pre-Maker states in `[5]` are unsafe under this definition, including the initial state. The forced sequence above is one concrete witness path.

Note this is a per-round-Q-monotone failure, not necessarily a final-score failure. The synthesizer also reports `S_fin = 4` for `[5]` (the integer score actually achievable from the initial state by some Maker), which equals `M/2 = 4*1 = 5*... ` wait, `M = sum w(e) = 10`, so `M/8 = 1.25`, and `S_fin = 4 >= 1.25` easily. The negative result is specifically: there is no strategy that satisfies Definition 4.5's per-round Q-nondecrease, even though the M/8 bound is achievable by SOME (non-Q-monotone) strategy.

## What this implies for Definition 4.5

Definition 4.5 requires that "Maker has a legal live edge f such that, after Maker plays f, every legal Breaker reply leaves the scaled potential Q at least as large as it was before Maker's move", restricted to T2-strategy-generated states. The K_5 q-fiber initial state and the trap state above both fail this condition. The hypothesis can hold only if T2 strategy generation never produces these states.

Open questions a moderator might raise:

1. **Is `K_5` over a single q reachable in T2 generation?** Activation Phase 1 of Section 4.2 activates pairs `(a, c)` of small primes. A residual `K_k` q-fiber would require k small primes `p_1, ..., p_k` each pairing with the same q. Whether the activation strategy actually produces such fibers (or whether it spreads pairs across distinct q's) depends on the choice of `B_{a,c}` and the activation order. If it can produce `K_5` or larger, Definition 4.5 fails on T2-generated states.

2. **Could a more permissive potential salvage things?** Buddhdev specifically uses the `8 S + sum Phi` potential because the constant 8 corresponds to a final-score floor of `M/8`. A different potential (e.g. weighted by fiber size) could be Q-monotone where this one is not, but would yield a different (probably worse) final-score bound.

3. **Is the safety-game model the right one?** The synthesizer treats Shortener as fully adversarial. The actual T2 game has additional constraints from the activation phase that may rule out the specific Shortener move (delete 3q) used in Step 1b. Verifying this requires reading Buddhdev's Section 4.2 carefully.

## What to verify yourself before posting

Walk through the script once, line by line, with the manuscript open to Appendix A.1. The specific things to confirm:

- The state tuple matches `(C, D_V, D_E, K, S)`.
- The potential formula `Q = 8 S + sum live Phi(e)` matches.
- `Phi(e) = 2^|e cap C| * w(e)` matches.
- Vertex deletion targets `v in V \ C`.
- Edge deletion targets any live edge.
- Alternate-scoring adds the edge to `K`, increments `S`, does NOT add vertices to `C`.

If all six match, the trace above is a faithful execution of Buddhdev's rules. If any do not match, the result needs to be re-verified.
