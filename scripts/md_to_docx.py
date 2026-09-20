"""Minimal Markdown -> .docx converter for the Anomalistik submission.

Handles: #/##/### headers, **bold**, *italic*, bullet lists (-), numbered
lists (1.), pipe tables, and plain paragraphs. Good enough for a single
structured manuscript, not a general-purpose converter.
"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_runs(paragraph, text):
    # Split on **bold** and *italic* (bold checked first to avoid ** matching as nested *)
    tokens = re.split(r"(\*\*.+?\*\*|\*.+?\*|`.+?`)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            paragraph.add_run(tok[2:-2]).bold = True
        elif tok.startswith("*") and tok.endswith("*") and not tok.startswith("**"):
            paragraph.add_run(tok[1:-1]).italic = True
        elif tok.startswith("`") and tok.endswith("`"):
            r = paragraph.add_run(tok[1:-1])
            r.font.name = "Consolas"
        else:
            paragraph.add_run(tok)


def parse_table_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def convert(md_path: Path, docx_path: Path):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(11)

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Table block
        if stripped.startswith("|"):
            table_lines = []
            while i < n and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            # drop separator row (---|---)
            rows = [parse_table_row(l) for l in table_lines if not re.match(r"^\|[\s:|-]+\|$", l)]
            if rows:
                ncols = len(rows[0])
                table = doc.add_table(rows=len(rows), cols=ncols)
                table.style = "Light Grid Accent 1"
                for r_idx, row in enumerate(rows):
                    for c_idx in range(ncols):
                        cell_text = row[c_idx] if c_idx < len(row) else ""
                        cell = table.rows[r_idx].cells[c_idx]
                        p = cell.paragraphs[0]
                        add_runs(p, cell_text)
                        if r_idx == 0:
                            for run in p.runs:
                                run.bold = True
            doc.add_paragraph("")
            continue

        # Headers
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            heading_level = min(level, 4)
            h = doc.add_heading(level=heading_level)
            add_runs(h, text)
            i += 1
            continue

        # Horizontal rule
        if stripped in ("---", "***"):
            doc.add_paragraph("_" * 40)
            i += 1
            continue

        # Bullet list
        if re.match(r"^[-*]\s+", stripped):
            p = doc.add_paragraph(style="List Bullet")
            add_runs(p, re.sub(r"^[-*]\s+", "", stripped))
            i += 1
            continue

        # Numbered list
        m2 = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m2:
            p = doc.add_paragraph(style="List Number")
            add_runs(p, m2.group(2))
            i += 1
            continue

        # Bold-only line (e.g. **Author:** ...)
        p = doc.add_paragraph()
        add_runs(p, stripped)
        i += 1

    doc.save(docx_path)
    print(f"Wrote {docx_path}")


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    convert(src, dst)
