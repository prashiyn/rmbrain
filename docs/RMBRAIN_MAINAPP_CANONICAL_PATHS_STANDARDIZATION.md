# rmbrain-mainapp Canonical Paths Standardization

## Summary

Standardized canonical schema paths in `rmbrain-mainapp` to use centralized configuration from `app/config.py`, aligning with the pattern used across all other services.

## Changes Made

### 1. `app/config.py`
- **Added**: `Path` import
- **Added**: `repo_root` property to calculate repository root (3 levels up from `app/config.py`)
- **Added**: `canonical_entities_dir` property pointing to `canonical/entities/`
- **Added**: `canonical_events_dir` property pointing to `canonical/events/`
- **Added**: `canonical_semantics_dir` property pointing to `canonical/semantics/`

**Pattern**:
```python
@property
def repo_root(self) -> Path:
    """Get repository root directory."""
    return Path(__file__).parent.parent.parent

@property
def canonical_entities_dir(self) -> Path:
    """Get canonical entities directory path."""
    return self.repo_root / "canonical" / "entities"
```

### 2. `app/schemas/validation.py`
- **Removed**: Direct `REPO_ROOT` calculation using `Path(__file__).parent.parent.parent.parent`
- **Removed**: Direct `CANONICAL_EVENTS_DIR` calculation
- **Added**: Import of `settings` from `app.config`
- **Updated**: `CANONICAL_EVENTS_DIR` to use `settings.canonical_events_dir`

**Before**:
```python
REPO_ROOT = Path(__file__).parent.parent.parent.parent
CANONICAL_EVENTS_DIR = REPO_ROOT / "canonical" / "events"
```

**After**:
```python
from app.config import settings

CANONICAL_EVENTS_DIR = settings.canonical_events_dir
```

### 3. `app/shared/canonical_schema_sdk/registry.py`
- **Removed**: Direct `REPO_ROOT` calculation using `Path(__file__).parent.parent.parent.parent.parent`
- **Removed**: Direct `SCHEMAS_DIR` and `SEMANTICS_DIR` calculations
- **Added**: Import of `settings` from `app.config`
- **Updated**: Module-level constants `SCHEMAS_DIR` and `SEMANTICS_DIR` to use `settings.canonical_entities_dir` and `settings.canonical_semantics_dir`

**Before**:
```python
REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent
SCHEMAS_DIR = REPO_ROOT / "canonical" / "entities"
SEMANTICS_DIR = REPO_ROOT / "canonical" / "semantics"
```

**After**:
```python
from app.config import settings

SCHEMAS_DIR = settings.canonical_entities_dir
SEMANTICS_DIR = settings.canonical_semantics_dir
```

**Note**: The module-level constants are maintained for backward compatibility with tests that patch them (e.g., `test_canonical_schema_sdk.py`).

## Files Updated

1. ✅ `rmbrain-mainapp/app/config.py` - Added canonical path properties
2. ✅ `rmbrain-mainapp/app/schemas/validation.py` - Updated to use `settings.canonical_events_dir`
3. ✅ `rmbrain-mainapp/app/shared/canonical_schema_sdk/registry.py` - Updated to use `settings.canonical_entities_dir` and `settings.canonical_semantics_dir`

## Test Compatibility

- **`tests/test_canonical_schema_sdk.py`**: No changes needed. Tests patch `SCHEMAS_DIR` and `SEMANTICS_DIR` module-level constants, which are still present and now sourced from `settings`.
- **`tests/test_schema_validation.py`**: No changes needed. Tests use the validation functions which now internally use `settings.canonical_events_dir`.

## Benefits

1. **Centralized Configuration**: All canonical paths are now defined in one place (`app/config.py`)
2. **Consistency**: Aligns with the pattern used across all other services
3. **Maintainability**: If canonical directory structure changes, only `config.py` needs updating
4. **Test Compatibility**: Module-level constants are preserved, allowing existing tests to continue working

## Verification

All changes follow the same pattern established in other services:
- Paths are calculated from `config.py` location
- Properties use `@property` decorator for lazy evaluation
- Module-level constants in `registry.py` are maintained for test compatibility
- No breaking changes to existing code or tests

## Status

✅ **Complete** - All canonical paths in `rmbrain-mainapp` are now standardized and centralized in `app/config.py`.
