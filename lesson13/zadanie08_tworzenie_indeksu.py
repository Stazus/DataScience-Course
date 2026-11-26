# Lekcja 13 - Zadanie 8: Tworzenie indeksu,
# EXPLAIN QUERY PLAN i pomiar czasu

import sqlite3
import time
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


def measure_query(conn, query, params, repeats=5):
    """Mierzy czas wykonania zapytania SQL."""

    times = []

    for _ in range(repeats):
        start = time.perf_counter()

        result = pd.read_sql_query(
            query,
            conn,
            params=params
        )

        end = time.perf_counter()

        times.append(end - start)

    return result, np.array(times)


def explain_query(conn, query, params):
    """Zwraca plan wykonania zapytania SQL."""

    return pd.read_sql_query(
        "EXPLAIN QUERY PLAN " + query,
        conn,
        params=params
    )


# Konfiguracja
N = 10_000
SEED = 42
REPEATS = 5
CUSTOMER_ID = 500

rng = np.random.default_rng(SEED)


print("=" * 75)
print("TWORZENIE INDEKSU I OPTYMALIZACJA SQL")
print("=" * 75)


# Utworzenie bazy danych SQLite w pamieci
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()


# Utworzenie tabeli orders
cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        amount REAL NOT NULL
    )
""")


section("1. GENEROWANIE DANYCH ZA POMOCA NUMPY")

order_ids = np.arange(1, N + 1)

customer_ids = rng.integers(
    1, 1001, size=N
)

product_ids = rng.integers(
    1, 501, size=N
)

amounts = rng.uniform(
    10, 5000, size=N
).round(2)


df_orders = pd.DataFrame({
    "order_id": order_ids,
    "customer_id": customer_ids,
    "product_id": product_ids,
    "amount": amounts
})


print(f"Liczba rekordow: {len(df_orders)}")
print(f"Liczba kolumn: {len(df_orders.columns)}")
print(f"Seed: {SEED}")

print(
    f"Liczba unikalnych klientow: "
    f"{df_orders['customer_id'].nunique()}"
)

print(
    f"Liczba unikalnych produktow: "
    f"{df_orders['product_id'].nunique()}"
)

print("\nPierwsze 10 rekordow:")

print(
    df_orders.head(10).to_string(index=False)
)


section("2. ZAPIS DANYCH DO SQLITE")

df_orders.to_sql(
    "orders",
    conn,
    if_exists="append",
    index=False
)

conn.commit()

df_count = pd.read_sql_query(
    "SELECT COUNT(*) AS liczba FROM orders",
    conn
)

record_count = int(df_count.iloc[0, 0])

print(f"Liczba rekordow w SQLite: {record_count}")


section("3. STATYSTYKI DANYCH")

print(
    df_orders.describe().round(2).to_string()
)


section("4. INDEKSY PRZED OPTYMALIZACJA")

indexes_before = pd.read_sql_query(
    "PRAGMA index_list('orders')",
    conn
)

if indexes_before.empty:
    print("Brak dodatkowych indeksow.")
else:
    print(indexes_before.to_string(index=False))


section("5. ZAPYTANIE TESTOWE")

query = """
SELECT *
FROM orders
WHERE customer_id = ?
"""

params = (CUSTOMER_ID,)

print(query)
print(f"Parametr customer_id: {CUSTOMER_ID}")


section("6. PLAN ZAPYTANIA BEZ INDEKSU")

plan_before = explain_query(
    conn,
    query,
    params
)

print(plan_before.to_string(index=False))

scan_before = plan_before["detail"].str.contains(
    "SCAN", case=False
).any()

print(f"\nWykryto SCAN: {scan_before}")


section("7. POMIAR CZASU BEZ INDEKSU")

# Rozgrzewka - poza pomiarem
pd.read_sql_query(
    query,
    conn,
    params=params
)

result_before, times_before = measure_query(
    conn,
    query,
    params,
    REPEATS
)

for i, elapsed in enumerate(
    times_before, start=1
):
    print(
        f"Proba {i}: "
        f"{elapsed:.8f} s "
        f"({elapsed * 1000:.4f} ms)"
    )

mean_before = np.mean(times_before)

print(f"\nSredni czas: {mean_before:.8f} s")
print(f"Minimalny czas: {times_before.min():.8f} s")
print(f"Maksymalny czas: {times_before.max():.8f} s")

print(f"Liczba wynikow: {len(result_before)}")

print("\nWyniki zapytania:")

print(result_before.to_string(index=False))


section("8. TWORZENIE INDEKSU")

index_query = """
CREATE INDEX idx_orders_customer_id
ON orders(customer_id)
"""

print(index_query)

start_index = time.perf_counter()

cursor.execute(index_query)
conn.commit()

index_time = time.perf_counter() - start_index

print("Indeks zostal utworzony.")
print(f"Czas tworzenia indeksu: {index_time:.8f} s")


section("9. INDEKSY PO OPTYMALIZACJI")

indexes_after = pd.read_sql_query(
    "PRAGMA index_list('orders')",
    conn
)

print(indexes_after.to_string(index=False))

index_info = pd.read_sql_query(
    "PRAGMA index_info('idx_orders_customer_id')",
    conn
)

print("\nKolumny indeksu:")

print(index_info.to_string(index=False))


section("10. PLAN ZAPYTANIA Z INDEKSEM")

plan_after = explain_query(
    conn,
    query,
    params
)

print(plan_after.to_string(index=False))

search_after = plan_after["detail"].str.contains(
    "SEARCH", case=False
).any()

using_index = plan_after["detail"].str.contains(
    "USING INDEX", case=False
).any()

print(f"\nWykryto SEARCH: {search_after}")
print(f"Wykryto USING INDEX: {using_index}")


section("11. POMIAR CZASU Z INDEKSEM")

# Rozgrzewka - poza pomiarem
pd.read_sql_query(
    query,
    conn,
    params=params
)

result_after, times_after = measure_query(
    conn,
    query,
    params,
    REPEATS
)

for i, elapsed in enumerate(
    times_after, start=1
):
    print(
        f"Proba {i}: "
        f"{elapsed:.8f} s "
        f"({elapsed * 1000:.4f} ms)"
    )

mean_after = np.mean(times_after)

print(f"\nSredni czas: {mean_after:.8f} s")
print(f"Minimalny czas: {times_after.min():.8f} s")
print(f"Maksymalny czas: {times_after.max():.8f} s")

print(f"Liczba wynikow: {len(result_after)}")

print("\nWyniki zapytania:")

print(result_after.to_string(index=False))


section("12. POROWNANIE WSZYSTKICH POMIAROW")

df_times = pd.DataFrame({
    "Proba": np.arange(1, REPEATS + 1),
    "Bez_indeksu_ms": times_before * 1000,
    "Z_indeksem_ms": times_after * 1000
})

df_times["Roznica_ms"] = (
    df_times["Bez_indeksu_ms"]
    - df_times["Z_indeksem_ms"]
)

print(df_times.round(6).to_string(index=False))


section("13. OBLICZENIE PRZYSPIESZENIA")

speedup = mean_before / mean_after

time_saved = mean_before - mean_after

saving_percent = (
    time_saved / mean_before
) * 100

print(f"Czas bez indeksu: {mean_before:.8f} s")
print(f"Czas z indeksem: {mean_after:.8f} s")
print(f"Roznica czasu: {time_saved:.8f} s")
print(f"Przyspieszenie: {speedup:.2f}x")
print(f"Redukcja czasu: {saving_percent:.2f}%")


section("14. RAPORT POROWNAWCZY")

df_report = pd.DataFrame({
    "Metryka": [
        "Sredni czas [ms]",
        "Minimalny czas [ms]",
        "Maksymalny czas [ms]",
        "Odchylenie standardowe [ms]",
        "Liczba pomiarow",
        "Liczba wynikow"
    ],
    "Bez_indeksu": [
        mean_before * 1000,
        times_before.min() * 1000,
        times_before.max() * 1000,
        times_before.std() * 1000,
        len(times_before),
        len(result_before)
    ],
    "Z_indeksem": [
        mean_after * 1000,
        times_after.min() * 1000,
        times_after.max() * 1000,
        times_after.std() * 1000,
        len(times_after),
        len(result_after)
    ]
})

print(df_report.round(6).to_string(index=False))


section("15. POROWNANIE PLANOW ZAPYTAN")

print("BEZ INDEKSU:")

for detail in plan_before["detail"]:
    print(f"  {detail}")

print("\nZ INDEKSEM:")

for detail in plan_after["detail"]:
    print(f"  {detail}")


section("16. TEKSTOWY WYKRES CZASU")

max_time = max(mean_before, mean_after)

for label, elapsed in [
    ("Bez indeksu", mean_before),
    ("Z indeksem", mean_after)
]:
    bar_length = max(
        1,
        round(elapsed / max_time * 50)
    )

    bar = "█" * bar_length

    print(
        f"{label:<15} | "
        f"{bar:<50} "
        f"{elapsed * 1000:.4f} ms"
    )


section("17. SELEKTYWNOSC ZAPYTANIA")

matched_count = len(result_after)

selectivity = (
    matched_count / record_count
) * 100

print(f"Wszystkie rekordy: {record_count}")
print(f"Pasujace rekordy: {matched_count}")
print(f"Selektywnosc: {selectivity:.4f}%")

print(
    f"Rekordy niespelniajace warunku: "
    f"{record_count - matched_count}"
)


section("18. WERYFIKACJA SQL ZA POMOCA PANDAS")

expected = df_orders[
    df_orders["customer_id"] == CUSTOMER_ID
].sort_values(
    "order_id"
).reset_index(drop=True)

before_sorted = result_before.sort_values(
    "order_id"
).reset_index(drop=True)

after_sorted = result_after.sort_values(
    "order_id"
).reset_index(drop=True)

same_results = before_sorted.equals(
    after_sorted
)

pandas_match = expected.equals(
    after_sorted
)

print(
    f"Zgodnosc wynikow przed i po: "
    f"{same_results}"
)

print(
    f"Zgodnosc SQL i Pandas: "
    f"{pandas_match}"
)


section("19. ANALIZA KOSZTU UTWORZENIA INDEKSU")

print(
    f"Czas utworzenia indeksu: "
    f"{index_time * 1000:.4f} ms"
)

print(
    f"Oszczednosc na jednym zapytaniu: "
    f"{time_saved * 1000:.4f} ms"
)

if time_saved > 0:
    break_even = int(
        np.ceil(index_time / time_saved)
    )

    print(
        f"Szacowana liczba zapytan potrzebna "
        f"do zwrotu kosztu utworzenia indeksu: "
        f"{break_even}"
    )
else:
    print(
        "Nie uzyskano oszczednosci czasu "
        "w tym pomiarze."
    )


section("20. AUTOMATYCZNE TESTY")

df_final = pd.read_sql_query(
    "SELECT * FROM orders ORDER BY order_id",
    conn
)

tests = {
    "Dataset zawiera 10000 rekordow":
        len(df_orders) == N,

    "SQLite zawiera 10000 rekordow":
        record_count == N,

    "Dataset zawiera 4 kolumny":
        len(df_orders.columns) == 4,

    "Identyfikatory zamowien sa unikalne":
        df_orders["order_id"].is_unique,

    "Brak wartosci NaN":
        df_orders.isna().sum().sum() == 0,

    "Brak dodatkowych indeksow przed":
        indexes_before.empty,

    "Plan przed zawiera SCAN":
        scan_before,

    "Wykonano 5 pomiarow bez indeksu":
        len(times_before) == REPEATS,

    "Czasy bez indeksu sa dodatnie":
        np.all(times_before > 0),

    "Sredni czas bez indeksu jest dodatni":
        mean_before > 0,

    "Indeks zostal utworzony":
        "idx_orders_customer_id"
        in indexes_after["name"].values,

    "Indeks dotyczy customer_id":
        "customer_id"
        in index_info["name"].values,

    "Plan po zawiera SEARCH":
        search_after,

    "Plan po zawiera USING INDEX":
        using_index,

    "Wykonano 5 pomiarow z indeksem":
        len(times_after) == REPEATS,

    "Czasy z indeksem sa dodatnie":
        np.all(times_after > 0),

    "Sredni czas z indeksem jest dodatni":
        mean_after > 0,

    "Czas tworzenia indeksu jest dodatni":
        index_time > 0,

    "Zapytanie zwraca rekordy":
        matched_count > 0,

    "Wszystkie wyniki przed spelniaja warunek":
        result_before["customer_id"]
        .eq(CUSTOMER_ID).all(),

    "Wszystkie wyniki po spelniaja warunek":
        result_after["customer_id"]
        .eq(CUSTOMER_ID).all(),

    "Liczba wynikow przed i po jest zgodna":
        len(result_before) == len(result_after),

    "Wyniki przed i po sa identyczne":
        same_results,

    "SQL i Pandas zwracaja identyczne wyniki":
        pandas_match,

    "Wspolczynnik przyspieszenia jest poprawny":
        np.isfinite(speedup) and speedup > 0,

    "Redukcja czasu zostala poprawnie obliczona":
        np.isclose(
            saving_percent,
            (1 - mean_after / mean_before) * 100
        ),

    "Tabela pomiarow zawiera 5 wierszy":
        len(df_times) == REPEATS,

    "Selektywnosc miesci sie w zakresie 0-100":
        0 <= selectivity <= 100,

    "Liczba rekordow pozostala niezmieniona":
        len(df_final) == N,

    "Oryginalne dane pozostaly niezmienione":
        df_orders.equals(df_final)
}


for name, passed in tests.items():
    print(f"Czy {name}: {bool(passed)}")

passed_count = sum(
    bool(passed) for passed in tests.values()
)

total_tests = len(tests)

print(
    f"\nZaliczone testy: "
    f"{passed_count}/{total_tests}"
)


section("WNIOSKI")

print("1. Indeks przyspiesza wyszukiwanie selektywnych danych.")
print("2. SCAN oznacza skanowanie tabeli.")
print("3. SEARCH oznacza wyszukiwanie wybranych rekordow.")
print("4. USING INDEX potwierdza wykorzystanie indeksu.")
print("5. CREATE INDEX tworzy dodatkowa strukture danych.")
print("6. Indeks nie zmienia wynikow zapytania.")
print("7. Indeksy zajmuja dodatkowa przestrzen.")
print("8. Indeksy moga spowalniac INSERT, UPDATE i DELETE.")
print("9. EXPLAIN QUERY PLAN pomaga analizowac zapytania.")
print("10. time.perf_counter mierzy czas wykonania.")
print("11. Srednia z kilku prob ogranicza przypadkowe wahania.")
print("12. Parametry zapytania pomagaja unikac SQL Injection.")
print("13. Pomiar obejmuje SQL i utworzenie DataFrame.")
print("14. Wyniki czasowe zaleza od sprzetu i obciazenia.")

if speedup > 1:
    print(
        f"15. W tym eksperymencie indeks zapewnil "
        f"przyspieszenie {speedup:.2f}x."
    )
else:
    print(
        "15. W tym eksperymencie nie odnotowano "
        "przyspieszenia czasowego."
    )


section("PODSUMOWANIE")

print(f"Liczba rekordow: {record_count}")
print(f"Liczba pomiarow na wariant: {REPEATS}")
print(f"Filtrowany klient: {CUSTOMER_ID}")
print(f"Liczba pasujacych rekordow: {matched_count}")
print(f"Plan przed: SCAN = {scan_before}")
print(f"Plan po: SEARCH = {search_after}")
print(f"Wykorzystanie indeksu: {using_index}")
print(f"Czas bez indeksu: {mean_before * 1000:.6f} ms")
print(f"Czas z indeksem: {mean_after * 1000:.6f} ms")
print(f"Przyspieszenie: {speedup:.2f}x")
print(f"Redukcja czasu: {saving_percent:.2f}%")
print(f"Zgodnosc wynikow: {same_results}")
print(f"Zaliczone testy: {passed_count}/{total_tests}")

conn.close()

assert passed_count == total_tests, \
    "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 8 wykonane poprawnie.")
