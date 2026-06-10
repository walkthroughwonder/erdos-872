# Erdos 872 compile notes

## Outcome

The file type-checks. After two fixes, `872_v2.lean` compiles against the real
built Mathlib (v4.27.0) with zero errors and zero linter warnings, leaving only
the expected `sorry` warnings. Verification was done with
`lake env lean FormalConjectures/ErdosProblems/872_v2_check.lean` (a single-file
type-check using the already-built `FormalConjectures.Util.ProblemImports`), not
a full `lake build` from scratch. Exit code 0.

The fixes were found by first type-checking the original `872.lean` the same
way, which surfaced two real errors and one linter warning (the rest of the file
was already correct).

## Environment confirmed

- Lean toolchain: `leanprover/lean4:v4.27.0` (from `lean-toolchain`).
- Mathlib pin: `rev = "v4.27.0"`, scope `leanprover-community` (from
  `lakefile.toml`, matching `lake-manifest.json` `inputRev = "v4.27.0"`).
- The `FormalConjectures` library uses glob inclusion
  (`globs = ["FormalConjectures.+"]` in `lakefile.toml`), so dropping the file
  into `FormalConjectures/ErdosProblems/872.lean` is sufficient. There is no
  hand-maintained import index file to edit.
- `warn.sorry = false` is set for the `FormalConjectures` library, so a real
  `lake build` of this file would emit no `sorry` warnings and no diagnostics.

## Errors found in the original and how they were fixed

### 1. Orphan doc-comment (error)

Original error:

```
872.lean:52:69: error: unexpected token '/--'; expected 'lemma'
```

The long block at original lines 35 to 52 was written as a doc comment
(`/-- ... -/`) but was not attached to any declaration (the `structure GamePos`
that follows has its own `/-- ... -/`). In Lean 4 a `/--` doc comment must be
immediately followed by a declaration, so the parser saw the next `/--` and
failed.

Fix: change that block from `/-- ... -/` to a plain block comment `/- ... -/`.
Confidence: high (confirmed by the compiler accepting the result; this is the
standard idiom for prose that does not document a single declaration).

### 2. Pipe-precedence type mismatch (error)

Original error:

```
872.lean:120:19: error: Type mismatch
  Finset.filter Nat.Prime (Finset.Icc 2 n)
has type
  Finset ℕ
but is expected to have type
  ℕ
```

The original wrote `L n ≥ (Finset.Icc 2 n).filter Nat.Prime |>.card`. The `|>.`
pipe binds more loosely than the `≥` comparison in this position, so the term
elaborated as `L n ≥ ((Finset.Icc 2 n).filter Nat.Prime)`, comparing a `ℕ`
against a `Finset ℕ`, and the trailing `.card` was left dangling.

Fix: parenthesize the filtered set and apply `.card` directly:
`((Finset.Icc 2 n).filter Nat.Prime).card`. Confidence: high (confirmed by the
compiler; `Finset.filter Nat.Prime` resolves because `DecidablePred Nat.Prime`
is available, and `.card` then yields the `ℕ` the inequality expects).

### 3. Second module docstring (linter warning)

Original warning:

```
872.lean:91:0: warning: This file has more than one module docstring
```

The header `/-! # Erdős Problem 872 ... -/` near the top is the module docstring.
The later `/-! ## Erdős Problem 872 ... -/` was a second module docstring, which
the project's `linter.style.moduleDocstring` (enabled via
`weak.linter.style.moduleDocstring = true`) flags.

Fix: change the second `/-! ... -/` to a plain block comment `/- ... -/`.
Confidence: high (confirmed by the compiler; matches neighbor files such as
`865.lean` and `873.lean`, which carry exactly one `/-!` header each).

## Items that were already correct (no change needed)

These were checked against neighbor files and the Mathlib source and confirmed by
the successful type-check:

- `answer(sorry) ↔ ...`. The macro is
  `syntax (name := Google.answer) "answer(" term ")" : term`
  (`FormalConjectures/Util/Answer/Syntax.lean`); `sorry` is a valid term. Matches
  `873.lean`.
- `@[category research open, AMS 5 11]` and `@[category research solved, ...]`.
  Match `865.lean`.
- `Finset.filter` argument order in `applyMove`: `p.pool.filter (fun y => ...)`
  elaborates to `Finset.filter (fun y => ...) p.pool`, the correct order; the
  `ℕ` predicate is decidable.
- `applyMove` field-by-field proof: `refine { ... , field := ?_, ... } <;> sorry`
  opens and closes the four proof-field goals (reported as four `sorry`
  warnings on the one declaration).
- `startPos` field proofs (`by simp`, `subset_refl _`,
  `intro x hx; refine ⟨?_, ?_⟩ <;> simp_all`) all closed successfully, so the
  `simp` and `simp_all` lemma sets were sufficient. No extra lemmas were needed.
- `Real.log`, `Filter.atTop`, `Finset.Icc` are all provided transitively by
  `FormalConjectures.Util.ProblemImports`; no extra imports were required.
- `noncomputable` annotations on `applyMove`, `startPos`, `gameLength`, `L` are
  correct.

## sorry / warning state of `872_v2.lean`

- `sorry` occurrences: nine declarations
  (`applyMove` (reported 4 times for its 4 field goals), `gameLength`, and the
  five theorems `weak`, `strong`, `trivial_upper_bound`, `prime_lower_bound`,
  `buddhdev_conditional`).
- Single-file type-check (`lake env lean`): only the `sorry` warnings above, no
  errors, no linter warnings.
- Under a real `lake build` (library option `warn.sorry = false`): no `sorry`
  warnings would be emitted either, so the file would build silently.

## Items that still warrant a full `lake build` to be fully certain

The single-file `lake env lean` check is authoritative for type-checking, since
it uses the already-built Mathlib and `ProblemImports` oleans. The only things it
does not exercise are project-build-specific behaviors:

- The project linters that run only under the `FormalConjectures` library build
  (for example `linter.style.ams_attribute`, `linter.style.category_attribute`,
  the namespace linter). The single-file check did pick up the module docstring
  linter and it now passes, which is a good sign, but a full library build is the
  only way to confirm every project linter is satisfied. Confidence that they
  pass: medium to high (the file follows neighbor idioms closely).
- Nothing in the file's mathematical content is verified, by design; all proofs
  remain `sorry`.

## PR readiness recommendation

The file is in good shape to open as a draft / RFC for community review. It
type-checks cleanly against the pinned Mathlib with only `sorry` proofs, the
statements follow the neighbor-file idioms (`answer(...)`, the `category` and
`AMS` attributes, single module docstring), and the two real errors plus the one
linter warning have been fixed and verified.

Recommendation: open it as a draft PR now, noting in the description that all
proofs are `sorry` and that the statements (especially the precise form of the
two main asymptotic bounds and the `buddhdev_conditional` variant) are the part
that wants reviewer eyes. The one thing worth doing before marking it ready
(non-draft) is a full `lake build FormalConjectures.ErdosProblems.872` in a
CI-like environment to confirm the project-specific linters all pass, since the
single-file check cannot run those.
