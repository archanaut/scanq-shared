# Implementation Plan: Option E Contract Hardening for Cross-Repo Adoption

**Branch**: `003-option-e-contract-hardening` | **Date**: 2026-06-16 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-option-e-contract-hardening/spec.md`

## Summary

Complete Option E contract hardening for cross-repo adoption by adding the missing
`MediaComposeRequest`/`MediaComposeResponse` schemas and `compose_media` typed client
method, introducing a strict `ErrorEnvelope` schema that uses the typed `ErrorCode`
enum, adding `MediaType` and `MediaComposeStatus` enums, extending integration and
roundtrip tests to cover all five contract areas, and publishing a release
compatibility guide for v1.2.0. All additions are additive within v1.x and classified
as a MINOR version bump (1.1.0 → 1.2.0).

## Technical Context

**Language/Version**: Python >= 3.14

**Primary Dependencies**: pydantic >= 2.9.2, httpx >= 0.27.2, typing-extensions >= 4.10.0

**Storage**: N/A for this repository; no DB persistence or migrations

**Testing**: pytest >= 8.3.3, pytest-asyncio >= 0.24.0; schema/model validation tests,
typed-client integration tests, roundtrip serialization tests, release compatibility tests

**Target Platform**: Python service runtimes consuming `scanq-shared` — `scanq-accreditation`,
`scanq-training-studio`, accreditation frontend

**Project Type**: Shared Python library/package

**Performance Goals**: Schema validation and client serialization overhead within existing
pytest baseline; no service latency SLA owned by this package

**Constraints**: Contracts-only scope; no API routers/persistence/runtime logic; all
changes are additive within v1.x; MINOR version bump only; existing exports must not be
removed or modified

**Scale/Scope**: Five contract areas; one new typed client method; new enums; expanded
integration and roundtrip test suites; one compatibility guide document

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Scope is contracts-only package work (schemas, enums, typed client additions, tests, docs).
- ✅ No API routers, controllers, or server bootstrap/runtime transport logic are introduced.
- ✅ No DB persistence, ORM coupling, or migration tooling/configuration is introduced.
- ✅ No runtime accreditation pipeline execution/orchestration logic is introduced.
- ✅ Semantic version impact: **MINOR** — all changes are additive new schemas, enums,
  typed client methods, and tests within v1.x; no public fields removed or redefined.
- ✅ No non-additive public contract changes; all existing Phase 1/2 contracts remain unchanged.

Gate status (pre-Phase 0): **PASS**

## Gap Analysis

### What Already Exists (from spec 002 / v1.1.0)

| Contract Area | Schemas | Typed Client | Integration Tests | Roundtrip Tests |
|---|---|---|---|---|
| Context Resolve | ✅ `context.py` | ✅ `TrainingStudioClient.resolve_context` | ✅ | ✅ |
| Service Token | ✅ `auth.py` | ✅ `TrainingStudioClient.get_service_token` | ✅ | ✅ |
| Lineage Register | ✅ `lineage.py` | ✅ `TrainingStudioClient.register_lineage` | ✅ | ✅ |
| Lineage Finalize | ✅ `lineage.py` | ✅ `TrainingStudioClient.finalize_lineage` | ✅ | ✅ |
| Media Compose | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing |
| ErrorEnvelope (typed) | ⚠️ `ErrorResponse` uses `str` code | N/A | ⚠️ Partial | ⚠️ Partial |

### What Must Be Added for spec 003

| Deliverable | FR | Status |
|---|---|---|
| `MediaType` enum | FR-007 | ❌ |
| `MediaComposeStatus` enum | FR-007 | ❌ |
| `MediaComposeRequest` schema | FR-004 | ❌ |
| `MediaComposeResponse` schema | FR-004 | ❌ |
| `ErrorEnvelope` schema with typed `ErrorCode` | FR-005 | ❌ |
| `compose_media` typed client method | FR-006 | ❌ |
| Media compose integration tests (success + 2 error) | FR-008 | ❌ |
| Media compose roundtrip tests | FR-009 | ❌ |
| Unknown enum graceful-handling test | FR-008 / edge | ❌ |
| Release compatibility guide (v1.2.0) | FR-010 | ❌ |
| Version bump 1.1.0 → 1.2.0 | FR-012 | ❌ |

### Key Design Decisions

1. **`ErrorEnvelope` vs `ErrorResponse`**: `ErrorResponse` (code: `str`) is retained
   unchanged to preserve backward compatibility. A new `ErrorEnvelope` schema is added
   alongside it, using the already-exported `ErrorCode` enum for its `code` field. Both
   are exported from `schemas/__init__.py`. Downstream consumers migrate to `ErrorEnvelope`
   at their own pace; `ErrorResponse` is never removed within v1.x.

2. **Media compose client method**: Added to `TrainingStudioClient` (same service cluster
   as accreditation endpoints). Endpoint path: `POST /accreditation/media/compose`.

3. **`MediaType` and `MediaComposeStatus` enums**: Defined in a new
   `enums/accreditation.py` module and re-exported from `enums/__init__.py`, consistent
   with the existing domain-layered enum convention.

4. **Release compatibility guide**: Delivered as `docs/release-compatibility/v1.2.0.md`.
   Covers all five contract areas, change type (additive/new), and recommended migration
   actions for downstream consumers.

## Project Structure

### Documentation (this feature)

```text
specs/003-option-e-contract-hardening/
├── plan.md              # This file (/speckit.plan command output)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code Changes

```text
src/scanq_shared/
├── enums/
│   ├── __init__.py              # MODIFY: re-export MediaType, MediaComposeStatus
│   └── accreditation.py         # NEW: MediaType, MediaComposeStatus enums
├── schemas/
│   ├── __init__.py              # MODIFY: export ErrorEnvelope, MediaComposeRequest/Response
│   ├── errors.py                # MODIFY: add ErrorEnvelope (keep ErrorResponse intact)
│   └── media_compose.py         # NEW: MediaComposeRequest, MediaComposeResponse
└── clients/
    └── training_studio.py       # MODIFY: add compose_media() typed client method

pyproject.toml                   # MODIFY: version 1.1.0 → 1.2.0

docs/
└── release-compatibility/
    └── v1.2.0.md                # NEW: release compatibility guide
```

### Test Changes

```text
tests/
├── contract/
│   └── test_media_compose_contracts.py   # NEW: media compose schema + enum tests
├── fixtures/
│   └── sample_payloads.py                # MODIFY: add media compose fixtures
└── integration/
    ├── test_training_studio_client_success.py   # MODIFY: add compose_media success tests
    ├── test_training_studio_client_errors.py    # MODIFY: add compose_media error tests
    └── test_shared_models_roundtrip.py          # MODIFY: add media compose roundtrip + unknown enum tests
```

## Enum Designs

### `MediaType` (new — `enums/accreditation.py`)

| Value | String |
|---|---|
| `FLOOR_PLAN` | `"floor_plan"` |
| `ELEVATION` | `"elevation"` |
| `SITE_PLAN` | `"site_plan"` |
| `PHOTOGRAPH` | `"photograph"` |

### `MediaComposeStatus` (new — `enums/accreditation.py`)

| Value | String |
|---|---|
| `PENDING` | `"pending"` |
| `PROCESSING` | `"processing"` |
| `COMPLETE` | `"complete"` |
| `FAILED` | `"failed"` |

## Schema Designs

### `ErrorEnvelope` (additive — `schemas/errors.py`)

```python
class ErrorEnvelope(BaseModel):
    code: ErrorCode          # typed enum — ErrorCode from enums/__init__.py
    message: str             # human-readable message
    detail: Any | None       # optional structured payload (replaces dict-only details)
    correlation_id: str | None  # optional correlation identifier
```

*Does not replace `ErrorResponse`; both are exported.*

### `MediaComposeRequest` (new — `schemas/media_compose.py`)

```python
class MediaComposeRequest(BaseModel):
    source_media_refs: list[str]   # ordered list of source media identifiers
    compose_type: MediaType        # typed enum
    output_format: str             # e.g. "pdf", "png"
    parameters: dict[str, Any]     # compose-specific parameters (optional, default {})
    metadata: dict[str, Any]       # caller-supplied context (optional, default {})
```

### `MediaComposeResponse` (new — `schemas/media_compose.py`)

```python
class MediaComposeResponse(BaseModel):
    compose_id: str                     # assigned compose job identifier
    status: MediaComposeStatus          # typed enum
    output_media_ref: str | None        # present when status=COMPLETE
    composed_at: datetime | None        # present when status=COMPLETE
    partial_items: list[str]            # IDs of items confirmed (for partial responses)
    request_id: str | None              # tracing identifier
```

### `compose_media` typed client method (new — `clients/training_studio.py`)

```python
async def compose_media(
    self,
    source_media_refs: list[str],
    compose_type: str | MediaType,
    output_format: str = "pdf",
    parameters: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> MediaComposeResponse:
    ...  # POST /accreditation/media/compose
```

## Integration Test Coverage Plan

| Client Method | Success Tests | Error Tests |
|---|---|---|
| `compose_media` | returns `MediaComposeResponse` with `MediaComposeStatus.COMPLETE`; verifies `compose_id` and `output_media_ref` | validation error (missing required field → `ValidationError`); server error (500 → `APIError` with `ErrorCode`); partial response (status=PENDING) |
| All 5 areas combined | — | unknown enum value in response does not raise (graceful handling) |

## Roundtrip Test Coverage Plan

All five contract areas validated with serialize → deserialize → re-serialize cycle:
- Fixture payload provided for each request and response schema
- Required fields verified to be present after roundtrip
- Optional fields verified to be `None` when absent
- Additional test: `MediaComposeResponse` with `partial_items` list

## Release Compatibility Guide Outline (`docs/release-compatibility/v1.2.0.md`)

1. Overview (MINOR bump, additive only)
2. New symbols per contract area
3. `ErrorEnvelope` vs `ErrorResponse` — migration path, no forced change in v1.x
4. `MediaCompose` area — how to import and use
5. New enums: `MediaType`, `MediaComposeStatus` — stable module paths
6. Affected downstream repos: `scanq-accreditation`, `scanq-training-studio`, accreditation frontend
7. Verification steps for downstream integrators

## Complexity Tracking

> No constitution violations. All additions are strictly additive within v1.x contracts-only
> scope. No runtime, persistence, or pipeline logic introduced.
