"""Base client with retry, timeout, and tracing support.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.
"""

import logging
import random
import asyncio
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)

_RequestT = TypeVar("_RequestT", bound=BaseModel)
_ResponseT = TypeVar("_ResponseT", bound=BaseModel)


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
        self.base_delay = 0.5
        self.max_delay = 30.0

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

            except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as exc:
                if attempt == self.max_retries:
                    from .exceptions import map_httpx_error

                    raise map_httpx_error(
                        exc,
                        url=full_url,
                        timeout_seconds=self.timeout,
                    ) from exc
                delay = min(self.max_delay, self.base_delay * (2**attempt))
                sleep_for = random.uniform(0, delay)
                logger.warning(
                    "Transient error on attempt %s/%s; retrying in %.3fs: %s",
                    attempt + 1,
                    self.max_retries + 1,
                    sleep_for,
                    exc,
                )
                await asyncio.sleep(sleep_for)

        raise RuntimeError("Unexpected: retry loop exhausted")

    async def _typed_request(
        self,
        method: str,
        url: str,
        request_model: _RequestT,
        response_type: type[_ResponseT],
    ) -> _ResponseT:
        """Typed request helper: serialize request, call API, deserialize response.

        This helper encapsulates the standard request/response translation
        pattern used by all Phase 1 fixed-inventory operations:
        1. Serialize the Pydantic request model to JSON.
        2. Call ``_request`` for retry/tracing handling.
        3. Raise on HTTP error status.
        4. Deserialize and validate the response against ``response_type``.

        Args:
            method: HTTP method (e.g., "POST").
            url: Path relative to base_url.
            request_model: Pydantic model instance to send as the JSON body.
            response_type: Pydantic model class to parse the JSON response into.

        Returns:
            A validated instance of ``response_type``.

        Raises:
            httpx.HTTPStatusError: On 4xx/5xx responses.
            scanq_shared.clients.exceptions.ValidationError: If the response
                body does not match ``response_type``.
        """
        from pydantic import ValidationError as PydanticValidationError

        from .exceptions import ValidationError as ClientValidationError

        try:
            response = await self._request(
                method,
                url,
                json=request_model.model_dump(mode="json"),
            )
            response.raise_for_status()
            return response_type(**response.json())
        except httpx.HTTPStatusError as exc:
            from .exceptions import map_httpx_error

            raise map_httpx_error(exc, url=url, timeout_seconds=self.timeout) from exc
        except PydanticValidationError as exc:
            raise ClientValidationError(
                f"Response validation failed: {exc.error_count()} errors",
                details=exc.errors(),
            ) from exc

    async def close(self) -> None:
        """Close the async client connection."""
        if self._client:
            await self._client.aclose()
            self._client = None
