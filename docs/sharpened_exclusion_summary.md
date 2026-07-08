# Sharpened multi-step K5 exclusion summary

Outcome: **sharpened but not solved**.

## What changed

The tighter checker replaced the baseline Rosser-Schoenfeld envelope with exact counts when available and Dusart 2010 bounds otherwise, but exact prime counting was unavailable in this run, so the actual certification used Dusart bounds ([exact-or-Dusart output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The tightened initial state has 64 certified safe moves instead of the single certified safe move \((3,5)\) found by the baseline checker ([exact-or-Dusart output](../src/t2_reachability_code/multi_step_exact_bounds.out), [baseline output](../src/t2_reachability_code/multi_step_activation_safety.out)).

A second certified move now exists, and the best-first search found a 12-step certified Maker-only prefix before stopping within budget ([exact-or-Dusart output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

No certified sequence claiming any K5 edge was found, and the best-first run ended with status `NEG_NO_POS_WITHIN_BUDGET` rather than exhaustion ([exact-or-Dusart output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

## What stayed unchanged

All ten K5 pair activations remain certified unsafe as initial moves, with deletion of vertex 3 still the worst upper-bound Breaker reply ([exact-or-Dusart output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The initial K5 exclusion therefore remains intact, although the broader multi-step exclusion is not proved ([K5 activation exclusion argument](k5_activation_exclusion_argument.md), [exact-or-Dusart findings](multi_step_exact_bounds_findings.md)).

## Structural status

The monovariant attempt did not find a proof-quality structural invariant, and no sampled state had a certified-safe K5 edge ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

The single-vertex candidate based on vertex 3 is not enough, because certified safe moves can capture vertex 3 while K5 moves remain unsafe ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

The edge-deletion and total-live-potential candidates are not decreasing monovariants on the sampled certified-safe transitions ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

## What remains open

Exact prime counts for all 2016 intervals remain open in this environment because no exact prime-counting backend was available ([exact-or-Dusart output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The tightened search should be extended with an exact `primecount` backend and a longer frontier budget, because the current best-first run stopped while a certified continuation still existed ([exact-or-Dusart output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

A proof-quality structural exclusion would need a new invariant, likely lexicographic, that handles both vertex-star losses and the low-prime pair-edge deletion debt seen after early safe captures ([monovariant analysis](monovariant_exclusion_analysis.md)).

Honest conclusion: this is **NEG within a tighter bounded search**, not a structural exclusion theorem ([exact-or-Dusart findings](multi_step_exact_bounds_findings.md), [monovariant analysis](monovariant_exclusion_analysis.md)).
