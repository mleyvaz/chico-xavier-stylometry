"""Run the full feature-extraction stage: stylometry + embeddings.

Reads data/processed/corpus.csv and writes:
  - data/processed/features.csv        (chunk_id + scalar stylometric/syntactic features)
  - data/processed/embeddings.npy      (dense semantic embeddings, row-aligned with features.csv)
  - data/processed/function_words.csv  (chunk_id x top-N function-word relative frequencies, for Burrows' Delta)
"""
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stylometry import build_feature_table  # noqa: E402
from embeddings import embed_texts  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
TOP_N_FUNCTION_WORDS = 60


def build_function_word_matrix(corpus: pd.DataFrame, function_word_counters: list) -> pd.DataFrame:
    global_counts: dict[str, int] = {}
    for counter in function_word_counters:
        for w, c in counter.items():
            global_counts[w] = global_counts.get(w, 0) + c
    top_words = [w for w, _ in sorted(global_counts.items(), key=lambda kv: -kv[1])[:TOP_N_FUNCTION_WORDS]]

    rows = []
    for counter, n_words in zip(function_word_counters, corpus["n_words"]):
        total = max(sum(counter.values()), 1)
        rows.append({w: counter.get(w, 0) / total for w in top_words})
    fw_df = pd.DataFrame(rows)
    fw_df.insert(0, "chunk_id", corpus["chunk_id"].values)
    return fw_df


def main() -> None:
    corpus_path = PROCESSED_DIR / "corpus.csv"
    corpus = pd.read_csv(corpus_path, keep_default_na=False)
    log.info("Loaded %d chunks from %s", len(corpus), corpus_path)

    log.info("Stage 1/2: stylometric + syntactic features (spaCy)")
    feat_table = build_feature_table(corpus)

    scalar_cols = [c for c in feat_table.columns if c not in ("text",)]
    feat_table[scalar_cols].to_csv(PROCESSED_DIR / "features.csv", index=False, encoding="utf-8")
    log.info("Saved %s", PROCESSED_DIR / "features.csv")

    fw_df = build_function_word_matrix(feat_table, feat_table.attrs["function_words"])
    fw_df.to_csv(PROCESSED_DIR / "function_words.csv", index=False, encoding="utf-8")
    log.info("Saved %s", PROCESSED_DIR / "function_words.csv")

    log.info("Stage 2/2: dense semantic embeddings (sentence-transformers)")
    embeddings = embed_texts(corpus["text"].tolist())
    np.save(PROCESSED_DIR / "embeddings.npy", embeddings)
    log.info("Saved %s, shape=%s", PROCESSED_DIR / "embeddings.npy", embeddings.shape)


if __name__ == "__main__":
    main()
