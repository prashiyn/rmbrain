# Canonical Schema Library

Shared canonical schema library for RM Brain microservices.

This library provides access to:
- **Entity Schemas**: Canonical JSON schemas for entities (client, task, document, etc.)
- **Event Schemas**: Canonical JSON schemas for events (client.created, task.completed, etc.)
- **Semantic Constraints**: YAML-based semantic validation rules

## Installation

Add to your service's `pyproject.toml`:

```toml
dependencies = [
    "canonical @ file:///${PROJECT_ROOT}/canonical",
    # ... other dependencies
]
```

Or using `uv`:

```bash
uv add "canonical @ file:///${PROJECT_ROOT}/canonical"
```

## Usage

### Loading Entity Schemas

```python
from canonical import load_entity_schema, SchemaNotFoundError

try:
    client_schema = load_entity_schema("client", "v1")
    # Use schema for validation
except SchemaNotFoundError as e:
    print(f"Schema not found: {e}")
```

### Loading Event Schemas

```python
from canonical import load_event_schema, load_event_envelope_schema, EventNotFoundError

# Load event envelope schema
envelope_schema = load_event_envelope_schema()

# Load specific event schema
try:
    client_created_schema = load_event_schema("client.created", "v1")
except EventNotFoundError as e:
    print(f"Event schema not found: {e}")
```

### Loading Semantic Constraints

```python
from canonical import load_semantic_constraints

# Load semantic constraints (returns empty if not found)
constraints = load_semantic_constraints("client", "v1")
required_fields = constraints.get("required_fields", [])
semantic_rules = constraints.get("semantic_constraints", {})
```

### Listing Available Schemas

```python
from canonical import list_entities, list_events, list_entity_versions

# List all entities
entities = list_entities()  # ['client', 'document', 'task', ...]

# List all events for a domain
client_events = list_events("client")  # ['client.created', 'client.updated', ...]

# List all events
all_events = list_events()  # All events across all domains

# List versions for an entity
versions = list_entity_versions("client")  # ['v1']
```

## API Reference

### Functions

- `load_entity_schema(entity: str, version: str = "v1") -> dict[str, Any]`
  - Load canonical entity schema
  - Raises `SchemaNotFoundError` if not found

- `load_event_schema(event_type: str, version: str = "v1") -> dict[str, Any]`
  - Load canonical event schema
  - Event type format: `"domain.event_name"` (e.g., `"client.created"`)
  - Raises `EventNotFoundError` if not found

- `load_event_envelope_schema() -> dict[str, Any]`
  - Load canonical event envelope schema
  - Raises `SchemaNotFoundError` if not found

- `load_semantic_constraints(entity: str, version: str = "v1") -> dict[str, Any]`
  - Load semantic constraints for an entity
  - Returns empty constraints if file not found (semantics are optional)

- `list_entities() -> list[str]`
  - List all available entity names

- `list_entity_versions(entity: str) -> list[str]`
  - List all versions for an entity

- `list_events(domain: str | None = None) -> list[str]`
  - List events for a domain, or all events if domain is None

- `list_event_versions(event_type: str) -> list[str]`
  - List all versions for an event type

### Exceptions

- `SchemaNotFoundError`: Raised when entity or envelope schema not found
- `EventNotFoundError`: Raised when event schema not found
- `SemanticNotFoundError`: Raised when semantic file exists but cannot be loaded

## Directory Structure

```
canonical/
├── __init__.py
├── registry.py
├── pyproject.toml
├── README.md
├── entities/
│   ├── client.v1.json
│   ├── task.v1.json
│   └── ...
├── events/
│   ├── event_envelope.v1.json
│   ├── client/
│   │   ├── client.created.v1.json
│   │   └── ...
│   └── ...
└── semantics/
    ├── client.v1.semantic.yaml
    └── ...
```

## Caching

All schemas are cached in memory after first load for performance. The cache is module-level and persists for the lifetime of the Python process.
