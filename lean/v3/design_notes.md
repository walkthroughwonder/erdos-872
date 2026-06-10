# Erdos 872 v3 design notes

## Files

- Final Lean file: `/home/user/workspace/erdos872/872_v3.lean`
- Compile log: `/home/user/workspace/erdos872/872_v3_compile.log`
- Checked copy in the local repository: `/home/user/fc-build/FormalConjectures/ErdosProblems/872.lean`

## Game value design

I chose the explicit-fuel minimax recursion style.

The position type is deliberately computational:

```lean
structure GamePos (n : ℕ) where
  claimed : Finset ℕ
  pool : Finset ℕ
```

The old proof-carrying fields were removed, which eliminates proof obligations in `applyMove` and avoids definition-level `sorry` terms. Legality is enforced at each node by

```lean
def legalMoves {n : ℕ} (p : GamePos n) : Finset ℕ :=
  p.pool.filter fun x => IsPrimitive n (insert x p.claimed)
```

The move operation is total and simple:

```lean
def applyMove {n : ℕ} (p : GamePos n) (x : ℕ) : GamePos n where
  claimed := insert x p.claimed
  pool := p.pool.erase x
```

This models the actual saturation game because illegal unclaimed elements are not removed early. They remain in `pool`, but `legalMoves` filters them out at every subsequent turn. The game stops exactly when no unclaimed element can be legally inserted into the claimed primitive set.

The minimax recursion is

```lean
def gameValueAux {n : ℕ} : ℕ → Bool → GamePos n → ℕ
```

with `turn = true` for Prolonger and `turn = false` for Shortener. At Prolonger nodes it takes `max'` over the finite set of child values, and at Shortener nodes it takes `min'`. The explicit fuel is initialized to `p.pool.card` in

```lean
def gameLength {n : ℕ} : GamePos n → ℕ := fun p =>
  gameValueAux p.pool.card true p
```

Termination is structural on the fuel argument, so there are no `termination_by` or `decreasing_by` obligations. Semantically, the fuel matches the game tree depth from the starting position because every played move erases the chosen pool element.

`noncomputable section` is used because `legalMoves` filters using the propositional predicate `IsPrimitive`; no definition body contains `sorry`.

## Statement changes

- `erdos_872.parts.weak` now states `∃ ε > 0, ∀ᶠ n in atTop, (L n : ℝ) ≥ ε * n`.
- `erdos_872.variants.prime_question` is framed as an open question theorem with `answer(sorry)` and the requested name.
- The Buddhdev conditional docstring now says it records a private manuscript statement pending publication.
- AMS tags use `AMS 5 11 91`.

## Remaining sorries

Only theorem proof placeholders remain:

- `erdos_872.parts.weak`
- `erdos_872.parts.strong`
- `erdos_872.trivial_upper_bound`
- `erdos_872.variants.prime_question`
- `erdos_872.variants.buddhdev_conditional`

The `answer(sorry)` terms are part of the repository's open-question idiom and are not definition bodies.

## Compile check

Command run from `/home/user/fc-build`:

```bash
/home/user/.elan/bin/lake env lean FormalConjectures/ErdosProblems/872.lean
```

Result: exit code 0. The output contains only the expected warnings that the five theorem declarations use `sorry`.
