# Research: Phase 1 Completion — Shared Contracts & ML Models

**Feature**: `002-shared-contracts-ml-models`
**Date**: 2026-06-15
**Phase**: 0 — Unknowns resolved before design

---

## Decision Log

### 1. Exponential Backoff Strategy

**Decision**: Implement exponential backoff inside `BaseClient._request()` using `asyncio.sleep`
with jitter — no new runtime dependency.

**Rationale**: The current retry loop in `base.py` retries immediately without delay, which can
amplify load on a degraded service. Exponential backoff with full jitter (sleep between 0 and
`base * 2^attempt`) is the standard pattern and is achievable with only `asyncio` (stdlib).

**Formula**: `delay = random.uniform(0, base_delay * (2 ** attempt))` where `base_delay=0.5s`,
capped at `max_delay=30s`.

**Alternatives considered**:
- `tenacity` library — rejected to avoid adding a runtime dependency for a single pattern.
- Fixed delay — rejected; does not reduce thundering-herd risk.

---

### 2. ML Inference Client Endpoint Conventions

**Decision**: `MLInferenceClient` follows the identical `BaseClient` pattern as
`TrainingStudioClient`: async context manager, `_typed_request`, Pydantic request/response
models, typed method signatures.

**Rationale**: Consumers import both clients from the same namespace; consistent patterns reduce
learning overhead. The ML inference service is an internal ScanQ service with a REST/JSON API.

**Assumed endpoint paths** (confirmed by spec FR-009 + FR-003 analogy):
- `POST /ml/floor-plan/trace` — floor-plan tracing request/response
- `POST /ml/nathers/attributes` — NatHERS attribute extraction request/response

**Alternatives considered**: Separate base class for ML clients — rejected; `BaseClient` already
provides all needed infrastructure (retry, tracing, timeout, typed requests).

---

### 3. Dwelling Source Enumeration

**Decision**: `DwellingSource` enum with values `IMPORT`, `MANUAL`, `SCAN`, `LEGACY`.

**Rationale**: The spec requires dwelling source classification for accreditation workflows.
These four values cover the known ScanQ ingestion pathways based on the Phase 1 spec context.

**Alternatives considered**: Free-form string field — rejected; typed enum enables compile-time
validation and IDE autocomplete per SC-005.

---

### 4. ConfidenceLevel Enumeration

**Decision**: `ConfidenceLevel` enum: `HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`.

**Rationale**: Covers the full confidence spectrum including an explicit `INSUFFICIENT` value
for the edge case where confidence metadata is unavailable (spec edge case 3). Consumer code
can check `confidence == ConfidenceLevel.INSUFFICIENT` to apply fallback logic.

**Alternatives considered**: Float confidence score only — rejected; typed enum provides
consistent handling across consumers without floating-point comparison logic.

---

### 5. ExecutionStatus Enumeration

**Decision**: `ExecutionStatus` enum: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`.

**Rationale**: Cross-repo execution state machine needed for ML inference job tracking and
accreditation run lifecycle. These five values map directly to the lineage event types already
used in Phase 1 (`LineageEventType`) plus the running-in-progress state.

**Alternatives considered**: Reusing `LineageEventType` — rejected; `LineageEventType` models
audit events (past tense), not current execution state. Separate enum keeps semantic clarity.

---

### 6. Cross-Repo Error Codes

**Decision**: `CrossRepoErrorCode` enum with standardized string values covering network,
authentication, validation, and timeout failure categories.

**Rationale**: FR-007 requires cross-repo error codes; FR-010 requires standardized error
mapping. An enum with string values enables serialization-friendly comparison and prevents
typo-based code mismatches across repositories.

**Values**: `CONNECTION_ERROR`, `TIMEOUT`, `AUTHENTICATION_FAILED`, `AUTHORIZATION_DENIED`,
`VALIDATION_ERROR`, `NOT_FOUND`, `RATE_LIMITED`, `INTERNAL_ERROR`, `UNKNOWN_ERROR`.

**Alternatives considered**: Free-form string constants module — rejected; enum enforces the
valid code set and enables IDE completion per SC-005.

---

### 7. Schema Module Split (schemas/ vs models/)

**Decision**: Keep the existing Phase 1 layering convention:
- `schemas/` — request/response payload contracts for service API boundaries
- `models/` — domain data structures used internally and across services

New additions follow this split:
- `schemas/project.py`, `schemas/environment.py`, `schemas/intake.py`, `schemas/job.py` —
  API request/response shapes
- `models/dwelling.py`, `models/ml_inference.py` — domain entity models

**Rationale**: Consistent with Phase 1 structure; consumers can import from the correct semantic
layer (`from scanq_shared.schemas import ProjectCreateRequest` vs
`from scanq_shared.models import DwellingInput`).

---

### 8. Version Bump Classification

**Decision**: **MINOR** version bump (1.0.0 → 1.1.0).

**Rationale**: All changes in this feature are additive — new modules, new symbols, no removals
or redefinitions of existing public contracts. Per the constitution (Principle V) and SemVer,
new backward-compatible capabilities MUST use MINOR.

**Migration note**: None required for existing consumers; new imports are opt-in.

---

### 9. Unknown Enum Value Handling (Edge Case 1)

**Decision**: All enums inherit from `(str, Enum)` (matching Phase 1 convention). Consumers
receive unknown values as raw strings when the enum is used without strict validation. Pydantic
models that accept enum fields use `use_enum_values=True` or allow string passthrough where
cross-version compatibility requires it.

**Rationale**: Edge case 1 in the spec: "How are consumers expected to handle unknown enum values
returned by an upstream service while preserving v1.x compatibility?" — `str` base class lets
the string value survive deserialization even if the enum member is unknown, allowing consumers
to apply defensive handling.

---

### 10. Optional Fields in Legacy Payloads (Edge Case 2)

**Decision**: All new schema fields that may be absent from legacy payloads are declared with
`default=None` or `default_factory`. Required fields are those confirmed to be always present
in the Phase 1 endpoint inventory.

**Rationale**: Edge case 2: "What happens when optional fields are omitted from legacy payloads
that must remain valid in patch releases?" — Pydantic v2 model validation accepts missing
optional fields with `None` defaults; no `model_config` changes needed.

---

## All NEEDS CLARIFICATION: Resolved

No open unknowns remain. All technical context items confirmed from:
- Phase 1 codebase (`src/scanq_shared/`)
- `pyproject.toml` dependency versions
- `specs/001-phase1-shared-contracts/` artifacts
- Feature spec (FR-001 through FR-013)
