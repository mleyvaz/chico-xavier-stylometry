# Stylometric & Neuro-Symbolic Decomposition of Poly-Author Psychographic Texts vs. Baseline Mediumship Language

**Status: COMPLETE, twice adversarially reviewed.** **This file is a summary;
`results/ARTICLE_DRAFT.md` is the authoritative, fully up-to-date paper —
including its Reproducibility section's revision log.** A first draft claimed
strong H1 support from chunk-level tests; independent review (four frontier
models, queried separately via OpenRouter) found this was pseudoreplication
and that the paper's central comparison had never actually been
significance-tested. A corrected book-level design and several rounds of
corpus/baseline expansion followed. A **second** round of independent review on
the corrected paper then found: a transcription error in one results table, an
arbitrarily narrow multiple-comparison correction family that excluded results
the paper's own prose treated as primary, and a "not significant vs. baseline
⇒ matches H0" inference that does not follow from a failure to reject a null
hypothesis. All three are fixed in the current version.

**Current headline results, both narrow findings, neither confirming or
refuting the paper's motivating hypotheses:**

1. **Psychographed "Humberto de Campos" does not reproduce his own genuine
   documented style** (FDR-adjusted p = 0.033–0.038, under a corrected,
   comprehensive 33-test correction family — see below). This test never
   touches the baseline, so it is unaffected by any baseline revision.
2. **Psychographed "André Luiz" is measurably distinct from Chico Xavier's own
   baseline material** (FDR-adjusted p = 0.038). This is confounded by genre:
   the baseline is entirely letters/spoken interview, while André Luiz's
   corpus is entirely narrative fiction. A genre-shift calibration using
   Machado de Assis (Section 4.6 below) found that an unrelated, single known
   author switching genres (letters vs. novels) produces a stylometric
   distance as large or larger than the André Luiz-vs-baseline distance on
   2 of 3 metrics — so a mundane genre explanation is not ruled out, and is in
   fact favored, by this design.
3. **The three-author decisive question — is genuine control closer to the
   psychographed text than the baseline is? — remains unresolved.** Its
   directional tally took three different values across three successive
   baseline configurations used in this project (documented in
   `ARTICLE_DRAFT.md`'s revision log); we report that instability, not any one
   tally, as the finding.

## What changed in the second adversarial-review round (this revision)

- **Fixed a real data-entry error**: the Cruz e Sousa psychographed-vs-genuine-
  control table row previously showed three different p-values (0.300, 0.200,
  0.700); the correct JSON value is 0.267 for all three metrics.
- **Broadened the FDR correction family from 15 to 33 tests** — every
  vs.-genuine-control, vs.-baseline, and decisive-role-swap test reported
  anywhere in the results tables, not a curated subset. Both headline findings
  above **still survive** under this much harder bar, which directly answers
  the reviewers' concern that the original 15-test family had been
  selectively scoped to protect a specific result.
- **Removed the claim that "not significantly different from baseline" is "the
  pattern H0 predicts."** Failing to reject a null hypothesis is not evidence
  the null is true, especially at the low power these book-level tests have
  (as few as 35 possible permutations for some comparisons). The paper now
  states this failure-to-reject as exactly that, with no interpretive gloss.
- **Removed the claim that the André Luiz p-value "moved in one consistent
  direction, therefore we trust it more"** — this was self-contradicted by the
  paper's own numbers elsewhere (0.015 → 0.030 → 0.007 is not monotonic) and
  was flagged by reviewers as an unverifiable historical claim dressed up as a
  robustness argument. The result is now reported on its own (corrected)
  merits — FDR-significant under the broad family — without that narrative.
- **Made the genre confound in the André Luiz result a primary caveat**, not a
  limitations-list footnote: the result is reported as "distinct from
  baseline," explicitly not as "distinct authorship."
- Minor corrections: Humberto de Campos's decisive-test Burrows' Δ p-value is
  0.048, not 0.049; "crosses p<0.05" language was replaced with exact values
  since one borderline result (Castro Alves cosine) equals 0.05 rather than
  falling below it.

## Genre-shift calibration added after the second review (this revision)

The André Luiz-vs-baseline result was the paper's own FDR-surviving finding
most vulnerable to a mundane genre explanation (narrative fiction vs.
letters/spoken interview). To measure how large "just genre" ordinarily is, we
built a small calibration corpus for Machado de Assis — a canonical
Brazilian author with no authorship question attached, chosen only for having
abundant public-domain letters *and* novels — and ran the same book-level
permutation test on his own letters (1 book, 145,118 words) vs. his own
novels (2 books, *Dom Casmurro* + *Memórias Póstumas de Brás Cubas*,
131,939 words combined). Full code in `scripts/calibration_genre_shift.py`,
raw output in `results/calibration/machado_genre_shift.json`.

| Metric | Machado, own letters vs. own novels (known same author) | André Luiz (psychographed) vs. Chico Xavier baseline |
|---|---|---|
| Burrows' Δ | 1.168 | 1.009 |
| Cosine | 0.701 | 0.590 |
| Stylometric (Euclidean) | 4.758 | 5.227 |

On 2 of 3 metrics, an unrelated author's ordinary genre switch produces a
*larger* stylometric distance than the André Luiz-vs-baseline gap; on the
third it is smaller but same order of magnitude. This does not prove the
André Luiz result is "only" genre — the calibration has just one control
author and three books, and its own permutation test has only 3 possible
book-to-group assignments (minimum p = 0.333, so it cannot itself reach
significance) — but it substantially weakens any reading of that result as
evidence of poly-authorship rather than of ordinary genre variation. This
finding is now Section 4.6 of `ARTICLE_DRAFT.md`.

---

## 1. Experimental protocol

Three-way comparison per the original design:

1. **Baseline** — Chico Xavier's own words, from three independent documents
   (spoken interview, personal letters, interview-book answers).
2. **Psychographed** — texts attributed, through Chico Xavier's psychography, to
   named authors: Emmanuel, André Luiz, Humberto de Campos (spirit), and Castro
   Alves / Cruz e Sousa (via poetry anthologies).
3. **Genuine control** — real, pre-mortem writings by the historical Castro Alves,
   Cruz e Sousa, and Humberto de Campos.

Note: Emmanuel and André Luiz have **no genuine control corpus** — both are
spirits with no independently attested pre-mortem authorial identity, so the
poly-authorship test for them can only be "does their psychographed style
differ from the medium's own baseline," not "does it match a known human hand."

### 1.1 Data sources and sizes (chunks of 500–1000 words, sliding window)

| Group | Author | Books | Chunks | Source |
|---|---|---|---|---|
| control | castro_alves | 3 (Espumas Flutuantes, Os Escravos, +1 microform) | 78 | archive.org OCR |
| control | cruz_e_sousa | 2 (Faróis, Evocações) | 84 | archive.org OCR + algosobre.com.br PDF |
| control | humberto_de_campos | 8 (O Brasil Anedótico, O Monstro..., +6 more) | 404 | archive.org OCR |
| psychographed | castro_alves | 2 (Parnaso de Além-Túmulo, Antologia dos Imortais) | 2 | archive.org OCR, manually segmented |
| psychographed | cruz_e_sousa | 4 (+Lira Imortal, +Relicário de Luz) | 7 | archive.org OCR, manually segmented |
| psychographed | humberto_de_campos | 4 (Crônicas de Além-Túmulo, Novas Mensagens, Brasil Coração..., Pontos e Contos) | 158 | oconsolador.com.br PDFs |
| psychographed | emmanuel | 5 (Fonte Viva, Renúncia, Ave Cristo, 50 Anos Depois, Pão Nosso) | 425 | archive.org OCR + oconsolador.com.br |
| psychographed | andre_luiz | 10 (full Nosso Lar series through Ação e Reação) | 593 | archive.org OCR |
| baseline | chico_xavier | 3 (TV interview 1971 — spoken; complete letters 1943-64 — written, 106 letters; interview-book answers 1968 — written, Q&A-separated) | 123 | Kaggle + 2 PDFs |

**Total: 1874 chunks, 41 books.** Full book list and exact filenames in
`data/manifest.json`.

A related-work section (`ARTICLE_DRAFT.md` §1.1) cites four real prior works
touching this corpus or this method: Sousa & Pires (2023) find the same
"psychographed ≠ genuine" pattern we find for Humberto de Campos, on a
different attributed poet in the same *Parnaso de Além-Túmulo* anthology;
Weiler (2026, conference abstract) reports the opposite conclusion on the same
anthology; Rocha et al. (2014) test factual accuracy of psychographed letters
rather than style; Weibel (2024, *Journal of Anomalistics*) is the closest
methodological precedent — a survey arguing stylometry is a "desirable
auxiliary science for mediumship research" and that replicating another
author's function-word/punctuation patterns is not a documented mediumistic
ability, which is exactly why our Burrows'-Delta test is a meaningful probe.
The existing literature does not agree on an answer, which is useful context
for reading our own instability.

### 1.2 Known data-quality limitations (disclose before interpreting any p-value below)

- **The three-author decisive test's direction has changed with every baseline
  revision** in this project (documented in `ARTICLE_DRAFT.md`'s revision
  log) — we do not consider its current tally stable.
- **The André Luiz vs.-baseline result is confounded by genre**: baseline =
  letters/spoken interview; André Luiz corpus = narrative fiction. We report
  it as "distinct from baseline," not as evidence of distinct authorship.
- **Speaker-separation risk**: the third baseline document's 227 "answers" were
  isolated from the interviewer's questions by a text heuristic (split each
  numbered Q&A block on its last "?"), spot-checked but not manually verified
  in full.
- **OCR noise.** Several psychographed poetry anthologies (1932, 1939) are
  degraded periodical/booklet scans; Castro Alves's psychographed sample is
  particularly small (2 short poems) and structurally incapable of reaching
  p<0.05 at its current size (minimum possible p = 0.1).
- **Asymmetric control availability.** Emmanuel and André Luiz cannot be tested
  against a genuine-authorship control by construction (no known pre-mortem
  corpus exists for either identity).
- **Genre confound (general).** Control and psychographed texts are not
  perfectly genre-matched (poetry vs. prose ratios differ across authors).

---

## 2. Feature extraction

- **Classical stylometry**: Yule's K, Simpson's D, TTR, MATTR(window=100), mean
  word/sentence length, function-word ratio, stop-word ratio (spaCy `pt_core_news_lg`).
- **Syntax**: POS bigrams/trigrams, mean dependency distance, mean dependency-tree
  depth, mean branching factor (spaCy dependency parser).
- **Semantics**: sentence-transformer embeddings, `paraphrase-multilingual-MiniLM-L12-v2`
  (384-dim, cosine-normalized).

A first implementation of tree-depth had a Python identity-comparison bug (`is`
instead of index equality on spaCy `Token` proxies) that silently pinned every
chunk's tree depth at the safety-cap value of 100; this was caught by inspecting the
lexical-richness figure (flat line at exactly 100.0 across all groups) and fixed
before producing the results below.

---

## 3. Figures

- `results/distance_heatmap.png` — group-level Burrows' Delta and cosine distance.
- `results/umap_authors_manifold.png` — semantic-embedding manifold; qualitative
  only, not recorded in `statistical_summary.json` (see `ARTICLE_DRAFT.md` §4.7).
- `results/lexical_richness_comparison.png` — Yule's K and dependency-tree depth
  by group; psychographed prose is not systematically simpler than genuine
  control prose.

## 4. Hypothesis tests — headline numbers

Full methodology, all tables, and the revision log are in
`results/ARTICLE_DRAFT.md` §3–5 and its Reproducibility section. Headline
results:

- **PERMANOVA** (global group separation, 9 labels, 1874 chunks): significant in
  both embedding space (pseudo-F ≈ 493,000) and stylometric space (pseudo-F ≈
  663,000), p<0.001 both — expected almost by construction, not evidence for
  either hypothesis. Clustering quality remains weak (silhouette −0.018 / 0.062).
- **Book-level psychographed-vs-genuine-control** (unaffected by the baseline):
  significant for Humberto de Campos (raw p = 0.002–0.004, FDR-adjusted p =
  0.033–0.038 under the full 33-test family). Not significant for Castro Alves
  or Cruz e Sousa (both underpowered by sample size, not by effect absence).
- **Book-level psychographed-vs-baseline** (no control needed): André Luiz
  significant and FDR-surviving (raw p = 0.007, adjusted p = 0.038 — see the
  genre-confound caveat above, and the genre-shift calibration in Section 4.6
  of `ARTICLE_DRAFT.md`, which found an unrelated author's ordinary genre
  switch produces a distance of the same or larger magnitude on 2 of 3
  metrics). Emmanuel close but not surviving correction (raw p = 0.018–0.054,
  adjusted p = 0.074+).
- **Decisive role-swap test** (genuine-vs-baseline proximity, 3 authors): two
  individual comparisons sit at or near raw p = 0.05 (Castro Alves cosine =
  0.050 exactly; Humberto de Campos Burrows' Δ = 0.048) but neither survives
  FDR correction (adjusted p = 0.143 both). Direction tally: 6 of 9 favor
  "genuine closer" in the current, best-resourced configuration — the third
  different tally across this project's baseline revisions.

## 5. Discussion (see `results/ARTICLE_DRAFT.md` §5–8 for the full version)

Two narrow, FDR-corrected findings, neither settling the poly-authorship
question: Humberto de Campos's psychographed text doesn't match his own
genuine style (stable, baseline-independent, no confound we're aware of), and
André Luiz's psychographed text is distinct from Chico Xavier's own baseline
(FDR-significant, but confounded by an uncontrolled genre difference this
design cannot separate from an authorship effect — a genre-shift calibration
against an unrelated known author found ordinary genre variation alone
produces a comparable or larger distance on 2 of 3 metrics, weakening any
authorship-based reading of this result). The three-author decisive
question remains open; we treat its instability across revisions, not any
single tally, as the honest finding. The core lesson of this project: a
statistically rigorous test design (exact permutation, comprehensive FDR
correction) does not protect against instability or confounding introduced by
an underpowered or unrepresentative sample feeding into it. What would still
be needed to fully resolve the decisive question, and to independently
replicate or rule out the genre explanation for the André Luiz result, is
specified in `results/ARTICLE_DRAFT.md` §6.

## 6. Reproducing this analysis

```
cd src/ingestion && python download_baseline.py   # requires ~/.kaggle/kaggle.json
cd ../ingestion  && python download_texts.py
cd ../ingestion  && python segment_parnaso.py
cd ../features   && python build_corpus.py
cd ../features   && python extract_all.py
cd ../models     && python analysis.py
cd ../visualization && python plots.py
cd ../../scripts && python calibration_genre_shift.py   # separate calibration corpus, own JSON output
```

All intermediate artifacts are cached under `data/processed/` and `results/`.
The genre-shift calibration is a standalone script/corpus/output, independent
of the main pipeline (`results/calibration/machado_genre_shift.json`, not part
of `statistical_summary.json`). Both rounds of adversarial review and the
bibliographic-search results (all via OpenRouter) are archived in
`results/adversarial_review/` (round 1: `round1_*`-prefixed files; round 2,
which reviewed the version before this one, unprefixed files).
