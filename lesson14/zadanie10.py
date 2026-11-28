# Lekcja 14 - Zadanie 10
# Eager vs Lazy Loading

import time
from statistics import mean, pstdev

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    event,
    inspect
)

from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    joinedload
)

from zadanie02 import Base, engine, DATABASE_PATH


Session = sessionmaker(bind=engine)

N_AUTHORS = 10
BOOKS_PER_AUTHOR = 5
N_BOOKS = N_AUTHORS * BOOKS_PER_AUTHOR
REPEATS = 3


# MODELE ORM

class Author(Base):

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(100),
        nullable=False,
        unique=True
    )

    books = relationship(
        "Book",
        back_populates="author",
        lazy="select",
        order_by="Book.id"
    )

    def __repr__(self):
        return (
            f"Author(id={self.id}, "
            f"name={self.name!r})"
        )


class Book(Base):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True)

    title = Column(
        String(200),
        nullable=False
    )

    author_id = Column(
        Integer,
        ForeignKey("authors.id"),
        nullable=False
    )

    author = relationship(
        "Author",
        back_populates="books"
    )

    def __repr__(self):
        return (
            f"Book(id={self.id}, "
            f"title={self.title!r}, "
            f"author_id={self.author_id})"
        )


def section(title):

    print(f"\n{title}")
    print("=" * 80)


# GENEROWANIE DANYCH

def generate_data():

    with Session.begin() as session:

        existing = {
            author.name: author
            for author in session.query(Author).all()
        }

        added_authors = 0
        added_books = 0

        for i in range(1, N_AUTHORS + 1):

            name = f"Author_{i:02d}"

            author = existing.get(name)

            if author is None:

                author = Author(name=name)

                session.add(author)

                added_authors += 1

            existing_titles = {
                book.title
                for book in author.books
            }

            for j in range(1, BOOKS_PER_AUTHOR + 1):

                title = f"Book_{i:02d}_{j:02d}"

                if title not in existing_titles:

                    author.books.append(
                        Book(title=title)
                    )

                    added_books += 1

        print(f"Dodano autorow: {added_authors}")
        print(f"Dodano ksiazek: {added_books}")

    print("Commit danych wykonany poprawnie.")


# AUTOMATYCZNY LICZNIK SQL

class QueryCounter:

    def __init__(self):

        self.count = 0
        self.statements = []

    def before_cursor_execute(
        self,
        conn,
        cursor,
        statement,
        parameters,
        context,
        executemany
    ):

        if statement.lstrip().upper().startswith("SELECT"):

            self.count += 1
            self.statements.append(statement)

    def __enter__(self):

        event.listen(
            engine,
            "before_cursor_execute",
            self.before_cursor_execute
        )

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        event.remove(
            engine,
            "before_cursor_execute",
            self.before_cursor_execute
        )


# LAZY LOADING

def lazy_loading(session):

    authors = (
        session.query(Author)
        .order_by(Author.id)
        .all()
    )

    result = []

    for author in authors:

        books = [
            (book.id, book.title)
            for book in author.books
        ]

        result.append(
            (author.id, author.name, books)
        )

    return result


# EAGER LOADING

def eager_loading(session):

    authors = (
        session.query(Author)
        .options(joinedload(Author.books))
        .order_by(Author.id)
        .all()
    )

    result = []

    for author in authors:

        books = [
            (book.id, book.title)
            for book in author.books
        ]

        result.append(
            (author.id, author.name, books)
        )

    return result


# BENCHMARK

def benchmark(strategy, name):

    times = []
    query_counts = []
    results = []
    statements = []

    for i in range(REPEATS):

        print(f"\n{name} - proba {i + 1}")

        # Nowa sesja dla kazdego pomiaru

        with Session() as session:

            with QueryCounter() as counter:

                start = time.perf_counter()

                result = strategy(session)

                elapsed = time.perf_counter() - start

            times.append(elapsed)

            query_counts.append(counter.count)

            statements.append(counter.statements)

            results.append(result)

        print(f"Czas: {elapsed:.6f} s")
        print(f"Liczba SELECT: {counter.count}")

    return {
        "name": name,
        "times": times,
        "mean_time": mean(times),
        "std_time": pstdev(times),
        "query_counts": query_counts,
        "mean_queries": mean(query_counts),
        "results": results,
        "result": results[-1],
        "statements": statements
    }


def reduction_percent(before, after):

    if before == 0:
        return 0.0

    return 100 * (before - after) / before


def print_results(result):

    total_books = 0

    for author_id, author_name, books in result:

        print(
            f"\nAutor: {author_name} "
            f"(ID: {author_id})"
        )

        for book_id, title in books:

            print(f"  - {title} (ID: {book_id})")

            total_books += 1

    print(f"\nLiczba autorow: {len(result)}")
    print(f"Liczba ksiazek: {total_books}")


def print_bar(label, value, maximum):

    length = round(
        40 * value / maximum
    ) if maximum > 0 else 0

    bar = "#" * length if length else "."

    print(f"{label:<15} {bar} {value:.6f}")


def main():

    print("=" * 80)
    print("ZADANIE 10 - EAGER VS LAZY LOADING")
    print("=" * 80)

    section("1. KONFIGURACJA")

    print(f"Baza danych: {DATABASE_PATH}")
    print(f"Autorzy: {N_AUTHORS}")
    print(f"Ksiazki na autora: {BOOKS_PER_AUTHOR}")
    print(f"Laczna liczba ksiazek: {N_BOOKS}")
    print(f"Liczba powtorzen: {REPEATS}")

    # Wymaganie zadania: echo=True

    engine.echo = True

    print(f"Echo SQL: {engine.echo}")

    section("2. TWORZENIE TABEL")

    tables_before = set(
        inspect(engine).get_table_names()
    )

    Base.metadata.create_all(engine)

    inspector = inspect(engine)

    tables_after = set(
        inspector.get_table_names()
    )

    print(f"Tabele przed: {sorted(tables_before)}")
    print(f"Tabele po: {sorted(tables_after)}")

    section("3. GENEROWANIE DANYCH")

    generate_data()

    section("4. WERYFIKACJA DANYCH")

    with Session() as session:

        authors_count = session.query(Author).count()
        books_count = session.query(Book).count()

        authors = (
            session.query(Author)
            .options(joinedload(Author.books))
            .order_by(Author.id)
            .all()
        )

        books_per_author = [
            len(author.books)
            for author in authors
        ]

        print(f"Liczba autorow: {authors_count}")
        print(f"Liczba ksiazek: {books_count}")
        print(f"Ksiazki na autora: {books_per_author}")

    assert authors_count == N_AUTHORS
    assert books_count == N_BOOKS

    assert all(
        count == BOOKS_PER_AUTHOR
        for count in books_per_author
    )

    section("5. LAZY LOADING - BENCHMARK")

    lazy = benchmark(
        lazy_loading,
        "Lazy Loading"
    )

    section("6. EAGER LOADING - BENCHMARK")

    eager = benchmark(
        eager_loading,
        "Eager Loading"
    )

    section("7. AUTORZY I ICH KSIAZKI")

    print_results(eager["result"])

    section("8. POROWNANIE WYNIKOW")

    print(
        f"{'Strategia':<20}"
        f"{'Czas [ms]':>15}"
        f"{'SELECT':>12}"
        f"{'Std [ms]':>15}"
    )

    print("-" * 62)

    for item in (lazy, eager):

        print(
            f"{item['name']:<20}"
            f"{item['mean_time'] * 1000:>15.4f}"
            f"{item['mean_queries']:>12.0f}"
            f"{item['std_time'] * 1000:>15.4f}"
        )

    section("9. ANALIZA ZAPYTAN SQL")

    print("Lazy Loading:")

    for i, sql in enumerate(
        lazy["statements"][0],
        start=1
    ):

        print(f"\nZapytanie {i}:")
        print(sql)

    print("\nEager Loading:")

    for i, sql in enumerate(
        eager["statements"][0],
        start=1
    ):

        print(f"\nZapytanie {i}:")
        print(sql)

    section("10. REDUKCJA ZAPYTAN I CZASU")

    query_reduction = reduction_percent(
        lazy["mean_queries"],
        eager["mean_queries"]
    )

    time_reduction = reduction_percent(
        lazy["mean_time"],
        eager["mean_time"]
    )

    speedup = (
        lazy["mean_time"] / eager["mean_time"]
    )

    print(
        f"Lazy Loading: "
        f"{lazy['mean_queries']:.0f} zapytan"
    )

    print(
        f"Eager Loading: "
        f"{eager['mean_queries']:.0f} zapytan"
    )

    print(
        f"Redukcja zapytan: "
        f"{query_reduction:.2f}%"
    )

    print(
        f"Redukcja czasu: "
        f"{time_reduction:.2f}%"
    )

    print(
        f"Wspolczynnik przyspieszenia: "
        f"{speedup:.2f}x"
    )

    section("11. WIZUALIZACJA TEKSTOWA")

    print("\nLiczba zapytan SQL:")

    print(
        "Lazy Loading:  "
        + "#" * int(lazy["mean_queries"])
    )

    print(
        "Eager Loading: "
        + "#" * int(eager["mean_queries"])
    )

    print("\nCzas wykonania [ms]:")

    maximum = max(
        lazy["mean_time"],
        eager["mean_time"]
    ) * 1000

    print_bar(
        "Lazy Loading",
        lazy["mean_time"] * 1000,
        maximum
    )

    print_bar(
        "Eager Loading",
        eager["mean_time"] * 1000,
        maximum
    )

    section("12. AUTOMATYCZNE TESTY")

    foreign_keys = inspector.get_foreign_keys(
        "books"
    )

    with Session() as session:

        final_authors = session.query(Author).count()
        final_books = session.query(Book).count()

    tests = {

        "Plik bazy danych istnieje":
            DATABASE_PATH.exists(),

        "Tabela authors istnieje":
            "authors" in tables_after,

        "Tabela books istnieje":
            "books" in tables_after,

        "Poprzednie tabele zachowane":
            tables_before.issubset(tables_after),

        "Poprawny klucz obcy":
            any(
                fk["referred_table"] == "authors"
                and fk["constrained_columns"] == ["author_id"]
                for fk in foreign_keys
            ),

        "Relacja Author.books istnieje":
            "books" in inspect(Author).relationships,

        "Relacja Book.author istnieje":
            "author" in inspect(Book).relationships,

        "Utworzono 10 autorow":
            authors_count == 10,

        "Utworzono 50 ksiazek":
            books_count == 50,

        "Kazdy autor ma 5 ksiazek":
            books_per_author == [5] * 10,

        "Echo SQL wlaczone":
            engine.echo is True,

        "Lazy Loading - trzy pomiary":
            len(lazy["times"]) == REPEATS,

        "Eager Loading - trzy pomiary":
            len(eager["times"]) == REPEATS,

        "Wszystkie czasy Lazy sa dodatnie":
            all(t > 0 for t in lazy["times"]),

        "Wszystkie czasy Eager sa dodatnie":
            all(t > 0 for t in eager["times"]),

        "Lazy Loading wykonuje 11 SELECT":
            lazy["query_counts"] == [11] * REPEATS,

        "Eager Loading wykonuje 1 SELECT":
            eager["query_counts"] == [1] * REPEATS,

        "Lazy Loading zwraca 10 autorow":
            len(lazy["result"]) == 10,

        "Eager Loading zwraca 10 autorow":
            len(eager["result"]) == 10,

        "Lazy Loading zwraca 50 ksiazek":
            sum(
                len(row[2])
                for row in lazy["result"]
            ) == 50,

        "Eager Loading zwraca 50 ksiazek":
            sum(
                len(row[2])
                for row in eager["result"]
            ) == 50,

        "Wyniki obu strategii identyczne":
            lazy["result"] == eager["result"],

        "Wszystkie powtorzenia daja identyczny wynik":
            all(
                result == lazy["result"]
                for result in lazy["results"]
                + eager["results"]
            ),

        "Eager Loading wykorzystuje JOIN":
            all(
                "JOIN" in statements[0].upper()
                for statements in eager["statements"]
            ),

        "Redukcja zapytan przekracza 90 procent":
            query_reduction > 90,

        "Liczba autorow bez zmian":
            final_authors == authors_count,

        "Liczba ksiazek bez zmian":
            final_books == books_count
    }

    for name, passed in tests.items():

        print(f"Czy {name}: {passed}")

    passed_count = sum(tests.values())

    print(
        f"\nZaliczone testy: "
        f"{passed_count}/{len(tests)}"
    )

    assert all(tests.values()), "Nie wszystkie testy zaliczone."

    section("13. WNIOSKI")

    conclusions = [

        "Lazy Loading pobiera relacje na zadanie.",

        "Lazy Loading moze powodowac problem N+1.",

        "Dla 10 autorow wykonano 11 zapytan SELECT.",

        "joinedload pobiera autorow i ksiazki razem.",

        "Eager Loading wykorzystuje LEFT OUTER JOIN.",

        "Eager Loading wykonuje jedno zapytanie SELECT.",

        "Obie strategie zwracaja identyczne dane.",

        "Nowa sesja ogranicza wplyw identity map.",

        "echo=True wyswietla wykonywane zapytania SQL.",

        "Event SQLAlchemy automatycznie liczy SELECT.",

        "perf_counter mierzy czas wykonania operacji.",

        "Srednia z trzech prob ogranicza wplyw wahan.",

        "Eager Loading ogranicza liczbe zapytan.",

        "JOIN moze zwielokrotniac wiersze SQL.",

        "Eager Loading nie zawsze jest szybszy.",

        "Lazy Loading jest przydatny, gdy relacje "
        "nie sa potrzebne.",

        "Wyniki czasowe zaleza od sprzetu i danych.",

        "Echo SQL wprowadza dodatkowy narzut czasowy."
    ]

    for i, conclusion in enumerate(
        conclusions,
        start=1
    ):

        print(f"{i}. {conclusion}")

    section("14. PODSUMOWANIE")

    print(f"Autorzy: {authors_count}")
    print(f"Ksiazki: {books_count}")

    print(
        f"Lazy Loading: "
        f"{lazy['mean_time'] * 1000:.4f} ms"
    )

    print(
        f"Eager Loading: "
        f"{eager['mean_time'] * 1000:.4f} ms"
    )

    print(
        f"Redukcja zapytan: "
        f"{query_reduction:.2f}%"
    )

    print(
        f"Redukcja czasu: "
        f"{time_reduction:.2f}%"
    )

    print(
        f"Zaliczone testy: "
        f"{passed_count}/{len(tests)}"
    )

    print("\nWszystkie testy zakonczone pomyslnie.")
    print("Zadanie 10 wykonane poprawnie.")


if __name__ == "__main__":
    main()
