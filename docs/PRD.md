# Product Requirements Document: scanq-shared

**Version**: 1.0  
**Date**: June 15, 2026  
**Status**: Active Development  
**Architecture**: Option E (Hybrid) — Shared Contracts Only

---

## Executive Summary

**scanq-shared** is a Python SDK package that serves as the single source of truth for request/response models, enums, and typed HTTP clients shared between **scanq-accreditation** and **scanq-training-studio**. It enables type-safe cross-service integration while maintaining strict separation of concerns: no routers, no persistence, no runtime pipeline logic.

---

## Scope

### In Scope (What scanq-shared Owns)

1. **Data Models & Schemas**
   - Request/response Pydantic models for all public APIs
   - Enums for status values, error codes, entity types, and domain concepts
   - Shared error schemas with standardized HTTP codes and error categories

2. **Typed HTTP Clients**
   - `TrainingStudioClient` for calling scanq-training-studio support endpoints:
     - Context resolution (project, environment, actor lookup)
     - Auth service token issuance
     - Lineage registration and finalization
   - Optional clients for future integrations (e.g., ScanQ App API, Jira)
   - Built on `httpx` with proper retry logic, timeout handling, and tracing hooks

3. **Type Hints & Validation**
   - Full type annotations for all public APIs
   - Pydantic v2 validation with strict mode
   - Python 3.14+ compatibility

4. **Documentation**
   - Inline docstrings (Google style) for all classes and methods
   - Schema reference documentation
   - Integration examples for consumers

### Out of Scope (Non-Goals)

1. **No API Routers** — FastAPI/Starlette route definitions and request handlers
2. **No Database Persistence** — ORM models, database schemas, migration scripts
3. **No Accreditation Runtime Logic** — Validation pipelines, scenario execution, evidence generation
4. **No Training-Studio Runtime Logic** — Media generation, provider adapters, project management
5. **No Admin/CLI Entrypoints** — Click commands, Typer decorators
6. **No Deployment Artifacts** — Docker definitions, Kubernetes manifests, CI/CD workflows

---

## Success Metrics

### Phase 1 (Extraction & Initial Release)

- ✅ **Correctness**: All extracted contracts pass type checking (`mypy --strict`) and validation tests
- ✅ **Completeness**: 100% of training-studio support endpoint schemas captured in `TrainingStudioClient`
- ✅ **Usability**: Accreditation CLI can instantiate and use `TrainingStudioClient` without modification
- ✅ **Coverage**: Minimum 85% code coverage for contracts and client logic (excluding external API calls)
- ✅ **Documentation**: All public classes/methods have docstrings with usage examples

### Phase 2 (Consumer Integration)

- ✅ **Adoption**: scanq-accreditation depends on v1.0+ with zero breaking changes in CLI
- ✅ **Compatibility**: scanq-training-studio can satisfy all endpoints defined in schemas
- ✅ **Performance**: HTTP client round-trip time < 200ms at p95 (local/staging)

### Phase 3 (Versioning & Stability)

- ✅ **Semantic Versioning**: Strict MAJOR.MINOR.PATCH with backward-compatible guarantee for MINOR/PATCH
- ✅ **Migration Path**: Clear upgrade guide if breaking changes required (MAJOR bump)
- ✅ **Support Window**: v1.x supported for 12 months minimum

---

## Key Requirements

### Consumer Requirements

1. **scanq-accreditation Requirements**
   - Import and instantiate `TrainingStudioClient` with zero additional setup
   - Call context resolve, token issuance, lineage register/finalize endpoints
   - Receive typed response objects with proper error handling
   - All requests respect timeouts and retry policies

2. **scanq-training-studio Requirements**
   - Use models from scanq-shared for request validation
   - Return response objects matching scanq-shared schemas
   - Support all documented HTTP methods and status codes

### Technical Requirements

1. **Type Safety**
   - Pass `mypy --strict` with zero errors
   - All function signatures fully annotated
   - No `Any` types except where strictly unavoidable (with comments)

2. **Testing**
   - Unit tests for all model validation edge cases
   - Integration tests for HTTP client (mocked backends)
   - No external API calls during test runs

3. **Compatibility**
   - Supported Python versions: 3.14+
   - Pinned dependency versions in `pyproject.toml`
   - No platform-specific code

4. **Performance**
   - Client instantiation < 10ms
   - Startup time with full schema validation < 50ms

---

## Constraints & Assumptions

### Constraints

- Must not import or depend on FastAPI, SQLAlchemy, Click, or other consumer-specific libraries
- Must not contain hardcoded URLs, API keys, or environment-specific values
- Must not implement business logic beyond data validation and HTTP transport

### Assumptions

- Consumers (accreditation, training-studio) handle all authentication token lifecycle
- training-studio endpoints are HTTP-accessible and follow REST conventions
- Request/response bodies are JSON (no multipart, protobuf, etc.)
- Errors follow a consistent HTTP 4xx/5xx + JSON body pattern

---

## Release & Versioning Strategy

### Initial Release: v1.0.0

**Timeline**: June 2026 (end of Phase 1 extraction)

**Contents**:
- Core data models and enums
- `TrainingStudioClient` with context, auth, lineage endpoints
- Full type annotations and docstrings
- 85%+ test coverage

### Backward Compatibility Policy

- **MAJOR version** (1.0 → 2.0): Breaking changes allowed (consumers must upgrade code)
- **MINOR version** (1.x → 1.y): New features and endpoints; fully backward compatible
- **PATCH version** (1.x.0 → 1.x.1): Bug fixes only; no schema changes

### Deprecation

- Deprecated endpoints/models will be marked with `@deprecated()` decorator
- 2 MINOR version releases (e.g., v1.1 → v1.2 → v1.3) before removal
- Deprecation notices in release notes and docstrings

---

## Success Criteria: Launch Checkpoint

Before marking Phase 1 complete:

1. ✅ All training-studio support endpoint schemas extracted to `TrainingStudioClient`
2. ✅ `mypy --strict` passes with zero errors
3. ✅ pytest coverage ≥ 85%
4. ✅ scanq-accreditation successfully imports and instantiates client
5. ✅ All public APIs documented with examples
6. ✅ v1.0.0 tagged and ready for release
