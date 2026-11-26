# Lekcja 13 - Zadanie 6: Podstawowy GROUP BY

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


# Utworzenie tabeli orders
cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        amount REAL NOT NULL
    )
""")


# Dane z zadania 4
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


# Wstawienie danych do tabeli
cursor.executemany("""
    INSERT INTO orders (
        order_id,
        customer_id,
        amount
    )
    VALUES (?, ?, ?)
""", orders)

conn.commit()


print("=" * 75)
print("PODSTAWOWY GROUP BY - AGREGACJA ZAMOWIEN")
print("=" * 75)


# Dane wejsciowe
section("1. TABELA ORDERS")

df_orders = pd.read_sql_query("""
    SELECT *
    FROM orders
    ORDER BY order_id
""", conn)

df_original = df_orders.copy()

print(df_orders.to_string(index=False))

print(f"\nLiczba zamowien: {len(df_orders)}")
print(
    f"Liczba klientow z zamowieniami: "
    f"{df_orders['customer_id'].nunique()}"
)


# Wymaganie 1 - liczba zamowien
section("2. LICZBA ZAMOWIEN DLA KAZDEGO KLIENTA")

query_count = """
SELECT
    customer_id,
    COUNT(*) AS liczba_zamowien
FROM orders
GROUP BY customer_id
ORDER BY customer_id
"""

df_count = pd.read_sql_query(query_count, conn)

print(query_count)
print(df_count.to_string(index=False))


# Wymaganie 2 - suma zamowien
section("3. LACZNA KWOTA ZAMOWIEN DLA KLIENTA")

query_sum = """
SELECT
    customer_id,
    SUM(amount) AS suma_zamowien
FROM orders
GROUP BY customer_id
ORDER BY customer_id
"""

df_sum = pd.read_sql_query(query_sum, conn)

print(query_sum)
print(df_sum.to_string(index=False))


# Wymaganie 3 - srednia wartosc zamowienia
section("4. SREDNIA WARTOSC ZAMOWIENIA DLA KLIENTA")

query_avg = """
SELECT
    customer_id,
    AVG(amount) AS srednia_kwota
FROM orders
GROUP BY customer_id
ORDER BY customer_id
"""

df_avg = pd.read_sql_query(query_avg, conn)

print(query_avg)
print(df_avg.to_string(index=False))


# Polaczenie wszystkich agregacji
section("5. KOMPLETNA AGREGACJA SQL")

query_all = """
SELECT
    customer_id,
    COUNT(*) AS liczba_zamowien,
    SUM(amount) AS suma_zamowien,
    AVG(amount) AS srednia_kwota,
    MIN(amount) AS minimalna_kwota,
    MAX(amount) AS maksymalna_kwota
FROM orders
GROUP BY customer_id
ORDER BY customer_id
"""

df_grouped = pd.read_sql_query(query_all, conn)

print(query_all)
print(df_grouped.round(2).to_string(index=False))


# Ranking klientow
section("6. RANKING KLIENTOW WEDLUG SPRZEDAZY")

query_ranking = """
SELECT
    customer_id,
    COUNT(*) AS liczba_zamowien,
    SUM(amount) AS suma_zamowien,
    AVG(amount) AS srednia_kwota
FROM orders
GROUP BY customer_id
ORDER BY suma_zamowien DESC, customer_id ASC
"""

df_ranking = pd.read_sql_query(query_ranking, conn)

print(query_ranking)
print(df_ranking.to_string(index=False))


# Analiza statystyczna
section("7. ANALIZA STATYSTYCZNA")

total_orders = len(df_orders)
total_customers = df_orders["customer_id"].nunique()
total_sales = df_orders["amount"].sum()
average_order = df_orders["amount"].mean()
median_order = df_orders["amount"].median()

statistics = pd.DataFrame({
    "Metryka": [
        "Liczba zamowien",
        "Liczba klientow",
        "Suma zamowien",
        "Srednia wartosc zamowienia",
        "Mediana zamowien",
        "Minimalna kwota",
        "Maksymalna kwota",
        "Srednia sprzedaz na klienta",
        "Srednia liczba zamowien na klienta"
    ],
    "Wartosc": [
        total_orders,
        total_customers,
        total_sales,
        average_order,
        median_order,
        df_orders["amount"].min(),
        df_orders["amount"].max(),
        total_sales / total_customers,
        total_orders / total_customers
    ]
})

print(statistics.round(2).to_string(index=False))


# Udzial klientow w sprzedazy
section("8. PROCENTOWY UDZIAL KLIENTOW W SPRZEDAZY")

df_contribution = df_ranking.copy()

df_contribution["udzial_proc"] = (
    df_contribution["suma_zamowien"]
    / total_sales * 100
)

print(
    df_contribution.round(2).to_string(index=False)
)

print(
    f"\nSuma udzialow: "
    f"{df_contribution['udzial_proc'].sum():.2f}%"
)


# Tekstowy wykres sprzedazy
section("9. TEKSTOWY WYKRES SPRZEDAZY")

print("Legenda: jeden znak = okolo 100 PLN\n")

for row in df_ranking.itertuples(index=False):
    bar = "█" * round(row.suma_zamowien / 100)

    print(
        f"Klient {row.customer_id:<3} | "
        f"{bar:<30} "
        f"{row.suma_zamowien:>8.2f} PLN"
    )


# Tekstowy wykres liczby zamowien
section("10. TEKSTOWY WYKRES LICZBY ZAMOWIEN")

print("Legenda: jeden znak = jedno zamowienie\n")

for row in df_count.itertuples(index=False):
    bar = "█" * row.liczba_zamowien

    print(
        f"Klient {row.customer_id:<3} | "
        f"{bar:<10} {row.liczba_zamowien}"
    )


# Agregacja za pomoca Pandas
section("11. AGREGACJA ZA POMOCA PANDAS")

df_pandas = (
    df_orders.groupby("customer_id")
    .agg(
        liczba_zamowien=("order_id", "count"),
        suma_zamowien=("amount", "sum"),
        srednia_kwota=("amount", "mean"),
        minimalna_kwota=("amount", "min"),
        maksymalna_kwota=("amount", "max")
    )
    .reset_index()
)

print(df_pandas.round(2).to_string(index=False))

sql_pandas_equal = df_grouped.equals(df_pandas)

print(
    "\nCzy SQL i Pandas zwracaja identyczne wyniki:",
    sql_pandas_equal
)


# Porownanie osobnych agregacji
section("12. POROWNANIE AGREGACJI")

count_equal = np.array_equal(
    df_count["liczba_zamowien"],
    df_grouped["liczba_zamowien"]
)

sum_equal = np.allclose(
    df_sum["suma_zamowien"],
    df_grouped["suma_zamowien"]
)

avg_equal = np.allclose(
    df_avg["srednia_kwota"],
    df_grouped["srednia_kwota"]
)

print(f"COUNT zgodny: {count_equal}")
print(f"SUM zgodny: {sum_equal}")
print(f"AVG zgodny: {avg_equal}")


# Najlepszy klient
section("13. KLIENT Z NAJWIEKSZA SPRZEDAZA")

best_customer = df_ranking.iloc[0]

print(
    f"ID klienta: "
    f"{int(best_customer['customer_id'])}"
)

print(
    f"Liczba zamowien: "
    f"{int(best_customer['liczba_zamowien'])}"
)

print(
    f"Suma zamowien: "
    f"{best_customer['suma_zamowien']:.2f} PLN"
)

print(
    f"Srednia wartosc zamowienia: "
    f"{best_customer['srednia_kwota']:.2f} PLN"
)


# Plan wykonania zapytania
section("14. EXPLAIN QUERY PLAN")

df_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_all,
    conn
)

print(df_plan.to_string(index=False))


# Ponowne odczytanie tabeli
df_after = pd.read_sql_query("""
    SELECT *
    FROM orders
    ORDER BY order_id
""", conn)


# Automatyczne testy
section("15. WERYFIKACJA")

tests = {
    "Tabela zawiera 10 zamowien":
        len(df_orders) == 10,

    "Tabela zawiera 3 kolumny":
        df_orders.shape[1] == 3,

    "Identyfikatory zamowien sa unikalne":
        df_orders["order_id"].is_unique,

    "Brak wartosci NaN":
        df_orders.isna().sum().sum() == 0,

    "Tabela zawiera 5 klientow z zamowieniami":
        total_customers == 5,

    "COUNT zwraca 5 grup":
        len(df_count) == 5,

    "SUM zwraca 5 grup":
        len(df_sum) == 5,

    "AVG zwraca 5 grup":
        len(df_avg) == 5,

    "Kompletna agregacja zawiera 5 klientow":
        len(df_grouped) == 5,

    "Kazdy klient ma 2 zamowienia":
        df_count["liczba_zamowien"].eq(2).all(),

    "Suma liczby zamowien wynosi 10":
        df_count["liczba_zamowien"].sum() == 10,

    "Suma zamowien wynosi 9170 PLN":
        np.isclose(total_sales, 9170),

    "Suma zagregowanych kwot wynosi 9170 PLN":
        np.isclose(
            df_grouped["suma_zamowien"].sum(),
            9170
        ),

    "Srednia wartosc zamowienia wynosi 917 PLN":
        np.isclose(average_order, 917),

    "Mediana zamowien wynosi 820 PLN":
        np.isclose(median_order, 820),

    "Minimalna kwota wynosi 300 PLN":
        df_orders["amount"].min() == 300,

    "Maksymalna kwota wynosi 2100 PLN":
        df_orders["amount"].max() == 2100,

    "Srednia liczba zamowien na klienta wynosi 2":
        np.isclose(total_orders / total_customers, 2),

    "Najlepszy klient ma ID 5":
        best_customer["customer_id"] == 5,

    "Najlepszy klient wydal 2480 PLN":
        np.isclose(
            best_customer["suma_zamowien"], 2480
        ),

    "Srednia zamowienia klienta 5 wynosi 1240 PLN":
        np.isclose(
            best_customer["srednia_kwota"], 1240
        ),

    "Ranking jest posortowany malejaco":
        df_ranking["suma_zamowien"]
        .is_monotonic_decreasing,

    "Suma udzialow wynosi 100 procent":
        np.isclose(
            df_contribution["udzial_proc"].sum(),
            100
        ),

    "COUNT jest zgodny z kompletna agregacja":
        count_equal,

    "SUM jest zgodny z kompletna agregacja":
        sum_equal,

    "AVG jest zgodny z kompletna agregacja":
        avg_equal,

    "SQL i Pandas zwracaja identyczne wyniki":
        sql_pandas_equal,

    "Srednia jest zgodna z suma podzielona przez liczbe":
        np.allclose(
            df_grouped["srednia_kwota"],
            df_grouped["suma_zamowien"]
            / df_grouped["liczba_zamowien"]
        ),

    "Srednie nie sa mniejsze od minimum":
        (
            df_grouped["srednia_kwota"]
            >= df_grouped["minimalna_kwota"]
        ).all(),

    "Srednie nie przekraczaja maksimum":
        (
            df_grouped["srednia_kwota"]
            <= df_grouped["maksymalna_kwota"]
        ).all(),

    "Oryginalna tabela pozostala niezmieniona":
        df_original.equals(df_after)
}


for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")


passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")


# Wnioski
section("WNIOSKI")

print("""
1. GROUP BY grupuje rekordy wedlug wybranej kolumny.
2. COUNT(*) liczy rekordy w kazdej grupie.
3. SUM() oblicza sume wartosci w grupie.
4. AVG() oblicza srednia wartosc w grupie.
5. MIN() zwraca najmniejsza wartosc.
6. MAX() zwraca najwieksza wartosc.
7. Jedno zapytanie moze zawierac wiele agregacji.
8. ORDER BY pozwala tworzyc rankingi klientow.
9. GROUP BY redukuje liczbe zwracanych wierszy.
10. Agregacja SQL odpowiada operacji groupby w Pandas.
11. Agregacja w bazie ogranicza transfer danych.
12. EXPLAIN QUERY PLAN pokazuje plan zapytania.
13. GROUP BY nie modyfikuje danych zrodlowych.
14. Grupowanie tabeli orders uwzglednia tylko
    klientow posiadajacych zamowienia.
15. Aby uwzglednic klientow bez zamowien,
    nalezy wykorzystac LEFT JOIN z tabela customers.
""".strip())


# Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba zamowien: {total_orders}")
print(f"Liczba klientow: {total_customers}")
print(f"Liczba grup: {len(df_grouped)}")
print(f"Suma zamowien: {total_sales:.2f} PLN")
print(f"Srednia wartosc zamowienia: {average_order:.2f} PLN")
print(f"Najlepszy klient: {int(best_customer['customer_id'])}")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 6 wykonane poprawnie.")
