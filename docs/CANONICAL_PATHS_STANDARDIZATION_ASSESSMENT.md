# Canonical Paths Standardization Assessment

## Objective
Standardize all canonical schema/event/semantic paths across all services by defining them in each service's `config.py` file.

## Current State Analysis

### Pattern 1: Inline Path Calculation (Most Common)
**Services using this pattern:**
- `client_service/cds_client/event_validator.py` - Lines 21-22
- `client_service/cds_client/schema_validator.py` - Lines 20-21
- `document_service/cds_document/validators.py` - Lines 19-20, 80-81, 107-109
- `relationship_service/cds_relationship/services/event_validator.py` - Lines 16-17
- `interaction_service/cds_interaction/app/main.py` - Lines 25-27

**Pattern:**
```python
repo_root = Path(__file__).parent.parent.parent.parent  # Varies by depth
canonical_events_dir = repo_root / "canonical" / "events"
canonical_entities_dir = repo_root / "canonical" / "entities"
```

### Pattern 2: Module-Level Constants
**Services using this pattern:**
- `product_service/app/validation/validate.py` - Lines 13-15
- `riskprofile_service/app/validation/envelope.py` - Lines 10-11
- `task_service/cds_task/event_envelope.py` - Lines 19-24
- `task_service/cds_task/json_schema.py` - Line 19

**Pattern:**
```python
REPO_ROOT = Path(__file__).parent.parent.parent.parent
CANONICAL_EVENTS_DIR = REPO_ROOT / "canonical" / "events"
CANONICAL_ENTITIES_DIR = REPO_ROOT / "canonical" / "entities"
```

### Pattern 3: Instance Variables
**Services using this pattern:**
- `relationship_service/cds_relationship/services/event_validator.py` - Lines 16-17 (in __init__)

**Pattern:**
```python
def __init__(self):
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    self.canonical_events_dir = repo_root / "canonical" / "events"
```

### Pattern 4: Local Schema (Non-Canonical)
**Services using this pattern:**
- `cas_service/cas_audit/schema_validator.py` - Line 16 (uses local schemas/ directory)

**Note:** CAS service has audit-specific schemas that are NOT canonical. These should remain local.

## Standardization Plan

### Step 1: Add Canonical Path Properties to config.py

Each service's `config.py` should include:

```python
from pathlib import Path

class Settings(BaseSettings):
    # ... existing fields ...
    
    # Canonical schema paths (computed properties)
    @property
    def canonical_entities_dir(self) -> Path:
        """Path to canonical/entities/ directory."""
        # Calculate repo root from config.py location
        # config.py is typically at: <service>/<module>/config.py
        # Repo root is typically 3-4 levels up
        repo_root = Path(__file__).parent.parent.parent.parent
        return repo_root / "canonical" / "entities"
    
    @property
    def canonical_events_dir(self) -> Path:
        """Path to canonical/events/ directory."""
        repo_root = Path(__file__).parent.parent.parent.parent
        return repo_root / "canonical" / "events"
    
    @property
    def canonical_semantics_dir(self) -> Path:
        """Path to canonical/semantics/ directory."""
        repo_root = Path(__file__).parent.parent.parent.parent
        return repo_root / "canonical" / "semantics"
```

**Note:** The number of `parent` calls may vary by service structure. Need to verify for each service.

### Step 2: Update All Code to Use config.settings

Replace all inline path calculations with:
```python
from <service>.config import settings

# Instead of:
repo_root = Path(__file__).parent.parent.parent.parent
canonical_events_dir = repo_root / "canonical" / "events"

# Use:
from cds_client.config import settings
canonical_events_dir = settings.canonical_events_dir
```

## Service-by-Service Changes Required

### 1. client_service
**Files to update:**
- `cds_client/config.py` - Add canonical path properties
- `cds_client/event_validator.py` - Use settings.canonical_events_dir
- `cds_client/schema_validator.py` - Use settings.canonical_entities_dir

**Repo root calculation:** `Path(__file__).parent.parent.parent.parent` (from cds_client/)

### 2. task_service
**Files to update:**
- `cds_task/config.py` - Add canonical path properties
- `cds_task/event_envelope.py` - Use settings.canonical_events_dir
- `cds_task/json_schema.py` - Use settings.canonical_entities_dir

**Repo root calculation:** `Path(__file__).parent.parent.parent.parent` (from cds_task/)

### 3. document_service
**Files to update:**
- `cds_document/config.py` - Add canonical path properties
- `cds_document/validators.py` - Use settings paths (3 locations)

**Repo root calculation:** `Path(__file__).parent.parent.parent.parent` (from cds_document/)

### 4. interaction_service
**Files to update:**
- `cds_interaction/app/config.py` - Add canonical path properties
- `cds_interaction/app/main.py` - Use settings paths
- `cds_interaction/services/envelope_validator.py` - Check if needs update
- `cds_interaction/services/payload_validator.py` - Check if needs update
- `cds_interaction/services/schema_validator.py` - Check if needs update

**Repo root calculation:** `Path(__file__).parent.parent.parent.parent` (from cds_interaction/app/)

### 5. relationship_service
**Files to update:**
- `cds_relationship/config.py` - Add canonical path properties
- `cds_relationship/services/event_validator.py` - Use settings paths
- `cds_relationship/services/schema_validator.py` - Check if needs update

**Repo root calculation:** `Path(__file__).parent.parent.parent.parent` (from cds_relationship/)

### 6. product_service
**Files to update:**
- `app/config.py` - Add canonical path properties
- `app/validation/validate.py` - Use settings paths instead of module constants

**Repo root calculation:** `Path(__file__).parent.parent.parent.parent` (from app/)

### 7. riskprofile_service
**Files to update:**
- `app/config.py` - Add canonical path properties
- `app/validation/envelope.py` - Use settings paths instead of module constants
- `app/validation/validate.py` - Check if needs update

**Repo root calculation:** `Path(__file__).parent.parent.parent.parent` (from app/)

### 8. cas_service
**Files to update:**
- `cas_audit/config.py` - Add canonical path properties (if needed)
- `cas_audit/schema_validator.py` - **NOTE:** Uses local schemas/, not canonical. May not need update.

**Repo root calculation:** `Path(__file__).parent.parent.parent.parent` (from cas_audit/)

### 9. policy_service
**Files to update:**
- `app/config.py` - Add canonical path properties (if needed)
- Check if policy service uses canonical schemas

**Note:** Policy service may use policy-specific schemas, not canonical.

## Implementation Order

1. ✅ Assessment (this document)
2. ⏳ Update client_service
3. ⏳ Update task_service
4. ⏳ Update document_service
5. ⏳ Update interaction_service
6. ⏳ Update relationship_service
7. ⏳ Update product_service
8. ⏳ Update riskprofile_service
9. ⏳ Update cas_service (if applicable)
10. ⏳ Update policy_service (if applicable)
11. ⏳ Verify all changes

## Verification Checklist

For each service:
- [ ] config.py has canonical path properties
- [ ] All code files updated to use settings paths
- [ ] No hardcoded path calculations remain
- [ ] Tests updated (if they reference paths)
- [ ] Path calculations verified (correct repo root)

## Benefits

1. **Centralized Configuration**: All paths in one place (config.py)
2. **Easy Updates**: Change path calculation in one location
3. **Consistency**: All services use same pattern
4. **Maintainability**: Easier to understand and modify
5. **Testability**: Can mock settings in tests
