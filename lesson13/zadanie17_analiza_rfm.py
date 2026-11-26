# Lekcja 13 - Zadanie 17: Analiza RFM
# Recency, Frequency, Monetary

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


# Konfiguracja
REFERENCE_DATE = "2025-01-01"
N_CUSTOMERS = 200

rng = np.random.default_rng(42)

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")


# ============================================================
# 1. TWORZENIE TABEL
# ============================================================

cursor.executescript("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        amount REAL NOT NULL CHECK (amount >= 0),
        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
    );
""")


# ============================================================
# 2. GENEROWANIE KLIENTOW
# ============================================================

cities = [
    "Warszawa",
    "Krakow",
    "Gdansk",
    "Wroclaw",
    "Poznan",
    "Kolobrzeg"
]

customers = [
    (
        customer_id,
        f"Klient_{customer_id:03d}",
        str(rng.choice(cities))
    )
    for customer_id in range(1, N_CUSTOMERS + 1)
]

cursor.executemany("""
    INSERT INTO customers (
        customer_id,
        name,
        city
    )
    VALUES (?, ?, ?)
""", customers)


# ============================================================
# 3. GENEROWANIE ZAMOWIEN
# ============================================================

orders = []
order_id = 1

reference_date = pd.Timestamp(REFERENCE_DATE)

for customer_id in range(1, N_CUSTOMERS + 1):

    # Rozne profile aktywnosci klientow
    if customer_id <= 30:
        # Bardzo aktywni klienci
        frequency = int(rng.integers(10, 26))
        recency = int(rng.integers(1, 31))
        min_amount = 300
        max_amount = 1000

    elif customer_id <= 100:
        # Regularni klienci
        frequency = int(rng.integers(2, 10))
        recency = int(rng.integers(1, 91))
        min_amount = 50
        max_amount = 500

    elif customer_id <= 150:
        # Klienci zagrozeni utrata
        frequency = int(rng.integers(1, 9))
        recency = int(rng.integers(91, 181))
        min_amount = 50
        max_amount = 700

    elif customer_id <= 190:
        # Klienci nieaktywni
        frequency = int(rng.integers(1, 6))
        recency = int(rng.integers(181, 331))
        min_amount = 30
        max_amount = 400

    else:
        # Klienci bez zamowien
        continue

    for number in range(frequency):

        if number == 0:
            days_ago = recency
        else:
            days_ago = int(
                rng.integers(recency, 367)
            )

        order_date = (
            reference_date
            - pd.Timedelta(days=days_ago)
        ).strftime("%Y-%m-%d")

        amount = round(
            float(rng.uniform(min_amount, max_amount)),
            2
        )

        orders.append((
            order_id,
            customer_id,
            order_date,
            amount
        ))

        order_id += 1


cursor.executemany("""
    INSERT INTO orders (
        order_id,
        customer_id,
        order_date,
        amount
    )
    VALUES (?, ?, ?, ?)
""", orders)

conn.commit()


# ============================================================
# 4. DANE WEJSCIOWE
# ============================================================

section("ANALIZA RFM - SEGMENTACJA KLIENTOW")

customers_df = pd.read_sql_query(
    "SELECT * FROM customers",
    conn
)

orders_df = pd.read_sql_query(
    "SELECT * FROM orders",
    conn
)

section("1. TABELA CUSTOMERS")

show_table(customers_df.head(10))

print(f"\nLiczba klientow: {len(customers_df)}")

section("2. TABELA ORDERS")

show_table(orders_df.head(10))

print(f"\nLiczba zamowien: {len(orders_df)}")
print(f"Data referencyjna: {REFERENCE_DATE}")
print(f"Pierwsze zamowienie: {orders_df['order_date'].min()}")
print(f"Ostatnie zamowienie: {orders_df['order_date'].max()}")
print(f"Laczny przychod: {orders_df['amount'].sum():,.2f} PLN")


# ============================================================
# 5. OBLICZENIE RFM W SQL
# ============================================================

section("3. OBLICZENIE RECENCY, FREQUENCY I MONETARY")

rfm_query = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    MAX(o.order_date) AS last_order_date,

    CAST(
        julianday(:reference_date)
        - julianday(MAX(o.order_date))
        AS INTEGER
    ) AS recency,

    COUNT(o.order_id) AS frequency,

    COALESCE(SUM(o.amount), 0) AS monetary

FROM customers AS c

LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
    AND o.order_date <= :reference_date

GROUP BY
    c.customer_id,
    c.name,
    c.city

ORDER BY c.customer_id
"""

params = {
    "reference_date": REFERENCE_DATE
}

print(rfm_query)

rfm = pd.read_sql_query(
    rfm_query,
    conn,
    params=params
)

show_table(rfm.head(15).round(2))

print(f"\nLiczba klientow w analizie RFM: {len(rfm)}")

print(
    "Klienci bez zamowien:",
    (rfm["frequency"] == 0).sum()
)


# ============================================================
# 6. SEGMENTACJA CASE WHEN
# ============================================================

section("4. SEGMENTACJA KLIENTOW - CASE WHEN")

segmentation_query = f"""
WITH rfm AS (
    {rfm_query}
)

SELECT
    customer_id,
    name,
    city,
    last_order_date,
    recency,
    frequency,
    monetary,

    CASE
        WHEN frequency = 0 THEN 'Lost'

        WHEN recency > 180 THEN 'Lost'

        WHEN recency > 90 THEN 'At-risk'

        WHEN recency <= 30
             AND frequency >= 10
             AND monetary >= 3000
        THEN 'VIP'

        ELSE 'Regular'
    END AS segment

FROM rfm

ORDER BY
    monetary DESC,
    customer_id ASC
"""

print(segmentation_query)

segmented = pd.read_sql_query(
    segmentation_query,
    conn,
    params=params
)

show_table(segmented.head(20).round(2))


# ============================================================
# 7. REGULY BIZNESOWE
# ============================================================

section("5. REGULY SEGMENTACJI")

rules = pd.DataFrame({
    "Segment": [
        "VIP",
        "Regular",
        "At-risk",
        "Lost"
    ],
    "Warunek": [
        "R <= 30, F >= 10, M >= 3000",
        "R <= 90, pozostali aktywni",
        "90 < R <= 180",
        "R > 180 lub F = 0"
    ],
    "Znaczenie": [
        "Najbardziej wartosciowi",
        "Aktywni klienci",
        "Zagrozeni utrata",
        "Nieaktywni lub bez zakupow"
    ]
})

show_table(rules)


# ============================================================
# 8. PODSUMOWANIE SEGMENTOW W SQL
# ============================================================

section("6. TABELA PODSUMOWUJACA SEGMENTY")

summary_query = f"""
WITH segmented AS (
    {segmentation_query}
)

SELECT
    segment,
    COUNT(*) AS customers_count,
    AVG(recency) AS avg_recency,
    AVG(frequency) AS avg_frequency,
    AVG(monetary) AS avg_monetary,
    SUM(frequency) AS total_orders,
    SUM(monetary) AS total_revenue,

    SUM(
        CASE
            WHEN frequency = 0 THEN 1
            ELSE 0
        END
    ) AS without_orders

FROM segmented

GROUP BY segment

ORDER BY
    CASE segment
        WHEN 'VIP' THEN 1
        WHEN 'Regular' THEN 2
        WHEN 'At-risk' THEN 3
        WHEN 'Lost' THEN 4
    END
"""

summary = pd.read_sql_query(
    summary_query,
    conn,
    params=params
)

summary["customers_pct"] = (
    summary["customers_count"]
    / N_CUSTOMERS
    * 100
)

total_revenue = segmented["monetary"].sum()

summary["revenue_pct"] = (
    summary["total_revenue"]
    / total_revenue
    * 100
)

show_table(summary.round(2))

print(
    "\nUwaga: AVG(recency) pomija NULL "
    "dla klientow bez zamowien."
)


# ============================================================
# 9. TEKSTOWA WIZUALIZACJA
# ============================================================

section("7. LICZBA KLIENTOW W SEGMENTACH")

print("Legenda: jeden znak = jeden klient\n")

for row in summary.itertuples(index=False):

    bar = "█" * int(row.customers_count)

    print(
        f"{row.segment:<10} | "
        f"{bar:<70} "
        f"{row.customers_count:>3} "
        f"({row.customers_pct:.1f}%)"
    )


section("8. PRZYCHOD WEDLUG SEGMENTOW")

print("Legenda: jeden znak = okolo 2% przychodu\n")

for row in summary.itertuples(index=False):

    bar = "█" * int(round(row.revenue_pct / 2))

    print(
        f"{row.segment:<10} | "
        f"{bar:<50} "
        f"{row.total_revenue:>12,.2f} PLN "
        f"({row.revenue_pct:.2f}%)"
    )


# ============================================================
# 10. STATYSTYKI RFM
# ============================================================

section("9. STATYSTYKI OPISOWE RFM")

statistics = segmented[
    ["recency", "frequency", "monetary"]
].describe()

print(statistics.round(2).to_string())


# ============================================================
# 11. TOP 10 KLIENTOW
# ============================================================

section("10. TOP 10 NAJBARDZIEJ WARTOSCIOWYCH KLIENTOW")

top_customers = segmented[
    [
        "customer_id",
        "name",
        "city",
        "recency",
        "frequency",
        "monetary",
        "segment"
    ]
].head(10)

show_table(top_customers.round(2))


# ============================================================
# 12. KLIENCI ZAGROZENI UTRATA
# ============================================================

section("11. KLIENCI AT-RISK")

at_risk = segmented[
    segmented["segment"] == "At-risk"
].sort_values(
    "monetary",
    ascending=False
)

show_table(at_risk.head(10).round(2))

print(f"\nLiczba klientow At-risk: {len(at_risk)}")

print(
    "Historyczny przychod klientow At-risk: "
    f"{at_risk['monetary'].sum():,.2f} PLN"
)


# ============================================================
# 13. KLIENCI BEZ ZAMOWIEN
# ============================================================

section("12. KLIENCI BEZ ZAMOWIEN")

without_orders = segmented[
    segmented["frequency"] == 0
]

show_table(without_orders)

print(
    "\nLiczba klientow bez zamowien:",
    len(without_orders)
)


# ============================================================
# 14. ANALIZA BIZNESOWA
# ============================================================

section("13. ANALIZA BIZNESOWA")

vip = segmented[
    segmented["segment"] == "VIP"
]

regular = segmented[
    segmented["segment"] == "Regular"
]

lost = segmented[
    segmented["segment"] == "Lost"
]

vip_customers_pct = len(vip) / N_CUSTOMERS * 100

vip_revenue_pct = (
    vip["monetary"].sum()
    / total_revenue
    * 100
)

print(f"Liczba klientow VIP: {len(vip)}")
print(f"Udzial klientow VIP: {vip_customers_pct:.2f}%")
print(f"Udzial VIP w przychodzie: {vip_revenue_pct:.2f}%")

print(
    "Srednia wartosc klienta VIP: "
    f"{vip['monetary'].mean():,.2f} PLN"
)

print(
    "Srednia wartosc klienta Regular: "
    f"{regular['monetary'].mean():,.2f} PLN"
)

print(
    "Historyczny przychod klientow Lost: "
    f"{lost['monetary'].sum():,.2f} PLN"
)

best_segment = summary.loc[
    summary["total_revenue"].idxmax()
]

largest_segment = summary.loc[
    summary["customers_count"].idxmax()
]

print(
    "\nSegment o najwyzszym przychodzie:",
    best_segment["segment"]
)

print(
    "Najliczniejszy segment:",
    largest_segment["segment"]
)


# ============================================================
# 15. REKOMENDACJE MARKETINGOWE
# ============================================================

section("14. REKOMENDACJE MARKETINGOWE")

recommendations = {
    "VIP": (
        "Program lojalnosciowy, oferty premium, "
        "indywidualna obsluga."
    ),
    "Regular": (
        "Cross-selling, up-selling, "
        "program punktowy."
    ),
    "At-risk": (
        "Kampania reaktywacyjna, rabat, "
        "przypomnienie o ofercie."
    ),
    "Lost": (
        "Kampania odzyskiwania dawnych klientow "
        "lub onboarding klientow bez zakupow."
    )
}

for segment, recommendation in recommendations.items():

    print(f"{segment:<10}: {recommendation}")


# ============================================================
# 16. WERYFIKACJA RFM ZA POMOCA PANDAS
# ============================================================

section("15. WERYFIKACJA SQL ZA POMOCA PANDAS")

orders_pd = orders_df.copy()

orders_pd["order_date"] = pd.to_datetime(
    orders_pd["order_date"]
)

orders_pd = orders_pd[
    orders_pd["order_date"] <= reference_date
]

pandas_rfm = orders_pd.groupby(
    "customer_id"
).agg(
    last_order_date=("order_date", "max"),
    frequency=("order_id", "count"),
    monetary=("amount", "sum")
).reset_index()

pandas_rfm = customers_df.merge(
    pandas_rfm,
    on="customer_id",
    how="left"
)

pandas_rfm["frequency"] = (
    pandas_rfm["frequency"]
    .fillna(0)
    .astype(int)
)

pandas_rfm["monetary"] = (
    pandas_rfm["monetary"]
    .fillna(0)
)

pandas_rfm["recency"] = (
    reference_date
    - pandas_rfm["last_order_date"]
).dt.days


# Niezalezna segmentacja w NumPy

conditions = [
    pandas_rfm["frequency"] == 0,

    pandas_rfm["recency"] > 180,

    pandas_rfm["recency"] > 90,

    (
        (pandas_rfm["recency"] <= 30)
        & (pandas_rfm["frequency"] >= 10)
        & (pandas_rfm["monetary"] >= 3000)
    )
]

choices = [
    "Lost",
    "Lost",
    "At-risk",
    "VIP"
]

pandas_rfm["segment"] = np.select(
    conditions,
    choices,
    default="Regular"
)

sql_sorted = segmented.sort_values(
    "customer_id"
).reset_index(drop=True)

pd_sorted = pandas_rfm.sort_values(
    "customer_id"
).reset_index(drop=True)

recency_match = np.allclose(
    sql_sorted["recency"],
    pd_sorted["recency"],
    equal_nan=True
)

frequency_match = np.array_equal(
    sql_sorted["frequency"],
    pd_sorted["frequency"]
)

monetary_match = np.allclose(
    sql_sorted["monetary"],
    pd_sorted["monetary"]
)

segment_match = np.array_equal(
    sql_sorted["segment"],
    pd_sorted["segment"]
)

print(f"Recency SQL vs Pandas: {recency_match}")
print(f"Frequency SQL vs Pandas: {frequency_match}")
print(f"Monetary SQL vs Pandas: {monetary_match}")
print(f"Segmentacja SQL vs NumPy: {segment_match}")


# ============================================================
# 17. EXPLAIN QUERY PLAN
# ============================================================

section("16. EXPLAIN QUERY PLAN")

plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + segmentation_query,
    conn,
    params=params
)

show_table(plan)


# ============================================================
# 18. AUTOMATYCZNE TESTY
# ============================================================

section("17. WERYFIKACJA")

tests = {
    "Tabela customers zawiera 200 klientow":
        len(customers_df) == 200,

    "Identyfikatory klientow sa unikalne":
        customers_df["customer_id"].is_unique,

    "Identyfikatory zamowien sa unikalne":
        orders_df["order_id"].is_unique,

    "Wszystkie zamowienia maja istniejacego klienta":
        orders_df["customer_id"].isin(
            customers_df["customer_id"]
        ).all(),

    "Wszystkie kwoty zamowien sa dodatnie":
        (orders_df["amount"] > 0).all(),

    "Brak zamowien po dacie referencyjnej":
        (orders_df["order_date"] <= REFERENCE_DATE).all(),

    "RFM zawiera wszystkich klientow":
        len(rfm) == N_CUSTOMERS,

    "RFM zawiera unikalnych klientow":
        rfm["customer_id"].is_unique,

    "Segmentacja zawiera wszystkich klientow":
        len(segmented) == N_CUSTOMERS,

    "Recency nie zawiera ujemnych wartosci":
        (rfm["recency"].dropna() >= 0).all(),

    "Frequency nie zawiera ujemnych wartosci":
        (rfm["frequency"] >= 0).all(),

    "Monetary nie zawiera ujemnych wartosci":
        (rfm["monetary"] >= 0).all(),

    "Suma Frequency jest zgodna z liczba zamowien":
        rfm["frequency"].sum() == len(orders_df),

    "Suma Monetary jest zgodna z przychodem":
        np.isclose(
            rfm["monetary"].sum(),
            orders_df["amount"].sum()
        ),

    "Dziesieciu klientow nie ma zamowien":
        len(without_orders) == 10,

    "Klienci bez zamowien maja NULL Recency":
        without_orders["recency"].isna().all(),

    "Klienci bez zamowien maja Monetary rowne 0":
        (without_orders["monetary"] == 0).all(),

    "Klienci bez zamowien sa w segmencie Lost":
        (without_orders["segment"] == "Lost").all(),

    "Istnieja wszystkie cztery segmenty":
        set(segmented["segment"]) == {
            "VIP", "Regular", "At-risk", "Lost"
        },

    "Brak pustych segmentow":
        segmented["segment"].notna().all(),

    "VIP maja Recency <= 30":
        (vip["recency"] <= 30).all(),

    "VIP maja Frequency >= 10":
        (vip["frequency"] >= 10).all(),

    "VIP maja Monetary >= 3000":
        (vip["monetary"] >= 3000).all(),

    "Regular maja Recency <= 90":
        (regular["recency"] <= 90).all(),

    "At-risk maja Recency > 90":
        (at_risk["recency"] > 90).all(),

    "At-risk maja Recency <= 180":
        (at_risk["recency"] <= 180).all(),

    "Lost spelniaja warunek nieaktywnosci":
        (
            (lost["recency"] > 180)
            | (lost["frequency"] == 0)
        ).all(),

    "Liczba klientow VIP wynosi 30":
        len(vip) == 30,

    "Liczba klientow Regular wynosi 70":
        len(regular) == 70,

    "Liczba klientow At-risk wynosi 50":
        len(at_risk) == 50,

    "Liczba klientow Lost wynosi 50":
        len(lost) == 50,

    "Suma liczebnosci segmentow jest poprawna":
        summary["customers_count"].sum() == N_CUSTOMERS,

    "Suma przychodow segmentow jest poprawna":
        np.isclose(
            summary["total_revenue"].sum(),
            total_revenue
        ),

    "Udzialy klientow sumuja sie do 100%":
        np.isclose(
            summary["customers_pct"].sum(),
            100
        ),

    "Udzialy przychodow sumuja sie do 100%":
        np.isclose(
            summary["revenue_pct"].sum(),
            100
        ),

    "Recency SQL i Pandas sa zgodne":
        recency_match,

    "Frequency SQL i Pandas sa zgodne":
        frequency_match,

    "Monetary SQL i Pandas sa zgodne":
        monetary_match,

    "Segmentacja SQL i NumPy jest zgodna":
        segment_match,

    "TOP 10 zawiera 10 klientow":
        len(top_customers) == 10,

    "Klienci sa posortowani wedlug Monetary":
        segmented["monetary"].is_monotonic_decreasing,

    "Tabela customers pozostala niezmieniona":
        cursor.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0] == N_CUSTOMERS,

    "Tabela orders pozostala niezmieniona":
        cursor.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0] == len(orders_df)
}

passed = 0

for name, result in tests.items():

    result = bool(result)

    if result:
        passed += 1

    print(f"Czy {name}: {result}")

print(f"\nZaliczone testy: {passed}/{len(tests)}")


# ============================================================
# 19. WNIOSKI
# ============================================================

section("18. WNIOSKI")

conclusions = [
    "RFM pozwala segmentowac klientow wedlug zakupow.",
    "Recency mierzy czas od ostatniego zamowienia.",
    "Frequency mierzy liczbe zamowien.",
    "Monetary mierzy laczna wartosc zamowien.",
    "julianday pozwala obliczac roznice miedzy datami.",
    "MAX(order_date) znajduje ostatnie zamowienie.",
    "LEFT JOIN zachowuje klientow bez zamowien.",
    "COUNT(order_id) poprawnie liczy zamowienia.",
    "COALESCE zamienia brak przychodu na zero.",
    "CASE WHEN umozliwia segmentacje w SQL.",
    "Kolejnosc warunkow CASE WHEN ma znaczenie.",
    "VIP wymagaja utrzymania lojalnosci.",
    "Regular maja potencjal dalszego rozwoju.",
    "At-risk wymagaja dzialan reaktywacyjnych.",
    "Lost obejmuje tutaj takze klientow bez zakupow.",
    "Progi RFM nalezy dopasowac do biznesu.",
    "SQL i Pandas pozwalaja uzyskac zgodne wyniki.",
    "RFM moze wspierac systemy CRM i modele ML.",
    "Monetary opisuje historyczny przychod, nie zysk.",
    "RFM nie jest samodzielna prognoza przyszlego LTV."
]

for number, conclusion in enumerate(conclusions, 1):

    print(f"{number}. {conclusion}")


# ============================================================
# 20. PODSUMOWANIE
# ============================================================

section("PODSUMOWANIE")

print(f"Liczba klientow: {len(customers_df)}")
print(f"Liczba zamowien: {len(orders_df)}")
print(f"Data referencyjna: {REFERENCE_DATE}")
print(f"Laczny przychod: {total_revenue:,.2f} PLN")
print(f"Klienci VIP: {len(vip)}")
print(f"Klienci Regular: {len(regular)}")
print(f"Klienci At-risk: {len(at_risk)}")
print(f"Klienci Lost: {len(lost)}")
print(f"Klienci bez zamowien: {len(without_orders)}")
print(f"Udzial VIP w przychodzie: {vip_revenue_pct:.2f}%")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

if passed == len(tests):

    print("\nWszystkie testy zakonczone pomyslnie.")
    print("Zadanie 17 wykonane poprawnie.")

else:

    raise AssertionError(
        "Nie wszystkie testy zostaly zaliczone."
    )
