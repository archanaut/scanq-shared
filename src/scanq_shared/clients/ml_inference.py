"""Typed client for ML inference service."""

from ..models import (
    FloorPlanTraceRequest,
    FloorPlanTraceResponse,
    NatHERSAttributeRequest,
    NatHERSAttributeResponse,
)
from .base import BaseClient


class MLInferenceClient(BaseClient):
    async def trace_floor_plan(
        self, request: FloorPlanTraceRequest
    ) -> FloorPlanTraceResponse:
        return await self._typed_request(
            "POST",
            "/ml/floor-plan/trace",
            request,
            FloorPlanTraceResponse,
        )

    async def extract_nathers_attributes(
        self, request: NatHERSAttributeRequest
    ) -> NatHERSAttributeResponse:
        return await self._typed_request(
            "POST",
            "/ml/nathers/attributes",
            request,
            NatHERSAttributeResponse,
        )

