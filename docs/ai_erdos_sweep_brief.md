# AI-Erdős Sweep Map: Brief for Problem #872 Work
*Research compiled June 2026 from the [AI-contributions-to-Erdős-problems wiki](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems), the [arXiv paper 2605.22763](https://arxiv.org/abs/2605.22763v1), and associated public sources.*

---

## Active Contributors

The wiki's section 1(d) ("AI collaborating with humans") lists every human credited alongside an AI system. The counts below are tallied directly from the raw markdown (634 lines, fetched June 2026).

| Rank | Name | Affiliation | Wiki rows (sect 1d) | Primary models used | Public contact |
|------|------|-------------|---------------------|---------------------|----------------|
| 1 | **Przemek Chojecki** | CEO, [ulam.ai](https://www.ulam.ai) (Warsaw); PhD mathematics Paris; postdoc Oxford | **32** | GPT-5.4 Pro, GPT-5.5 Pro, Aristotle | GitHub: [przchojecki](https://github.com/przchojecki), X: [@prz_chojecki](https://x.com/prz_chojecki), LinkedIn: [przchojecki](https://www.linkedin.com/in/przchojecki) |
| 2 | **Nat Sothanaphan** | Unknown affiliation; frequent wiki contributor | **12** | GPT-5.2 Thinking, GPT-5.4 Thinking, GPT-5.4 Pro, Aristotle, AlphaEvolve, AlphaProof | No public contact found |
| 3 | **Terence Tao** | UCLA, Fields Medal; maintains [erdosproblems.com](https://www.erdosproblems.com) | **11** | GPT-5.4 Pro, Aristotle, AlphaEvolve, AlphaProof, Gemini | MathOverflow, personal blog, GitHub: [teorth](https://github.com/teorth) |
| 4 | **Boon Suan Ho** | Unknown affiliation | **7** | GPT-5.4 Pro | No public contact found |
| 5 | **Quanyu Tang** | Unknown affiliation; co-author on [arXiv paper 2605.22763](https://arxiv.org/abs/2605.22763v1) (DeepMind) | **7** | GPT-5.2 Thinking, GPT-5.4 Thinking, GPT-5.5 Pro, AlphaProof | Listed in DeepMind AlphaProof Nexus paper |
| 6 | **David Turturean** | Unknown affiliation | **6** | GPT-5.4 Pro, GPT-5.5 Pro, Claude Code, Claude Opus 4.7 | No public contact found |
| 7 | **Wouter van Doorn** | Unknown affiliation; frequent Lean formalizer | **6** | Aristotle, GPT-5.4 Pro, AlphaProof | No public contact found |
| 8 | **Malek Zribi** | Unknown affiliation | **6** | Claude, GPT-5.4, GPT-5.5 Pro | No public contact found |
| 9 | **Ingo Althöfer** | Professor, Friedrich Schiller Universität Jena; combinatorial game theory | **5** | GPT-5.5, GPT-5.5 Pro, GPT-5.4 Pro | [Personal page](https://www.althofer.de) |
| 10 | **Boris Alexeev** | Research mathematician; contributor to [Xena project formalization post](https://xenaproject.wordpress.com/2025/12/05/formalization-of-erdos-problems/) | **5** | GPT-5.5, Aristotle, AlphaEvolve | Listed in arXiv 2605.22763 acknowledgments |

**Notes on counts.** These counts cover only the 1(d) (human-collaborative) section. Chojecki's true impact is broader: he has entries in sections 1(b) (AI alongside literature) and formalization rows, and his agentic-erdos system has tracked all 632 open problems. The wiki also credits him on at least 6 formalization rows (problems 1148, 1151, 603, etc.) where his prior solution was then formalized by Aristotle.

**Problem #872 specifically.** Two 1(d) rows exist for #872 as of the wiki snapshot:
- [Om_Buddhdev_sensho](https://www.erdosproblems.com/872) with GPT-5.4 Pro (16 Apr 2026): partial result (yellow).
- [Jonas Silva](https://www.erdosproblems.com/872) with GPT-5.5 Pro (29 Apr 2026): unverified candidate partial result (white circle).
- One standalone 1(a) row: GPT-5.2 Pro (16 Feb 2026): partial result (yellow).

---

## Methodology Pattern

### Evidence available

The clearest public methodology documentation comes from three sources:

**1. Chojecki / ulam.ai agentic sweep**

The [agentic-erdos GitHub repo](https://github.com/przchojecki/agentic-erdos) (32 stars, JavaScript, Vercel-deployed) runs a "parallel, agentic research loop over the full open Erdős problem set." It tracks all 632 open problems as individual `epNNN.json` + `epNNN.md` + `epNNN.mjs` file triples. The workflow is:
- Feed each problem to an LLM (GPT-4/5 series, primarily GPT-5.4 Pro then GPT-5.5 Pro as models were released).
- Record computational evidence (branch-and-bound, randomized search) in the JSON file.
- Record proof attempts in the markdown notes.
- Revisit problems "with deeper computations or stronger arguments as new signals appear."
- Deploy a browseable problem browser at [agentic-erdos.vercel.app](https://agentic-erdos.vercel.app/).

This is operator-in-the-loop: Chojecki reads outputs, judges partial vs. full, and submits to the wiki with his name attached. He is not fully autonomous. He submitted entries across all numbered ranges (25, 342, 460, 503, 514, 598, 603, 610, 750, 852, 856, 858, 888, 896, 906, 953, 956, 1092, 1133, 1143, 1148, 1151, 1183, 1190, 1201, etc.).

The [ulam.ai data page](https://www.ulam.ai/data) shows the commercial arm: 1,000+ research-level trajectories (Erdős-style + arXiv problems) with Proof Verification Units (PVUs), dependency-gated rewards, and negative traces, sold as RLVR training data. The public [HuggingFace dataset](https://huggingface.co/datasets/ulamai/verified-research-reasoning-trajectories) includes sample trajectories for problems #258 and #1201.

**2. DeepMind AlphaProof Nexus (formal, institutional)**

The [arXiv paper 2605.22763](https://arxiv.org/abs/2605.22763v1) (Tsoukalas, Kovsharov, Shirobokov et al., DeepMind, May 2026) is the most detailed public methodology description. It solved 9 of 353 formalized Erdős problems. Key architecture:
- Agent A ("Ralph loop"): multi-turn Gemini 3.1 Pro, search-and-replace edits to a Lean proof sketch, Lean compilation feedback after each turn.
- Agent B: Agent A + AlphaProof to fill missing proof parts.
- Agent C (evolutionary): maintains a population of sketches rated by Gemini 3.0 Flash using Elo scores and P-UCB sampling (inspired by AlphaEvolve).
- Agent D: full combination. 100 independent attempts per problem (Agents A/B) or 10 subagents × 10 attempts (Agents C/D).
- Cost: "a few hundred dollars" per solved problem.
- Problem selection: all 353 problems that had been formalized in Lean by the open-source community as of February 2026 (no cherry-picking; bias toward formalizable problems).
- Code and Lean outputs: [github.com/google-deepmind/alphaproof-nexus-results](https://github.com/google-deepmind/alphaproof-nexus-results).

**3. Individual contributors (no formal methodology writeup found)**

Contributors like Nat Sothanaphan, Boon Suan Ho, Vjekoslav Kovač, and Aron Bhalla appear to work independently, prompting GPT-5.4/5.5 Pro on individual problems. No public harness or repo from these contributors has been found. Their wiki entries span a mix of low-numbered (12, 25, 138, 396, 423) and higher-numbered (684, 749, 873, 976, 1196) problems, suggesting opportunistic selection rather than a systematic sweep.

**4. Tim Gowers / Isaac Rajagopal (documented in blog post)**

Gowers's [May 2026 blog post](https://gowers.wordpress.com/2026/05/08/a-recent-experience-with-chatgpt-5-5-pro/) documents a specific session: a single extended prompt to GPT-5.5 Pro (17 min 5 sec thinking time), followed by manual LaTeX writeup, followed by expert peer review (Rajagopal). This is deeply operator-in-the-loop, not automated.

### Problem selection patterns

From a count of all 1(d) entries by problem number:
- No strong bias toward low-numbered problems. Chojecki alone spans problems #25 through #1201.
- Cluster around 400-600 range (Chojecki's April 2026 burst: 415, 460, 488, 503, 514, 598, 603, 610).
- Cluster around 850-906 (Chojecki: 852, 856, 858, 888, 896, 906) in same April-May burst.
- High-activity problems: #52, #90, #347, #686, #848, #1026, #1153 have 4-10 contributors each, suggesting community convergence on tractable or famous problems.

### Signs of coordination

- No public Discord or mailing list found.
- The [erdosproblems.com forum](https://www.erdosproblems.com/forum/) exists and is the recommended channel for discussion (threads visible per problem).
- Chojecki's agentic-erdos repo accepts PRs and lists a contribution workflow, but has only 1 fork and 32 stars.
- The DeepMind team coordinated internally; their results feed into the wiki retroactively.
- Multiple contributors (Chojecki, Tao, Alexeev, van Doorn) appear together on single problems (#347, #1026, #1153), suggesting loose ad-hoc collaboration through the wiki and forum rather than a formal coordinating organization.
- Tao himself participates actively in section 1(d) on 11 problems, acting as both a contributor and wiki organizer.

---

## Tooling Stack

### LLM backbones (by wiki row count)

| Model | Row count (all wiki sections) | Notes |
|-------|------------------------------|-------|
| Aristotle (Harmonic) | 187 | Dominant formalization engine; produces verified Lean 4 proofs |
| GPT-5.5 Pro | 65 | Primary reasoning model for human-collaborative entries |
| GPT-5.4 Pro | 50 | Earlier wave; most of Chojecki's April entries |
| GPT-5.5 | 14 | Non-Pro version |
| Aletheia (Google DeepMind/Gemini 3 Deep Think) | 14 | Google's research agent; solved 4 Erdős problems autonomously plus 63 with human guidance across 700 problems tested |
| GPT-5.2 Pro / Thinking variants | ~30 combined (counted in script) | Earlier wave |
| Gemini 3.1 Pro | Used in AlphaProof Nexus (DeepMind) and by individual contributors | |
| Claude Opus 4.5-4.8 | Multiple formalization rows | Mainly for Lean formalization |
| AlphaEvolve | 9 | Population-based construction search |
| AlphaProof | 5 | Lean proof search (DeepMind) |
| Aleph Prover | 3 | Formalization; appeared on #90 (OpenAI result) and #1067, #1071 |
| Codex | Multiple rows | Lean code generation |

### Provers

| Prover | Role |
|--------|------|
| **Aristotle** (Harmonic) | LLM + Lean 4 proof search; formally verified output. Architecture: informal reasoning LLM + Lean proof search + geometry solver. Reached IMO gold-medal level (2025). Key formalization workhorse for the wiki. [nextomoro.com/aristotle](https://nextomoro.com/aristotle/) |
| **AlphaProof** (DeepMind) | Lean-based proof search; component of AlphaProof Nexus. Runs in "low-compute tree search inference mode." |
| **Lean 4** | Underlying formal language; version v4.27 used in AlphaProof Nexus. |
| **Aleph Prover** | Used for formalization of #90, #1067, #1071; provenance unclear beyond wiki mentions. |
| **Seed Prover 1.5** | Used by DeepMind-adjacent contributors on #379, #493, #958. |
| **UlamAI Prover** | Chojecki's in-house Lean prover ([github.com/ulamai/ulamai](https://github.com/ulamai/ulamai)); open source. |
| **Gauss** | Appeared once for formalization of #1196; minimal wiki context. |
| **Numina Lean Agent / Project Numina** | Used for formalization of #93, #433. |

### Search and exploration

| Tool | Role |
|------|------|
| **AlphaEvolve** | Population-based evolutionary search for constructions (problems #36, #507, #1097, #651, #1026, #1038, #1132, #1153). Inspired Agent C in AlphaProof Nexus. |
| **ChatGPT Deep Research** | Literature search (section 2a); used on ~20 problems. |
| **Gemini Deep Research** | Literature search; used in parallel with ChatGPT Deep Research. |
| **agentic-erdos** (Chojecki) | Parallel problem tracker with per-problem data + note + script files; deployed at [agentic-erdos.vercel.app](https://agentic-erdos.vercel.app/). Covers all 632 open problems. |
| **Mehmet Mars Seven's LLM hunter** | [mehmetmars7.github.io/Erdosproblems-llm-hunter/erdos.html](https://mehmetmars7.github.io/Erdosproblems-llm-hunter/erdos.html); independent tracking page. |
| **Neel Somani's tracker** | [ocf.berkeley.edu/~neel/erdos.html](https://www.ocf.berkeley.edu/~neel/erdos.html); independent tracking page. |

### Orchestration

- **No single shared orchestration harness has been made public.** The sweep is decentralized.
- Chojecki's agentic-erdos is the closest to a shared harness (JavaScript, Vercel, per-problem files), but it is his own system and has minimal external contributors.
- DeepMind AlphaProof Nexus is an institutional system with full Python/asyncio orchestration, Docker sandboxes, and a global goal cache; its code is partially available via [alphaproof-nexus-results](https://github.com/google-deepmind/alphaproof-nexus-results) (outputs only, not the runner).
- The dominant informal pattern for individual contributors is: single-session GPT-5.5 Pro prompt (with extended thinking), manual verification, then wiki submission.

---

## How to Engage

### Best single contributor to reach out to

**Przemek Chojecki** is the most tractable contact. He has 32 wiki rows (more than any other individual), runs an open public repo and website specifically for this work, is active on X ([@prz_chojecki](https://x.com/prz_chojecki)) and LinkedIn, and has stated publicly that he gives talks on his methodology. He is building a commercial dataset (ulam.ai) from Erdős problem trajectories and has structural incentive to document and share methodology. For problem #872 specifically: he has not yet worked on it (no wiki entry under his name), making him a natural collaborator rather than a competitor.

**Second option:** Nat Sothanaphan (12 rows, second most active individual) works on a wide range of problems including many that overlap in character with #872, but has no known public contact.

### Best forum / issue tracker to participate in

1. **[erdosproblems.com forum, problem #872 thread](https://www.erdosproblems.com/forum/thread/872)** - the canonical community space for this specific problem. Every problem has a dedicated thread. This is where Jonas Silva and Om_Buddhdev_sensho's partial results would naturally be discussed.

2. **[teorth/erdosproblems GitHub issues](https://github.com/teorth/erdosproblems/issues)** - for meta-discussion about the wiki structure, problem formulations, or requesting a Lean formalization of a result.

3. **[przchojecki/agentic-erdos GitHub PRs](https://github.com/przchojecki/agentic-erdos/pulls)** - if contributing a computation or proof attempt to Chojecki's tracker. His repo has a clear PR workflow and accepts per-problem additions.

4. **X / Twitter with hashtag** - no dominant community hashtag has emerged yet. Posts by Tao, Chojecki, and others go under no single tag. Following [@prz_chojecki](https://x.com/prz_chojecki), [@tao_math](https://x.com/tao_math) (Tao's handle), and tagging [erdosproblems.com](https://www.erdosproblems.com) reaches the active participants. Scott Aaronson's [Shtetl-Optimized](https://scottaaronson.blog/?p=9782) has also covered this wave.

### For problem #872 specifically: recommended path

The official guidance from the wiki's [submission FAQ](https://github.com/teorth/erdosproblems/wiki/What-to-do-when-I-think-I-managed-to-get-AI-to-solve-an-Erd%C5%91s-problems%3F) is:

**(a) Submit a wiki PR to Tao's repo** - yes, this is the correct final step once the work meets the checklist (understanding key ideas, literature review done, professional writeup exists).

**(b) Raise as a GitHub issue on teorth/erdosproblems** - useful if you want to flag an existing wiki entry as incorrect or request a Lean formalization, but not the primary submission channel.

**(c) Email a specific person** - not recommended as a first step; the wiki FAQ says to be "respectful of expert time." If Tao or Chojecki is already engaged via (d) or (a), follow-on email is reasonable.

**(d) Post on erdosproblems.com forum** - yes, this is the recommended community vetting step before a wiki PR. Post a summary with a link to your writeup on [the #872 forum thread](https://www.erdosproblems.com/forum/thread/872). The wiki FAQ explicitly says: "After due diligence, announce your solution with relevant links and summaries to the Erdős problem page."

**(e) Share on X with a specific hashtag** - secondary; useful for visibility but not for evaluation. Tag [@prz_chojecki](https://x.com/prz_chojecki) and [@tao_math](https://x.com/tao_math) directly for fastest community response.

**Recommended sequence for #872:** (1) Post on [erdosproblems.com/forum/thread/872](https://www.erdosproblems.com/forum/thread/872) with a writeup link. (2) If response is positive and a Lean formalization is possible, open a wiki PR on [teorth/erdosproblems](https://github.com/teorth/erdosproblems). (3) Optionally, reach out to Chojecki via X or LinkedIn since he has not yet engaged with #872 and may want to include it in his trajectory dataset.

---

## Open Questions

1. **What LLM-specific prompting strategy works best for game-combinatorics problems like #872?** The sweep entries for #872 show only GPT-5.2 Pro (standalone partial, Feb 2026) and GPT-5.5 Pro (human-collaborative candidate partial, Apr 2026). Neither entry has a public writeup or Lean certificate. It is unclear whether the #872 partial results use a different prompting approach than the successful full solutions in comparable combinatorial problems (e.g., #205, #457, #728) where Aristotle + GPT-5.2 Thinking succeeded. The community on [the forum thread](https://www.erdosproblems.com/forum/thread/872) would be the right place to ask.

2. **Is Aletheia (Google's research agent) accessible outside Google, and did it attempt #872?** Aletheia has 14 wiki rows but is described as powered by Gemini 3 Deep Think and available only through "Google AI Ultra + API Early Access." It was tested on 700 Erdős problems and generated 200 candidate answers. It is unclear whether #872 was in that set and whether those results are public. Asking on the forum or via Google's research blog ([the Pasquale Pillitteri breakdown](https://pasqualepillitteri.it/en/news/286/gemini-3-deep-think-aletheia-benchmarks-discoveries)) may clarify access.

3. **Is there a shared Lean formalization of the #872 problem statement?** The DeepMind AlphaProof Nexus paper solved only problems that had been pre-formalized in Lean by the open-source community (353 of 1200+ problems). If #872 lacks a Lean statement in the [formal-conjectures repo](https://github.com/google-deepmind/formal-conjectures), it is invisible to the most powerful automated provers. Checking the formal-conjectures repo and, if absent, contributing a Lean statement would make #872 available to AlphaProof Nexus, Aristotle, and other formal systems in future sweeps.

---

## Appendix: Raw Model Count in Wiki

From parsing the full 634-line wiki markdown (all sections):

| Model | Row count |
|-------|-----------|
| Aristotle | 187 |
| GPT-5.5 Pro | 65 |
| GPT-5.4 Pro | 50 |
| Aletheia | 14 |
| GPT-5.5 | 14 |
| AlphaEvolve | 9 |
| AlphaProof | 5 |
| Aleph Prover | 3 |

*Note: GPT-5.2 Pro, GPT-5.2 Thinking, GPT-5.4 Thinking, Gemini variants, Claude variants, and Codex each have additional counts not extracted by the targeted-model pattern above. "Aristotle" dominates because it is used as a formalization engine across all sections, not only for primary proof discovery.*

---

*Sources: [AI-contributions wiki raw markdown](https://raw.githubusercontent.com/wiki/teorth/erdosproblems/AI-contributions-to-Erd%C5%91s-problems.md) (fetched June 2026); [arXiv 2605.22763](https://arxiv.org/abs/2605.22763v1); [Gowers blog](https://gowers.wordpress.com/2026/05/08/a-recent-experience-with-chatgpt-5-5-pro/); [agentic-erdos repo](https://github.com/przchojecki/agentic-erdos); [ulam.ai data](https://www.ulam.ai/data); [HuggingFace ulamai dataset](https://huggingface.co/datasets/ulamai/verified-research-reasoning-trajectories); [wiki submission FAQ](https://github.com/teorth/erdosproblems/wiki/What-to-do-when-I-think-I-managed-to-get-AI-to-solve-an-Erd%C5%91s-problems%3F); [Aristotle description](https://nextomoro.com/aristotle/); [Aletheia description](https://pasqualepillitteri.it/en/news/286/gemini-3-deep-think-aletheia-benchmarks-discoveries); [OpenAI unit-distance announcement](https://openai.com/index/model-disproves-discrete-geometry-conjecture/); [Scott Aaronson coverage](https://scottaaronson.blog/?p=9782); [alphaproof-nexus-results](https://github.com/google-deepmind/alphaproof-nexus-results); [Przemek Chojecki LinkedIn](https://www.linkedin.com/in/przchojecki).*
