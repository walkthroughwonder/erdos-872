# Forum post: erdosproblems.com/forum/thread/872

**Subject**: Lean statement file for #872 merged + computational analysis (negative result on K_5 q-fibers, conditional on Buddhdev's framework)

---

Two small contributions on this thread, both with AI disclosure up front.

## 1. Lean statement file for #872 (merged)

[PR #4226 on google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures/pull/4226) has been merged (2026-07-02), adding [FormalConjectures/ErdosProblems/872.lean](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/872.lean) and closing the tracking issue #994. The open statements have `sorry` proofs; the trivial bound and two supporting lemmas are fully proved. The merged file contains:

- `erdos_872.parts.i` (research open): the weak form, whether there exists ε > 0 with L(n) ≥ ε·n for all sufficiently large n
- `erdos_872.parts.ii` (research open): the strong form, whether L(n) ≥ (1-ε)·n/2 eventually for every ε > 0, with a status note recording the Shortener strategies discussed in this thread ((23/48 + o(1))·n and the claimed 0.19·n)
- `erdos_872.trivial_upper_bound` (textbook, fully proved): L(n) ≤ n-1, via the fuel-recursion cardinality bound `gameValueAux_le`
- `erdos_872.variants.prime_question` (research open): the question raised earlier in this thread, stated structurally: must every maximal primitive subset of {2,...,n} have size at least π(n)?
- The game semantics: `L n` is defined by a genuine finite minimax recursion (positions, legal moves, fuel-bounded `gameValueAux`), not an uninterpreted placeholder, with API lemmas `mem_legalMoves` and `gameValueAux_le` proved

The file fixes Prolonger to move first (following the convention in this thread) and documents why the choice matters: computational data suggests the Shortener-first value tracks π(n) while the Prolonger-first value grows linearly.

Buddhdev's conditional c_δ · n · (log log n)² / log n bound is not in the merged file. The manuscript is not yet public, so the citation could not be evaluated, and a faithful formal statement of the conditional form needs the restricted safe-edge hypothesis formalized. It can follow as a second PR once the manuscript is available.

Review was straightforward: mo271 approved, with one note (docstrings should be LaTeX markdown) addressed in a follow-up commit before merge. If anyone spots issues with the game formalization (especially @Pommeret, who self-identified as working on formalization), corrections via a follow-up PR are easy.

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

Happy to extend the multi-step activation checker, add Lean proofs to specific cases, or coordinate with anyone already working on this. Tagging @Om_Buddhdev_sensho, @jonaslsa, @Pommeret, @old-bielefelder.
