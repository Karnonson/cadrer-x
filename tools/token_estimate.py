# /// script
# requires-python = ">=3.10"
# dependencies = ["tiktoken>=0.8", "tokenizers>=0.20", "huggingface_hub>=0.25"]
# ///
"""Estimate how many tokens a skill set costs, and compare it with the same skills in another wording.

Claude's current tokenizer is not public, so the counts come from public ones —
OpenAI's (tiktoken) and the open-weight models' (Hugging Face). Absolute counts
differ between tokenizers; the FR/EN ratio is what carries over, so the report
ends with the median ratio across them as the estimate for Claude.

If ANTHROPIC_API_KEY is set, Claude's own count_tokens endpoint is added as an
exact row (it costs nothing, but sends the text to the API).

    uv run tools/token_estimate.py skills
    uv run tools/token_estimate.py skills --files --detail o200k
    uv run tools/token_estimate.py skills path/to/fr/skills

Directories are scanned for SKILL.md files and the helpers' aide.md (read by
path, no description, never listed), evals/ left out. Skills are paired by
folder name, or through --map EN=FR. --files adds each skill's other .md
files (references/, templates/), which a skill reads when it needs them.
Adapted from cadrer's tools/token_estimate.py.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

TIKTOKEN = {
    "o200k": ("o200k_base", "OpenAI GPT-4o / 4.1 / o-series / GPT-5"),
    "cl100k": ("cl100k_base", "OpenAI GPT-4 / 3.5"),
}

HUGGINGFACE = {
    "llama3": ("NousResearch/Meta-Llama-3-8B", "Meta Llama 3"),
    "qwen3": ("Qwen/Qwen3-8B", "Qwen 3"),
    "deepseek3": ("deepseek-ai/DeepSeek-V3", "DeepSeek V3"),
    "mistral-nemo": ("mistralai/Mistral-Nemo-Instruct-2407", "Mistral Nemo (Tekken)"),
    "gemma3": ("unsloth/gemma-3-1b-it", "Google Gemma 3"),
    "claude-legacy": ("Xenova/claude-tokenizer", "Anthropic Claude 1/2 — not Claude 3+"),
}


MAIN = ("SKILL.md", "aide.md")  # a skill's file, a helper's file


@dataclass
class Doc:
    key: str  # pairing key: the English skill name, or the file name
    path: Path
    description: str  # frontmatter description — always loaded into context
    body: str  # everything after the frontmatter — loaded when the skill runs
    extra: str = ""  # the skill's other .md files, with --files

    @property
    def full(self) -> str:
        return self.path.read_text(encoding="utf-8") + self.extra


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---", 4)
    if end == -1:
        return "", text
    head, body = text[4:end], text[end + 4 :].lstrip("\n")
    description = ""
    for line in head.splitlines():
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip()
    return description, body


def extra_files(skill_dir: Path) -> str:
    """the skill's other .md files: its references and templates, never its evals."""
    files = [f for f in sorted(skill_dir.rglob("*.md"))
             if f.name not in MAIN and "evals" not in f.relative_to(skill_dir).parts]
    return "".join("\n" + f.read_text(encoding="utf-8") for f in files)


def load(path: Path, rename: dict[str, str], with_files: bool = False) -> list[Doc]:
    if path.is_dir():
        files = sorted(f for m in MAIN for f in path.rglob(m) if "evals" not in f.relative_to(path).parts)
    else:
        files = [path]
    if not files:
        sys.exit(f"no SKILL.md or aide.md under {path}")
    docs = []
    for f in files:
        name = f.parent.name if f.name in MAIN else f.stem
        description, body = split_frontmatter(f.read_text(encoding="utf-8"))
        extra = extra_files(f.parent) if with_files and f.name in MAIN else ""
        docs.append(Doc(rename.get(name, name), f, description, body, extra))
    return docs


def pair(en: list[Doc], fr: list[Doc]) -> list[tuple[Doc, Doc]]:
    if len(en) == 1 and len(fr) == 1:
        return [(en[0], fr[0])]
    fr_by_key = {d.key: d for d in fr}
    pairs, missing = [], []
    for d in en:
        if d.key in fr_by_key:
            pairs.append((d, fr_by_key.pop(d.key)))
        else:
            missing.append(d.key)
    if missing or fr_by_key:
        print(f"unpaired — en: {missing or '-'}, fr: {list(fr_by_key) or '-'}", file=sys.stderr)
    if not pairs:
        sys.exit("nothing to compare: no skill names matched (see --map)")
    return pairs


class Counter:
    def __init__(self, name: str, label: str, encode):
        self.name, self.label, self._encode = name, label, encode

    def __call__(self, text: str) -> int:
        return self._encode(text) if text else 0


def public_counters(wanted: list[str] | None) -> list[Counter]:
    counters = []
    for name, (encoding, label) in TIKTOKEN.items():
        if wanted and name not in wanted:
            continue
        try:
            import tiktoken

            enc = tiktoken.get_encoding(encoding)
            counters.append(Counter(name, label, lambda t, e=enc: len(e.encode(t, disallowed_special=()))))
        except Exception as err:  # offline, blocked download
            print(f"skipping {name}: {err}", file=sys.stderr)
    for name, (repo, label) in HUGGINGFACE.items():
        if wanted and name not in wanted:
            continue
        try:
            from huggingface_hub import hf_hub_download
            from tokenizers import Tokenizer

            tok = Tokenizer.from_file(hf_hub_download(repo, "tokenizer.json"))
            counters.append(
                Counter(name, label, lambda t, k=tok: len(k.encode(t, add_special_tokens=False).ids))
            )
        except Exception as err:
            print(f"skipping {name}: {err}", file=sys.stderr)
    return counters


def claude_counter(model: str) -> Counter | None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None

    def count(text: str) -> int:
        request = urllib.request.Request(
            "https://api.anthropic.com/v1/messages/count_tokens",
            data=json.dumps({"model": model, "messages": [{"role": "user", "content": text}]}).encode(),
            headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        )
        with urllib.request.urlopen(request) as response:
            return json.load(response)["input_tokens"]

    overhead = count(".") - 1  # the message wrapper, counted on every call
    return Counter("claude", f"{model} (exact, via API)", lambda t: count(t) - overhead)


def measure(counters: list[Counter], docs: list[Doc]) -> dict[str, dict[str, int]]:
    """tokens per counter, split into the always-loaded descriptions and the whole files."""
    return {
        c.name: {
            "description": sum(c(d.description) for d in docs),
            "full": sum(c(d.full) for d in docs),
        }
        for c in counters
    }


def ratio(fr: int, en: int) -> float:
    return fr / en if en else float("nan")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("en", type=Path, help="English skill file or directory (or the only set to count)")
    parser.add_argument("fr", type=Path, nargs="?", help="French version: file or directory, compared against the first")
    parser.add_argument("--map", action="append", default=[], metavar="EN=FR",
                        help="pair skills whose folders are named differently (repeatable)")
    parser.add_argument("--files", action="store_true",
                        help="add each skill's other .md files (references/, templates/) to its count")
    parser.add_argument("--only", help="comma-separated tokenizers: " + ", ".join([*TIKTOKEN, *HUGGINGFACE]))
    parser.add_argument("--detail", metavar="TOKENIZER", help="per-skill breakdown with this tokenizer")
    parser.add_argument("--claude-model", default="claude-sonnet-5-5", help="model for count_tokens (default: %(default)s)")
    parser.add_argument("--json", action="store_true", help="print the numbers as JSON")
    args = parser.parse_args()

    mapping = dict(m.split("=", 1) for m in args.map)
    en_docs = load(args.en, {}, args.files)
    fr_docs = load(args.fr, {fr: en for en, fr in mapping.items()}, args.files) if args.fr else []
    pairs = pair(en_docs, fr_docs) if args.fr else []
    if pairs:
        en_docs, fr_docs = [p[0] for p in pairs], [p[1] for p in pairs]

    counters = public_counters(args.only.split(",") if args.only else None)
    exact = claude_counter(args.claude_model)
    if exact:
        counters.append(exact)
    if not counters:
        sys.exit("no tokenizer could be loaded")

    en = measure(counters, en_docs)
    fr = measure(counters, fr_docs) if pairs else None
    chars_en = sum(len(d.full) for d in en_docs)
    chars_fr = sum(len(d.full) for d in fr_docs) if pairs else 0

    public = [c for c in counters if c.name != "claude" and c.name != "claude-legacy"]
    estimate = None
    if fr and public:
        full = [ratio(fr[c.name]["full"], en[c.name]["full"]) for c in public]
        desc = [ratio(fr[c.name]["description"], en[c.name]["description"]) for c in public]
        estimate = {
            "full": {"median": statistics.median(full), "min": min(full), "max": max(full)},
            "description": {"median": statistics.median(desc), "min": min(desc), "max": max(desc)},
        }

    if args.json:
        print(json.dumps({"skills": len(en_docs), "chars": {"en": chars_en, "fr": chars_fr},
                          "en": en, "fr": fr, "fr_en_ratio": estimate}, indent=2))
        return

    print(f"{len(en_docs)} skill(s) · {chars_en:,} chars EN" + (f" · {chars_fr:,} chars FR ({ratio(chars_fr, chars_en):.2f}×)" if fr else ""))
    print()
    if fr:
        print(f"{'tokenizer':<15} {'EN full':>8} {'FR full':>8} {'FR/EN':>6}   {'EN desc':>7} {'FR desc':>7} {'FR/EN':>6}   model")
        for c in counters:
            e, f = en[c.name], fr[c.name]
            print(f"{c.name:<15} {e['full']:>8,} {f['full']:>8,} {ratio(f['full'], e['full']):>5.2f}×"
                  f"   {e['description']:>7,} {f['description']:>7,} {ratio(f['description'], e['description']):>5.2f}×   {c.label}")
    else:
        print(f"{'tokenizer':<15} {'full':>8} {'desc':>7}   model")
        for c in counters:
            print(f"{c.name:<15} {en[c.name]['full']:>8,} {en[c.name]['description']:>7,}   {c.label}")

    if args.detail:
        counter = next((c for c in counters if c.name == args.detail), None)
        if not counter:
            sys.exit(f"--detail: unknown or unloaded tokenizer {args.detail}")
        print(f"\nper skill, {counter.name}:")
        for i, d in enumerate(en_docs):
            line = f"  {d.key:<24} EN {counter(d.full):>6,}" + ("  aide.md" if d.path.name == "aide.md" else "")
            if fr:
                g = fr_docs[i]
                line += f"   FR {counter(g.full):>6,}  {ratio(counter(g.full), counter(d.full)):.2f}×  ({g.path.parent.name})"
            print(line)

    if estimate:
        f, d = estimate["full"], estimate["description"]
        print(f"\nFR costs {f['median']:.2f}× the tokens of EN when a skill runs "
              f"(public tokenizers range {f['min']:.2f}–{f['max']:.2f}×),")
        print(f"and {d['median']:.2f}× for the always-loaded descriptions ({d['min']:.2f}–{d['max']:.2f}×).")
        if exact:
            print(f"Claude, measured: {ratio(fr['claude']['full'], en['claude']['full']):.2f}× full, "
                  f"{ratio(fr['claude']['description'], en['claude']['description']):.2f}× descriptions.")
        else:
            print("Claude's tokenizer is not public: take the median as the estimate, "
                  "or set ANTHROPIC_API_KEY for an exact row.")


if __name__ == "__main__":
    main()
