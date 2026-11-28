# Lekcja 14 - Zadanie 12
# Migracja z Alembic

from pathlib import Path

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Date
)

from sqlalchemy.orm import declarative_base


DATABASE_PATH = (
    Path(__file__).resolve().parent / "alembic_test.db"
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()


class Article(Base):

    __tablename__ = "articles"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    published_date = Column(
        Date,
        nullable=True
    )

    def __repr__(self):
        return (
            f"Article("
            f"id={self.id}, "
            f"title={self.title!r})"
        )


def main():

    print("=" * 70)
    print("ZADANIE 12 - MIGRACJA Z ALEMBIC")
    print("=" * 70)

    print("\n1. KONFIGURACJA BAZY DANYCH")
    print("-" * 70)

    print(f"Baza danych: {DATABASE_PATH}")
    print(f"Connection string: {DATABASE_URL}")
    print(f"Dialekt: {engine.dialect.name}")

    print("\n2. DEFINICJA MODELU ARTICLE")
    print("-" * 70)

    print(f"Model: {Article.__name__}")
    print(f"Tabela: {Article.__tablename__}")

    for column in Article.__table__.columns:

        print(
            f"Kolumna: {column.name:<20}"
            f"Typ: {str(column.type):<20}"
            f"PK: {column.primary_key}"
        )

    print("\n3. AUTOMATYCZNE TESTY")
    print("-" * 70)

    columns = Article.__table__.columns

    tests = {
        "Model dziedziczy po Base":
            issubclass(Article, Base),

        "Poprawna nazwa tabeli":
            Article.__tablename__ == "articles",

        "Model zawiera 4 kolumny":
            len(columns) == 4,

        "Poprawne nazwy kolumn":
            list(columns.keys()) == [
                "id", "title", "content", "published_date"
            ],

        "ID ma typ Integer":
            isinstance(columns.id.type, Integer),

        "ID jest kluczem glownym":
            columns.id.primary_key,

        "Title ma typ String":
            isinstance(columns.title.type, String),

        "Title ma dlugosc 200":
            columns.title.type.length == 200,

        "Title jest wymagany":
            not columns.title.nullable,

        "Content ma typ Text":
            isinstance(columns.content.type, Text),

        "Content jest wymagany":
            not columns.content.nullable,

        "Kolumna published_date istnieje":
            "published_date" in columns,

        "Published_date ma typ Date":
            isinstance(columns.published_date.type, Date),

        "Published_date dopuszcza NULL":
            columns.published_date.nullable,

        "Oddzielna baza dla Alembic":
            DATABASE_PATH.name == "alembic_test.db"
    }

    for name, result in tests.items():
        print(f"Czy {name}: {result}")

    passed = sum(tests.values())

    print(f"\nZaliczone testy: {passed}/{len(tests)}")

    assert all(tests.values()), "Nie wszystkie testy zaliczone."

    print("\n4. PODSUMOWANIE")
    print("-" * 70)

    print("Model Article zdefiniowany poprawnie.")
    print("Model zawiera 4 kolumny.")
    print("Metadane gotowe do migracji.")
    print("Struktura tabeli jest zarzadzana przez Alembic.")
    print("Wszystkie testy zakonczone pomyslnie.")


if __name__ == "__main__":
    main()
