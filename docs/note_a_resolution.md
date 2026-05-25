# Note A resolution: ordinary capture removes edge from live

## Question

Does an ordinary edge capture by Maker remove the edge from the "live" set in Buddhdev's Appendix A.1 game?

## Answer

Yes, unambiguously. Two manuscript passages settle it.

## Manuscript evidence

### Capture rule (Buddhdev manuscript, Appendix A.1, p. 36)

Line 2118-2121 of the OCR text states:

> "An edge is live if it is not in D_E ∪ K and contains no deleted vertex. Maker may capture a live edge, adding its vertices to C and adding its weight to S; in the scored hypergraph variant, Maker may instead use an alternate-scoring move to score the target without adding slot vertices to C."

The wording "adding its weight to S" makes the captured edge equivalent in score accounting to a scored-edge addition to K. The phrase "live if it is not in D_E ∪ K" then implies the captured edge is no longer live after capture, because adding weight to S without putting the edge anywhere would leave Q double-counting.

### Confirmation in Proposition A.2's K_4 example (Buddhdev manuscript, p. 37-38)

Buddhdev's own worked example confirms the convention:

> "If Maker plays e_{17,19}, by ordinary capture or by alternate scoring, then the change in Q is +8·1 - 8 = 0, because S increases by 1, the edge of potential 8 is removed, and no new vertex is added to C."

"The edge of potential 8 is removed" is explicit: ordinary capture removes the edge from the live sum in Q. This appears in the manuscript's own analysis of the same game we are studying.

## Implication for v4 code

The v4 reproducer (src/v4_k5_bad_path.py) treats captured edges as removed from the live sum (via a "captured" set added to K). This matches the manuscript.

## Conclusion

Remove the Note A clarification from the Buddhdev outreach email. The convention is stated by the manuscript and confirmed by A.2's worked example.
