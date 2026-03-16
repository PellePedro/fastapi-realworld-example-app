import pytest
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repositories.authors import AuthorsRepository

pytestmark = pytest.mark.asyncio


async def test_empty_list_when_no_authors_exist(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.get(app.url_path_for("authors:list-authors"))
    assert response.status_code == 200
    assert response.json() == {"authors": [], "authorsCount": 0}


async def test_author_not_found(app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(
        app.url_path_for("authors:get-author", username="nonexistent")
    )
    assert response.status_code == 404


async def test_create_author(
    app: FastAPI, authorized_client: AsyncClient, test_user, pool: Pool
) -> None:
    response = await authorized_client.post(
        app.url_path_for("authors:create-author"),
        json={
            "author": {
                "specialty": "Python",
                "location": "NYC",
                "website": "https://example.com",
            }
        },
    )
    assert response.status_code == 201
    author = response.json()["author"]
    assert author["specialty"] == "Python"
    assert author["location"] == "NYC"
    assert author["website"] == "https://example.com"
    assert author["username"] == test_user.username


async def test_create_author_duplicate(
    app: FastAPI, authorized_client: AsyncClient, test_user, pool: Pool
) -> None:
    await authorized_client.post(
        app.url_path_for("authors:create-author"),
        json={"author": {"specialty": "Python"}},
    )
    response = await authorized_client.post(
        app.url_path_for("authors:create-author"),
        json={"author": {"specialty": "Go"}},
    )
    assert response.status_code == 400


async def test_get_author_by_username(
    app: FastAPI, authorized_client: AsyncClient, client: AsyncClient, test_user, pool: Pool
) -> None:
    await authorized_client.post(
        app.url_path_for("authors:create-author"),
        json={"author": {"specialty": "FastAPI"}},
    )
    response = await client.get(
        app.url_path_for("authors:get-author", username=test_user.username)
    )
    assert response.status_code == 200
    assert response.json()["author"]["specialty"] == "FastAPI"


async def test_list_authors_with_data(
    app: FastAPI, authorized_client: AsyncClient, client: AsyncClient, test_user, pool: Pool
) -> None:
    await authorized_client.post(
        app.url_path_for("authors:create-author"),
        json={"author": {"specialty": "Testing"}},
    )
    response = await client.get(app.url_path_for("authors:list-authors"))
    assert response.status_code == 200
    data = response.json()
    assert data["authorsCount"] == 1
    assert len(data["authors"]) == 1


async def test_update_author(
    app: FastAPI, authorized_client: AsyncClient, test_user, pool: Pool
) -> None:
    await authorized_client.post(
        app.url_path_for("authors:create-author"),
        json={"author": {"specialty": "Python"}},
    )
    response = await authorized_client.put(
        app.url_path_for("authors:update-author"),
        json={"author": {"specialty": "Rust", "location": "SF"}},
    )
    assert response.status_code == 200
    author = response.json()["author"]
    assert author["specialty"] == "Rust"
    assert author["location"] == "SF"


async def test_update_nonexistent_author(
    app: FastAPI, authorized_client: AsyncClient, test_user
) -> None:
    response = await authorized_client.put(
        app.url_path_for("authors:update-author"),
        json={"author": {"specialty": "Rust"}},
    )
    assert response.status_code == 404


async def test_delete_author(
    app: FastAPI, authorized_client: AsyncClient, client: AsyncClient, test_user, pool: Pool
) -> None:
    await authorized_client.post(
        app.url_path_for("authors:create-author"),
        json={"author": {"specialty": "Python"}},
    )
    response = await authorized_client.delete(
        app.url_path_for("authors:delete-author")
    )
    assert response.status_code == 204

    response = await client.get(
        app.url_path_for("authors:get-author", username=test_user.username)
    )
    assert response.status_code == 404


async def test_delete_nonexistent_author(
    app: FastAPI, authorized_client: AsyncClient, test_user
) -> None:
    response = await authorized_client.delete(
        app.url_path_for("authors:delete-author")
    )
    assert response.status_code == 404


async def test_create_author_unauthenticated(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.post(
        app.url_path_for("authors:create-author"),
        json={"author": {"specialty": "Python"}},
    )
    assert response.status_code == 403
