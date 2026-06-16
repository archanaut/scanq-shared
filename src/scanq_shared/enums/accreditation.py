"""Accreditation-specific enumeration types."""

from enum import Enum


class MediaType(str, Enum):
    """Types of media accepted by media-compose."""

    FLOOR_PLAN = "floor_plan"
    ELEVATION = "elevation"
    SITE_PLAN = "site_plan"
    PHOTOGRAPH = "photograph"


class MediaComposeStatus(str, Enum):
    """Lifecycle states for media-compose jobs."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"
