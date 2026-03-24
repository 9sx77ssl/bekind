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
    "еба",
    "ебл",
    "ебн",
    "ебуч",
    "ебаш",
    "ебош",
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
    "хуй",
    "хуе",
    "шалав",
    "шлюх",
    "шмар",
    "ублюд",
    "говн",
    "дерьм",
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


def load_roots() -> set[str]:
    return {normalize(line) for line in read_lines(DATA_DIR / "roots.txt")}


def load_bars38_words() -> set[str]:
    return {normalize(line) for line in read_lines(SOURCES_DIR / "bars38_words.txt")}


def load_source_words() -> set[str]:
    words = load_bars38_words()
    return {
        word
        for word in words
        if any(marker in word for marker in SOURCE_MARKERS)
    }
