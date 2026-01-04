# Actor Schema Migration - Impact Assessment

This document assesses the impact of migrating to the unified actor schema module (`canonical_schemas/actor.py`) across all services.

## Overview

**New Module**: `canonical_schemas/actor.py`
- Provides `ActorType` enum (human_internal, human_external, system, service)
- Provides `ActorRole` enum (all documented roles)
- Provides `Actor` Pydantic model
- Single source of truth for actor definitions

## Impact Summary

### Files Requiring Updates

#### High Priority (Critical Inconsistencies)

1. **Interaction Schemas** - Missing `actor_type`
   - `canonical/entities/interaction.v1.json` - Add `actor_type` to participants
   - `canonical/events/interaction/interaction.initiated.v1.json` - Add `actor_type` to participants
   - **Impact**: Schema changes, may require database migrations

2. **Python Models Using Plain Strings** - Need enum migration
   - `task_service/cds_task/schemas.py` - `AssigneeSchema`
   - `bff_service/app/auth/actor_resolver.py` - `Actor` model
   - `bff_service/app/models/audit.py` - `AuditActor` model
   - `policy_service/cps_policy/models.py` - `Actor` model
   - **Impact**: Type safety improvements, potential validation changes

#### Medium Priority (Consistency Improvements)

3. **Relationship Service** - Already has enum, but should use shared module
   - `relationship_service/cds_relationship/schemas/relationship.py` - Replace local `ActorType` with import
   - **Impact**: Low - already correct, just needs import change

4. **Service-Specific Extensions** - Document or standardize
   - `bff_service/app/auth/actor_resolver.py` - `Actor.tenant_id` field
   - `policy_service/cps_policy/models.py` - `Actor.tenant_id` field
   - **Impact**: Low - these may be intentional service-specific extensions

---

## Detailed File-by-File Impact

### 1. JSON Schema Files

#### 1.1 `canonical/entities/interaction.v1.json`

**Current State**:
```json
{
  "participants": {
    "items": {
      "required": ["actor_id", "actor_role"],
      "properties": {
        "actor_id": { "type": "string" },
        "actor_role": {
          "type": "string",
          "enum": ["rm", "product_manager", "investment_specialist", "client", "system"]
        },
        "display_name": { "type": "string" }
      }
    }
  }
}
```

**Required Change**:
```json
{
  "participants": {
    "items": {
      "required": ["actor_id", "actor_role", "actor_type"],
      "properties": {
        "actor_id": { "type": "string" },
        "actor_role": {
          "type": "string",
          "description": "Role from canonical actor taxonomy"
        },
        "actor_type": {
          "type": "string",
          "enum": ["human_internal", "human_external", "system", "service"]
        },
        "display_name": { "type": "string" }
      }
    }
  }
}
```

**Impact**:
- ⚠️ **Breaking Change**: Existing interaction records may not have `actor_type`
- ⚠️ **Database Impact**: May need migration to add default `actor_type` values
- ⚠️ **API Impact**: API consumers must provide `actor_type` when creating interactions

**Migration Strategy**:
1. Add `actor_type` as optional first (backward compatible)
2. Populate existing records with inferred `actor_type` based on `actor_role`
3. Make `actor_type` required after migration

#### 1.2 `canonical/events/interaction/interaction.initiated.v1.json`

**Current State**: Same as interaction entity (missing `actor_type`)

**Required Change**: Same as above - add `actor_type` to participants

**Impact**: Same as above

---

### 2. Python Model Files

#### 2.1 `task_service/cds_task/schemas.py`

**Current State**:
```python
class AssigneeSchema(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: str  # Plain string
```

**Required Change**:
```python
from canonical_schemas.actor import Actor, ActorRole, ActorType

class AssigneeSchema(Actor):  # Inherit from Actor
    pass
# OR
class AssigneeSchema(BaseModel):
    actor_id: str
    actor_role: ActorRole  # Use enum
    actor_type: ActorType  # Use enum
```

**Impact**:
- ✅ **Type Safety**: Enum prevents invalid values
- ✅ **Validation**: Pydantic validates enum values automatically
- ⚠️ **Breaking Change**: Code expecting plain strings will need updates
- ⚠️ **Import Path**: Need to ensure `canonical_schemas` is in Python path

**Files That Import This**:
- `task_service/cds_task/main.py` - Uses `AssigneeSchema`
- `task_service/cds_task/repository.py` - May use assignee
- `task_service/cds_task/event_handler.py` - May use assignee
- Test files

#### 2.2 `bff_service/app/auth/actor_resolver.py`

**Current State**:
```python
class Actor(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: str  # Plain string
    tenant_id: Optional[str] = None  # Service-specific extension
```

**Required Change**:
```python
from canonical_schemas.actor import Actor as CanonicalActor, ActorRole, ActorType

class Actor(CanonicalActor):  # Extend canonical actor
    tenant_id: Optional[str] = None  # Keep service-specific field
```

**Impact**:
- ✅ **Consistency**: Uses canonical base
- ✅ **Type Safety**: Enum validation
- ⚠️ **Breaking Change**: Header parsing may need updates
- ⚠️ **Import Path**: Need to ensure `canonical_schemas` is in Python path

**Files That Import This**:
- `bff_service/app/routes/*.py` - Uses `ActorResolver`
- Test files

#### 2.3 `bff_service/app/models/audit.py`

**Current State**:
```python
class AuditActor(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: str = Field(default="human_internal")  # Plain string with default
```

**Required Change**:
```python
from canonical_schemas.actor import Actor as CanonicalActor, ActorType

class AuditActor(CanonicalActor):
    actor_type: ActorType = Field(default=ActorType.HUMAN_INTERNAL)
```

**Impact**:
- ✅ **Type Safety**: Enum with proper default
- ⚠️ **Breaking Change**: Default value changes from string to enum
- ⚠️ **Import Path**: Need to ensure `canonical_schemas` is in Python path

**Files That Import This**:
- `bff_service/app/routes/*.py` - Uses `AuditActor`
- Test files

#### 2.4 `policy_service/cps_policy/models.py`

**Current State**:
```python
class Actor(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: str  # Plain string
    tenant_id: str  # Required, not in canonical
```

**Required Change**:
```python
from canonical_schemas.actor import Actor as CanonicalActor, ActorRole, ActorType

class Actor(CanonicalActor):
    tenant_id: str  # Keep service-specific required field
```

**Impact**:
- ✅ **Consistency**: Uses canonical base
- ✅ **Type Safety**: Enum validation
- ⚠️ **Breaking Change**: API consumers must provide enum values
- ⚠️ **Import Path**: Need to ensure `canonical_schemas` is in Python path

**Files That Import This**:
- `policy_service/cps_policy/service.py` - Uses `Actor`
- `policy_service/cps_policy/evaluator.py` - Uses `Actor`
- Test files

#### 2.5 `relationship_service/cds_relationship/schemas/relationship.py`

**Current State**:
```python
class ActorType(str, Enum):
    HUMAN_INTERNAL = "human_internal"
    HUMAN_EXTERNAL = "human_external"
    SYSTEM = "system"
    SERVICE = "service"

class Actor(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: ActorType
    display_name: Optional[str] = None
```

**Required Change**:
```python
from canonical_schemas.actor import Actor as CanonicalActor, ActorType, ActorRole

# Remove local ActorType enum
# Use CanonicalActor directly or extend if needed
class Actor(CanonicalActor):
    pass  # Or add relationship-specific fields if needed
```

**Impact**:
- ✅ **Consistency**: Uses shared definition
- ✅ **No Breaking Change**: Already using enum, just changing import
- ⚠️ **Import Path**: Need to ensure `canonical_schemas` is in Python path

**Files That Import This**:
- `relationship_service/cds_relationship/schemas/relationship.py` - Defines it
- `relationship_service/cds_relationship/services/*.py` - Uses Actor
- Test files

---

## Database Impact

### Interaction Service

**Potential Migration Needed**:
- Existing `interactions` table has `participants` JSONB column
- If `actor_type` is added as required, existing records need updates
- Migration strategy:
  1. Add `actor_type` as optional in schema
  2. Backfill existing records with inferred `actor_type`:
     - `rm`, `product_manager`, etc. → `human_internal`
     - `client`, `prospect` → `human_external`
     - `system` → `system`
  3. Make `actor_type` required after backfill

**SQL Migration Example**:
```sql
-- Step 1: Update existing records
UPDATE interactions
SET participants = jsonb_set(
    participants,
    '{0,actor_type}',
    '"human_internal"'
)
WHERE participants->0->>'actor_role' IN ('rm', 'product_manager', 'investment_specialist');

-- Repeat for other role types...
```

---

## API Impact

### Breaking Changes

1. **Interaction Creation API**
   - Currently: `participants` only need `actor_id` and `actor_role`
   - After: `participants` must include `actor_type`
   - **Mitigation**: Make `actor_type` optional initially, then required

2. **Task Assignment API**
   - Currently: `assignee.actor_type` is plain string
   - After: `assignee.actor_type` must be enum value
   - **Impact**: API consumers must use exact enum values

3. **Policy Service API**
   - Currently: `actor.actor_type` is plain string
   - After: `actor.actor_type` must be enum value
   - **Impact**: API consumers must use exact enum values

### Non-Breaking Changes

1. **Relationship Service**
   - Already uses enum, just changing import source
   - No API changes needed

---

## Testing Impact

### Test Files Requiring Updates

1. **Interaction Service Tests**
   - Update test fixtures to include `actor_type`
   - Update validation tests

2. **Task Service Tests**
   - Update test fixtures to use enum values
   - Update validation tests

3. **BFF Service Tests**
   - Update actor resolver tests
   - Update audit model tests

4. **Policy Service Tests**
   - Update actor model tests
   - Update authorization request tests

5. **Relationship Service Tests**
   - Update imports (minimal changes)

---

## Migration Strategy

### Phase 1: Create Shared Module ✅
- [x] Create `canonical_schemas/actor.py`
- [x] Define `ActorType` enum
- [x] Define `ActorRole` enum
- [x] Define `Actor` model
- [x] Add documentation

### Phase 2: Update JSON Schemas (Breaking)
- [ ] Update `canonical/entities/interaction.v1.json`
  - Add `actor_type` as **optional** first
  - Update description
- [ ] Update `canonical/events/interaction/interaction.initiated.v1.json`
  - Add `actor_type` as **optional** first
- [ ] Deploy and test with optional `actor_type`
- [ ] Backfill existing interaction records
- [ ] Make `actor_type` **required** after backfill

### Phase 3: Update Python Models (Type Safety)
- [ ] Update `task_service/cds_task/schemas.py`
- [ ] Update `bff_service/app/auth/actor_resolver.py`
- [ ] Update `bff_service/app/models/audit.py`
- [ ] Update `policy_service/cps_policy/models.py`
- [ ] Update `relationship_service/cds_relationship/schemas/relationship.py`

### Phase 4: Update Service Code
- [ ] Update all imports
- [ ] Update validation logic
- [ ] Update serialization/deserialization
- [ ] Update tests

### Phase 5: Database Migration (If Needed)
- [ ] Create migration script for interaction service
- [ ] Backfill `actor_type` in existing records
- [ ] Verify data integrity

### Phase 6: Documentation
- [ ] Update API documentation
- [ ] Update service READMEs
- [ ] Update developer guides

---

## Risk Assessment

### High Risk
- **Interaction schema changes**: Breaking change for API consumers
- **Database migrations**: Data integrity concerns

### Medium Risk
- **Python model changes**: Type mismatches in existing code
- **Import path issues**: Services may not find `canonical_schemas`

### Low Risk
- **Relationship service**: Already using enum, minimal impact
- **Documentation updates**: No code impact

---

## Rollback Plan

If issues arise:

1. **JSON Schema Rollback**: Revert schema files, keep `actor_type` optional
2. **Python Model Rollback**: Keep enum imports but make fields accept strings
3. **Database Rollback**: No destructive changes, can revert migration

---

## Success Criteria

- [ ] All services use `canonical_schemas.actor` imports
- [ ] All JSON schemas include `actor_type` field
- [ ] All Python models use enum types
- [ ] All tests pass
- [ ] No breaking changes to existing APIs (after migration period)
- [ ] Documentation updated

---

## Next Steps

1. **Review this assessment** with team
2. **Approve migration strategy**
3. **Create implementation plan** with timelines
4. **Begin Phase 2** (JSON schema updates)
