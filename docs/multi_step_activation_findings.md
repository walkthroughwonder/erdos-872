# Multi-step K5 activation findings

Executive summary: **NEG**. No certified multi-step counterexample was found within the implemented Maker-only search, and the rigorous checker stops after the single certified first move \((3,5)\) because no second move is certified safe by the same Rosser-Schoenfeld one-sided bounds ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

This is **not** a proof that no multi-step activation strategy exists. The result is a bounded negative search with conservative sufficient safety certificates, so the gap remains open unless a sharper argument closes the indeterminate post-\((3,5)\) states ([multi-step checker](../src/t2_reachability_code/multi_step_activation_safety.py)).

## Instance and rules used

The instance checked is \(n=10^{20}\), \(\delta=1/8\), \(Y=316\), \(P_Y\) equal to the 64 odd primes from 3 through 313, \(K_5=\{101,103,107,109,113\}\), and \(q=4806305873305829\) ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

The checker confirms that \(q\) is prime and lies in all ten \(K_5\) pair intervals for this instance ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

The safety rule used is Definition 4.5 and Proposition A.6 as summarized in the audit: after Maker plays a live activation edge, every modeled Breaker reply must leave the scaled potential \(Q\) at least as large as it was before Maker's move ([Buddhdev setup audit](buddhdev_setup_audit.md)).

The modeled Breaker replies are deletion of an uncaptured small-prime vertex or deletion of one currently live pair edge, matching the activation graph version described in Proposition A.6 ([Buddhdev setup audit](buddhdev_setup_audit.md)).

The activation potential is the same bookkeeping used in the first-move exclusion checker: unclaimed live pair edges carry coefficients \(1/8\), \(1/4\), or \(1/2\) according to captured endpoints, while claimed edges carry full weight and deleted edges carry zero ([full activation checker](../src/t2_reachability_code/full_activation_safety.py)).

## Search strategy

The new checker represents a state as captured vertices, claimed edges, deleted vertices, and deleted edges ([multi-step checker](../src/t2_reachability_code/multi_step_activation_safety.py)).

For each candidate Maker activation, the checker computes a lower bound for Maker's potential gain and an upper bound for the largest possible Breaker loss, and it certifies safety only when the lower gain is at least the upper loss ([multi-step checker](../src/t2_reachability_code/multi_step_activation_safety.py)).

The checker also records certifiable unsafety when Maker's upper gain is below Breaker's lower loss, but indeterminate moves are not treated as safe ([multi-step checker](../src/t2_reachability_code/multi_step_activation_safety.py)).

The search first tries a greedy certified Maker-only path, then runs a best-first certified Maker-only search with pruning over safe moves ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

The search is Maker-only in the sense that it tests safe Maker activations along a proposed ordering without committing any particular Breaker deletion to the next state, so a positive result would still need a separate adversarial strategy-tree interpretation ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

## Result

At the initial state, the checker finds 2016 live edges, only one certified safe move, and that move is \((3,5)\) ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

For \((3,5)\), the certified Maker gain lower bound is \(1.066196\times10^{17}\), the Breaker loss upper bound is \(1.028865\times10^{17}\), and the certified safety margin is \(3.733091\times10^{15}\) ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

All ten \(K_5\) moves are still massively uncertified at the initial state under the stronger safety direction, with worst upper-bound Breaker reply equal to deletion of vertex 3 in each case ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

After applying the only certified safe first move \((3,5)\), the greedy search finds no second certified safe move, so it stops with zero claimed \(K_5\) edges ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

The best-first certified search exhausts its frontier after two expansions, because the initial state has only one certified safe child and that child has no certified safe continuation ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

No state was reached where all ten \(K_5\) pair edges were certified safely activatable, and no sequence was found whose endpoint claims all ten \(K_5\) activations ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

## Meaning for the initial-state exclusion result

The initial-state exclusion remains valid: every \(K_5\) pair is unsafe as a first activation move by the earlier one-sided certificate against deletion of vertex 3 ([K5 activation exclusion argument](k5_activation_exclusion_argument.md)).

The new search does not upgrade that result to a structural multi-step exclusion proof, because the failure after \((3,5)\) is caused by conservative certification bounds rather than an exhaustive mathematical impossibility result ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

The practical takeaway is that the most natural neutralization attempt starts with \((3,5)\), but the current rigorous bounds do not certify any safe continuation from that state ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

## Adversarial caveat

Even the first certified Maker-only step \((3,5)\) leaves all five \(K_5\) vertices deletable and all ten \(K_5\) edges live, so it is not an adversarial strategy-tree certificate for eventually claiming the \(K_5\) clique ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).

Thus a future positive result must specify how the sequence is interpreted against actual modeled Breaker replies, or else provide a strategy tree rather than a single Maker-only ordering ([Buddhdev setup audit](buddhdev_setup_audit.md)).

## Limitations

This checker is bounded and heuristic, not exhaustive over all 2016 activation edges and all Breaker-reply branches ([multi-step checker](../src/t2_reachability_code/multi_step_activation_safety.py)).

The certification is deliberately conservative: safety requires lower-bound Maker gain to dominate upper-bound Breaker loss, so many truly safe moves may be left indeterminate ([multi-step checker](../src/t2_reachability_code/multi_step_activation_safety.py)).

The conclusion should be recorded as no counterexample found within budget, not as no counterexample exists ([multi-step checker output](../src/t2_reachability_code/multi_step_activation_safety.out)).
