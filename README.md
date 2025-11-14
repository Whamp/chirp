# Chirp

Chirp is a Windows dictation app that runs fully locally using Parakeet speech-to-text models and is managed end-to-end with `uv`.

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
   # optionally using gh cli
   # gh repo clone Whamp/chirp
   cd chirp
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
- (Optional) remove Chirp user data from your Roaming profile:
  ```powershell
  Remove-Item -Recurse -Force "$Env:AppData\Chirp"
  ```
