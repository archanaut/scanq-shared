"""Integration tests: Shared model roundtrip serialization.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Verifies that all Phase 1 shared models can be serialized to dict/JSON
and deserialized back without data loss or type coercion errors.
"""

import json
from datetime import datetime, timezone


from scanq_shared.schemas import (
    ContextResolveRequest,
    ContextResolveResponse,
    LineageFinalizeRequest,
    LineageFinalizeResponse,
    LineageRegisterRequest,
    LineageRegisterResponse,
    ServiceTokenRequest,
    ServiceTokenResponse,
    ErrorResponse,
    ProjectCreateRequest,
    EnvironmentCreateRequest,
    IntakeDraftGenerateRequest,
    JobResponse,
)
from scanq_shared.enums import DwellingSource, ExecutionStatus, LineageEventType


class TestContextRoundtrip:
    def test_request_dict_roundtrip(self, sample_context_request):
        dumped = sample_context_request.model_dump()
        rebuilt = ContextResolveRequest(**dumped)
        assert rebuilt == sample_context_request

    def test_request_json_roundtrip(self, sample_context_request):
        json_str = sample_context_request.model_dump_json()
        data = json.loads(json_str)
        rebuilt = ContextResolveRequest(**data)
        assert rebuilt.project_id == sample_context_request.project_id

    def test_response_dict_roundtrip(self, sample_context_response):
        dumped = sample_context_response.model_dump()
        rebuilt = ContextResolveResponse(**dumped)
        assert rebuilt.status == sample_context_response.status

    def test_response_json_roundtrip(self, sample_context_response):
        json_str = sample_context_response.model_dump_json()
        data = json.loads(json_str)
        rebuilt = ContextResolveResponse(**data)
        assert rebuilt.project_id == sample_context_response.project_id

    def test_optional_fields_preserved_as_none(self):
        req = ContextResolveRequest(
            project_id="proj-x",
            environment_id="env-x",
        )
        dumped = req.model_dump()
        assert dumped["actor_id"] is None
        rebuilt = ContextResolveRequest(**dumped)
        assert rebuilt.actor_id is None


class TestServiceTokenRoundtrip:
    def test_request_dict_roundtrip(self, sample_token_request):
        dumped = sample_token_request.model_dump()
        rebuilt = ServiceTokenRequest(**dumped)
        assert rebuilt == sample_token_request

    def test_response_dict_roundtrip(self, sample_token_response):
        dumped = sample_token_response.model_dump()
        rebuilt = ServiceTokenResponse(**dumped)
        assert rebuilt.status == sample_token_response.status

    def test_response_json_roundtrip(self, sample_token_response):
        json_str = sample_token_response.model_dump_json()
        data = json.loads(json_str)
        rebuilt = ServiceTokenResponse(**data)
        assert rebuilt.token == sample_token_response.token


class TestLineageRegisterRoundtrip:
    def test_request_dict_roundtrip(self, sample_lineage_register_request):
        dumped = sample_lineage_register_request.model_dump()
        rebuilt = LineageRegisterRequest(**dumped)
        assert rebuilt == sample_lineage_register_request

    def test_response_dict_roundtrip(self, sample_lineage_register_response):
        dumped = sample_lineage_register_response.model_dump()
        rebuilt = LineageRegisterResponse(**dumped)
        assert rebuilt.lineage_id == sample_lineage_register_response.lineage_id


class TestLineageFinalizeRoundtrip:
    def test_request_dict_roundtrip(self):
        req = LineageFinalizeRequest(
            lineage_id="lin-abc",
            status=LineageEventType.FINALIZED,
            summary="Done",
            metrics={"passed": 5},
        )
        dumped = req.model_dump()
        rebuilt = LineageFinalizeRequest(**dumped)
        assert rebuilt == req

    def test_response_dict_roundtrip(self):
        resp = LineageFinalizeResponse(
            lineage_id="lin-abc",
            status=LineageEventType.FINALIZED,
            finalized_at=datetime.now(tz=timezone.utc),
            request_id="req-xyz",
        )
        dumped = resp.model_dump()
        rebuilt = LineageFinalizeResponse(**dumped)
        assert rebuilt.lineage_id == resp.lineage_id


class TestErrorResponseRoundtrip:
    def test_dict_roundtrip(self):
        from scanq_shared.schemas.errors import ErrorSchema

        err = ErrorResponse(
            error=ErrorSchema(
                code="not_found",
                message="Not found.",
                status_code=404,
            )
        )
        dumped = err.model_dump()
        rebuilt = ErrorResponse(**dumped)
        assert rebuilt.error.code == "not_found"

    def test_json_roundtrip(self):
        from scanq_shared.schemas.errors import ErrorSchema

        err = ErrorResponse(
            error=ErrorSchema(
                code="internal_error",
                message="Server error.",
                status_code=500,
            ),
            request_id="req-abc",
        )
        json_str = err.model_dump_json()
        data = json.loads(json_str)
        rebuilt = ErrorResponse(**data)
        assert rebuilt.request_id == "req-abc"


class TestUs1ImportSurface:
    def test_new_schema_symbols_import_and_roundtrip(self):
        p = ProjectCreateRequest(name="proj", owner_id="owner")
        assert ProjectCreateRequest(**p.model_dump()) == p
        e = EnvironmentCreateRequest(project_id="proj-1", name="staging")
        assert e.project_id == "proj-1"
        i = IntakeDraftGenerateRequest(
            project_id="proj-1",
            environment_id="env-1",
            source_type=DwellingSource.IMPORT,
        )
        assert i.source_type == DwellingSource.IMPORT
        j = JobResponse(
            id="job-1",
            project_id="proj-1",
            environment_id="env-1",
            status=ExecutionStatus.PENDING,
            created_at=datetime.now(tz=timezone.utc),
        )
        assert j.status == ExecutionStatus.PENDING
