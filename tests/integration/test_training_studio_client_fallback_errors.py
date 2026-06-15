"""Integration tests: TrainingStudioClient unknown/fallback error handling.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Tests that unexpected or malformed error responses are handled gracefully —
the client surfaces a diagnosable error without losing the raw payload.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from scanq_shared.clients.training_studio import TrainingStudioClient


BASE_URL = "http://training-studio-test:8000"


def _mock_response_with_body(status_code: int, body: dict, raise_on_status: bool = False):
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = status_code
    mock_resp.json.return_value = body
    if raise_on_status:
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=mock_resp
        )
    else:
        mock_resp.raise_for_status = MagicMock()
    return mock_resp


class TestFallbackErrorHandling:
    """When the API returns an unexpected/malformed payload on error status,
    the client should raise rather than silently discard the error."""

    @pytest.mark.asyncio
    async def test_unexpected_error_body_still_raises(self):
        """A non-standard error body on a 500 still raises HTTPStatusError."""
        unexpected_body = {"msg": "something went wrong", "code": 500}
        mock_resp = _mock_response_with_body(500, unexpected_body, raise_on_status=True)
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=mock_resp)):
            with pytest.raises(httpx.HTTPStatusError):
                await client.resolve_context(
                    project_id="proj-x",
                    environment_id="env-x",
                )

    @pytest.mark.asyncio
    async def test_html_error_body_still_raises(self):
        """An HTML error response (e.g., nginx 502) still raises."""
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 502
        mock_resp.json.side_effect = Exception("Not JSON")
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "bad gateway", request=MagicMock(), response=mock_resp
        )
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=mock_resp)):
            with pytest.raises(httpx.HTTPStatusError):
                await client.get_service_token(service_id="svc")

    @pytest.mark.asyncio
    async def test_timeout_raises(self):
        """A timeout on _request propagates out of the client method."""
        client = TrainingStudioClient(BASE_URL)
        with patch.object(
            client,
            "_request",
            new=AsyncMock(side_effect=httpx.TimeoutException("timed out")),
        ):
            with pytest.raises(Exception):
                await client.register_lineage(
                    run_id="run-x",
                    dwelling_id="dw-x",
                    pack_version="v1.0.0",
                    initiated_by="ci",
                    environment="staging",
                )

    @pytest.mark.asyncio
    async def test_malformed_success_response_raises_validation_error(self):
        """A 200 with an invalid response body raises ClientValidationError."""
        from scanq_shared.clients.exceptions import ValidationError as ClientValidationError

        malformed_body = {"unexpected_key": "oops"}  # missing required fields
        mock_resp = _mock_response_with_body(200, malformed_body)
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=mock_resp)):
            with pytest.raises(ClientValidationError):
                await client.resolve_context(
                    project_id="proj-x",
                    environment_id="env-x",
                )
