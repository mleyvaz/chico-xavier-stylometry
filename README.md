# Stylometric Evidence for Poly-Authorship in the Psychographic Corpus of Chico Xavier

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22856185.svg)](https://doi.org/10.5281/zenodo.22856185)

Code, derived data, and results supporting the paper *"Stylometric Evidence
for Poly-Authorship in the Psychographic Corpus of Chico Xavier: A
Computational Case Study"* (Maikel Leyva-Vázquez).

The full paper text is in [`results/ARTICLE_DRAFT.md`](results/ARTICLE_DRAFT.md);
a shorter summary is in [`results/PAPER_SUMMARY.md`](results/PAPER_SUMMARY.md).

## What this repository contains

- `src/` — the full pipeline: data ingestion, stylometric/syntactic feature
  extraction (spaCy), sentence embeddings, distance metrics (Burrows' Delta,
  cosine, standardized Euclidean), and statistical tests (exact-enumeration
  book-level permutation tests, PERMANOVA, Benjamini-Hochberg FDR correction).
- `scripts/calibration_genre_shift.py` — the independent Machado de Assis
  genre-shift calibration described in Section 4.6 of the paper.
- `scripts/adversarial_review.py` — the multi-model adversarial review
  harness (via OpenRouter) used for two independent review rounds; the
  reviews themselves are archived in `results/adversarial_review/`.
- `data/manifest.json` — full bibliographic metadata and original source
  URLs (archive.org, publisher PDFs) for every document in the corpus.
- `data/processed/features.csv`, `function_words.csv`, `embeddings.npy` —
  derived numeric features and embeddings for every text chunk (**no raw
  source text**; see below).
- `results/statistical_summary.json` — the complete, code-generated numeric
  record underlying every statistic reported in the paper.
- `results/calibration/machado_genre_shift.json` — the calibration study's
  output.
- `results/*.png` — the paper's figures.

## What this repository deliberately does NOT contain

**Raw source texts are not redistributed.** Several of the psychographed
works analyzed here were first published while Chico Xavier (d. 2002) was
alive and remain under copyright; some control-corpus and baseline texts are
public domain (e.g. Castro Alves, Cruz e Sousa, Machado de Assis — all
public-domain by author-death-plus-70-years) but were sourced from
third-party scans (archive.org, publisher PDF hosts) we do not have
independent rights to redistribute in bulk. Instead, `data/manifest.json`
lists the original public source for every document, so the corpus can be
independently reconstructed and the pipeline re-run against it
(`python src/features/build_corpus.py`). This excludes `data/raw/` and the
two processed files that embed full chunk text (`corpus.csv`,
`baseline_chico_xavier.csv`) from version control; everything needed to
verify the *statistics* (not to re-read the source books) is included.

## Reproducing the analysis

```bash
cd src/ingestion && python download_baseline.py   # requires a Kaggle API token
cd ../ingestion  && python download_texts.py       # re-fetches from data/manifest.json
cd ../ingestion  && python segment_parnaso.py
cd ../features   && python build_corpus.py
cd ../features   && python extract_all.py
cd ../models     && python analysis.py
cd ../visualization && python plots.py
cd ../../scripts && python calibration_genre_shift.py
```

`results/statistical_summary.json` and `results/calibration/machado_genre_shift.json`
are the outputs of `analysis.py` and `calibration_genre_shift.py`
respectively, and are already included in this repository so the reported
numbers can be checked without re-running the full pipeline.

## AI disclosure

This project's code, corpus assembly, and successive manuscript drafts were
produced with extensive assistance from Claude (Anthropic; Claude Code
interface). Two independent rounds of adversarial review of the manuscript
and its numerical claims were each conducted by four large language models
accessed via the OpenRouter API; the full reviews are archived in
`results/adversarial_review/`. See the AI Disclosure Statement in the
manuscript for full detail.

## License

Code in `src/` and `scripts/` is released under the MIT License (see
`LICENSE`). Derived numeric data (`data/processed/`, `results/*.json`) is
released under CC BY 4.0. This license covers only material we generated;
it does not extend to the copyright status of the underlying source texts,
which remains with their respective rights holders and is unaffected by
this repository.
