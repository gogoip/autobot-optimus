# Autobot Optimus Local Scaffold

This repository now includes executable local scaffolding for:

- `backend/` API + orchestration endpoints
- `agent/` state machine + tool-calling loop
- `ui/` chat + approval dashboard shell
- `data/` schema + deterministic seed script

## One-command local startup (Windows VS Code friendly)

From repository root in VS Code terminal:

```powershell
./scripts/run-local.ps1
```

The script will:

1. Seed deterministic local data (`data/seed.py`)
2. Start backend (`backend/main.py`)
3. Start agent loop (`agent/main.py`)
4. Start UI server (`ui/main.py`)

## Alternative cross-platform command

```bash
python scripts/run_local.py
```


## Python dependencies

Install runtime and test dependencies before starting services:

```bash
python -m pip install -r requirements.txt
```

Run backend API tests:

```bash
pytest backend/tests/test_api.py
```
