"""Common enumeration types used across ScanQ services."""

from enum import Enum


class ServiceStatus(str, Enum):
    """Service health and availability status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class TokenStatus(str, Enum):
    """Status of an auth service token."""

    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"


class ContextStatus(str, Enum):
    """Status of a context resolution operation."""

    RESOLVED = "resolved"
    PARTIAL = "partial"  # Some fields resolved, others not found
    NOTFOUND = "not_found"
    ERROR = "error"


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


class LineageEventType(str, Enum):
    """Types of lineage events for audit trails."""

    REGISTERED = "registered"
    UPDATED = "updated"
    FINALIZED = "finalized"
    FAILED = "failed"
    CANCELLED = "cancelled"
