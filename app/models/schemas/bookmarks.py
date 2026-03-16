from typing import List, Optional

from app.models.domain.bookmarks import Bookmark
from app.models.schemas.rwschema import RWSchema


class BookmarkForResponse(RWSchema, Bookmark):
    pass


class BookmarkInResponse(RWSchema):
    bookmark: BookmarkForResponse


class BookmarkInCreate(RWSchema):
    article_slug: str
    note: str = ""


class ListOfBookmarksInResponse(RWSchema):
    bookmarks: List[BookmarkForResponse]
    bookmarks_count: int
