# Multi-step exact-or-Dusart bounds findings

Outcome: **sharpened NEG within budget, with more certified safe moves but no K5 activation sequence found**.

## Bound backend

The new checker is `/home/user/workspace/erdos872/src/t2_reachability_code/multi_step_exact_bounds.py`, and its run output is `/home/user/workspace/erdos872/src/t2_reachability_code/multi_step_exact_bounds.out` ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The script attempted to use a local `primecount` executable for exact values of \(\pi(x)\), but no exact backend was available in this environment, so it used Dusart 2010 explicit bounds instead ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The Dusart fallback uses \(\pi(x)>x/(\log x-1)\) and \(\pi(x)<x/(\log x-1.1)\) in the large range relevant here, consistent with Dusart's 2010 prime-counting estimates ([Dusart arXiv record](https://arxiv.org/abs/1002.0442), [prime-counting function summary](https://en.wikipedia.org/wiki/Prime-counting_function)).

The interval model was kept identical to the existing activation bookkeeping, namely \(B_{a,c}=\{b\text{ prime}: n/(2ac)<b\le n/(ac)\}\), because this is the edge weight model used by the established single-move and multi-step checkers ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out), [full activation checker](../src/t2_reachability_code/full_activation_safety.py)).

## Weight interval effect

The new bounds cover all 2016 distinct pair intervals and use zero exact edge counts because no exact prime-counting backend was found ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The maximum relative interval-bound width under the Dusart backend is about \(9.27\times 10^{-3}\), which is far tighter than the old Rosser-Schoenfeld envelope used in the baseline multi-step checker ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out), [baseline multi-step checker](../src/t2_reachability_code/multi_step_activation_safety.py)).

For example, the interval for \((3,5)\) is bounded between \(7.721829\times 10^{16}\) and \(7.778360\times 10^{16}\), while the interval for \((101,103)\) is bounded between \(1.312059\times 10^{14}\) and \(1.323490\times 10^{14}\) ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

## Initial-state result

The tighter bounds change the initial-state search substantially: 64 moves certify safe initially instead of only one under the baseline Rosser-Schoenfeld checker ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out), [baseline output](../src/t2_reachability_code/multi_step_activation_safety.out)).

The best certified initial move under the ranking used by the new checker is \((3,101)\), with lower Maker gain \(6.461783\times 10^{16}\), upper Breaker loss \(5.035272\times 10^{16}\), and certified margin \(1.426511\times 10^{16}\) ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The old branch \((3,5)\) remains certified safe, but its margin improves to \(1.064121\times 10^{17}\) under the tighter bounds ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

All ten initial K5 moves remain certified unsafe by a large margin, and their worst upper-bound Breaker reply is still deletion of vertex 3 ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The least-bad initial K5 move under the new bounds is \((101,103)\), with margin \(-5.619969\times 10^{16}\), so the initial structural obstruction is unchanged in sign ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

## Multi-step search result

A second move does certify under the tighter bounds: the greedy prefix starts \((3,101),(5,103)\), and the best-first search extends to a 12-step certified Maker-only sequence within the configured budget ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The best-first sequence found claims no K5 edges, although it captures three K5 vertices as side effects through \((3,101),(5,103),(7,107)\) ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The best-first search stopped with status `NEG_NO_POS_WITHIN_BUDGET` after 216.39 seconds, 12 expansions, and 258 seen states, so it did not exhaust the tightened certified frontier ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

The best current diagnostic at the stopping state was \((5,7)\), still certified safe with margin \(1.578431\times 10^{15}\), which means the budget ended before the certified path was exhausted ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).

## Interpretation

The sharpening upgrades the old result from "only \((3,5)\) certifies and no second move certifies" to "many initial moves certify and multi-step certified play continues", but it does not produce a certified K5 activation path ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out), [baseline output](../src/t2_reachability_code/multi_step_activation_safety.out)).

This remains a Maker-only ordering search, not an adversarial strategy-tree proof, matching the caveat in the original multi-step checker ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out), [baseline findings](multi_step_activation_findings.md)).

Exact prime counts remain open for this run because no exact prime-counting backend was available, but the Dusart fallback makes the previous negative result materially sharper ([new checker output](../src/t2_reachability_code/multi_step_exact_bounds.out)).
