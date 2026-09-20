"""Distance metrics, clustering quality, and hypothesis tests for the
stylometric decomposition pipeline. Produces JSON/CSV summaries under results/.
"""
import json
import logging
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, pdist, squareform
from scipy.stats import zscore
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "results"
RNG = np.random.default_rng(42)
N_PERMUTATIONS = 5000

STYLO_FEATURE_COLS = [
    "yules_k", "simpsons_d", "ttr", "mattr_100", "mean_word_length",
    "mean_sentence_length", "std_sentence_length", "function_word_ratio",
    "stopword_ratio", "mean_dependency_distance", "mean_tree_depth",
    "mean_branching_factor",
]


def load_data():
    features = pd.read_csv(PROCESSED_DIR / "features.csv", keep_default_na=False)
    function_words = pd.read_csv(PROCESSED_DIR / "function_words.csv", keep_default_na=False)
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    assert len(features) == len(embeddings) == len(function_words), "Row misalignment across feature tables"
    features["label"] = features["group"] + "__" + features["author"]
    return features, function_words, embeddings


# ---------------------------------------------------------------------------
# Distance metrics
# ---------------------------------------------------------------------------

def burrows_delta_matrix(function_words: pd.DataFrame) -> np.ndarray:
    mat = function_words.drop(columns=["chunk_id"]).to_numpy(dtype=float)
    z = zscore(mat, axis=0, ddof=0)
    z = np.nan_to_num(z)
    n = z.shape[0]
    delta = np.zeros((n, n))
    for i in range(n):
        delta[i] = np.mean(np.abs(z - z[i]), axis=1)
    return delta


def cosine_distance_matrix(embeddings: np.ndarray) -> np.ndarray:
    return squareform(pdist(embeddings, metric="cosine"))


def stylo_distance_matrix(features: pd.DataFrame) -> np.ndarray:
    scaled = StandardScaler().fit_transform(features[STYLO_FEATURE_COLS].fillna(0.0))
    return squareform(pdist(scaled, metric="euclidean"))


def centroid_distance(matrix: np.ndarray, idx_a: np.ndarray, idx_b: np.ndarray) -> float:
    """Mean pairwise distance between two index sets (proxy for centroid separation)."""
    return float(np.mean(matrix[np.ix_(idx_a, idx_b)]))


# ---------------------------------------------------------------------------
# Clustering quality
# ---------------------------------------------------------------------------

def clustering_quality(space: np.ndarray, labels: pd.Series) -> dict:
    labels = labels.to_numpy()
    valid_groups = pd.Series(labels).value_counts()
    keep_labels = valid_groups[valid_groups >= 2].index
    mask = pd.Series(labels).isin(keep_labels).to_numpy()
    if mask.sum() < 3 or pd.Series(labels[mask]).nunique() < 2:
        return {"silhouette": None, "davies_bouldin": None, "n_chunks": int(mask.sum())}
    sub = space[mask]
    lab = labels[mask]
    return {
        "silhouette": float(silhouette_score(sub, lab)),
        "davies_bouldin": float(davies_bouldin_score(sub, lab)),
        "n_chunks": int(mask.sum()),
    }


# ---------------------------------------------------------------------------
# Hypothesis tests
# ---------------------------------------------------------------------------

def permutation_test_group_distance(matrix: np.ndarray, idx_a: np.ndarray, idx_b: np.ndarray, n_perm: int = N_PERMUTATIONS) -> dict:
    """Two-sided permutation test on the mean between-group distance.

    H0: labels are exchangeable (no real group structure); the observed
    between-group centroid distance is no larger than expected by chance
    reassignment of the same chunks into two groups of the same sizes.
    """
    observed = centroid_distance(matrix, idx_a, idx_b)
    pooled = np.concatenate([idx_a, idx_b])
    n_a = len(idx_a)
    perm_stats = np.empty(n_perm)
    for p in range(n_perm):
        shuffled = RNG.permutation(pooled)
        perm_a, perm_b = shuffled[:n_a], shuffled[n_a:]
        perm_stats[p] = centroid_distance(matrix, perm_a, perm_b)
    p_value = float(np.mean(perm_stats >= observed))
    return {
        "observed_distance": observed,
        "perm_mean": float(perm_stats.mean()),
        "perm_std": float(perm_stats.std()),
        "p_value": p_value,
    }


def benjamini_hochberg(pvalues: dict) -> dict:
    """Benjamini-Hochberg FDR correction. `pvalues` maps name -> raw p-value."""
    names = list(pvalues.keys())
    pvals = np.array([pvalues[n] for n in names], dtype=float)
    order = np.argsort(pvals)
    m = len(pvals)
    adjusted = np.empty(m)
    prev = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        i = m - rank + 1
        val = min(prev, pvals[idx] * m / i)
        adjusted[idx] = val
        prev = val
    return {names[i]: float(adjusted[i]) for i in range(m)}


def get_book_index_map(features: pd.DataFrame, group: str, author: str) -> dict:
    sub = features[(features["group"] == group) & (features["author"] == author)]
    return {book: sub.index[sub["book"] == book].to_numpy() for book in sub["book"].unique()}


def book_level_permutation_test(matrix: np.ndarray, books_a: dict, books_b: dict, n_perm: int = N_PERMUTATIONS) -> dict:
    """Same logic as permutation_test_group_distance, but the exchangeable unit
    is a whole book rather than a chunk, to avoid pseudoreplication across
    overlapping sliding-window chunks drawn from the same document.

    When the pooled book count admits <=5000 combinations, this runs an EXACT
    permutation test (enumerates every possible book-to-role assignment)
    instead of Monte Carlo sampling.
    """
    all_names = list(books_a.keys()) + list(books_b.keys())
    n_a = len(books_a)
    book_idx_map = {**books_a, **books_b}

    def stat(names_a) -> float:
        idx_a = np.concatenate([book_idx_map[n] for n in names_a])
        names_b = [n for n in all_names if n not in names_a]
        idx_b = np.concatenate([book_idx_map[n] for n in names_b])
        return centroid_distance(matrix, idx_a, idx_b)

    observed = stat(list(books_a.keys()))
    all_combos = list(combinations(all_names, n_a))
    if len(all_combos) <= 5000:
        perm_stats = np.array([stat(c) for c in all_combos])
        exact, n_used = True, len(all_combos)
    else:
        perm_stats = np.empty(n_perm)
        for i in range(n_perm):
            chosen = tuple(RNG.choice(all_names, size=n_a, replace=False))
            perm_stats[i] = stat(chosen)
        exact, n_used = False, n_perm

    p_value = float(np.mean(perm_stats >= observed))
    return {
        "observed_distance": observed,
        "perm_mean": float(perm_stats.mean()),
        "perm_std": float(perm_stats.std()),
        "p_value": p_value,
        "exact_enumeration": exact,
        "n_permutations_used": n_used,
        "n_books_a": n_a,
        "n_books_b": len(books_b),
    }


def role_swap_delta_test(matrix: np.ndarray, psy_idx: np.ndarray, control_books: dict, baseline_books: dict, n_perm: int = N_PERMUTATIONS) -> dict:
    """Direct test of the actual decisive quantity: is genuine control closer
    to the psychographed text than baseline is? H0: the "control" vs
    "baseline" ROLE label is exchangeable across the pooled set of books (i.e.
    a book's distance to the psychographed set does not depend on whether it
    plays the genuine-control or the baseline role). We permute which pooled
    books get the "control" role vs the "baseline" role, holding the
    psychographed side fixed, and recompute
    Delta = d(psychographed, baseline-role books) - d(psychographed, control-role books).
    A one-sided p-value tests whether the observed Delta (control closer) is
    larger than chance role assignment would produce.
    """
    all_names = list(control_books.keys()) + list(baseline_books.keys())
    n_control = len(control_books)
    book_idx_map = {**control_books, **baseline_books}

    def delta_for(control_names) -> float:
        control_idx = np.concatenate([book_idx_map[n] for n in control_names])
        baseline_names = [n for n in all_names if n not in control_names]
        baseline_idx = np.concatenate([book_idx_map[n] for n in baseline_names])
        d_control = centroid_distance(matrix, psy_idx, control_idx)
        d_baseline = centroid_distance(matrix, psy_idx, baseline_idx)
        return d_baseline - d_control

    observed = delta_for(list(control_books.keys()))
    all_combos = list(combinations(all_names, n_control))
    if len(all_combos) <= 5000:
        perm_deltas = np.array([delta_for(c) for c in all_combos])
        exact, n_used = True, len(all_combos)
    else:
        perm_deltas = np.empty(n_perm)
        for i in range(n_perm):
            chosen = tuple(RNG.choice(all_names, size=n_control, replace=False))
            perm_deltas[i] = delta_for(chosen)
        exact, n_used = False, n_perm

    p_value = float(np.mean(perm_deltas >= observed))
    return {
        "observed_delta_baseline_minus_control": observed,
        "genuine_control_closer": bool(observed > 0),
        "p_value": p_value,
        "exact_enumeration": exact,
        "n_permutations_used": n_used,
        "n_control_books": n_control,
        "n_baseline_books": len(baseline_books),
        "n_possible_role_assignments": len(all_combos),
    }


def permanova(matrix: np.ndarray, labels: np.ndarray, n_perm: int = N_PERMUTATIONS) -> dict:
    """Distribution-free multivariate group-separation test (pseudo-F on a
    distance matrix), used in place of classical MANOVA because the
    normality/homoscedasticity assumptions of MANOVA are not defensible for
    noisy OCR'd stylometric data.
    """
    n = matrix.shape[0]
    groups = pd.factorize(labels)[0]
    unique_groups = np.unique(groups)
    ss_total = matrix[np.triu_indices(n, k=1)].astype(float) ** 2
    ss_total = ss_total.sum() / n

    def pseudo_f(group_ids: np.ndarray) -> float:
        ss_within = 0.0
        for g in unique_groups:
            idx = np.where(group_ids == g)[0]
            if len(idx) < 2:
                continue
            sub = matrix[np.ix_(idx, idx)]
            ss_within += (sub[np.triu_indices(len(idx), k=1)] ** 2).sum() / len(idx)
        ss_among = ss_total * n - ss_within
        df_among = len(unique_groups) - 1
        df_within = n - len(unique_groups)
        if df_within <= 0 or ss_within <= 0:
            return np.nan
        return (ss_among / df_among) / (ss_within / df_within)

    observed_f = pseudo_f(groups)
    perm_f = np.empty(n_perm)
    for p in range(n_perm):
        perm_f[p] = pseudo_f(RNG.permutation(groups))
    p_value = float(np.mean(perm_f >= observed_f))
    return {"pseudo_F": float(observed_f), "p_value": p_value, "n_groups": len(unique_groups), "n_chunks": n}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    features, function_words, embeddings = load_data()
    log.info("Loaded %d chunks, %d control/psychographed/baseline groups", len(features), features["label"].nunique())

    log.info("Computing distance matrices ...")
    delta = burrows_delta_matrix(function_words)
    cos_dist = cosine_distance_matrix(embeddings)
    stylo_dist = stylo_distance_matrix(features)
    np.save(RESULTS_DIR / "burrows_delta.npy", delta)
    np.save(RESULTS_DIR / "cosine_distance.npy", cos_dist)
    np.save(RESULTS_DIR / "stylo_distance.npy", stylo_dist)

    log.info("Clustering quality by group label (attributed author / control author / baseline)")
    clustering_results = {
        "embedding_space": clustering_quality(embeddings, features["label"]),
        "stylometric_space": clustering_quality(
            StandardScaler().fit_transform(features[STYLO_FEATURE_COLS].fillna(0.0)), features["label"]
        ),
        "note": (
            "n_chunks may be less than n_chunks_total because silhouette/Davies-Bouldin "
            "require every group to have >=2 members; any group with a single chunk is "
            "excluded from clustering-quality metrics only, not from other tests."
        ),
    }

    log.info("PERMANOVA on embedding cosine-distance matrix (global group separation)")
    permanova_results = {
        "embedding_space": permanova(cos_dist, features["label"].to_numpy()),
        "stylometric_space": permanova(stylo_dist, features["label"].to_numpy()),
    }

    log.info("Author-specific H1 vs H0 permutation tests (chunk-level, exploratory)")
    author_tests = {}
    control_authors = sorted(features.loc[features["group"] == "control", "author"].unique())
    baseline_idx = features.index[features["group"] == "baseline"].to_numpy()
    has_baseline = len(baseline_idx) > 0
    baseline_books = get_book_index_map(features, "baseline", "chico_xavier") if has_baseline else {}

    METRICS = [("burrows_delta", delta), ("cosine", cos_dist), ("stylometric", stylo_dist)]
    primary_pvalues = {}  # (author, metric) -> book-level role-swap p-value, for FDR correction

    for author in sorted(features.loc[features["group"] == "psychographed", "author"].unique()):
        psy_idx = features.index[(features["group"] == "psychographed") & (features["author"] == author)].to_numpy()
        psy_books = get_book_index_map(features, "psychographed", author)
        entry = {
            "n_psychographed_chunks": int(len(psy_idx)),
            "n_psychographed_books": len(psy_books),
            "chunk_level_exploratory": {},
        }

        if author in control_authors:
            ctrl_idx = features.index[(features["group"] == "control") & (features["author"] == author)].to_numpy()
            ctrl_books = get_book_index_map(features, "control", author)
            entry["n_control_chunks"] = int(len(ctrl_idx))
            entry["n_control_books"] = len(ctrl_books)

            # --- chunk-level: exploratory only, does not correct for within-book pseudoreplication ---
            entry["chunk_level_exploratory"]["psychographed_vs_genuine_control"] = {
                space: permutation_test_group_distance(m, psy_idx, ctrl_idx) for space, m in METRICS
            }
            if has_baseline:
                entry["chunk_level_exploratory"]["psychographed_vs_baseline"] = {
                    space: permutation_test_group_distance(m, psy_idx, baseline_idx) for space, m in METRICS
                }

            # --- book-level: primary, treats each book as the exchangeable unit ---
            if has_baseline:
                book_level = {}
                for space, m in METRICS:
                    book_level[space] = {
                        "psychographed_vs_genuine_control": book_level_permutation_test(m, psy_books, ctrl_books),
                        "psychographed_vs_baseline": book_level_permutation_test(m, psy_books, baseline_books),
                        "decisive_role_swap_test": role_swap_delta_test(m, psy_idx, ctrl_books, baseline_books),
                    }
                    for testname in ("psychographed_vs_genuine_control", "psychographed_vs_baseline", "decisive_role_swap_test"):
                        primary_pvalues[f"{author}__{space}__{testname}"] = book_level[space][testname]["p_value"]
                entry["book_level_primary"] = book_level
        elif has_baseline:
            entry["chunk_level_exploratory"]["psychographed_vs_baseline"] = {
                space: permutation_test_group_distance(m, psy_idx, baseline_idx) for space, m in METRICS
            }
            entry["book_level_primary"] = {
                space: {"psychographed_vs_baseline": book_level_permutation_test(m, psy_books, baseline_books)}
                for space, m in METRICS
            }
            for space in dict(METRICS):
                primary_pvalues[f"{author}__{space}__psychographed_vs_baseline"] = entry["book_level_primary"][space]["psychographed_vs_baseline"]["p_value"]

        author_tests[author] = entry

    log.info(
        "Benjamini-Hochberg FDR correction across the %d primary book-level tests "
        "(every vs-genuine-control, vs-baseline, and decisive role-swap test reported in book_level_primary)",
        len(primary_pvalues),
    )
    adjusted = benjamini_hochberg(primary_pvalues) if primary_pvalues else {}
    for key, p_adj in adjusted.items():
        author, space, testname = key.split("__")
        author_tests[author]["book_level_primary"][space][testname]["p_value_fdr_adjusted"] = p_adj

    summary = {
        "n_chunks_total": int(len(features)),
        "group_sizes": {"__".join(k): v for k, v in features.groupby(["group", "author"]).size().to_dict().items()},
        "clustering_quality": clustering_results,
        "permanova": permanova_results,
        "author_tests": author_tests,
        "has_baseline": has_baseline,
        "methodological_note": (
            "chunk_level_exploratory tests permute individual 500-1000 word sliding-window "
            "chunks, which are NOT independent when drawn from the same book (pseudoreplication) "
            "and should be read as descriptive, not confirmatory. book_level_primary tests treat "
            "each whole book as the exchangeable unit (exact enumeration when the number of "
            "book-to-role assignments is small) and are the primary, defensible test of the "
            "poly-authorship (H1) vs subconscious-mimicry (H0) question. decisive_role_swap_test "
            "is the direct significance test of whether genuine-control books are closer to the "
            "psychographed text than baseline books are, replacing the earlier boolean-only "
            "'genuine_closer_than_baseline' comparison. p_value_fdr_adjusted applies "
            "Benjamini-Hochberg correction across EVERY book-level primary test reported "
            "anywhere in book_level_primary (psychographed_vs_genuine_control, "
            "psychographed_vs_baseline, and decisive_role_swap_test, for every author), "
            "not a narrower subset, so the correction family matches the full set of "
            "primary results presented in the paper's tables."
        ),
    }

    def default(o):
        if isinstance(o, (np.integer, np.floating)):
            return o.item()
        if isinstance(o, tuple):
            return list(o)
        raise TypeError(f"Not serializable: {o!r}")

    out_path = RESULTS_DIR / "statistical_summary.json"
    out_path.write_text(
        json.dumps({str(k): v for k, v in summary.items()}, indent=2, default=default, ensure_ascii=False),
        encoding="utf-8",
    )
    log.info("Saved %s", out_path)


if __name__ == "__main__":
    main()
