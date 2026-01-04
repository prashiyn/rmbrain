"""Registry for canonical Python schemas.

This module provides a registry pattern for accessing canonical schemas.
Currently focused on actor schemas, but can be extended for other schema types.
"""

from typing import Type, get_type_hints
from canonical_schemas.actor import Actor, ActorRole, ActorType


# Registry of available schema classes
_SCHEMA_REGISTRY: dict[str, Type] = {
    "Actor": Actor,
    "ActorRole": ActorRole,
    "ActorType": ActorType,
}


def get_schema_class(schema_name: str) -> Type:
    """
    Get a schema class by name from the registry.
    
    Args:
        schema_name: Name of the schema class (e.g., "Actor", "ActorRole")
        
    Returns:
        Schema class
        
    Raises:
        KeyError: If schema class not found in registry
    """
    if schema_name not in _SCHEMA_REGISTRY:
        available = ", ".join(_SCHEMA_REGISTRY.keys())
        raise KeyError(
            f"Schema class '{schema_name}' not found in registry. "
            f"Available schemas: {available}"
        )
    return _SCHEMA_REGISTRY[schema_name]


def list_schemas() -> list[str]:
    """
    List all available schema classes in the registry.
    
    Returns:
        List of schema class names
    """
    return sorted(_SCHEMA_REGISTRY.keys())


def register_schema(schema_name: str, schema_class: Type) -> None:
    """
    Register a new schema class in the registry.
    
    Args:
        schema_name: Name to register the schema under
        schema_class: The schema class to register
        
    Example:
        >>> from canonical_schemas.registry import register_schema
        >>> register_schema("MySchema", MySchemaClass)
    """
    _SCHEMA_REGISTRY[schema_name] = schema_class


__all__ = [
    "get_schema_class",
    "list_schemas",
    "register_schema",
]
