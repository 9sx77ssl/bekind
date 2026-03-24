from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    api_id: int
    api_hash: str
    session_name: str


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _dotenv_candidates() -> list[Path]:
    return [
        Path.cwd() / ".env",
        PROJECT_ROOT / ".env",
    ]


def _load_dotenv() -> None:
    for env_path in _dotenv_candidates():
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
        return


def load_settings() -> Settings:
    _load_dotenv()

    api_id_raw = os.environ.get("TG_API_ID", "").strip()
    api_hash = os.environ.get("TG_API_HASH", "").strip()
    session_name = os.environ.get("TG_SESSION_NAME", "bekind").strip() or "bekind"

    if not api_id_raw:
        raise RuntimeError("Missing TG_API_ID. Add it to .env or export it in the shell.")

    if not api_hash:
        raise RuntimeError("Missing TG_API_HASH. Add it to .env or export it in the shell.")

    try:
        api_id = int(api_id_raw)
    except ValueError as exc:
        raise RuntimeError("TG_API_ID must be an integer.") from exc

    session_path = PROJECT_ROOT / session_name

    return Settings(api_id=api_id, api_hash=api_hash, session_name=str(session_path))
