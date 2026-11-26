# Lekcja 13 - Zadanie 16: Optymalizacja zapytan (czas + plan)

import sqlite3
import time
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 90)


# Konfiguracja
N_CUSTOMERS = 5_000
N_SALES = 100_000
REPEATS = 3

rng = np.random.default_rng(42)

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("PRAGMA automatic_index = OFF")


section("OPTYMALIZACJA ZAPYTAN SQL")


# ============================================================
# 1. TWORZENIE TABEL
# ============================================================

section("1. TWORZENIE BAZY DANYCH")

cursor.executescript("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );

    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        sale_date TEXT NOT NULL,
        revenue REAL NOT NULL,
        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
    );
""")


# ============================================================
# 2. GENEROWANIE DANYCH ZA POMOCA NUMPY
# ============================================================

section("2. GENEROWANIE DANYCH")

cities = [
    "Warszawa",
    "Krakow",
    "Gdansk",
    "Wroclaw",
    "Kolobrzeg",
    "Poznan"
]

categories = [
    "Elektronika",
    "Odziez",
    "Sport",
    "Dom",
    "Ksiazki",
    "Kosmetyki"
]

customers = pd.DataFrame({
    "customer_id": np.arange(1, N_CUSTOMERS + 1),
    "name": [
        f"Klient_{i}"
        for i in range(1, N_CUSTOMERS + 1)
    ],
    "city": rng.choice(cities, N_CUSTOMERS)
})

dates = (
    np.datetime64("2024-01-01")
    + rng.integers(0, 366, N_SALES).astype("timedelta64[D]")
)

sales = pd.DataFrame({
    "sale_id": np.arange(1, N_SALES + 1),
    "customer_id": rng.integers(
        1, N_CUSTOMERS + 1, N_SALES
    ),
    "category": rng.choice(categories, N_SALES),
    "sale_date": dates.astype(str),
    "revenue": np.round(
        rng.uniform(10, 2000, N_SALES), 2
    )
})

customers.to_sql(
    "customers",
    conn,
    if_exists="append",
    index=False
)

sales.to_sql(
    "sales",
    conn,
    if_exists="append",
    index=False
)

conn.commit()

print(f"Liczba klientow: {len(customers):,}")
print(f"Liczba transakcji: {len(sales):,}")
print(f"Liczba kategorii: {len(categories)}")
print(f"Liczba miast: {len(cities)}")
print(f"Liczba powtorzen pomiaru: {REPEATS}")

print("\nPrzykladowi klienci:")
print(customers.head().to_string(index=False))

print("\nPrzykladowe transakcje:")
print(sales.head().to_string(index=False))


# ============================================================
# 3. ZLOZONE ZAPYTANIE SQL
# ============================================================

section("3. ZLOZONE ZAPYTANIE SQL")

query = """
SELECT
    c.city,
    s.category,
    COUNT(*) AS liczba_transakcji,
    ROUND(SUM(s.revenue), 2) AS przychod,
    ROUND(AVG(s.revenue), 2) AS srednia_transakcja
FROM sales AS s
INNER JOIN customers AS c
    ON s.customer_id = c.customer_id
WHERE s.category = 'Elektronika'
    AND s.sale_date >= '2024-10-01'
    AND s.sale_date <= '2024-10-31'
GROUP BY
    c.city,
    s.category
HAVING SUM(s.revenue) > 10000
ORDER BY przychod DESC, c.city ASC
"""

print(query)


# ============================================================
# 4. FUNKCJE POMIAROWE
# ============================================================

def measure_query(connection, sql, repeats=3):
    """Mierzy czas wykonania i pobrania wynikow."""

    # Rozgrzewka poza pomiarem
    connection.execute(sql).fetchall()

    times = []

    for _ in range(repeats):
        start = time.perf_counter()

        connection.execute(sql).fetchall()

        end = time.perf_counter()
        times.append(end - start)

    return {
        "times": times,
        "mean": float(np.mean(times)),
        "min": float(np.min(times)),
        "max": float(np.max(times)),
        "std": float(np.std(times))
    }


def get_query_plan(connection, sql):
    """Pobiera plan wykonania jako DataFrame."""

    return pd.read_sql_query(
        "EXPLAIN QUERY PLAN " + sql,
        connection
    )


def plan_signature(plan):
    """Zwraca opis operacji z planu."""

    return " | ".join(plan["detail"].tolist())


def get_indexes(connection):
    """Zwraca liste dodatkowych indeksow."""

    return pd.read_sql_query("""
        SELECT
            name AS indeks,
            tbl_name AS tabela,
            sql AS definicja
        FROM sqlite_master
        WHERE type = 'index'
            AND sql IS NOT NULL
        ORDER BY name
    """, connection)


# ============================================================
# 5. POMIAR BEZ DODATKOWYCH INDEKSOW
# ============================================================

section("4. POMIAR BAZOWY - BEZ INDEKSOW")

baseline_result = pd.read_sql_query(query, conn)

baseline_measurement = measure_query(
    conn, query, REPEATS
)

baseline_plan = get_query_plan(conn, query)

baseline_time = baseline_measurement["mean"]

print("Wynik zapytania:")
print(baseline_result.to_string(index=False))

print("\nCzasy poszczegolnych prob:")

for i, elapsed in enumerate(
    baseline_measurement["times"], 1
):
    print(f"Proba {i}: {elapsed:.8f} s")

print(f"\nSredni czas: {baseline_time:.8f} s")

print("\nEXPLAIN QUERY PLAN:")
print(baseline_plan.to_string(index=False))

print("\nDodatkowe indeksy:")
print(get_indexes(conn).to_string(index=False))


# ============================================================
# 6. IDENTYFIKACJA KOLUMN DO INDEKSOWANIA
# ============================================================

section("5. KOLUMNY DO INDEKSOWANIA")

candidates = pd.DataFrame([
    ["sales.customer_id", "JOIN"],
    ["customers.customer_id", "JOIN - PRIMARY KEY"],
    ["sales.category", "WHERE / GROUP BY"],
    ["sales.sale_date", "WHERE"],
    ["customers.city", "GROUP BY"],
    ["sales.revenue", "Agregacja / covering index"]
], columns=["Kolumna", "Zastosowanie"])

print(candidates.to_string(index=False))

print(
    "\nPRIMARY KEY jest juz obslugiwany "
    "przez mechanizm SQLite."
)

print(
    "SCAN oznacza skanowanie tabeli lub indeksu, "
    "a nie pojedynczej kolumny."
)

print(
    "SEARCH oznacza wyszukiwanie ograniczone "
    "warunkiem dostepu."
)


# ============================================================
# 7. DEFINICJE INDEKSOW
# ============================================================

index_definitions = [
    (
        "idx_sales_customer",
        """
        CREATE INDEX idx_sales_customer
        ON sales(customer_id)
        """,
        "JOIN"
    ),
    (
        "idx_sales_category",
        """
        CREATE INDEX idx_sales_category
        ON sales(category)
        """,
        "WHERE / GROUP BY"
    ),
    (
        "idx_sales_date",
        """
        CREATE INDEX idx_sales_date
        ON sales(sale_date)
        """,
        "WHERE - zakres dat"
    ),
    (
        "idx_customers_city",
        """
        CREATE INDEX idx_customers_city
        ON customers(city)
        """,
        "GROUP BY"
    ),
    (
        "idx_sales_category_date",
        """
        CREATE INDEX idx_sales_category_date
        ON sales(category, sale_date)
        """,
        "WHERE - indeks zlozony"
    ),
    (
        "idx_sales_covering",
        """
        CREATE INDEX idx_sales_covering
        ON sales(
            category,
            sale_date,
            customer_id,
            revenue
        )
        """,
        "Indeks pokrywajacy"
    )
]


# ============================================================
# 8. PRZYGOTOWANIE RAPORTOW
# ============================================================

results = [{
    "Etap": 0,
    "Indeks": "Brak dodatkowych indeksow",
    "Czas_s": baseline_time,
    "Min_s": baseline_measurement["min"],
    "Max_s": baseline_measurement["max"],
    "Std_s": baseline_measurement["std"],
    "Przyspieszenie_x": 1.0,
    "Zmiana_vs_poprzedni_pct": 0.0,
    "Zmiana_planu": False,
    "Nowy_indeks_w_planie": False,
    "Wyniki_zgodne": True,
    "Czas_tworzenia_indeksu_s": 0.0,
    "Plan": plan_signature(baseline_plan)
}]

plans = [
    baseline_plan.assign(
        Etap=0,
        Indeks="Brak dodatkowych indeksow"
    )
]

all_measurements = [
    {
        "Etap": 0,
        "Indeks": "Brak dodatkowych indeksow",
        "Proba": i,
        "Czas_s": elapsed
    }
    for i, elapsed in enumerate(
        baseline_measurement["times"], 1
    )
]

previous_time = baseline_time
previous_plan = plan_signature(baseline_plan)


# ============================================================
# 9. DODAWANIE INDEKSOW POJEDYNCZO
# ============================================================

section("6. TESTOWANIE INDEKSOW")

for stage, definition in enumerate(
    index_definitions, 1
):
    index_name, create_sql, purpose = definition

    section(f"ETAP {stage}: {index_name}")

    print(f"Przeznaczenie: {purpose}")
    print(create_sql.strip())

    # Pomiar czasu tworzenia indeksu
    start = time.perf_counter()

    cursor.execute(create_sql)
    conn.commit()

    creation_time = time.perf_counter() - start

    # Pomiar czasu zapytania
    measurement = measure_query(
        conn, query, REPEATS
    )

    current_time = measurement["mean"]

    # Pobranie planu
    current_plan = get_query_plan(conn, query)
    current_signature = plan_signature(current_plan)

    # Sprawdzenie poprawnosci wynikow
    current_result = pd.read_sql_query(query, conn)

    same_result = baseline_result.equals(
        current_result
    )

    speedup = baseline_time / current_time

    improvement = (
        (previous_time - current_time)
        / previous_time * 100
    )

    plan_changed = (
        current_signature != previous_plan
    )

    index_used = index_name in current_signature

    results.append({
        "Etap": stage,
        "Indeks": index_name,
        "Czas_s": current_time,
        "Min_s": measurement["min"],
        "Max_s": measurement["max"],
        "Std_s": measurement["std"],
        "Przyspieszenie_x": speedup,
        "Zmiana_vs_poprzedni_pct": improvement,
        "Zmiana_planu": plan_changed,
        "Nowy_indeks_w_planie": index_used,
        "Wyniki_zgodne": same_result,
        "Czas_tworzenia_indeksu_s": creation_time,
        "Plan": current_signature
    })

    plans.append(
        current_plan.assign(
            Etap=stage,
            Indeks=index_name
        )
    )

    for i, elapsed in enumerate(
        measurement["times"], 1
    ):
        all_measurements.append({
            "Etap": stage,
            "Indeks": index_name,
            "Proba": i,
            "Czas_s": elapsed
        })

        print(f"Proba {i}: {elapsed:.8f} s")

    print(f"\nSredni czas: {current_time:.8f} s")
    print(f"Przyspieszenie: {speedup:.2f}x")
    print(f"Zmiana wzgledem poprzedniego: {improvement:.2f}%")
    print(f"Czas tworzenia indeksu: {creation_time:.8f} s")
    print(f"Zmiana planu: {plan_changed}")
    print(f"Nowy indeks wykorzystany: {index_used}")
    print(f"Wyniki zgodne z bazowymi: {same_result}")

    print("\nEXPLAIN QUERY PLAN:")
    print(current_plan.to_string(index=False))

    previous_time = current_time
    previous_plan = current_signature


# ============================================================
# 10. DATAFRAME Z CZASAMI
# ============================================================

section("7. RAPORT CZASOW WYKONANIA")

report = pd.DataFrame(results)

report["Oszczednosc_czasu_pct"] = (
    1 - report["Czas_s"] / baseline_time
) * 100

report_columns = [
    "Etap",
    "Indeks",
    "Czas_s",
    "Przyspieszenie_x",
    "Oszczednosc_czasu_pct",
    "Zmiana_vs_poprzedni_pct",
    "Zmiana_planu",
    "Nowy_indeks_w_planie"
]

print(
    report[report_columns].to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}"
    )
)


# ============================================================
# 11. WSZYSTKIE PROBY POMIAROWE
# ============================================================

section("8. WSZYSTKIE PROBY POMIAROWE")

measurements_df = pd.DataFrame(all_measurements)

print(
    measurements_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.8f}"
    )
)


# ============================================================
# 12. WSZYSTKIE PLANY WYKONANIA
# ============================================================

section("9. WSZYSTKIE PLANY EXPLAIN QUERY PLAN")

plans_df = pd.concat(
    plans,
    ignore_index=True
)

print(
    plans_df[
        ["Etap", "Indeks", "id", "parent", "detail"]
    ].to_string(index=False)
)


# ============================================================
# 13. POROWNANIE OPERACJI SCAN I SEARCH
# ============================================================

section("10. ANALIZA OPERACJI SCAN I SEARCH")

plan_analysis = []

for stage, group in plans_df.groupby("Etap"):
    details = group["detail"]

    plan_analysis.append({
        "Etap": stage,
        "SCAN": int(
            details.str.contains(r"\bSCAN\b").sum()
        ),
        "SEARCH": int(
            details.str.contains(r"\bSEARCH\b").sum()
        ),
        "COVERING_INDEX": int(
            details.str.contains("COVERING INDEX").sum()
        ),
        "TEMP_B_TREE": int(
            details.str.contains("TEMP B-TREE").sum()
        )
    })

plan_analysis_df = pd.DataFrame(plan_analysis)

print(plan_analysis_df.to_string(index=False))


# ============================================================
# 14. LISTA UTWORZONYCH INDEKSOW
# ============================================================

section("11. LISTA UTWORZONYCH INDEKSOW")

indexes_df = get_indexes(conn)

print(indexes_df.to_string(index=False))

print(f"\nLiczba indeksow: {len(indexes_df)}")


# ============================================================
# 15. TEKSTOWA WIZUALIZACJA PRZYSPIESZENIA
# ============================================================

section("12. TEKSTOWY WYKRES PRZYSPIESZENIA")

print("Legenda: jeden znak = okolo 1x")
print("Wartosci ponizej 1x oznaczaja spowolnienie.\n")

for row in report.itertuples(index=False):
    speedup = row.Przyspieszenie_x
    bar = "█" * int(round(speedup))

    print(
        f"{row.Indeks:30s} | "
        f"{bar} {speedup:.2f}x"
    )


# ============================================================
# 16. NAJLEPSZY ETAP OPTYMALIZACJI
# ============================================================

section("13. NAJLEPSZY ETAP OPTYMALIZACJI")

best = report.loc[
    report["Czas_s"].idxmin()
]

indexed_report = report[
    report["Etap"] > 0
]

best_increment = indexed_report.loc[
    indexed_report[
        "Zmiana_vs_poprzedni_pct"
    ].idxmax()
]

print(f"Najlepszy etap: {best['Etap']}")
print(f"Ostatni dodany indeks: {best['Indeks']}")
print(f"Czas bazowy: {baseline_time:.8f} s")
print(f"Najlepszy czas: {best['Czas_s']:.8f} s")

print(
    f"Najlepsze przyspieszenie: "
    f"{best['Przyspieszenie_x']:.2f}x"
)

print(
    f"Oszczednosc czasu: "
    f"{best['Oszczednosc_czasu_pct']:.2f}%"
)

print(
    f"\nNajwieksza zmierzona poprawa etapowa: "
    f"{best_increment['Indeks']}"
)

print(
    f"Zmiana wzgledem poprzedniego etapu: "
    f"{best_increment['Zmiana_vs_poprzedni_pct']:.2f}%"
)

if best_increment["Zmiana_vs_poprzedni_pct"] <= 0:
    print("Zaden kolejny etap nie przyniosl poprawy.")

print("\nPlan najlepszego etapu:")
print(
    plans_df[
        plans_df["Etap"] == best["Etap"]
    ].to_string(index=False)
)


# ============================================================
# 17. WERYFIKACJA ZA POMOCA PANDAS
# ============================================================

section("14. WERYFIKACJA SQL ZA POMOCA PANDAS")

merged = sales.merge(
    customers,
    on="customer_id",
    how="inner"
)

filtered = merged[
    (merged["category"] == "Elektronika")
    & (merged["sale_date"] >= "2024-10-01")
    & (merged["sale_date"] <= "2024-10-31")
]

pandas_result = (
    filtered.groupby(
        ["city", "category"],
        as_index=False
    )
    .agg(
        liczba_transakcji=("sale_id", "count"),
        przychod=("revenue", "sum"),
        srednia_transakcja=("revenue", "mean")
    )
)

pandas_result = pandas_result[
    pandas_result["przychod"] > 10000
].copy()

pandas_result["przychod"] = (
    pandas_result["przychod"].round(2)
)

pandas_result["srednia_transakcja"] = (
    pandas_result["srednia_transakcja"].round(2)
)

pandas_result = (
    pandas_result.sort_values(
        ["przychod", "city"],
        ascending=[False, True]
    )
    .reset_index(drop=True)
)

print(pandas_result.to_string(index=False))

same_groups = (
    baseline_result[["city", "category"]]
    .equals(pandas_result[["city", "category"]])
)

numeric_columns = [
    "liczba_transakcji",
    "przychod",
    "srednia_transakcja"
]

same_values = (
    baseline_result.shape == pandas_result.shape
    and np.allclose(
        baseline_result[numeric_columns],
        pandas_result[numeric_columns],
        rtol=0,
        atol=0.01
    )
)

print(f"\nZgodnosc grup: {same_groups}")
print(f"Zgodnosc wartosci: {same_values}")


# ============================================================
# 18. TESTY AUTOMATYCZNE
# ============================================================

section("15. WERYFIKACJA")

final_sales_count = cursor.execute(
    "SELECT COUNT(*) FROM sales"
).fetchone()[0]

final_customers_count = cursor.execute(
    "SELECT COUNT(*) FROM customers"
).fetchone()[0]

expected_stages = len(index_definitions) + 1

tests = {
    "Tabela sales zawiera 100000 rekordow":
        len(sales) == 100_000,

    "Tabela customers zawiera 5000 rekordow":
        len(customers) == 5_000,

    "Identyfikatory sprzedazy sa unikalne":
        sales["sale_id"].is_unique,

    "Identyfikatory klientow sa unikalne":
        customers["customer_id"].is_unique,

    "Brak brakujacych danych sprzedazy":
        not sales.isna().any().any(),

    "Brak brakujacych danych klientow":
        not customers.isna().any().any(),

    "Wszystkie transakcje maja klienta":
        sales["customer_id"].isin(
            customers["customer_id"]
        ).all(),

    "Daty naleza do roku 2024":
        sales["sale_date"].str.startswith("2024").all(),

    "Przychody sa dodatnie":
        (sales["revenue"] > 0).all(),

    "Zapytanie zawiera JOIN":
        "JOIN" in query.upper(),

    "Zapytanie zawiera WHERE":
        "WHERE" in query.upper(),

    "Zapytanie zawiera GROUP BY":
        "GROUP BY" in query.upper(),

    "Zapytanie zawiera HAVING":
        "HAVING" in query.upper(),

    "Zapytanie zawiera ORDER BY":
        "ORDER BY" in query.upper(),

    "Wynik bazowy nie jest pusty":
        not baseline_result.empty,

    "Wynik zawiera tylko Elektronike":
        baseline_result["category"].eq(
            "Elektronika"
        ).all(),

    "Przychody grup przekraczaja 10000":
        (baseline_result["przychod"] > 10000).all(),

    "Wyniki posortowano malejaco":
        baseline_result["przychod"]
        .is_monotonic_decreasing,

    "Wykonano wszystkie etapy":
        len(report) == expected_stages,

    "Wykonano po 3 pomiary na etap":
        measurements_df.groupby("Etap")
        .size().eq(REPEATS).all(),

    "Liczba pomiarow jest poprawna":
        len(measurements_df)
        == expected_stages * REPEATS,

    "Wszystkie czasy sa dodatnie":
        (measurements_df["Czas_s"] > 0).all(),

    "Wszystkie srednie czasy sa dodatnie":
        (report["Czas_s"] > 0).all(),

    "Bazowe przyspieszenie wynosi 1x":
        np.isclose(
            report.iloc[0]["Przyspieszenie_x"],
            1.0
        ),

    "Przyspieszenia obliczono poprawnie":
        np.allclose(
            report["Przyspieszenie_x"],
            baseline_time / report["Czas_s"]
        ),

    "Oszczednosc czasu obliczono poprawnie":
        np.allclose(
            report["Oszczednosc_czasu_pct"],
            (1 - report["Czas_s"] / baseline_time)
            * 100
        ),

    "Plan bazowy zawiera SCAN":
        baseline_plan["detail"]
        .str.contains(r"\bSCAN\b").any(),

    "Zapisano plany wszystkich etapow":
        plans_df["Etap"].nunique() == expected_stages,

    "Utworzono wszystkie indeksy":
        len(indexes_df) == len(index_definitions),

    "Wszystkie wyniki SQL pozostaly zgodne":
        report["Wyniki_zgodne"].all(),

    "Najlepszy etap ma minimalny czas":
        np.isclose(
            best["Czas_s"],
            report["Czas_s"].min()
        ),

    "SQL i Pandas zwracaja zgodne grupy":
        same_groups,

    "SQL i Pandas zwracaja zgodne wartosci":
        same_values,

    "Tabela sales pozostala niezmieniona":
        final_sales_count == N_SALES,

    "Tabela customers pozostala niezmieniona":
        final_customers_count == N_CUSTOMERS
}

passed = 0

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")
    passed += int(bool(result))

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), (
    "Nie wszystkie testy zostaly zaliczone."
)


# ============================================================
# 19. WNIOSKI
# ============================================================

section("16. WNIOSKI")

print("1. Indeksy moga ograniczyc skanowanie tabel.")
print("2. EXPLAIN QUERY PLAN pokazuje sposob dostepu do danych.")
print("3. SEARCH moze oznaczac wykorzystanie indeksu.")
print("4. PRIMARY KEY nie wymaga dodatkowego indeksu.")
print("5. Nie kazdy utworzony indeks jest wykorzystywany.")
print("6. Indeksy zlozone obsluguja wiele warunkow.")
print("7. Kolejnosc kolumn w indeksie ma znaczenie.")
print("8. Covering index moze ograniczyc odczyty tabeli.")
print("9. GROUP BY moze wymagac tymczasowego B-TREE.")
print("10. ORDER BY agregatu moze wymagac sortowania.")
print("11. Indeksy zwiekszaja koszt zapisu i zajmuja pamiec.")
print("12. Pomiar wydajnosci wymaga kilku powtorzen.")
print("13. Optymalizacja nie powinna zmieniac wynikow.")
print("14. Wyniki czasowe zaleza od sprzetu i obciazenia.")
print("15. Kolejne etapy mierza kumulacyjny efekt indeksow.")
print("16. Trzy proby nie gwarantuja istotnosci roznic.")

if best["Etap"] > 0:
    print(
        f"\nNajlepsza konfiguracja: etap {best['Etap']}, "
        f"przyspieszenie {best['Przyspieszenie_x']:.2f}x."
    )
else:
    print("\nW tym pomiarze najlepszy byl wariant bazowy.")


# ============================================================
# 20. PODSUMOWANIE
# ============================================================

section("PODSUMOWANIE")

print(f"Liczba klientow: {N_CUSTOMERS:,}")
print(f"Liczba transakcji: {N_SALES:,}")
print(f"Liczba utworzonych indeksow: {len(indexes_df)}")
print(f"Liczba etapow: {len(report)}")
print(f"Liczba pomiarow: {len(measurements_df)}")
print(f"Czas bez dodatkowych indeksow: {baseline_time:.8f} s")
print(f"Najlepszy czas: {best['Czas_s']:.8f} s")
print(f"Najlepszy etap: {best['Etap']}")
print(f"Ostatni dodany indeks: {best['Indeks']}")
print(f"Przyspieszenie: {best['Przyspieszenie_x']:.2f}x")
print(f"Oszczednosc czasu: {best['Oszczednosc_czasu_pct']:.2f}%")
print(f"Zaliczone testy: {passed}/{len(tests)}")

conn.close()

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 16 wykonane poprawnie.")
