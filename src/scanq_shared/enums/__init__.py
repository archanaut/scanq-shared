"""Common enumeration types used across ScanQ services.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Export policy (Phase 1):
  Training-studio-specific enums are defined in ``training_studio.py``
  and re-exported here for consumer convenience.  Generic/shared enums
  (ServiceStatus, ErrorCode, EntityType) are defined directly in this
  module.

  Adding a new enum class or value is a MINOR change.
  Removing or renaming an enum class or value is a MAJOR change.
"""

from enum import Enum

# ---------------------------------------------------------------------------
# Training-studio-specific enums (canonical source: training_studio.py)
# ---------------------------------------------------------------------------

from .ml_inference import (
    ConfidenceLevel,
    CrossRepoErrorCode,
    DwellingSource,
    ExecutionStatus,
)
from .training_studio import ContextStatus, LineageEventType, TokenStatus


# ---------------------------------------------------------------------------
# Generic shared enums
# ---------------------------------------------------------------------------


class ServiceStatus(str, Enum):
    """Service health and availability status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class ErrorCode(str, Enum):
    """Standard error codes across ScanQ services."""

    INVALID_REQUEST = "invalid_request"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    TIMEOUT = "timeout"


class EntityType(str, Enum):
    """Types of entities in the ScanQ system."""

    PROJECT = "project"
    ENVIRONMENT = "environment"
    ACTOR = "actor"
    ACCREDITATION_PACK = "accreditation_pack"
    LINEAGE_RECORD = "lineage_record"


__all__ = [
    # training_studio
    "ContextStatus",
    "TokenStatus",
    "LineageEventType",
    "ConfidenceLevel",
    "ExecutionStatus",
    "DwellingSource",
    "CrossRepoErrorCode",
    # generic
    "ServiceStatus",
    "ErrorCode",
    "EntityType",
]
