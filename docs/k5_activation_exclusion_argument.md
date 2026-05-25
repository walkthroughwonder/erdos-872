# K5 activation exclusion argument

Outcome: **NEG**.

The concrete K5 q-fiber witness cannot be upgraded to a full-graph safe activation certificate, because every K5 pair is unsafe as a first activation edge in the full activation graph ([full checker output](t2_reachability_code/full_activation_safety.out)).

## Failing pair and Shortener response

The least-bad K5 first move is \((101,103)\), but even this move fails: Maker's gain is at most \(1.224271\times10^{16}\), while Shortener can delete the still-uncaptured small-prime vertex 3 and remove at least \(4.369887\times10^{16}\) of activation potential ([full checker output](t2_reachability_code/full_activation_safety.out)).

The resulting certified decrease is at least \(3.145616\times10^{16}\), so Definition 4.5's requirement that every legal Breaker reply leave \(Q\) at least as large as before Maker's move is violated ([Buddhdev manuscript, p. 11, Definition 4.5](buddhdev_872.pdf), [full checker output](t2_reachability_code/full_activation_safety.out)).

The same vertex-3 reply excludes all ten possible K5 first moves, with certified loss-to-gain ratios ranging from 3.569379 to 3.872907 ([full checker output](t2_reachability_code/full_activation_safety.out)).

## Structural reason

The obstruction is not the arithmetic existence of the common token \(q\), since the checker confirms that \(q=4806305873305829\) lies in all ten K5 pair intervals ([full checker output](t2_reachability_code/full_activation_safety.out)).

The obstruction is the full activation graph: the star at the small prime 3 carries far more token potential than the potential gained by claiming any pair among \(101,103,107,109,113\) ([full checker output](t2_reachability_code/full_activation_safety.out)).

Since Proposition A.6 requires safety against modeled activation vertex deletions, and deleting vertex 3 is a legal modeled reply after any first K5-pair activation, no ordering can start with a safe K5 pair ([Buddhdev manuscript, pp. 40 to 41, Proposition A.6](buddhdev_872.pdf)).

Therefore an activation-phase play consisting of the ten K5 pair activations as safe full-graph choices does not exist for this concrete witness ([full checker output](t2_reachability_code/full_activation_safety.out)).
