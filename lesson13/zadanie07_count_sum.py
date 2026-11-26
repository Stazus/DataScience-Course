# Lekcja 13 - Zadanie 7: COUNT i SUM

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


# Dane zgodne z zadaniem 1
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
    (10, "Drukarka", "Elektronika", 650.0, 15)
]


cursor.executemany("""
    INSERT INTO products
    (product_id, name, category, price, stock)
    VALUES (?, ?, ?, ?, ?)
""", products)

conn.commit()


print("=" * 75)
print("COUNT I SUM - ANALIZA ZAPASOW MAGAZYNOWYCH")
print("=" * 75)


section("1. DANE WEJSCIOWE")

df_products = pd.read_sql_query(
    "SELECT * FROM products ORDER BY product_id",
    conn
)

df_original = df_products.copy()

print(df_products.to_string(index=False))


section("2. LACZNA LICZBA PRODUKTOW")

query_count = """
SELECT COUNT(*) AS liczba_produktow
FROM products
"""

df_count = pd.read_sql_query(query_count, conn)

print(query_count)
print(df_count.to_string(index=False))

product_count = int(df_count.iloc[0, 0])


section("3. LACZNA WARTOSC ZAPASOW")

query_sum = """
SELECT
    SUM(stock * price) AS wartosc_zapasow
FROM products
"""

df_sum = pd.read_sql_query(query_sum, conn)

print(query_sum)
print(df_sum.to_string(index=False))

total_value = float(df_sum.iloc[0, 0])

print(f"\nWartosc magazynu: {total_value:.2f} PLN")


section("4. SREDNIA CENA W KAZDEJ KATEGORII")

query_avg = """
SELECT
    category,
    AVG(price) AS srednia_cena
FROM products
GROUP BY category
ORDER BY category
"""

df_avg = pd.read_sql_query(query_avg, conn)

print(query_avg)
print(df_avg.round(2).to_string(index=False))


section("5. WARTOSC ZAPASOW KAZDEGO PRODUKTU")

query_products_value = """
SELECT
    product_id,
    name,
    category,
    price,
    stock,
    stock * price AS wartosc_zapasow
FROM products
ORDER BY wartosc_zapasow DESC, product_id
"""

df_values = pd.read_sql_query(
    query_products_value,
    conn
)

print(query_products_value)
print(df_values.to_string(index=False))


section("6. KOMPLETNA AGREGACJA WEDLUG KATEGORII")

query_categories = """
SELECT
    category,
    COUNT(*) AS liczba_produktow,
    SUM(stock) AS liczba_sztuk,
    SUM(stock * price) AS wartosc_zapasow,
    AVG(price) AS srednia_cena,
    MIN(price) AS minimalna_cena,
    MAX(price) AS maksymalna_cena
FROM products
GROUP BY category
ORDER BY category
"""

df_categories = pd.read_sql_query(
    query_categories,
    conn
)

print(query_categories)
print(df_categories.round(2).to_string(index=False))


section("7. UDZIAL KATEGORII W WARTOSCI MAGAZYNU")

df_share = df_categories.copy()

df_share["udzial_proc"] = (
    df_share["wartosc_zapasow"]
    / total_value
    * 100
)

df_share = df_share.sort_values(
    "wartosc_zapasow",
    ascending=False
)

print(
    df_share[
        [
            "category",
            "wartosc_zapasow",
            "udzial_proc"
        ]
    ].round(2).to_string(index=False)
)

print(
    f"\nSuma udzialow: "
    f"{df_share['udzial_proc'].sum():.2f}%"
)


section("8. TEKSTOWY WYKRES WARTOSCI ZAPASOW")

print("Legenda: jeden znak = okolo 5000 PLN\n")

for _, row in df_share.iterrows():

    value = row["wartosc_zapasow"]
    bars = "█" * round(value / 5000)

    print(
        f"{row['category']:<15} | "
        f"{bars:<45} "
        f"{value:>10.2f} PLN"
    )


section("9. TEKSTOWY WYKRES SREDNICH CEN")

print("Legenda: jeden znak = okolo 50 PLN\n")

for _, row in df_avg.iterrows():

    value = row["srednia_cena"]
    bars = "█" * round(value / 50)

    print(
        f"{row['category']:<15} | "
        f"{bars:<45} "
        f"{value:>10.2f} PLN"
    )


section("10. ANALIZA STATYSTYCZNA MAGAZYNU")

total_stock = df_products["stock"].sum()

average_price = df_products["price"].mean()

weighted_average = total_value / total_stock

statistics = pd.DataFrame({
    "Metryka": [
        "Liczba produktow",
        "Liczba kategorii",
        "Laczna liczba sztuk",
        "Wartosc magazynu",
        "Srednia cena produktu",
        "Srednia cena wazona zapasem",
        "Mediana cen",
        "Minimalna cena",
        "Maksymalna cena"
    ],
    "Wartosc": [
        product_count,
        df_products["category"].nunique(),
        total_stock,
        total_value,
        average_price,
        weighted_average,
        df_products["price"].median(),
        df_products["price"].min(),
        df_products["price"].max()
    ]
})

print(statistics.round(2).to_string(index=False))


section("11. POROWNANIE COUNT(*) I SUM(stock)")

query_comparison = """
SELECT
    COUNT(*) AS liczba_produktow,
    COUNT(DISTINCT category) AS liczba_kategorii,
    SUM(stock) AS liczba_sztuk,
    SUM(stock * price) AS wartosc_magazynu
FROM products
"""

df_comparison = pd.read_sql_query(
    query_comparison,
    conn
)

print(query_comparison)
print(df_comparison.to_string(index=False))

print("\nCOUNT(*) liczy rekordy produktow.")
print("SUM(stock) liczy wszystkie sztuki w magazynie.")
print("SUM(stock * price) oblicza wartosc magazynu.")


section("12. PRODUKT O NAJWIEKSZEJ WARTOSCI ZAPASOW")

best_product = df_values.iloc[0]

print(f"Produkt: {best_product['name']}")
print(f"Cena: {best_product['price']:.2f} PLN")
print(f"Zapas: {best_product['stock']} szt.")
print(
    f"Wartosc zapasow: "
    f"{best_product['wartosc_zapasow']:.2f} PLN"
)


section("13. WERYFIKACJA SQL ZA POMOCA PANDAS")

df_pandas = df_products.copy()

df_pandas["wartosc_zapasow"] = (
    df_pandas["stock"] * df_pandas["price"]
)

pandas_count = len(df_pandas)

pandas_sum = df_pandas["wartosc_zapasow"].sum()

pandas_avg = (
    df_pandas.groupby("category")["price"]
    .mean()
    .reset_index(name="srednia_cena")
)

pandas_categories = (
    df_pandas.groupby("category")
    .agg(
        liczba_produktow=("product_id", "count"),
        liczba_sztuk=("stock", "sum"),
        wartosc_zapasow=("wartosc_zapasow", "sum"),
        srednia_cena=("price", "mean"),
        minimalna_cena=("price", "min"),
        maksymalna_cena=("price", "max")
    )
    .reset_index()
)

count_equal = product_count == pandas_count

sum_equal = np.isclose(total_value, pandas_sum)

avg_equal = (
    df_avg["category"].equals(pandas_avg["category"])
    and np.allclose(
        df_avg["srednia_cena"],
        pandas_avg["srednia_cena"]
    )
)

categories_equal = (
    df_categories["category"].equals(
        pandas_categories["category"]
    )
    and np.allclose(
        df_categories.drop(columns="category"),
        pandas_categories.drop(columns="category")
    )
)

print(pandas_categories.round(2).to_string(index=False))

print(f"\nCOUNT SQL vs Pandas: {count_equal}")
print(f"SUM SQL vs Pandas: {sum_equal}")
print(f"AVG SQL vs Pandas: {avg_equal}")
print(f"Agregacje kategorii zgodne: {categories_equal}")


section("14. EXPLAIN QUERY PLAN")

for name, query in [
    ("COUNT", query_count),
    ("SUM", query_sum),
    ("AVG i GROUP BY", query_avg)
]:

    print(f"\nPlan zapytania: {name}")

    plan = pd.read_sql_query(
        "EXPLAIN QUERY PLAN " + query,
        conn
    )

    print(plan.to_string(index=False))


section("15. AUTOMATYCZNE TESTY")

df_after = pd.read_sql_query(
    "SELECT * FROM products ORDER BY product_id",
    conn
)

expected_avg = {
    "Akcesoria": 400 / 3,
    "Elektronika": 1930.0,
    "Pamięć": 197.5
}

actual_avg = df_avg.set_index(
    "category"
)["srednia_cena"].to_dict()

tests = {
    "Tabela zawiera 10 produktow":
        len(df_products) == 10,

    "Tabela zawiera 5 kolumn":
        df_products.shape[1] == 5,

    "Identyfikatory sa unikalne":
        df_products["product_id"].is_unique,

    "Brak wartosci NaN":
        not df_products.isna().any().any(),

    "Wszystkie ceny sa dodatnie":
        (df_products["price"] > 0).all(),

    "Zapasy sa nieujemne":
        (df_products["stock"] >= 0).all(),

    "COUNT zwraca 10 produktow":
        product_count == 10,

    "Liczba kategorii wynosi 3":
        df_products["category"].nunique() == 3,

    "Laczna liczba sztuk wynosi 530":
        total_stock == 530,

    "Wartosc magazynu wynosi 236750 PLN":
        np.isclose(total_value, 236750),

    "AVG zwraca 3 kategorie":
        len(df_avg) == 3,

    "Srednia cena Akcesoriow jest poprawna":
        np.isclose(
            actual_avg["Akcesoria"],
            expected_avg["Akcesoria"]
        ),

    "Srednia cena Elektroniki wynosi 1930":
        np.isclose(
            actual_avg["Elektronika"],
            expected_avg["Elektronika"]
        ),

    "Srednia cena Pamieci wynosi 197.5":
        np.isclose(
            actual_avg["Pamięć"],
            expected_avg["Pamięć"]
        ),

    "Suma wartosci poszczegolnych produktow jest zgodna":
        np.isclose(
            df_values["wartosc_zapasow"].sum(),
            total_value
        ),

    "Suma wartosci kategorii jest zgodna":
        np.isclose(
            df_categories["wartosc_zapasow"].sum(),
            total_value
        ),

    "Suma liczby produktow w kategoriach wynosi 10":
        df_categories["liczba_produktow"].sum() == 10,

    "Suma sztuk w kategoriach wynosi 530":
        df_categories["liczba_sztuk"].sum() == 530,

    "Suma udzialow wynosi 100 procent":
        np.isclose(df_share["udzial_proc"].sum(), 100),

    "Wszystkie udzialy sa nieujemne":
        (df_share["udzial_proc"] >= 0).all(),

    "Najwieksza wartosc zapasow dotyczy Smartfona":
        best_product["name"] == "Smartfon",

    "Najwieksza wartosc zapasow wynosi 75000":
        np.isclose(
            best_product["wartosc_zapasow"],
            75000
        ),

    "COUNT SQL i Pandas sa zgodne":
        count_equal,

    "SUM SQL i Pandas sa zgodne":
        sum_equal,

    "AVG SQL i Pandas sa zgodne":
        avg_equal,

    "Agregacje kategorii SQL i Pandas sa zgodne":
        categories_equal,

    "Srednie cen nie sa mniejsze od minimum":
        (
            df_categories["srednia_cena"]
            >= df_categories["minimalna_cena"]
        ).all(),

    "Srednie cen nie przekraczaja maksimum":
        (
            df_categories["srednia_cena"]
            <= df_categories["maksymalna_cena"]
        ).all(),

    "Wartosci zapasow sa posortowane malejaco":
        df_values["wartosc_zapasow"].is_monotonic_decreasing,

    "Oryginalna tabela pozostala niezmieniona":
        df_original.equals(df_after)
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")


section("WNIOSKI")

conclusions = [
    "COUNT(*) liczy wszystkie rekordy w tabeli.",
    "COUNT(DISTINCT category) liczy unikalne kategorie.",
    "SUM(stock) oblicza laczna liczbe sztuk.",
    "SUM(stock * price) oblicza wartosc magazynu.",
    "SUM moze agregowac wynik wyrazenia matematycznego.",
    "AVG(price) oblicza srednia arytmetyczna cen.",
    "GROUP BY pozwala agregowac dane wedlug kategorii.",
    "MIN i MAX okreslaja zakres cen w kategorii.",
    "Srednia wazona uwzglednia liczbe sztuk produktu.",
    "Srednia wazona rozni sie od sredniej arytmetycznej.",
    "SQL i Pandas pozwalaja uzyskac zgodne agregacje.",
    "Agregacja w SQL ogranicza transfer danych.",
    "EXPLAIN QUERY PLAN pokazuje sposob wykonania zapytania.",
    "Agregacje nie modyfikuja danych zrodlowych."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba produktow: {product_count}")
print(f"Liczba kategorii: {len(df_categories)}")
print(f"Laczna liczba sztuk: {total_stock}")
print(f"Wartosc magazynu: {total_value:.2f} PLN")
print(f"Srednia cena produktu: {average_price:.2f} PLN")
print(f"Srednia cena wazona: {weighted_average:.2f} PLN")
print(f"Najcenniejszy zapas: {best_product['name']}")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 7 wykonane poprawnie.")
