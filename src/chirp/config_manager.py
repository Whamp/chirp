from __future__ import annotations

import json
import re
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from platformdirs import PlatformDirs


@dataclass(kw_only=True, slots=True)
class ChirpConfig:
    primary_shortcut: str = "ctrl+shift"
    stt_backend: str = "parakeet"
    parakeet_model: str = "nemo-parakeet-tdt-0.6b-v3"
    parakeet_quantization: Optional[str] = None
    onnx_providers: str = "cpu"
    threads: Optional[int] = None
    language: Optional[str] = None
    word_overrides: Dict[str, str] = field(default_factory=dict)
    whisper_prompt: str = ""
    paste_mode: str = "ctrl"
    clipboard_behavior: bool = True
    clipboard_clear_delay: float = 0.75
    audio_feedback: bool = True
    start_sound_path: Optional[str] = None
    stop_sound_path: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChirpConfig":
        merged = DEFAULT_CONFIG | data
        merged["word_overrides"] = {
            str(k).lower(): str(v) for k, v in merged.get("word_overrides", {}).items()
        }
        merged["primary_shortcut"] = str(merged["primary_shortcut"]).lower()
        merged["paste_mode"] = str(merged["paste_mode"]).lower()
        merged["onnx_providers"] = str(merged["onnx_providers"]).lower()
        quant = merged.get("parakeet_quantization")
        merged["parakeet_quantization"] = str(quant).lower() if quant else None
        lang = merged.get("language")
        merged["language"] = str(lang) if lang else None
        return cls(**merged)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["word_overrides"] = dict(self.word_overrides)
        return payload


DEFAULT_CONFIG: Dict[str, Any] = {
    "primary_shortcut": "win+alt+d",
    "stt_backend": "parakeet",
    "parakeet_model": "nemo-parakeet-tdt-0.6b-v3",
    "parakeet_quantization": None,
    "onnx_providers": "cpu",
    "threads": None,
    "language": None,
    "word_overrides": {},
    "whisper_prompt": "",
    "paste_mode": "ctrl",
    "clipboard_behavior": True,
    "clipboard_clear_delay": 0.75,
    "audio_feedback": True,
    "start_sound_path": None,
    "stop_sound_path": None,
}


class ConfigManager:
    def __init__(self, *, app_name: str = "Chirp", legacy_app_author: Optional[str] = "Will") -> None:
        dirs = PlatformDirs(appname=app_name, appauthor=False, roaming=True)
        self._base_dir = Path(dirs.user_config_dir)
        self._config_path = self._base_dir / "config.json"
        self._models_root = self._base_dir / "models"
        self._migrate_legacy_path(app_name=app_name, legacy_app_author=legacy_app_author)

    @property
    def config_path(self) -> Path:
        return self._config_path

    @property
    def models_root(self) -> Path:
        return self._models_root

    def ensure_exists(self) -> None:
        if self._config_path.exists():
            return
        self._base_dir.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")

    def load(self) -> ChirpConfig:
        self.ensure_exists()
        data = json.loads(self._config_path.read_text(encoding="utf-8"))
        return ChirpConfig.from_dict(data)

    def save(self, config: ChirpConfig) -> None:
        self._base_dir.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")

    def model_dir(self, model_name: str, quantization: Optional[str]) -> Path:
        suffix = "-int8" if (quantization or "").lower() == "int8" else ""
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", model_name.lower()).strip("-") or "model"
        return self._models_root / f"{safe}{suffix}"

    def _migrate_legacy_path(self, *, app_name: str, legacy_app_author: Optional[str]) -> None:
        if not legacy_app_author:
            return
        if self._base_dir.exists():
            return
        legacy_dirs = PlatformDirs(appname=app_name, appauthor=legacy_app_author, roaming=True)
        legacy_dir = Path(legacy_dirs.user_config_dir)
        if not legacy_dir.exists():
            return
        try:
            legacy_dir.rename(self._base_dir)
            return
        except OSError:
            pass
        self._base_dir.mkdir(parents=True, exist_ok=True)
        for item in legacy_dir.iterdir():
            target = self._base_dir / item.name
            if target.exists():
                continue
            if item.is_dir():
                shutil.copytree(item, target)
            else:
                shutil.copy2(item, target)
