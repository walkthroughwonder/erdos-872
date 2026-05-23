# Outreach: email to Om Buddhdev

To: sensho@sensho.xyz
From: edwinrosero@gmail.com
Subject: Erdős #872: a trap-aware refinement of Proposition A.9 (RSE holds computationally on every multi-fiber tested)

Hi Om,

I have been working on the conditional gap in Theorem 4.7 of your April 2026 manuscript (the residual safe-edge hypothesis from Definition 4.5), and I think I have a refinement that makes RSE hold computationally on every multi-fiber rank-3 configuration I have been able to enumerate. I posted a summary to thread 872 at [erdosproblems.com](https://www.erdosproblems.com/forum/thread/872) and wanted to send the short version directly.

The core observation: the `K_4` failure in Proposition A.2 is gated on reaching a specific local geometry in some fiber (`0` vertex deletions, `0` scored edges, `>= 1` ordinary capture, `>= 1` post-capture live edge with `Phi == 8`). Call this the near-trap state. The unrestricted Maker strategy in your residual game can walk into it in two Shortener responses; the three local heuristics I tested (max-gain, dominant-capture, one-step lookahead) all get caught.

The fix is a strategy I call `v3`. At every pre-Maker state, classify each live edge `f` as:

  - SAFE_CAPTURE if ordinary capture of `f` does NOT push the host fiber into the near-trap state
  - SAFE_SCORE if `f` is used in an alternate-scoring move (always safe; preserves all other `Phi` values)
  - UNSAFE otherwise

Maker plays the max-`Q`-gain SAFE_CAPTURE if any exists, falls back to max-`Q`-gain SAFE_SCORE, and never plays UNSAFE when a safe move exists.

Computational evidence under `v3` against an adversarial Shortener:

  - exhaustive enumeration on `[4, 2]`, `[4, 3]`, `[4, 4]`, `[3, 3, 3]`, `[4, 3, 2]`, `[3, 3]`, `[3, 2, 2]`, `[2, 2, 2, 2]`: 0 RSE failures (vs. up to 30808 in the baseline strategy)
  - Monte Carlo on `[5, 4]`, `[4, 4, 2]`, `[5, 4, 3]`, `[6, 4]`: 60000 trials, ~486000 visited states, 0 RSE failures
  - `S_fin >= M/8` (Proposition A.3) holds in every exhaustively tested config

If this pattern is real, Proposition A.9 could be tightened by replacing the unrestricted "max-gain ordinary capture" specification with the `v3` selection rule, and Theorem 4.7 would become unconditional under that refined residual strategy. I have a Lean 4 skeleton stating the strategy invariant, but no proof yet.

Repo with all code and JSON results: [github.com/walkthroughwonder/erdos-872](https://github.com/walkthroughwonder/erdos-872).

Two specific asks if you have a few minutes:

  1. Does the near-trap predicate match what you had in mind when you noted in Section 8 that any potential-function proof must restrict to the strategy-generated state subspace?
  2. Is there a structural reason `v3` should also fail on some larger configuration I haven't enumerated, or is there a clean inductive argument lurking?

Happy to chat anywhere works for you. Either way, your manuscript was the right setup for this problem and made all of the above possible.

Best,
Edwin Rosero (Ero23)
[github.com/walkthroughwonder](https://github.com/walkthroughwonder)
