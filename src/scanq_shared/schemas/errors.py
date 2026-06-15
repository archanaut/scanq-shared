"""Error schema definitions for consistent error handling."""

from typing import Any

from pydantic import BaseModel, Field


class ErrorSchema(BaseModel):
    """Standard error response schema."""

    code: str = Field(
        ...,
        description="Machine-readable error code",
        examples=[
            "invalid_request",
            "not_found",
            "unauthorized",
            "internal_error",
        ],
    )
    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Project not found", "Insufficient permissions"],
    )
    status_code: int = Field(
        ...,
        description="HTTP status code",
        ge=400,
        le=599,
    )
    details: dict[str, Any] | None = Field(
        default=None,
        description="Additional error context (field errors, nested details)",
    )
    request_id: str | None = Field(
        default=None,
        description="Unique identifier for request tracing",
    )
