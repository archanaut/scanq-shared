# Implementation Plan: Phase 1 Completion — Shared Contracts & ML Models

**Branch**: `002-shared-contracts-ml-models` | **Date**: 2026-06-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-shared-contracts-ml-models/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Complete Phase 1 of `scanq-shared` by (1) extracting the remaining training-studio
service contracts (project, environment, intake, job, provider) into canonical shared
schemas, (2) adding accreditation-oriented dwelling domain models, (3) adding ML
inference contracts for floor-plan tracing and NatHERS attribute extraction, (4)
adding a typed `MLInferenceClient`, and (5) upgrading `BaseClient` retry logic to
use exponential backoff. All additions are additive and classified as a MINOR version
bump within v1.x.

## Technical Context

**Language/Version**: Python >= 3.14

**Primary Dependencies**: pydantic >= 2.9.2, httpx >= 0.27.2, typing-extensions >= 4.10.0

**Storage**: N/A for this repository; no DB persistence or migrations

**Testing**: pytest >= 8.3.3, pytest-asyncio >= 0.24.0; schema/model validation tests, typed-client behavior tests, compatibility/contract tests

**Target Platform**: Python service runtimes used by ScanQ backend repositories (`scanq-accreditation`, `scanq-training-studio`, ml-inference service)

**Project Type**: Shared Python library/package

**Performance Goals**: Schema validation and client serialization overhead within current pytest baseline; no service latency SLA owned by this package

**Constraints**: Contracts-only scope, no API routers/persistence/runtime logic; additive changes only within v1.x; MINOR version bump; exponential backoff must use only `httpx` + stdlib `asyncio` (no new runtime dependency)

**Scale/Scope**: Three consuming repositories; two typed client domains (training-studio, ml-inference); expanded enums and model coverage completing Phase 1 contract inventory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Scope is contracts-only package work (schemas, models, enums, typed clients, validation helpers).
- ✅ No API routers, controllers, or server bootstrap/runtime transport logic are introduced.
- ✅ No DB persistence, ORM coupling, or migration tooling/configuration is introduced.
- ✅ No runtime accreditation pipeline execution/orchestration logic is introduced.
- ✅ Semantic version impact: **MINOR** — all changes are additive new contracts and typed clients within v1.x; no public fields removed or redefined.
- ✅ No non-additive public contract changes; existing Phase 1 contracts remain unchanged.

Gate status (pre-Phase 0): **PASS**

## Project Structure

### Documentation (this feature)

```text
specs/002-shared-contracts-ml-models/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
└── scanq_shared/
    ├── clients/
    │   ├── base.py                  # MODIFY: add exponential backoff to _request()
    │   ├── exceptions.py            # existing
    │   ├── training_studio.py       # existing
    │   └── ml_inference.py          # NEW: MLInferenceClient
    ├── enums/
    │   ├── __init__.py              # MODIFY: re-export new enums
    │   ├── training_studio.py       # existing
    │   └── ml_inference.py          # NEW: ConfidenceLevel, ExecutionStatus, DwellingSource, CrossRepoErrorCode
    ├── models/
    │   ├── __init__.py              # MODIFY: re-export new models
    │   ├── training_studio.py       # existing
    │   ├── dwelling.py              # NEW: DwellingInput, DwellingConfiguration, etc.
    │   └── ml_inference.py          # NEW: FloorPlanTraceRequest/Response, NatHERSAttributeRequest/Response, etc.
    ├── schemas/
    │   ├── __init__.py              # MODIFY: re-export new schemas
    │   ├── auth.py                  # existing
    │   ├── context.py               # existing
    │   ├── errors.py                # existing
    │   ├── lineage.py               # existing
    │   ├── project.py               # NEW: ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse, ProjectEnvironmentResponse
    │   ├── environment.py           # NEW: EnvironmentCreateRequest, EnvironmentResponse
    │   ├── intake.py                # NEW: IntakeDraftGenerateRequest, DevLoginRequest
    │   └── job.py                   # NEW: JobResponse, ProviderProfile, CostEstimate
    └── types/
        └── __init__.py              # existing

tests/
├── conftest.py                      # existing
├── contract/
│   ├── test_migration_plan_requirements.py   # existing
│   ├── test_phase1_schema_fixtures.py        # existing
│   ├── test_release_classification_rules.py  # existing
│   ├── test_shared_enums.py                  # existing
│   ├── test_project_schemas.py               # NEW
│   ├── test_dwelling_models.py               # NEW
│   └── test_ml_inference_contracts.py        # NEW
├── fixtures/
│   ├── compatibility_payloads.py    # existing
│   └── sample_payloads.py           # MODIFY: add ML and dwelling samples
└── integration/
    ├── test_shared_models_roundtrip.py        # existing
    ├── test_training_studio_client_*.py       # existing
    └── test_ml_inference_client_*.py          # NEW
```

**Structure Decision**: Single shared package under `src/scanq_shared` with domain-layered
subpackages, extending the established Phase 1 layout. New modules follow the existing naming
and layering conventions exactly.

## Complexity Tracking

> No constitution violations.
