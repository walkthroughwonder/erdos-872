# Forum post: erdosproblems.com/forum/thread/872

**Subject**: Lean formalization draft + computational analysis (negative result on K_5 q-fibers, conditional on Buddhdev's framework)

---

Two small contributions on this thread, both with AI disclosure up front.

## 1. Lean statement file for #872

I have opened a PR on [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures) adding `ErdosProblems/872.lean` (link will go here once the PR number is assigned). The file is statements only (all proofs `sorry`) and covers:

- The two asymptotic targets in the original problem (ε·n and (1-ε)·n/2)
- The trivial upper bound L(n) ≤ n-1
- The Angelo-style π(n) lower bound raised above in this thread
- Buddhdev's conditional c_δ · n · (log log n)² / log n bound

Problem 872 is currently the first game-theoretic Erdős problem in the repo, so reviewers will likely have opinions on how to formalize Maker-Breaker semantics. Feedback welcome on the formalization (especially from @pommeret who self-identified as working on formalization).

## 2. Computational analysis of Buddhdev's manuscript framework

I have been working through Buddhdev's manuscript (the c_δ · n · (log log n)² / log n result) and synthesizing exhaustive safety-game strategies for the rank-3 unit-weight residual slot game in Appendix A. Repo: [walkthroughwonder/erdos-872](https://github.com/walkthroughwonder/erdos-872) (MIT, public, with a v3 retraction documented).

Two results:

(a) **Positive**: per-round Q-monotone Maker strategies exist on isolated K_4 unit q-fibers over {13, 17, 19, 23} (the exact fiber in Buddhdev's Proposition A.2 example), and on small configurations like [4,2], [4,3], [3,3,3].

(b) **Negative**: on an isolated K_5 unit q-fiber, no per-round Q-monotone Maker strategy exists. Shortener can force a state with three live Φ = 8 edges, after which every Maker move admits a worst-case full-round Q-delta of -8. The full forced sequence is verified line-by-line against Appendix A.1 in [v4_k5_walkthrough.md](https://github.com/walkthroughwonder/erdos-872/blob/main/docs/v4_k5_walkthrough.md). Reproducer at [src/v4_k5_bad_path.py](https://github.com/walkthroughwonder/erdos-872/blob/main/src/v4_k5_bad_path.py).

This raises the question of whether Buddhdev's Definition 4.5 (states "actually reached by the T2 activation strategy") admits such fibers. I investigated and found:

(c) **Initial-state K_5 activation exclusion**. Using Proposition A.6's safety potential and a concrete arithmetic instance (n = 10^20, δ = 1/8, primes {101, 103, 107, 109, 113}, q = 4806305873305829), all ten K_5 pair activations are unsafe as a first activation move in the full activation graph. The structural reason is that the small-prime vertex 3 carries a star of token weight far larger than the gain from claiming any near-100 pair. Certified margin ≥ 3.15 × 10^16. Details at [docs/k5_safe_edge_certification.md](https://github.com/walkthroughwonder/erdos-872/blob/main/docs/k5_safe_edge_certification.md).

The exclusion does **not** cover multi-step activation strategies that first secure small-prime pairs before attempting K_5 pairs. That extension is open.

(d) **Reading question on Definition 4.5**. Proposition A.6 says Prolonger picks "a safe edge supplied by that hypothesis," which leaves the selector existential. Is the intended reading a canonical selector, a selector chosen to make Proposition A.9 work, every selector that always chooses a safe edge, or every legal play? Proposition A.2 already flags this distinction for the K_4 case. Clarification from @Om_Buddhdev_sensho would be very helpful.

## Disclosure

All of this used AI assistance (Claude Sonnet 4.6 and GPT-5.5 Pro via Perplexity Computer) for code generation and safety-game synthesis, with manual verification against the manuscript. The v3 retraction in the repo documents an earlier flawed attempt that I withdrew after self-criticism caught it; the v4 result above survived that critique.

Happy to extend the multi-step activation checker, add Lean proofs to specific cases, or coordinate with anyone already working on this. Tagging @Om_Buddhdev_sensho, @Jonas Silva, @pommeret, @old-bielefelder.
