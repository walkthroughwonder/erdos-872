"""
Residual rank-3 RSE check, faithful to Buddhdev Proposition A.5 + A.9.

After activation, each secured pair (a, c) carries a set B_{a,c}(t) of
surviving large primes. The residual game is the rank-3 hypergraph game on
targets t = acb with b in some surviving fiber. The slot vertices are
b, ab, cb across all (a, c, b) triples.

KEY REFINEMENT vs. my Phase 4 single-fiber model:

  The residual game starts with C = (set of small primes a, c committed
  during activation) ALREADY POPULATED. More precisely: when activation
  claimed pair (a, c) by playing acb_0 for some witness b_0, the slot
  vertices b_0, ab_0, cb_0 are NOT added to C in the residual board (they
  are EXCLUDED from residual targets). What IS in C in the residual game?

  Looking back at A.5 and A.9: the residual game inherits the captures from
  activation only insofar as the activation captured small primes a, c. In
  the rank-3 residual game, the slot vertices are b, ab, cb where a, c are
  small. The small primes a, c are NOT slot vertices in the residual game.
  So the residual game starts with C_residual = empty.

  HOWEVER: not every (a, c, b) is in T_*. Only those with a securing target
  already played. That means for a in P_Y, c in P_Y, both small primes
  a, c are already "secured" by activation (so a and c are no longer
  available as divisibility moves, but they don't enter C_residual).

So the residual hypergraph is just the rank-3 hypergraph
  G_T* = { e_{a,c,b} = {b, ab, cb} : (a, c, b) in T_* }
with no pre-existing captures. The K_4-fiber refutation requires reaching
a state where six K_4 edges over a common right vertex q are live and
nothing is captured. This is reachable in the unconstrained game.

But: the residual game is played AFTER activation. The constraint here is
not on initial captures but on the STRUCTURE OF T_*. Specifically, T_*
contains acb for all pairs (a, c) that were secured during activation and
all surviving b in B_{a,c}. After activation, the surviving fibers are
typically NOT a complete K_4 over a single right vertex; they are sparse
because activation has consumed many tokens.

ALTERNATIVE FORMULATION: rather than enumerate the full slot hypergraph
game, we observe that the K_4-fiber refutation depends on having 4 small
primes a < c < e < f all in P_Y and a common large prime q with q in
B_{a,c} cap B_{a,e} cap B_{a,f} cap B_{c,e} cap B_{c,f} cap B_{e,f}.

The interval B_{a,c} = (n/(2ac), n/ac] cap Primes. For the four small
primes 13, 17, 19, 23, all pairs have ac in [221, 437], so a common q in
(n/442, n/437] works (Buddhdev's example).

In the residual game on T_*, for q to remain on all 6 edges, q must
survive activation. Activation never plays target acq for a, c in P_Y_4 =
{13, 17, 19, 23}, so q only survives if NO target involving (a,c) and any
b near q got played that killed q.

This is hard to model abstractly without simulating activation. Instead,
let's check: among reachable RESIDUAL states (starting from C_residual =
empty, with rank-3 hypergraph = some K_4 fiber over q plus possibly other
fibers), does RSE hold under the SPECIFIC RESIDUAL STRATEGY of A.9 (max-
gain in scaled-rank-3 potential)?

This is morally the same question as Phase 4. The honest answer from Phase 4
is: NO, raw RSE fails on isolated K_4 fibers.

But Proposition A.9 ('Residual phase scaled capture') states that Prolonger
plays an UNCONDITIONAL max-gain capture rule and Buddhdev BOUNDS the loss
incurred by safe-edge violations as a lower-order term. Let me re-read A.9.
"""
# Re-read A.9 first - we'll get the precise residual strategy and bound from
# the manuscript pages 41-42 to determine the actual structure to test.
print("This file is a scaffold. Re-reading pages 41-42 first.")
