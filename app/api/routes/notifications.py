from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.notifications import NotificationsRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.notifications import (
    ListOfNotificationsInResponse,
    NotificationForResponse,
    NotificationInCreate,
    NotificationInResponse,
)
from app.resources import strings

router = APIRouter()


@router.get(
    "",
    response_model=ListOfNotificationsInResponse,
    name="notifications:list-notifications",
)
async def list_notifications(
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    notifications_repo: NotificationsRepository = Depends(
        get_repository(NotificationsRepository),
    ),
) -> ListOfNotificationsInResponse:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )
    notifications = await notifications_repo.get_notifications_for_user(
        user_id=user_in_db.id_,
    )
    return ListOfNotificationsInResponse(
        notifications=[
            NotificationForResponse.from_orm(n) for n in notifications
        ],
        notifications_count=len(notifications),
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationInResponse,
    name="notifications:get-notification",
)
async def get_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    notifications_repo: NotificationsRepository = Depends(
        get_repository(NotificationsRepository),
    ),
) -> NotificationInResponse:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    try:
        notification = await notifications_repo.get_notification_by_id(
            notification_id=notification_id,
            user_id=user_in_db.id_,
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=strings.NOTIFICATION_DOES_NOT_EXIST_ERROR,
        )

    return NotificationInResponse(
        notification=NotificationForResponse.from_orm(notification),
    )


@router.post(
    "",
    response_model=NotificationInResponse,
    status_code=HTTP_201_CREATED,
    name="notifications:create-notification",
)
async def create_notification(
    notification_create: NotificationInCreate = Body(
        ...,
        embed=True,
        alias="notification",
    ),
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    notifications_repo: NotificationsRepository = Depends(
        get_repository(NotificationsRepository),
    ),
) -> NotificationInResponse:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    notification = await notifications_repo.create_notification(
        user_id=user_in_db.id_,
        type=notification_create.type,
        message=notification_create.message,
    )
    return NotificationInResponse(
        notification=NotificationForResponse.from_orm(notification),
    )


@router.put(
    "/{notification_id}/read",
    response_model=NotificationInResponse,
    name="notifications:mark-as-read",
)
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    notifications_repo: NotificationsRepository = Depends(
        get_repository(NotificationsRepository),
    ),
) -> NotificationInResponse:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    try:
        notification = await notifications_repo.mark_as_read(
            notification_id=notification_id,
            user_id=user_in_db.id_,
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=strings.NOTIFICATION_DOES_NOT_EXIST_ERROR,
        )

    return NotificationInResponse(
        notification=NotificationForResponse.from_orm(notification),
    )


@router.delete(
    "/{notification_id}",
    status_code=HTTP_204_NO_CONTENT,
    name="notifications:delete-notification",
)
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    notifications_repo: NotificationsRepository = Depends(
        get_repository(NotificationsRepository),
    ),
) -> None:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    try:
        await notifications_repo.get_notification_by_id(
            notification_id=notification_id,
            user_id=user_in_db.id_,
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=strings.NOTIFICATION_DOES_NOT_EXIST_ERROR,
        )

    await notifications_repo.delete_notification(
        notification_id=notification_id,
        user_id=user_in_db.id_,
    )
