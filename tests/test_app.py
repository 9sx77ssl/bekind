from pathlib import Path
import os
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from telegram_autoblur.config import load_settings


class ConfigTests(unittest.TestCase):
    def test_load_settings_from_environment(self) -> None:
        old_api_id = os.environ.get("TG_API_ID")
        old_api_hash = os.environ.get("TG_API_HASH")
        old_session_name = os.environ.get("TG_SESSION_NAME")
        try:
            os.environ["TG_API_ID"] = "123456"
            os.environ["TG_API_HASH"] = "hash"
            os.environ["TG_SESSION_NAME"] = "session"
            settings = load_settings()
            self.assertEqual(settings.api_id, 123456)
            self.assertEqual(settings.api_hash, "hash")
            self.assertEqual(settings.session_name, "session")
        finally:
            if old_api_id is None:
                os.environ.pop("TG_API_ID", None)
            else:
                os.environ["TG_API_ID"] = old_api_id
            if old_api_hash is None:
                os.environ.pop("TG_API_HASH", None)
            else:
                os.environ["TG_API_HASH"] = old_api_hash
            if old_session_name is None:
                os.environ.pop("TG_SESSION_NAME", None)
            else:
                os.environ["TG_SESSION_NAME"] = old_session_name
