# Technical Requirements Document: scanq-shared

**Version**: 1.0  
**Date**: June 15, 2026  
**Companion**: PRD.md  
**Focus**: Package structure, versioning, release workflows, and migration patterns

---

## Part 1: Package Structure & Organization

### Directory Layout

```
scanq-shared/
├── pyproject.toml                      # Project metadata, dependencies, build config
├── README.md                           # Usage quickstart and overview
├── CONTRIBUTING.md                     # Development setup, testing, release process
├── LICENSE                             # Apache 2.0 or equivalent
│
├── src/
│   └── scanq_shared/
│       ├── __init__.py                 # Public API exports
│       ├── version.py                  # Single source of truth for version
│       │
│       ├── models/                     # Pydantic data models (no DB ORM)
│       │   ├── __init__.py
│       │   ├── common.py               # Shared base models (timestamps, IDs, errors)
│       │   ├── accreditation.py        # Accreditation-specific models
│       │   ├── training_studio.py      # Training-studio-specific models
│       │   └── lineage.py              # Lineage/audit trail models
│       │
│       ├── schemas/                    # Request/response schemas (API contract)
│       │   ├── __init__.py
│       │   ├── context.py              # Context resolution request/response
│       │   ├── auth.py                 # Auth token request/response
│       │   ├── lineage.py              # Lineage register/finalize schemas
│       │   └── errors.py               # Standard error schemas
│       │
│       ├── enums/                      # Status/type enumerations
│       │   ├── __init__.py
│       │   ├── common.py               # Universal enums (status, error codes)
│       │   ├── accreditation.py        # Accreditation-specific enums
│       │   └── training_studio.py      # Training-studio-specific enums
│       │
│       ├── clients/                    # Typed HTTP clients (httpx-based)
│       │   ├── __init__.py
│       │   ├── base.py                 # BaseClient with retry, timeout, tracing
│       │   ├── training_studio.py      # TrainingStudioClient (context, auth, lineage)
│       │   └── exceptions.py           # Client-specific exceptions
│       │
│       └── types/                      # Type aliases and runtime checks
│           ├── __init__.py
│           └── core.py                 # Shared type definitions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # Pytest fixtures and configuration
│   │
│   ├── unit/
│   │   ├── test_models.py              # Data model validation tests
│   │   ├── test_schemas.py             # Schema parsing and validation
│   │   ├── test_enums.py               # Enum coverage tests
│   │   └── test_clients.py             # Client instantiation and retry logic
│   │
│   ├── integration/
│   │   ├── conftest.py                 # Mock training-studio endpoint setup
│   │   ├── test_training_studio_client.py  # End-to-end client tests
│   │   └── test_error_handling.py      # Error response handling
│   │
│   └── fixtures/
│       ├── __init__.py
│       └── sample_payloads.py          # Reusable request/response fixtures
│
├── docs/
│   ├── PRD.md                          # Product Requirements Document (this file)
│   ├── TRD.md                          # Technical Requirements Document (this file)
│   ├── API_REFERENCE.md                # Schema and client API reference
│   ├── INTEGRATION_GUIDE.md            # How-to integrate in scanq-accreditation/training-studio
│   ├── MIGRATION.md                    # Version upgrade guide
│   └── ARCHITECTURE.md                 # Detailed architecture diagrams and rationale
│
└── .github/
    └── workflows/
        ├── test.yml                    # Unit/integration tests on PR
        ├── release.yml                 # Tag-triggered release to PyPI
        └── type-check.yml              # mypy --strict on every commit
```

---

## Part 2: Version Management

### Single Source of Truth: `src/scanq_shared/version.py`

```python
# src/scanq_shared/version.py
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Metadata
__author__ = "Archanaut"
__license__ = "Apache 2.0"
```

### Versioning Scheme: Semantic Versioning 2.0.0

**Format**: `MAJOR.MINOR.PATCH[+build]`

| Bump Type | Trigger | Example | Consumer Action |
|-----------|---------|---------|-----------------|
| **MAJOR** | Breaking API changes, schema incompatibilities | 1.0.0 → 2.0.0 | Review migration guide, update code |
| **MINOR** | New endpoints, new models, backward-compatible features | 1.0.0 → 1.1.0 | No code changes required; opt-in to new features |
| **PATCH** | Bug fixes, documentation, non-functional changes | 1.0.0 → 1.0.1 | Recommended but optional |

### Version Bumping Checklist

Before releasing:

```bash
# 1. Update version.py
# 2. Update pyproject.toml [project] version
# 3. Update CHANGELOG.md
# 4. Commit: "chore: bump version to X.Y.Z"
# 5. Create git tag: git tag -a vX.Y.Z -m "Release X.Y.Z"
# 6. Push tag: git push origin vX.Y.Z
# 7. Trigger release workflow: .github/workflows/release.yml
```

---

## Part 3: Release & Distribution Process

### Three-Channel Strategy

#### Channel 1: Development (Main Branch)

**Trigger**: Merges to `main` branch  
**Artifact**: Wheel on GitHub Releases (pre-release)  
**Version**: `X.Y.Z-dev.<build_number>`

```toml
# pyproject.toml (development)
version = "1.0.0-dev.42"
```

**Use Case**: Internal testing, CI pipelines  
**Stability**: Not guaranteed; may have breaking changes

#### Channel 2: Staging (Release Candidate)

**Trigger**: Create `release/X.Y.Z` branch, all checks pass  
**Artifact**: Wheel on GitHub Releases (pre-release tag)  
**Version**: `X.Y.Z-rc1`, `X.Y.Z-rc2`, etc.

```bash
git checkout -b release/1.0.0
# Make any last-minute fixes
git tag -a v1.0.0-rc1 -m "Release candidate 1"
git push origin v1.0.0-rc1
# Workflow publishes to PyPI with pre-release marker
```

**Use Case**: Beta testing in dependent services  
**Stability**: Assumed stable; final testing gate

#### Channel 3: Stable (Production)

**Trigger**: Create annotated git tag `vX.Y.Z` on `main`, all checks pass  
**Artifact**: Wheel on PyPI (stable index)  
**Version**: `X.Y.Z`

```bash
git tag -a v1.0.0 -m "Release 1.0.0: Initial stable release"
git push origin v1.0.0
# Workflow publishes to PyPI (stable)
```

**Use Case**: Production dependencies  
**Stability**: Full; subject to semantic versioning contract

### Release Workflow (.github/workflows/release.yml)

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14'
      
      # Build wheel
      - run: pip install hatchling
      - run: python -m hatchling build
      
      # Publish to PyPI (or private registry)
      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
      
      # Create GitHub Release
      - uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```

---

## Part 4: Dependency Management & Pinning

### Production Dependencies

```toml
[project]
dependencies = [
  "pydantic>=2.9.2,<3.0",      # Lock major version; auto-accept patches
  "typing-extensions>=4.10.0,<5.0",
  "httpx>=0.27.2,<1.0",        # Lock major for stability
]
```

### Rationale

- **Pydantic 2.x**: Required for performance, strict validation
- **typing-extensions**: Backport modern type syntax to 3.14
- **httpx**: Modern async/sync HTTP client; mature, well-maintained

### Development Dependencies

```toml
[dependency-groups]
dev = [
  "mypy>=1.11.2,<2.0",
  "pytest>=8.3.3,<9.0",
  "pytest-cov>=5.0.0,<6.0",
  "ruff>=0.6.9,<1.0",
  "black>=24.0.0,<25.0",
]
```

### Update Strategy

- **Monthly**: Check for Pydantic/httpx patch updates (auto-merge)
- **Quarterly**: Review MINOR version upgrades (manual review, test)
- **Biannually**: Evaluate MAJOR version migrations (long lead time)

### Dependency Drift Prevention

```bash
# Weekly: Check for new releases
uv pip list --outdated

# Monthly: Lock updates
uv sync --upgrade

# Check: Test full suite
uv run pytest --cov=src/scanq_shared
```

---

## Part 5: Backward Compatibility Policy

### Contract Stability Rules

#### ✅ Backward-Compatible (MINOR Bump)

1. **Adding new optional fields** to request/response models
   ```python
   class ContextResponse(BaseModel):
       project_id: str
       environment_id: str
       actor_id: str
       tags: dict | None = None  # NEW: optional, default None
   ```

2. **Adding new status enum values** (consumers ignore unknown values)
   ```python
   class TokenStatus(str, Enum):
       ACTIVE = "active"
       EXPIRED = "expired"
       REVOKED = "revoked"  # NEW
   ```

3. **Adding new optional query parameters** to client methods
   ```python
   async def resolve_context(
       self,
       project_id: str,
       include_metadata: bool = False  # NEW: default False
   ) -> ContextResponse:
   ```

4. **Adding new client methods** (accreditation CLI doesn't need to use them)
   ```python
   class TrainingStudioClient:
       async def new_endpoint(self) -> NewResponse:  # NEW
           ...
   ```

#### ❌ Breaking Changes (MAJOR Bump Required)

1. **Removing fields** from models (existing consumers expect them)
2. **Renaming fields** or changing types
3. **Removing enum values** that consumers depend on
4. **Changing client method signatures** (required parameters)
5. **Changing response structure** (e.g., wrapping response in envelope)

### Migration Strategy for Breaking Changes

If a MAJOR version bump is unavoidable:

1. **Announce early** (GitHub issue, 30-day notice)
2. **Provide upgrade guide** in MIGRATION.md with code examples
3. **Support parallel versions** if feasible (e.g., `/v1/` and `/v2/` endpoints)
4. **Maintain v1.x branch** for critical security fixes for 6 months

---

## Part 6: Compatibility Matrix

### Python Version Support

| Python | scanq-shared | Status | EOL |
|--------|--------------|--------|-----|
| 3.13 | 1.0.0+ | Not supported | June 2029 |
| 3.14 | 1.0.0+ | **Recommended** | October 2030 |
| 3.15 | 1.1.0+ | Supported | May 2031 |

### Consumer Service Compatibility

| Service | Min Version | Max Version | Notes |
|---------|------------|-------------|-------|
| scanq-accreditation | 1.0.0 | < 2.0.0 | CLI depends on models/clients |
| scanq-training-studio | 1.0.0 | < 2.0.0 | API responses use schemas |

### Dependency Compatibility Matrix

```yaml
scanq-shared:
  v1.0.0:
    pydantic: [2.9.2, 2.10.x)  # Patches only
    httpx: [0.27.2, 1.0.0)
    python: [3.14]
  
  v1.1.0:
    pydantic: [2.10.0, 3.0.0)  # Minor bump OK
    httpx: [0.28.0, 1.0.0)
    python: [3.14, 3.15)  # New version support
```

---

## Part 7: Migration Steps by Version

### v0.x → v1.0.0 (Initial Release)

No migration needed; first stable release.

### v1.x → v1.y (Minor Release)

**Action**: Update pyproject.toml

```toml
[project]
dependencies = [
  "scanq-shared>=1.y,<2.0.0",
]
```

**Code Changes**: None required (use new features optionally)

### v1.x → v2.0.0 (Major Release — Hypothetical)

**Step 1**: Review MIGRATION.md for breaking changes

```markdown
# Migration Guide: v1.x → v2.0.0

## Breaking Changes

1. **ContextResponse schema changed**
   - Old: `project_id` (string)
   - New: `project: ProjectModel` (nested object)

2. **TrainingStudioClient.resolve_context() signature changed**
   - Old: `resolve_context(project_id, environment_id)`
   - New: `resolve_context(project_id, environment_id, actor_id)`

## Migration Steps

### Before (v1.x)
\`\`\`python
client = TrainingStudioClient("http://...")
ctx = await client.resolve_context("proj-123", "env-456")
print(ctx.project_id)
\`\`\`

### After (v2.0.0)
\`\`\`python
client = TrainingStudioClient("http://...")
ctx = await client.resolve_context("proj-123", "env-456", actor_id="user-789")
print(ctx.project.id)
\`\`\`
```

**Step 2**: Update imports and code

**Step 3**: Run tests to verify

**Step 4**: Pin new version in pyproject.toml

```toml
[project]
dependencies = [
  "scanq-shared>=2.0.0,<3.0.0",
]
```

---

## Part 8: Testing Strategy

### Unit Tests (models, schemas, enums)

**Location**: `tests/unit/`  
**Coverage Target**: 95%

```python
# tests/unit/test_models.py
import pytest
from scanq_shared.models import ContextResponse
from pydantic import ValidationError

def test_context_response_valid():
    """Valid payload parses correctly."""
    payload = {
        "project_id": "proj-123",
        "environment_id": "env-456",
        "actor_id": "actor-789",
    }
    resp = ContextResponse(**payload)
    assert resp.project_id == "proj-123"

def test_context_response_missing_required_field():
    """Missing required field raises ValidationError."""
    payload = {
        "project_id": "proj-123",
        # missing environment_id
    }
    with pytest.raises(ValidationError):
        ContextResponse(**payload)
```

### Integration Tests (HTTP client)

**Location**: `tests/integration/`  
**Coverage Target**: 85%

```python
# tests/integration/test_training_studio_client.py
import pytest
from httpx import AsyncClient
from scanq_shared.clients import TrainingStudioClient

@pytest.fixture
async def mock_training_studio(httpx_mock):
    """Mock training-studio responses."""
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8000/accreditation/context/resolve",
        json={
            "project_id": "proj-123",
            "environment_id": "env-456",
            "actor_id": "actor-789",
        },
        status_code=200,
    )
    return httpx_mock

@pytest.mark.asyncio
async def test_resolve_context(mock_training_studio):
    """Client correctly calls resolve_context endpoint."""
    client = TrainingStudioClient("http://localhost:8000")
    ctx = await client.resolve_context("proj-123", "env-456")
    assert ctx.project_id == "proj-123"
```

### Type Checking

**Tool**: mypy with strict mode

```bash
mypy --strict src/scanq_shared
```

**Coverage Target**: 100% (zero errors)

---

## Part 9: CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test & Type Check

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.14"]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install uv
          uv sync
      
      - name: Run tests
        run: uv run pytest tests/ --cov=src/scanq_shared --cov-report=xml
      
      - name: Type check
        run: uv run mypy --strict src/scanq_shared
      
      - name: Lint
        run: uv run ruff check src/scanq_shared tests/
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

---

## Part 10: Documentation Requirements

### API Reference (AUTO-GENERATED)

```bash
# Generate from docstrings
uv run pydoc-markdown src/scanq_shared > docs/API_REFERENCE.md
```

### Integration Guide

**Location**: `docs/INTEGRATION_GUIDE.md`

**Contents**:
- How to install scanq-shared in scanq-accreditation
- How to use TrainingStudioClient
- Error handling patterns
- Retry and timeout configuration

### Architecture Documentation

**Location**: `docs/ARCHITECTURE.md`

**Contents**:
- Design rationale (why not include routers, DB logic, etc.)
- Data flow diagrams
- Dependency justification
- Future extensibility points

---

## Part 11: Support & Maintenance

### Issue Triage (by priority)

| Priority | Response Time | Resolution Time |
|----------|---------------|-----------------|
| **P0 (Critical)** | 4 hours | 24 hours | Type errors in core models, client crashes |
| **P1 (High)** | 24 hours | 1 week | Missing/incorrect schemas, test failures |
| **P2 (Medium)** | 3 days | 2 weeks | Documentation, new feature requests |
| **P3 (Low)** | 1 week | 1 month | Style improvements, nice-to-haves |

### Release Cadence

- **PATCH**: Ad-hoc (critical bugs only)
- **MINOR**: Monthly or as needed
- **MAJOR**: Biannual or as needed

---

## Checklist: Release Readiness

- [ ] All unit tests passing (`pytest --cov ≥ 85%`)
- [ ] Type checking passing (`mypy --strict`)
- [ ] Linting passing (`ruff check`)
- [ ] Documentation updated (API reference, migration guide if MAJOR)
- [ ] CHANGELOG.md updated with version and date
- [ ] version.py and pyproject.toml bumped
- [ ] CONTRIBUTING.md reviewed and current
- [ ] All PRs approved and merged
- [ ] Release branch created (if MAJOR/MINOR)
- [ ] GitHub Release drafted with notes
- [ ] Tag pushed and workflow triggered
- [ ] PyPI package verified and installable
