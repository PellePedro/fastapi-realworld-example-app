from typing import List

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.notifications import Notification


class NotificationsRepository(BaseRepository):
    async def get_notifications_for_user(
        self,
        *,
        user_id: int,
    ) -> List[Notification]:
        rows = await queries.get_notifications_by_user_id(
            self.connection,
            user_id=user_id,
        )
        return [Notification(**row) for row in rows]

    async def get_notification_by_id(
        self,
        *,
        notification_id: int,
        user_id: int,
    ) -> Notification:
        row = await queries.get_notification_by_id(
            self.connection,
            id=notification_id,
            user_id=user_id,
        )
        if row:
            return Notification(**row)

        raise EntityDoesNotExist("notification does not exist")

    async def create_notification(
        self,
        *,
        user_id: int,
        type: str,
        message: str,
    ) -> Notification:
        async with self.connection.transaction():
            row = await queries.create_new_notification(
                self.connection,
                user_id=user_id,
                type=type,
                message=message,
            )

        return Notification(
            id=row["id"],
            user_id=user_id,
            type=type,
            message=message,
            is_read=row["is_read"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def mark_as_read(
        self,
        *,
        notification_id: int,
        user_id: int,
    ) -> Notification:
        notification = await self.get_notification_by_id(
            notification_id=notification_id,
            user_id=user_id,
        )

        async with self.connection.transaction():
            notification.updated_at = await queries.mark_notification_as_read(
                self.connection,
                id=notification_id,
                user_id=user_id,
            )

        notification.is_read = True
        return notification

    async def delete_notification(
        self,
        *,
        notification_id: int,
        user_id: int,
    ) -> None:
        await queries.delete_notification_by_id(
            self.connection,
            id=notification_id,
            user_id=user_id,
        )
