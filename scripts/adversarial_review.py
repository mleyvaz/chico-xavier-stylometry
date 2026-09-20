"""Send the Chico Xavier article draft to multiple independent frontier models
via OpenRouter for adversarial review (veracity + method/argument combined).
"""
import json
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = (ROOT / "results" / "ARTICLE_DRAFT.md").read_text(encoding="utf-8")
STATS = (ROOT / "results" / "statistical_summary.json").read_text(encoding="utf-8")

API_KEY = os.environ["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "openai/gpt-5.6-terra-pro",
    "google/gemini-3.1-pro-preview",
    "x-ai/grok-4.6",
    "deepseek/deepseek-v4-pro-0813",
]

SYSTEM_PROMPT = """You are an adversarial peer reviewer for a computational stylometry paper.
Attack it on THREE fronts simultaneously:
1. VERACITY: does every number, statistic, and claim in the text match the raw
   `statistical_summary.json` provided? Flag any number that is wrong, rounded
   misleadingly, or not traceable to the JSON.
2. METHOD & ARGUMENT: is the reasoning from evidence to conclusion (H1 over H0)
   sound? Are sample-size, genre-confound, and multiple-comparison issues
   adequately acknowledged or glossed over? Is any claim overstated relative to
   what a permutation test with these p-values and these n's can actually support?
3. WRITING: does the prose show tells of AI-generated academic writing (empty
   hedging, inflated significance language, unjustified rule-of-three lists,
   promotional adjectives)? Is APA-style citation used correctly, and are any
   citations suspicious/unverifiable?

Be genuinely adversarial - your job is to find every real weakness, not to be
encouraging. Structure your response as a numbered list of concrete findings,
each with: severity (critical/major/minor), the exact quote or section it
concerns, and why it's a problem. End with a one-paragraph overall verdict on
whether this draft is ready to show a human co-author."""

USER_PROMPT = f"""Here is the raw statistical record (ground truth, code-generated):

```json
{STATS}
```

Here is the article draft to review:

```markdown
{ARTICLE}
```

Perform the adversarial review as instructed."""


def review_with_model(model: str) -> str:
    resp = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT},
            ],
            "temperature": 0.2,
        },
        timeout=300,
    )
    resp.raise_for_status()
    data = resp.json()
    if "choices" not in data:
        raise RuntimeError(f"Unexpected response for {model}: {data}")
    return data["choices"][0]["message"]["content"]


def main() -> None:
    out_dir = ROOT / "results" / "adversarial_review"
    out_dir.mkdir(parents=True, exist_ok=True)
    for model in MODELS:
        slug = model.replace("/", "__")
        out_path = out_dir / f"{slug}.md"
        print(f"Reviewing with {model} ...", file=sys.stderr)
        try:
            review = review_with_model(model)
        except Exception as exc:
            print(f"  FAILED: {exc}", file=sys.stderr)
            out_path.write_text(f"FAILED: {exc}", encoding="utf-8")
            continue
        out_path.write_text(review, encoding="utf-8")
        print(f"  saved -> {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
