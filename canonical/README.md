# Canonical Schema Library

Shared canonical schema library for RM Brain microservices.

This library provides access to:
- **Entity Schemas**: Canonical JSON schemas for entities (client, task, document, etc.)
- **Event Schemas**: Canonical JSON schemas for events (client.created, task.completed, etc.)
- **Semantic Constraints**: YAML-based semantic validation rules

---

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

---

## Quick Start

```python
from canonical import load_entity_schema, load_event_schema

# Load entity schema
client_schema = load_entity_schema("client", "v1")

# Load event schema
client_created_schema = load_event_schema("client.created", "v1")
```

For detailed usage instructions, see [CANONICAL_USAGE_GUIDE.md](./CANONICAL_USAGE_GUIDE.md).

---

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

- `get_event_schema_path(event_type: str, version: str = "v1") -> Path`
  - Get the file path for an event schema (for testing/debugging)

### Exceptions

- `SchemaNotFoundError`: Raised when entity or envelope schema not found
- `EventNotFoundError`: Raised when event schema not found
- `SemanticNotFoundError`: Raised when semantic file exists but cannot be loaded

---

## Complete Directory Structure

```
canonical/
├── pyproject.toml              # Package configuration
├── uv.lock                     # Dependency lock file
├── README.md                   # This file
├── CANONICAL_USAGE_GUIDE.md    # Comprehensive usage guide
└── src/
    └── canonical/
        ├── __init__.py         # Package exports
        ├── registry.py         # Schema loading and caching logic
        ├── entities/           # Entity JSON schemas
        │   ├── client.v1.json
        │   ├── client_link.v1.json
        │   ├── document.v1.json
        │   ├── interaction.v1.json
        │   ├── product.v1.json
        │   ├── relationship.v1.json
        │   ├── riskprofile.v1.json
        │   ├── suitability_assessment.v1.json
        │   └── task.v1.json
        ├── events/             # Event JSON schemas
        │   ├── event_envelope.v1.json
        │   ├── client/          # Client domain events
        │   │   ├── client.created.v1.json
        │   │   ├── client.updated.v1.json
        │   │   ├── client.status_changed.v1.json
        │   │   ├── client_link.created.v1.json
        │   │   ├── client_link.updated.v1.json
        │   │   └── client_link.terminated.v1.json
        │   ├── document/        # Document domain events
        │   │   ├── document.ingested.v1.json
        │   │   ├── document.updated.v1.json
        │   │   ├── document.status_changed.v1.json
        │   │   ├── document.access_changed.v1.json
        │   │   ├── document.linked.v1.json
        │   │   ├── document.version_added.v1.json
        │   │   └── document.superseded.v1.json
        │   ├── interaction/    # Interaction domain events
        │   │   ├── interaction.created.v1.json
        │   │   ├── interaction.initiated.v1.json
        │   │   ├── interaction.completed.v1.json
        │   │   ├── interaction.finalized.v1.json
        │   │   ├── interaction.status_changed.v1.json
        │   │   ├── interaction.review_started.v1.json
        │   │   ├── interaction.cancelled.v1.json
        │   │   ├── interaction.superseded.v1.json
        │   │   ├── interaction.documents_attached.v1.json
        │   │   └── document.linked.v1.json
        │   ├── product/         # Product domain events
        │   │   ├── product.created.v1.json
        │   │   ├── product.updated.v1.json
        │   │   ├── product.deactivated.v1.json
        │   │   ├── product.status_changed.v1.json
        │   │   └── product.artefact.linked.v1.json
        │   ├── relationship/    # Relationship domain events
        │   │   ├── relationship.created.v1.json
        │   │   ├── relationship.status_changed.v1.json
        │   │   ├── relationship.health_updated.v1.json
        │   │   ├── relationship.preferences_updated.v1.json
        │   │   ├── relationship.at_risk.v1.json
        │   │   └── relationship.terminated.v1.json
        │   ├── riskprofile/     # Risk profile domain events
        │   │   ├── riskprofile.created.v1.json
        │   │   ├── riskprofile.updated.v1.json
        │   │   ├── riskprofile.activated.v1.json
        │   │   ├── riskprofile.superseded.v1.json
        │   │   ├── suitability.assessed.v1.json
        │   │   └── suitability.breached.v1.json
        │   └── task/            # Task domain events
        │       ├── task.created.v1.json
        │       ├── task.completed.v1.json
        │       ├── task.status_changed.v1.json
        │       ├── task.expired.v1.json
        │       ├── document.uploaded.v1.json
        │       ├── interaction.finalized.v1.json
        │       └── riskprofile.changed.v1.json
        └── semantics/          # Semantic constraint YAML files
            └── client.v1.semantic.yaml
```

---

## Available Entities

- `client` - Client entity schema
- `client_link` - Client link/relationship schema
- `document` - Document entity schema
- `interaction` - Interaction entity schema
- `product` - Product entity schema
- `relationship` - Relationship entity schema
- `riskprofile` - Risk profile entity schema
- `suitability_assessment` - Suitability assessment entity schema
- `task` - Task entity schema

---

## Available Event Domains

- **client** - Client lifecycle events (created, updated, status_changed, client_link events)
- **document** - Document lifecycle events (ingested, updated, status_changed, etc.)
- **interaction** - Interaction lifecycle events (created, initiated, completed, etc.)
- **product** - Product lifecycle events (created, updated, deactivated, etc.)
- **relationship** - Relationship lifecycle events (created, status_changed, terminated, etc.)
- **riskprofile** - Risk profile and suitability events
- **task** - Task lifecycle events and consumed events

---

## Caching

All schemas are cached in memory after first load for performance. The cache is module-level and persists for the lifetime of the Python process.

---

## See Also

- [CANONICAL_USAGE_GUIDE.md](./CANONICAL_USAGE_GUIDE.md) - Comprehensive usage guide with examples
- [canonical_schemas/](../canonical_schemas/) - Alternative schema library (if applicable)
