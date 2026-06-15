# Migration Runbook: scanq-accreditation → scanq-shared Phase 1

**Consumer**: `scanq-accreditation`
**Target release**: `scanq-shared >= 1.0.0`
**Dual-support window**: 1 release

---

## Pre-migration state

The following local contract definitions in `scanq-accreditation` are to be replaced with shared imports:

| Local Definition | Shared Equivalent | Module |
|---|---|---|
| Local `ContextResolveRequest` | `ContextResolveRequest` | `scanq_shared.schemas.context` |
| Local `ContextResolveResponse` | `ContextResolveResponse` | `scanq_shared.schemas.context` |
| Local `ServiceTokenRequest` | `ServiceTokenRequest` | `scanq_shared.schemas.auth` |
| Local `ServiceTokenResponse` | `ServiceTokenResponse` | `scanq_shared.schemas.auth` |
| Local `LineageRegisterRequest` | `LineageRegisterRequest` | `scanq_shared.schemas.lineage` |
| Local `LineageRegisterResponse` | `LineageRegisterResponse` | `scanq_shared.schemas.lineage` |
| Local `LineageFinalizeRequest` | `LineageFinalizeRequest` | `scanq_shared.schemas.lineage` |
| Local `LineageFinalizeResponse` | `LineageFinalizeResponse` | `scanq_shared.schemas.lineage` |
| Local lineage/context enums | `LineageEventType`, `ContextStatus` | `scanq_shared.enums` |

---

## Import replacement mapping

```python
# BEFORE (local definitions)
from accreditation.contracts import ContextResolveRequest, ContextResolveResponse
from accreditation.contracts import ServiceTokenRequest, ServiceTokenResponse
from accreditation.contracts import (
    LineageRegisterRequest, LineageRegisterResponse,
    LineageFinalizeRequest, LineageFinalizeResponse,
)

# AFTER (shared imports)
from scanq_shared.schemas import (
    ContextResolveRequest,
    ContextResolveResponse,
    ServiceTokenRequest,
    ServiceTokenResponse,
    LineageRegisterRequest,
    LineageRegisterResponse,
    LineageFinalizeRequest,
    LineageFinalizeResponse,
)
from scanq_shared.enums import LineageEventType, ContextStatus, TokenStatus
from scanq_shared.clients import TrainingStudioClient
```

---

## Dry-run execution record

> **Instructions**: Replace local imports in a feature branch, run the repository test suite, and record outcomes below.

**Branch**: `feat/migrate-to-scanq-shared-phase1`
**Date**: _pending_
**Executed by**: _pending_

### Steps

1. `pip install scanq-shared>=1.0.0` (or update `pyproject.toml` / `requirements.txt`).
2. Search for local contract definitions:
   ```
   grep -r "ContextResolveRequest\|ServiceTokenRequest\|LineageRegisterRequest\|LineageFinalizeRequest" src/
   ```
3. Replace imports per mapping table above.
4. Replace any instantiation of a local `TrainingStudioClient` with `from scanq_shared.clients import TrainingStudioClient`.
5. Run: `pytest -q`
6. Record results below.

### Outcomes

| Check | Result | Notes |
|---|---|---|
| Imports resolve without errors | **PASS** | Verified via `uv run python -c "from scanq_shared.schemas import ContextResolveRequest, ServiceTokenRequest, LineageRegisterRequest, LineageFinalizeRequest; print('OK')"` |
| Phase 1 schema round-trip tests pass | **PASS** | `uv run pytest tests/contract/ tests/integration/ -q` — 75 passed |
| Shared client importable | **PASS** | `from scanq_shared.clients import TrainingStudioClient` resolves correctly |
| No consumer-side changes applied yet | N/A | Consumer repo `scanq-accreditation` not in scope of this workspace |

> **Note**: Full consumer-side dry-run (replacing local imports in `scanq-accreditation`) must be performed in that repository. Use this runbook's import replacement mapping as the migration guide.

---

## Dual-support release checkpoint

During the one-release dual-support window:
- `scanq-accreditation` may still ship with local contract definitions **and** `scanq-shared` as a dependency.
- Both import paths must resolve without conflict.
- Verify: `python -c "from scanq_shared.clients import TrainingStudioClient; print('OK')"` passes.

**Window release**: _pending_ (version that begins dual-support)
**Cutover release**: _pending_ (version that removes local definitions)

---

## Cutover exit criteria

All of the following must be true before removing local contract definitions:

- [ ] All tests pass with shared imports only (no local contract fallback).
- [ ] `grep -r "local_contracts\|local.schemas" src/` returns no matches.
- [ ] `scanq-shared` version pinned to `>=1.0.0` in `pyproject.toml`.
- [ ] `TrainingStudioClient` is imported exclusively from `scanq_shared.clients`.
- [ ] Cutover PR reviewed and approved by a second engineer.
- [ ] Release note references `scanq-shared Phase 1` migration.

### Rollback gate

If cutover fails:
1. Revert the import replacement PR.
2. Keep local definitions in place.
3. File an issue in `scanq-shared` with the failure details.
4. Do NOT extend dual-support window without a new feature specification.
