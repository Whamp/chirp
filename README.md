# Chirp

Chirp is a Windows dictation app that runs fully locally using ParakeetV3 and is managed end-to-end with `uv`. Chirp does not require the ability to run executable files (like .exe) on Windows. It was designed so that if you're allowed to run Python on your machine, you can run Chirp. 

## Why ParakeetV3? 

ParakeetV3 has indistinguishable accuracy from Whisper-large-V3 (multilingual WER 4.91 vs 5.05) but is 17x faster and only requires a CPU while Whisper models of comparable accuracy require GPU's. 

https://huggingface.co/spaces/hf-audio/open_asr_leaderboard

## Goals
- Provide fast, reliable, local-first dictation on Windows.
- Keep onboarding to a single setup step with predictable daily usage.
- Maintain a minimal, auditable codebase with explicit configuration.

## Features
- Local STT via Parakeet TDT 0.6B v3 with optional int8 quantization.
- Global hotkey to toggle capture, clipboard paste injection, and configurable word overrides.
- Optional audio feedback cues and style prompting for post-processed text.
- CPU support by default with optional GPU providers when available.

## Architecture
- `src/chirp/main.py` — CLI entrypoint and application loop.
- `src/chirp/config_manager.py` — configuration loading and Windows-specific paths.
- `src/chirp/parakeet_manager.py` — Parakeet backend integration and provider handling.
- `src/chirp/setup.py` — one-time setup routine that prepares local model assets.

## Setup (Windows, uv-only)
1. Clone the repository and enter it:
   ```powershell
   git clone https://github.com/Whamp/chirp.git
   cd chirp
   uv run python -m chirp.setup #one-time setup and model downloading
   ```
   
## Running
- Daily usage (preferred, works even on systems that block `.exe` launchers):
  ```powershell
  uv run python -m chirp.main
  ```
- Verbose/debug logging:
  ```powershell
  uv run python -m chirp.main -- --verbose
  ```
- CLI help and options:
  ```powershell
  uv run python -m chirp.main -- --help
  ```

## Removal
- Delete the cloned `chirp` directory.
- That's it. 

### Acknowledgments

- NVIDA - https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3
- Ilya Stupakov - https://huggingface.co/istupakov/parakeet-tdt-0.6b-v3-onnx