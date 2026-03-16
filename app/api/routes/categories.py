from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.categories import CategoriesRepository
from app.models.domain.users import User
from app.models.schemas.categories import (
    CategoryForResponse,
    CategoryInCreate,
    CategoryInResponse,
    CategoryInUpdate,
    ListOfCategoriesInResponse,
)
from app.resources import strings

router = APIRouter()


@router.get(
    "",
    response_model=ListOfCategoriesInResponse,
    name="categories:list-categories",
)
async def list_categories(
    categories_repo: CategoriesRepository = Depends(
        get_repository(CategoriesRepository),
    ),
) -> ListOfCategoriesInResponse:
    categories = await categories_repo.get_all_categories()
    return ListOfCategoriesInResponse(
        categories=[CategoryForResponse.from_orm(c) for c in categories],
        categories_count=len(categories),
    )


@router.get(
    "/{slug}",
    response_model=CategoryInResponse,
    name="categories:get-category",
)
async def get_category(
    slug: str,
    categories_repo: CategoriesRepository = Depends(
        get_repository(CategoriesRepository),
    ),
) -> CategoryInResponse:
    try:
        category = await categories_repo.get_category_by_slug(slug=slug)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=strings.CATEGORY_DOES_NOT_EXIST_ERROR,
        )

    return CategoryInResponse(category=CategoryForResponse.from_orm(category))


@router.post(
    "",
    response_model=CategoryInResponse,
    status_code=HTTP_201_CREATED,
    name="categories:create-category",
)
async def create_category(
    category_create: CategoryInCreate = Body(..., embed=True, alias="category"),
    _: User = Depends(get_current_user_authorizer()),
    categories_repo: CategoriesRepository = Depends(
        get_repository(CategoriesRepository),
    ),
) -> CategoryInResponse:
    category = await categories_repo.create_category(
        name=category_create.name,
        description=category_create.description,
    )
    return CategoryInResponse(category=CategoryForResponse.from_orm(category))


@router.put(
    "/{slug}",
    response_model=CategoryInResponse,
    name="categories:update-category",
)
async def update_category(
    slug: str,
    category_update: CategoryInUpdate = Body(..., embed=True, alias="category"),
    _: User = Depends(get_current_user_authorizer()),
    categories_repo: CategoriesRepository = Depends(
        get_repository(CategoriesRepository),
    ),
) -> CategoryInResponse:
    try:
        category = await categories_repo.update_category(
            slug=slug,
            **category_update.dict(exclude_unset=True),
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=strings.CATEGORY_DOES_NOT_EXIST_ERROR,
        )

    return CategoryInResponse(category=CategoryForResponse.from_orm(category))


@router.delete(
    "/{slug}",
    status_code=HTTP_204_NO_CONTENT,
    name="categories:delete-category",
)
async def delete_category(
    slug: str,
    _: User = Depends(get_current_user_authorizer()),
    categories_repo: CategoriesRepository = Depends(
        get_repository(CategoriesRepository),
    ),
) -> None:
    try:
        await categories_repo.get_category_by_slug(slug=slug)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=strings.CATEGORY_DOES_NOT_EXIST_ERROR,
        )

    await categories_repo.delete_category(slug=slug)
