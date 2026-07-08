# Summary of changes for run 32731fa9-8fb0-4d78-929a-d6a1f9e22aa2
I formalized your `5/8` argument for Erdős 865 in Lean 4 / Mathlib. The project builds cleanly and contains **no `sorry`s and no added axioms** — every theorem depends only on the standard `propext`, `Classical.choice`, `Quot.sound`.

**Scope (as you agreed):** the development is *conditional on* the external "coarse theorem", carried as an explicit hypothesis
`CoarseBound θ K₀ := ∀ M S, MemRange M S → IsBad S → (S.card:ℝ) ≤ θ*M + K₀` with `θ < 2/3`. It cannot be added as an `axiom` without breaking soundness, so it is a hypothesis of the main results. Thus the Lean proof **certifies that your reduction is correct** ("coarse theorem ⟹ 5/8 bound"), but does not by itself establish Erdős 865 unconditionally — that additionally needs a formal proof of `CoarseBound` for some `θ < 2/3` (you cited `f₃(M) ≤ (2/3−ε)M`; I did not independently verify that this is an established result).

**What is fully proved** (namespace `Erdos865`):
- `Defs.lean`: `HasTriple`, `IsBad`, the folded-sum sets (`lowSums`/`highSums`/`collisions`), `FoldedOK`, and the folding sets `Xset`/`Yset`/`Bset`/`Eset`.
- `Lemma1.lean`: **Lemma 1** (the folded additive lemma `|B| − |C(B)| ≤ m/4 + O(1)`) proved in full from scratch — reflection symmetry, the four-set inclusion–exclusion in `ZMod m` with all six pairwise-intersection bounds, and the deletion induction.
- `Main.lean`: `lemma2` (folding around a pivot, `|X|+|Y| ≤ (5/4)h − |I| + O(1)`), `badset_even` and `badset_card_le` (the `5/4·H` / `5/8·N` bounds, even case then odd reduction), `erdos865` (the threshold form: there is `C` with every `A ⊆ {1,…,N}`, `|A| ≥ (5/8)N + C`, containing a triple), and `sharp` (for `N=8k`, `[k,2k] ∪ [4k,8k]` is bad with `5k+2 = (5/8)N+2` elements, so `5/8` is optimal).

**Findings:** I sanity-checked the problem computationally (the maximum bad-set size and your construction match the true optimum at small `N`), and crucially **no step of your argument turned out to be false** — every lemma you stated formalized and was provable as written, including all the hand-waved `O(1)` bounds, which I had to pin down to explicit constants (the bookkeeping works out to `5/8 N + O(1)`). The remaining `O(1)` constants are existentially quantified, matching your write-up.

**Caveats:** some machine-generated proofs carry benign linter warnings (unused `hm`/`hB` hypotheses in a few internal helper lemmas and a few redundant `simp` arguments); these are cosmetic, the file compiles, and I left them rather than risk destabilizing verified proofs. A high `maxHeartbeats` is set because several proofs are computationally heavy.

See `PROOF_NOTES.md` for the file-by-file structure and the precise statement of the conditional dependency.