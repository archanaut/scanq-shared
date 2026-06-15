from datetime import datetime, timezone

import pytest

from scanq_shared.enums import ConfidenceLevel, DwellingSource
from scanq_shared.models import (
    DwellingConfiguration,
    DwellingExpectedOutputs,
    DwellingInput,
    FloorPlanFeatureAttributes,
    SpecificationAttributes,
    WindowAttributes,
)


def test_dwelling_input_required_fields():
    model = DwellingInput(
        dwelling_id="dw-1",
        source=DwellingSource.IMPORT,
        configuration=DwellingConfiguration(climate_zone="6"),
    )
    assert model.dwelling_id == "dw-1"


def test_orientation_validation():
    with pytest.raises(Exception):
        DwellingConfiguration(climate_zone="6", orientation_degrees=361)


def test_nathers_rating_validation():
    with pytest.raises(Exception):
        DwellingExpectedOutputs(nathers_rating=11)


def test_window_area_property():
    window = WindowAttributes(width_m=1.2, height_m=1.5)
    assert window.area_m2 == pytest.approx(1.8)


def test_floor_plan_insufficient_confidence_valid():
    features = FloorPlanFeatureAttributes(confidence=ConfidenceLevel.INSUFFICIENT)
    assert features.confidence == ConfidenceLevel.INSUFFICIENT


def test_specification_optional_fields():
    spec = SpecificationAttributes(
        spec_version="1.0",
        assessment_date=datetime.now(tz=timezone.utc),
    )
    assert spec.compliance_pathway is None
