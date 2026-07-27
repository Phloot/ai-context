from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..domains.marketplace import Availability, ComponentType


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CatalogValidationResponse(StrictModel):
    valid: bool
    summary: str | None = None
    using_last_valid_catalog: bool = False


class CompatibilityResponse(StrictModel):
    compatible: bool
    reason: str | None = None


class ExternalDependencyResponse(StrictModel):
    type: str
    id: str
    name: str
    description: str
    required: bool
    availability: Availability


class ConflictResponse(StrictModel):
    code: str
    title: str
    explanation: str
    relative_path: str | None = None
    next_action: str


class ComponentResponse(StrictModel):
    id: str
    type: ComponentType
    name: str
    description: str
    available_version: str
    applied_version: str | None
    enabled: bool
    update_available: bool
    compatibility: CompatibilityResponse
    dependencies: list[str]
    dependents: list[str]
    external_dependencies: list[ExternalDependencyResponse]
    tags: list[str]
    release_summary: str
    conflicts: list[ConflictResponse]


class ProfileResponse(StrictModel):
    id: str
    name: str
    description: str
    version: str
    component_states: dict[str, bool]


class SyncSummaryResponse(StrictModel):
    catalog_updated: bool
    components_updated: list[str] = Field(default_factory=list)
    components_skipped: list[str] = Field(default_factory=list)
    conflict_count: int = 0
    new_components: list[str] = Field(default_factory=list)


class SummaryCounts(StrictModel):
    enabled: int
    updates: int
    conflicts: int


class MigrationResponse(StrictModel):
    required: bool
    matching: int = 0
    conflicting: int = 0
    unmanaged: int = 0


class MarketplaceResponse(StrictModel):
    catalog_version: str
    source_revision: str
    catalog_validation: CatalogValidationResponse
    available_component_types: list[ComponentType]
    profiles: list[ProfileResponse]
    components: list[ComponentResponse]
    summary: SummaryCounts
    last_synchronization: SyncSummaryResponse | None
    last_synchronized_at: datetime | None
    migration: MigrationResponse


class MutationResponse(StrictModel):
    operation: str
    result: str
    changed_component_ids: list[str]
    automatically_enabled_dependency_ids: list[str]
    applied_versions: dict[str, str]
    conflicts: list[ConflictResponse]
    summary: SummaryCounts


class ActivityResponse(StrictModel):
    timestamp: datetime
    operation: str
    target_id: str | None
    previous_version: str | None
    new_version: str | None
    result: str
    conflict_count: int


class ActivityPageResponse(StrictModel):
    items: list[ActivityResponse]
    limit: int
