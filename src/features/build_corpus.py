"""Walk data/raw/{control,psychographed}/<author>/*.txt, chunk into sliding
windows, and write a single tidy table to data/processed/corpus.parquet
(and .csv for easy inspection).
"""
import logging
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ingestion"))
from common import chunk_text, clean_text  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"


def load_baseline() -> pd.DataFrame:
    """Baseline = Chico Xavier's own words, from two independent sources:
    (a) the Kaggle TV-interview transcript (spoken), and (b) any raw .txt
    files under data/raw/baseline/chico_xavier/ (written — e.g. his own
    letters), each treated as its own book for book-level testing.
    """
    rows = []

    csv_path = PROCESSED_DIR / "baseline_chico_xavier.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        full_text = clean_text(" ".join(df["text"].astype(str)))
        chunks = chunk_text(full_text)
        rows.extend(
            {
                "group": "baseline",
                "author": "chico_xavier",
                "book": "pinga_fogo_tv_tupi_1971",
                "chunk_id": f"baseline_chico_xavier_pinga_fogo_{i:03d}",
                "text": c,
            }
            for i, c in enumerate(chunks)
        )
    else:
        log.warning("Baseline CSV not found at %s — run download_baseline.py first.", csv_path)

    written_dir = RAW_DIR / "baseline" / "chico_xavier"
    if written_dir.exists():
        for txt_path in sorted(written_dir.glob("*.txt")):
            book = txt_path.stem
            text = clean_text(txt_path.read_text(encoding="utf-8"))
            chunks = chunk_text(text)
            rows.extend(
                {
                    "group": "baseline",
                    "author": "chico_xavier",
                    "book": book,
                    "chunk_id": f"baseline_chico_xavier_{book}_{i:03d}",
                    "text": c,
                }
                for i, c in enumerate(chunks)
            )
            log.info("Baseline (written) %s: %d words -> %d chunk(s)", book, len(text.split()), len(chunks))

    log.info("Baseline: %d chunks total, %d book(s)", len(rows), len({r['book'] for r in rows}))
    return pd.DataFrame(rows)


def load_group(group: str) -> pd.DataFrame:
    group_dir = RAW_DIR / group
    rows = []
    if not group_dir.exists():
        return pd.DataFrame(columns=["group", "author", "book", "chunk_id", "text"])

    for author_dir in sorted(p for p in group_dir.iterdir() if p.is_dir()):
        author = author_dir.name
        for txt_path in sorted(author_dir.glob("*.txt")):
            book = txt_path.stem
            text = clean_text(txt_path.read_text(encoding="utf-8"))
            chunks = chunk_text(text)
            for i, c in enumerate(chunks):
                rows.append(
                    {
                        "group": group,
                        "author": author,
                        "book": book,
                        "chunk_id": f"{group}_{author}_{book}_{i:03d}",
                        "text": c,
                    }
                )
            log.info("%s / %s / %s: %d words -> %d chunk(s)", group, author, book, len(text.split()), len(chunks))
    return pd.DataFrame(rows)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    parts = [load_baseline(), load_group("control"), load_group("psychographed")]
    corpus = pd.concat(parts, ignore_index=True)
    corpus["word_count"] = corpus["text"].str.split().str.len()
    corpus = corpus[corpus["word_count"] >= 30].reset_index(drop=True)

    out_csv = PROCESSED_DIR / "corpus.csv"
    corpus.to_csv(out_csv, index=False, encoding="utf-8")
    log.info("Saved %d chunks to %s", len(corpus), out_csv)
    log.info("\n%s", corpus.groupby(["group", "author"]).size().to_string())


if __name__ == "__main__":
    main()
