# Tasks: Option E Contract Hardening for Cross-Repo Adoption

**Input**: Design documents from `/specs/003-option-e-contract-hardening/`

**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Integration and roundtrip tests are explicitly required by spec.md (FR-008, FR-009, SC-002, SC-003), so test tasks are included in each user story phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare release and fixture scaffolding used across all stories.

- [x] T001 Create v1.2.0 compatibility guide scaffold in docs/release-compatibility/v1.2.0.md
- [x] T002 Add canonical media compose and error-envelope fixture payloads in tests/fixtures/sample_payloads.py
- [x] T003 [P] Create public-export regression test module in tests/contract/test_public_exports.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core contract assets that all user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Create MediaType and MediaComposeStatus enums in src/scanq_shared/enums/accreditation.py
- [x] T005 [P] Re-export MediaType and MediaComposeStatus in src/scanq_shared/enums/__init__.py
- [x] T006 Create MediaComposeRequest and MediaComposeResponse schemas in src/scanq_shared/schemas/media_compose.py
- [x] T007 Create typed ErrorEnvelope model using ErrorCode in src/scanq_shared/schemas/errors.py
- [x] T008 Re-export ErrorEnvelope and media compose schemas in src/scanq_shared/schemas/__init__.py
- [x] T009 Update package version from 1.1.0 to 1.2.0 in pyproject.toml

**Checkpoint**: Foundation ready — user story implementation can proceed.

---

## Phase 3: User Story 1 - Stable Cross-Repo Contract Adoption (Priority: P1) 🎯 MVP

**Goal**: Ensure downstream repositories can import stable, documented contracts with no missing exports.

**Independent Test**: Install package build and confirm all context-resolve, service-token, lineage, media-compose, and error-envelope imports resolve and validate expected payloads.

### Tests for User Story 1

- [x] T010 [P] [US1] Add five-contract-area import coverage in tests/contract/test_public_exports.py
- [x] T011 [P] [US1] Add media compose schema validation tests in tests/contract/test_media_compose_contracts.py
- [x] T012 [US1] Add ErrorEnvelope typed-code and backward-compat tests in tests/contract/test_media_compose_contracts.py

### Implementation for User Story 1

- [x] T013 [US1] Document additive contract matrix for all five areas in docs/release-compatibility/v1.2.0.md
- [x] T014 [US1] Document ErrorResponse-to-ErrorEnvelope migration path in docs/release-compatibility/v1.2.0.md
- [x] T015 [US1] Add stable import examples for downstream repos in docs/release-compatibility/v1.2.0.md

**Checkpoint**: User Story 1 is independently testable for stable contract adoption.

---

## Phase 4: User Story 2 - Typed Client Coverage for Accreditation and Training-Studio Endpoints (Priority: P2)

**Goal**: Deliver typed `compose_media` client behavior with predictable success and error mappings.

**Independent Test**: Call each typed client method against stubs and verify success deserializes to typed responses while validation/server failures map to typed errors.

### Tests for User Story 2

- [x] T016 [P] [US2] Add compose_media success mapping tests in tests/integration/test_training_studio_client_success.py
- [x] T017 [P] [US2] Add compose_media validation and server-error mapping tests in tests/integration/test_training_studio_client_errors.py

### Implementation for User Story 2

- [x] T018 [US2] Implement compose_media typed method and POST wiring in src/scanq_shared/clients/training_studio.py
- [x] T019 [US2] Implement compose_media ErrorEnvelope/APIError mapping in src/scanq_shared/clients/training_studio.py
- [x] T020 [US2] Add compose_media client fixtures for integration tests in tests/fixtures/sample_payloads.py
- [x] T021 [US2] Normalize compose_media typing imports to MediaType and MediaComposeResponse in src/scanq_shared/clients/training_studio.py

**Checkpoint**: User Story 2 is independently testable for typed client usage and error handling.

---

## Phase 5: User Story 3 - Integration Tests for Typed Client Mappings and Schema Roundtrips (Priority: P3)

**Goal**: Enforce regression safety with roundtrip, unknown-enum, and release compatibility test coverage.

**Independent Test**: Run contract/integration suites against canonical fixtures and confirm all roundtrip, mapping, and compatibility scenarios pass.

### Tests for User Story 3

- [x] T022 [P] [US3] Expand all-five-area canonical fixtures for roundtrip checks in tests/fixtures/sample_payloads.py
- [x] T023 [US3] Add media-compose roundtrip assertions in tests/integration/test_shared_models_roundtrip.py
- [x] T024 [US3] Add unknown-enum graceful-handling regression in tests/integration/test_training_studio_client_errors.py
- [x] T025 [P] [US3] Add v1.x release compatibility regression suite in tests/integration/test_release_compatibility.py

### Implementation for User Story 3

- [x] T026 [US3] Add downstream verification commands and CI guidance in docs/release-compatibility/v1.2.0.md

**Checkpoint**: User Story 3 is independently testable for regression and compatibility enforcement.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finish cross-story packaging and release consistency tasks.

- [x] T027 [P] Add release adoption pointer for v1.2.0 in README.md
- [x] T028 Align pytest/packaging metadata for new contract suites in pyproject.toml
- [x] T029 [P] Normalize new export ordering in src/scanq_shared/schemas/__init__.py and src/scanq_shared/enums/__init__.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1; blocks all user stories.
- **Phase 3 (US1)**: Depends on Phase 2.
- **Phase 4 (US2)**: Depends on Phase 2 and reuses US1 contract artifacts.
- **Phase 5 (US3)**: Depends on Phases 3-4 contract/client implementation.
- **Phase 6 (Polish)**: Depends on all user stories.

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependency on other stories.
- **US2 (P2)**: Starts after Foundational; consumes schemas/enums finalized in US1.
- **US3 (P3)**: Starts after US1 and US2 to validate complete behavior and compatibility.

### Within Each User Story

- Tests are written before implementation updates in that story.
- Schema/enum/model updates precede typed-client and documentation updates.
- Story-level checkpoint must pass before moving to next priority.

### Parallel Opportunities

- Phase 1: T003 can run in parallel with T001-T002.
- Phase 2: T005 can run in parallel once T004 exists.
- US1: T010 and T011 can run in parallel.
- US2: T016 and T017 can run in parallel.
- US3: T022 and T025 can run in parallel.
- Polish: T027 and T029 can run in parallel.

---

## Parallel Example: User Story 1

```bash
Task: "T010 [US1] Add five-contract-area import coverage in tests/contract/test_public_exports.py"
Task: "T011 [US1] Add media compose schema validation tests in tests/contract/test_media_compose_contracts.py"
```

## Parallel Example: User Story 2

```bash
Task: "T016 [US2] Add compose_media success mapping tests in tests/integration/test_training_studio_client_success.py"
Task: "T017 [US2] Add compose_media validation and server-error mapping tests in tests/integration/test_training_studio_client_errors.py"
```

## Parallel Example: User Story 3

```bash
Task: "T022 [US3] Expand all-five-area canonical fixtures in tests/fixtures/sample_payloads.py"
Task: "T025 [US3] Add v1.x release compatibility regression suite in tests/integration/test_release_compatibility.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (Setup).
2. Complete Phase 2 (Foundational).
3. Complete Phase 3 (US1).
4. Validate US1 independent import/export and schema checks before expanding scope.

### Incremental Delivery

1. Foundation (Phases 1-2).
2. Deliver US1 (stable contracts + release guide).
3. Deliver US2 (typed client compose_media + error mapping).
4. Deliver US3 (regression/roundtrip/compatibility enforcement).
5. Finalize Phase 6 polish tasks.

### Parallel Team Strategy

1. Team finishes Phases 1-2 together.
2. Then split work:
   - Engineer A: US1 doc + contract tests.
   - Engineer B: US2 client implementation + integration tests.
   - Engineer C: US3 compatibility and roundtrip suites.
3. Merge with Phase 6 cross-cutting cleanup.

---

## Notes

- All tasks follow strict checklist format with Task ID, optional [P], required [USx] labels for story phases, and explicit file paths.
- Contract scope only: no runtime orchestration, persistence, or migration tasks are included.
