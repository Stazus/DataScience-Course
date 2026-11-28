# Lekcja 14 - Zadanie 13
# E-commerce Database Design

import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from datetime import datetime, timezone, timedelta
from random import Random
from sqlalchemy import func

from sqlalchemy import (
    create_engine,
    event,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Numeric,
    ForeignKey,
    Table,
    CheckConstraint,
    inspect
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    validates
)


DATABASE_PATH = (
    Path(__file__).resolve().parent / "ecommerce.db"
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()








ORDER_STATUSES = (
    "pending",
    "paid",
    "shipped",
    "completed",
    "cancelled"
)


def validate_name(value, max_length):
    if not isinstance(value, str):
        raise ValueError("Nazwa musi byc tekstem.")

    value = value.strip()

    if not value:
        raise ValueError("Nazwa nie moze byc pusta.")

    if len(value) > max_length:
        raise ValueError("Nazwa jest za dluga.")

    return value


def validate_money(value):
    if isinstance(value, bool):
        raise ValueError("Niepoprawna cena.")

    try:
        value = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Niepoprawna cena.")

    if not value.is_finite():
        raise ValueError("Cena musi byc skonczona.")

    if value <= 0:
        raise ValueError("Cena musi byc wieksza od zera.")

    if value > Decimal("99999999.99"):
        raise ValueError("Cena przekracza dozwolony zakres.")

    rounded = value.quantize(Decimal("0.01"))

    if value != rounded:
        raise ValueError(
            "Cena moze miec maksymalnie 2 miejsca po przecinku."
        )

    return rounded


def validate_integer(value, minimum):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("Wartosc musi byc liczba calkowita.")

    if value < minimum:
        raise ValueError(
            f"Wartosc musi wynosic co najmniej {minimum}."
        )

    return value


product_categories = Table(
    "product_categories",
    Base.metadata,

    Column(
        "product_id",
        Integer,
        ForeignKey("products.id"),
        primary_key=True
    ),

    Column(
        "category_id",
        Integer,
        ForeignKey("categories.id"),
        primary_key=True,
        index=True
    )
)


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) BETWEEN 1 AND 100",
            name="ck_users_name"
        ),
        CheckConstraint(
            "length(email) BETWEEN 3 AND 150",
            name="ck_users_email_length"
        ),
        CheckConstraint(
            "email = lower(trim(email))",
            name="ck_users_email_normalized"
        ),
    )



    orders = relationship(
        "Order",
        back_populates="user"
    )

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=False,
        unique=True
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )


    @validates("name")
    def validate_user_name(self, key, value):
        return validate_name(value, 100)

    @validates("email")
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Email musi byc tekstem.")

        value = value.strip().lower()

        if len(value) > 150:
            raise ValueError("Email jest za dlugi.")

        if not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            value
        ):
            raise ValueError("Niepoprawny format email.")

        return value

    def __repr__(self):
        return (
            f"User(id={self.id}, "
            f"name={self.name!r}, "
            f"email={self.email!r})"
        )




class Category(Base):
    __tablename__ = "categories"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) BETWEEN 1 AND 100",
            name="ck_categories_name"
        ),
    )



    products = relationship(
        "Product",
        secondary=product_categories,
        back_populates="categories"
    )

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False,
        unique=True
    )

    description = Column(
        Text,
        nullable=True
    )


    @validates("name")
    def validate_category_name(self, key, value):
        return validate_name(value, 100)

    def __repr__(self):
        return (
            f"Category(id={self.id}, "
            f"name={self.name!r})"
        )




class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) BETWEEN 1 AND 200",
            name="ck_products_name"
        ),
        CheckConstraint(
            "price > 0 AND price <= 99999999.99",
            name="ck_products_price"
        ),
        CheckConstraint(
            "stock >= 0",
            name="ck_products_stock"
        ),
    )



    categories = relationship(
        "Category",
        secondary=product_categories,
        back_populates="products"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(200),
        nullable=False
    )

    price = Column(
        Numeric(10, 2),
        nullable=False
    )

    stock = Column(
        Integer,
        nullable=False,
        default=0
    )

    description = Column(
        Text,
        nullable=True
    )


    @validates("name")
    def validate_product_name(self, key, value):
        return validate_name(value, 200)

    @validates("price")
    def validate_price(self, key, value):
        return validate_money(value)

    @validates("stock")
    def validate_stock(self, key, value):
        return validate_integer(value, 0)

    def __repr__(self):
        return (
            f"Product(id={self.id}, "
            f"name={self.name!r}, "
            f"price={self.price}, "
            f"stock={self.stock})"
        )




class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'paid', 'shipped', "
            "'completed', 'cancelled')",
            name="ck_orders_status"
        ),
    )



    user = relationship(
        "User",
        back_populates="orders"
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    order_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    status = Column(
        String(20),
        nullable=False,
        default="pending"
    )


    @validates("status")
    def validate_status(self, key, value):
        if value not in ORDER_STATUSES:
            raise ValueError("Niepoprawny status zamowienia.")

        return value

    def __repr__(self):
        return (
            f"Order(id={self.id}, "
            f"user_id={self.user_id}, "
            f"status={self.status!r})"
        )




class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_items_quantity"
        ),
        CheckConstraint(
            "unit_price > 0 AND unit_price <= 99999999.99",
            name="ck_order_items_unit_price"
        ),
    )



    order = relationship(
        "Order",
        back_populates="items"
    )

    product = relationship(
        "Product",
        back_populates="order_items"
    )

    id = Column(
        Integer,
        primary_key=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    unit_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    @property
    def subtotal(self):
        return self.quantity * self.unit_price


    @validates("quantity")
    def validate_quantity(self, key, value):
        return validate_integer(value, 1)

    @validates("unit_price")
    def validate_unit_price(self, key, value):
        return validate_money(value)

    def __repr__(self):
        return (
            f"OrderItem(id={self.id}, "
            f"order_id={self.order_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"unit_price={self.unit_price})"
        )




def create_database():
    Base.metadata.create_all(bind=engine)

    print("\nSchemat bazy danych utworzony pomyslnie.")


def verify_database_schema():
    inspector = inspect(engine)

    expected_tables = set(Base.metadata.tables.keys())
    actual_tables = set(inspector.get_table_names())

    if actual_tables != expected_tables:
        raise RuntimeError(
            f"Niepoprawny zestaw tabel: {actual_tables}"
        )

    for table_name, table in Base.metadata.tables.items():
        expected_columns = set(table.columns.keys())

        actual_columns = {
            column["name"]
            for column in inspector.get_columns(table_name)
        }

        if actual_columns != expected_columns:
            raise RuntimeError(
                f"Niepoprawne kolumny tabeli {table_name}"
            )

    print("Weryfikacja schematu zakonczona pomyslnie.")

    return True


def show_database_schema():
    inspector = inspect(engine)

    print("\n" + "=" * 70)
    print("SCHEMAT BAZY DANYCH E-COMMERCE")
    print("=" * 70)

    for table_name in sorted(inspector.get_table_names()):
        print(f"\nTabela: {table_name}")
        print("-" * 70)

        for column in inspector.get_columns(table_name):
            print(
                f"  {column['name']:<20} "
                f"{str(column['type']):<20} "
                f"Nullable: {column['nullable']}"
            )

        primary_key = inspector.get_pk_constraint(
            table_name
        )

        print(
            f"  PRIMARY KEY: "
            f"{primary_key['constrained_columns']}"
        )

        for fk in inspector.get_foreign_keys(table_name):
            print(
                f"  FOREIGN KEY: "
                f"{fk['constrained_columns']} -> "
                f"{fk['referred_table']}."
                f"{fk['referred_columns']}"
            )

        for constraint in inspector.get_unique_constraints(
            table_name
        ):
            print(
                f"  UNIQUE: "
                f"{constraint['column_names']}"
            )

        for constraint in inspector.get_check_constraints(
            table_name
        ):
            print(
                f"  CHECK: "
                f"{constraint['name']} - "
                f"{constraint['sqltext']}"
            )

        for index in inspector.get_indexes(table_name):
            print(
                f"  INDEX: "
                f"{index['name']} - "
                f"{index['column_names']}"
            )

    print(
        f"\nLiczba tabel: "
        f"{len(inspector.get_table_names())}"
    )




def get_database_counts(session):
    return {
        "users": session.query(User).count(),
        "categories": session.query(Category).count(),
        "products": session.query(Product).count(),
        "orders": session.query(Order).count(),
        "order_items": session.query(OrderItem).count(),
        "product_categories": (
            session.query(product_categories).count()
        )
    }


def generate_sample_data():
    rng = Random(42)

    expected_counts = {
        "users": 10,
        "categories": 5,
        "products": 20,
        "orders": 30,
        "order_items": 90,
        "product_categories": 28
    }

    with SessionLocal.begin() as session:

        counts = get_database_counts(session)

        if counts == expected_counts:
            print("\nDane przykladowe juz istnieja.")
            return False

        if any(counts.values()):
            raise RuntimeError(
                "Baza zawiera dane o nieoczekiwanej "
                "strukturze. Import przerwany."
            )

        # 1. Kategorie

        categories = [
            Category(
                name="Elektronika",
                description="Sprzet elektroniczny"
            ),
            Category(
                name="Biuro",
                description="Wyposazenie biurowe"
            ),
            Category(
                name="Dom i ogrod",
                description="Produkty do domu i ogrodu"
            ),
            Category(
                name="Sport",
                description="Sprzet sportowy"
            ),
            Category(
                name="Ksiazki",
                description="Literatura i edukacja"
            )
        ]

        session.add_all(categories)

        # 2. Produkty

        product_data = [
            ("Laptop", "3499.99", 50, [0, 1]),
            ("Smartfon", "1899.00", 80, [0]),
            ("Sluchawki bezprzewodowe", "249.90", 150, [0, 3]),
            ("Monitor", "899.00", 60, [0, 1]),
            ("Klawiatura", "149.90", 120, [1, 0]),
            ("Mysz bezprzewodowa", "89.90", 200, [1, 0]),
            ("Drukarka", "599.00", 40, [1, 0]),
            ("Fotel biurowy", "749.00", 35, [1]),
            ("Ekspres do kawy", "1299.00", 30, [2]),
            ("Odkurzacz", "699.00", 45, [2]),
            ("Czajnik elektryczny", "129.90", 100, [2]),
            ("Lampa LED", "79.90", 180, [2, 1]),
            ("Hantle", "199.90", 90, [3]),
            ("Mata treningowa", "69.90", 130, [3]),
            ("Rower treningowy", "1499.00", 25, [3]),
            ("Bidon sportowy", "39.90", 250, [3]),
            ("Python - programowanie", "119.00", 100, [4]),
            ("SQL - bazy danych", "99.00", 120, [4]),
            ("Data Science", "149.00", 80, [4]),
            ("Machine Learning", "169.00", 75, [4, 1])
        ]

        products = []

        for name, price, stock, category_ids in product_data:

            product = Product(
                name=name,
                price=Decimal(price),
                stock=stock,
                description=f"Produkt: {name}"
            )

            product.categories = [
                categories[index]
                for index in category_ids
            ]

            products.append(product)

        session.add_all(products)

        # 3. Uzytkownicy

        user_data = [
            ("Anna Kowalska", "anna.kowalska"),
            ("Piotr Nowak", "piotr.nowak"),
            ("Maria Wisniewska", "maria.wisniewska"),
            ("Tomasz Wojcik", "tomasz.wojcik"),
            ("Katarzyna Kaminska", "katarzyna.kaminska"),
            ("Pawel Lewandowski", "pawel.lewandowski"),
            ("Joanna Zielinska", "joanna.zielinska"),
            ("Michal Szymanski", "michal.szymanski"),
            ("Agnieszka Wozniak", "agnieszka.wozniak"),
            ("Robert Dabrowski", "robert.dabrowski")
        ]

        base_date = datetime(
            2026, 9, 1,
            tzinfo=timezone.utc
        )

        users = []

        for name, email_prefix in user_data:

            user = User(
                name=name,
                email=f"{email_prefix}@example.com",
                created_at=base_date
            )

            users.append(user)

        session.add_all(users)

        # 4. Zamowienia i pozycje zamowien

        statuses = (
            ["completed"] * 18
            + ["paid"] * 5
            + ["shipped"] * 3
            + ["pending"] * 2
            + ["cancelled"] * 2
        )

        rng.shuffle(statuses)

        orders = []

        for index in range(30):

            order = Order(
                user=users[index % len(users)],
                order_date=(
                    base_date
                    + timedelta(days=index * 2)
                ),
                status=statuses[index]
            )

            # Gwarantujemy wykorzystanie wszystkich
            # 20 produktow w zamowieniach.

            first_product = products[
                index % len(products)
            ]

            remaining_products = [
                product
                for product in products
                if product is not first_product
            ]

            selected_products = [
                first_product,
                *rng.sample(remaining_products, 2)
            ]

            for product in selected_products:

                item = OrderItem(
                    product=product,
                    quantity=rng.randint(1, 5),
                    unit_price=product.price
                )

                order.items.append(item)

            orders.append(order)

        session.add_all(orders)

        session.flush()

        actual_counts = get_database_counts(session)

        if actual_counts != expected_counts:
            raise RuntimeError(
                f"Niepoprawna liczba rekordow: "
                f"{actual_counts}"
            )

    print("\nDane przykladowe zapisane pomyslnie.")

    for table_name, count in actual_counts.items():
        print(f"{table_name:<22}: {count}")

    print(
        f"Laczna liczba rekordow: "
        f"{sum(actual_counts.values())}"
    )

    return True




SALES_STATUSES = (
    "completed",
    "paid",
    "shipped"
)


def get_top_products(session, limit=5):

    if (
        isinstance(limit, bool)
        or not isinstance(limit, int)
        or limit <= 0
    ):
        raise ValueError(
            "Limit musi byc dodatnia liczba calkowita."
        )

    units_sold = func.sum(
        OrderItem.quantity
    ).label("units_sold")

    revenue = func.sum(
        OrderItem.quantity * OrderItem.unit_price
    ).label("revenue")

    order_count = func.count(
        func.distinct(OrderItem.order_id)
    ).label("order_count")

    return (
        session.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            units_sold,
            order_count,
            revenue
        )
        .join(
            OrderItem,
            Product.id == OrderItem.product_id
        )
        .join(
            Order,
            Order.id == OrderItem.order_id
        )
        .filter(
            Order.status.in_(SALES_STATUSES)
        )
        .group_by(
            Product.id,
            Product.name
        )
        .order_by(
            units_sold.desc(),
            revenue.desc(),
            Product.id.asc()
        )
        .limit(limit)
        .all()
    )


def get_sales_summary(session):

    result = (
        session.query(
            func.count(
                func.distinct(Order.id)
            ).label("order_count"),

            func.count(
                OrderItem.id
            ).label("item_count"),

            func.coalesce(
                func.sum(OrderItem.quantity),
                0
            ).label("units_sold"),

            func.coalesce(
                func.sum(
                    OrderItem.quantity
                    * OrderItem.unit_price
                ),
                0
            ).label("revenue")
        )
        .select_from(OrderItem)
        .join(
            Order,
            Order.id == OrderItem.order_id
        )
        .filter(
            Order.status.in_(SALES_STATUSES)
        )
        .one()
    )

    return result


def show_top_products_report(limit=5):

    with SessionLocal() as session:

        products = get_top_products(
            session,
            limit=limit
        )

        summary = get_sales_summary(session)

        print("\n" + "=" * 90)
        print(
            f"TOP {limit} NAJLEPIEJ "
            f"SPRZEDAJACYCH SIE PRODUKTOW"
        )
        print("=" * 90)

        print(
            f"{'Lp.':<5}"
            f"{'ID':<5}"
            f"{'Produkt':<30}"
            f"{'Sztuki':>8}"
            f"{'Zamowienia':>13}"
            f"{'Sprzedaz [zl]':>18}"
        )

        print("-" * 90)

        for position, product in enumerate(
            products,
            start=1
        ):

            print(
                f"{position:<5}"
                f"{product.product_id:<5}"
                f"{product.product_name:<30}"
                f"{product.units_sold:>8}"
                f"{product.order_count:>13}"
                f"{product.revenue:>18.2f}"
            )

        print("-" * 90)

        top_units = sum(
            product.units_sold
            for product in products
        )

        top_revenue = sum(
            (product.revenue for product in products),
            Decimal("0.00")
        )

        print(
            f"TOP {limit} - sprzedane sztuki: "
            f"{top_units}"
        )

        print(
            f"TOP {limit} - wartosc sprzedazy: "
            f"{top_revenue:.2f} zl"
        )

        print("\nPODSUMOWANIE SPRZEDAZY")
        print("-" * 90)

        print(
            f"Uwzglednione statusy: "
            f"{', '.join(SALES_STATUSES)}"
        )

        print(
            f"Liczba zamowien: "
            f"{summary.order_count}"
        )

        print(
            f"Liczba pozycji zamowien: "
            f"{summary.item_count}"
        )

        print(
            f"Laczna liczba sprzedanych sztuk: "
            f"{summary.units_sold}"
        )

        print(
            f"Laczna wartosc sprzedazy: "
            f"{summary.revenue:.2f} zl"
        )

        if summary.revenue > 0:

            share = (
                top_revenue
                / summary.revenue
                * 100
            )

            print(
                f"Udzial TOP {limit} w sprzedazy: "
                f"{share:.2f}%"
            )

        print("=" * 90)

        return products


if __name__ == "__main__":
    print("=" * 70)
    print("ZADANIE 13 - E-COMMERCE DATABASE DESIGN")
    print("=" * 70)

    print(f"\nBaza danych: {DATABASE_PATH}")
    print(f"Connection string: {DATABASE_URL}")
    print(f"Dialekt: {engine.dialect.name}")

    with engine.connect() as connection:
        foreign_keys = connection.exec_driver_sql(
            "PRAGMA foreign_keys"
        ).scalar()

        print(f"Klucze obce aktywne: {foreign_keys == 1}")

    print(f"Baza danych istnieje: {DATABASE_PATH.exists()}")

    create_database()
    verify_database_schema()
    show_database_schema()

    generate_sample_data()

    show_top_products_report()

    engine.dispose()

    print("\nKonfiguracja zakonczona pomyslnie.")
