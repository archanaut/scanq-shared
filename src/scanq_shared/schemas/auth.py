"""Authentication token schemas for training-studio support endpoints."""

from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from ..enums import TokenStatus


class ServiceTokenRequest(BaseModel):
    """Request to issue a service-to-service authentication token."""

    service_id: str = Field(
        ...,
        description="ID of requesting service",
        examples=["scanq-accreditation"],
    )
    scopes: list[str] = Field(
        default_factory=lambda: ["read:context", "write:lineage"],
        description="Requested access scopes",
    )
    ttl_seconds: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Token time-to-live in seconds (1 min - 24 hrs)",
    )
    metadata: dict[str, str] | None = Field(
        default=None,
        description="Additional metadata (correlation IDs, etc.)",
    )


class ServiceTokenResponse(BaseModel):
    """Response containing a short-lived service token."""

    status: TokenStatus = Field(..., description="Token status")
    token: str = Field(..., description="The authentication token (bearer token)")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_at: datetime = Field(
        ..., description="Timestamp when token expires (UTC)"
    )
    scopes: list[str] = Field(
        ..., description="Scopes granted to this token"
    )
    issued_at: datetime = Field(..., description="Timestamp when token was issued")
    request_id: str | None = Field(
        default=None, description="Unique identifier for request tracing"
    )

    @property
    def expires_in(self) -> int:
        """Returns seconds until token expiration."""
        delta = self.expires_at - datetime.utcnow()
        return max(0, int(delta.total_seconds()))
