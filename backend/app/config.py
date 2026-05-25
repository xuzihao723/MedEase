from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"
LOGS_DIR = BACKEND_DIR / "logs"


def _load_env_file() -> None:
    env_path = BACKEND_DIR / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_file()


@dataclass(frozen=True)
class Settings:
    closeai_base_url: str = os.getenv("CLOSEAI_BASE_URL", "https://api.openai-proxy.org/v1")
    closeai_api_key: str = os.getenv("CLOSEAI_API_KEY", "")
    closeai_model: str = os.getenv("CLOSEAI_MODEL", "gpt-4.1-mini")
    closeai_fallback_model: str = os.getenv("CLOSEAI_FALLBACK_MODEL", "gpt-4o-mini")
    closeai_temperature: float = float(os.getenv("CLOSEAI_TEMPERATURE", "0.2"))
    request_timeout_seconds: float = float(os.getenv("CLOSEAI_TIMEOUT_SECONDS", "45"))
    backend_host: str = os.getenv("MEDEASE_BACKEND_HOST", "127.0.0.1")
    backend_port: int = int(os.getenv("MEDEASE_BACKEND_PORT", "8000"))
    logging_enabled: bool = os.getenv("MEDEASE_LOGGING_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"}
    logs_dir: Path = LOGS_DIR

    @property
    def closeai_ready(self) -> bool:
        return bool(self.closeai_api_key.strip())


settings = Settings()
