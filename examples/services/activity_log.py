from ..domains.marketplace import Activity
from ..schemas.marketplace import ActivityPageResponse, ActivityResponse


class ActivityLog:
    """Bounded, non-sensitive activity history used by the example service."""

    def __init__(self, source_revision: str, retention: int = 100) -> None:
        self._source_revision = source_revision
        self._retention = retention
        self._items: list[Activity] = []

    def page(self, limit: int) -> ActivityPageResponse:
        items = [
            ActivityResponse(
                timestamp=item.timestamp,
                operation=item.operation,
                target_id=item.target_id,
                previous_version=item.previous_version,
                new_version=item.new_version,
                result=item.result,
                conflict_count=item.conflict_count,
            )
            for item in reversed(self._items[-limit:])
        ]
        return ActivityPageResponse(items=items, limit=limit)

    def record(
        self,
        operation: str,
        target_id: str | None,
        *,
        previous_version: str | None = None,
        new_version: str | None = None,
    ) -> None:
        self._items.append(
            Activity.now(
                operation=operation,
                target_id=target_id,
                source_revision=self._source_revision,
                previous_version=previous_version,
                new_version=new_version,
            )
        )
        del self._items[: -self._retention]
