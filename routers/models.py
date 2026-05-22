from pydantic import BaseModel


class BookIn(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True


class Book(BookIn):
    id: int


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    year: int
