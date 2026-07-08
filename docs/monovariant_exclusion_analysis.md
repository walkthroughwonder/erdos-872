# Monovariant exclusion analysis

Outcome: **no proof-quality structural monovariant found**.

## Script and scope

The monovariant script is `/home/user/workspace/erdos872/src/t2_reachability_code/monovariant_analysis.py`, and its output is `/home/user/workspace/erdos872/src/t2_reachability_code/monovariant_analysis.out` ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

The analysis used the same Dusart-bound weights as the tighter multi-step checker, not exact prime counts, because exact prime counting was unavailable in this environment ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out), [exact-or-Dusart output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The explored state graph used certified-safe Maker-only transitions, consistent with the existing multi-step search limitation rather than a full adversarial strategy tree ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out), [baseline findings](multi_step_activation_findings.md)).

## Candidate diagnostics

At the initial state, the vertex-3 deletion weight is \(6.007341\times 10^{16}\), the maximum vertex-deletion weight is also \(6.007341\times 10^{16}\), and the best K5 margin is \(-5.619969\times 10^{16}\) ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

After the old first move \((3,5)\), the vertex-3 candidate drops to zero, but the best K5 margin remains negative at \(-3.539009\times 10^{16}\), so vertex 3 alone cannot be a structural certificate ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

After the tighter-bound prefix \((3,101),(5,103),(7,107)\), the vertex-3 candidate is still zero, but the best K5 margin remains negative at \(-3.237638\times 10^{16}\), so capturing vertex 3 does not open K5 safety by itself ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

A hand cleanup prefix that captures several low primes and three K5 vertices improves the best K5 margin to \(-3.769325\times 10^{15}\), but still reaches no certified K5-safe state ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

## Monotonicity checks

On 40 sampled certified-safe Maker-only transitions, `star3_upper` had no increases, but this candidate is too weak because it can drop to zero after certified safe moves while K5 remains unsafe ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

On the same sampled transitions, `max_vertex_loss_upper` and `total_uncaptured_star_upper` had no increases, but the sample was budget-limited and reached no K5-safe state, so these observations do not define a separating threshold ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

The edge-deletion candidates fail as ordinary monovariants: `max_edge_phi_upper` increased on 39 sampled transitions, and `low_pair_debt_upper` increased on 39 sampled transitions ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

The total-live-potential candidate also fails as a decreasing monovariant because `total_live_phi_upper` increased on all 40 sampled transitions ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

## K5 threshold check

The sampled analysis evaluated 41 states and found zero states with any certified-safe K5 edge ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

The best K5 margin seen in the sample was still negative at \(-3.188182\times 10^{16}\), so no empirical K5-safe threshold was available to compare against candidate \(\Psi\) values ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

## Structural conclusion

No structural exclusion proof is visible from these candidates, because the obstruction shifts from vertex deletion to deletion of large low-prime pair edges as safe captures accumulate ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).

A plausible future direction is a lexicographic invariant that first controls vertex-star losses and then controls edge-deletion debt, but the current data do not justify claiming such an invariant ([monovariant output](../src/t2_reachability_code/monovariant_analysis.out)).
