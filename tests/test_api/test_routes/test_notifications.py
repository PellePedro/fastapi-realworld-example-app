import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.models.domain.users import UserInDB

pytestmark = pytest.mark.asyncio


async def test_empty_notifications_list(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    response = await authorized_client.get(
        app.url_path_for("notifications:list-notifications")
    )
    assert response.status_code == 200
    assert response.json() == {"notifications": [], "notificationsCount": 0}


async def test_create_notification(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    response = await authorized_client.post(
        app.url_path_for("notifications:create-notification"),
        json={
            "notification": {
                "type": "follow",
                "message": "User X followed you",
            }
        },
    )
    assert response.status_code == 201
    notification = response.json()["notification"]
    assert notification["type"] == "follow"
    assert notification["message"] == "User X followed you"
    assert notification["isRead"] is False


async def test_get_notification(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    create_resp = await authorized_client.post(
        app.url_path_for("notifications:create-notification"),
        json={"notification": {"type": "comment", "message": "New comment"}},
    )
    notification_id = create_resp.json()["notification"]["id"]

    response = await authorized_client.get(
        app.url_path_for(
            "notifications:get-notification",
            notification_id=notification_id,
        )
    )
    assert response.status_code == 200
    assert response.json()["notification"]["type"] == "comment"


async def test_get_nonexistent_notification(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    response = await authorized_client.get(
        app.url_path_for("notifications:get-notification", notification_id=99999)
    )
    assert response.status_code == 404


async def test_mark_notification_as_read(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    create_resp = await authorized_client.post(
        app.url_path_for("notifications:create-notification"),
        json={"notification": {"type": "favorite", "message": "Article favorited"}},
    )
    notification_id = create_resp.json()["notification"]["id"]

    response = await authorized_client.put(
        app.url_path_for(
            "notifications:mark-as-read",
            notification_id=notification_id,
        )
    )
    assert response.status_code == 200
    assert response.json()["notification"]["isRead"] is True


async def test_mark_nonexistent_notification_as_read(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    response = await authorized_client.put(
        app.url_path_for("notifications:mark-as-read", notification_id=99999)
    )
    assert response.status_code == 404


async def test_delete_notification(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    create_resp = await authorized_client.post(
        app.url_path_for("notifications:create-notification"),
        json={"notification": {"type": "follow", "message": "Followed"}},
    )
    notification_id = create_resp.json()["notification"]["id"]

    response = await authorized_client.delete(
        app.url_path_for(
            "notifications:delete-notification",
            notification_id=notification_id,
        )
    )
    assert response.status_code == 204

    response = await authorized_client.get(
        app.url_path_for("notifications:list-notifications")
    )
    assert response.json()["notificationsCount"] == 0


async def test_delete_nonexistent_notification(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    response = await authorized_client.delete(
        app.url_path_for(
            "notifications:delete-notification",
            notification_id=99999,
        )
    )
    assert response.status_code == 404


async def test_list_notifications_with_data(
    app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
) -> None:
    await authorized_client.post(
        app.url_path_for("notifications:create-notification"),
        json={"notification": {"type": "follow", "message": "Msg 1"}},
    )
    await authorized_client.post(
        app.url_path_for("notifications:create-notification"),
        json={"notification": {"type": "comment", "message": "Msg 2"}},
    )
    response = await authorized_client.get(
        app.url_path_for("notifications:list-notifications")
    )
    assert response.status_code == 200
    data = response.json()
    assert data["notificationsCount"] == 2


async def test_notifications_unauthenticated(
    app: FastAPI, client: AsyncClient
) -> None:
    response = await client.get(
        app.url_path_for("notifications:list-notifications")
    )
    assert response.status_code == 403
