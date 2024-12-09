from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import init_db, get_session
from models import Book

app = FastAPI()

# Inicjalizacja bazy danych przy starcie aplikacji
@app.on_event("startup")
def on_startup():
    init_db()

# Endpoint: Dodawanie nowej książki
@app.post("/books/", response_model=Book)
def add_book(book: Book, session: Session = Depends(get_session)):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

# Endpoint: Pobieranie listy książek
@app.get("/books/", response_model=list[Book])
def get_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book)).all()
    return books

# Endpoint: Pobieranie szczegółów książki po ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Endpoint: Aktualizacja dostępności książki
@app.patch("/books/{book_id}", response_model=Book)
def update_book_availability(book_id: int, available: bool, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.available = available
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

# Endpoint: Usuwanie książki
@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}
