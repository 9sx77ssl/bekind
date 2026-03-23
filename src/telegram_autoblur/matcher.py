from __future__ import annotations

import re
from dataclasses import dataclass

from telegram_autoblur.loader import WORD_RE, load_manual_words, load_patterns, load_safe_words, load_source_words, normalize


@dataclass(frozen=True)
class Matcher:
    exact_words: frozenset[str]
    safe_words: frozenset[str]
    patterns: tuple[re.Pattern[str], ...]

    def should_blur(self, word: str) -> bool:
        normalized = normalize(word)
        if len(normalized) < 3:
            return False
        if normalized in self.safe_words:
            return False
        if normalized in self.exact_words:
            return True
        return any(pattern.match(normalized) for pattern in self.patterns)

    def blur_word(self, word: str) -> str:
        if len(word) <= 2:
            return word
        if len(word) == 3:
            return f"{word[0]}*{word[-1]}"
        if len(word) == 4:
            return f"{word[:2]}*{word[-1]}"
        return f"{word[:2]}*{word[-2:]}"

    def blur_text(self, text: str) -> str:
        def replace(match: re.Match[str]) -> str:
            token = match.group(0)
            return self.blur_word(token) if self.should_blur(token) else token

        return WORD_RE.sub(replace, text)


def build_matcher() -> Matcher:
    exact_words = load_source_words()
    exact_words.update(load_manual_words())
    safe_words = load_safe_words()
    patterns = tuple(re.compile(pattern) for pattern in load_patterns())
    return Matcher(
        exact_words=frozenset(exact_words),
        safe_words=frozenset(safe_words),
        patterns=patterns,
    )


DEFAULT_MATCHER = build_matcher()


def should_blur(word: str) -> bool:
    return DEFAULT_MATCHER.should_blur(word)


def blur_word(word: str) -> str:
    return DEFAULT_MATCHER.blur_word(word)


def blur_text(text: str) -> str:
    return DEFAULT_MATCHER.blur_text(text)
