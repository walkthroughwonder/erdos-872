This AI Wiki collects contributions of AI systems to the understanding of Erdős problems.

If you are interested in getting started with using AI for research mathematics, we have some [free advice](https://github.com/teorth/erdosproblems/wiki/Getting-started-with-using-AI-for-research-mathematics).

If you are looking for famous solutions, we have information on some [notable cases](https://github.com/teorth/erdosproblems/wiki/Notable-cases-of-AI-contributions-to-Erd%C5%91s-problems).

## Introduction

### Color indicators

* 🟢: *Full* resolution.
* 🟡: *Partial* progress.
* 🔴: *Incorrect* work.
* ⚪: Unverified.

### Section placement

Full details are [found here](https://github.com/teorth/erdosproblems/wiki/AI-contribution-section-placement-system).

* [1. Primary contributions](#sect-1)

  - [1(a). AI standalone](#sect-1a)

  - [1(b). AI alongside literature](#sect-1b)

  - [1(c). AI building on literature](#sect-1c)

  - [1(d). AI collaborating with humans](#sect-1d)

* [2. Secondary contributions](#sect-2)

  - [2(a). Literature search](#sect-2a)

  - [2(b). Formalization](#sect-2b)

  - [2(c). Rewriting](#sect-2c)

  - [2(d). Computation](#sect-2d)

### Disclaimers

We have collected some [disclaimers](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats):

1. [This page is not a benchmark](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-1)
2. [Many problems on the site lack a thorough literature review](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-2)
3. [Keep selection bias in mind when drawing conclusions about success rates of AI systems](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-3)
4. [In some cases, Erdős himself or the problem site stated the problem incorrectly](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-4)
5. [Absence of past progress may reflect obscurity rather than difficulty](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-5)
6. [Contributions should be evaluated holistically](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-6)
7. [A solution to an Erdős problem does not automatically qualify as publishable paper in a journal](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-7)
8. [We encourage formalizations of AI proofs in a formal language such as Lean](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-8)
9. [This wiki is only a superficial reference and is not definitive verdict or assessment](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-9)
10. [The information provided on this wiki is provisional rather than final](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-10)
11. [Problem solving is only one component of mathematical research](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats#disclaimer-11)

### Frequently asked questions

* [How have AI companies been invested in Erdős problems?](https://github.com/teorth/erdosproblems/wiki/How-have-AI-companies-been-invested-in-Erd%C5%91s-problems%3F)
* [What to do when I think I managed to get AI to solve an Erdős problem?](https://github.com/teorth/erdosproblems/wiki/What-to-do-when-I-think-I-managed-to-get-AI-to-solve-an-Erd%C5%91s-problem%3F)

### External links

Sorted by the author's last name alphabetically.

* [Blog post "Formalization of Erdős problems"](https://xenaproject.wordpress.com/2025/12/05/formalization-of-erdos-problems/) by Boris Alexeev, 5 Dec, 2025.
* [Webpage](https://agentic-erdos.vercel.app/) by Przemek Chojecki, collecting AI attempts on Erdős problems.
* [Webpage](https://mehmetmars7.github.io/Erdosproblems-llm-hunter/erdos.html) by Mehmet Mars Seven, collecting AI attempts on Erdős problems.
* [Webpage](https://www.ocf.berkeley.edu/~neel/erdos.html) by Neel Somani, collecting AI attempts on Erdős problems.

<a id="sect-1"></a>
## 1. Primary contributions

**Notice. Sections 1(a)-1(d) are equally important. We do not intend section 1(a) to be more important than other sections.**

<a id="sect-1a"></a>
### 1(a). AI standalone

*Literature presence*: comparable literature unknown.<br>
*Human involvement*: non-significant.

| Problem | AI systems | Date | Outcome |
| ------- | ---------- | ---- | ------- |
| [[11]](https://www.erdosproblems.com/11) | Aristotle, GPT | 24 Jan, 2026 | 🔴 Incorrect claim made
| [[38]](https://www.erdosproblems.com/38) | GPT-5.5 Pro | 25 Apr, 2026 | 🟢 Full solution
| [[42]](https://www.erdosproblems.com/42) | Codex, GPT-5.2, GPT-5.2 Pro | 19 Jan, 2026 | 🟡 Partial result (Lean)
| [[51]](https://www.erdosproblems.com/51) | ChatGPT free version | 11 Jan, 2026 | 🔴 Incorrect proof found
| [[52]](https://www.erdosproblems.com/52) | Claude Mythos | 3 Jun, 2026 | 🟡 Solution to variant problem
| [[75]](https://www.erdosproblems.com/75) | Aletheia | 1 Feb, 2026 | 🟡 Solution to variant problem (implicit in literature)
| [[90]](https://www.erdosproblems.com/90) | OpenAI internal model | 20 May, 2026 | 🟢 Full solution
| [[90]](https://www.erdosproblems.com/90) | Claude Mythos | 26 May, 2026 | 🟢 Full solution
| [[124]](https://www.erdosproblems.com/124) | Aristotle | 29 Nov, 2025 | 🟡 Partial result (Lean)
| [[125]](https://www.erdosproblems.com/125) | DeepMind prover agent | 21 Feb, 2026 | 🟡 Solution to variant problem (Lean)
| [[125]](https://www.erdosproblems.com/125) | DeepMind prover agent | 30 Mar, 2026 | 🟢 Full solution (Lean)
| [[138]](https://www.erdosproblems.com/138) | DeepMind prover agent | 10 Apr, 2026 | 🟡 Partial result (Lean)
| [[176]](https://www.erdosproblems.com/176) | Codex, GPT-5.5 Pro | 23 Jun, 2026 | ⚪ Candidate partial result (Lean)
| [[205]](https://www.erdosproblems.com/205) | Aristotle, GPT-5.2 Thinking | 10 Jan, 2026 | 🟢 Full solution (Lean)
| [[233]](https://www.erdosproblems.com/233) | GPT-5.2 Pro | 18 Jan, 2026 | 🔴 Incorrect (conditional) proof found
| [[251]](https://www.erdosproblems.com/251) | GPT-5.4 Pro | 15 Apr, 2026 | 🟡 Solution to variant problem
| [[263]](https://www.erdosproblems.com/263) | Aristotle, Claude Opus 4.7, GPT-5.5 Pro | 9 May, 2026 | 🟡 Partial result (Lean) (solution to second part)
| [[358]](https://www.erdosproblems.com/358) | GPT-5.2 Pro | 11 Feb, 2026 | 🔴 Argument with major gaps made
| [[457]](https://www.erdosproblems.com/457) | Aristotle, GPT-5.2 Pro | 2 Mar, 2026 | 🟢 Full solution (Lean)
| [[477]](https://www.erdosproblems.com/477) | AlphaProof | 7 Jan, 2026 | 🟡 Solution to variant problem (Lean)
| [[536]](https://www.erdosproblems.com/536) | Codex, GPT-5.5 Pro | 22 Jun, 2026 | 🟡 Partial result (Lean)
| [[539]](https://www.erdosproblems.com/539) | Codex, GPT-5.5, ProofCouncil | 10 Jun, 2026 | 🟡 Partial result (Lean)
| [[550]](https://www.erdosproblems.com/550) | GPT | 22 Jun, 2026 | ⚪ Candidate full solution
| [[616]](https://www.erdosproblems.com/616) | Claude Sonnet 4.5, Gemini 3 Pro, GPT-5.2 Pro | 18 Jan, 2026 | 🔴 Incorrect proof found
| [[619]](https://www.erdosproblems.com/619) | Claude Fable 5, Codex, GPT-5.5 | 9 Jun, 2026 | 🟢 Full solution (Lean)
| [[647]](https://www.erdosproblems.com/647) | ChatGPT Deep research, DeepSeek DeepThink, Gemini  | 28 Jan, 2026 | 🔴 Incorrect proof found
| [[654]](https://www.erdosproblems.com/654) | Aletheia | 1 Feb, 2026 | 🟡 Partial result
| [[671]](https://www.erdosproblems.com/671) | Codex, GPT-5.5 Pro | 22 Jun, 2026 | ⚪ Candidate full solution (Lean)
| [[684]](https://www.erdosproblems.com/684) | OpenAI internal model | 31 Mar, 2026 | 🟡 Partial result
| [[694]](https://www.erdosproblems.com/694) | GPT-5.5 Pro | 1 May, 2026 | 🟢 Full solution
| [[730]](https://www.erdosproblems.com/730) | GPT-5.5 Pro | 24 Jun, 2026 | ⚪ Candidate full solution
| [[741]](https://www.erdosproblems.com/741) | DeepMind prover agent | 31 Mar, 2026 | 🟡 Partial result (Lean) (solution to variant of first part; solution to second part)
| [[741]](https://www.erdosproblems.com/741) | OpenAI internal model | 31 Mar, 2026 | 🟡 Partial result (solution to second part)
| [[741]](https://www.erdosproblems.com/741) | DeepMind prover agent | 16 Apr, 2026 | 🟢 Full solution (Lean)
| [[783]](https://www.erdosproblems.com/783) | GPT-5.2 | 23 Jan, 2026 | 🟡 Partial result
| [[836]](https://www.erdosproblems.com/836) | GPT-5.5 Pro | 27 Apr, 2026 | ⚪ Candidate partial result (solution to second part)
| [[872]](https://www.erdosproblems.com/872) | GPT-5.2 Pro | 16 Feb, 2026 | 🟡 Partial result
| [[888]](https://www.erdosproblems.com/888) | Claude Opus 4.5, Gemini 3 Pro, GPT-5.2 Thinking | 18 Jan, 2026 | 🔴 Incorrect proof found
| [[949]](https://www.erdosproblems.com/949) | AlphaProof | 7 Jan, 2026 | 🟡 Solution to variant problem (Lean)
| [[951]](https://www.erdosproblems.com/951) | GPT-5.2 Pro | 27 Jan, 2026 | 🟡 Solution to variant problem
| [[960]](https://www.erdosproblems.com/960) | OpenAI internal model | 9 Apr, 2026 | 🟢 Full solution
| [[963]](https://www.erdosproblems.com/963) | Gemini 3 Pro | 22 Jan, 2026  | 🔴 Argument with major gaps made
| [[987]](https://www.erdosproblems.com/987) | OpenAI internal model | 9 Apr, 2026 | 🟢 Full solution
| [[990]](https://www.erdosproblems.com/990) | OpenAI internal model | 9 Apr, 2026 | 🟢 Full solution
| [[1014]](https://www.erdosproblems.com/1014) | OpenAI internal model | 23 Apr, 2026 | 🟢 Full solution
| [[1039]](https://www.erdosproblems.com/1039) | GPT-5.5 Pro | 7 May, 2026 | 🟡 Partial result
| [[1040]](https://www.erdosproblems.com/1040) | Aletheia | 1 Feb, 2026 | 🟡 Solution to one part of problem; 🔴 incorrect solution to other part
| [[1041]](https://www.erdosproblems.com/1041) | GPT-5.4 Thinking | 22 Apr, 2026 | 🔴 Argument with major gaps made
| [[1044]](https://www.erdosproblems.com/1044) | GPT-5.2 Pro | 5 Jan, 2026  | 🔴 Incorrect claim made
| [[1051]](https://www.erdosproblems.com/1051) | Aletheia | 29 Jan, 2026 | 🟢 Full solution (Lean)
| [[1054]](https://www.erdosproblems.com/1054) | Claude Opus 4.8, GPT-5.5 Pro, Principia Math | 22-23 Jun, 2026 | 🟡 Partial result (Lean)
| [[1091]](https://www.erdosproblems.com/1091) | OpenAI internal model | 9 Apr, 2026 | 🟢 Full solution
| [[1101]](https://www.erdosproblems.com/1101) | GPT-5.5 Pro | 27 Apr, 2026 | ⚪ Candidate partial result (solution to second part)
| [[1131]](https://www.erdosproblems.com/1131) | GPT-5.5 Pro | 26 Apr, 2026 | ⚪ Candidate partial result
| [[1141]](https://www.erdosproblems.com/1141) | OpenAI internal model | 9 Apr, 2026 | 🟢 Full solution
| [[1194]](https://www.erdosproblems.com/1194) | GPT-5.4 Pro | 23 Apr, 2026 | 🟡 Partial result
| [[1196]](https://www.erdosproblems.com/1196) | GPT-5.4 Pro | 13 Apr, 2026 | 🟢 Full solution
| [[1202]](https://www.erdosproblems.com/1202) | GPT-5.4 Pro | 1 Apr, 2026 | 🟢 Full solution
| [[1217]](https://www.erdosproblems.com/1217) | GPT-5.4 Pro | 16 Apr, 2026 | 🟢 Full solution

<a id="sect-1b"></a>
### 1(b). AI alongside literature

*Literature presence*: comparable literature discovered *afterwards*.<br>
*Human involvement*: non-significant.

| Problem | AI systems | Date | Outcome | Literature | Literature found on | Similar? |
| ------- | ---------- | ---- | ------- | ---------- | ------------------- | -------- |
| [[120]](https://www.erdosproblems.com/120) | DeepMind prover agent | 14 Mar, 2026 | 🟡 Solution to variant problem (Lean) | 🟡 de Reyna (1983) | 14 Mar, 2026 | No
| [[152]](https://www.erdosproblems.com/152) | DeepMind prover agent | 3 Apr, 2026 | 🟢 Full solution (Lean) | 🟡 Erdős, Sárközy, and Sós (1994) | 3 Apr, 2026 | Yes
| [[176]](https://www.erdosproblems.com/176) | Codex, GPT-5.5 Pro | 21 Jun, 2026 | 🟡 Partial result (Lean) | 🟡 Hunter (2026) | 21 Jun, 2026 | Yes
| [[218]](https://www.erdosproblems.com/218) | GPT | 28 Jan, 2026 | 🟡 Conditional solution | 🟡 Banks (2023) | 28 Jan, 2026 | Yes
| [[281]](https://www.erdosproblems.com/281) | GPT-5.2 Pro | 17 Jan, 2026 | 🟢 Full solution | 🟢 Davenport and Erdős (1936) + Rogers (in Halberstam-Roth (1966)) | 18 Jan, 2026 | No
| [[333]](https://www.erdosproblems.com/333) | Claude Opus 4.5, GPT-5.2 Pro | 25 Dec, 2025 | 🟢 Full solution (Lean) | 🟢 Erdős and Newman (1977) | 25 Dec, 2025 | Yes
| [[346]](https://www.erdosproblems.com/346) | Codex, GPT-5.5 Pro | 19 Jun, 2026 | 🟡 Solution to variant problem (Lean) | 🟡 Burr and Erdős (1981) | 20 Jun, 2026 | Yes
| [[366]](https://www.erdosproblems.com/366) | Automated research pipeline | 14 Apr, 2026 | 🟡 Conditional partial result | 🟡 Aktaş and Murty (2017) | 15 Apr, 2026 | Yes
| [[397]](https://www.erdosproblems.com/397) | Aristotle, GPT-5.2 Pro | 10 Jan, 2026 | 🟢 Full solution (Lean) | 🟢 China TST competition (2012) | 14 Jan, 2026 | Yes
| [[397]](https://www.erdosproblems.com/397) | Aletheia | 2 Feb, 2026 | 🟢 Full solution | 🟢 China TST competition (2012) | 2 Feb, 2026 | Yes
| [[543]](https://www.erdosproblems.com/543) | GPT-5.2 Pro | 21 Jan, 2026 | 🟢 Full solution | 🟡 Erdős and Hall (1977) | 26 Jan, 2026 | Yes
| [[629]](https://www.erdosproblems.com/629) | Gemini 3.1 Pro, GPT-5.4 Thinking | 4 Apr, 2026 | 🟡 Partial result | 🟡 Erdős (1964) + Erdős, Rubin, and Taylor (1980) | 4 Apr, 2026 | Yes
| [[635]](https://www.erdosproblems.com/635) | Aristotle, GPT-5.2 Pro | 30 Jan, 2026 | 🟡 Solution to one part of problem (Lean) | 🟡 Elliott (1979) (reduces one part of problem to a much simpler one) | 30 Jan, 2026 | Yes (for a large portion of the proof)
| [[650]](https://www.erdosproblems.com/650) | GPT-5.4 Pro | 6-7 Mar, 2026 | 🟢 Full solution (stronger than literature) | 🟢 Erdős and Selfridge (1978) | 7 Mar, 2026 | No
| [[659]](https://www.erdosproblems.com/659) | Aletheia | 2 Feb, 2026 | 🟢 Full solution | 🟡 Sheffer and Lund (2014); 🟢 Grayzel (2026) | 2 Feb, 2026; 14 Jan, 2026 | Yes
| [[728]](https://www.erdosproblems.com/728) | Aristotle, GPT-5.2 Pro | 6 Jan, 2026 | 🟢 Full solution (Lean) | 🟡 Pomerance (2014) | 5-6 Jan, 2026 | Yes
| [[846]](https://www.erdosproblems.com/846) | DeepMind prover agent; OpenAI internal model (independently) | 21-25 Feb, 2026 | 🟢 Full solution (Lean); 🟢 Full solution | 🟡 Reiher, Rödl, and Sales (2024) | 25 Feb, 2026 | No
| [[851]](https://www.erdosproblems.com/851) | GPT-5.2 Pro | Feb 5, 2026 | 🟢 Full solution (building upon 🟡 Romanoff (1934)) | Matthews (1982); 🟢 Green and Sawhney (unpublished) | 6 Feb, 2026 | Yes
| [[897]](https://www.erdosproblems.com/897) | Archivara, Aristotle | 26 Dec, 2025 | 🟢 Full solution (Lean) | 🟢 Wirsing (1981) | 26 Dec, 2025 | Yes
| [[935]](https://www.erdosproblems.com/935) | Aletheia | 1 Feb, 2026 | 🟡 Solution to one part of problem | 🟡 van Doorn (2025) (solution to one part of [367]) | 2 Feb, 2026 | Yes
| [[983]](https://www.erdosproblems.com/983) | GPT-5.5 Pro | 30 Apr, 2026 | 🟡 Partial result (solution to first part) | 🟡 Erdős (1970) | 19 May, 2026 | Yes
| [[997]](https://www.erdosproblems.com/997) | OpenAI internal model | 31 Mar, 2026 | 🟢 Full solution | 🟡 Benatar (2014) | 1 Apr, 2026 | Yes
| [[1026]](https://www.erdosproblems.com/1026) | Aristotle | 7 Dec, 2025  | 🟢 Full solution (Lean) | 🟢 Tidor, Wang, and Yang (2016) | 8 Dec, 2025 | Only after applying an argument from Seidenberg (1959)
| [[1082]](https://www.erdosproblems.com/1082) | DeepMind prover agent | 14 Feb, 2026 | 🟡 Counterexample to one part (Lean) | 🟡 Fishburn (2002) | 25 Feb, 2026 | Yes
| [[1089]](https://www.erdosproblems.com/1089) | Aletheia | 1 Feb, 2026 | 🟢 Full solution found | 🟢 Bannai and Bannai (1981) | 1 Feb, 2026 | Yes

<a id="sect-1c"></a>
### 1(c). AI building on literature

*Literature presence*: comparable literature known *beforehand* and not discovered *afterwards*.<br>
*Human involvement*: non-significant.

| Problem | AI systems | Date | Literature | Outcome |  
| ------- | ---------- | ---- | ---------- | ------- |
| [[12]](https://www.erdosproblems.com/12) | DeepMind prover agent | 7 Apr, 2026 | 🟡 Erdős and Sárközy (1970) | 🟡 Partial result (Lean) (solutions to first part and second part)
| [[26]](https://www.erdosproblems.com/26) | DeepMind prover agent | 6 Apr, 2026 | 🟢 Ruzsa | 🟢 Solution to stronger problem
| [[36]](https://www.erdosproblems.com/36) | AlphaEvolve | 3 Nov, 2025 | 🟡 Haugland (2016) | 🟡 Slight improvement to past construction
| [[43]](https://www.erdosproblems.com/43) | Aristotle | 4 Dec, 2025 | 🟡 Barreto (2025) | 🟡 New proof of partial result (Lean)
| [[75]](https://www.erdosproblems.com/75) | GPT-5.4 Pro | 12 Apr, 2026 | 🟡 Erdős, Hajnal, and Szemerédi (1982) | 🟡 Partial result
| [[198]](https://www.erdosproblems.com/198) | AlphaProof | 2025 | 🟢 Baumgartner (1975) | 🟢 New proof found
| [[224]](https://www.erdosproblems.com/224) | Codex, GPT-5.2 Thinking | 14 Jan, 2026 | 🟢 Danzer and Grünbaum (1962) | 🟢 New proof found (Lean)
| [[258]](https://www.erdosproblems.com/258) | GPT-5.4 Pro | 14 Apr, 2026 | 🟡 Tao and Teräväinen (2025) | 🟢 Full solution
| [[264]](https://www.erdosproblems.com/264) | Aristotle | 18 Dec, 2025 | 🟡 Kovač and Tao (2024) | 🟡 New proof of partial result (Lean)
| [[349]](https://www.erdosproblems.com/349) | GPT-5.2 Thinking | 9 Mar, 2026 | 🟡 van Doorn (2026) | 🟡 Improved partial result
| [[379]](https://www.erdosproblems.com/379) | Seed Prover 1.5 | 21 Dec, 2025 | 🟢 Cambie, Kovač, and Tao (2025) | 🟢 New proof found
| [[488]](https://www.erdosproblems.com/488) | Aristotle | 27 Nov, 2025 | 🟡 Cambie (2025) | 🟡 New solution to variant problem (Lean)
| [[493]](https://www.erdosproblems.com/493) | Aristotle, GPT, Seed Prover | 2025 | 🟢 Seamans (2025) | 🟢 New or existing proof found (Lean)
| [[507]](https://www.erdosproblems.com/507) | AlphaEvolve | 3 Nov, 2025 | 🟡 Friedman (2015) | 🟡 Surpassed some past constructions
| [[513]](https://www.erdosproblems.com/513) | GPT-5.2 Thinking | 1 Mar, 2026 | 🟡 He and Tang (2026) | 🟡 Slight improvement to past construction
| [[524]](https://www.erdosproblems.com/524) | Gemini, GPT-5.2, Grok | 30 Jan, 2026 | 🟡 Sawhney (2025) | 🟡 Improved partial result
| [[679]](https://www.erdosproblems.com/679) | Aristotle | 12 Jan, 2026 | 🟡 DottedCalculator (2025) | 🟡 Improved proof by reducing dependence on prime number theorem
| [[729]](https://www.erdosproblems.com/729) | Aristotle, GPT-5.2 Pro | 8-10 Jan, 2026 | 🟡 Aristotle, Barreto, and GPT-5.2 Pro (2026) (full solution to [728]) | 🟢 Full solution (Lean)
| [[788]](https://www.erdosproblems.com/788) | GPT-5.2 Pro | 20 Jan, 2026 | 🟡 Hunter (2025) | 🟡 New partial result
| [[848]](https://www.erdosproblems.com/848) | Gemini 3.1 Pro, GPT-5.2 Thinking, GPT-5.4 Thinking | 5-23 Mar, 2026 | 🟢 Sawhney (2025) | 🟢 Derived explicit bound; 🟡 Partial result of variant problem
| [[868]](https://www.erdosproblems.com/868) | GPT-5.2 multi-agent system | 13 Jan, 2026 | 🟡 Erdős and Nathanson (1989) | 🟡 New partial result
| [[871]](https://www.erdosproblems.com/871) | Claude Opus 4.5, Gemini 3 Pro | 5 Jan, 2026 | 🟡 Erdős and Nathanson (1989) | 🟢 Existing partial result upgraded to full solution (Lean)
| [[942]](https://www.erdosproblems.com/942) | Gemini | 23 Nov, 2025 | 🟡 Erdős (unpublished, 1976) | 🟡 New proof found
| [[948]](https://www.erdosproblems.com/948) | Aristotle, GPT-5.5 Pro | 21 Jun, 2026 | 🟡 Erdős and Galvin (1991) | 🟢 Full solution (Lean)
| [[951]](https://www.erdosproblems.com/951) | AlphaEvolve | 28 Jan, 2026 | 🟡 Barreto, GPT-5.2 Pro, and Price (2026) + GPT-5.2 Thinking and Sothanaphan (2026) (solution to variant problem) | 🟡 New solution to variant problem
| [[958]](https://www.erdosproblems.com/958) | Aristotle | 27 Dec, 2025 | 🟢 Clemen, Dumitrescu, and Liu (2025) | 🟢 New proof found (Lean)
| [[966]](https://www.erdosproblems.com/966) | Aristotle | 25 Feb, 2026 | 🟢 Spencer (unpublished) | 🟢 Full solution (Lean)
| [[1004]](https://www.erdosproblems.com/1004) | GPT-5.5 Pro | 29 Apr, 2026 | 🟡 Pollack, Pomerance, and Treviño (2013) | 🟡 Partial result (implicit in literature)
| [[1007]](https://www.erdosproblems.com/1007) | Aristotle | 19 Jan, 2026 | 🟢 House (2013); 🟢 Chaffee and Noble (2016) | 🟢 New proof found (Lean)
| [[1032]](https://www.erdosproblems.com/1032) | Codex, GPT-5.5 Pro | 7 May, 2026 | 🟡 Luo, Ma, and Yang (2023) | 🟡 Improved partial result (Lean)
| [[1043]](https://www.erdosproblems.com/1043) | Aristotle | 28 Dec, 2025 | 🟢 Pommerenke (1961) | 🟢 New proof found (Lean)
| [[1043]](https://www.erdosproblems.com/1043) | GPT | 30 Dec, 2025 | 🟢 Pommerenke (1961); Aristotle | 🟢 New proof found
| [[1047]](https://www.erdosproblems.com/1047) | Aristotle | 21 Jan, 2026 | 🟢 Goodman (1966) | 🟢 New proof found (Lean)
| [[1048]](https://www.erdosproblems.com/1048) | Aristotle | 28 Jan, 2026 | 🟢 Pommerenke (1961) | 🟢 Proof found (Lean), which is a specific case of Pommerenke
| [[1090]](https://www.erdosproblems.com/1090) | Aristotle, Gemini 3 Flash | 27 Feb, 2026 | 🟢 Graham and Selfridge (unpublished, ~1975) | 🟢 Proof found (Lean)
| [[1095]](https://www.erdosproblems.com/1095) | Aristotle | 30 Dec, 2025 | 🟡 Ecklund, Erdős, and Selfridge (1975) | 🟡 New proof of (slightly weaker) partial result (Lean)
| [[1097]](https://www.erdosproblems.com/1097) | AlphaEvolve | 3 Nov, 2025 | 🟡 Lemm (2015) | 🟡 Slight improvement to past construction
| [[1197]](https://www.erdosproblems.com/1197) | Aristotle, Claude Opus 4.7, GPT-5.4 Pro | 13 Apr-21 Jun, 2026 | 🟡 Buczolich and Mauldin (1999) | 🟢 Full solution (Lean)

<a id="sect-1d"></a>
### 1(d). AI collaborating with humans

*Literature presence*: any.<br>
*Human involvement*: significant.

| Problem | Humans | AI systems | Date | Outcome |
| ------- | ------ | ---------- | ---- | ------- |
| [[7]](https://www.erdosproblems.com/7) | Jinook Lee | Aristotle | 2 May, 2026 | 🔴 Incorrect proof found
| [[12]](https://www.erdosproblems.com/12) | Nat Sothanaphan, Terence Tao | GPT-5.4 Thinking | 7 Apr, 2026 | 🟡 Partial result
| [[21]](https://www.erdosproblems.com/21) | Varun Sivashankar | Aristotle, GPT-5.5 Pro | 23 Jun, 2026 | 🟡 Partial result (Lean)
| [[25]](https://www.erdosproblems.com/25) | Przemek Chojecki | GPT-5.4 Pro | 19 Mar, 2026 | 🟡 Partial result
| [[42]](https://www.erdosproblems.com/42) | Harjas Sandhu | GPT-5.5 Pro | 27 Apr, 2026 | 🟢 Full solution
| [[52]](https://www.erdosproblems.com/52) | Thomas Bloom, Will Sawin, Carl Schildkraut, Dmitrii Zhelezov | GPT-5.5 Pro | 28 May, 2026 | 🟡 Solution to variant problem
| [[52]](https://www.erdosproblems.com/52) | Ingo Althöfer | GPT-5.5 | 28 May, 2026 | 🟡 Improved bound to variant problem
| [[52]](https://www.erdosproblems.com/52) | Boris Alexeev | GPT-5.5 | 4 Jun, 2026 | ⚪ Candidate solution to variant problem
| [[81]](https://www.erdosproblems.com/81) | Wouter van Doorn | Aristotle, GPT-5.5 Pro | 19 Jun, 2026 | 🟡 Partial result (Lean)
| [[90]](https://www.erdosproblems.com/90) | Ingo Althöfer, Michael Emmerich, Paata Ivanisvili, Tomasz Kania, leloy, mlewko, Eric Naslund, norxornor, Will Sawin, Carl Schildkraut, spiderduckpig, Tseng | GPT-5.5 Pro | 21 May-9 Jun, 2026 | 🟢 Improved explicit bound
| [[138]](https://www.erdosproblems.com/138) | Nat Sothanaphan | GPT-5.4 Thinking | 10 Apr, 2026 | 🟡 Partial result of variant problem
| [[202]](https://www.erdosproblems.com/202) | Boon Suan Ho | GPT-5.4 Pro | 23 Apr, 2026 | 🟢 Full solution
| [[202]](https://www.erdosproblems.com/202) | Przemek Chojecki | GPT-5.5 Pro | 30 Apr, 2026 | ⚪ Candidate full solution
| [[283]](https://www.erdosproblems.com/283) | Kevin Barreto, Liam Price | GPT-5.5 Pro | 3 May, 2026 | 🟢 Full solution
| [[288]](https://www.erdosproblems.com/288) | Ritvik Nayak | GPT-5.5 Thinking | 3 May, 2026 | ⚪ Candidate partial result
| [[306]](https://www.erdosproblems.com/306) | Shisheng Li | Claude, Claude Code | 17 Jun, 2026 | 🟡 Partial result (Lean)
| [[306]](https://www.erdosproblems.com/306) | Yuren Tang | Unspecified | 19 Jun, 2026 | ⚪ Candidate full solution (Lean)
| [[326]](https://www.erdosproblems.com/326) | Aron Bhalla | Aristotle, Codex, GPT-5.5 | 20 May-14 Jun, 2026 | 🟢 Full solution (Lean)
| [[327]](https://www.erdosproblems.com/327) | Yu Leon Liu | GPT-5.5, Rethlas | 13 May, 2026 | ⚪ Candidate partial result
| [[330]](https://www.erdosproblems.com/330) | David Turturean | GPT-5.5 Pro | 24 Apr, 2026 | 🟢 Full solution
| [[342]](https://www.erdosproblems.com/342) | Przemek Chojecki | GPT-5.2 Pro, GPT-5.4 Pro | 20 Jan-23 Mar, 2026 | 🟡 Partial result
| [[345]](https://www.erdosproblems.com/345) | Wouter van Doorn | Aristotle, GPT | 16 May, 2026 | 🟡 Partial result (Lean)
| [[346]](https://www.erdosproblems.com/346) | Kenta Kitamura | Codex, GPT | 21 Jun, 2026 | 🟢 Full solution (Lean)
| [[347]](https://www.erdosproblems.com/347) | Enrique Barschkis, Wouter van Doorn, jbbaehr22, Bartosz Naskrecki, Terence Tao | Aristotle, Claude Opus, Codex, GPT | 25 Oct, 2025-4 Feb, 2026 | 🟢 Full solution (Lean)
| [[351]](https://www.erdosproblems.com/351) | Kevin Barreto, Liam Price | GPT-5.5 Pro | 3 May, 2026 | 🟢 Full solution
| [[352]](https://www.erdosproblems.com/352) | Aleksandar Bulj, Vjekoslav Kovač | GPT-5.4 Pro, GPT-5.5 Pro | 29 May, 2026 | 🟡 Partial result of variant problem
| [[358]](https://www.erdosproblems.com/358) | Nat Sothanaphan | GPT-5.2 Thinking | 13-20 Feb, 2026 | 🔴 Argument with major gaps made
| [[367]](https://www.erdosproblems.com/367) | Boris Alexeev, Wouter van Doorn, Terence Tao | Aristotle, Gemini Deep Think | 20-22 Nov, 2025 | 🟡 Partial result
| [[369]](https://www.erdosproblems.com/369) | Sky Yang | GPT | 26 Mar, 2026 | 🟢 Full solution
| [[374]](https://www.erdosproblems.com/374) | Terence Tao | GPT-5.4 Pro | 31 Mar, 2026 | 🟡 Partial result
| [[380]](https://www.erdosproblems.com/380) | Terence Tao | GPT-5.4 Pro | 31 Mar, 2026 | 🟢 Full solution
| [[388]](https://www.erdosproblems.com/388) | Malek Zribi | Claude, Gemini, GPT-5.4 | 12-15 Mar, 2026 | 🔴 Incorrect proof found
| [[390]](https://www.erdosproblems.com/390) | Samuel Mausberg | GPT-5.5 Pro | 2 May, 2026 | ⚪ Candidate partial result
| [[393]](https://www.erdosproblems.com/393) | David Turturean | GPT-5.5 Pro | 3 May, 2026 | 🟡 Conditional partial result
| [[396]](https://www.erdosproblems.com/396) | Malek Zribi | Claude, Codex, GPT | 15 Mar, 2026 | 🟡 Partial result
| [[396]](https://www.erdosproblems.com/396) | Justin Dehorty, Nat Sothanaphan | GPT-5.4 Pro, GPT-5.4 Thinking | 5-7 Apr, 2026 | 🟡 Related result
| [[400]](https://www.erdosproblems.com/400) | Eric Li | GPT | 22 Jun, 2026 | ⚪ Candidate partial result
| [[401]](https://www.erdosproblems.com/401) | Boris Alexeev, Kevin Barreto, Liam Price, Nat Sothanaphan | Aristotle, GPT-5.2 Pro | 10-11 Jan, 2026 | 🟢 Full solution (Lean); solution to variant problem
| [[411]](https://www.erdosproblems.com/411) | hoodieuser | Claude | 3 Apr, 2026 | 🔴 Incorrect proof found
| [[415]](https://www.erdosproblems.com/415) | Przemek Chojecki | GPT-5.4 Pro | 19 Apr, 2026 | 🟡 Partial result
| [[423]](https://www.erdosproblems.com/423) | Quanyu Tang, Nat Sothanaphan | GPT-5.2 Thinking, GPT-5.4 Thinking | 11-12 Mar, 2026 | 🟡 Partial result
| [[432]](https://www.erdosproblems.com/432) | Sungchul Lee | GPT-5.5 Pro | 23 Jun, 2026 | ⚪ Candidate partial result
| [[451]](https://www.erdosproblems.com/451) | Wouter van Doorn, Quanyu Tang | Aristotle, GPT-5.5 Pro | 26 Apr-19 Jun, 2026 | 🟡 Partial result (Lean)
| [[456]](https://www.erdosproblems.com/456) | David Turturean | GPT-5.5 Pro | 4 May, 2026 | ⚪ Candidate partial result (solutions to first part and second part; conditional solution to third part)
| [[460]](https://www.erdosproblems.com/460) | Przemek Chojecki | GPT-5.2 | 13 Jan, 2026 | 🟡 Reduction to a simpler problem
| [[488]](https://www.erdosproblems.com/488) | Przemek Chojecki | Aristotle, GPT-5.4 | 20 Mar, 2026 | 🟡 Partial result
| [[501]](https://www.erdosproblems.com/501) | Sungchul Lee | GPT-5.5 Pro | 29 May-1 Jun, 2026 | ⚪ Candidate conditional partial result (conditional solution to first part)
| [[503]](https://www.erdosproblems.com/503) | Przemek Chojecki | Aristotle, GPT-5.4 Pro | 22 Apr, 2026 | 🔴 Argument with major gaps made
| [[503]](https://www.erdosproblems.com/503) | Przemek Chojecki, Junnosuke Koizumi, RealBelgian | GPT-5.5 Pro | 27-28 May, 2026 | 🟡 Partial result
| [[514]](https://www.erdosproblems.com/514) | Przemek Chojecki | GPT-5.4 Pro | 20 Apr, 2026 | 🟡 Partial result (solutions to first part and second part)
| [[514]](https://www.erdosproblems.com/514) | Yuta Oriike | GPT-5.5 Pro | 28 Apr, 2026 | 🟡 Partial result (Lean) (solution to third part)
| [[521]](https://www.erdosproblems.com/521) | Vjekoslav Kovač | GPT-5.5 Pro | 25 Apr, 2026 | 🟡 Solution to variant problem
| [[521]](https://www.erdosproblems.com/521) | Vjekoslav Kovač | GPT-5.5 Pro | 30 Apr, 2026 | ⚪ Candidate full solution
| [[524]](https://www.erdosproblems.com/524) | Brayden Letwin, Mehtaab Sawhney | GPT-5.4 Pro | 21 Apr, 2026 | 🟡 Partial result
| [[535]](https://www.erdosproblems.com/535) | Kireet Cheri, Sourish Kumrawat, Hrishi Sunder | GPT-5.5 Thinking | 27 Apr, 2026 | 🟡 Partial result (implicit in literature)
| [[593]](https://www.erdosproblems.com/593) | Eric Li | GPT | 23 Jun, 2026 | ⚪ Candidate full solution
| [[598]](https://www.erdosproblems.com/598) | Przemek Chojecki | Aristotle, GPT-5.4 Pro | 22 Apr, 2026 | ⚪ Candidate partial result
| [[603]](https://www.erdosproblems.com/603) | Przemek Chojecki | GPT-5.4 Pro | 21 Apr, 2026 | 🟢 Full solution
| [[610]](https://www.erdosproblems.com/610) | Przemek Chojecki | Aristotle, GPT-5.4 Pro | 21 Apr, 2026 | 🟢 Full solution (Lean) (implicit in literature)
| [[623]](https://www.erdosproblems.com/623) | Sungchul Lee | GPT-5.5 Pro | 4 Jun, 2026 | ⚪ Candidate full solution
| [[659]](https://www.erdosproblems.com/659) | Benjamin Grayzel | Gemini 3 | 13 Jan, 2026 | 🟢 Full solution
| [[675]](https://www.erdosproblems.com/675) | Boon Suan Ho | GPT-5.4 Pro | 18 Apr, 2026 | 🟡 Partial result
| [[684]](https://www.erdosproblems.com/684) | Quanyu Tang | GPT-5.2 Thinking | 19 Jan, 2026 | 🟡 Partial result
| [[684]](https://www.erdosproblems.com/684) | Nat Sothanaphan | GPT-5.4 Thinking | 2 Apr, 2026 | 🟡 Partial result
| [[686]](https://www.erdosproblems.com/686) | Adenwalla, Stijn Cambie, Wouter van Doorn, Vjekoslav Kovač, Miklos, Nat Sothanaphan, Quanyu Tang, Terence Tao, vilc, Malek Zribi | AlphaProof, Claude, Gemini Deep Think, GPT-5.2 Thinking, GPT-5.4 Thinking, Seed 2.0 Pro | 9 Aug, 2025-15 Mar, 2026 | 🟡 Various partial results
| [[689]](https://www.erdosproblems.com/689) | Boris Alexeev, Przemek Chojecki, Dogmachine, jleng01, Mehtaab Sawhney, Terence Tao, Malek Zribi | Codex, GPT-5.2, GPT-5.5 Pro | 29 Oct, 2025-2 Jun, 2026 | ⚪ Candidate full solution
| [[690]](https://www.erdosproblems.com/690) | Davide Crapis, Shouqiao Wang | Multiscalar Fields System | 8 May, 2026 | 🟢 Full solution
| [[696]](https://www.erdosproblems.com/696) | Jake Mallen, David Turturean | Aristotle, Claude Code, Claude Opus 4.7, GPT-5.5 Pro | 26 Apr-5 Jun, 2026 | 🟢 Full solution (Lean)
| [[749]](https://www.erdosproblems.com/749) | Aron Bhalla | GPT-5.4 Thinking | 4-6 Apr, 2026 | 🟡 Partial result; 🟡 Solution to variant problem
| [[750]](https://www.erdosproblems.com/750) | Przemek Chojecki | GPT-5.5 Pro | 3 May, 2026 | 🟢 Full solution
| [[768]](https://www.erdosproblems.com/768) | Eric Li | GPT | 22 Jun, 2026 | ⚪ Candidate full solution
| [[776]](https://www.erdosproblems.com/776) | Yixin He, Quanyu Tang | GPT-5.2 Thinking | 11 Feb, 2026 | 🟡 Partial result
| [[819]](https://www.erdosproblems.com/819) | Yu Leon Liu | GPT-5.5, Rethlas | 15 May, 2026 | ⚪ Candidate partial result
| [[848]](https://www.erdosproblems.com/848) | Malek Zribi | Claude Opus 4.6, GPT-5.4 | 12-15 Mar, 2026 | 🔴 Incorrect proof found
| [[848]](https://www.erdosproblems.com/848) | Mehtaab Sawhney, Mark Sellke | GPT-5 | 12 Oct-20 Nov, 2025 | 🟢 Full solution
| [[852]](https://www.erdosproblems.com/852) | Aron Bhalla | GPT-5.4 | 15 Apr, 2026 | 🟡 Partial result
| [[852]](https://www.erdosproblems.com/852) | Przemek Chojecki, David Turturean | GPT-5.5 Pro | 24 Apr, 2026 | ⚪ Candidate partial result
| [[856]](https://www.erdosproblems.com/856) | Przemek Chojecki | GPT-5.4 Pro | 15 Apr, 2026 | ⚪ Candidate full solution
| [[858]](https://www.erdosproblems.com/858) | Przemek Chojecki | GPT-5.4 Pro | 15 Apr, 2026 | 🟢 Full solution
| [[863]](https://www.erdosproblems.com/863) | Boon Suan Ho | GPT-5.4 Pro | 22 Apr, 2026 | 🟢 Full solution
| [[865]](https://www.erdosproblems.com/865) | Ricky Cipollini | GPT-5.5 Pro | 21-22 Jun, 2026 | 🟢 Full solution
| [[866]](https://www.erdosproblems.com/866) | Wouter van Doorn | Aristotle, GPT-5.3 Instant | 4 May, 2026 | 🟡 Partial result (Lean)
| [[870]](https://www.erdosproblems.com/870) | David Turturean | GPT-5.4 Pro, GPT-5.5 Pro | 24 Apr-May 2, 2026 | ⚪ Candidate full solution
| [[872]](https://www.erdosproblems.com/872) | Om_Buddhdev_sensho | GPT-5.4 Pro | 16 Apr, 2026 | 🟡 Partial result
| [[872]](https://www.erdosproblems.com/872) | Jonas Silva | GPT-5.5 Pro | 29 Apr, 2026 | ⚪ Candidate partial result
| [[873]](https://www.erdosproblems.com/873) | Ritvik Nayak | GPT-5.4 Thinking | 29 Apr, 2026 | ⚪ Candidate partial result
| [[873]](https://www.erdosproblems.com/873) | Ingo Althöfer | GPT-5.5 Thinking | 30 Apr, 2026 | ⚪ Candidate partial result
| [[875]](https://www.erdosproblems.com/875) | Lech Mazur | Codex, GPT-5.5 Pro | 7 May, 2026 | 🟡 Partial result (Lean)
| [[888]](https://www.erdosproblems.com/888) | Przemek Chojecki | Aristotle, GPT-5.5 Pro | 25 Apr, 2026 | 🟢 Full solution
| [[896]](https://www.erdosproblems.com/896) | Przemek Chojecki | GPT-5.5 Pro | 26 Apr, 2026 | 🟢 Full solution
| [[906]](https://www.erdosproblems.com/906) | Adriano Almeida | Unspecified | 25 Apr, 2026 | ⚪ Candidate full solution
| [[906]](https://www.erdosproblems.com/906) | Przemek Chojecki | GPT-5.5 Pro | 25 Apr, 2026 | ⚪ Candidate full solution
| [[931]](https://www.erdosproblems.com/931) | Adenwalla, Malek Zribi | Claude, GPT-5.4 | 12 Mar-8 Jun, 2026 | 🟡 Partial result
| [[942]](https://www.erdosproblems.com/942) | Scott Hughes | Aristotle, Claude Opus 4.8, Codex, GPT-5.5 | 13-14 Jun, 2026 | 🟡 Partial result (Lean)
| [[943]](https://www.erdosproblems.com/943) | Przemek Chojecki | GPT-5.4 Pro | 3 Feb-18 Mar, 2026 | 🟡 Partial result
| [[953]](https://www.erdosproblems.com/953) | Przemek Chojecki | GPT-5.5 Pro | 27 Apr, 2026 | 🟢 Full solution
| [[956]](https://www.erdosproblems.com/956) | Przemek Chojecki | Aristotle, GPT-5.5 Pro | 27 Apr, 2026 | ⚪ Candidate full solution
| [[986]](https://www.erdosproblems.com/986) | Domagoj Bradač | Claude, OpenAI internal model | 27 May-16 Jun, 2026 | 🟢 Full solution
| [[995]](https://www.erdosproblems.com/995) | Boon Suan Ho | GPT-5.4 Pro | 21 Apr, 2026 | 🟡 Partial result
| [[996]](https://www.erdosproblems.com/996) | Boon Suan Ho | GPT-5.4 Pro | 21 Apr, 2026 | 🟢 Full solution
| [[951]](https://www.erdosproblems.com/951) | Nat Sothanaphan | GPT-5.2 Thinking | 28 Jan, 2026 | 🟡 New solution to variant problem
| [[976]](https://www.erdosproblems.com/976) | Aron Bhalla | GPT-5.4 | 16 Apr, 2026 | 🟡 Conditional partial result
| [[1026]](https://www.erdosproblems.com/1026) | Boris Alexeev, Stijn Cambie, Terence Tao, Lawrence Wu | AlphaEvolve, Aristotle, Gemini, GPT | 8 Dec, 2025  | 🟢 Full solution (Lean)
| [[1038]](https://www.erdosproblems.com/1038) | catsflowers5544, jspier, Junnosuke Koizumi, Kenneth Mendoza, Nat Sothanaphan, Terence Tao, Hua Xu | AlphaEvolve, Claude Fable 5, Codex, GPT-5.2 Thinking, GPT-5.4 Thinking, GPT-5.5 | 16 Dec, 2025-10 Jun, 2026 | 🟡 Partial result
| [[1039]](https://www.erdosproblems.com/1039) | Houi | Aristotle, Claude Opus 4.6 | 6-8 Mar, 2026 | 🟡 Partial result (Lean)
| [[1041]](https://www.erdosproblems.com/1041) | shtuka | Claude Opus 4.6, Gemini 3.1 Pro, GPT-5.4 | 17-24 Mar, 2026 | 🔴 Argument with major gaps made
| [[1061]](https://www.erdosproblems.com/1061) | Eric Li | GPT | 24 Jun, 2026 | ⚪ Candidate full solution
| [[1062]](https://www.erdosproblems.com/1062) | Damek Davis | GPT-5.4 Pro | 19 Apr, 2026 | 🟡 Partial result
| [[1092]](https://www.erdosproblems.com/1092) | Przemek Chojecki | GPT-5.5 Pro | 28 Apr, 2026 | 🟢 Full solution
| [[1095]](https://www.erdosproblems.com/1095) | shtuka | Claude Opus 4.6, Gemini 3.1 Pro, GPT-5.4 Pro | 13 Mar, 2026 | 🟡 Partial result
| [[1132]](https://www.erdosproblems.com/1132) | Terence Tao | AlphaEvolve, Claude, Gemini Pro, GPT-5.4 Pro | 2 Feb-24 Mar, 2026 | 🟡 Partial result
| [[1133]](https://www.erdosproblems.com/1133) | Przemek Chojecki | GPT-5.5 Pro | 29 Apr, 2026 | ⚪ Candidate full solution
| [[1138]](https://www.erdosproblems.com/1138) | Kireet Cheri, Sourish Kumrawat, Hrishi Sunder | GPT-5.5 Pro, GPT-5.5 Thinking | 25 Apr, 2026 | 🟢 Full solution
| [[1139]](https://www.erdosproblems.com/1139) | Przemek Chojecki, gavinsherry, Liam Price, Terence Tao | GPT-5.2 Pro, GPT-5.5 Pro | 26 Jan-19 Jun, 2026 | ⚪ Candidate full solution
| [[1141]](https://www.erdosproblems.com/1141) | Quanyu Tang | GPT-5.2 Pro, GPT-5.2 Thinking | 25 Jan, 2026 | 🟡 Partial result of variant problem
| [[1143]](https://www.erdosproblems.com/1143) | Przemek Chojecki | GPT-5.5 Pro | 29 Apr, 2026 | 🟡 Partial result (implicit in literature)
| [[1148]](https://www.erdosproblems.com/1148) | Ingo Althöfer, Przemek Chojecki, Wouter van Doorn | Gemini 3 Pro, Gemini 3.1 Pro, GPT-5.2 Pro, GPT-5.2 Thinking, GPT-5.4 Pro | 24 Jan-16 Mar, 2026 | 🟢 Full solution
| [[1148]](https://www.erdosproblems.com/1148) | Ingo Althöfer, Przemek Chojecki | GPT-5.5 Pro | 19 May, 2026 | 🟢 Solution to stronger problem
| [[1151]](https://www.erdosproblems.com/1151) | Przemek Chojecki | GPT-5.5 Pro | 30 Apr, 2026 | 🟢 Full solution
| [[1153]](https://www.erdosproblems.com/1153) | Aron Bhalla, Nat Sothanaphan, Terence Tao | AlphaEvolve, Claude, Gemini Pro, GPT-5.2 Thinking, GPT-5.4 Pro | 2 Feb-24 Mar, 2026 | 🟢 Full solution
| [[1177]](https://www.erdosproblems.com/1177) | Eric Li | GPT | 23 Jun, 2026 | ⚪ Candidate full solution
| [[1183]](https://www.erdosproblems.com/1183) | Przemek Chojecki, Quanyu Tang | GPT-5.4 Pro | 18 Mar, 2026  | 🟡 Partial result
| [[1190]](https://www.erdosproblems.com/1190) | Boon Suan Ho | GPT-5.4 Pro | 23 Apr, 2026 | 🟢 Full solution
| [[1190]](https://www.erdosproblems.com/1190) | Przemek Chojecki | GPT-5.5 Pro | 30 Apr, 2026 | ⚪ Candidate full solution
| [[1194]](https://www.erdosproblems.com/1194) | Lech Mazur | Codex, GPT-5.5 Pro | 2 May, 2026 | 🟡 Partial result (Lean)
| [[1195]](https://www.erdosproblems.com/1195) | Boon Suan Ho | GPT-5.4 Pro | 19 Apr, 2026 | 🟢 Full solution
| [[1196]](https://www.erdosproblems.com/1196) | Nat Sothanaphan | GPT-5.4 Thinking | 16 Apr, 2026 | 🟢 Full solution (stronger than literature)
| [[1201]](https://www.erdosproblems.com/1201) | Przemek Chojecki | GPT-5.5 Pro | 30 Apr, 2026 | ⚪ Candidate full solution
| [[1208]](https://www.erdosproblems.com/1208) | Sungchul Lee | GPT-5.5 Pro | 14 Jun, 2026 | ⚪ Candidate partial result
| [[1209]](https://www.erdosproblems.com/1209) | Enrique Barschkis | GPT-5.4 Pro | 15 Apr, 2026  | 🟡 Partial result (Lean)

<a id="sect-2"></a>
## 2. Secondary contributions

<a id="sect-2a"></a>
### 2(a). Literature search

| Problem | AI systems | Date | Outcome |
| ------- | ---------- | ---- | ------- |
| [[35]](https://www.erdosproblems.com/35) | GPT-5 | 13 Oct, 2025 | 🟡 Partial results found
| [[66]](https://www.erdosproblems.com/66) | GPT-5 | 13 Oct, 2025 | 🟡 Partial results found
| [[94]](https://www.erdosproblems.com/94) | GPT-5 | 2 Nov, 2025 | 🟢 Full solution found
| [[120]](https://www.erdosproblems.com/120) | GPT-5.4 Thinking | 14 Mar, 2026 | 🟢 Solution to variant problem found
| [[167]](https://www.erdosproblems.com/167) | GPT-5 | 12 Oct, 2025 | 🟡 Partial results found
| [[188]](https://www.erdosproblems.com/188) | GPT-5 | 13 Oct, 2025 | 🟡 Partial results found
| [[214]](https://www.erdosproblems.com/214) | ChatGPT Deep research, Gemini Deep Research | 20 Feb, 2026 | 🟡 Partial results found
| [[223]](https://www.erdosproblems.com/223) | GPT-5 | 13 Oct, 2025 | 🟢 Full solution found
| [[306]](https://www.erdosproblems.com/306) | GPT-5.2 Thinking | 25 Feb, 2026 | 🟡 Partial results found
| [[325]](https://www.erdosproblems.com/325) | ChatGPT Deep research | 9 Mar, 2026 | 🟡 Partial results found
| [[330]](https://www.erdosproblems.com/330) | ChatGPT Deep research, Claude, Gemini Deep Research | 19 Dec, 2025 | 🔴 Partial results found with inaccuracies; literature proof not found
| [[333]](https://www.erdosproblems.com/333) | GPT-5.2 Pro | 25 Dec, 2025 | 🔴 Incorrect proof claimed; literature proof not found
| [[333]](https://www.erdosproblems.com/333) | Aletheia | 1 Feb, 2026 | 🟢 Full solution found
| [[339]](https://www.erdosproblems.com/339) | GPT-5 | 11 Oct, 2025 | 🟢 Full solution found
| [[347]](https://www.erdosproblems.com/347) | ChatGPT Deep research | 25 Oct, 2025 | 🟡 Partial results found
| [[354]](https://www.erdosproblems.com/354) | ChatGPT Deep research | 19 Oct, 2025 | 🟡 Partial results found |
| [[370]](https://www.erdosproblems.com/370) | ChatGPT Deep research, Gemini, Gemini Deep Research | 17 Oct, 2025 | 🟡 Problem found to be misstated; solutions to variant problems found |
| [[387]](https://www.erdosproblems.com/387) | ChatGPT Deep research | 1 Nov, 2025 | 🟡 Partial results found
| [[397]](https://www.erdosproblems.com/397) | ChatGPT Deep research | 10 Jan, 2026 | 🟢 Full solution found
| [[481]](https://www.erdosproblems.com/481) | ChatGPT Deep research, Gemini Deep Research | 1 Dec, 2025 | 🟡 Unwittingly reproduced existing proof
| [[481]](https://www.erdosproblems.com/481) | GPT | 3 Dec, 2025 | 🟢 Full solution found
| [[494]](https://www.erdosproblems.com/494) | GPT-5 | 13 Oct, 2025 | 🟢 Full solution found
| [[515]](https://www.erdosproblems.com/515) | GPT-5 | 15 Oct, 2025 | 🟢 Full solution found
| [[516]](https://www.erdosproblems.com/516) | ChatGPT Deep research, Claude, Gemini Deep Research | 28 Dec, 2025 | 🟢 Problem found to be misstated; full solution to actual problem found
| [[524]](https://www.erdosproblems.com/524) | GPT-5.2 Pro | 27 Dec, 2025 | 🟡 Partial results found
| [[533]](https://www.erdosproblems.com/533) | GPT | 26 Jan, 2026 | 🟢 Full solution found
| [[559]](https://www.erdosproblems.com/559) | ChatGPT Deep research, Gemini Deep Research | 26 Oct, 2025 | 🟡 Partial results found
| [[574]](https://www.erdosproblems.com/574) | GPT-5.4 Pro | 28 Mar, 2026 | 🟢 Full solution found
| [[575]](https://www.erdosproblems.com/575) | GPT | 14 Jan, 2026 | 🟡 Paper identifying a misstatement to the problem found
| [[591]](https://www.erdosproblems.com/591) | ChatGPT Deep research | 17 Jan, 2026 | 🟢 Full solution found
| [[591]](https://www.erdosproblems.com/591) | Aletheia | 1 Feb, 2026 | 🟢 Full solution found
| [[602]](https://www.erdosproblems.com/602) | GPT-5.4 Thinking | 20 Apr, 2026 | 🟡 Related results found
| [[621]](https://www.erdosproblems.com/621) | GPT-5 | 13 Oct, 2025 | 🟢 Full solution found
| [[645]](https://www.erdosproblems.com/645) | GPT-5 | 20 Oct, 2025 | 🟢 Full solution found
| [[650]](https://www.erdosproblems.com/650) | ChatGPT Deep research | 6 Mar, 2026 | 🟢 Full solution found
| [[652]](https://www.erdosproblems.com/652) | GPT-5.2 Pro | 17 Jan, 2026 | 🟢 Full solution by applying literature results
| [[652]](https://www.erdosproblems.com/652) | Aletheia | 2 Feb, 2026 | 🟢 Full solution by applying literature results
| [[659]](https://www.erdosproblems.com/659) | Gemini Deep Research | 13 Jan, 2026 | 🟡 Partial results, upgradeable to full solution, found
| [[672]](https://www.erdosproblems.com/672) | GPT | 7 Jan, 2026 | 🟡 Partial results found
| [[705]](https://www.erdosproblems.com/705) | GPT | 26 Jan, 2026 | 🟢 Full solution found
| [[705]](https://www.erdosproblems.com/705) | Aletheia | 1 Feb, 2026 | 🟢 Full solution found
| [[729]](https://www.erdosproblems.com/729) | ChatGPT Deep research | Jan 10, 2026 | 🟡 Related results found
| [[737]](https://www.erdosproblems.com/737) | GPT-5 | 30 Sep, 2025 | 🟢 Full solution found
| [[749]](https://www.erdosproblems.com/749) | GPT-5.4 Thinking | 3 Apr, 2026 | 🟡 Partial results found
| [[750]](https://www.erdosproblems.com/750) | GPT-5 | 13 Oct, 2025 | 🟡 Partial results found
| [[788]](https://www.erdosproblems.com/788) | GPT-5 | 14 Oct, 2025 | 🟡 Partial results found
| [[793]](https://www.erdosproblems.com/793) | ChatGPT Deep research | 30 Nov, 2025 | 🟡 Partial results found
| [[811]](https://www.erdosproblems.com/811) | GPT-5 | 13 Oct, 2025 | 🟡 Partial results found
| [[822]](https://www.erdosproblems.com/822) | GPT-5 | 13 Oct, 2025 | 🟢 Full solution found
| [[827]](https://www.erdosproblems.com/827) | GPT-5 | 14 Oct, 2025 | 🟡 Partial results found
| [[829]](https://www.erdosproblems.com/829) | GPT-5 | 13 Oct, 2025 | 🟡 Partial results found
| [[847]](https://www.erdosproblems.com/847) | GPT-5.2 Pro | 19 Jan, 2026 | 🟢 Full solution found
| [[851]](https://www.erdosproblems.com/851) | ChatGPT Deep research, Claude, Gemini Deep Research | 5 Feb, 2026 | 🔴🔴 Confused with another problem; 🟡 Partial results found
| [[871]](https://www.erdosproblems.com/871) | ChatGPT Deep research | 6 Dec, 2025 | 🟡 Partial results found
| [[903]](https://www.erdosproblems.com/903) | GPT-5 | 14 Oct, 2025 | 🟢 Full solution found
| [[915]](https://www.erdosproblems.com/915) | ChatGPT Deep research | 26 Oct, 2025 | 🟡 Partial results found
| [[942]](https://www.erdosproblems.com/942) | ChatGPT Deep research | 23 Nov, 2025 | 🟡 Partial results found
| [[965]](https://www.erdosproblems.com/965) | GPT | 2 Jan, 2026 | 🟢 Full solution found
| [[971]](https://www.erdosproblems.com/971) | Claude | 31 Jan, 2026 | 🟡 Partial results found
| [[985]](https://www.erdosproblems.com/985) | GPT-5.4 Thinking | 6 Mar, 2026 | 🟡 Partial results found
| [[990]](https://www.erdosproblems.com/990) | ChatGPT Deep research, Gemini Deep Research | 20 Oct, 2025 | 🟡 Partial results found
| [[992]](https://www.erdosproblems.com/992) | Aletheia | 1 Feb, 2026 | 🟢 Full solution found
| [[1008]](https://www.erdosproblems.com/1008) | GPT-5 | 29 Sep, 2025 | 🟢 Full solution found
| [[1011]](https://www.erdosproblems.com/1011) | GPT-5 | 13 Oct, 2025 | 🟡 Partial results found
| [[1016]](https://www.erdosproblems.com/1016) | ChatGPT Deep research, Gemini Deep Research | 18 Oct, 2025 | 🟡 Partial results found
| [[1019]](https://www.erdosproblems.com/1019) | ChatGPT Deep research, Gemini Deep Research | 18 Oct, 2025 | 🟡 Solution claim found, but precise citation not found
| [[1021]](https://www.erdosproblems.com/1021) | GPT | 21 Jan, 2026 | 🟢 Full solution (which was previously noted) found
| [[1043]](https://www.erdosproblems.com/1043) | GPT-5 | 12 Oct, 2025 | 🟢 Full solution found
| [[1079]](https://www.erdosproblems.com/1079) | GPT-5 | 13 Oct, 2025 | 🟢 Full solution found
| [[1084]](https://www.erdosproblems.com/1084) | GPT | 21 Jan, 2026 | 🟡 Partial results found
| [[1099]](https://www.erdosproblems.com/1099) | ChatGPT Deep research, Gemini, Gemini Deep Research | 19 Oct, 2025 | 🟢 Full solution found
| [[1105]](https://www.erdosproblems.com/1105) | ChatGPT Deep research | 19 Jan, 2026 | 🟡 Partial results found
| [[1105]](https://www.erdosproblems.com/1105) | Aletheia | 1 Feb, 2026 | 🟢 Full solution found; 🔴 Gave some wrong references
| [[1123]](https://www.erdosproblems.com/1123) | Gemini Deep Research | 31 Jan, 2026 | 🟢 Full solution found
| [[1124]](https://www.erdosproblems.com/1124) | GPT | 31 Dec, 2025 | 🟢 Solution to variant problem found
| [[1129]](https://www.erdosproblems.com/1129) | GPT-5.2 Pro | 17 Jan, 2026 | 🟢 Full solution found
| [[1130]](https://www.erdosproblems.com/1130) | GPT-5.2 Pro | 17 Jan, 2026 | 🟢 Full solution found
| [[1147]](https://www.erdosproblems.com/1147) | GPT-5.2 Thinking | 26 Jan, 2026 | 🟢 Full solution found
| [[1150]](https://www.erdosproblems.com/1150) | Gemini Deep Research | 4 Feb, 2026 | 🟡 Claimed solution found (likely incorrect)
| [[1154]](https://www.erdosproblems.com/1154) | GPT-5.2 Thinking | 24 Jan, 2026 | 🟡 Partial results found
| [[1161]](https://www.erdosproblems.com/1161) | GPT-5.2 Thinking | 24 Jan, 2026 | 🟢 Full solution found
| [[1198]](https://www.erdosproblems.com/1198) | GPT-5.4 | 16 Apr, 2026 | 🟡 Partial results found
| [[1216]](https://www.erdosproblems.com/1216) | ChatGPT Deep research | 10 Mar, 2026 | 🟢 Solution stronger than problem found
| [[1216]](https://www.erdosproblems.com/1216) | GPT-5.4 Thinking | 12 Apr, 2026 | 🟡 Related results found

<a id="sect-2b"></a>
### 2(b). Formalization

| Problem | Proof to formalize | AI systems | Date |
| ------- | ------------------ | ---------- | -----|
| [[16]](https://www.erdosproblems.com/16) | 🟢 Chen (2023) | Antigravity, Gemini 3.1 Pro | 25 Feb, 2026
| [[24]](https://www.erdosproblems.com/24) | 🟢 Grzesik (2012) | Aristotle | 23 Apr-26 May, 2026
| [[26]](https://www.erdosproblems.com/26) | 🟢 Ruzsa | Aristotle | 28 Dec, 2025
| [[31]](https://www.erdosproblems.com/31) | 🟢 Lorentz (1954), Wouter van Doorn (2025) | Aristotle, GPT | 24 Nov, 2025
| [[34]](https://www.erdosproblems.com/34) | 🟢 Konieczny (2015) | Aristotle | 5 Feb, 2026
| [[38]](https://www.erdosproblems.com/38) | 🟢 GPT-5.5 Pro (2026) | Aristotle | 1 May, 2026
| [[42]](https://www.erdosproblems.com/42) | 🟢 GPT-5.5 Pro (2026) | Codex, GPT-5.5 Pro | 10 May, 2026
| [[43]](https://www.erdosproblems.com/43) | 🟡 Barreto (2025) | Aristotle, Claude | 21 Dec, 2025
| [[56]](https://www.erdosproblems.com/56) | 🟢 Ahlswede and Khachatrian (1995) | Aristotle, GPT | 25 Nov, 2025-27 May, 2026
| [[71]](https://www.erdosproblems.com/71) | 🟢 Bollobás (1977) | Aristotle, Claude Opus 4.7, GPT-5.5 | 24 May, 2026
| [[90]](https://www.erdosproblems.com/90) | 🟢 OpenAI internal model (2026) | Aleph Prover | 28 May-12 Jun, 2026
| [[93]](https://www.erdosproblems.com/93) | 🟢 Altman (1963) | Aristotle, Claude Opus 4.5, Claude Opus 4.6, Gemini 3 Flash, Gemini 3 Pro, Numina Lean Agent | 17 Feb, 2026
| [[94]](https://www.erdosproblems.com/94) | 🟢 Lefmann and Thiele (1995) | Codex, GPT-5.2 Thinking; Seed Prover | 15 Jan, 2026
| [[105]](https://www.erdosproblems.com/105) | 🟢 Xichuan (2025) | Aristotle, GPT Pro | 17 Nov, 2025
| [[106]](https://www.erdosproblems.com/106) | 🟡 Baek, Koizumi, and Ueoro (2024) | Aristotle | 10 Dec, 2025
| [[115]](https://www.erdosproblems.com/115) | 🟢 Eremenko and Lempert (1994) | Aristotle, Claude Opus 4.6, Claude Sonnet 4.6, Gemini 3 Flash, Gemini 3.1 Pro, ulam.ai scaffold with Gemini 3 Flash and Gemini 3.1 Pro | 3 Mar, 2026
| [[134]](https://www.erdosproblems.com/134) | 🟢 Alon | Aristotle | 7 Feb, 2026
| [[150]](https://www.erdosproblems.com/150) | 🟢 Bradač (2024) | Aristotle | 31 Mar, 2026
| [[154]](https://www.erdosproblems.com/154) | 🟢 Lindström (1998) | Aristotle, GPT | 6 Feb, 2026
| [[164]](https://www.erdosproblems.com/164) | 🟢 Alexeev, Barreto, Li, Lichtman, Price, Shah, Tang, and Tao (2026) | Codex | 4 May, 2026
| [[165]](https://www.erdosproblems.com/165) | 🟡 Hefty, Horn, King and Pfender (2025) | Trellis | 10 Jun, 2026
| [[178]](https://www.erdosproblems.com/178) | 🟢 Beck (1981) | Aristotle | 21 Apr, 2026
| [[189]](https://www.erdosproblems.com/189) | 🟢 Kovač (2023) | Aristotle, Gemini 3 Pro | 17 Dec, 2025
| [[192]](https://www.erdosproblems.com/192) | 🟢 Keränen (1992) | Aristotle | 9-10 May, 2026
| [[194]](https://www.erdosproblems.com/194) | 🟢 Ardal, Brown, and Jungić (2011) | Aristotle | 15 Apr, 2026
| [[198]](https://www.erdosproblems.com/198) | 🟢 Baumgartner (1975) | Aristotle, GPT | 24 Nov, 2025
| [[199]](https://www.erdosproblems.com/199) | 🟢 Baumgartner (1975) | Aristotle | 24 Feb, 2026
| [[202]](https://www.erdosproblems.com/202) | 🟢 Boon Suan Ho and GPT-5.4 Pro (2026) | Unspecified | 14 May, 2026
| [[204]](https://www.erdosproblems.com/204) | 🟢 Adenwalla (2025) | Aristotle | 15 Mar, 2026
| [[206]](https://www.erdosproblems.com/206) | 🟢 Kovač (2024) | Aristotle | 28 Apr, 2026
| [[209]](https://www.erdosproblems.com/209) | 🟢 Escudero (2016) | AxiomProver | 19 Jun, 2026
| [[214]](https://www.erdosproblems.com/214) | 🟢 Juhász (1979) | Aristotle | 2 Mar, 2026
| [[221]](https://www.erdosproblems.com/221) | 🟢 Ruzsa (1972) + van Doorn (2025) | Aristotle | 31 Jan, 2026
| [[226]](https://www.erdosproblems.com/226) | 🟢 Sato and Rankin (1974) | Aristotle | 29 Dec, 2025
| [[229]](https://www.erdosproblems.com/229) | 🟢 Barth and Schneider (1972) | Aristotle | 28 Dec, 2025
| [[231]](https://www.erdosproblems.com/231) | 🟢 Keränen (1992) | Aristotle | 9 May, 2026
| [[237]](https://www.erdosproblems.com/237) | 🟢 Chen and Ding (2022) | Aristotle | 4 Apr, 2026
| [[246]](https://www.erdosproblems.com/246) | 🟢 Birch (1959) | Aristotle | 28 Dec, 2025
| [[258]](https://www.erdosproblems.com/258) | 🟢 GPT-5.4 Pro (2026) | Aristotle | 14 Apr, 2026
| [[259]](https://www.erdosproblems.com/259) | 🟢 Chen and Ruzsa (1999) | Aristotle | 21 Apr, 2026
| [[268]](https://www.erdosproblems.com/268) | 🟢 Kovač (2024) | Aristotle | 13 Apr-26 May, 2026
| [[275]](https://www.erdosproblems.com/275) | 🟢 Balister, Bollobas, Morris, Sahasrabudhe, and Tiba (2020) | Aristotle | 20 Jan, 2026
| [[280]](https://www.erdosproblems.com/280) | 🟢 Cambie (2025) | Aristotle | 18 Apr, 2026
| [[281]](https://www.erdosproblems.com/281) | 🟢 GPT-5.2 Pro (2026) | Aristotle, Gemini 3 Flash | 19 Jan, 2026
| [[283]](https://www.erdosproblems.com/283) | 🟡 van Doorn (2025) | Aristotle | 28 Mar, 2026
| [[283]](https://www.erdosproblems.com/283) | 🟢 Barreto, GPT-5.5 Pro, and Price (2026) | Claude Opus 4.7, GPT-5.5 Pro | 6 May, 2026
| [[290]](https://www.erdosproblems.com/290) | 🟢 van Doorn (2024) | Aristotle | 14 Jan, 2026
| [[296]](https://www.erdosproblems.com/296) | 🟢 Hunter and Sawhney | Aristotle | 22 Apr-26 May, 2026
| [[303]](https://www.erdosproblems.com/303) | 🟢 Brown and Rödl (1991) | Seed Prover | 21 Dec, 2025
| [[314]](https://www.erdosproblems.com/314) | 🟢 Lim and Steinerberger (2024) | Aristotle | 1 Apr, 2026
| [[315]](https://www.erdosproblems.com/315) | 🟢 Kamio (2025) | Aristotle | 31 Jan, 2026
| [[328]](https://www.erdosproblems.com/328) | 🟢 Nešetřil and Rödl (1985) | AxiomProver | 19 Jun, 2026
| [[330]](https://www.erdosproblems.com/330) | 🟢 GPT-5.5 Pro and Turturean (2026) | Codex, GPT-5.5 Pro | 5 May, 2026
| [[331]](https://www.erdosproblems.com/331) | 🟢 Ruzsa | Aristotle | 31 Jan, 2026
| [[337]](https://www.erdosproblems.com/337) | 🟢 Ruzsa and Turjányi (1985) | Aristotle | 10 Dec, 2025
| [[350]](https://www.erdosproblems.com/350) | 🟢 Ryavec (1974) | Aristotle, GPT | 25 Nov, 2025
| [[351]](https://www.erdosproblems.com/351) | 🟢 Barreto, GPT-5.5 Pro, and Price (2026) | Claude Opus 4.7, GPT-5.5 Pro | 6 May, 2026
| [[353]](https://www.erdosproblems.com/353) | 🟢 Kovač and Predojević (2024) + Koizumi (2025) | Aristotle | 19-20 Jun, 2026
| [[355]](https://www.erdosproblems.com/355) | 🟢 van Doorn and Kovač (2025) (almost the entirety) | Aristotle, Gemini 3 | 30 Jan-13 Mar, 2026
| [[363]](https://www.erdosproblems.com/363) | 🟢 Ulas (2005) | Aristotle | 10 Mar, 2026
| [[367]](https://www.erdosproblems.com/367) | 🟡 van Doorn and Tao (2025) | Aristotle | 22 Nov, 2025
| [[368]](https://www.erdosproblems.com/368) | 🟡 Pólya (1918) | Aristotle | 17 Feb, 2026
| [[369]](https://www.erdosproblems.com/369) | 🟢 GPT and Yang (2026) | Aristotle | 27 Mar, 2026
| [[370]](https://www.erdosproblems.com/370) | 🟢 Steinerberger (2025) | Aristotle, GPT | 24 Nov, 2025
| [[392]](https://www.erdosproblems.com/392) | 🟢 Tao (2026) | Various | 6 Jan-23 Feb, 2026
| [[399]](https://www.erdosproblems.com/399) | 🟢 Barfield (2025) | Codex | Feb 2026
| [[403]](https://www.erdosproblems.com/403) | 🟢 Unspecified | AxiomProver | 19 Jun, 2026
| [[418]](https://www.erdosproblems.com/418) | 🟢 Browkin and Schinzel (1995) | Aristotle, GPT | 22 Nov, 2025
| [[419]](https://www.erdosproblems.com/419) | 🟢 Sawhney (2025) | Aristotle | 31 Jan, 2026
| [[425]](https://www.erdosproblems.com/425) | 🟢 Erdős (1938) | Aristotle, GPT | 5-17 May, 2026
| [[426]](https://www.erdosproblems.com/426) | 🟢 Bradač and Christoph (2024) | Aristotle | 20 Apr, 2026
| [[427]](https://www.erdosproblems.com/427) | 🟢 Pilatte | Aristotle | 26 Apr, 2026
| [[429]](https://www.erdosproblems.com/429) | 🟢 Weisenberg (2024) | Aristotle | 29 Jan, 2026
| [[433]](https://www.erdosproblems.com/433) | 🟢 Dixmier (1990) | Aristotle, Claude Opus 4.8, Claude Sonnet 4.6, Gemini 3 Flash, Gemini 3.1 Pro, Project Numina | 24 Feb-29 May, 2026
| [[434]](https://www.erdosproblems.com/434) | 🟢 Continued from [433] formalization | Aristotle, Claude Opus 4.8 | 24 Feb-29 May, 2026
| [[435]](https://www.erdosproblems.com/435) | 🟢 Cambie (2025) | Aristotle | 4 Feb, 2026
| [[441]](https://www.erdosproblems.com/441) | 🟡 Chen and Dai (2007) | AxiomProver | 19 Jun, 2026
| [[443]](https://www.erdosproblems.com/443) | 🟢 Hegyvári (2025) | Aristotle | 4 Feb, 2026
| [[447]](https://www.erdosproblems.com/447) | 🟢 Kleitman (1971) | Aristotle | 10 Feb, 2026
| [[453]](https://www.erdosproblems.com/453) | 🟢 Pomerance (1979) | Aristotle | 31 Jan, 2026
| [[459]](https://www.erdosproblems.com/459) | 🟢 Cambie (2026) | Aristotle | 11 Mar, 2026
| [[464]](https://www.erdosproblems.com/464) | 🟢 de Mathan (1980) | Aristotle | 21 Jun, 2026
| [[476]](https://www.erdosproblems.com/476) | 🟢 Alon, Nathanson, and Ruzsa (1995) | Aristotle | 31 Dec, 2025
| [[480]](https://www.erdosproblems.com/480) | 🟢 Chung and Graham (1984) | Aristotle | 28 Nov, 2025
| [[481]](https://www.erdosproblems.com/481) | 🟢 Barreto (2025) | Aristotle, Claude | 1 Dec, 2025
| [[484]](https://www.erdosproblems.com/484) | 🟢 Erdős, Sárközy, and Sós (1989) | Aristotle | 15 Apr, 2026
| [[487]](https://www.erdosproblems.com/487) | 🟢 Kleitman (1971) | Aristotle | 16 Feb, 2026
| [[490]](https://www.erdosproblems.com/490) | 🟢 Szemerédi (1976) | Aristotle, GPT-5.5 Pro | 17 May, 2026
| [[497]](https://www.erdosproblems.com/497) | 🟢 Kleitman (1969) | Aristotle | 4 Feb, 2026
| [[498]](https://www.erdosproblems.com/498) | 🟢 Kleitman (1965) | Aristotle, Claude Opus, Gemini Flash, Gemini Pro | Jan 27, 2026
| [[499]](https://www.erdosproblems.com/499) | 🟢 Marcus and Minc (1962) | Aristotle | 29 Nov, 2025
| [[502]](https://www.erdosproblems.com/502) | 🟢 Petrov and Pohoata (2021) | Aristotle | 2 Feb, 2026
| [[505]](https://www.erdosproblems.com/505) | 🟢 Kahn and Kalai (1993) | Aristotle | 2 Feb, 2026
| [[512]](https://www.erdosproblems.com/512) | 🟢 McGehee, Pigno, and Smith (1981) | Aristotle | 22 Jun, 2026
| [[519]](https://www.erdosproblems.com/519) | 🟢 Atkinson (1961) | Aristotle | 19 Apr, 2026
| [[537]](https://www.erdosproblems.com/537) | 🟢 Ruzsa | Aristotle | 6 Feb, 2026
| [[540]](https://www.erdosproblems.com/540) | 🟢 Szemerédi (1970) | Aristotle | 15 Apr, 2026
| [[541]](https://www.erdosproblems.com/541) | 🟢 Grynkiewicz (2011) | Aristotle, GPT | 30 Dec, 2025
| [[582]](https://www.erdosproblems.com/582) | 🟢 Folkman (1970) | Aristotle | 5 Feb, 2026
| [[603]](https://www.erdosproblems.com/603) | 🟢 Chojecki and GPT-5.4 Pro (2026) | Codex, GPT-5.5 | 17 May, 2026
| [[613]](https://www.erdosproblems.com/613) | 🟢 Pikhurko (2001) | GPT Pro | 4 Nov, 2025
| [[618]](https://www.erdosproblems.com/618) | 🟢 Alon | Aristotle | 8 Feb, 2026
| [[621]](https://www.erdosproblems.com/621) | 🟢 Norin and Sun (2016) | Aristotle | 19 Apr, 2026
| [[639]](https://www.erdosproblems.com/639) | 🟢 Keevash and Sudakov (2004) | Aristotle | 3 May, 2026
| [[645]](https://www.erdosproblems.com/645) | 🟢 Brown and Landman (1999) | Aristotle, GPT | 23 Nov, 2025
| [[646]](https://www.erdosproblems.com/646) | 🟢 Berend (1997) | Aristotle | 27 Feb, 2026
| [[648]](https://www.erdosproblems.com/648) | 🟢 Cambie (2025) | Aristotle | 4 Feb, 2026
| [[649]](https://www.erdosproblems.com/649) | 🟢 Tong; Sampaio | Aristotle, GPT | 7 Feb-1 Jun, 2026
| [[650]](https://www.erdosproblems.com/650) | 🟢 He, Li and Tang (2026) | Aristotle | 6-8 Mar, 2026
| [[658]](https://www.erdosproblems.com/658) | 🟢 Solymosi (2004) | Aristotle | 20 Apr, 2026
| [[659]](https://www.erdosproblems.com/659) | 🟢 Gemini and Grayzel (2026) | Aristotle | 14 Jan, 2026
| [[666]](https://www.erdosproblems.com/666) | 🟢 Chung (1992), Brouwer, Dejter, and Thomassen (1993) | Aristotle | 6 Feb, 2026
| [[678]](https://www.erdosproblems.com/678) | 🟢 Cambie (2025) | Aristotle | 7 Jan, 2026
| [[692]](https://www.erdosproblems.com/692) | 🟢 Cambie (2025) | Aristotle | 2 Apr, 2026
| [[694]](https://www.erdosproblems.com/694) | 🟢 GPT-5.5 Pro (2026) | Aristotle, Claude Code, Claude Opus 4.7, GPT-5.5 Pro | 3 May-5 Jun, 2026
| [[698]](https://www.erdosproblems.com/698) | 🟢 Bergman (2011) | Aristotle | 16 Jan, 2026
| [[707]](https://www.erdosproblems.com/707) | 🟢 Hall (1947) | GPT | 23 Nov, 2025
| [[716]](https://www.erdosproblems.com/716) | 🟢 Ruzsa and Szemerédi (1978) | Aristotle | 20 Jun, 2026
| [[728]](https://www.erdosproblems.com/728) | 🟢 Pomerance (2026) | Aristotle | 22 Jan, 2026
| [[750]](https://www.erdosproblems.com/750) | 🟢 Chojecki and GPT-5.5 Pro (2026) | Claude Code, Claude Opus 4.7, GPT-5.5 Pro | 4 May, 2026
| [[751]](https://www.erdosproblems.com/751) | 🟢 Bondy and Vince (1998) | GPT-5.2-Codex, GPT-5.2 Thinking | 27 Jan, 2026
| [[753]](https://www.erdosproblems.com/753) | 🟢 Alon (1992) | Aristotle | 14 Apr, 2026
| [[756]](https://www.erdosproblems.com/756) | 🟢 Bhowmick (2024) | Aristotle | 15 Mar, 2026
| [[760]](https://www.erdosproblems.com/760) | 🟢 Alon, Krivelevich, and Sudakov (1997) | Aristotle | 23 Apr-2 Jun, 2026
| [[762]](https://www.erdosproblems.com/762) | 🟢 Steiner (2024) | Aristotle, Claude Opus 4.7, GPT | 8 Feb-3 Jun, 2026
| [[765]](https://www.erdosproblems.com/765) | 🟢 Aigner and Ziegler (1998) | Aristotle | 16 May, 2026
| [[775]](https://www.erdosproblems.com/775) | 🟢 Gao (2025) | Aristotle | 19 Apr-3 Jun, 2026
| [[785]](https://www.erdosproblems.com/785) | 🟡 Narkiewicz (1959/60) + 🟢 Ruzsa (2015) | Aristotle | 6 Mar, 2026
| [[788]](https://www.erdosproblems.com/788) | 🟡 GPT-5.2 Pro (2026) | Aristotle | 20 Jan, 2026
| [[794]](https://www.erdosproblems.com/794) | 🟢 Harris (2025) | Aristotle | 5 Feb, 2026
| [[798]](https://www.erdosproblems.com/798) | 🟢 Alon (1991) | Aristotle | 8 May, 2026
| [[818]](https://www.erdosproblems.com/818) | 🟢 Solymosi (2009) | Aristotle | 25 Apr, 2026
| [[835]](https://www.erdosproblems.com/835) | 🟡 Likely folklore | AlphaProof | 26 Dec, 2025
| [[844]](https://www.erdosproblems.com/844) | 🟢 Chvátal (1974) + Weisenberg | Aristotle | 26 Apr, 2026
| [[845]](https://www.erdosproblems.com/845) | 🟢 van Doorn and Everts (2025) | Aristotle | 8 Jan, 2026 (one form of result), 21 Jan, 2026 (second form)
| [[848]](https://www.erdosproblems.com/848) | 🟢 Sawhney (2025) | Aristotle, Claude, GPT-5.2 | 28 Jan, 2026
| [[862]](https://www.erdosproblems.com/862) | 🟢 Saxton and Thomason (2015) | Aristotle | 21 Jan, 2026
| [[867]](https://www.erdosproblems.com/867) | 🟢 Freud (1993) | Aristotle | 7 Apr, 2026
| [[897]](https://www.erdosproblems.com/897) | 🟢 Erdős and Wirsing (1975) | Aristotle | 27 Nov, 2025
| [[898]](https://www.erdosproblems.com/898) | 🟢 Barrow and Mordell (1937) | Aristotle, Gemini 3 Flash | 28 Jan, 2026
| [[904]](https://www.erdosproblems.com/904) | 🟢 Bollobás and Nikiforov (2005) | Aristotle | 18 Apr, 2026
| [[905]](https://www.erdosproblems.com/905) | 🟢 Khadžiivanov and Nikiforov (1979) | Aristotle, GPT-5.4 | 7 Apr, 2026
| [[907]](https://www.erdosproblems.com/907) | 🟢 de Bruijn (1951) | Aristotle | 7 Apr, 2026
| [[914]](https://www.erdosproblems.com/914) | 🟢 Kierstead and Kostochka (2008) | Aristotle | 15 Apr, 2026
| [[923]](https://www.erdosproblems.com/923) | 🟢 Rödl (1977) | Aristotle | 20 Apr, 2026
| [[927]](https://www.erdosproblems.com/927) | 🟢 Spencer (1971) | Aristotle | 5 Jun, 2026
| [[947]](https://www.erdosproblems.com/947) | 🟢 Mirsky and Newman + Davenport and Rado | Aristotle, GPT | 2 Feb, 2026
| [[958]](https://www.erdosproblems.com/958) | 🟢 Clemen, Dumitrescu, and Liu (2025) | Seed Prover 1.5 | 19 Dec, 2025
| [[964]](https://www.erdosproblems.com/964) | 🟢 Eberhard (2025) | Antigravity, Aristotle, Gemini | 14 Feb, 2026
| [[967]](https://www.erdosproblems.com/967) | 🟢 Yip (2025) | Aristotle | 19 Dec, 2025
| [[974]](https://www.erdosproblems.com/974) | 🟢 Tijdeman (1966) | Aristotle | 27 Apr, 2026
| [[986]](https://www.erdosproblems.com/986) | 🟡 Bradač (2026) | Trellis | 10 Jun, 2026
| [[990]](https://www.erdosproblems.com/990) | 🟢 OpenAI internal model (2026) | GPT-5.4 Pro | 10 Apr, 2026
| [[997]](https://www.erdosproblems.com/997) | 🟢 OpenAI internal model (2026) | Aristotle | 1 Apr, 2026
| [[1000]](https://www.erdosproblems.com/1000) | 🟢 Haight | Aristotle, GPT | 28 Dec, 2025
| [[1007]](https://www.erdosproblems.com/1007) | 🟢 House (2013) | Aristotle | 19 Jan, 2026
| [[1008]](https://www.erdosproblems.com/1008) | 🟢 Conlon, Fox, and Sudakov (2014) | Aristotle | 17 Jan, 2026
| [[1022]](https://www.erdosproblems.com/1022) | 🟢 KoishiChan (2025) | Aristotle | 22 Jan, 2026
| [[1023]](https://www.erdosproblems.com/1023) | 🟢 Kleitman (1971) | Aristotle | 10 Feb, 2026
| [[1028]](https://www.erdosproblems.com/1028) | 🟢 Erdős (1963); Erdős and Spencer (1971) | Aristotle | 19 Jan, 2026
| [[1034]](https://www.erdosproblems.com/1034) | 🟢 Ma and Tang (2025) | Aristotle | 4 Dec, 2025
| [[1036]](https://www.erdosproblems.com/1036) | 🟢 Shelah (1998) | Aristotle | 20 Jan, 2026
| [[1037]](https://www.erdosproblems.com/1037) | 🟢 Cambie, Chan, and Hunter (2025) | Aristotle | 19 Jan, 2026
| [[1039]](https://www.erdosproblems.com/1039) | 🟡 GPT-5.5 Pro (2026) | Codex, GPT-5.5 | 15 May, 2026
| [[1044]](https://www.erdosproblems.com/1044) | 🟢 Tang (2026) | Aristotle | 28 Apr, 2026
| [[1048]](https://www.erdosproblems.com/1048) | 🟢 Pommerenke (1961) | Aristotle | 27 Jan, 2026
| [[1067]](https://www.erdosproblems.com/1067) | 🟢 Bowler and Pitz (2024) | Aleph Prover, Aristotle | 28 Jan, 2026
| [[1071]](https://www.erdosproblems.com/1071) | 🟢 Danzer; Alexeev (2026) | Aleph Prover, Aristotle, GPT | 29 Jan, 2026 (second part); 12 Feb, 2026 (first part)
| [[1080]](https://www.erdosproblems.com/1080) | 🟢 De Caen and Székely (1992) | Aristotle | 28 Dec, 2025
| [[1095]](https://www.erdosproblems.com/1095) | 🟡 Konyagin (1999) | Aristotle | 20 Jun, 2026
| [[1098]](https://www.erdosproblems.com/1098) | 🟢 Neumann (1976) | Aristotle | 25 Apr, 2026
| [[1102]](https://www.erdosproblems.com/1102) | 🟢 van Doorn and Tao (2025) | Aristotle | 23 Feb, 2026
| [[1121]](https://www.erdosproblems.com/1121) | 🟢 Goodman and Goodman (1945) | Aristotle | 16 Apr, 2026
| [[1125]](https://www.erdosproblems.com/1125) | 🟢 Laczkovich (1984) | Aristotle | 11 Apr, 2026
| [[1126]](https://www.erdosproblems.com/1126) | 🟢 de Bruijn (1966) | Aristotle | 27 Feb, 2026
| [[1134]](https://www.erdosproblems.com/1134) | 🟢 Unspecified | AxiomProver | 19 Jun, 2026
| [[1136]](https://www.erdosproblems.com/1136) | 🟢 Müller (2011) | Aristotle | 19 Apr, 2026
| [[1138]](https://www.erdosproblems.com/1138) | 🟢 Cheri, Kumrawat, and Sunder (2026) | Aristotle | 4 May, 2026
| [[1141]](https://www.erdosproblems.com/1141) | 🟢 OpenAI internal model (2026) | GPT-5.4 Pro | 11 Apr, 2026
| [[1148]](https://www.erdosproblems.com/1148) | 🟢 Chojecki (2026) | Claude Opus 4.6, Gemini 3.1, GPT-5.4, UlamAI Prover | 17 Mar, 2026
| [[1151]](https://www.erdosproblems.com/1151) | 🟢 Chojecki (2026) (main part) | Codex, GPT | 6 May, 2026
| [[1187]](https://www.erdosproblems.com/1187) | 🟢 Trivial (second part) | Codex, GPT-5.5 | 12 May, 2026
| [[1190]](https://www.erdosproblems.com/1190) | 🟢 Boon Suan Ho and GPT-5.4 Pro (2026) | Unspecified | 14 May, 2026
| [[1193]](https://www.erdosproblems.com/1193) | 🟢 Trivial | Aristotle | 13 Apr, 2026
| [[1196]](https://www.erdosproblems.com/1196) | 🟢 GPT-5.4 Pro (2026) | Gauss | 16 Apr, 2026

<a id="sect-2c"></a>
### 2(c). Rewriting

| Problem | AI systems | Date | Argument to rewrite |
| ------- | ---------- | ---- | ------------------- |
| [[281]](https://www.erdosproblems.com/281) | Gemini 3 Pro, GPT-5.2 Pro | 17 Jan, 2026 | 🟢 GPT-5.2 Pro (2026)
| [[392]](https://www.erdosproblems.com/392) | GPT-5.2 Thinking | 27 Feb, 2026 | 🟢 Tao (2026)
| [[457]](https://www.erdosproblems.com/457) | GPT-5.2 Thinking | 3 Mar, 2026 | 🟢 Tao (2026) (extension of problem)
| [[543]](https://www.erdosproblems.com/543) | GPT-5.2 Thinking | 23 Jan, 2026 | 🟢 GPT-5.2 Pro (2026)
| [[728]](https://www.erdosproblems.com/728) | Aristotle, GPT-5.2 Thinking | 5-7 Jan, 2026 | 🟢 Aristotle and GPT-5.2 Pro (2026)
| [[783]](https://www.erdosproblems.com/783) | GPT-5.2 Thinking | 24 Jan, 2026 | 🟡 GPT-5.2 (2026)
| [[783]](https://www.erdosproblems.com/783) | GPT-5.2 Thinking | 21 Feb, 2026 | 🟡 Tao (2026)
| [[846]](https://www.erdosproblems.com/846) | GPT-5.2 Thinking | 25 Feb, 2026 | 🟢 DeepMind prover agent (2026)
| [[1039]](https://www.erdosproblems.com/1039) | GPT-5.5 Thinking | 8 May, 2026 | 🟡 GPT-5.5 Pro (2026)
| [[1196]](https://www.erdosproblems.com/1196) | GPT-5.4 Thinking | 20 Apr, 2026 | 🟢 Tao (2026)

<a id="sect-2d"></a>
### 2(d). Computation

| Problem | AI systems | Date | Computation |
| ------- | ---------- | ---- | ----------- |
| [[396]](https://www.erdosproblems.com/396) | Claude Opus 4.6, Gemini 3.1 Deep Think, GPT-5.4 Pro | 23 Mar-4 Apr, 2026 | OEIS sequence
| [[513]](https://www.erdosproblems.com/513) | GPT-5.2 Pro | 12 Feb, 2026 | Numerical certificate
| [[650]](https://www.erdosproblems.com/650) | AlphaEvolve | 7 Mar, 2026 | Numerical optimization
