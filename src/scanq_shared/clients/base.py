"""Base client with retry, timeout, and tracing support."""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class BaseClient:
    """Base HTTP client with retry logic, timeout handling, and tracing.

    Provides common functionality for all typed clients:
    - Automatic retry on transient failures
    - Request timeout enforcement
    - Request/response tracing
    - Consistent error handling
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        trace_requests: bool = False,
    ) -> None:
        """Initialize BaseClient.

        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries on transient failures (default: 3)
            trace_requests: Enable request/response logging (default: False)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.trace_requests = trace_requests
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "BaseClient":
        """Async context manager entry."""
        self._client = httpx.AsyncClient(base_url=self.base_url)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> httpx.AsyncClient:
        """Get or create async client."""
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=self.base_url)
        return self._client

    async def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make HTTP request with retry logic.

        Args:
            method: HTTP method
            url: Request URL (relative to base_url)
            **kwargs: Additional httpx parameters

        Returns:
            Response object
        """
        client = self._get_client()
        full_url = f"{self.base_url}{url}"

        for attempt in range(self.max_retries + 1):
            try:
                if self.trace_requests:
                    logger.debug(
                        f"[{method}] {full_url} (attempt {attempt + 1}/{self.max_retries + 1})"
                    )

                response = await client.request(
                    method,
                    url,
                    timeout=self.timeout,
                    **kwargs,
                )

                if self.trace_requests:
                    logger.debug(f"Response: {response.status_code}")

                return response

            except httpx.TimeoutException as e:
                if attempt == self.max_retries:
                    raise
                logger.warning(f"Timeout on attempt {attempt + 1}, retrying...")

            except (httpx.ConnectError, httpx.NetworkError) as e:
                if attempt == self.max_retries:
                    raise
                logger.warning(
                    f"Network error on attempt {attempt + 1}: {e}, retrying..."
                )

        raise RuntimeError("Unexpected: retry loop exhausted")

    async def close(self) -> None:
        """Close the async client connection."""
        if self._client:
            await self._client.aclose()
            self._client = None
