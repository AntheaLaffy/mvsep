import os
import json
from typing import Optional


DEFAULT_CONFIG_PATH = os.path.expanduser("~/.mvsep_cli_config")


class Config:
    DEFAULT_OUTPUT_FORMAT = 1
    DEFAULT_INTERVAL = 5
    DEFAULT_OUTPUT_DIR = "."
    DEFAULT_MIRROR = "main"

    MIRRORS = {
        "main": "https://mvsep.com",
        "mirror": "https://mirror.mvsep.com",
    }

    OUTPUT_FORMATS = {
        0: "mp3 (320 kbps)",
        1: "wav (16 bit)",
        2: "flac (16 bit)",
        3: "m4a (lossy)",
        4: "wav (32 bit)",
        5: "flac (24 bit)",
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self._config = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self._config, f, indent=2)

    @property
    def api_token(self) -> Optional[str]:
        return self._config.get("api_token")

    @api_token.setter
    def api_token(self, value: str):
        self._config["api_token"] = value
        self.save()

    @property
    def default_sep_type(self) -> Optional[int]:
        return self._config.get("sep_type")

    @default_sep_type.setter
    def default_sep_type(self, value: int):
        self._config["sep_type"] = value
        self.save()

    @property
    def default_output_format(self) -> int:
        return self._config.get("output_format", self.DEFAULT_OUTPUT_FORMAT)

    @default_output_format.setter
    def default_output_format(self, value: int):
        self._config["output_format"] = value
        self.save()

    @property
    def poll_interval(self) -> int:
        return self._config.get("interval", self.DEFAULT_INTERVAL)

    @poll_interval.setter
    def poll_interval(self, value: int):
        self._config["interval"] = value
        self.save()

    @property
    def default_output_dir(self) -> str:
        return self._config.get("output_dir", self.DEFAULT_OUTPUT_DIR)

    @default_output_dir.setter
    def default_output_dir(self, value: str):
        self._config["output_dir"] = value
        self.save()

    @property
    def mirror(self) -> str:
        return self._config.get("mirror", self.DEFAULT_MIRROR)

    @mirror.setter
    def mirror(self, value: str):
        if value not in self.MIRRORS:
            raise ValueError(
                f"Invalid mirror. Available: {', '.join(self.MIRRORS.keys())}"
            )
        self._config["mirror"] = value
        self.save()

    @property
    def base_url(self) -> str:
        return self.MIRRORS.get(self.mirror, self.MIRRORS["main"])


def get_api_token() -> str:
    env_token = os.environ.get("MVSEP_API_TOKEN")
    if env_token:
        return env_token

    config = Config()
    token = config.api_token
    if token:
        return token

    raise ValueError(
        "API token not found. Please either:\n"
        "  1. Set environment variable: export MVSEP_API_TOKEN='your_token'\n"
        "  2. Or configure with: mvsep config set-token <your_token>"
    )
