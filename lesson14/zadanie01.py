# Lekcja 14 - Zadanie 1
# Instalacja i konfiguracja SQLAlchemy

from pathlib import Path

import sqlalchemy
import psycopg2

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def main():
    print("=" * 70)
    print("ZADANIE 1 - INSTALACJA I KONFIGURACJA")
    print("=" * 70)

    print("\n1. WERSJE BIBLIOTEK")
    print("-" * 70)

    print(f"SQLAlchemy: {sqlalchemy.__version__}")
    print(f"psycopg2: {psycopg2.__version__}")

    print("\n2. KONFIGURACJA BAZY DANYCH")
    print("-" * 70)

    database_path = Path(__file__).resolve().parent / "test.db"

    database_url = f"sqlite:///{database_path}"

    engine = create_engine(
        database_url,
        echo=True
    )

    print(f"Sciezka bazy: {database_path}")
    print(f"Connection string: {database_url}")
    print(f"Dialekt: {engine.dialect.name}")
    print(f"Sterownik: {engine.dialect.driver}")

    try:
        print("\n3. TEST POLACZENIA")
        print("-" * 70)

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            ).scalar_one()

            sqlite_version = connection.execute(
                text("SELECT sqlite_version()")
            ).scalar_one()

            print(f"Wynik SELECT 1: {result}")
            print(f"Wersja SQLite: {sqlite_version}")
            print("Polaczenie z baza danych udane!")

        print("\n4. AUTOMATYCZNE TESTY")
        print("-" * 70)

        tests = {
            "SQLAlchemy zainstalowane":
                bool(sqlalchemy.__version__),

            "psycopg2 zainstalowane":
                bool(psycopg2.__version__),

            "Utworzono plik test.db":
                database_path.is_file(),

            "Poprawny dialekt SQLite":
                engine.dialect.name == "sqlite",

            "Poprawny sterownik SQLite":
                engine.dialect.driver == "pysqlite",

            "Zapytanie SELECT 1 dziala":
                result == 1,

            "Odczytano wersje SQLite":
                bool(sqlite_version)
        }

        for name, passed in tests.items():
            print(f"Czy {name}: {passed}")

        passed_count = sum(tests.values())

        print(
            f"\nZaliczone testy: "
            f"{passed_count}/{len(tests)}"
        )

        assert all(tests.values()), "Nie wszystkie testy zaliczone."

        print("\n5. PODSUMOWANIE")
        print("-" * 70)

        print("Biblioteki zainstalowane poprawnie.")
        print("Baza SQLite utworzona poprawnie.")
        print("Engine skonfigurowany poprawnie.")
        print("Polaczenie z baza dziala poprawnie.")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 1 wykonane poprawnie.")

    except SQLAlchemyError as error:
        print(f"Blad bazy danych: {error}")
        raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
