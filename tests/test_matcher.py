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
            "хуесос": "хуе*ос",
            "пидор": "пи*ор",
            "уебан": "уе*ан",
            "выблядок": "выбл*док",
            "мразь": "мр*зь",
            "шлюха": "шл*ха",
            "шмара": "шм*ра",
            "шлендра": "шле*дра",
            "шлёндра": "шлё*дра",
            "разъебал": "раз*ебал",
            "подъебка": "под*ебка",
            "съебался": "съе*ался",
            "охуевший": "охуе*ший",
            "пидорасина": "пидор*сина",
            "пиздецнахуй": "пиз*ецна*уй",
            "тывыблядок": "тывыбл*док",
            "пидораснахуй": "пид*расна*уй",
            "ебучийговнюк": "ебу*ийгов*юк",
            "шлюхасука": "шл*хасу*а",
            "мразотностью": "мра*отностью",
            "шмаристая": "шм*ристая",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(self.matcher.blur_text(source), expected)

    def test_blurs_inside_sentence(self) -> None:
        source = "ты хуесос и уебан, а это выблядок"
        expected = "ты хуе*ос и уе*ан, а это выбл*док"
        self.assertEqual(self.matcher.blur_text(source), expected)

    def test_does_not_blur_safe_words(self) -> None:
        safe_words = [
            "тебя",
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

    def test_does_not_blur_tebya_inside_phrase(self) -> None:
        source = "я бы тебя выебал"
        expected = "я бы тебя вы*бал"
        self.assertEqual(self.matcher.blur_text(source), expected)
