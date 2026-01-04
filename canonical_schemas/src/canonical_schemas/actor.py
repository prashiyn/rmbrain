"""Canonical Actor Schema Definitions.

This module provides the canonical actor schema definitions used across all services.
These definitions align with the canonical actor taxonomy documented in
relationship_service/docs/relationship_service.md.

Actor Types:
- human_internal: Internal human actors (RMs, specialists, etc.)
- human_external: External human actors (clients, prospects, etc.)
- system: System actors (automated processes)
- service: Service actors (microservices, workflows)

Actor Roles (by type):
- Human Internal: rm, relationship_manager, investment_specialist, product_manager,
                  portfolio_manager, risk_manager, compliance_officer, service_rm
- Human External: client, prospect, external_advisor
- System/Service: system, scheduler, workflow_engine, cds_relationship
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ActorType(str, Enum):
    """Canonical actor type enum.
    
    Matches the actor_type enum values defined in canonical JSON schemas.
    All services should use these exact values for consistency.
    """
    
    HUMAN_INTERNAL = "human_internal"
    HUMAN_EXTERNAL = "human_external"
    SYSTEM = "system"
    SERVICE = "service"


class ActorRole(str, Enum):
    """Canonical actor role enum.
    
    These roles are documented in relationship_service/docs/relationship_service.md
    (lines 42-62). All services should use these exact role values.
    
    Note: Actor roles are distinct from permissions. Permissions are enforced
    by the Policy Engine.
    """
    
    # Human Internal Roles
    RM = "rm"
    RELATIONSHIP_MANAGER = "relationship_manager"
    INVESTMENT_SPECIALIST = "investment_specialist"
    PRODUCT_MANAGER = "product_manager"
    PORTFOLIO_MANAGER = "portfolio_manager"
    RISK_MANAGER = "risk_manager"
    COMPLIANCE_OFFICER = "compliance_officer"
    SERVICE_RM = "service_rm"
    
    # Human External Roles
    CLIENT = "client"
    PROSPECT = "prospect"
    EXTERNAL_ADVISOR = "external_advisor"
    
    # System/Service Roles
    SYSTEM = "system"
    SCHEDULER = "scheduler"
    WORKFLOW_ENGINE = "workflow_engine"
    CDS_RELATIONSHIP = "cds_relationship"


class Actor(BaseModel):
    """Canonical Actor schema.
    
    This is the standard actor representation used across all services.
    All actor definitions should conform to this schema for consistency.
    
    Attributes:
        actor_id: Unique identifier for the actor
        actor_role: Role of the actor (from ActorRole enum)
        actor_type: Type of the actor (from ActorType enum)
        display_name: Optional human-readable display name
    
    Example:
        >>> actor = Actor(
        ...     actor_id="rm_123",
        ...     actor_role=ActorRole.RM,
        ...     actor_type=ActorType.HUMAN_INTERNAL,
        ...     display_name="John Doe"
        ... )
    """
    
    actor_id: str = Field(
        ...,
        description="Unique identifier for the actor"
    )
    actor_role: ActorRole = Field(
        ...,
        description="Role of the actor from canonical actor taxonomy"
    )
    actor_type: ActorType = Field(
        ...,
        description="Type of the actor (human_internal, human_external, system, service)"
    )
    display_name: Optional[str] = Field(
        None,
        description="Optional human-readable display name for the actor"
    )
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "actor_id": "rm_123",
                "actor_role": "rm",
                "actor_type": "human_internal",
                "display_name": "John Doe"
            }
        }


# Convenience mappings for role validation by type
ACTOR_ROLES_BY_TYPE = {
    ActorType.HUMAN_INTERNAL: [
        ActorRole.RM,
        ActorRole.RELATIONSHIP_MANAGER,
        ActorRole.INVESTMENT_SPECIALIST,
        ActorRole.PRODUCT_MANAGER,
        ActorRole.PORTFOLIO_MANAGER,
        ActorRole.RISK_MANAGER,
        ActorRole.COMPLIANCE_OFFICER,
        ActorRole.SERVICE_RM,
    ],
    ActorType.HUMAN_EXTERNAL: [
        ActorRole.CLIENT,
        ActorRole.PROSPECT,
        ActorRole.EXTERNAL_ADVISOR,
    ],
    ActorType.SYSTEM: [
        ActorRole.SYSTEM,
        ActorRole.SCHEDULER,
        ActorRole.WORKFLOW_ENGINE,
    ],
    ActorType.SERVICE: [
        ActorRole.CDS_RELATIONSHIP,
    ],
}


def validate_actor_role_type(actor_role: ActorRole, actor_type: ActorType) -> bool:
    """Validate that an actor role is valid for the given actor type.
    
    Args:
        actor_role: The actor role to validate
        actor_type: The actor type to validate against
        
    Returns:
        True if the role is valid for the type, False otherwise
        
    Example:
        >>> validate_actor_role_type(ActorRole.RM, ActorType.HUMAN_INTERNAL)
        True
        >>> validate_actor_role_type(ActorRole.CLIENT, ActorType.HUMAN_INTERNAL)
        False
    """
    valid_roles = ACTOR_ROLES_BY_TYPE.get(actor_type, [])
    return actor_role in valid_roles
