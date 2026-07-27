from ..domains.marketplace import Component, MarketplaceError


def dependency_order(
    component: Component, components: dict[str, Component]
) -> list[str]:
    """Return dependencies before dependents and reject missing IDs or cycles."""
    ordered: list[str] = []
    visiting: set[str] = set()

    def visit(component_id: str) -> None:
        if component_id in visiting:
            raise MarketplaceError("DEPENDENCY_CYCLE", "A dependency cycle was found.")
        if component_id in ordered:
            return
        current = components.get(component_id)
        if current is None:
            raise MarketplaceError(
                "DEPENDENCY_MISSING",
                "A required catalog component does not exist.",
                details={"component_id": component_id},
            )
        visiting.add(component_id)
        for dependency_id in current.dependencies:
            visit(dependency_id)
        visiting.remove(component_id)
        ordered.append(component_id)

    for dependency_id in component.dependencies:
        visit(dependency_id)
    return ordered
