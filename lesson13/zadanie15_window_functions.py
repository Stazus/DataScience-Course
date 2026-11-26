# Lekcja 13 - Zadanie 15: Window Functions (zaawansowane)

import sqlite3
import time
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 90)


start_time = time.perf_counter()

# Konfiguracja generatora losowego
np.random.seed(42)

# Utworzenie bazy SQLite
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")


# ============================================================
# 1. UTWORZENIE TABEL
# ============================================================

cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        revenue REAL NOT NULL,
        FOREIGN KEY (product_id)
            REFERENCES products(product_id)
    )
""")


# ============================================================
# 2. DANE PRODUKTOW
# ============================================================

products = [
    (1, "Laptop", "Elektronika", 3500),
    (2, "Smartfon", "Elektronika", 2500),
    (3, "Tablet", "Elektronika", 1800),
    (4, "Monitor", "Elektronika", 1200),
    (5, "Drukarka", "Elektronika", 650),

    (6, "Mysz", "Akcesoria", 50),
    (7, "Klawiatura", "Akcesoria", 200),
    (8, "Sluchawki", "Akcesoria", 150),
    (9, "Kamera", "Akcesoria", 250),
    (10, "Mikrofon", "Akcesoria", 300),

    (11, "Dysk SSD", "Pamiec", 350),
    (12, "Dysk HDD", "Pamiec", 250),
    (13, "Pendrive", "Pamiec", 45),
    (14, "Karta SD", "Pamiec", 80),
    (15, "RAM", "Pamiec", 400),

    (16, "Biurko", "Meble", 800),
    (17, "Fotel", "Meble", 1200),
    (18, "Szafka", "Meble", 500),
    (19, "Regal", "Meble", 450),
    (20, "Stolik", "Meble", 300)
]

cursor.executemany("""
    INSERT INTO products
    VALUES (?, ?, ?, ?)
""", products)


# ============================================================
# 3. GENEROWANIE 1000 TRANSAKCJI
# ============================================================

N = 1000

product_ids = np.random.randint(1, 21, size=N)
quantities = np.random.randint(1, 6, size=N)

price_map = {
    product_id: price
    for product_id, product, category, price in products
}

sales = []

for sale_id, (product_id, quantity) in enumerate(
    zip(product_ids, quantities), start=1
):
    product_id = int(product_id)
    quantity = int(quantity)

    revenue = quantity * price_map[product_id]

    sales.append((
        sale_id,
        product_id,
        quantity,
        revenue
    ))

cursor.executemany("""
    INSERT INTO sales
    VALUES (?, ?, ?, ?)
""", sales)

conn.commit()


# ============================================================
# 4. DANE WEJSCIOWE
# ============================================================

section("WINDOW FUNCTIONS - RANKING PRODUKTOW")

section("1. TABELA PRODUCTS")

df_products = pd.read_sql_query("""
    SELECT *
    FROM products
    ORDER BY product_id
""", conn)

print(df_products.to_string(index=False))

section("2. TABELA SALES - PIERWSZE 10 TRANSAKCJI")

df_sales = pd.read_sql_query("""
    SELECT *
    FROM sales
    ORDER BY sale_id
""", conn)

print(df_sales.head(10).to_string(index=False))

print(f"\nLiczba produktow: {len(df_products)}")
print(f"Liczba kategorii: {df_products['category'].nunique()}")
print(f"Liczba transakcji: {len(df_sales)}")
print(f"Laczny przychod: {df_sales['revenue'].sum():,.2f} PLN")


# ============================================================
# 5. AGREGACJA SPRZEDAZY
# ============================================================

section("3. AGREGACJA SPRZEDAZY WEDLUG PRODUKTU")

query_aggregation = """
SELECT
    p.product_id,
    p.category,
    p.product,
    COUNT(s.sale_id) AS transactions,
    SUM(s.quantity) AS quantity,
    SUM(s.revenue) AS revenue
FROM products AS p
INNER JOIN sales AS s
    ON p.product_id = s.product_id
GROUP BY
    p.product_id,
    p.category,
    p.product
"""

df_aggregation = pd.read_sql_query(
    query_aggregation,
    conn
)

print(
    df_aggregation.sort_values(
        "revenue", ascending=False
    ).to_string(index=False)
)


# ============================================================
# 6. FUNKCJA RANK()
# ============================================================

section("4. RANK - RANKING W KATEGORIACH")

query_rank = f"""
WITH product_sales AS (
    {query_aggregation}
)
SELECT
    category,
    product,
    revenue,
    RANK() OVER (
        PARTITION BY category
        ORDER BY revenue DESC
    ) AS category_rank
FROM product_sales
ORDER BY category, category_rank, product
"""

print(query_rank)

df_rank = pd.read_sql_query(query_rank, conn)

print(df_rank.to_string(index=False))


# ============================================================
# 7. ROW_NUMBER I DENSE_RANK
# ============================================================

section("5. POROWNANIE FUNKCJI OKIENKOWYCH")

query_windows = f"""
WITH product_sales AS (
    {query_aggregation}
)
SELECT
    category,
    product_id,
    product,
    revenue,

    RANK() OVER (
        PARTITION BY category
        ORDER BY revenue DESC
    ) AS category_rank,

    DENSE_RANK() OVER (
        PARTITION BY category
        ORDER BY revenue DESC
    ) AS dense_rank,

    ROW_NUMBER() OVER (
        PARTITION BY category
        ORDER BY revenue DESC, product_id ASC
    ) AS row_number

FROM product_sales
"""

df_windows = pd.read_sql_query(
    query_windows + """
    ORDER BY category, row_number
    """,
    conn
)

print(df_windows.to_string(index=False))


# ============================================================
# 8. TOP 3 PRODUKTOW W KAZDEJ KATEGORII
# ============================================================

section("6. TOP 3 PRODUKTOW - RANK")

query_top3_rank = f"""
WITH ranked_products AS (
    {query_windows}
)
SELECT
    category,
    product,
    revenue,
    category_rank
FROM ranked_products
WHERE category_rank <= 3
ORDER BY category, category_rank, product_id
"""

df_top3_rank = pd.read_sql_query(
    query_top3_rank,
    conn
)

print(df_top3_rank.to_string(index=False))


section("7. TOP 3 PRODUKTOW - ROW_NUMBER")

query_top3 = f"""
WITH ranked_products AS (
    {query_windows}
)
SELECT
    category,
    product,
    revenue,
    category_rank,
    row_number
FROM ranked_products
WHERE row_number <= 3
ORDER BY category, row_number
"""

print(query_top3)

df_top3 = pd.read_sql_query(query_top3, conn)

print(df_top3.to_string(index=False))

print(f"\nLiczba produktow TOP 3: {len(df_top3)}")


# ============================================================
# 9. ANALIZA POSZCZEGOLNYCH KATEGORII
# ============================================================

section("8. ANALIZA KATEGORII")

category_stats = df_aggregation.groupby(
    "category"
).agg(
    products=("product", "count"),
    transactions=("transactions", "sum"),
    quantity=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
    avg_revenue=("revenue", "mean")
).reset_index()

category_stats["revenue_share_pct"] = (
    category_stats["total_revenue"]
    / category_stats["total_revenue"].sum()
    * 100
)

category_stats = category_stats.sort_values(
    "total_revenue",
    ascending=False
)

print(
    category_stats.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)


# ============================================================
# 10. UDZIAL TOP 3 W PRZYCHODACH KATEGORII
# ============================================================

section("9. UDZIAL TOP 3 W PRZYCHODACH KATEGORII")

top3_summary = df_top3.groupby(
    "category"
)["revenue"].sum().rename("top3_revenue")

category_revenue = df_aggregation.groupby(
    "category"
)["revenue"].sum().rename("category_revenue")

contribution = pd.concat(
    [top3_summary, category_revenue],
    axis=1
).reset_index()

contribution["top3_share_pct"] = (
    contribution["top3_revenue"]
    / contribution["category_revenue"]
    * 100
)

print(
    contribution.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)


# ============================================================
# 11. TEKSTOWA WIZUALIZACJA
# ============================================================

section("10. TEKSTOWY RANKING TOP 3")

print("Legenda: 1 znak = okolo 10 000 PLN")

for category, group in df_top3.groupby("category"):

    print(f"\nKATEGORIA: {category}")
    print("-" * 90)

    for row in group.itertuples(index=False):

        bar_length = max(
            1,
            round(row.revenue / 10000)
        )

        bar = "█" * bar_length

        print(
            f"{row.row_number}. "
            f"{row.product:<15} | "
            f"{bar:<60} "
            f"{row.revenue:>12,.2f} PLN"
        )


# ============================================================
# 12. RANKING GLOBALNY
# ============================================================

section("11. GLOBALNY RANKING PRODUKTOW")

query_global = f"""
WITH product_sales AS (
    {query_aggregation}
)
SELECT
    category,
    product,
    revenue,
    RANK() OVER (
        ORDER BY revenue DESC
    ) AS global_rank
FROM product_sales
ORDER BY global_rank, product_id
"""

df_global = pd.read_sql_query(query_global, conn)

print(df_global.to_string(index=False))


# ============================================================
# 13. KONTROLOWANY PRZYKLAD REMISOW
# ============================================================

section("12. RANK, DENSE_RANK I ROW_NUMBER - REMISY")

query_ties = """
WITH example(product, revenue) AS (
    VALUES
        ('Produkt A', 10000),
        ('Produkt B', 8000),
        ('Produkt C', 8000),
        ('Produkt D', 6000)
)
SELECT
    product,
    revenue,

    RANK() OVER (
        ORDER BY revenue DESC
    ) AS rank_value,

    DENSE_RANK() OVER (
        ORDER BY revenue DESC
    ) AS dense_rank_value,

    ROW_NUMBER() OVER (
        ORDER BY revenue DESC, product ASC
    ) AS row_number_value

FROM example
ORDER BY row_number_value
"""

df_ties = pd.read_sql_query(query_ties, conn)

print(df_ties.to_string(index=False))

print("\nRANK:        1, 2, 2, 4")
print("DENSE_RANK:  1, 2, 2, 3")
print("ROW_NUMBER:  1, 2, 3, 4")

print(
    "\nRANK moze zwrocic wiecej niz 3 produkty "
    "w TOP 3, jezeli wystapi remis."
)

print(
    "ROW_NUMBER pozwala ograniczyc wynik "
    "do maksymalnie 3 produktow na kategorie."
)


# ============================================================
# 14. WERYFIKACJA ZA POMOCA PANDAS
# ============================================================

section("13. WERYFIKACJA SQL ZA POMOCA PANDAS")

df_pandas = df_sales.merge(
    df_products,
    on="product_id",
    how="inner"
)

df_pandas = df_pandas.groupby(
    ["category", "product_id", "product"],
    as_index=False
).agg(
    revenue=("revenue", "sum")
)

df_pandas = df_pandas.sort_values(
    ["category", "revenue", "product_id"],
    ascending=[True, False, True]
).reset_index(drop=True)

df_pandas["category_rank"] = (
    df_pandas.groupby("category")["revenue"]
    .rank(method="min", ascending=False)
    .astype(int)
)

df_pandas["dense_rank"] = (
    df_pandas.groupby("category")["revenue"]
    .rank(method="dense", ascending=False)
    .astype(int)
)

df_pandas["row_number"] = (
    df_pandas.groupby("category").cumcount() + 1
)

columns = [
    "category",
    "product_id",
    "product",
    "revenue",
    "category_rank",
    "dense_rank",
    "row_number"
]

sql_pandas_equal = (
    df_windows[columns]
    .reset_index(drop=True)
    .equals(df_pandas[columns])
)

df_pandas_top3 = df_pandas[
    df_pandas["row_number"] <= 3
].reset_index(drop=True)

top3_columns = [
    "category",
    "product",
    "revenue",
    "category_rank",
    "row_number"
]

top3_equal = (
    df_top3[top3_columns]
    .reset_index(drop=True)
    .equals(df_pandas_top3[top3_columns])
)

print(f"SQL vs Pandas - pelny ranking: {sql_pandas_equal}")
print(f"SQL vs Pandas - TOP 3: {top3_equal}")


# ============================================================
# 15. EXPLAIN QUERY PLAN
# ============================================================

section("14. EXPLAIN QUERY PLAN")

df_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_top3,
    conn
)

print(df_plan.to_string(index=False))


# ============================================================
# 16. POMIAR CZASU WYKONANIA
# ============================================================

section("15. POMIAR CZASU ZAPYTANIA")

times = []

for _ in range(5):

    query_start = time.perf_counter()

    pd.read_sql_query(query_top3, conn)

    query_end = time.perf_counter()

    times.append(query_end - query_start)

for i, elapsed in enumerate(times, start=1):
    print(f"Proba {i}: {elapsed:.6f} s")

print(f"\nSredni czas: {np.mean(times):.6f} s")
print(f"Minimalny czas: {np.min(times):.6f} s")
print(f"Maksymalny czas: {np.max(times):.6f} s")


# ============================================================
# 17. AUTOMATYCZNE TESTY
# ============================================================

section("16. WERYFIKACJA")

tests = {

    "Tabela products zawiera 20 produktow":
        len(df_products) == 20,

    "Tabela sales zawiera 1000 transakcji":
        len(df_sales) == 1000,

    "Istnieja 4 kategorie":
        df_products["category"].nunique() == 4,

    "Kazda kategoria zawiera 5 produktow":
        df_products.groupby("category")
        .size().eq(5).all(),

    "Identyfikatory produktow sa unikalne":
        df_products["product_id"].is_unique,

    "Identyfikatory transakcji sa unikalne":
        df_sales["sale_id"].is_unique,

    "Wszystkie transakcje maja istniejacy produkt":
        df_sales["product_id"]
        .isin(df_products["product_id"]).all(),

    "Wszystkie ilosci sa dodatnie":
        df_sales["quantity"].gt(0).all(),

    "Wszystkie przychody sa dodatnie":
        df_sales["revenue"].gt(0).all(),

    "Brak brakujacych danych":
        not df_sales.isna().any().any(),

    "Agregacja zawiera 20 produktow":
        len(df_aggregation) == 20,

    "Suma transakcji jest zgodna":
        df_aggregation["transactions"].sum() == 1000,

    "Suma przychodow jest zgodna":
        np.isclose(
            df_aggregation["revenue"].sum(),
            df_sales["revenue"].sum()
        ),

    "Suma sprzedanych sztuk jest zgodna":
        df_aggregation["quantity"].sum()
        == df_sales["quantity"].sum(),

    "Ranking RANK zawiera 20 produktow":
        len(df_rank) == 20,

    "Ranking zaczyna sie od 1 w kazdej kategorii":
        df_rank.groupby("category")["category_rank"]
        .min().eq(1).all(),

    "ROW_NUMBER zaczyna sie od 1":
        df_windows.groupby("category")["row_number"]
        .min().eq(1).all(),

    "ROW_NUMBER konczy sie na 5":
        df_windows.groupby("category")["row_number"]
        .max().eq(5).all(),

    "ROW_NUMBER jest unikalny w kategorii":
        not df_windows.duplicated(
            ["category", "row_number"]
        ).any(),

    "TOP 3 zawiera 12 produktow":
        len(df_top3) == 12,

    "Kazda kategoria ma dokladnie 3 produkty TOP":
        df_top3.groupby("category")
        .size().eq(3).all(),

    "TOP 3 nie zawiera duplikatow":
        not df_top3.duplicated(
            ["category", "product"]
        ).any(),

    "TOP 3 zawiera wszystkie kategorie":
        df_top3["category"].nunique() == 4,

    "TOP 3 ma poprawne numery wierszy":
        df_top3["row_number"].between(1, 3).all(),

    "TOP 3 RANK zawiera pozycje od 1 do 3":
        df_top3_rank["category_rank"]
        .between(1, 3).all(),

    "Przychody sa posortowane malejaco":
        all(
            group["revenue"].is_monotonic_decreasing
            for _, group in df_windows.groupby("category")
        ),

    "RANK poprawnie obsluguje remisy":
        df_ties["rank_value"].tolist()
        == [1, 2, 2, 4],

    "DENSE_RANK poprawnie obsluguje remisy":
        df_ties["dense_rank_value"].tolist()
        == [1, 2, 2, 3],

    "ROW_NUMBER poprawnie obsluguje remisy":
        df_ties["row_number_value"].tolist()
        == [1, 2, 3, 4],

    "SQL i Pandas - ranking sa zgodne":
        sql_pandas_equal,

    "SQL i Pandas - TOP 3 sa zgodne":
        top3_equal,

    "Udzialy kategorii sumuja sie do 100 procent":
        np.isclose(
            category_stats["revenue_share_pct"].sum(),
            100
        ),

    "Udzial TOP 3 nie przekracza 100 procent":
        contribution["top3_share_pct"]
        .between(0, 100).all(),

    "Ranking globalny zawiera 20 produktow":
        len(df_global) == 20,

    "Ranking globalny zaczyna sie od 1":
        df_global["global_rank"].min() == 1,

    "Wykonano 5 pomiarow czasu":
        len(times) == 5,

    "Wszystkie pomiary czasu sa dodatnie":
        all(t > 0 for t in times),

    "Tabela products pozostala niezmieniona":
        pd.read_sql_query(
            "SELECT * FROM products ORDER BY product_id",
            conn
        ).equals(df_products),

    "Tabela sales pozostala niezmieniona":
        pd.read_sql_query(
            "SELECT * FROM sales ORDER BY sale_id",
            conn
        ).equals(df_sales)
}

passed = sum(bool(result) for result in tests.values())
total = len(tests)

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

print(f"\nZaliczone testy: {passed}/{total}")

failed = [
    name
    for name, result in tests.items()
    if not result
]


# ============================================================
# 18. WNIOSKI
# ============================================================

section("17. WNIOSKI")

print("""
1. Funkcje okienkowe pozwalaja analizowac grupy rekordow.
2. OVER definiuje okno obliczeniowe.
3. PARTITION BY dzieli dane na niezalezne grupy.
4. ORDER BY wewnatrz OVER okresla kolejnosc rankingu.
5. RANK przypisuje te same pozycje przy remisach.
6. RANK pozostawia luki po remisach.
7. DENSE_RANK nie pozostawia luk w rankingu.
8. ROW_NUMBER nadaje unikalne numery w grupie.
9. ROW_NUMBER pozwala wybrac dokladnie TOP N,
   jezeli grupa zawiera co najmniej N rekordow.
10. CTE ulatwia filtrowanie wynikow funkcji okienkowych.
11. SUM pozwala obliczyc laczny przychod produktu.
12. GROUP BY agreguje transakcje przed rankingiem.
13. Funkcje okienkowe nie redukuja liczby wierszy.
14. Ranking globalny nie wymaga PARTITION BY.
15. SQL i Pandas pozwalaja uzyskac zgodne rankingi.
16. EXPLAIN QUERY PLAN pomaga analizowac zapytania.
17. Rankingi TOP N sa przydatne w Business Intelligence.
""")


# ============================================================
# 19. PODSUMOWANIE
# ============================================================

section("PODSUMOWANIE")

total_time = time.perf_counter() - start_time

print(f"Liczba produktow: {len(df_products)}")
print(f"Liczba kategorii: {df_products['category'].nunique()}")
print(f"Liczba transakcji: {len(df_sales)}")
print(f"Liczba produktow TOP 3: {len(df_top3)}")
print(f"Laczny przychod: {df_sales['revenue'].sum():,.2f} PLN")
print(f"Najlepszy produkt: {df_global.iloc[0]['product']}")
print(f"Najlepsza kategoria: {category_stats.iloc[0]['category']}")
print(f"Sredni czas zapytania: {np.mean(times):.6f} s")
print(f"Calkowity czas wykonania: {total_time:.4f} s")
print(f"Zaliczone testy: {passed}/{total}")

conn.close()

if failed:
    raise AssertionError(
        "Niezaliczone testy: " + ", ".join(failed)
    )

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 15 wykonane poprawnie.")
