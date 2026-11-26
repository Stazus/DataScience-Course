# Lekcja 13 - Zadanie 20: Green SQL Challenge
# Wersja 2 - Czesciowo zoptymalizowana

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


# Zapytanie pobiera tylko potrzebne kolumny
# i rekordy spelniajace warunki filtrowania

QUERY = """
SELECT
    product,
    revenue
FROM sales
WHERE region = ?
  AND sale_date >= ?
  AND sale_date < ?
"""

PARAMS = (
    REGION,
    DATE_FROM,
    DATE_TO
)


def strategy(conn):
    """Filtruje w SQL, agreguje w Pythonie."""

    downloaded = pd.read_sql_query(
        QUERY,
        conn,
        params=PARAMS
    )

    result = aggregate_python(downloaded)

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
    print("WERSJA 2 - CZESCIOWO ZOPTYMALIZOWANA")
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

    print("""
CREATE INDEX IF NOT EXISTS idx_sales_region_date
ON sales(region, sale_date)
    """.strip())

    create_indexes(conn)

    indexes = pd.read_sql_query(
        "PRAGMA index_list('sales')",
        conn
    )

    print("\nIndeksy tabeli sales:")
    print(indexes.to_string(index=False))

    index_columns = pd.read_sql_query(
        "PRAGMA index_info('idx_sales_region_date')",
        conn
    )

    print("\nKolumny indeksu:")
    print(index_columns.to_string(index=False))

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

    print(f"Wszystkie rekordy: {N_RECORDS:,}")
    print(f"Pobrane rekordy: {downloaded_rows:,}")
    print(f"Niepobrane rekordy: {avoided_rows:,}")
    print(f"Redukcja liczby pobranych wierszy: {transfer_reduction:.2f}%")
    print(f"Liczba pobranych kolumn: 2")
    print(f"Koncowa liczba wynikow: {len(result)}")

    section("10. RAPORT METRYK")

    report = pd.DataFrame([{
        "Strategia": "Czesciowa",
        "Czas_s": metrics["time_s"],
        "Pamiec_MiB": metrics["memory_mb"],
        "Pobrane_wiersze": downloaded_rows,
        "Proxy_energii": metrics["energy_proxy"]
    }])

    print(
        report.round(6).to_string(index=False)
    )

    section("11. TEKSTOWA WIZUALIZACJA")

    time_bar = "█" * max(
        1, round(metrics["time_s"] / 0.01)
    )

    memory_bar = "█" * max(
        1, round(
            metrics["memory_bytes"] / (500 * 1024)
        )
    )

    print("Czas wykonania (1 znak = okolo 10 ms):")
    print(time_bar)
    print(f"{metrics['time_s']:.6f} s")

    print("\nPamiec (1 znak = okolo 500 KiB):")
    print(memory_bar)
    print(f"{metrics['memory_mb']:.4f} MiB")

    section("12. WERYFIKACJA SQL I PANDAS")

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

    print(reference.to_string(index=False))

    print(
        "\nCzy wyniki SQL i Pandas sa identyczne:",
        result.equals(reference)
    )

    filtered_count = conn.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE region = ?
          AND sale_date >= ?
          AND sale_date < ?
    """, PARAMS).fetchone()[0]

    downloaded_sample = pd.read_sql_query(
        QUERY,
        conn,
        params=PARAMS
    )

    section("13. AUTOMATYCZNE TESTY")

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

        "Indeks zawiera kolumne region":
            "region" in index_columns["name"].values,

        "Indeks zawiera kolumne sale_date":
            "sale_date" in index_columns["name"].values,

        "Poprawna kolejnosc kolumn indeksu":
            index_columns["name"].tolist()
            == ["region", "sale_date"],

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

        "Pobrano mniej niz 500 000 rekordow":
            downloaded_rows < N_RECORDS,

        "Liczba pobranych rekordow jest poprawna":
            downloaded_rows == filtered_count,

        "Pobrano 31 006 rekordow":
            downloaded_rows == 31_006,

        "Pobrano tylko dwie kolumny":
            downloaded_sample.shape[1] == 2,

        "Pobrano wlasciwe kolumny":
            list(downloaded_sample.columns)
            == ["product", "revenue"],

        "Redukcja liczby wierszy przekracza 90 procent":
            transfer_reduction > 90,

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

    section("14. WNIOSKI")

    conclusions = [
        "WHERE filtruje rekordy bezposrednio w bazie.",
        "Indeks zlozony wspiera filtrowanie po regionie i dacie.",
        "SEARCH USING INDEX oznacza wykorzystanie indeksu.",
        "Indeks ogranicza potrzebe skanowania calej tabeli.",
        "SELECT wybranych kolumn ogranicza ilosc danych.",
        "Filtrowanie SQL zmniejsza liczbe pobieranych rekordow.",
        "Mniejszy DataFrame ogranicza zuzycie pamieci.",
        "Parametry SQL oddzielaja dane od tresci zapytania.",
        "Agregacja nadal odbywa sie w Pandas.",
        "Sortowanie i TOP 10 nadal odbywaja sie w Pythonie.",
        "Indeksy zajmuja dodatkowa pamiec.",
        "Indeksy moga zwiekszac koszt operacji zapisu.",
        "Czas tworzenia indeksu nie jest czescia benchmarku.",
        "Proxy energii jest wskaznikiem umownym.",
        "Kolejny etap to przeniesienie agregacji do SQL."
    ]

    for i, conclusion in enumerate(
        conclusions, start=1
    ):
        print(f"{i}. {conclusion}")

    section("PODSUMOWANIE")

    print("Strategia: Czesciowo zoptymalizowana")
    print(f"Liczba rekordow: {N_RECORDS:,}")
    print(f"Pobrane rekordy: {downloaded_rows:,}")
    print(f"Redukcja liczby wierszy: {transfer_reduction:.2f}%")
    print(f"Sredni czas: {metrics['time_s']:.6f} s")
    print(f"Pamiec: {metrics['memory_mb']:.4f} MiB")
    print(f"Proxy energii: {metrics['energy_proxy']:.6f}")
    print(f"Zaliczone testy: {passed}/{len(tests)}")

    conn.close()

    assert passed == len(tests), "Nie wszystkie testy zaliczone."

    print("\nWszystkie testy zakonczone pomyslnie.")
    print("Wersja 2 wykonana poprawnie.")


if __name__ == "__main__":
    main()
