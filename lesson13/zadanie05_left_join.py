# Lekcja 13 - Zadanie 5: LEFT JOIN

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


# Dane klientow z zadania 4
customers = [
    (1, "Jan Kowalski", "Warszawa"),
    (2, "Anna Nowak", "Krakow"),
    (3, "Piotr Wisniewski", "Gdansk"),
    (4, "Maria Zielinska", "Wroclaw"),
    (5, "Tomasz Wojcik", "Kolobrzeg"),
    (6, "Ewa Kaminska", "Poznan")
]


# Dane zamowien z zadania 4
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
print("LEFT JOIN - WSZYSCY KLIENCI I ZAMOWIENIA")
print("=" * 75)


# Wczytanie danych do Pandas
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


section("3. LEFT JOIN - WSZYSCY KLIENCI")

query_left = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    o.order_id,
    o.amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY o.amount DESC, o.order_id ASC
"""

print(query_left)

df_left = pd.read_sql_query(
    query_left,
    conn
)

print(df_left.to_string(index=False))

print(f"\nLiczba wierszy: {len(df_left)}")

print(
    f"Liczba unikalnych klientow: "
    f"{df_left['customer_id'].nunique()}"
)

print(
    f"Liczba brakujacych kwot: "
    f"{df_left['amount'].isna().sum()}"
)


section("4. LEFT JOIN Z COALESCE")

query_coalesce = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    o.order_id,
    COALESCE(o.amount, 0) AS amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY amount DESC, o.order_id ASC
"""

print(query_coalesce)

df_coalesce = pd.read_sql_query(
    query_coalesce,
    conn
)

print(df_coalesce.to_string(index=False))

print(
    f"\nBrakujace kwoty przed COALESCE: "
    f"{df_left['amount'].isna().sum()}"
)

print(
    f"Brakujace kwoty po COALESCE: "
    f"{df_coalesce['amount'].isna().sum()}"
)


section("5. POROWNANIE NULL I COALESCE")

comparison_null = pd.DataFrame({
    "Klient": df_left["name"],
    "Kwota_przed": df_left["amount"],
    "Kwota_po": df_coalesce["amount"]
})

print(comparison_null.to_string(index=False))


section("6. KLIENCI BEZ ZAMOWIEN")

query_no_orders = """
SELECT
    c.customer_id,
    c.name,
    c.city
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id
"""

print(query_no_orders)

df_no_orders = pd.read_sql_query(
    query_no_orders,
    conn
)

print(df_no_orders.to_string(index=False))

print(
    f"\nLiczba klientow bez zamowien: "
    f"{len(df_no_orders)}"
)


section("7. KLIENCI Z ZAMOWIENIAMI")

query_active = """
SELECT DISTINCT
    c.customer_id,
    c.name,
    c.city
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NOT NULL
ORDER BY c.customer_id
"""

df_active = pd.read_sql_query(
    query_active,
    conn
)

print(df_active.to_string(index=False))

print(
    f"\nLiczba klientow z zamowieniami: "
    f"{len(df_active)}"
)


section("8. POROWNANIE INNER JOIN I LEFT JOIN")

query_inner = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    o.order_id,
    o.amount
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY o.amount DESC, o.order_id ASC
"""

df_inner = pd.read_sql_query(
    query_inner,
    conn
)

join_comparison = pd.DataFrame({
    "Rodzaj_JOIN": [
        "INNER JOIN",
        "LEFT JOIN",
        "LEFT JOIN + COALESCE"
    ],
    "Liczba_wierszy": [
        len(df_inner),
        len(df_left),
        len(df_coalesce)
    ],
    "Unikalni_klienci": [
        df_inner["customer_id"].nunique(),
        df_left["customer_id"].nunique(),
        df_coalesce["customer_id"].nunique()
    ],
    "Brakujace_kwoty": [
        df_inner["amount"].isna().sum(),
        df_left["amount"].isna().sum(),
        df_coalesce["amount"].isna().sum()
    ]
})

print(join_comparison.to_string(index=False))


section("9. AGREGACJA WEDLUG WSZYSTKICH KLIENTOW")

query_aggregation = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    COUNT(o.order_id) AS liczba_zamowien,
    COALESCE(SUM(o.amount), 0) AS suma_zamowien,
    COALESCE(AVG(o.amount), 0) AS srednia_kwota
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY suma_zamowien DESC, c.customer_id
"""

print(query_aggregation)

df_aggregation = pd.read_sql_query(
    query_aggregation,
    conn
)

print(
    df_aggregation.round(2).to_string(index=False)
)


section("10. POROWNANIE COUNT(*) I COUNT(order_id)")

query_count = """
SELECT
    c.name,
    COUNT(*) AS count_all,
    COUNT(o.order_id) AS count_orders
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id
"""

df_count = pd.read_sql_query(
    query_count,
    conn
)

print(df_count.to_string(index=False))

print(
    "\nCOUNT(*) liczy wszystkie wiersze "
    "wyniku LEFT JOIN."
)

print(
    "COUNT(order_id) liczy tylko rzeczywiste "
    "zamowienia, pomijajac NULL."
)


section("11. ANALIZA STATYSTYCZNA")

total_customers = len(df_customers)
active_customers = len(df_active)
inactive_customers = len(df_no_orders)

active_rate = active_customers / total_customers * 100
inactive_rate = inactive_customers / total_customers * 100

total_amount = df_coalesce["amount"].sum()

statistics = pd.DataFrame({
    "Metryka": [
        "Wszyscy klienci",
        "Klienci z zamowieniami",
        "Klienci bez zamowien",
        "Aktywni klienci (%)",
        "Nieaktywni klienci (%)",
        "Liczba zamowien",
        "Suma zamowien",
        "Srednia wartosc zamowienia",
        "Srednia sprzedaz na klienta"
    ],
    "Wartosc": [
        total_customers,
        active_customers,
        inactive_customers,
        active_rate,
        inactive_rate,
        len(df_orders),
        total_amount,
        df_orders["amount"].mean(),
        total_amount / total_customers
    ]
})

print(statistics.round(2).to_string(index=False))


section("12. TEKSTOWY WYKRES SPRZEDAZY")

print("Legenda: jeden znak = okolo 100 PLN\n")

for _, row in df_aggregation.iterrows():
    amount = row["suma_zamowien"]
    bar = "█" * int(round(amount / 100))

    print(
        f"{row['name']:20} | "
        f"{bar:30} "
        f"{amount:8.2f} PLN"
    )


section("13. TEKSTOWY WYKRES AKTYWNOSCI KLIENTOW")

print("Legenda: jeden znak = jeden klient\n")

print(
    f"Klienci z zamowieniami  | "
    f"{'█' * active_customers:10} "
    f"{active_customers} ({active_rate:.2f}%)"
)

print(
    f"Klienci bez zamowien    | "
    f"{'█' * inactive_customers:10} "
    f"{inactive_customers} ({inactive_rate:.2f}%)"
)


section("14. WERYFIKACJA SQL ZA POMOCA PANDAS")

df_pandas_left = (
    df_customers.merge(
        df_orders,
        on="customer_id",
        how="left"
    )
    .sort_values(
        ["amount", "order_id"],
        ascending=[False, True],
        na_position="last"
    )
    [["customer_id", "name", "city", "order_id", "amount"]]
    .reset_index(drop=True)
)

df_pandas_coalesce = df_pandas_left.copy()

df_pandas_coalesce["amount"] = (
    df_pandas_coalesce["amount"].fillna(0)
)

df_pandas_no_orders = (
    df_pandas_left.loc[
        df_pandas_left["order_id"].isna(),
        ["customer_id", "name", "city"]
    ]
    .sort_values("customer_id")
    .reset_index(drop=True)
)


# Porownanie wartosci z tolerancja typow danych
def frames_equal(left, right):
    try:
        pd.testing.assert_frame_equal(
            left,
            right,
            check_dtype=False
        )
        return True
    except AssertionError:
        return False


left_equal = frames_equal(
    df_left,
    df_pandas_left
)

coalesce_equal = frames_equal(
    df_coalesce,
    df_pandas_coalesce
)

no_orders_equal = frames_equal(
    df_no_orders,
    df_pandas_no_orders
)

print(f"SQL LEFT JOIN vs Pandas merge: {left_equal}")

print(
    f"SQL COALESCE vs Pandas fillna: "
    f"{coalesce_equal}"
)

print(
    f"SQL IS NULL vs Pandas isna: "
    f"{no_orders_equal}"
)


section("15. ALTERNATYWNE ZAPYTANIE NOT EXISTS")

query_not_exists = """
SELECT
    c.customer_id,
    c.name,
    c.city
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
)
ORDER BY c.customer_id
"""

print(query_not_exists)

df_not_exists = pd.read_sql_query(
    query_not_exists,
    conn
)

print(df_not_exists.to_string(index=False))

not_exists_equal = frames_equal(
    df_no_orders,
    df_not_exists
)

print(
    f"\nCzy LEFT JOIN IS NULL i NOT EXISTS "
    f"sa zgodne: {not_exists_equal}"
)


section("16. PLAN WYKONANIA LEFT JOIN")

df_plan_left = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_left,
    conn
)

print(df_plan_left.to_string(index=False))


section("17. PLAN WYKONANIA ZAPYTANIA IS NULL")

df_plan_null = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_no_orders,
    conn
)

print(df_plan_null.to_string(index=False))


section("18. WERYFIKACJA")

ewa = df_aggregation.loc[
    df_aggregation["customer_id"] == 6
].iloc[0]

ewa_count = df_count.loc[
    df_count["name"] == "Ewa Kaminska"
].iloc[0]

tests = {
    "Tabela customers zawiera 6 klientow":
        len(df_customers) == 6,

    "Tabela orders zawiera 10 zamowien":
        len(df_orders) == 10,

    "Identyfikatory klientow sa unikalne":
        df_customers["customer_id"].is_unique,

    "Identyfikatory zamowien sa unikalne":
        df_orders["order_id"].is_unique,

    "LEFT JOIN zwraca 11 wierszy":
        len(df_left) == 11,

    "LEFT JOIN zawiera wszystkich 6 klientow":
        df_left["customer_id"].nunique() == 6,

    "LEFT JOIN zawiera jedna brakujaca kwote":
        df_left["amount"].isna().sum() == 1,

    "LEFT JOIN zawiera jeden brakujacy order_id":
        df_left["order_id"].isna().sum() == 1,

    "COALESCE zachowuje 11 wierszy":
        len(df_coalesce) == 11,

    "COALESCE usuwa wszystkie braki kwot":
        not df_coalesce["amount"].isna().any(),

    "COALESCE zamienia jedna kwote na zero":
        (df_coalesce["amount"] == 0).sum() == 1,

    "COALESCE nie zmienia istniejacych kwot":
        np.allclose(
            df_left["amount"].dropna(),
            df_coalesce.loc[
                df_left["amount"].notna(),
                "amount"
            ]
        ),

    "COALESCE zachowuje brakujacy order_id":
        df_coalesce["order_id"].isna().sum() == 1,

    "Suma kwot przed i po COALESCE jest zgodna":
        np.isclose(
            df_left["amount"].sum(),
            df_coalesce["amount"].sum()
        ),

    "Suma zamowien wynosi 9170 PLN":
        np.isclose(total_amount, 9170),

    "Jeden klient nie ma zamowien":
        len(df_no_orders) == 1,

    "Klient bez zamowien to Ewa Kaminska":
        df_no_orders.iloc[0]["name"] == "Ewa Kaminska",

    "Klient bez zamowien ma ID 6":
        df_no_orders.iloc[0]["customer_id"] == 6,

    "Pieciu klientow ma zamowienia":
        len(df_active) == 5,

    "Aktywni i nieaktywni daja wszystkich klientow":
        active_customers + inactive_customers
        == total_customers,

    "Udzialy klientow sumuja sie do 100 procent":
        np.isclose(active_rate + inactive_rate, 100),

    "INNER JOIN zwraca 10 wierszy":
        len(df_inner) == 10,

    "INNER JOIN zawiera 5 klientow":
        df_inner["customer_id"].nunique() == 5,

    "LEFT JOIN zawiera wiecej wierszy niz INNER JOIN":
        len(df_left) > len(df_inner),

    "Agregacja zawiera wszystkich 6 klientow":
        len(df_aggregation) == 6,

    "Suma liczby zamowien wynosi 10":
        df_aggregation["liczba_zamowien"].sum() == 10,

    "Suma zagregowanych kwot wynosi 9170 PLN":
        np.isclose(
            df_aggregation["suma_zamowien"].sum(),
            9170
        ),

    "Ewa Kaminska ma zero zamowien":
        ewa["liczba_zamowien"] == 0,

    "Ewa Kaminska ma zero sprzedazy":
        np.isclose(ewa["suma_zamowien"], 0),

    "Ewa Kaminska ma srednia prezentowana jako zero":
        np.isclose(ewa["srednia_kwota"], 0),

    "COUNT(*) dla Ewy wynosi 1":
        ewa_count["count_all"] == 1,

    "COUNT(order_id) dla Ewy wynosi 0":
        ewa_count["count_orders"] == 0,

    "SQL LEFT JOIN i Pandas sa zgodne":
        left_equal,

    "SQL COALESCE i Pandas fillna sa zgodne":
        coalesce_equal,

    "SQL IS NULL i Pandas isna sa zgodne":
        no_orders_equal,

    "LEFT JOIN IS NULL i NOT EXISTS sa zgodne":
        not_exists_equal,

    "Kwoty sa posortowane malejaco":
        df_coalesce["amount"].is_monotonic_decreasing,

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
    "LEFT JOIN zachowuje wszystkie rekordy lewej tabeli.",
    "Brak dopasowania powoduje pojawienie sie NULL.",
    "COALESCE zwraca pierwsza wartosc rozna od NULL.",
    "COALESCE pozwala prezentowac brak kwoty jako zero.",
    "COALESCE nie modyfikuje danych zrodlowych.",
    "IS NULL pozwala znalezc klientow bez zamowien.",
    "IS NOT NULL pozwala znalezc klientow z zamowieniami.",
    "COUNT(*) uwzglednia wszystkie wiersze wyniku.",
    "COUNT(order_id) pomija wartosci NULL.",
    "SUM dla grupy bez zamowien zwraca NULL.",
    "AVG dla grupy bez zamowien zwraca NULL.",
    "Zero sredniej dla nieaktywnych to decyzja prezentacyjna.",
    "LEFT JOIN jest przydatny w analizie aktywnosci klientow.",
    "NOT EXISTS jest alternatywa dla LEFT JOIN IS NULL.",
    "Pandas merge(how='left') odpowiada LEFT JOIN.",
    "Pandas fillna(0) odpowiada COALESCE(amount, 0).",
    "EXPLAIN QUERY PLAN pokazuje sposob wykonania zapytania."
]

for number, conclusion in enumerate(conclusions, 1):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba klientow: {total_customers}")
print(f"Liczba zamowien: {len(df_orders)}")
print(f"Wiersze INNER JOIN: {len(df_inner)}")
print(f"Wiersze LEFT JOIN: {len(df_left)}")
print(f"Klienci z zamowieniami: {active_customers}")
print(f"Klienci bez zamowien: {inactive_customers}")
print(f"Aktywni klienci: {active_rate:.2f}%")
print(f"Nieaktywni klienci: {inactive_rate:.2f}%")
print(f"Suma zamowien: {total_amount:.2f} PLN")

print(
    f"Brakujace kwoty przed COALESCE: "
    f"{df_left['amount'].isna().sum()}"
)

print(
    f"Brakujace kwoty po COALESCE: "
    f"{df_coalesce['amount'].isna().sum()}"
)

print(f"Zaliczone testy: {passed}/{total}")

conn.close()

assert passed == total, "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 5 wykonane poprawnie.")
