import pytest
from fastapi import FastAPI
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_empty_list_when_no_categories_exist(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.get(app.url_path_for("categories:list-categories"))
    assert response.status_code == 200
    assert response.json() == {"categories": [], "categoriesCount": 0}


async def test_category_not_found(app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(
        app.url_path_for("categories:get-category", slug="nonexistent")
    )
    assert response.status_code == 404


async def test_create_category(
    app: FastAPI, authorized_client: AsyncClient, test_user
) -> None:
    response = await authorized_client.post(
        app.url_path_for("categories:create-category"),
        json={
            "category": {
                "name": "Technology",
                "description": "Tech articles",
            }
        },
    )
    assert response.status_code == 201
    category = response.json()["category"]
    assert category["name"] == "Technology"
    assert category["slug"] == "technology"
    assert category["description"] == "Tech articles"


async def test_get_category_by_slug(
    app: FastAPI, authorized_client: AsyncClient, client: AsyncClient, test_user
) -> None:
    await authorized_client.post(
        app.url_path_for("categories:create-category"),
        json={"category": {"name": "Science"}},
    )
    response = await client.get(
        app.url_path_for("categories:get-category", slug="science")
    )
    assert response.status_code == 200
    assert response.json()["category"]["name"] == "Science"


async def test_list_categories_with_data(
    app: FastAPI, authorized_client: AsyncClient, client: AsyncClient, test_user
) -> None:
    await authorized_client.post(
        app.url_path_for("categories:create-category"),
        json={"category": {"name": "Art"}},
    )
    await authorized_client.post(
        app.url_path_for("categories:create-category"),
        json={"category": {"name": "Music"}},
    )
    response = await client.get(app.url_path_for("categories:list-categories"))
    assert response.status_code == 200
    data = response.json()
    assert data["categoriesCount"] == 2


async def test_update_category(
    app: FastAPI, authorized_client: AsyncClient, test_user
) -> None:
    await authorized_client.post(
        app.url_path_for("categories:create-category"),
        json={"category": {"name": "Tech"}},
    )
    response = await authorized_client.put(
        app.url_path_for("categories:update-category", slug="tech"),
        json={"category": {"name": "Technology", "description": "Updated"}},
    )
    assert response.status_code == 200
    category = response.json()["category"]
    assert category["name"] == "Technology"
    assert category["slug"] == "technology"
    assert category["description"] == "Updated"


async def test_update_nonexistent_category(
    app: FastAPI, authorized_client: AsyncClient, test_user
) -> None:
    response = await authorized_client.put(
        app.url_path_for("categories:update-category", slug="nonexistent"),
        json={"category": {"name": "New Name"}},
    )
    assert response.status_code == 404


async def test_delete_category(
    app: FastAPI, authorized_client: AsyncClient, client: AsyncClient, test_user
) -> None:
    await authorized_client.post(
        app.url_path_for("categories:create-category"),
        json={"category": {"name": "ToDelete"}},
    )
    response = await authorized_client.delete(
        app.url_path_for("categories:delete-category", slug="todelete")
    )
    assert response.status_code == 204

    response = await client.get(
        app.url_path_for("categories:get-category", slug="todelete")
    )
    assert response.status_code == 404


async def test_delete_nonexistent_category(
    app: FastAPI, authorized_client: AsyncClient, test_user
) -> None:
    response = await authorized_client.delete(
        app.url_path_for("categories:delete-category", slug="nonexistent")
    )
    assert response.status_code == 404


async def test_create_category_unauthenticated(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.post(
        app.url_path_for("categories:create-category"),
        json={"category": {"name": "Test"}},
    )
    assert response.status_code == 403
