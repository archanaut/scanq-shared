"""Environment contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EnvironmentCreateRequest(BaseModel):
    project_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=100)
    config: dict[str, Any] = Field(default_factory=dict)


class EnvironmentResponse(BaseModel):
    id: str
    project_id: str
    name: str
    config: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

