"""Lineage tracking schemas for audit trails and cross-system integration."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from ..enums import LineageEventType


class LineageRegisterRequest(BaseModel):
    """Request to register a new lineage record for an accreditation run."""

    run_id: str = Field(
        ...,
        description="Unique identifier for this accreditation run",
        examples=["run-dwelling-101-2026-06-15"],
    )
    dwelling_id: str = Field(
        ...,
        description="Dwelling ID being tested",
        examples=["dwelling-nathrs-uip-101"],
    )
    pack_version: str = Field(
        ...,
        description="Version of accreditation test pack",
        examples=["v1.0.0"],
    )
    initiated_by: str = Field(
        ...,
        description="User or service ID that initiated the run",
        examples=["ci-pipeline", "user@example.com"],
    )
    environment: str = Field(
        ...,
        description="Environment where run is occurring",
        examples=["staging", "production"],
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context (Git commit, CI job ID, etc.)",
    )


class LineageRegisterResponse(BaseModel):
    """Response confirming lineage record creation."""

    lineage_id: str = Field(..., description="Assigned lineage record ID")
    run_id: str = Field(..., description="The run ID from the request")
    status: LineageEventType = Field(
        default=LineageEventType.REGISTERED,
        description="Event type recorded",
    )
    registered_at: datetime = Field(
        ..., description="Timestamp when lineage was registered"
    )
    request_id: str | None = Field(
        default=None, description="Unique identifier for request tracing"
    )


class LineageFinalizeRequest(BaseModel):
    """Request to finalize a lineage record after accreditation completes."""

    lineage_id: str = Field(
        ...,
        description="The lineage_id from registration response",
        examples=["lin-uuid-abc123"],
    )
    status: LineageEventType = Field(
        ...,
        description="Final status of the run",
    )
    summary: str | None = Field(
        default=None,
        description="Human-readable summary of results",
    )
    metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Metrics/results (pass/fail counts, evidence generated, etc.)",
    )


class LineageFinalizeResponse(BaseModel):
    """Response confirming lineage finalization."""

    lineage_id: str = Field(..., description="The lineage record ID")
    status: LineageEventType = Field(
        ..., description="Final recorded status"
    )
    finalized_at: datetime = Field(
        ..., description="Timestamp when lineage was finalized"
    )
    request_id: str | None = Field(
        default=None, description="Unique identifier for request tracing"
    )
