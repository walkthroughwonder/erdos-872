# Erdős 865 — formalization of the `5/8` argument

This project formalizes, in Lean 4 / Mathlib, the argument that every set
`A ⊆ {1,…,N}` avoiding a "triple" (three distinct `a, b, c ∈ A` with `a+b, a+c, b+c ∈ A`)
has `|A| ≤ (5/8)N + O(1)`, together with a matching construction showing `5/8` is optimal.

## What is proved (0 `sorry`, only standard axioms `propext`, `Classical.choice`, `Quot.sound`)

All statements live in namespace `Erdos865`.

* `RequestProject/Defs.lean` — definitions: `HasTriple`, `IsBad`, the folded sum sets
  `lowSums`/`highSums`/`collisions`, the `FoldedOK` predicate, and the folding sets
  `Xset`/`Yset`/`Bset`/`Eset`.
* `RequestProject/Lemma1.lean` — **Lemma 1**, the folded additive lemma
  `|B| − |C(B)| ≤ m/4 + O(1)`, proved in full (reflection symmetry, a four-set
  inclusion–exclusion in `ZMod m` with all six pairwise-intersection bounds, and the
  deletion induction).
* `RequestProject/Main.lean`:
  * `lemma2` — folding a bad set around a pivot, `|X| + |Y| ≤ (5/4)h − |I| + O(1)`.
  * `badset_even`, `badset_card_le` — the `5/4·H` / `5/8·N` upper bounds (even case, then
    the reduction to general `N`).
  * `erdos865` — the threshold form: there is `C` such that every `A ⊆ {1,…,N}` with
    `|A| ≥ (5/8)N + C` contains a triple.
  * `sharp` — for `N = 8k`, the set `[k,2k] ∪ [4k,8k]` is bad and has `5k + 2 = (5/8)N + 2`
    elements, so the constant `5/8` is best possible.

## The one assumption: `CoarseBound`

The whole argument is **conditional on** the external "coarse theorem", formalized as the
hypothesis

```
CoarseBound θ K₀  :=  ∀ M S, MemRange M S → IsBad S → (S.card : ℝ) ≤ θ * M + K₀
```

for some `θ < 2/3`. This is the user's stated "one external input". It is carried as an
explicit hypothesis of `badset_even`, `badset_card_le`, and `erdos865` (it cannot be added
as an `axiom` without compromising soundness, and proving it is a separate result).

Consequently this development **certifies that the reduction is correct** — i.e. *"coarse
theorem ⟹ `5/8` bound"* is a fully verified theorem — but it does **not** establish
Erdős 865 unconditionally. An unconditional proof additionally requires a formal proof of
`CoarseBound θ K₀` for some `θ < 2/3`.

No step of the user's argument was found to be false: every lemma stated was provable as
written.
