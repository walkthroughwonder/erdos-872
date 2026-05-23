# erdos-872

Computational attack on [Erdős Problem #872](https://www.erdosproblems.com/872): the largest antichain in the divisibility poset of `{1, ..., n}`, a.k.a. `L(n)`.

This repository accompanies a forum post at [erdosproblems.com/forum/thread/872](https://www.erdosproblems.com/forum/thread/872) proposing a trap-aware refinement of the residual Maker strategy in the Buddhdev slot-game framework (Apr 2026 manuscript). The refinement (called `v3`) achieves 100 percent restricted safe-edge hypothesis (RSE) pass on every small multi-fiber configuration tested, and satisfies the `M/8` final-score lower bound against an adversarial Shortener in every tested case.

## Headline result (computational, not yet proved)

Strategy `v3` (`src/k4_avoidance_v3.py`) passes RSE on:

| Config | Baseline failures | v3 failures |
|--------|-------------------|-------------|
| [4, 2] | 74 | 0 |
| [4, 3] | 686 | 0 |
| [4, 4] | 30808 | 0 |
| [3, 3, 3] | 576 | 0 |
| [4, 3, 2] | 5008 | 0 |
| [3, 3] | 0 | 0 |
| [3, 2, 2] | 0 | 0 |
| [2, 2, 2, 2] | 0 | 0 |

Final scores against adversarial Shortener:

| Config | `\|E\|` | `S_fin` | `M/8` | Holds? |
|--------|---------|---------|-------|--------|
| [4, 2] | 7 | 1 | 0.875 | yes |
| [4, 3] | 9 | 2 | 1.125 | yes |
| [4, 4] | 12 | 2 | 1.5 | yes |
| [3, 3, 3] | 9 | 3 | 1.125 | yes |

Larger configurations like `[5, 4]` and `[4, 4, 2]` exceed the current enumeration budget (8M pre-Maker states).

## Strategy v3 in one sentence

At every pre-Maker state, mark a live edge `f` as SAFE_CAPTURE if Maker's ordinary capture of `f` does NOT cause any fiber to enter the near-trap state (no vertex deletion, no scored edge in fiber, `>= 1` ordinary capture, `>= 1` live edge with post-capture `Phi >= 4`; equivalently, no live edge becomes `Phi == 8`). Mark `f` as SAFE_SCORE if Maker plays alternate-scoring (always safe). Prefer SAFE_CAPTURE with max `Q` gain, fall back to SAFE_SCORE with max `Q` gain. UNSAFE captures are forbidden if any safe move exists.

## Repository layout

```
src/
  activation_rank2_rse.py     # rank-2 activation RSE checker (Proposition A.6)
  fiber_rse_check.py          # single-fiber rank-3 RSE checker
  multi_fiber_rse.py          # multi-fiber rank-3 enumerator
  k4_avoidance_strategy.py    # v1, v2 trap-aware strategies (earlier iterations)
  k4_avoidance_v3.py          # v3 strategy, the one that achieves 100 percent RSE
  t2_reachability.py          # BFS under specific Maker strategies
  min_mp_sat.py               # Phase 2.5 SAT-based brute-force baseline
results/
  fiber_rse_k3.json           # single-fiber k=3 dump
  fiber_rse_k4.json           # single-fiber k=4 dump (216 RSE violations cataloged)
  phase2_merged.json          # SAT brute-force baseline
  sat_plot.png                # four-panel plot of brute-force results
lean/
  Erdos872.lean               # Lean 4 skeleton (statements only, no proofs)
docs/
  forum_post_draft.md         # forum post text
  phase4_computational_findings.md
  phase5_multi_fiber_findings.md
  gpt55_rse_attempt.md        # GPT-5.5 Pro's attempt with dominant-capture certificate
```

## Running

All scripts are pure Python 3.10+. No external dependencies beyond `numpy` (and `matplotlib` for `sat_plot.png`).

```bash
python src/k4_avoidance_v3.py                 # reproduces the v3 table above
python src/activation_rank2_rse.py            # rank-2 activation RSE
python src/multi_fiber_rse.py [4 3]           # multi-fiber rank-3 enum for [4, 3]
```

## Open mathematical question

The computational evidence is consistent across all tested configurations but is not a proof. The remaining task:

> Prove that for strategy `v3` and any fiber configuration `(k_1, k_2, ..., k_F)` with `k_i >= 2` and disjoint slot supports, at every reachable pre-Maker state with at least one positive-weight live edge, the SAFE_CAPTURE-or-SAFE_SCORE set is nonempty AND the chosen `v3` move yields a per-round `Q` change `>= 0` under any Shortener reply.

A proof would make Theorem 4.7 of Buddhdev unconditional, improving the unconditional lower bound on `L(n)` from `(1/8 - o(1)) n loglog n / log n` to `c_delta n (loglog n)^2 / log n`.

## Acknowledgments

This work builds directly on:

  - Om Buddhdev (Apr 2026), [slot-game framework manuscript](https://www.sensho.xyz/papers/erdos-872.pdf)
  - Jonas Silva (Apr 2026), [dyadic semiprime note](https://github.com/jonaslsaa/maths/blob/main/872.pdf)
  - Terence Tao's [AI-contributions-to-Erdős-problems wiki](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems)

Methodology: AI-assisted code generation and analysis using GPT-5.5 Pro and Claude Sonnet 4.6, orchestrated through Perplexity Computer.

## License

MIT. See `LICENSE`.

## Author

Edwin Rosero (Ero23), May 2026. Contact via GitHub issues on this repo.
