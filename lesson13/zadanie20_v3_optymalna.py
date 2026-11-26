# Lekcja 13 - Zadanie 20: Green SQL Challenge
# Wersja 3 - W pelni zoptymalizowana

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
    create_indexes,
    explain_query,
    aggregate_python,
    measure_strategy,
    reduction_percent
)


# Wszystkie operacje analityczne wykonywane w SQL

QUERY = """
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
"""

PARAMS = (
    REGION,
    DATE_FROM,
    DATE_TO,
    TOP_N
)


def strategy(conn):
    """Wykonuje wszystkie operacje analityczne w SQL."""

    downloaded = pd.read_sql_query(
        QUERY,
        conn,
        params=PARAMS
    )

    result = downloaded

    return result, downloaded


def get_plan(conn):
    """Zwraca plan wykonania zapytania."""

    return explain_query(
        conn,
        QUERY,
        PARAMS
    )


def main():

    print("=" * 80)
    print("GREEN SQL CHALLENGE")
    print("WERSJA 3 - W PELNI ZOPTYMALIZOWANA")
    print("=" * 80)

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
    print(f"\nParametry: {PARAMS}")

    section("3. PLAN PRZED UTWORZENIEM INDEKSU")

    plan_before = get_plan(conn)

    print(plan_before.to_string(index=False))

    section("4. UTWORZENIE INDEKSU")

    create_indexes(conn)

    indexes = pd.read_sql_query(
        "PRAGMA index_list('sales')",
        conn
    )

    print(indexes.to_string(index=False))

    section("5. PLAN PO UTWORZENIU INDEKSU")

    plan = get_plan(conn)

    print(plan.to_string(index=False))

    section("6. POROWNANIE PLANOW ZAPYTANIA")

    print("Przed optymalizacja:")

    for detail in plan_before["detail"]:
        print(f"  {detail}")

    print("\nPo optymalizacji:")

    for detail in plan["detail"]:
        print(f"  {detail}")

    section("7. POMIAR WYDAJNOSCI")

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
        f"{metrics['memory_mb']:.6f} MiB"
    )

    print(
        f"Pamiec DataFrame w bajtach: "
        f"{metrics['memory_bytes']:,}"
    )

    print(
        f"Pobrane rekordy: "
        f"{metrics['downloaded_rows']:,}"
    )

    print(
        f"Proxy energii: "
        f"{metrics['energy_proxy']:.9f} s * MiB"
    )

    section("8. TOP 10 PRODUKTOW")

    result = metrics["result"]

    print(result.to_string(index=False))

    section("9. ANALIZA TRANSFERU DANYCH")

    downloaded_rows = metrics["downloaded_rows"]

    avoided_rows = N_RECORDS - downloaded_rows

    transfer_reduction = reduction_percent(
        N_RECORDS,
        downloaded_rows
    )

    filtered_count = conn.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE region = ?
          AND sale_date >= ?
          AND sale_date < ?
    """, (
        REGION,
        DATE_FROM,
        DATE_TO
    )).fetchone()[0]

    print(f"Wszystkie rekordy: {N_RECORDS:,}")
    print(f"Rekordy spelniajace warunki: {filtered_count:,}")
    print(f"Pobrane rekordy: {downloaded_rows:,}")
    print(f"Niepobrane rekordy: {avoided_rows:,}")
    print(f"Redukcja liczby wierszy: {transfer_reduction:.4f}%")

    print(
        f"Zmniejszenie liczby pobranych wierszy: "
        f"{N_RECORDS / downloaded_rows:,.0f} razy"
    )

    section("10. RAPORT METRYK")

    report = pd.DataFrame([{
        "Strategia": "Optymalna",
        "Czas_s": metrics["time_s"],
        "Pamiec_MiB": metrics["memory_mb"],
        "Pobrane_wiersze": downloaded_rows,
        "Proxy_energii": metrics["energy_proxy"]
    }])

    print(
        report.round(9).to_string(index=False)
    )

    section("11. TEKSTOWA WIZUALIZACJA")

    time_units = round(
        metrics["time_s"] / 0.01
    )

    memory_units = round(
        metrics["memory_bytes"] / (500 * 1024)
    )

    time_bar = (
        "█" * time_units
        if time_units > 0 else "·"
    )

    memory_bar = (
        "█" * memory_units
        if memory_units > 0 else "·"
    )

    print("Czas wykonania (1 znak = okolo 10 ms):")
    print(time_bar)
    print(f"{metrics['time_s']:.6f} s")

    print("\nPamiec (1 znak = okolo 500 KiB):")
    print(memory_bar)
    print(f"{metrics['memory_mb']:.6f} MiB")

    print("\nSymbol · oznacza wartosc ponizej polowy jednostki.")

    section("12. WERYFIKACJA SQL ZA POMOCA PANDAS")

    # Weryfikacja poza pomiarem wydajnosci

    filtered = pd.read_sql_query("""
        SELECT
            product,
            revenue
        FROM sales
        WHERE region = ?
          AND sale_date >= ?
          AND sale_date < ?
    """, conn, params=(
        REGION,
        DATE_FROM,
        DATE_TO
    ))

    reference = aggregate_python(filtered)

    print(reference.to_string(index=False))

    print(
        "\nCzy wyniki SQL i Pandas sa identyczne:",
        result.equals(reference)
    )

    section("13. ANALIZA OPERACJI SQL")

    operations = pd.DataFrame([
        {
            "Operacja": "WHERE",
            "Zadanie": "Filtrowanie danych",
            "Miejsce": "SQL"
        },
        {
            "Operacja": "SUM",
            "Zadanie": "Sumowanie przychodow",
            "Miejsce": "SQL"
        },
        {
            "Operacja": "COUNT",
            "Zadanie": "Liczenie transakcji",
            "Miejsce": "SQL"
        },
        {
            "Operacja": "GROUP BY",
            "Zadanie": "Grupowanie produktow",
            "Miejsce": "SQL"
        },
        {
            "Operacja": "ORDER BY",
            "Zadanie": "Sortowanie wynikow",
            "Miejsce": "SQL"
        },
        {
            "Operacja": "LIMIT",
            "Zadanie": "Wybor TOP 10",
            "Miejsce": "SQL"
        }
    ])

    print(operations.to_string(index=False))

    section("14. AUTOMATYCZNE TESTY")

    tests = {
        "Baza zawiera 500 000 rekordow":
            conn.execute(
                "SELECT COUNT(*) FROM sales"
            ).fetchone()[0] == N_RECORDS,

        "Utworzono dodatkowy indeks":
            not indexes.empty,

        "Indeks ma poprawna nazwe":
            "idx_sales_region_date"
            in indexes["name"].values,

        "Plan przed optymalizacja zawiera SCAN":
            plan_before["detail"].str.contains(
                "SCAN"
            ).any(),

        "Plan po optymalizacji zawiera SEARCH":
            plan["detail"].str.contains(
                "SEARCH"
            ).any(),

        "Plan wykorzystuje indeks":
            plan["detail"].str.contains(
                "idx_sales_region_date"
            ).any(),

        "Zapytanie wykorzystuje WHERE":
            "WHERE" in QUERY.upper(),

        "Zapytanie wykorzystuje SUM":
            "SUM(" in QUERY.upper(),

        "Zapytanie wykorzystuje COUNT":
            "COUNT(" in QUERY.upper(),

        "Zapytanie wykorzystuje GROUP BY":
            "GROUP BY" in QUERY.upper(),

        "Zapytanie wykorzystuje ORDER BY":
            "ORDER BY" in QUERY.upper(),

        "Zapytanie wykorzystuje LIMIT":
            "LIMIT" in QUERY.upper(),

        "Zapytanie nie wykorzystuje SELECT *":
            "SELECT *" not in QUERY.upper(),

        "Pobrano tylko 10 rekordow":
            downloaded_rows == TOP_N,

        "Pobrano mniej rekordow niz w wersji 2":
            downloaded_rows < filtered_count,

        "Liczba rekordow po filtrowaniu jest poprawna":
            filtered_count == 31_006,

        "Redukcja liczby wierszy wynosi 99.998 procent":
            np.isclose(transfer_reduction, 99.998),

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

        "Nazwy kolumn wyniku sa poprawne":
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

        "Brak brakujacych wartosci":
            not result.isna().any().any(),

        "Najlepszy produkt to Product_017":
            result.iloc[0]["product"] == "Product_017",

        "Najwyzszy przychod wynosi 513583":
            result.iloc[0]["total_revenue"] == 513583,

        "Najlepszy produkt ma 336 transakcji":
            result.iloc[0]["transactions"] == 336,

        "Wyniki SQL i Pandas sa identyczne":
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

    section("15. WNIOSKI - GREEN SQL")

    conclusions = [
        "WHERE ogranicza liczbe przetwarzanych rekordow.",
        "Indeks wspiera wyszukiwanie danych.",
        "SELECT pobiera tylko potrzebne kolumny.",
        "SUM oblicza przychody bezposrednio w bazie.",
        "COUNT liczy transakcje bezposrednio w bazie.",
        "GROUP BY agreguje dane po stronie SQL.",
        "ORDER BY sortuje zagregowane wyniki.",
        "LIMIT ogranicza liczbe zwracanych rekordow.",
        "Python otrzymuje gotowy wynik analizy.",
        "Nie trzeba pobierac wszystkich danych do Pandas.",
        "Mniejszy DataFrame ogranicza zuzycie pamieci.",
        "Mniej pobranych rekordow ogranicza transfer danych.",
        "EXPLAIN QUERY PLAN pomaga analizowac wydajnosc.",
        "Indeksy maja koszt tworzenia i utrzymania.",
        "Indeksy moga zwiekszac koszt operacji zapisu.",
        "Czas tworzenia indeksu nie jest czescia benchmarku.",
        "Optymalizacja nie moze zmieniac wynikow analizy.",
        "Proxy energii nie jest rzeczywistym pomiarem energii.",
        "Pamiec DataFrame nie oznacza calej pamieci procesu.",
        "Wydajnosc zalezy od danych, sprzetu i planu zapytania."
    ]

    for i, conclusion in enumerate(
        conclusions, start=1
    ):
        print(f"{i}. {conclusion}")

    section("PODSUMOWANIE")

    print("Strategia: W pelni zoptymalizowana")
    print(f"Liczba rekordow: {N_RECORDS:,}")
    print(f"Pobrane rekordy: {downloaded_rows:,}")
    print(f"Redukcja liczby wierszy: {transfer_reduction:.4f}%")
    print(f"Sredni czas: {metrics['time_s']:.6f} s")
    print(f"Pamiec: {metrics['memory_mb']:.6f} MiB")
    print(f"Proxy energii: {metrics['energy_proxy']:.9f}")
    print(f"Zaliczone testy: {passed}/{len(tests)}")

    conn.close()

    assert passed == len(tests), "Nie wszystkie testy zaliczone."

    print("\nWszystkie testy zakonczone pomyslnie.")
    print("Wersja 3 wykonana poprawnie.")


if __name__ == "__main__":
    main()
