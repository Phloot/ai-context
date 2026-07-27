from collections.abc import Callable

from ..domains.marketplace import Availability, Component, MarketplaceError
from ..schemas.marketplace import MutationResponse
from .dependencies import dependency_order
from .queries import summary_counts


class ComponentMutations:
    """Own enable, disable, and update policy for every component type."""

    def __init__(
        self,
        components: dict[str, Component],
        record: Callable[..., None],
    ) -> None:
        self._components = components
        self._record = record

    def enable(self, component_id: str) -> MutationResponse:
        component = self._component(component_id)
        if not component.compatible:
            raise MarketplaceError(
                "COMPONENT_INCOMPATIBLE",
                "This component is not compatible with the current environment.",
            )
        unavailable = [
            item
            for item in component.external_dependencies
            if item.required and item.availability == Availability.UNAVAILABLE
        ]
        if unavailable:
            raise MarketplaceError(
                "EXTERNAL_DEPENDENCY_UNAVAILABLE",
                "A required external dependency is unavailable.",
                details={"dependency_ids": [item.id for item in unavailable]},
            )
        changed: list[str] = []
        automatic: list[str] = []
        dependencies = dependency_order(component, self._components)
        for dependency_id in [*dependencies, component.id]:
            candidate = self._component(dependency_id)
            if not candidate.enabled:
                candidate.enabled = True
                candidate.applied_version = candidate.available_version
                changed.append(candidate.id)
                if candidate.id != component.id:
                    automatic.append(candidate.id)
        self._record("enable", component.id)
        return self._response("enable", changed, automatic)

    def disable(self, component_id: str) -> MutationResponse:
        component = self._component(component_id)
        dependents = [
            item.id
            for item in self._components.values()
            if item.enabled and component.id in item.dependencies
        ]
        if dependents:
            raise MarketplaceError(
                "DEPENDENCY_IN_USE",
                "Disable enabled dependents first.",
                details={"dependent_ids": dependents},
            )
        changed = []
        if component.enabled:
            component.enabled = False
            component.applied_version = None
            changed.append(component.id)
        self._record("disable", component.id)
        return self._response("disable", changed)

    def update(self, component_id: str) -> MutationResponse:
        component = self._component(component_id)
        if (
            not component.enabled
            or component.applied_version == component.available_version
        ):
            return self._response("update", [])
        previous = component.applied_version
        component.applied_version = component.available_version
        self._record(
            "update",
            component.id,
            previous_version=previous,
            new_version=component.available_version,
        )
        return self._response("update", [component.id])

    def _component(self, component_id: str) -> Component:
        component = self._components.get(component_id)
        if component is None:
            raise MarketplaceError(
                "COMPONENT_NOT_FOUND",
                "The requested component does not exist.",
                status_code=404,
            )
        return component

    def _response(
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
            summary=summary_counts(self._components),
        )
