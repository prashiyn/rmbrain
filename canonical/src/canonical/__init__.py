"""Canonical schema library for RM Brain.

This library provides access to canonical entity schemas, event schemas,
and semantic constraints used across all services.
"""

from canonical.registry import (
    load_entity_schema,
    load_event_schema,
    load_event_envelope_schema,
    load_semantic_constraints,
    list_entities,
    list_entity_versions,
    list_events,
    list_event_versions,
    get_event_schema_path,
    SchemaNotFoundError,
    EventNotFoundError,
    SemanticNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    "load_entity_schema",
    "load_event_schema",
    "load_event_envelope_schema",
    "load_semantic_constraints",
    "list_entities",
    "list_entity_versions",
    "list_events",
    "list_event_versions",
    "get_event_schema_path",
    "SchemaNotFoundError",
    "EventNotFoundError",
    "SemanticNotFoundError",
]
