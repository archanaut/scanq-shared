# Phase 1: Contracts Extraction — Initial Tasks

**Timeline**: June 2026  
**Deliverables**: v1.0.0 stable release  
**Owner**: ScanQ Team  

---

## Phase 1 Scope

Extract and validate all contracts needed for scanq-accreditation ↔ scanq-training-studio integration:
- Data models and enums
- Request/response schemas
- Typed HTTP client (`TrainingStudioClient`)
- Full type annotations and docstrings
- 85%+ test coverage

---

## Epic: Foundation & Testing

### Task 1.1: Verify Package Structure & Dependencies
**Status**: NOT STARTED  
**Effort**: 0.5d  
**Owner**: (Assign)

**Description**:
- Verify all directories exist: `models/`, `schemas/`, `enums/`, `clients/`, `types/`
- Confirm `pyproject.toml` has all required dependencies (Pydantic 2.9.2+, httpx, typing-extensions)
- Run `pip install -e ".[dev]"` and verify no errors
- Confirm `mypy --version` and `pytest --version` work

**Definition of Done**:
- [ ] All directories created
- [ ] Dependencies installed and verified
- [ ] Package imports without errors: `python -c "import scanq_shared"`
- [ ] Development tools (mypy, pytest, ruff) available

**Tests**: Manual verification

---

### Task 1.2: Implement Common Enums
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/enums/__init__.py` with enums used across services:
  - `ServiceStatus` (healthy, degraded, unavailable)
  - `TokenStatus` (active, expired, revoked, pending)
  - `ContextStatus` (resolved, partial, not_found, error)
  - `ErrorCode` (invalid_request, unauthorized, forbidden, not_found, conflict, internal_error, service_unavailable, timeout)
  - `EntityType` (project, environment, actor, accreditation_pack, lineage_record)
  - `LineageEventType` (registered, updated, finalized, failed, cancelled)

**Definition of Done**:
- [ ] All enums defined with proper docstrings
- [ ] No `mypy` errors: `mypy --strict src/scanq_shared/enums/`
- [ ] Enums export correctly from `scanq_shared.enums`

**Tests**:
- `tests/unit/test_enums.py`:
  - Verify each enum has all expected values
  - Test string serialization (e.g., `TokenStatus.ACTIVE.value == "active"`)

---

### Task 1.3: Implement Base Models
**Status**: NOT STARTED  
**Effort**: 1.5d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/models/__init__.py` with base classes:
  - `BaseResponse` (status, timestamp, request_id)
  - `ErrorDetail` (code, message, details dict)
  - `ErrorResponse` (extends BaseResponse)
  - `PaginationParams` (limit, offset)
  - `PaginatedResponse` (total, limit, offset, items)
- Add Pydantic v2 validation configuration
- Include Field descriptions and examples for all models

**Definition of Done**:
- [ ] All base models defined with docstrings and Field metadata
- [ ] No `mypy --strict` errors
- [ ] Models validate example payloads without errors

**Tests**:
- `tests/unit/test_models.py`:
  - Verify each model instantiates with valid data
  - Test validation errors for missing required fields
  - Test default values (timestamp auto-generation, empty request_id)

---

### Task 1.4: Implement Training-Studio Models
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/models/training_studio.py`:
  - `ProjectModel` (id, name, description, owner_id, created_at, updated_at, metadata)
  - `EnvironmentModel` (id, project_id, name, config, created_at)
  - `ActorModel` (id, project_id, type, name, email, active, created_at)
- Add Field descriptions and timestamp defaults

**Definition of Done**:
- [ ] All models defined with docstrings
- [ ] Import and use from `scanq_shared.models.training_studio`
- [ ] No `mypy --strict` errors

**Tests**:
- `tests/unit/test_models.py`:
  - Instantiate each model with valid data
  - Verify serialization to dict/JSON

---

## Epic: Training-Studio Contracts

### Task 1.5: Implement Context Resolution Schemas
**Status**: NOT STARTED  
**Effort**: 1.5d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/schemas/context.py`:
  - `ContextResolveRequest` (project_id, environment_id, actor_id, include_metadata)
  - `ContextResolveResponse` (status, project_id, project_name, environment_id, environment_name, actor_id, actor_name, resolved_at, metadata, request_id)
- Use `ContextStatus` enum from `enums`
- Add comprehensive Field descriptions and examples

**Definition of Done**:
- [ ] Schemas match training-studio API specification
- [ ] No `mypy --strict` errors
- [ ] Validate example request/response payloads

**Tests**:
- `tests/unit/test_schemas.py`:
  - Test request validation (required vs. optional fields)
  - Test response parsing with full metadata
  - Test enum serialization

---

### Task 1.6: Implement Auth Token Schemas
**Status**: NOT STARTED  
**Effort**: 1.5d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/schemas/auth.py`:
  - `ServiceTokenRequest` (service_id, scopes, ttl_seconds, metadata)
  - `ServiceTokenResponse` (status, token, token_type, expires_at, scopes, issued_at, request_id)
  - Add `expires_in` property to calculate remaining seconds
- Use `TokenStatus` enum
- Add validation (ttl_seconds: 60-86400)

**Definition of Done**:
- [ ] Schemas match training-studio API specification
- [ ] `expires_in` property correctly calculates remaining seconds
- [ ] No `mypy --strict` errors

**Tests**:
- `tests/unit/test_schemas.py`:
  - Test ttl_seconds validation (min/max bounds)
  - Test `expires_in` calculation
  - Test token serialization

---

### Task 1.7: Implement Lineage Schemas
**Status**: NOT STARTED  
**Effort**: 1.5d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/schemas/lineage.py`:
  - `LineageRegisterRequest` (run_id, dwelling_id, pack_version, initiated_by, environment, metadata)
  - `LineageRegisterResponse` (lineage_id, run_id, status, registered_at, request_id)
  - `LineageFinalizeRequest` (lineage_id, status, summary, metrics)
  - `LineageFinalizeResponse` (lineage_id, status, finalized_at, request_id)
- Use `LineageEventType` enum
- Add comprehensive docstrings and Field examples

**Definition of Done**:
- [ ] All schemas defined with docstrings
- [ ] Validate example register and finalize payloads
- [ ] No `mypy --strict` errors

**Tests**:
- `tests/unit/test_schemas.py`:
  - Test register request validation
  - Test finalize request validation
  - Test response parsing

---

### Task 1.8: Implement Error Schemas
**Status**: NOT STARTED  
**Effort**: 0.5d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/schemas/errors.py`:
  - `ErrorSchema` (code, message, status_code, details, request_id)
- Add validation for HTTP status codes (400-599)

**Definition of Done**:
- [ ] Schema defined with docstrings and examples
- [ ] No `mypy --strict` errors

**Tests**:
- `tests/unit/test_schemas.py`:
  - Test status_code validation
  - Test error parsing

---

## Epic: HTTP Client

### Task 1.9: Implement Base Client
**Status**: NOT STARTED  
**Effort**: 1.5d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/clients/base.py`:
  - `BaseClient` with async support (httpx.AsyncClient)
  - Constructor: base_url, timeout, max_retries, trace_requests
  - `_request()` method with retry logic on transient failures
  - `__aenter__` / `__aexit__` for async context manager
  - `close()` method to cleanup client

**Features**:
- Retry on `TimeoutException`, `ConnectError`, `NetworkError`
- Exponential backoff (optional)
- Request/response tracing (configurable logging)

**Definition of Done**:
- [ ] Base client instantiates and manages httpx.AsyncClient
- [ ] Async context manager works
- [ ] Retry logic tested with mock failures
- [ ] No `mypy --strict` errors

**Tests**:
- `tests/unit/test_clients.py`:
  - Test instantiation with various parameters
  - Test context manager usage
  - Mock transient failures and verify retry count

---

### Task 1.10: Implement Client Exceptions
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/clients/exceptions.py` with custom exception hierarchy:
  - `ClientError` (base)
  - `ConnectionError` (host, reason)
  - `TimeoutError` (operation, timeout_seconds)
  - `AuthenticationError` (reason)
  - `ValidationError` (message, details dict)
  - `APIError` (status_code, code, message, details)

**Definition of Done**:
- [ ] All exception classes inherit properly
- [ ] Exceptions include helpful attributes
- [ ] No `mypy --strict` errors

**Tests**:
- `tests/unit/test_clients.py`:
  - Verify exception attributes and messages

---

### Task 1.11: Implement TrainingStudioClient
**Status**: NOT STARTED  
**Effort**: 2d  
**Owner**: (Assign)

**Description**:
- Create `src/scanq_shared/clients/training_studio.py`:
  - `TrainingStudioClient(BaseClient)` with async methods:
    - `resolve_context(project_id, environment_id, actor_id, include_metadata)` → ContextResolveResponse
    - `get_service_token(service_id, scopes, ttl_seconds, metadata)` → ServiceTokenResponse
    - `register_lineage(run_id, dwelling_id, pack_version, initiated_by, environment, metadata)` → LineageRegisterResponse
    - `finalize_lineage(lineage_id, status, summary, metrics)` → LineageFinalizeResponse

**Features**:
- Pydantic request validation before sending
- Pydantic response validation after receiving
- Proper error handling (APIError, ValidationError, TimeoutError)
- Comprehensive docstrings with usage examples
- Logging on errors

**Definition of Done**:
- [ ] All methods implemented and type-annotated
- [ ] Request/response validation works
- [ ] Error handling tested
- [ ] No `mypy --strict` errors
- [ ] Full docstrings with examples

**Tests**:
- `tests/integration/test_training_studio_client.py`:
  - Mock training-studio endpoints using httpx_mock
  - Test each method with valid and invalid responses
  - Test timeout and connection error handling
  - Test request validation (invalid requests rejected locally)

---

## Epic: Testing & Documentation

### Task 1.12: Set Up Test Infrastructure
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Create `tests/conftest.py` with pytest fixtures
- Create `tests/unit/conftest.py` and `tests/integration/conftest.py` if needed
- Create `tests/fixtures/sample_payloads.py` with reusable request/response fixtures
- Configure pytest.ini or pyproject.toml with test settings
- Set up coverage reporting

**Features**:
- Fixtures for common Pydantic models
- Mock training-studio responses (httpx_mock)
- Parametrized tests for valid/invalid inputs

**Definition of Done**:
- [ ] Test directories created
- [ ] Fixtures defined and importable
- [ ] `pytest tests/` runs without errors
- [ ] Coverage report generated

**Tests**: Manual verification

---

### Task 1.13: Unit Tests for Models & Schemas
**Status**: NOT STARTED  
**Effort**: 2d  
**Owner**: (Assign)

**Description**:
- Create `tests/unit/test_models.py`: Test all model validation
- Create `tests/unit/test_schemas.py`: Test request/response parsing
- Create `tests/unit/test_enums.py`: Test enum values
- Create `tests/unit/test_clients.py`: Test exception classes

**Coverage Target**: ≥ 90% for models/schemas/enums

**Definition of Done**:
- [ ] All tests pass: `pytest tests/unit/ -v`
- [ ] Coverage report shows ≥ 90%: `pytest tests/unit/ --cov=src/scanq_shared`

---

### Task 1.14: Integration Tests for TrainingStudioClient
**Status**: NOT STARTED  
**Effort**: 2d  
**Owner**: (Assign)

**Description**:
- Create `tests/integration/test_training_studio_client.py`:
  - Test each client method with mocked endpoints
  - Test error responses and exception mapping
  - Test retry logic (mock transient failures)
  - Test timeout handling

**Coverage Target**: ≥ 80% for client code

**Definition of Done**:
- [ ] All integration tests pass: `pytest tests/integration/ -v`
- [ ] Coverage for client code ≥ 80%

---

### Task 1.15: Type Checking & Linting
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Run `mypy --strict src/scanq_shared` and fix all errors
- Run `ruff check src/scanq_shared tests/` and fix linting issues
- Run `black src/scanq_shared tests/` for formatting (if configured)
- Update `pyproject.toml` with tool configurations

**Definition of Done**:
- [ ] `mypy --strict src/scanq_shared` exits with 0 errors
- [ ] `ruff check` shows no errors
- [ ] All files properly formatted

---

### Task 1.16: Generate API Reference Documentation
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Create `docs/API_REFERENCE.md` with schema and client API reference
- Auto-generate from docstrings (e.g., using pydoc-markdown or pdoc)
- Include examples for all client methods

**Definition of Done**:
- [ ] API_REFERENCE.md is comprehensive and up-to-date
- [ ] All public classes/methods documented

---

### Task 1.17: Create Integration Guide
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Create `docs/INTEGRATION_GUIDE.md`:
  - Installation: `pip install scanq-shared`
  - Import examples
  - TrainingStudioClient usage patterns
  - Error handling best practices
  - Retry and timeout configuration
  - Async/await patterns

**Definition of Done**:
- [ ] Guide covers all consumer use cases (scanq-accreditation, scanq-training-studio)
- [ ] Code examples are tested and correct

---

### Task 1.18: Update README.md
**Status**: NOT STARTED  
**Effort**: 0.5d  
**Owner**: (Assign)

**Description**:
- Update `README.md`:
  - Add installation instructions
  - Add quick-start example (resolve context, get token)
  - Link to API reference and integration guide
  - Update scope section

**Definition of Done**:
- [ ] README is current and accurate
- [ ] Links to docs are correct

---

### Task 1.19: Create CONTRIBUTING.md
**Status**: NOT STARTED  
**Effort**: 0.5d  
**Owner**: (Assign)

**Description**:
- Create `CONTRIBUTING.md`:
  - Development setup (install uv, clone, `uv sync`)
  - Running tests, type checking, linting
  - Release process (version bumping, tagging, publishing)
  - Code style guidelines

**Definition of Done**:
- [ ] Developers can follow guide to set up environment

---

## Epic: Release & Deployment

### Task 1.20: Prepare v1.0.0 Release
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Update `src/scanq_shared/version.py` to `1.0.0`
- Update `pyproject.toml` version to `1.0.0`
- Create `CHANGELOG.md` with v1.0.0 entry
  - Initial stable release
  - Include all extracted models, schemas, clients
  - List breaking changes (none for v1.0)
- Create git tag: `git tag -a v1.0.0 -m "Release 1.0.0: Initial stable release"`

**Definition of Done**:
- [ ] Version bumped in all files
- [ ] CHANGELOG.md created
- [ ] Git tag created

---

### Task 1.21: Set Up GitHub Actions Workflows
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Create `.github/workflows/test.yml`:
  - Run on PR and push to main
  - Run pytest with coverage
  - Run mypy --strict
  - Run ruff check
  - Upload coverage to codecov
- Create `.github/workflows/release.yml`:
  - Trigger on git tag `v*`
  - Build wheel
  - Publish to PyPI (or private repo)
  - Create GitHub Release

**Definition of Done**:
- [ ] Workflows created and tested
- [ ] PR tests pass automatically
- [ ] Release workflow works (dry-run on tag)

---

### Task 1.22: Final QA & Checklist
**Status**: NOT STARTED  
**Effort**: 1d  
**Owner**: (Assign)

**Description**:
- Verify release readiness checklist:
  - [ ] All unit tests passing (pytest --cov ≥ 85%)
  - [ ] All integration tests passing
  - [ ] Type checking passing (mypy --strict)
  - [ ] Linting passing (ruff check)
  - [ ] Documentation updated and accurate
  - [ ] CHANGELOG.md up-to-date
  - [ ] Version bumped in all files
  - [ ] GitHub workflows functional
  - [ ] Package can be installed locally: `pip install -e .`
  - [ ] All public APIs are importable

**Definition of Done**:
- [ ] All checklist items verified
- [ ] Ready for v1.0.0 release

---

## Summary of Deliverables

| Category | Item | Effort |
|----------|------|--------|
| **Models & Schemas** | Enums, base models, training-studio models, context/auth/lineage schemas | 8d |
| **Client** | Base client, exceptions, TrainingStudioClient | 3.5d |
| **Testing** | Test infrastructure, unit tests, integration tests | 5d |
| **Documentation** | API reference, integration guide, README, CONTRIBUTING | 3d |
| **Release** | Versioning, GitHub Actions, final QA | 3d |
| **TOTAL** | | **22.5d** (≈ 3-4 weeks) |

---

## Success Criteria for Phase 1 Completion

✅ **Correctness**: `mypy --strict` and `pytest` pass with zero errors  
✅ **Coverage**: ≥ 85% code coverage  
✅ **Documentation**: All public APIs documented with examples  
✅ **Integration**: scanq-accreditation can import and instantiate `TrainingStudioClient`  
✅ **Release**: v1.0.0 tagged and ready for publishing  

---

## Next Steps (Phase 2+)

After Phase 1 completes:
- **Phase 2**: Integrate scanq-shared into scanq-accreditation CLI
- **Phase 3**: Implement training-studio support endpoints
- **Phase 4**: End-to-end integration testing
