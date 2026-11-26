# Lekcja 13 - Zadanie 12: Subquery (podzapytanie)

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


# Utworzenie tabeli products
cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
""")


# Dane produktow z poprzednich zadan
products = [
    (1, "Laptop", "Elektronika", 3500.0, 10),
    (2, "Mysz", "Akcesoria", 50.0, 150),
    (3, "Klawiatura", "Akcesoria", 200.0, 80),
    (4, "Monitor", "Elektronika", 1200.0, 25),
    (5, "Słuchawki", "Akcesoria", 150.0, 60),
    (6, "Smartfon", "Elektronika", 2500.0, 30),
    (7, "Tablet", "Elektronika", 1800.0, 20),
    (8, "Pendrive", "Pamięć", 45.0, 100),
    (9, "Dysk SSD", "Pamięć", 350.0, 40),
    (10, "Drukarka", "Elektronika", 650.0, 15),
]

cursor.executemany("""
    INSERT INTO products
    VALUES (?, ?, ?, ?, ?)
""", products)

conn.commit()


print("=" * 75)
print("SUBQUERY - PRODUKTY DROZSZE OD SREDNIEJ")
print("=" * 75)


# 1. Dane wejsciowe
section("1. DANE WEJSCIOWE")

df_products = pd.read_sql_query("""
    SELECT *
    FROM products
    ORDER BY product_id
""", conn)

print(df_products.to_string(index=False))
print(f"\nLiczba produktow: {len(df_products)}")


# 2. Obliczenie sredniej ceny
section("2. SREDNIA CENA WSZYSTKICH PRODUKTOW")

query_avg = """
SELECT AVG(price) AS avg_price
FROM products
"""

print(query_avg)

df_avg = pd.read_sql_query(query_avg, conn)
avg_price = df_avg.loc[0, "avg_price"]

print(f"Srednia cena: {avg_price:.2f} PLN")


# 3. Podstawowe podzapytanie
section("3. PRODUKTY DROZSZE OD SREDNIEJ")

query_subquery = """
SELECT
    name,
    price
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
)
ORDER BY price DESC, product_id ASC
"""

print(query_subquery)

df_above = pd.read_sql_query(query_subquery, conn)

print(df_above.to_string(index=False))
print(f"\nLiczba produktow: {len(df_above)}")


# 4. Roznica kwotowa i procentowa
section("4. ROZNICA OD SREDNIEJ - PLN I PROCENTY")

query_difference = """
SELECT
    name,
    price,
    (SELECT AVG(price) FROM products) AS avg_price,
    price - (
        SELECT AVG(price) FROM products
    ) AS difference,
    100.0 * (
        price - (SELECT AVG(price) FROM products)
    ) / NULLIF(
        (SELECT AVG(price) FROM products), 0
    ) AS difference_pct
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
)
ORDER BY price DESC, product_id ASC
"""

print(query_difference)

df_result = pd.read_sql_query(query_difference, conn)

print(
    df_result.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)


# 5. Analiza statystyczna
section("5. ANALIZA STATYSTYCZNA")

df_stats = pd.read_sql_query("""
    SELECT
        COUNT(*) AS liczba_produktow,
        SUM(price) AS suma_cen,
        AVG(price) AS srednia_cena,
        MIN(price) AS minimalna_cena,
        MAX(price) AS maksymalna_cena
    FROM products
""", conn)

print(df_stats.T.to_string(header=False))

print(
    f"\nMediana cen: "
    f"{df_products['price'].median():.2f} PLN"
)

above_count = len(df_result)
total_count = len(df_products)
below_count = int((df_products["price"] < avg_price).sum())
equal_count = int((df_products["price"] == avg_price).sum())

above_pct = above_count / total_count * 100

print(f"Produkty powyzej sredniej: {above_count}")
print(f"Produkty ponizej sredniej: {below_count}")
print(f"Produkty rowne sredniej: {equal_count}")
print(f"Udzial produktow powyzej sredniej: {above_pct:.2f}%")


# 6. Porownanie wszystkich produktow ze srednia
section("6. KLASYFIKACJA PRODUKTOW WEDLUG CENY")

query_classification = """
SELECT
    name,
    price,
    CASE
        WHEN price > (SELECT AVG(price) FROM products)
            THEN 'Powyzej sredniej'
        WHEN price < (SELECT AVG(price) FROM products)
            THEN 'Ponizej sredniej'
        ELSE 'Rowna sredniej'
    END AS klasyfikacja
FROM products
ORDER BY price DESC, product_id ASC
"""

df_classification = pd.read_sql_query(
    query_classification, conn
)

print(df_classification.to_string(index=False))


# 7. Tekstowy wykres roznic procentowych
section("7. TEKSTOWY WYKRES - PROCENT POWYZEJ SREDNIEJ")

print("Legenda: jeden znak = okolo 10 punktow procentowych\n")

for row in df_result.itertuples(index=False):
    bar = "█" * round(row.difference_pct / 10)

    print(
        f"{row.name:<15} | "
        f"{bar:<25} "
        f"+{row.difference_pct:>7.2f}%"
    )


# 8. Alternatywne rozwiazanie za pomoca CTE
section("8. ALTERNATYWNE ROZWIAZANIE - CTE")

query_cte = """
WITH average_price AS (
    SELECT AVG(price) AS avg_price
    FROM products
)
SELECT
    p.name,
    p.price,
    a.avg_price,
    p.price - a.avg_price AS difference,
    100.0 * (p.price - a.avg_price)
        / NULLIF(a.avg_price, 0) AS difference_pct
FROM products AS p
CROSS JOIN average_price AS a
WHERE p.price > a.avg_price
ORDER BY p.price DESC, p.product_id ASC
"""

print(query_cte)

df_cte = pd.read_sql_query(query_cte, conn)

print(
    df_cte.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)

cte_match = (
    df_result["name"].equals(df_cte["name"])
    and np.allclose(
        df_result.select_dtypes(include="number"),
        df_cte.select_dtypes(include="number")
    )
)

print(f"\nCzy Subquery i CTE sa zgodne: {cte_match}")


# 9. Weryfikacja za pomoca Pandas
section("9. WERYFIKACJA SQL ZA POMOCA PANDAS")

pandas_avg = df_products["price"].mean()

df_pandas = df_products.loc[
    df_products["price"] > pandas_avg,
    ["product_id", "name", "price"]
].copy()

df_pandas["avg_price"] = pandas_avg

df_pandas["difference"] = (
    df_pandas["price"] - pandas_avg
)

df_pandas["difference_pct"] = (
    df_pandas["difference"] / pandas_avg * 100
)

df_pandas = (
    df_pandas
    .sort_values(
        ["price", "product_id"],
        ascending=[False, True]
    )
    .drop(columns="product_id")
    .reset_index(drop=True)
)

print(
    df_pandas.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)

pandas_match = (
    df_result["name"].equals(df_pandas["name"])
    and np.allclose(
        df_result.select_dtypes(include="number"),
        df_pandas.select_dtypes(include="number")
    )
)

print(f"\nCzy SQL i Pandas sa zgodne: {pandas_match}")


# 10. Plan wykonania zapytania
section("10. EXPLAIN QUERY PLAN")

df_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_subquery,
    conn
)

print(df_plan.to_string(index=False))


# 11. Automatyczne testy
section("11. WERYFIKACJA")

df_after = pd.read_sql_query("""
    SELECT *
    FROM products
    ORDER BY product_id
""", conn)

tests = {
    "Tabela zawiera 10 produktow":
        len(df_products) == 10,

    "Tabela zawiera 5 kolumn":
        df_products.shape[1] == 5,

    "Identyfikatory sa unikalne":
        df_products["product_id"].is_unique,

    "Brak brakujacych danych":
        not df_products.isna().any().any(),

    "Srednia cena wynosi 1044.50 PLN":
        np.isclose(avg_price, 1044.50),

    "Suma cen wynosi 10445 PLN":
        np.isclose(df_products["price"].sum(), 10445),

    "Podzapytanie zwraca 4 produkty":
        len(df_above) == 4,

    "Wynik zawiera 5 kolumn":
        df_result.shape[1] == 5,

    "Wszystkie ceny przekraczaja srednia":
        (df_result["price"] > avg_price).all(),

    "Wszystkie roznice sa dodatnie":
        (df_result["difference"] > 0).all(),

    "Wszystkie roznice procentowe sa dodatnie":
        (df_result["difference_pct"] > 0).all(),

    "Ceny sa posortowane malejaco":
        df_result["price"].is_monotonic_decreasing,

    "Najdrozszy produkt to Laptop":
        df_result.iloc[0]["name"] == "Laptop",

    "Najwyzsza cena wynosi 3500 PLN":
        np.isclose(df_result.iloc[0]["price"], 3500),

    "Roznica ceny Laptopa wynosi 2455.50 PLN":
        np.isclose(
            df_result.iloc[0]["difference"], 2455.50
        ),

    "Ostatni produkt to Monitor":
        df_result.iloc[-1]["name"] == "Monitor",

    "Roznica ceny Monitora wynosi 155.50 PLN":
        np.isclose(
            df_result.iloc[-1]["difference"], 155.50
        ),

    "Lista produktow jest poprawna":
        df_result["name"].tolist() == [
            "Laptop", "Smartfon", "Tablet", "Monitor"
        ],

    "Udzial produktow powyzej sredniej wynosi 40%":
        np.isclose(above_pct, 40),

    "Szesc produktow znajduje sie ponizej sredniej":
        below_count == 6,

    "Brak produktow rownych sredniej":
        equal_count == 0,

    "Klasyfikacja obejmuje wszystkie produkty":
        len(df_classification) == total_count,

    "Suma liczebnosci grup jest poprawna":
        above_count + below_count + equal_count == total_count,

    "Roznice kwotowe obliczono poprawnie":
        np.allclose(
            df_result["difference"],
            df_result["price"] - avg_price
        ),

    "Roznice procentowe obliczono poprawnie":
        np.allclose(
            df_result["difference_pct"],
            (df_result["price"] - avg_price)
            / avg_price * 100
        ),

    "Srednia SQL i Pandas jest zgodna":
        np.isclose(avg_price, pandas_avg),

    "Subquery i CTE zwracaja zgodne wyniki":
        cte_match,

    "SQL i Pandas zwracaja zgodne wyniki":
        pandas_match,

    "Plan wykonania zawiera podzapytanie":
        df_plan["detail"].str.contains(
            "SUBQUERY", case=False
        ).any(),

    "Oryginalna tabela pozostala niezmieniona":
        df_products.equals(df_after),
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())
total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")


# 12. Wnioski
section("12. WNIOSKI")

conclusions = [
    "Subquery to zapytanie zagniezdzone w innym zapytaniu.",
    "AVG(price) oblicza srednia cene wszystkich produktow.",
    "Podzapytanie moze dostarczyc wartosc dla WHERE.",
    "Operator > wybiera produkty scisle drozsze od sredniej.",
    "Podzapytania mozna stosowac takze w SELECT.",
    "Roznica kwotowa pokazuje odchylenie ceny od sredniej.",
    "Roznica procentowa ulatwia porownywanie cen.",
    "NULLIF zabezpiecza przed dzieleniem przez zero.",
    "CASE pozwala klasyfikowac rekordy.",
    "CTE pozwala zapisac obliczenie sredniej w jednym miejscu.",
    "EXPLAIN QUERY PLAN pokazuje sposob wykonania zapytania.",
    "SQL i Pandas pozwalaja uzyskac zgodne wyniki.",
    "Podzapytanie nie modyfikuje danych zrodlowych.",
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


# 13. Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba produktow: {total_count}")
print(f"Srednia cena: {avg_price:.2f} PLN")
print(f"Produkty powyzej sredniej: {above_count}")
print(f"Produkty ponizej sredniej: {below_count}")
print(f"Udzial produktow powyzej sredniej: {above_pct:.2f}%")
print(f"Najdrozszy produkt: {df_result.iloc[0]['name']}")
print(f"Zaliczone testy: {passed}/{total}")

conn.close()

assert passed == total, "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 12 wykonane poprawnie.")
