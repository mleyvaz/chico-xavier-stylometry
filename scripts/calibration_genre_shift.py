"""Genre-shift calibration: how large is the stylometric distance between an
author's own letters and their own novels, when we KNOW it's the same author?

We use Machado de Assis (1839-1908), a canonical Brazilian author with both
extensive public-domain correspondence and public-domain novels, unrelated to
Chico Xavier. This gives a reference magnitude for "genre alone" distance,
against which we compare the André Luiz (psychographed, narrative fiction) vs.
Chico Xavier baseline (letters + spoken interview + interview answers) result
from the main study (Section 4.3-4.4 of ARTICLE_DRAFT.md).
"""
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "ingestion"))
sys.path.insert(0, str(ROOT / "src" / "features"))
sys.path.insert(0, str(ROOT / "src" / "models"))

from common import chunk_text, clean_text  # noqa: E402
from stylometry import build_feature_table  # noqa: E402
from embeddings import embed_texts  # noqa: E402
from analysis import (  # noqa: E402
    burrows_delta_matrix,
    cosine_distance_matrix,
    stylo_distance_matrix,
    book_level_permutation_test,
)
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import pdist, squareform

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

RAW_DIR = ROOT / "data" / "raw" / "calibration"
OUT_DIR = ROOT / "results" / "calibration"


def build_corpus() -> pd.DataFrame:
    rows = []
    for group_dir, group in [(RAW_DIR / "machado_letters", "letters"), (RAW_DIR / "machado_novels", "novels")]:
        for txt_path in sorted(group_dir.glob("*.txt")):
            book = txt_path.stem
            text = clean_text(txt_path.read_text(encoding="utf-8"))
            chunks = chunk_text(text)
            for i, c in enumerate(chunks):
                rows.append({"group": group, "book": book, "chunk_id": f"{group}_{book}_{i:03d}", "text": c})
            log.info("%s / %s: %d words -> %d chunks", group, book, len(text.split()), len(chunks))
    df = pd.DataFrame(rows)
    df["word_count"] = df["text"].str.split().str.len()
    return df[df["word_count"] >= 30].reset_index(drop=True)


def build_function_word_matrix(corpus: pd.DataFrame, counters: list, top_n: int = 60) -> pd.DataFrame:
    global_counts: dict[str, int] = {}
    for counter in counters:
        for w, c in counter.items():
            global_counts[w] = global_counts.get(w, 0) + c
    top_words = [w for w, _ in sorted(global_counts.items(), key=lambda kv: -kv[1])[:top_n]]
    rows = []
    for counter, n_words in zip(counters, corpus["n_words"]):
        total = max(sum(counter.values()), 1)
        rows.append({w: counter.get(w, 0) / total for w in top_words})
    return pd.DataFrame(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    corpus = build_corpus()
    log.info("Calibration corpus: %d chunks, %s", len(corpus), corpus.groupby(["group", "book"]).size().to_dict())

    log.info("Extracting stylometric/syntactic features ...")
    feat_table = build_feature_table(corpus)
    fw_df = build_function_word_matrix(feat_table, feat_table.attrs["function_words"])

    log.info("Extracting embeddings ...")
    embeddings = embed_texts(corpus["text"].tolist())

    delta = burrows_delta_matrix(fw_df.assign(chunk_id=corpus["chunk_id"]))
    cos_dist = cosine_distance_matrix(embeddings)
    stylo_dist = stylo_distance_matrix(feat_table)

    letters_books = {
        b: feat_table.index[(feat_table["group"] == "letters") & (feat_table["book"] == b)].to_numpy()
        for b in feat_table.loc[feat_table["group"] == "letters", "book"].unique()
    }
    novels_books = {
        b: feat_table.index[(feat_table["group"] == "novels") & (feat_table["book"] == b)].to_numpy()
        for b in feat_table.loc[feat_table["group"] == "novels", "book"].unique()
    }
    log.info("letters books: %s", list(letters_books.keys()))
    log.info("novels books: %s", list(novels_books.keys()))

    results = {}
    for space, matrix in [("burrows_delta", delta), ("cosine", cos_dist), ("stylometric", stylo_dist)]:
        test = book_level_permutation_test(matrix, letters_books, novels_books)
        results[space] = test
        log.info(
            "%s: observed genre-shift distance = %.4f (perm mean %.4f, p=%.3f, n=%d)",
            space, test["observed_distance"], test["perm_mean"], test["p_value"], test["n_permutations_used"],
        )

    import json

    (OUT_DIR / "machado_genre_shift.json").write_text(
        json.dumps(results, indent=2, default=lambda o: o.item() if hasattr(o, "item") else o),
        encoding="utf-8",
    )
    log.info("Saved %s", OUT_DIR / "machado_genre_shift.json")


if __name__ == "__main__":
    main()
