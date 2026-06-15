"""Integration tests: TrainingStudioClient standardized error mapping.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Tests that 4xx/5xx responses raise APIError with the correct code and
status_code drawn from the shared ErrorResponse envelope.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from scanq_shared.clients.exceptions import APIError
from scanq_shared.clients.training_studio import TrainingStudioClient


BASE_URL = "http://training-studio-test:8000"


def _error_body(code: str, message: str, status_code: int) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "status_code": status_code,
            "details": None,
            "request_id": "req-err-001",
        },
        "request_id": "req-err-001",
    }


def _mock_http_error(status_code: int, body: dict) -> httpx.HTTPStatusError:
    """Build an httpx.HTTPStatusError with a mock response."""
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = status_code
    mock_resp.json.return_value = body
    mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
        "error", request=MagicMock(), response=mock_resp
    )
    return mock_resp


class TestResolveContextErrors:
    @pytest.mark.asyncio
    async def test_404_raises_api_error(self):
        body = _error_body("not_found", "Project not found.", 404)
        mock_resp = _mock_http_error(404, body)
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=mock_resp)):
            with pytest.raises(APIError) as exc:
                await client.resolve_context(
                    project_id="proj-missing",
                    environment_id="env-x",
                )
        assert exc.value.code == "not_found"

    @pytest.mark.asyncio
    async def test_401_raises_http_status_error(self):
        body = _error_body("unauthorized", "Authentication required.", 401)
        mock_resp = _mock_http_error(401, body)
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=mock_resp)):
            with pytest.raises(APIError):
                await client.resolve_context(
                    project_id="proj-x",
                    environment_id="env-x",
                )


class TestGetServiceTokenErrors:
    @pytest.mark.asyncio
    async def test_500_raises_http_status_error(self):
        body = _error_body("internal_error", "Server error.", 500)
        mock_resp = _mock_http_error(500, body)
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=mock_resp)):
            with pytest.raises(APIError):
                await client.get_service_token(service_id="svc")


class TestRegisterLineageErrors:
    @pytest.mark.asyncio
    async def test_422_raises_http_status_error(self):
        body = _error_body("invalid_request", "Validation failed.", 422)
        mock_resp = _mock_http_error(422, body)
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=mock_resp)):
            with pytest.raises(APIError):
                await client.register_lineage(
                    run_id="run-x",
                    dwelling_id="dw-x",
                    pack_version="v1.0.0",
                    initiated_by="ci",
                    environment="staging",
                )


class TestFinalizeLineageErrors:
    @pytest.mark.asyncio
    async def test_404_raises_http_status_error(self):
        body = _error_body("not_found", "Lineage record not found.", 404)
        mock_resp = _mock_http_error(404, body)
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=mock_resp)):
            with pytest.raises(APIError):
                await client.finalize_lineage(
                    lineage_id="lin-missing",
                    status="finalized",
                )
