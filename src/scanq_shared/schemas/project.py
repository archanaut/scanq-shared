"""Project contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .environment import EnvironmentResponse


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    owner_id: str = Field(..., min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    metadata: dict[str, str] | None = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    owner_id: str
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProjectEnvironmentResponse(BaseModel):
    project: ProjectResponse
    environments: list[EnvironmentResponse] = Field(default_factory=list)
    total_environments: int = Field(default=0, ge=0)

