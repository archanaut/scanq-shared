# Feature Specification: Phase 1 Completion - Shared Contracts and ML Models

**Feature Branch**: `[002-shared-contracts-ml-models]`

**Created**: 2026-06-15

**Status**: Draft

**Input**: User description: "Create a feature specification for scanq-shared Phase 1 Completion: Extract Training-Studio Contracts & Add ML Request/Response Models."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consolidate Shared Contracts (Priority: P1)

As a platform developer, I need contract models currently duplicated across services to be centralized in scanq-shared so each service can import the same request, response, and enum definitions.

**Why this priority**: Eliminating duplication is the prerequisite for consistency, compatibility, and low-risk cross-repo integration.

**Independent Test**: Can be fully tested by replacing duplicate contract definitions in one consumer service with imports from scanq-shared and confirming no contract behavior changes.

**Acceptance Scenarios**:

1. **Given** training-studio currently defines project, environment, intake, auth, job, and provider contracts locally, **When** the Phase 1 shared package is published, **Then** those contracts are available from scanq-shared under documented module paths.
2. **Given** a consumer imports extracted contracts from scanq-shared, **When** existing payloads are validated, **Then** validation outcomes remain equivalent to previous behavior for v1-compatible use cases.

---

### User Story 2 - Support Accreditation Flows with Shared Types and Clients (Priority: P2)

As an accreditation developer, I need standardized dwelling data models and typed client methods to resolve context, request service auth, and register lineage without redefining contracts.

**Why this priority**: Accreditation integration depends on shared contract semantics and typed cross-service interactions, but can follow once core extraction exists.

**Independent Test**: Can be tested by implementing only accreditation-facing shared models and typed client methods, then executing context resolution and lineage registration flows against existing service endpoints.

**Acceptance Scenarios**:

1. **Given** accreditation has a dwelling workflow with multiple source types, **When** it constructs dwelling payloads using shared models, **Then** payloads validate consistently and include required source and feature attributes.
2. **Given** accreditation calls shared typed client methods for context, token issuance, and lineage, **When** requests succeed or fail, **Then** responses and errors follow shared contract and error-code definitions.

---

### User Story 3 - Standardize ML Inference Request/Response Contracts (Priority: P3)

As an ML integration developer, I need floor-plan tracing and NatHERS attribute contracts in scanq-shared so model services and consumers exchange strongly typed, version-compatible payloads.

**Why this priority**: ML contracts are critical for end-to-end feature completeness but depend on the shared package foundation established in higher-priority stories.

**Independent Test**: Can be tested by defining ML request/response contracts and consuming them in ml-inference without implementing model runtime logic.

**Acceptance Scenarios**:

1. **Given** ml-inference defines floor-plan and NatHERS payloads, **When** it uses shared ML request/response models and enums, **Then** payload schemas are uniform across producer and consumer repositories.
2. **Given** a consumer uses typed ML client methods with shared contracts, **When** development-time checks are run, **Then** request/response shape mismatches are detected before runtime.

### Edge Cases

- How are consumers expected to handle unknown enum values returned by an upstream service while preserving v1.x compatibility?
- What happens when optional fields are omitted from legacy payloads that must remain valid in patch releases?
- How are partial ML confidence details represented when some confidence metadata is unavailable?
- What is the expected error contract when network failures and payload validation failures occur in the same client interaction lifecycle?

## Constitution Alignment *(mandatory)*

- This feature remains a contracts-only package change in scanq-shared.
- No API routers or transport runtime application logic are introduced.
- No database persistence, migrations, or stateful storage behavior are introduced.
- No accreditation runtime orchestration or business pipeline execution logic is introduced.
- Semantic Versioning impact is minor within v1.x: additive contracts and typed clients are introduced with backward-compatible behavior; patch releases must remain non-breaking.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide shared project request/response contracts covering project creation, project update, project response, and project-environment response under scanq-shared project contract modules.
- **FR-002**: System MUST provide shared environment request/response contracts covering environment creation and environment response under scanq-shared environment contract modules.
- **FR-003**: System MUST provide shared intake and auth contracts covering intake draft generation requests, development login request, and service token response under scanq-shared intake and auth modules.
- **FR-004**: System MUST provide shared job and provider contracts covering job response, job status, provider profile, and cost estimate under scanq-shared model modules.
- **FR-005**: System MUST provide accreditation-oriented dwelling contracts including dwelling input, dwelling configuration, expected outputs, floor-plan feature attributes, specification attributes, and dwelling source enumerations.
- **FR-006**: System MUST provide ML contracts for floor-plan tracing and NatHERS attribute extraction, including window attributes and confidence metadata.
- **FR-007**: System MUST provide shared enums and value types including execution status, confidence level, cross-repo error codes, lineage metadata, artifact manifest, and execution context.
- **FR-008**: System MUST maintain existing typed training-studio client operations (context resolution, service token retrieval, lineage registration, and lineage finalization) and regression-validate request/response contract enforcement while introducing new shared models and enums.
- **FR-009**: System MUST provide a typed ML inference client that supports floor-plan tracing and attribute extraction using shared request/response contracts.
- **FR-010**: System MUST provide HTTP utility behavior for retries with exponential backoff, standardized timeout/connection/validation error mapping, and structured request/response logging patterns.
- **FR-011**: System MUST enforce that shared contracts are validation-ready and safe for response serialization across consumer repositories.
- **FR-012**: System MUST maintain v1.x contract compatibility such that patch updates introduce no breaking contract shape changes.
- **FR-013**: System MUST exclude API routers, database concerns, and service business logic from this feature scope.

### Key Entities *(include if feature involves data)*

- **Project Contract Set**: Canonical project and environment request/response definitions used by multiple repositories.
- **Intake and Auth Contract Set**: Canonical intake draft and service-auth payload definitions supporting cross-service integration.
- **Job and Provider Contract Set**: Shared representations of job lifecycle state and provider pricing/profile information.
- **Dwelling Domain Model**: Accreditation-oriented dwelling data structure including source classification, configuration, expected outputs, and specification attributes.
- **ML Inference Contract Set**: Floor-plan tracing and NatHERS extraction request/response definitions including confidence details.
- **Execution and Lineage Types**: Shared metadata for execution state, artifacts, context, and lineage lifecycle reporting.
- **Typed Service Clients**: Reusable client interfaces for training-studio and ML inference endpoints that enforce contract-consistent payload exchange.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All targeted duplicate contract definitions in training-studio Phase 1 scope are replaced with scanq-shared imports, with no duplicated equivalent contract remaining in that scope.
- **SC-002**: Accreditation integration regression tests confirm context resolution, service token retrieval, and lineage register/finalize flows remain contract-compatible when using shared models and enums from this release.
- **SC-003**: ML inference integration can define and exchange floor-plan tracing and NatHERS attribute payloads exclusively through scanq-shared contracts in integration tests.
- **SC-004**: All three repositories consume the same published scanq-shared minor release for this feature (target: v1.1.0) and complete CI contract validation without cross-repo schema drift findings.
- **SC-005**: Consumer developers can discover typed request/response fields and enums through IDE autocomplete for all Phase 1 client methods and contract models.

## Assumptions

- Consumer repositories can adopt a single shared package source for the feature release target (v1.1.0) during Phase 1 completion.
- Contract definitions introduced in this phase are additive and remain backward compatible within v1.x.
- Shared contract models are treated as immutable by consumers to prevent accidental mutation during request assembly and response handling.
- Typed clients are exposed from a dedicated shared client namespace to simplify adoption across repositories.
- Existing service endpoints required by typed clients remain available and behaviorally consistent during migration.