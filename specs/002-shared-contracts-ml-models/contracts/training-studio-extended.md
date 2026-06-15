# Contract: Training-Studio Extended Endpoint Inventory

**Feature**: `002-shared-contracts-ml-models`
**Date**: 2026-06-15
**Scope**: Additional training-studio contracts extracted into `scanq-shared` as canonical schemas

---

## Overview

This document covers the Phase 1 Completion additions to the training-studio contract
set. Phase 1 already established context, auth, and lineage contracts. This feature adds
project, environment, intake, job, and provider contracts.

The implemented Pydantic schemas in `src/scanq_shared/schemas/` are the canonical definitions. This
document describes them in interface-first format.

---

## Project Endpoints

### Create Project

**Method**: `POST`
**Path**: `/projects`
**Request**: `ProjectCreateRequest`
**Response**: `ProjectResponse`

```json
// Request
{
  "name": "Accreditation Pack v2",
  "description": "Phase 2 accreditation test pack",
  "owner_id": "user-abc123",
  "metadata": {"team": "accreditation"}
}

// Response
{
  "id": "proj-xyz-001",
  "name": "Accreditation Pack v2",
  "description": "Phase 2 accreditation test pack",
  "owner_id": "user-abc123",
  "created_at": "2026-06-15T00:00:00Z",
  "updated_at": "2026-06-15T00:00:00Z",
  "metadata": {"team": "accreditation"}
}
```

### Update Project

**Method**: `PATCH`
**Path**: `/projects/{project_id}`
**Request**: `ProjectUpdateRequest` (partial — all fields optional)
**Response**: `ProjectResponse`

### Get Project with Environments

**Method**: `GET`
**Path**: `/projects/{project_id}/environments`
**Response**: `ProjectEnvironmentResponse`

```json
{
  "project": { "id": "proj-xyz-001", "name": "...", "..." : "..." },
  "environments": [
    { "id": "env-staging", "project_id": "proj-xyz-001", "name": "staging", "config": {}, "created_at": "..." }
  ],
  "total_environments": 1
}
```

---

## Environment Endpoints

### Create Environment

**Method**: `POST`
**Path**: `/projects/{project_id}/environments`
**Request**: `EnvironmentCreateRequest`
**Response**: `EnvironmentResponse`

```json
// Request
{
  "project_id": "proj-xyz-001",
  "name": "staging",
  "config": {"region": "ap-southeast-2"}
}

// Response
{
  "id": "env-staging-001",
  "project_id": "proj-xyz-001",
  "name": "staging",
  "config": {"region": "ap-southeast-2"},
  "created_at": "2026-06-15T00:00:00Z"
}
```

---

## Intake Endpoints

### Generate Intake Draft

**Method**: `POST`
**Path**: `/intake/draft`
**Request**: `IntakeDraftGenerateRequest`
**Response**: `JobResponse` (the draft generation is treated as an async job)

```json
// Request
{
  "project_id": "proj-xyz-001",
  "environment_id": "env-staging-001",
  "source_type": "import",
  "reference_id": "ext-ref-456",
  "metadata": {}
}

// Response (202 Accepted → async job)
{
  "id": "job-draft-001",
  "project_id": "proj-xyz-001",
  "environment_id": "env-staging-001",
  "status": "pending",
  "created_at": "2026-06-15T00:00:00Z",
  "started_at": null,
  "completed_at": null,
  "metadata": {"source_type": "import"},
  "error": null
}
```

### Developer Login (Non-Production Only)

**Method**: `POST`
**Path**: `/auth/dev-login`
**Request**: `DevLoginRequest`
**Response**: `ServiceTokenResponse` (existing Phase 1 schema)

> **WARNING**: This endpoint is restricted to development and staging environments.
> It MUST NOT be exposed in production. Production authentication uses service tokens
> via `ServiceTokenRequest`.

---

## Job & Provider Endpoints

### Get Job Status

**Method**: `GET`
**Path**: `/jobs/{job_id}`
**Response**: `JobResponse`

```json
{
  "id": "job-draft-001",
  "project_id": "proj-xyz-001",
  "environment_id": "env-staging-001",
  "status": "completed",
  "created_at": "2026-06-15T00:00:00Z",
  "started_at": "2026-06-15T00:00:10Z",
  "completed_at": "2026-06-15T00:00:15Z",
  "metadata": {},
  "error": null
}
```

### Get Provider Profile

**Method**: `GET`
**Path**: `/providers/{provider_id}`
**Response**: `ProviderProfile`

```json
{
  "provider_id": "provider-nathers-certified",
  "name": "NatHERS Certified Assessor",
  "capabilities": ["nathers:assess", "nathers:certify"],
  "active": true,
  "metadata": {}
}
```

### Get Cost Estimate

**Method**: `POST`
**Path**: `/jobs/{job_id}/estimate`
**Response**: `CostEstimate`

```json
{
  "job_id": "job-draft-001",
  "provider_id": "provider-nathers-certified",
  "estimated_cost": 250.00,
  "currency": "AUD",
  "valid_until": "2026-06-16T00:00:00Z"
}
```

---

## Error Contract

All error responses use the shared `ErrorResponse` envelope (Phase 1,
`src/scanq_shared/schemas/errors.py`). Error codes follow `CrossRepoErrorCode` values.

---

## Consumer Module Paths

After this feature ships, consumers import contracts as follows:

```python
# Project contracts
from scanq_shared.schemas import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectResponse,
    ProjectEnvironmentResponse,
)

# Environment contracts
from scanq_shared.schemas import EnvironmentCreateRequest, EnvironmentResponse

# Intake contracts
from scanq_shared.schemas import IntakeDraftGenerateRequest, DevLoginRequest

# Job & provider contracts
from scanq_shared.schemas import JobResponse, ProviderProfile, CostEstimate

# New enums
from scanq_shared.enums import (
    ConfidenceLevel,
    ExecutionStatus,
    DwellingSource,
    CrossRepoErrorCode,
)

# Dwelling models
from scanq_shared.models import (
    DwellingInput,
    DwellingConfiguration,
    DwellingExpectedOutputs,
    FloorPlanFeatureAttributes,
    SpecificationAttributes,
)

# ML inference models
from scanq_shared.models import (
    WindowAttributes,
    ConfidenceMetadata,
    FloorPlanTraceRequest,
    FloorPlanTraceResponse,
    NatHERSAttributeRequest,
    NatHERSAttributeResponse,
)

# ML typed client
from scanq_shared.clients import MLInferenceClient
```
