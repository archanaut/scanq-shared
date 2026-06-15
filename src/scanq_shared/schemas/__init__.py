"""Schema module exports for convenience.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Export policy (Phase 1):
  - Only schemas in the fixed Phase 1 endpoint inventory are exported here.
  - Adding a new export is a MINOR change; removing one is a MAJOR change.
  - Internal/private schemas must NOT be exported from this module.
"""

from .auth import ServiceTokenRequest, ServiceTokenResponse
from .context import ContextResolveRequest, ContextResolveResponse
from .errors import ErrorResponse, ErrorSchema
from .lineage import (
    LineageFinalizeRequest,
    LineageFinalizeResponse,
    LineageRegisterRequest,
    LineageRegisterResponse,
)

__all__ = [
    "ContextResolveRequest",
    "ContextResolveResponse",
    "ServiceTokenRequest",
    "ServiceTokenResponse",
    "LineageRegisterRequest",
    "LineageRegisterResponse",
    "LineageFinalizeRequest",
    "LineageFinalizeResponse",
    "ErrorSchema",
    "ErrorResponse",
]
