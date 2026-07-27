from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import FileResponse

from ..schemas.marketplace import (
    ActivityPageResponse,
    MarketplaceResponse,
    MigrationResponse,
    MutationResponse,
)
from ..services.marketplace import MarketplaceService

router = APIRouter()
TEMPLATE = (
    Path(__file__).resolve().parents[1] / "templates" / "context_marketplace.html"
)


def get_marketplace_service(request: Request) -> MarketplaceService:
    return request.app.state.marketplace_service


Service = Annotated[MarketplaceService, Depends(get_marketplace_service)]


@router.get("/marketplace", include_in_schema=False)
async def marketplace_page() -> FileResponse:
    return FileResponse(TEMPLATE)


@router.get("/api/context-marketplace", response_model=MarketplaceResponse)
async def get_marketplace(service: Service) -> MarketplaceResponse:
    return await service.get_marketplace()


@router.get("/api/context-marketplace/activity", response_model=ActivityPageResponse)
async def get_activity(
    service: Service, limit: Annotated[int, Query(ge=1, le=100)] = 50
) -> ActivityPageResponse:
    return await service.get_activity(limit)


@router.post("/api/context-marketplace/sync", response_model=MutationResponse)
async def sync_marketplace(service: Service) -> MutationResponse:
    return await service.sync()


@router.post(
    "/api/context-marketplace/components/{component_id}/enable",
    response_model=MutationResponse,
)
async def enable_component(component_id: str, service: Service) -> MutationResponse:
    return await service.enable(component_id)


@router.post(
    "/api/context-marketplace/components/{component_id}/disable",
    response_model=MutationResponse,
)
async def disable_component(component_id: str, service: Service) -> MutationResponse:
    return await service.disable(component_id)


@router.post(
    "/api/context-marketplace/components/{component_id}/update",
    response_model=MutationResponse,
)
async def update_component(component_id: str, service: Service) -> MutationResponse:
    return await service.update(component_id)


@router.post(
    "/api/context-marketplace/profiles/{profile_id}/apply",
    response_model=MutationResponse,
)
async def apply_profile(profile_id: str, service: Service) -> MutationResponse:
    return await service.apply_profile(profile_id)


@router.post("/api/context-marketplace/migrate", response_model=MigrationResponse)
async def migrate_marketplace(service: Service) -> MigrationResponse:
    return await service.migrate()
