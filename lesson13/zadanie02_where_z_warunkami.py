# Lekcja 13 - Zadanie 2: WHERE z warunkami

import sqlite3
import pandas as pd


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Utworzenie bazy danych SQLite
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


# Produkty z zadania 1
products = [
    (1, "Laptop", "Elektronika", 3500.00, 10),
    (2, "Mysz", "Akcesoria", 50.00, 150),
    (3, "Klawiatura", "Akcesoria", 200.00, 80),
    (4, "Monitor", "Elektronika", 1200.00, 25),
    (5, "Słuchawki", "Akcesoria", 150.00, 60),
    (6, "Smartfon", "Elektronika", 2500.00, 30),
    (7, "Tablet", "Elektronika", 1800.00, 20),
    (8, "Pendrive", "Pamięć", 45.00, 100),
    (9, "Dysk SSD", "Pamięć", 350.00, 40),
    (10, "Drukarka", "Elektronika", 650.00, 15),
]


cursor.executemany("""
    INSERT INTO products
    VALUES (?, ?, ?, ?, ?)
""", products)

conn.commit()


print("=" * 75)
print("WHERE Z WARUNKAMI - FILTROWANIE PRODUKTOW")
print("=" * 75)


# Dane wejsciowe
section("DANE WEJSCIOWE")

df_all = pd.read_sql_query("""
    SELECT *
    FROM products
    ORDER BY product_id
""", conn)

print(df_all.to_string(index=False))
print(f"\nLiczba produktow: {len(df_all)}")


# Zapytanie 1 - produkty drozsze niz 100 PLN
section("1. PRODUKTY DROZSZE NIZ 100 PLN")

query1 = """
SELECT *
FROM products
WHERE price > 100
ORDER BY price DESC
"""

print(query1)

df_price = pd.read_sql_query(query1, conn)

print(df_price.to_string(index=False))
print(f"\nLiczba wynikow: {len(df_price)}")


# Zapytanie 2 - Elektronika LUB cena ponizej 50 PLN
section("2. ELEKTRONIKA LUB CENA PONIZEJ 50 PLN")

query2 = """
SELECT *
FROM products
WHERE category = 'Elektronika'
   OR price < 50
ORDER BY product_id
"""

print(query2)

df_or = pd.read_sql_query(query2, conn)

print(df_or.to_string(index=False))
print(f"\nLiczba wynikow: {len(df_or)}")


# Zapytanie 3 - zapas magazynowy od 10 do 50
section("3. ZAPAS MAGAZYNOWY OD 10 DO 50")

query3 = """
SELECT *
FROM products
WHERE stock BETWEEN 10 AND 50
ORDER BY stock
"""

print(query3)

df_stock = pd.read_sql_query(query3, conn)

print(df_stock.to_string(index=False))
print(f"\nLiczba wynikow: {len(df_stock)}")


# Porownanie BETWEEN z operatorami AND
section("POROWNANIE BETWEEN I AND")

query_and = """
SELECT *
FROM products
WHERE stock >= 10 AND stock <= 50
ORDER BY stock
"""

df_and = pd.read_sql_query(query_and, conn)

print("Zapytanie alternatywne:")
print(query_and)

print(
    "Czy BETWEEN i AND zwracaja identyczne wyniki:",
    df_stock.equals(df_and)
)


# Weryfikacja SQL za pomoca Pandas
section("WERYFIKACJA SQL ZA POMOCA PANDAS")

pd_price = df_all[df_all["price"] > 100]

pd_or = df_all[
    (df_all["category"] == "Elektronika")
    | (df_all["price"] < 50)
]

pd_stock = df_all[
    df_all["stock"].between(10, 50)
]


def same_results(sql_df, pandas_df):
    """Porownuje wyniki niezaleznie od kolejnosci."""
    return (
        sql_df.sort_values("product_id")
        .reset_index(drop=True)
        .equals(
            pandas_df.sort_values("product_id")
            .reset_index(drop=True)
        )
    )


print(
    "SQL vs Pandas - price > 100:",
    same_results(df_price, pd_price)
)

print(
    "SQL vs Pandas - OR:",
    same_results(df_or, pd_or)
)

print(
    "SQL vs Pandas - BETWEEN:",
    same_results(df_stock, pd_stock)
)


# Statystyki filtrowania
section("STATYSTYKI FILTROWANIA")

summary = pd.DataFrame({
    "Warunek": [
        "Wszystkie produkty",
        "Cena > 100 PLN",
        "Elektronika LUB cena < 50 PLN",
        "Stock BETWEEN 10 AND 50"
    ],
    "Liczba_produktow": [
        len(df_all),
        len(df_price),
        len(df_or),
        len(df_stock)
    ]
})

summary["Udzial_%"] = (
    summary["Liczba_produktow"]
    / len(df_all) * 100
).round(2)

print(summary.to_string(index=False))


# Tekstowy wykres liczby produktow
section("TEKSTOWY WYKRES WYNIKOW")

print("Legenda: jeden znak = jeden produkt\n")

for _, row in summary.iterrows():
    count = int(row["Liczba_produktow"])
    bar = "█" * count

    print(
        f"{row['Warunek']:<35} | "
        f"{bar:<10} "
        f"{count:>2} "
        f"({row['Udzial_%']:.2f}%)"
    )


# Dodatkowa analiza wynikow
section("ANALIZA WYNIKOW")

print(
    f"Srednia cena produktow powyzej 100 PLN: "
    f"{df_price['price'].mean():.2f} PLN"
)

print(
    f"Najdrozszy produkt: "
    f"{df_price.iloc[0]['name']}"
)

print(
    f"Suma zapasow produktow z zakresu 10-50: "
    f"{df_stock['stock'].sum()}"
)

print(
    f"Liczba produktow z kategorii Elektronika: "
    f"{(df_all['category'] == 'Elektronika').sum()}"
)

print(
    f"Liczba produktow ponizej 50 PLN: "
    f"{(df_all['price'] < 50).sum()}"
)


# Automatyczne testy
section("WERYFIKACJA")

tests = {
    "Tabela zawiera 10 produktow":
        len(df_all) == 10,

    "Tabela zawiera 5 kolumn":
        df_all.shape == (10, 5),

    "Identyfikatory sa unikalne":
        df_all["product_id"].is_unique,

    "Brak wartosci NaN":
        not df_all.isna().any().any(),

    "Cena > 100 zwraca 8 produktow":
        len(df_price) == 8,

    "Wszystkie ceny w zapytaniu 1 przekraczaja 100":
        (df_price["price"] > 100).all(),

    "Zapytanie OR zwraca 6 produktow":
        len(df_or) == 6,

    "Wszystkie produkty spelniaja warunek OR":
        (
            (df_or["category"] == "Elektronika")
            | (df_or["price"] < 50)
        ).all(),

    "BETWEEN zwraca 6 produktow":
        len(df_stock) == 6,

    "Wszystkie zapasy mieszcza sie w zakresie":
        df_stock["stock"].between(10, 50).all(),

    "BETWEEN uwzglednia dolna granice 10":
        10 in df_stock["stock"].values,

    "BETWEEN i AND sa zgodne":
        df_stock.equals(df_and),

    "SQL i Pandas - price sa zgodne":
        same_results(df_price, pd_price),

    "SQL i Pandas - OR sa zgodne":
        same_results(df_or, pd_or),

    "SQL i Pandas - stock sa zgodne":
        same_results(df_stock, pd_stock),

    "Cena 50 PLN nie spelnia warunku price < 50":
        "Mysz" not in df_or["name"].values,

    "Pendrive spelnia warunek OR":
        "Pendrive" in df_or["name"].values,

    "Laptop spelnia warunek BETWEEN":
        "Laptop" in df_stock["name"].values,

    "Ceny sa posortowane malejaco":
        df_price["price"].is_monotonic_decreasing,

    "Zapasy sa posortowane rosnaco":
        df_stock["stock"].is_monotonic_increasing,

    "Oryginalna tabela pozostala niezmieniona":
        df_all.equals(
            pd.read_sql_query(
                "SELECT * FROM products ORDER BY product_id",
                conn
            )
        )
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."


# Wnioski
section("WNIOSKI")

conclusions = [
    "WHERE filtruje rekordy wedlug warunku.",
    "Operator > oznacza scisle wiekszy.",
    "Operator < oznacza scisle mniejszy.",
    "OR wymaga spelnienia przynajmniej jednego warunku.",
    "AND wymaga spelnienia wszystkich warunkow.",
    "BETWEEN uwzglednia obie granice przedzialu.",
    "ORDER BY pozwala sortowac wyniki zapytania.",
    "SQL pozwala filtrowac dane przed wczytaniem do Pandas.",
    "Wyniki filtrowania SQL i Pandas sa zgodne.",
    "Filtrowanie ogranicza liczbe pobieranych rekordow."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


# Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba produktow: {len(df_all)}")
print(f"Produkty drozsze niz 100 PLN: {len(df_price)}")
print(f"Elektronika LUB cena < 50 PLN: {len(df_or)}")
print(f"Zapas od 10 do 50: {len(df_stock)}")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 2 wykonane poprawnie.")
