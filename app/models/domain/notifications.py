from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class Notification(IDModelMixin, DateTimeModelMixin, RWModel):
    user_id: int
    type: str
    message: str
    is_read: bool = False
