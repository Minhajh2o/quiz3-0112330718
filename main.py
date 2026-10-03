from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
books = {}     # in-memory storage
next_id = 1    # auto-increment ID

class Book(BaseModel):
    title: str
    author: str
    price: float

@app.get("/books")
def get_all_books():
    return books

class BookUpdate(BaseModel):
    title:  Optional[str]   = None
    price:  Optional[float] = None

@app.put("/books/{book_id}")
def update_book(book_id: int, update: BookUpdate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Not found")
    data = books[book_id]
    if update.title:  data["title"] = update.title
    if update.price is not None: data["price"] = update.price
    return data

@app.post("/books", status_code=201)
def create_book(book: Book):
    global next_id
    books[next_id] = book.dict()
    book_id = next_id
    next_id += 1
    return {"id": book_id, **books[book_id]}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Not found")
    del books[book_id]
    return {"message": "Book deleted"}