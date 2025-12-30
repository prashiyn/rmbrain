# Canonical Schema Migration Assessment

## Executive Summary

This document provides a comprehensive assessment of migrating all event and entity schemas from service-specific locations to a shared canonical registry, as specified in `docs/cds_shcred_infra.md`.

**Current State**: Schemas are scattered across 8 services in `libs/schemas/` directories and in `rmbrain-mainapp/schemas/`.

**Target State**: All canonical schemas consolidated in `canonical/` directory at repository root.

## Current Schema Inventory

### 1. Event Envelope Schema (Duplicated 8+ times)
**Location**: Found in multiple services
- `client_service/libs/schemas/events/event_envelope.v1.json`
- `document_service/libs/schemas/events/event_envelope.v1.json`
- `interaction_service/libs/schemas/events/event_envelope.v1.json`
- `product_service/libs/schemas/events/event_envelope.v1.json`
- `relationship_service/libs/schemas/events/event_envelope.v1.json`
- `riskprofile_service/libs/schemas/events/event_envelope.v1.json`
- `task_service/libs/schemas/events/event_envelope.v1.json`
- `rmbrain-mainapp/schemas/event_envelope.v1.json`
- `product_service/libs/schemas/envelope/event-envelope.v1.json` (alternate location)

**Action**: Consolidate to `canonical/events/event_envelope.v1.json`

### 2. Entity Schemas

#### Client Service
- `client_service/libs/schemas/entities/client.v1.json`
- `client_service/libs/schemas/entities/client_link.v1.json`

#### Document Service
- `document_service/libs/schemas/entities/document.v1.json`

#### Interaction Service
- `interaction_service/libs/schemas/entities/interaction.v1.json`

#### Product Service
- `product_service/libs/schemas/entities/product.v1.json`

#### Relationship Service
- `relationship_service/libs/schemas/entities/relationship.v1.json`

#### Risk Profile Service
- `riskprofile_service/libs/schemas/entities/riskprofile.v1.json`
- `riskprofile_service/libs/schemas/entities/suitability_assessment.v1.json`

#### Task Service
- `task_service/libs/schemas/entities/task.v1.json`

**Action**: Move all to `canonical/entities/`

### 3. Event Schemas by Service

#### Client Service Events
- `client_service/libs/schemas/events/client.created.v1.json`
- `client_service/libs/schemas/events/client.updated.v1.json`
- `client_service/libs/schemas/events/client.status_changed.v1.json`
- `client_service/libs/schemas/events/client_link.created.v1.json`
- `client_service/libs/schemas/events/client_link.updated.v1.json`

#### Document Service Events
- `document_service/libs/schemas/events/document.access_changed.v1.json`
- `document_service/libs/schemas/events/document.ingested.v1.json`
- `document_service/libs/schemas/events/document.linked.v1.json`
- `document_service/libs/schemas/events/document.status_changed.v1.json`
- `document_service/libs/schemas/events/document.superseded.v1.json`
- `document_service/libs/schemas/events/document.updated.v1.json`
- `document_service/libs/schemas/events/document.version_added.v1.json`

#### Interaction Service Events
- `interaction_service/libs/schemas/events/interaction.cancelled.v1.json`
- `interaction_service/libs/schemas/events/interaction.completed.v1.json`
- `interaction_service/libs/schemas/events/interaction.created.v1.json`
- `interaction_service/libs/schemas/events/interaction.documents_attached.v1.json`
- `interaction_service/libs/schemas/events/interaction.finalized.v1.json`
- `interaction_service/libs/schemas/events/interaction.initiated.v1.json`
- `interaction_service/libs/schemas/events/interaction.review_started.v1.json`
- `interaction_service/libs/schemas/events/interaction.status_changed.v1.json`
- `interaction_service/libs/schemas/events/interaction.superseded.v1.json`
- `interaction_service/libs/schemas/events/document.linked.v1.json` (shared event)

#### Product Service Events
- `product_service/libs/schemas/events/product.artefact.linked.v1.json`
- `product_service/libs/schemas/events/product.created.v1.json`
- `product_service/libs/schemas/events/product.deactivated.v1.json`
- `product_service/libs/schemas/events/product.status_changed.v1.json`
- `product_service/libs/schemas/events/product.updated.v1.json`

#### Relationship Service Events
- `relationship_service/libs/schemas/events/relationship.at_risk.v1.json`
- `relationship_service/libs/schemas/events/relationship.created.v1.json`
- `relationship_service/libs/schemas/events/relationship.health_updated.v1.json`
- `relationship_service/libs/schemas/events/relationship.preferences_updated.v1.json`
- `relationship_service/libs/schemas/events/relationship.status_changed.v1.json`
- `relationship_service/libs/schemas/events/relationship.terminated.v1.json`
- `relationship_service/libs/schemas/events/document.ingested.v1.json` (shared event)
- `relationship_service/libs/schemas/events/interaction.finalized.v1.json` (shared event)

#### Risk Profile Service Events
- `riskprofile_service/libs/schemas/events/riskprofile.activated.v1.json`
- `riskprofile_service/libs/schemas/events/riskprofile.created.v1.json`
- `riskprofile_service/libs/schemas/events/riskprofile.superseded.v1.json`
- `riskprofile_service/libs/schemas/events/riskprofile.updated.v1.json`
- `riskprofile_service/libs/schemas/events/suitability.assessed.v1.json`
- `riskprofile_service/libs/schemas/events/suitability.breached.v1.json`

#### Task Service Events
- `task_service/libs/schemas/events/task_created.v1.json` (note: underscore, not dot)
- `task_service/libs/schemas/events/task_completed.v1.json`
- `task_service/libs/schemas/events/task_expired.v1.json`
- `task_service/libs/schemas/events/task_status_changed.v1.json`
- `task_service/libs/schemas/events/interaction_finalized.v1.json` (note: underscore)
- `task_service/libs/schemas/events/document_uploaded.v1.json` (note: underscore)
- `task_service/libs/schemas/events/riskprofile_changed.v1.json` (note: underscore)

**Note**: Task service uses underscores instead of dots in some event names. Need to standardize.

**Action**: Move all to `canonical/events/` organized by domain (interaction/, task/, etc.)

### 4. RMBrain Main App Schemas

#### Canonical Schemas
- `rmbrain-mainapp/schemas/event_envelope.v1.json` (duplicate)
- `rmbrain-mainapp/schemas/event.envelope.schema.json` (alternate format?)

#### Plugin Schemas (Keep in rmbrain-mainapp)
- `rmbrain-mainapp/schemas/plugin.manifest.schema.json` (plugin-specific, keep)
- `rmbrain-mainapp/schemas/plugin.events.manifest.schema.json` (plugin-specific, keep)

#### Other Schemas (Keep in rmbrain-mainapp)
- `rmbrain-mainapp/app/ai_prompts/schemas/*.json` (prompt-specific, keep)
- `rmbrain-mainapp/app/plugins/*/schemas/*.json` (plugin-specific, keep)
- `rmbrain-mainapp/app/shared/canonical_schema_sdk/schemas/client.v1.json` (SDK example, review)

**Action**: Move `event_envelope.v1.json` to canonical, keep plugin/prompt schemas in rmbrain-mainapp

### 5. Other Schema Files

#### CAS Service
- `cas_service/schemas/audit_event.v1.schema.json` (audit-specific, may stay or move to canonical)

#### Policy Service
- `policy_service/schemas/policy_rules.v1.schema.json` (policy-specific, may stay)

#### Task Service
- `task_service/libs/schemas/task_rules/task_rules.v1.schema.json` (rules, not entity/event)

## Current Import Patterns

### Pattern 1: Direct Path Construction
```python
# client_service/cds_client/event_validator.py
schema_dir = Path(__file__).parent.parent / "libs" / "schemas" / "events"
envelope_path = schema_dir / "event_envelope.v1.json"
```

### Pattern 2: Relative Path from Module
```python
# task_service/cds_task/event_envelope.py
_ENVELOPE_SCHEMA_PATH = (
    Path(__file__).parent.parent
    / "libs"
    / "schemas"
    / "events"
    / "event_envelope.v1.json"
)
```

### Pattern 3: SCHEMAS_DIR Constant
```python
# product_service/app/validation/validate.py
SCHEMAS_DIR = Path(__file__).parent.parent.parent / "libs" / "schemas"
schema_path = SCHEMAS_DIR / "events" / "event_envelope.v1.json"
```

### Pattern 4: RMBrain Main App Pattern
```python
# rmbrain-mainapp/app/schemas/validation.py
SCHEMAS_DIR = Path(__file__).parent.parent.parent / "schemas"
schema_path = SCHEMAS_DIR / "event_envelope.v1.json"
```

## Target Structure

```
rmbrain/
├── canonical/
│   ├── events/
│   │   ├── event_envelope.v1.json          # Single source of truth
│   │   ├── interaction/
│   │   │   ├── interaction.created.v1.json
│   │   │   ├── interaction.completed.v1.json
│   │   │   ├── interaction.finalized.v1.json
│   │   │   └── ...
│   │   ├── task/
│   │   │   ├── task.created.v1.json
│   │   │   ├── task.completed.v1.json
│   │   │   └── ...
│   │   ├── client/
│   │   │   ├── client.created.v1.json
│   │   │   └── ...
│   │   ├── document/
│   │   │   ├── document.ingested.v1.json
│   │   │   └── ...
│   │   ├── product/
│   │   │   ├── product.created.v1.json
│   │   │   └── ...
│   │   ├── relationship/
│   │   │   ├── relationship.created.v1.json
│   │   │   └── ...
│   │   └── riskprofile/
│   │       ├── riskprofile.created.v1.json
│   │       └── ...
│   ├── entities/
│   │   ├── client.v1.json
│   │   ├── client_link.v1.json
│   │   ├── document.v1.json
│   │   ├── interaction.v1.json
│   │   ├── product.v1.json
│   │   ├── relationship.v1.json
│   │   ├── riskprofile.v1.json
│   │   ├── suitability_assessment.v1.json
│   │   └── task.v1.json
│   └── semantics/
│       └── (future: semantic constraints)
```

## Migration Strategy

### Phase 1: Create Canonical Structure
1. Create `canonical/` directory at repository root
2. Create subdirectories: `events/`, `entities/`, `semantics/`
3. Create domain subdirectories under `events/`: `interaction/`, `task/`, `client/`, `document/`, `product/`, `relationship/`, `riskprofile/`

### Phase 2: Consolidate Event Envelope
1. Compare all `event_envelope.v1.json` files to ensure they're identical
2. Move one canonical version to `canonical/events/event_envelope.v1.json`
3. Update all imports to point to canonical location

### Phase 3: Migrate Entity Schemas
1. Move all entity schemas to `canonical/entities/`
2. Update all imports

### Phase 4: Migrate Event Schemas (Service by Service)
1. **Client Service**: Move client events to `canonical/events/client/`
2. **Document Service**: Move document events to `canonical/events/document/`
3. **Interaction Service**: Move interaction events to `canonical/events/interaction/`
4. **Product Service**: Move product events to `canonical/events/product/`
5. **Relationship Service**: Move relationship events to `canonical/events/relationship/`
6. **Risk Profile Service**: Move riskprofile events to `canonical/events/riskprofile/`
7. **Task Service**: Move task events to `canonical/events/task/` (standardize naming)

### Phase 5: Update All Imports
For each service, update:
- Event validators
- Schema loaders
- Entity validators
- Any direct file path references

### Phase 6: Update RMBrain Main App
1. Move `event_envelope.v1.json` to canonical
2. Update imports in `app/schemas/validation.py`
3. Update imports in `app/event_gateway/gateway.py`
4. Keep plugin-specific schemas in rmbrain-mainapp

### Phase 7: Cleanup
1. Remove old `libs/schemas/` directories from services
2. Remove duplicate `event_envelope.v1.json` files
3. Update documentation

## Files Requiring Import Updates

### Client Service
- `client_service/cds_client/event_validator.py` (line 20)
- Any other files importing schemas

### Document Service
- `document_service/cds_document/validators.py` (lines 18, 77, 102)

### Interaction Service
- `interaction_service/cds_interaction/services/envelope_validator.py`
- `interaction_service/cds_interaction/services/payload_validator.py`

### Product Service
- `product_service/app/validation/validate.py` (lines 12, 29, 38, 96)

### Relationship Service
- `relationship_service/cds_relationship/services/event_validator.py` (line 15)

### Risk Profile Service
- `riskprofile_service/app/validation/envelope.py` (line 9)

### Task Service
- `task_service/cds_task/event_envelope.py` (lines 19-24)
- `task_service/cds_task/json_schema.py`
- `task_service/cds_task/models.py` (references entity schema)

### RMBrain Main App
- `rmbrain-mainapp/app/schemas/validation.py` (line 13)
- `rmbrain-mainapp/app/event_gateway/gateway.py` (line 188)
- `rmbrain-mainapp/app/shared/canonical_schema_sdk/` (if it uses schemas)

## Naming Standardization Issues

### Task Service Event Names
Current (inconsistent):
- `task_created.v1.json` (underscore)
- `task.completed.v1.json` (dot)

Should be:
- `task.created.v1.json` (dot notation, consistent with others)

**Action**: Rename during migration to use dot notation consistently.

## Dependencies and Considerations

1. **Tests**: All test files that reference schema paths need updates
2. **CI/CD**: Any schema validation in CI needs path updates
3. **Documentation**: README files mentioning schema locations need updates
4. **Backward Compatibility**: Consider symlinks or deprecation warnings during transition

## Risk Assessment

**Low Risk**:
- Moving files is straightforward
- Path updates are mechanical
- Tests can validate correctness

**Medium Risk**:
- Need to ensure all services can access canonical directory
- May need to update pyproject.toml or package configurations
- Need to handle relative vs absolute paths correctly

**Mitigation**:
- Test each service after migration
- Keep old paths temporarily with deprecation warnings
- Use absolute paths from repository root

## Next Steps

1. **Review this assessment** with stakeholders
2. **Create canonical directory structure**
3. **Migrate service by service** (start with one service as proof of concept)
4. **Update all imports** systematically
5. **Run tests** after each service migration
6. **Clean up** old schema directories
