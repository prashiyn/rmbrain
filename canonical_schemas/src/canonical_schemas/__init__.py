"""Canonical schemas package for shared Python schema definitions.

This package provides Python implementations of canonical schemas that are
shared across all services. These schemas correspond to the JSON schemas
defined in the `canonical/` directory.
"""

from canonical_schemas.actor import (
    Actor,
    ActorRole,
    ActorType,
    ACTOR_ROLES_BY_TYPE,
    validate_actor_role_type,
)

__version__ = "1.0.0"

__all__ = [
    "Actor",
    "ActorRole",
    "ActorType",
    "ACTOR_ROLES_BY_TYPE",
    "validate_actor_role_type",
]
