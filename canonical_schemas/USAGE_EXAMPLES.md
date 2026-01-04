# Usage Examples - Canonical Actor Schemas

This document provides practical examples of how to use the canonical actor schemas in different service contexts.

## Prerequisites

The `canonical-schemas` package must be installed as a dependency in your service's `pyproject.toml`:

```toml
dependencies = [
    "canonical-schemas @ file:///media/prashanth/extmnt1/rmbrain/canonical_schemas",
]
```

Install with:
```bash
uv sync
```

## Basic Usage

### Importing the Schemas

The package provides clean imports - no path manipulation needed:

```python
# Preferred: Import from package root
from canonical_schemas import Actor, ActorRole, ActorType

# Alternative: Import from specific module (also works)
from canonical_schemas.actor import Actor, ActorRole, ActorType
```

### Creating an Actor

```python
# Basic actor
actor = Actor(
    actor_id="rm_123",
    actor_role=ActorRole.RM,
    actor_type=ActorType.HUMAN_INTERNAL,
    display_name="John Doe"
)

# Actor without display name
actor = Actor(
    actor_id="client_456",
    actor_role=ActorRole.CLIENT,
    actor_type=ActorType.HUMAN_EXTERNAL
)

# System actor
system_actor = Actor(
    actor_id="scheduler_001",
    actor_role=ActorRole.SCHEDULER,
    actor_type=ActorType.SYSTEM
)
```

### Serialization

```python
# To dict (for JSON serialization)
actor_dict = actor.model_dump()
# Output: {
#     "actor_id": "rm_123",
#     "actor_role": "rm",
#     "actor_type": "human_internal",
#     "display_name": "John Doe"
# }

# To JSON string
actor_json = actor.model_dump_json()
```

### Deserialization

```python
# From dict
actor_data = {
    "actor_id": "rm_123",
    "actor_role": "rm",
    "actor_type": "human_internal",
    "display_name": "John Doe"
}
actor = Actor(**actor_data)

# From JSON string
actor = Actor.model_validate_json(actor_json_string)
```

## Service-Specific Examples

### Task Service - Assignee Schema

**Before**:
```python
class AssigneeSchema(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: str  # Plain string
```

**After**:
```python
from canonical_schemas import Actor

class AssigneeSchema(Actor):
    """Task assignee - uses canonical Actor schema."""
    pass
```

**Usage**:
```python
assignee = AssigneeSchema(
    actor_id="rm_123",
    actor_role=ActorRole.RM,
    actor_type=ActorType.HUMAN_INTERNAL
)
```

### BFF Service - Actor Resolver with Extension

**Before**:
```python
class Actor(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: str
    tenant_id: Optional[str] = None
```

**After**:
```python
from canonical_schemas import Actor as CanonicalActor

class Actor(CanonicalActor):
    """BFF actor with tenant context."""
    tenant_id: Optional[str] = None
```

**Usage**:
```python
actor = Actor(
    actor_id="rm_123",
    actor_role=ActorRole.RM,
    actor_type=ActorType.HUMAN_INTERNAL,
    tenant_id="tenant_001"
)
```

### Policy Service - Actor with Required Tenant

**Before**:
```python
class Actor(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: str
    tenant_id: str  # Required
```

**After**:
```python
from canonical_schemas.actor import Actor as CanonicalActor

class Actor(CanonicalActor):
    """Policy service actor with required tenant."""
    tenant_id: str  # Required for policy evaluation
```

### Relationship Service - Direct Usage

**Before**:
```python
class ActorType(str, Enum):
    HUMAN_INTERNAL = "human_internal"
    # ... etc

class Actor(BaseModel):
    actor_id: str
    actor_role: str
    actor_type: ActorType
    display_name: Optional[str] = None
```

**After**:
```python
from canonical_schemas import Actor, ActorType, ActorRole

# Use directly, no need to redefine
```

## Validation Examples

### Validating Actor Role and Type

```python
from canonical_schemas import validate_actor_role_type, ActorRole, ActorType

# Valid combinations
assert validate_actor_role_type(ActorRole.RM, ActorType.HUMAN_INTERNAL) == True
assert validate_actor_role_type(ActorRole.CLIENT, ActorType.HUMAN_EXTERNAL) == True
assert validate_actor_role_type(ActorRole.SYSTEM, ActorType.SYSTEM) == True

# Invalid combinations
assert validate_actor_role_type(ActorRole.CLIENT, ActorType.HUMAN_INTERNAL) == False
assert validate_actor_role_type(ActorRole.RM, ActorType.SYSTEM) == False
```

### Pydantic Validation

```python
from canonical_schemas import Actor, ActorRole, ActorType
from pydantic import ValidationError

try:
    # Invalid actor_type
    actor = Actor(
        actor_id="test",
        actor_role=ActorRole.RM,
        actor_type="invalid_type"  # Will raise ValidationError
    )
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    # Invalid actor_role
    actor = Actor(
        actor_id="test",
        actor_role="invalid_role",  # Will raise ValidationError
        actor_type=ActorType.HUMAN_INTERNAL
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```

## FastAPI Integration

### Request/Response Models

```python
from fastapi import FastAPI
from canonical_schemas import Actor, ActorRole, ActorType

app = FastAPI()

@app.post("/tasks/{task_id}/assign")
async def assign_task(task_id: str, assignee: Actor):
    """Assign task to actor."""
    # assignee is already validated by Pydantic
    if assignee.actor_type != ActorType.HUMAN_INTERNAL:
        raise HTTPException(
            status_code=400,
            detail="Only human_internal actors can be assigned tasks"
        )
    # ... assign task
    return {"status": "assigned", "assignee": assignee.model_dump()}
```

### Header-Based Actor Resolution

```python
from fastapi import Header
from canonical_schemas import Actor, ActorRole, ActorType

@app.get("/tasks")
async def list_tasks(
    x_actor_id: str = Header(..., alias="X-Actor-Id"),
    x_actor_role: str = Header(..., alias="X-Actor-Role"),
    x_actor_type: str = Header(..., alias="X-Actor-Type"),
):
    """List tasks for actor."""
    # Convert headers to canonical actor
    actor = Actor(
        actor_id=x_actor_id,
        actor_role=ActorRole(x_actor_role),  # Enum validation
        actor_type=ActorType(x_actor_type)   # Enum validation
    )
    # ... use actor
    return {"tasks": []}
```

## Database Integration

### SQLAlchemy JSONB Column

```python
from sqlalchemy import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from canonical_schemas import Actor

class Task(Base):
    __tablename__ = "tasks"
    
    assignee: Mapped[dict] = mapped_column(JSONB, nullable=False)
    
    def set_assignee(self, actor: Actor):
        """Set assignee from Actor model."""
        self.assignee = actor.model_dump()
    
    def get_assignee(self) -> Actor:
        """Get assignee as Actor model."""
        return Actor(**self.assignee)
```

## Event Publishing

### Creating Event with Actor

```python
from canonical_schemas import Actor, ActorRole, ActorType
from canonical.events.event_envelope import create_event_envelope

actor = Actor(
    actor_id="rm_123",
    actor_role=ActorRole.RM,
    actor_type=ActorType.HUMAN_INTERNAL
)

event = create_event_envelope(
    event_type="task.created",
    entity_type="task",
    entity_id="task_123",
    actor=actor.model_dump(),  # Convert to dict for JSON
    payload={"task_id": "task_123", ...}
)
```

## Testing Examples

### Test Fixtures

```python
import pytest
from canonical_schemas import Actor, ActorRole, ActorType

@pytest.fixture
def rm_actor():
    """Fixture for RM actor."""
    return Actor(
        actor_id="rm_test_123",
        actor_role=ActorRole.RM,
        actor_type=ActorType.HUMAN_INTERNAL,
        display_name="Test RM"
    )

@pytest.fixture
def client_actor():
    """Fixture for client actor."""
    return Actor(
        actor_id="client_test_456",
        actor_role=ActorRole.CLIENT,
        actor_type=ActorType.HUMAN_EXTERNAL
    )

def test_task_assignment(rm_actor):
    """Test task assignment."""
    task = create_task(assignee=rm_actor.model_dump())
    assert task.assignee["actor_type"] == "human_internal"
    assert task.assignee["actor_role"] == "rm"
```

### Mocking in Tests

```python
from unittest.mock import patch
from canonical_schemas import Actor, ActorRole, ActorType

@patch('canonical_schemas.Actor')
def test_with_mocked_actor(mock_actor):
    """Test with mocked actor."""
    mock_actor.return_value = Actor(
        actor_id="mock_123",
        actor_role=ActorRole.RM,
        actor_type=ActorType.HUMAN_INTERNAL
    )
    # ... test code
```

## Package Structure

The package follows standard Python package structure:

```
canonical_schemas/
├── pyproject.toml              # Package configuration
├── README.md                   # Package documentation
├── USAGE_EXAMPLES.md           # This file
└── src/
    └── canonical_schemas/
        ├── __init__.py         # Package exports (Actor, ActorRole, ActorType)
        ├── actor.py            # Actor schema definitions
        └── registry.py         # Schema registry pattern
```

### Import Patterns

The package supports two import patterns:

```python
# Pattern 1: Import from package root (recommended)
from canonical_schemas import Actor, ActorRole, ActorType

# Pattern 2: Import from specific module (also works)
from canonical_schemas.actor import Actor, ActorRole, ActorType
```

Both patterns work, but importing from the package root is recommended as it's cleaner and aligns with the package's `__init__.py` exports.

## Migration Helper Functions

### Converting Legacy Data

```python
from canonical_schemas import Actor, ActorRole, ActorType

def infer_actor_type_from_role(actor_role: str) -> ActorType:
    """Infer actor_type from legacy actor_role string."""
    role_mapping = {
        "rm": ActorType.HUMAN_INTERNAL,
        "product_manager": ActorType.HUMAN_INTERNAL,
        "investment_specialist": ActorType.HUMAN_INTERNAL,
        "client": ActorType.HUMAN_EXTERNAL,
        "prospect": ActorType.HUMAN_EXTERNAL,
        "system": ActorType.SYSTEM,
    }
    return role_mapping.get(actor_role, ActorType.HUMAN_INTERNAL)

def migrate_legacy_actor(legacy_data: dict) -> Actor:
    """Convert legacy actor dict to canonical Actor."""
    actor_type = legacy_data.get("actor_type")
    if not actor_type:
        # Infer from role if missing
        actor_type = infer_actor_type_from_role(legacy_data["actor_role"])
    
    return Actor(
        actor_id=legacy_data["actor_id"],
        actor_role=ActorRole(legacy_data["actor_role"]),
        actor_type=ActorType(actor_type),
        display_name=legacy_data.get("display_name")
    )
```
