# Deferred Endpoints Backlog

This file tracks training-studio support endpoint operations that were evaluated for Phase 1 but deferred to a future feature specification.

> **Phase 1 fixed inventory is frozen.** New operations must be added via a new feature spec, not by editing `training-studio-support.md`.

## Deferred Operations

| Candidate Operation ID | Reason for Deferral | Target Phase |
|---|---|---|
| `context.list` | Out of Phase 1 scope; read-list operations not required by initial consumers | Phase 2+ |
| `auth.revoke-token` | Not required by Phase 1 consumer use cases | Phase 2+ |
| `lineage.update` | Partial-update semantics require additional contract design work | Phase 2+ |
| `lineage.list` | Pagination and filtering contract needs separate specification | Phase 2+ |
| `health.check` | Infrastructure health endpoint; not a consumer contract concern | Phase 2+ |

## Process for Promoting a Deferred Operation

1. Raise a new feature specification (`speckit.specify`).
2. Reference this file and `training-studio-support.md` in the new spec.
3. After ratification, move the operation from this backlog to the fixed inventory in `training-studio-support.md`.
4. Issue a `MINOR` version bump (new operation = additive change).
