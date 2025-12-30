# Canonical Schema Migration - Progress Report

## ✅ Completed Phases

### Phase 1: Create Canonical Structure ✅
- Created `canonical/` directory at repository root
- Created subdirectories: `events/`, `entities/`, `semantics/`
- Created domain subdirectories: `interaction/`, `task/`, `client/`, `document/`, `product/`, `relationship/`, `riskprofile/`

### Phase 2: Consolidate Event Envelope ✅
- Migrated `event_envelope.v1.json` to `canonical/events/event_envelope.v1.json`
- Single source of truth established

### Phase 3: Migrate Entity Schemas ✅
- All 9 entity schemas migrated to `canonical/entities/`:
  - client.v1.json
  - client_link.v1.json
  - document.v1.json
  - interaction.v1.json
  - product.v1.json
  - relationship.v1.json
  - riskprofile.v1.json
  - suitability_assessment.v1.json
  - task.v1.json

### Phase 4: Migrate Event Schemas ✅
- **Client Service**: 3 events → `canonical/events/client/`
- **Document Service**: 7 events → `canonical/events/document/`
- **Interaction Service**: 10 events → `canonical/events/interaction/`
- **Product Service**: 5 events → `canonical/events/product/`
- **Relationship Service**: 6 events → `canonical/events/relationship/`
- **Risk Profile Service**: 6 events → `canonical/events/riskprofile/`
- **Task Service**: 7 events → `canonical/events/task/` (with naming fixes: task_created → task.created)

**Total**: 54 schema files migrated

### Phase 5: Update Main Code Imports ✅

#### Client Service
- ✅ `cds_client/event_validator.py` - Updated to use canonical paths
- ✅ `cds_client/schema_validator.py` - Updated entity schema paths

#### Task Service
- ✅ `cds_task/event_envelope.py` - Updated envelope and payload schema paths
- ✅ `cds_task/json_schema.py` - Updated entity schema path
- ✅ `cds_task/models.py` - Updated comments
- ✅ `cds_task/main.py` - Updated error message

#### Product Service
- ✅ `app/validation/validate.py` - Updated all schema paths (envelope, payload, entity)

#### Document Service
- ✅ `cds_document/validators.py` - Updated all validator schema paths

#### Relationship Service
- ✅ `cds_relationship/services/event_validator.py` - Updated envelope and payload paths
- ✅ `cds_relationship/db/models.py` - Updated comment

#### Risk Profile Service
- ✅ `app/validation/envelope.py` - Updated envelope and payload paths

#### RMBrain Main App
- ✅ `app/schemas/validation.py` - Updated event_envelope to use canonical

## 🔄 In Progress

### Phase 6: Update Test Files
**Status**: 8 test files identified, need to update:
1. `document_service/tests/test_events.py`
2. `interaction_service/tests/test_envelope_validator.py`
3. `interaction_service/tests/test_event_handler.py`
4. `product_service/tests/test_handlers.py`
5. `product_service/tests/test_validation.py`
6. `rmbrain-mainapp/tests/test_schema_validation.py`
7. `task_service/tests/test_event_envelope.py`
8. `task_service/tests/test_event_handler.py`

**Action Required**: Update test files to use canonical schema paths

### Phase 7: Update Interaction Service Validators
**Status**: Need to check how `EnvelopeValidator` and `PayloadValidator` are instantiated
- They take `Path` parameters, so may need to update call sites

## 📋 Remaining Tasks

### Phase 8: Cleanup
- Remove old `libs/schemas/` directories from services
- Remove duplicate `event_envelope.v1.json` files
- Update any remaining references in scripts, docs, etc.

### Phase 9: Verification
- Run all tests to ensure they pass
- Verify all services can access canonical schemas
- Check for any broken imports

## 📊 Statistics

- **Total Schema Files Migrated**: 54
- **Services Updated**: 7 services + rmbrain-mainapp
- **Python Files Updated**: ~15 main code files
- **Test Files to Update**: 8 files
- **Naming Fixes**: Task service events standardized (underscore → dot notation)

## 🔍 Key Changes Made

### Path Pattern Changes

**Before**:
```python
schema_path = Path(__file__).parent.parent / "libs" / "schemas" / "events" / "event_envelope.v1.json"
```

**After**:
```python
repo_root = Path(__file__).parent.parent.parent.parent  # Adjust based on depth
schema_path = repo_root / "canonical" / "events" / "event_envelope.v1.json"
```

### Domain-Based Event Schema Loading

**Before**:
```python
schema_path = SCHEMAS_DIR / "events" / f"{event_type}.{event_version}.json"
```

**After**:
```python
domain = event_type.split(".")[0]  # e.g., "task.created" -> "task"
schema_path = CANONICAL_EVENTS_DIR / domain / f"{event_type}.{event_version}.json"
```

## ⚠️ Notes

1. **Interaction Service Validators**: Use constructor injection with `Path` parameters. Need to check where they're instantiated and update those call sites.

2. **Test Files**: Some tests may create temporary schema files or use relative paths. Need careful review.

3. **Scripts**: Check for any validation scripts that reference old schema paths.

4. **Documentation**: Update any README files that mention schema locations.
