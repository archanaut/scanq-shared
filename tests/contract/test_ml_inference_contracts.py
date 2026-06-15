from scanq_shared.enums import ConfidenceLevel, ExecutionStatus
from scanq_shared.models import (
    ConfidenceMetadata,
    DwellingConfiguration,
    FloorPlanFeatureAttributes,
    FloorPlanTraceRequest,
    FloorPlanTraceResponse,
    NatHERSAttributeRequest,
    NatHERSAttributeResponse,
    WindowAttributes,
)


def test_floor_plan_trace_request_roundtrip():
    req = FloorPlanTraceRequest(dwelling_id="dw-1", image_url="https://example.com/a.png")
    rebuilt = FloorPlanTraceRequest(**req.model_dump())
    assert rebuilt == req


def test_floor_plan_trace_response_insufficient_confidence():
    response = FloorPlanTraceResponse(
        dwelling_id="dw-1",
        status=ExecutionStatus.COMPLETED,
        features=FloorPlanFeatureAttributes(confidence=ConfidenceLevel.INSUFFICIENT),
        confidence=ConfidenceMetadata(level=ConfidenceLevel.INSUFFICIENT, score=0.1),
        processing_time_ms=123,
    )
    assert response.confidence.level == ConfidenceLevel.INSUFFICIENT


def test_nathers_request_response_roundtrip():
    features = FloorPlanFeatureAttributes(windows=[WindowAttributes(width_m=1.0, height_m=1.0)])
    req = NatHERSAttributeRequest(
        dwelling_id="dw-1",
        floor_plan_features=features,
        configuration=DwellingConfiguration(climate_zone="6"),
    )
    assert req.floor_plan_features.windows[0].area_m2 == 1.0

    resp = NatHERSAttributeResponse(
        dwelling_id="dw-1",
        status=ExecutionStatus.COMPLETED,
        predicted_rating=6.5,
        heating_load_mj=10,
        cooling_load_mj=5,
        confidence=ConfidenceMetadata(level=ConfidenceLevel.HIGH, score=0.9),
        processing_time_ms=500,
        request_id="req-1",
    )
    rebuilt = NatHERSAttributeResponse(**resp.model_dump())
    assert rebuilt.request_id == "req-1"
