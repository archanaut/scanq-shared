<!--
Sync Impact Report
Version change: 0.0.0-template -> 1.0.0
Modified principles:
- Principle 1 -> I. Contracts-Only Package
- Principle 2 -> II. No API Routers
- Principle 3 -> III. No DB Persistence or Migrations
- Principle 4 -> IV. No Runtime Accreditation Pipeline Logic
- Principle 5 -> V. Semantic Versioning and Backward Compatibility
Added sections:
- Repository Boundaries
- Delivery & Quality Workflow
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ⚠ pending: .specify/templates/commands/*.md (directory not present in this repository)
Follow-up TODOs:
- None
-->

# ScanQ Shared Constitution

## Core Principles

### I. Contracts-Only Package
This repository MUST remain a shared contracts and typed-client package. Deliverables
MUST be limited to schemas, models, enums, typed clients, validation helpers, and
packaging metadata required to distribute and consume those contracts. Rationale:
limiting scope preserves a stable integration surface across services.

### II. No API Routers
This repository MUST NOT include HTTP route handlers, controller layers, or framework
router registrations. Transport-specific request handling belongs to service
repositories. Rationale: routers couple contracts to runtime hosting concerns and
reduce reuse.

### III. No DB Persistence or Migrations
This repository MUST NOT implement persistence layers, ORM models tied to storage
engines, migration scripts, or migration tooling configuration. Contract data
structures MUST be storage-agnostic. Rationale: persistence concerns are deployment
specific and break package portability.

### IV. No Runtime Accreditation Pipeline Logic
This repository MUST NOT contain runtime orchestration or execution logic for
accreditation pipelines. It MAY expose type-safe request/response contracts used by
pipeline services, but execution policy and workflow behavior MUST remain external.
Rationale: keeping runtime logic out of shared packages prevents hidden cross-service
coupling.

### V. Semantic Versioning and Backward Compatibility
All releases MUST follow Semantic Versioning. Backward-incompatible contract changes
MUST use a MAJOR version bump and include an explicit migration note. New backward-
compatible fields or capabilities MUST use a MINOR bump. Non-behavioral fixes MUST
use a PATCH bump. Public contract fields MUST be additive by default and removals or
redefinitions MUST be explicitly justified in change documentation. Rationale:
predictable versioning reduces integration risk across dependent repositories.

## Repository Boundaries

- In-scope artifacts: shared schemas, typed clients, enums, error types, lineage and
	context contracts, and packaging/version metadata.
- Out-of-scope artifacts: API routers, web server bootstrapping, persistence/migration
	code, runtime accreditation workflows, and deployment-specific infrastructure.
- Any proposed feature that crosses out-of-scope boundaries MUST be rejected or moved
	to the owning service repository before implementation begins.

## Delivery & Quality Workflow

- Every specification and plan MUST include a Constitution Check that confirms
	package-only scope and no prohibited runtime concerns.
- Every contract change MUST include compatibility analysis (additive/non-additive),
	release bump classification, and test coverage updates for serialization/validation.
- Pull requests MUST include release-note entries when public contracts or typed-client
	behavior changes.
- Reviewers MUST block merges when scope boundaries or versioning rules are violated.

## Governance

This constitution supersedes local implementation preferences and sample template
content. Amendments require: (1) a documented proposal, (2) explicit maintainer
approval, and (3) updates to affected templates and guidance files in the same change.

Versioning policy for this constitution:
- MAJOR: Removal or incompatible redefinition of a principle or governance guarantee.
- MINOR: New principle/section or materially expanded mandatory guidance.
- PATCH: Clarifications, wording improvements, and non-semantic refinements.

Compliance review is required in specification, planning, and pull-request review.
Non-compliant work MUST be corrected before merge.

**Version**: 1.0.0 | **Ratified**: 2026-06-15 | **Last Amended**: 2026-06-15
