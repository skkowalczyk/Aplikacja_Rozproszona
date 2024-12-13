from sqlmodel import SQLModel, Field
from typing import Optional

# Model dla tabeli z książkami
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Klucz główny
    title: str  # Tytuł książki
    author: str  # Autor książki
    year: int  # Rok wydania
    available: bool = True  # Czy książka jest dostępna do wypożyczenia

# Model dla tabeli z użytkownikami
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Klucz główny
    username: str  # Nazwa użytkownika
    email: str  # Adres email
    hashed_password: str  # Zahasłowane hasło użytkownika