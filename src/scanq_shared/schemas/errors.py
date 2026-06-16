"""Error schema definitions for consistent error handling.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.
"""

from typing import Any

from pydantic import BaseModel, Field

from ..enums import ErrorCode


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


class ErrorResponse(BaseModel):
    """Canonical error envelope returned by all Phase 1 operations.

    Used as the common ``ErrorResponse`` contract referenced in the
    fixed Phase 1 endpoint inventory.  Unknown/unexpected errors must
    also be mapped to this envelope with ``code="unknown_error"`` and
    the original diagnostic information preserved in ``details``.
    """

    error: ErrorSchema = Field(..., description="Error details")
    request_id: str | None = Field(
        default=None,
        description="Unique identifier for request tracing (top-level convenience copy)",
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ErrorResponse":
        """Construct an ErrorResponse from a raw API response dict.

        Falls back to an ``unknown_error`` envelope if the payload does
        not match the expected structure, preserving the raw data in
        ``details`` for diagnostics.
        """
        try:
            return cls(**data)
        except Exception:
            return cls(
                error=ErrorSchema(
                    code="unknown_error",
                    message="An unexpected error response was received.",
                    status_code=data.get("status_code", 500),
                    details={"raw": data},
                ),
            )


class ErrorEnvelope(BaseModel):
    """Standardized error envelope used by typed clients."""

    code: ErrorCode = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    detail: Any | None = Field(
        default=None,
        description="Optional structured error payload",
    )
    correlation_id: str | None = Field(
        default=None,
        description="Optional correlation identifier",
    )
