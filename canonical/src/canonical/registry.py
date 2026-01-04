"""Registry for canonical schemas, events, and semantic constraints."""

import json
import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# Base directory for canonical schemas
# Data directories are now in the package directory (src/canonical/)
_BASE_DIR = Path(__file__).parent
_ENTITIES_DIR = _BASE_DIR / "entities"
_EVENTS_DIR = _BASE_DIR / "events"
_SEMANTICS_DIR = _BASE_DIR / "semantics"


class SchemaNotFoundError(Exception):
    """Raised when a schema file is not found."""

    pass


class EventNotFoundError(Exception):
    """Raised when an event schema file is not found."""

    pass


class SemanticNotFoundError(Exception):
    """Raised when a semantic constraint file is not found."""

    pass


# Cache for loaded schemas
_entity_schemas: dict[str, dict[str, Any]] = {}
_event_schemas: dict[str, dict[str, Any]] = {}
_semantic_constraints: dict[str, dict[str, Any]] = {}
_envelope_schema: dict[str, Any] | None = None


def load_entity_schema(entity: str, version: str = "v1") -> dict[str, Any]:
    """
    Load canonical JSON schema for an entity.

    Args:
        entity: Entity name (e.g., "client", "task", "document")
        version: Schema version (default: "v1")

    Returns:
        JSON Schema definition as a dictionary

    Raises:
        SchemaNotFoundError: If schema file not found
    """
    cache_key = f"{entity}.{version}"

    if cache_key in _entity_schemas:
        return _entity_schemas[cache_key]

    schema_file = _ENTITIES_DIR / f"{entity}.{version}.json"

    if not schema_file.exists():
        raise SchemaNotFoundError(
            f"Canonical entity schema not found: {schema_file}. "
            f"Available entities: {', '.join(list_entities())}"
        )

    try:
        with open(schema_file, "r") as f:
            schema = json.load(f)

        _entity_schemas[cache_key] = schema
        logger.debug(f"Loaded canonical entity schema: {cache_key}")
        return schema
    except json.JSONDecodeError as e:
        raise SchemaNotFoundError(
            f"Invalid JSON in schema file {schema_file}: {str(e)}"
        ) from e
    except Exception as e:
        raise SchemaNotFoundError(
            f"Failed to load canonical entity schema {cache_key}: {str(e)}"
        ) from e


def load_event_envelope_schema() -> dict[str, Any]:
    """
    Load the canonical event envelope schema.

    Returns:
        Event envelope JSON schema definition

    Raises:
        SchemaNotFoundError: If envelope schema file not found
    """
    global _envelope_schema

    if _envelope_schema is not None:
        return _envelope_schema

    envelope_file = _EVENTS_DIR / "event_envelope.v1.json"

    if not envelope_file.exists():
        raise SchemaNotFoundError(
            f"Canonical event envelope schema not found: {envelope_file}"
        )

    try:
        with open(envelope_file, "r") as f:
            _envelope_schema = json.load(f)

        logger.debug("Loaded canonical event envelope schema")
        return _envelope_schema
    except json.JSONDecodeError as e:
        raise SchemaNotFoundError(
            f"Invalid JSON in envelope schema file {envelope_file}: {str(e)}"
        ) from e
    except Exception as e:
        raise SchemaNotFoundError(
            f"Failed to load canonical event envelope schema: {str(e)}"
        ) from e


def load_event_schema(event_type: str, version: str = "v1") -> dict[str, Any]:
    """
    Load canonical JSON schema for an event.

    Args:
        event_type: Event type (e.g., "client.created", "task.completed")
        version: Schema version (default: "v1")

    Returns:
        Event JSON schema definition as a dictionary

    Raises:
        EventNotFoundError: If event schema file not found
    """
    cache_key = f"{event_type}.{version}"

    if cache_key in _event_schemas:
        return _event_schemas[cache_key]

    # Event schemas are organized by domain (e.g., client/, task/, etc.)
    # event_type format: "domain.event_name" (e.g., "client.created")
    parts = event_type.split(".", 1)
    if len(parts) != 2:
        raise EventNotFoundError(
            f"Invalid event type format: {event_type}. "
            "Expected format: 'domain.event_name' (e.g., 'client.created')"
        )

    domain, event_name = parts
    event_file = _EVENTS_DIR / domain / f"{event_type}.{version}.json"

    if not event_file.exists():
        # Try alternative location (some events might be in root)
        event_file = _EVENTS_DIR / f"{event_type}.{version}.json"
        if not event_file.exists():
            raise EventNotFoundError(
                f"Canonical event schema not found: {event_type}.{version}. "
                f"Checked: {_EVENTS_DIR / domain} and {_EVENTS_DIR}"
            )

    try:
        with open(event_file, "r") as f:
            schema = json.load(f)

        _event_schemas[cache_key] = schema
        logger.debug(f"Loaded canonical event schema: {cache_key}")
        return schema
    except json.JSONDecodeError as e:
        raise EventNotFoundError(
            f"Invalid JSON in event schema file {event_file}: {str(e)}"
        ) from e
    except Exception as e:
        raise EventNotFoundError(
            f"Failed to load canonical event schema {cache_key}: {str(e)}"
        ) from e


def load_semantic_constraints(
    entity: str, version: str = "v1"
) -> dict[str, Any]:
    """
    Load semantic constraints for an entity.

    Args:
        entity: Entity name (e.g., "client")
        version: Schema version (default: "v1")

    Returns:
        Semantic constraint definition as a dictionary.
        Returns empty constraints if file not found (semantics are optional).

    Raises:
        SemanticNotFoundError: If semantic file exists but cannot be loaded
    """
    cache_key = f"{entity}.{version}"

    if cache_key in _semantic_constraints:
        return _semantic_constraints[cache_key]

    semantic_file = _SEMANTICS_DIR / f"{entity}.{version}.semantic.yaml"

    if not semantic_file.exists():
        # Semantic constraints are optional - return empty constraints
        logger.debug(
            f"Semantic constraints not found: {semantic_file}, using empty constraints"
        )
        return {
            "entity": entity,
            "version": version,
            "required_fields": [],
            "semantic_constraints": {},
            "cross_field_constraints": [],
        }

    try:
        with open(semantic_file, "r") as f:
            constraints = yaml.safe_load(f)

        _semantic_constraints[cache_key] = constraints
        logger.debug(f"Loaded semantic constraints: {cache_key}")
        return constraints
    except yaml.YAMLError as e:
        raise SemanticNotFoundError(
            f"Invalid YAML in semantic constraints file {semantic_file}: {str(e)}"
        ) from e
    except Exception as e:
        raise SemanticNotFoundError(
            f"Failed to load semantic constraints {cache_key}: {str(e)}"
        ) from e


def list_entities() -> list[str]:
    """
    List all available canonical entities.

    Returns:
        Sorted list of entity names
    """
    entities = set()
    for schema_file in _ENTITIES_DIR.glob("*.json"):
        # Extract entity from filename: entity.version.json
        parts = schema_file.stem.split(".")
        if len(parts) >= 2:
            entities.add(parts[0])
    return sorted(entities)


def list_entity_versions(entity: str) -> list[str]:
    """
    List all available versions for an entity.

    Args:
        entity: Entity name

    Returns:
        Sorted list of version strings
    """
    versions = []
    for schema_file in _ENTITIES_DIR.glob(f"{entity}.*.json"):
        # Extract version from filename: entity.version.json
        parts = schema_file.stem.split(".")
        if len(parts) >= 2:
            versions.append(parts[1])
    return sorted(versions)


def list_events(domain: str | None = None) -> list[str]:
    """
    List all available events for a domain, or all events if domain is None.

    Args:
        domain: Domain name (e.g., "client", "task"). If None, lists all events.

    Returns:
        Sorted list of event types (e.g., ["client.created", "client.updated"])
    """
    events = set()

    if domain:
        domain_dir = _EVENTS_DIR / domain
        if domain_dir.exists():
            for event_file in domain_dir.glob("*.json"):
                # Extract event type from filename: event_type.version.json
                parts = event_file.stem.split(".")
                if len(parts) >= 2:
                    # Reconstruct event type: domain.event_name
                    event_name = ".".join(parts[:-1])  # Remove version
                    events.add(event_name)
    else:
        # List all events from all domains
        for domain_dir in _EVENTS_DIR.iterdir():
            if domain_dir.is_dir():
                for event_file in domain_dir.glob("*.json"):
                    parts = event_file.stem.split(".")
                    if len(parts) >= 2:
                        event_name = ".".join(parts[:-1])
                        events.add(event_name)

    return sorted(events)


def list_event_versions(event_type: str) -> list[str]:
    """
    List all available versions for an event.

    Args:
        event_type: Event type (e.g., "client.created")

    Returns:
        Sorted list of version strings
    """
    versions = []
    parts = event_type.split(".", 1)
    if len(parts) == 2:
        domain, event_name = parts
        event_dir = _EVENTS_DIR / domain
        if event_dir.exists():
            pattern = f"{event_type}.*.json"
            for event_file in event_dir.glob(pattern):
                parts = event_file.stem.split(".")
                if len(parts) >= 2:
                    versions.append(parts[-1])  # Last part is version
    return sorted(versions)


def get_event_schema_path(event_type: str, version: str = "v1") -> Path:
    """
    Get the file path for an event schema (for testing/debugging).

    Args:
        event_type: Event type (e.g., "client.created")
        version: Schema version (default: "v1")

    Returns:
        Path object to the event schema file

    Raises:
        EventNotFoundError: If event schema file not found
    """
    parts = event_type.split(".", 1)
    if len(parts) != 2:
        raise EventNotFoundError(
            f"Invalid event type format: {event_type}. "
            "Expected format: 'domain.event_name'"
        )

    domain, event_name = parts
    event_file = _EVENTS_DIR / domain / f"{event_type}.{version}.json"

    if not event_file.exists():
        event_file = _EVENTS_DIR / f"{event_type}.{version}.json"
        if not event_file.exists():
            raise EventNotFoundError(
                f"Event schema file not found: {event_type}.{version}"
            )

    return event_file
