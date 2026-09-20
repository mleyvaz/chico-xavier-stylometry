"""Download control and psychographed texts listed in data/manifest.json.

Two source types:
- archive_org: fetch the OCR plain-text (_djvu.txt) file directly, no auth required.
- pdf_extract: download a PDF and extract text with pdfplumber (fallback: pypdf).
"""
import json
import logging
import urllib.parse
from pathlib import Path

import requests

from common import clean_text

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "manifest.json"
RAW_DIR = ROOT / "data" / "raw"
HEADERS = {"User-Agent": "stylometry-research-bot/1.0 (academic use)"}


def fetch_archive_org_text(identifier: str, filename: str) -> str:
    encoded = urllib.parse.quote(filename)
    url = f"https://archive.org/download/{identifier}/{encoded}"
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    return resp.text


def extract_pdf_text(pdf_bytes: bytes) -> str:
    import io

    try:
        import pdfplumber

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        text = "\n".join(pages)
        if len(text.split()) > 30:
            return text
    except Exception as exc:
        log.warning("pdfplumber failed (%s), falling back to pypdf", exc)

    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def extract_doc_text(doc_bytes: bytes) -> str:
    import subprocess
    import sys
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".doc", delete=False) as tmp:
        tmp.write(doc_bytes)
        tmp_path = tmp.name
    out_path = tmp_path + ".out.txt"
    script = (
        "import textract,sys\n"
        "text = textract.process(sys.argv[1]).decode('utf-8','replace')\n"
        "open(sys.argv[2], 'w', encoding='utf-8').write(text)\n"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", script, tmp_path, out_path],
            capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace",
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        return Path(out_path).read_text(encoding="utf-8")
    finally:
        Path(tmp_path).unlink(missing_ok=True)
        Path(out_path).unlink(missing_ok=True)


def out_path_for(group: str, author: str, book: str) -> Path:
    slug = "".join(c if c.isalnum() else "_" for c in book).strip("_").lower()
    d = RAW_DIR / group / author
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{slug}.txt"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    for entry in manifest.get("archive_org", []):
        authors = entry.get("attributed_authors") or [entry.get("author") or entry.get("attributed_author")]
        group = entry["group"]
        book = entry["book"]
        for author in authors:
            out_path = out_path_for(group, author, book)
            if out_path.exists():
                log.info("Skipping %s / %s (already downloaded)", author, book)
                continue
            log.info("Fetching archive.org %s :: %s", entry["identifier"], entry["file"])
            try:
                text = fetch_archive_org_text(entry["identifier"], entry["file"])
            except Exception as exc:
                log.error("Failed to fetch %s/%s: %s", entry["identifier"], entry["file"], exc)
                continue
            out_path.write_text(clean_text(text), encoding="utf-8")
            log.info("Saved %s (%d words)", out_path, len(text.split()))

    for entry in manifest.get("pdf_extract", []):
        author = entry.get("author") or entry.get("attributed_author")
        group = entry["group"]
        book = entry["book"]
        out_path = out_path_for(group, author, book)
        if out_path.exists():
            log.info("Skipping %s / %s (already downloaded)", author, book)
            continue
        log.info("Downloading PDF for %s / %s: %s", author, book, entry["url"])
        try:
            resp = requests.get(entry["url"], headers=HEADERS, timeout=60)
            resp.raise_for_status()
            text = extract_pdf_text(resp.content)
        except Exception as exc:
            log.error("Failed to download/extract %s: %s", entry["url"], exc)
            continue
        if len(text.split()) < 50:
            log.warning("Extracted very little text (%d words) from %s — check manually", len(text.split()), entry["url"])
        out_path.write_text(clean_text(text), encoding="utf-8")
        log.info("Saved %s (%d words)", out_path, len(text.split()))

    for entry in manifest.get("doc_extract", []):
        author = entry.get("author") or entry.get("attributed_author")
        group = entry["group"]
        book = entry["book"]
        out_path = out_path_for(group, author, book)
        if out_path.exists():
            log.info("Skipping %s / %s (already downloaded)", author, book)
            continue
        log.info("Downloading DOC for %s / %s: %s", author, book, entry["url"])
        try:
            resp = requests.get(entry["url"], headers=HEADERS, timeout=60)
            resp.raise_for_status()
            text = extract_doc_text(resp.content)
        except Exception as exc:
            log.error("Failed to download/extract %s: %s", entry["url"], exc)
            continue
        if len(text.split()) < 50:
            log.warning("Extracted very little text (%d words) from %s — check manually", len(text.split()), entry["url"])
        out_path.write_text(clean_text(text), encoding="utf-8")
        log.info("Saved %s (%d words)", out_path, len(text.split()))


if __name__ == "__main__":
    main()
