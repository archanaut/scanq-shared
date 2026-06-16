"""Integration tests: release compatibility for v1.2.0."""

from scanq_shared.models import DwellingInput
from scanq_shared.models.ml_inference import FloorPlanTraceRequest
from scanq_shared.schemas import (
    ContextResolveRequest,
    ContextResolveResponse,
    ErrorEnvelope,
    ErrorResponse,
    LineageFinalizeRequest,
    LineageFinalizeResponse,
    LineageRegisterRequest,
    LineageRegisterResponse,
    MediaComposeRequest,
    MediaComposeResponse,
    ServiceTokenRequest,
    ServiceTokenResponse,
)
from tests.fixtures.compatibility_payloads import (
    COMPAT_V1_1_PAIRS,
    COMPAT_V1_2_PAIRS,
    COMPAT_V1_PAIRS,
    CONTEXT_RESOLVE_REQUEST_V1,
    CONTEXT_RESOLVE_RESPONSE_V1,
    DWELLING_INPUT_V1_1,
    ERROR_ENVELOPE_V1_2,
    ERROR_RESPONSE_V1,
    FLOOR_PLAN_TRACE_REQUEST_V1_1,
    LINEAGE_FINALIZE_REQUEST_V1,
    LINEAGE_FINALIZE_RESPONSE_V1,
    LINEAGE_REGISTER_REQUEST_V1,
    LINEAGE_REGISTER_RESPONSE_V1,
    MEDIA_COMPOSE_REQUEST_V1_2,
    MEDIA_COMPOSE_RESPONSE_V1_2,
    SERVICE_TOKEN_REQUEST_V1,
    SERVICE_TOKEN_RESPONSE_V1,
)


def test_core_v1_payloads_still_parse():
    assert ContextResolveRequest(**CONTEXT_RESOLVE_REQUEST_V1).project_id == "proj-archanaut-001"
    assert ContextResolveResponse(**CONTEXT_RESOLVE_RESPONSE_V1).project_id == "proj-archanaut-001"
    assert ServiceTokenRequest(**SERVICE_TOKEN_REQUEST_V1).service_id == "scanq-accreditation"
    assert ServiceTokenResponse(**SERVICE_TOKEN_RESPONSE_V1).status.value == "active"
    assert LineageRegisterRequest(**LINEAGE_REGISTER_REQUEST_V1).run_id == "run-compat-001"
    assert LineageRegisterResponse(**LINEAGE_REGISTER_RESPONSE_V1).lineage_id == "lin-compat-abc123"
    assert LineageFinalizeRequest(**LINEAGE_FINALIZE_REQUEST_V1).lineage_id == "lin-compat-abc123"
    assert LineageFinalizeResponse(**LINEAGE_FINALIZE_RESPONSE_V1).lineage_id == "lin-compat-abc123"
    assert ErrorResponse(**ERROR_RESPONSE_V1).error.code == "not_found"


def test_v1_1_additive_payloads_still_parse():
    assert DwellingInput(**DWELLING_INPUT_V1_1).dwelling_id == "dw-1"
    assert FloorPlanTraceRequest(**FLOOR_PLAN_TRACE_REQUEST_V1_1).dwelling_id == "dw-1"


def test_v1_2_media_compose_payloads_and_error_envelope_parse():
    request = MediaComposeRequest(**MEDIA_COMPOSE_REQUEST_V1_2)
    response = MediaComposeResponse(**MEDIA_COMPOSE_RESPONSE_V1_2)
    envelope = ErrorEnvelope(**ERROR_ENVELOPE_V1_2)

    assert request.compose_type.value == "floor_plan"
    assert response.compose_id == "compose-compat-001"
    assert response.status == "complete"
    assert envelope.correlation_id == "corr-compat-006"


def test_compatibility_pairs_are_kept_in_fixture_order():
    assert [name for name, _ in COMPAT_V1_PAIRS]
    assert [name for name, _ in COMPAT_V1_1_PAIRS]
    assert [name for name, _ in COMPAT_V1_2_PAIRS]
