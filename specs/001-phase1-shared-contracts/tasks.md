# Tasks: ScanQ Shared Phase 1

**Input**: Design documents from /specs/001-phase1-shared-contracts/

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Include contract and integration tests because the specification requires independently testable stories and measurable outcomes.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization for Phase 1 implementation and validation.

- [X] T001 Create contract test directories in tests/contract/ and tests/integration/ (done when both directories exist with an empty __init__.py or .gitkeep)
- [X] T002 Create migration planning directory in specs/001-phase1-shared-contracts/migrations/ (done when directory exists with a placeholder README.md listing expected runbook files)
- [X] T003 [P] Add Phase 1 endpoint inventory anchor section in specs/001-phase1-shared-contracts/contracts/training-studio-support.md
- [X] T004 [P] Add SemVer release-note checklist section in specs/001-phase1-shared-contracts/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core constraints and compatibility baseline required before story work.

**⚠️ CRITICAL**: No user story work begins until this phase completes.

- [X] T005 Freeze Phase 1 operation inventory IDs and paths in specs/001-phase1-shared-contracts/contracts/training-studio-support.md
- [X] T006 [P] Define compatibility classification matrix in specs/001-phase1-shared-contracts/research.md
- [X] T007 [P] Add common error envelope contracts in src/scanq_shared/schemas/errors.py
- [X] T008 Add package export policy for shared contracts in src/scanq_shared/__init__.py
- [X] T009 Add version compatibility constants for one-release window in src/scanq_shared/version.py
- [X] T010 Create compatibility regression fixtures in tests/fixtures/compatibility_payloads.py
- [X] T011 Create deferred endpoint backlog in specs/001-phase1-shared-contracts/contracts/deferred-endpoints.md and cross-link it from specs/001-phase1-shared-contracts/contracts/training-studio-support.md

**Checkpoint**: Foundational baseline complete.

---

## Phase 3: User Story 1 - Publish Shared Contracts (Priority: P1) 🎯 MVP

**Goal**: Deliver canonical shared models, schemas, and enums for the fixed Phase 1 scope.

**Independent Test**: Validate agreed payload fixtures against shared schemas/enums with no service-specific schema forks.

### Tests for User Story 1

- [X] T012 [P] [US1] Add schema fixture validation tests in tests/contract/test_phase1_schema_fixtures.py
- [X] T013 [P] [US1] Add enum drift/value constraint tests in tests/contract/test_shared_enums.py
- [X] T014 [P] [US1] Add shared model roundtrip serialization tests in tests/integration/test_shared_models_roundtrip.py

### Implementation for User Story 1

- [X] T015 [P] [US1] Implement or update shared enum definitions in src/scanq_shared/enums/training_studio.py
- [X] T016 [US1] Export Phase 1 enums in src/scanq_shared/enums/__init__.py
- [X] T017 [P] [US1] Implement shared contract models in src/scanq_shared/models/training_studio.py
- [X] T018 [US1] Export shared models in src/scanq_shared/models/__init__.py
- [X] T019 [P] [US1] Implement context schemas for fixed inventory in src/scanq_shared/schemas/context.py
- [X] T020 [P] [US1] Implement auth schemas for fixed inventory in src/scanq_shared/schemas/auth.py
- [X] T021 [P] [US1] Implement lineage schemas for fixed inventory in src/scanq_shared/schemas/lineage.py
- [X] T022 [US1] Export Phase 1 schemas in src/scanq_shared/schemas/__init__.py
- [X] T023 [US1] Align inventory contract references to concrete schema names in specs/001-phase1-shared-contracts/contracts/training-studio-support.md

**Checkpoint**: User Story 1 is independently functional and testable.

---

## Phase 4: User Story 2 - Use Typed Training Studio Client (Priority: P2)

**Goal**: Provide typed client operations for the fixed endpoint inventory with standardized error mapping.

**Independent Test**: Invoke each supported client operation with mocks and verify typed success and standardized error outcomes.

### Tests for User Story 2

- [X] T024 [P] [US2] Add typed client success-path tests in tests/integration/test_training_studio_client_success.py
- [X] T025 [P] [US2] Add standardized error mapping tests in tests/integration/test_training_studio_client_errors.py
- [X] T026 [P] [US2] Add unknown-error fallback tests in tests/integration/test_training_studio_client_fallback_errors.py

### Implementation for User Story 2

- [X] T027 [US2] Align shared client exception classes with error envelope in src/scanq_shared/clients/exceptions.py
- [X] T028 [US2] Add reusable typed request helper and translation hook in src/scanq_shared/clients/base.py
- [X] T029 [US2] Implement fixed-inventory operation methods in src/scanq_shared/clients/training_studio.py
- [X] T030 [US2] Export typed client entry points in src/scanq_shared/clients/__init__.py
- [X] T031 [US2] Document operation-to-schema mapping in specs/001-phase1-shared-contracts/contracts/training-studio-support.md

**Checkpoint**: User Story 2 is independently functional and testable.

---

## Phase 5: User Story 3 - Execute Consumer Migration Plan (Priority: P3)

**Goal**: Produce and execute migration plans for both target repositories with one-release dual-support and explicit cutover criteria.

**Independent Test**: Run migration dry runs in each target repository and verify duplicate local definitions are replaced by shared imports.

### Tests for User Story 3

- [X] T032 [P] [US3] Add migration plan field validation tests in tests/contract/test_migration_plan_requirements.py
- [X] T033 [P] [US3] Add SemVer classification rule tests in tests/contract/test_release_classification_rules.py

### Implementation for User Story 3

- [X] T034 [US3] Create migration runbook for scanq-training-studio in specs/001-phase1-shared-contracts/migrations/scanq-training-studio.md
- [X] T035 [US3] Create migration runbook for scanq-accreditation in specs/001-phase1-shared-contracts/migrations/scanq-accreditation.md
- [X] T036 [US3] Add one-release dual-support exit criteria and rollback/escalation gates in specs/001-phase1-shared-contracts/quickstart.md
- [X] T037 [US3] Add deprecation and legacy import removal sequencing in specs/001-phase1-shared-contracts/research.md
- [X] T038 [US3] Execute migration dry run in scanq-training-studio and capture outcomes in specs/001-phase1-shared-contracts/migrations/scanq-training-studio.md
- [X] T039 [US3] Execute migration dry run in scanq-accreditation and capture outcomes in specs/001-phase1-shared-contracts/migrations/scanq-accreditation.md

**Checkpoint**: User Story 3 is independently actionable and testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final release-readiness and cross-story quality checks.

- [X] T040 [P] Update package usage and migration notes in README.md
- [X] T041 Run full validation suite (`uv run pytest -q`, `ruff check src tests`, `mypy src`) and append a signed-off evidence block to specs/001-phase1-shared-contracts/quickstart.md that records exit codes, test counts, and any failures (done when all three commands pass with zero errors and evidence is committed)
- [X] T042 [P] Run lint checks (`ruff check src tests`) and record command, exit code, and output summary in specs/001-phase1-shared-contracts/quickstart.md
- [X] T043 [P] Run type checks (`mypy src`) and record command, exit code, and output summary in specs/001-phase1-shared-contracts/quickstart.md
- [X] T044 Verify release bump recommendation and compatibility notes in specs/001-phase1-shared-contracts/research.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): No dependencies; starts immediately.
- Foundational (Phase 2): Depends on Setup completion; blocks all stories.
- User Story phases (Phases 3-5): Depend on Foundational completion.
- Polish (Phase 6): Depends on completion of desired stories.

### User Story Dependencies

- User Story 1 (P1): Starts after Phase 2; no story dependency.
- User Story 2 (P2): Starts after Phase 2 and depends on US1 schema/model exports.
- User Story 3 (P3): Starts after Phase 2 and depends on stable US1/US2 contract outputs.

### Within Each User Story

- Tests first, confirm fail, then implement.
- Contracts/models before client and migration integration.
- Complete story checkpoint before moving on.

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel.
- Foundational tasks T006 and T007 can run in parallel.
- US1 tests T012-T014 can run in parallel.
- US1 schema implementations T019-T021 can run in parallel.
- US2 tests T024-T026 can run in parallel.
- US3 validations T032-T033 can run in parallel.
- US3 migration dry runs T038-T039 can run in parallel when both repositories are available.
- Polish tasks T040, T042, T043 can run in parallel.

---

## Parallel Example: User Story 2

```bash
# Run tests in parallel:
Task: "T024 Add typed client success-path tests in tests/integration/test_training_studio_client_success.py"
Task: "T025 Add standardized error mapping tests in tests/integration/test_training_studio_client_errors.py"
Task: "T026 Add unknown-error fallback tests in tests/integration/test_training_studio_client_fallback_errors.py"

# Then implement client updates:
Task: "T027 Align shared client exception classes in src/scanq_shared/clients/exceptions.py"
Task: "T028 Add typed request helper in src/scanq_shared/clients/base.py"
Task: "T029 Implement inventory methods in src/scanq_shared/clients/training_studio.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate SC-001 before continuing.

### Incremental Delivery

1. Deliver shared contracts (US1).
2. Deliver typed client coverage (US2).
3. Deliver and execute migration plans (US3).
4. Finish polish and release-readiness checks.

### Parallel Team Strategy

1. Complete Setup + Foundational together.
2. After Phase 2:
   - Developer A: US1
   - Developer B: US2
   - Developer C: US3
3. Converge on Phase 6 evidence and release gates.

---

## Notes

- Every task follows required checklist format.
- Story labels are used only in user story phases.
- Task descriptions include exact file paths for direct execution.
