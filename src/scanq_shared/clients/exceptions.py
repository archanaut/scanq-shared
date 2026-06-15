"""Client exceptions.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from scanq_shared.schemas.errors import ErrorResponse


class ClientError(Exception):
    """Base exception for scanq-shared client errors."""

    def __init__(self, message: str, code: str | None = None) -> None:
        """Initialize ClientError.

        Args:
            message: Human-readable error message
            code: Machine-readable error code
        """
        super().__init__(message)
        self.message = message
        self.code = code or "client_error"


class ConnectionError(ClientError):
    """Raised when unable to connect to the service."""

    def __init__(self, url: str, reason: str) -> None:
        """Initialize ConnectionError.

        Args:
            url: The service URL that failed to connect
            reason: Reason for connection failure
        """
        super().__init__(
            f"Failed to connect to {url}: {reason}",
            code="connection_error",
        )
        self.url = url


class TimeoutError(ClientError):
    """Raised when request times out."""

    def __init__(self, operation: str, timeout_seconds: int) -> None:
        """Initialize TimeoutError.

        Args:
            operation: The operation that timed out
            timeout_seconds: The timeout threshold
        """
        super().__init__(
            f"{operation} timed out after {timeout_seconds}s",
            code="timeout",
        )
        self.operation = operation
        self.timeout_seconds = timeout_seconds


class AuthenticationError(ClientError):
    """Raised for authentication/authorization failures."""

    def __init__(self, reason: str = "Authentication failed") -> None:
        """Initialize AuthenticationError.

        Args:
            reason: Specific reason for auth failure
        """
        super().__init__(reason, code="authentication_error")


class ValidationError(ClientError):
    """Raised for request/response validation failures."""

    def __init__(self, message: str, details: list[Any] | dict[str, Any] | None = None) -> None:
        """Initialize ValidationError.

        Args:
            message: Error message
            details: Additional validation error details (list of Pydantic error
                dicts, or a plain dict for other cases).
        """
        super().__init__(message, code="validation_error")
        self.details: list[Any] | dict[str, Any] = details if details is not None else {}


class APIError(ClientError):
    """Raised for API-level errors (4xx, 5xx responses).

    Aligned with the shared ``ErrorResponse`` envelope so callers can
    inspect ``status_code``, ``code``, and ``details`` without parsing
    the raw HTTP response themselves.
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: dict[str, Any] | None = None,
        request_id: str | None = None,
    ) -> None:
        """Initialize APIError.

        Args:
            status_code: HTTP status code
            code: API error code (from ErrorSchema.code)
            message: Error message (from ErrorSchema.message)
            details: Additional error details (from ErrorSchema.details)
            request_id: Request tracing ID (from ErrorResponse.request_id)
        """
        super().__init__(message, code=code)
        self.status_code = status_code
        self.details = details or {}
        self.request_id = request_id

    @classmethod
    def from_error_response(cls, error_response: "ErrorResponse") -> "APIError":
        """Construct an APIError from a shared ErrorResponse envelope.

        Args:
            error_response: Parsed ErrorResponse instance.

        Returns:
            APIError populated from the envelope fields.
        """
        return cls(
            status_code=error_response.error.status_code,
            code=error_response.error.code,
            message=error_response.error.message,
            details=error_response.error.details,
            request_id=error_response.request_id,
        )
