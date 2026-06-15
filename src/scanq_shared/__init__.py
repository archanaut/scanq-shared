"""
scanq_shared: Shared contracts and typed clients for ScanQ ecosystem.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

This package provides:
- Pydantic models and enums for request/response contracts
- Typed HTTP clients for cross-service integration
- No routers, persistence logic, or runtime pipeline logic

Export policy:
  Adding a new top-level export is a MINOR change.
  Removing or renaming an export is a MAJOR change requiring migration notes.
"""

from . import clients, enums, models, schemas
from .version import (
    COMPATIBILITY_NOTE,
    DUAL_SUPPORT_WINDOW,
    MIN_CONSUMER_VERSION,
    PHASE1_RELEASE,
    __version__,
    __version_info__,
)

__all__ = [
    "__version__",
    "__version_info__",
    "PHASE1_RELEASE",
    "MIN_CONSUMER_VERSION",
    "DUAL_SUPPORT_WINDOW",
    "COMPATIBILITY_NOTE",
    "models",
    "schemas",
    "enums",
    "clients",
]
