from __future__ import annotations

from pathlib import Path

from huggingface_hub import snapshot_download

from .config_manager import ConfigManager


REPO_MAP = {
    "nemo-parakeet-tdt-0.6b-v3": "istupakov/parakeet-tdt-0.6b-v3-onnx",
}


def _model_ready(model_dir: Path) -> bool:
    return (model_dir / "config.json").exists() and any(model_dir.glob("*.onnx"))


def _resolve_repo(model_name: str) -> str:
    repo = REPO_MAP.get(model_name)
    if not repo:
        raise SystemExit(f"Unsupported model '{model_name}'.")
    return repo


def main() -> None:
    config_manager = ConfigManager()
    config = config_manager.load()
    model_dir = config_manager.model_dir(config.parakeet_model, config.parakeet_quantization)
    repo_id = _resolve_repo(config.parakeet_model)

    if _model_ready(model_dir):
        print(f"Model already present at {model_dir}")
        return

    model_dir.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id, local_dir=str(model_dir), local_dir_use_symlinks=False)
    print(f"Downloaded model snapshot to {model_dir}")


if __name__ == "__main__":  # pragma: no cover
    main()
