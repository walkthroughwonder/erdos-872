## Summary

This PR adds a Lean 4 statement file for [Erdős Problem 872](https://www.erdosproblems.com/872), which asks how long the divisibility-antichain saturation game on `{2, ..., n}` can be guaranteed to last.

The file contains three open statements (with `sorry` proofs), a fully proved trivial upper bound, and two proved API lemmas. The goal is to add a precise formal statement for reviewer feedback and future proof attempts.

## Why this problem

In a keyword scan of the existing `ErdosProblems/*.lean` files (game / strategy / player / Maker / Breaker), I did not find another file centered on a game-value formalization. Adding 872 opens the corpus to saturation-game style questions, of which Erdős posed several.

## Contents

| Theorem | Status | Source |
|---------|--------|--------|
| `parts.i` | open | Erdős original, weak form (existence of a positive linear lower bound) |
| `parts.ii` | open | Erdős original, strong form (≥ (1-ε)·n/2). The forum thread records accepted-but-unpublished Shortener strategies (≤ (23/48+o(1))·n, and a claimed ≤ 0.19·n) that would answer this negatively; disclosed in the docstring. |
| `trivial_upper_bound` | textbook (trivial), **proved in the file** | L(n) ≤ n-1 |
| `variants.prime_question` | open | Forum thread question: is every maximal primitive subset of `{2, ..., n}` of size at least π(n)? |

Two `@[category API]` lemmas (`mem_legalMoves`, `gameValueAux_le`) are proved rather than sorried; the second is the induction that powers the proof of `trivial_upper_bound`. Together they demonstrate that the game definitions are workable, not just well-typed.

## Modeling choices

The game is formalized via:

- `IsPrimitive n A`: predicate for `A ⊆ {2, ..., n}` being primitive (no element divides another).
- `GamePos n`: a position consisting of the already-claimed set and the still-unclaimed pool.
- `legalMoves p`: the unclaimed elements whose insertion preserves primitiveness.
- `applyMove p x`: total move function (claims `x`, erases it from the pool); used by the recursion only on legal moves.
- `gameValueAux fuel turn p`: explicit-fuel minimax recursion. Prolonger maximizes, Shortener minimizes, both over `legalMoves`. Fuel is initialized to `p.pool.card`, which is sufficient because every played move strictly shrinks the pool.
- `gameLength p := gameValueAux p.pool.card true p`: a real total definition (no `sorry` in the body).
- `L n := gameLength (startPos n)`: the Erdős primitive-set game length.

**Turn order.** The problem statement does not specify who moves first. The file fixes Prolonger to move first, matching the convention used in the forum discussion of the problem, and the choice is load-bearing: computed values for small `n` (in the audit repo linked below) suggest the Shortener-first value tracks π(n) while the Prolonger-first value grows linearly, so the two conventions plausibly give different answers to the weak question. The forum questions concern the Prolonger-first quantity, which is what `L` formalizes.

**Prime-question variant.** The forum question is stated structurally: every *maximal* primitive subset of `{2, ..., n}` (via Mathlib's `Maximal` with the subset order) has size at least `π(n)`. This is the faithful reading of the forum thread — it bounds every completed play regardless of strategy, which is strictly stronger than a bound on the optimal-play game value `L n` alone.

The Prolonger-Shortener (saturation-game) alternation is the lightest semantics that makes the problem precise. If reviewers prefer a different formalization (e.g., reusing existing combinatorial-game machinery in Mathlib, or a Conway-style `GameValue` definition), I am happy to adapt.

## Disclosure

This file was drafted with AI assistance (Claude Sonnet 4.6 + Perplexity Computer, revised with Claude Fable 5) and reviewed manually against the style of [873.lean](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/873.lean), [868.lean](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/868.lean), and [865.lean](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/865.lean). The author has been working on Problem 872 since early 2026 and maintains a manuscript-faithful audit + computational analysis [here](https://github.com/walkthroughwonder/erdos-872).

## Checklist

- [x] References both the problem page and the related forum thread
- [x] Theorem statements categorized via `@[category research open]` / `@[category textbook]` / `@[category API]`
- [x] AMS codes (5, 11, 91) attached
- [x] Open-problem proofs are `sorry`; `trivial_upper_bound` and the API lemmas are fully proved; no new axioms introduced

## Questions for reviewers

- Does the repo prefer a separate `Maker_Breaker` (or saturation-game) module for the game machinery, or inline definitions per problem?
- Reviewers familiar with combinatorial game formalization in Mathlib would be especially welcome.
