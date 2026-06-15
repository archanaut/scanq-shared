"""ML inference domain models."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..enums import ConfidenceLevel, ExecutionStatus


class WindowAttributes(BaseModel):
    window_id: str | None = None
    width_m: float = Field(..., gt=0)
    height_m: float = Field(..., gt=0)
    orientation: str | None = None
    glazing_type: str | None = None
    frame_type: str | None = None
    confidence: ConfidenceLevel = ConfidenceLevel.HIGH

    @property
    def area_m2(self) -> float:
        return self.width_m * self.height_m


class ConfidenceMetadata(BaseModel):
    level: ConfidenceLevel
    score: float | None = Field(default=None, ge=0, le=1)
    model_version: str | None = None
    notes: str | None = None


class FloorPlanTraceRequest(BaseModel):
    dwelling_id: str = Field(..., min_length=1)
    image_url: str = Field(..., min_length=1)
    image_format: str = "png"
    extract_windows: bool = True
    extract_walls: bool = True
    metadata: dict[str, str] = Field(default_factory=dict)


class FloorPlanTraceResponse(BaseModel):
    dwelling_id: str
    status: ExecutionStatus
    features: "FloorPlanFeatureAttributes | None" = None
    confidence: ConfidenceMetadata
    processing_time_ms: int | None = Field(default=None, ge=0)
    request_id: str | None = None


class NatHERSAttributeRequest(BaseModel):
    dwelling_id: str = Field(..., min_length=1)
    floor_plan_features: "FloorPlanFeatureAttributes"
    configuration: "DwellingConfiguration"
    metadata: dict[str, str] = Field(default_factory=dict)


class NatHERSAttributeResponse(BaseModel):
    dwelling_id: str
    status: ExecutionStatus
    predicted_rating: float | None = Field(default=None, ge=0, le=10)
    heating_load_mj: float | None = Field(default=None, ge=0)
    cooling_load_mj: float | None = Field(default=None, ge=0)
    confidence: ConfidenceMetadata
    processing_time_ms: int | None = Field(default=None, ge=0)
    request_id: str | None = None


from .dwelling import DwellingConfiguration, FloorPlanFeatureAttributes  # noqa: E402

FloorPlanTraceResponse.model_rebuild()
NatHERSAttributeRequest.model_rebuild()
