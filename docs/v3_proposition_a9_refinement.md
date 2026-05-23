# Refined Proposition A.9 + Q-monotonicity argument for strategy v3

## Notation (matches Buddhdev manuscript, April 2026)

  - `S = (V, E)` is the rank-3 residual slot hypergraph after the activation phase.
  - `V = {q} cup B` where `q` is the common right-vertex and `B = {b_1, ..., b_n}` are the surviving "shifted" left-vertices.
  - Each rank-3 hyperedge `e` has the form `{a_e b_e, a'_e b'_e, q}` with `a_e, a'_e` distinct small odd primes and `b_e, b'_e in B`. The "small-prime support" of `e` is `pi(e) = {a_e, a'_e}`.
  - A *fiber* over a pair `{a, a'}` of small primes is the set of hyperedges with `pi(e) = {a, a'}`. Different fibers are *slot-disjoint* in the sense that they share at most the vertex `q`.
  - `sigma` denotes a pre-Maker (=pre-Prolonger) state. The state tuple is `(C_sigma, D_V, D_E, K, S_sigma)` where `C_sigma` is the captured slot set, `D_V` the deleted vertices, `D_E` the deleted edges, `K` the scored edges, `S_sigma` the running score.
  - For a live edge `f`, its *potential* `Phi_sigma(f) in {0, 2, 4, 8}` is `2^|{v in f : v in C_sigma}|` if `f` has no captured vertex incident to a deleted vertex, else `0`. Live edges with `Phi >= 4` are *threatening*.
  - `Q_sigma = sum over live f of Phi_sigma(f) * w_sigma(f)` is the potential function. `M = sum of initial weights w_0(f)`. Buddhdev Prop A.3 asks for `S_final >= M/8`.

## Near-trap predicate (the key local condition)

For a fiber `phi` (i.e. for an unordered pair `{a, a'}` of small primes) and a state `sigma`, define

  - `c_phi(sigma) = |{e in phi : e in C_sigma}|` (ordinary captures inside the fiber)
  - `k_phi(sigma) = |{e in phi : e in K}|` (scored edges inside the fiber)
  - `dv_phi(sigma) = |{v in supp(phi) : v in D_V}|` (deleted vertices in the fiber support)
  - `Tau_phi(sigma) = max over live e in phi of Phi_sigma(e)` (max threatening potential in the fiber)

**Definition (Near-trap).** A fiber `phi` is in the *near-trap state* at `sigma` if
  (a) `dv_phi(sigma) = 0`, AND
  (b) `k_phi(sigma) = 0`, AND
  (c) `c_phi(sigma) >= 1`, AND
  (d) `Tau_phi(sigma) >= 4`.

The K_4 refutation of Buddhdev Proposition A.2 reaches the near-trap state with `c_phi = 2`, `Tau_phi = 8` (two emergent `Phi == 8` live edges); after one more Shortener edge-deletion the unrestricted Maker strategy has no positive-gain move that preserves RSE.

## v3 strategy specification

**Definition (SAFE).** Let `f` be a live edge in fiber `phi` at state `sigma`. Let `sigma + f` denote the state after Maker plays ordinary-capture on `f`.

  - `f` is a **SAFE_CAPTURE** at `sigma` if no fiber is in the near-trap state at `sigma + f`.
  - `f` is a **SAFE_SCORE** at `sigma` if Maker plays the alternate-scoring move on `f`. This is always safe by inspection: scoring removes `f` from `L_sigma` and adds it to `K`, increments `S_sigma` by `w_sigma(f)`, and does NOT change `Phi_sigma(e)` for any other live edge `e`.
  - `f` is **UNSAFE** at `sigma` otherwise.

**Strategy v3.** At each pre-Maker state `sigma` with at least one positive-weight live edge:

  1. If the SAFE_CAPTURE set is non-empty, Maker plays the SAFE_CAPTURE `f^*` with maximum `Delta_Q := Phi_sigma(f^*) * w_sigma(f^*)`.
  2. Else (i.e. every live edge is UNSAFE for capture), Maker plays the SAFE_SCORE with maximum `w_sigma(f^*)`.

This is the strategy verified computationally to achieve 100 percent RSE on the 8 multi-fiber configurations enumerated exhaustively and on 60000 Monte Carlo trials at four larger configurations.

## Proposed refined Proposition A.9

**Proposition A.9' (refined).** Let `S = (V, E)` be the rank-3 residual slot hypergraph after the activation phase, with fiber decomposition `E = bigsqcup_phi E_phi` (slot-disjoint fibers). Let Maker play strategy `v3` against any Shortener strategy. Then for any Shortener strategy `T`, at every reachable pre-Maker state `sigma`:

  (i) the SAFE_CAPTURE-union-SAFE_SCORE set is non-empty whenever there is a positive-weight live edge,
  (ii) the per-round `Q` change satisfies `Q_{sigma_after_round} >= Q_sigma - 8 * w_max(sigma)` where `w_max(sigma) := max over live f of w_sigma(f)`,
  (iii) the final running score `S_final` satisfies `S_final >= M/8 + Q_final/8`.

Items (ii) and (iii) together imply Buddhdev's Proposition A.3 (because `Q_final >= 0` trivially, so `S_final >= M/8`), and item (i) plus (ii) plus (iii) plus the activation-phase rank-2 RSE (which I have also verified computationally; see `activation_rank2_rse.py`) gives Theorem 4.7 unconditionally.

## Why (i) holds (informal argument)

SAFE_SCORE is always available as long as there is at least one positive-weight live edge, since alternate-scoring is a legal Maker move and is always safe by the definition above. So (i) is essentially trivial. The substantive content is that the SAFE_CAPTURE set is also non-empty whenever capturing is even slightly preferable; this is the content of (ii).

## Why (ii) should hold (Q-monotonicity sketch)

Let `sigma` be a pre-Maker state. Maker plays move `m`, Shortener replies with move `t` to reach `sigma'`.

  - **Case A: Maker plays SAFE_CAPTURE on `f`.** `Delta_Q_Maker = -Phi_sigma(f) * w_sigma(f)`. Shortener's reply `t` can be either:
      (A1) edge-delete some live edge `e_d`, with `Delta_Q_t = -Phi_sigma(e_d) * w_sigma(e_d)`. Shortener picks `e_d` to maximize this, so the worst-case Q-loss in one round is `Phi_sigma(f) * w_sigma(f) + max over e_d of Phi_sigma(e_d) * w_sigma(e_d) <= 2 * 8 * w_max = 16 w_max`. But we can do better: Maker chose `f^*` with maximum `Delta_Q`, so `Phi_sigma(f^*) * w_sigma(f^*) >= Phi_sigma(e_d) * w_sigma(e_d)` for every `e_d`. This means after Maker's move, the maximum remaining Shortener edge-delete loss is at most `Phi_sigma(f^*) * w_sigma(f^*)`. Total Q-change `>= -2 * Phi_sigma(f^*) * w_sigma(f^*) >= -16 * w_max(sigma)`.
      (A2) vertex-delete some `v`, with `Delta_Q_t = -sum over live e incident to v of Phi_sigma(e) * w_sigma(e)`. By Buddhdev Lemma 4.4 (max-degree right capture) the vertex-deletion choice is bounded by the same `2 * Phi_sigma(f^*) * w_sigma(f^*)` term, since `f^*` was the max-gain capture. This is where the slot-game potential weighting `w_sigma(f) = w_0(f) / |slots remaining of f|` does its work.
  - **Case B: Maker plays SAFE_SCORE on `f`.** `Delta_Q_Maker = -Phi_sigma(f) * w_sigma(f)`, AND `Delta_S_Maker = +w_sigma(f)`. Shortener's reply contributes `<= 8 * w_max`. So `Delta_Q >= -8 * w_max - Phi_sigma(f) * w_sigma(f) >= -16 * w_max`.

Combining: in every round `Q_{sigma'} >= Q_sigma - 16 * w_max(sigma)`. Since `w_max(sigma)` is decreasing across the game (weights only shrink as slots are consumed), summing over all `T` rounds yields `Q_T >= Q_0 - 16 * sum w_max(sigma_t)`.

The actual constant `8` in the proposition (rather than `16`) comes from the standard slot-game amortization: alternate-scoring captures `w_sigma(f)` of the score budget for free, and the maximum potential `Phi = 8` only occurs at edges with all three slots captured, which can happen at most once per fiber under `v3` (this is exactly the near-trap-avoidance content). Tightening this constant from 16 to 8 requires a fiber-aggregate argument: across all fibers, the total `Phi = 8` events is bounded by the number of SAFE_CAPTURE moves Maker plays, each contributing `+w` to the score.

## Where this argument is currently incomplete

  1. The slot-game amortization tightening from `16` to `8` needs a precise accounting of "Phi = 8 events" per fiber. v3 prevents `>= 2` such events per fiber (since the second one would require entering the near-trap), so the total over all fibers is `<= F = O(loglog n / log log log n)` -- but this is not yet a tight Q-charging argument.
  2. The cross-fiber interaction is bounded because fibers share only the vertex `q`. Shortener can delete `q`, but this kills all live edges in one shot, and the resulting `Delta_Q` is exactly the loss of the entire game's remaining live-edge potential -- which is `<= 8 * M`, matching the M/8 bound exactly.
  3. The "no UNSAFE-only state" claim (item (i) for SAFE_CAPTURE specifically) needs proof. Computationally I see SAFE_CAPTURE always available in the configurations tested; a structural argument would proceed by induction on the number of fibers that have already had one capture.

## Concrete next mathematical step

Reduce the strategy invariant to the following finite combinatorial claim:

**Claim.** For any fiber configuration `(k_1, ..., k_F)` and any reachable state `sigma` under v3:

> Either (a) every fiber `phi` has `c_phi(sigma) = 0`, in which case any max-`Delta_Q` live edge is a SAFE_CAPTURE (because near-trap requires `c_phi >= 1`); or (b) some fiber has `c_phi >= 1`, in which case the previous-round Maker move was an ordinary capture into a fiber that was previously fresh, and the near-trap-avoidance check on that move forces all current live edges in that fiber to have `Phi <= 4`. Live edges in fresh fibers continue to have any `Phi`; one of them is therefore SAFE_CAPTURE.

If this claim is provable in finite combinatorial terms (induction on the number of fibers touched), then item (i) of refined Proposition A.9 is established. Item (ii) then follows from the standard slot-game amortization.

I would welcome any of: a proof of the Claim, a counterexample at larger fiber configurations, or a sharper formulation of the Q-charging step that yields the constant `8` cleanly.
