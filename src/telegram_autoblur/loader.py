from __future__ import annotations

import re
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
SOURCES_DIR = DATA_DIR / "sources"

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+(?:-[A-Za-zА-Яа-яЁё]+)*")
SOURCE_MARKERS = (
    "бля",
    "бзд",
    "дроч",
    "дрюч",
    "еб",
    "ебл",
    "жоп",
    "залуп",
    "манд",
    "мраз",
    "муд",
    "педер",
    "педик",
    "пид",
    "пизд",
    "сра",
    "сук",
    "трах",
    "уеб",
    "хер",
    "хрен",
    "ху",
    "шалав",
    "шлюх",
    "шмар",
)


def normalize(text: str) -> str:
    return text.strip().lower().replace("ё", "е").replace("ъ", "")


def read_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_manual_words() -> set[str]:
    return {normalize(line) for line in read_lines(DATA_DIR / "manual_words.txt")}


def load_safe_words() -> set[str]:
    return {normalize(line) for line in read_lines(DATA_DIR / "safe_words.txt")}


def load_patterns() -> list[str]:
    return [line.removesuffix(".*").strip() for line in read_lines(DATA_DIR / "patterns.txt")]


def load_bars38_words() -> set[str]:
    return {normalize(line) for line in read_lines(SOURCES_DIR / "bars38_words.txt")}


def _is_in_relevant_section(line: str, active: bool) -> bool:
    if line.startswith("## "):
        return line in {
            "## Базовые слова",
            "## Приставки",
            "## Производные слова",
            "## Словообороты и выражения",
        }
    return active


def _extract_words(text: str) -> set[str]:
    return {
        normalize(match.group(0))
        for match in WORD_RE.finditer(text)
        if len(normalize(match.group(0))) >= 3
    }


def load_nickname76_words() -> set[str]:
    result: set[str] = set()
    active = False
    path = SOURCES_DIR / "nickname76_readme.md"
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("## "):
            active = _is_in_relevant_section(line, active)
            continue
        if not active:
            continue
        if line.startswith("- "):
            result.update(_extract_words(line[2:]))
        elif line.startswith("### "):
            result.update(_extract_words(line[4:]))
    return result


def load_source_words() -> set[str]:
    words = set()
    words.update(load_bars38_words())
    words.update(load_nickname76_words())
    return {
        word
        for word in words
        if any(marker in word for marker in SOURCE_MARKERS)
    }
