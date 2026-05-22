from fastapi import APIRouter, HTTPException, status
from routers.models import Book, BookIn, BookOut

router = APIRouter(
    prefix="/books",  # prepended to every route in this file
    tags=["books"],  # groups routes in /docs
)


next_id = 101
books: list[Book] = []


@router.get("", response_model=list[BookOut])
def fetch_all_books():
    return books


@router.get("/{id}", response_model=BookOut)
def fetch_a_book(id: int):
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_a_book(book: BookIn):
    global next_id
    new_book = Book(id=next_id, **book.model_dump())
    books.append(new_book)
    next_id += 1
    return new_book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_book(id: int):
    for book in books:
        if book.id == id:
            books.remove(book)
            return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
