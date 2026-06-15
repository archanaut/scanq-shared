"""Integration tests: TrainingStudioClient success paths.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Tests that each of the four fixed Phase 1 operations returns a correctly
typed response when the HTTP layer returns a well-formed success payload.
Uses httpx transport mocking — no live server required.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from scanq_shared.clients.training_studio import TrainingStudioClient
from scanq_shared.enums import ContextStatus, LineageEventType, TokenStatus
from scanq_shared.schemas import (
    ContextResolveResponse,
    LineageFinalizeResponse,
    LineageRegisterResponse,
    ServiceTokenResponse,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_response(status_code: int, body: dict) -> MagicMock:
    """Return a mock httpx.Response."""
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = body
    resp.raise_for_status = MagicMock()
    return resp


BASE_URL = "http://training-studio-test:8000"


# ---------------------------------------------------------------------------
# context.resolve
# ---------------------------------------------------------------------------

class TestResolveContextSuccess:
    @pytest.mark.asyncio
    async def test_returns_typed_response(self):
        body = {
            "status": "resolved",
            "project_id": "proj-001",
            "project_name": "Test Project",
            "environment_id": "env-staging",
            "environment_name": "Staging",
            "actor_id": "actor-svc",
            "actor_name": "Service",
            "resolved_at": "2026-06-15T10:00:00Z",
            "metadata": {},
            "request_id": "req-001",
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))):
            result = await client.resolve_context(
                project_id="proj-001",
                environment_id="env-staging",
            )
        assert isinstance(result, ContextResolveResponse)
        assert result.status == ContextStatus.RESOLVED
        assert result.project_id == "proj-001"

    @pytest.mark.asyncio
    async def test_passes_actor_id_when_provided(self):
        body = {
            "status": "resolved",
            "project_id": "proj-001",
            "project_name": None,
            "environment_id": "env-prod",
            "environment_name": None,
            "actor_id": "actor-x",
            "actor_name": None,
            "resolved_at": "2026-06-15T10:00:00Z",
            "metadata": {},
            "request_id": None,
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))) as mock_req:
            await client.resolve_context(
                project_id="proj-001",
                environment_id="env-prod",
                actor_id="actor-x",
            )
        call_kwargs = mock_req.call_args.kwargs
        assert call_kwargs["json"]["actor_id"] == "actor-x"


# ---------------------------------------------------------------------------
# auth.service-token
# ---------------------------------------------------------------------------

class TestGetServiceTokenSuccess:
    @pytest.mark.asyncio
    async def test_returns_typed_response(self):
        body = {
            "status": "active",
            "token": "bearer-xyz",
            "token_type": "Bearer",
            "expires_at": "2026-06-15T11:00:00Z",
            "scopes": ["read:context", "write:lineage"],
            "issued_at": "2026-06-15T10:00:00Z",
            "request_id": "req-002",
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))):
            result = await client.get_service_token(service_id="scanq-accreditation")
        assert isinstance(result, ServiceTokenResponse)
        assert result.status == TokenStatus.ACTIVE
        assert result.token_type == "Bearer"

    @pytest.mark.asyncio
    async def test_uses_default_scopes(self):
        body = {
            "status": "active",
            "token": "tok",
            "token_type": "Bearer",
            "expires_at": "2026-06-15T11:00:00Z",
            "scopes": ["read:context", "write:lineage"],
            "issued_at": "2026-06-15T10:00:00Z",
            "request_id": None,
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))) as mock_req:
            await client.get_service_token(service_id="svc")
        sent_scopes = mock_req.call_args.kwargs["json"]["scopes"]
        assert "read:context" in sent_scopes
        assert "write:lineage" in sent_scopes

    @pytest.mark.asyncio
    async def test_get_service_token_success_regression(self):
        body = {
            "status": "active",
            "token": "tok2",
            "token_type": "Bearer",
            "expires_at": "2026-06-15T11:00:00Z",
            "scopes": ["read:context"],
            "issued_at": "2026-06-15T10:00:00Z",
            "request_id": "req-ts-token",
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))):
            out = await client.get_service_token("svc")
        assert out.request_id == "req-ts-token"


# ---------------------------------------------------------------------------
# lineage.register
# ---------------------------------------------------------------------------

class TestRegisterLineageSuccess:
    @pytest.mark.asyncio
    async def test_returns_typed_response(self):
        body = {
            "lineage_id": "lin-001",
            "run_id": "run-001",
            "status": "registered",
            "registered_at": "2026-06-15T10:00:00Z",
            "request_id": "req-003",
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))):
            result = await client.register_lineage(
                run_id="run-001",
                dwelling_id="dw-001",
                pack_version="v1.0.0",
                initiated_by="ci",
                environment="staging",
            )
        assert isinstance(result, LineageRegisterResponse)
        assert result.lineage_id == "lin-001"
        assert result.status == LineageEventType.REGISTERED


# ---------------------------------------------------------------------------
# lineage.finalize
# ---------------------------------------------------------------------------

class TestFinalizeLineageSuccess:
    @pytest.mark.asyncio
    async def test_returns_typed_response(self):
        body = {
            "lineage_id": "lin-001",
            "status": "finalized",
            "finalized_at": "2026-06-15T10:45:00Z",
            "request_id": "req-004",
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))):
            result = await client.finalize_lineage(
                lineage_id="lin-001",
                status="finalized",
                metrics={"passed": 10},
            )
        assert isinstance(result, LineageFinalizeResponse)
        assert result.status == LineageEventType.FINALIZED

    @pytest.mark.asyncio
    async def test_sends_correct_path(self):
        body = {
            "lineage_id": "lin-999",
            "status": "finalized",
            "finalized_at": "2026-06-15T10:45:00Z",
            "request_id": None,
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))) as mock_req:
            await client.finalize_lineage(
                lineage_id="lin-999",
                status="finalized",
            )
        call_args = mock_req.call_args
        assert "lin-999" in call_args.args[1]

    @pytest.mark.asyncio
    async def test_register_and_finalize_success_regression(self):
        register_body = {
            "lineage_id": "lin-101",
            "run_id": "run-101",
            "status": "registered",
            "registered_at": "2026-06-15T10:00:00Z",
            "request_id": "req-reg",
        }
        finalize_body = {
            "lineage_id": "lin-101",
            "status": "finalized",
            "finalized_at": "2026-06-15T10:05:00Z",
            "request_id": "req-fin",
        }
        client = TrainingStudioClient(BASE_URL)
        with patch.object(
            client,
            "_request",
            new=AsyncMock(side_effect=[_mock_response(200, register_body), _mock_response(200, finalize_body)]),
        ):
            reg = await client.register_lineage(
                run_id="run-101",
                dwelling_id="dw-101",
                pack_version="v1.0.0",
                initiated_by="ci",
                environment="staging",
            )
            fin = await client.finalize_lineage(lineage_id=reg.lineage_id, status="finalized")
        assert fin.status == LineageEventType.FINALIZED
