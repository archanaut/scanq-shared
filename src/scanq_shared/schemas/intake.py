"""Intake contracts."""

from pydantic import BaseModel, Field

from ..enums import DwellingSource


class IntakeDraftGenerateRequest(BaseModel):
    project_id: str = Field(..., min_length=1)
    environment_id: str = Field(..., min_length=1)
    source_type: DwellingSource
    reference_id: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class DevLoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    environment: str = Field(..., min_length=1)

