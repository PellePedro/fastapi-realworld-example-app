from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.authors import AuthorsRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.authors import (
    AuthorForResponse,
    AuthorInCreate,
    AuthorInResponse,
    AuthorInUpdate,
    ListOfAuthorsInResponse,
)
from app.resources import strings

router = APIRouter()


@router.get("", response_model=ListOfAuthorsInResponse, name="authors:list-authors")
async def list_authors(
    authors_repo: AuthorsRepository = Depends(get_repository(AuthorsRepository)),
) -> ListOfAuthorsInResponse:
    authors = await authors_repo.get_all_authors()
    return ListOfAuthorsInResponse(
        authors=[AuthorForResponse.from_orm(author) for author in authors],
        authors_count=len(authors),
    )


@router.get(
    "/{username}",
    response_model=AuthorInResponse,
    name="authors:get-author",
)
async def get_author(
    username: str,
    authors_repo: AuthorsRepository = Depends(get_repository(AuthorsRepository)),
) -> AuthorInResponse:
    try:
        author = await authors_repo.get_author_by_username(username=username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.AUTHOR_DOES_NOT_EXIST_ERROR,
        )

    return AuthorInResponse(author=AuthorForResponse.from_orm(author))


@router.post(
    "",
    response_model=AuthorInResponse,
    status_code=HTTP_201_CREATED,
    name="authors:create-author",
)
async def create_author(
    author_create: AuthorInCreate = Body(..., embed=True, alias="author"),
    current_user: User = Depends(get_current_user_authorizer()),
    authors_repo: AuthorsRepository = Depends(get_repository(AuthorsRepository)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> AuthorInResponse:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    author_exists = True
    try:
        await authors_repo.get_author_by_user_id(user_id=user_in_db.id_)
    except EntityDoesNotExist:
        author_exists = False

    if author_exists:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.AUTHOR_ALREADY_EXISTS,
        )

    author = await authors_repo.create_author(
        user_id=user_in_db.id_,
        specialty=author_create.specialty,
        location=author_create.location,
        website=author_create.website,
    )
    author.username = current_user.username

    return AuthorInResponse(author=AuthorForResponse.from_orm(author))


@router.put(
    "",
    response_model=AuthorInResponse,
    name="authors:update-author",
)
async def update_author(
    author_update: AuthorInUpdate = Body(..., embed=True, alias="author"),
    current_user: User = Depends(get_current_user_authorizer()),
    authors_repo: AuthorsRepository = Depends(get_repository(AuthorsRepository)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> AuthorInResponse:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    try:
        author = await authors_repo.update_author(
            user_id=user_in_db.id_,
            **author_update.dict(exclude_unset=True),
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.AUTHOR_DOES_NOT_EXIST_ERROR,
        )

    return AuthorInResponse(author=AuthorForResponse.from_orm(author))


@router.delete(
    "",
    status_code=HTTP_204_NO_CONTENT,
    name="authors:delete-author",
)
async def delete_author(
    current_user: User = Depends(get_current_user_authorizer()),
    authors_repo: AuthorsRepository = Depends(get_repository(AuthorsRepository)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> None:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    try:
        await authors_repo.get_author_by_user_id(user_id=user_in_db.id_)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.AUTHOR_DOES_NOT_EXIST_ERROR,
        )

    await authors_repo.delete_author(user_id=user_in_db.id_)
