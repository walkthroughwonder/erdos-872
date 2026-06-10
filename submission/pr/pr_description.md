# Add Erdős Problem 872 (primitive set game)

## Summary

This PR adds a Lean 4 statement file for [Erdős Problem 872](https://www.erdosproblems.com/872), which asks how long the divisibility-antichain saturation game on `{2, ..., n}` can be guaranteed to last.

The file is statements only (all theorem proofs are `sorry`). The goal is to add a precise formal statement for reviewer feedback and future proof attempts.

## Why this problem

In a keyword scan of the existing `ErdosProblems/*.lean` files (game / strategy / player / Maker / Breaker), I did not find another file centered on a game-value formalization. Adding 872 opens the corpus to saturation-game style questions, of which Erdős posed several.

## Contents

Five theorem statements, all open or trivially-solved:

| Theorem | Status | Source |
|---------|--------|--------|
| `parts.weak` | open | Erdős original (existence of a positive linear lower bound) |
| `parts.strong` | open | Erdős original (≥ (1-ε)·n/2) |
| `trivial_upper_bound` | solved (trivial) | L(n) ≤ n-1 |
| `variants.prime_question` | open | Forum thread question (whether every terminal play has size at least π(n)) |
| `variants.buddhdev_conditional` | open | Om Buddhdev (2026, private manuscript shared with the contributor), conditional on the restricted safe-edge hypothesis (see [audit](https://github.com/walkthroughwonder/erdos-872)) |

## Modeling choices

The game is formalized via:

- `IsPrimitive n A`: predicate for `A ⊆ {2, ..., n}` being primitive (no element divides another).
- `GamePos n`: a position consisting of the already-claimed set and the still-unclaimed pool.
- `legalMoves p`: the unclaimed elements whose insertion preserves primitiveness.
- `applyMove p x`: total move function (claims `x`, erases it from the pool); used by the recursion only on legal moves.
- `gameValueAux fuel turn p`: explicit-fuel minimax recursion. Prolonger maximizes, Shortener minimizes, both over `legalMoves`. Fuel is initialized to `p.pool.card`, which is sufficient because every played move strictly shrinks the pool.
- `gameLength p := gameValueAux p.pool.card true p`: a real total definition (no `sorry` in the body).
- `L n := gameLength (startPos n)`: the canonical Erdős-Cameron primitive-set game length.

The Prolonger-Shortener (saturation-game) alternation is the lightest semantics that makes the problem precise. If reviewers prefer a different formalization (e.g., reusing existing combinatorial-game machinery in Mathlib, or a Conway-style `GameValue` definition), I am happy to adapt.

## Notes on the conditional variant

`variants.buddhdev_conditional` records a candidate partial result from a private manuscript shared with the contributor by Om Buddhdev (April 2026). Under the restricted safe-edge hypothesis (Definition 4.5 of the manuscript, applied to states actually reachable by the T2 activation strategy and residual slot construction), Theorem 4.7 gives `L(n) ≥ c_δ · n · (log log n)² / log n` for every fixed `0 < δ < 1/4`. Proposition A.9 repeats the conditional T2 lower bound for activation-graph states.

The hypothesis itself is non-trivial. See [this analysis](https://github.com/walkthroughwonder/erdos-872) for (a) an exhaustive local obstruction on isolated K_5 unit q-fibers (no per-round Q-monotone Maker strategy exists), and (b) a first-activation obstruction for one concrete K_5 witness (n=10^20, primes {101,103,107,109,113}, q=4806305873305829, all ten K_5 pair activations unsafe as a first activation move, certified margin ≥ 3.15×10^16). This does NOT rule out multi-step activation strategies that first secure small-prime pairs before attempting K_5 pairs, which remains an open question.

The conditional form is the version actually proved in the manuscript; the unconditional version remains open. The manuscript is not yet public; the formal statement records the conditional implication as stated by the author, pending publication. Reviewers who want to evaluate the cited statements may request the manuscript text via the linked audit repo.

## Disclosure

This file was drafted with AI assistance (Claude Sonnet 4.6 + Perplexity Computer) and reviewed manually against the style of [873.lean](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/873.lean), [868.lean](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/868.lean), and [865.lean](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/865.lean). The author has been working on Problem 872 since early 2026 and submitted a manuscript-faithful audit + computational analysis [here](https://github.com/walkthroughwonder/erdos-872).

## Checklist

- [x] References both the problem page and the related forum thread
- [x] Theorem statements categorized via `@[category research open]` / `@[category research solved]`
- [x] AMS codes (5, 11, 91) attached
- [x] Theorem proofs are `sorry`; no new axioms introduced
- [ ] Reviewers requested: maintainers familiar with combinatorial game formalization in Mathlib
- [ ] Open question: does the repo prefer a separate `Maker_Breaker` module for the game machinery, or inline definitions per problem
