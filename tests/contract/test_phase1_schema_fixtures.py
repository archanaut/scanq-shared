"""Contract tests: Phase 1 schema fixture validation.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Validates that agreed-upon Phase 1 payload shapes can be parsed by
shared schemas without errors, and that compatibility regression
payloads remain stable.
"""

import pytest

from scanq_shared.schemas import (
    ContextResolveRequest,
    ContextResolveResponse,
    ErrorResponse,
    LineageFinalizeRequest,
    LineageFinalizeResponse,
    LineageRegisterRequest,
    LineageRegisterResponse,
    ServiceTokenRequest,
    ServiceTokenResponse,
)
from scanq_shared.enums import ContextStatus, LineageEventType, TokenStatus
from tests.fixtures.compatibility_payloads import (
    CONTEXT_RESOLVE_REQUEST_V1,
    CONTEXT_RESOLVE_RESPONSE_V1,
    ERROR_RESPONSE_V1,
    LINEAGE_FINALIZE_REQUEST_V1,
    LINEAGE_FINALIZE_RESPONSE_V1,
    LINEAGE_REGISTER_REQUEST_V1,
    LINEAGE_REGISTER_RESPONSE_V1,
    SERVICE_TOKEN_REQUEST_V1,
    SERVICE_TOKEN_RESPONSE_V1,
)


# ---------------------------------------------------------------------------
# context.resolve
# ---------------------------------------------------------------------------

class TestContextResolveSchemas:
    def test_request_parses_v1_payload(self):
        req = ContextResolveRequest(**CONTEXT_RESOLVE_REQUEST_V1)
        assert req.project_id == "proj-archanaut-001"
        assert req.environment_id == "env-staging"
        assert req.actor_id == "actor-service-accreditation"
        assert req.include_metadata is False

    def test_response_parses_v1_payload(self):
        resp = ContextResolveResponse(**CONTEXT_RESOLVE_RESPONSE_V1)
        assert resp.status == ContextStatus.RESOLVED
        assert resp.project_id == "proj-archanaut-001"

    def test_request_roundtrip(self, sample_context_request):
        dumped = sample_context_request.model_dump()
        rebuilt = ContextResolveRequest(**dumped)
        assert rebuilt == sample_context_request

    def test_response_roundtrip(self, sample_context_response):
        dumped = sample_context_response.model_dump()
        rebuilt = ContextResolveResponse(**dumped)
        assert rebuilt == sample_context_response

    def test_request_optional_actor_id(self):
        req = ContextResolveRequest(
            project_id="proj-123",
            environment_id="env-prod",
        )
        assert req.actor_id is None
        assert req.include_metadata is False


# ---------------------------------------------------------------------------
# auth.service-token
# ---------------------------------------------------------------------------

class TestServiceTokenSchemas:
    def test_request_parses_v1_payload(self):
        req = ServiceTokenRequest(**SERVICE_TOKEN_REQUEST_V1)
        assert req.service_id == "scanq-accreditation"
        assert req.scopes == ["read:context", "write:lineage"]
        assert req.ttl_seconds == 3600

    def test_response_parses_v1_payload(self):
        resp = ServiceTokenResponse(**SERVICE_TOKEN_RESPONSE_V1)
        assert resp.status == TokenStatus.ACTIVE
        assert resp.token_type == "Bearer"

    def test_request_ttl_minimum(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            ServiceTokenRequest(service_id="svc", ttl_seconds=30)

    def test_request_ttl_maximum(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            ServiceTokenRequest(service_id="svc", ttl_seconds=99999)

    def test_request_default_scopes(self):
        req = ServiceTokenRequest(service_id="svc")
        assert "read:context" in req.scopes
        assert "write:lineage" in req.scopes


# ---------------------------------------------------------------------------
# lineage.register
# ---------------------------------------------------------------------------

class TestLineageRegisterSchemas:
    def test_request_parses_v1_payload(self):
        req = LineageRegisterRequest(**LINEAGE_REGISTER_REQUEST_V1)
        assert req.run_id == "run-compat-001"
        assert req.dwelling_id == "dwelling-compat-101"

    def test_response_parses_v1_payload(self):
        resp = LineageRegisterResponse(**LINEAGE_REGISTER_RESPONSE_V1)
        assert resp.status == LineageEventType.REGISTERED
        assert resp.lineage_id == "lin-compat-abc123"


# ---------------------------------------------------------------------------
# lineage.finalize
# ---------------------------------------------------------------------------

class TestLineageFinalizeSchemas:
    def test_request_parses_v1_payload(self):
        req = LineageFinalizeRequest(**LINEAGE_FINALIZE_REQUEST_V1)
        assert req.lineage_id == "lin-compat-abc123"
        assert req.status == LineageEventType.FINALIZED

    def test_response_parses_v1_payload(self):
        resp = LineageFinalizeResponse(**LINEAGE_FINALIZE_RESPONSE_V1)
        assert resp.status == LineageEventType.FINALIZED


# ---------------------------------------------------------------------------
# Error envelope
# ---------------------------------------------------------------------------

class TestErrorResponseSchema:
    def test_parses_v1_payload(self):
        err = ErrorResponse(**ERROR_RESPONSE_V1)
        assert err.error.code == "not_found"
        assert err.error.status_code == 404

    def test_from_dict_known_structure(self):
        err = ErrorResponse.from_dict(ERROR_RESPONSE_V1)
        assert err.error.code == "not_found"

    def test_from_dict_unknown_structure_fallback(self):
        err = ErrorResponse.from_dict({"unexpected": "payload", "status_code": 503})
        assert err.error.code == "unknown_error"
        assert err.error.details is not None
