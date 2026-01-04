# Canonical Package Build Fix

## Issue

When building the canonical package, hatchling couldn't determine which files to ship in the wheel because it couldn't find the package directory. Additionally, the package structure needed to be reorganized to use the standard Python `src/` layout.

## Error

```
ValueError: Unable to determine which files to ship inside the wheel
The most likely cause of this is that there is no directory that matches the
name of your project (canonical).
```

## Solution

### 1. Restructured to src/ Layout

Moved package files to the standard Python package structure:
- `canonical/__init__.py` → `canonical/src/canonical/__init__.py`
- `canonical/registry.py` → `canonical/src/canonical/registry.py`
- `canonical/entities/` → `canonical/src/canonical/entities/`
- `canonical/events/` → `canonical/src/canonical/events/`
- `canonical/semantics/` → `canonical/src/canonical/semantics/`

### 2. Updated pyproject.toml

```toml
[tool.hatch.build.targets.wheel]
# Package is in src/canonical/ directory (standard Python package structure)
# Hatchling automatically maps src/canonical/ to canonical/ in the wheel
# Data directories (entities, events, semantics) are now in src/canonical/
# so they'll be included automatically as part of the package
packages = ["src/canonical"]
```

### 3. Updated Registry Paths

Updated `registry.py` to use package-relative paths:
```python
# Data directories are now in the package directory (src/canonical/)
_BASE_DIR = Path(__file__).parent
_ENTITIES_DIR = _BASE_DIR / "entities"
_EVENTS_DIR = _BASE_DIR / "events"
_SEMANTICS_DIR = _BASE_DIR / "semantics"
```

This ensures:
1. The package uses the standard Python `src/` layout
2. Hatchling correctly identifies and packages the code
3. Data directories are included as part of the package
4. Paths work both in development and when installed

## Additional Fix: Direct References

When services use the canonical package as a local dependency, hatchling requires explicit permission for direct references. Added to all service `pyproject.toml` files:

```toml
[tool.hatch.metadata]
allow-direct-references = true
```

## Dependency Format

All services now use the absolute path format:

```toml
dependencies = [
    "canonical @ file:///media/prashanth/extmnt1/rmbrain/canonical",
    # ... other dependencies
]
```

**Note:** This uses an absolute path. For portability, use the `scripts/update_canonical_paths.py` script to update paths based on your repository location.

## Update Script

A helper script `scripts/update_canonical_paths.py` is available to update all service `pyproject.toml` files with the correct canonical path based on the current repository location.

Usage:
```bash
python3 scripts/update_canonical_paths.py
```

This will update all service `pyproject.toml` files with the correct absolute path to the canonical directory.

## Verification

After fixes:
- ✅ Canonical package builds successfully
- ✅ Services can install canonical dependency
- ✅ Services can import from canonical library
- ✅ All schema/event/semantic files are included in the package

## Future Improvements

For production deployment, consider:
1. Using uv workspace feature for better monorepo support
2. Publishing canonical as a proper package to a private registry
3. Using environment variables or build scripts to resolve paths dynamically
