# scanq-shared

Shared contracts and typed clients for ScanQ ecosystem repositories.

**Copyright © 2026 Archanaut Pty Ltd. All rights reserved.**

This software is licensed under the Archanaut Proprietary License. See [LICENSE](LICENSE) for terms and conditions.

## Scope

- Shared request/response schemas for Phase 1 + Phase 2 endpoint inventories
- Shared enums and error schemas
- Typed async HTTP clients (`TrainingStudioClient`, `MLInferenceClient`)
- Version compatibility constants and migration guidance

## Non-Goals

- No API routers
- No database persistence logic
- No accreditation pipeline runtime logic

## Endpoint Inventory

| Operation | Client Method | Path |
|---|---|---|
| `context.resolve` | `TrainingStudioClient.resolve_context` | `POST /accreditation/context/resolve` |
| `auth.service-token` | `TrainingStudioClient.get_service_token` | `POST /accreditation/auth/service-token` |
| `lineage.register` | `TrainingStudioClient.register_lineage` | `POST /accreditation/lineage/register` |
| `lineage.finalize` | `TrainingStudioClient.finalize_lineage` | `POST /accreditation/lineage/{lineage_id}/finalize` |
| `media.compose` | `TrainingStudioClient.compose_media` | `POST /accreditation/media/compose` |
| `ml.floor-plan.trace` | `MLInferenceClient.trace_floor_plan` | `POST /ml/floor-plan/trace` |
| `ml.nathers.attributes` | `MLInferenceClient.extract_nathers_attributes` | `POST /ml/nathers/attributes` |

## Quick Usage

```python
from scanq_shared.clients import TrainingStudioClient, MLInferenceClient
from scanq_shared.models import FloorPlanTraceRequest

async with TrainingStudioClient("http://training-studio:8000") as client:
    ctx = await client.resolve_context(
        project_id="proj-001",
        environment_id="env-staging",
    )
    print(ctx.status)

async with MLInferenceClient("http://ml-inference:9000") as client:
    trace = await client.trace_floor_plan(
        FloorPlanTraceRequest(
            dwelling_id="dwelling-101",
            image_url="https://example.com/floor.png",
        )
    )
    print(trace.status)
```

## Consumer Migration

If your repository uses local contract definitions, migrate to imports from:
- `scanq_shared.schemas` for project/environment/intake/job payloads
- `scanq_shared.schemas` for media-compose and error-envelope payloads
- `scanq_shared.models` for dwelling + ML inference contracts
- `scanq_shared.enums` for `ConfidenceLevel`, `ExecutionStatus`, `DwellingSource`, `CrossRepoErrorCode`, `MediaType`, and `MediaComposeStatus`
- `scanq_shared.clients` for `MLInferenceClient`

## Development

```bash
uv sync --dev           # Install dependencies
uv run pytest -q        # Run tests
ruff check src tests    # Lint
mypy src                # Type check
```

## Version Policy

All public contract changes follow SemVer. Current release is **1.2.0** (MINOR additive bump from 1.1.0).

See [docs/release-compatibility/v1.2.0.md](docs/release-compatibility/v1.2.0.md) for the upgrade notes.
