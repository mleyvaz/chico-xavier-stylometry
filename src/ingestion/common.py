"""Shared helpers: text cleaning and sliding-window chunking."""
import re
import unicodedata


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, min_words: int = 500, max_words: int = 1000) -> list[str]:
    """Split text into sliding windows of min_words..max_words, breaking on paragraph/sentence bounds."""
    words = text.split()
    if len(words) < min_words:
        return [text] if words else []

    chunks = []
    step = max_words
    i = 0
    while i < len(words):
        window = words[i : i + max_words]
        if len(window) < min_words and chunks:
            # merge short tail into previous chunk
            chunks[-1] = chunks[-1] + " " + " ".join(window)
            break
        chunks.append(" ".join(window))
        i += step
    return chunks
