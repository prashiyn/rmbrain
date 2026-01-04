# Canonical Library Migration

## Overview

Converting the `canonical/` directory into a proper Python library that can be imported by all services, replacing path-based access with direct library imports.

## Status

### ✅ Completed

1. **Library Structure Created**
   - `canonical/__init__.py` - Library exports
   - `canonical/registry.py` - Core registry functions
   - `canonical/pyproject.toml` - Library package definition
   - `canonical/README.md` - Library documentation

2. **Dependencies Updated**
   - All services' `pyproject.toml` files updated to include `canonical @ file:///${PROJECT_ROOT}/canonical`

3. **Code Files Updated**
   - ✅ `client_service/cds_client/event_validator.py`
   - ✅ `client_service/cds_client/schema_validator.py`
   - ✅ `task_service/cds_task/event_envelope.py`
   - ✅ `task_service/cds_task/json_schema.py`

### ⏳ In Progress

4. **Remaining Code Files to Update**
   - `document_service/cds_document/validators.py`
   - `interaction_service/cds_interaction/app/main.py`
   - `relationship_service/cds_relationship/services/event_validator.py`
   - `relationship_service/cds_relationship/services/schema_validator.py`
   - `product_service/app/validation/validate.py`
   - `riskprofile_service/app/validation/envelope.py`
   - `riskprofile_service/app/validation/validate.py`
   - `rmbrain-mainapp/app/schemas/validation.py`
   - `rmbrain-mainapp/app/shared/canonical_schema_sdk/registry.py`

5. **Config Files to Update**
   - Remove `canonical_entities_dir`, `canonical_events_dir`, `canonical_semantics_dir` properties from all `config.py` files

6. **Test Files to Update**
   - Update test fixtures and mocks to use canonical library
   - Update test files that reference canonical paths

## Migration Pattern

### Before (Path-based)
```python
from pathlib import Path
from cds_client.config import settings

canonical_events_dir = settings.canonical_events_dir
envelope_path = canonical_events_dir / "event_envelope.v1.json"
with open(envelope_path) as f:
    schema = json.load(f)
```

### After (Library-based)
```python
from canonical import load_event_envelope_schema

schema = load_event_envelope_schema()
```

## API Reference

### Entity Schemas
```python
from canonical import load_entity_schema, SchemaNotFoundError

schema = load_entity_schema("client", "v1")
```

### Event Schemas
```python
from canonical import load_event_schema, load_event_envelope_schema, EventNotFoundError

envelope_schema = load_event_envelope_schema()
event_schema = load_event_schema("client.created", "v1")
```

### Semantic Constraints
```python
from canonical import load_semantic_constraints

constraints = load_semantic_constraints("client", "v1")
```

## Next Steps

1. Continue updating remaining code files
2. Remove canonical path properties from all config.py files
3. Update test files
4. Verify all changes work correctly
5. Update documentation
