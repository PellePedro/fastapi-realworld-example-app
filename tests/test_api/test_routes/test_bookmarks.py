import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.models.domain.articles import Article
from app.models.domain.users import UserInDB

pytestmark = pytest.mark.asyncio


async def test_empty_bookmarks_list(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    response = await authorized_client.get(
        app.url_path_for("bookmarks:list-bookmarks")
    )
    assert response.status_code == 200
    assert response.json() == {"bookmarks": [], "bookmarksCount": 0}


async def test_create_bookmark(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    test_article: Article,
) -> None:
    response = await authorized_client.post(
        app.url_path_for("bookmarks:create-bookmark"),
        json={
            "bookmark": {
                "articleSlug": test_article.slug,
                "note": "Read later",
            }
        },
    )
    assert response.status_code == 201
    bookmark = response.json()["bookmark"]
    assert bookmark["articleSlug"] == test_article.slug
    assert bookmark["articleTitle"] == test_article.title
    assert bookmark["note"] == "Read later"


async def test_create_bookmark_for_nonexistent_article(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    response = await authorized_client.post(
        app.url_path_for("bookmarks:create-bookmark"),
        json={"bookmark": {"articleSlug": "nonexistent"}},
    )
    assert response.status_code == 404


async def test_create_duplicate_bookmark(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    test_article: Article,
) -> None:
    await authorized_client.post(
        app.url_path_for("bookmarks:create-bookmark"),
        json={"bookmark": {"articleSlug": test_article.slug}},
    )
    response = await authorized_client.post(
        app.url_path_for("bookmarks:create-bookmark"),
        json={"bookmark": {"articleSlug": test_article.slug}},
    )
    assert response.status_code == 400


async def test_list_bookmarks_with_data(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    test_article: Article,
) -> None:
    await authorized_client.post(
        app.url_path_for("bookmarks:create-bookmark"),
        json={"bookmark": {"articleSlug": test_article.slug}},
    )
    response = await authorized_client.get(
        app.url_path_for("bookmarks:list-bookmarks")
    )
    assert response.status_code == 200
    data = response.json()
    assert data["bookmarksCount"] == 1
    assert data["bookmarks"][0]["articleSlug"] == test_article.slug


async def test_delete_bookmark(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    test_article: Article,
) -> None:
    await authorized_client.post(
        app.url_path_for("bookmarks:create-bookmark"),
        json={"bookmark": {"articleSlug": test_article.slug}},
    )
    response = await authorized_client.delete(
        app.url_path_for("bookmarks:delete-bookmark", slug=test_article.slug)
    )
    assert response.status_code == 204

    response = await authorized_client.get(
        app.url_path_for("bookmarks:list-bookmarks")
    )
    assert response.json()["bookmarksCount"] == 0


async def test_delete_nonexistent_bookmark(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    response = await authorized_client.delete(
        app.url_path_for("bookmarks:delete-bookmark", slug="nonexistent")
    )
    assert response.status_code == 404


async def test_bookmarks_unauthenticated(app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(app.url_path_for("bookmarks:list-bookmarks"))
    assert response.status_code == 403
