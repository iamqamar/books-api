from fastapi import APIRouter, HTTPException, status

from routers.models import Book, BookIn, BookOut, BookUpdate

router = APIRouter(
    prefix="/books",  # prepended to every route in this file
    tags=["books"],  # groups routes in /docs
)


books: list[Book] = [
    Book(
        id=101, title="Atomic Habits", author="James Clear", year=2018, available=True
    ),
    Book(id=102, title="Deep Work", author="Cal Newport", year=2016, available=True),
    Book(
        id=103,
        title="Clean Code",
        author="Robert C. Martin",
        year=2008,
        available=False,
    ),
    Book(
        id=104,
        title="The Pragmatic Programmer",
        author="Andrew Hunt",
        year=1999,
        available=True,
    ),
    Book(
        id=105,
        title="Python Crash Course",
        author="Eric Matthes",
        year=2019,
        available=False,
    ),
]

next_id = 106


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


@router.put("/{id}", response_model=BookOut, status_code=status.HTTP_200_OK)
def update_book(id: int, book: BookIn):
    for index, stored_book in enumerate(books):
        if stored_book.id == id:
            updated = Book(id=id, **book.model_dump())
            books[index] = updated
            return updated

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.patch("/{id}", response_model=BookOut, status_code=status.HTTP_200_OK)
def partial_update_book(id: int, book_update: BookUpdate):
    for index, stored_book in enumerate(books):
        if stored_book.id == id:
            stored_data = stored_book.model_dump()  # stored_data -> dict[str, any]
            update_data = book_update.model_dump(exclude_none=True)
            merged = {**stored_data, **update_data}
            books[index] = Book(**merged)
            return books[index]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
