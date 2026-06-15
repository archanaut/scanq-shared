# Contract: Training Studio Support Endpoints (Phase 1)

<a name="phase1-endpoint-inventory"></a>

## Scope Rule

Only endpoints listed in this document are in Phase 1 scope. Additional endpoints are deferred to [deferred-endpoints.md](./deferred-endpoints.md).

> **FROZEN** — Phase 1 inventory IDs and paths are locked as of 2026-06-15. No new operations may be added to this inventory without a new feature specification. Deferred operations are tracked in [deferred-endpoints.md](./deferred-endpoints.md).

## Fixed Phase 1 Endpoint Inventory

| Operation ID | Method | Path | Request Contract | Response Contract | Error Contract |
|---|---|---|---|---|---|
| `context.resolve` | `POST` | `/accreditation/context/resolve` | `ContextResolveRequest` | `ContextResolveResponse` | `ErrorResponse` |
| `auth.service-token` | `POST` | `/accreditation/auth/service-token` | `ServiceTokenRequest` | `ServiceTokenResponse` | `ErrorResponse` |
| `lineage.register` | `POST` | `/accreditation/lineage/register` | `LineageRegisterRequest` | `LineageRegisterResponse` | `ErrorResponse` |
| `lineage.finalize` | `POST` | `/accreditation/lineage/{lineage_id}/finalize` | `LineageFinalizeRequest` | `LineageFinalizeResponse` | `ErrorResponse` |

## Typed Client Contract Rules

1. Each operation must expose one typed request model and one typed response model.
2. Error payloads must map to shared standardized error schema/types.
3. Unknown error payloads must map to fallback standardized error type while retaining diagnostics.
4. Operations outside the fixed inventory are rejected for Phase 1 and logged as deferred.

## Compatibility Rules

1. Additive request/response fields require MINOR bump and migration notes.
2. Non-additive field removals or semantic redefinitions require MAJOR bump and explicit migration steps.
3. Dual-support migration window is one release per target repository.

## Operation-to-Schema Mapping

<a name="operation-schema-mapping"></a>

| Operation ID | Client Method | Request Schema (module) | Response Schema (module) | Error Schema (module) |
|---|---|---|---|---|
| `context.resolve` | `TrainingStudioClient.resolve_context` | `ContextResolveRequest` (`scanq_shared.schemas.context`) | `ContextResolveResponse` (`scanq_shared.schemas.context`) | `ErrorResponse` (`scanq_shared.schemas.errors`) |
| `auth.service-token` | `TrainingStudioClient.get_service_token` | `ServiceTokenRequest` (`scanq_shared.schemas.auth`) | `ServiceTokenResponse` (`scanq_shared.schemas.auth`) | `ErrorResponse` (`scanq_shared.schemas.errors`) |
| `lineage.register` | `TrainingStudioClient.register_lineage` | `LineageRegisterRequest` (`scanq_shared.schemas.lineage`) | `LineageRegisterResponse` (`scanq_shared.schemas.lineage`) | `ErrorResponse` (`scanq_shared.schemas.errors`) |
| `lineage.finalize` | `TrainingStudioClient.finalize_lineage` | `LineageFinalizeRequest` (`scanq_shared.schemas.lineage`) | `LineageFinalizeResponse` (`scanq_shared.schemas.lineage`) | `ErrorResponse` (`scanq_shared.schemas.errors`) |

## Deferred Endpoints

Operations not in the Phase 1 inventory are tracked in [deferred-endpoints.md](./deferred-endpoints.md).
