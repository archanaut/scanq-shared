"""Training-studio specific data models.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ProjectModel(BaseModel):
    """Represents a project in training-studio."""

    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Human-readable project name")
    description: str | None = Field(default=None, description="Project description")
    owner_id: str = Field(..., description="User ID of project owner")
    created_at: datetime = Field(..., description="Project creation timestamp")
    updated_at: datetime = Field(..., description="Project last update timestamp")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional project metadata"
    )


class EnvironmentModel(BaseModel):
    """Represents an environment within a project."""

    id: str = Field(..., description="Unique environment identifier")
    project_id: str = Field(..., description="Parent project ID")
    name: str = Field(..., description="Environment name (e.g., staging, production)")
    config: dict[str, Any] = Field(
        default_factory=dict, description="Environment configuration"
    )
    created_at: datetime = Field(..., description="Environment creation timestamp")


class ActorModel(BaseModel):
    """Represents an actor (user or service) in the system."""

    id: str = Field(..., description="Unique actor identifier")
    project_id: str = Field(..., description="Project this actor belongs to")
    type: str = Field(..., description="Actor type (user, service, bot, etc.)")
    name: str = Field(..., description="Actor display name")
    email: str | None = Field(default=None, description="Actor email address")
    active: bool = Field(default=True, description="Whether actor is active")
    created_at: datetime = Field(..., description="Actor creation timestamp")
