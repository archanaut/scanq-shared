"""Contract tests: Shared enum value constraints and drift prevention.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Ensures Phase 1 enum values remain stable and that no cross-repository
enum drift can occur silently.
"""


from scanq_shared.enums import (
    ConfidenceLevel,
    ContextStatus,
    CrossRepoErrorCode,
    DwellingSource,
    ErrorCode,
    ExecutionStatus,
    LineageEventType,
    TokenStatus,
)


class TestContextStatus:
    """ContextStatus must cover all Phase 1 resolution outcomes."""

    def test_required_values_present(self):
        values = {e.value for e in ContextStatus}
        assert "resolved" in values
        assert "partial" in values
        assert "not_found" in values
        assert "error" in values

    def test_is_string_enum(self):
        assert isinstance(ContextStatus.RESOLVED, str)
        assert ContextStatus.RESOLVED == "resolved"

    def test_serializes_as_string(self):
        import json
        from pydantic import BaseModel

        class M(BaseModel):
            s: ContextStatus

        m = M(s=ContextStatus.RESOLVED)
        data = json.loads(m.model_dump_json())
        assert data["s"] == "resolved"


class TestTokenStatus:
    """TokenStatus must cover all Phase 1 token lifecycle states."""

    def test_required_values_present(self):
        values = {e.value for e in TokenStatus}
        assert "active" in values
        assert "expired" in values
        assert "revoked" in values
        assert "pending" in values

    def test_is_string_enum(self):
        assert isinstance(TokenStatus.ACTIVE, str)


class TestLineageEventType:
    """LineageEventType must cover all Phase 1 lineage event states."""

    def test_required_values_present(self):
        values = {e.value for e in LineageEventType}
        assert "registered" in values
        assert "finalized" in values
        assert "failed" in values
        assert "cancelled" in values
        assert "updated" in values

    def test_is_string_enum(self):
        assert isinstance(LineageEventType.REGISTERED, str)

    def test_finalized_value(self):
        assert LineageEventType.FINALIZED == "finalized"


class TestErrorCode:
    """ErrorCode must cover the standard HTTP error classifications."""

    def test_required_values_present(self):
        values = {e.value for e in ErrorCode}
        assert "invalid_request" in values
        assert "unauthorized" in values
        assert "not_found" in values
        assert "internal_error" in values
        assert "service_unavailable" in values

    def test_is_string_enum(self):
        assert isinstance(ErrorCode.NOT_FOUND, str)


class TestEnumStability:
    """Regression guard: enum value strings must not change without a MAJOR bump."""

    def test_context_status_value_strings_frozen(self):
        assert ContextStatus.RESOLVED.value == "resolved"
        assert ContextStatus.PARTIAL.value == "partial"
        assert ContextStatus.NOTFOUND.value == "not_found"
        assert ContextStatus.ERROR.value == "error"

    def test_token_status_value_strings_frozen(self):
        assert TokenStatus.ACTIVE.value == "active"
        assert TokenStatus.EXPIRED.value == "expired"
        assert TokenStatus.REVOKED.value == "revoked"
        assert TokenStatus.PENDING.value == "pending"

    def test_lineage_event_type_value_strings_frozen(self):
        assert LineageEventType.REGISTERED.value == "registered"
        assert LineageEventType.UPDATED.value == "updated"
        assert LineageEventType.FINALIZED.value == "finalized"
        assert LineageEventType.FAILED.value == "failed"
        assert LineageEventType.CANCELLED.value == "cancelled"

    def test_error_code_value_strings_frozen(self):
        assert ErrorCode.INVALID_REQUEST.value == "invalid_request"
        assert ErrorCode.UNAUTHORIZED.value == "unauthorized"
        assert ErrorCode.NOT_FOUND.value == "not_found"
        assert ErrorCode.INTERNAL_ERROR.value == "internal_error"


class TestMlAndCrossRepoEnums:
    def test_confidence_level_values(self):
        assert {e.value for e in ConfidenceLevel} == {
            "high",
            "medium",
            "low",
            "insufficient",
        }

    def test_execution_status_values(self):
        assert {e.value for e in ExecutionStatus} == {
            "pending",
            "running",
            "completed",
            "failed",
            "cancelled",
        }

    def test_dwelling_source_values(self):
        assert {e.value for e in DwellingSource} == {
            "import",
            "manual",
            "scan",
            "legacy",
        }

    def test_cross_repo_error_code_values(self):
        assert "validation_error" in {e.value for e in CrossRepoErrorCode}
