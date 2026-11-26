# Lekcja 13 - Zadanie 10: HAVING i grupowanie

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


# Utworzenie tabeli sprzedazy
cursor.execute("""
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        category TEXT NOT NULL,
        product TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount >= 0)
    )
""")


# Syntetyczne dane sprzedazowe
sales = [
    (1, "Elektronika", "Laptop", 3500),
    (2, "Elektronika", "Monitor", 1200),
    (3, "Elektronika", "Smartfon", 2500),
    (4, "Elektronika", "Tablet", 1800),
    (5, "Elektronika", "Drukarka", 650),

    (6, "Akcesoria", "Mysz", 150),
    (7, "Akcesoria", "Klawiatura", 350),
    (8, "Akcesoria", "Sluchawki", 450),
    (9, "Akcesoria", "Kamera", 400),
    (10, "Akcesoria", "Glosniki", 250),

    (11, "Pamiec", "Dysk SSD", 700),
    (12, "Pamiec", "Pendrive", 150),
    (13, "Pamiec", "Dysk HDD", 450),
    (14, "Pamiec", "Karta SD", 200),

    (15, "Oprogramowanie", "Antywirus", 250),
    (16, "Oprogramowanie", "Edytor", 350),
    (17, "Oprogramowanie", "Licencja", 400),

    (18, "Biuro", "Papier", 120),
    (19, "Biuro", "Segregatory", 180),
    (20, "Biuro", "Dlugopisy", 100),

    (21, "Meble", "Biurko", 850),
    (22, "Meble", "Fotel", 1200),
    (23, "Meble", "Regal", 450),
    (24, "Meble", "Szafka", 600)
]


cursor.executemany("""
    INSERT INTO sales
    (sale_id, category, product, amount)
    VALUES (?, ?, ?, ?)
""", sales)

conn.commit()


print("=" * 75)
print("HAVING I GRUPOWANIE - ANALIZA SPRZEDAZY")
print("=" * 75)


section("1. DANE WEJSCIOWE")

df_sales = pd.read_sql_query("""
    SELECT *
    FROM sales
    ORDER BY sale_id
""", conn)

df_original = df_sales.copy()

print(df_sales.to_string(index=False))

print(f"\nLiczba transakcji: {len(df_sales)}")
print(f"Liczba kategorii: {df_sales['category'].nunique()}")
print(f"Przychod: {df_sales['amount'].sum():.2f} PLN")


section("2. GRUPOWANIE WSZYSTKICH KATEGORII")

query_all = """
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_transaction
FROM sales
GROUP BY category
ORDER BY total_revenue DESC, category ASC
"""

df_all = pd.read_sql_query(query_all, conn)

print(query_all)
print(df_all.round(2).to_string(index=False))


section("3. HAVING - PRZYCHOD POWYZEJ 1000 PLN")

threshold = 1000

query_having = """
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_transaction
FROM sales
GROUP BY category
HAVING SUM(amount) > ?
ORDER BY total_revenue DESC, category ASC
"""

df_having = pd.read_sql_query(
    query_having,
    conn,
    params=(threshold,)
)

print(query_having)
print(f"Parametr: {threshold} PLN\n")

print(df_having.round(2).to_string(index=False))

print(f"\nLiczba zakwalifikowanych kategorii: {len(df_having)}")


section("4. KATEGORIE ODRZUCONE PRZEZ HAVING")

query_rejected = """
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_transaction
FROM sales
GROUP BY category
HAVING SUM(amount) <= ?
ORDER BY total_revenue DESC, category ASC
"""

df_rejected = pd.read_sql_query(
    query_rejected,
    conn,
    params=(threshold,)
)

print(df_rejected.round(2).to_string(index=False))


section("5. POROWNANIE WHERE I HAVING")

query_where = """
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_transaction
FROM sales
WHERE amount > ?
GROUP BY category
ORDER BY total_revenue DESC, category ASC
"""

df_where = pd.read_sql_query(
    query_where,
    conn,
    params=(threshold,)
)

print("WHERE amount > 1000:")
print(df_where.round(2).to_string(index=False))

print("\nHAVING SUM(amount) > 1000:")
print(df_having.round(2).to_string(index=False))

print("\nWHERE filtruje pojedyncze transakcje.")
print("HAVING filtruje cale grupy po agregacji.")


section("6. POROWNANIE OPERATOROW > ORAZ >=")

query_ge = """
SELECT
    category,
    SUM(amount) AS total_revenue
FROM sales
GROUP BY category
HAVING SUM(amount) >= ?
ORDER BY total_revenue DESC, category ASC
"""

df_ge = pd.read_sql_query(
    query_ge,
    conn,
    params=(threshold,)
)

print("HAVING SUM(amount) >= 1000:")
print(df_ge.to_string(index=False))

print("\nKategorie dla > 1000:", len(df_having))
print("Kategorie dla >= 1000:", len(df_ge))


section("7. UDZIAL KATEGORII W PRZYCHODZIE")

total_revenue = df_all["total_revenue"].sum()

df_report = df_all.copy()

df_report["revenue_share_pct"] = (
    df_report["total_revenue"] / total_revenue * 100
)

df_report["qualified"] = (
    df_report["total_revenue"] > threshold
)

print(df_report.round(2).to_string(index=False))


section("8. TEKSTOWY WYKRES PRZYCHODOW")

print("Legenda: jeden znak = okolo 250 PLN\n")

for row in df_report.itertuples(index=False):
    bar = "█" * round(row.total_revenue / 250)
    status = "TAK" if row.qualified else "NIE"

    print(
        f"{row.category:18} | "
        f"{bar:40} "
        f"{row.total_revenue:10.2f} PLN "
        f"| HAVING: {status}"
    )


section("9. ANALIZA STATYSTYCZNA")

qualified_revenue = df_having["total_revenue"].sum()
rejected_revenue = df_rejected["total_revenue"].sum()

qualified_share = qualified_revenue / total_revenue * 100
rejected_share = rejected_revenue / total_revenue * 100

qualified_transactions = df_having["transaction_count"].sum()

weighted_average = (
    qualified_revenue / qualified_transactions
)

metrics = pd.DataFrame({
    "Metryka": [
        "Liczba transakcji",
        "Liczba kategorii",
        "Kategorie zakwalifikowane",
        "Kategorie odrzucone",
        "Calkowity przychod",
        "Przychod zakwalifikowany",
        "Przychod odrzucony",
        "Udzial zakwalifikowany (%)",
        "Udzial odrzucony (%)",
        "Srednia transakcja zakwalifikowana"
    ],
    "Wartosc": [
        len(df_sales),
        len(df_all),
        len(df_having),
        len(df_rejected),
        total_revenue,
        qualified_revenue,
        rejected_revenue,
        qualified_share,
        rejected_share,
        weighted_average
    ]
})

print(metrics.round(2).to_string(index=False))


section("10. WERYFIKACJA SQL ZA POMOCA PANDAS")

df_pandas_all = (
    df_sales.groupby("category", as_index=False)
    .agg(
        transaction_count=("sale_id", "count"),
        total_revenue=("amount", "sum"),
        avg_transaction=("amount", "mean")
    )
    .sort_values(
        ["total_revenue", "category"],
        ascending=[False, True]
    )
    .reset_index(drop=True)
)

df_pandas_having = (
    df_pandas_all[
        df_pandas_all["total_revenue"] > threshold
    ]
    .reset_index(drop=True)
)

print(df_pandas_having.round(2).to_string(index=False))

all_equal = df_all.equals(df_pandas_all)
having_equal = df_having.equals(df_pandas_having)

print(f"\nSQL vs Pandas - GROUP BY: {all_equal}")
print(f"SQL vs Pandas - HAVING: {having_equal}")


section("11. EXPLAIN QUERY PLAN")

df_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_having,
    conn,
    params=(threshold,)
)

print(df_plan.to_string(index=False))


section("12. AUTOMATYCZNE TESTY")

df_after = pd.read_sql_query("""
    SELECT *
    FROM sales
    ORDER BY sale_id
""", conn)

tests = {
    "Tabela zawiera 24 transakcje":
        len(df_sales) == 24,

    "Tabela zawiera 4 kolumny":
        df_sales.shape[1] == 4,

    "Identyfikatory sa unikalne":
        df_sales["sale_id"].is_unique,

    "Brak wartosci NaN":
        not df_sales.isna().any().any(),

    "Istnieje 6 kategorii":
        df_sales["category"].nunique() == 6,

    "GROUP BY zwraca 6 kategorii":
        len(df_all) == 6,

    "HAVING zwraca 4 kategorie":
        len(df_having) == 4,

    "Odrzucono 2 kategorie":
        len(df_rejected) == 2,

    "Wszystkie przychody HAVING przekraczaja 1000":
        (df_having["total_revenue"] > threshold).all(),

    "Odrzucone przychody nie przekraczaja 1000":
        (df_rejected["total_revenue"] <= threshold).all(),

    "Elektronika ma przychod 9650 PLN":
        np.isclose(
            df_all.loc[
                df_all["category"] == "Elektronika",
                "total_revenue"
            ].iloc[0],
            9650
        ),

    "Meble maja przychod 3100 PLN":
        np.isclose(
            df_all.loc[
                df_all["category"] == "Meble",
                "total_revenue"
            ].iloc[0],
            3100
        ),

    "Akcesoria maja przychod 1600 PLN":
        np.isclose(
            df_all.loc[
                df_all["category"] == "Akcesoria",
                "total_revenue"
            ].iloc[0],
            1600
        ),

    "Pamiec ma przychod 1500 PLN":
        np.isclose(
            df_all.loc[
                df_all["category"] == "Pamiec",
                "total_revenue"
            ].iloc[0],
            1500
        ),

    "Oprogramowanie ma przychod 1000 PLN":
        np.isclose(
            df_all.loc[
                df_all["category"] == "Oprogramowanie",
                "total_revenue"
            ].iloc[0],
            1000
        ),

    "Oprogramowanie wykluczone przez HAVING >":
        "Oprogramowanie" not in df_having["category"].values,

    "Oprogramowanie uwzglednione przez HAVING >=":
        "Oprogramowanie" in df_ge["category"].values,

    "HAVING >= zwraca 5 kategorii":
        len(df_ge) == 5,

    "Biuro zostalo odrzucone":
        "Biuro" in df_rejected["category"].values,

    "Przychody posortowane malejaco":
        df_having["total_revenue"].is_monotonic_decreasing,

    "Elektronika zajmuje pierwsze miejsce":
        df_having.iloc[0]["category"] == "Elektronika",

    "Liczba zagregowanych transakcji jest zgodna":
        df_all["transaction_count"].sum() == len(df_sales),

    "Suma przychodow jest zgodna":
        np.isclose(
            total_revenue,
            df_sales["amount"].sum()
        ),

    "Calkowity przychod wynosi 17250 PLN":
        np.isclose(total_revenue, 17250),

    "Przychod zakwalifikowany wynosi 15850 PLN":
        np.isclose(qualified_revenue, 15850),

    "Przychod odrzucony wynosi 1400 PLN":
        np.isclose(rejected_revenue, 1400),

    "Suma przychodow zakwalifikowanych i odrzuconych":
        np.isclose(
            qualified_revenue + rejected_revenue,
            total_revenue
        ),

    "Udzialy kategorii sumuja sie do 100 procent":
        np.isclose(
            df_report["revenue_share_pct"].sum(),
            100
        ),

    "Srednie transakcji sa poprawne":
        np.allclose(
            df_all["avg_transaction"],
            df_all["total_revenue"]
            / df_all["transaction_count"]
        ),

    "SQL i Pandas - GROUP BY sa zgodne":
        all_equal,

    "SQL i Pandas - HAVING sa zgodne":
        having_equal,

    "WHERE i HAVING zwracaja rozne wyniki":
        not df_where.equals(df_having),

    "Oryginalna tabela pozostala niezmieniona":
        df_original.equals(df_after)
}


for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."


section("13. WNIOSKI")

conclusions = [
    "GROUP BY grupuje rekordy wedlug kategorii.",
    "COUNT(*) oblicza liczbe transakcji.",
    "SUM(amount) oblicza laczny przychod.",
    "AVG(amount) oblicza srednia wartosc transakcji.",
    "WHERE filtruje rekordy przed grupowaniem.",
    "HAVING filtruje grupy po agregacji.",
    "HAVING SUM(amount) > 1000 wyklucza wartosc 1000.",
    "Operator >= uwzglednia wartosc graniczna.",
    "ORDER BY DESC sortuje przychody malejaco.",
    "Parametry SQL pozwalaja unikac skladania zapytan z danych.",
    "SQL i Pandas pozwalaja uzyskac zgodne agregacje.",
    "EXPLAIN QUERY PLAN pokazuje sposob wykonania zapytania.",
    "Agregacja zmniejsza liczbe rekordow pobieranych z bazy."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba transakcji: {len(df_sales)}")
print(f"Liczba kategorii: {len(df_all)}")
print(f"Prog HAVING: {threshold} PLN")
print(f"Kategorie zakwalifikowane: {len(df_having)}")
print(f"Kategorie odrzucone: {len(df_rejected)}")
print(f"Calkowity przychod: {total_revenue:.2f} PLN")
print(f"Przychod zakwalifikowany: {qualified_revenue:.2f} PLN")
print(f"Przychod odrzucony: {rejected_revenue:.2f} PLN")
print(f"Udzial zakwalifikowany: {qualified_share:.2f}%")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 10 wykonane poprawnie.")
