from sqlmodel import SQLModel, create_engine, Session

# Tworzenie połączenia z bazą danych SQLite
DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL, echo=True)

# Funkcja inicjalizująca bazę danych
def init_db():
    SQLModel.metadata.create_all(engine)

# Tworzenie sesji dla bazy danych
def get_session():
    with Session(engine) as session:
        yield session
