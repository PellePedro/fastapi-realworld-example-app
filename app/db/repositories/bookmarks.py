from typing import List

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.bookmarks import Bookmark


class BookmarksRepository(BaseRepository):
    async def get_bookmarks_for_user(self, *, user_id: int) -> List[Bookmark]:
        rows = await queries.get_bookmarks_by_user_id(
            self.connection,
            user_id=user_id,
        )
        return [Bookmark(**row) for row in rows]

    async def get_bookmark(self, *, user_id: int, slug: str) -> Bookmark:
        row = await queries.get_bookmark(
            self.connection,
            user_id=user_id,
            slug=slug,
        )
        if row:
            return Bookmark(**row)

        raise EntityDoesNotExist("bookmark does not exist")

    async def create_bookmark(
        self,
        *,
        user_id: int,
        article_id: int,
        article_slug: str,
        article_title: str,
        note: str = "",
    ) -> Bookmark:
        async with self.connection.transaction():
            row = await queries.create_new_bookmark(
                self.connection,
                user_id=user_id,
                article_id=article_id,
                note=note,
            )

        return Bookmark(
            user_id=user_id,
            article_id=article_id,
            article_slug=article_slug,
            article_title=article_title,
            note=note,
            created_at=row["created_at"],
        )

    async def delete_bookmark(self, *, user_id: int, article_id: int) -> None:
        await queries.delete_bookmark(
            self.connection,
            user_id=user_id,
            article_id=article_id,
        )
