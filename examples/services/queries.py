from datetime import datetime

from ..domains.marketplace import Component, ComponentType, Profile
from ..schemas.marketplace import (
    CatalogValidationResponse,
    CompatibilityResponse,
    ComponentResponse,
    ConflictResponse,
    ExternalDependencyResponse,
    MarketplaceResponse,
    MigrationResponse,
    ProfileResponse,
    SummaryCounts,
    SyncSummaryResponse,
)


def summary_counts(components: dict[str, Component]) -> SummaryCounts:
    values = list(components.values())
    return SummaryCounts(
        enabled=sum(item.enabled for item in values),
        updates=sum(
            item.enabled
            and item.applied_version is not None
            and item.applied_version != item.available_version
            for item in values
        ),
        conflicts=sum(bool(item.conflicts) for item in values),
    )


def build_marketplace_response(
    *,
    components: dict[str, Component],
    profiles: dict[str, Profile],
    catalog_version: str,
    source_revision: str,
    last_sync: SyncSummaryResponse | None,
    last_sync_at: datetime | None,
    migration_required: bool,
) -> MarketplaceResponse:
    dependents = {
        component_id: [
            item.id for item in components.values() if component_id in item.dependencies
        ]
        for component_id in components
    }
    response_components = [
        ComponentResponse(
            id=item.id,
            type=item.type,
            name=item.name,
            description=item.description,
            available_version=item.available_version,
            applied_version=item.applied_version,
            enabled=item.enabled,
            update_available=(
                item.enabled
                and item.applied_version is not None
                and item.applied_version != item.available_version
            ),
            compatibility=CompatibilityResponse(
                compatible=item.compatible, reason=item.compatibility_reason
            ),
            dependencies=list(item.dependencies),
            dependents=dependents[item.id],
            external_dependencies=[
                ExternalDependencyResponse(
                    type=dependency.type,
                    id=dependency.id,
                    name=dependency.name,
                    description=dependency.description,
                    required=dependency.required,
                    availability=dependency.availability,
                )
                for dependency in item.external_dependencies
            ],
            tags=list(item.tags),
            release_summary=item.release_summary,
            conflicts=[ConflictResponse(**conflict) for conflict in item.conflicts],
        )
        for item in sorted(components.values(), key=lambda value: value.name.lower())
    ]
    return MarketplaceResponse(
        catalog_version=catalog_version,
        source_revision=source_revision,
        catalog_validation=CatalogValidationResponse(valid=True),
        available_component_types=list(ComponentType),
        profiles=[
            ProfileResponse(
                id=profile.id,
                name=profile.name,
                description=profile.description,
                version=profile.version,
                component_states=profile.component_states,
            )
            for profile in profiles.values()
        ],
        components=response_components,
        summary=summary_counts(components),
        last_synchronization=last_sync,
        last_synchronized_at=last_sync_at,
        migration=MigrationResponse(required=migration_required),
    )
