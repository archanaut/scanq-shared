"""ML inference and cross-repository enums."""

from enum import Enum


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INSUFFICIENT = "insufficient"


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DwellingSource(str, Enum):
    IMPORT = "import"
    MANUAL = "manual"
    SCAN = "scan"
    LEGACY = "legacy"


class CrossRepoErrorCode(str, Enum):
    CONNECTION_ERROR = "connection_error"
    TIMEOUT = "timeout"
    AUTHENTICATION_FAILED = "authentication_failed"
    AUTHORIZATION_DENIED = "authorization_denied"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    RATE_LIMITED = "rate_limited"
    INTERNAL_ERROR = "internal_error"
    UNKNOWN_ERROR = "unknown_error"

