"""Configuration management."""
import os
from dataclasses import dataclass


@dataclass
class Config:
    api_url: str = "http://localhost:3000"
    api_token: str = ""
    debug: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            api_url=os.getenv("API_URL", cls.api_url),
            api_token=os.getenv("API_TOKEN", cls.api_token),
            debug=os.getenv("DEBUG", "").lower() in ("1", "true"),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
        )
