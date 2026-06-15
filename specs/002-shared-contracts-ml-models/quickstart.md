# Quickstart: Phase 1 Completion — Shared Contracts & ML Models

**Feature**: `002-shared-contracts-ml-models`
**Date**: 2026-06-15

This guide documents the runnable validation scenarios that prove the feature works
end-to-end. It covers prerequisites, setup, and the expected outcomes for each
acceptance scenario.

---

## Prerequisites

- Python >= 3.14 installed
- `uv` package manager (`pip install uv` or see [uv docs](https://docs.astral.sh/uv/))
- Repository cloned and virtual environment created:

```bash
cd /path/to/scanq-shared
uv venv --python 3.14
source .venv/bin/activate
uv pip install -e ".[dev]"
```

---

## Scenario 1: Training-Studio Service Contracts Are Importable

**Validates**: FR-001, FR-002, FR-003, FR-004, SC-001, SC-005

```bash
pytest tests/contract/test_project_schemas.py -v
```

**Expected outcome**: All contract round-trip tests pass. The tests confirm that:
- `ProjectCreateRequest`, `ProjectUpdateRequest`, `ProjectResponse`, `ProjectEnvironmentResponse`
  serialize/deserialize without data loss
- `EnvironmentCreateRequest`, `EnvironmentResponse` validate correctly
- `IntakeDraftGenerateRequest`, `DevLoginRequest` accept valid payloads and reject invalid ones
- `JobResponse` with `ExecutionStatus` transitions round-trips correctly
- `ProviderProfile` and `CostEstimate` validate field constraints

---

## Scenario 2: Dwelling Models Validate Correctly

**Validates**: FR-005, SC-002, SC-005

```bash
pytest tests/contract/test_dwelling_models.py -v
```

**Expected outcome**: All dwelling model tests pass. Confirms:
- `DwellingInput` requires `dwelling_id`, `source`, and `configuration`
- `DwellingConfiguration.orientation_degrees` rejects values ≥ 360
- `DwellingExpectedOutputs.nathers_rating` rejects values outside 0–10
- `WindowAttributes.area_m2` computed property returns `width_m * height_m`
- `FloorPlanFeatureAttributes` with `ConfidenceLevel.INSUFFICIENT` is valid
- `SpecificationAttributes` accepts optional fields as `None`

---

## Scenario 3: ML Inference Contracts Round-Trip

**Validates**: FR-006, FR-007, SC-003, SC-005

```bash
pytest tests/contract/test_ml_inference_contracts.py -v
```

**Expected outcome**: All ML contract round-trip tests pass. Confirms:
- `FloorPlanTraceRequest` serializes to the expected JSON shape (see [contracts/ml-inference-endpoints.md](../contracts/ml-inference-endpoints.md))
- `FloorPlanTraceResponse` with `status=completed` and non-empty `features` deserializes correctly
- `FloorPlanTraceResponse` with `confidence.level=insufficient` and null `features` deserializes correctly
- `NatHERSAttributeRequest` accepts a `FloorPlanFeatureAttributes` input and `DwellingConfiguration`
- `NatHERSAttributeResponse` with `predicted_rating=None` (insufficient confidence) is valid

---

## Scenario 4: New Enums Are Serialization-Safe

**Validates**: FR-007, edge case 1 (unknown enum values)

```bash
pytest tests/contract/test_shared_enums.py -v
```

**Expected outcome**: Enum tests pass. Confirms:
- `ConfidenceLevel`, `ExecutionStatus`, `DwellingSource`, `CrossRepoErrorCode` all have string
  base class (values survive JSON serialization/deserialization as strings)
- `ConfidenceLevel` values: `HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`
- `ExecutionStatus` transitions: `PENDING → RUNNING → COMPLETED/FAILED/CANCELLED`

---

## Scenario 5: BaseClient Uses Exponential Backoff

**Validates**: FR-010

```bash
pytest tests/integration/test_training_studio_client_fallback_errors.py -v -k "backoff"
```

**Expected outcome**: Retry backoff tests pass. Confirms:
- On transient network failures, `BaseClient` waits between retries (exponential backoff with jitter)
- After `max_retries` exhausted, the appropriate exception (`ConnectionError` or `TimeoutError`) is raised
- No sleep is injected before the first attempt

---

## Scenario 6: MLInferenceClient Typed Methods

**Validates**: FR-009, SC-003, SC-005

```bash
pytest tests/integration/test_ml_inference_client_success.py -v
pytest tests/integration/test_ml_inference_client_errors.py -v
```

**Expected outcome**: ML client integration tests pass. Confirms:
- `MLInferenceClient.trace_floor_plan()` sends the correct JSON body and returns a typed
  `FloorPlanTraceResponse`
- `MLInferenceClient.extract_nathers_attributes()` returns a typed `NatHERSAttributeResponse`
- On 422 response, `ValidationError` (from `scanq_shared.clients.exceptions`) is raised
- On timeout, `TimeoutError` is raised
- On connection failure, `ConnectionError` is raised

---

## Scenario 7: Full Contract Validation Suite

**Validates**: SC-004 (all repositories can run CI without cross-repo schema drift)

```bash
pytest tests/ -v --tb=short
```

**Expected outcome**: All tests pass (exit code 0). Specifically:
- All Phase 1 existing tests still pass (no regressions introduced)
- All new contract tests pass
- All new integration tests pass (using mocked HTTP responses)
- `mypy src/` passes with no new type errors

```bash
mypy src/ --strict
```

---

## Scenario 8: Package Import Surface

**Validates**: SC-005 (IDE autocomplete for all Phase 1 client methods and contract models)

Run interactively in a Python REPL or in a test:

```python
# All new symbols must be importable from the documented top-level paths
from scanq_shared.schemas import (
    ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse,
    ProjectEnvironmentResponse, EnvironmentCreateRequest, EnvironmentResponse,
    IntakeDraftGenerateRequest, DevLoginRequest,
    JobResponse, ProviderProfile, CostEstimate,
)
from scanq_shared.models import (
    DwellingInput, DwellingConfiguration, DwellingExpectedOutputs,
    FloorPlanFeatureAttributes, SpecificationAttributes,
    WindowAttributes, ConfidenceMetadata,
    FloorPlanTraceRequest, FloorPlanTraceResponse,
    NatHERSAttributeRequest, NatHERSAttributeResponse,
)
from scanq_shared.enums import (
    ConfidenceLevel, ExecutionStatus, DwellingSource, CrossRepoErrorCode,
)
from scanq_shared.clients import MLInferenceClient

print("All imports OK")
```

**Expected outcome**: No `ImportError` or `ModuleNotFoundError`.

---

## References

- Data model: [data-model.md](../data-model.md)
- ML inference contract: [contracts/ml-inference-endpoints.md](../contracts/ml-inference-endpoints.md)
- Training-studio extended contract: [contracts/training-studio-extended.md](../contracts/training-studio-extended.md)
- Feature spec: [spec.md](../spec.md)

---

## Validation Evidence (2026-06-15)

- `uv run pytest -q` → **115 passed**, 0 failed
- `uv run ruff check src tests` → **passed**
- `uv run mypy src tests --strict` → **passed**

Cross-repo smoke evidence (SC-004, v1.1.0 readiness):

- **scanq-training-studio**: imports and typed methods (`resolve_context`, `get_service_token`, `register_lineage`, `finalize_lineage`) validated by integration coverage in `tests/integration/test_training_studio_client_success.py`.
- **scanq-accreditation**: dwelling contract and enum consumption validated by `tests/contract/test_dwelling_models.py` and `tests/contract/test_shared_enums.py`.
- **ml-inference service**: endpoint contract and typed client coverage validated by `tests/contract/test_ml_inference_contracts.py`, `tests/integration/test_ml_inference_client_success.py`, and `tests/integration/test_ml_inference_client_errors.py`.

Schema drift summary:

- Shared package now exports canonical project/environment/intake/job schemas, dwelling models, and ML inference contracts from `scanq_shared` package surfaces.
- Contract compatibility remains additive with MINOR bump to **1.1.0**; no Phase 1 schema removals detected.
