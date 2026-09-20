"""Download and filter the baseline Chico Xavier corpus from Kaggle."""
import logging
import sys
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DATASET = "iaespirita/pinga-fogo-com-chico-xavier-tv-tupi-1971"
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"


def download_dataset() -> Path:
    """Download the Kaggle dataset into data/raw/. Requires ~/.kaggle/kaggle.json."""
    import kaggle

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    log.info("Downloading Kaggle dataset %s", DATASET)
    kaggle.api.dataset_download_files(DATASET, path=str(RAW_DIR), unzip=True)
    log.info("Download complete: %s", RAW_DIR)
    return RAW_DIR


def find_csv(raw_dir: Path) -> Path:
    candidates = sorted(raw_dir.rglob("*.csv"))
    if not candidates:
        raise FileNotFoundError(f"No CSV found under {raw_dir}. Did the download succeed?")
    return candidates[0]


def extract_baseline(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    log.info("Loaded %d rows, columns: %s", len(df), list(df.columns))

    speaker_col = next((c for c in df.columns if c.lower() in {"speaker", "falante", "interlocutor"}), None)
    text_col = next((c for c in df.columns if c.lower() in {"text", "texto", "fala", "speech"}), None)
    if speaker_col is None or text_col is None:
        raise ValueError(
            f"Could not identify speaker/text columns automatically. Columns present: {list(df.columns)}. "
            "Edit this script to map the correct column names."
        )

    mask = df[speaker_col].astype(str).str.strip().str.lower() == "chico xavier"
    baseline = df.loc[mask, [speaker_col, text_col]].rename(
        columns={speaker_col: "speaker", text_col: "text"}
    )
    baseline["text"] = baseline["text"].astype(str).str.strip()
    baseline = baseline[baseline["text"].str.len() > 0].reset_index(drop=True)
    log.info("Extracted %d turns attributed to Chico Xavier", len(baseline))
    return baseline


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    try:
        download_dataset()
    except Exception as exc:  # kaggle.json missing/invalid, network, etc.
        log.error("Kaggle download failed: %s", exc)
        log.error(
            "Place kaggle.json in ~/.kaggle/ (Windows: %%USERPROFILE%%\\.kaggle\\) "
            "or manually download the dataset ZIP from kaggle.com/datasets/%s "
            "and extract its CSV into %s",
            DATASET,
            RAW_DIR,
        )
        sys.exit(1)

    csv_path = find_csv(RAW_DIR)
    baseline = extract_baseline(csv_path)
    out_path = PROCESSED_DIR / "baseline_chico_xavier.csv"
    baseline.to_csv(out_path, index=False, encoding="utf-8")
    log.info("Saved baseline corpus to %s", out_path)


if __name__ == "__main__":
    main()
