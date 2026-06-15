"""Type aliases and runtime type checks.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.
"""

from typing import NotRequired, TypeAlias, TypedDict

# UUID-like identifiers
ServiceID: TypeAlias = str
ProjectID: TypeAlias = str
EnvironmentID: TypeAlias = str
ActorID: TypeAlias = str
LineageID: TypeAlias = str
RunID: TypeAlias = str

# Status and codes
StatusCode: TypeAlias = str
ErrorCode: TypeAlias = str

# HTTP
HttpMethod: TypeAlias = str
HttpStatus: TypeAlias = int


class ArtifactManifest(TypedDict):
    artifact_id: str
    artifact_type: str
    uri: str
    checksum: NotRequired[str]
    metadata: NotRequired[dict[str, str]]


class ExecutionContext(TypedDict):
    run_id: str
    project_id: str
    environment_id: str
    initiated_by: str
    request_id: NotRequired[str]
    tags: NotRequired[dict[str, str]]

__all__ = [
    "ServiceID",
    "ProjectID",
    "EnvironmentID",
    "ActorID",
    "LineageID",
    "RunID",
    "StatusCode",
    "ErrorCode",
    "HttpMethod",
    "HttpStatus",
    "ArtifactManifest",
    "ExecutionContext",
]
