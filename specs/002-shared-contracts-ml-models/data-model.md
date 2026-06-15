# Data Model: Phase 1 Completion — Shared Contracts & ML Models

**Feature**: `002-shared-contracts-ml-models`
**Date**: 2026-06-15

---

## Overview

This document defines all new entities introduced in this feature, their fields,
relationships, validation rules, and state transitions. All existing Phase 1 entities
(Project/Environment models, Auth, Context, Lineage schemas) are unchanged.

---

## New Enums (`src/scanq_shared/enums/ml_inference.py`)

### `ConfidenceLevel`

Confidence level for ML inference outputs.

| Value | Description |
|---|---|
| `HIGH` | High-confidence prediction (≥ 0.85 threshold) |
| `MEDIUM` | Medium-confidence prediction (0.50–0.84) |
| `LOW` | Low-confidence prediction (0.20–0.49) |
| `INSUFFICIENT` | Confidence data unavailable or below minimum threshold |

**Base**: `(str, Enum)` — string values for cross-version serialization safety.

---

### `ExecutionStatus`

Current execution state for ML inference jobs and accreditation runs.

| Value | Description |
|---|---|
| `PENDING` | Job queued but not yet started |
| `RUNNING` | Job actively executing |
| `COMPLETED` | Job completed successfully |
| `FAILED` | Job terminated with errors |
| `CANCELLED` | Job cancelled before completion |

**State transitions**:
```
PENDING → RUNNING → COMPLETED
                 → FAILED
         → CANCELLED (from PENDING or RUNNING)
```

---

### `DwellingSource`

Source classification for dwelling data ingestion.

| Value | Description |
|---|---|
| `IMPORT` | Dwelling imported from external system or file |
| `MANUAL` | Dwelling created manually via UI or API |
| `SCAN` | Dwelling captured via physical scan/survey |
| `LEGACY` | Dwelling migrated from a pre-v1 system |

---

### `CrossRepoErrorCode`

Standardized error codes for cross-repository error handling (used in `ErrorSchema.code`).

| Value | HTTP Equivalent |
|---|---|
| `CONNECTION_ERROR` | 503 / network-level |
| `TIMEOUT` | 504 |
| `AUTHENTICATION_FAILED` | 401 |
| `AUTHORIZATION_DENIED` | 403 |
| `VALIDATION_ERROR` | 422 |
| `NOT_FOUND` | 404 |
| `RATE_LIMITED` | 429 |
| `INTERNAL_ERROR` | 500 |
| `UNKNOWN_ERROR` | 500 (fallback) |

---

## New Schemas — Training-Studio Service Contracts

### `ProjectCreateRequest` (`src/scanq_shared/schemas/project.py`)

Request to create a new project in training-studio.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `name` | `str` | ✅ | min_length=1, max_length=200 | Project display name |
| `description` | `str \| None` | — | max_length=2000 | Optional description |
| `owner_id` | `str` | ✅ | min_length=1 | Owner user ID |
| `metadata` | `dict[str, str]` | — | default={} | Arbitrary string metadata |

### `ProjectUpdateRequest` (`src/scanq_shared/schemas/project.py`)

Request to update an existing project. All fields optional (partial update).

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `name` | `str \| None` | — | min_length=1, max_length=200 | New project name |
| `description` | `str \| None` | — | max_length=2000 | New description |
| `metadata` | `dict[str, str] \| None` | — | — | Metadata to merge/replace |

### `ProjectResponse` (`src/scanq_shared/schemas/project.py`)

Canonical response for a project resource.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `str` | ✅ | Project unique identifier |
| `name` | `str` | ✅ | Project display name |
| `description` | `str \| None` | — | Project description |
| `owner_id` | `str` | ✅ | Owner user ID |
| `created_at` | `datetime` | ✅ | UTC creation timestamp |
| `updated_at` | `datetime` | ✅ | UTC last-update timestamp |
| `metadata` | `dict[str, Any]` | — | Additional project metadata |

### `ProjectEnvironmentResponse` (`src/scanq_shared/schemas/project.py`)

Combined project + environment resource (e.g., for context-aware listing).

| Field | Type | Required | Description |
|---|---|---|---|
| `project` | `ProjectResponse` | ✅ | Nested project resource |
| `environments` | `list[EnvironmentResponse]` | ✅ | Environments belonging to the project |
| `total_environments` | `int` | ✅ | Count of environments |

---

### `EnvironmentCreateRequest` (`src/scanq_shared/schemas/environment.py`)

Request to create an environment within a project.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `project_id` | `str` | ✅ | min_length=1 | Parent project ID |
| `name` | `str` | ✅ | min_length=1, max_length=100 | Environment name (e.g., staging) |
| `config` | `dict[str, Any]` | — | default={} | Environment configuration |

### `EnvironmentResponse` (`src/scanq_shared/schemas/environment.py`)

Canonical response for an environment resource.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `str` | ✅ | Environment unique identifier |
| `project_id` | `str` | ✅ | Parent project ID |
| `name` | `str` | ✅ | Environment name |
| `config` | `dict[str, Any]` | — | Environment configuration |
| `created_at` | `datetime` | ✅ | UTC creation timestamp |

---

### `IntakeDraftGenerateRequest` (`src/scanq_shared/schemas/intake.py`)

Request to generate an intake draft for a new accreditation candidate.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `project_id` | `str` | ✅ | min_length=1 | Target project ID |
| `environment_id` | `str` | ✅ | min_length=1 | Target environment ID |
| `source_type` | `DwellingSource` | ✅ | — | Source classification |
| `reference_id` | `str \| None` | — | — | External reference identifier |
| `metadata` | `dict[str, str]` | — | default={} | Additional intake metadata |

### `DevLoginRequest` (`src/scanq_shared/schemas/intake.py`)

Request for developer login (development/staging environments only).

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `username` | `str` | ✅ | min_length=1 | Developer username |
| `password` | `str` | ✅ | min_length=1 | Developer password |
| `environment` | `str` | ✅ | — | Target environment (e.g., staging) |

> **Note**: `DevLoginRequest` is for development environments only. Production auth
> uses `ServiceTokenRequest` (existing Phase 1 schema).

---

### `JobResponse` (`src/scanq_shared/schemas/job.py`)

Canonical response for a job resource.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `str` | ✅ | Job unique identifier |
| `project_id` | `str` | ✅ | Owning project ID |
| `environment_id` | `str` | ✅ | Target environment ID |
| `status` | `ExecutionStatus` | ✅ | Current execution status |
| `created_at` | `datetime` | ✅ | UTC creation timestamp |
| `started_at` | `datetime \| None` | — | UTC start timestamp |
| `completed_at` | `datetime \| None` | — | UTC completion timestamp |
| `metadata` | `dict[str, Any]` | — | Job metadata |
| `error` | `ErrorSchema \| None` | — | Error detail if status=FAILED |

### `ProviderProfile` (`src/scanq_shared/schemas/job.py`)

Provider profile used for job cost estimation and capability lookup.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `provider_id` | `str` | ✅ | min_length=1 | Provider unique identifier |
| `name` | `str` | ✅ | — | Display name |
| `capabilities` | `list[str]` | ✅ | — | List of capability codes |
| `active` | `bool` | ✅ | default=True | Whether provider is active |
| `metadata` | `dict[str, Any]` | — | default={} | Additional provider metadata |

### `CostEstimate` (`src/scanq_shared/schemas/job.py`)

Cost estimate for a job execution.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `job_id` | `str` | ✅ | — | Job being estimated |
| `provider_id` | `str` | ✅ | — | Provider for this estimate |
| `estimated_cost` | `float` | ✅ | ge=0 | Estimated cost in AUD (cents or decimal) |
| `currency` | `str` | — | default="AUD" | Currency code |
| `valid_until` | `datetime \| None` | — | — | Estimate expiry timestamp |

---

## New Models — Domain Entities

### `DwellingInput` (`src/scanq_shared/models/dwelling.py`)

Top-level dwelling data structure submitted for accreditation.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `dwelling_id` | `str` | ✅ | min_length=1 | Unique dwelling identifier |
| `source` | `DwellingSource` | ✅ | — | Ingestion source classification |
| `configuration` | `DwellingConfiguration` | ✅ | — | Dwelling physical configuration |
| `expected_outputs` | `DwellingExpectedOutputs \| None` | — | — | Expected accreditation outputs |
| `specification` | `SpecificationAttributes \| None` | — | — | Specification reference attributes |
| `floor_plan_features` | `FloorPlanFeatureAttributes \| None` | — | — | Extracted floor-plan features |
| `metadata` | `dict[str, Any]` | — | default={} | Additional dwelling metadata |

### `DwellingConfiguration` (`src/scanq_shared/models/dwelling.py`)

Physical and spatial configuration of a dwelling.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `address` | `str \| None` | — | max_length=500 | Street address |
| `climate_zone` | `str` | ✅ | — | NatHERS climate zone code |
| `floor_area_m2` | `float \| None` | — | gt=0 | Total floor area in m² |
| `num_bedrooms` | `int \| None` | — | ge=0 | Number of bedrooms |
| `num_storeys` | `int` | — | ge=1, default=1 | Number of storeys |
| `construction_year` | `int \| None` | — | ge=1800, le=2100 | Year of construction |
| `orientation_degrees` | `float \| None` | — | ge=0, lt=360 | Building orientation (degrees N) |

### `DwellingExpectedOutputs` (`src/scanq_shared/models/dwelling.py`)

Expected accreditation result targets for a dwelling.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `nathers_rating` | `float \| None` | — | ge=0, le=10 | Target NatHERS star rating |
| `heating_load_mj` | `float \| None` | — | ge=0 | Target heating load (MJ/m²) |
| `cooling_load_mj` | `float \| None` | — | ge=0 | Target cooling load (MJ/m²) |
| `total_load_mj` | `float \| None` | — | ge=0 | Target total load (MJ/m²) |

### `FloorPlanFeatureAttributes` (`src/scanq_shared/models/dwelling.py`)

Floor-plan-level attributes extracted from ML inference or manual entry.

| Field | Type | Required | Description |
|---|---|---|---|
| `windows` | `list[WindowAttributes]` | — | Window elements in the floor plan |
| `total_window_area_m2` | `float \| None` | — | Summed window area |
| `external_wall_area_m2` | `float \| None` | — | Total external wall area |
| `glazing_ratio` | `float \| None` | — | Window-to-wall ratio (0–1) |
| `confidence` | `ConfidenceLevel` | — | Overall extraction confidence |

### `SpecificationAttributes` (`src/scanq_shared/models/dwelling.py`)

Reference specification attributes tied to the dwelling.

| Field | Type | Required | Description |
|---|---|---|---|
| `spec_version` | `str` | ✅ | Specification version string |
| `compliance_pathway` | `str \| None` | — | NatHERS compliance pathway code |
| `assessor_id` | `str \| None` | — | Assessor identifier |
| `assessment_date` | `datetime \| None` | — | Assessment date |
| `notes` | `str \| None` | — | Free-form assessor notes |

---

### `WindowAttributes` (`src/scanq_shared/models/ml_inference.py`)

Attributes for an individual window element from floor-plan extraction.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `window_id` | `str \| None` | — | — | Optional window element ID |
| `width_m` | `float` | ✅ | gt=0 | Window width in metres |
| `height_m` | `float` | ✅ | gt=0 | Window height in metres |
| `orientation` | `str \| None` | — | — | Compass orientation (e.g., "N", "NE") |
| `glazing_type` | `str \| None` | — | — | Glazing type code |
| `frame_type` | `str \| None` | — | — | Frame material code |
| `confidence` | `ConfidenceLevel` | — | default=HIGH | Per-window extraction confidence |

**Computed property**: `area_m2 → width_m * height_m`

### `ConfidenceMetadata` (`src/scanq_shared/models/ml_inference.py`)

Per-field confidence metadata returned with ML inference responses.

| Field | Type | Required | Description |
|---|---|---|---|
| `level` | `ConfidenceLevel` | ✅ | Confidence level classification |
| `score` | `float \| None` | — | Raw confidence score (0.0–1.0) |
| `model_version` | `str \| None` | — | ML model version that produced this output |
| `notes` | `str \| None` | — | Human-readable confidence notes |

---

### `FloorPlanTraceRequest` (`src/scanq_shared/models/ml_inference.py`)

Request to perform ML floor-plan tracing.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `dwelling_id` | `str` | ✅ | min_length=1 | Dwelling being processed |
| `image_url` | `str` | ✅ | — | URL of the floor-plan image |
| `image_format` | `str` | — | default="png" | Image format (png, jpg, pdf) |
| `extract_windows` | `bool` | — | default=True | Whether to extract window elements |
| `extract_walls` | `bool` | — | default=True | Whether to extract wall elements |
| `metadata` | `dict[str, str]` | — | default={} | Additional request metadata |

### `FloorPlanTraceResponse` (`src/scanq_shared/models/ml_inference.py`)

Response from floor-plan tracing.

| Field | Type | Required | Description |
|---|---|---|---|
| `dwelling_id` | `str` | ✅ | Echoed dwelling ID |
| `status` | `ExecutionStatus` | ✅ | Tracing execution status |
| `features` | `FloorPlanFeatureAttributes \| None` | — | Extracted features (present when status=COMPLETED) |
| `confidence` | `ConfidenceMetadata` | ✅ | Overall extraction confidence |
| `processing_time_ms` | `int \| None` | — | Server-side processing time |
| `request_id` | `str \| None` | — | Request tracing ID |

---

### `NatHERSAttributeRequest` (`src/scanq_shared/models/ml_inference.py`)

Request to perform NatHERS attribute extraction from a floor plan.

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `dwelling_id` | `str` | ✅ | min_length=1 | Dwelling being processed |
| `floor_plan_features` | `FloorPlanFeatureAttributes` | ✅ | — | Extracted floor-plan features (from tracing) |
| `configuration` | `DwellingConfiguration` | ✅ | — | Dwelling physical configuration |
| `metadata` | `dict[str, str]` | — | default={} | Additional request metadata |

### `NatHERSAttributeResponse` (`src/scanq_shared/models/ml_inference.py`)

Response from NatHERS attribute extraction.

| Field | Type | Required | Description |
|---|---|---|---|
| `dwelling_id` | `str` | ✅ | Echoed dwelling ID |
| `status` | `ExecutionStatus` | ✅ | Extraction execution status |
| `predicted_rating` | `float \| None` | — | Predicted NatHERS star rating (0–10) |
| `heating_load_mj` | `float \| None` | — | Predicted heating load (MJ/m²) |
| `cooling_load_mj` | `float \| None` | — | Predicted cooling load (MJ/m²) |
| `confidence` | `ConfidenceMetadata` | ✅ | Prediction confidence |
| `processing_time_ms` | `int \| None` | — | Server-side processing time |
| `request_id` | `str \| None` | — | Request tracing ID |

---

## Relationships

```
DwellingInput
  ├─ configuration: DwellingConfiguration
  ├─ expected_outputs: DwellingExpectedOutputs
  ├─ specification: SpecificationAttributes
  └─ floor_plan_features: FloorPlanFeatureAttributes
       └─ windows[]: WindowAttributes
                └─ confidence: ConfidenceLevel

FloorPlanTraceRequest ──► FloorPlanTraceResponse
                             └─ features: FloorPlanFeatureAttributes
                             └─ confidence: ConfidenceMetadata

NatHERSAttributeRequest
  ├─ floor_plan_features: FloorPlanFeatureAttributes
  └─ configuration: DwellingConfiguration
NatHERSAttributeRequest ──► NatHERSAttributeResponse
                               └─ confidence: ConfidenceMetadata

ProjectCreateRequest ──► ProjectResponse
ProjectUpdateRequest ──► ProjectResponse
ProjectEnvironmentResponse
  ├─ project: ProjectResponse
  └─ environments[]: EnvironmentResponse

EnvironmentCreateRequest ──► EnvironmentResponse

IntakeDraftGenerateRequest (references DwellingSource enum)
JobResponse (references ExecutionStatus, ErrorSchema)
ProviderProfile + CostEstimate (job cost estimation pair)
```

---

## Validation Rules Summary

| Entity | Rule |
|---|---|
| `ProjectCreateRequest.name` | Required, 1–200 chars |
| `DwellingConfiguration.construction_year` | 1800–2100 if present |
| `DwellingConfiguration.orientation_degrees` | 0 ≤ x < 360 if present |
| `DwellingExpectedOutputs.nathers_rating` | 0–10 if present |
| `WindowAttributes.width_m`, `height_m` | Must be > 0 |
| `ConfidenceMetadata.score` | 0.0–1.0 if present |
| `NatHERSAttributeResponse.predicted_rating` | 0–10 if present |
| `CostEstimate.estimated_cost` | Must be ≥ 0 |
| `DevLoginRequest` | Non-empty username and password |
| `ServiceTokenRequest.ttl_seconds` | 60–86400 (inherited from Phase 1) |
