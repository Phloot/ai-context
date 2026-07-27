import asyncio
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from typing import TypeVar

from ..domains.marketplace import Component, MarketplaceError, Profile
from ..schemas.marketplace import (
    ActivityPageResponse,
    MarketplaceResponse,
    MigrationResponse,
    MutationResponse,
    SummaryCounts,
    SyncSummaryResponse,
)
from .activity_log import ActivityLog
from .component_mutations import ComponentMutations
from .dependencies import dependency_order
from .example_data import create_example_components, create_example_profiles
from .queries import build_marketplace_response, summary_counts

T = TypeVar("T")


class MarketplaceService:
    """Example orchestration service.

    Replace the in-memory state with the real catalog loader, state repository,
    projection engine, and activity repository. The router and response schemas
    should not need to change when those production adapters are introduced.
    """

    def __init__(self, components: list[Component], profiles: list[Profile]) -> None:
        self._components = {component.id: component for component in components}
        self._profiles = {profile.id: profile for profile in profiles}
        self._mutation_lock = asyncio.Lock()
        self._catalog_version = "2026.07.1"
        self._source_revision = "example-revision"
        self._activity = ActivityLog(self._source_revision)
        self._last_sync: SyncSummaryResponse | None = None
        self._last_sync_at: datetime | None = None
        self._migration_required = True
        self._component_mutations = ComponentMutations(
            self._components, self._activity.record
        )

    @classmethod
    def example(cls) -> "MarketplaceService":
        return cls(create_example_components(), create_example_profiles())

    async def get_marketplace(self) -> MarketplaceResponse:
        return self._marketplace_response()

    async def get_activity(self, limit: int = 50) -> ActivityPageResponse:
        return self._activity.page(limit)

    async def enable(self, component_id: str) -> MutationResponse:
        async def operation() -> MutationResponse:
            return self._component_mutations.enable(component_id)

        return await self._run_mutation(operation)

    async def disable(self, component_id: str) -> MutationResponse:
        async def operation() -> MutationResponse:
            return self._component_mutations.disable(component_id)

        return await self._run_mutation(operation)

    async def update(self, component_id: str) -> MutationResponse:
        async def operation() -> MutationResponse:
            return self._component_mutations.update(component_id)

        return await self._run_mutation(operation)

    async def sync(self) -> MutationResponse:
        async def operation() -> MutationResponse:
            # Production: update checkout, validate, preserve the last valid
            # catalog on failure, then safely update enabled components.
            self._last_sync = SyncSummaryResponse(catalog_updated=True)
            self._last_sync_at = datetime.now(timezone.utc)
            self._activity.record("sync", None)
            return self._mutation("sync", [])

        return await self._run_mutation(operation)

    async def apply_profile(self, profile_id: str) -> MutationResponse:
        async def operation() -> MutationResponse:
            profile = self._profiles.get(profile_id)
            if profile is None:
                raise MarketplaceError(
                    "PROFILE_NOT_FOUND",
                    "The requested profile does not exist.",
                    status_code=404,
                )
            changed: list[str] = []
            automatic: list[str] = []
            for component_id, should_enable in profile.component_states.items():
                component = self._component(component_id)
                if should_enable:
                    for dependency_id in dependency_order(component, self._components):
                        dependency = self._component(dependency_id)
                        if not dependency.enabled:
                            dependency.enabled = True
                            dependency.applied_version = dependency.available_version
                            changed.append(dependency.id)
                            automatic.append(dependency.id)
                    if not component.enabled:
                        component.enabled = True
                        component.applied_version = component.available_version
                        changed.append(component.id)
                elif component.enabled:
                    component.enabled = False
                    component.applied_version = None
                    changed.append(component.id)
            self._activity.record("apply_profile", profile.id)
            return self._mutation("apply_profile", changed, automatic)

        return await self._run_mutation(operation)

    async def migrate(self) -> MigrationResponse:
        async def operation() -> MigrationResponse:
            # Production compares content hashes and never claims matching paths alone.
            self._migration_required = False
            self._activity.record("migrate", None)
            return MigrationResponse(
                required=False, matching=2, conflicting=0, unmanaged=1
            )

        return await self._run_mutation(operation)

    async def _run_mutation(self, operation: Callable[[], Awaitable[T]]) -> T:
        if self._mutation_lock.locked():
            raise MarketplaceError(
                "MARKETPLACE_BUSY",
                "Another marketplace operation is already running.",
                status_code=409,
            )
        async with self._mutation_lock:
            return await operation()

    def _component(self, component_id: str) -> Component:
        component = self._components.get(component_id)
        if component is None:
            raise MarketplaceError(
                "COMPONENT_NOT_FOUND",
                "The requested component does not exist.",
                status_code=404,
            )
        return component

    def _marketplace_response(self) -> MarketplaceResponse:
        return build_marketplace_response(
            components=self._components,
            profiles=self._profiles,
            catalog_version=self._catalog_version,
            source_revision=self._source_revision,
            last_sync=self._last_sync,
            last_sync_at=self._last_sync_at,
            migration_required=self._migration_required,
        )

    def _counts(self) -> SummaryCounts:
        return summary_counts(self._components)

    def _mutation(
        self,
        operation: str,
        changed: list[str],
        automatic: list[str] | None = None,
    ) -> MutationResponse:
        return MutationResponse(
            operation=operation,
            result="succeeded",
            changed_component_ids=changed,
            automatically_enabled_dependency_ids=automatic or [],
            applied_versions={
                component_id: component.applied_version
                for component_id, component in self._components.items()
                if component.applied_version is not None
            },
            conflicts=[],
            summary=self._counts(),
        )
