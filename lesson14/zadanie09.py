# Lekcja 14 - Zadanie 9
# Relacja Many-to-Many z danymi

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    inspect,
    select,
    func
)

from sqlalchemy.orm import (
    relationship,
    sessionmaker
)

from sqlalchemy.exc import SQLAlchemyError

from zadanie02 import Base, Student, engine, DATABASE_PATH
from zadanie07 import Teacher, Course
from zadanie08 import Product


Session = sessionmaker(bind=engine)


# TABELA ASOCJACYJNA

movie_actor = Table(
    "movie_actor",
    Base.metadata,

    Column(
        "movie_id",
        Integer,
        ForeignKey("movies.id"),
        primary_key=True
    ),

    Column(
        "actor_id",
        Integer,
        ForeignKey("actors.id"),
        primary_key=True
    )
)


# MODEL MOVIE

class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)

    title = Column(
        String(200),
        nullable=False,
        unique=True
    )

    year = Column(
        Integer,
        nullable=False
    )

    actors = relationship(
        "Actor",
        secondary=movie_actor,
        back_populates="movies"
    )

    def __repr__(self):

        return (
            f"Movie(id={self.id}, "
            f"title='{self.title}', "
            f"year={self.year})"
        )


# MODEL ACTOR

class Actor(Base):

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(150),
        nullable=False,
        unique=True
    )

    movies = relationship(
        "Movie",
        secondary=movie_actor,
        back_populates="actors"
    )

    def __repr__(self):

        return (
            f"Actor(id={self.id}, "
            f"name='{self.name}')"
        )


# DATASET

ACTORS_DATA = [
    "Leonardo DiCaprio",
    "Tom Hardy",
    "Cillian Murphy",
    "Michael Caine",
    "Joseph Gordon-Levitt",
    "Christian Bale",
    "Matthew McConaughey"
]


MOVIES_DATA = [
    (
        "Inception",
        2010,
        [
            "Leonardo DiCaprio",
            "Tom Hardy",
            "Cillian Murphy",
            "Michael Caine",
            "Joseph Gordon-Levitt"
        ]
    ),

    (
        "Batman Begins",
        2005,
        [
            "Christian Bale",
            "Cillian Murphy",
            "Michael Caine"
        ]
    ),

    (
        "The Dark Knight Rises",
        2012,
        [
            "Christian Bale",
            "Tom Hardy",
            "Cillian Murphy",
            "Michael Caine",
            "Joseph Gordon-Levitt"
        ]
    ),

    (
        "Interstellar",
        2014,
        [
            "Matthew McConaughey",
            "Michael Caine"
        ]
    ),

    (
        "Dunkirk",
        2017,
        [
            "Tom Hardy",
            "Cillian Murphy"
        ]
    )
]


def section(title):

    print(f"\n{title}")
    print("-" * 80)


def snapshot_existing_data(session):

    models = [
        Student,
        Teacher,
        Course,
        Product
    ]

    return {
        model.__tablename__: [
            tuple(row)
            for row in session.execute(
                select(model.__table__)
                .order_by(model.__table__.c.id)
            ).all()
        ]
        for model in models
    }


def count_relations(session):

    return session.scalar(
        select(func.count())
        .select_from(movie_actor)
    )


def main():

    print("=" * 80)
    print("ZADANIE 9 - RELACJA MANY-TO-MANY")
    print("=" * 80)

    try:

        section("1. KONFIGURACJA BAZY DANYCH")

        print(f"Baza danych: {DATABASE_PATH}")
        print(f"Dialekt: {engine.dialect.name}")

        section("2. DEFINICJA MODELI")

        print(f"Model: {Movie.__name__}")
        print(f"Tabela: {Movie.__tablename__}")

        print(f"Model: {Actor.__name__}")
        print(f"Tabela: {Actor.__tablename__}")

        print(f"Tabela asocjacyjna: {movie_actor.name}")

        section("3. TWORZENIE TABEL")

        Base.metadata.create_all(engine)

        inspector = inspect(engine)

        tables = inspector.get_table_names()

        print(f"Tabele w bazie: {tables}")

        section("4. STRUKTURA TABELI ASOCJACYJNEJ")

        association_columns = inspector.get_columns(
            "movie_actor"
        )

        for column in association_columns:

            print(
                f"Kolumna: {column['name']:<15}"
                f"Typ: {column['type']}"
            )

        primary_key = inspector.get_pk_constraint(
            "movie_actor"
        )

        foreign_keys = inspector.get_foreign_keys(
            "movie_actor"
        )

        print(f"\nKlucz glowny: {primary_key}")

        print("\nKlucze obce:")

        for foreign_key in foreign_keys:

            print(
                f"{foreign_key['constrained_columns']} "
                f"-> {foreign_key['referred_table']}"
                f"{foreign_key['referred_columns']}"
            )

        section("5. STAN BAZY PRZED DODANIEM")

        with Session() as session:

            existing_data_before = (
                snapshot_existing_data(session)
            )

            movies_before = session.query(Movie).count()
            actors_before = session.query(Actor).count()
            relations_before = count_relations(session)

            print(f"Filmy: {movies_before}")
            print(f"Aktorzy: {actors_before}")
            print(f"Powiazania: {relations_before}")

            section("6. TWORZENIE OBIEKTOW ACTOR")

            actors = {}

            new_actors = []

            for name in ACTORS_DATA:

                actor = (
                    session.query(Actor)
                    .filter(Actor.name == name)
                    .first()
                )

                if actor is None:

                    actor = Actor(name=name)

                    new_actors.append(actor)

                actors[name] = actor

                print(actor)

            session.add_all(new_actors)

            print(f"\nAktorzy: {len(actors)}")
            print(f"Nowi aktorzy: {len(new_actors)}")

            section("7. TWORZENIE OBIEKTOW MOVIE")

            movies = {}

            new_movies = []

            for title, year, cast in MOVIES_DATA:

                movie = (
                    session.query(Movie)
                    .filter(Movie.title == title)
                    .first()
                )

                if movie is None:

                    movie = Movie(
                        title=title,
                        year=year
                    )

                    new_movies.append(movie)

                movies[title] = movie

                print(movie)

            session.add_all(new_movies)

            print(f"\nFilmy: {len(movies)}")
            print(f"Nowe filmy: {len(new_movies)}")

            section("8. TWORZENIE RELACJI MANY-TO-MANY")

            added_relations = 0

            for title, year, cast in MOVIES_DATA:

                movie = movies[title]

                print(f"\nFilm: {title}")

                for actor_name in cast:

                    actor = actors[actor_name]

                    if actor not in movie.actors:

                        movie.actors.append(actor)

                        added_relations += 1

                        print(f"  Dodano: {actor.name}")

                    else:

                        print(
                            f"  Istnieje: {actor.name}"
                        )

            print(
                f"\nNowe powiazania: "
                f"{added_relations}"
            )

            section("9. FLUSH I WERYFIKACJA")

            session.flush()

            print("session.flush() wykonany poprawnie.")

            print(
                f"Liczba powiazan: "
                f"{count_relations(session)}"
            )

            for title, year, cast in MOVIES_DATA:

                movie = movies[title]

                assert movie.year == year

                assert {
                    actor.name
                    for actor in movie.actors
                } == set(cast)

            section("10. COMMIT TRANSAKCJI")

            session.commit()

            print("session.commit() wykonany poprawnie.")

        with Session() as session:

            section("11. ODCZYT DANYCH W NOWEJ SESJI")

            saved_movies = (
                session.query(Movie)
                .order_by(Movie.year, Movie.title)
                .all()
            )

            saved_actors = (
                session.query(Actor)
                .order_by(Actor.name)
                .all()
            )

            movies_after = len(saved_movies)
            actors_after = len(saved_actors)
            relations_after = count_relations(session)

            print(f"Filmy: {movies_after}")
            print(f"Aktorzy: {actors_after}")
            print(f"Powiazania: {relations_after}")

            section("12. WSZYSTKIE FILMY I ICH AKTORZY")

            for movie in saved_movies:

                print(
                    f"\n{movie.title} ({movie.year})"
                )

                print(
                    f"Liczba aktorow: "
                    f"{len(movie.actors)}"
                )

                for actor in sorted(
                    movie.actors,
                    key=lambda actor: actor.name
                ):

                    print(f"  - {actor.name}")

            section("13. WSZYSCY AKTORZY I ICH FILMY")

            for actor in saved_actors:

                print(f"\n{actor.name}")

                print(
                    f"Liczba filmow: "
                    f"{len(actor.movies)}"
                )

                for movie in sorted(
                    actor.movies,
                    key=lambda movie: movie.year
                ):

                    print(
                        f"  - {movie.title} "
                        f"({movie.year})"
                    )

            section("14. ZAPYTANIE - FILMY AKTORA X")

            actor_x = (
                session.query(Actor)
                .filter(
                    Actor.name == "Tom Hardy"
                )
                .first()
            )

            assert actor_x is not None

            print(f"Aktor: {actor_x.name}")

            actor_x_movies = {
                movie.title
                for movie in actor_x.movies
            }

            for title in sorted(actor_x_movies):

                print(f"  - {title}")

            print(
                f"Liczba filmow: "
                f"{len(actor_x_movies)}"
            )

            section("15. ZAPYTANIE - AKTORZY FILMU Y")

            movie_y = (
                session.query(Movie)
                .filter(
                    Movie.title == "Inception"
                )
                .first()
            )

            assert movie_y is not None

            print(f"Film: {movie_y.title}")

            movie_y_actors = {
                actor.name
                for actor in movie_y.actors
            }

            for name in sorted(movie_y_actors):

                print(f"  - {name}")

            print(
                f"Liczba aktorow: "
                f"{len(movie_y_actors)}"
            )

            section("16. ODCZYT TABELI ASOCJACYJNEJ")

            association_rows = session.execute(
                select(movie_actor)
                .order_by(
                    movie_actor.c.movie_id,
                    movie_actor.c.actor_id
                )
            ).all()

            print(f"{'MOVIE_ID':<15}{'ACTOR_ID':<15}")
            print("-" * 30)

            for row in association_rows:

                print(
                    f"{row.movie_id:<15}"
                    f"{row.actor_id:<15}"
                )

            section("17. STATYSTYKI RELACJI")

            print("Liczba filmow wedlug aktorow:")

            for actor in sorted(
                saved_actors,
                key=lambda actor: (
                    -len(actor.movies),
                    actor.name
                )
            ):

                count = len(actor.movies)

                print(
                    f"{actor.name:<25}"
                    f"{count} "
                    f"{'#' * count}"
                )

            print("\nLiczba aktorow wedlug filmow:")

            for movie in saved_movies:

                count = len(movie.actors)

                print(
                    f"{movie.title:<25}"
                    f"{count} "
                    f"{'#' * count}"
                )

            print(
                f"\nSrednia liczba aktorow na film: "
                f"{relations_after / movies_after:.2f}"
            )

            print(
                f"Srednia liczba filmow na aktora: "
                f"{relations_after / actors_after:.2f}"
            )

            section("18. WERYFIKACJA RELACJI")

            expected_casts = {
                title: set(cast)
                for title, year, cast in MOVIES_DATA
            }

            actual_casts = {
                movie.title: {
                    actor.name
                    for actor in movie.actors
                }
                for movie in saved_movies
            }

            expected_actor_movies = {
                name: {
                    title
                    for title, year, cast in MOVIES_DATA
                    if name in cast
                }
                for name in ACTORS_DATA
            }

            actual_actor_movies = {
                actor.name: {
                    movie.title
                    for movie in actor.movies
                }
                for actor in saved_actors
            }

            existing_data_after = (
                snapshot_existing_data(session)
            )

            print(
                f"Obsady filmow poprawne: "
                f"{actual_casts == expected_casts}"
            )

            print(
                f"Filmy aktorow poprawne: "
                f"{actual_actor_movies == expected_actor_movies}"
            )

            section("19. AUTOMATYCZNE TESTY")

            tests = {

                "Plik test.db istnieje":
                    DATABASE_PATH.is_file(),

                "Movie dziedziczy po Base":
                    issubclass(Movie, Base),

                "Actor dziedziczy po Base":
                    issubclass(Actor, Base),

                "Tabela movies istnieje":
                    "movies" in tables,

                "Tabela actors istnieje":
                    "actors" in tables,

                "Tabela movie_actor istnieje":
                    "movie_actor" in tables,

                "Wszystkie 7 tabel istnieje":
                    {
                        "students",
                        "teachers",
                        "courses",
                        "products",
                        "movies",
                        "actors",
                        "movie_actor"
                    }.issubset(tables),

                "Tabela asocjacyjna ma 2 kolumny":
                    len(association_columns) == 2,

                "Poprawne kolumny tabeli asocjacyjnej":
                    {
                        column["name"]
                        for column in association_columns
                    } == {"movie_id", "actor_id"},

                "Zlozony klucz glowny":
                    set(
                        primary_key["constrained_columns"]
                    ) == {"movie_id", "actor_id"},

                "Dwa klucze obce":
                    len(foreign_keys) == 2,

                "Poprawne tabele kluczy obcych":
                    {
                        fk["referred_table"]
                        for fk in foreign_keys
                    } == {"movies", "actors"},

                "Poprawne kolumny kluczy obcych":
                    {
                        (
                            tuple(fk["constrained_columns"]),
                            fk["referred_table"],
                            tuple(fk["referred_columns"])
                        )
                        for fk in foreign_keys
                    } == {
                        (("movie_id",), "movies", ("id",)),
                        (("actor_id",), "actors", ("id",))
                    },

                "Relacja Movie.actors Many-to-Many":
                    inspect(Movie).relationships[
                        "actors"
                    ].direction.name == "MANYTOMANY",

                "Relacja Actor.movies Many-to-Many":
                    inspect(Actor).relationships[
                        "movies"
                    ].direction.name == "MANYTOMANY",

                "Movie.actors uzywa tabeli asocjacyjnej":
                    inspect(Movie).relationships[
                        "actors"
                    ].secondary is movie_actor,

                "Actor.movies uzywa tabeli asocjacyjnej":
                    inspect(Actor).relationships[
                        "movies"
                    ].secondary is movie_actor,

                "Zapisano 5 filmow":
                    movies_after == 5,

                "Zapisano 7 aktorow":
                    actors_after == 7,

                "Zapisano 17 powiazan":
                    relations_after == 17,

                "Poprawne tytuly filmow":
                    set(actual_casts) == set(expected_casts),

                "Poprawne nazwiska aktorow":
                    set(actual_actor_movies)
                    == set(ACTORS_DATA),

                "Poprawne lata filmow":
                    {
                        movie.title: movie.year
                        for movie in saved_movies
                    } == {
                        title: year
                        for title, year, cast in MOVIES_DATA
                    },

                "Wszystkie filmy maja aktorow":
                    all(
                        len(movie.actors) > 0
                        for movie in saved_movies
                    ),

                "Wszyscy aktorzy maja filmy":
                    all(
                        len(actor.movies) > 0
                        for actor in saved_actors
                    ),

                "Wszystkie filmy maja ID":
                    all(
                        movie.id is not None
                        for movie in saved_movies
                    ),

                "Wszyscy aktorzy maja ID":
                    all(
                        actor.id is not None
                        for actor in saved_actors
                    ),

                "Brak duplikatow powiazan":
                    len({
                        (row.movie_id, row.actor_id)
                        for row in association_rows
                    }) == relations_after,

                "Wszystkie obsady sa poprawne":
                    actual_casts == expected_casts,

                "Wszystkie filmy aktorow sa poprawne":
                    actual_actor_movies
                    == expected_actor_movies,

                "Tom Hardy ma 3 filmy":
                    len(actor_x_movies) == 3,

                "Poprawne filmy Toma Hardy":
                    actor_x_movies == {
                        "Inception",
                        "The Dark Knight Rises",
                        "Dunkirk"
                    },

                "Inception ma 5 wybranych aktorow":
                    len(movie_y_actors) == 5,

                "Poprawni aktorzy filmu Inception":
                    movie_y_actors
                    == expected_casts["Inception"],

                "Leonardo DiCaprio ma 1 film":
                    len(
                        actual_actor_movies[
                            "Leonardo DiCaprio"
                        ]
                    ) == 1,

                "Michael Caine ma 4 filmy":
                    len(
                        actual_actor_movies[
                            "Michael Caine"
                        ]
                    ) == 4,

                "Cillian Murphy ma 4 filmy":
                    len(
                        actual_actor_movies[
                            "Cillian Murphy"
                        ]
                    ) == 4,

                "Suma relacji po stronie filmow":
                    sum(
                        len(movie.actors)
                        for movie in saved_movies
                    ) == relations_after,

                "Suma relacji po stronie aktorow":
                    sum(
                        len(actor.movies)
                        for actor in saved_actors
                    ) == relations_after,

                "Poprawna liczba nowych filmow":
                    movies_after - movies_before
                    == len(new_movies),

                "Poprawna liczba nowych aktorow":
                    actors_after - actors_before
                    == len(new_actors),

                "Poprawna liczba nowych powiazan":
                    relations_after - relations_before
                    == added_relations,

                "Dane studentow bez zmian":
                    existing_data_before["students"]
                    == existing_data_after["students"],

                "Dane nauczycieli bez zmian":
                    existing_data_before["teachers"]
                    == existing_data_after["teachers"],

                "Dane kursow bez zmian":
                    existing_data_before["courses"]
                    == existing_data_after["courses"],

                "Dane produktow bez zmian":
                    existing_data_before["products"]
                    == existing_data_after["products"],

                "Brak nowych obiektow w sesji":
                    len(session.new) == 0,

                "Brak zmodyfikowanych obiektow":
                    len(session.dirty) == 0,

                "Brak obiektow do usuniecia":
                    len(session.deleted) == 0
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

        section("20. PODSUMOWANIE")

        print("Modele: Movie, Actor")
        print("Relacja: Many-to-Many")
        print("Tabela asocjacyjna: movie_actor")
        print(f"Liczba filmow: {movies_after}")
        print(f"Liczba aktorow: {actors_after}")
        print(f"Liczba powiazan: {relations_after}")
        print(f"Liczba tabel w bazie: {len(tables)}")

        print("Wykorzystano ForeignKey.")
        print("Wykorzystano relationship().")
        print("Wykorzystano secondary.")
        print("Wykorzystano back_populates.")
        print("Wykorzystano session.add_all().")
        print("Wykonano session.commit().")
        print("Zweryfikowano relacje w obu kierunkach.")
        print("Dane z poprzednich zadan bez zmian.")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 9 wykonane poprawnie.")

    except SQLAlchemyError as error:

        print(f"Blad SQLAlchemy: {error}")

        raise

    finally:

        engine.dispose()


if __name__ == "__main__":
    main()
