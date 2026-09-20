1. **Critical — Section 4.3 table, Cruz e Sousa vs. genuine control**
   - **Quote:** “Cruz e Sousa (4 psy books vs. 2 ctrl) | vs. genuine control | 0.300 (15) | 0.200 (15) | 0.700 (15)”
   - **Problem:** Two of the three reported p-values are plainly wrong relative to the supplied JSON. The exact book-level values are:
     - Burrows’ Delta: **0.266666...**, which may reasonably be rounded to **0.267**, not **0.300**.
     - Cosine: **0.266666...**, not **0.200**.
     - Stylometric: **0.266666...**, not **0.700**.
     
     This is not a rounding issue; it is a serious transcription or table-generation failure in a central primary-results table. It directly undermines the draft’s claim that “Every number below is traceable to `results/statistical_summary.json`.”

2. **Critical — Section 4.2 falsely says all chunk-level tests are significant**
   - **Quote:** “all remain nominally ‘significant’ for the same pseudoreplication reasons already discussed”
   - **Problem:** This is contradicted by the JSON. Several exploratory chunk-level tests are not nominally significant:
     - Castro Alves, psychographed vs. genuine control, cosine: **p = 0.199**
     - Castro Alves, psychographed vs. baseline, cosine: **p = 0.0654**
     - Cruz e Sousa, psychographed vs. genuine control, cosine: **p = 0.1848**
     
     One could say that many chunk-level results are significant and methodologically invalid as confirmatory evidence; one cannot say “all” are significant.

3. **Major — Section 3.3 misstates the range of exact enumeration sizes**
   - **Quote:** “When the number of possible book-to-role assignments is small enough (**2 to 495 across the tests in this paper**)”
   - **Problem:** The JSON contains exact-enumeration counts of **10, 15, 20, 35, 56, 165, 286, and 495**. There is no test with two possible assignments. If “2” refers to books in a group, the sentence says “possible book-to-role assignments,” so it is still wrong. This is minor numerically but troubling because the paper repeatedly emphasizes exact combinatorial resolution.

4. **Major — Section 4.4 calls p = .050 a result crossing a “p < .05” threshold**
   - **Quote:** “Two individual decisive-test comparisons now cross the conventional raw p<0.05 threshold — Castro Alves cosine (p = 0.050, right at the boundary) …”
   - **Problem:** A p-value of exactly **0.050** does not satisfy **p < .05**. The JSON gives Castro Alves cosine **p = 0.05** exactly. The correct wording is “equals the conventional .05 threshold” or, better, avoid threshold rhetoric altogether. The draft partly acknowledges the boundary in parentheses but retains the mathematically false “cross” claim.

5. **Major — The paper’s multiple-comparison family is selectively constructed around the desired André Luiz result**
   - **Quote:** “Benjamini-Hochberg FDR correction is applied across all 15 primary book-level p-values we report as evidence”
   - **Problem:** This is not “all” book-level primary tests in the JSON. The draft includes only:
     - 9 decisive role-swap tests; and
     - 6 vs.-baseline tests for Emmanuel and André Luiz.
     
     It excludes the book-level psychographed-vs-genuine-control and psychographed-vs-baseline tests for Castro Alves, Cruz e Sousa, and Humberto de Campos—even though the Humberto psychographed-vs-genuine finding is repeatedly called “fully load-bearing,” “robust,” and one of the two “genuinely supported” conclusions. The JSON supplies no FDR-adjusted values for those omitted tests. A correction family that excludes a featured headline result cannot be called the paper’s “full primary claim family” without a pre-specified and defensible rationale.

6. **Major — “The only result … that survives FDR correction” is misleadingly singular**
   - **Quote:** “The only result in the entire 15-test family that survives FDR correction is André Luiz’s vs.-baseline test”
   - **Problem:** There are three André Luiz metric-specific tests, each with raw **p = 0.006993...** and FDR-adjusted **p = 0.034965...**. Since the manuscript treats Burrows’ Delta, cosine, and stylometric distance as separate tests elsewhere, there are technically three FDR-surviving metric results, not one. Calling the collection an “André Luiz test” might be acceptable if the three metrics were predeclared as a single composite inferential claim—but no such composite was defined or tested.

7. **Major — The “stable” André Luiz narrative is contradicted by the values quoted in the manuscript itself**
   - **Quote:** “its p-value has moved in one direction only” and “p = 0.015 → 0.030 → 0.007 raw”
   - **Problem:** The sequence **.015 → .030 → .007** is not movement in one direction. It first becomes less significant, then more significant. The claim of monotonic corroboration is therefore internally false even before asking whether the earlier-revision values are documented. This is a textbook example of post hoc narrative-fitting to an appealing result.

8. **Major — Historical revision trajectories and prior p-values are not traceable to the provided ground truth**
   - **Quote:** “the decisive-test direction tally has been 8/9 … → 4/9 … → 6/9”; “the smallest decisive-test p-value was 0.111”; “p = 0.015 → 0.030 → 0.007”; “66 → 286 possible assignments”
   - **Problem:** The supplied `statistical_summary.json` contains only the current analysis. It supports the current 6/9 tally, current p-values, and current 286 assignments, but not prior revisions, prior tallies, prior baseline configurations, prior p-values, or the claimed previous 66 assignments. These claims may exist in archived files, but they are not traceable to the asserted raw record. The opening assurance that every number is traceable to the JSON is demonstrably untrue.

9. **Major — The paper repeatedly treats non-significant results as affirmative support for H0**
   - **Quote:** “Humberto de Campos’s psychographed text is unlike his own genuine writing but statistically indistinguishable from Chico Xavier’s baseline (the pattern H0 predicts)”
   - **Problem:** Failure to reject a difference from the baseline is not evidence of equivalence, indistinguishability, or “the pattern H0 predicts.” The relevant Humberto vs.-baseline p-values are **.057, .314, and .514**, based on only **4 psychographed books versus 3 baseline documents** and 35 possible assignments. No equivalence margin, non-inferiority analysis, Bayes factor, or power calculation is provided. The defensible statement is merely that these tests did not reject the null under the chosen design.

10. **Major — The André Luiz result does not distinguish H1 from plausible non-H1 alternatives**
    - **Quote:** “consistent with, though not proof of, an independent stylistic source for that persona”
    - **Problem:** André Luiz differs from a baseline comprising spoken TV interview, personal letters, and interview-book answers. André Luiz consists of literary psychographed books. A significant distance from this heterogeneous, non-genre-matched baseline can reflect genre, medium, editorial intervention, chronology, topic, narrative voice, corpus curation, or feature/model behavior. It does not particularly privilege an “independent stylistic source,” and it certainly does not support poly-authorship as formulated in H1, which requires closeness to independently known authorship. The paper acknowledges genre mismatch but then rhetorically promotes the André Luiz result far beyond what the design can discriminate.

11. **Major — H1 and H0 are presented as a false dichotomy**
    - **Quote:** “two competing hypotheses” followed by H1 poly-authorship versus H0 subconscious mimicry / single attractor.
    - **Problem:** The observed space is not exhausted by these hypotheses. Other serious explanations include deliberate or unconscious genre-shifting by Chico Xavier, editorial normalization, varying source quality and OCR artifacts, temporal change in Xavier’s style, differential translation/transcription practices, topic and register effects, and stylistic imitation without independent authorship. In particular, “not baseline-like” is not evidence for “independent author.” The inferential leap from a distance test to metaphysically charged authorship hypotheses is not methodologically disciplined.

12. **Major — “Robust,” “fully stable,” and “well-powered” are unsupported descriptions of the Humberto result**
    - **Quote:** “the study’s one fully stable, well-powered finding” and “robustly significant on all three metrics”
    - **Problem:** The result is based on **4 psychographed books against 8 genuine-control books**. Exact enumeration makes the p-value conditional on the exchangeability scheme; it does not make an n=4 psychographed corpus “well-powered.” Nor does three-metric agreement provide three independent confirmations: the paper correctly says the metrics are correlated, then repeatedly uses their joint significance as rhetorical reinforcement. Further, this comparison is severely vulnerable to the acknowledged genre/register and corpus-composition confounds. “Stable across revisions” means only that the baseline was not involved; it does not validate the comparison.

13. **Major — The exact permutation p-values are described as stronger than they are**
    - **Quote:** “the reported p-value is exact, not approximate”
    - **Problem:** Exact enumeration gives an exact p-value for the specified permutation procedure, statistic, exchangeability assumption, corpus, preprocessing, and post hoc analysis plan. It does not cure invalid exchangeability caused by genre, period, source, or document-level heterogeneity, and it does not protect against researcher degrees of freedom across corpus revisions and analytic choices. The prose risks equating computational exactness with substantive validity.

14. **Major — PERMANOVA interpretation does not adequately acknowledge dispersion and pseudoreplication**
    - **Quote:** “Both PERMANOVA tests reject the null of no group structure”
    - **Problem:** The draft notes chunk dependence, which is good, but omits a core PERMANOVA limitation: the test can respond to differences in multivariate dispersion as well as differences in group centroids. Given radically unequal group sizes—e.g., 2 psychographed Castro Alves chunks, 7 Cruz e Sousa chunks, 593 André Luiz chunks, 404 Humberto control chunks—and extreme genre/register imbalance, this is not a peripheral concern. The enormous pseudo-F values (**492,993.2** and **662,850.5**) should provoke methodological scrutiny, not merely be presented as expected “group structure.”

15. **Major — The clustering results are overinterpreted**
    - **Quote:** “consistent with heavily overlapping surface signatures”
    - **Problem:** The JSON provides silhouette scores and Davies–Bouldin indices, not a direct test of “overlap” or of stylistic similarity. A silhouette of **−0.0175** in embedding space and **0.0625** in stylometric space indicates poor separation for the imposed labels under those representations; it does not establish that groups share “heavily overlapping surface signatures,” much less that this has implications for H0 or H1. The prose transforms generic clustering diagnostics into a substantive stylistic claim.

16. **Major — Key corpus and preprocessing claims are unverified by the supplied record**
    - **Quote:** “106 letters (85 chunks),” “85,250 words,” “114 turns → 18 chunks,” “20,295 words → 20 chunks,” “41 books/documents,” “5000 permutations,” “60 most frequent function words,” and the detailed title-level bibliography.
    - **Problem:** The JSON supports only aggregate group counts and book counts: 123 baseline chunks and 3 baseline documents; total 1,874 chunks; the stated group sizes; and author-level book counts. It does not support the component baseline chunk split, word counts, turn counts, exact title lists, source provenance, chunk-window details beyond the methodological note, 5,000 permutations, 60 function words, or the claimed total-document construction history. These may be true, but they are not traceable to the alleged ground-truth record.

17. **Major — The manuscript’s strongest substantive wording is inconsistent with its own limitations**
    - **Quote:** “two findings we consider genuinely supported by this analysis” and “the one baseline-dependent result we now trust”
    - **Problem:** The paper simultaneously admits that its baseline is only three documents, is modality- and register-mismatched, was partly heuristic speaker-separation, and has changed results sharply between revisions. It then treats André Luiz as an exception based on a post hoc story about its p-value trajectory—one that is not actually monotonic. This is exactly the kind of selective trust the manuscript claims to warn against. A p=.007 FDR-adjusted to .035 in a small, evolving, post hoc corpus is a result worth reporting cautiously, not a result one can “trust” as robust evidence of an independent source.

18. **Minor — The current numerical statements that are correct should be made more precise**
    - **Quote:** “Humberto de Campos … p = 0.002–0.004”; “André Luiz … p = 0.007 … p = 0.035”; “Emmanuel … p = 0.018 raw, p = 0.054 adjusted.”
    - **Problem:** These are broadly faithful roundings:
      - Humberto genuine-control: .002020, .002020, .004040;
      - André Luiz: .006993 raw and .034965 adjusted;
      - Emmanuel cosine/stylometric: .017857 raw and .053571 adjusted.
      
      But the draft should report enough precision to preserve the discrete exact-enumeration context—for example, p=.00699 rather than .007—and should avoid implying continuous “wide margins” when values are constrained by 286 or 56 permutations. This is especially relevant where conclusions hinge on p-values near .05.

19. **Major — The prose has conspicuous AI-generated/pseudo-academic tells**
    - **Quote:** “fully load-bearing,” “the strongest baseline-dependent result so far,” “a much cleaner result,” “the honest finding,” “genuinely supported,” “the binding constraint,” and repeated assertions that this revision is “the first” to do something.
    - **Problem:** This is promotional and self-validating language, not neutral scientific prose. “Load-bearing” appears repeatedly as an imported metaphor rather than a technical category. “Cleaner,” “trustworthy,” “honest,” and “genuinely supported” ask the reader to endorse the authors’ confidence rather than evaluate the methods. The draft also repeatedly restates the same conclusion in triadic form—two solid findings, a third unresolved finding; three baseline configurations; three documents; three metrics—giving it the cadence of generated argumentative prose rather than a concise research report.

20. **Major — The extensive LLM-review narrative is methodologically irrelevant and rhetorically suspicious**
    - **Quote:** “A four-model adversarial review (OpenAI, Google, xAI, DeepSeek, run independently via OpenRouter) converged…” and “asking four independent LLMs … for bibliographic leads”
    - **Problem:** Naming commercial AI providers and OpenRouter does not validate the statistical correction or the bibliographic search. It reads as vendor-name signaling. LLM convergence is not independent peer review, and LLM-generated bibliographic leads are not evidence that sources were correctly identified, transcribed, or licensed. If these details remain, they require reproducible prompts, model versions, dates, retrieval conditions, complete outputs, verification protocol, and a clear explanation of why they matter. Otherwise, remove them from the scholarly narrative.

21. **Major — Citation practice is incomplete and only partly APA-compliant**
    - **Quote:** “Honnibal & Montani, 2017 — a software release note, not a peer-reviewed article; cited here as the standard reference for spaCy.”
    - **Problem:** The spaCy reference lacks a version and URL/repository location, which are normally necessary for software citation. The cited document’s bibliographic status and title should be checked rather than defended in prose. The actual multilingual MiniLM model used is not specifically cited; Reimers and Gurevych (2019) describe Sentence-BERT, not necessarily `paraphrase-multilingual-MiniLM-L12-v2` or its training data/model card. UMAP is in the references but not cited in the UMAP-results paragraph. Conversely, major empirical and historical claims about Xavier, Spiritism, corpus contents, publication dates, and genuine-author identities lack scholarly citations.

22. **Major — The references themselves advertise unverifiability**
    - **Quote:** “none is asserted here to avoid citing sources not verified in this session” and “text obtained from two independent PDF mirrors … not cross-checked against a physical edition.”
    - **Problem:** A paper cannot responsibly make strong claims about a highly contested historical corpus while explicitly declining to cite domain literature or verify key editions. The issue is not merely APA style. Corpus provenance is central to the inference: edition, transcription, editorial intervention, authenticity, dates, and source integrity can all alter stylometric conclusions. The Schubert entry also embeds a long methodological disclaimer in the reference list rather than documenting corpus acquisition and verification in a data/provenance appendix.

23. **Minor — The UMAP paragraph is ungrounded in the supplied numerical record**
    - **Quote:** “A UMAP projection … places Emmanuel, André Luiz, and psychographed Humberto de Campos … in one broad region”
    - **Problem:** No UMAP settings, random seed, distance choices, plot, cluster statistics, or source data are supplied in the JSON. The conclusion is therefore not auditable from the declared ground truth. Since UMAP is highly sensitive to hyperparameters and is visually seductive, it should be explicitly exploratory and accompanied by a reproducible figure and parameters—or omitted.

24. **Major — The conclusion overstates what the reported statistics establish**
    - **Quote:** “psychographed ‘André Luiz’ text is significantly distinct from Chico Xavier’s own documented voice”
    - **Problem:** The actual result is that, under three chosen feature/distance schemes and a book-role permutation design, the André Luiz corpus differs from the particular three-document Xavier baseline. “Chico Xavier’s own documented voice” implies a representative population-level construct that the study does not sample adequately. The baseline’s three documents span radically different registers but none is genre-matched literary prose of the relevant sort. This is not a semantic quibble; it is the central construct-validity problem.

**Overall verdict:** This draft is not ready to show a human co-author as a substantive manuscript, despite some commendable acknowledgment of pseudoreplication and genre limitations. It contains at least one central results-table error, a false claim that all exploratory tests are significant, a mathematically incorrect “p<.05” statement, and numerous historical/revision numbers that are not traceable to the supplied ground-truth JSON. More fundamentally, the inferential argument confuses non-rejection with evidence for H0 and treats distance from a small, register-mismatched baseline as suggestive evidence of independent authorship. The FDR family is selectively defined while headline Humberto claims sit outside it. Before circulation, the authors need a complete numerical audit, pre-specified claim and multiplicity families, a substantially more restrained interpretation, independently verified corpus provenance, and a rewrite removing promotional/LLM-centered rhetoric.