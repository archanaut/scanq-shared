# Implementation Plan: ScanQ Shared Phase 1

**Branch**: `[001-phase1-shared-contracts]` | **Date**: 2026-06-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-phase1-shared-contracts/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Deliver Phase 1 of `scanq-shared` as a contracts-only package update with four
outcomes: (1) canonical shared models/schemas/enums for agreed integration
payloads, (2) typed client coverage for a fixed training-studio support endpoint
inventory, (3) migration plans for `scanq-accreditation` and
`scanq-training-studio`, and (4) a controlled compatibility release flow with a
single-release dual-support window for consumer adoption.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python >= 3.14

**Primary Dependencies**: pydantic >= 2.9.2, httpx >= 0.27.2, typing-extensions >= 4.10.0

**Storage**: N/A for this repository; no DB persistence or migrations

**Testing**: pytest >= 8.3.3, schema/model validation tests, typed-client behavior tests, compatibility tests

**Target Platform**: Python service runtimes used by ScanQ backend repositories

**Project Type**: Shared Python library/package

**Performance Goals**: Keep model/schema validation and typed-client request serialization overhead within current baseline test runtime; no service latency SLA owned by this package

**Constraints**: Contracts-only scope, fixed Phase 1 endpoint inventory, one-release dual-support migration window, SemVer compliance with explicit compatibility notes

**Scale/Scope**: Two consuming repositories (`scanq-accreditation`, `scanq-training-studio`), one typed client domain (training-studio support endpoints), additive contract expansion for Phase 1

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Scope is contracts-only package work (schemas, models, enums, typed clients, validation helpers).
- No API routers, controllers, or server bootstrap/runtime transport logic are introduced.
- No DB persistence, ORM coupling, or migration tooling/configuration is introduced.
- No runtime accreditation pipeline execution/orchestration logic is introduced.
- Semantic version impact is classified (MAJOR/MINOR/PATCH) with backward-compatibility rationale.
- Non-additive public contract changes include explicit migration notes and consumer impact.

Gate status (pre-Phase 0): PASS

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-shared-contracts/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
└── scanq_shared/
  ├── clients/
  │   ├── base.py
  │   ├── exceptions.py
  │   └── training_studio.py
  ├── enums/
  ├── models/
  ├── schemas/
  ├── types/
  └── version.py

tests/
├── conftest.py
└── fixtures/
```

**Structure Decision**: Single shared package under `src/scanq_shared` with
domain-layered subpackages (`schemas`, `models`, `enums`, `clients`) and pytest
validation under `tests/`. This structure directly matches contracts-only
governance and keeps runtime service concerns out of scope.

## Architecture Overview

1. Contract Layer: `schemas/`, `models/`, `enums/` define canonical payload and
  value contracts shared by both consumer repositories.
2. Client Layer: `clients/training_studio.py` maps fixed endpoint inventory
  operations to typed request/response contracts and shared error translation.
3. Compatibility Layer: Version metadata plus migration guidance controls
  additive vs non-additive change handling and dual-support retirement.

## Package Structure Plan

1. `schemas/`: request/response schema classes for context, auth, lineage, and
  supporting endpoint payloads in Phase 1 inventory.
2. `models/`: reusable domain models that decouple consumer logic from transport
  details while remaining persistence-agnostic.
3. `enums/`: constrained shared values to eliminate cross-repository drift.
4. `clients/`: typed integration surface for training-studio support endpoints,
  with standardized exceptions.
5. `types/`: shared aliases/protocol types used across schemas and clients.

## Release Flow

1. Contract change classification: each PR tags changes as additive (MINOR),
  non-behavioral (PATCH), or breaking (MAJOR).
2. Candidate release prep: generate compatibility notes and identify migration
  tasks for both consumer repositories.
3. Staged adoption: consumers migrate via one-release dual-support window where
  legacy and shared imports coexist.
4. Cutover gate: remove legacy contract paths only after exit criteria pass in
  each consumer repository.
5. Post-cutover: publish finalized migration status and deprecation closure
  notes.

## Testing Strategy

1. Schema/model validation tests: fixture-driven serialization and validation
  checks for all in-scope payloads.
2. Typed client behavior tests: request construction, response parsing,
  standardized error mapping, and unknown-error fallback coverage.
3. Compatibility tests: ensure additive field changes do not break previous
  fixtures and validate one-release dual-support migration assumptions.
4. Consumer migration verification: document and run migration dry-run checklists
  in both target repositories using this package version.

## Phase 0 Output: Research

`research.md` captures decisions for endpoint scoping, migration rollout model,
compatibility window, and release governance.

## Phase 1 Output: Design & Contracts

1. `data-model.md`: entity definitions and validation constraints for shared
  contracts and migration artifacts.
2. `contracts/training-studio-support.md`: fixed Phase 1 endpoint contract
  inventory and typed client operation mapping.
3. `quickstart.md`: end-to-end validation guide for package verification and
  migration dry runs.

Constitution Check (post-design): PASS

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
