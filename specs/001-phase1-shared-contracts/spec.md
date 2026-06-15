# Feature Specification: ScanQ Shared Phase 1

**Feature Branch**: `[001-phase1-shared-contracts]`

**Created**: 2026-06-15

**Status**: Draft

**Input**: User description: "Run speckit.specify for Phase 1 of scanq-shared. Scope: shared models, schemas, enums; typed client for training-studio support endpoints; migration plan for scanq-accreditation and scanq-training-studio"

## Clarifications

### Session 2026-06-15

- Q: How should Phase 1 training-studio support endpoints be scoped? -> A: Include only a fixed Phase 1 endpoint inventory agreed upfront; defer new endpoints to later phases.
- Q: Which migration strategy should be used across target repositories? -> A: Staged rollout with a time-boxed dual-support window for old and new contract imports.
- Q: What should the dual-support duration be? -> A: One release window.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Publish Shared Contracts (Priority: P1)

As a maintainer of ScanQ services, I need a single shared package of models, schemas, and enums so both producer and consumer services use one consistent contract surface.

**Why this priority**: Shared contract consistency is foundational and blocks safe cross-repository integration.

**Independent Test**: Can be fully tested by validating representative payload fixtures from dependent services against the shared schemas and enums without changing runtime service behavior.

**Acceptance Scenarios**:

1. **Given** existing service payload examples, **When** they are validated against the shared schemas, **Then** all in-scope payloads conform without service-specific schema forks.
2. **Given** contract entities used in both dependent repositories, **When** maintainers import the shared models and enums, **Then** they can replace local duplicate definitions with shared definitions.

---

### User Story 2 - Use Typed Training Studio Client (Priority: P2)

As an integration developer, I need a typed client for training-studio support endpoints so calling services use consistent request and response contracts and error handling.

**Why this priority**: Typed client integration reduces endpoint misuse and improves reliability of cross-service calls.

**Independent Test**: Can be tested by invoking each supported client operation against mocked endpoint responses and validating typed request/response parsing and shared error mapping.

**Acceptance Scenarios**:

1. **Given** a supported training-studio support endpoint contract, **When** a consumer calls the typed client with valid input, **Then** the client returns a typed response aligned with shared schemas.
2. **Given** an endpoint error response, **When** the typed client receives the error payload, **Then** it returns a standardized shared error type.

---

### User Story 3 - Execute Consumer Migration Plan (Priority: P3)

As a repository maintainer, I need a migration plan for scanq-accreditation and scanq-training-studio so both repositories can adopt the shared package with controlled backward compatibility.

**Why this priority**: Migration planning ensures adoption is coordinated and minimizes integration regressions.

**Independent Test**: Can be tested by executing documented migration steps in each target repository and confirming duplicate local contract definitions are replaced by shared package imports.

**Acceptance Scenarios**:

1. **Given** scanq-accreditation and scanq-training-studio repositories, **When** maintainers follow the migration plan, **Then** each repo completes the defined migration steps and compiles/tests with shared contracts.
2. **Given** contract version constraints in the migration plan, **When** a non-additive change is required, **Then** the plan documents required version bump and compatibility impact before rollout.

---

### Edge Cases

- What happens when endpoint responses include optional fields unknown to older consumers? The shared contracts preserve additive compatibility and migration guidance marks optional field handling expectations.
- How does system handle mixed-version consumers during migration? The migration plan defines phased adoption windows and compatibility checks for both repositories.
- What happens when training-studio support endpoint errors do not match expected schema? The typed client maps unknown errors to a standardized fallback shared error type while preserving raw diagnostic context.
- What happens if one repository misses the dual-support cutoff? The migration plan defines escalation and release-gating rules before legacy imports can be removed.

## Constitution Alignment *(mandatory)*

- This feature remains a contracts-only package change focused on shared models, schemas, enums, typed clients, and migration documentation.
- No API routers or transport runtime logic are introduced.
- No DB persistence or migration-engine behavior is introduced.
- No runtime accreditation pipeline orchestration or execution logic is introduced.
- Expected Semantic Versioning impact for this phase is **MINOR** for additive contracts and typed client surface; any non-additive change requires **MAJOR** and explicit migration notes.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide shared models for all Phase 1 in-scope entities used by scanq-accreditation and scanq-training-studio integrations.
- **FR-002**: System MUST provide shared schemas for all in-scope request and response payloads used by the typed training-studio support client.
- **FR-003**: System MUST provide shared enums for all constrained value sets used by the in-scope contracts.
- **FR-004**: System MUST expose a typed client interface for training-studio support endpoints defined as in-scope for Phase 1.
- **FR-005**: Typed client operations MUST return shared typed response models for successful outcomes.
- **FR-006**: Typed client operations MUST map error responses to shared standardized error types.
- **FR-007**: System MUST define and publish a migration plan for scanq-accreditation adoption of the shared package.
- **FR-008**: System MUST define and publish a migration plan for scanq-training-studio adoption of the shared package.
- **FR-009**: Migration plans MUST include backward-compatibility guidance and version bump classification rules for contract changes.
- **FR-010**: System MUST document deprecation guidance for local duplicate contract definitions being replaced by shared package usage.
- **FR-011**: System MUST define and freeze a named Phase 1 training-studio support endpoint inventory before implementation planning begins.
- **FR-012**: System MUST treat endpoints outside the frozen Phase 1 inventory as out of scope and defer them to subsequent phases.
- **FR-013**: Migration plans MUST use a staged rollout and define a time-boxed dual-support window where legacy and shared contract imports are both supported.
- **FR-014**: Migration plans MUST define exit criteria for ending dual-support and completing full shared-contract adoption in each target repository.
- **FR-015**: The dual-support window MUST be limited to one release window per target repository unless an exception is explicitly approved and documented.

### Key Entities *(include if feature involves data)*

- **Shared Contract Model**: Canonical representation of domain objects consumed across ScanQ repositories, including required and optional field definitions.
- **Shared Schema**: Validation definition for request/response payload shapes used by typed clients and consuming repositories.
- **Shared Enum**: Controlled value set used across contracts to prevent service-specific value drift.
- **Typed Training Studio Operation**: A typed request/response operation that maps a support endpoint interaction to shared models and standardized errors.
- **Migration Work Item**: A documented step in consumer repository adoption (imports, replacement, compatibility check, and rollout checkpoint).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of agreed Phase 1 payload fixtures from both target repositories validate against shared schemas without local schema overrides.
- **SC-002**: 100% of in-scope training-studio support endpoint operations are invokable through typed client methods with typed success and standardized error outcomes.
- **SC-003**: Both target repositories complete a documented migration dry run with all migration steps executed and no unresolved contract-definition duplication.
- **SC-004**: For Phase 1 release candidates, all detected non-additive contract changes are accompanied by explicit compatibility notes and version bump classification before release approval.
- **SC-005**: 100% of migration plans enforce a one-release dual-support window with explicit cutover and legacy-removal checkpoints.

## Assumptions

- Phase 1 scope is limited to shared models, schemas, enums, typed training-studio support client operations, and migration guidance artifacts.
- Endpoint inventory for training-studio support integration is fixed and named for Phase 1 before planning starts; additional endpoints are deferred to later phases.
- A staged migration with a time-boxed dual-support compatibility window is acceptable to both target repository maintainers.
- scanq-accreditation and scanq-training-studio maintainers can run their existing validation/test workflows during migration dry runs.
- Runtime hosting, API routing, persistence, and accreditation orchestration remain out of scope and owned by service repositories.
