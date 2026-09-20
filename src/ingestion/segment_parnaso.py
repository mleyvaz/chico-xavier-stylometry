"""Segment the Parnaso de Alem-Tumulo anthology into per-poet excerpts.

The 1932 OCR scan is noisy (period magazine layout). Each attributed poem opens
with a title line and a short biographical signature line naming the poet
(e.g. "CASTRO ALVES", "CRUZ E SOUZA"), found by manual inspection of the raw
text (see project notes). Sections below were identified this way; this is a
one-off manual mapping, not a general-purpose parser, because the anthology
attributes each poet only once or twice in this particular digitization.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "raw" / "psychographed_anthology" / "castro_alves" / "parnaso_de_além_túmulo__1932.txt"

# (author_dir, start_line, end_line) — 1-indexed, inclusive, from manual inspection
SECTIONS = {
    "castro_alves": (1241, 1381),
    "cruz_e_sousa": (2477, 3008),
}


def main() -> None:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    for author, (start, end) in SECTIONS.items():
        excerpt = "\n".join(lines[start - 1 : end])
        out_dir = ROOT / "data" / "raw" / "psychographed_anthology" / author
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "parnaso_de_além_túmulo__1932.txt"
        out_path.write_text(excerpt, encoding="utf-8")
        print(f"{author}: {len(excerpt.split())} words -> {out_path}")


if __name__ == "__main__":
    main()
