from fastapi import FastAPI
from routers import books
from routers import health

app = FastAPI()

app.include_router(books.router)
app.include_router(health.router)