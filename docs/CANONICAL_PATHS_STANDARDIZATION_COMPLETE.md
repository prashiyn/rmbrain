# Canonical Paths Standardization - Complete

## Overview

All canonical schema, event, and semantic paths have been standardized across all services. Paths are now defined in each service's `config.py` file and used consistently throughout the codebase.

## Standard Pattern

### config.py Pattern

Each service's `config.py` now includes three computed properties:

```python
from pathlib import Path

class Settings(BaseSettings):
    # ... existing fields ...
    
    # Canonical schema paths (computed properties)
    @property
    def canonical_entities_dir(self) -> Path:
        """Path to canonical/entities/ directory."""
        repo_root = Path(__file__).parent.parent.parent  # Adjust depth as needed
        return repo_root / "canonical" / "entities"
    
    @property
    def canonical_events_dir(self) -> Path:
        """Path to canonical/events/ directory."""
        repo_root = Path(__file__).parent.parent.parent
        return repo_root / "canonical" / "events"
    
    @property
    def canonical_semantics_dir(self) -> Path:
        """Path to canonical/semantics/ directory."""
        repo_root = Path(__file__).parent.parent.parent
        return repo_root / "canonical" / "semantics"
```

### Usage Pattern

All code now uses these properties:

```python
from <service>.config import settings

# Instead of:
repo_root = Path(__file__).parent.parent.parent.parent
canonical_events_dir = repo_root / "canonical" / "events"

# Use:
canonical_events_dir = settings.canonical_events_dir
```

## Services Updated

### 1. client_service ✅
**Files Updated:**
- `cds_client/config.py` - Added canonical path properties
- `cds_client/event_validator.py` - Uses `settings.canonical_events_dir`
- `cds_client/schema_validator.py` - Uses `settings.canonical_entities_dir`

**Repo Root Depth:** 3 levels (`client_service/cds_client/config.py` → `client_service/` → repo_root)

### 2. task_service ✅
**Files Updated:**
- `cds_task/config.py` - Added canonical path properties
- `cds_task/event_envelope.py` - Uses `settings.canonical_events_dir`
- `cds_task/json_schema.py` - Uses `settings.canonical_entities_dir`

**Repo Root Depth:** 3 levels

### 3. document_service ✅
**Files Updated:**
- `cds_document/config.py` - Added canonical path properties
- `cds_document/validators.py` - Uses `settings.canonical_entities_dir` and `settings.canonical_events_dir` (3 locations)

**Repo Root Depth:** 3 levels

### 4. interaction_service ✅
**Files Updated:**
- `cds_interaction/app/config.py` - Added canonical path properties
- `cds_interaction/app/main.py` - Uses `settings.canonical_events_dir`
- `cds_interaction/tests/conftest.py` - Uses `settings.canonical_entities_dir`
- `cds_interaction/tests/test_envelope_validator.py` - Uses `settings.canonical_events_dir`
- `cds_interaction/tests/test_event_handler.py` - Uses `settings.canonical_events_dir`
- `cds_interaction/tests/test_payload_validator.py` - Uses `settings.canonical_events_dir`

**Repo Root Depth:** 4 levels (`interaction_service/cds_interaction/app/config.py` → `interaction_service/cds_interaction/` → `interaction_service/` → repo_root)

**Note:** `cds_interaction/services/` validators take paths as constructor parameters, so they're fine.

### 5. relationship_service ✅
**Files Updated:**
- `cds_relationship/config.py` - Added canonical path properties
- `cds_relationship/services/event_validator.py` - Uses `settings.canonical_events_dir`
- `cds_relationship/services/schema_validator.py` - Uses `settings.canonical_entities_dir`

**Repo Root Depth:** 3 levels

### 6. product_service ✅
**Files Updated:**
- `app/config.py` - Added canonical path properties
- `app/validation/validate.py` - Uses `settings.canonical_events_dir` and `settings.canonical_entities_dir` (replaced module constants)

**Repo Root Depth:** 3 levels

### 7. riskprofile_service ✅
**Files Updated:**
- `app/config.py` - Added canonical path properties
- `app/validation/envelope.py` - Uses `settings.canonical_events_dir` (replaced module constant)
- `app/validation/validate.py` - Uses `settings.canonical_entities_dir` (replaced module constant)

**Repo Root Depth:** 3 levels

### 8. cas_service ✅
**Files Updated:**
- `cas_audit/config.py` - Added canonical path properties (for consistency)

**Note:** CAS service uses local audit schemas (`schemas/audit_event.v1.schema.json`), not canonical schemas. Properties added for consistency but not currently used.

**Repo Root Depth:** 3 levels

### 9. policy_service ℹ️
**Status:** No changes needed

**Reason:** Policy service uses policy-specific schemas (`schemas/policy_rules.v1.schema.json`), not canonical schemas. No canonical path properties needed.

## Files Not Updated (By Design)

### Validation Scripts
These standalone utility scripts can keep direct path calculations:
- `interaction_service/verify_schema_consistency.py`
- `client_service/scripts/validate_schema_consistency.py`
- `relationship_service/verify_schema_sync.py`
- `riskprofile_service/check_consistency.py`

**Reason:** These are utility scripts, not part of the service runtime code. They can calculate paths directly.

### rmbrain-mainapp
These files are part of the main app infrastructure and can keep their path calculations:
- `app/schemas/validation.py` - Uses `REPO_ROOT` constant
- `app/shared/canonical_schema_sdk/registry.py` - Uses `REPO_ROOT` constant

**Reason:** These are infrastructure-level files, not service code. They can use their own path calculation patterns.

## Benefits

1. **Centralized Configuration**: All canonical paths defined in one place per service (`config.py`)
2. **Easy Updates**: Change path calculation in one location if needed
3. **Consistency**: All services use the same pattern
4. **Maintainability**: Easier to understand and modify
5. **Testability**: Can mock `settings` in tests
6. **Type Safety**: Properties return `Path` objects with proper typing

## Verification

### All Services Have Properties ✅
- ✅ client_service
- ✅ task_service
- ✅ document_service
- ✅ interaction_service
- ✅ relationship_service
- ✅ product_service
- ✅ riskprofile_service
- ✅ cas_service

### All Code Uses Settings ✅
- ✅ Event validators use `settings.canonical_events_dir`
- ✅ Schema validators use `settings.canonical_entities_dir`
- ✅ Test fixtures use `settings` paths
- ✅ No hardcoded path calculations in service code

## Migration Complete

All canonical paths are now standardized and centralized in each service's `config.py` file. This makes the codebase more maintainable and consistent.
