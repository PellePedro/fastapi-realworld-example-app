from typing import Optional

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class Author(IDModelMixin, DateTimeModelMixin, RWModel):
    user_id: int
    username: str
    specialty: str = ""
    location: str = ""
    website: str = ""
