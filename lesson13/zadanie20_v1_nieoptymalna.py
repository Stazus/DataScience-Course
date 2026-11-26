# Lekcja 13 - Zadanie 20: Green SQL Challenge
# Wersja 1 - Nieoptymalna

import pandas as pd
import numpy as np

from zadanie20_common import (
    N_RECORDS,
    REGION,
    DATE_FROM,
    DATE_TO,
    TOP_N,
    REPEATS,
    section,
    create_database,
    explain_query,
    aggregate_python,
    measure_strategy
)


QUERY = """
SELECT *
FROM sales
"""


def strategy(conn):
    """Pobiera wszystkie dane i przetwarza je w Pythonie."""

    # Pobranie wszystkich rekordow z bazy
    downloaded = pd.read_sql_query(
        QUERY,
        conn
    )

    # Filtrowanie w Pandas zamiast SQL
    filtered = downloaded.loc[
        (downloaded["region"] == REGION)
        & (downloaded["sale_date"] >= DATE_FROM)
        & (downloaded["sale_date"] < DATE_TO)
    ]

    # Grupowanie, sortowanie i TOP 10 w Pythonie
    result = aggregate_python(filtered)

    return result, downloaded


def get_plan(conn):
    """Zwraca plan wykonania zapytania."""

    return explain_query(conn, QUERY)


def main():

    print("=" * 80)
    print("GREEN SQL CHALLENGE")
    print("WERSJA 1 - NIEOPTYMALNA")
    print("=" * 80)

    # Utworzenie bazy bez dodatkowych indeksow
    conn = create_database()

    section("1. PARAMETRY ANALIZY")

    print(f"Liczba rekordow: {N_RECORDS:,}")
    print(f"Region: {REGION}")
    print(f"Data od: {DATE_FROM}")
    print(f"Data do (bez tej daty): {DATE_TO}")
    print(f"TOP produktow: {TOP_N}")
    print(f"Liczba powtorzen: {REPEATS}")

    section("2. ZAPYTANIE SQL")

    print(QUERY.strip())

    section("3. INDEKSY")

    indexes = pd.read_sql_query(
        "PRAGMA index_list('sales')",
        conn
    )

    if indexes.empty:
        print("Brak dodatkowych indeksow.")
    else:
        print(indexes.to_string(index=False))

    section("4. EXPLAIN QUERY PLAN")

    plan = get_plan(conn)

    print(plan.to_string(index=False))

    section("5. POMIAR WYDAJNOSCI")

    metrics = measure_strategy(strategy, conn)

    for i, elapsed in enumerate(
        metrics["times"], start=1
    ):
        print(f"Proba {i}: {elapsed:.6f} s")

    print(
        f"\nSredni czas: "
        f"{metrics['time_s']:.6f} s"
    )

    print(
        f"Odchylenie standardowe: "
        f"{np.std(metrics['times']):.6f} s"
    )

    print(
        f"Pamiec DataFrame: "
        f"{metrics['memory_mb']:.4f} MiB"
    )

    print(
        f"Pobrane rekordy: "
        f"{metrics['downloaded_rows']:,}"
    )

    print(
        f"Proxy energii: "
        f"{metrics['energy_proxy']:.6f} s * MiB"
    )

    section("6. TOP 10 PRODUKTOW")

    result = metrics["result"]

    print(result.to_string(index=False))

    section("7. ANALIZA TRANSFERU DANYCH")

    filtered_count = conn.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE region = ?
          AND sale_date >= ?
          AND sale_date < ?
    """, (REGION, DATE_FROM, DATE_TO)).fetchone()[0]

    downloaded_rows = metrics["downloaded_rows"]

    unnecessary_rows = (
        downloaded_rows - filtered_count
    )

    unnecessary_pct = (
        100 * unnecessary_rows / downloaded_rows
    )

    print(f"Pobrane rekordy: {downloaded_rows:,}")
    print(f"Rekordy spelniajace warunki: {filtered_count:,}")
    print(f"Niepotrzebnie pobrane: {unnecessary_rows:,}")
    print(f"Niepotrzebne rekordy: {unnecessary_pct:.2f}%")
    print(f"Koncowa liczba wynikow: {len(result)}")

    section("8. RAPORT METRYK")

    report = pd.DataFrame([{
        "Strategia": "Nieoptymalna",
        "Czas_s": metrics["time_s"],
        "Pamiec_MiB": metrics["memory_mb"],
        "Pobrane_wiersze": downloaded_rows,
        "Proxy_energii": metrics["energy_proxy"]
    }])

    print(
        report.round(6).to_string(index=False)
    )

    section("9. TEKSTOWA WIZUALIZACJA")

    # Jeden znak = 10 ms
    time_bar = "█" * max(
        1, round(metrics["time_s"] / 0.01)
    )

    # Jeden znak = 500 KiB
    memory_bar = "█" * max(
        1, round(metrics["memory_bytes"] / (500 * 1024))
    )

    print("Czas wykonania (1 znak = 10 ms):")
    print(time_bar)
    print(f"{metrics['time_s']:.6f} s")

    print("\nPamiec (1 znak = 500 KiB):")
    print(memory_bar)
    print(f"{metrics['memory_mb']:.4f} MiB")

    section("10. WERYFIKACJA")

    # Niezalezne zapytanie kontrolne
    reference = pd.read_sql_query("""
        SELECT
            product,
            SUM(revenue) AS total_revenue,
            COUNT(*) AS transactions
        FROM sales
        WHERE region = ?
          AND sale_date >= ?
          AND sale_date < ?
        GROUP BY product
        ORDER BY total_revenue DESC, product ASC
        LIMIT ?
    """, conn, params=(
        REGION,
        DATE_FROM,
        DATE_TO,
        TOP_N
    ))

    tests = {
        "Baza zawiera 500 000 rekordow":
            conn.execute(
                "SELECT COUNT(*) FROM sales"
            ).fetchone()[0] == N_RECORDS,

        "Brak dodatkowych indeksow":
            indexes.empty,

        "Pobrano wszystkie rekordy":
            downloaded_rows == N_RECORDS,

        "Plan zawiera SCAN":
            plan["detail"].str.contains(
                "SCAN"
            ).any(),

        "Plan nie korzysta z dodatkowego indeksu":
            not plan["detail"].str.contains(
                "USING INDEX|USING COVERING INDEX",
                regex=True
            ).any(),

        "Wykonano trzy pomiary":
            len(metrics["times"]) == REPEATS,

        "Wszystkie czasy sa dodatnie":
            all(t > 0 for t in metrics["times"]),

        "Sredni czas jest dodatni":
            metrics["time_s"] > 0,

        "Zuzycie pamieci jest dodatnie":
            metrics["memory_bytes"] > 0,

        "Proxy energii jest dodatnie":
            metrics["energy_proxy"] > 0,

        "Wynik zawiera 10 produktow":
            len(result) == TOP_N,

        "Wynik zawiera 3 kolumny":
            result.shape[1] == 3,

        "Nazwy kolumn sa poprawne":
            list(result.columns) == [
                "product",
                "total_revenue",
                "transactions"
            ],

        "Produkty sa unikalne":
            result["product"].is_unique,

        "Przychody sa dodatnie":
            (result["total_revenue"] > 0).all(),

        "Liczby transakcji sa dodatnie":
            (result["transactions"] > 0).all(),

        "Przychody sa posortowane malejaco":
            result["total_revenue"].is_monotonic_decreasing,

        "Filtrowanie zmniejsza liczbe rekordow":
            filtered_count < downloaded_rows,

        "Brak brakujacych wartosci":
            not result.isna().any().any(),

        "Wyniki Python i SQL sa identyczne":
            result.equals(reference),

        "Oryginalna tabela pozostala niezmieniona":
            conn.execute(
                "SELECT COUNT(*) FROM sales"
            ).fetchone()[0] == N_RECORDS
    }

    passed = 0

    for name, status in tests.items():

        print(f"Czy {name}: {bool(status)}")

        if status:
            passed += 1

    print(f"\nZaliczone testy: {passed}/{len(tests)}")

    section("11. WNIOSKI")

    conclusions = [
        "SELECT * pobiera wszystkie kolumny.",
        "Brak indeksu powoduje pelne skanowanie tabeli.",
        "Filtrowanie w Pythonie wymaga pobrania danych.",
        "Pobieranie niepotrzebnych danych zwieksza transfer.",
        "Duzy DataFrame zwieksza zuzycie pamieci.",
        "Agregacja w Pythonie wymaga dodatkowych operacji.",
        "Sortowanie w Pythonie odbywa sie po pobraniu danych.",
        "LIMIT w Pythonie nie ogranicza transferu z bazy.",
        "EXPLAIN QUERY PLAN pokazuje sposob wykonania SQL.",
        "Wersja nieoptymalna jest punktem odniesienia.",
        "Proxy energii nie jest pomiarem rzeczywistej energii.",
        "Pamiec DataFrame nie oznacza calej pamieci procesu."
    ]

    for i, conclusion in enumerate(
        conclusions, start=1
    ):
        print(f"{i}. {conclusion}")

    section("PODSUMOWANIE")

    print("Strategia: Nieoptymalna")
    print(f"Liczba rekordow: {N_RECORDS:,}")
    print(f"Pobrane rekordy: {downloaded_rows:,}")
    print(f"Sredni czas: {metrics['time_s']:.6f} s")
    print(f"Pamiec: {metrics['memory_mb']:.4f} MiB")
    print(f"Proxy energii: {metrics['energy_proxy']:.6f}")
    print(f"Zaliczone testy: {passed}/{len(tests)}")

    conn.close()

    assert passed == len(tests), "Nie wszystkie testy zaliczone."

    print("\nWszystkie testy zakonczone pomyslnie.")
    print("Wersja 1 wykonana poprawnie.")


if __name__ == "__main__":
    main()
