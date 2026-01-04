# Actor Schema Unified Module - Review Document

## Summary

A unified actor schema module has been created at `canonical_schemas/actor.py` to provide a single source of truth for actor definitions across all services.

## What Has Been Created

### 1. Core Module: `canonical_schemas/actor.py`

**Location**: `/media/prashanth/extmnt1/rmbrain/canonical_schemas/actor.py`

**Contents**:
- `ActorType` enum: `human_internal`, `human_external`, `system`, `service`
- `ActorRole` enum: All documented roles from relationship_service.md
  - Human Internal: rm, relationship_manager, investment_specialist, product_manager, portfolio_manager, risk_manager, compliance_officer, service_rm
  - Human External: client, prospect, external_advisor
  - System/Service: system, scheduler, workflow_engine, cds_relationship
- `Actor` Pydantic model: Standard actor schema with validation
- `validate_actor_role_type()`: Helper function to validate role/type combinations
- `ACTOR_ROLES_BY_TYPE`: Mapping of valid roles by type

**Key Features**:
- ✅ Type-safe enums (prevents invalid values)
- ✅ Pydantic validation
- ✅ Matches canonical JSON schemas
- ✅ Comprehensive documentation
- ✅ Helper functions for validation

### 2. Package Structure

```
canonical_schemas/
├── __init__.py          # Package exports
├── actor.py             # Actor schema definitions
├── README.md            # Package documentation
└── USAGE_EXAMPLES.md    # Practical usage examples
```

### 3. Documentation

- **README.md**: Package overview and usage instructions
- **USAGE_EXAMPLES.md**: Comprehensive examples for different service contexts
- **ACTOR_SCHEMA_MIGRATION_IMPACT_ASSESSMENT.md**: Detailed impact analysis
- **ACTOR_SCHEMA_DEFINITIONS_AUDIT.md**: Complete audit of existing definitions

## Design Decisions

### 1. Location: `canonical_schemas/` at Repository Root

**Rationale**:
- Aligns with `canonical/` directory structure (JSON schemas)
- Easy to import from any service
- Clear naming convention
- Separate from service-specific code

**Alternative Considered**: 
- `shared/schemas/` - Less clear connection to canonical schemas
- `libs/canonical_schemas/` - More nested, harder to import

### 2. Enum-Based Design

**Rationale**:
- Type safety (prevents invalid values)
- IDE autocomplete support
- Self-documenting code
- Matches relationship service pattern

**Alternative Considered**:
- Plain strings with validation - Less type-safe
- Constants - Less structured

### 3. Pydantic BaseModel

**Rationale**:
- Already used across all services
- Built-in validation
- JSON serialization support
- Field validation and documentation

### 4. ActorRole Enum Includes All Documented Roles

**Rationale**:
- Complete coverage of documented roles
- Prevents typos and inconsistencies
- Easy to extend if new roles are added

**Note**: The enum can be extended if new roles are documented in the future.

## What Needs Review

### 1. Module Structure ✅

**Question**: Is `canonical_schemas/` at root level the right location?

**Options**:
- ✅ Current: `canonical_schemas/` at root (recommended)
- Alternative: `shared/canonical_schemas/`
- Alternative: Package as installable dependency

### 2. Import Strategy

**Current Approach**: Services import via Python path

```python
# Services need to add repo root to PYTHONPATH or use relative imports
from canonical_schemas.actor import Actor, ActorType, ActorRole
```

**Question**: Should we:
- ✅ Keep current approach (simple, no build step)
- Create installable package (more complex, but cleaner)
- Use relative imports (service-specific)

### 3. ActorRole Enum Values

**Current**: All roles from relationship_service.md are included

**Question**: 
- Are all these roles correct?
- Should we add more roles that are used but not documented?
- Should we mark some roles as deprecated?

### 4. Service-Specific Extensions

**Current**: Services can extend `Actor` for service-specific fields (e.g., `tenant_id`)

**Example**:
```python
from canonical_schemas.actor import Actor as CanonicalActor

class Actor(CanonicalActor):
    tenant_id: Optional[str] = None  # Service-specific
```

**Question**: Is this pattern acceptable, or should we:
- Include common fields in base `Actor`?
- Use composition instead of inheritance?
- Keep service-specific fields separate?

### 5. Backward Compatibility

**Current**: Enum values match existing string values (no breaking change for values)

**Question**: 
- Should we maintain backward compatibility with plain strings?
- Or require enum usage immediately?

### 6. Validation Strictness

**Current**: `validate_actor_role_type()` is provided but not enforced

**Question**: Should we:
- ✅ Make it optional (current)
- Enforce in `Actor` model validation
- Provide as separate validation step

## Migration Plan (Pending Approval)

### Phase 1: Review & Approval ✅ (Current)
- [x] Create unified module
- [x] Document impact
- [ ] **Review by team** ← YOU ARE HERE
- [ ] Approve design decisions
- [ ] Approve migration strategy

### Phase 2: JSON Schema Updates (Breaking)
- [ ] Update interaction schemas to include `actor_type`
- [ ] Deploy with optional `actor_type`
- [ ] Backfill existing data
- [ ] Make `actor_type` required

### Phase 3: Python Model Updates
- [ ] Update task service
- [ ] Update BFF service
- [ ] Update policy service
- [ ] Update relationship service
- [ ] Update interaction service (if Python models exist)

### Phase 4: Testing & Validation
- [ ] Update all tests
- [ ] Run integration tests
- [ ] Validate API compatibility
- [ ] Performance testing

### Phase 5: Documentation
- [ ] Update API docs
- [ ] Update service READMEs
- [ ] Update developer guides

## Files Created for Review

1. **`canonical_schemas/actor.py`** - Core module (PRIMARY REVIEW)
2. **`canonical_schemas/__init__.py`** - Package exports
3. **`canonical_schemas/README.md`** - Package documentation
4. **`canonical_schemas/USAGE_EXAMPLES.md`** - Usage examples
5. **`docs/ACTOR_SCHEMA_MIGRATION_IMPACT_ASSESSMENT.md`** - Impact analysis
6. **`docs/ACTOR_SCHEMA_DEFINITIONS_AUDIT.md`** - Existing definitions audit

## Key Questions for Review

1. **Module Location**: Is `canonical_schemas/` at root acceptable?
2. **Import Strategy**: Is Python path import acceptable, or should we package it?
3. **ActorRole Enum**: Are all roles correct? Any missing?
4. **Service Extensions**: Is inheritance pattern acceptable?
5. **Migration Timeline**: When should we proceed with Phase 2?
6. **Breaking Changes**: Are we comfortable with interaction schema changes?

## Next Steps After Review

Once approved:
1. Address any feedback on the module design
2. Finalize migration plan with timelines
3. Begin Phase 2 (JSON schema updates)
4. Coordinate with team on breaking changes

## Contact

For questions or feedback on this module, please review the files and provide feedback on:
- Module structure and design
- Enum values and roles
- Migration strategy
- Timeline and priorities
