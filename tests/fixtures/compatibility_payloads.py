"""Compatibility regression payloads for Phase 1 contract stability testing.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

These fixtures represent agreed-upon payload shapes at Phase 1 release.
They must NOT be modified after release — any change indicates a
compatibility-breaking regression that requires a SemVer bump.
"""

# ---------------------------------------------------------------------------
# context.resolve — POST /accreditation/context/resolve
# ---------------------------------------------------------------------------

CONTEXT_RESOLVE_REQUEST_V1 = {
    "project_id": "proj-archanaut-001",
    "environment_id": "env-staging",
    "actor_id": "actor-service-accreditation",
    "include_metadata": False,
}

CONTEXT_RESOLVE_RESPONSE_V1 = {
    "status": "resolved",
    "project_id": "proj-archanaut-001",
    "project_name": None,
    "environment_id": "env-staging",
    "environment_name": None,
    "actor_id": "actor-service-accreditation",
    "actor_name": None,
    "resolved_at": "2026-06-15T10:30:00Z",
    "metadata": {},
    "request_id": "req-compat-001",
}

# ---------------------------------------------------------------------------
# auth.service-token — POST /accreditation/auth/service-token
# ---------------------------------------------------------------------------

SERVICE_TOKEN_REQUEST_V1 = {
    "service_id": "scanq-accreditation",
    "scopes": ["read:context", "write:lineage"],
    "ttl_seconds": 3600,
    "metadata": None,
}

SERVICE_TOKEN_RESPONSE_V1 = {
    "status": "active",
    "token": "compat-bearer-token-v1",
    "token_type": "Bearer",
    "expires_at": "2026-06-15T11:30:00Z",
    "scopes": ["read:context", "write:lineage"],
    "issued_at": "2026-06-15T10:30:00Z",
    "request_id": "req-compat-002",
}

# ---------------------------------------------------------------------------
# lineage.register — POST /accreditation/lineage/register
# ---------------------------------------------------------------------------

LINEAGE_REGISTER_REQUEST_V1 = {
    "run_id": "run-compat-001",
    "dwelling_id": "dwelling-compat-101",
    "pack_version": "v1.0.0",
    "initiated_by": "ci-pipeline",
    "environment": "staging",
    "metadata": {},
}

LINEAGE_REGISTER_RESPONSE_V1 = {
    "lineage_id": "lin-compat-abc123",
    "run_id": "run-compat-001",
    "status": "registered",
    "registered_at": "2026-06-15T10:30:00Z",
    "request_id": "req-compat-003",
}

# ---------------------------------------------------------------------------
# lineage.finalize — POST /accreditation/lineage/{lineage_id}/finalize
# ---------------------------------------------------------------------------

LINEAGE_FINALIZE_REQUEST_V1 = {
    "lineage_id": "lin-compat-abc123",
    "status": "finalized",
    "summary": "Accreditation run completed successfully.",
    "metrics": {"passed": 10, "failed": 0},
}

LINEAGE_FINALIZE_RESPONSE_V1 = {
    "lineage_id": "lin-compat-abc123",
    "status": "finalized",
    "finalized_at": "2026-06-15T10:45:00Z",
    "request_id": "req-compat-004",
}

# ---------------------------------------------------------------------------
# Error envelope
# ---------------------------------------------------------------------------

ERROR_RESPONSE_V1 = {
    "error": {
        "code": "not_found",
        "message": "Project not found.",
        "status_code": 404,
        "details": None,
        "request_id": "req-compat-005",
    },
    "request_id": "req-compat-005",
}

# ---------------------------------------------------------------------------
# media.compose — POST /accreditation/media/compose
# ---------------------------------------------------------------------------

MEDIA_COMPOSE_REQUEST_V1_2 = {
    "source_media_refs": ["media-floor-001", "media-elev-002"],
    "compose_type": "floor_plan",
    "output_format": "pdf",
    "parameters": {"include_annotations": True},
    "metadata": {"correlation_id": "corr-compose-001"},
}

MEDIA_COMPOSE_RESPONSE_V1_2 = {
    "compose_id": "compose-compat-001",
    "status": "complete",
    "output_media_ref": "media-compose-999",
    "composed_at": "2026-06-15T10:40:00Z",
    "partial_items": ["media-floor-001", "media-elev-002"],
    "request_id": "req-compat-006",
}

ERROR_ENVELOPE_V1_2 = {
    "code": "invalid_request",
    "message": "Validation error",
    "detail": {"output_format": "must be a supported media format"},
    "correlation_id": "corr-compat-006",
}

# ---------------------------------------------------------------------------
# All v1 payload pairs (used in regression tests)
# ---------------------------------------------------------------------------

COMPAT_V1_PAIRS = [
    ("context.resolve.request", CONTEXT_RESOLVE_REQUEST_V1),
    ("context.resolve.response", CONTEXT_RESOLVE_RESPONSE_V1),
    ("auth.service-token.request", SERVICE_TOKEN_REQUEST_V1),
    ("auth.service-token.response", SERVICE_TOKEN_RESPONSE_V1),
    ("lineage.register.request", LINEAGE_REGISTER_REQUEST_V1),
    ("lineage.register.response", LINEAGE_REGISTER_RESPONSE_V1),
    ("lineage.finalize.request", LINEAGE_FINALIZE_REQUEST_V1),
    ("lineage.finalize.response", LINEAGE_FINALIZE_RESPONSE_V1),
    ("error.response", ERROR_RESPONSE_V1),
]

# ---------------------------------------------------------------------------
# Phase 2 additive compatibility payloads (v1.1.0)
# ---------------------------------------------------------------------------

PROJECT_CREATE_REQUEST_V1_1 = {
    "name": "Project A",
    "description": "Shared contract project",
    "owner_id": "user-1",
    "metadata": {},
}

DWELLING_INPUT_V1_1 = {
    "dwelling_id": "dw-1",
    "source": "import",
    "configuration": {"climate_zone": "6", "num_storeys": 1},
    "metadata": {},
}

FLOOR_PLAN_TRACE_REQUEST_V1_1 = {
    "dwelling_id": "dw-1",
    "image_url": "https://example.com/floor.png",
    "image_format": "png",
    "extract_windows": True,
    "extract_walls": True,
    "metadata": {},
}

COMPAT_V1_1_PAIRS = [
    ("project.create.request", PROJECT_CREATE_REQUEST_V1_1),
    ("dwelling.input", DWELLING_INPUT_V1_1),
    ("ml.floor_plan.trace.request", FLOOR_PLAN_TRACE_REQUEST_V1_1),
]

COMPAT_V1_2_PAIRS = [
    ("media.compose.request", MEDIA_COMPOSE_REQUEST_V1_2),
    ("media.compose.response", MEDIA_COMPOSE_RESPONSE_V1_2),
    ("error.envelope", ERROR_ENVELOPE_V1_2),
]
