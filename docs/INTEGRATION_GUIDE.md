# Integration Guide: Using scanq-shared

**Audience**: Developers of scanq-accreditation and scanq-training-studio  
**Focus**: Installation, usage patterns, error handling, configuration

---

## Installation

### For scanq-accreditation

```bash
# Add to pyproject.toml [project] dependencies
scanq-shared>=1.0.0,<2.0.0

# Or install directly
pip install scanq-shared>=1.0.0
# or
uv pip install scanq-shared>=1.0.0
```

### For scanq-training-studio

```bash
# Add to pyproject.toml [project] dependencies
scanq-shared>=1.0.0,<2.0.0

# Verify installation
python -c "from scanq_shared import __version__; print(__version__)"
```

---

## Basic Usage: scanq-accreditation CLI

### Scenario 1: Resolve Dwelling Context

```python
import asyncio
from scanq_shared.clients import TrainingStudioClient

async def resolve_dwelling_context():
    """Resolve project, environment, and actor context."""
    async with TrainingStudioClient("http://training-studio:8000") as client:
        context = await client.resolve_context(
            project_id="proj-archanaut",
            environment_id="env-staging",
            actor_id="actor-accreditation-service",
            include_metadata=True
        )
        
        print(f"Project: {context.project_name}")
        print(f"Environment: {context.environment_name}")
        print(f"Actor: {context.actor_name}")
        
        return context

# Usage in CLI command
context = asyncio.run(resolve_dwelling_context())
```

### Scenario 2: Get Service Authentication Token

```python
async def get_auth_token():
    """Issue short-lived authentication token."""
    async with TrainingStudioClient("http://training-studio:8000") as client:
        token_response = await client.get_service_token(
            service_id="scanq-accreditation",
            scopes=["read:context", "write:lineage"],
            ttl_seconds=3600  # 1 hour
        )
        
        print(f"Token expires in: {token_response.expires_in} seconds")
        print(f"Scopes: {', '.join(token_response.scopes)}")
        
        # Use token in subsequent requests
        headers = {
            "Authorization": f"{token_response.token_type} {token_response.token}"
        }
        
        return token_response

token = asyncio.run(get_auth_token())
```

### Scenario 3: Register Accreditation Run Lineage

```python
async def register_run_lineage(run_id: str, dwelling_id: str):
    """Register lineage for audit trail."""
    async with TrainingStudioClient("http://training-studio:8000") as client:
        lineage = await client.register_lineage(
            run_id=run_id,
            dwelling_id=dwelling_id,
            pack_version="v1.0.0",
            initiated_by="ci-pipeline",
            environment="staging",
            metadata={
                "git_commit": "abc123def456",
                "ci_job_id": "gh-actions-12345"
            }
        )
        
        print(f"Lineage ID: {lineage.lineage_id}")
        return lineage.lineage_id

run_id = "run-dwelling-101-2026-06-15-143022"
dwelling_id = "dwelling-nathrs-uip-101"
lineage_id = asyncio.run(register_run_lineage(run_id, dwelling_id))
```

### Scenario 4: Finalize Accreditation Run Lineage

```python
async def finalize_run_lineage(lineage_id: str, metrics: dict):
    """Finalize lineage after run completes."""
    async with TrainingStudioClient("http://training-studio:8000") as client:
        result = await client.finalize_lineage(
            lineage_id=lineage_id,
            status="finalized",
            summary="All 42 validation scenarios passed",
            metrics={
                "total_scenarios": 42,
                "passed": 42,
                "failed": 0,
                "evidence_items": 15
            }
        )
        
        print(f"Finalized at: {result.finalized_at}")
        return result

metrics = {"total": 42, "passed": 42}
result = asyncio.run(finalize_run_lineage(lineage_id, metrics))
```

---

## Basic Usage: scanq-training-studio

### Using Request Models for Validation

```python
from fastapi import FastAPI, HTTPException
from scanq_shared.schemas import ContextResolveRequest, ContextResolveResponse
from scanq_shared.enums import ContextStatus

app = FastAPI()

@app.post("/accreditation/context/resolve", response_model=ContextResolveResponse)
async def resolve_context(request: ContextResolveRequest) -> ContextResolveResponse:
    """
    FastAPI automatically:
    1. Validates request against ContextResolveRequest schema
    2. Converts response to ContextResolveResponse schema
    3. Serializes to JSON
    """
    
    # Your logic here
    project = fetch_project(request.project_id)
    environment = fetch_environment(request.environment_id)
    
    if not project or not environment:
        return ContextResolveResponse(
            status=ContextStatus.NOTFOUND,
            project_id=request.project_id,
            environment_id=request.environment_id,
            resolved_at=datetime.utcnow()
        )
    
    return ContextResolveResponse(
        status=ContextStatus.RESOLVED,
        project_id=project.id,
        project_name=project.name,
        environment_id=environment.id,
        environment_name=environment.name,
        resolved_at=datetime.utcnow(),
        metadata={"region": "us-west-2"}
    )
```

---

## Error Handling

### Common Client Errors

```python
from scanq_shared.clients import TrainingStudioClient
from scanq_shared.clients.exceptions import (
    ClientError,
    APIError,
    TimeoutError,
    ValidationError,
    ConnectionError,
)

async def resolve_with_error_handling():
    try:
        async with TrainingStudioClient("http://training-studio:8000") as client:
            context = await client.resolve_context(
                project_id="proj-123",
                environment_id="env-staging"
            )
            return context
    
    except ValidationError as e:
        # Request or response validation failed
        print(f"Validation error: {e.message}")
        print(f"Details: {e.details}")
        return None
    
    except APIError as e:
        # Server returned 4xx or 5xx
        print(f"API error {e.status_code}: {e.message} ({e.code})")
        if e.status_code == 404:
            print("Context not found")
        elif e.status_code == 401:
            print("Token expired or invalid")
        return None
    
    except TimeoutError as e:
        # Request timed out
        print(f"Timeout after {e.timeout_seconds}s on {e.operation}")
        return None
    
    except ConnectionError as e:
        # Connection failed
        print(f"Connection failed to {e.url}: {e.message}")
        return None
    
    except ClientError as e:
        # Generic client error
        print(f"Client error: {e.message}")
        return None
```

### Retry Configuration

```python
from scanq_shared.clients import TrainingStudioClient

# Custom retry and timeout settings
client = TrainingStudioClient(
    base_url="http://training-studio:8000",
    timeout=60,           # 60-second timeout
    max_retries=5,        # Retry up to 5 times
    trace_requests=True   # Enable debug logging
)
```

---

## Data Models & Schemas

### Using Enums

```python
from scanq_shared.enums import (
    TokenStatus,
    ContextStatus,
    LineageEventType,
    ErrorCode,
)

# Serialize enum to string
status = TokenStatus.ACTIVE
status_str = status.value  # "active"

# Parse string to enum
status_parsed = TokenStatus(status_str)

# Type-safe comparison
if status == TokenStatus.ACTIVE:
    print("Token is active")
```

### Using Pydantic Models

```python
from scanq_shared.schemas import ContextResolveResponse
from datetime import datetime

# Create from dict
data = {
    "status": "resolved",
    "project_id": "proj-123",
    "environment_id": "env-456",
    "resolved_at": "2026-06-15T10:30:00Z",
}
response = ContextResolveResponse(**data)

# Serialize to dict
response_dict = response.model_dump()

# Serialize to JSON
response_json = response.model_dump_json()

# Type-safe access
print(response.project_id)  # IDE autocomplete works
```

---

## Async vs. Sync Usage

### Async (Recommended)

```python
import asyncio
from scanq_shared.clients import TrainingStudioClient

async def main():
    async with TrainingStudioClient("http://...") as client:
        context = await client.resolve_context("proj-123", "env-staging")
    # Context manager closes client automatically

asyncio.run(main())
```

### Sync with asyncio.run()

```python
from scanq_shared.clients import TrainingStudioClient
import asyncio

def get_context():
    async def _async_get():
        async with TrainingStudioClient("http://...") as client:
            return await client.resolve_context("proj-123", "env-staging")
    
    return asyncio.run(_async_get())

context = get_context()
```

### Manual Client Lifecycle

```python
from scanq_shared.clients import TrainingStudioClient
import asyncio

async def main():
    client = TrainingStudioClient("http://...")
    await client.__aenter__()
    
    try:
        context = await client.resolve_context("proj-123", "env-staging")
        print(context)
    finally:
        await client.__aexit__(None, None, None)

asyncio.run(main())
```

---

## Configuration & Best Practices

### Environment Variables

```python
import os
from scanq_shared.clients import TrainingStudioClient

# Configure from environment
TRAINING_STUDIO_URL = os.getenv("TRAINING_STUDIO_URL", "http://localhost:8000")
TRAINING_STUDIO_TIMEOUT = int(os.getenv("TRAINING_STUDIO_TIMEOUT", "30"))
TRAINING_STUDIO_RETRIES = int(os.getenv("TRAINING_STUDIO_RETRIES", "3"))

client = TrainingStudioClient(
    base_url=TRAINING_STUDIO_URL,
    timeout=TRAINING_STUDIO_TIMEOUT,
    max_retries=TRAINING_STUDIO_RETRIES,
    trace_requests=os.getenv("DEBUG") == "true"
)
```

### Logging

```python
import logging

# Enable trace logging
logging.basicConfig(level=logging.DEBUG)

# scanq-shared uses Python's standard logging
logger = logging.getLogger("scanq_shared.clients")
logger.setLevel(logging.DEBUG)

client = TrainingStudioClient(
    "http://...",
    trace_requests=True  # Logs all requests/responses
)
```

### Request Tracing

```python
from scanq_shared.schemas import ContextResolveRequest

# Include correlation IDs for tracing
request = ContextResolveRequest(
    project_id="proj-123",
    environment_id="env-staging"
)

# Request ID is auto-populated by service
# Use in logs for tracing across services
async with TrainingStudioClient("http://...") as client:
    response = await client.resolve_context(**request.model_dump())
    print(f"Request ID: {response.request_id}")  # Trace this in logs
```

---

## Dependency Pinning

### In Consumer Projects

```toml
# pyproject.toml

[project]
dependencies = [
  "scanq-shared>=1.0.0,<2.0.0",  # Lock major version only
]

[dependency-groups]
dev = [
  "pytest>=8.3.3",
  "mypy>=1.11.2",
]
```

### Version Compatibility

```python
from scanq_shared import __version__

# Check version at runtime
if __version__.startswith("1."):
    print("Using scanq-shared v1")
elif __version__.startswith("2."):
    print("Using scanq-shared v2 (breaking changes possible)")
```

---

---

## Usage: ML Inference Service

### Scenario 1: Trace Floor Plan

```python
import asyncio
from scanq_shared.clients import MLInferenceClient
from scanq_shared.models import FloorPlanTraceRequest

async def trace_floor_plan():
    """Trace floor plan using configured tool adapter."""
    async with MLInferenceClient("http://scanq-ml-inference:8000") as ml_client:
        response = await ml_client.trace_floor_plan(
            FloorPlanTraceRequest(
                dwelling_id="dwelling-101",
                floor_plan_pdf_path="s3://bucket/dwelling-101.pdf",
                include_ocr=True,
                tool_preference="auto"  # Use best available tool
            )
        )
        
        print(f"Tool used: {response.tool_used}")
        print(f"Confidence: {response.confidence_score:.2%}")
        print(f"Warnings: {response.warnings}")
        
        return response

trace = asyncio.run(trace_floor_plan())
```

### Scenario 2: Extract NatHERS Attributes

```python
async def extract_attributes():
    """Extract NatHERS-specific attributes from traced floor plan."""
    async with MLInferenceClient("http://scanq-ml-inference:8000") as ml_client:
        response = await ml_client.extract_attributes(
            NatHERSAttributesRequest(
                dwelling_id="dwelling-101",
                floor_plan_pdf_path="s3://bucket/dwelling-101.pdf",
                specification_pdf_path="s3://bucket/dwelling-101-spec.pdf",
                extract_scale=True,
                extract_windows=True,
                extract_materials=True,
                extract_hvac=True,
                extract_zoning=True
            )
        )
        
        print(f"Overall confidence: {response.overall_confidence:.2%}")
        print(f"Windows extracted: {len(response.windows)}")
        print(f"Review required: {response.review_required}")
        
        if response.review_required:
            print(f"Reasons: {response.review_reasons}")
        
        # Use extracted attributes for downstream processing
        for window in response.windows:
            print(f"  {window.location}: {window.type} (confidence: {window.confidence:.2%})")
        
        return response

attributes = asyncio.run(extract_attributes())
```

### Scenario 3: Integrated Accreditation Workflow

```python
async def accreditation_with_ml_assist(dwelling_id: str, floor_plan_path: str):
    """Accreditation workflow with optional ML attribute pre-extraction."""
    
    # Step 1: Optional ML pre-assist
    ml_attributes = None
    if config.enable_ml_assist:
        async with MLInferenceClient("http://scanq-ml-inference:8000") as ml_client:
            ml_response = await ml_client.extract_attributes(
                NatHERSAttributesRequest(
                    dwelling_id=dwelling_id,
                    floor_plan_pdf_path=floor_plan_path,
                    extract_windows=True,
                    extract_materials=True
                )
            )
            
            if ml_response.overall_confidence >= 0.75:
                ml_attributes = ml_response
                logger.info(
                    "ml_attributes_available",
                    dwelling_id=dwelling_id,
                    confidence=ml_response.overall_confidence
                )
            else:
                logger.warning(
                    "ml_attributes_low_confidence",
                    dwelling_id=dwelling_id,
                    confidence=ml_response.overall_confidence,
                    reasons=ml_response.review_reasons
                )
    
    # Step 2: Standard accreditation validation and run
    # (ML attributes are optional hints; human expert judgment is always final)
    validator = DwellingValidator(dwelling_id, floor_plan_path)
    
    if ml_attributes:
        # Pass ML hints to validator (for pre-filling review UI, etc.)
        validator.set_ml_hints(ml_attributes)
    
    validation_result = await validator.validate()
    
    # Step 3: Human expert review (mandatory)
    if validation_result.has_issues:
        await route_to_expert_review(validation_result, ml_attributes)
    
    return validation_result

# In accreditation CLI
result = asyncio.run(
    accreditation_with_ml_assist(
        dwelling_id="dwelling-101",
        floor_plan_path="./data/sources/floor_plans/dwelling_101.pdf"
    )
)
```

### Error Handling for ML Service

```python
async def robust_ml_extract(dwelling_id: str, floor_plan_path: str):
    """Robust extraction with fallback if ML service unavailable."""
    try:
        async with MLInferenceClient("http://scanq-ml-inference:8000", timeout=30) as ml_client:
            response = await ml_client.extract_attributes(
                NatHERSAttributesRequest(
                    dwelling_id=dwelling_id,
                    floor_plan_pdf_path=floor_plan_path
                )
            )
            return response
    
    except TimeoutError:
        logger.warning(
            "ml_service_timeout",
            dwelling_id=dwelling_id,
            fallback="human_only"
        )
        return None  # Fall back to manual review
    
    except ConnectionError:
        logger.warning(
            "ml_service_unavailable",
            dwelling_id=dwelling_id,
            fallback="human_only"
        )
        return None  # Fall back to manual review
    
    except Exception as e:
        logger.error(
            "ml_service_error",
            dwelling_id=dwelling_id,
            error=str(e),
            fallback="human_only"
        )
        return None  # Always fallback gracefully

# Usage
ml_response = asyncio.run(robust_ml_extract("dwelling-101", "floor_plan.pdf"))
if ml_response is None:
    print("ML service unavailable; proceeding with manual review only")
```

---

## Common Pitfalls

### ❌ Creating Client Without Context Manager

```python
# BAD: Client not closed properly
client = TrainingStudioClient("http://...")
context = await client.resolve_context("proj-123", "env-staging")
# httpx.AsyncClient is never closed; connection leaks
```

### ✅ Correct: Use Context Manager

```python
# GOOD: Client closed automatically
async with TrainingStudioClient("http://...") as client:
    context = await client.resolve_context("proj-123", "env-staging")
# Client is properly closed
```

### ❌ Not Handling Timeouts

```python
# BAD: Unhandled timeout
async with TrainingStudioClient("http://...", timeout=5) as client:
    context = await client.resolve_context(...)  # May raise TimeoutError
```

### ✅ Correct: Handle Timeouts

```python
# GOOD: Catch and handle timeouts
try:
    async with TrainingStudioClient("http://...", timeout=5) as client:
        context = await client.resolve_context(...)
except TimeoutError:
    logger.error("Request timed out; falling back to cached context")
    context = get_cached_context()
```

---

## Support

For issues, questions, or contributions:
- GitHub: [scanq-shared](https://github.com/archanaut/scanq-shared)
- Docs: See [API_REFERENCE.md](API_REFERENCE.md) and [TRD.md](TRD.md)
- Report bugs: GitHub Issues
