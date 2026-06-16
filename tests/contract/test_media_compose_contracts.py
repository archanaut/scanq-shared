"""Contract tests: media compose schemas and error envelope."""

from scanq_shared.enums import ErrorCode, MediaComposeStatus, MediaType
from scanq_shared.schemas import ErrorEnvelope, ErrorResponse, MediaComposeRequest, MediaComposeResponse
from tests.fixtures.sample_payloads import (
    ERROR_ENVELOPE_INVALID_REQUEST,
    MEDIA_COMPOSE_REQUEST,
    MEDIA_COMPOSE_RESPONSE,
)
from tests.fixtures.compatibility_payloads import ERROR_RESPONSE_V1


def test_media_type_values_are_stable():
    assert {e.value for e in MediaType} == {
        "floor_plan",
        "elevation",
        "site_plan",
        "photograph",
    }


def test_media_compose_status_values_are_stable():
    assert {e.value for e in MediaComposeStatus} == {
        "pending",
        "processing",
        "complete",
        "failed",
    }


def test_media_compose_request_parses_canonical_payload():
    request = MediaComposeRequest(**MEDIA_COMPOSE_REQUEST)
    assert request.compose_type == MediaType.FLOOR_PLAN
    assert request.parameters["include_annotations"] is True


def test_media_compose_response_parses_canonical_payload():
    response = MediaComposeResponse(**MEDIA_COMPOSE_RESPONSE)
    assert response.status == MediaComposeStatus.COMPLETE
    assert response.output_media_ref == "media-compose-999"
    assert response.partial_items == ["media-floor-001", "media-elev-002"]


def test_error_envelope_uses_typed_code_and_backward_compatibility():
    envelope = ErrorEnvelope(**ERROR_ENVELOPE_INVALID_REQUEST)
    assert envelope.code == ErrorCode.INVALID_REQUEST
    assert envelope.correlation_id == "corr-err-001"

    legacy = ErrorResponse.from_dict(ERROR_RESPONSE_V1)
    assert legacy.error.code == "not_found"
    assert legacy.error.status_code == 404
