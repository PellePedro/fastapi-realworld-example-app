from typing import List, Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.authors import Author


class AuthorsRepository(BaseRepository):
    async def get_all_authors(self) -> List[Author]:
        author_rows = await queries.get_all_authors(  # type: ignore
            self.connection,
        )
        return [Author(**row) for row in author_rows]

    async def get_author_by_username(self, *, username: str) -> Author:
        author_row = await queries.get_author_by_username(  # type: ignore
            self.connection,
            username=username,
        )
        if author_row:
            return Author(**author_row)

        raise EntityDoesNotExist(
            "author with username {0} does not exist".format(username),
        )

    async def create_author(
        self,
        *,
        user_id: int,
        specialty: str = "",
        location: str = "",
        website: str = "",
    ) -> Author:
        async with self.connection.transaction():
            author_row = await queries.create_new_author(  # type: ignore
                self.connection,
                user_id=user_id,
                specialty=specialty,
                location=location,
                website=website,
            )

        return Author(
            id_=author_row["id"],
            user_id=user_id,
            username="",
            specialty=specialty,
            location=location,
            website=website,
            created_at=author_row["created_at"],
            updated_at=author_row["updated_at"],
        )

    async def update_author(
        self,
        *,
        user_id: int,
        specialty: Optional[str] = None,
        location: Optional[str] = None,
        website: Optional[str] = None,
    ) -> Author:
        author = await self.get_author_by_user_id(user_id=user_id)

        author.specialty = specialty if specialty is not None else author.specialty
        author.location = location if location is not None else author.location
        author.website = website if website is not None else author.website

        async with self.connection.transaction():
            author.updated_at = await queries.update_author_by_user_id(  # type: ignore
                self.connection,
                user_id=user_id,
                specialty=author.specialty,
                location=author.location,
                website=author.website,
            )

        return author

    async def delete_author(self, *, user_id: int) -> None:
        await queries.delete_author_by_user_id(  # type: ignore
            self.connection,
            user_id=user_id,
        )

    async def get_author_by_user_id(self, *, user_id: int) -> Author:
        author_rows = await queries.get_all_authors(  # type: ignore
            self.connection,
        )
        for row in author_rows:
            if row["user_id"] == user_id:
                return Author(**row)

        raise EntityDoesNotExist(
            "author with user_id {0} does not exist".format(user_id),
        )
