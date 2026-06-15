# Research: ScanQ Shared Phase 1

## Decision 1: Freeze a fixed Phase 1 endpoint inventory

- Decision: Use a named, fixed inventory of training-studio support endpoints for Phase 1 and defer newly discovered endpoints.
- Rationale: Planning and testing remain deterministic; typed client and schema coverage can be measured against a stable scope.
- Alternatives considered:
  - Open-ended endpoint discovery during implementation: rejected due to scope creep risk and unclear release boundaries.
  - Read-only-only endpoint scope: rejected because migration requirements include support operations requiring mutation paths.

## Decision 2: Use staged migration with dual-support

- Decision: Migrate `scanq-training-studio` and `scanq-accreditation` via a staged rollout with temporary dual-support.
- Rationale: Repositories can adopt independently while preserving compatibility during transition.
- Alternatives considered:
  - Big-bang cutover: rejected due to coordinated deployment risk across multiple repositories.
  - Uncoordinated independent migration with no overlap guarantee: rejected due to high breakage potential.

## Decision 3: Dual-support duration is one release window

- Decision: Limit dual-support to one release window per consumer repository, with explicit cutover checkpoints.
- Rationale: Provides a bounded transition period and avoids indefinite maintenance of legacy contract paths.
- Alternatives considered:
  - 30/90-day time windows: rejected because release cadence, not elapsed days, controls contract adoption behavior.
  - Two-release window: rejected to reduce prolonged drift and duplicate maintenance burden.

## Decision 4: SemVer-first release governance

- Decision: Enforce SemVer classification and compatibility notes on every public contract/client change.
- Rationale: Consumer repositories need predictable upgrade semantics and migration guidance.
- Alternatives considered:
  - Release without formal compatibility notes: rejected because it weakens migration safety and auditability.

## Decision 5: Testing emphasis on contract and compatibility behavior

- Decision: Prioritize schema/model validation, typed-client behavior tests, and compatibility regression fixtures.
- Rationale: The package owns contracts and typed integrations, not runtime service behavior.
- Alternatives considered:
  - End-to-end service integration tests in this repository: rejected as out of scope for contracts-only governance.

---

## Compatibility Classification Matrix

<a name="compatibility-matrix"></a>

| Change Type | Example | SemVer Bump | Dual-Support Required | Migration Notes Required |
|---|---|---|---|---|
| Add optional field to request/response schema | New `metadata` field with `default=None` | `MINOR` | No | Yes (note new field in changelog) |
| Add required field to request schema | New required `environment` field | `MAJOR` | Yes (one release) | Yes (consumer must populate field) |
| Remove field from request/response schema | Remove `actor_id` field | `MAJOR` | Yes (one release) | Yes (consumers must stop using field) |
| Rename field (semantics unchanged) | `user_id` → `actor_id` | `MAJOR` | Yes (one release) | Yes (old field deprecation + removal plan) |
| Add new enum value | `LineageEventType.ARCHIVED` | `MINOR` | No | Yes (note new value) |
| Remove enum value | Remove `LineageEventType.CANCELLED` | `MAJOR` | Yes (one release) | Yes (consumers must handle value removal) |
| Change field type (compatible widening) | `str` → `str \| None` | `MINOR` | No | Yes (note changed optionality) |
| Change field type (narrowing or breaking) | `str` → `int` | `MAJOR` | Yes (one release) | Yes (schema migration required) |
| Add new typed client operation method | New `check_health()` method | `MINOR` | No | No |
| Remove typed client operation method | Remove `get_service_token()` | `MAJOR` | Yes (one release) | Yes (consumers must migrate calls) |
| Patch/bugfix (no contract shape change) | Fix validation range in `ttl_seconds` | `PATCH` | No | No |

### Usage Rules

1. Classify every public contract change against this matrix before release.
2. MAJOR bumps trigger the one-release dual-support window per consumer repository.
3. Multiple MINOR changes may be bundled into a single MINOR release.
4. PATCH releases must never alter schema field names, types, or required/optional status.

---

## Deprecation and Legacy Import Removal Sequencing

<a name="deprecation-sequencing"></a>

When a consumer repository begins migration:

### Step 1 — Add shared dependency (Release N)
- Consumer adds `scanq-shared >= 1.0.0` to dependencies.
- Consumer switches import sites from local definitions to shared imports.
- Local definitions are **kept in place** (dual-support window begins).
- Both local and shared imports must resolve without conflict.

### Step 2 — Verify and commit dual-support (Release N)
- Consumer runs full test suite with shared imports.
- Dual-support release checkpoint is recorded in the relevant runbook.
- Cutover exit criteria are reviewed and ticked off in the runbook.

### Step 3 — Remove legacy definitions (Release N+1, cutover)
- Consumer removes local contract definitions in the next release.
- Imports are exclusively from `scanq_shared`.
- Cutover PR is reviewed and merged.
- Release note references `scanq-shared Phase 1` migration completion.

### Escalation path

If a consumer cannot complete cutover within one release:
1. File a bug in `scanq-shared` referencing the consumer and blockers.
2. The `scanq-shared` maintainer reviews and either:
   - Provides a compatibility fix (PATCH or MINOR bump), or
   - Opens a new feature spec to extend the dual-support policy.
3. Do NOT silently extend the window; document the decision in this file.
