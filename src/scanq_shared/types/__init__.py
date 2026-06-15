"""Type aliases and runtime type checks."""

from typing import TypeAlias

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
]
