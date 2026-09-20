# Adversarial Peer Review: "Stylometric Evidence for Poly-Authorship in the Psychographic Corpus of Chico Xavier"

## VERACITY REVIEW

**1. [CRITICAL] Baseline chunk count discrepancy in Abstract vs. Table 1**
- Quote: "a 1971 televised-interview transcript (18 chunks), his complete published personal-letter collection, 1943–1964, 106 letters (85 chunks), and his own answers…in a 1968 published interview book (20 chunks)"
- Table 1 lists baseline chico_xavier as 123 chunks total; 18+85+20 = 123. This is internally consistent. HOWEVER, the abstract says the total is "1874 chunks, drawn from 41 books/documents" (Table 1). The JSON `n_chunks_total` is 1874. The table rows sum: 123+78+84+404+2+7+158+425+593 = 1874. ✓ No error here. Withdrawn as finding. Wait—recheck: 123+78=201; +84=285; +404=689; +2=691; +7=698; +158=856; +425=1281; +593=1874. ✓ Correct.

**2. [CRITICAL] André Luiz raw p-value claimed as "0.007 (286)" is exactly 2/286**
- Quote: "raw p = 0.007, all three metrics, out of 286 possible assignments"
- JSON: `andre_luiz.book_level_primary` → all three metrics `p_value: 0.006993006993006993`, `n_permutations_used: 286`. 0.00699 = 2/286. ✓ Matches. But the paper rounds to 0.007 in Section 4.3 table, and in Section 4.5 says "p = 0.015 → 0.030 → 0.007 raw across three successive baseline configurations." The 0.015 and 0.030 intermediate values are NOT traceable to the JSON—only the final 0.007 is recorded. This historical claim is unverifiable from the provided ground truth. **Flag as untraceable.**

**3. [CRITICAL] Humberto de Campos psychographed-vs-baseline Burrows' Δ p-value claimed as 0.057**
- Quote: "vs.-baseline: p = 0.057 Burrows' Δ, 0.314 cosine, 0.514 stylometric, n = 35 assignments"
- JSON: `humberto_de_campos.book_level_primary.burrows_delta.psychographed_vs_baseline.p_value: 0.05714285714285714` = 2/35. ✓
- Cosine: 0.3142857142857143 = 11/35. ✓
- Stylometric: 0.5142857142857142 = 18/35. ✓
All traceable. ✓

**4. [MAJOR] Emmanuel's "p = 0.018–0.054" range is true but hides the Burrows' Δ result being close to the FDR boundary**
- Quote: "Emmanuel's equivalent comparison (p = 0.018–0.054 raw) is suggestive but does not clear FDR correction."
- JSON: Burrows: 0.05357142857142857 (=3/56), Cosine: 0.017857142857142856 (=1/56), Stylometric: 0.017857 (=1/56). The range 0.018–0.054 is accurate but the Burrows p=0.054 is just above 0.05 and its FDR-adjusted value is 0.100—double the André Luiz adjusted value. The paper correctly reports this. ✓ Minor concern: "does not survive correction" is stated, consistency confirmed.

**5. [CRITICAL] Castro Alves book-level vs-genuine-control p-values claimed as 0.100 (10) in table but 0.300 in one Cruz cell**
- Table in Section 4.3 lists: Castro Alves vs. genuine control: all three = 0.100 (10). JSON: `castro_alves.book_level_primary.{burrows,cosine,stylometric}.psychographed_vs_genuine_control.p_value: 0.1`, `n_permutations_used: 10`. 0.1 = 1/10. ✓
- Cruz e Sousa Stylometric vs. genuine control: table says 0.700 (15). JSON: p=0.26666666666666666. **ERROR: the table reports 0.700 but the JSON says 0.267 (4/15).** This is a veracity failure. The Discussion at 4.4 doesn't mention this specific value, but the table itself is wrong.
- Also, the Cruz e Sousa Burrows vs. genuine control table value is 0.300, JSON says 0.26666666666666666. **ERROR: 0.300 ≠ 0.267.** Cosmetic rounding? No, 0.267 rounds to 0.27, not 0.30. This is a discrepancy beyond rounding error.

**6. [MAJOR] Castro Alves cosine "decisive" raw p = 0.050 claimed as "right at the boundary"**
- Quote: "Castro Alves cosine (p = 0.050, right at the boundary)"
- JSON: `castro_alves.book_level_primary.cosine.decisive_role_swap_test.p_value: 0.05`, `n_possible_role_assignments: 20`. 0.05 = 1/20. ✓

**7. [MAJOR] Humberto de Campos Burrows decisive raw p = 0.049**
- Quote: "Humberto de Campos Burrows' Δ (p = 0.049)"
- JSON: `0.048484848484848485` = 8/165. Rounds to 0.048, not 0.049. **Flag: 0.049 is wrong; 0.048 is correct.** A borderline p-value reported with an extra 0.001 could be seen as inflating significance perception.

**8. [MINOR] UMAP Section 4.6 claims "genuine-control authors (dominated by poetry for Castro Alves/Cruz e Sousa) occupy a separate region"**
- This is a qualitative claim about a UMAP projection not provided in the JSON. No UMAP coordinates or clustering metrics beyond silhouette/DB are in the ground truth. This cannot be verified from the given record. It may be correct, but it's untraceable.

**9. [CRITICAL] Section 4.5 claims André Luiz p-value trajectory "0.030 → 0.007 raw as the third baseline document was added"**
- The JSON contains only the final state after all three baseline documents; intermediate values (0.030, 0.015 earlier) are asserted from the paper's own revision history. No code-generated record supports these. **Untraceable historical claims.**

**10. [MAJOR] Silhouette/DB "n_chunks 1874" claim conflicts with JSON note**
- Quote (Section 3.3): "Silhouette score and Davies-Bouldin index assess clustering quality in both embedding and stylometric-feature space, over all 1874 chunks (every group has ≥2 chunks, so none is excluded)."
- JSON `clustering_quality.note`: "n_chunks may be less than n_chunks_total because silhouette/Davies-Bouldin require every group to have >=2 members; any group with a single chunk is excluded from clustering-quality metrics only." AND the group sizes show `psychographed__castro_alves: 2` and `psychographed__cruz_e_sousa: 7`—both ≥2, so all 1874 chunks ARE included. So the claim happens to be true here, but the paper's parenthetical "every group has ≥2 chunks" is NOT supported by the JSON's own caveat—it's an assertion not provable from the given record. Minor because it's true in this specific case.

**11. [MINOR] Permanova pseudo-F rounding**
- Quote: "pseudo-F = 492993.2, p<0.001; stylometric space: pseudo-F = 662850.5"
- JSON: 492993.246... and 662850.485... ✓ correctly rounded to 4 significant figures. ✓

**12. [MINOR] "9 groups, 1874 chunks" Permanova**
- JSON confirms n_groups=9, n_chunks=1874. ✓

## METHOD & ARGUMENT REVIEW

**13. [CRITICAL] The multiple-comparison FDR family is mis-specified and undercounted**
- Quote (Section 3.3): "Benjamini-Hochberg FDR correction is applied across all 15 primary book-level p-values we report as evidence: the 9 decisive role-swap tests (3 authors with control × 3 metrics) plus the 6 psychographed-vs-baseline tests for the 2 personas with no control (Emmanuel, André Luiz × 3 metrics)."
- This EXCLUDES: (a) Castro Alves, Cruz e Sousa, Humberto de Campos psychographed-vs-genuine-control tests (3 authors × 3 metrics = 9 tests), (b) Castro Alves, Cruz e Sousa, Humberto de Campos psychographed-vs-baseline tests (3 authors × 3 metrics = 9 tests). The total book-level tests actually reported as primary evidence in Section 4.3 is 6+6+6+3+3 = 24 tests, not 15. The FDR correction based on 15 tests is invalid if the paper actually interprets all 24; worse, the text in Section 4.3 itself presents the vs-genuine-control and vs-baseline tests as primary evidence. The paper's FDR family is cherry-picked: it excludes exactly the Humberto de Campos vs-genuine-control tests that are most significant (p=0.002–0.004), which would otherwise strengthen the correction, AND excludes the vs-baseline tests for the three control authors (p=0.0567–0.314). **The stated "15 primary tests" is not the full primary analysis as presented.** This is a critical methodological flaw.

**14. [CRITICAL] The "first result in five revisions to survive correction" claim is undermined by the FDR family selection**
- Quote: "the first result in five revisions of this analysis to survive that correction"
- With 24 tests in the full book-level primary analysis, André Luiz's p=0.007 would still survive FDR with p≈0.168 if all 24 were included—no wait, FDR at α=0.05: 24 tests, smallest p = 0.00202 (HdC Burrows vs-genuine), second = 0.00202 (HdC cosine vs-genuine), third = 0.00404 (HdC stylometric vs-genuine), then 0.00699 (André Luiz ×3). Corrected thresholds: (1/24)×0.05=0.00208; (2/24)×0.05=0.00417; (3/24)×0.05=0.00625; (4/24)×0.05=0.00833. So André Luiz (0.00699) would be just below the 4th threshold but need to be the 4th-smallest p. With HdC's three p=0.002-0.004 results ahead of it, André Luiz would be 4th, and 0.00699 < 0.00833, so it WOULD also survive. So the conclusion might not change under a properly broader family. But the family is still methodologically arbitrary and understated. The exact quote "all 15 primary tests" is misleading.

**15. [MAJOR] The "Humberto de Campos vs baseline" conclusion "pattern H0 predicts" is overstated**
- Quote: "Humberto de Campos's psychographed text is significantly unlike his own genuine writing (p = 0.002–0.004) but is not significantly distinguishable from Chico Xavier's own baseline (vs.-baseline: p = 0.057 Burrows' Δ, 0.314 cosine, 0.514 stylometric)"
- A failure to reject (p=0.057, 0.314, 0.514) is NOT evidence that the two are indistinguishable. With n=35 assignments for vs-baseline, power is very low. The paper acknowledges this in Section 7 but still asserts "the pattern H0 predicts" in multiple places (Abstract, Discussion, Conclusion). This is abandoning good frequentist caution in service of rhetorical symmetry. **Overstated.**

**16. [CRITICAL] The "two findings point in opposite directions" narrative is built on an asymmetric comparison**
- Quote: "these two load-bearing findings point in opposite directions: Humberto de Campos's psychographed text is unlike his own genuine writing but statistically indistinguishable from Chico Xavier's baseline…while André Luiz's is distinguishable from Chico Xavier's baseline with no genuine author to compare it against either way"
- This comparison is logically flawed: HdC's "unlike his genuine writing" test has high resolution (495 assignments, 4 vs 8 books) and is robustly significant. His "indistinguishable from baseline" assertion comes from a lower-resolution test (35 assignments) and is a failure-to-reject. André Luiz's test has higher resolution (286) and is significant. The claimed "opposite directions" requires treating non-rejection as positive evidence of indistinguishability, which is not justified. **The central narrative of the paper rests on a statistical fallacy.**

**17. [MAJOR] Sample size for Castro Alves psychographed is n=2 books; any permutation test with 2 books against 3 is exact but fundamentally underpowered**
- Quote: "Castro Alves's psychographed sample is still the weakest-powered in the study (2 books)."
- The minimal p-value achievable with n_books_a=2, n_books_b=3 is 1/10 = 0.1. The paper reports all three metrics as p=0.1. This means the test can NEVER reach significance at α=0.05 with this design. The paper acknowledges this but still presents the results in the primary table without marking them as structurally non-significant-by-construction. **Misleading presentation.**

**18. [CRITICAL] Genre confound is acknowledged but then downplayed**
- Quote (Section 2.2): "Poetry vs. prose ratios differ by author and are not matched between control and psychographed corpora for two of the three testable authors."
- Section 4.6: "plausibly reflecting the modality/genre confound (Section 2.2) rather than an authorship signal, and not statistically decisive either way"
- Yet Section 5 draws substantive conclusions ("pattern H0 predicts for this persona") without controlling for genre in any of the three distance families. Genre is the most severe confound in this study, and the paper acknowledges it but doesn't test it. **Major methodological gap.**

**19. [MINOR] The "5000 permutations" claim for chunk-level tests is not in the JSON**
- Quote (Section 3.3): "Permutes individual 500–1000-word chunks between groups, 5000 permutations."
- The JSON does not record the number of chunk-level permutations, only p-values and perm_mean/perm_std. This is untraceable.

**20. [MAJOR] The decisive role-swap test's null distribution is based on n_possible_role_assignments=20, 10, or 165, but the reported Δ values are point estimates from observed data only**
- The prediction "Δ>0 means control is closer" is fine. The FDR-adjusted p-values in JSON match exact_enumeration. But the paper spends enormous space on the directional tally 8/9→4/9→6/9 as if it were statistically meaningful, when none of the individual direction calls survive FDR. The tally itself has no significance test. **The instability narrative, while candid, still reifies a statistic with no distributional basis.**

**21. [MAJOR] The "book-level primary" designation is inconsistently applied**
- Section 4.3 table includes Castro Alves vs-genuine-control (p=0.100) which is book-level (10 assignments). But the vs-baseline for Castro Alves also has 10 assignments. All are book-level. However, the FDR family in Section 3.3 excludes all six Castro Alves/Cruz/Humberto vs-genuine and vs-baseline tests. So the primary section presents tests as "primary" that are not part of the correction family. **Internal inconsistency.**

**22. [MINOR] Unique claim "unchanged across five revisions" for HdC vs genuine control despite never involving baseline**
- Quote: "This test never involves the baseline, so it is identical across all five revisions."
- Given the data acquisition history described, this is plausible. ✓ No issue.

## WRITING REVIEW

**23. [MAJOR] AI-generated academic prose indicators present throughout**
- "empirically tractable question," "binding constraint," "load-bearing," "demonstrably unstable," "exact enumeration," "methodological lesson worth stating plainly" — these phrases are characteristic of LLM-generated academic hedging and meta-commentary. The draft is written in the register of a paper *about* its own revision process, not a standard computational stylometry paper. The meta-narrative ("this fifth revision," "four rounds of corpus expansion," "learned the hard way") is editorializing that belongs in a lab notebook, not a manuscript.

**24. [CRITICAL] APA citation format errors and suspicious sources**
- Honnibal & Montani, 2017 is cited as "[Software]. Explosion AI" — spaCy's citation format is typically Honnibal, M., Montani, I., Van Landeghem, S., & Boyd, A. (2020). *spaCy: Industrial-Strength Natural Language Processing in Python*. The 2017 date here likely refers to spaCy 2 release notes; the paper explicitly notes this is "a software release note, not a peer-reviewed article" — good candor but in APA this would not be listed as a primary reference in the same format.
- McInnes et al., 2018 is cited as arXiv. Fine.
- Barbosa, 1968; Schubert, 1985; additional domain literature are cited with pinky-promise caveats: "(Interview book;...)" and "text obtained from two independent PDF mirrors...not cross-checked." These are essentially unverifiable citations for the core data sources. The paper admits no domain literature is cited ("none is asserted here to avoid citing sources not verified in this session") — this is a huge gap for a paper about Chico Xavier.
- **No citation for the `paraphrase-multilingual-MiniLM-L12-v2` SBERT model beyond Reimers & Gurevych 2019. The specific model name and its publication venue are missing.**
- Yule, 1944 is cited without page/chapter. Acceptable for APA but unusual.

**25. [MAJOR] Overstatement of significance language despite honest caveats**
- "significantly and robustly different," "the strongest baseline-dependent result so far," "a much cleaner result than any previous revision produced" — promotional adjectives that would not survive standard peer review. Claiming "robustly" for a result that changed across revisions is contradictory.

**26. [MINOR] Rule-of-three lists**
- The limitations section has 9 items; the "What a properly powered version would need" has 5 items. Not egregious but consistent with LLM style.

**27. [MINOR] Inconsistent p-value formatting**
- "p = 0.007" vs. "p = 0.006993" vs. "p = 0.002–0.004" — the paper oscillates between 3-4 significant figures and ranges. The abstract says "rounded to 3–4 significant figures" but then reports some values as integers with "(286)" in parentheses and others as ranges.

**28. [MINOR] The self-referential draft header**
- The opening note "revised five times... An earlier version of this draft claimed..." is not part of a standard scientific paper and would be stripped before submission. Its presence signals this is a working draft, but the prose style is aspirational-peer-review.

## OVERALL VERDICT

This draft is not ready to show a human co-author who intends to publish. The veracity is uneven: several key numbers (Cruz e Sousa table values, Humberto's p=0.049) do not match the ground-truth JSON, and the paper's historical trajectory claims (0.015→0.030→0.007) are untraceable. The method is architecturally sound in concept—book-level permutation, exact enumeration, FDR—but the FDR family is arbitrarily truncated to 15 tests when the primary analysis presents 24, the narrative pivot on "opposite directions" depends on treating non-rejection as positive evidence of indistinguishability, and Castro Alves's n=2 psychographed books make any test meaningless at the stated significance level. The writing is clinically LLM-generated, with inflated significance language, editorial meta-commentary, and a revision-history framing that would confuse a reviewer. Honest as it is about its own instability, the paper's core statistical claims are not all traceable to the provided JSON, and its most rhetorically central distinction—Humberto de Campos fails differently than André Luiz—rests on a power asymmetry the paper never fully confronts. Until the FDR family is specified to match the actual evidence presented, every cited number matches the JSON, and the "opposite directions" narrative is rebuilt on statistically valid footing, this draft should not advance.