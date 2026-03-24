from __future__ import annotations

from functools import lru_cache
import re
import tomllib
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
SOURCES_DIR = DATA_DIR / "sources"
RULES_PATH = DATA_DIR / "rules.toml"

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+(?:-[A-Za-zА-Яа-яЁё]+)*")


def normalize(text: str) -> str:
    return text.strip().lower().replace("ё", "е").replace("ъ", "")


def read_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


@lru_cache(maxsize=1)
def load_rules() -> dict:
    with RULES_PATH.open("rb") as handle:
        return tomllib.load(handle)


def _normalized_words(values: list[str]) -> set[str]:
    return {normalize(value) for value in values}


def load_manual_words() -> set[str]:
    rules = load_rules()
    return _normalized_words(rules["manual"]["words"])


def load_safe_words() -> set[str]:
    rules = load_rules()
    return _normalized_words(rules["safe"]["words"])


def load_patterns() -> list[str]:
    rules = load_rules()
    return [pattern.strip() for pattern in rules["manual"]["patterns"]]


def load_roots() -> set[str]:
    rules = load_rules()
    return _normalized_words(rules["manual"]["roots"])


def load_bars38_words() -> set[str]:
    rules = load_rules()
    words: set[str] = set()
    for relative_path in rules["sources"]["paths"]:
        words.update({normalize(line) for line in read_lines(DATA_DIR / relative_path)})
    return words


def load_source_words() -> set[str]:
    rules = load_rules()
    source_markers = tuple(normalize(marker) for marker in rules["sources"]["markers"])
    words = load_bars38_words()
    return {
        word
        for word in words
        if any(marker in word for marker in source_markers)
    }
