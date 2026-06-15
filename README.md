# scanq-shared

Shared contracts and typed clients for ScanQ ecosystem repositories.

**Copyright © 2026 Archanaut Pty Ltd. All rights reserved.**

This software is licensed under the Archanaut Proprietary License. See [LICENSE](LICENSE) for terms and conditions.

## Scope

- Shared request/response schemas for the Phase 1 fixed endpoint inventory
- Shared enums and error schemas
- Typed async HTTP client (`TrainingStudioClient`) for training-studio support endpoints
- Version compatibility constants and migration guidance

## Non-Goals

- No API routers
- No database persistence logic
- No accreditation pipeline runtime logic

## Phase 1 Endpoint Inventory

| Operation | Client Method | Path |
|---|---|---|
| `context.resolve` | `TrainingStudioClient.resolve_context` | `POST /accreditation/context/resolve` |
| `auth.service-token` | `TrainingStudioClient.get_service_token` | `POST /accreditation/auth/service-token` |
| `lineage.register` | `TrainingStudioClient.register_lineage` | `POST /accreditation/lineage/register` |
| `lineage.finalize` | `TrainingStudioClient.finalize_lineage` | `POST /accreditation/lineage/{lineage_id}/finalize` |

## Quick Usage

```python
from scanq_shared.clients import TrainingStudioClient
from scanq_shared.schemas import ContextResolveResponse

async with TrainingStudioClient("http://training-studio:8000") as client:
    ctx: ContextResolveResponse = await client.resolve_context(
        project_id="proj-001",
        environment_id="env-staging",
    )
    print(ctx.status)
```

## Consumer Migration

If your repository uses local contract definitions, see the migration runbooks under
`specs/001-phase1-shared-contracts/migrations/` for step-by-step import replacement
guidance and the one-release dual-support policy.

## Development

```bash
uv sync --dev           # Install dependencies
uv run pytest -q        # Run tests
ruff check src tests    # Lint
mypy src                # Type check
```

## Version Policy

All public contract changes follow SemVer. See `specs/001-phase1-shared-contracts/research.md`
for the compatibility classification matrix and `version.py` for the current compatibility constants.
