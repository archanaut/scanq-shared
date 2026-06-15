"""Common base models and data types used across scanq-shared."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BaseResponse(BaseModel):
    """Base model for all API responses with common metadata."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "resolved",
                "timestamp": "2026-06-15T10:30:00Z",
            }
        }
    )

    status: str = Field(
        ...,
        description="Status of the response (resolved, partial, error, etc.)",
        examples=["resolved", "partial", "not_found"],
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when response was generated (UTC)",
    )
    request_id: str | None = Field(
        default=None,
        description="Unique identifier for request tracing",
    )


class ErrorDetail(BaseModel):
    """Standard error response structure."""

    code: str = Field(
        ...,
        description="Machine-readable error code",
        examples=["invalid_request", "not_found", "internal_error"],
    )
    message: str = Field(
        ...,
        description="Human-readable error message",
    )
    details: dict[str, Any] | None = Field(
        default=None,
        description="Additional error context (field-specific errors, etc.)",
    )


class ErrorResponse(BaseResponse):
    """Standard error response with error details."""

    status: str = "error"
    error: ErrorDetail = Field(..., description="Error details")


class PaginationParams(BaseModel):
    """Standard pagination parameters for list endpoints."""

    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""

    total: int = Field(..., description="Total number of items")
    limit: int = Field(..., description="Limit parameter used")
    offset: int = Field(..., description="Offset parameter used")
    items: list[Any] = Field(default=[], description="Items in this page")
