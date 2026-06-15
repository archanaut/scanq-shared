from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from scanq_shared.clients import MLInferenceClient
from scanq_shared.enums import ConfidenceLevel, ExecutionStatus
from scanq_shared.models import (
    ConfidenceMetadata,
    DwellingConfiguration,
    FloorPlanFeatureAttributes,
    FloorPlanTraceRequest,
    FloorPlanTraceResponse,
    NatHERSAttributeRequest,
    NatHERSAttributeResponse,
)


def _mock_response(status_code: int, body: dict) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = body
    resp.raise_for_status = MagicMock()
    return resp


@pytest.mark.asyncio
async def test_trace_floor_plan_success():
    client = MLInferenceClient("http://ml:9000")
    req = FloorPlanTraceRequest(dwelling_id="dw-1", image_url="https://example.com/a.png")
    body = FloorPlanTraceResponse(
        dwelling_id="dw-1",
        status=ExecutionStatus.COMPLETED,
        features=FloorPlanFeatureAttributes(confidence=ConfidenceLevel.HIGH),
        confidence=ConfidenceMetadata(level=ConfidenceLevel.HIGH, score=0.9),
    ).model_dump(mode="json")
    with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))):
        out = await client.trace_floor_plan(req)
    assert out.status == ExecutionStatus.COMPLETED


@pytest.mark.asyncio
async def test_extract_nathers_attributes_success():
    client = MLInferenceClient("http://ml:9000")
    req = NatHERSAttributeRequest(
        dwelling_id="dw-1",
        floor_plan_features=FloorPlanFeatureAttributes(confidence=ConfidenceLevel.HIGH),
        configuration=DwellingConfiguration(climate_zone="6"),
    )
    body = NatHERSAttributeResponse(
        dwelling_id="dw-1",
        status=ExecutionStatus.COMPLETED,
        predicted_rating=6.5,
        heating_load_mj=10,
        cooling_load_mj=5,
        confidence=ConfidenceMetadata(level=ConfidenceLevel.HIGH, score=0.9),
    ).model_dump(mode="json")
    with patch.object(client, "_request", new=AsyncMock(return_value=_mock_response(200, body))):
        out = await client.extract_nathers_attributes(req)
    assert out.predicted_rating == 6.5

