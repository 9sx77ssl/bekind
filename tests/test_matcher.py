from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from telegram_autoblur.matcher import build_matcher


class MatcherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matcher = build_matcher()

    def test_blurs_requested_words(self) -> None:
        cases = {
            "хуесос": "ху*ос",
            "пидор": "пи*ор",
            "уебан": "уе*ан",
            "выблядок": "вы*ок",
            "мразь": "мр*зь",
            "шлюха": "шл*ха",
            "шмара": "шм*ра",
            "разъебал": "ра*ал",
            "подъебка": "по*ка",
            "съебался": "съ*ся",
            "охуевший": "ох*ий",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(self.matcher.blur_text(source), expected)

    def test_blurs_inside_sentence(self) -> None:
        source = "ты хуесос и уебан, а это выблядок"
        expected = "ты ху*ос и уе*ан, а это вы*ок"
        self.assertEqual(self.matcher.blur_text(source), expected)

    def test_does_not_blur_safe_words(self) -> None:
        safe_words = [
            "страхуй",
            "подстрахуй",
            "мандат",
            "мандарин",
            "хулиган",
            "хулиганить",
            "сукно",
            "спам",
            "spam",
            "аборт",
            "вагина",
            "клитор",
        ]
        for word in safe_words:
            with self.subTest(word=word):
                self.assertEqual(self.matcher.blur_text(word), word)

    def test_does_not_touch_clean_sentence(self) -> None:
        source = "подстрахуй меня и возьми мандарин у хулигана"
        self.assertEqual(self.matcher.blur_text(source), source)
