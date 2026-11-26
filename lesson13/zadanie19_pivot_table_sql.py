# Lekcja 13 - Zadanie 19: Pivot Table w SQL

import sqlite3
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 90)


def show_table(df):
    """Wyswietla DataFrame bez indeksu."""
    print(df.to_string(index=False))


# ============================================================
# 1. GENEROWANIE DANYCH
# ============================================================

rng = np.random.default_rng(42)

N = 1000

dates = pd.date_range(
    start="2024-01-01",
    end="2024-12-31",
    freq="D"
)

sales = pd.DataFrame({
    "date": rng.choice(dates, size=N),
    "category": rng.choice(
        ["A", "B"],
        size=N,
        p=[0.55, 0.45]
    ),
    "revenue": rng.integers(50, 1001, size=N)
})

sales["date"] = pd.to_datetime(
    sales["date"]
).dt.strftime("%Y-%m-%d")


# ============================================================
# 2. UTWORZENIE BAZY SQLITE
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
    CREATE TABLE sales (
        date TEXT NOT NULL,
        category TEXT NOT NULL
            CHECK(category IN ('A', 'B')),
        revenue INTEGER NOT NULL
            CHECK(revenue >= 0)
    )
""")

sales.to_sql(
    "sales",
    conn,
    if_exists="append",
    index=False
)

print("=" * 90)
print("PIVOT TABLE W SQL - ANALIZA SPRZEDAZY")
print("=" * 90)


section("1. DANE WEJSCIOWE")

df_sales = pd.read_sql_query(
    "SELECT * FROM sales",
    conn
)

show_table(df_sales.head(10))

print(f"\nLiczba transakcji: {len(df_sales)}")
print(f"Liczba kategorii: {df_sales['category'].nunique()}")
print(f"Pierwsza data: {df_sales['date'].min()}")
print(f"Ostatnia data: {df_sales['date'].max()}")
print(f"Laczny przychod: {df_sales['revenue'].sum():,.2f} PLN")


# ============================================================
# 3. TRADYCYJNA AGREGACJA SQL
# ============================================================

section("2. TRADYCYJNA AGREGACJA - GROUP BY")

query_group = """
SELECT
    strftime('%Y-%m', date) AS month,
    category,
    COUNT(*) AS transactions,
    SUM(revenue) AS revenue
FROM sales
GROUP BY month, category
ORDER BY month, category
"""

print(query_group)

df_group = pd.read_sql_query(
    query_group,
    conn
)

show_table(df_group)

print(f"\nLiczba wierszy: {len(df_group)}")


# ============================================================
# 4. PIVOT TABLE W SQL
# ============================================================

section("3. PIVOT TABLE - CASE WHEN I GROUP BY")

query_pivot = """
SELECT
    strftime('%Y-%m', date) AS month,

    SUM(
        CASE
            WHEN category = 'A'
            THEN revenue
            ELSE 0
        END
    ) AS cat_A,

    SUM(
        CASE
            WHEN category = 'B'
            THEN revenue
            ELSE 0
        END
    ) AS cat_B

FROM sales
GROUP BY month
ORDER BY month
"""

print(query_pivot)

df_pivot = pd.read_sql_query(
    query_pivot,
    conn
)

show_table(df_pivot)

print(f"\nLiczba miesiecy: {len(df_pivot)}")
print(f"Liczba kolumn: {len(df_pivot.columns)}")


# ============================================================
# 5. ROZSZERZONA TABELA PRZESTAWNA
# ============================================================

section("4. ROZSZERZONA TABELA PRZESTAWNA")

query_extended = """
SELECT
    strftime('%Y-%m', date) AS month,

    SUM(
        CASE WHEN category = 'A'
        THEN revenue ELSE 0 END
    ) AS cat_A,

    SUM(
        CASE WHEN category = 'B'
        THEN revenue ELSE 0 END
    ) AS cat_B,

    SUM(revenue) AS total_revenue,

    COUNT(*) AS transactions,

    ROUND(AVG(revenue), 2) AS avg_revenue

FROM sales
GROUP BY month
ORDER BY month
"""

df_extended = pd.read_sql_query(
    query_extended,
    conn
)

show_table(df_extended)


# ============================================================
# 6. UDZIAL PROCENTOWY KATEGORII
# ============================================================

section("5. UDZIAL PROCENTOWY KATEGORII")

df_share = df_pivot.copy()

df_share["total"] = (
    df_share["cat_A"] + df_share["cat_B"]
)

df_share["cat_A_pct"] = (
    df_share["cat_A"]
    / df_share["total"]
    * 100
)

df_share["cat_B_pct"] = (
    df_share["cat_B"]
    / df_share["total"]
    * 100
)

show_table(df_share.round(2))


# ============================================================
# 7. PODSUMOWANIE ROCZNE
# ============================================================

section("6. PODSUMOWANIE ROCZNE")

query_year = """
SELECT
    category,
    COUNT(*) AS transactions,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_revenue,
    MIN(revenue) AS min_revenue,
    MAX(revenue) AS max_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC
"""

df_year = pd.read_sql_query(
    query_year,
    conn
)

show_table(df_year)

total_A = df_pivot["cat_A"].sum()
total_B = df_pivot["cat_B"].sum()

total_revenue = total_A + total_B

print(f"\nPrzychod kategorii A: {total_A:,.2f} PLN")
print(f"Przychod kategorii B: {total_B:,.2f} PLN")
print(f"Przychod calkowity: {total_revenue:,.2f} PLN")

print(f"Udzial kategorii A: {total_A / total_revenue * 100:.2f}%")
print(f"Udzial kategorii B: {total_B / total_revenue * 100:.2f}%")


# ============================================================
# 8. TEKSTOWA WIZUALIZACJA
# ============================================================

section("7. TEKSTOWE SLUPKI PRZYCHODOW")

scale = 1000

print("Legenda: jeden znak = okolo 1000 PLN")
print("A - kategoria A")
print("B - kategoria B")

for row in df_pivot.itertuples(index=False):

    bar_A = "█" * round(row.cat_A / scale)
    bar_B = "█" * round(row.cat_B / scale)

    print(f"\n{row.month}")
    print(f" A | {bar_A:<40} {row.cat_A:>10,.2f} PLN")
    print(f" B | {bar_B:<40} {row.cat_B:>10,.2f} PLN")


# ============================================================
# 9. STACKED BAR - WYKRES SKUMULOWANY
# ============================================================

section("8. SKUMULOWANY ROZKLAD PRZYCHODOW")

print("Legenda:")
print("█ - kategoria A")
print("░ - kategoria B")
print("Jeden znak = okolo 1000 PLN\n")

for row in df_pivot.itertuples(index=False):

    bar_A = "█" * round(row.cat_A / scale)
    bar_B = "░" * round(row.cat_B / scale)

    total = row.cat_A + row.cat_B

    print(
        f"{row.month} | "
        f"{bar_A + bar_B:<70} "
        f"{total:>10,.2f} PLN"
    )


# ============================================================
# 10. WYKRES PROCENTOWY
# ============================================================

section("9. PROCENTOWY ROZKLAD PRZYCHODOW")

width = 50

print("Legenda: █ = A, ░ = B")
print("Kazdy slupek reprezentuje 100% przychodu\n")

for row in df_share.itertuples(index=False):

    length_A = round(
        row.cat_A_pct / 100 * width
    )

    length_B = width - length_A

    bar = (
        "█" * length_A
        + "░" * length_B
    )

    print(
        f"{row.month} | {bar} | "
        f"A: {row.cat_A_pct:6.2f}% "
        f"B: {row.cat_B_pct:6.2f}%"
    )


# ============================================================
# 11. NAJLEPSZE MIESIACE
# ============================================================

section("10. RANKING MIESIECY")

df_ranking = df_extended.sort_values(
    "total_revenue",
    ascending=False
).reset_index(drop=True)

df_ranking.insert(
    0,
    "rank",
    np.arange(1, len(df_ranking) + 1)
)

show_table(df_ranking)

best_month = df_ranking.iloc[0]
worst_month = df_ranking.iloc[-1]

print(
    f"\nNajlepszy miesiac: "
    f"{best_month['month']}"
)

print(
    f"Przychod: "
    f"{best_month['total_revenue']:,.2f} PLN"
)

print(
    f"\nNajslabszy miesiac: "
    f"{worst_month['month']}"
)

print(
    f"Przychod: "
    f"{worst_month['total_revenue']:,.2f} PLN"
)


# ============================================================
# 12. ANALIZA STATYSTYCZNA
# ============================================================

section("11. ANALIZA STATYSTYCZNA")

df_stats = pd.DataFrame({
    "Metryka": [
        "Liczba transakcji",
        "Liczba miesiecy",
        "Laczny przychod",
        "Sredni przychod miesieczny",
        "Mediana przychodu miesiecznego",
        "Minimalny przychod miesieczny",
        "Maksymalny przychod miesieczny",
        "Odchylenie standardowe"
    ],
    "Wartosc": [
        len(df_sales),
        len(df_pivot),
        total_revenue,
        df_extended["total_revenue"].mean(),
        df_extended["total_revenue"].median(),
        df_extended["total_revenue"].min(),
        df_extended["total_revenue"].max(),
        df_extended["total_revenue"].std()
    ]
})

show_table(df_stats.round(2))


# ============================================================
# 13. DOMINUJACA KATEGORIA
# ============================================================

section("12. DOMINUJACA KATEGORIA W MIESIACU")

query_dominant = """
WITH monthly_pivot AS (
    SELECT
        strftime('%Y-%m', date) AS month,

        SUM(
            CASE WHEN category = 'A'
            THEN revenue ELSE 0 END
        ) AS cat_A,

        SUM(
            CASE WHEN category = 'B'
            THEN revenue ELSE 0 END
        ) AS cat_B

    FROM sales
    GROUP BY month
)
SELECT
    month,
    cat_A,
    cat_B,
    ABS(cat_A - cat_B) AS difference,

    CASE
        WHEN cat_A > cat_B THEN 'A'
        WHEN cat_B > cat_A THEN 'B'
        ELSE 'Remis'
    END AS dominant_category

FROM monthly_pivot
ORDER BY month
"""

df_dominant = pd.read_sql_query(
    query_dominant,
    conn
)

show_table(df_dominant)

print("\nLiczba miesiecy wedlug dominujacej kategorii:")

print(
    df_dominant["dominant_category"]
    .value_counts()
    .to_string()
)


# ============================================================
# 14. POROWNANIE SQL I PANDAS
# ============================================================

section("13. PIVOT TABLE ZA POMOCA PANDAS")

df_pandas = df_sales.copy()

df_pandas["month"] = pd.to_datetime(
    df_pandas["date"]
).dt.strftime("%Y-%m")

pivot_pandas = pd.pivot_table(
    df_pandas,
    index="month",
    columns="category",
    values="revenue",
    aggfunc="sum",
    fill_value=0
)

pivot_pandas = pivot_pandas.reindex(
    columns=["A", "B"],
    fill_value=0
)

pivot_pandas = pivot_pandas.rename(
    columns={
        "A": "cat_A",
        "B": "cat_B"
    }
).reset_index()

pivot_pandas.columns.name = None

pivot_pandas = pivot_pandas.sort_values(
    "month"
).reset_index(drop=True)

show_table(pivot_pandas)

sql_pandas_equal = df_pivot.equals(
    pivot_pandas
)

print(
    f"\nCzy SQL i Pandas sa zgodne: "
    f"{sql_pandas_equal}"
)


# ============================================================
# 15. PLAN WYKONANIA ZAPYTANIA
# ============================================================

section("14. EXPLAIN QUERY PLAN")

df_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_pivot,
    conn
)

show_table(df_plan)


# ============================================================
# 16. AUTOMATYCZNE TESTY
# ============================================================

section("15. WERYFIKACJA")

expected_months = pd.date_range(
    "2024-01-01",
    periods=12,
    freq="MS"
).strftime("%Y-%m").tolist()

expected_A = df_sales.loc[
    df_sales["category"] == "A",
    "revenue"
].sum()

expected_B = df_sales.loc[
    df_sales["category"] == "B",
    "revenue"
].sum()

df_after = pd.read_sql_query(
    "SELECT * FROM sales",
    conn
)

tests = {

    "Tabela zawiera 1000 transakcji":
        len(df_sales) == 1000,

    "Tabela zawiera 3 kolumny":
        len(df_sales.columns) == 3,

    "Nazwy kolumn sa poprawne":
        list(df_sales.columns)
        == ["date", "category", "revenue"],

    "Brak brakujacych danych":
        not df_sales.isna().any().any(),

    "Istnieja dwie kategorie":
        df_sales["category"].nunique() == 2,

    "Kategorie to A i B":
        set(df_sales["category"]) == {"A", "B"},

    "Wszystkie przychody sa dodatnie":
        (df_sales["revenue"] > 0).all(),

    "Wszystkie daty pochodza z 2024 roku":
        df_sales["date"].str.startswith("2024").all(),

    "Pivot zawiera 12 miesiecy":
        len(df_pivot) == 12,

    "Pivot zawiera 3 kolumny":
        len(df_pivot.columns) == 3,

    "Nazwy kolumn pivot sa poprawne":
        list(df_pivot.columns)
        == ["month", "cat_A", "cat_B"],

    "Miesiace sa unikalne":
        df_pivot["month"].is_unique,

    "Pivot zawiera wszystkie miesiace":
        df_pivot["month"].tolist() == expected_months,

    "Miesiace sa posortowane":
        df_pivot["month"].is_monotonic_increasing,

    "Brak NULL w tabeli pivot":
        not df_pivot.isna().any().any(),

    "Przychody kategorii A sa nieujemne":
        (df_pivot["cat_A"] >= 0).all(),

    "Przychody kategorii B sa nieujemne":
        (df_pivot["cat_B"] >= 0).all(),

    "Suma kategorii A jest poprawna":
        total_A == expected_A,

    "Suma kategorii B jest poprawna":
        total_B == expected_B,

    "Suma pivot jest zgodna z danymi":
        total_revenue == df_sales["revenue"].sum(),

    "Tradycyjna agregacja zawiera 24 wiersze":
        len(df_group) == 24,

    "Suma tradycyjnej agregacji jest poprawna":
        df_group["revenue"].sum() == total_revenue,

    "Suma liczby transakcji jest poprawna":
        df_extended["transactions"].sum() == N,

    "Suma miesiecznych przychodow jest poprawna":
        df_extended["total_revenue"].sum()
        == total_revenue,

    "Sumy miesieczne A i B sa zgodne":
        (
            df_extended["cat_A"]
            + df_extended["cat_B"]
            == df_extended["total_revenue"]
        ).all(),

    "Udzialy kategorii sumuja sie do 100 procent":
        np.allclose(
            df_share["cat_A_pct"]
            + df_share["cat_B_pct"],
            100
        ),

    "Udzialy kategorii A sa poprawne":
        df_share["cat_A_pct"].between(0, 100).all(),

    "Udzialy kategorii B sa poprawne":
        df_share["cat_B_pct"].between(0, 100).all(),

    "Podsumowanie roczne zawiera dwie kategorie":
        len(df_year) == 2,

    "Podsumowanie roczne ma poprawna sume":
        df_year["total_revenue"].sum()
        == total_revenue,

    "Ranking zawiera 12 miesiecy":
        len(df_ranking) == 12,

    "Ranking jest posortowany malejaco":
        df_ranking["total_revenue"]
        .is_monotonic_decreasing,

    "Najlepszy miesiac jest poprawny":
        best_month["total_revenue"]
        == df_extended["total_revenue"].max(),

    "Najslabszy miesiac jest poprawny":
        worst_month["total_revenue"]
        == df_extended["total_revenue"].min(),

    "Dominujaca kategoria obejmuje 12 miesiecy":
        len(df_dominant) == 12,

    "Dominujaca kategoria ma poprawne wartosci":
        set(df_dominant["dominant_category"])
        .issubset({"A", "B", "Remis"}),

    "Roznice kategorii sa nieujemne":
        (df_dominant["difference"] >= 0).all(),

    "SQL i Pandas zwracaja identyczne wyniki":
        sql_pandas_equal,

    "Plan wykonania nie jest pusty":
        not df_plan.empty,

    "Oryginalna tabela pozostala niezmieniona":
        df_sales.equals(df_after)
}

passed = 0

for name, result in tests.items():

    print(f"Czy {name}: {bool(result)}")

    if result:
        passed += 1

print(f"\nZaliczone testy: {passed}/{len(tests)}")


# ============================================================
# 17. WNIOSKI
# ============================================================

section("16. WNIOSKI")

conclusions = [
    "Pivot Table przeksztalca wartosci kategorii w kolumny.",
    "CASE WHEN umozliwia agregacje warunkowa.",
    "SUM oblicza przychod dla wybranej kategorii.",
    "ELSE 0 zapobiega brakujacym wartosciom w istniejacych grupach.",
    "GROUP BY tworzy jeden wiersz dla kazdego miesiaca.",
    "strftime pozwala grupowac dane wedlug miesiecy.",
    "ORDER BY zapewnia chronologiczna kolejnosc.",
    "Pivot ulatwia porownywanie kategorii.",
    "Agregacja zmniejsza liczbe analizowanych wierszy.",
    "Slupki tekstowe nie wymagaja bibliotek graficznych.",
    "Wykres skumulowany pokazuje laczny przychod.",
    "Wykres procentowy pokazuje strukture przychodow.",
    "CTE ulatwia organizacje zlozonych zapytan.",
    "CASE WHEN pozwala wskazac dominujaca kategorie.",
    "Pandas pivot_table pozwala odtworzyc pivot SQL.",
    "EXPLAIN QUERY PLAN pokazuje sposob wykonania SQL.",
    "Agregacja w SQL ogranicza dane przesylane do aplikacji.",
    "Nowe kategorie wymagaja rozszerzenia statycznego pivot SQL.",
    "Brakujace miesiace wymagaja dodatkowej tabeli kalendarza.",
    "Pivot Table nie modyfikuje danych zrodlowych."
]

for number, conclusion in enumerate(
    conclusions,
    start=1
):
    print(f"{number}. {conclusion}")


# ============================================================
# 18. PODSUMOWANIE
# ============================================================

section("PODSUMOWANIE")

print(f"Liczba transakcji: {N}")
print(f"Liczba kategorii: 2")
print(f"Liczba miesiecy: {len(df_pivot)}")
print(f"Wiersze przed agregacja: {len(df_sales)}")
print(f"Wiersze po agregacji: {len(df_pivot)}")

reduction = (
    1 - len(df_pivot) / len(df_sales)
) * 100

print(f"Redukcja liczby wierszy: {reduction:.2f}%")

print(f"Przychod kategorii A: {total_A:,.2f} PLN")
print(f"Przychod kategorii B: {total_B:,.2f} PLN")
print(f"Laczny przychod: {total_revenue:,.2f} PLN")
print(f"Najlepszy miesiac: {best_month['month']}")
print(f"Najslabszy miesiac: {worst_month['month']}")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

assert passed == len(tests), "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 19 wykonane poprawnie.")
