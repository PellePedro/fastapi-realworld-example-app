from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.articles import ArticlesRepository
from app.db.repositories.bookmarks import BookmarksRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.bookmarks import (
    BookmarkForResponse,
    BookmarkInCreate,
    BookmarkInResponse,
    ListOfBookmarksInResponse,
)
from app.resources import strings

router = APIRouter()


@router.get(
    "",
    response_model=ListOfBookmarksInResponse,
    name="bookmarks:list-bookmarks",
)
async def list_bookmarks(
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    bookmarks_repo: BookmarksRepository = Depends(
        get_repository(BookmarksRepository),
    ),
) -> ListOfBookmarksInResponse:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )
    bookmarks = await bookmarks_repo.get_bookmarks_for_user(user_id=user_in_db.id_)
    return ListOfBookmarksInResponse(
        bookmarks=[BookmarkForResponse.from_orm(b) for b in bookmarks],
        bookmarks_count=len(bookmarks),
    )


@router.post(
    "",
    response_model=BookmarkInResponse,
    status_code=HTTP_201_CREATED,
    name="bookmarks:create-bookmark",
)
async def create_bookmark(
    bookmark_create: BookmarkInCreate = Body(..., embed=True, alias="bookmark"),
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    bookmarks_repo: BookmarksRepository = Depends(
        get_repository(BookmarksRepository),
    ),
    articles_repo: ArticlesRepository = Depends(
        get_repository(ArticlesRepository),
    ),
) -> BookmarkInResponse:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    try:
        article = await articles_repo.get_article_by_slug(
            slug=bookmark_create.article_slug,
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=strings.ARTICLE_DOES_NOT_EXIST_ERROR,
        )

    try:
        await bookmarks_repo.get_bookmark(
            user_id=user_in_db.id_,
            slug=bookmark_create.article_slug,
        )
    except EntityDoesNotExist:
        pass
    else:
        raise HTTPException(
            status_code=400,
            detail=strings.BOOKMARK_ALREADY_EXISTS,
        )

    bookmark = await bookmarks_repo.create_bookmark(
        user_id=user_in_db.id_,
        article_id=article.id_,
        article_slug=article.slug,
        article_title=article.title,
        note=bookmark_create.note,
    )
    return BookmarkInResponse(bookmark=BookmarkForResponse.from_orm(bookmark))


@router.delete(
    "/{slug}",
    status_code=HTTP_204_NO_CONTENT,
    name="bookmarks:delete-bookmark",
)
async def delete_bookmark(
    slug: str,
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    bookmarks_repo: BookmarksRepository = Depends(
        get_repository(BookmarksRepository),
    ),
) -> None:
    user_in_db = await users_repo.get_user_by_username(
        username=current_user.username,
    )

    try:
        bookmark = await bookmarks_repo.get_bookmark(
            user_id=user_in_db.id_,
            slug=slug,
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=strings.BOOKMARK_DOES_NOT_EXIST_ERROR,
        )

    await bookmarks_repo.delete_bookmark(
        user_id=user_in_db.id_,
        article_id=bookmark.article_id,
    )
