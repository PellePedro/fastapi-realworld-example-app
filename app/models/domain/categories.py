from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class Category(IDModelMixin, DateTimeModelMixin, RWModel):
    name: str
    slug: str
    description: str = ""
