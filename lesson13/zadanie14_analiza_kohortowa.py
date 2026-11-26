# Lekcja 13 - Zadanie 14: Analiza kohortowa klientow

import sqlite3
import pandas as pd
import numpy as np
import time


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 80)


# Konfiguracja
np.random.seed(42)

N_CUSTOMERS = 600
START_DATE = pd.Timestamp("2024-01-01")
END_DATE = pd.Timestamp("2024-12-31")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)

start_time = time.perf_counter()


# ============================================================
# 1. UTWORZENIE BAZY DANYCH SQLITE
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.executescript("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        registration_date TEXT NOT NULL
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount > 0),
        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
    );
""")


# ============================================================
# 2. GENEROWANIE KLIENTOW
# ============================================================

section("1. GENEROWANIE DANYCH KLIENTOW")

registration_offsets = np.random.randint(
    0,
    (END_DATE - START_DATE).days + 1,
    size=N_CUSTOMERS
)

registration_dates = (
    START_DATE
    + pd.to_timedelta(registration_offsets, unit="D")
)

customers = pd.DataFrame({
    "customer_id": np.arange(1, N_CUSTOMERS + 1),
    "registration_date": registration_dates.strftime("%Y-%m-%d")
})

customers.to_sql(
    "customers",
    conn,
    if_exists="append",
    index=False
)

print(customers.head(10).to_string(index=False))
print(f"\nLiczba klientow: {len(customers)}")


# ============================================================
# 3. GENEROWANIE ZAMOWIEN
# ============================================================

section("2. GENEROWANIE ZAMOWIEN")

order_records = []
order_id = 1

for customer in customers.itertuples(index=False):

    registration_date = pd.Timestamp(
        customer.registration_date
    )

    available_days = (
        END_DATE - registration_date
    ).days

    number_of_orders = np.random.poisson(
        0.8 * (available_days + 1) / 30
    )

    for _ in range(number_of_orders):

        offset = np.random.randint(
            0,
            available_days + 1
        )

        order_date = (
            registration_date
            + pd.Timedelta(days=int(offset))
        )

        amount = round(
            float(np.random.uniform(20, 1000)),
            2
        )

        order_records.append({
            "order_id": order_id,
            "customer_id": customer.customer_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "amount": amount
        })

        order_id += 1


orders = pd.DataFrame(order_records)

orders.to_sql(
    "orders",
    conn,
    if_exists="append",
    index=False
)

conn.commit()

print(orders.head(10).to_string(index=False))
print(f"\nLiczba zamowien: {len(orders)}")
print(f"Laczny przychod: {orders['amount'].sum():.2f} PLN")


# ============================================================
# 4. PODZIAL KLIENTOW NA KOHORTY
# ============================================================

section("3. KOHORTY MIESIECZNE")

query_cohorts = """
SELECT
    strftime('%Y-%m', registration_date) AS cohort,
    COUNT(*) AS customers_count
FROM customers
GROUP BY cohort
ORDER BY cohort
"""

cohorts = pd.read_sql_query(
    query_cohorts,
    conn
)

print(query_cohorts)
print(cohorts.to_string(index=False))

print(f"\nLiczba kohort: {len(cohorts)}")


# ============================================================
# 5. ANALIZA KOHORTOWA SQL
# ============================================================

section("4. STATYSTYKI WEDLUG KOHORT")

query_summary = """
SELECT
    strftime('%Y-%m', c.registration_date) AS cohort,

    COUNT(DISTINCT c.customer_id) AS customers_count,

    COUNT(o.order_id) AS orders_count,

    COALESCE(SUM(o.amount), 0) AS total_revenue,

    COALESCE(AVG(o.amount), 0) AS avg_order_value,

    COALESCE(SUM(o.amount), 0)
        / COUNT(DISTINCT c.customer_id) AS ltv,

    1.0 * COUNT(o.order_id)
        / COUNT(DISTINCT c.customer_id)
        AS orders_per_customer

FROM customers AS c

LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id

GROUP BY cohort

ORDER BY cohort
"""

summary = pd.read_sql_query(
    query_summary,
    conn
)

print(query_summary)
print(summary.round(2).to_string(index=False))


# ============================================================
# 6. STATYSTYKI GLOBALNE
# ============================================================

section("5. STATYSTYKI GLOBALNE")

total_customers = len(customers)
total_orders = len(orders)
total_revenue = orders["amount"].sum()

global_ltv = total_revenue / total_customers
avg_order_value = total_revenue / total_orders

active_customers = orders["customer_id"].nunique()

inactive_customers = (
    total_customers - active_customers
)

global_stats = pd.DataFrame({
    "Metryka": [
        "Liczba klientow",
        "Liczba zamowien",
        "Laczny przychod",
        "Srednia wartosc zamowienia",
        "Globalny LTV",
        "Klienci aktywni",
        "Klienci bez zamowien"
    ],
    "Wartosc": [
        total_customers,
        total_orders,
        total_revenue,
        avg_order_value,
        global_ltv,
        active_customers,
        inactive_customers
    ]
})

print(global_stats.round(2).to_string(index=False))


# ============================================================
# 7. MIESIACE OD REJESTRACJI
# ============================================================

section("6. PRZYCHOD WEDLUG MIESIECY OD REJESTRACJI")

query_monthly = """
WITH cohort_sizes AS (
    SELECT
        strftime('%Y-%m', registration_date) AS cohort,
        COUNT(*) AS cohort_size
    FROM customers
    GROUP BY cohort
),

order_activity AS (
    SELECT
        strftime('%Y-%m', c.registration_date) AS cohort,

        (
            CAST(strftime('%Y', o.order_date) AS INTEGER)
            - CAST(strftime('%Y', c.registration_date) AS INTEGER)
        ) * 12
        +
        (
            CAST(strftime('%m', o.order_date) AS INTEGER)
            - CAST(strftime('%m', c.registration_date) AS INTEGER)
        ) AS months_since_registration,

        o.customer_id,
        o.order_id,
        o.amount

    FROM customers AS c

    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
)

SELECT
    a.cohort,
    a.months_since_registration,

    s.cohort_size,

    COUNT(DISTINCT a.customer_id) AS active_customers,

    COUNT(a.order_id) AS orders_count,

    SUM(a.amount) AS monthly_revenue,

    SUM(a.amount) / s.cohort_size AS monthly_ltv

FROM order_activity AS a

INNER JOIN cohort_sizes AS s
    ON a.cohort = s.cohort

GROUP BY
    a.cohort,
    a.months_since_registration,
    s.cohort_size

ORDER BY
    a.cohort,
    a.months_since_registration
"""

monthly = pd.read_sql_query(
    query_monthly,
    conn
)

print(monthly.round(2).to_string(index=False))


# ============================================================
# 8. TABELA PIVOT
# ============================================================

section("7. TABELA PIVOT - MIESIECZNY LTV")

pivot = monthly.pivot(
    index="cohort",
    columns="months_since_registration",
    values="monthly_ltv"
)

pivot = pivot.reindex(
    index=cohorts["cohort"].tolist(),
    columns=range(12)
)

# Uzupelnienie obserwowanych miesiecy bez zamowien.
# Przyszle, nieobserwowane miesiace pozostaja NaN.

for cohort in pivot.index:

    cohort_period = pd.Period(cohort, freq="M")

    for month in pivot.columns:

        activity_period = cohort_period + month

        if activity_period <= END_DATE.to_period("M"):

            if pd.isna(pivot.loc[cohort, month]):
                pivot.loc[cohort, month] = 0.0

pivot.columns = [
    f"M{month}" for month in pivot.columns
]

print(
    pivot.round(2).to_string(
        na_rep="---"
    )
)


# ============================================================
# 9. KWARTYLE LTV
# ============================================================

section("8. KWARTYLE MIESIECZNEGO LTV")

valid_values = pivot.to_numpy().ravel()

valid_values = valid_values[
    ~np.isnan(valid_values)
]

q1, q2, q3 = np.percentile(
    valid_values,
    [25, 50, 75]
)

print(f"Q1 (25%): {q1:.2f} PLN")
print(f"Q2 (50%): {q2:.2f} PLN")
print(f"Q3 (75%): {q3:.2f} PLN")

print(f"\nMinimum: {valid_values.min():.2f} PLN")
print(f"Maksimum: {valid_values.max():.2f} PLN")


# ============================================================
# 10. TEKSTOWA HEATMAPA
# ============================================================

section("9. TEKSTOWA HEATMAPA LTV")


def ltv_symbol(value):

    if pd.isna(value):
        return "."

    if value <= q1:
        return "░"

    if value <= q2:
        return "▒"

    if value <= q3:
        return "▓"

    return "█"


print("Legenda:")
print(". - brak obserwacji")
print("░ - niski LTV")
print("▒ - sredni LTV")
print("▓ - wysoki LTV")
print("█ - bardzo wysoki LTV")

print()

header = "Kohorta  | " + " ".join(
    f"{column:>3}"
    for column in pivot.columns
)

print(header)
print("-" * len(header))

for cohort, row in pivot.iterrows():

    symbols = " ".join(
        f"{ltv_symbol(value):>3}"
        for value in row
    )

    print(f"{cohort}  | {symbols}")


# ============================================================
# 11. RANKING KOHORT
# ============================================================

section("10. RANKING KOHORT WEDLUG LTV")

ranking = summary.sort_values(
    "ltv",
    ascending=False
).reset_index(drop=True)

ranking.index = ranking.index + 1

print(
    ranking[
        [
            "cohort",
            "customers_count",
            "orders_count",
            "total_revenue",
            "ltv"
        ]
    ].round(2).to_string()
)

best_cohort = ranking.iloc[0]
worst_cohort = ranking.iloc[-1]

print(
    f"\nNajwyzszy LTV: "
    f"{best_cohort['cohort']} - "
    f"{best_cohort['ltv']:.2f} PLN"
)

print(
    f"Najnizszy LTV: "
    f"{worst_cohort['cohort']} - "
    f"{worst_cohort['ltv']:.2f} PLN"
)


# ============================================================
# 12. TEKSTOWY WYKRES LTV
# ============================================================

section("11. TEKSTOWY WYKRES LTV KOHORT")

print("Legenda: jeden znak = okolo 100 PLN\n")

for row in summary.itertuples(index=False):

    bar = "█" * int(round(row.ltv / 100))

    print(
        f"{row.cohort} | "
        f"{bar:<45} "
        f"{row.ltv:>10.2f} PLN"
    )


# ============================================================
# 13. SKUMULOWANY LTV
# ============================================================

section("12. SKUMULOWANY LTV")

cumulative_ltv = pivot.cumsum(axis=1)

print(
    cumulative_ltv.round(2).to_string(
        na_rep="---"
    )
)

# Porownanie kohort w jednakowym okresie obserwacji

section("13. POROWNANIE KOHORT PO 3 MIESIACACH")

ltv_3_months = (
    cumulative_ltv["M2"]
    .dropna()
    .sort_values(ascending=False)
)

print(
    ltv_3_months.round(2)
    .rename("LTV_3_months")
    .to_string()
)

print(
    "\nPorownanie M0-M2 ogranicza problem "
    "roznej dlugosci obserwacji kohort."
)


# ============================================================
# 14. WERYFIKACJA ZA POMOCA PANDAS
# ============================================================

section("14. WERYFIKACJA SQL ZA POMOCA PANDAS")

merged = customers.merge(
    orders,
    on="customer_id",
    how="left",
    validate="one_to_many"
)

merged["cohort"] = pd.to_datetime(
    merged["registration_date"]
).dt.strftime("%Y-%m")

pandas_summary = (
    merged.groupby("cohort")
    .agg(
        customers_count=("customer_id", "nunique"),
        orders_count=("order_id", "count"),
        total_revenue=("amount", "sum"),
        avg_order_value=("amount", "mean")
    )
    .reset_index()
)

pandas_summary["avg_order_value"] = (
    pandas_summary["avg_order_value"].fillna(0)
)

pandas_summary["ltv"] = (
    pandas_summary["total_revenue"]
    / pandas_summary["customers_count"]
)

pandas_summary["orders_per_customer"] = (
    pandas_summary["orders_count"]
    / pandas_summary["customers_count"]
)

print(
    pandas_summary.round(2).to_string(index=False)
)

sql_pandas_equal = (
    summary["cohort"].equals(
        pandas_summary["cohort"]
    )
    and np.allclose(
        summary.drop(columns="cohort").to_numpy(),
        pandas_summary.drop(columns="cohort").to_numpy()
    )
)

print(
    f"\nCzy SQL i Pandas sa zgodne: "
    f"{sql_pandas_equal}"
)


# ============================================================
# 15. PLAN WYKONANIA ZAPYTANIA
# ============================================================

section("15. EXPLAIN QUERY PLAN")

plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_summary,
    conn
)

print(plan.to_string(index=False))


# ============================================================
# 16. AUTOMATYCZNE TESTY
# ============================================================

section("16. AUTOMATYCZNE TESTY")

registration_check = orders.merge(
    customers,
    on="customer_id",
    validate="many_to_one"
)

last_ltv = cumulative_ltv.apply(
    lambda row: row.dropna().iloc[-1],
    axis=1
)

expected_ltv = summary.set_index("cohort")["ltv"]

expected_observations = sum(
    12 - pd.Period(cohort, freq="M").month + 1
    for cohort in pivot.index
)

tests = {
    "Wygenerowano 600 klientow":
        len(customers) == 600,

    "Wygenerowano zamowienia":
        len(orders) > 0,

    "Identyfikatory klientow sa unikalne":
        customers["customer_id"].is_unique,

    "Identyfikatory zamowien sa unikalne":
        orders["order_id"].is_unique,

    "Brak NaN w tabeli customers":
        not customers.isna().any().any(),

    "Brak NaN w tabeli orders":
        not orders.isna().any().any(),

    "Wszystkie kwoty sa dodatnie":
        (orders["amount"] > 0).all(),

    "Wszystkie zamowienia maja klienta":
        orders["customer_id"].isin(
            customers["customer_id"]
        ).all(),

    "Daty rejestracji nie przekraczaja konca roku":
        (
            pd.to_datetime(customers["registration_date"])
            <= END_DATE
        ).all(),

    "Zamowienia nie poprzedzaja rejestracji":
        (
            registration_check["order_date"]
            >= registration_check["registration_date"]
        ).all(),

    "Zamowienia nie przekraczaja konca roku":
        (
            pd.to_datetime(orders["order_date"])
            <= END_DATE
        ).all(),

    "Utworzono 12 kohort":
        len(cohorts) == 12,

    "Suma klientow w kohortach wynosi 600":
        cohorts["customers_count"].sum() == 600,

    "Podsumowanie zawiera 12 kohort":
        len(summary) == 12,

    "LEFT JOIN zachowuje wszystkich klientow":
        summary["customers_count"].sum()
        == total_customers,

    "Liczba zamowien w kohortach jest zgodna":
        summary["orders_count"].sum()
        == total_orders,

    "Przychod kohort jest zgodny":
        np.isclose(
            summary["total_revenue"].sum(),
            total_revenue
        ),

    "LTV kohort obliczono poprawnie":
        np.allclose(
            summary["ltv"],
            summary["total_revenue"]
            / summary["customers_count"]
        ),

    "LTV nie przyjmuje wartosci ujemnych":
        (summary["ltv"] >= 0).all(),

    "Srednia wartosc zamowienia jest poprawna":
        np.allclose(
            summary["avg_order_value"],
            np.divide(
                summary["total_revenue"].to_numpy(),
                summary["orders_count"].to_numpy(),
                out=np.zeros(len(summary)),
                where=summary["orders_count"].to_numpy() > 0
            )
        ),

    "Miesiace od rejestracji sa nieujemne":
        (
            monthly["months_since_registration"] >= 0
        ).all(),

    "Maksymalny okres wynosi 11 miesiecy":
        (
            monthly["months_since_registration"] <= 11
        ).all(),

    "Przychod miesieczny jest zgodny":
        np.isclose(
            monthly["monthly_revenue"].sum(),
            total_revenue
        ),

    "Liczba miesiecznych zamowien jest zgodna":
        monthly["orders_count"].sum()
        == total_orders,

    "Tabela pivot ma rozmiar 12x12":
        pivot.shape == (12, 12),

    "Liczba obserwowanych komorek jest poprawna":
        pivot.notna().sum().sum()
        == expected_observations,

    "Heatmapa zawiera brakujace obserwacje":
        pivot.isna().any().any(),

    "Kwartyle sa uporzadkowane":
        q1 <= q2 <= q3,

    "Brak obserwacji ma symbol kropki":
        ltv_symbol(np.nan) == ".",

    "Niski LTV ma poprawny symbol":
        ltv_symbol(q1) == "░",

    "Bardzo wysoki LTV ma poprawny symbol":
        ltv_symbol(q3 + 1) == "█",

    "Ranking jest posortowany malejaco":
        ranking["ltv"].is_monotonic_decreasing,

    "Skumulowany LTV jest zgodny z podsumowaniem":
        np.allclose(
            last_ltv.sort_index(),
            expected_ltv.sort_index()
        ),

    "Globalny LTV jest zgodny z kohortami":
        np.isclose(
            np.average(
                summary["ltv"],
                weights=summary["customers_count"]
            ),
            global_ltv
        ),

    "SQL i Pandas zwracaja zgodne wyniki":
        sql_pandas_equal,

    "Tabela customers pozostala niezmieniona":
        pd.read_sql_query(
            "SELECT COUNT(*) AS n FROM customers",
            conn
        ).iloc[0, 0] == total_customers,

    "Tabela orders pozostala niezmieniona":
        pd.read_sql_query(
            "SELECT COUNT(*) AS n FROM orders",
            conn
        ).iloc[0, 0] == total_orders
}

passed = 0

for name, result in tests.items():

    if result:
        passed += 1

    print(f"Czy {name}: {bool(result)}")

print(f"\nZaliczone testy: {passed}/{len(tests)}")


# ============================================================
# 17. WNIOSKI
# ============================================================

section("17. WNIOSKI")

conclusions = [
    "Kohorta grupuje klientow wedlug miesiaca rejestracji.",
    "LEFT JOIN zachowuje klientow bez zamowien.",
    "COUNT DISTINCT zapobiega wielokrotnemu liczeniu klientow.",
    "COUNT(order_id) nie liczy wartosci NULL.",
    "SUM pozwala obliczyc laczny przychod.",
    "AVG pozwala obliczyc srednia wartosc zamowienia.",
    "LTV to przychod przypadajacy na klienta.",
    "Miesieczny LTV uwzglednia cala liczebnosc kohorty.",
    "strftime pozwala grupowac dane wedlug miesiaca.",
    "CTE ulatwia budowanie zlozonych zapytan SQL.",
    "Pivot przeksztalca dane w macierz kohortowa.",
    "Kwartyle wyznaczaja poziomy intensywnosci heatmapy.",
    "NaN oznacza okres jeszcze nieobserwowany.",
    "Zero oznacza obserwowany okres bez przychodu.",
    "Skumulowany LTV pokazuje przychod narastajaco.",
    "Starsze kohorty maja dluzszy okres obserwacji.",
    "Kohorty nalezy porownywac w jednakowym horyzoncie.",
    "SQL i Pandas pozwalaja uzyskac zgodne wyniki.",
    "Dane syntetyczne nie dowodza rzeczywistych zachowan klientow."
]

for i, conclusion in enumerate(conclusions, start=1):
    print(f"{i}. {conclusion}")


# ============================================================
# 18. PODSUMOWANIE
# ============================================================

section("PODSUMOWANIE")

elapsed_time = time.perf_counter() - start_time

print(f"Liczba klientow: {total_customers}")
print(f"Liczba zamowien: {total_orders}")
print(f"Liczba kohort: {len(cohorts)}")
print(f"Laczny przychod: {total_revenue:.2f} PLN")
print(f"Srednia wartosc zamowienia: {avg_order_value:.2f} PLN")
print(f"Globalny LTV: {global_ltv:.2f} PLN")
print(f"Klienci aktywni: {active_customers}")
print(f"Klienci bez zamowien: {inactive_customers}")
print(f"Rozmiar heatmapy: {pivot.shape}")
print(f"Liczba obserwowanych komorek: {expected_observations}")
print(f"Najlepsza kohorta wedlug LTV: {best_cohort['cohort']}")
print(f"Najwyzszy LTV: {best_cohort['ltv']:.2f} PLN")
print(f"Czas wykonania: {elapsed_time:.4f} s")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

assert passed == len(tests), "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 14 wykonane poprawnie.")
