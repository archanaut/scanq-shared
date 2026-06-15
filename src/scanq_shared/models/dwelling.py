"""Dwelling domain models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from ..enums import ConfidenceLevel, DwellingSource


class DwellingConfiguration(BaseModel):
    address: str | None = Field(default=None, max_length=500)
    climate_zone: str
    floor_area_m2: float | None = Field(default=None, gt=0)
    num_bedrooms: int | None = Field(default=None, ge=0)
    num_storeys: int = Field(default=1, ge=1)
    construction_year: int | None = Field(default=None, ge=1800, le=2100)
    orientation_degrees: float | None = Field(default=None, ge=0, lt=360)


class DwellingExpectedOutputs(BaseModel):
    nathers_rating: float | None = Field(default=None, ge=0, le=10)
    heating_load_mj: float | None = Field(default=None, ge=0)
    cooling_load_mj: float | None = Field(default=None, ge=0)
    total_load_mj: float | None = Field(default=None, ge=0)


class SpecificationAttributes(BaseModel):
    spec_version: str
    compliance_pathway: str | None = None
    assessor_id: str | None = None
    assessment_date: datetime | None = None
    notes: str | None = None


class FloorPlanFeatureAttributes(BaseModel):
    windows: list["WindowAttributes"] = Field(default_factory=list)
    total_window_area_m2: float | None = Field(default=None, ge=0)
    external_wall_area_m2: float | None = Field(default=None, ge=0)
    glazing_ratio: float | None = Field(default=None, ge=0, le=1)
    confidence: ConfidenceLevel | None = None


class DwellingInput(BaseModel):
    dwelling_id: str = Field(..., min_length=1)
    source: DwellingSource
    configuration: DwellingConfiguration
    expected_outputs: DwellingExpectedOutputs | None = None
    specification: SpecificationAttributes | None = None
    floor_plan_features: FloorPlanFeatureAttributes | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


from .ml_inference import WindowAttributes  # noqa: E402

FloorPlanFeatureAttributes.model_rebuild()
