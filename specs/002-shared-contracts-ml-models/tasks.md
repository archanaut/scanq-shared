# Tasks: Phase 1 Completion - Shared Contracts and ML Models

**Input**: Design documents from /specs/002-shared-contracts-ml-models/

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Include contract and integration tests because the specification defines independent tests per story and measurable CI outcomes.

**Organization**: Tasks are grouped by user story so each story can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare package structure and test scaffolding for feature implementation.

- [X] T001 Create feature module stubs for new contracts in src/scanq_shared/schemas/project.py
- [X] T002 [P] Create feature module stubs for new contracts in src/scanq_shared/schemas/environment.py
- [X] T003 [P] Create feature module stubs for new contracts in src/scanq_shared/schemas/intake.py
- [X] T004 [P] Create feature module stubs for new contracts in src/scanq_shared/schemas/job.py
- [X] T005 [P] Create feature model stub for dwelling entities in src/scanq_shared/models/dwelling.py
- [X] T006 [P] Create feature model stub for ML inference entities in src/scanq_shared/models/ml_inference.py
- [X] T007 [P] Create feature enum stub for ML and cross-repo values in src/scanq_shared/enums/ml_inference.py
- [X] T008 [P] Create feature client stub for ML inference operations in src/scanq_shared/clients/ml_inference.py
- [X] T009 Create new contract and integration test files for feature scope in tests/contract/test_project_schemas.py
- [X] T010 [P] Create new contract and integration test files for feature scope in tests/contract/test_dwelling_models.py
- [X] T011 [P] Create new contract and integration test files for feature scope in tests/contract/test_ml_inference_contracts.py
- [X] T012 [P] Create ML client integration success test scaffold in tests/integration/test_ml_inference_client_success.py
- [X] T013 [P] Create ML client integration error test scaffold in tests/integration/test_ml_inference_client_errors.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared building blocks required by all user stories.

**CRITICAL**: No user story work starts until this phase is complete.

- [X] T014 Implement exponential backoff with jitter for retries in src/scanq_shared/clients/base.py
- [X] T015 Implement shared timeout/connection/validation error translation in src/scanq_shared/clients/exceptions.py
- [X] T016 Implement ConfidenceLevel, ExecutionStatus, DwellingSource, and CrossRepoErrorCode enums in src/scanq_shared/enums/ml_inference.py
- [X] T017 Export new enum symbols from package surface in src/scanq_shared/enums/__init__.py
- [X] T018 Add baseline compatibility payload fixtures for new schemas and models in tests/fixtures/compatibility_payloads.py
- [X] T019 Add baseline sample payload fixtures for new schemas and models in tests/fixtures/sample_payloads.py
- [X] T020 Add release classification assertions for additive MINOR change scope in tests/contract/test_release_classification_rules.py
- [X] T055 [P] Implement ArtifactManifest and ExecutionContext shared types for FR-007 in src/scanq_shared/types/__init__.py
- [X] T056 [P] Add contract tests for ArtifactManifest and ExecutionContext in tests/contract/test_shared_context_types.py
- [X] T057 Export ArtifactManifest and ExecutionContext from package surface in src/scanq_shared/__init__.py

**Checkpoint**: Foundation complete; user stories can begin.

---

## Phase 3: User Story 1 - Consolidate Shared Contracts (Priority: P1) MVP

**Goal**: Centralize training-studio project/environment/intake/job/provider contracts in scanq-shared.

**Independent Test**: Replace one consumer's duplicate contracts with shared imports and verify equivalent validation outcomes.

### Tests for User Story 1

- [X] T021 [P] [US1] Add contract validation tests for project and environment schemas in tests/contract/test_project_schemas.py
- [X] T022 [P] [US1] Add contract validation tests for intake and job/provider schemas in tests/contract/test_project_schemas.py
- [X] T023 [P] [US1] Add import-surface regression tests for US1 symbols in tests/integration/test_shared_models_roundtrip.py

### Implementation for User Story 1

- [X] T024 [P] [US1] Implement project request/response schemas in src/scanq_shared/schemas/project.py
- [X] T025 [P] [US1] Implement environment request/response schemas in src/scanq_shared/schemas/environment.py
- [X] T026 [P] [US1] Implement intake request schemas including dev login in src/scanq_shared/schemas/intake.py
- [X] T027 [P] [US1] Implement job response, provider profile, and cost estimate schemas in src/scanq_shared/schemas/job.py
- [X] T028 [US1] Export all new US1 schemas in src/scanq_shared/schemas/__init__.py
- [X] T029 [US1] Update training-studio extended contract mapping to implemented schema symbols in specs/002-shared-contracts-ml-models/contracts/training-studio-extended.md

**Checkpoint**: User Story 1 is complete and independently testable.

---

## Phase 4: User Story 2 - Support Accreditation Flows with Shared Types and Clients (Priority: P2)

**Goal**: Provide dwelling domain models and typed client behavior used by accreditation context/auth/lineage flows.

**Independent Test**: Validate dwelling models and execute context/token/lineage typed client flows with standardized error mapping.

### Tests for User Story 2

- [X] T030 [P] [US2] Add dwelling model validation tests including edge constraints in tests/contract/test_dwelling_models.py
- [X] T031 [P] [US2] Add cross-repo enum and unknown-value compatibility tests in tests/contract/test_shared_enums.py
- [X] T062 [P] [US2] Add explicit success-path regression tests for resolve_context and get_service_token in tests/integration/test_training_studio_client_success.py
- [X] T063 [P] [US2] Add explicit success-path regression tests for register_lineage and finalize_lineage in tests/integration/test_training_studio_client_success.py
- [X] T032 [P] [US2] Extend training-studio client error mapping tests for new cross-repo error codes in tests/integration/test_training_studio_client_errors.py
- [X] T033 [P] [US2] Extend fallback/backoff behavior tests for retry timing semantics in tests/integration/test_training_studio_client_fallback_errors.py

### Implementation for User Story 2

- [X] T034 [P] [US2] Implement DwellingInput, DwellingConfiguration, DwellingExpectedOutputs, and SpecificationAttributes in src/scanq_shared/models/dwelling.py
- [X] T035 [P] [US2] Implement FloorPlanFeatureAttributes and dwelling-linked feature structures in src/scanq_shared/models/dwelling.py
- [X] T036 [US2] Export dwelling domain models through package surface in src/scanq_shared/models/__init__.py
- [X] T037 [US2] Add regression-success coverage and maintain contract enforcement behavior for context/token/lineage methods in src/scanq_shared/clients/training_studio.py
- [X] T038 [US2] Document dwelling and enum contract expectations for accreditation consumers in specs/002-shared-contracts-ml-models/contracts/training-studio-extended.md

**Checkpoint**: User Story 2 is complete and independently testable.

---

## Phase 5: User Story 3 - Standardize ML Inference Request/Response Contracts (Priority: P3)

**Goal**: Provide ML inference request/response contracts and typed ML client methods for floor-plan tracing and NatHERS extraction.

**Independent Test**: Validate ML request/response contracts and typed client calls without model runtime implementation.

### Tests for User Story 3

- [X] T039 [P] [US3] Add floor-plan tracing and NatHERS contract round-trip tests in tests/contract/test_ml_inference_contracts.py
- [X] T040 [P] [US3] Add ML typed client success-path tests for both endpoints in tests/integration/test_ml_inference_client_success.py
- [X] T041 [P] [US3] Add ML typed client failure-path tests for validation/timeout/connection in tests/integration/test_ml_inference_client_errors.py

### Implementation for User Story 3

- [X] T042 [P] [US3] Implement WindowAttributes and ConfidenceMetadata models in src/scanq_shared/models/ml_inference.py
- [X] T043 [P] [US3] Implement FloorPlanTraceRequest and FloorPlanTraceResponse in src/scanq_shared/models/ml_inference.py
- [X] T044 [P] [US3] Implement NatHERSAttributeRequest and NatHERSAttributeResponse in src/scanq_shared/models/ml_inference.py
- [X] T045 [US3] Export ML inference models through package surface in src/scanq_shared/models/__init__.py
- [X] T046 [US3] Implement trace_floor_plan and extract_nathers_attributes typed methods in src/scanq_shared/clients/ml_inference.py
- [X] T047 [US3] Export MLInferenceClient from package entry points in src/scanq_shared/clients/__init__.py
- [X] T048 [US3] Finalize ML endpoint contract documentation to implemented model names in specs/002-shared-contracts-ml-models/contracts/ml-inference-endpoints.md

**Checkpoint**: User Story 3 is complete and independently testable.

---

## Phase 6: Polish and Cross-Cutting Concerns

**Purpose**: Final validation, release prep, and consumer-facing documentation updates.

- [X] T049 [P] Update top-level package exports for new symbols in src/scanq_shared/__init__.py
- [X] T050 [P] Update version and compatibility metadata for MINOR release bump in src/scanq_shared/version.py
- [X] T051 [P] Update usage examples and migration guidance for new contracts and client in README.md
- [X] T052 Record feature validation command outputs and pass/fail evidence in specs/002-shared-contracts-ml-models/quickstart.md
- [X] T053 Run full test suite and resolve any regressions in tests/integration/test_shared_models_roundtrip.py
- [X] T054 Run static analysis and typing checks across src/ and tests/ and update pyproject.toml only if configuration changes are required
- [X] T058 [P] Record scanq-training-studio contract-consumption smoke test evidence for scanq-shared v1.1.0 in specs/002-shared-contracts-ml-models/quickstart.md
- [X] T059 [P] Record scanq-accreditation contract-consumption smoke test evidence for scanq-shared v1.1.0 in specs/002-shared-contracts-ml-models/quickstart.md
- [X] T060 [P] Record ml-inference contract-consumption smoke test evidence for scanq-shared v1.1.0 in specs/002-shared-contracts-ml-models/quickstart.md
- [X] T061 Consolidate cross-repo schema drift check summary for SC-004 in specs/002-shared-contracts-ml-models/quickstart.md

---

## Dependencies and Execution Order

### Phase Dependencies

- Phase 1 Setup: no dependencies, start immediately.
- Phase 2 Foundational: depends on Phase 1, blocks all user stories.
- Phases 3-5 User Stories: all depend on Phase 2 completion.
- Phase 6 Polish: depends on completion of selected user stories.

### User Story Dependencies

- User Story 1 (P1): starts after foundational phase; independent from other stories.
- User Story 2 (P2): starts after foundational phase; integrates with shared enums and base client behavior from Phase 2.
- User Story 3 (P3): starts after foundational phase; depends on enum and error foundations from Phase 2, but is independently testable from US2.

### Within Each User Story

- Write tests first and confirm failure before implementation.
- Implement models/schemas before client methods.
- Export symbols after implementation.
- Update contract docs after code symbols are finalized.

## Parallel Opportunities

- Setup tasks T002-T008 and T010-T013 can run in parallel.
- Foundational tasks T015-T019 can run in parallel after T014 starts.
- Foundational FR-007 tasks T055-T056 can run in parallel after T016 starts.
- US1 implementation tasks T024-T027 can run in parallel.
- US2 test tasks T030-T033 can run in parallel.
- US2 regression-success tasks T062-T063 can run in parallel.
- US3 model tasks T042-T044 can run in parallel.
- Polish tasks T049-T051 can run in parallel.
- Cross-repo SC-004 evidence tasks T058-T060 can run in parallel.

## Parallel Example: User Story 1

- Run in parallel: T021, T022, T023.
- Run in parallel: T024, T025, T026, T027.
- Then sequence: T028 -> T029.

## Parallel Example: User Story 3

- Run in parallel: T039, T040, T041.
- Run in parallel: T042, T043, T044.
- Then sequence: T045 -> T046 -> T047 -> T048.

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate US1 independent test criteria and publish MVP package cut.

### Incremental Delivery

1. Deliver US1 contracts and schema exports.
2. Deliver US2 dwelling models and accreditation client compatibility.
3. Deliver US3 ML contracts and MLInferenceClient.
4. Finish with release/version polish and full CI validation.

### Parallel Team Strategy

1. Team completes Phase 1 and Phase 2 together.
2. After foundational completion:
   - Engineer A focuses on US1 schema set.
   - Engineer B focuses on US2 dwelling models and training-studio client alignment.
   - Engineer C focuses on US3 ML models and ML client.
3. Converge for Phase 6 release readiness and evidence capture.

## Notes

- All tasks use required checklist format: checkbox, Task ID, optional [P], required [USx] in story phases, and explicit file path.
- Story labels are used only in user story phases.
- Tasks are ordered for independent story delivery and testability.