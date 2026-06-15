"""Pytest configuration and shared fixtures."""

import pytest
from datetime import datetime, timedelta
from scanq_shared.enums import (
    ContextStatus,
    ErrorCode,
    TokenStatus,
    LineageEventType,
)
from scanq_shared.schemas import (
    ContextResolveRequest,
    ContextResolveResponse,
    ServiceTokenRequest,
    ServiceTokenResponse,
    LineageRegisterRequest,
    LineageRegisterResponse,
    LineageFinalizeRequest,
    LineageFinalizeResponse,
)


@pytest.fixture
def sample_context_request():
    """Sample ContextResolveRequest fixture."""
    return ContextResolveRequest(
        project_id="proj-archanaut-001",
        environment_id="env-staging",
        actor_id="actor-service-accreditation",
        include_metadata=True,
    )


@pytest.fixture
def sample_context_response():
    """Sample ContextResolveResponse fixture."""
    return ContextResolveResponse(
        status=ContextStatus.RESOLVED,
        project_id="proj-archanaut-001",
        project_name="Archanaut Training Studio",
        environment_id="env-staging",
        environment_name="Staging",
        actor_id="actor-service-accreditation",
        actor_name="ScanQ Accreditation Service",
        resolved_at=datetime.utcnow(),
        metadata={"region": "us-west-2"},
        request_id="req-uuid-12345",
    )


@pytest.fixture
def sample_token_request():
    """Sample ServiceTokenRequest fixture."""
    return ServiceTokenRequest(
        service_id="scanq-accreditation",
        scopes=["read:context", "write:lineage"],
        ttl_seconds=3600,
        metadata={"correlation_id": "corr-12345"},
    )


@pytest.fixture
def sample_token_response():
    """Sample ServiceTokenResponse fixture."""
    issued_at = datetime.utcnow()
    expires_at = issued_at + timedelta(hours=1)
    return ServiceTokenResponse(
        status=TokenStatus.ACTIVE,
        token="bearer-token-abc123xyz",
        token_type="Bearer",
        expires_at=expires_at,
        scopes=["read:context", "write:lineage"],
        issued_at=issued_at,
        request_id="req-uuid-12345",
    )


@pytest.fixture
def sample_lineage_register_request():
    """Sample LineageRegisterRequest fixture."""
    return LineageRegisterRequest(
        run_id="run-dwelling-101-2026-06-15",
        dwelling_id="dwelling-nathrs-uip-101",
        pack_version="v1.0.0",
        initiated_by="ci-pipeline",
        environment="staging",
        metadata={"git_commit": "abc123def456", "ci_job_id": "job-9876"},
    )


@pytest.fixture
def sample_lineage_register_response():
    """Sample LineageRegisterResponse fixture."""
    return LineageRegisterResponse(
        lineage_id="lin-uuid-abc123",
        run_id="run-dwelling-101-2026-06-15",
        status=LineageEventType.REGISTERED,
        registered_at=datetime.utcnow(),
        request_id="req-uuid-12345",
    )


@pytest.fixture
def sample_lineage_finalize_request():
    """Sample LineageFinalizeRequest fixture."""
    return LineageFinalizeRequest(
        lineage_id="lin-uuid-abc123",
        status=LineageEventType.FINALIZED,
        summary="All validation tests passed",
        metrics={"passed": 42, "failed": 0, "evidence_items": 15},
    )


@pytest.fixture
def sample_lineage_finalize_response():
    """Sample LineageFinalizeResponse fixture."""
    return LineageFinalizeResponse(
        lineage_id="lin-uuid-abc123",
        status=LineageEventType.FINALIZED,
        finalized_at=datetime.utcnow(),
        request_id="req-uuid-12345",
    )
