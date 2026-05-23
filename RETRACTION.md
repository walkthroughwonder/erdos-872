# Retraction notice (2026-05-23)

The original `docs/forum_post_draft.md` and `docs/v3_proposition_a9_refinement.md`
contained claims about strategy `v3` that **do not hold**.

A self-critical review (`docs/v3_critique.md`) produced an explicit counterexample
on the `[5, 4]` configuration (one of the configurations the Monte Carlo evidence
was supposed to support):

- At the initial state of `[5, 4]`, `raw_rse(s)` is True (a safe capture exists),
  but the v3 strategy selects a SAFE_SCORE move because every first ordinary
  capture in a `K_5` fiber raises an adjacent live edge's `Phi` to 4.
- After v3's score, Shortener deletes the shared `q` vertex of the `K_5` fiber,
  collapsing nine live edges in one move.
- Full-round `Q` change: `-2`. The forum draft claimed nonnegative per-round Q.

A stronger single-fiber `[7]` example breaks the proposed `Q_after >= Q_before - 8 * w_max`
bound (observed delta `-13`).

Reproducer: `src/v3_counterexample_attempt.py`.

## What was wrong

1. The exhaustive enumeration and Monte Carlo checks tested `raw_rse(s)` (does *some* safe move exist
   from state s?) instead of "is the v3-selected move actually safe?"
2. The near-trap predicate is overbroad: it flags every first ordinary capture in any
   `K_k` fiber as unsafe, forcing v3 into SAFE_SCORE, which leaves a high-degree shared
   `q` vertex available for catastrophic Shortener deletion.
3. The analytical sketch in `v3_proposition_a9_refinement.md` contains several
   misformalizations of Buddhdev's manuscript, including a type error in `c_phi`,
   an incorrect lemma citation, and a quantifier error in the SAFE_CAPTURE
   non-emptiness claim.

## What remains valid

- The rank-2 activation RSE checker (`src/activation_rank2_rse.py`) and its
  100% pass on `k = 3, 4, 5` for several weight patterns are unaffected.
- The single-fiber `K_4` RSE failure characterization (Phase 4) is correct.
- The Buddhdev / Silva citations in `docs/phase3_forum_recon.md` are unaffected.

## Next steps

The forum post was **not** published; the outreach emails to Buddhdev and Silva
were **not** sent. See `docs/v3_critique.md` for the full diagnostic.
