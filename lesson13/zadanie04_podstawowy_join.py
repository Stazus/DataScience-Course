# Lekcja 13 - Zadanie 4: Podstawowy JOIN

import sqlite3
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Utworzenie bazy danych SQLite w pamieci
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Wlaczenie kontroli kluczy obcych
cursor.execute("PRAGMA foreign_keys = ON")


# Utworzenie tabeli customers
cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    )
""")


# Utworzenie tabeli orders
cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
    )
""")


# Dane klientow
customers = [
    (1, "Jan Kowalski", "Warszawa"),
    (2, "Anna Nowak", "Krakow"),
    (3, "Piotr Wisniewski", "Gdansk"),
    (4, "Maria Zielinska", "Wroclaw"),
    (5, "Tomasz Wojcik", "Kolobrzeg"),
    (6, "Ewa Kaminska", "Poznan")
]


# Dane zamowien
orders = [
    (1, 1, 1200.00),
    (2, 2, 350.00),
    (3, 1, 750.00),
    (4, 3, 2100.00),
    (5, 4, 450.00),
    (6, 2, 890.00),
    (7, 5, 1500.00),
    (8, 3, 300.00),
    (9, 4, 650.00),
    (10, 5, 980.00)
]


# Wstawienie danych
cursor.executemany("""
    INSERT INTO customers
    VALUES (?, ?, ?)
""", customers)

cursor.executemany("""
    INSERT INTO orders
    VALUES (?, ?, ?)
""", orders)

conn.commit()


print("=" * 75)
print("PODSTAWOWY JOIN - KLIENCI I ZAMOWIENIA")
print("=" * 75)


# Wczytanie tabel do Pandas
df_customers = pd.read_sql_query(
    "SELECT * FROM customers",
    conn
)

df_orders = pd.read_sql_query(
    "SELECT * FROM orders",
    conn
)


section("1. TABELA CUSTOMERS")

print(df_customers.to_string(index=False))
print(f"\nLiczba klientow: {len(df_customers)}")


section("2. TABELA ORDERS")

print(df_orders.to_string(index=False))
print(f"\nLiczba zamowien: {len(df_orders)}")


section("3. INNER JOIN - KLIENCI I ZAMOWIENIA")

query = """
SELECT
    c.name,
    c.city,
    o.amount
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY o.amount DESC, o.order_id ASC
"""

print(query)

df_join = pd.read_sql_query(query, conn)

print(df_join.to_string(index=False))

print(f"\nLiczba wynikow: {len(df_join)}")
print(f"Liczba kolumn: {len(df_join.columns)}")


section("4. ANALIZA STATYSTYCZNA ZAMOWIEN")

statistics = pd.DataFrame({
    "Metryka": [
        "Liczba zamowien",
        "Suma zamowien",
        "Srednia kwota",
        "Mediana kwoty",
        "Minimalna kwota",
        "Maksymalna kwota"
    ],
    "Wartosc": [
        len(df_join),
        df_join["amount"].sum(),
        df_join["amount"].mean(),
        df_join["amount"].median(),
        df_join["amount"].min(),
        df_join["amount"].max()
    ]
})

print(statistics.round(2).to_string(index=False))


section("5. AGREGACJA ZAMOWIEN WEDLUG KLIENTA")

query_aggregation = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    COUNT(o.order_id) AS liczba_zamowien,
    SUM(o.amount) AS suma_zamowien,
    AVG(o.amount) AS srednia_kwota
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY suma_zamowien DESC
"""

df_aggregation = pd.read_sql_query(
    query_aggregation,
    conn
)

print(
    df_aggregation.round(2).to_string(index=False)
)


section("6. TEKSTOWY WYKRES ZAMOWIEN")

print("Legenda: jeden znak = okolo 100 PLN\n")

for _, row in df_join.iterrows():
    bar = "█" * int(round(row["amount"] / 100))

    print(
        f"{row['name']:20} | "
        f"{bar:25} "
        f"{row['amount']:8.2f} PLN"
    )


section("7. KLIENCI BEZ ZAMOWIEN")

query_no_orders = """
SELECT
    c.customer_id,
    c.name,
    c.city
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
"""

df_no_orders = pd.read_sql_query(
    query_no_orders,
    conn
)

print(df_no_orders.to_string(index=False))

print(
    f"\nLiczba klientow bez zamowien: "
    f"{len(df_no_orders)}"
)

print(
    "INNER JOIN nie uwzglednia klientow "
    "bez pasujacych zamowien."
)


section("8. POROWNANIE INNER JOIN I LEFT JOIN")

query_left = """
SELECT
    c.name,
    c.city,
    o.amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY o.amount DESC, o.order_id ASC
"""

df_left = pd.read_sql_query(query_left, conn)

print(df_left.to_string(index=False))

comparison = pd.DataFrame({
    "Rodzaj_JOIN": ["INNER JOIN", "LEFT JOIN"],
    "Liczba_wierszy": [
        len(df_join),
        len(df_left)
    ],
    "Brakujace_kwoty": [
        df_join["amount"].isna().sum(),
        df_left["amount"].isna().sum()
    ]
})

print("\nPorownanie:")
print(comparison.to_string(index=False))


section("9. WERYFIKACJA SQL ZA POMOCA PANDAS")

df_pandas = (
    df_customers.merge(
        df_orders,
        on="customer_id",
        how="inner"
    )
    .sort_values(
        ["amount", "order_id"],
        ascending=[False, True]
    )
    [["name", "city", "amount"]]
    .reset_index(drop=True)
)

print(df_pandas.to_string(index=False))

sql_pandas_equal = df_join.equals(df_pandas)

print(
    f"\nCzy SQL i Pandas zwracaja "
    f"identyczne wyniki: {sql_pandas_equal}"
)


section("10. PLAN WYKONANIA ZAPYTANIA")

df_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query,
    conn
)

print(df_plan.to_string(index=False))


section("11. WERYFIKACJA")

tests = {
    "Tabela customers zawiera 6 klientow":
        len(df_customers) == 6,

    "Tabela orders zawiera 10 zamowien":
        len(df_orders) == 10,

    "Identyfikatory klientow sa unikalne":
        df_customers["customer_id"].is_unique,

    "Identyfikatory zamowien sa unikalne":
        df_orders["order_id"].is_unique,

    "Wszystkie zamowienia maja istniejacego klienta":
        df_orders["customer_id"].isin(
            df_customers["customer_id"]
        ).all(),

    "INNER JOIN zwraca 10 wierszy":
        len(df_join) == 10,

    "INNER JOIN zwraca 3 kolumny":
        len(df_join.columns) == 3,

    "Wybrano wlasciwe kolumny":
        list(df_join.columns) ==
        ["name", "city", "amount"],

    "Brak wartosci NaN w INNER JOIN":
        not df_join.isna().any().any(),

    "Kwoty sa posortowane malejaco":
        df_join["amount"].is_monotonic_decreasing,

    "Najwyzsza kwota wynosi 2100 PLN":
        np.isclose(df_join["amount"].max(), 2100),

    "Najnizsza kwota wynosi 300 PLN":
        np.isclose(df_join["amount"].min(), 300),

    "Najwieksze zamowienie nalezy do Piotra":
        df_join.iloc[0]["name"] == "Piotr Wisniewski",

    "Suma zamowien wynosi 9170 PLN":
        np.isclose(df_join["amount"].sum(), 9170),

    "Srednia kwota wynosi 917 PLN":
        np.isclose(df_join["amount"].mean(), 917),

    "INNER JOIN zawiera 5 klientow":
        df_join["name"].nunique() == 5,

    "Jeden klient nie ma zamowien":
        len(df_no_orders) == 1,

    "Klient bez zamowien to Ewa Kaminska":
        df_no_orders.iloc[0]["name"] == "Ewa Kaminska",

    "INNER JOIN nie zawiera Ewy Kaminskiej":
        "Ewa Kaminska" not in df_join["name"].values,

    "LEFT JOIN zawiera 11 wierszy":
        len(df_left) == 11,

    "LEFT JOIN zawiera wszystkich klientow":
        df_left["name"].nunique() == 6,

    "LEFT JOIN zawiera jedna brakujaca kwote":
        df_left["amount"].isna().sum() == 1,

    "Agregacja zawiera 5 klientow":
        len(df_aggregation) == 5,

    "Suma zagregowanych zamowien jest zgodna":
        np.isclose(
            df_aggregation["suma_zamowien"].sum(),
            df_join["amount"].sum()
        ),

    "Liczba zagregowanych zamowien jest zgodna":
        df_aggregation["liczba_zamowien"].sum() == 10,

    "SQL i Pandas zwracaja identyczne wyniki":
        sql_pandas_equal,

    "Tabela customers pozostala niezmieniona":
        df_customers.equals(
            pd.read_sql_query(
                "SELECT * FROM customers", conn
            )
        ),

    "Tabela orders pozostala niezmieniona":
        df_orders.equals(
            pd.read_sql_query(
                "SELECT * FROM orders", conn
            )
        )
}

for description, result in tests.items():
    print(f"Czy {description}: {result}")

passed = sum(bool(result) for result in tests.values())
total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")


section("WNIOSKI")

conclusions = [
    "INNER JOIN laczy pasujace rekordy z dwoch tabel.",
    "ON okresla warunek laczenia tabel.",
    "PRIMARY KEY identyfikuje rekord w tabeli.",
    "FOREIGN KEY tworzy powiazanie z inna tabela.",
    "Jeden klient moze miec wiele zamowien.",
    "INNER JOIN pomija klientow bez zamowien.",
    "LEFT JOIN zachowuje wszystkich klientow.",
    "Aliasy c i o upraszczaja zapytanie SQL.",
    "ORDER BY DESC sortuje kwoty malejaco.",
    "GROUP BY pozwala agregowac polaczone dane.",
    "Pandas merge odpowiada operacji JOIN.",
    "EXPLAIN QUERY PLAN pokazuje plan zapytania.",
    "JOIN nie modyfikuje danych zrodlowych."
]

for number, conclusion in enumerate(conclusions, 1):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba klientow: {len(df_customers)}")
print(f"Liczba zamowien: {len(df_orders)}")
print(f"Wiersze INNER JOIN: {len(df_join)}")
print(f"Wiersze LEFT JOIN: {len(df_left)}")
print(f"Klienci bez zamowien: {len(df_no_orders)}")
print(f"Suma zamowien: {df_join['amount'].sum():.2f} PLN")
print(f"Srednia kwota: {df_join['amount'].mean():.2f} PLN")
print(f"Zaliczone testy: {passed}/{total}")

conn.close()

assert passed == total, "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 4 wykonane poprawnie.")
