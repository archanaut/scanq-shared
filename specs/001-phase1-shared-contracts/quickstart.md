# Quickstart: ScanQ Shared Phase 1 Validation

This guide validates Phase 1 artifacts end-to-end for contracts, typed client mappings, and migration readiness.

## Prerequisites

- Python 3.14+ environment
- Project dependencies installed
- Access to both consumer repositories for migration dry-run checks

## 1. Install dependencies

```bash
uv sync --dev
```

Expected outcome:
- Development dependencies (pytest, mypy, ruff) are available.

## 2. Run contract and fixture validation tests

```bash
pytest -q
```

Expected outcome:
- Existing and new fixture validations pass for shared schemas/models/enums.
- No failing schema compatibility checks for agreed Phase 1 payload fixtures.

## 3. Validate fixed endpoint inventory coverage

Validation references:
- [training-studio-support contract](./contracts/training-studio-support.md)
- [data model](./data-model.md)

Expected outcome:
- All operations in fixed inventory have typed request/response/error mappings.
- No out-of-scope endpoint operation is included in Phase 1 implementation tasks.

## 4. Verify compatibility and release classification

Checklist:
1. Confirm each contract/client change has SemVer classification (PATCH/MINOR/MAJOR).
2. Confirm non-additive changes include migration notes.
3. Confirm dual-support window is defined as one release.

Expected outcome:
- Release notes and migration docs satisfy compatibility governance.

## 5. Consumer migration dry-run checks

For each repository (`scanq-accreditation`, `scanq-training-studio`):
1. Replace targeted local contract imports with shared package imports.
2. Run repository test/validation workflow.
3. Record dual-support release checkpoint and cutover exit criteria.

Expected outcome:
- Both repositories complete documented dry runs with no unresolved duplicate contract definitions.

### Dual-Support Exit Criteria

Before removing local contract definitions in either consumer:

- [ ] All tests pass with shared imports only (no local contract fallback).
- [ ] `scanq-shared` version is pinned to `>=1.0.0` in the consumer's `pyproject.toml`.
- [ ] No duplicate local contract definitions remain (verified with `grep`).
- [ ] Cutover PR reviewed and approved.
- [ ] Release note references `scanq-shared Phase 1` migration.

### Rollback Gate

If the cutover of either consumer fails during the dual-support window:
1. Revert the import replacement PR in the affected consumer repository.
2. Keep local definitions in place until the issue is resolved.
3. File a bug in `scanq-shared` referencing the consumer and failure details.
4. Do NOT extend the dual-support window beyond one release without a new feature specification.

## 6. Readiness gate

Phase 1 is ready for task generation when all are true:
- Contract tests pass.
- Typed client operation coverage matches fixed endpoint inventory.
- Migration dry-run evidence exists for both target repositories.
- Release classification and compatibility notes are complete.

---

## 7. SemVer Release-Note Checklist

<a name="semver-release-checklist"></a>

Before tagging any release from this package, verify each item below:

- [ ] All public contract/schema changes have a SemVer classification: `PATCH` (no-op), `MINOR` (additive), or `MAJOR` (breaking).
- [ ] `version.py` `__version__` is bumped to match the classification.
- [ ] Non-additive changes include migration notes in `specs/001-phase1-shared-contracts/migrations/`.
- [ ] `CHANGELOG` or release notes reference each changed operation ID from the fixed inventory.
- [ ] Dual-support window (one release) is explicitly declared for any consumer-breaking change.
- [ ] `research.md` compatibility classification matrix is updated if a new classification pattern is introduced.
- [ ] All tests pass: `uv run pytest -q && ruff check src tests && mypy src`.

---

## Validation Evidence (Phase 1 implementation — 2026-06-15)

### pytest
```
82 passed, 6 warnings in 0.06s
```
Exit code: **0**

### ruff check src tests
```
All checks passed!
```
Exit code: **0**

### mypy src
```
Success: no issues found in 16 source files
```
Exit code: **0**

**Signed off**: Phase 1 implementation complete. All three commands passed with zero errors.
