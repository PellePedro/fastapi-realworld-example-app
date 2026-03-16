from typing import List

from app.models.domain.notifications import Notification
from app.models.schemas.rwschema import RWSchema


class NotificationForResponse(RWSchema, Notification):
    pass


class NotificationInResponse(RWSchema):
    notification: NotificationForResponse


class NotificationInCreate(RWSchema):
    type: str
    message: str


class ListOfNotificationsInResponse(RWSchema):
    notifications: List[NotificationForResponse]
    notifications_count: int
