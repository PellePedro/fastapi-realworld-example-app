import pytest
from fastapi import FastAPI
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health_check(app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(app.url_path_for("health_check"))
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
