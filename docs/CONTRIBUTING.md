# Contributing to scanq-shared

**Welcome to scanq-shared!** This document outlines the development workflow, testing requirements, and release process.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Making Changes](#making-changes)
3. [Testing](#testing)
4. [Code Quality](#code-quality)
5. [Documentation](#documentation)
6. [Submitting Changes](#submitting-changes)
7. [Release Process](#release-process)

---

## Development Setup

### Prerequisites

- Python 3.14+
- Git
- `uv` (Python package manager) — [Install uv](https://docs.astral.sh/uv/)

### Clone & Setup

```bash
# Clone repository
git clone https://github.com/archanaut/scanq-shared.git
cd scanq-shared

# Install dependencies (including dev)
uv sync

# Verify installation
python -c "import scanq_shared; print(scanq_shared.__version__)"
```

### Verify Environment

```bash
# Python version
python --version  # Should be 3.14+

# mypy
uv run mypy --version

# pytest
uv run pytest --version

# ruff
uv run ruff --version
```

---

## Making Changes

### Branch Naming

Use descriptive branch names:

```bash
# Feature branch
git checkout -b feature/new-client-method

# Bugfix branch
git checkout -b fix/timeout-handling

# Docs branch
git checkout -b docs/update-integration-guide

# NOT this
git checkout -b my-changes
```

### Commit Message Format

Follow conventional commits:

```
<type>(<scope>): <description>

<body>

<footer>
```

**Types**:
- `feat:` New feature (e.g., new client method, new schema)
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring (no behavior change)
- `test:` Test additions or updates
- `chore:` Dependency updates, tooling changes

**Examples**:

```bash
# Feature
git commit -m "feat(client): add batch context resolution

Implement resolve_context_batch() for resolving multiple
contexts in a single round-trip to training-studio.

Closes #123"

# Bugfix
git commit -m "fix(client): handle timeout errors on retry

Previously, TimeoutError was not caught during retry loop.
Now properly retries transient timeout failures.

Closes #456"

# Docs
git commit -m "docs: add error handling section to integration guide"

# Refactor
git commit -m "refactor(enums): consolidate status enums"
```

---

## Testing

### Running Tests

```bash
# All tests
uv run pytest tests/ -v

# Unit tests only
uv run pytest tests/unit/ -v

# Integration tests only
uv run pytest tests/integration/ -v

# Single test file
uv run pytest tests/unit/test_models.py -v

# Single test
uv run pytest tests/unit/test_models.py::test_base_response -v

# With coverage
uv run pytest tests/ --cov=src/scanq_shared --cov-report=term-missing
```

### Writing Tests

**Location**: `tests/unit/` or `tests/integration/`

**Pattern**: Test file name matches module: `src/scanq_shared/models.py` → `tests/unit/test_models.py`

**Example test**:

```python
# tests/unit/test_schemas.py

import pytest
from pydantic import ValidationError
from scanq_shared.schemas import ContextResolveResponse
from scanq_shared.enums import ContextStatus

def test_context_response_valid():
    """Valid payload instantiates correctly."""
    response = ContextResolveResponse(
        status=ContextStatus.RESOLVED,
        project_id="proj-123",
        environment_id="env-456",
        resolved_at=datetime.utcnow(),
    )
    assert response.project_id == "proj-123"

def test_context_response_missing_required_field():
    """Missing required field raises ValidationError."""
    with pytest.raises(ValidationError):
        ContextResolveResponse(
            status=ContextStatus.RESOLVED,
            project_id="proj-123",
            # Missing: environment_id, resolved_at
        )
```

### Test Coverage Target

- **Overall**: ≥ 85%
- **Models/Schemas**: ≥ 95%
- **Clients**: ≥ 80%
- **Enums**: 100%

```bash
# Generate coverage report
uv run pytest tests/ --cov=src/scanq_shared --cov-report=html

# View report
open htmlcov/index.html
```

---

## Code Quality

### Type Checking

Run mypy with strict mode:

```bash
# Check all code
uv run mypy --strict src/scanq_shared

# Check tests too
uv run mypy --strict src/scanq_shared tests/
```

**Target**: Zero errors

**No `Any` types** without clear justification:

```python
# ❌ BAD
def process_data(data: Any) -> Any:
    return data

# ✅ GOOD
from typing import TypeVar

T = TypeVar("T")

def process_data(data: T) -> T:
    return data
```

### Linting

Run ruff (fast Python linter):

```bash
# Check code
uv run ruff check src/scanq_shared tests/

# Auto-fix issues
uv run ruff check --fix src/scanq_shared tests/

# Format code
uv run ruff format src/scanq_shared tests/
```

### Code Style

- **Indentation**: 4 spaces
- **Line length**: 88 characters (configured in `pyproject.toml`)
- **Imports**: Alphabetical, organized (stdlib, third-party, local)
- **Docstrings**: Google style with type hints

**Example**:

```python
"""Module docstring."""

from datetime import datetime
from typing import Any

import httpx
import pydantic

from . import models


class MyClass:
    """Class docstring with description.
    
    Attributes:
        name: The name
        value: The value
    """
    
    def __init__(self, name: str, value: int) -> None:
        """Initialize MyClass.
        
        Args:
            name: The name
            value: The value
        
        Raises:
            ValueError: If value < 0
        """
        if value < 0:
            raise ValueError("value must be >= 0")
        
        self.name = name
        self.value = value
```

### Pre-Commit Hook (Optional)

Set up a local hook to run checks before commit:

```bash
# Create hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

echo "Running tests..."
uv run pytest tests/ -q

echo "Type checking..."
uv run mypy --strict src/scanq_shared

echo "Linting..."
uv run ruff check src/scanq_shared

echo "✓ All checks passed"
EOF

chmod +x .git/hooks/pre-commit
```

---

## Documentation

### Docstrings

All public classes, methods, and functions must have docstrings:

```python
class BaseClient:
    """Base HTTP client with retry logic and request tracing.
    
    Provides common functionality for all typed clients including
    automatic retry on transient failures, timeout handling, and
    optional request/response tracing.
    
    Attributes:
        base_url: Base URL for all requests
        timeout: Request timeout in seconds
        max_retries: Maximum number of retries on transient failures
        trace_requests: Enable request/response logging
    """
    
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        trace_requests: bool = False,
    ) -> None:
        """Initialize BaseClient.
        
        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries (default: 3)
            trace_requests: Enable request/response logging (default: False)
        
        Raises:
            ValueError: If timeout <= 0 or max_retries < 0
        """
```

### README Updates

If adding a new feature, update [README.md](../README.md):

```markdown
## New Feature: Batch Context Resolution

The client now supports resolving multiple contexts in a single round-trip:

\`\`\`python
async with TrainingStudioClient("http://...") as client:
    contexts = await client.resolve_context_batch([
        ("proj-1", "env-staging"),
        ("proj-2", "env-prod"),
    ])
\`\`\`

See [Integration Guide](docs/INTEGRATION_GUIDE.md) for more details.
```

### API Reference

Auto-generated from docstrings:

```bash
# Generate API reference
uv run pydoc-markdown src/scanq_shared > docs/API_REFERENCE.md
```

---

## Submitting Changes

### Pull Request (PR) Workflow

1. **Create branch** from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/my-feature
   ```

2. **Make changes** and commit:
   ```bash
   git add src/scanq_shared/...
   git commit -m "feat(client): add new method"
   ```

3. **Push to GitHub**:
   ```bash
   git push origin feature/my-feature
   ```

4. **Open PR** on GitHub:
   - Title: Clear and descriptive
   - Description: What, why, and how
   - Link related issues: "Closes #123"
   - Include testing notes

5. **Wait for CI checks** to pass:
   - Tests (pytest)
   - Type checking (mypy)
   - Linting (ruff)
   - Coverage reporting

6. **Respond to review** comments:
   ```bash
   # Make changes
   git add ...
   git commit -m "chore: address review comments"
   git push origin feature/my-feature
   ```

7. **Get approval** from a maintainer

8. **Merge PR**:
   - Maintainer clicks "Squash and merge" (for clean history)
   - Branch is auto-deleted

### PR Checklist

Before submitting:

- [ ] Branch created from `main`
- [ ] Code follows style guide (ruff, mypy)
- [ ] All tests pass locally (`pytest tests/`)
- [ ] New tests added for new code
- [ ] Docstrings added for all public APIs
- [ ] README/docs updated if needed
- [ ] Commit message follows conventional commits
- [ ] No breaking changes (or documented if MAJOR)

---

## Release Process

### Pre-Release Checklist

1. **Decide version bump** (PATCH/MINOR/MAJOR):
   - PATCH: Bug fixes only
   - MINOR: New features, backward compatible
   - MAJOR: Breaking changes

2. **Update version**:
   ```bash
   # Edit src/scanq_shared/version.py
   __version__ = "1.1.0"
   __version_info__ = (1, 1, 0)
   
   # Edit pyproject.toml [project]
   version = "1.1.0"
   ```

3. **Update CHANGELOG.md**:
   ```markdown
   ## [1.1.0] - 2026-07-15
   
   ### Added
   - New `TrainingStudioClient.batch_resolve_context()` method
   - Optional `include_tags` parameter to context resolution
   
   ### Fixed
   - Timeout handling in retry loop
   
   ### Changed
   - Default retry count increased from 2 to 3
   ```

4. **Run full test suite**:
   ```bash
   uv run pytest tests/ --cov=src/scanq_shared
   uv run mypy --strict src/scanq_shared tests/
   uv run ruff check src/scanq_shared tests/
   ```

5. **Commit version bump**:
   ```bash
   git add src/scanq_shared/version.py pyproject.toml CHANGELOG.md
   git commit -m "chore: bump version to 1.1.0"
   git push origin main
   ```

### Create Release Tag

```bash
# Create annotated tag
git tag -a v1.1.0 -m "Release 1.1.0

New features:
- Batch context resolution
- Optional metadata tags

Fixes:
- Timeout handling in retry loop

See CHANGELOG.md for details."

# Push tag (triggers release workflow)
git push origin v1.1.0
```

### Release Workflow

GitHub Actions automatically:

1. Builds the wheel: `python -m hatchling build`
2. Publishes to PyPI (requires PYPI_API_TOKEN secret)
3. Creates GitHub Release with artifacts and notes

---

## Troubleshooting

### mypy Errors

```bash
# Common: Missing type on function parameter
# Error: Argument 1 has incompatible type "str" (revealed type "Any")

# Fix: Add type annotation
def my_func(name: str) -> None:  # ← Add : str
    ...
```

### pytest Failures

```bash
# Run with verbose output
uv run pytest tests/unit/test_models.py -vv

# Print debug info
uv run pytest tests/unit/test_models.py -s

# Stop on first failure
uv run pytest tests/unit/test_models.py -x
```

### Import Errors

```bash
# Verify package structure
ls -la src/scanq_shared/

# Reinstall in editable mode
uv sync

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

---

## Questions?

- **GitHub Issues**: https://github.com/archanaut/scanq-shared/issues
- **Discussions**: https://github.com/archanaut/scanq-shared/discussions
- **Email**: dev@archanaut.com

---

## Code of Conduct

Please be respectful and inclusive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).
