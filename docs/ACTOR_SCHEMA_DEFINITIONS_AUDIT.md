# Actor Schema Definitions Audit

This document catalogs all instances of actor schema definitions across the codebase to identify inconsistencies and ensure standardization.

## Summary of Findings

### Actor Type Enum Values (Consistent)
All schemas that include `actor_type` use the same 4 enum values:
- `human_internal`
- `human_external`
- `system`
- `service`

### Key Inconsistencies Found

1. **Interaction schemas are missing `actor_type`** - Only have `actor_id` and `actor_role`
2. **Mixed use of enums vs strings** - Some Python models use enums, others use plain strings
3. **Optional fields inconsistency** - Some schemas have `display_name`, others don't
4. **Main app has different structure** - Uses `ActorContext` with different fields

---

## Detailed Schema Definitions

### 1. Relationship Service - Canonical Definition ✅

**File**: `relationship_service/cds_relationship/schemas/relationship.py`

```python
class ActorType(str, Enum):
    """Actor type enum - matches JSON Schema."""
    HUMAN_INTERNAL = "human_internal"
    HUMAN_EXTERNAL = "human_external"
    SYSTEM = "system"
    SERVICE = "service"

class Actor(BaseModel):
    """Actor in a relationship - matches JSON Schema."""
    actor_id: str
    actor_role: str
    actor_type: ActorType  # Uses enum
    display_name: Optional[str] = None
```

**Status**: ✅ **CANONICAL** - This is the most complete and properly typed definition.

---

### 2. Canonical JSON Schemas

#### 2.1 Relationship Entity
**File**: `canonical/entities/relationship.v1.json`

```json
{
  "required": ["actor_id", "actor_role", "actor_type"],
  "properties": {
    "actor_id": { "type": "string" },
    "actor_role": { "type": "string", "description": "Role from canonical actor taxonomy" },
    "actor_type": {
      "type": "string",
      "enum": ["human_internal", "human_external", "system", "service"]
    },
    "display_name": { "type": "string" }
  }
}
```

**Status**: ✅ Consistent with relationship service

---

#### 2.2 Task Entity
**File**: `canonical/entities/task.v1.json`

```json
{
  "assignee": {
    "required": ["actor_id", "actor_role", "actor_type"],
    "properties": {
      "actor_id": { "type": "string" },
      "actor_role": { "type": "string" },
      "actor_type": {
        "type": "string",
        "enum": ["human_internal", "human_external", "system", "service"]
      }
    }
  }
}
```

**Status**: ✅ Consistent - Note: No `display_name` field

---

#### 2.3 Interaction Entity ⚠️
**File**: `canonical/entities/interaction.v1.json`

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

**Status**: ⚠️ **INCONSISTENT** - Missing `actor_type` field! Only has `actor_id` and `actor_role`.

---

#### 2.4 Event Envelope
**File**: `canonical/events/event_envelope.v1.json`

```json
{
  "actor": {
    "required": ["actor_id", "actor_role", "actor_type"],
    "properties": {
      "actor_id": { "type": "string" },
      "actor_role": { "type": "string" },
      "actor_type": {
        "type": "string",
        "enum": ["human_internal", "human_external", "system", "service"]
      }
    }
  }
}
```

**Status**: ✅ Consistent - Note: No `display_name` field

---

### 3. Task Service

#### 3.1 Python Schema
**File**: `task_service/cds_task/schemas.py`

```python
class AssigneeSchema(BaseModel):
    """Assignee schema."""
    actor_id: str
    actor_role: str
    actor_type: str  # ⚠️ Plain string, not enum
```

**Status**: ⚠️ **INCONSISTENT** - Uses plain `str` instead of `ActorType` enum. Should import and use the enum from relationship service or define locally.

---

#### 3.2 Task Event Schemas
**Files**: 
- `canonical/events/task/task.created.v1.json`
- `canonical/events/task/task.completed.v1.json`
- `canonical/events/task/task.status_changed.v1.json`
- `canonical/events/task/task.expired.v1.json`

All use consistent structure:
```json
{
  "actor_id": { "type": "string" },
  "actor_role": { "type": "string" },
  "actor_type": {
    "type": "string",
    "enum": ["human_internal", "human_external", "system", "service"]
  }
}
```

**Status**: ✅ Consistent across all task events

---

### 4. Interaction Service

#### 4.1 Interaction Event Schema
**File**: `canonical/events/interaction/interaction.initiated.v1.json`

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

**Status**: ⚠️ **INCONSISTENT** - Missing `actor_type` field, same as interaction entity.

---

### 5. Relationship Event Schema

**File**: `canonical/events/relationship/relationship.created.v1.json`

```json
{
  "actors": {
    "items": {
      "required": ["actor_id", "actor_role", "actor_type"],
      "properties": {
        "actor_id": { "type": "string" },
        "actor_role": { "type": "string" },
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

**Status**: ✅ Consistent with relationship entity

---

### 6. BFF Service

#### 6.1 Actor Resolver
**File**: `bff_service/app/auth/actor_resolver.py`

```python
class Actor(BaseModel):
    """Actor model."""
    actor_id: str
    actor_role: str
    actor_type: str  # ⚠️ Plain string
    tenant_id: Optional[str] = None
```

**Status**: ⚠️ **INCONSISTENT** - Uses plain `str` instead of enum. Also includes `tenant_id` which is not in canonical schemas.

---

#### 6.2 Audit Model
**File**: `bff_service/app/models/audit.py`

```python
class AuditActor(BaseModel):
    """Actor in audit event."""
    actor_id: str
    actor_role: str
    actor_type: str = Field(default="human_internal")  # ⚠️ Plain string with default
```

**Status**: ⚠️ **INCONSISTENT** - Uses plain `str` with default value.

---

### 7. Policy Service

**File**: `policy_service/cps_policy/models.py`

```python
class Actor(BaseModel):
    """Actor requesting authorization."""
    actor_id: str
    actor_role: str
    actor_type: str  # ⚠️ Plain string
    tenant_id: str  # ⚠️ Required, not in canonical
```

**Status**: ⚠️ **INCONSISTENT** - Uses plain `str` and includes required `tenant_id`.

---

### 8. Main App - Agent Orchestration

**File**: `rmbrain-mainapp/app/agent_orchestration/schemas.py`

```python
@dataclass
class ActorContext:
    """Actor Context (Read-Only)."""
    actor_id: str
    actor_type: str  # ⚠️ Different meaning: "rm" | "rm_team" | "client" | "client_rep"
    role: str  # ⚠️ Different field name (not actor_role)
    authority_level: str  # ⚠️ Additional field
    relationship_id: str  # ⚠️ Additional field
    communication_preferences: dict[str, Any] = field(default_factory=dict)
```

**Status**: ⚠️ **DIFFERENT STRUCTURE** - This appears to be a different concept (orchestration context) rather than a canonical actor schema. The `actor_type` here has different values and meaning.

---

## Inconsistency Summary

### Critical Issues

1. **Interaction schemas missing `actor_type`**
   - `canonical/entities/interaction.v1.json` - participants only have `actor_id` and `actor_role`
   - `canonical/events/interaction/interaction.initiated.v1.json` - same issue
   - **Impact**: Cannot determine if participant is human_internal, human_external, system, or service

2. **Python models using plain strings instead of enums**
   - `task_service/cds_task/schemas.py` - `AssigneeSchema.actor_type: str`
   - `bff_service/app/auth/actor_resolver.py` - `Actor.actor_type: str`
   - `bff_service/app/models/audit.py` - `AuditActor.actor_type: str`
   - `policy_service/cps_policy/models.py` - `Actor.actor_type: str`
   - **Impact**: No type safety, potential for invalid values

### Minor Issues

3. **Optional `display_name` field inconsistency**
   - Present in: relationship schemas, interaction schemas
   - Missing in: task schemas, event envelope
   - **Impact**: Low - field is optional, but inconsistency may cause confusion

4. **Additional fields in some models**
   - `bff_service/app/auth/actor_resolver.py` - `Actor.tenant_id: Optional[str]`
   - `policy_service/cps_policy/models.py` - `Actor.tenant_id: str` (required)
   - **Impact**: Medium - These are service-specific extensions, but should be documented

5. **Main app `ActorContext` has different structure**
   - Uses different field names and additional fields
   - **Impact**: Low - Appears to be intentionally different (orchestration context vs canonical actor)

---

## Recommendations

### High Priority

1. **Add `actor_type` to interaction schemas**
   - Update `canonical/entities/interaction.v1.json` participants schema
   - Update `canonical/events/interaction/interaction.initiated.v1.json` participants schema
   - Update interaction service models if needed

2. **Standardize Python models to use `ActorType` enum**
   - Create a shared `ActorType` enum (or import from relationship service)
   - Update all Python models to use the enum instead of plain strings
   - Consider creating a shared `Actor` base model

### Medium Priority

3. **Document optional fields**
   - Clarify when `display_name` should be included
   - Document service-specific extensions (like `tenant_id`)

4. **Consider shared actor schema module**
   - Create a canonical Python module with `ActorType` enum and `Actor` model
   - Import across all services for consistency

### Low Priority

5. **Clarify `ActorContext` vs `Actor`**
   - Document that `ActorContext` in main app is different from canonical `Actor`
   - Ensure naming doesn't cause confusion

---

## Files Requiring Updates

### JSON Schemas
- [ ] `canonical/entities/interaction.v1.json` - Add `actor_type` to participants
- [ ] `canonical/events/interaction/interaction.initiated.v1.json` - Add `actor_type` to participants

### Python Models
- [ ] `task_service/cds_task/schemas.py` - Use `ActorType` enum
- [ ] `bff_service/app/auth/actor_resolver.py` - Use `ActorType` enum
- [ ] `bff_service/app/models/audit.py` - Use `ActorType` enum
- [ ] `policy_service/cps_policy/models.py` - Use `ActorType` enum

### Shared Module (New)
- [ ] Create shared actor schema module (e.g., `canonical/schemas/actor.py` or similar)
  - Export `ActorType` enum
  - Export `Actor` base model
  - All services import from this module

---

## Notes

- The relationship service has the most complete and properly typed definition
- All JSON schemas that include `actor_type` use the same enum values (consistent)
- The main inconsistency is interaction schemas missing `actor_type`
- Python models should be updated to use enums for type safety
