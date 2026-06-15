"""Job/provider contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from ..enums import ExecutionStatus
from .errors import ErrorSchema


class JobResponse(BaseModel):
    id: str
    project_id: str
    environment_id: str
    status: ExecutionStatus
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: ErrorSchema | None = None


class ProviderProfile(BaseModel):
    provider_id: str = Field(..., min_length=1)
    name: str
    capabilities: list[str] = Field(default_factory=list)
    active: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class CostEstimate(BaseModel):
    job_id: str
    provider_id: str
    estimated_cost: float = Field(..., ge=0)
    currency: str = "AUD"
    valid_until: datetime | None = None

