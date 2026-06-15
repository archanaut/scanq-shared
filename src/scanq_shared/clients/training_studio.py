"""Typed HTTP client for training-studio support endpoints.

Provides typed, validated access to training-studio support APIs:
- Context resolution (project, environment, actor lookup)
- Service token issuance
- Lineage registration and finalization

Usage:
    async with TrainingStudioClient("http://training-studio:8000") as client:
        context = await client.resolve_context(
            project_id="proj-123",
            environment_id="env-staging"
        )
        print(context.project_id)
"""

import logging
from typing import Any

from pydantic import ValidationError

from ..schemas import (
    ContextResolveRequest,
    ContextResolveResponse,
    LineageFinalizeRequest,
    LineageFinalizeResponse,
    LineageRegisterRequest,
    LineageRegisterResponse,
    ServiceTokenRequest,
    ServiceTokenResponse,
)
from .base import BaseClient
from .exceptions import APIError, TimeoutError, ValidationError as ClientValidationError

logger = logging.getLogger(__name__)


class TrainingStudioClient(BaseClient):
    """Typed client for scanq-training-studio support endpoints.

    Manages requests to training-studio support APIs for:
    - Context resolution
    - Service authentication
    - Lineage tracking and finalization

    Example:
        async with TrainingStudioClient("http://localhost:8000") as client:
            # Resolve context
            ctx = await client.resolve_context(
                project_id="proj-123",
                environment_id="env-staging"
            )

            # Get auth token
            token = await client.get_service_token(
                service_id="scanq-accreditation",
                scopes=["read:context", "write:lineage"]
            )

            # Register lineage
            lineage = await client.register_lineage(
                run_id="run-dwelling-101-2026-06-15",
                dwelling_id="dwelling-101",
                pack_version="v1.0.0",
                initiated_by="ci-pipeline",
                environment="staging"
            )

            # Finalize lineage
            await client.finalize_lineage(
                lineage_id=lineage.lineage_id,
                status="finalized",
                metrics={"passed": 10, "failed": 0}
            )
    """

    async def resolve_context(
        self,
        project_id: str,
        environment_id: str,
        actor_id: str | None = None,
        include_metadata: bool = False,
    ) -> ContextResolveResponse:
        """Resolve project, environment, and actor context.

        Calls: POST /accreditation/context/resolve

        Args:
            project_id: Project identifier to resolve
            environment_id: Environment identifier to resolve
            actor_id: Actor identifier (optional)
            include_metadata: Include full metadata objects vs. IDs only

        Returns:
            ContextResolveResponse with resolved entities

        Raises:
            ValidationError: If request/response validation fails
            APIError: If the API returns an error
            TimeoutError: If request times out
        """
        request = ContextResolveRequest(
            project_id=project_id,
            environment_id=environment_id,
            actor_id=actor_id,
            include_metadata=include_metadata,
        )

        try:
            response = await self._request(
                "POST",
                "/accreditation/context/resolve",
                json=request.model_dump(),
            )

            response.raise_for_status()

            data = response.json()
            return ContextResolveResponse(**data)

        except ValidationError as e:
            raise ClientValidationError(
                f"Response validation failed: {e.error_count()} errors",
                details=e.errors(),
            ) from e
        except Exception as e:
            logger.error(f"resolve_context failed: {e}")
            raise

    async def get_service_token(
        self,
        service_id: str,
        scopes: list[str] | None = None,
        ttl_seconds: int = 3600,
        metadata: dict[str, str] | None = None,
    ) -> ServiceTokenResponse:
        """Issue a short-lived service-to-service authentication token.

        Calls: POST /accreditation/auth/service-token

        Args:
            service_id: ID of requesting service (e.g., "scanq-accreditation")
            scopes: List of requested scopes (default: ["read:context", "write:lineage"])
            ttl_seconds: Token time-to-live in seconds (default: 3600)
            metadata: Additional metadata for token request

        Returns:
            ServiceTokenResponse with bearer token and expiration

        Raises:
            ValidationError: If request/response validation fails
            APIError: If the API returns an error
            TimeoutError: If request times out
        """
        if scopes is None:
            scopes = ["read:context", "write:lineage"]

        request = ServiceTokenRequest(
            service_id=service_id,
            scopes=scopes,
            ttl_seconds=ttl_seconds,
            metadata=metadata,
        )

        try:
            response = await self._request(
                "POST",
                "/accreditation/auth/service-token",
                json=request.model_dump(),
            )

            response.raise_for_status()

            data = response.json()
            return ServiceTokenResponse(**data)

        except ValidationError as e:
            raise ClientValidationError(
                f"Response validation failed: {e.error_count()} errors",
                details=e.errors(),
            ) from e
        except Exception as e:
            logger.error(f"get_service_token failed: {e}")
            raise

    async def register_lineage(
        self,
        run_id: str,
        dwelling_id: str,
        pack_version: str,
        initiated_by: str,
        environment: str,
        metadata: dict[str, Any] | None = None,
    ) -> LineageRegisterResponse:
        """Register a new lineage record for an accreditation run.

        Calls: POST /accreditation/lineage/register

        Args:
            run_id: Unique identifier for this accreditation run
            dwelling_id: Dwelling ID being tested
            pack_version: Version of accreditation test pack
            initiated_by: User or service ID that initiated the run
            environment: Environment where run is occurring (e.g., staging, production)
            metadata: Additional context (Git commit, CI job ID, etc.)

        Returns:
            LineageRegisterResponse with assigned lineage_id

        Raises:
            ValidationError: If request/response validation fails
            APIError: If the API returns an error
            TimeoutError: If request times out
        """
        request = LineageRegisterRequest(
            run_id=run_id,
            dwelling_id=dwelling_id,
            pack_version=pack_version,
            initiated_by=initiated_by,
            environment=environment,
            metadata=metadata or {},
        )

        try:
            response = await self._request(
                "POST",
                "/accreditation/lineage/register",
                json=request.model_dump(),
            )

            response.raise_for_status()

            data = response.json()
            return LineageRegisterResponse(**data)

        except ValidationError as e:
            raise ClientValidationError(
                f"Response validation failed: {e.error_count()} errors",
                details=e.errors(),
            ) from e
        except Exception as e:
            logger.error(f"register_lineage failed: {e}")
            raise

    async def finalize_lineage(
        self,
        lineage_id: str,
        status: str,
        summary: str | None = None,
        metrics: dict[str, Any] | None = None,
    ) -> LineageFinalizeResponse:
        """Finalize a lineage record after accreditation completes.

        Calls: POST /accreditation/lineage/{lineage_id}/finalize

        Args:
            lineage_id: The lineage_id from registration response
            status: Final status of the run (registered, updated, finalized, failed, cancelled)
            summary: Human-readable summary of results
            metrics: Metrics/results (pass/fail counts, evidence generated, etc.)

        Returns:
            LineageFinalizeResponse confirming finalization

        Raises:
            ValidationError: If request/response validation fails
            APIError: If the API returns an error
            TimeoutError: If request times out
        """
        request = LineageFinalizeRequest(
            lineage_id=lineage_id,
            status=status,
            summary=summary,
            metrics=metrics or {},
        )

        try:
            response = await self._request(
                "POST",
                f"/accreditation/lineage/{lineage_id}/finalize",
                json=request.model_dump(),
            )

            response.raise_for_status()

            data = response.json()
            return LineageFinalizeResponse(**data)

        except ValidationError as e:
            raise ClientValidationError(
                f"Response validation failed: {e.error_count()} errors",
                details=e.errors(),
            ) from e
        except Exception as e:
            logger.error(f"finalize_lineage failed: {e}")
            raise
