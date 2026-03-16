from typing import List, Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.categories import Category
from app.services.categories import get_slug_for_category


class CategoriesRepository(BaseRepository):
    async def get_all_categories(self) -> List[Category]:
        rows = await queries.get_all_categories(self.connection)
        return [Category(**row) for row in rows]

    async def get_category_by_slug(self, *, slug: str) -> Category:
        row = await queries.get_category_by_slug(self.connection, slug=slug)
        if row:
            return Category(**row)

        raise EntityDoesNotExist(
            "category with slug {0} does not exist".format(slug),
        )

    async def create_category(
        self,
        *,
        name: str,
        description: str = "",
    ) -> Category:
        slug = get_slug_for_category(name)

        async with self.connection.transaction():
            row = await queries.create_new_category(
                self.connection,
                name=name,
                slug=slug,
                description=description,
            )

        return Category(
            id=row["id"],
            name=name,
            slug=slug,
            description=description,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def update_category(
        self,
        *,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Category:
        category = await self.get_category_by_slug(slug=slug)

        category.name = name if name is not None else category.name
        category.description = (
            description if description is not None else category.description
        )
        new_slug = get_slug_for_category(category.name) if name else category.slug

        async with self.connection.transaction():
            category.updated_at = await queries.update_category_by_slug(
                self.connection,
                slug=slug,
                new_name=category.name,
                new_slug=new_slug,
                new_description=category.description,
            )

        category.slug = new_slug
        return category

    async def delete_category(self, *, slug: str) -> None:
        await queries.delete_category_by_slug(self.connection, slug=slug)
