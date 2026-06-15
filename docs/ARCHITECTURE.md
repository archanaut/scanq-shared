# Architecture: scanq-shared Design & Rationale

**Scope**: Design decisions, component boundaries, data flows, and extensibility points

---

## Design Philosophy

### Core Principle: Contracts-Only, No Logic

**scanq-shared is a contract library, not a framework.**

- ✅ Defines request/response schemas using Pydantic
- ✅ Provides typed HTTP clients for cross-service calls
- ✅ Exports enums and base models
- ❌ Does NOT contain business logic (validation pipelines, data transformations)
- ❌ Does NOT contain routers or API definitions
- ❌ Does NOT contain database persistence
- ❌ Does NOT run accreditation workflows

**Rationale**: By staying contracts-only, scanq-shared:
1. Remains lightweight and dependency-free (only Pydantic + httpx)
2. Can be used by any number of services without bloat
3. Acts as the single source of truth for API contracts
4. Avoids version-lock conflicts (services can independently update business logic)

---

## Component Hierarchy

```
scanq-shared/
│
├── enums/                          # Type-safe domain values
│   ├── ServiceStatus, TokenStatus, ContextStatus, ErrorCode, EntityType, LineageEventType
│   └── No dependencies; pure Python enums
│
├── models/                         # Core data structures (no persistence)
│   ├── BaseResponse, ErrorDetail, PaginationParams
│   ├── ProjectModel, EnvironmentModel, ActorModel (training-studio concepts)
│   └── Pydantic BaseModel subclasses; JSON-serializable
│
├── schemas/                        # Request/response API contracts
│   ├── context.py: ContextResolveRequest, ContextResolveResponse
│   ├── auth.py: ServiceTokenRequest, ServiceTokenResponse
│   ├── lineage.py: LineageRegisterRequest/Response, LineageFinalizeRequest/Response
│   ├── errors.py: ErrorSchema
│   └── Mapped 1:1 to training-studio API endpoints
│
└── clients/                        # Typed HTTP clients (no persistence, no logic)
    ├── base.py: BaseClient (retry, timeout, tracing)
    ├── training_studio.py: TrainingStudioClient (resolve_context, get_token, register_lineage, finalize_lineage)
    ├── exceptions.py: ClientError, APIError, TimeoutError, ValidationError
    └── httpx-based async clients; request/response validation built-in
```

---

## Data Flow: Context Resolution Example

```
┌─────────────────────┐
│ scanq-accreditation │
│      CLI            │
└──────────┬──────────┘
           │
           │ create TrainingStudioClient
           ▼
┌──────────────────────────────────┐
│ TrainingStudioClient             │
│                                  │
│ resolve_context(                 │
│   project_id,                    │
│   environment_id,                │
│   actor_id,                      │
│   include_metadata               │
│ )                                │
└──────┬───────────────────────────┘
       │ Validate request (ContextResolveRequest)
       ▼
┌──────────────────────┐
│ ContextResolveRequest│ (Pydantic validation)
│ - project_id (str)  │
│ - environment_id    │
│ - actor_id (opt)    │
│ - include_metadata  │
└──────┬───────────────┘
       │ Serialize to JSON
       │ POST /accreditation/context/resolve
       ▼
┌─────────────────────────┐
│ training-studio API     │
│ (scanq-training-studio) │
│                         │
│ Lookup project,         │
│ environment, actor      │
│ in PostgreSQL           │
└──────┬──────────────────┘
       │ JSON response
       ▼
┌──────────────────────────────┐
│ ContextResolveResponse       │ (Pydantic validation)
│ - status: ContextStatus      │
│ - project_id, project_name   │
│ - environment_id, name       │
│ - actor_id, actor_name       │
│ - resolved_at: datetime      │
│ - metadata: dict             │
│ - request_id: str            │
└──────┬───────────────────────┘
       │ Typed response object returned
       │ to scanq-accreditation CLI
       ▼
┌──────────────────────────────┐
│ scanq-accreditation CLI      │
│                              │
│ Use resolved context:        │
│ - project_name              │
│ - environment_name          │
│ - actor_name                │
│                              │
│ Continue workflow...        │
└──────────────────────────────┘
```

---

## Dependency Justification

### Pydantic v2

**Why**: Data validation and JSON serialization with strict types

```python
from pydantic import BaseModel, Field

class ContextResolveResponse(BaseModel):
    project_id: str = Field(..., description="...")
    resolved_at: datetime = Field(...)
```

**Alternative**: dataclasses + json module
- **Rejected**: Less strict validation, manual serialization, no field metadata

### httpx

**Why**: Modern async/sync HTTP client with retry and timeout support

```python
client = httpx.AsyncClient()
response = await client.get(url, timeout=30)
```

**Alternative**: requests library
- **Rejected**: Sync-only, less control over retries, no built-in async

### typing-extensions

**Why**: Backport modern Python typing to 3.14+

```python
from typing_extensions import TypeAlias

MyType: TypeAlias = str | int
```

**Alternative**: Native Python 3.10+ syntax
- **Rejected**: Need compatibility with 3.14+, typing-extensions ensures portability

---

## API Endpoint Mapping

**Training-Studio Support Endpoints** (implemented by scanq-training-studio, contracted by scanq-shared):

| Endpoint | Client Method | Request | Response |
|----------|---------------|---------|----------|
| `POST /accreditation/context/resolve` | `resolve_context()` | `ContextResolveRequest` | `ContextResolveResponse` |
| `POST /accreditation/auth/service-token` | `get_service_token()` | `ServiceTokenRequest` | `ServiceTokenResponse` |
| `POST /accreditation/lineage/register` | `register_lineage()` | `LineageRegisterRequest` | `LineageRegisterResponse` |
| `POST /accreditation/lineage/{id}/finalize` | `finalize_lineage()` | `LineageFinalizeRequest` | `LineageFinalizeResponse` |

All responses include:
- `status` (success/error indicator)
- `timestamp` (UTC)
- `request_id` (tracing)

All errors return:
- `code` (machine-readable error code)
- `message` (human-readable)
- `details` (additional context)
- `status_code` (HTTP status)

---

## Extensibility Points

### Future Client: ScanQ App API Client

When scanq-accreditation needs to call ScanQ App API:

```python
# src/scanq_shared/clients/scanq_app.py

class ScanQAppClient(BaseClient):
    """Client for ScanQ App dwelling scenario execution."""
    
    async def validate_dwelling(self, dwelling_id: str) -> ValidationResponse:
        """POST /api/dwellings/{id}/validate"""
        ...
    
    async def generate_dwelling(self, dwelling_id: str) -> GenerateResponse:
        """POST /api/dwellings/{id}/generate"""
        ...
    
    async def run_dwelling_scenario(self, dwelling_id: str, scenario_id: str) -> RunResponse:
        """POST /api/dwellings/{id}/scenarios/{scenario_id}/run"""
        ...
```

**Process**:
1. Extract ScanQ App API schemas into `schemas/scanq_app.py`
2. Create `ScanQAppClient` in `clients/scanq_app.py`
3. Export from `clients/__init__.py`
4. Increment MINOR version (v1.1.0)

---

### Future Client: Jira Integration

```python
# src/scanq_shared/clients/jira.py

class JiraClient(BaseClient):
    """Client for Jira issue creation/updates."""
    
    async def create_defect_issue(self, issue: JiraIssueRequest) -> JiraIssueResponse:
        """POST /rest/api/3/issues"""
        ...
    
    async def update_issue_status(self, issue_id: str, status: str) -> JiraIssueResponse:
        """PUT /rest/api/3/issues/{id}"""
        ...
```

---

### Future Schema: Confluence Publishing

```python
# src/scanq_shared/schemas/confluence.py

class ConfluencePublishRequest(BaseModel):
    """Request to publish evidence to Confluence."""
    
    space_key: str
    page_title: str
    content_html: str
    parent_page_id: str | None = None


class ConfluencePublishResponse(BaseModel):
    """Response from Confluence publish."""
    
    page_id: str
    page_url: str
    published_at: datetime
```

---

## Backward Compatibility Strategy

### MINOR Version: New Client or Schema

```python
# v1.0.0
class TrainingStudioClient(BaseClient):
    async def resolve_context(...) -> ContextResolveResponse: ...
    async def get_service_token(...) -> ServiceTokenResponse: ...

# v1.1.0 - New method, backward compatible
class TrainingStudioClient(BaseClient):
    async def resolve_context(...) -> ContextResolveResponse: ...
    async def get_service_token(...) -> ServiceTokenResponse: ...
    
    # NEW
    async def batch_resolve_context(...) -> list[ContextResolveResponse]: ...
```

Old code continues to work:
```python
# v1.0.0 consumer code
client = TrainingStudioClient(...)
context = await client.resolve_context(...)  # ✅ Still works in v1.1.0
```

### MAJOR Version: Schema Change

```python
# v1.0.0
class ContextResolveResponse(BaseModel):
    project_id: str
    environment_id: str
    resolved_at: datetime

# v2.0.0 - Breaking change (different structure)
class ContextResolveResponse(BaseModel):
    context: ContextData  # WRAPPED in object (breaking)
    resolved_at: datetime

# OLD CODE BREAKS:
context = await client.resolve_context(...)
print(context.project_id)  # ❌ AttributeError in v2.0.0
```

**Mitigation**:
- Clear MIGRATION.md guide
- 30-day deprecation notice
- Support v1.x for security fixes for 6+ months

---

## Testing Strategy

### Unit Tests: Model & Schema Validation

```python
# tests/unit/test_models.py

def test_context_response_required_fields():
    """Validate required field check."""
    with pytest.raises(ValidationError):
        ContextResolveResponse(
            status="resolved",
            project_id="proj-123"
            # MISSING: environment_id, resolved_at
        )

def test_enum_serialization():
    """Validate enum string conversion."""
    response = ContextResolveResponse(
        status=ContextStatus.RESOLVED,
        ...
    )
    assert response.model_dump()["status"] == "resolved"
```

### Integration Tests: Client Methods

```python
# tests/integration/test_training_studio_client.py

async def test_resolve_context_success(httpx_mock):
    """Mock training-studio and test client call."""
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8000/accreditation/context/resolve",
        json=CONTEXT_RESOLVE_RESPONSE,
        status_code=200,
    )
    
    async with TrainingStudioClient("http://localhost:8000") as client:
        response = await client.resolve_context("proj-123", "env-staging")
        assert response.project_id == "proj-123"
```

### Type Checking: mypy --strict

```bash
$ mypy --strict src/scanq_shared/
Success: no issues found in 1 source file
```

---

## Performance Characteristics

### Startup Time

- **Package import**: < 10ms (Pydantic model loading)
- **Client instantiation**: < 5ms (no network calls)
- **First request**: 50-200ms (network round-trip depends on training-studio latency)

### Memory

- **Base package**: ~5 MB (Pydantic, httpx, typing-extensions)
- **Client per instance**: ~1 KB (async client handle)

### Network

- **Request timeout**: Configurable (default: 30s)
- **Retry policy**: Up to 3 retries on transient failures (configurable)
- **Connection pooling**: Built-in via httpx

---

## Security Considerations

### No Credential Storage

scanq-shared does NOT store:
- API keys
- Passwords
- Tokens
- Database credentials

**Consumer's responsibility**: Pass credentials/tokens as parameters to client methods.

### Request/Response Validation

All requests and responses validated by Pydantic before use:
- Type mismatch detected early
- Invalid data rejected with clear error messages
- Prevents injection attacks from malformed JSON

### HTTPS Support

```python
client = TrainingStudioClient(
    base_url="https://training-studio.example.com",  # ✅ HTTPS
    timeout=30
)
```

---

## Deployment & Distribution

### Package Publishing

1. **GitHub Releases**: Tagged releases with source distributions
2. **PyPI (Python Package Index)**:
   ```bash
   # Install from PyPI
   pip install scanq-shared
   
   # Or specific version
   pip install scanq-shared==1.0.0
   ```
3. **Private Repo** (if Archanaut has internal PyPI):
   ```bash
   pip install --index-url https://private-pypi.archanaut.com/ scanq-shared
   ```

### Version Management

Each release tagged as `vX.Y.Z`:
```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

CI/CD workflow publishes to PyPI on tag.

---

## Migration Path: scanq-shared v1 → v2 (Hypothetical)

### Before (v1.x)

```python
from scanq_shared.clients import TrainingStudioClient

client = TrainingStudioClient("http://...")
context = await client.resolve_context("proj-123", "env-staging")
print(context.project_id)
```

### After (v2.0.0)

```python
from scanq_shared.clients import TrainingStudioClient

client = TrainingStudioClient("http://...")

# Schema changed: context is now nested
context = await client.resolve_context("proj-123", "env-staging")
print(context.context.project.id)  # Different structure
```

**Migration Guide (MIGRATION.md)**:
1. Update pyproject.toml dependency to `scanq-shared>=2.0.0`
2. Replace `context.project_id` with `context.context.project.id`
3. Run tests: `pytest tests/`
4. Verify type checking: `mypy --strict`

---

## Roadmap: Future Phases

### Phase 2: Consumer Integration
- Integrate scanq-shared into scanq-accreditation CLI
- Implement training-studio support endpoints

### Phase 3: Extended Clients
- ScanQ App API client (validate, generate, run scenarios)
- Jira client (create/update issues)

### Phase 4: Advanced Features
- Request/response caching (optional)
- Circuit breaker pattern for fault tolerance
- Distributed tracing integration (OpenTelemetry)

---

## Glossary

| Term | Definition |
|------|-----------|
| **Contract** | Request/response schema that defines API communication |
| **Schema** | Pydantic model defining request or response structure |
| **Model** | Core data structure (ProjectModel, ActorModel, etc.) |
| **Enum** | Type-safe enumeration (TokenStatus, ErrorCode) |
| **Client** | Typed HTTP client (TrainingStudioClient, etc.) |
| **Lineage** | Audit trail of accreditation run (who, when, what) |
| **Context** | Project, environment, and actor information |
