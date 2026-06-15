# Contract: ML Inference Service Endpoints

**Feature**: `002-shared-contracts-ml-models`
**Date**: 2026-06-15
**Scope**: ML inference service REST/JSON API — shared request/response shapes exposed via `MLInferenceClient`

---

## Overview

This contract documents the two ML inference endpoints that `MLInferenceClient` covers.
Both endpoints accept JSON bodies and return JSON responses. The implemented Pydantic models defined
in `src/scanq_shared/models/ml_inference.py` are the canonical contract — this document
describes them in an interface-first format for cross-team review.

---

## Endpoint 1: Floor-Plan Tracing

**Method**: `POST`
**Path**: `/ml/floor-plan/trace`
**Client method**: `MLInferenceClient.trace_floor_plan(request: FloorPlanTraceRequest) → FloorPlanTraceResponse`

### Request (`FloorPlanTraceRequest`)

```json
{
  "dwelling_id": "dwelling-nathrs-uip-101",
  "image_url": "https://storage.scanq.internal/floor-plans/uip-101.png",
  "image_format": "png",
  "extract_windows": true,
  "extract_walls": true,
  "metadata": {
    "job_id": "job-abc123",
    "initiated_by": "ci-pipeline"
  }
}
```

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `dwelling_id` | string | ✅ | — | min 1 char |
| `image_url` | string | ✅ | — | Internal storage URL |
| `image_format` | string | — | `"png"` | `png`, `jpg`, or `pdf` |
| `extract_windows` | boolean | — | `true` | Enable window element extraction |
| `extract_walls` | boolean | — | `true` | Enable wall element extraction |
| `metadata` | object | — | `{}` | String key-value pairs |

### Response (`FloorPlanTraceResponse`)

**Success (200)**:
```json
{
  "dwelling_id": "dwelling-nathrs-uip-101",
  "status": "completed",
  "features": {
    "windows": [
      {
        "window_id": "w-001",
        "width_m": 1.2,
        "height_m": 1.5,
        "orientation": "N",
        "glazing_type": "double",
        "frame_type": "aluminium",
        "confidence": "high"
      }
    ],
    "total_window_area_m2": 1.8,
    "external_wall_area_m2": 42.5,
    "glazing_ratio": 0.042,
    "confidence": "high"
  },
  "confidence": {
    "level": "high",
    "score": 0.91,
    "model_version": "fp-tracer-v2.1.0",
    "notes": null
  },
  "processing_time_ms": 842,
  "request_id": "req-uuid-abc"
}
```

**Partial/low-confidence (200)**:
```json
{
  "dwelling_id": "dwelling-nathrs-uip-202",
  "status": "completed",
  "features": {
    "windows": [],
    "total_window_area_m2": null,
    "external_wall_area_m2": null,
    "glazing_ratio": null,
    "confidence": "insufficient"
  },
  "confidence": {
    "level": "insufficient",
    "score": 0.12,
    "model_version": "fp-tracer-v2.1.0",
    "notes": "Image resolution too low for reliable extraction"
  },
  "processing_time_ms": 390,
  "request_id": "req-uuid-xyz"
}
```

**Error (422 — Validation)**:
```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "status_code": 422,
    "details": {"field": "image_url", "reason": "must not be empty"},
    "request_id": "req-uuid-err"
  },
  "request_id": "req-uuid-err"
}
```

---

## Endpoint 2: NatHERS Attribute Extraction

**Method**: `POST`
**Path**: `/ml/nathers/attributes`
**Client method**: `MLInferenceClient.extract_nathers_attributes(request: NatHERSAttributeRequest) → NatHERSAttributeResponse`

### Request (`NatHERSAttributeRequest`)

```json
{
  "dwelling_id": "dwelling-nathrs-uip-101",
  "floor_plan_features": {
    "windows": [
      {
        "width_m": 1.2,
        "height_m": 1.5,
        "orientation": "N",
        "confidence": "high"
      }
    ],
    "total_window_area_m2": 1.8,
    "external_wall_area_m2": 42.5,
    "glazing_ratio": 0.042,
    "confidence": "high"
  },
  "configuration": {
    "climate_zone": "6",
    "floor_area_m2": 185.0,
    "num_bedrooms": 4,
    "num_storeys": 2,
    "construction_year": 2018,
    "orientation_degrees": 15.0
  },
  "metadata": {}
}
```

### Response (`NatHERSAttributeResponse`)

**Success (200)**:
```json
{
  "dwelling_id": "dwelling-nathrs-uip-101",
  "status": "completed",
  "predicted_rating": 6.5,
  "heating_load_mj": 48.2,
  "cooling_load_mj": 31.7,
  "confidence": {
    "level": "high",
    "score": 0.88,
    "model_version": "nathers-attr-v1.3.2",
    "notes": null
  },
  "processing_time_ms": 1210,
  "request_id": "req-uuid-def"
}
```

**Insufficient confidence (200)**:
```json
{
  "dwelling_id": "dwelling-nathrs-uip-303",
  "status": "completed",
  "predicted_rating": null,
  "heating_load_mj": null,
  "cooling_load_mj": null,
  "confidence": {
    "level": "insufficient",
    "score": null,
    "model_version": "nathers-attr-v1.3.2",
    "notes": "Floor-plan feature data incomplete for reliable prediction"
  },
  "processing_time_ms": 120,
  "request_id": "req-uuid-ins"
}
```

---

## Error Contract

All error responses use the shared `ErrorResponse` envelope from Phase 1
(`src/scanq_shared/schemas/errors.py`). The `code` field uses values from `CrossRepoErrorCode`.

| Scenario | HTTP Status | `code` |
|---|---|---|
| Validation failure | 422 | `validation_error` |
| Unauthenticated | 401 | `authentication_failed` |
| Forbidden | 403 | `authorization_denied` |
| Resource not found | 404 | `not_found` |
| Upstream timeout | 504 | `timeout` |
| ML service unavailable | 503 | `connection_error` |
| Rate limit exceeded | 429 | `rate_limited` |
| Unexpected failure | 500 | `internal_error` |

---

## Client Usage Pattern

```python
from scanq_shared.clients import MLInferenceClient
from scanq_shared.models import FloorPlanTraceRequest, DwellingConfiguration

async with MLInferenceClient("http://ml-inference:9000") as client:
    trace = await client.trace_floor_plan(
        FloorPlanTraceRequest(
            dwelling_id="dwelling-101",
            image_url="https://storage.scanq.internal/fp/101.png",
        )
    )
    if trace.features:
        attrs = await client.extract_nathers_attributes(
            NatHERSAttributeRequest(
                dwelling_id="dwelling-101",
                floor_plan_features=trace.features,
                configuration=DwellingConfiguration(
                    climate_zone="6",
                    floor_area_m2=185.0,
                ),
            )
        )
```
