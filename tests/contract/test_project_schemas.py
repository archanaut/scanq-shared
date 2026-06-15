from datetime import datetime, timezone

import pytest

from scanq_shared.enums import DwellingSource, ExecutionStatus
from scanq_shared.schemas import (
    CostEstimate,
    DevLoginRequest,
    EnvironmentCreateRequest,
    EnvironmentResponse,
    IntakeDraftGenerateRequest,
    JobResponse,
    ProjectCreateRequest,
    ProjectEnvironmentResponse,
    ProjectResponse,
    ProjectUpdateRequest,
    ProviderProfile,
)


def test_project_create_validation():
    schema = ProjectCreateRequest(name="P", owner_id="u-1")
    assert schema.name == "P"
    with pytest.raises(Exception):
        ProjectCreateRequest(name="", owner_id="u-1")


def test_project_update_partial():
    schema = ProjectUpdateRequest(description="updated")
    assert schema.description == "updated"


def test_environment_roundtrip():
    env = EnvironmentResponse(
        id="env-1",
        project_id="proj-1",
        name="staging",
        config={"region": "ap-southeast-2"},
        created_at=datetime.now(tz=timezone.utc),
    )
    assert EnvironmentResponse(**env.model_dump()) == env


def test_project_environment_response():
    project = ProjectResponse(
        id="proj-1",
        name="Project",
        owner_id="owner-1",
        created_at=datetime.now(tz=timezone.utc),
        updated_at=datetime.now(tz=timezone.utc),
    )
    env = EnvironmentResponse(
        id="env-1",
        project_id="proj-1",
        name="staging",
        created_at=datetime.now(tz=timezone.utc),
    )
    combined = ProjectEnvironmentResponse(
        project=project,
        environments=[env],
        total_environments=1,
    )
    assert combined.total_environments == 1


def test_intake_and_dev_login_validation():
    req = IntakeDraftGenerateRequest(
        project_id="proj-1",
        environment_id="env-1",
        source_type=DwellingSource.IMPORT,
    )
    assert req.source_type == DwellingSource.IMPORT
    login = DevLoginRequest(username="dev", password="pw", environment="staging")
    assert login.environment == "staging"


def test_job_provider_cost_contracts():
    job = JobResponse(
        id="job-1",
        project_id="proj-1",
        environment_id="env-1",
        status=ExecutionStatus.PENDING,
        created_at=datetime.now(tz=timezone.utc),
    )
    assert job.status == ExecutionStatus.PENDING
    provider = ProviderProfile(provider_id="provider-1", name="Provider")
    assert provider.active is True
    estimate = CostEstimate(job_id="job-1", provider_id="provider-1", estimated_cost=12)
    assert estimate.currency == "AUD"
    with pytest.raises(Exception):
        CostEstimate(job_id="job-1", provider_id="provider-1", estimated_cost=-1)


def test_environment_create_request():
    req = EnvironmentCreateRequest(project_id="proj-1", name="prod")
    assert req.name == "prod"

