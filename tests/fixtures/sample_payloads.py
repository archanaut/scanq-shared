"""Sample payloads for testing and documentation.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.
"""


# ============================================================================
# Context Resolution Samples
# ============================================================================

CONTEXT_RESOLVE_REQUEST = {
    "project_id": "proj-archanaut-001",
    "environment_id": "env-staging",
    "actor_id": "actor-service-accreditation",
    "include_metadata": True,
}

CONTEXT_RESOLVE_RESPONSE = {
    "status": "resolved",
    "project_id": "proj-archanaut-001",
    "project_name": "Archanaut Training Studio",
    "environment_id": "env-staging",
    "environment_name": "Staging",
    "actor_id": "actor-service-accreditation",
    "actor_name": "ScanQ Accreditation Service",
    "resolved_at": "2026-06-15T10:30:00Z",
    "metadata": {
        "region": "us-west-2",
        "availability_zone": "us-west-2a",
    },
    "request_id": "req-uuid-12345",
}

# ============================================================================
# Service Token Samples
# ============================================================================

SERVICE_TOKEN_REQUEST = {
    "service_id": "scanq-accreditation",
    "scopes": ["read:context", "write:lineage"],
    "ttl_seconds": 3600,
    "metadata": {
        "correlation_id": "corr-12345",
        "source": "ci-pipeline",
    },
}

SERVICE_TOKEN_RESPONSE = {
    "status": "active",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzY2FucS1hY2NyZWRpdGF0aW9uIiwiaWF0IjoxNjE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    "token_type": "Bearer",
    "expires_at": "2026-06-15T11:30:00Z",
    "scopes": ["read:context", "write:lineage"],
    "issued_at": "2026-06-15T10:30:00Z",
    "request_id": "req-uuid-12345",
}

# ============================================================================
# Lineage Register Samples
# ============================================================================

LINEAGE_REGISTER_REQUEST = {
    "run_id": "run-dwelling-101-2026-06-15-143022",
    "dwelling_id": "dwelling-nathrs-uip-101",
    "pack_version": "v1.0.0",
    "initiated_by": "ci-pipeline",
    "environment": "staging",
    "metadata": {
        "git_commit": "abc123def456789",
        "git_branch": "main",
        "ci_job_id": "job-9876-5432",
        "ci_pipeline_id": "pipeline-1234",
    },
}

LINEAGE_REGISTER_RESPONSE = {
    "lineage_id": "lin-uuid-abc123def456",
    "run_id": "run-dwelling-101-2026-06-15-143022",
    "status": "registered",
    "registered_at": "2026-06-15T10:30:22Z",
    "request_id": "req-uuid-12345",
}

# ============================================================================
# Lineage Finalize Samples
# ============================================================================

LINEAGE_FINALIZE_REQUEST = {
    "lineage_id": "lin-uuid-abc123def456",
    "status": "finalized",
    "summary": "All validation tests passed; 42 scenarios executed successfully",
    "metrics": {
        "total_scenarios": 42,
        "passed": 42,
        "failed": 0,
        "skipped": 0,
        "evidence_items": 15,
        "duration_seconds": 342,
    },
}

LINEAGE_FINALIZE_RESPONSE = {
    "lineage_id": "lin-uuid-abc123def456",
    "status": "finalized",
    "finalized_at": "2026-06-15T10:36:04Z",
    "request_id": "req-uuid-12345",
}

# ============================================================================
# Error Response Samples
# ============================================================================

ERROR_RESPONSE_NOT_FOUND = {
    "code": "not_found",
    "message": "Project not found",
    "status_code": 404,
    "details": {
        "project_id": "proj-unknown",
    },
    "request_id": "req-uuid-12345",
}

ERROR_RESPONSE_INVALID_REQUEST = {
    "code": "invalid_request",
    "message": "Validation error",
    "status_code": 400,
    "details": {
        "actor_id": "Invalid format: expected UUID",
    },
    "request_id": "req-uuid-12345",
}

ERROR_RESPONSE_UNAUTHORIZED = {
    "code": "unauthorized",
    "message": "Missing or invalid authentication token",
    "status_code": 401,
    "details": None,
    "request_id": "req-uuid-12345",
}

ERROR_RESPONSE_INTERNAL = {
    "code": "internal_error",
    "message": "An unexpected error occurred",
    "status_code": 500,
    "details": {
        "error_id": "err-uuid-xyz",
        "timestamp": "2026-06-15T10:30:00Z",
    },
    "request_id": "req-uuid-12345",
}

ERROR_ENVELOPE_INVALID_REQUEST = {
    "code": "invalid_request",
    "message": "Validation error",
    "detail": {
        "compose_type": "must be one of: floor_plan, elevation, site_plan, photograph",
    },
    "correlation_id": "corr-err-001",
}

# ============================================================================
# Media Compose Samples
# ============================================================================

MEDIA_COMPOSE_REQUEST = {
    "source_media_refs": ["media-floor-001", "media-elev-002"],
    "compose_type": "floor_plan",
    "output_format": "pdf",
    "parameters": {"include_annotations": True},
    "metadata": {"correlation_id": "corr-compose-001"},
}

MEDIA_COMPOSE_RESPONSE = {
    "compose_id": "compose-001",
    "status": "complete",
    "output_media_ref": "media-compose-999",
    "composed_at": "2026-06-15T10:40:00Z",
    "partial_items": ["media-floor-001", "media-elev-002"],
    "request_id": "req-compose-001",
}

# ============================================================================
# Phase 2 Samples (v1.1.0)
# ============================================================================

PROJECT_CREATE_REQUEST = {
    "name": "Accreditation Pack v2",
    "description": "Phase 2 accreditation test pack",
    "owner_id": "user-abc123",
    "metadata": {"team": "accreditation"},
}

DWELLING_INPUT = {
    "dwelling_id": "dwelling-nathrs-uip-101",
    "source": "import",
    "configuration": {"climate_zone": "6", "num_storeys": 1},
    "expected_outputs": {"nathers_rating": 6.5},
    "metadata": {},
}

ML_FLOOR_PLAN_TRACE_REQUEST = {
    "dwelling_id": "dwelling-nathrs-uip-101",
    "image_url": "https://storage.scanq.internal/floor-plans/uip-101.png",
    "image_format": "png",
    "extract_windows": True,
    "extract_walls": True,
    "metadata": {},
}
