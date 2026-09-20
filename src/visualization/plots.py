"""Generate the three required figures under results/."""
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
import umap

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "results"

sns.set_theme(style="whitegrid", context="talk")
PALETTE = sns.color_palette("colorblind")


def load_data():
    features = pd.read_csv(PROCESSED_DIR / "features.csv", keep_default_na=False)
    features["label"] = features["group"] + " / " + features["author"]
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    delta = np.load(RESULTS_DIR / "burrows_delta.npy")
    cos_dist = np.load(RESULTS_DIR / "cosine_distance.npy")
    return features, embeddings, delta, cos_dist


def group_mean_matrix(matrix: np.ndarray, labels: pd.Series) -> pd.DataFrame:
    unique = sorted(labels.unique())
    out = pd.DataFrame(index=unique, columns=unique, dtype=float)
    for a in unique:
        idx_a = np.where(labels.values == a)[0]
        for b in unique:
            idx_b = np.where(labels.values == b)[0]
            out.loc[a, b] = matrix[np.ix_(idx_a, idx_b)].mean()
    return out


def plot_distance_heatmap(features: pd.DataFrame, delta: np.ndarray, cos_dist: np.ndarray) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(20, 9))
    for ax, matrix, title in [
        (axes[0], delta, "Burrows' Delta (function-word z-scores)"),
        (axes[1], cos_dist, "Cosine distance (semantic embeddings)"),
    ]:
        gm = group_mean_matrix(matrix, features["label"])
        sns.heatmap(gm.astype(float), annot=True, fmt=".2f", cmap="rocket_r", ax=ax, cbar_kws={"label": "mean distance"})
        ax.set_title(title)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.tick_params(axis="x", rotation=45)
        for label in ax.get_xticklabels():
            label.set_ha("right")

    fig.suptitle("Group-level stylistic distance: baseline vs. control vs. psychographed authors", y=1.02, fontsize=18)
    fig.tight_layout()
    out = RESULTS_DIR / "distance_heatmap.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved %s", out)


def plot_umap_manifold(features: pd.DataFrame, embeddings: np.ndarray) -> None:
    n_neighbors = min(15, max(2, len(features) - 1))
    reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=0.1, metric="cosine", random_state=42)
    coords = reducer.fit_transform(embeddings)

    fig, ax = plt.subplots(figsize=(14, 11))
    markers = {"baseline": "*", "control": "s", "psychographed": "o"}
    for i, group in enumerate(sorted(features["group"].unique())):
        sub_mask = features["group"] == group
        authors = sorted(features.loc[sub_mask, "author"].unique())
        for j, author in enumerate(authors):
            mask = sub_mask & (features["author"] == author)
            ax.scatter(
                coords[mask.values, 0], coords[mask.values, 1],
                label=f"{group} / {author}",
                marker=markers.get(group, "o"),
                s=90 if group != "baseline" else 220,
                alpha=0.75,
                color=PALETTE[(i * 4 + j) % len(PALETTE)],
                edgecolor="black", linewidth=0.3,
            )
    ax.set_title("UMAP manifold of semantic embeddings\n(does each attributed author form its own cluster, or collapse into Chico Xavier's baseline?)")
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=11, frameon=True)
    fig.tight_layout()
    out = RESULTS_DIR / "umap_authors_manifold.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved %s", out)


def plot_lexical_richness(features: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    order = sorted(features["label"].unique())

    sns.boxplot(data=features, x="label", y="yules_k", order=order, ax=axes[0], palette=PALETTE)
    axes[0].set_title("Yule's Characteristic K (lexical richness)\nlower = richer vocabulary")
    axes[0].set_xlabel("")
    axes[0].tick_params(axis="x", rotation=60)
    for label in axes[0].get_xticklabels():
        label.set_ha("right")

    sns.boxplot(data=features, x="label", y="mean_tree_depth", order=order, ax=axes[1], palette=PALETTE)
    axes[1].set_title("Mean dependency-tree depth\n(syntactic complexity)")
    axes[1].set_xlabel("")
    axes[1].tick_params(axis="x", rotation=60)
    for label in axes[1].get_xticklabels():
        label.set_ha("right")

    fig.suptitle("Lexical richness and syntactic complexity by group / author", y=1.03, fontsize=18)
    fig.tight_layout()
    out = RESULTS_DIR / "lexical_richness_comparison.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved %s", out)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    features, embeddings, delta, cos_dist = load_data()
    plot_distance_heatmap(features, delta, cos_dist)
    plot_umap_manifold(features, embeddings)
    plot_lexical_richness(features)


if __name__ == "__main__":
    main()
