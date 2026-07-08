# 2026-06-26 #865 solution check

## Sources checked

- Problem page: [Erdős Problems #865](https://www.erdosproblems.com/865).
- AI-contributions wiki: [AI contributions to Erdős problems](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems).
- Discussion thread with writeup links: [#865 discussion thread](https://www.erdosproblems.com/forum/discuss/865).
- Linked writeup: [Overleaf writeup](https://www.overleaf.com/read/fzsvxkttcfpn#b71c6e).
- Linked formalization: [mrricky22/erdos-865-lean](https://github.com/mrricky22/erdos-865-lean).
- Formalization notes: [PROOF_NOTES.md](https://github.com/mrricky22/erdos-865-lean/blob/main/PROOF_NOTES.md) and [ARISTOTLE_SUMMARY.md](https://github.com/mrricky22/erdos-865-lean/blob/main/ARISTOTLE_SUMMARY.md).
- #872 reference statement: [formal-conjectures PR #4226](https://github.com/google-deepmind/formal-conjectures/pull/4226).

## Problem #865 statement

Problem #865 asks whether there exists a constant \(C>0\) such that, for all large \(N\), every \(A\subseteq\{1,\ldots,N\}\) of size at least \(5N/8+C\) contains distinct \(a,b,c\in A\) with \(a+b,a+c,b+c\in A\) ([Erdős Problems #865](https://www.erdosproblems.com/865)).

The page notes that the example \([N/8,N/4]\cup[N/2,N]\) shows the \(5/8\) constant would be best possible, and it frames #865 as the \(k=3\) case of an Erdős-Sós conjecture on pairwise sums ([Erdős Problems #865](https://www.erdosproblems.com/865)).

## AI-contributions row and writeup

The wiki row for #865 lists Ricky Cipollini, GPT-5.5 Pro, dates 21-22 Jun 2026, and outcome “Full solution,” but the row itself has no explicit writeup URL ([AI contributions to Erdős problems](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems)).

The #865 discussion thread links a short Overleaf paper and a Lean formalization repository for the claimed solution ([#865 discussion thread](https://www.erdosproblems.com/forum/discuss/865)).

## Technique summary

The Overleaf paper is titled “A sharp \(5/8\) bound for an Erdős-Sós pairwise-sums problem” and claims \(f_3(N)\le 5N/8+O(1)\), matching the standard lower-bound construction to resolve #865 ([Overleaf writeup](https://www.overleaf.com/read/fzsvxkttcfpn#b71c6e)).

The proof is a reduction from the Choi-Erdős-Szemerédi coarse bound \(f_3(N)\le (2/3-\varepsilon)N\) to the sharp \(5/8\) threshold ([Overleaf writeup](https://www.overleaf.com/read/fzsvxkttcfpn#b71c6e)).

The Lean notes describe the core method as a folding argument: a folded additive lemma \(|B|-|C(B)|\le m/4+O(1)\), reflection symmetry, four-set inclusion-exclusion in \(\mathbb{Z}/m\mathbb{Z}\), deletion induction, and folding around a pivot to obtain the \(5/4\cdot H\) or \(5/8\cdot N\) upper bound ([PROOF_NOTES.md](https://github.com/mrricky22/erdos-865-lean/blob/main/PROOF_NOTES.md)).

The formalization is conditional on an explicit `CoarseBound` hypothesis rather than an unconditional Lean proof of the Choi-Erdős-Szemerédi input ([ARISTOTLE_SUMMARY.md](https://github.com/mrricky22/erdos-865-lean/blob/main/ARISTOTLE_SUMMARY.md)).

## Relevance verdict for #872

Verdict: NOT-RELEVANT.

The #865 technique is additive-combinatorial folding for pairwise sums, while #872 is a two-player primitive-set saturation game governed by divisibility and antichain legality ([Erdős Problems #865](https://www.erdosproblems.com/865), [formal-conjectures PR #4226](https://github.com/google-deepmind/formal-conjectures/pull/4226)).

There may be process-level relevance from the Lean workflow and conditional-formalization pattern, but the mathematical mechanism does not address #872’s saturation-game dynamics, q-fiber residual hypergraphs, or safe-edge obstruction structure ([PROOF_NOTES.md](https://github.com/mrricky22/erdos-865-lean/blob/main/PROOF_NOTES.md), [formal-conjectures PR #4226](https://github.com/google-deepmind/formal-conjectures/pull/4226)).
