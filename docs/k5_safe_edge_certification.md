# K5 safe-edge certification for the concrete T2 witness

Outcome: **NEG**.

At the concrete instance \(n=10^{20}\), \(\delta=1/8\), \(Y=316\), \(P_5=\{101,103,107,109,113\}\), and \(q=4806305873305829\), no activation-phase ordering can secure the ten K5 pairs as safe edges in the full activation graph, because every possible first K5 pair is already unsafe at the initial full activation state ([checker output](t2_reachability_code/full_activation_safety.out)).

## Manuscript rule used

Definition 4.5 says that in each finite graph or scored rank-three hypergraph state actually reached by the T2 activation strategy and residual construction, whenever a positive-weight live edge exists, Maker must have a legal live edge \(f\) such that after Maker plays \(f\), every legal Breaker reply leaves the scaled potential \(Q\) at least as large as it was before Maker's move ([Buddhdev manuscript, p. 11, Definition 4.5](buddhdev_872.pdf)).

Proposition A.3 makes the relevant Breaker replies explicit: vertex deletion, unscored edge deletion, and, only in the scored-hypergraph variant, scored-edge reply ([Buddhdev manuscript, pp. 38 to 39, Proposition A.3](buddhdev_872.pdf)).

Proposition A.6 specializes this to activation by forming a finite rank-2 graph game whose vertices are the small primes, whose live edges are unclaimed pairs \((a,c)\) with current token weight \(w_t(e)=|B_e(t)|>0\), and whose modeled Shortener replies are graph vertex deletions \(a\) or graph edge deletions \(ac\) ([Buddhdev manuscript, pp. 40 to 41, Proposition A.6](buddhdev_872.pdf)).

The activation potential used here is exactly Proposition A.6's potential
\[
Q_t=S_t+\sum_e \phi_t(e),
\]
where \(\phi_t(e)=\frac18w_t(e)\), \(\frac14w_t(e)\), or \(\frac12w_t(e)\) for unclaimed edges with 0, 1, or 2 captured endpoints, \(\phi_t(e)=w_t(e)\) for claimed edges, and \(\phi_t(e)=0\) for deleted edges ([Buddhdev manuscript, pp. 40 to 41, Proposition A.6](buddhdev_872.pdf)).

This is the activation-stage normalization, not the Appendix A rank-three normalization \(Q=8S+\sum 2^{|e\cap C|}w(e)\), although it is the same scaled argument divided by 8 in the graph activation bookkeeping ([Buddhdev manuscript, pp. 36 to 37, Auxiliary slot game and potential](buddhdev_872.pdf)).

## Full activation graph computed

The full activation graph for the concrete instance has \(P_Y\) equal to the 64 odd primes at most 316, from 3 through 313, and therefore has \(\binom{64}{2}=2016\) pair edges ([checker output](t2_reachability_code/full_activation_safety.out)).

For each pair \((a,c)\), the token set is \(B_{a,c}=P\cap(n/(2ac),n/(ac)]\), matching Appendix A.1's definition of \(I_{a,c}\) and \(B_{a,c}\) ([Buddhdev manuscript, p. 36, Appendix A.1](buddhdev_872.pdf)).

The checker verifies that all 2016 full-graph pair edges have positive token weight by a lower bound on \(|B_{a,c}|\), with the minimum lower bound \(1.068819\times 10^{13}\) ([checker output](t2_reachability_code/full_activation_safety.out)).

The checker also verifies that the witness prime \(q=4806305873305829\) is prime and lies in \(B_{a,c}\) for all ten K5 pairs ([checker output](t2_reachability_code/full_activation_safety.out)).

## Safety calculation

At the initial activation state, no small-prime vertex is captured and no pair edge is claimed or deleted, so the first edge in any proposed ordering of the ten K5 pair activations must itself be safe in the full graph ([Buddhdev manuscript, pp. 40 to 41, Proposition A.6](buddhdev_872.pdf)).

If Maker first claims a K5 pair \((a,c)\), the checker upper-bounds Maker's total potential gain by adding the claimed-edge gain \(\frac78w(a,c)\) and the coefficient-doubling gains \(rac18w(a,x)+\frac18w(c,x)\) over all other small primes \(x\in P_Y\setminus\{a,c\}\) ([checker source](t2_reachability_code/full_activation_safety.py)).

After that Maker move, vertex 3 is still uncaptured for every K5 pair, so Breaker may legally delete vertex 3 as a modeled activation graph vertex deletion ([Buddhdev manuscript, pp. 40 to 41, Proposition A.6](buddhdev_872.pdf)).

The checker lower-bounds the resulting potential loss by \(\frac14w(3,a)+\frac14w(3,c)+\sum_{x\in P_Y\setminus\{3,a,c\}}\frac18w(3,x)\), which is a lower bound for the live star potential at vertex 3 after Maker captures \((a,c)\) ([checker source](t2_reachability_code/full_activation_safety.py)).

The bounds are one-sided in the certifying direction: Maker gain is bounded above and Breaker loss is bounded below, so a positive lower-loss-minus-upper-gain margin proves unsafety without exact prime counts ([checker source](t2_reachability_code/full_activation_safety.py)).

The smallest certified margin among the ten K5 first moves is \(3.145616\times10^{16}\), occurring for pair \((101,103)\), where the Maker gain upper bound is \(1.224271\times10^{16}\) and the vertex-3 deletion loss lower bound is \(4.369887\times10^{16}\) ([checker output](t2_reachability_code/full_activation_safety.out)).

All ten K5 first moves have loss-to-gain ratios between 3.569379 and 3.872907 under this same certifying test ([checker output](t2_reachability_code/full_activation_safety.out)).

## Ordering conclusion

No ordering of the ten K5 pairs can satisfy the full-graph safe-edge requirement, because the first move of any such ordering is one of the ten K5 pairs and every one of those ten choices is unsafe at the initial full activation graph state ([checker output](t2_reachability_code/full_activation_safety.out)).

The structural reason is that the full activation graph contains the very high-weight star at the small prime 3, and claiming a pair among primes near 100 does not add enough potential to dominate Shortener's legal deletion of that star ([checker output](t2_reachability_code/full_activation_safety.out)).

## Verification and limitations

The main computation uses conservative Rosser-Schoenfeld style prime-count bounds for interval weights, so it does not rely on exact prime counting over intervals near \(10^{18}\) ([checker source](t2_reachability_code/full_activation_safety.py)).

As an independent sanity check of the potential algebra, the checker includes a reduced exact-count instance \(n=10^8\), \(Y=31\), and K5-like primes \((13,17,19,23,29)\), where exact prime enumeration gives the same kind of first-move failure against deletion of vertex 3 ([checker output](t2_reachability_code/full_activation_safety.out)).

The conclusion does not rule out other activation strategies that first secure small-prime pairs and only later attempt some of the K5 pairs, but it does answer the requested question negatively because the requested play requires the ten K5 pair activations to be the secured sequence under consideration and hence has a K5 pair as its first required safe edge ([checker output](t2_reachability_code/full_activation_safety.out)).
