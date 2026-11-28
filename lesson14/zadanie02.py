# Lekcja 14 - Zadanie 2
# Pierwszy model SQLAlchemy

from pathlib import Path

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    inspect
)

from sqlalchemy.orm import declarative_base


DATABASE_PATH = Path(__file__).resolve().parent / "test.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()


class Student(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    email = Column(String(150), unique=True)

    def __repr__(self):
        return (
            f"Student(id={self.id}, "
            f"name={self.name!r}, "
            f"age={self.age}, "
            f"email={self.email!r})"
        )


def main():

    print("=" * 70)
    print("ZADANIE 2 - PIERWSZY MODEL")
    print("=" * 70)

    try:

        print("\n1. KONFIGURACJA BAZY DANYCH")
        print("-" * 70)

        print(f"Baza danych: {DATABASE_PATH}")
        print(f"Dialekt: {engine.dialect.name}")

        print("\n2. DEFINICJA MODELU STUDENT")
        print("-" * 70)

        print(f"Model: {Student.__name__}")
        print(f"Tabela: {Student.__tablename__}")

        for column in Student.__table__.columns:

            print(
                f"Kolumna: {column.name:10s} "
                f"Typ: {str(column.type):15s} "
                f"PK: {column.primary_key} "
                f"Unique: {bool(column.unique)}"
            )

        print("\n3. TWORZENIE TABELI")
        print("-" * 70)

        Base.metadata.create_all(engine)

        print("Tabela students zostala utworzona.")

        print("\n4. SPRAWDZENIE STRUKTURY BAZY")
        print("-" * 70)

        inspector = inspect(engine)

        tables = inspector.get_table_names()

        print(f"Tabele w bazie: {tables}")

        columns = inspector.get_columns("students")

        for column in columns:

            print(
                f"Nazwa: {column['name']:10s} "
                f"Typ: {str(column['type']):15s} "
                f"Nullable: {column['nullable']}"
            )

        print("\n5. KLUCZ GLOWNY")
        print("-" * 70)

        primary_key = inspector.get_pk_constraint(
            "students"
        )

        print(primary_key)

        print("\n6. OGRANICZENIA UNIQUE")
        print("-" * 70)

        unique_constraints = (
            inspector.get_unique_constraints("students")
        )

        for constraint in unique_constraints:
            print(constraint)

        column_map = {
            column["name"]: column
            for column in columns
        }

        print("\n7. AUTOMATYCZNE TESTY")
        print("-" * 70)

        tests = {
            "Model dziedziczy po Base":
                issubclass(Student, Base),

            "Plik test.db istnieje":
                DATABASE_PATH.is_file(),

            "Baza nie jest pusta":
                DATABASE_PATH.stat().st_size > 0,

            "Tabela students istnieje":
                "students" in tables,

            "Tabela zawiera 4 kolumny":
                len(columns) == 4,

            "Nazwy kolumn sa poprawne":
                list(column_map) == [
                    "id", "name", "age", "email"
                ],

            "Kolumna id ma typ Integer":
                isinstance(
                    column_map["id"]["type"],
                    Integer
                ),

            "Kolumna id jest kluczem glownym":
                primary_key["constrained_columns"]
                == ["id"],

            "Kolumna name ma typ String":
                isinstance(
                    column_map["name"]["type"],
                    String
                ),

            "Kolumna name ma dlugosc 100":
                column_map["name"]["type"].length == 100,

            "Kolumna age ma typ Integer":
                isinstance(
                    column_map["age"]["type"],
                    Integer
                ),

            "Kolumna email ma typ String":
                isinstance(
                    column_map["email"]["type"],
                    String
                ),

            "Kolumna email ma dlugosc 150":
                column_map["email"]["type"].length == 150,

            "Kolumna email ma ograniczenie UNIQUE":
                any(
                    constraint["column_names"] == ["email"]
                    for constraint in unique_constraints
                )
        }

        for name, passed in tests.items():
            print(f"Czy {name}: {passed}")

        passed_count = sum(tests.values())

        print(
            f"\nZaliczone testy: "
            f"{passed_count}/{len(tests)}"
        )

        assert all(tests.values()), (
            "Nie wszystkie testy zaliczone."
        )

        print("\n8. PODSUMOWANIE")
        print("-" * 70)

        print(f"Model: {Student.__name__}")
        print(f"Tabela: {Student.__tablename__}")
        print(f"Liczba kolumn: {len(columns)}")
        print(
            f"Rozmiar bazy: "
            f"{DATABASE_PATH.stat().st_size:,} bajtow"
        )

        print("Klucz glowny: id")
        print("Ograniczenie UNIQUE: email")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 2 wykonane poprawnie.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
