from __future__ import annotations

from dataclasses import dataclass
import re

from telegram_autoblur.loader import WORD_RE, load_manual_words, load_patterns, load_roots, load_safe_words, load_source_words, normalize


@dataclass(frozen=True)
class Matcher:
    exact_words: frozenset[str]
    roots: tuple[str, ...]
    safe_words: frozenset[str]
    patterns: tuple[re.Pattern[str], ...]

    def _exact_spans(self, normalized: str) -> list[tuple[int, int]]:
        spans: list[tuple[int, int]] = []
        for candidate in self.exact_words:
            if len(candidate) < 4:
                if normalized == candidate:
                    spans.append((0, len(candidate)))
                continue
            start = normalized.find(candidate)
            while start != -1:
                spans.append((start, start + len(candidate)))
                start = normalized.find(candidate, start + 1)
        return spans

    def _pattern_spans(self, normalized: str) -> list[tuple[int, int]]:
        spans: list[tuple[int, int]] = []
        for start in range(len(normalized)):
            suffix = normalized[start:]
            for pattern in self.patterns:
                match = pattern.match(suffix)
                if match:
                    if match.end() < 4:
                        continue
                    spans.append((start, start + match.end()))
        return spans

    def _root_spans(self, normalized: str) -> list[tuple[int, int]]:
        spans: list[tuple[int, int]] = []
        for root in self.roots:
            if len(root) < 4:
                if normalized == root:
                    spans.append((0, len(root)))
                continue
            start = normalized.find(root)
            while start != -1:
                spans.append((start, start + len(root)))
                start = normalized.find(root, start + 1)
        return spans

    def _select_spans(self, spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
        selected: list[tuple[int, int]] = []
        for start, end in sorted(spans, key=lambda item: (item[0], -(item[1] - item[0]))):
            if any(not (end <= kept_start or start >= kept_end) for kept_start, kept_end in selected):
                continue
            selected.append((start, end))
        return selected

    def _blur_spans(self, word: str, spans: list[tuple[int, int]]) -> str:
        chars = list(word)
        for start, end in spans:
            if end - start <= 0:
                continue
            middle = start + ((end - start) // 2)
            if 0 <= middle < len(chars):
                chars[middle] = "*"
        return "".join(chars)

    def find_blur_spans(self, word: str) -> list[tuple[int, int]]:
        normalized = normalize(word)
        if len(normalized) < 3:
            return []
        if normalized in self.safe_words:
            return []
        if any(normalized.startswith(safe_word) for safe_word in self.safe_words if len(safe_word) >= 4):
            return []

        spans = self._exact_spans(normalized)
        spans.extend(self._root_spans(normalized))
        spans.extend(self._pattern_spans(normalized))
        return self._select_spans(spans)

    def should_blur(self, word: str) -> bool:
        return bool(self.find_blur_spans(word))

    def blur_word(self, word: str) -> str:
        spans = self.find_blur_spans(word)
        if not spans:
            return word
        return self._blur_spans(word, spans)

    def blur_text(self, text: str) -> str:
        def replace(match: re.Match[str]) -> str:
            token = match.group(0)
            return self.blur_word(token) if self.should_blur(token) else token

        return WORD_RE.sub(replace, text)


def build_matcher() -> Matcher:
    exact_words = load_source_words()
    exact_words.update(load_manual_words())
    roots = tuple(sorted(load_roots(), key=len, reverse=True))
    safe_words = load_safe_words()
    patterns = tuple(re.compile(pattern) for pattern in load_patterns())
    return Matcher(
        exact_words=frozenset(exact_words),
        roots=roots,
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
