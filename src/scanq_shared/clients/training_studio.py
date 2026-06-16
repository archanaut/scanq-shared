"""Typed HTTP client for training-studio support endpoints."""

from typing import Any

from ..enums import LineageEventType, MediaType
from ..schemas import (
    ContextResolveRequest,
    ContextResolveResponse,
    MediaComposeRequest,
    MediaComposeResponse,
    LineageFinalizeRequest,
    LineageFinalizeResponse,
    LineageRegisterRequest,
    LineageRegisterResponse,
    ServiceTokenRequest,
    ServiceTokenResponse,
)
from .base import BaseClient


class TrainingStudioClient(BaseClient):
    """Typed client for training-studio APIs."""

    async def resolve_context(
        self,
        project_id: str,
        environment_id: str,
        actor_id: str | None = None,
        include_metadata: bool = False,
    ) -> ContextResolveResponse:
        request = ContextResolveRequest(
            project_id=project_id,
            environment_id=environment_id,
            actor_id=actor_id,
            include_metadata=include_metadata,
        )
        return await self._typed_request(
            "POST",
            "/accreditation/context/resolve",
            request,
            ContextResolveResponse,
        )

    async def get_service_token(
        self,
        service_id: str,
        scopes: list[str] | None = None,
        ttl_seconds: int = 3600,
        metadata: dict[str, str] | None = None,
    ) -> ServiceTokenResponse:
        request = ServiceTokenRequest(
            service_id=service_id,
            scopes=scopes or ["read:context", "write:lineage"],
            ttl_seconds=ttl_seconds,
            metadata=metadata,
        )
        return await self._typed_request(
            "POST",
            "/accreditation/auth/service-token",
            request,
            ServiceTokenResponse,
        )

    async def register_lineage(
        self,
        run_id: str,
        dwelling_id: str,
        pack_version: str,
        initiated_by: str,
        environment: str,
        metadata: dict[str, Any] | None = None,
    ) -> LineageRegisterResponse:
        request = LineageRegisterRequest(
            run_id=run_id,
            dwelling_id=dwelling_id,
            pack_version=pack_version,
            initiated_by=initiated_by,
            environment=environment,
            metadata=metadata or {},
        )
        return await self._typed_request(
            "POST",
            "/accreditation/lineage/register",
            request,
            LineageRegisterResponse,
        )

    async def finalize_lineage(
        self,
        lineage_id: str,
        status: str | LineageEventType,
        summary: str | None = None,
        metrics: dict[str, Any] | None = None,
    ) -> LineageFinalizeResponse:
        request = LineageFinalizeRequest(
            lineage_id=lineage_id,
            status=LineageEventType(status),
            summary=summary,
            metrics=metrics or {},
        )
        return await self._typed_request(
            "POST",
            f"/accreditation/lineage/{lineage_id}/finalize",
            request,
            LineageFinalizeResponse,
        )

    async def compose_media(
        self,
        source_media_refs: list[str],
        compose_type: str | MediaType,
        output_format: str = "pdf",
        parameters: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MediaComposeResponse:
        request = MediaComposeRequest(
            source_media_refs=source_media_refs,
            compose_type=MediaType(compose_type),
            output_format=output_format,
            parameters=parameters or {},
            metadata=metadata or {},
        )
        return await self._typed_request(
            "POST",
            "/accreditation/media/compose",
            request,
            MediaComposeResponse,
        )
