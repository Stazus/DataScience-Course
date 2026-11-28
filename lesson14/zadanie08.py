# Lekcja 14 - Zadanie 8
# Pandas + ORM

from decimal import Decimal

import pandas as pd

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    inspect
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from zadanie02 import (
    Base,
    Student,
    engine,
    DATABASE_PATH
)

from zadanie07 import Teacher, Course


Session = sessionmaker(bind=engine)


# MODEL PRODUCT

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(150),
        nullable=False,
        unique=True
    )

    category = Column(
        String(100),
        nullable=False
    )

    price = Column(
        Numeric(10, 2),
        nullable=False
    )

    def __repr__(self):

        return (
            f"Product(id={self.id}, "
            f"name='{self.name}', "
            f"category='{self.category}', "
            f"price={self.price})"
        )


# DATASET

PRODUCTS_DATA = [
    ("Laptop", "Electronics", "3499.99"),
    ("Monitor", "Electronics", "899.99"),
    ("Keyboard", "Electronics", "199.99"),
    ("Smartphone", "Electronics", "2499.99"),
    ("Desk", "Furniture", "799.00"),
    ("Chair", "Furniture", "449.00"),
    ("Bookshelf", "Furniture", "599.00"),
    ("Python Programming", "Books", "129.90"),
    ("Data Science Handbook", "Books", "159.90"),
    ("SQL Fundamentals", "Books", "89.90")
]


def section(title):

    print(f"\n{title}")
    print("-" * 80)


def normalize_dataframe(df):

    result = df[
        ["name", "category", "price"]
    ].copy()

    result["price"] = result["price"].map(
        lambda value: Decimal(str(value)).quantize(
            Decimal("0.01")
        )
    )

    return (
        result
        .sort_values("name")
        .reset_index(drop=True)
    )


def snapshot_existing_data(session):

    return {

        "students": [
            (s.id, s.name, s.age, s.email)
            for s in session.query(Student)
            .order_by(Student.id).all()
        ],

        "teachers": [
            (t.id, t.name)
            for t in session.query(Teacher)
            .order_by(Teacher.id).all()
        ],

        "courses": [
            (c.id, c.title, c.teacher_id)
            for c in session.query(Course)
            .order_by(Course.id).all()
        ]
    }


def main():

    print("=" * 80)
    print("ZADANIE 8 - PANDAS + ORM")
    print("=" * 80)

    try:

        section("1. KONFIGURACJA BAZY DANYCH")

        print(f"Baza danych: {DATABASE_PATH}")
        print(f"Dialekt: {engine.dialect.name}")
        print(f"Pandas: {pd.__version__}")

        section("2. DEFINICJA MODELU PRODUCT")

        print(f"Model: {Product.__name__}")
        print(f"Tabela: {Product.__tablename__}")

        for column in Product.__table__.columns:

            print(
                f"Kolumna: {column.name:<12}"
                f"Typ: {str(column.type):<18}"
                f"PK: {column.primary_key}"
            )

        section("3. TWORZENIE TABELI PRODUCTS")

        Base.metadata.create_all(engine)

        inspector = inspect(engine)

        tables = inspector.get_table_names()

        print(f"Tabele w bazie: {tables}")

        section("4. UTWORZENIE DATAFRAME")

        df = pd.DataFrame(
            PRODUCTS_DATA,
            columns=["name", "category", "price"]
        )

        df["price"] = df["price"].map(Decimal)

        print(df.to_string(index=False))

        print(f"\nLiczba wierszy: {len(df)}")
        print(f"Liczba kolumn: {len(df.columns)}")
        print(f"Rozmiar DataFrame: {df.shape}")

        print("\nTypy danych:")

        print(df.dtypes)

        section("5. ANALIZA DATAFRAME")

        print("Liczba produktow wedlug kategorii:")

        category_counts = (
            df["category"]
            .value_counts()
            .sort_index()
        )

        print(category_counts.to_string())

        print(
            f"\nLaczna wartosc: "
            f"{df['price'].sum():.2f} PLN"
        )

        print(
            f"Srednia cena: "
            f"{df['price'].mean():.2f} PLN"
        )

        print(
            f"Najtanszy produkt: "
            f"{df['price'].min():.2f} PLN"
        )

        print(
            f"Najdrozszy produkt: "
            f"{df['price'].max():.2f} PLN"
        )

        section("6. KONWERSJA DATAFRAME NA SLOWNIKI")

        records = df.to_dict(orient="records")

        for record in records:

            print(record)

        print(
            f"\nLiczba slownikow: "
            f"{len(records)}"
        )

        section("7. KONWERSJA NA OBIEKTY ORM")

        products = [
            Product(**record)
            for record in records
        ]

        for product in products:

            print(product)

        print(
            f"\nLiczba obiektow Product: "
            f"{len(products)}"
        )

        with Session() as session:

            section("8. STAN BAZY PRZED DODANIEM")

            existing_data_before = (
                snapshot_existing_data(session)
            )

            products_before = (
                session.query(Product).count()
            )

            print(
                f"Produkty przed: "
                f"{products_before}"
            )

            existing_names = {
                name
                for (name,) in session.query(
                    Product.name
                ).all()
            }

            new_products = [
                product
                for product in products
                if product.name not in existing_names
            ]

            section("9. DODAWANIE OBIEKTOW - ADD_ALL")

            session.add_all(new_products)

            added_count = len(new_products)

            print(
                f"Nowe obiekty w sesji: "
                f"{len(session.new)}"
            )

            print(
                f"Pominiete istniejace produkty: "
                f"{len(products) - added_count}"
            )

            section("10. FLUSH I WERYFIKACJA")

            session.flush()

            for product in new_products:

                print(product)

            assert all(
                product.id is not None
                for product in new_products
            )

            # Weryfikacja danych przed zatwierdzeniem

            pending_products = (
                session.query(Product)
                .filter(
                    Product.name.in_(
                        df["name"].tolist()
                    )
                )
                .all()
            )

            pending_df = pd.DataFrame(
                [
                    {
                        "name": product.name,
                        "category": product.category,
                        "price": product.price
                    }
                    for product in pending_products
                ],
                columns=["name", "category", "price"]
            )

            pd.testing.assert_frame_equal(
                normalize_dataframe(df),
                normalize_dataframe(pending_df)
            )

            section("11. COMMIT TRANSAKCJI")

            session.commit()

            print(
                "session.commit() wykonany poprawnie."
            )

            print(
                f"Dodano produktow: {added_count}"
            )

        with Session() as session:

            section("12. ODCZYT DANYCH W NOWEJ SESJI")

            saved_products = (
                session.query(Product)
                .filter(
                    Product.name.in_(
                        df["name"].tolist()
                    )
                )
                .order_by(Product.id)
                .all()
            )

            for product in saved_products:

                print(product)

            products_after = (
                session.query(Product).count()
            )

            print(
                f"\nOdczytano produktow: "
                f"{len(saved_products)}"
            )

            section("13. KONWERSJA ORM NA DATAFRAME")

            df_from_db = pd.DataFrame(
                [
                    {
                        "name": product.name,
                        "category": product.category,
                        "price": product.price
                    }
                    for product in saved_products
                ],
                columns=["name", "category", "price"]
            )

            print(
                df_from_db.to_string(index=False)
            )

            print(
                f"\nRozmiar DataFrame z bazy: "
                f"{df_from_db.shape}"
            )

            section("14. POROWNANIE DATAFRAME")

            original_df = normalize_dataframe(df)

            database_df = normalize_dataframe(
                df_from_db
            )

            print("Oryginalny DataFrame:")

            print(
                original_df.to_string(index=False)
            )

            print("\nDataFrame odczytany z bazy:")

            print(
                database_df.to_string(index=False)
            )

            frames_equal = original_df.equals(
                database_df
            )

            print(
                f"\nCzy DataFrame sa identyczne: "
                f"{frames_equal}"
            )

            pd.testing.assert_frame_equal(
                original_df,
                database_df
            )

            print(
                "assert_frame_equal(): OK"
            )

            section("15. STATYSTYKI WEDLUG KATEGORII")

            statistics = (
                df_from_db
                .groupby("category")
                .agg(
                    products=("name", "count"),
                    total_price=("price", "sum"),
                    min_price=("price", "min"),
                    max_price=("price", "max")
                )
                .reset_index()
            )

            print(
                statistics.to_string(index=False)
            )

            original_total = df["price"].sum()

            database_total = (
                df_from_db["price"].sum()
            )

            print(
                f"\nWartosc oryginalna: "
                f"{original_total:.2f} PLN"
            )

            print(
                f"Wartosc z bazy: "
                f"{database_total:.2f} PLN"
            )

            section("16. SPRAWDZENIE STRUKTURY TABELI")

            columns = inspector.get_columns(
                "products"
            )

            for column in columns:

                print(
                    f"Nazwa: {column['name']:<12}"
                    f"Typ: {str(column['type']):<18}"
                    f"Nullable: {column['nullable']}"
                )

            existing_data_after = (
                snapshot_existing_data(session)
            )

            section("17. AUTOMATYCZNE TESTY")

            tests = {

                "Plik test.db istnieje":
                    DATABASE_PATH.is_file(),

                "Model Product dziedziczy po Base":
                    issubclass(Product, Base),

                "Tabela products istnieje":
                    "products" in tables,

                "Tabela students nadal istnieje":
                    "students" in tables,

                "Tabela teachers nadal istnieje":
                    "teachers" in tables,

                "Tabela courses nadal istnieje":
                    "courses" in tables,

                "Tabela products ma 4 kolumny":
                    len(columns) == 4,

                "Poprawne nazwy kolumn tabeli":
                    {c["name"] for c in columns}
                    == {"id", "name", "category", "price"},

                "Poprawny klucz glowny":
                    inspector.get_pk_constraint(
                        "products"
                    )["constrained_columns"] == ["id"],

                "DataFrame zawiera 10 produktow":
                    len(df) == 10,

                "DataFrame zawiera 3 kolumny":
                    len(df.columns) == 3,

                "Poprawne nazwy kolumn DataFrame":
                    list(df.columns)
                    == ["name", "category", "price"],

                "DataFrame zawiera 3 kategorie":
                    df["category"].nunique() == 3,

                "Poprawne kategorie":
                    set(df["category"])
                    == {"Electronics", "Furniture", "Books"},

                "Electronics zawiera 4 produkty":
                    category_counts["Electronics"] == 4,

                "Furniture zawiera 3 produkty":
                    category_counts["Furniture"] == 3,

                "Books zawiera 3 produkty":
                    category_counts["Books"] == 3,

                "Nazwy produktow sa unikalne":
                    df["name"].is_unique,

                "Brak brakujacych wartosci":
                    not df.isna().any().any(),

                "Wszystkie ceny sa dodatnie":
                    bool((df["price"] > 0).all()),

                "Utworzono 10 slownikow":
                    len(records) == 10,

                "Utworzono 10 obiektow ORM":
                    len(products) == 10,

                "Wszystkie obiekty sa typu Product":
                    all(
                        isinstance(product, Product)
                        for product in products
                    ),

                "Poprawna liczba dodanych rekordow":
                    products_after - products_before
                    == added_count,

                "Odczytano 10 produktow z bazy":
                    len(saved_products) == 10,

                "Wszystkie zapisane produkty maja ID":
                    all(
                        product.id is not None
                        for product in saved_products
                    ),

                "Identyfikatory sa unikalne":
                    len({
                        product.id
                        for product in saved_products
                    }) == 10,

                "Ceny z bazy maja typ Decimal":
                    all(
                        isinstance(product.price, Decimal)
                        for product in saved_products
                    ),

                "DataFrame z bazy ma rozmiar 10 x 3":
                    df_from_db.shape == (10, 3),

                "DataFrame sa identyczne":
                    frames_equal,

                "Laczne wartosci sa identyczne":
                    original_total == database_total,

                "Laczna wartosc wynosi 9326.66 PLN":
                    database_total == Decimal("9326.66"),

                "Dane studentow bez zmian":
                    existing_data_before["students"]
                    == existing_data_after["students"],

                "Dane nauczycieli bez zmian":
                    existing_data_before["teachers"]
                    == existing_data_after["teachers"],

                "Dane kursow bez zmian":
                    existing_data_before["courses"]
                    == existing_data_after["courses"],

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

        section("18. PODSUMOWANIE")

        print("Model: Product")
        print("Tabela: products")
        print("Technologie: Pandas + SQLAlchemy ORM")
        print("Liczba produktow: 10")
        print("Liczba kategorii: 3")

        print(
            f"Laczna wartosc: "
            f"{database_total:.2f} PLN"
        )

        print("DataFrame przekonwertowano na obiekty ORM.")
        print("Wykorzystano session.add_all().")
        print("Wykonano session.commit().")
        print("Odczytano dane w nowej sesji.")
        print("Porownano oba DataFrame.")
        print("Dane w pozostalych tabelach bez zmian.")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 8 wykonane poprawnie.")

    except SQLAlchemyError as error:

        print(f"Blad SQLAlchemy: {error}")

        raise

    finally:

        engine.dispose()


if __name__ == "__main__":
    main()
