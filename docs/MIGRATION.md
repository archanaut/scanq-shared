# Migration Guide: scanq-shared Version Upgrades

**Audience**: Developers maintaining scanq-accreditation and scanq-training-studio  
**Focus**: Steps to upgrade between major versions with minimal breaking changes

---

## Versioning Philosophy

scanq-shared follows **Semantic Versioning 2.0.0**:

| Version | Stability | Breaking Changes | Action |
|---------|-----------|------------------|--------|
| **1.x.x** | Stable | None (backward compatible) | Auto-merge patches; opt-in minor upgrades |
| **2.0.0** | Stable | Yes (breaking changes) | Read migration guide; review code; test thoroughly |
| **2.x.x** | Stable | None within v2 | Safe to upgrade from 2.0.0 |

---

## v1.0.0 → v1.x.x (MINOR/PATCH Upgrades)

### No Migration Required

PATCH upgrades (1.0.0 → 1.0.1) and MINOR upgrades (1.0.0 → 1.1.0) are **fully backward compatible**.

**Example**: v1.0.0 → v1.1.0
- ✅ New optional client methods added
- ✅ New optional model fields added
- ✅ Existing code unchanged
- ✅ No test rewrites needed

### Update Process

```bash
# Update pyproject.toml dependency
# Before:
# scanq-shared>=1.0.0,<2.0.0

# After:
# scanq-shared>=1.1.0,<2.0.0

# Or let it float
# scanq-shared>=1.0.0,<2.0.0  (auto-gets v1.1.0)

# Sync dependencies
uv sync

# Test (should all pass without code changes)
pytest tests/
```

---

## v1.x.x → v2.0.0 (MAJOR Upgrade)

### Breaking Changes

This section documents all breaking changes from v1.x to v2.0.0 (hypothetical example).

#### Change 1: ContextResolveResponse Schema Restructure

**v1.x (Old)**:
```python
class ContextResolveResponse(BaseModel):
    status: str
    project_id: str
    project_name: str | None
    environment_id: str
    environment_name: str | None
    actor_id: str | None
    actor_name: str | None
    resolved_at: datetime
    metadata: dict
```

**v2.0.0 (New)**:
```python
class ContextResolveResponse(BaseModel):
    status: str
    context: ContextData  # ← NESTED (breaking change)
    resolved_at: datetime

class ContextData(BaseModel):
    project: ProjectModel
    environment: EnvironmentModel
    actor: ActorModel | None
    metadata: dict
```

**Impact**: Direct field access now broken

#### Change 2: TrainingStudioClient.resolve_context() Signature

**v1.x (Old)**:
```python
async def resolve_context(
    self,
    project_id: str,
    environment_id: str,
    actor_id: str | None = None,
    include_metadata: bool = False,
) -> ContextResolveResponse:
```

**v2.0.0 (New)**:
```python
async def resolve_context(
    self,
    project_id: str,
    environment_id: str,
    actor_id: str,  # ← NOW REQUIRED (breaking change)
    include_metadata: bool = False,
) -> ContextResolveResponse:
```

**Impact**: Calls without actor_id now fail

---

### Migration Steps

#### Step 1: Review Breaking Changes

Read the v2.0.0 release notes:
```
scanq-shared v2.0.0 - Breaking Changes

1. ContextResolveResponse schema restructured (context nested in object)
2. TrainingStudioClient.resolve_context() now requires actor_id parameter
3. ErrorCode.SERVICE_UNAVAILABLE renamed to ErrorCode.UNAVAILABLE
...
```

#### Step 2: Update pyproject.toml

```toml
# Before
[project]
dependencies = [
  "scanq-shared>=1.0.0,<2.0.0",  # Locked to v1.x
]

# After
[project]
dependencies = [
  "scanq-shared>=2.0.0,<3.0.0",  # Updated to v2.x
]
```

#### Step 3: Identify Affected Code

Search for usage of broken APIs:

```bash
# Find all resolve_context calls
grep -r "resolve_context" src/ tests/

# Find all direct ContextResolveResponse field accesses
grep -r "\.project_id\|\.environment_id\|\.actor_id" src/ tests/
```

#### Step 4: Migrate Code

**Old code (v1.x)**:
```python
# scanq-accreditation/src/cli/commands.py

async def accredit_dwelling(dwelling_id: str):
    async with TrainingStudioClient("http://...") as client:
        # actor_id was optional
        context = await client.resolve_context(
            project_id="proj-archanaut",
            environment_id="env-staging"
        )
        
        # Direct field access
        print(f"Project: {context.project_name}")
        print(f"Environment: {context.environment_name}")
```

**New code (v2.0.0)**:
```python
# scanq-accreditation/src/cli/commands.py

async def accredit_dwelling(dwelling_id: str):
    async with TrainingStudioClient("http://...") as client:
        # actor_id now required
        context = await client.resolve_context(
            project_id="proj-archanaut",
            environment_id="env-staging",
            actor_id="actor-accreditation-service"  # ← NOW REQUIRED
        )
        
        # Access nested structure
        print(f"Project: {context.context.project.name}")
        print(f"Environment: {context.context.environment.name}")
```

#### Step 5: Update Tests

**Old test (v1.x)**:
```python
# tests/integration/test_context.py

async def test_resolve_context():
    async with TrainingStudioClient("http://...") as client:
        context = await client.resolve_context(
            project_id="proj-123",
            environment_id="env-staging"
        )
        
        assert context.project_id == "proj-123"
        assert context.environment_name == "staging"
```

**New test (v2.0.0)**:
```python
# tests/integration/test_context.py

async def test_resolve_context():
    async with TrainingStudioClient("http://...") as client:
        context = await client.resolve_context(
            project_id="proj-123",
            environment_id="env-staging",
            actor_id="actor-service"  # ← NOW REQUIRED
        )
        
        assert context.context.project.id == "proj-123"
        assert context.context.environment.name == "staging"
```

#### Step 6: Run Tests

```bash
# Type check
mypy --strict src/ tests/

# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Full test suite with coverage
pytest tests/ --cov=src/
```

#### Step 7: Verify Imports

```bash
# Check that old imports still work (if aliased)
python -c "from scanq_shared.clients import TrainingStudioClient; print(TrainingStudioClient)"

# Or identify import failures
python -c "from scanq_shared.schemas import ContextResolveResponse; print(ContextResolveResponse)"
```

#### Step 8: Manual Testing

Test the affected subsystem manually:

```bash
# For scanq-accreditation CLI
uv run scanq-accredit validate dwelling-101 --environment staging

# Check logs for context resolution
grep "context resolved" logs/*.log

# Verify accreditation workflow completes
```

#### Step 9: Commit & Deploy

```bash
# Commit migration changes
git add -A
git commit -m "chore: migrate to scanq-shared v2.0.0

- Updated resolve_context() calls to include required actor_id parameter
- Updated ContextResolveResponse field access to use nested .context object
- Updated all tests to match new schema structure
- All tests passing; type checking clean

Closes #456"

git push origin main

# Deploy to staging first
make deploy-staging

# Monitor for errors
tail -f logs/accreditation.log

# If successful, deploy to production
make deploy-production
```

---

## Compatibility Matrix: All Versions

| Version | Release Date | Status | Python | Pydantic | httpx | EOL |
|---------|--------------|--------|--------|----------|-------|-----|
| 1.0.0 | 2026-06-30 | Stable | 3.14+ | 2.9.2+ | 0.27.2+ | 2027-06-30 |
| 1.1.0 | 2026-08-15 | Stable | 3.14+ | 2.10.0+ | 0.28.0+ | 2027-08-15 |
| 2.0.0 | 2026-12-01 | Stable | 3.14+ | 3.0.0+ | 1.0.0+ | 2027-12-01 |

---

## Deprecation Timeline Example

### Planned for v1.3.0 (hypothetical)

Functions marked for removal in v2.0.0:

```python
# scanq_shared/clients/training_studio.py

from warnings import warn

class TrainingStudioClient(BaseClient):
    @deprecated(
        "Use resolve_context_v2() instead",
        version="1.3.0",
        removal_version="2.0.0"
    )
    async def resolve_context(self, project_id: str, ...) -> ContextResolveResponse:
        warn(
            "resolve_context() is deprecated as of v1.3.0; "
            "use resolve_context_v2() instead. "
            "This method will be removed in v2.0.0.",
            DeprecationWarning,
            stacklevel=2
        )
        ...
    
    async def resolve_context_v2(self, ...) -> ContextResolveResponseV2:
        """New API with different signature."""
        ...
```

### v1.3.0 → 1.4.0

Consumers can migrate at their own pace:
```python
# Warnings appear in logs but code still works
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    context = await client.resolve_context(...)  # Still works, but deprecated
```

### v2.0.0

Old methods removed:
```python
# This will fail in v2.0.0
context = await client.resolve_context(...)  # ❌ AttributeError
```

---

## Rollback Procedure

If v2.0.0 upgrade fails in production:

```bash
# 1. Revert pyproject.toml to v1.x
git checkout HEAD~1 -- pyproject.toml

# 2. Reinstall old version
uv sync

# 3. Revert code changes
git checkout HEAD~1 -- src/ tests/

# 4. Commit rollback
git commit -m "rollback: revert to scanq-shared v1.x

Reason: XXX (critical issue found in v2.0.0)
Reopened: #456"

# 5. Deploy previous version
git push origin main
make deploy-production

# 6. Report issue to scanq-shared team
# GitHub: https://github.com/archanaut/scanq-shared/issues/new
```

---

## Support Policy

### v1.x Support (6 months)

| Phase | Period | Support |
|-------|--------|---------|
| **Active** | Months 1-4 | Patches for bugs, security fixes |
| **Maintenance** | Months 5-6 | Security fixes only |
| **EOL** | After Month 6 | No support |

### v2.x Support (12+ months)

v2.0.0 and later versions supported for at least 12 months with security patches and critical bug fixes.

---

## Questions & Support

For migration issues:
1. Check this guide and [MIGRATION.md](MIGRATION.md)
2. See [API_REFERENCE.md](API_REFERENCE.md) for complete API documentation
3. Review [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for usage patterns
4. Open GitHub issue: https://github.com/archanaut/scanq-shared/issues
