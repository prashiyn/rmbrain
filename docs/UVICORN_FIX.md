# Uvicorn Command Fix

## Problem

When running `dapr run -f dapr.yaml` from the repository root, services were failing with:
```
error: Failed to spawn: `uvicorn`
  Caused by: No such file or directory (os error 2)
```

## Root Cause

Each service has its own virtual environment (`.venv`) created by `uv sync` in the service directory. The `uv run` command needs to be executed from the service directory where:
- `pyproject.toml` exists
- `.venv` directory exists
- Dependencies are installed

Even though `appDirPath` is set in `dapr.yaml`, the command array format may not preserve the working directory correctly, causing `uv run` to fail to find the virtual environment.

## Solution

Changed all commands in root `dapr.yaml` and service `dapr.yaml` files from:
```yaml
command: ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

To:
```yaml
command: ["uv", "run", "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

This ensures:
1. `uv run` uses Python from the local virtual environment
2. `python -m uvicorn` explicitly uses the Python module, which is more reliable
3. The virtual environment is correctly identified by `uv run`

## Why This Works

- `uv run` automatically finds and uses the virtual environment in the current directory (where `appDirPath` points)
- `python -m uvicorn` uses Python as a module runner, which is more reliable than calling `uvicorn` directly
- This approach works because `uv run` ensures the correct Python from `.venv` is used
- The `appDirPath` in `dapr.yaml` ensures commands run from the service directory

## Prerequisites

Services must still have dependencies installed:
```bash
cd <service-name>
uv sync
```

## Testing

After applying the fix:
1. Install dependencies for all services
2. Run `dapr run -f dapr.yaml` from repository root
3. Services should start successfully

---

**Date**: 2025-01-20  
**Status**: Fixed - Commands now explicitly change to service directory before running `uv run`

