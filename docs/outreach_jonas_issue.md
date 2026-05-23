# Outreach: GitHub issue on jonaslsaa/maths

Repo: https://github.com/jonaslsaa/maths
Title: Erdős #872: trap-aware refinement of the residual strategy (Buddhdev Proposition A.9)

Body:

Hi Jonas,

Your April 2026 dyadic semiprime note on #872 was a great read. I have been working on the *other* half of the bound (the conditional T2 in Buddhdev's Theorem 4.7) and posted a refinement to thread 872 at [erdosproblems.com](https://www.erdosproblems.com/forum/thread/872).

Quick summary: the residual safe-edge hypothesis (Definition 4.5) fails on isolated `K_4` fibers (Proposition A.2), but the failure is gated on reaching a "near-trap" local geometry (`0` vertex deletions, `0` scored edges in fiber, `>= 1` ordinary capture, `>= 1` post-capture live edge with `Phi == 8`). I tested a Maker strategy `v3` that classifies each live edge as SAFE_CAPTURE / SAFE_SCORE / UNSAFE based on whether ordinary capture would enter the near-trap state, and only plays SAFE moves when any exist. `v3` achieves 100 percent RSE pass on every exhaustively enumerable multi-fiber configuration (8 of them) and on 60000 Monte Carlo trials at `[5, 4]`, `[4, 4, 2]`, `[5, 4, 3]`, `[6, 4]`. Final score `S_fin >= M/8` (Proposition A.3) holds in every case.

Repo with code, Lean 4 skeleton, and JSON outputs: [github.com/walkthroughwonder/erdos-872](https://github.com/walkthroughwonder/erdos-872).

The open question is whether `v3` can be proved sound for all fiber configurations, which would make Theorem 4.7 unconditional and push the unconditional lower bound from `(1/8 - o(1)) n loglog n / log n` to `c_delta n (loglog n)^2 / log n`.

Curious whether this connects to anything in your dyadic-chain construction (in particular, whether the H-secured small odd primes in your setup play a similar role to the activation phase that interacts with the residual game). Would love to hear your take.

Edwin Rosero
[github.com/walkthroughwonder](https://github.com/walkthroughwonder)
