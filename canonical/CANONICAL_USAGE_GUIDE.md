# Canonical Schema Library - Comprehensive Usage Guide

**Complete guide for using the Canonical Schema Library in RM Brain services**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Core Concepts](#core-concepts)
4. [Entity Schemas](#entity-schemas)
5. [Event Schemas](#event-schemas)
6. [Event Envelope](#event-envelope)
7. [Semantic Constraints](#semantic-constraints)
8. [Using Schemas Independently](#using-schemas-independently)
9. [Using Schemas Collectively](#using-schemas-collectively)
10. [Validation Examples](#validation-examples)
11. [Common Patterns](#common-patterns)
12. [Error Handling](#error-handling)
13. [Best Practices](#best-practices)
14. [Complete Schema Reference](#complete-schema-reference)

---

## Introduction

The Canonical Schema Library provides a centralized, versioned collection of JSON schemas for all entities and events in the RM Brain system. This library ensures consistency across all microservices and provides a single source of truth for data structures.

### Key Benefits

- **Consistency**: All services use the same schema definitions
- **Type Safety**: JSON Schema validation ensures data integrity
- **Versioning**: Support for schema versioning and evolution
- **Caching**: In-memory caching for performance
- **Discoverability**: Easy listing and discovery of available schemas

---

## Installation

### Add to pyproject.toml

```toml
[project]
dependencies = [
    "canonical @ file:///${PROJECT_ROOT}/canonical",
    # ... other dependencies
]
```

### Using uv

```bash
uv add "canonical @ file:///${PROJECT_ROOT}/canonical"
```

### Using pip

```bash
pip install -e /path/to/canonical
```

---

## Core Concepts

### Entity Schemas

Entity schemas define the structure of core business entities (e.g., `client`, `task`, `document`). These are the canonical representations of domain objects.

### Event Schemas

Event schemas define the payload structure for domain events (e.g., `client.created`, `task.completed`). Events are organized by domain (client, task, document, etc.).

### Event Envelope

All events are wrapped in a standard event envelope that provides metadata (event_id, source, actor, timestamp, etc.) and contains the event-specific payload.

### Semantic Constraints

Optional YAML files that define additional semantic validation rules beyond JSON Schema validation.

---

## Entity Schemas

### Loading Entity Schemas

```python
from canonical import load_entity_schema, SchemaNotFoundError

try:
    # Load client entity schema
    client_schema = load_entity_schema("client", "v1")
    
    # Use schema for validation
    import jsonschema
    jsonschema.validate(instance=client_data, schema=client_schema)
    
except SchemaNotFoundError as e:
    print(f"Schema not found: {e}")
```

### Available Entity Schemas

| Entity | Description | Version |
|--------|-------------|---------|
| `client` | Client entity schema | v1 |
| `client_link` | Client link/relationship schema | v1 |
| `document` | Document entity schema | v1 |
| `interaction` | Interaction entity schema | v1 |
| `product` | Product entity schema | v1 |
| `relationship` | Relationship entity schema | v1 |
| `riskprofile` | Risk profile entity schema | v1 |
| `suitability_assessment` | Suitability assessment entity schema | v1 |
| `task` | Task entity schema | v1 |

### Example: Using Client Entity Schema

```python
from canonical import load_entity_schema
import jsonschema

# Load schema
client_schema = load_entity_schema("client", "v1")

# Validate client data
client_data = {
    "client_id": "CLIENT_123",
    "tenant_id": "TENANT_001",
    "name": "Acme Corp",
    "status": "active",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
}

try:
    jsonschema.validate(instance=client_data, schema=client_schema)
    print("Client data is valid")
except jsonschema.ValidationError as e:
    print(f"Validation error: {e.message}")
```

### Example: Using Task Entity Schema

```python
from canonical import load_entity_schema
import jsonschema

# Load schema
task_schema = load_entity_schema("task", "v1")

# Validate task data
task_data = {
    "task_id": "TASK_456",
    "tenant_id": "TENANT_001",
    "task_type": "compliance_review",
    "status": "open",
    "priority": "high",
    "assignee": {
        "actor_id": "USER_789",
        "actor_role": "relationship_manager",
        "actor_type": "human_internal"
    },
    "scope": {
        "primary_client_id": "CLIENT_123"
    },
    "source_event": {
        "event_type": "document.ingested",
        "entity_type": "document",
        "entity_id": "DOC_789"
    },
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
}

jsonschema.validate(instance=task_data, schema=task_schema)
```

---

## Event Schemas

### Loading Event Schemas

```python
from canonical import load_event_schema, EventNotFoundError

try:
    # Load event schema (format: "domain.event_name")
    client_created_schema = load_event_schema("client.created", "v1")
    
    # Use for validation
    import jsonschema
    jsonschema.validate(instance=event_payload, schema=client_created_schema)
    
except EventNotFoundError as e:
    print(f"Event schema not found: {e}")
```

### Event Naming Convention

Events follow the pattern: `domain.event_name` (e.g., `client.created`, `task.completed`)

### Available Event Schemas by Domain

#### Client Domain Events

| Event | Description |
|-------|-------------|
| `client.created` | Client entity created |
| `client.updated` | Client entity updated |
| `client.status_changed` | Client status changed |
| `client_link.created` | Client link created |
| `client_link.updated` | Client link updated |
| `client_link.terminated` | Client link terminated |

#### Document Domain Events

| Event | Description |
|-------|-------------|
| `document.ingested` | Document ingested into system |
| `document.updated` | Document updated |
| `document.status_changed` | Document status changed |
| `document.access_changed` | Document access permissions changed |
| `document.linked` | Document linked to entity |
| `document.version_added` | New document version added |
| `document.superseded` | Document superseded by another |

#### Interaction Domain Events

| Event | Description |
|-------|-------------|
| `interaction.created` | Interaction created |
| `interaction.initiated` | Interaction initiated |
| `interaction.completed` | Interaction completed |
| `interaction.finalized` | Interaction finalized |
| `interaction.status_changed` | Interaction status changed |
| `interaction.review_started` | Interaction review started |
| `interaction.cancelled` | Interaction cancelled |
| `interaction.superseded` | Interaction superseded |
| `interaction.documents_attached` | Documents attached to interaction |
| `document.linked` | Document linked to interaction |

#### Product Domain Events

| Event | Description |
|-------|-------------|
| `product.created` | Product created |
| `product.updated` | Product updated |
| `product.deactivated` | Product deactivated |
| `product.status_changed` | Product status changed |
| `product.artefact.linked` | Artefact linked to product |

#### Relationship Domain Events

| Event | Description |
|-------|-------------|
| `relationship.created` | Relationship created |
| `relationship.status_changed` | Relationship status changed |
| `relationship.health_updated` | Relationship health updated |
| `relationship.preferences_updated` | Relationship preferences updated |
| `relationship.at_risk` | Relationship marked as at risk |
| `relationship.terminated` | Relationship terminated |

#### Risk Profile Domain Events

| Event | Description |
|-------|-------------|
| `riskprofile.created` | Risk profile created |
| `riskprofile.updated` | Risk profile updated |
| `riskprofile.activated` | Risk profile activated |
| `riskprofile.superseded` | Risk profile superseded |
| `suitability.assessed` | Suitability assessment completed |
| `suitability.breached` | Suitability breach detected |

#### Task Domain Events

| Event | Description |
|-------|-------------|
| `task.created` | Task created |
| `task.completed` | Task completed |
| `task.status_changed` | Task status changed |
| `task.expired` | Task expired |
| `document.uploaded` | Document uploaded (consumed event) |
| `interaction.finalized` | Interaction finalized (consumed event) |
| `riskprofile.changed` | Risk profile changed (consumed event) |

### Example: Using Client Created Event Schema

```python
from canonical import load_event_schema
import jsonschema

# Load event schema
client_created_schema = load_event_schema("client.created", "v1")

# Validate event payload
event_payload = {
    "client_id": "CLIENT_123",
    "tenant_id": "TENANT_001",
    "name": "Acme Corp",
    "status": "active",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
}

jsonschema.validate(instance=event_payload, schema=client_created_schema)
```

### Example: Using Task Created Event Schema

```python
from canonical import load_event_schema

# Load event schema
task_created_schema = load_event_schema("task.created", "v1")

# Task created event contains full task entity
task_event_payload = {
    "task_id": "TASK_456",
    "tenant_id": "TENANT_001",
    "task_type": "compliance_review",
    "status": "open",
    "priority": "high",
    "assignee": {
        "actor_id": "USER_789",
        "actor_role": "relationship_manager",
        "actor_type": "human_internal"
    },
    "scope": {
        "primary_client_id": "CLIENT_123"
    },
    "source_event": {
        "event_type": "document.ingested",
        "entity_type": "document",
        "entity_id": "DOC_789"
    },
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
}

jsonschema.validate(instance=task_event_payload, schema=task_created_schema)
```

---

## Event Envelope

All events in RM Brain are wrapped in a standard event envelope. The envelope provides metadata and contains the event-specific payload.

### Loading Event Envelope Schema

```python
from canonical import load_event_envelope_schema

# Load envelope schema
envelope_schema = load_event_envelope_schema()
```

### Event Envelope Structure

```python
{
    "event_id": "EVENT_UUID",
    "event_type": "client.created",
    "event_version": "v1",
    "source": {
        "service": "cds_client",
        "environment": "prod"
    },
    "tenant_id": "TENANT_001",
    "entity": {
        "entity_type": "client",
        "entity_id": "CLIENT_123"
    },
    "actor": {
        "actor_id": "USER_789",
        "actor_role": "relationship_manager",
        "actor_type": "human_internal"
    },
    "occurred_at": "2025-01-15T10:00:00Z",
    "correlation_id": "CORR_123",  # Optional
    "payload": {
        # Event-specific payload (validated against event schema)
    }
}
```

### Example: Creating and Validating Event Envelope

```python
from canonical import load_event_envelope_schema, load_event_schema
import jsonschema
import uuid
from datetime import datetime

# Load schemas
envelope_schema = load_event_envelope_schema()
client_created_schema = load_event_schema("client.created", "v1")

# Create event envelope
event_envelope = {
    "event_id": str(uuid.uuid4()),
    "event_type": "client.created",
    "event_version": "v1",
    "source": {
        "service": "cds_client",
        "environment": "prod"
    },
    "tenant_id": "TENANT_001",
    "entity": {
        "entity_type": "client",
        "entity_id": "CLIENT_123"
    },
    "actor": {
        "actor_id": "USER_789",
        "actor_role": "relationship_manager",
        "actor_type": "human_internal"
    },
    "occurred_at": datetime.utcnow().isoformat() + "Z",
    "payload": {
        "client_id": "CLIENT_123",
        "tenant_id": "TENANT_001",
        "name": "Acme Corp",
        "status": "active",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
}

# Validate envelope
jsonschema.validate(instance=event_envelope, schema=envelope_schema)

# Validate payload separately
jsonschema.validate(instance=event_envelope["payload"], schema=client_created_schema)
```

---

## Semantic Constraints

Semantic constraints provide additional validation rules beyond JSON Schema. They are optional and defined in YAML files.

### Loading Semantic Constraints

```python
from canonical import load_semantic_constraints

# Load constraints (returns empty dict if not found)
constraints = load_semantic_constraints("client", "v1")

# Access constraint data
required_fields = constraints.get("required_fields", [])
semantic_rules = constraints.get("semantic_constraints", {})
cross_field_constraints = constraints.get("cross_field_constraints", [])
```

### Example: Using Semantic Constraints

```python
from canonical import load_semantic_constraints

constraints = load_semantic_constraints("client", "v1")

# Check required fields
if "name" not in constraints.get("required_fields", []):
    raise ValueError("Name is required")

# Apply semantic rules
semantic_rules = constraints.get("semantic_constraints", {})
if "email" in semantic_rules:
    email_rule = semantic_rules["email"]
    # Apply email validation rule
```

---

## Using Schemas Independently

### Pattern 1: Entity Validation in Service Layer

```python
from canonical import load_entity_schema
import jsonschema
from fastapi import HTTPException

def create_client(client_data: dict):
    # Load schema
    client_schema = load_entity_schema("client", "v1")
    
    # Validate before saving
    try:
        jsonschema.validate(instance=client_data, schema=client_schema)
    except jsonschema.ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid client data: {e.message}")
    
    # Proceed with creation
    # ...
```

### Pattern 2: Event Payload Validation

```python
from canonical import load_event_schema
import jsonschema

def emit_client_created_event(client_data: dict):
    # Load event schema
    event_schema = load_event_schema("client.created", "v1")
    
    # Validate payload
    try:
        jsonschema.validate(instance=client_data, schema=event_schema)
    except jsonschema.ValidationError as e:
        raise ValueError(f"Invalid event payload: {e.message}")
    
    # Create and emit event
    # ...
```

### Pattern 3: Schema Discovery

```python
from canonical import list_entities, list_events, list_entity_versions

# Discover available entities
entities = list_entities()
print(f"Available entities: {entities}")

# Discover events for a domain
client_events = list_events("client")
print(f"Client events: {client_events}")

# Discover all events
all_events = list_events()
print(f"All events: {all_events}")

# Check versions
versions = list_entity_versions("client")
print(f"Client versions: {versions}")
```

---

## Using Schemas Collectively

### Pattern 1: Event Publishing with Envelope

```python
from canonical import load_event_envelope_schema, load_event_schema
import jsonschema
import uuid
from datetime import datetime

def publish_event(event_type: str, payload: dict, actor: dict, tenant_id: str):
    # Load both schemas
    envelope_schema = load_event_envelope_schema()
    event_schema = load_event_schema(event_type, "v1")
    
    # Validate payload first
    jsonschema.validate(instance=payload, schema=event_schema)
    
    # Create envelope
    envelope = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "event_version": "v1",
        "source": {
            "service": "cds_client",
            "environment": "prod"
        },
        "tenant_id": tenant_id,
        "entity": {
            "entity_type": event_type.split(".")[0],
            "entity_id": payload.get(f"{event_type.split('.')[0]}_id")
        },
        "actor": actor,
        "occurred_at": datetime.utcnow().isoformat() + "Z",
        "payload": payload
    }
    
    # Validate envelope
    jsonschema.validate(instance=envelope, schema=envelope_schema)
    
    # Publish via Dapr
    # ...
```

### Pattern 2: Event Consumption with Validation

```python
from canonical import load_event_envelope_schema, load_event_schema
import jsonschema

def handle_event(event_envelope: dict):
    # Load envelope schema
    envelope_schema = load_event_envelope_schema()
    
    # Validate envelope
    jsonschema.validate(instance=event_envelope, schema=envelope_schema)
    
    # Extract event details
    event_type = event_envelope["event_type"]
    event_version = event_envelope["event_version"]
    payload = event_envelope["payload"]
    
    # Load and validate event-specific schema
    event_schema = load_event_schema(event_type, event_version)
    jsonschema.validate(instance=payload, schema=event_schema)
    
    # Process event
    # ...
```

### Pattern 3: Multi-Entity Validation

```python
from canonical import load_entity_schema
import jsonschema

def validate_relationship_creation(relationship_data: dict, client_data: dict):
    # Load multiple schemas
    relationship_schema = load_entity_schema("relationship", "v1")
    client_schema = load_entity_schema("client", "v1")
    
    # Validate both
    jsonschema.validate(instance=relationship_data, schema=relationship_schema)
    jsonschema.validate(instance=client_data, schema=client_schema)
    
    # Additional cross-entity validation
    if relationship_data["primary_client_id"] != client_data["client_id"]:
        raise ValueError("Primary client ID mismatch")
    
    # Proceed with creation
    # ...
```

### Pattern 4: Schema-Based Data Transformation

```python
from canonical import load_entity_schema, load_event_schema

def transform_to_event_payload(entity_data: dict, event_type: str):
    # Load entity and event schemas
    entity_name = event_type.split(".")[0]
    entity_schema = load_entity_schema(entity_name, "v1")
    event_schema = load_event_schema(event_type, "v1")
    
    # Get required fields from event schema
    event_required = event_schema.get("required", [])
    
    # Build event payload from entity data
    event_payload = {}
    for field in event_required:
        if field in entity_data:
            event_payload[field] = entity_data[field]
    
    # Add optional fields that exist in entity
    for field in event_schema.get("properties", {}):
        if field in entity_data and field not in event_payload:
            event_payload[field] = entity_data[field]
    
    return event_payload
```

---

## Validation Examples

### Example 1: FastAPI Request Validation

```python
from fastapi import FastAPI, HTTPException
from canonical import load_entity_schema
import jsonschema

app = FastAPI()

@app.post("/clients")
def create_client(client_data: dict):
    # Load schema
    client_schema = load_entity_schema("client", "v1")
    
    # Validate
    try:
        jsonschema.validate(instance=client_data, schema=client_schema)
    except jsonschema.ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Validation failed",
                "message": e.message,
                "path": list(e.path)
            }
        )
    
    # Create client
    # ...
```

### Example 2: Pydantic Integration

```python
from pydantic import BaseModel, validator
from canonical import load_entity_schema
import jsonschema

# Load schema once
client_schema = load_entity_schema("client", "v1")

class Client(BaseModel):
    client_id: str
    tenant_id: str
    name: str
    status: str
    
    @validator('*', pre=True)
    def validate_against_schema(cls, v, values):
        # Validate against canonical schema
        data = {**values, **v} if isinstance(v, dict) else values
        jsonschema.validate(instance=data, schema=client_schema)
        return v
```

### Example 3: Event Validation Middleware

```python
from canonical import load_event_envelope_schema, load_event_schema
import jsonschema

def validate_event_middleware(event_envelope: dict):
    # Validate envelope
    envelope_schema = load_event_envelope_schema()
    jsonschema.validate(instance=event_envelope, schema=envelope_schema)
    
    # Validate payload
    event_type = event_envelope["event_type"]
    event_version = event_envelope["event_version"]
    event_schema = load_event_schema(event_type, event_version)
    jsonschema.validate(instance=event_envelope["payload"], schema=event_schema)
    
    return event_envelope
```

---

## Common Patterns

### Pattern 1: Service Event Handler

```python
from canonical import load_event_schema
import jsonschema

class EventHandler:
    def __init__(self):
        self._event_schemas = {}
    
    def get_event_schema(self, event_type: str, version: str = "v1"):
        cache_key = f"{event_type}.{version}"
        if cache_key not in self._event_schemas:
            self._event_schemas[cache_key] = load_event_schema(event_type, version)
        return self._event_schemas[cache_key]
    
    def handle_event(self, event_payload: dict, event_type: str):
        schema = self.get_event_schema(event_type)
        jsonschema.validate(instance=event_payload, schema=schema)
        
        # Route to specific handler
        handler_name = f"handle_{event_type.replace('.', '_')}"
        handler = getattr(self, handler_name, None)
        if handler:
            handler(event_payload)
```

### Pattern 2: Schema Registry Service

```python
from canonical import (
    load_entity_schema,
    load_event_schema,
    load_event_envelope_schema,
    list_entities,
    list_events
)

class SchemaRegistry:
    """Centralized schema registry for service"""
    
    def __init__(self):
        self._entity_schemas = {}
        self._event_schemas = {}
        self._envelope_schema = None
    
    def get_entity_schema(self, entity: str, version: str = "v1"):
        cache_key = f"{entity}.{version}"
        if cache_key not in self._entity_schemas:
            self._entity_schemas[cache_key] = load_entity_schema(entity, version)
        return self._entity_schemas[cache_key]
    
    def get_event_schema(self, event_type: str, version: str = "v1"):
        cache_key = f"{event_type}.{version}"
        if cache_key not in self._event_schemas:
            self._event_schemas[cache_key] = load_event_schema(event_type, version)
        return self._event_schemas[cache_key]
    
    def get_envelope_schema(self):
        if self._envelope_schema is None:
            self._envelope_schema = load_event_envelope_schema()
        return self._envelope_schema
    
    def list_available_entities(self):
        return list_entities()
    
    def list_available_events(self, domain: str = None):
        return list_events(domain)
```

### Pattern 3: Event Builder

```python
from canonical import load_event_schema, load_event_envelope_schema
import uuid
from datetime import datetime

class EventBuilder:
    """Helper class for building validated events"""
    
    def __init__(self, service_name: str, environment: str = "prod"):
        self.service_name = service_name
        self.environment = environment
        self._envelope_schema = load_event_envelope_schema()
    
    def build_event(
        self,
        event_type: str,
        payload: dict,
        tenant_id: str,
        actor: dict,
        correlation_id: str = None
    ):
        # Load and validate event schema
        event_schema = load_event_schema(event_type, "v1")
        import jsonschema
        jsonschema.validate(instance=payload, schema=event_schema)
        
        # Extract entity info from payload
        entity_type = event_type.split(".")[0]
        entity_id_key = f"{entity_type}_id"
        entity_id = payload.get(entity_id_key)
        
        # Build envelope
        envelope = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "event_version": "v1",
            "source": {
                "service": self.service_name,
                "environment": self.environment
            },
            "tenant_id": tenant_id,
            "entity": {
                "entity_type": entity_type,
                "entity_id": entity_id
            },
            "actor": actor,
            "occurred_at": datetime.utcnow().isoformat() + "Z",
            "payload": payload
        }
        
        # Add correlation ID if provided
        if correlation_id:
            envelope["correlation_id"] = correlation_id
        
        # Validate envelope
        jsonschema.validate(instance=envelope, schema=self._envelope_schema)
        
        return envelope
```

---

## Error Handling

### Handling Schema Not Found

```python
from canonical import load_entity_schema, SchemaNotFoundError

try:
    schema = load_entity_schema("nonexistent", "v1")
except SchemaNotFoundError as e:
    print(f"Schema not found: {e}")
    # Handle gracefully - maybe use default schema or raise HTTP 404
```

### Handling Event Not Found

```python
from canonical import load_event_schema, EventNotFoundError

try:
    schema = load_event_schema("client.invalid", "v1")
except EventNotFoundError as e:
    print(f"Event schema not found: {e}")
    # Handle gracefully - maybe log and skip event
```

### Handling Validation Errors

```python
import jsonschema
from canonical import load_entity_schema

def validate_with_detailed_errors(data: dict, entity: str):
    schema = load_entity_schema(entity, "v1")
    
    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    
    if errors:
        error_details = []
        for error in errors:
            error_details.append({
                "path": list(error.path),
                "message": error.message,
                "validator": error.validator
            })
        return {"valid": False, "errors": error_details}
    
    return {"valid": True}
```

---

## Best Practices

### 1. Cache Schemas at Service Startup

```python
from canonical import load_entity_schema, load_event_schema, list_entities, list_events

class Service:
    def __init__(self):
        # Pre-load commonly used schemas
        self.entity_schemas = {}
        self.event_schemas = {}
        
        # Load all entity schemas
        for entity in list_entities():
            self.entity_schemas[entity] = load_entity_schema(entity, "v1")
        
        # Load all event schemas for your domain
        for event in list_events("client"):  # Replace with your domain
            self.event_schemas[event] = load_event_schema(event, "v1")
```

### 2. Validate Early, Validate Often

```python
# Validate at API boundary
@app.post("/clients")
def create_client(client_data: dict):
    validate_entity(client_data, "client")
    # ...

# Validate before database write
def save_client(client_data: dict):
    validate_entity(client_data, "client")
    # ...

# Validate before event emission
def emit_client_created(client_data: dict):
    validate_event_payload(client_data, "client.created")
    # ...
```

### 3. Use Type Hints with Schema Validation

```python
from typing import TypedDict
from canonical import load_entity_schema

# Load schema once
client_schema = load_entity_schema("client", "v1")

# Create TypedDict from schema (manually or via code generation)
class Client(TypedDict):
    client_id: str
    tenant_id: str
    name: str
    status: str
    # ... other fields
```

### 4. Centralize Schema Access

```python
# schema_registry.py
from canonical import load_entity_schema, load_event_schema

class SchemaRegistry:
    @staticmethod
    def get_entity(entity: str, version: str = "v1"):
        return load_entity_schema(entity, version)
    
    @staticmethod
    def get_event(event_type: str, version: str = "v1"):
        return load_event_schema(event_type, version)

# Use in services
from schema_registry import SchemaRegistry

schema = SchemaRegistry.get_entity("client")
```

### 5. Log Schema Validation Failures

```python
import logging
import jsonschema
from canonical import load_entity_schema

logger = logging.getLogger(__name__)

def validate_entity(data: dict, entity: str):
    schema = load_entity_schema(entity, "v1")
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        logger.error(
            f"Schema validation failed for {entity}",
            extra={
                "entity": entity,
                "error": e.message,
                "path": list(e.path),
                "data": data
            }
        )
        raise
```

---

## Complete Schema Reference

### All Entity Schemas

1. **client** (`client.v1.json`)
   - Core client entity
   - Fields: client_id, tenant_id, name, status, created_at, updated_at, etc.

2. **client_link** (`client_link.v1.json`)
   - Client-to-client relationships
   - Fields: link_id, from_client_id, to_client_id, link_type, status, etc.

3. **document** (`document.v1.json`)
   - Document entity
   - Fields: document_id, tenant_id, document_type, status, access, storage, etc.

4. **interaction** (`interaction.v1.json`)
   - Interaction entity
   - Fields: interaction_id, tenant_id, interaction_type, status, participants, etc.

5. **product** (`product.v1.json`)
   - Product entity
   - Fields: product_id, tenant_id, product_type, status, attributes, etc.

6. **relationship** (`relationship.v1.json`)
   - Relationship entity
   - Fields: relationship_id, tenant_id, primary_client_id, status, health, etc.

7. **riskprofile** (`riskprofile.v1.json`)
   - Risk profile entity
   - Fields: riskprofile_id, tenant_id, client_id, risk_level, assessments, etc.

8. **suitability_assessment** (`suitability_assessment.v1.json`)
   - Suitability assessment entity
   - Fields: assessment_id, tenant_id, relationship_id, suitability_status, etc.

9. **task** (`task.v1.json`)
   - Task entity
   - Fields: task_id, tenant_id, task_type, status, priority, assignee, scope, etc.

### All Event Schemas by Domain

#### Client Domain (7 events)
- `client.created`, `client.updated`, `client.status_changed`
- `client_link.created`, `client_link.updated`, `client_link.terminated`

#### Document Domain (7 events)
- `document.ingested`, `document.updated`, `document.status_changed`
- `document.access_changed`, `document.linked`, `document.version_added`, `document.superseded`

#### Interaction Domain (11 events)
- `interaction.created`, `interaction.initiated`, `interaction.completed`, `interaction.finalized`
- `interaction.status_changed`, `interaction.review_started`, `interaction.cancelled`
- `interaction.superseded`, `interaction.documents_attached`
- `document.linked` (interaction-specific)

#### Product Domain (5 events)
- `product.created`, `product.updated`, `product.deactivated`
- `product.status_changed`, `product.artefact.linked`

#### Relationship Domain (6 events)
- `relationship.created`, `relationship.status_changed`, `relationship.health_updated`
- `relationship.preferences_updated`, `relationship.at_risk`, `relationship.terminated`

#### Risk Profile Domain (6 events)
- `riskprofile.created`, `riskprofile.updated`, `riskprofile.activated`, `riskprofile.superseded`
- `suitability.assessed`, `suitability.breached`

#### Task Domain (7 events)
- `task.created`, `task.completed`, `task.status_changed`, `task.expired`
- `document.uploaded`, `interaction.finalized`, `riskprofile.changed`

**Total: 50+ event schemas**

---

## Integration with Services

### Example: CDS Client Service

```python
from canonical import load_entity_schema, load_event_schema, load_event_envelope_schema
import jsonschema

class ClientService:
    def __init__(self):
        self.client_schema = load_entity_schema("client", "v1")
        self.client_created_schema = load_event_schema("client.created", "v1")
        self.envelope_schema = load_event_envelope_schema()
    
    def create_client(self, client_data: dict, actor: dict):
        # Validate entity
        jsonschema.validate(instance=client_data, schema=self.client_schema)
        
        # Save to database
        # ...
        
        # Emit event
        event = self._build_event("client.created", client_data, actor)
        self._publish_event(event)
    
    def _build_event(self, event_type: str, payload: dict, actor: dict):
        # Build and validate event envelope
        # ...
```

### Example: Task Service Event Handler

```python
from canonical import load_event_schema
import jsonschema

class TaskEventHandler:
    def handle_document_uploaded(self, event_payload: dict):
        schema = load_event_schema("document.uploaded", "v1")
        jsonschema.validate(instance=event_payload, schema=schema)
        
        # Create task based on document upload
        # ...
    
    def handle_interaction_finalized(self, event_payload: dict):
        schema = load_event_schema("interaction.finalized", "v1")
        jsonschema.validate(instance=event_payload, schema=schema)
        
        # Create task based on interaction
        # ...
```

---

## Cursor Instructions for Services

When building services that use the canonical library:

1. **Always validate at boundaries**: Validate entity data when receiving from API, before database writes, and before event emission.

2. **Use event envelope**: Always wrap events in the standard event envelope when publishing.

3. **Validate event payloads**: When consuming events, validate both the envelope and the payload.

4. **Cache schemas**: Pre-load commonly used schemas at service startup for performance.

5. **Handle errors gracefully**: Catch `SchemaNotFoundError` and `EventNotFoundError` and handle appropriately.

6. **Use semantic constraints**: When available, apply semantic constraints in addition to JSON Schema validation.

7. **Discover schemas**: Use `list_entities()` and `list_events()` to discover available schemas dynamically.

8. **Version awareness**: Always specify version when loading schemas (default is "v1").

---

## Summary

The Canonical Schema Library provides:

- ✅ **9 Entity Schemas** for core business entities
- ✅ **50+ Event Schemas** organized by domain
- ✅ **Event Envelope Schema** for standard event wrapping
- ✅ **Semantic Constraints** for additional validation
- ✅ **In-memory Caching** for performance
- ✅ **Schema Discovery** functions for dynamic usage
- ✅ **Type-safe Validation** via JSON Schema

Use this library in all RM Brain services to ensure consistency, type safety, and maintainability.
