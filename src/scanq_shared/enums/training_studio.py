"""Training-studio-specific enumeration types.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

These enums are scoped to training-studio support endpoint contracts.
They are re-exported from ``scanq_shared.enums`` for consumer convenience.
"""

from enum import Enum


class ContextStatus(str, Enum):
    """Status of a context resolution operation."""

    RESOLVED = "resolved"
    PARTIAL = "partial"
    NOTFOUND = "not_found"
    ERROR = "error"


class TokenStatus(str, Enum):
    """Status of an auth service token."""

    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"


class LineageEventType(str, Enum):
    """Types of lineage events for audit trails."""

    REGISTERED = "registered"
    UPDATED = "updated"
    FINALIZED = "finalized"
    FAILED = "failed"
    CANCELLED = "cancelled"
