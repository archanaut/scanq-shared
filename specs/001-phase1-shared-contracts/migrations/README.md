# Migration Runbooks: ScanQ Shared Phase 1

This directory contains per-consumer migration runbooks for adopting `scanq-shared` Phase 1 contracts.

## Expected Runbook Files

| File | Consumer | Status |
|------|----------|--------|
| `scanq-training-studio.md` | scanq-training-studio | Pending |
| `scanq-accreditation.md` | scanq-accreditation | Pending |

## Dual-Support Policy

Each consumer repository has a **one-release dual-support window** to complete migration (see `research.md` Decision 3). After the window, legacy local contract definitions are removed.

## Runbook Format

Each runbook must document:
1. Pre-migration state (local definitions to replace)
2. Import replacement mapping
3. Dry-run execution record and outcomes
4. Dual-support release checkpoint
5. Cutover exit criteria and rollback gate
