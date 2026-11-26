# Lekcja 13 - Zadanie 20: Green SQL Challenge
# Wspolny modul generowania danych i pomiarow

import sqlite3
import time

import numpy as np
import pandas as pd


N_RECORDS = 500_000
SEED = 42
REGION = "North"
DATE_FROM = "2024-07-01"
DATE_TO = "2024-10-01"
TOP_N = 10
REPEATS = 3


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 80)


def create_database():
    """Tworzy baze SQLite z 500 000 transakcji."""

    rng = np.random.default_rng(SEED)

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            region TEXT NOT NULL,
            sale_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            revenue INTEGER NOT NULL
        )
    """)

    products = np.array([
        f"Product_{i:03d}"
        for i in range(1, 101)
    ])

    categories = np.array([
        "Electronics",
        "Food",
        "Clothing",
        "Home",
        "Sport"
    ])

    regions = np.array([
        "North",
        "South",
        "East",
        "West"
    ])

    product_idx = rng.integers(
        0, len(products), N_RECORDS
    )

    dates = (
        np.datetime64("2024-01-01")
        + rng.integers(0, 366, N_RECORDS).astype(
            "timedelta64[D]"
        )
    )

    quantities = rng.integers(
        1, 11, N_RECORDS
    )

    prices = rng.integers(
        10, 501, N_RECORDS
    )

    sales = pd.DataFrame({
        "sale_id": np.arange(1, N_RECORDS + 1),
        "product": products[product_idx],
        "category": categories[
            product_idx % len(categories)
        ],
        "region": rng.choice(regions, N_RECORDS),
        "sale_date": dates.astype(str),
        "quantity": quantities,
        "revenue": quantities * prices
    })

    sales.to_sql(
        "sales",
        conn,
        if_exists="append",
        index=False,
        chunksize=10_000
    )

    conn.commit()

    return conn


def create_indexes(conn):
    """Tworzy indeks zlozony dla filtrowania."""

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_sales_region_date
        ON sales(region, sale_date)
    """)

    conn.commit()


def memory_bytes(df):
    """Zwraca zuzycie pamieci DataFrame w bajtach."""

    return int(
        df.memory_usage(deep=True).sum()
    )


def memory_mb(df):
    """Zwraca zuzycie pamieci DataFrame w MiB."""

    return memory_bytes(df) / 1024**2


def explain_query(conn, query, params=()):
    """Zwraca plan wykonania zapytania."""

    return pd.read_sql_query(
        "EXPLAIN QUERY PLAN " + query,
        conn,
        params=params
    )


def aggregate_python(df):
    """Agreguje dane i zwraca TOP 10 produktow."""

    return (
        df.groupby("product", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            transactions=("revenue", "size")
        )
        .sort_values(
            ["total_revenue", "product"],
            ascending=[False, True]
        )
        .head(TOP_N)
        .reset_index(drop=True)
    )


def measure_strategy(strategy, conn):
    """Mierzy czas strategii w trzech powtorzeniach."""

    times = []
    memories = []
    rows = []
    result = None

    for _ in range(REPEATS):

        start = time.perf_counter()

        result, downloaded = strategy(conn)

        elapsed = time.perf_counter() - start

        times.append(elapsed)
        memories.append(memory_bytes(downloaded))
        rows.append(len(downloaded))

        del downloaded

    return {
        "time_s": float(np.mean(times)),
        "memory_bytes": float(np.mean(memories)),
        "memory_mb": float(np.mean(memories)) / 1024**2,
        "downloaded_rows": int(np.mean(rows)),
        "energy_proxy": (
            float(np.mean(times))
            * float(np.mean(memories))
            / 1024**2
        ),
        "times": times,
        "result": result
    }


def reduction_percent(before, after):
    """Oblicza procentowa redukcje metryki."""

    if before == 0:
        return 0.0

    return 100 * (before - after) / before


if __name__ == "__main__":

    section("GREEN SQL CHALLENGE - GENEROWANIE BAZY")

    start = time.perf_counter()

    conn = create_database()

    elapsed = time.perf_counter() - start

    summary = pd.read_sql_query("""
        SELECT
            COUNT(*) AS records,
            COUNT(DISTINCT product) AS products,
            COUNT(DISTINCT category) AS categories,
            COUNT(DISTINCT region) AS regions,
            MIN(sale_date) AS first_date,
            MAX(sale_date) AS last_date,
            SUM(revenue) AS total_revenue
        FROM sales
    """, conn)

    print(summary.T.to_string(header=False))

    print(f"\nCzas tworzenia bazy: {elapsed:.4f} s")

    section("PRZYKLADOWE REKORDY")

    sample = pd.read_sql_query("""
        SELECT *
        FROM sales
        ORDER BY sale_id
        LIMIT 10
    """, conn)

    print(sample.to_string(index=False))

    section("WERYFIKACJA")

    assert summary.loc[0, "records"] == N_RECORDS
    print("[OK] Baza zawiera 500 000 rekordow")

    assert summary.loc[0, "products"] == 100
    print("[OK] Baza zawiera 100 produktow")

    assert summary.loc[0, "categories"] == 5
    print("[OK] Baza zawiera 5 kategorii")

    assert summary.loc[0, "regions"] == 4
    print("[OK] Baza zawiera 4 regiony")

    assert summary.loc[0, "first_date"] == "2024-01-01"
    print("[OK] Poprawna data poczatkowa")

    assert summary.loc[0, "last_date"] == "2024-12-31"
    print("[OK] Poprawna data koncowa")

    indexes = pd.read_sql_query("""
        PRAGMA index_list('sales')
    """, conn)

    assert indexes.empty
    print("[OK] Brak dodatkowych indeksow")

    conn.close()

    section("PODSUMOWANIE")

    print("Zaliczone testy: 7/7")
    print("Wspolny modul przygotowany poprawnie.")
