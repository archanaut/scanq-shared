"""Client exceptions."""


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

    def __init__(self, message: str, details: dict | None = None) -> None:
        """Initialize ValidationError.

        Args:
            message: Error message
            details: Additional validation error details
        """
        super().__init__(message, code="validation_error")
        self.details = details or {}


class APIError(ClientError):
    """Raised for API-level errors (4xx, 5xx responses)."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: dict | None = None,
    ) -> None:
        """Initialize APIError.

        Args:
            status_code: HTTP status code
            code: API error code
            message: Error message
            details: Additional error details
        """
        super().__init__(message, code=code)
        self.status_code = status_code
        self.details = details or {}
