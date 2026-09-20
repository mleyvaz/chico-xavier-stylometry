# Stylometric Evidence for Poly-Authorship in the Psychographic Corpus of Chico Xavier: A Computational Case Study

**Working draft, twice adversarially reviewed.** An earlier version relied on
chunk-level permutation tests that treat overlapping 500–1000-word
sliding-window fragments from the same book as independent observations
(pseudoreplication); a first round of independent review (four frontier models,
queried separately) identified this and several other issues, detailed with
the revision log in the Reproducibility section. All results below use the
corrected book-level test design and the multiple-comparison family described
in Section 3.3. Numbers are drawn from `results/statistical_summary.json`
(rounded to 3–5 significant figures) unless otherwise noted; word/chunk counts
for individual source documents (Section 2.1) come from the ingestion logs
referenced in Reproducibility, not from that JSON file, since it records only
aggregated corpus statistics.

## Abstract

Francisco Cândido Xavier ("Chico Xavier", 1910–2002) was Brazil's most prolific
psychographic medium, producing several hundred books he attributed to more than
100 discarnate authors, including historical literary figures (exact totals vary
by source and are not independently verified in this study). This raises an
empirically tractable question for cognitive science and computational
linguistics: do texts psychographed under different attributed authorships carry
independent stylistic profiles (**poly-authorship hypothesis, H1**), or do they
collapse into a single stylistic attractor corresponding to the medium's own
baseline language (**subconscious-mimicry hypothesis, H0**)? We built a
computational pipeline comparing (i) Chico Xavier's own words from three
independent written/spoken sources — a 1971 televised-interview transcript, his
published personal-letter collection (1943–1964, 106 letters), and his own
answers, isolated from the interviewer's questions, in a 1968 published
interview book — (ii) genuine pre-mortem writings by three historical
Portuguese-language authors (Castro Alves: 3 books; Cruz e Sousa: 2 books;
Humberto de Campos: 8 books), and (iii) texts psychographically attributed to
those same three authors plus two discarnate personas with no independent
authorial history (Emmanuel: 5 books; André Luiz: 10 books). Using three
distance families — function-word Burrows' Delta, multilingual
sentence-embedding cosine distance, and a syntactic/lexical stylometric feature
distance — and testing at the level of whole books (the correct exchangeable
unit, since overlapping 500–1000-word chunks from the same book are not
independent observations, with exact permutation enumeration), two results
survive Benjamini-Hochberg correction across the full family of 33 book-level
tests we report: (1) psychographed "Humberto de Campos" text is significantly
different from the genuine historical Humberto de Campos's own writing (raw p =
0.002–0.004, FDR-adjusted p = 0.033–0.038, 495 possible book-to-group
assignments); and (2) psychographed "André Luiz" text is significantly distant
from Chico Xavier's own baseline (raw p = 0.007, FDR-adjusted p = 0.038, 286
possible assignments). Both hold up under a substantially broader correction
family than an earlier revision of this analysis used, addressing a specific
concern raised in review that the original family had been selectively scoped.
We do not read these two results as jointly confirming or refuting either
hypothesis. The Humberto de Campos result rules out simple reproduction of his
documented style but is silent on what the text resembles instead (his
vs.-baseline comparison does not reject the null either, at raw p =
0.057–0.514 — a failure to reject, which we explicitly do not treat as evidence
of equivalence). The André Luiz result has no genuine-author comparison
available at all and is confounded by an unavoidable genre mismatch between
epistolary/spoken baseline material and his psychographed narrative prose; we
ran a calibration check using Machado de Assis, an author with no connection to
this corpus whose own letters and novels are both public domain, and found that
his own, single-author letters-vs-novels distance is as large as or larger than
the André Luiz-vs-baseline distance on two of our three metrics. This
calibration does not prove genre is the entire explanation, but it means the
observed magnitude requires no authorship effect beyond ordinary genre-shift to
account for it, and we report the André Luiz result accordingly — as
unexplained by simple baseline reproduction, not as evidence of a distinct
authorial voice. The paper's central three-author question — is genuine
control closer to the psychographed text than Chico Xavier's baseline is? —
remains unresolved and, across three successive baseline configurations used
over the course of this analysis, its directional tally has taken three
different values (documented in the Reproducibility section's revision log)
without ever reaching significance in either direction. We report this
instability, not any single tally, as the paper's central finding: repeated
small expansions of the baseline sample changed which comparisons looked
significant, in both directions, indicating that baseline representativeness —
not the rigor of the statistical test itself — is the binding constraint on
this research question.

## 1. Introduction

Psychography — the claimed production of written text by a medium under the
purported authorship of a discarnate personality — is a widespread practice within
Brazilian Spiritism and has produced one of the largest attributed-multi-author
corpora available for computational stylometric analysis: the psychographed
books of Chico Xavier. Because Chico Xavier's own baseline language is
independently documented (broadcast interviews, letters) and several of his
attributed "spirit authors" correspond to historical writers whose genuine
pre-mortem work is also independently documented and digitized, this case admits
a controlled comparison that is rarely available in either forensic or literary
stylometry.

We frame the question as two competing hypotheses:

- **H1 (poly-authorship).** Psychographed texts attributed to different authors
  carry stylistic signatures that are measurably closer to those authors'
  independently known writing than to the medium's own baseline language.
- **H0 (subconscious mimicry / single attractor).** All psychographed texts,
  regardless of attributed authorship, are better explained as variations on the
  medium's own baseline stylistic profile than as independent authorial voices.

This paper's contribution is methodological as much as substantive: we show, by
example, why a chunk-level permutation test on a small, highly-sliced corpus can
produce spuriously strong significance, and we report both the naive chunk-level
result and the corrected, document-level result side by side so the size of the
inflation is visible.

### 1.1 Related work

This is not the first attempt at a computational or empirical test of this
corpus, and the small existing literature does not converge on one answer:

- **Sousa & Pires (2023)**, *Domínios de Lingu@gem*, 17, e1749, ran a
  statistical-computational authorship-attribution analysis on the same
  anthology we use for two of our five authors, *Parnaso de Além-Túmulo*
  (1932) — specifically its 31 poems attributed to Augusto dos Anjos, a poet we
  did not test. They report that these poems do **not** stylistically resemble
  his proven genuine work, *Eu* (1912), and instead resemble *Lira Imortal*
  (1939) — another Chico Xavier psychographed anthology, which we also use
  (Section 2.1) — more closely than they resemble Augusto dos Anjos's own
  writing. This is the same qualitative pattern we find for Humberto de Campos
  (Section 4): the attributed historical author's genuine style is not
  reproduced. Sousa & Pires interpret their result as evidence the poems
  collapse toward a shared psychographic register rather than toward any one
  historical voice — a finding our design does not directly test (we compare
  against Chico Xavier's own baseline, not against other psychographed
  anthologies), but one worth testing explicitly in future work on this corpus.
- **Weiler** (conference presentation, *The Science of Consciousness* 2026;
  University of Virginia Division of Perceptual Studies) reports, on the same
  *Parnaso de Além-Túmulo* anthology (259 poems across all attributed authors),
  stylistic and thematic evidence she interprets as *supporting* authorship
  compatibility with the named historical poets — the opposite qualitative
  conclusion from Sousa & Pires (2023) and from our own Humberto de Campos
  result, though for different authors within the same anthology and using a
  different analytical framework. We were unable to access a full peer-reviewed
  paper for this work at the time of writing; we cite the conference abstract
  as-is and flag it as not yet independently verified through peer review.
- **Rocha, Paraná, Freire, et al. (2014)**, *Explore: The Journal of Science
  and Healing*, 10(5), 300–308, take a different empirical approach entirely:
  rather than stylometric authorship attribution, they test the **factual
  accuracy** of biographical claims in a set of Chico Xavier's psychographed
  letters against independently verifiable records. This is a complementary,
  not competing, line of evidence — it speaks to content veracity, not to
  stylistic authorship, and we do not draw on its findings here.
- **Weibel (2024)**, *Journal of Anomalistics / Zeitschrift für Anomalistik*,
  24(1), 55–79, is not an empirical study of this or any specific corpus but a
  methodological survey making the case that stylometry is a "desirable
  auxiliary science for mediumship research," tracing its development from
  single numerical functions through word-frequency statistics to contemporary
  machine-learning methods. Weibel's central methodological claim — that
  replicating another author's style at the level of function words and
  punctuation is not a documented mediumistic ability, which is precisely why
  a function-word-level test (Burrows' Delta, our primary metric) is a
  meaningful probe rather than a foregone conclusion — is the closest
  methodological precedent we found for treating stylometry itself as the
  right instrument for this question, independent of which specific corpus it
  is applied to.

Three things follow from this literature. First, our approach — comparing
psychographed text against the medium's own independently documented baseline,
rather than only asking whether it matches the named historical author — is,
as far as we can establish, novel within this small literature; Sousa & Pires
and Weiler both compare psychographed text only against the genuine historical
author, which cannot distinguish "matches nobody in particular" from "matches
the medium's own voice instead." Second, the disagreement between Weiler and
Sousa & Pires on the same anthology is itself evidence that this corpus does
not yet have a settled answer, which is consistent with — and should temper
overconfidence in — our own study's central finding of instability (Section 5).
Third, Weibel's methodological argument for stylometry as a suitable
instrument for mediumship research is a premise this paper adopts but does not
itself defend from first principles; we take the instrument's validity as
given and focus on applying it rigorously to this specific corpus.

## 2. Data

### 2.1 Corpus construction

Three corpora were assembled and chunked into sliding windows of 500–1000 words,
across five revisions: an initial 20-book pass; a first expansion to 35 books; a
second expansion to 39 books adding a small (~1,800-word) excerpt of a second
baseline document; a substitution of that excerpt with the **complete** document
(85,250 words); and a final addition of a **third** independent baseline
document plus one more Cruz e Sousa psychographed source. Bibliographic leads
for the baseline and for additional psychographed poetry sources came from
asking four independent LLMs (via OpenRouter) and verifying each candidate
against archive.org/PDF sources before use:

1. **Baseline** — Chico Xavier's own words, from **three independent, complete
   documents**: (a) the public *Pinga-Fogo com Chico Xavier* (TV Tupi, 1971)
   transcript, spoken, 114 turns → 18 chunks; (b) his complete published
   personal-letter collection to Wantuil de Freitas, 1943–1964, 106 letters, in
   *Testemunhos de Chico Xavier* (Suely Caldas Schubert, FEB, 1985) — 85,250
   words → 85 chunks; (c) his own answers, programmatically separated from the
   interviewer's questions, in *No Mundo de Chico Xavier* (Elias Barbosa, 1968)
   — a numbered Q&A-format interview book where each question ends in "?" and
   each answer is the text following it; we kept only the answer portions,
   20,295 words → 20 chunks. All three documents are non-psychographed, in
   Chico Xavier's own voice.
2. **Genuine control** — pre-mortem writings by the historical Castro Alves (3
   books: *Espumas Flutuantes* 1870, *Os Escravos* 1883, and a microform
   combining *A Cachoeira de Paulo Afonso*/*Gonzaga*), Cruz e Sousa (2 books:
   *Faróis* 1900, *Evocações*), and Humberto de Campos (8 books: *O Brasil
   Anedótico* 1927, *O Monstro e outros Contos* 1932, *Mealheiro de Agripa* 1925,
   *Memórias e Memórias Inacabadas*, *O Arco de Esopo* 1926, *Sepultando os meus
   Mortos* 1935, *Últimas Crônicas* 1936, *Sombras que Sofrem*).
3. **Psychographed** — texts Chico Xavier attributed, through psychography, to
   Castro Alves (2 books: *Parnaso de Além-Túmulo* 1932, *Antologia dos
   Imortais* 1963) and Cruz e Sousa (4 books: the same two plus *Lira Imortal*
   1939 and *Relicário de Luz*), to the historical Humberto de Campos (4 books:
   *Crônicas de Além-Túmulo* 1937, *Novas Mensagens* 1935, *Brasil, Coração do
   Mundo, Pátria do Evangelho* 1938, *Pontos e Contos*), and to two discarnate
   personas with no independently attested pre-mortem authorial identity —
   Emmanuel (5 books: *Fonte Viva*, *Renúncia*, *Ave, Cristo*, *50 Anos
   Depois*, *Pão Nosso*) and André Luiz (10 books: the full *Nosso Lar* series
   through *Ação e Reação*).

| Group | Author | Chunks | Books |
|---|---|---|---|
| baseline | chico_xavier | 123 | 3 |
| control | castro_alves | 78 | 3 |
| control | cruz_e_sousa | 84 | 2 |
| control | humberto_de_campos | 404 | 8 |
| psychographed | castro_alves | 2 | 2 |
| psychographed | cruz_e_sousa | 7 | 4 |
| psychographed | humberto_de_campos | 158 | 4 |
| psychographed | emmanuel | 425 | 5 |
| psychographed | andre_luiz | 593 | 10 |

**Total: 1874 chunks, drawn from 41 books/documents.** The last column — books —
is the actually independent sample size for any authorship claim. Going from 2
to 3 baseline documents directly increased the decisive tests' combinatorial
resolution (e.g. André Luiz's vs.-baseline test: 66 → 286 possible book-to-role
assignments) — this is the change responsible for Section 4's new result, unlike
the previous revision where only the baseline's *size*, not its document count,
changed. Castro Alves's psychographed sample is still the weakest-powered in
the study (2 books).

Because Emmanuel and André Luiz have no genuine pre-mortem corpus, H1 can only be
tested for them in the weaker sense of "distinctiveness from baseline," not in the
stronger sense of "match to an independent human hand."

### 2.2 Data-quality and design limitations

- **Baseline document count (3) still bounds the decisive tests, but less
  tightly than before.** Each additional independent baseline document
  multiplies the combinatorial resolution of every vs.-baseline and decisive
  role-swap test; going from 1→2→3 documents produced the two largest results
  changes in this paper's history (Sections 4, 5). A fourth document would keep
  improving resolution, though with diminishing marginal returns as the
  existing documents already total 123 chunks.
- **Modality and register mix.** The baseline is now spoken interview (18
  chunks), personal letters (85 chunks), and Q&A-interview answers (20 chunks)
  — three different registers of "Chico Xavier's own voice," which is more
  representative than any single register alone, but still not matched to the
  literary-prose/poetry register of the control and psychographed corpora.
- **Speaker-separation risk in the interview book.** *No Mundo de Chico
  Xavier*'s answers were isolated by a text-based heuristic (splitting on the
  last "?" in each numbered block) rather than by manual reading of all 227
  extracted answers; we spot-checked a sample for correct attribution but did
  not verify every instance.
- **OCR noise.** The 1932 anthology *Parnaso de Além-Túmulo* and 1939 *Lira
  Imortal* are degraded periodical/booklet scans; Castro Alves and Cruz e Sousa
  psychographed samples remain small (2 and 7 chunks respectively).
- **Genre mismatch.** Poetry vs. prose ratios differ by author and are not
  matched between control and psychographed corpora for two of the three
  testable authors.

## 3. Methods

### 3.1 Feature extraction

- **Classical stylometry**: Yule's characteristic K, Simpson's D, type-token ratio
  (TTR), moving-average TTR (window 100), mean word/sentence length, function-word
  ratio, stop-word ratio.
- **Syntax**: POS bigrams/trigrams, mean dependency distance, mean dependency-tree
  depth, mean branching factor, using spaCy's Portuguese pipeline
  (`pt_core_news_lg`; Honnibal & Montani, 2017 — a software release note, not a
  peer-reviewed article; cited here as the standard reference for spaCy).
- **Dense semantics**: 384-dimensional sentence embeddings from the multilingual
  Sentence-BERT model `paraphrase-multilingual-MiniLM-L12-v2` (Reimers &
  Gurevych, 2019), cosine-normalized.

### 3.2 Distance metrics

- **Burrows' Delta** (Burrows, 2002), computed on z-scored relative frequencies of
  the 60 most frequent function words in the corpus.
- **Cosine distance** on the dense sentence embeddings.
- **Stylometric Euclidean distance** on the standardized classical/syntactic
  feature vector.
These three metrics are derived from the same underlying texts and are therefore
correlated by construction; they are reported as convergent, not independent,
lines of evidence.

### 3.3 Statistical tests

Two levels of permutation testing are reported, deliberately side by side:

- **Chunk-level (exploratory only).** Permutes individual 500–1000-word chunks
  between groups, 5000 permutations. This is what a naive stylometry pipeline
  typically reports, and what our own first draft reported before adversarial
  review. It does **not** account for the fact that chunks from the same book
  share vocabulary, topic, and style regardless of any authorship signal
  (pseudoreplication), so it systematically overstates significance when a group
  is dominated by one or two long books sliced into many overlapping windows.
- **Book-level (primary).** Permutes whole books between roles rather than
  individual chunks. Across the tests in this paper the number of possible
  book-to-role assignments ranges from 6 to 495; whenever that count is small
  enough to enumerate in full (every case here), we do exact enumeration rather
  than Monte Carlo sampling, so the reported p-value is exact for the stated
  null, not an approximation. A direct consequence, visible in Section 4.3–4.4,
  is that the smallest attainable p-value is mechanically bounded by that count
  (e.g. a 10-assignment test can never report p below 0.1) — a floor effect
  that is a property of the sample size, not of the effect being tested.
- **Decisive role-swap test.** For each of the three authors with a
  genuine-control corpus, we directly test the paper's key quantity — is
  genuine control closer to the psychographed text than baseline is? — by
  pooling that author's control books with the baseline documents and
  permuting which pooled books play the "control" role vs. the "baseline"
  role, holding the psychographed side fixed.
- **Benjamini-Hochberg FDR correction** is applied across **every book-level
  test reported in Section 4.3–4.4's tables** — 33 tests in total: for each of
  the three control-bearing authors (Castro Alves, Cruz e Sousa, Humberto de
  Campos), the psychographed-vs-genuine-control, psychographed-vs-baseline, and
  decisive role-swap tests, each on 3 metrics (27 tests); plus the
  psychographed-vs-baseline test for Emmanuel and André Luiz, each on 3 metrics
  (6 tests). An earlier revision of this analysis corrected only a
  narrower 15-test subset (the decisive tests plus the two no-control authors'
  vs.-baseline tests); independent review correctly flagged that narrower
  family as arbitrarily excluding results — including the Humberto de Campos
  vs.-genuine-control test — that the paper's own prose treated as primary
  evidence. We now correct across the full set instead.
- **PERMANOVA** (pseudo-F on a distance matrix, 5000 chunk-level permutations)
  tests global separation of the nine group/author labels; interpreted only as
  "these buckets are not identical," not as evidence for either hypothesis, given
  the same chunk-level non-independence concern.
- **Silhouette score and Davies-Bouldin index** assess clustering quality in both
  embedding and stylometric-feature space, over all 1874 chunks (every group has
  ≥2 chunks, so none is excluded).

## 4. Results

### 4.1 Global group separation

Both PERMANOVA tests reject the null of no group structure (embedding space:
pseudo-F = 492993.2, p<0.001; stylometric space: pseudo-F = 662850.5, p<0.001;
9 groups, 1874 chunks). Given the chunk-level non-independence discussed above,
this only shows the nine labels are not identical — expected almost by
construction — not that they correspond to independent authorial voices.
Clustering quality is correspondingly weak (embedding-space silhouette = −0.018,
Davies-Bouldin = 5.21; stylometric-space silhouette = 0.062, Davies-Bouldin =
2.23), consistent with heavily overlapping surface signatures.

### 4.2 Chunk-level tests (exploratory; reported for transparency, not as evidence)

These are not uniformly significant — for example Castro Alves's chunk-level
vs.-genuine-control cosine test is not significant (p = 0.199), nor is its
vs.-baseline cosine test (p = 0.065) or Cruz e Sousa's vs.-genuine-control
cosine test (p = 0.185) — but a majority are nominally significant, for the
pseudoreplication reasons already discussed. None of these numbers should be
read as evidence, significant or not; the book-level tests in Section 4.3 are
the ones we treat as primary. Exact values in `statistical_summary.json` →
`chunk_level_exploratory`.

### 4.3 Book-level tests (primary)

Permuting whole books (exact enumeration; number of possible book-to-role
assignments in parentheses). **The third baseline document raises resolution
substantially for every vs.-baseline test** (e.g. André Luiz: 66 → 286 possible
assignments):

| Author | Comparison | Burrows' Δ p | Cosine p | Stylometric p |
|---|---|---|---|---|
| Castro Alves (2 psy books vs. 3 ctrl) | vs. genuine control | 0.100 (10) | 0.100 (10) | 0.100 (10) |
| | vs. baseline (2 vs. 3) | 0.100 (10) | 0.100 (10) | 0.100 (10) |
| Cruz e Sousa (4 psy books vs. 2 ctrl) | vs. genuine control | 0.267 (15) | 0.267 (15) | 0.267 (15) |
| | vs. baseline (4 vs. 3) | 0.057 (35) | 0.086 (35) | 0.086 (35) |
| **Humberto de Campos (4 psy books vs. 8 ctrl)** | **vs. genuine control** | **0.002 (495)** | **0.002 (495)** | **0.004 (495)** |
| | vs. baseline (4 vs. 3) | 0.057 (35) | 0.314 (35) | 0.514 (35) |
| Emmanuel (5 psy books vs. 3 baseline) | vs. baseline | 0.054 (56) | **0.018 (56)** | **0.018 (56)** |
| **André Luiz (10 psy books vs. 3 baseline)** | **vs. baseline** | **0.007 (286)** | **0.007 (286)** | **0.007 (286)** |

Note the Cruz e Sousa vs.-genuine-control row: all three metrics give the
identical value 4/15 = 0.267, because the most extreme possible book-to-group
assignment happens to be the same rank under all three distance measures for
this small (15-assignment) test — this is a coincidence of the discretized
sample, not three independent confirmations.

**Humberto de Campos's psychographed-vs-genuine-control test is significant on
all three metrics** (p = 0.002–0.004 out of 495 possible book-to-group
assignments) — this test never involves the baseline, so it is identical across
every revision of this analysis. **André Luiz's vs.-baseline test is
significant before correction on all three metrics** (raw p = 0.007, 286
possible assignments), and Emmanuel's is close (raw p = 0.018–0.054). Section
4.4 reports which of these, and the decisive tests below, survive joint FDR
correction.

### 4.4 The decisive role-swap test, and the corrected multiple-comparison view

For the three authors with a genuine-control corpus, we directly test whether
genuine-control books are closer to the psychographed text than baseline book(s)
are (Δ = d(psychographed, baseline) − d(psychographed, control); Δ>0 means
control is closer). Raw and Benjamini-Hochberg-adjusted p-values below are
computed **jointly across the full 33-test family described in Section 3.3**
(all vs.-genuine-control, vs.-baseline, and decisive tests reported anywhere in
this section — not a narrower subset):

| Author | Metric | Δ (baseline − control) | Genuine closer? | Raw p | FDR-adjusted p |
|---|---|---|---|---|---|
| Castro Alves (3 ctrl books) | Burrows' Δ | +0.009 | Yes | 0.500 | 0.566 |
| | Cosine | +0.099 | Yes | 0.050 | 0.143 |
| | Stylometric | +1.464 | Yes | 0.100 | 0.143 |
| Cruz e Sousa (2 ctrl books) | Burrows' Δ | +0.122 | Yes | 0.200 | 0.275 |
| | Cosine | +0.092 | Yes | 0.100 | 0.143 |
| | **Stylometric** | **−0.663** | **No** | 0.600 | 0.639 |
| Humberto de Campos (8 ctrl books) | Burrows' Δ | +0.060 | Yes | 0.048 | 0.143 |
| | **Cosine** | **−0.046** | **No** | 0.994 | 0.994 |
| | **Stylometric** | **−0.384** | **No** | 0.812 | 0.838 |

Two individual decisive-test comparisons reach the raw p = 0.05 boundary —
Castro Alves cosine (p = 0.050 exactly, the most extreme of its 20 possible
assignments) and Humberto de Campos Burrows' Δ (p = 0.048) — but strictly
speaking only the latter is below 0.05; the former equals it. **Neither
survives FDR correction** (adjusted p = 0.143 for both, under the full 33-test
family of Section 3.3). The overall direction tally is **6 of 9** favoring
"genuine control closer." Across the three successive baseline configurations
used over the course of this analysis, this same tally took three different
values (documented in the Reproducibility section's revision log); we treat
that instability, not the current 6/9, as the informative fact about this
comparison.

Separately, under the same broad 33-test correction, **two results from
Section 4.3 do survive**: Humberto de Campos's psychographed-vs-genuine-control
test (FDR-adjusted p = 0.033–0.038 across the three metrics) and André Luiz's
vs.-baseline test (FDR-adjusted p = 0.038, all three metrics). These are the
only two of the 33 tests that clear conventional significance after correction.

### 4.5 Interpreting the two results that survive correction

Two results clear FDR correction under the full 33-test family; neither, on
its own, adjudicates H1 vs. H0, and we set out explicitly what each does and
does not support.

**Humberto de Campos vs. genuine control** (FDR-adjusted p = 0.033–0.038) is a
high-resolution test (495 possible assignments, 4 psychographed books against
8 control books) and does not depend on the baseline at all, so it is
unaffected by any of the baseline revisions in this project's history. It
supports a narrow, negative claim: the psychographed "Humberto de Campos" text
does not reproduce his own documented prose style. It does **not** by itself
tell us what the text *does* resemble — Humberto de Campos's own
vs.-baseline comparison fails to reject the null (raw p = 0.057–0.514, Section
4.3), which is a failure to detect a difference, not evidence that the
psychographed text *is* equivalent to Chico Xavier's baseline. We explicitly
avoid the inference "not significant vs. baseline, therefore matches the
baseline" in this paper; the correct, narrower statement is that this specific
low-power comparison (35 possible assignments; the smallest achievable p is
1/35 ≈ 0.029) did not detect a difference.

**André Luiz vs. baseline** (FDR-adjusted p = 0.038) is also a
comparatively high-resolution test (286 possible assignments, the largest in
this study) and supports the claim that the psychographed "André Luiz" corpus
is measurably different from Chico Xavier's own baseline material. It does
**not** support any claim about *what* produced that difference. In
particular, the baseline is exclusively personal correspondence, spoken
interview, and interview-book answers, while the André Luiz corpus is
exclusively long-form narrative fiction (the *Nosso Lar* series) — a genre
contrast at least as large as any plausible authorial one. We were not able to
construct a genre-matched control for this comparison (Section 2.2), so a
mundane explanation — that any long-form narrative prose, regardless of
attributed author, would differ this much from personal letters and spoken
interviews — remains fully consistent with this result and is not ruled out by
our design. We report the result because it is the one comparison in this
study that reaches significance under a properly broad multiple-comparison
correction, not because we believe it isolates an authorship effect.

### 4.6 Genre-shift calibration: how large is "just genre," normally?

Section 4.5 flags an uncontrolled genre confound for the André Luiz result but
does not quantify it. We ran a calibration check: how large is the same kind
of distance when we compare one **known, single author's** letters against
their own novels — a case where genre changes and authorship provably does
not? We used Machado de Assis (1839–1908), a canonical Brazilian author with
extensive public-domain correspondence and public-domain novels, unrelated to
Chico Xavier or this study's corpus. We assembled his published correspondence
(*Correspondência de Machado de Assis*, Tomo II, 1870–1889, Academia
Brasileira de Letras edition, 1 book after removing editorial front matter)
and two of his novels (*Dom Casmurro*, 1899; *Memórias Póstumas de Brás
Cubas*, 1881), processed through the identical pipeline (same chunking,
features, and distance metrics as the main study), and computed the
book-level distance between his letters and his novels:

| Metric | Machado de Assis: letters vs. his own novels (same author) | André Luiz (psychographed) vs. Chico Xavier baseline |
|---|---|---|
| Burrows' Δ | **1.168** | 1.009 |
| Cosine | **0.701** | 0.590 |
| Stylometric | 4.758 | **5.227** |

**The distance between one uncontested single author's own letters and his own
novels is as large as, or larger than, the André Luiz-vs-baseline distance on
two of the three metrics**, and only modestly smaller on the third. In other
words: the magnitude of stylistic distance we measured between psychographed
André Luiz and Chico Xavier's own baseline is fully within the range that
ordinary genre-switching produces for a single, known author with no
authorship question attached at all. This calibration does not prove genre is
the whole explanation — a real authorship effect on top of a genre effect
remains possible — but it substantially weakens any reading of the André Luiz
result as evidence of a distinct authorial voice, since a mundane genre
account alone, calibrated against a real single-author example, already
predicts a difference at least this large. We revise our interpretation of
this result accordingly in Section 5: it should be read as "not explained by
authorship beyond what genre alone predicts," not as "distinct from Chico
Xavier's voice" in any stronger sense.

### 4.7 Manifold and surface-feature comparisons

This section describes `results/umap_authors_manifold.png` directly; unlike
Sections 4.1–4.5, its content is not recorded in `statistical_summary.json`
and should be read as a qualitative, exploratory visualization rather than a
traceable statistic. A UMAP projection (cosine metric, default parameters) of
the semantic embeddings places Emmanuel, André Luiz, and psychographed
Humberto de Campos (all prose) in one broad region that also contains the
baseline points, while the genuine-control authors (dominated by poetry for
Castro Alves/Cruz e Sousa) occupy a separate region — plausibly reflecting the
modality/genre confound (Section 2.2) rather than an authorship signal. We do
not treat this figure as evidence either way.

## 5. Discussion

Two results survive correction across the full 33-test family (Section 4.4),
and one comparison remains genuinely unresolved. We take each in turn, without
treating "significant" as a stand-in for "supports H1" or "not significant" as
a stand-in for "supports H0" — a substitution we made in earlier revisions of
this analysis and which independent review correctly identified as unsound.

**Humberto de Campos vs. genuine control** (FDR-adjusted p = 0.033–0.038) does
not depend on the baseline, so it is unchanged across every revision of this
paper. It supports one claim only: the psychographed "Humberto de Campos" text
does not reproduce his own documented prose style. His separate
vs.-baseline comparison fails to reject the null (raw p = 0.057–0.514, 35
possible assignments) — we report this as a non-result, not as confirmation
that the psychographed text matches Chico Xavier's own voice instead. A
non-significant result at 35 assignments (minimum attainable p ≈ 0.029) has
very limited power to detect a real difference even if one exists; treating it
as evidence of equivalence would be the same error, in the opposite direction,
that we are trying to avoid throughout this paper.

**André Luiz vs. baseline** (FDR-adjusted p = 0.038) is the best-powered
baseline-dependent result in this study (286 possible assignments) and
supports a similarly narrow claim: the psychographed "André Luiz" corpus is
measurably different from Chico Xavier's own baseline material. We do not read
this as evidence of an independent authorial source. The comparison is
confounded with genre — the baseline is entirely personal letters, spoken
interview, and interview-book answers, while André Luiz's corpus is entirely
long-form narrative fiction — and our genre-shift calibration (Section 4.6),
using Machado de Assis's own letters against his own novels, found a
same-author distance as large as or larger than this one on two of three
metrics. An account in which *any* sustained narrative prose — regardless of
attributed author — would differ this much from personal correspondence and
spoken interview is not merely uncontrolled for in our design; it is
positively supported by a real single-author calibration. We report the result
as the one comparison in this study that clears a properly broad
multiple-comparison correction and is not explained by simple baseline
reproduction — not as evidence for poly-authorship, and not even as our
strongest candidate for such evidence.

**The three-author decisive question — is genuine control closer to the
psychographed text than Chico Xavier's own baseline is? — remains unresolved,
and its instability across this project's revisions is itself the most
informative fact we can report about it.** Across the three successive
baseline configurations used over the course of this analysis, its directional
tally took three different values (documented in the Reproducibility section's
revision log), and in the current, best-resourced configuration, two
individual comparisons (Castro Alves cosine, Humberto de Campos Burrows' Δ)
sit at or just below the raw p = 0.05 mark without surviving FDR correction
(adjusted p = 0.143 for both). We do not read the current directional tally as
evidence for H1, nor any earlier tally as evidence for H0: each reflects which
baseline documents happened to be available when the test was run, not a
stable quantity that repeated identical analysis would reproduce.

This instability is the paper's central methodological finding, and it
applies with equal force to the two results we do report as
correction-surviving: a statistically rigorous test design (book-level
permutation, exact enumeration, a correction family scoped to match every
primary result actually presented) does not protect against instability
introduced by an underpowered or unrepresentative sample feeding into it. We
have tried, in this revision, to report the Humberto de Campos and André Luiz
results with the specific limits of what each can support stated alongside
the number — narrow negative findings about surface style, not settled answers
to the poly-authorship question that motivated this project.

## 6. What a properly powered version of this study would still need

Four rounds of corpus expansion — more control/psychographed documents, then
progressively three independent baseline documents — produced one
FDR-significant but genre-confounded new result (André Luiz vs. baseline,
Section 4.5–4.6) and left the three-author decisive comparison unresolved.
What remains:

1. **A fourth (and further) independent baseline document, focused specifically
   on stabilizing the three-author decisive test.** Every baseline document
   added so far has changed that specific test's tally; we cannot yet say
   whether a fourth would continue moving it or would confirm convergence.
   Candidates not yet pursued: his signed prefaces/notes inside psychographed
   books ("nota do médium"), newspaper columns under his own name, or other
   published correspondence collections.
2. **More psychographed books for Castro Alves and Cruz e Sousa.** We found
   three additional sources this session (*Lira Imortal*, *Antologia dos
   Imortais*, *Relicário de Luz*) beyond the original *Parnaso* anthology, but
   Castro Alves remains limited to 2 short poems; his result stays the
   weakest-powered in the study.
3. **A within-corpus genre-matched control**, not just the external Machado de
   Assis calibration (Section 4.6). Ideally, genuine narrative fiction written
   by Chico Xavier himself under his own name — if any exists — would let us
   test the André Luiz result directly rather than by analogy to an unrelated
   author.
4. **Independent replication of the André Luiz result** with a held-out
   baseline document not used to select or tune the method, and with the
   Machado de Assis calibration extended to additional control authors, to
   check how consistently "same-author genre shift" reproduces a distance this
   large.
5. **A pre-registered minimum sample size for any baseline or control document
   before it is used**, not just before the statistical test is chosen — this
   revision's clearest lesson, learned the hard way with a 2-chunk excerpt that
   should have been flagged as insufficient from the start.

## 7. Limitations (consolidated)

1. The three-author decisive test's direction has changed with every baseline
   revision (8/9 → 4/9 → 6/9); we do not consider its current tally stable or
   trustworthy, only the trajectory informative.
2. Modality and register mix in the baseline (spoken interview, personal
   letters, Q&A-interview answers) is more representative than any single
   register but still not matched to literary prose/poetry.
3. The interview-book answers (Section 2.1) were speaker-separated by a
   text heuristic, spot-checked but not exhaustively verified.
4. Castro Alves's psychographed sample remains extremely small (2 short poems,
   OCR-degraded source); his results are the weakest-powered in the study.
5. Emmanuel and André Luiz have no genuine-authorship control by construction —
   their vs.-baseline results (including the significant André Luiz result)
   speak to distinctiveness from Chico Xavier, not to matching an independent
   historical voice.
6. Poetry/prose genre ratios are not matched between control and psychographed
   corpora for two of the three testable authors, and the same holds for the
   baseline vs. André Luiz's corpus (Section 4.6).
7. The three distance metrics are correlated by construction (same underlying
   texts), so multi-metric agreement is convergent, not independent, evidence.
8. Single-case-study design: results characterize this medium's corpus and
   cannot be generalized to psychography as a phenomenon.
9. **The Machado de Assis genre-shift calibration (Section 4.6) itself rests on
   a single control author and only 3 books** (1 letters, 2 novels) — it
   demonstrates that a distance this large is *unsurprising* for ordinary
   genre-switching, not that genre is *necessarily* the entire explanation for
   André Luiz. A broader calibration across several authors would strengthen
   or weaken this reading.
10. This paper's own revision history is itself evidence that small-sample
    baseline/control documents can manufacture or erase apparent findings;
    the same skepticism we applied to the now-abandoned "8/9 direction" claim
    applies to every result in this paper, including the two that currently
    survive correction.

## 8. Conclusion

Using a computational stylometry pipeline combining lexical, syntactic, and
dense semantic features across 41 source documents, we report two narrow,
FDR-corrected findings, each with an explicitly limited interpretation:
psychographed "Humberto de Campos" text does not reproduce the real Humberto
de Campos's own documented style (FDR-adjusted p = 0.033–0.038, independent of
the baseline and stable across every revision of this analysis), and
psychographed "André Luiz" text is measurably distinct from Chico Xavier's own
baseline material (FDR-adjusted p = 0.038) — though a genre-shift calibration
against an unrelated single author (Machado de Assis, letters vs. his own
novels, Section 4.6) found a same-author distance as large or larger on two of
three metrics, so this second result requires no authorship effect beyond
ordinary genre-switching to explain it, and we report it as such rather than
as evidence of a distinct voice. Neither result, individually or together,
confirms or refutes poly-authorship. The paper's central three-author
question — is genuine control closer to the psychographed text than Chico
Xavier's own baseline is — remains unresolved: across the three successive
baseline configurations used in this project, its directional tally took three
different values, none of them statistically stable, which we report as
evidence that this specific comparison is underpowered given the currently
available data rather than evidence for either hypothesis. We consider the
resulting methodological point — that baseline, control, and genre
representativeness, not the sophistication of the statistical test, was the
binding constraint throughout this project — as important as either individual
number reported above.

## Reproducibility

All results are produced by the pipeline in `src/`; see
`results/PAPER_SUMMARY.md` for exact commands, and
`results/statistical_summary.json` for the complete, code-generated numeric
record underlying Sections 4.1–4.5, including the `methodological_note` field
explaining the chunk-level vs. book-level distinction and the FDR correction
family. Section 4.6's genre-shift calibration is produced by the standalone
`scripts/calibration_genre_shift.py` and recorded in
`results/calibration/machado_genre_shift.json` — a separate corpus and JSON
file from the main study's, not part of `statistical_summary.json`. Section
4.7 (UMAP) and the per-document word/chunk counts in Section 2.1 are not
recorded in any JSON file; they come from the ingestion scripts' logs and
`data/manifest.json`, and should be independently regenerated (`python
build_corpus.py`) rather than taken on faith from this prose.

**Revision log.** This paper went through five data/analysis revisions. The
first three are summarized in Section 1's opening note. The two most
recent are relevant to numbers discussed in Sections 4–5:

- With a 2-document baseline (TV transcript + a short ~1,800-word letters
  excerpt), the André Luiz vs.-baseline book-level test reported raw p = 0.030
  (66 possible assignments); the three-author decisive-test direction tally
  was 4/9 (having been 8/9 in an earlier, since-corrected chunk-level-only
  analysis with a still smaller baseline).
- After replacing the excerpt with the complete 106-letter collection (same
  2-document count, larger word count per document), the André Luiz figure
  did not move materially; the three-author tally was still computed under a
  2-document baseline.
- After adding the third baseline document (the interview-book answers), the
  André Luiz raw p dropped to 0.007 (286 possible assignments, Section 4.3),
  and the three-author decisive tally became 6/9 (Section 4.4).

These intermediate values are recorded here as a narrative log of this
session's work, not as fields in the current `statistical_summary.json`
(which reflects only the final, three-document-baseline state) — readers
who want to verify them would need to re-run the pipeline with the
corresponding earlier subsets of `data/manifest.json`. We no longer describe
this sequence as "monotonic" or as grounds for extra trust in the André Luiz
result; §5 explains why.

The four independent adversarial reviews (two rounds) that prompted the
corrections described throughout this paper, and the independent
bibliographic-search responses that led to the three baseline documents and
the additional psychographed poetry sources, are archived in full in
`results/adversarial_review/` (round 1: bare filenames; round 2, after this
revision: `round1_*` prefix marks the originals, unprefixed files are the
round-2 review of this version).

## References

- Barbosa, E. (1968). *No Mundo de Chico Xavier: Entrevistas*.
- Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A
  Practical and Powerful Approach to Multiple Testing. *Journal of the Royal
  Statistical Society: Series B*, 57(1), 289–300.
- Burrows, J. (2002). 'Delta': A Measure of Stylistic Difference and a Guide to
  Likely Authorship. *Literary and Linguistic Computing*, 17(3), 267–287.
- Honnibal, M., & Montani, I. (2017). *spaCy 2: Natural language understanding
  with Bloom embeddings, convolutional neural networks and incremental parsing*
  [Software]. Explosion AI.
- Machado de Assis, J. M. (2009). *Correspondência de Machado de Assis, Tomo
  II: 1870–1889* (I. Moutinho & S. Eutério, Orgs.; S. P. Rouanet, Coord.).
  Academia Brasileira de Letras. (Genre-shift calibration source, Section 4.6.)
- Machado de Assis, J. M. (1899). *Dom Casmurro*.
- Machado de Assis, J. M. (1881). *Memórias Póstumas de Brás Cubas*.
- McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform Manifold
  Approximation and Projection for Dimension Reduction. *arXiv:1802.03426*.
- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using
  Siamese BERT-Networks. In *Proceedings of the 2019 Conference on Empirical
  Methods in Natural Language Processing* (pp. 3982–3992). (The specific
  checkpoint used, `paraphrase-multilingual-MiniLM-L12-v2`, is a community
  model built on this architecture; we found no separate model-card citation
  for it beyond the Hugging Face repository itself.)
- Rocha, A. C., Paraná, D., Freire, E. S., et al. (2014). Investigating the Fit
  and Accuracy of Alleged Mediumistic Writing: A Case Study of Chico Xavier's
  Letters. *Explore: The Journal of Science and Healing*, 10(5), 300–308.
- Schubert, S. C. (Ed.) (1985). *Testemunhos de Chico Xavier*. Federação
  Espírita Brasileira.
- Sousa, A. P. N., & Pires, E. (2023). Análises estatístico-computacionais de
  atribuição de autoria: Augusto dos Anjos e a obra psicografada Parnaso de
  Além-Túmulo. *Domínios de Lingu@gem*, 17, e1749.
- Weibel, A. (2024). Mediumship and Stylometry: Exploring a New Way of
  Attributing Authorship to Mediumistic Writings. *Journal of Anomalistics /
  Zeitschrift für Anomalistik*, 24(1), 55–79.
  https://doi.org/10.23793/zfa.2024.055
- Weiler, M. (2026). Stylistic and Thematic Evidence for Authorship
  Compatibility in the Mediumistic Poetry of Chico Xavier. Conference
  presentation abstract, *The Science of Consciousness 2026*, Tucson, AZ. Not a
  peer-reviewed publication; see Section 1.1 for this caveat in context.
- Yule, G. U. (1944). *The Statistical Study of Literary Vocabulary*. Cambridge
  University Press.

Corpus-acquisition details for Barbosa (1968) and Schubert (1985) — including
the Q&A speaker-separation heuristic and the fact that the Schubert text was
obtained from two independent PDF mirrors rather than a physical edition — are
documented as data provenance in Section 2.1, not repeated here.

*(Section 1.1 and the four domain-specific citations above — Rocha et al. 2014,
Sousa & Pires 2023, Weibel 2024, Weiler 2026 — were located and
bibliographically verified in this session, including cross-checking author
names directly against the publishing journal's table of contents for Sousa &
Pires, and against the journal's own contents page and DOI for Weibel. Broader
Spiritism/Kardecism background literature, and any further authorship studies
of this
corpus we did not find, should still be reviewed by Maikel before submission.)*
