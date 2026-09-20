"""Classical stylometry + syntactic feature extraction for Portuguese text chunks."""
import logging
import math
from collections import Counter

import numpy as np
import pandas as pd
import spacy

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

FUNCTION_POS = {"DET", "ADP", "CCONJ", "SCONJ", "PRON", "AUX"}

_NLP = None


def get_nlp():
    global _NLP
    if _NLP is None:
        log.info("Loading spaCy pt_core_news_lg ...")
        _NLP = spacy.load("pt_core_news_lg", disable=["ner", "lemmatizer"])
    return _NLP


def yules_k(word_counts: Counter, n_tokens: int) -> float:
    if n_tokens == 0:
        return 0.0
    freq_of_freq = Counter(word_counts.values())
    m1 = n_tokens
    m2 = sum(freq * (count**2) for count, freq in freq_of_freq.items())
    if m1 == 0:
        return 0.0
    return 10_000 * (m2 - m1) / (m1**2)


def simpsons_d(word_counts: Counter, n_tokens: int) -> float:
    if n_tokens <= 1:
        return 0.0
    return sum(c * (c - 1) for c in word_counts.values()) / (n_tokens * (n_tokens - 1))


def mattr(tokens: list[str], window: int = 100) -> float:
    """Moving-Average Type-Token Ratio."""
    n = len(tokens)
    if n < window:
        return len(set(tokens)) / n if n else 0.0
    ratios = []
    for i in range(0, n - window + 1):
        w = tokens[i : i + window]
        ratios.append(len(set(w)) / window)
    return float(np.mean(ratios))


def extract_features(doc) -> dict:
    tokens = [t for t in doc if not t.is_space]
    words = [t.text.lower() for t in tokens if t.is_alpha]
    n_words = len(words)
    word_counts = Counter(words)

    sentences = list(doc.sents)
    sent_lengths = [len([t for t in s if t.is_alpha]) for s in sentences]
    word_lengths = [len(w) for w in words]

    pos_tags = [t.pos_ for t in tokens if t.is_alpha]
    pos_bigrams = Counter(zip(pos_tags[:-1], pos_tags[1:])) if len(pos_tags) > 1 else Counter()
    pos_trigrams = Counter(zip(pos_tags[:-2], pos_tags[1:-1], pos_tags[2:])) if len(pos_tags) > 2 else Counter()

    function_word_ratio = (sum(1 for t in tokens if t.pos_ in FUNCTION_POS and t.is_alpha) / n_words) if n_words else 0.0
    stopword_ratio = (sum(1 for t in tokens if t.is_stop) / n_words) if n_words else 0.0

    dep_distances = [abs(t.i - t.head.i) for t in tokens if t.is_alpha and t.head.i != t.i]
    tree_depths = []
    for s in sentences:
        depth = 0
        for t in s:
            d = 0
            head = t
            while head.head.i != head.i and d < 100:
                head = head.head
                d += 1
            depth = max(depth, d)
        tree_depths.append(depth)

    branching = [len(list(t.children)) for t in tokens if t.is_alpha]

    return {
        "n_words": n_words,
        "n_sentences": len(sentences),
        "yules_k": yules_k(word_counts, n_words),
        "simpsons_d": simpsons_d(word_counts, n_words),
        "ttr": (len(word_counts) / n_words) if n_words else 0.0,
        "mattr_100": mattr(words, window=100),
        "mean_word_length": float(np.mean(word_lengths)) if word_lengths else 0.0,
        "mean_sentence_length": float(np.mean(sent_lengths)) if sent_lengths else 0.0,
        "std_sentence_length": float(np.std(sent_lengths)) if sent_lengths else 0.0,
        "function_word_ratio": function_word_ratio,
        "stopword_ratio": stopword_ratio,
        "mean_dependency_distance": float(np.mean(dep_distances)) if dep_distances else 0.0,
        "mean_tree_depth": float(np.mean(tree_depths)) if tree_depths else 0.0,
        "mean_branching_factor": float(np.mean(branching)) if branching else 0.0,
        "_pos_unigrams": Counter(pos_tags),
        "_pos_bigrams": pos_bigrams,
        "_pos_trigrams": pos_trigrams,
        "_function_words": Counter(t.text.lower() for t in tokens if t.pos_ in FUNCTION_POS and t.is_alpha),
    }


def build_feature_table(corpus: pd.DataFrame, batch_size: int = 16, n_process: int = 1) -> pd.DataFrame:
    nlp = get_nlp()
    records = []
    texts = corpus["text"].tolist()
    for i, doc in enumerate(nlp.pipe(texts, batch_size=batch_size, n_process=n_process)):
        feats = extract_features(doc)
        records.append(feats)
        if (i + 1) % 50 == 0:
            log.info("Processed %d/%d chunks", i + 1, len(texts))

    feat_df = pd.DataFrame(records)
    scalar_cols = [c for c in feat_df.columns if not c.startswith("_")]
    result = pd.concat([corpus.reset_index(drop=True), feat_df[scalar_cols]], axis=1)
    result.attrs["pos_unigrams"] = feat_df["_pos_unigrams"].tolist()
    result.attrs["pos_bigrams"] = feat_df["_pos_bigrams"].tolist()
    result.attrs["pos_trigrams"] = feat_df["_pos_trigrams"].tolist()
    result.attrs["function_words"] = feat_df["_function_words"].tolist()
    return result
