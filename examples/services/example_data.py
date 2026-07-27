from ..domains.marketplace import (
    Availability,
    Component,
    ComponentType,
    ExternalDependency,
    Profile,
)


def create_example_components() -> list[Component]:
    """Representative data only; production reads validated catalog manifests."""
    mcp = ExternalDependency(
        type="mcp",
        id="intellij",
        name="IntelliJ MCP",
        description="Provides IDE-aware search operations.",
        required=True,
        availability=Availability.UNKNOWN,
    )
    return [
        Component(
            id="maintainable-code",
            type=ComponentType.SKILL,
            name="Maintainable Code",
            description="Keeps implementation slices small, explicit, and verifiable.",
            available_version="1.2.0",
            applied_version="1.1.0",
            enabled=True,
            release_summary="Adds file-growth checks and clearer adapter boundaries.",
            tags=("quality", "python"),
        ),
        Component(
            id="api-review",
            type=ComponentType.AGENT,
            name="API Review",
            description="Reviews HTTP contracts for compatibility and consumer impact.",
            available_version="1.0.0",
            release_summary="Initial API review agent.",
            tags=("api", "review"),
            dependencies=("maintainable-code",),
            external_dependencies=(mcp,),
        ),
        Component(
            id="python-style",
            type=ComponentType.INSTRUCTION,
            name="Python Style",
            description="Applies the team's Python conventions.",
            available_version="1.0.0",
            release_summary="Initial Python instruction set.",
            tags=("python", "style"),
        ),
        Component(
            id="review-prompt",
            type=ComponentType.PROMPT,
            name="Review Prompt",
            description="Starts a focused change review.",
            available_version="1.0.0",
            release_summary="Initial review prompt.",
        ),
        Component(
            id="quality-hook",
            type=ComponentType.HOOK,
            name="Quality Hook",
            description="Runs maintainability guidance before delegated work.",
            available_version="1.0.0",
            release_summary="Initial quality hook.",
            dependencies=("maintainable-code",),
        ),
    ]


def create_example_profiles() -> list[Profile]:
    return [
        Profile(
            id="python-team",
            name="Python Team",
            description="Recommended Python development context.",
            version="1.0.0",
            component_states={"maintainable-code": True, "python-style": True},
        )
    ]
