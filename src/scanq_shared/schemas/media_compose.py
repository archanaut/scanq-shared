"""Media compose request and response schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from ..enums import MediaComposeStatus, MediaType


class MediaComposeRequest(BaseModel):
    """Request to compose media artifacts into a derived output."""

    source_media_refs: list[str] = Field(
        ...,
        min_length=1,
        description="Ordered list of source media identifiers",
    )
    compose_type: MediaType = Field(..., description="Requested compose type")
    output_format: str = Field(
        ...,
        description="Output format for the composed artifact",
        examples=["pdf", "png"],
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Compose-specific parameters",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Caller-supplied context and tracing metadata",
    )


class MediaComposeResponse(BaseModel):
    """Response describing a media-compose job outcome."""

    compose_id: str = Field(..., description="Assigned compose job identifier")
    status: MediaComposeStatus | str = Field(
        ...,
        description="Compose job status; unknown values are preserved for forward compatibility",
    )
    output_media_ref: str | None = Field(
        default=None,
        description="Output media reference when the compose job completes",
    )
    composed_at: datetime | None = Field(
        default=None,
        description="Timestamp when the compose job completed",
    )
    partial_items: list[str] = Field(
        default_factory=list,
        description="Identifiers confirmed for partial responses",
    )
    request_id: str | None = Field(
        default=None,
        description="Unique identifier for request tracing",
    )
