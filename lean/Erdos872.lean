/-
  Erdős Problem 872: Primitive-set saturation game
  ------------------------------------------------
  Two players (Long, Short) alternately pick distinct integers from {2, ..., n}
  into a shared set A subject to the primitive-set rule: no element of A divides
  another. The game ends when no further legal move exists. Long maximizes |A|,
  Short minimizes |A|.

  Define:
    sat_L(n) := game length under optimal Long, optimal Short, Long moves first.
    sat_S(n) := game length under optimal Long, optimal Short, Short moves first.

  Conjectures and bounds (Phase 3, aligned with Buddhdev manuscript Apr 2026 and
  the erdosproblems.com/forum/thread/872 community state of the art, 22 May 2026):

  Community notation: L(n) := sat_L n (Prolonger-first variant). Erdős's weak
  conjecture is
    (WeakErdos)   ∃ ε > 0. ∀ n sufficiently large.  L(n) ≥ ε · n.

  Current state of the art (unconditional):
    (LowerBound)  L(n) ≥ (1/8 − o(1)) · n · log log n / log n   (Buddhdev Thm 1.2)
    (UpperBound)  L(n) ≤ (W_4 / 2 + o(1)) · n  <  0.19 · n      (Buddhdev Thm 1.1)

  Conditional improvement target:
    (T2)  L(n) ≥ c_δ · n · (log log n)^2 / log n  (Buddhdev Thm 4.7, conditional
                                                  on the restricted safe-edge
                                                  hypothesis Def. 4.5).

  Our active goal: prove the restricted safe-edge hypothesis for the strategy-
  generated state subspace Σ_T2 of the rank-3 slot hypergraph G(n, δ), making T2
  unconditional. See gpt55_prompt.md for the precise statement.

  The Short-first variant sat_S satisfies an independent observation (not the
  Erdős problem itself, but useful as a separate finite-combinatorial fact):
    (SatS)  ∃ C : ℕ. ∀ n ≥ 4.  sat_S n ≤ Nat.primeCounter n + C
  Empirically sat_S(n) − π(n) ∈ {0, 1, 2} for n ∈ [4, 78] (CP-SAT + explicit
  "Short plays smallest available prime" strategy).

  Authors: Edwin Rosero, Phase 1 21 May 2026, Phase 2 22 May 2026, Phase 3
  reconciliation 22 May 2026 (afternoon) via Perplexity Computer + Buddhdev
  manuscript.
-/

import Mathlib.Data.Nat.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Lattice
import Mathlib.Data.Nat.Divisors
import Mathlib.Order.WellFounded

open Finset

namespace Erdos872

/-- The board: integers in `{2, ..., n}`. -/
def Board (n : ℕ) : Finset ℕ := (Finset.range (n + 1)).filter (· ≥ 2)

/-- A position is the set of integers still legal to play (not yet picked and not
    divisible-related to any picked element). -/
abbrev Position (n : ℕ) := Finset ℕ

/-- After playing `x`, remove from `S` every element `y` with `x ∣ y` or `y ∣ x`.
    Also remove `x` itself. -/
def play (x : ℕ) (S : Finset ℕ) : Finset ℕ :=
  S.filter (fun y => y ≠ x ∧ ¬ (x ∣ y) ∧ ¬ (y ∣ x))

/-- A move is legal in position `S` if `x ∈ S`. -/
def legal (x : ℕ) (S : Finset ℕ) : Prop := x ∈ S

/-- The game value with `Long` to move. -/
noncomputable def valueLong (S : Finset ℕ) : ℕ :=
  if h : S = ∅ then 0
  else
    have : ∃ x, x ∈ S := by
      rcases Finset.nonempty_of_ne_empty h with ⟨x, hx⟩
      exact ⟨x, hx⟩
    -- Long picks x maximizing 1 + valueShort (play x S)
    (S.image (fun x => 1 + valueShort (play x S))).max'
      (by
        rcases this with ⟨x, hx⟩
        exact ⟨1 + valueShort (play x S), Finset.mem_image.mpr ⟨x, hx, rfl⟩⟩)
termination_by S.card
decreasing_by
  simp_wf
  -- play strictly decreases card because x ∈ S is removed
  sorry

/-- The game value with `Short` to move. -/
noncomputable def valueShort (S : Finset ℕ) : ℕ :=
  if h : S = ∅ then 0
  else
    have : ∃ x, x ∈ S := by
      rcases Finset.nonempty_of_ne_empty h with ⟨x, hx⟩
      exact ⟨x, hx⟩
    (S.image (fun x => 1 + valueLong (play x S))).min'
      (by
        rcases this with ⟨x, hx⟩
        exact ⟨1 + valueLong (play x S), Finset.mem_image.mpr ⟨x, hx, rfl⟩⟩)
termination_by S.card
decreasing_by
  simp_wf
  sorry

/-- sat_L(n) = game value starting from the full board with Long to move. -/
noncomputable def satL (n : ℕ) : ℕ := valueLong (Board n)

/-- sat_S(n) = game value starting with Short to move. -/
noncomputable def satS (n : ℕ) : ℕ := valueShort (Board n)

------------------------------------------------------------------------
-- Empirical anchors (verified by exhaustive search up to n = 40)
------------------------------------------------------------------------

/-- Empirically-verified base values. Marked `axiom` for now; replace with
    `decide` once `valueLong` is made computable via a Lean implementation
    of the bitmask DP. -/
axiom satL_table :
  satL 10 = 5 ∧ satL 11 = 6 ∧ satL 20 = 9 ∧ satL 30 = 13 ∧ satL 40 = 16

------------------------------------------------------------------------
-- Phase 2 conjecture (current proof target)
------------------------------------------------------------------------

/-- The prime counting function π(n). -/
noncomputable def primeCounter (n : ℕ) : ℕ :=
  ((Finset.range (n + 1)).filter Nat.Prime).card

/-- PHASE 2 CONJECTURE: sat_S(n) ≤ π(n) + C for some absolute constant C ≥ 1.
    Proving this refutes the original Erdős weak conjecture (and a fortiori the strong
    conjecture), because π(n) ~ n / log n = o(n). -/
def phase2Conjecture : Prop :=
  ∃ C : ℕ, ∀ n ≥ 4, satS n ≤ primeCounter n + C

/-- Matching lower bound: sat_S(n) ≥ π(n).
    Reason: any terminal position is a maximal primitive subset of {2,…,n}; the primes
    are a minimum example, and (Lemma A below, verified by brute force for n ≤ 30)
    no smaller maximal primitive subset exists. -/
def phase2LowerBound : Prop :=
  ∀ n ≥ 4, satS n ≥ primeCounter n

/-- Corollary if both directions hold: sat_S(n) = π(n) + O(1). -/
def phase2Tight : Prop :=
  phase2LowerBound ∧ phase2Conjecture

------------------------------------------------------------------------
-- Phase 1 conjectures (historical; not the current target)
------------------------------------------------------------------------

/-- (Phase 1) WEAK CONJECTURE: positive density of `sat_L`. Empirically holds with
    slope ~ 1/e, but is NOT the game value, so does not bear on the Erdős questions. -/
def weakConjecture : Prop :=
  ∃ ε : ℝ, 0 < ε ∧ ∀ᶠ n in Filter.atTop, (satL n : ℝ) ≥ ε * n

/-- (Phase 1) STRONG CONJECTURE: same caveat as weak. -/
def strongConjecture : Prop :=
  ∀ ε : ℝ, 0 < ε → ∀ᶠ n in Filter.atTop, (satL n : ℝ) ≥ (1 - ε) * n / 2

/-- (Phase 1) regret growth -/
def regret (n : ℕ) : ℤ := (n / 2 : ℤ) - satL n

------------------------------------------------------------------------
-- Phase 2 supporting lemmas (proof obligations for GPT-5.5 Pro / Aristotle)
------------------------------------------------------------------------

/-- Lemma A (verified by brute force for n ≤ 30):
    The minimum size of a maximal primitive subset of {2,…,n} is exactly π(n),
    and the set of primes ≤ n is always a minimum example. -/
def lemma_A_min_maximal_primitive : Prop :=
  ∀ n ≥ 4, ∀ M : Finset ℕ, M ⊆ Board n →
    (∀ a ∈ M, ∀ b ∈ M, a ≠ b → ¬ (a ∣ b)) →
    (∀ x ∈ Board n, x ∉ M → ∃ m ∈ M, m ∣ x ∨ x ∣ m) →
    M.card ≥ primeCounter n

/-- Lemma B (verified for n ≤ 30):
    Short's optimal first move is always 2. -/
lemma_B_short_plays_two : Prop :=
  ∀ n ≥ 4, valueShort (Board n) = 1 + valueLong (play 2 (Board n))

/-- Lemma C: After Short plays 2, the remaining universe is exactly the odd integers in [3, n]. -/
lemma play_two_kills_evens (n : ℕ) (hn : n ≥ 4) :
    play 2 (Board n) = (Board n).filter (fun x => x % 2 = 1) := by
  ext x
  simp [play, Board]
  constructor
  · rintro ⟨hx, hxne, hnotdvd, hnotydvd⟩
    refine ⟨hx, ?_⟩
    -- 2 ∤ x  ⇔  x odd
    omega
  · rintro ⟨hx, hodd⟩
    refine ⟨hx, ?_, ?_, ?_⟩
    · -- x ≠ 2 because x is odd and 2 is even
      omega
    · -- ¬ (2 ∣ x) because x is odd
      omega
    · -- ¬ (x ∣ 2) because x ≥ 3
      have : x ≥ 3 := by
        simp [Board] at hx
        omega
      omega

/-- Strategy `S*` for Short (specification):
    1. Play 2 first.
    2. At each subsequent Short turn, play the smallest prime p ≤ √n still legal,
       OR if no such prime is legal, play the smallest composite c that maximizes
       the number of currently-alive elements killed.
    The claim is that `S*` produces a terminal set of size at most π(n) + C. -/
noncomputable def strategy_S_star (n : ℕ) : Strategy n :=
  fun S =>
    if 2 ∈ S then 2
    else
      -- smallest prime ≤ √n still in S
      let small_primes := S.filter (fun x => Nat.Prime x ∧ x * x ≤ n)
      if small_primes.Nonempty then small_primes.min' (by assumption)
      else
        -- fallback: smallest element
        S.min' (by sorry)

/-- Phase 2 main theorem (proof target): sat_S(n) ≤ π(n) + 1 for n ∈ [25, ?].
    The bound π(n) + 1 is consistent with all data n ∈ [25, 42]; the constant might
    need to be relaxed to π(n) + C for larger n. -/
theorem satS_upper_bound (n : ℕ) (hn : n ≥ 25) :
    satS n ≤ primeCounter n + 1 := by
  sorry

/-- Phase 2 lower bound (immediate from Lemma A): sat_S(n) ≥ π(n). -/
theorem satS_lower_bound (n : ℕ) (hn : n ≥ 4) :
    satS n ≥ primeCounter n := by
  -- The terminal position from Short-first optimal play is a maximal primitive subset,
  -- hence has size at least the minimum maximal primitive size, which is π(n) by Lemma A.
  sorry

/-- NOTE (Phase 3, 22 May 2026): the earlier theorem name `weak_conjecture_refuted`
    was based on a notation mistake. The Erdős weak conjecture is about
    `satL n` (Prolonger-first), not `satS n`. The community lower bound
    `satL n ≥ (1/8 - o(1)) n loglog n / log n` (Buddhdev Thm 1.2) is unconditional,
    while `satL n ≤ 0.19 n` (Buddhdev Thm 1.1) is also unconditional. The weak
    conjecture `satL n ≥ ε n` remains open.

    The result below is the (technically true but irrelevant-to-Erdős)
    refutation of a Short-first analogue, not the Erdős conjecture itself. -/
theorem satS_not_linearly_lower_bounded
    (hP : phase2Conjecture) :
    ¬ (∃ ε : ℝ, 0 < ε ∧ ∀ᶠ n in Filter.atTop, (satS n : ℝ) ≥ ε * n) := by
  -- π(n)/n → 0 by PNT, so any linear lower bound on sat_S contradicts sat_S ≤ π(n) + C.
  sorry

/-- The actual Phase 3 target: prove the restricted safe-edge hypothesis for the
    T2 activation strategy on the rank-3 slot hypergraph G(n, δ). See
    `gpt55_prompt.md` for the precise statement. If proved, Buddhdev Thm 4.7
    becomes unconditional, giving `satL n ≥ c_δ n (loglog n)^2 / log n`. -/
def restrictedSafeEdgeHypothesis : Prop := sorry  -- to be stated in slot-game terms

/-- Conditional T2 (Buddhdev Thm 4.7): if the restricted safe-edge hypothesis
    holds for the strategy-generated state subspace, then there is `c > 0` such
    that `satL n ≥ c n (loglog n)^2 / log n` for all sufficiently large `n`. -/
theorem satL_T2_conditional
    (hRSE : restrictedSafeEdgeHypothesis) :
    ∃ c : ℝ, 0 < c ∧ ∀ᶠ n in Filter.atTop,
      (satL n : ℝ) ≥ c * (n : ℝ) * (Real.log (Real.log n))^2 / Real.log n := by
  sorry

/-- The wide-open weak Erdős conjecture (Phase 3 ultimate target). -/
def weakErdosConjecture : Prop :=
  ∃ ε : ℝ, 0 < ε ∧ ∀ᶠ n in Filter.atTop, (satL n : ℝ) ≥ ε * (n : ℝ)

/-- The wide-open strong Erdős conjecture. -/
def strongErdosConjecture : Prop :=
  ∀ ε : ℝ, 0 < ε → ∀ᶠ n in Filter.atTop, (satL n : ℝ) ≥ (1/2 - ε) * (n : ℝ)

------------------------------------------------------------------------
-- Strategy v4 specification (operational)
------------------------------------------------------------------------

/-- A `Strategy` for Long is a function from a position to a legal move. -/
abbrev Strategy (n : ℕ) := Position n → ℕ

/-- Strategy v4: at each Long-turn position, pick the move that maximizes
    1 + min_over_short_replies(continuation_under_v2). -/
noncomputable def strategy_v4 (n : ℕ) : Strategy n :=
  -- Implementation deferred; specified operationally in `strategy_v4.py`.
  fun S => S.min' (by sorry)

/-- v4 achieves gap ≤ 1 across n ∈ [10, 35]. (Empirically verified.)
    Goal: prove v4 achieves gap ≤ C for some constant C, all n ≥ 10. -/
def v4_gap_bound_conjecture : Prop :=
  ∃ C : ℕ, ∀ n ≥ 10, satL n ≤ valueOf_v4 n + C
where
  valueOf_v4(n : ℕ) : ℕ := sorry

end Erdos872
