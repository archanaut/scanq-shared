from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from scanq_shared.clients import MLInferenceClient
from scanq_shared.clients.exceptions import ConnectionError, TimeoutError, ValidationError
from scanq_shared.models import FloorPlanTraceRequest


def _mock_http_error(status_code: int, body: dict) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = body
    resp.raise_for_status.side_effect = httpx.HTTPStatusError(
        "error", request=MagicMock(), response=resp
    )
    return resp


@pytest.mark.asyncio
async def test_validation_error_mapping():
    client = MLInferenceClient("http://ml:9000")
    req = FloorPlanTraceRequest(dwelling_id="dw-1", image_url="https://example.com/a.png")
    body = {"error": {"code": "validation_error", "message": "bad", "status_code": 422}}
    with patch.object(client, "_request", new=AsyncMock(return_value=_mock_http_error(422, body))):
        with pytest.raises(ValidationError) as exc:
            await client.trace_floor_plan(req)
    assert exc.value.code == "validation_error"


@pytest.mark.asyncio
async def test_timeout_error_mapping():
    client = MLInferenceClient("http://ml:9000")
    req = FloorPlanTraceRequest(dwelling_id="dw-1", image_url="https://example.com/a.png")
    with patch.object(client, "_request", new=AsyncMock(side_effect=TimeoutError("trace", 30))):
        with pytest.raises(TimeoutError):
            await client.trace_floor_plan(req)


@pytest.mark.asyncio
async def test_connection_error_mapping():
    client = MLInferenceClient("http://ml:9000")
    req = FloorPlanTraceRequest(dwelling_id="dw-1", image_url="https://example.com/a.png")
    with patch.object(client, "_request", new=AsyncMock(side_effect=ConnectionError("http://ml:9000", "down"))):
        with pytest.raises(ConnectionError):
            await client.trace_floor_plan(req)

