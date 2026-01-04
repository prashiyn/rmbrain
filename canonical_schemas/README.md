# Canonical Schemas Package

This package provides Python implementations of canonical schemas that are shared across all services in the RM Brain codebase.

## Purpose

The schemas in this package correspond to the JSON schemas defined in the `canonical/` directory and provide:
- Type-safe Python models using Pydantic
- Enum definitions for consistent values
- Validation logic
- Single source of truth for schema definitions

## Installation

This package is installed as a dependency in all services via `pyproject.toml`:

```toml
dependencies = [
    "canonical-schemas @ file:///media/prashanth/extmnt1/rmbrain/canonical_schemas",
    # ... other dependencies
]
```

Install using `uv`:

```bash
cd <service_directory>
uv sync
```

Or using `pip`:

```bash
pip install -e /path/to/rmbrain/canonical_schemas
```

## Usage

### Importing Actor Schemas

The package provides clean imports - no path manipulation needed:

```python
from canonical_schemas import Actor, ActorRole, ActorType

# Create an actor
actor = Actor(
    actor_id="rm_123",
    actor_role=ActorRole.RM,
    actor_type=ActorType.HUMAN_INTERNAL,
    display_name="John Doe"
)
```

You can also import from the specific module:

```python
from canonical_schemas.actor import Actor, ActorRole, ActorType
```

### Using in Service Code

All services should import and use these schemas instead of defining their own:

```python
# ✅ Good - Import from canonical_schemas package
from canonical_schemas import Actor, ActorType

# ❌ Bad - Don't define your own
class Actor(BaseModel):
    actor_id: str
    actor_type: str  # Plain string, no validation
```

## Package Structure

```
canonical_schemas/
├── pyproject.toml              # Package configuration
├── README.md                   # This file
├── USAGE_EXAMPLES.md           # Detailed usage examples
└── src/
    └── canonical_schemas/
        ├── __init__.py         # Package exports
        ├── actor.py            # Actor schema definitions
        └── registry.py         # Schema registry pattern
```

### Available Schemas

- **Actor**: Canonical actor model with `actor_id`, `actor_role`, `actor_type`, `display_name`
- **ActorType**: Enum for actor types (`human_internal`, `human_external`, `system`, `service`)
- **ActorRole**: Enum for actor roles (rm, relationship_manager, client, etc.)

### Registry Pattern

The package includes a registry for schema classes:

```python
from canonical_schemas.registry import get_schema_class, list_schemas

# Get a schema class by name
ActorClass = get_schema_class("Actor")

# List all available schemas
schemas = list_schemas()  # Returns: ["Actor", "ActorRole", "ActorType"]
```

## Alignment with JSON Schemas

The Python schemas in this package are designed to match the JSON schemas in `canonical/entities/` and `canonical/events/`. When JSON schemas are updated, corresponding Python schemas should be updated to maintain consistency.

## Development

### Adding New Schemas

To add a new schema to the package:

1. Create a new module in `src/canonical_schemas/` (e.g., `task.py`)
2. Define your Pydantic models and enums
3. Export them in `src/canonical_schemas/__init__.py`
4. Optionally register them in `registry.py`

### Package Version

The package version is defined in `pyproject.toml` and `src/canonical_schemas/__init__.py`. Update both when releasing a new version.

## Documentation

For detailed usage examples, see:
- `USAGE_EXAMPLES.md` - Comprehensive examples for different service contexts

For detailed documentation on actor types and roles, see:
- `relationship_service/docs/relationship_service.md` (lines 42-62)

## Dependencies

- `pydantic>=2.5.0` - For schema definitions and validation

## Related Packages

- `canonical` - JSON schema registry for entity and event schemas
