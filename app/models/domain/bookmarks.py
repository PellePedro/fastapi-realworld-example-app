import datetime

from app.models.domain.rwmodel import RWModel


class Bookmark(RWModel):
    user_id: int
    article_id: int
    article_slug: str
    article_title: str
    note: str = ""
    created_at: datetime.datetime = None  # type: ignore
