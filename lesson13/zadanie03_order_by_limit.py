# Lekcja 13 - Zadanie 3: ORDER BY i LIMIT

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


# Dane zgodne z zadaniami 1 i 2
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
    (10, "Drukarka", "Elektronika", 650.00, 15)
]


# Wstawienie danych
cursor.executemany("""
    INSERT INTO products
    (product_id, name, category, price, stock)
    VALUES (?, ?, ?, ?, ?)
""", products)

conn.commit()


print("=" * 75)
print("ORDER BY I LIMIT - SORTOWANIE PRODUKTOW")
print("=" * 75)


section("DANE WEJSCIOWE")

df = pd.read_sql_query(
    "SELECT * FROM products ORDER BY product_id",
    conn
)

df_original = df.copy()

print(df.to_string(index=False))
print(f"\nLiczba produktow: {len(df)}")


# ============================================================
# 1. TOP 5 NAJDROZSZYCH PRODUKTOW
# ============================================================

section("1. TOP 5 NAJDROZSZYCH PRODUKTOW")

query_top_price = """
SELECT *
FROM products
ORDER BY price DESC, product_id ASC
LIMIT 5
"""

print(query_top_price)

top_price = pd.read_sql_query(
    query_top_price,
    conn
)

print(top_price.to_string(index=False))

print(f"\nLiczba wynikow: {len(top_price)}")
print(f"Najwyzsza cena: {top_price['price'].max():.2f} PLN")
print(f"Najnizsza cena w TOP 5: {top_price['price'].min():.2f} PLN")
print(f"Srednia cena TOP 5: {top_price['price'].mean():.2f} PLN")


# ============================================================
# 2. TOP 5 PRODUKTOW Z NAJMNIEJSZYM ZAPASEM
# ============================================================

section("2. TOP 5 PRODUKTOW Z NAJMNIEJSZYM ZAPASEM")

query_low_stock = """
SELECT *
FROM products
ORDER BY stock ASC, product_id ASC
LIMIT 5
"""

print(query_low_stock)

low_stock = pd.read_sql_query(
    query_low_stock,
    conn
)

print(low_stock.to_string(index=False))

print(f"\nLiczba wynikow: {len(low_stock)}")
print(f"Minimalny zapas: {low_stock['stock'].min()}")
print(f"Maksymalny zapas w TOP 5: {low_stock['stock'].max()}")
print(f"Suma zapasow: {low_stock['stock'].sum()}")


# ============================================================
# 3. SORTOWANIE ALFABETYCZNE
# ============================================================

section("3. PRODUKTY POSORTOWANE ALFABETYCZNIE")

query_alphabetical = """
SELECT *
FROM products
ORDER BY name ASC, product_id ASC
"""

print(query_alphabetical)

alphabetical = pd.read_sql_query(
    query_alphabetical,
    conn
)

print(alphabetical.to_string(index=False))

print(f"\nLiczba wynikow: {len(alphabetical)}")
print(f"Pierwszy produkt: {alphabetical.iloc[0]['name']}")
print(f"Ostatni produkt: {alphabetical.iloc[-1]['name']}")


# ============================================================
# 4. POROWNANIE ASC I DESC
# ============================================================

section("POROWNANIE ASC I DESC")

ascending = pd.read_sql_query("""
    SELECT name, price
    FROM products
    ORDER BY price ASC, product_id ASC
""", conn)

descending = pd.read_sql_query("""
    SELECT name, price
    FROM products
    ORDER BY price DESC, product_id ASC
""", conn)

comparison = pd.DataFrame({
    "ASC_produkt": ascending["name"],
    "ASC_cena": ascending["price"],
    "DESC_produkt": descending["name"],
    "DESC_cena": descending["price"]
})

print(comparison.to_string(index=False))


# ============================================================
# 5. WERYFIKACJA ZA POMOCA PANDAS
# ============================================================

section("WERYFIKACJA SQL ZA POMOCA PANDAS")

pandas_top_price = (
    df.sort_values(
        ["price", "product_id"],
        ascending=[False, True]
    )
    .head(5)
    .reset_index(drop=True)
)

pandas_low_stock = (
    df.sort_values(
        ["stock", "product_id"],
        ascending=[True, True]
    )
    .head(5)
    .reset_index(drop=True)
)

pandas_alphabetical = (
    df.sort_values(
        ["name", "product_id"]
    )
    .reset_index(drop=True)
)

price_match = top_price.equals(pandas_top_price)
stock_match = low_stock.equals(pandas_low_stock)
name_match = alphabetical.equals(pandas_alphabetical)

print(f"SQL vs Pandas - TOP 5 cen: {price_match}")
print(f"SQL vs Pandas - TOP 5 zapasow: {stock_match}")
print(f"SQL vs Pandas - nazwy: {name_match}")


# ============================================================
# 6. ANALIZA STATYSTYCZNA
# ============================================================

section("ANALIZA STATYSTYCZNA")

statistics = pd.DataFrame({
    "Metryka": [
        "Liczba produktow",
        "Srednia cena",
        "Mediana ceny",
        "Minimalna cena",
        "Maksymalna cena",
        "Suma zapasow",
        "Sredni zapas"
    ],
    "Wartosc": [
        len(df),
        df["price"].mean(),
        df["price"].median(),
        df["price"].min(),
        df["price"].max(),
        df["stock"].sum(),
        df["stock"].mean()
    ]
})

print(statistics.round(2).to_string(index=False))


section("ANALIZA TOP 5 NAJDROZSZYCH PRODUKTOW")

total_prices = df["price"].sum()
top_prices_sum = top_price["price"].sum()

price_share = top_prices_sum / total_prices * 100

print(f"Suma cen wszystkich produktow: {total_prices:.2f} PLN")
print(f"Suma cen TOP 5: {top_prices_sum:.2f} PLN")
print(f"Udzial TOP 5 w sumie cen: {price_share:.2f}%")

print(
    f"Srednia cena wszystkich produktow: "
    f"{df['price'].mean():.2f} PLN"
)

print(
    f"Srednia cena TOP 5: "
    f"{top_price['price'].mean():.2f} PLN"
)


section("ANALIZA PRODUKTOW Z NAJMNIEJSZYM ZAPASEM")

total_stock = df["stock"].sum()
low_stock_sum = low_stock["stock"].sum()

stock_share = low_stock_sum / total_stock * 100

print(f"Calkowity zapas: {total_stock}")
print(f"Zapas 5 produktow: {low_stock_sum}")
print(f"Udzial w calkowitym zapasie: {stock_share:.2f}%")


# ============================================================
# 7. TEKSTOWE WYKRESY
# ============================================================

section("TEKSTOWY WYKRES TOP 5 CEN")

print("Legenda: jeden znak = okolo 100 PLN\n")

for row in top_price.itertuples(index=False):
    bar = "█" * round(row.price / 100)

    print(
        f"{row.name:<15} | "
        f"{bar:<35} "
        f"{row.price:>8.2f} PLN"
    )


section("TEKSTOWY WYKRES NAJMNIEJSZYCH ZAPASOW")

print("Legenda: jeden znak = jedna sztuka\n")

for row in low_stock.itertuples(index=False):
    bar = "█" * int(row.stock)

    print(
        f"{row.name:<15} | "
        f"{bar:<30} "
        f"{row.stock:>3}"
    )


# ============================================================
# 8. DODATKOWE PRZYKLADY LIMIT I OFFSET
# ============================================================

section("DODATKOWY PRZYKLAD - LIMIT I OFFSET")

query_offset = """
SELECT name, price
FROM products
ORDER BY price DESC, product_id ASC
LIMIT 3 OFFSET 5
"""

print(query_offset)

offset_result = pd.read_sql_query(
    query_offset,
    conn
)

print(offset_result.to_string(index=False))

print("\nOFFSET 5 pomija pierwszych 5 rekordow.")
print("LIMIT 3 zwraca kolejne 3 rekordy.")


section("POROWNANIE LIMIT 1 Z MAX")

most_expensive = pd.read_sql_query("""
    SELECT *
    FROM products
    ORDER BY price DESC, product_id ASC
    LIMIT 1
""", conn)

max_price = pd.read_sql_query("""
    SELECT MAX(price) AS max_price
    FROM products
""", conn)

print(most_expensive.to_string(index=False))

print(
    f"\nMAX(price): "
    f"{max_price.iloc[0]['max_price']:.2f} PLN"
)

print(
    "Zgodnosc ORDER BY LIMIT 1 i MAX:",
    np.isclose(
        most_expensive.iloc[0]["price"],
        max_price.iloc[0]["max_price"]
    )
)


# ============================================================
# 9. AUTOMATYCZNE TESTY
# ============================================================

section("WERYFIKACJA")

df_after = pd.read_sql_query(
    "SELECT * FROM products ORDER BY product_id",
    conn
)

tests = {
    "Tabela zawiera 10 produktow":
        len(df) == 10,

    "Tabela zawiera 5 kolumn":
        df.shape == (10, 5),

    "Identyfikatory sa unikalne":
        df["product_id"].is_unique,

    "Brak wartosci NaN":
        not df.isna().any().any(),

    "TOP cen zawiera 5 produktow":
        len(top_price) == 5,

    "TOP zapasow zawiera 5 produktow":
        len(low_stock) == 5,

    "Sortowanie alfabetyczne zawiera 10 produktow":
        len(alphabetical) == 10,

    "Ceny sa posortowane malejaco":
        top_price["price"].is_monotonic_decreasing,

    "Zapasy sa posortowane rosnaco":
        low_stock["stock"].is_monotonic_increasing,

    "Nazwy sa posortowane rosnaco":
        alphabetical["name"].is_monotonic_increasing,

    "Najdrozszy produkt to Laptop":
        top_price.iloc[0]["name"] == "Laptop",

    "Najwyzsza cena wynosi 3500":
        np.isclose(top_price.iloc[0]["price"], 3500),

    "Piaty najdrozszy produkt to Drukarka":
        top_price.iloc[-1]["name"] == "Drukarka",

    "Minimalny zapas wynosi 10":
        low_stock.iloc[0]["stock"] == 10,

    "Piaty najmniejszy zapas wynosi 30":
        low_stock.iloc[-1]["stock"] == 30,

    "Suma najmniejszych zapasow wynosi 100":
        low_stock["stock"].sum() == 100,

    "Pierwszy alfabetycznie jest produkt Drukarka":
        alphabetical.iloc[0]["name"] == "Drukarka",

    "Ostatni alfabetycznie jest produkt Tablet":
        alphabetical.iloc[-1]["name"] == "Tablet",

    "SQL i Pandas - ceny sa zgodne":
        price_match,

    "SQL i Pandas - zapasy sa zgodne":
        stock_match,

    "SQL i Pandas - nazwy sa zgodne":
        name_match,

    "LIMIT z OFFSET zwraca 3 rekordy":
        len(offset_result) == 3,

    "OFFSET zwraca poprawne produkty":
        offset_result["name"].tolist()
        == descending.iloc[5:8]["name"].tolist(),

    "LIMIT 1 i MAX zwracaja zgodna cene":
        np.isclose(
            most_expensive.iloc[0]["price"],
            max_price.iloc[0]["max_price"]
        ),

    "ASC sortuje ceny rosnaco":
        ascending["price"].is_monotonic_increasing,

    "DESC sortuje ceny malejaco":
        descending["price"].is_monotonic_decreasing,

    "TOP 5 nie zawiera duplikatow":
        top_price["product_id"].is_unique,

    "Oryginalna tabela pozostala niezmieniona":
        df_original.equals(df_after)
}

for name, result in tests.items():
    print(f"Czy {name}: {result}")

passed = sum(bool(result) for result in tests.values())
total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")


# ============================================================
# 10. WNIOSKI
# ============================================================

section("WNIOSKI")

conclusions = [
    "ORDER BY sortuje wyniki zapytania SQL.",
    "ASC oznacza sortowanie rosnace.",
    "DESC oznacza sortowanie malejace.",
    "LIMIT ogranicza liczbe zwracanych rekordow.",
    "OFFSET pozwala pominac okreslona liczbe rekordow.",
    "ORDER BY i LIMIT pozwalaja tworzyc rankingi TOP N.",
    "Dodatkowe sortowanie po ID rozstrzyga remisy.",
    "Sortowanie tekstu zalezy od reguly porownywania znakow.",
    "SQL i Pandas pozwalaja uzyskac zgodne wyniki.",
    "LIMIT zmniejsza liczbe rekordow przesylanych do aplikacji.",
    "LIMIT nie zawsze eliminuje koszt sortowania w bazie.",
    "Sortowanie nie modyfikuje danych w tabeli."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


# ============================================================
# 11. PODSUMOWANIE
# ============================================================

section("PODSUMOWANIE")

print(f"Liczba produktow: {len(df)}")
print(f"Liczba najdrozszych produktow: {len(top_price)}")
print(f"Liczba produktow z najmniejszym zapasem: {len(low_stock)}")
print(f"Liczba produktow alfabetycznie: {len(alphabetical)}")
print(f"Najdrozszy produkt: {top_price.iloc[0]['name']}")
print(f"Najmniejszy zapas: {low_stock.iloc[0]['stock']}")
print(f"Zaliczone testy: {passed}/{total}")

conn.close()

assert passed == total, "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 3 wykonane poprawnie.")
