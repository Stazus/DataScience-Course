# Lekcja 13 - Zadanie 9: JOIN 3 tabel

import sqlite3
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Generator liczb losowych
rng = np.random.default_rng(42)


# Utworzenie bazy danych SQLite
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")


# =========================================================
# 1. TWORZENIE TABEL
# =========================================================

cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
    )
""")

cursor.execute("""
    CREATE TABLE order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        price REAL NOT NULL CHECK (price >= 0),
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        FOREIGN KEY (order_id)
            REFERENCES orders(order_id)
    )
""")


# =========================================================
# 2. GENEROWANIE DANYCH
# =========================================================

customers = [
    (1, "Jan Kowalski", "Warszawa"),
    (2, "Anna Nowak", "Krakow"),
    (3, "Piotr Wisniewski", "Gdansk"),
    (4, "Maria Zielinska", "Wroclaw"),
    (5, "Tomasz Wojcik", "Kolobrzeg"),
    (6, "Ewa Kaminska", "Poznan"),
    (7, "Adam Lewandowski", "Szczecin"),
    (8, "Katarzyna Dabrowska", "Lodz"),
    (9, "Pawel Mazur", "Lublin"),
    (10, "Agnieszka Krawczyk", "Katowice")
]

cursor.executemany("""
    INSERT INTO customers
    VALUES (?, ?, ?)
""", customers)


# Katalog produktow
products = [
    ("Laptop", 3500.0),
    ("Mysz", 50.0),
    ("Klawiatura", 200.0),
    ("Monitor", 1200.0),
    ("Sluchawki", 150.0),
    ("Smartfon", 2500.0),
    ("Tablet", 1800.0),
    ("Pendrive", 45.0),
    ("Dysk SSD", 350.0),
    ("Drukarka", 650.0)
]


# Generowanie 20 zamowien
orders = []

dates = pd.date_range(
    start="2026-01-01",
    periods=20,
    freq="D"
)

for order_id in range(1, 21):

    customer_id = int(rng.integers(1, 11))

    order_date = dates[
        order_id - 1
    ].strftime("%Y-%m-%d")

    orders.append((
        order_id,
        customer_id,
        order_date
    ))


cursor.executemany("""
    INSERT INTO orders
    VALUES (?, ?, ?)
""", orders)


# Generowanie pozycji zamowien
order_items = []
item_id = 1

for order_id in range(1, 21):

    number_of_products = int(
        rng.integers(1, 5)
    )

    selected_products = rng.choice(
        len(products),
        size=number_of_products,
        replace=False
    )

    for product_index in selected_products:

        product_name, price = products[
            int(product_index)
        ]

        quantity = int(rng.integers(1, 4))

        order_items.append((
            item_id,
            order_id,
            product_name,
            price,
            quantity
        ))

        item_id += 1


cursor.executemany("""
    INSERT INTO order_items
    VALUES (?, ?, ?, ?, ?)
""", order_items)

conn.commit()


print("=" * 75)
print("JOIN 3 TABEL - ANALIZA ZAMOWIEN SKLEPU")
print("=" * 75)


# =========================================================
# 3. DANE WEJSCIOWE
# =========================================================

df_customers = pd.read_sql_query(
    "SELECT * FROM customers ORDER BY customer_id",
    conn
)

df_orders = pd.read_sql_query(
    "SELECT * FROM orders ORDER BY order_id",
    conn
)

df_items = pd.read_sql_query(
    "SELECT * FROM order_items ORDER BY item_id",
    conn
)


section("1. TABELA CUSTOMERS")

print(df_customers.to_string(index=False))
print(f"\nLiczba klientow: {len(df_customers)}")


section("2. TABELA ORDERS")

print(df_orders.to_string(index=False))
print(f"\nLiczba zamowien: {len(df_orders)}")


section("3. TABELA ORDER_ITEMS")

print(df_items.to_string(index=False))
print(f"\nLiczba pozycji: {len(df_items)}")


# =========================================================
# 4. JOIN TRZECH TABEL
# =========================================================

section("4. INNER JOIN TRZECH TABEL")

query_join = """
SELECT
    c.customer_id,
    c.name AS customer_name,
    o.order_id,
    o.order_date,
    i.product_name,
    i.price,
    i.quantity,
    i.price * i.quantity AS item_value
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
INNER JOIN order_items AS i
    ON o.order_id = i.order_id
ORDER BY o.order_id, i.item_id
"""

df_join = pd.read_sql_query(
    query_join,
    conn
)

print(query_join)
print(df_join.to_string(index=False))

print(f"\nLiczba wierszy: {len(df_join)}")
print(f"Liczba kolumn: {len(df_join.columns)}")


# =========================================================
# 5. WARTOSC KAZDEGO ZAMOWIENIA
# =========================================================

section("5. LACZNA WARTOSC KAZDEGO ZAMOWIENIA")

query_totals = """
SELECT
    o.order_id,
    c.name AS customer_name,
    o.order_date,
    COUNT(i.item_id) AS liczba_pozycji,
    SUM(i.quantity) AS liczba_sztuk,
    SUM(i.price * i.quantity) AS wartosc_zamowienia
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
INNER JOIN order_items AS i
    ON o.order_id = i.order_id
GROUP BY
    o.order_id,
    c.name,
    o.order_date
"""

df_totals = pd.read_sql_query(
    query_totals + "\nORDER BY o.order_id",
    conn
)

print(query_totals)
print(df_totals.to_string(index=False))

print(f"\nLiczba zamowien: {len(df_totals)}")


# =========================================================
# 6. TOP 10 NAJWIEKSZYCH ZAMOWIEN
# =========================================================

section("6. TOP 10 NAJWIEKSZYCH ZAMOWIEN")

query_top10 = query_totals + """
ORDER BY wartosc_zamowienia DESC, o.order_id ASC
LIMIT 10
"""

df_top10 = pd.read_sql_query(
    query_top10,
    conn
)

print(query_top10)
print(df_top10.to_string(index=False))


# =========================================================
# 7. ANALIZA STATYSTYCZNA
# =========================================================

section("7. ANALIZA STATYSTYCZNA")

values = df_totals["wartosc_zamowienia"]

total_sales = values.sum()
top10_sales = df_top10["wartosc_zamowienia"].sum()

top10_share = top10_sales / total_sales * 100

statistics = pd.DataFrame({
    "Metryka": [
        "Liczba klientow",
        "Liczba zamowien",
        "Liczba pozycji",
        "Liczba sprzedanych sztuk",
        "Calkowita wartosc sprzedazy",
        "Srednia wartosc zamowienia",
        "Mediana wartosci zamowienia",
        "Minimalna wartosc zamowienia",
        "Maksymalna wartosc zamowienia",
        "Wartosc TOP 10",
        "Udzial TOP 10 (%)"
    ],
    "Wartosc": [
        len(df_customers),
        len(df_orders),
        len(df_items),
        df_items["quantity"].sum(),
        total_sales,
        values.mean(),
        values.median(),
        values.min(),
        values.max(),
        top10_sales,
        top10_share
    ]
})

print(statistics.round(2).to_string(index=False))


# =========================================================
# 8. SPRZEDAZ WEDLUG KLIENTA
# =========================================================

section("8. SPRZEDAZ WEDLUG KLIENTA")

query_customers = """
SELECT
    c.customer_id,
    c.name,
    COUNT(DISTINCT o.order_id) AS liczba_zamowien,
    COUNT(i.item_id) AS liczba_pozycji,
    COALESCE(SUM(i.quantity), 0) AS liczba_sztuk,
    COALESCE(
        SUM(i.price * i.quantity), 0
    ) AS laczna_sprzedaz
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
LEFT JOIN order_items AS i
    ON o.order_id = i.order_id
GROUP BY c.customer_id, c.name
ORDER BY laczna_sprzedaz DESC, c.customer_id
"""

df_customer_sales = pd.read_sql_query(
    query_customers,
    conn
)

print(df_customer_sales.to_string(index=False))


# =========================================================
# 9. SPRZEDAZ WEDLUG PRODUKTU
# =========================================================

section("9. SPRZEDAZ WEDLUG PRODUKTU")

query_products = """
SELECT
    product_name,
    COUNT(DISTINCT order_id) AS liczba_zamowien,
    SUM(quantity) AS sprzedane_sztuki,
    SUM(price * quantity) AS wartosc_sprzedazy
FROM order_items
GROUP BY product_name
ORDER BY wartosc_sprzedazy DESC, product_name
"""

df_product_sales = pd.read_sql_query(
    query_products,
    conn
)

print(df_product_sales.to_string(index=False))


# =========================================================
# 10. TEKSTOWY WYKRES TOP 10
# =========================================================

section("10. TEKSTOWY WYKRES TOP 10 ZAMOWIEN")

max_value = df_top10[
    "wartosc_zamowienia"
].max()

print("Najwieksze zamowienie = 40 znakow\n")

for row in df_top10.itertuples(index=False):

    bar_length = round(
        row.wartosc_zamowienia / max_value * 40
    )

    bar = "█" * bar_length

    print(
        f"Zamowienie {row.order_id:02d} | "
        f"{bar:<40} "
        f"{row.wartosc_zamowienia:10.2f} PLN"
    )


# =========================================================
# 11. WERYFIKACJA ZA POMOCA PANDAS
# =========================================================

section("11. WERYFIKACJA SQL ZA POMOCA PANDAS")

df_pandas_join = (
    df_customers
    .merge(
        df_orders,
        on="customer_id",
        how="inner",
        validate="one_to_many"
    )
    .merge(
        df_items,
        on="order_id",
        how="inner",
        validate="one_to_many"
    )
    .rename(columns={
        "name": "customer_name"
    })
)

df_pandas_join["item_value"] = (
    df_pandas_join["price"]
    * df_pandas_join["quantity"]
)

df_pandas_join = (
    df_pandas_join
    .sort_values(["order_id", "item_id"])
    [df_join.columns]
    .reset_index(drop=True)
)

join_equal = df_join.equals(
    df_pandas_join
)

print(f"SQL vs Pandas - JOIN: {join_equal}")


df_pandas_totals = (
    df_pandas_join
    .groupby(
        [
            "order_id",
            "customer_name",
            "order_date"
        ],
        as_index=False
    )
    .agg(
        liczba_pozycji=("product_name", "size"),
        liczba_sztuk=("quantity", "sum"),
        wartosc_zamowienia=("item_value", "sum")
    )
    .sort_values("order_id")
    .reset_index(drop=True)
)

totals_equal = df_totals.equals(
    df_pandas_totals
)

print(
    f"SQL vs Pandas - agregacja: {totals_equal}"
)


df_pandas_top10 = (
    df_pandas_totals
    .sort_values(
        ["wartosc_zamowienia", "order_id"],
        ascending=[False, True]
    )
    .head(10)
    .reset_index(drop=True)
)

top10_equal = df_top10.equals(
    df_pandas_top10
)

print(f"SQL vs Pandas - TOP 10: {top10_equal}")


# =========================================================
# 12. ANALIZA PLANU ZAPYTANIA
# =========================================================

section("12. EXPLAIN QUERY PLAN - JOIN")

df_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_join,
    conn
)

print(df_plan.to_string(index=False))


section("13. EXPLAIN QUERY PLAN - TOP 10")

df_plan_top10 = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_top10,
    conn
)

print(df_plan_top10.to_string(index=False))


# =========================================================
# 13. AUTOMATYCZNE TESTY
# =========================================================

section("14. WERYFIKACJA")

foreign_key_errors = cursor.execute(
    "PRAGMA foreign_key_check"
).fetchall()

expected_values = (
    df_items["price"] * df_items["quantity"]
)

expected_total = expected_values.sum()

tests = {
    "Tabela customers zawiera 10 klientow":
        len(df_customers) == 10,

    "Tabela orders zawiera 20 zamowien":
        len(df_orders) == 20,

    "Kazde zamowienie ma przynajmniej jedna pozycje":
        df_items["order_id"].nunique() == 20,

    "Identyfikatory klientow sa unikalne":
        df_customers["customer_id"].is_unique,

    "Identyfikatory zamowien sa unikalne":
        df_orders["order_id"].is_unique,

    "Identyfikatory pozycji sa unikalne":
        df_items["item_id"].is_unique,

    "Brak naruszen kluczy obcych":
        len(foreign_key_errors) == 0,

    "Wszystkie zamowienia maja istniejacego klienta":
        df_orders["customer_id"].isin(
            df_customers["customer_id"]
        ).all(),

    "Wszystkie pozycje maja istniejace zamowienie":
        df_items["order_id"].isin(
            df_orders["order_id"]
        ).all(),

    "Ceny produktow sa dodatnie":
        (df_items["price"] > 0).all(),

    "Ilosci produktow sa dodatnie":
        (df_items["quantity"] > 0).all(),

    "JOIN zwraca wszystkie pozycje":
        len(df_join) == len(df_items),

    "JOIN zawiera 8 kolumn":
        len(df_join.columns) == 8,

    "JOIN zawiera nazwe klienta":
        "customer_name" in df_join.columns,

    "JOIN zawiera date zamowienia":
        "order_date" in df_join.columns,

    "JOIN zawiera nazwe produktu":
        "product_name" in df_join.columns,

    "JOIN zawiera cene produktu":
        "price" in df_join.columns,

    "Brak wartosci NaN w JOIN":
        not df_join.isna().any().any(),

    "Wartosci pozycji sa poprawne":
        np.allclose(
            df_join["item_value"],
            df_join["price"] * df_join["quantity"]
        ),

    "Agregacja zawiera 20 zamowien":
        len(df_totals) == 20,

    "Kazde zamowienie wystepuje raz":
        df_totals["order_id"].is_unique,

    "Suma liczby pozycji jest zgodna":
        df_totals["liczba_pozycji"].sum()
        == len(df_items),

    "Suma liczby sztuk jest zgodna":
        df_totals["liczba_sztuk"].sum()
        == df_items["quantity"].sum(),

    "Calkowita wartosc sprzedazy jest zgodna":
        np.isclose(total_sales, expected_total),

    "TOP 10 zawiera 10 zamowien":
        len(df_top10) == 10,

    "TOP 10 jest posortowane malejaco":
        df_top10[
            "wartosc_zamowienia"
        ].is_monotonic_decreasing,

    "TOP 10 zawiera unikalne zamowienia":
        df_top10["order_id"].is_unique,

    "Najwieksze zamowienie jest poprawne":
        np.isclose(
            df_top10.iloc[0]["wartosc_zamowienia"],
            values.max()
        ),

    "Wartosc TOP 10 nie przekracza sprzedazy":
        top10_sales <= total_sales,

    "Udzial TOP 10 miesci sie w zakresie":
        0 <= top10_share <= 100,

    "Agregacja klientow zawiera wszystkich klientow":
        len(df_customer_sales) == 10,

    "Liczba zamowien klientow jest zgodna":
        df_customer_sales["liczba_zamowien"].sum()
        == len(df_orders),

    "Suma sprzedazy klientow jest zgodna":
        np.isclose(
            df_customer_sales["laczna_sprzedaz"].sum(),
            total_sales
        ),

    "Suma sprzedazy produktow jest zgodna":
        np.isclose(
            df_product_sales["wartosc_sprzedazy"].sum(),
            total_sales
        ),

    "SQL i Pandas - JOIN sa zgodne":
        join_equal,

    "SQL i Pandas - agregacja sa zgodne":
        totals_equal,

    "SQL i Pandas - TOP 10 sa zgodne":
        top10_equal,

    "Plan wykonania JOIN nie jest pusty":
        not df_plan.empty,

    "Plan wykonania TOP 10 nie jest pusty":
        not df_plan_top10.empty,

    "Tabela customers pozostala niezmieniona":
        df_customers.equals(
            pd.read_sql_query(
                "SELECT * FROM customers ORDER BY customer_id",
                conn
            )
        ),

    "Tabela orders pozostala niezmieniona":
        df_orders.equals(
            pd.read_sql_query(
                "SELECT * FROM orders ORDER BY order_id",
                conn
            )
        ),

    "Tabela order_items pozostala niezmieniona":
        df_items.equals(
            pd.read_sql_query(
                "SELECT * FROM order_items ORDER BY item_id",
                conn
            )
        )
}

for description, result in tests.items():
    print(f"Czy {description}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")


# =========================================================
# 14. WNIOSKI
# =========================================================

section("15. WNIOSKI")

conclusions = [
    "INNER JOIN pozwala laczyc wiecej niz dwie tabele.",
    "Kazdy JOIN wymaga odpowiedniego warunku ON.",
    "Klucze obce zapewniaja integralnosc relacji.",
    "Relacja jeden do wielu pozwala przechowywac wiele pozycji.",
    "Wartosc pozycji to cena pomnozona przez ilosc.",
    "SUM i GROUP BY obliczaja wartosc zamowienia.",
    "COUNT DISTINCT zapobiega wielokrotnemu liczeniu zamowien.",
    "ORDER BY DESC i LIMIT pozwalaja tworzyc rankingi.",
    "LEFT JOIN zachowuje rowniez klientow bez zamowien.",
    "COALESCE pozwala zastapic NULL wartoscia domyslna.",
    "Agregacja SQL ogranicza ilosc danych pobieranych z bazy.",
    "Pandas merge pozwala zweryfikowac wyniki SQL.",
    "EXPLAIN QUERY PLAN pokazuje sposob wykonania zapytania.",
    "JOIN i agregacje nie modyfikuja danych zrodlowych."
]

for number, conclusion in enumerate(
    conclusions,
    start=1
):
    print(f"{number}. {conclusion}")


# =========================================================
# 15. PODSUMOWANIE
# =========================================================

section("PODSUMOWANIE")

print(f"Liczba tabel: 3")
print(f"Liczba klientow: {len(df_customers)}")
print(f"Liczba zamowien: {len(df_orders)}")
print(f"Liczba pozycji: {len(df_items)}")
print(f"Liczba wierszy JOIN: {len(df_join)}")
print(f"Liczba sprzedanych sztuk: {df_items['quantity'].sum()}")
print(f"Calkowita sprzedaz: {total_sales:.2f} PLN")
print(f"Srednia wartosc zamowienia: {values.mean():.2f} PLN")
print(f"Najwieksze zamowienie: {values.max():.2f} PLN")
print(f"Wartosc TOP 10: {top10_sales:.2f} PLN")
print(f"Udzial TOP 10: {top10_share:.2f}%")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 9 wykonane poprawnie.")
