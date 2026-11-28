# Lekcja 14 - Zadanie 12
# Testy koncowe migracji Alembic

from datetime import date

from sqlalchemy import (
    inspect,
    select,
    text,
    Date
)

from sqlalchemy.orm import Session

from zadanie12 import Article, engine, DATABASE_PATH


ARTICLES_DATA = [
    (
        "Wprowadzenie do SQLAlchemy",
        "SQLAlchemy to biblioteka ORM dla jezyka Python.",
        date(2026, 11, 25)
    ),
    (
        "Migracje baz danych",
        "Alembic umozliwia zarzadzanie zmianami struktury bazy danych.",
        date(2026, 11, 26)
    ),
    (
        "Data Science i bazy danych",
        "Bazy danych stanowia wazny element projektow Data Science.",
        date(2026, 11, 27)
    ),
    (
        "Zarzadzanie migracjami",
        "Alembic pozwala wersjonowac strukture bazy danych.",
        date(2026, 11, 28)
    )
]


def section(title):
    print(f"\n{title}")
    print("-" * 70)


def main():

    print("=" * 70)
    print("ZADANIE 12 - TESTY KONCOWE ALEMBIC")
    print("=" * 70)

    section("1. WERYFIKACJA STRUKTURY")

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    columns = {
        column["name"]: column
        for column in inspector.get_columns("articles")
    }

    print(f"Tabele: {tables}")

    for name, column in columns.items():
        print(f"{name}: {column['type']}")

    with engine.connect() as conn:

        revision = conn.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()

    print(f"Aktualna migracja: {revision}")

    section("2. ZAPIS DAT PUBLIKACJI")

    with Session(engine) as session:

        # Testy danych wykonujemy w jednej transakcji.
        # Na koncu wycofamy zmiany przez rollback.

        for title, content, published_date in ARTICLES_DATA:

            article = session.scalar(
                select(Article).where(
                    Article.title == title
                )
            )

            if article is None:

                article = Article(
                    title=title,
                    content=content
                )

                session.add(article)

            article.published_date = published_date

            print(f"{title}: {published_date}")

        session.flush()

        section("3. ODCZYT ARTYKULOW")

        session.expire_all()

        articles = session.scalars(
            select(Article).order_by(
                Article.published_date
            )
        ).all()

        actual_data = [
            (
                article.title,
                article.content,
                article.published_date
            )
            for article in articles
        ]

        for article in articles:

            print(
                f"ID: {article.id} | "
                f"{article.published_date} | "
                f"{article.title}"
            )

        section("4. FILTROWANIE WEDLUG DATY")

        filtered = session.scalars(
            select(Article).where(
                Article.published_date >= date(2026, 11, 27)
            )
        ).all()

        for article in filtered:
            print(
                f"{article.published_date} | "
                f"{article.title}"
            )

        section("5. SORTOWANIE MALEJACE")

        sorted_articles = session.scalars(
            select(Article).order_by(
                Article.published_date.desc()
            )
        ).all()

        dates = [
            article.published_date
            for article in sorted_articles
        ]

        for article in sorted_articles:
            print(
                f"{article.published_date} | "
                f"{article.title}"
            )

        section("6. TEST WARTOSCI NULL")

        unpublished = Article(
            title="Artykul bez daty publikacji",
            content="Test dopuszczalnej wartosci NULL."
        )

        session.add(unpublished)
        session.flush()

        unpublished_id = unpublished.id

        session.expire(unpublished)

        null_allowed = (
            unpublished.published_date is None
        )

        print(f"ID: {unpublished_id}")
        print(f"Data publikacji: {unpublished.published_date}")

        section("7. AUTOMATYCZNE TESTY")

        tests = {
            "Baza danych istnieje":
                DATABASE_PATH.exists(),

            "Tabela articles istnieje":
                "articles" in tables,

            "Tabela alembic_version istnieje":
                "alembic_version" in tables,

            "Poprawna wersja migracji":
                revision == "075832ead7fc",

            "Tabela zawiera 4 kolumny":
                len(columns) == 4,

            "Kolumna published_date istnieje":
                "published_date" in columns,

            "Published_date ma typ DATE":
                isinstance(
                    columns["published_date"]["type"],
                    Date
                ),

            "Published_date dopuszcza NULL":
                columns["published_date"]["nullable"],

            "ID jest kluczem glownym":
                inspector.get_pk_constraint(
                    "articles"
                )["constrained_columns"] == ["id"],

            "Model zgodny ze struktura bazy":
                list(Article.__table__.columns.keys())
                == list(columns),

            "Cztery artykuly z datami":
                len(articles) == 4,

            "Poprawne dane artykulow":
                actual_data == ARTICLES_DATA,

            "Daty sa obiektami date":
                all(
                    isinstance(a.published_date, date)
                    for a in articles
                ),

            "Poprawna pierwsza data":
                articles[0].published_date
                == date(2026, 11, 25),

            "Poprawna ostatnia data":
                articles[-1].published_date
                == date(2026, 11, 28),

            "Filtrowanie zwraca 2 artykuly":
                len(filtered) == 2,

            "Filtrowanie zwraca poprawne daty":
                all(
                    a.published_date >= date(2026, 11, 27)
                    for a in filtered
                ),

            "Sortowanie malejace dziala":
                dates == sorted(dates, reverse=True),

            "Najnowszy artykul jest pierwszy":
                sorted_articles[0].title
                == "Zarzadzanie migracjami",

            "Nowy artykul otrzymal ID":
                unpublished_id is not None,

            "Mozna zapisac artykul bez daty":
                null_allowed
        }

        for name, result in tests.items():
            print(f"Czy {name}: {result}")

        passed = sum(tests.values())

        print(
            f"\nZaliczone testy: "
            f"{passed}/{len(tests)}"
        )

        assert all(tests.values()), (
            "Nie wszystkie testy zaliczone."
        )

        session.rollback()

    section("8. PODSUMOWANIE")

    print("Obie migracje zastosowane poprawnie.")
    print("Model zgodny ze struktura bazy danych.")
    print("Zapis i odczyt dat dziala poprawnie.")
    print("Filtrowanie i sortowanie dziala poprawnie.")
    print("Kolumna published_date dopuszcza NULL.")
    print("Zmiany testowe zostaly wycofane.")
    print("Wszystkie testy zakonczone pomyslnie.")

    engine.dispose()


if __name__ == "__main__":
    main()
