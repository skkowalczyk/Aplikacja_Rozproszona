from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import init_db, get_session
from models import Book, User
from passlib.context import CryptContext

app = FastAPI()  # Tworzenie instancji aplikacji FastAPI

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)  # Funkcja do hashowania haseł

# Inicjalizacja bazy danych przy starcie aplikacji
@app.on_event("startup")
def on_startup():
    init_db()

# Endpoint: Dodawanie książki
@app.post("/books/", response_model=Book)
def add_book(book: Book, session: Session = Depends(get_session)):
    session.add(book)  # Dodanie książki do sesji
    session.commit()  # Zapisanie zmian w bazie danych
    session.refresh(book)  # Odświeżenie danych książki
    return book  # Zwrócenie dodanej książki

# Endpoint: Pobieranie listy książek
@app.get("/books/", response_model=list[Book])
def get_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book)).all()  # Pobranie wszystkich książek
    return books  # Zwrócenie listy książek

# Endpoint: Pobieranie szczegółów książki po ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)  # Pobranie książki po ID
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Endpoint: Aktualizacja dostępności książki
@app.patch("/books/{book_id}", response_model=Book)
def update_book_availability(book_id: int, available: bool, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)  # Pobranie książki po ID
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.available = available  # Aktualizacja dostępności
    session.add(book)  # Dodanie zmienionej książki do sesji
    session.commit()  # Zapisanie zmian
    session.refresh(book)  # Odświeżenie danych
    return book

# Endpoint: Usuwanie książki
@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)  # Pobranie książki po ID
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)  # Usunięcie książki
    session.commit()  # Zapisanie zmian
    return {"ok": True}  # Zwrócenie potwierdzenia

# Endpoint: Rejestracja użytkownika
@app.post("/users/", response_model=User)
def register_user(user: User, session: Session = Depends(get_session)):
    user.hashed_password = hash_password(user.hashed_password)  # Hashowanie hasła
    session.add(user)  # Dodanie użytkownika do sesji
    session.commit()  # Zapisanie zmian w bazie danych
    session.refresh(user)  # Odświeżenie danych użytkownika
    return user  # Zwrócenie dodanego użytkownika

# Endpoint: Pobieranie listy użytkowników
@app.get("/users/", response_model=list[User])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()  # Pobranie wszystkich użytkowników
    return users  # Zwrócenie listy użytkowników