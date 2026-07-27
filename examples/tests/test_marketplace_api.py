import pytest
from httpx import ASGITransport, AsyncClient

from examples.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client


@pytest.mark.anyio
async def test_marketplace_exposes_all_component_types(client: AsyncClient) -> None:
    response = await client.get("/api/context-marketplace")

    assert response.status_code == 200
    body = response.json()
    assert set(body["available_component_types"]) == {
        "skill",
        "agent",
        "instruction",
        "prompt",
        "hook",
    }
    assert body["summary"] == {"enabled": 1, "updates": 1, "conflicts": 0}
    assert body["auto_update_enabled"] is False


@pytest.mark.anyio
async def test_auto_update_is_opt_in_and_server_authoritative(
    client: AsyncClient,
) -> None:
    response = await client.put(
        "/api/context-marketplace/settings/auto-update", json={"enabled": True}
    )

    assert response.status_code == 200
    assert response.json() == {"enabled": True}
    marketplace = (await client.get("/api/context-marketplace")).json()
    assert marketplace["auto_update_enabled"] is True


@pytest.mark.anyio
async def test_enable_waits_for_server_and_returns_refreshed_counts(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/api/context-marketplace/components/python-style/enable"
    )

    assert response.status_code == 200
    assert response.json()["changed_component_ids"] == ["python-style"]
    marketplace = (await client.get("/api/context-marketplace")).json()
    python_style = next(
        item for item in marketplace["components"] if item["id"] == "python-style"
    )
    assert python_style["enabled"] is True
    assert marketplace["summary"]["enabled"] == 2


@pytest.mark.anyio
async def test_unknown_component_uses_stable_safe_error(client: AsyncClient) -> None:
    response = await client.post("/api/context-marketplace/components/not-real/enable")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "COMPONENT_NOT_FOUND",
            "message": "The requested component does not exist.",
            "details": {},
        }
    }


@pytest.mark.anyio
async def test_disable_is_blocked_by_an_enabled_dependent(client: AsyncClient) -> None:
    await client.post("/api/context-marketplace/components/quality-hook/enable")

    response = await client.post(
        "/api/context-marketplace/components/maintainable-code/disable"
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "DEPENDENCY_IN_USE"
    assert response.json()["error"]["details"] == {"dependent_ids": ["quality-hook"]}
