from typing import List, Optional

from app.models.domain.authors import Author
from app.models.schemas.rwschema import RWSchema


class AuthorForResponse(RWSchema, Author):
    pass


class AuthorInResponse(RWSchema):
    author: AuthorForResponse


class AuthorInCreate(RWSchema):
    specialty: str = ""
    location: str = ""
    website: str = ""


class AuthorInUpdate(RWSchema):
    specialty: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None


class ListOfAuthorsInResponse(RWSchema):
    authors: List[AuthorForResponse]
    authors_count: int
