from __future__ import annotations

from functools import lru_cache
import re
import tomllib
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
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

def load_source_words() -> set[str]:
    return set()
