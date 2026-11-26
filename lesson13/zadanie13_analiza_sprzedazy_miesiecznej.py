# Lekcja 13 - Zadanie 13: Analiza sprzedazy miesiecznej

import sqlite3
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 90)


# Konfiguracja generatora losowego
np.random.seed(42)

N = 1000
BAR_UNIT = 500


# Utworzenie bazy danych SQLite w pamieci
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()


# Utworzenie tabeli sales
cursor.execute("""
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        product TEXT NOT NULL,
        category TEXT NOT NULL,
        sale_date TEXT NOT NULL,
        revenue REAL NOT NULL
    )
""")


# Produkty i odpowiadajace im kategorie
product_categories = {
    "Laptop": "Elektronika",
    "Smartfon": "Elektronika",
    "Monitor": "Elektronika",
    "Tablet": "Elektronika",
    "Mysz": "Akcesoria",
    "Klawiatura": "Akcesoria",
    "Sluchawki": "Akcesoria",
    "Pendrive": "Pamiec",
    "Dysk SSD": "Pamiec",
    "Drukarka": "Elektronika"
}


# Generowanie losowych produktow
products = np.random.choice(
    list(product_categories.keys()),
    size=N
)

categories = [
    product_categories[product]
    for product in products
]


# Generowanie dat - 2024 jest rokiem przestepnym
start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2024-12-31")

number_of_days = (end_date - start_date).days + 1

random_days = np.random.randint(
    0,
    number_of_days,
    size=N
)

sale_dates = (
    start_date
    + pd.to_timedelta(random_days, unit="D")
)


# Generowanie losowych przychodow
revenues = np.round(
    np.random.uniform(50, 1000, size=N),
    2
)


# Przygotowanie rekordow
records = [
    (
        i + 1,
        str(products[i]),
        categories[i],
        sale_dates[i].strftime("%Y-%m-%d"),
        float(revenues[i])
    )
    for i in range(N)
]


# Wstawienie danych do SQLite
cursor.executemany("""
    INSERT INTO sales (
        sale_id,
        product,
        category,
        sale_date,
        revenue
    )
    VALUES (?, ?, ?, ?, ?)
""", records)

conn.commit()


# Naglowek programu
print("=" * 90)
print("ANALIZA SPRZEDAZY MIESIECZNEJ - 2024")
print("=" * 90)


# 1. Dane wejsciowe
section("1. DANE WEJSCIOWE")

sales = pd.read_sql_query("""
    SELECT *
    FROM sales
    ORDER BY sale_id
""", conn)

print(sales.head(15).to_string(index=False))

print(f"\nLiczba transakcji: {len(sales)}")
print(f"Liczba produktow: {sales['product'].nunique()}")
print(f"Liczba kategorii: {sales['category'].nunique()}")
print(f"Najwczesniejsza data: {sales['sale_date'].min()}")
print(f"Najpozniejsza data: {sales['sale_date'].max()}")


# 2. Statystyki calego roku
section("2. STATYSTYKI SPRZEDAZY ROCZNEJ")

annual_query = """
SELECT
    COUNT(*) AS liczba_transakcji,
    SUM(revenue) AS laczny_przychod,
    AVG(revenue) AS srednia_transakcja,
    MIN(revenue) AS minimalna_transakcja,
    MAX(revenue) AS maksymalna_transakcja
FROM sales
"""

annual = pd.read_sql_query(
    annual_query,
    conn
)

print(annual.round(2).to_string(index=False))

annual_revenue = float(
    annual.loc[0, "laczny_przychod"]
)

annual_transactions = int(
    annual.loc[0, "liczba_transakcji"]
)


# 3. Agregacja miesieczna
section("3. PODSUMOWANIE MIESIECZNE")

monthly_query = """
SELECT
    strftime('%Y-%m', sale_date) AS miesiac,
    SUM(revenue) AS przychod,
    COUNT(*) AS liczba_transakcji,
    AVG(revenue) AS srednia_transakcja
FROM sales
GROUP BY strftime('%Y-%m', sale_date)
ORDER BY miesiac ASC
"""

print(monthly_query)

monthly = pd.read_sql_query(
    monthly_query,
    conn
)

print(monthly.round(2).to_string(index=False))

print(f"\nLiczba miesiecy: {len(monthly)}")


# 4. Sredni przychod miesieczny
section("4. SREDNI PRZYCHOD MIESIECZNY")

average_query = """
SELECT AVG(m_rev) AS sredni_przychod_miesieczny
FROM (
    SELECT
        strftime('%Y-%m', sale_date) AS miesiac,
        SUM(revenue) AS m_rev
    FROM sales
    GROUP BY strftime('%Y-%m', sale_date)
)
"""

average_result = pd.read_sql_query(
    average_query,
    conn
)

average_monthly_revenue = float(
    average_result.loc[
        0,
        "sredni_przychod_miesieczny"
    ]
)

print(average_query)

print(
    f"Sredni przychod miesieczny: "
    f"{average_monthly_revenue:,.2f} PLN"
)


# 5. Tekstowa wizualizacja przychodow
section("5. TEKSTOWY TREND PRZYCHODOW")

print("Legenda: jeden znak = okolo 500 PLN\n")

for row in monthly.itertuples(index=False):

    bar_length = int(
        round(row.przychod / BAR_UNIT)
    )

    bar = "█" * bar_length

    print(
        f"{row.miesiac} | "
        f"{bar} "
        f"{row.przychod:,.2f} PLN"
    )


# 6. Miesiace z przychodem powyzej sredniej
section("6. MIESIACE Z PRZYCHODEM POWYZEJ SREDNIEJ")

best_months_query = """
SELECT
    strftime('%Y-%m', sale_date) AS miesiac,
    SUM(revenue) AS przychod,
    COUNT(*) AS liczba_transakcji,
    AVG(revenue) AS srednia_transakcja
FROM sales
GROUP BY strftime('%Y-%m', sale_date)
HAVING SUM(revenue) > (
    SELECT AVG(m_rev)
    FROM (
        SELECT
            strftime('%Y-%m', sale_date),
            SUM(revenue) AS m_rev
        FROM sales
        GROUP BY strftime('%Y-%m', sale_date)
    )
)
ORDER BY przychod DESC
"""

print(best_months_query)

best_months = pd.read_sql_query(
    best_months_query,
    conn
)

best_months["roznica_od_sredniej"] = (
    best_months["przychod"]
    - average_monthly_revenue
)

best_months["powyzej_sredniej_pct"] = (
    best_months["roznica_od_sredniej"]
    / average_monthly_revenue
    * 100
)

print(
    best_months.round(2).to_string(index=False)
)

print(
    f"\nLiczba miesiecy powyzej sredniej: "
    f"{len(best_months)}"
)


# 7. Ranking wszystkich miesiecy
section("7. RANKING MIESIECZNY")

ranking = monthly.sort_values(
    "przychod",
    ascending=False
).reset_index(drop=True)

ranking.insert(
    0,
    "miejsce",
    np.arange(1, len(ranking) + 1)
)

ranking["udzial_roczny_pct"] = (
    ranking["przychod"]
    / annual_revenue
    * 100
)

print(ranking.round(2).to_string(index=False))

best_month = ranking.iloc[0]
worst_month = ranking.iloc[-1]

print(
    f"\nNajlepszy miesiac: "
    f"{best_month['miesiac']}"
)

print(
    f"Najwyzszy przychod: "
    f"{best_month['przychod']:,.2f} PLN"
)

print(
    f"Najslabszy miesiac: "
    f"{worst_month['miesiac']}"
)

print(
    f"Najnizszy przychod: "
    f"{worst_month['przychod']:,.2f} PLN"
)


# 8. Zmiana miesiac do miesiaca
section("8. DYNAMIKA PRZYCHODOW MIESIAC DO MIESIACA")

monthly_changes = monthly.copy()

monthly_changes["zmiana_PLN"] = (
    monthly_changes["przychod"].diff()
)

monthly_changes["zmiana_pct"] = (
    monthly_changes["przychod"].pct_change()
    * 100
)

monthly_changes["przychod_narastajaco"] = (
    monthly_changes["przychod"].cumsum()
)

print(
    monthly_changes[
        [
            "miesiac",
            "przychod",
            "zmiana_PLN",
            "zmiana_pct",
            "przychod_narastajaco"
        ]
    ].round(2).to_string(
        index=False,
        na_rep="---"
    )
)

growth_months = int(
    (monthly_changes["zmiana_pct"] > 0).sum()
)

decline_months = int(
    (monthly_changes["zmiana_pct"] < 0).sum()
)

print(f"\nMiesiace ze wzrostem: {growth_months}")
print(f"Miesiace ze spadkiem: {decline_months}")


# 9. Analiza wedlug kategorii
section("9. PRZYCHODY WEDLUG KATEGORII")

category_query = """
SELECT
    category,
    COUNT(*) AS liczba_transakcji,
    SUM(revenue) AS przychod,
    AVG(revenue) AS srednia_transakcja
FROM sales
GROUP BY category
ORDER BY przychod DESC
"""

category_summary = pd.read_sql_query(
    category_query,
    conn
)

category_summary["udzial_pct"] = (
    category_summary["przychod"]
    / annual_revenue
    * 100
)

print(
    category_summary.round(2).to_string(
        index=False
    )
)


# 10. Analiza kwartalna
section("10. PODSUMOWANIE KWARTALNE")

quarter_query = """
SELECT
    CAST(
        (
            CAST(strftime('%m', sale_date) AS INTEGER)
            - 1
        ) / 3 AS INTEGER
    ) + 1 AS kwartal,
    COUNT(*) AS liczba_transakcji,
    SUM(revenue) AS przychod,
    AVG(revenue) AS srednia_transakcja
FROM sales
GROUP BY kwartal
ORDER BY kwartal
"""

quarterly = pd.read_sql_query(
    quarter_query,
    conn
)

quarterly["udzial_pct"] = (
    quarterly["przychod"]
    / annual_revenue
    * 100
)

print(
    quarterly.round(2).to_string(index=False)
)


# 11. Alternatywne rozwiazanie - CTE
section("11. ALTERNATYWNE ROZWIAZANIE - CTE")

cte_query = """
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', sale_date) AS miesiac,
        SUM(revenue) AS przychod,
        COUNT(*) AS liczba_transakcji,
        AVG(revenue) AS srednia_transakcja
    FROM sales
    GROUP BY strftime('%Y-%m', sale_date)
)
SELECT *
FROM monthly_sales
WHERE przychod > (
    SELECT AVG(przychod)
    FROM monthly_sales
)
ORDER BY przychod DESC
"""

print(cte_query)

cte_result = pd.read_sql_query(
    cte_query,
    conn
)

print(
    cte_result.round(2).to_string(index=False)
)

cte_matches = np.allclose(
    cte_result["przychod"],
    best_months["przychod"]
) and (
    cte_result["miesiac"].tolist()
    == best_months["miesiac"].tolist()
)

print(
    f"\nCzy HAVING i CTE sa zgodne: "
    f"{cte_matches}"
)


# 12. Weryfikacja SQL za pomoca Pandas
section("12. WERYFIKACJA SQL ZA POMOCA PANDAS")

sales_pandas = sales.copy()

sales_pandas["miesiac"] = (
    pd.to_datetime(sales_pandas["sale_date"])
    .dt.strftime("%Y-%m")
)

monthly_pandas = (
    sales_pandas
    .groupby("miesiac")
    .agg(
        przychod=("revenue", "sum"),
        liczba_transakcji=("sale_id", "count"),
        srednia_transakcja=("revenue", "mean")
    )
    .reset_index()
    .sort_values("miesiac")
    .reset_index(drop=True)
)

print(
    monthly_pandas.round(2).to_string(index=False)
)

months_match = (
    monthly["miesiac"].tolist()
    == monthly_pandas["miesiac"].tolist()
)

revenue_match = np.allclose(
    monthly["przychod"],
    monthly_pandas["przychod"]
)

count_match = np.array_equal(
    monthly["liczba_transakcji"],
    monthly_pandas["liczba_transakcji"]
)

average_match = np.allclose(
    monthly["srednia_transakcja"],
    monthly_pandas["srednia_transakcja"]
)

print(f"\nZgodnosc miesiecy: {months_match}")
print(f"Zgodnosc przychodow: {revenue_match}")
print(f"Zgodnosc liczby transakcji: {count_match}")
print(f"Zgodnosc srednich: {average_match}")


# 13. Plan wykonania zapytania
section("13. EXPLAIN QUERY PLAN")

monthly_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + monthly_query,
    conn
)

print("Plan agregacji miesiecznej:\n")
print(monthly_plan.to_string(index=False))

having_plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + best_months_query,
    conn
)

print("\nPlan zapytania HAVING:\n")
print(having_plan.to_string(index=False))


# 14. Automatyczne testy
section("14. WERYFIKACJA")

expected_months = pd.period_range(
    "2024-01",
    "2024-12",
    freq="M"
).astype(str).tolist()

expected_best_months = monthly.loc[
    monthly["przychod"] > average_monthly_revenue
].sort_values(
    "przychod",
    ascending=False
)

final_sales = pd.read_sql_query("""
    SELECT *
    FROM sales
    ORDER BY sale_id
""", conn)

tests = {
    "Tabela zawiera 1000 transakcji":
        len(sales) == 1000,

    "Tabela zawiera 5 kolumn":
        sales.shape[1] == 5,

    "Identyfikatory sa unikalne":
        sales["sale_id"].is_unique,

    "Brak brakujacych wartosci":
        not sales.isna().any().any(),

    "Rok 2024 zawiera 366 dni":
        number_of_days == 366,

    "Wszystkie daty sa z 2024 roku":
        sales["sale_date"].between(
            "2024-01-01",
            "2024-12-31"
        ).all(),

    "Wszystkie przychody sa dodatnie":
        (sales["revenue"] > 0).all(),

    "Przychody mieszcza sie w zakresie 50-1000":
        sales["revenue"].between(50, 1000).all(),

    "Kategorie odpowiadaja produktom":
        (
            sales["product"].map(product_categories)
            == sales["category"]
        ).all(),

    "Agregacja zawiera 12 miesiecy":
        len(monthly) == 12,

    "Wszystkie miesiace sa poprawne":
        monthly["miesiac"].tolist() == expected_months,

    "Miesiace sa posortowane chronologicznie":
        monthly["miesiac"].is_monotonic_increasing,

    "Roczna liczba transakcji wynosi 1000":
        annual_transactions == N,

    "Suma miesiecznych transakcji wynosi 1000":
        monthly["liczba_transakcji"].sum() == N,

    "Suma miesiecznych przychodow jest zgodna":
        np.isclose(
            monthly["przychod"].sum(),
            annual_revenue
        ),

    "Sredni przychod miesieczny jest poprawny":
        np.isclose(
            average_monthly_revenue,
            annual_revenue / 12
        ),

    "Srednie wartosci transakcji sa poprawne":
        np.allclose(
            monthly["srednia_transakcja"],
            monthly["przychod"]
            / monthly["liczba_transakcji"]
        ),

    "Wszystkie najlepsze miesiace przekraczaja srednia":
        (
            best_months["przychod"]
            > average_monthly_revenue
        ).all(),

    "HAVING zwraca wszystkie wlasciwe miesiace":
        best_months["miesiac"].tolist()
        == expected_best_months["miesiac"].tolist(),

    "Najlepsze miesiace sa posortowane malejaco":
        best_months["przychod"].is_monotonic_decreasing,

    "Roznice od sredniej sa dodatnie":
        (best_months["roznica_od_sredniej"] > 0).all(),

    "Roznice procentowe sa poprawne":
        np.allclose(
            best_months["powyzej_sredniej_pct"],
            (
                best_months["przychod"]
                / average_monthly_revenue - 1
            ) * 100
        ),

    "Ranking obejmuje 12 miesiecy":
        len(ranking) == 12,

    "Ranking jest posortowany malejaco":
        ranking["przychod"].is_monotonic_decreasing,

    "Udzialy miesieczne sumuja sie do 100 procent":
        np.isclose(
            ranking["udzial_roczny_pct"].sum(),
            100
        ),

    "Przychod narastajacy jest zgodny z rocznym":
        np.isclose(
            monthly_changes[
                "przychod_narastajaco"
            ].iloc[-1],
            annual_revenue
        ),

    "Pierwsza zmiana miesieczna jest nieokreslona":
        pd.isna(
            monthly_changes["zmiana_pct"].iloc[0]
        ),

    "Suma przychodow kategorii jest zgodna":
        np.isclose(
            category_summary["przychod"].sum(),
            annual_revenue
        ),

    "Agregacja zawiera 4 kwartaly":
        len(quarterly) == 4,

    "Suma kwartalnych transakcji wynosi 1000":
        quarterly["liczba_transakcji"].sum() == N,

    "Suma kwartalnych przychodow jest zgodna":
        np.isclose(
            quarterly["przychod"].sum(),
            annual_revenue
        ),

    "HAVING i CTE zwracaja zgodne wyniki":
        cte_matches,

    "SQL i Pandas - miesiace sa zgodne":
        months_match,

    "SQL i Pandas - przychody sa zgodne":
        revenue_match,

    "SQL i Pandas - liczby transakcji sa zgodne":
        count_match,

    "SQL i Pandas - srednie sa zgodne":
        average_match,

    "Plan agregacji nie jest pusty":
        not monthly_plan.empty,

    "Plan HAVING nie jest pusty":
        not having_plan.empty,

    "Oryginalna tabela pozostala niezmieniona":
        sales.equals(final_sales)
}

passed = 0

for name, result in tests.items():

    result = bool(result)

    print(f"Czy {name}: {result}")

    if result:
        passed += 1

print(f"\nZaliczone testy: {passed}/{len(tests)}")


# 15. Wnioski
section("15. WNIOSKI")

print("1. NumPy pozwala generowac syntetyczne dane sprzedazowe.")
print("2. SQLite przechowuje daty w formacie ISO YYYY-MM-DD.")
print("3. strftime('%Y-%m') wyodrebnia rok i miesiac.")
print("4. GROUP BY pozwala agregowac dane miesiecznie.")
print("5. SUM oblicza laczny przychod.")
print("6. COUNT oblicza liczbe transakcji.")
print("7. AVG oblicza srednia wartosc transakcji.")
print("8. HAVING filtruje wyniki po agregacji.")
print("9. Podzapytanie oblicza sredni przychod miesieczny.")
print("10. CTE upraszcza wieloetapowe zapytania.")
print("11. Tekstowe slupki pozwalaja porownywac przychody.")
print("12. pct_change oblicza dynamike miesiac do miesiaca.")
print("13. cumsum oblicza przychod narastajaco.")
print("14. EXPLAIN QUERY PLAN pokazuje sposob wykonania SQL.")
print("15. Pandas pozwala niezaleznie zweryfikowac agregacje SQL.")
print("16. Losowe dane nie potwierdzaja rzeczywistej sezonowosci.")


# Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba transakcji: {annual_transactions}")
print(f"Liczba miesiecy: {len(monthly)}")
print(f"Liczba kwartalow: {len(quarterly)}")

print(
    f"Roczny przychod: "
    f"{annual_revenue:,.2f} PLN"
)

print(
    f"Sredni przychod miesieczny: "
    f"{average_monthly_revenue:,.2f} PLN"
)

print(
    f"Miesiace powyzej sredniej: "
    f"{len(best_months)}"
)

print(
    f"Najlepszy miesiac: "
    f"{best_month['miesiac']}"
)

print(
    f"Najslabszy miesiac: "
    f"{worst_month['miesiac']}"
)

print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

if passed == len(tests):
    print("\nWszystkie testy zakonczone pomyslnie.")
    print("Zadanie 13 wykonane poprawnie.")
else:
    raise AssertionError(
        "Nie wszystkie testy zostaly zaliczone."
    )
