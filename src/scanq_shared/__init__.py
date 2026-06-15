"""
scanq_shared: Shared contracts and typed clients for ScanQ ecosystem.

This package provides:
- Pydantic models and enums for request/response contracts
- Typed HTTP clients for cross-service integration
- No routers, persistence logic, or runtime pipeline logic
"""

from . import clients, enums, models, schemas
from .version import __version__, __version_info__

__all__ = [
    "__version__",
    "__version_info__",
    "models",
    "schemas",
    "enums",
    "clients",
]
