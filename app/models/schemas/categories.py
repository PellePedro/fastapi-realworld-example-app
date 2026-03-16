from typing import List, Optional

from app.models.domain.categories import Category
from app.models.schemas.rwschema import RWSchema


class CategoryForResponse(RWSchema, Category):
    pass


class CategoryInResponse(RWSchema):
    category: CategoryForResponse


class CategoryInCreate(RWSchema):
    name: str
    description: str = ""


class CategoryInUpdate(RWSchema):
    name: Optional[str] = None
    description: Optional[str] = None


class ListOfCategoriesInResponse(RWSchema):
    categories: List[CategoryForResponse]
    categories_count: int
