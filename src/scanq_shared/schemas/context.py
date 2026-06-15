"""Context resolution schemas for training-studio support endpoints."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from ..enums import ContextStatus


class ContextResolveRequest(BaseModel):
    """Request to resolve project, environment, and actor context."""

    project_id: str = Field(
        ...,
        description="Project identifier to resolve",
        examples=["proj-archanaut-001"],
    )
    environment_id: str = Field(
        ...,
        description="Environment identifier to resolve",
        examples=["env-staging"],
    )
    actor_id: str | None = Field(
        default=None,
        description="Actor identifier to resolve (optional)",
        examples=["actor-service-accreditation"],
    )
    include_metadata: bool = Field(
        default=False,
        description="Include full metadata objects vs. IDs only",
    )


class ContextResolveResponse(BaseModel):
    """Response from context resolution with resolved entities."""

    status: ContextStatus = Field(
        ...,
        description="Status of context resolution (resolved, partial, not_found)",
    )
    project_id: str = Field(..., description="Resolved project ID")
    project_name: str | None = Field(
        default=None, description="Project name (if include_metadata=true)"
    )
    environment_id: str = Field(..., description="Resolved environment ID")
    environment_name: str | None = Field(
        default=None, description="Environment name (if include_metadata=true)"
    )
    actor_id: str | None = Field(
        default=None, description="Resolved actor ID (if provided in request)"
    )
    actor_name: str | None = Field(
        default=None, description="Actor name (if include_metadata=true)"
    )
    resolved_at: datetime = Field(
        ..., description="Timestamp when context was resolved"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context metadata (if include_metadata=true)",
    )
    request_id: str | None = Field(
        default=None, description="Unique identifier for request tracing"
    )
