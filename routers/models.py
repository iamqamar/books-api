from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1450, le=datetime.now().year)
    available: bool = True

    @field_validator("title", "author", mode="before")
    @classmethod
    def no_blank_strings(cls, v: str) -> str :
        if not v.strip():
            raise ValueError("Fields cannot be blank or whitespace only")
        return v.strip()


class Book(BookIn):
    id: int


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    year: int


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1450, le=datetime.now().year)
    available: bool | None = None

    @field_validator("title", "author", mode="before")
    @classmethod
    def no_blank_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Field cannot be blank or whitespace only")
        return v.strip()
