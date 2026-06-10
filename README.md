# erdos-872

A working repository for the AI-assisted attack on [Erdős Problem 872](https://www.erdosproblems.com/872), the divisibility-antichain saturation game on `{2, ..., n}`.

Companion forum thread: [erdosproblems.com/forum/thread/872](https://www.erdosproblems.com/forum/thread/872).

## What is in here

This repo is the working record of one contributor's attempt (April-June 2026) to (a) replicate, audit, and probe Om Buddhdev's April 2026 conditional `L(n) ≥ c_δ · n · (log log n)² / log n` lower bound, (b) test a self-derived `v3` trap-aware refinement of the residual Maker strategy, (c) push a formal Lean 4 statement of Problem 872 to `google-deepmind/formal-conjectures`.

The repo is unpolished on purpose. All raw logs, JSON results, intermediate scripts, and AI-generated drafts are preserved so that anyone (human or model) can audit the chain of reasoning end to end.

## v3 status (RETRACTED)

The `v3` strategy in `src/k4_avoidance_v3.py` originally appeared to pass restricted safe-edge hypothesis (RSE) on every tested multi-fiber configuration. The retraction document at [`RETRACTION.md`](RETRACTION.md) explains why this was an artifact of incomplete adversarial sampling. The corrected `v4` findings are at [`docs/v4_findings.md`](docs/v4_findings.md).

## v4 findings (current)

- **K_5 local obstruction**: no per-round Q-monotone Maker strategy exists on an isolated K_5 unit q-fiber ([`docs/v4_k5_walkthrough.md`](docs/v4_k5_walkthrough.md)).
- **First-activation obstruction for one K_5 witness**: all ten K_5 pair activations are unsafe as a first activation move with certified margin ≥ 3.15 × 10^16 (witness: `n = 10^20`, primes `{101, 103, 107, 109, 113}`, `q = 4806305873305829`) ([`docs/k5_safe_edge_certification.md`](docs/k5_safe_edge_certification.md)).
- **Structural reason**: vertex-3 star deletion carries far more weight than any near-100 pair claim ([`docs/k5_activation_exclusion_argument.md`](docs/k5_activation_exclusion_argument.md)).
- **Open**: multi-step activation strategies that first secure small-prime pairs before attempting K_5 pairs. Not ruled out by anything in this repo.

## T2 reachability

Outcome (C) of the T2 reachability question: there is a conditional incidence witness on `n = 10^20` with the prime tuple above ([`docs/t2_reachability_proof.md`](docs/t2_reachability_proof.md), code at [`src/t2_reachability_code/`](src/t2_reachability_code/)).

## Lean 4 formalization

The Lean statement file lives at [`lean/872.lean`](lean/872.lean). It uses an explicit-fuel minimax recursion (`gameValueAux`) so that `gameLength` is a real total definition with no `sorry` in its body. Only the five theorem proofs are `sorry`. Design notes and compile log are under [`lean/v3/`](lean/v3/).

The submission package to `google-deepmind/formal-conjectures` (PR body, GPT-5.5 audit report) is under [`submission/pr/`](submission/pr/). The audit identified five blocking issues in the prior `872_v2.lean` draft (weak quantifier bug, undefined `gameLength`, K_5 overclaim, prime variant misstatement, dishonest checklist line); all are fixed in the current `lean/872.lean`.

## Layout

```
lean/             current Lean 4 statement file (872.lean) + design notes + archive of prior drafts
submission/pr/    PR body for google-deepmind/formal-conjectures + GPT-5.5 audit
submission/forum/ forum-post drafts (v1, v2, v3) for erdosproblems.com/forum/thread/872
submission/outreach/  email drafts to Buddhdev and Jonas Silva (none sent as of this commit)
docs/             phase findings (0-5), v3/v4 reports, K_5 results, T2 reachability, AI sweep brief, manuscripts
src/              Python analysis code; t2_reachability_code/ has the K_5 arithmetic witness construction
src/legacy/       earlier solver / SAT / strategy prototypes preserved for traceability
results/          JSON result tables and the SAT plot
logs/             raw run logs from every script in src/
```

## AI assistance

This repository was produced primarily by Edwin Rosero (Ero23, [walkthroughwonder](https://github.com/walkthroughwonder)) with substantial AI assistance from Claude Sonnet 4.6 and GPT-5.5, orchestrated via Perplexity Computer. The GPT-5.5 audit at [`submission/pr/gpt55_audit_2026-06-09.md`](submission/pr/gpt55_audit_2026-06-09.md) is itself a worked example of cross-model checking on a Lean 4 / mathematical writeup.

Every quantitative claim in this repo (RSE pass rates, K_5 margins, T2 incidence witnesses) is reproducible from the scripts in `src/` and the results in `results/`. If anything fails to reproduce or looks wrong, please open an issue or post to the forum thread.

## License

MIT, see [`LICENSE`](LICENSE).
