# Lekcja 13 - Zadanie 20: Green SQL Challenge
# Koncowy raport porownawczy trzech strategii

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
    measure_strategy,
    reduction_percent
)

import zadanie20_v1_nieoptymalna as v1
import zadanie20_v2_czesciowa as v2
import zadanie20_v3_optymalna as v3


def text_bar(value, unit):
    """Tworzy tekstowy slupek o okreslonej skali."""

    units = round(value / unit)

    return "█" * units if units > 0 else "·"


def main():

    print("=" * 80)
    print("GREEN SQL CHALLENGE")
    print("KONCOWY RAPORT POROWNAWCZY")
    print("=" * 80)

    section("1. PARAMETRY BENCHMARKU")

    print(f"Liczba rekordow: {N_RECORDS:,}")
    print(f"Region: {REGION}")
    print(f"Data od: {DATE_FROM}")
    print(f"Data do: {DATE_TO}")
    print(f"TOP produktow: {TOP_N}")
    print(f"Liczba powtorzen: {REPEATS}")

    section("2. PRZYGOTOWANIE BAZY DANYCH")

    conn = create_database()

    record_count = conn.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    print(f"Liczba rekordow w bazie: {record_count:,}")

    # Wersja 1 - bez indeksow

    section("3. WERSJA 1 - NIEOPTYMALNA")

    plan1 = explain_query(
        conn,
        v1.QUERY
    )

    metrics1 = measure_strategy(
        v1.strategy,
        conn
    )

    print(plan1.to_string(index=False))

    print(f"Czas: {metrics1['time_s']:.6f} s")
    print(f"Pamiec: {metrics1['memory_mb']:.6f} MiB")
    print(f"Pobrane rekordy: {metrics1['downloaded_rows']:,}")

    # Utworzenie indeksu dla wersji 2 i 3

    section("4. UTWORZENIE INDEKSU")

    create_indexes(conn)

    indexes = pd.read_sql_query(
        "PRAGMA index_list('sales')",
        conn
    )

    print(indexes.to_string(index=False))

    # Wersja 2 - filtrowanie SQL, agregacja Python

    section("5. WERSJA 2 - CZESCIOWO ZOPTYMALIZOWANA")

    plan2 = explain_query(
        conn,
        v2.QUERY,
        (REGION, DATE_FROM, DATE_TO)
    )

    metrics2 = measure_strategy(
        v2.strategy,
        conn
    )

    print(plan2.to_string(index=False))

    print(f"Czas: {metrics2['time_s']:.6f} s")
    print(f"Pamiec: {metrics2['memory_mb']:.6f} MiB")
    print(f"Pobrane rekordy: {metrics2['downloaded_rows']:,}")

    # Wersja 3 - wszystkie operacje w SQL

    section("6. WERSJA 3 - W PELNI ZOPTYMALIZOWANA")

    plan3 = explain_query(
        conn,
        v3.QUERY,
        v3.PARAMS
    )

    metrics3 = measure_strategy(
        v3.strategy,
        conn
    )

    print(plan3.to_string(index=False))

    print(f"Czas: {metrics3['time_s']:.6f} s")
    print(f"Pamiec: {metrics3['memory_mb']:.6f} MiB")
    print(f"Pobrane rekordy: {metrics3['downloaded_rows']:,}")

    section("7. TABELA POROWNAWCZA - 3 WERSJE x 4 METRYKI")

    strategies = [
        ("Nieoptymalna", metrics1),
        ("Czesciowa", metrics2),
        ("Optymalna", metrics3)
    ]

    report = pd.DataFrame([
        {
            "Strategia": name,
            "Czas_s": metrics["time_s"],
            "Pamiec_MiB": metrics["memory_mb"],
            "Pobrane_wiersze": metrics["downloaded_rows"],
            "Proxy_energii": metrics["energy_proxy"]
        }
        for name, metrics in strategies
    ]).set_index("Strategia")

    print(report.round(9).to_string())

    section("8. SZCZEGOLOWE CZASY POMIAROW")

    timings = pd.DataFrame({
        name: metrics["times"]
        for name, metrics in strategies
    })

    timings.index = range(1, REPEATS + 1)
    timings.index.name = "Proba"

    print(timings.round(6).to_string())

    print("\nOdchylenia standardowe:")

    for name, metrics in strategies:
        print(
            f"{name:15s}: "
            f"{np.std(metrics['times']):.6f} s"
        )

    section("9. POROWNANIE PLANOW WYKONANIA")

    plans = []

    for name, plan in [
        ("Nieoptymalna", plan1),
        ("Czesciowa", plan2),
        ("Optymalna", plan3)
    ]:

        current_plan = plan.copy()
        current_plan.insert(0, "Strategia", name)

        plans.append(current_plan)

    all_plans = pd.concat(
        plans,
        ignore_index=True
    )

    print(all_plans.to_string(index=False))

    section("10. POROWNANIE STRATEGII")

    operations = pd.DataFrame([
        ["Indeks", "Nie", "Tak", "Tak"],
        ["SELECT", "Wszystkie", "Wybrane", "Wybrane"],
        ["Filtrowanie", "Python", "SQL", "SQL"],
        ["Agregacja", "Python", "Python", "SQL"],
        ["Sortowanie", "Python", "Python", "SQL"],
        ["TOP 10", "Python", "Python", "SQL"]
    ], columns=[
        "Operacja",
        "Nieoptymalna",
        "Czesciowa",
        "Optymalna"
    ])

    print(operations.to_string(index=False))

    section("11. PRZYSPIESZENIE WYKONANIA")

    speedup2 = (
        metrics1["time_s"] / metrics2["time_s"]
    )

    speedup3 = (
        metrics1["time_s"] / metrics3["time_s"]
    )

    speedup32 = (
        metrics2["time_s"] / metrics3["time_s"]
    )

    print(f"Wersja 2 vs 1: {speedup2:.2f}x")
    print(f"Wersja 3 vs 1: {speedup3:.2f}x")
    print(f"Wersja 3 vs 2: {speedup32:.2f}x")

    section("12. REDUKCJA ZUZYCIA ZASOBOW")

    metric_names = {
        "time_s": "Czas",
        "memory_bytes": "Pamiec DataFrame",
        "downloaded_rows": "Pobrane rekordy",
        "energy_proxy": "Proxy energii"
    }

    reductions = []

    for key, label in metric_names.items():

        reductions.append({
            "Metryka": label,
            "V2_vs_V1_%": reduction_percent(
                metrics1[key],
                metrics2[key]
            ),
            "V3_vs_V1_%": reduction_percent(
                metrics1[key],
                metrics3[key]
            ),
            "V3_vs_V2_%": reduction_percent(
                metrics2[key],
                metrics3[key]
            )
        })

    reduction_report = pd.DataFrame(reductions)

    print(
        reduction_report.round(6).to_string(index=False)
    )

    section("13. TEKSTOWY WYKRES CZASU")

    print("Legenda: 1 znak = okolo 10 ms\n")

    for name, metrics in strategies:

        bar = text_bar(
            metrics["time_s"],
            0.01
        )

        print(f"{name}:")
        print(bar)
        print(f"{metrics['time_s']:.6f} s\n")

    section("14. TEKSTOWY WYKRES PAMIECI")

    print("Legenda: 1 znak = okolo 500 KiB\n")

    for name, metrics in strategies:

        bar = text_bar(
            metrics["memory_bytes"],
            500 * 1024
        )

        print(f"{name}:")
        print(bar)
        print(f"{metrics['memory_mb']:.6f} MiB\n")

    section("15. TEKSTOWY WYKRES POBRANYCH REKORDOW")

    print("Legenda: 1 znak = okolo 5000 rekordow\n")

    for name, metrics in strategies:

        bar = text_bar(
            metrics["downloaded_rows"],
            5000
        )

        print(f"{name}:")
        print(bar)
        print(f"{metrics['downloaded_rows']:,} rekordow\n")

    print("Symbol · oznacza wartosc ponizej polowy jednostki.")

    section("16. ANALIZA PROXY ENERGII")

    for name, metrics in strategies:

        print(
            f"{name:15s}: "
            f"{metrics['energy_proxy']:.9f} s * MiB"
        )

    energy_reduction = reduction_percent(
        metrics1["energy_proxy"],
        metrics3["energy_proxy"]
    )

    print(
        f"\nRedukcja proxy energii: "
        f"{energy_reduction:.6f}%"
    )

    print(
        "Proxy energii = sredni czas * pamiec DataFrame."
    )

    print(
        "Nie jest to rzeczywisty pomiar energii w J lub kWh."
    )

    section("17. WERYFIKACJA ZGODNOSCI WYNIKOW")

    result1 = metrics1["result"]
    result2 = metrics2["result"]
    result3 = metrics3["result"]

    equal12 = result1.equals(result2)
    equal13 = result1.equals(result3)
    equal23 = result2.equals(result3)

    print(f"Wersja 1 == Wersja 2: {equal12}")
    print(f"Wersja 1 == Wersja 3: {equal13}")
    print(f"Wersja 2 == Wersja 3: {equal23}")

    section("18. WSPOLNY WYNIK - TOP 10 PRODUKTOW")

    print(result3.to_string(index=False))

    section("19. ANALIZA OSZCZEDNOSCI")

    saved_time = (
        metrics1["time_s"] - metrics3["time_s"]
    )

    saved_memory = (
        metrics1["memory_bytes"]
        - metrics3["memory_bytes"]
    )

    saved_rows = (
        metrics1["downloaded_rows"]
        - metrics3["downloaded_rows"]
    )

    print(f"Oszczedzony czas: {saved_time:.6f} s")

    print(
        f"Oszczedzona pamiec DataFrame: "
        f"{saved_memory / 1024**2:.6f} MiB"
    )

    print(f"Niepobrane rekordy: {saved_rows:,}")

    print(
        f"Redukcja czasu: "
        f"{reduction_percent(metrics1['time_s'], metrics3['time_s']):.6f}%"
    )

    print(
        f"Redukcja pamieci: "
        f"{reduction_percent(metrics1['memory_bytes'], metrics3['memory_bytes']):.6f}%"
    )

    print(
        f"Redukcja liczby pobranych rekordow: "
        f"{reduction_percent(metrics1['downloaded_rows'], metrics3['downloaded_rows']):.6f}%"
    )

    print(
        f"Redukcja proxy energii: "
        f"{energy_reduction:.6f}%"
    )

    section("20. AUTOMATYCZNE TESTY")

    tests = {
        "Baza zawiera 500 000 rekordow":
            record_count == N_RECORDS,

        "Raport zawiera 3 strategie i 4 metryki":
            report.shape == (3, 4),

        "Wersja 1 pobiera wszystkie rekordy":
            metrics1["downloaded_rows"] == N_RECORDS,

        "Wersja 2 pobiera 31 006 rekordow":
            metrics2["downloaded_rows"] == 31_006,

        "Wersja 3 pobiera 10 rekordow":
            metrics3["downloaded_rows"] == TOP_N,

        "Liczba pobranych rekordow maleje":
            metrics1["downloaded_rows"]
            > metrics2["downloaded_rows"]
            > metrics3["downloaded_rows"],

        "Pamiec DataFrame maleje":
            metrics1["memory_bytes"]
            > metrics2["memory_bytes"]
            > metrics3["memory_bytes"],

        "Wersja 1 wykorzystuje SCAN":
            plan1["detail"].str.contains("SCAN").any(),

        "Wersja 2 wykorzystuje indeks":
            plan2["detail"].str.contains(
                "idx_sales_region_date"
            ).any(),

        "Wersja 3 wykorzystuje indeks":
            plan3["detail"].str.contains(
                "idx_sales_region_date"
            ).any(),

        "Wersja 3 wykorzystuje GROUP BY":
            "GROUP BY" in v3.QUERY.upper(),

        "Wersja 3 wykorzystuje LIMIT":
            "LIMIT" in v3.QUERY.upper(),

        "Wszystkie strategie wykonaly 3 pomiary":
            all(
                len(metrics["times"]) == REPEATS
                for _, metrics in strategies
            ),

        "Wszystkie czasy sa dodatnie":
            all(
                metrics["time_s"] > 0
                for _, metrics in strategies
            ),

        "Wszystkie wartosci pamieci sa dodatnie":
            all(
                metrics["memory_bytes"] > 0
                for _, metrics in strategies
            ),

        "Wszystkie proxy energii sa dodatnie":
            all(
                metrics["energy_proxy"] > 0
                for _, metrics in strategies
            ),

        "Proxy energii obliczono poprawnie":
            all(
                np.isclose(
                    metrics["energy_proxy"],
                    metrics["time_s"] * metrics["memory_mb"]
                )
                for _, metrics in strategies
            ),

        "Wersja 1 i 2 zwracaja identyczne wyniki":
            equal12,

        "Wersja 1 i 3 zwracaja identyczne wyniki":
            equal13,

        "Wersja 2 i 3 zwracaja identyczne wyniki":
            equal23,

        "Wszystkie wyniki zawieraja TOP 10":
            all(
                len(metrics["result"]) == TOP_N
                for _, metrics in strategies
            ),

        "Wynik zawiera 3 kolumny":
            result3.shape[1] == 3,

        "Produkty sa unikalne":
            result3["product"].is_unique,

        "Przychody sa posortowane malejaco":
            result3["total_revenue"].is_monotonic_decreasing,

        "Brak brakujacych wartosci":
            not result3.isna().any().any(),

        "Najlepszy produkt to Product_017":
            result3.iloc[0]["product"] == "Product_017",

        "Najwyzszy przychod wynosi 513583":
            result3.iloc[0]["total_revenue"] == 513583,

        "Redukcja liczby rekordow wynosi 99.998 procent":
            np.isclose(
                reduction_percent(
                    metrics1["downloaded_rows"],
                    metrics3["downloaded_rows"]
                ),
                99.998
            ),

        "Raport zawiera wszystkie plany":
            all_plans["Strategia"].nunique() == 3,

        "Oryginalna tabela zachowala liczbe rekordow":
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

    section("21. BEST PRACTICES - GREEN SQL")

    conclusions = [
        "Unikaj SELECT * w zapytaniach analitycznych.",
        "Pobieraj tylko potrzebne kolumny.",
        "Filtruj dane bezposrednio w SQL.",
        "Stosuj indeksy dopasowane do zapytan.",
        "Sprawdzaj plany przez EXPLAIN QUERY PLAN.",
        "Przenos agregacje do silnika bazy danych.",
        "Uzywaj GROUP BY, SUM i COUNT.",
        "Sortuj dane po stronie SQL, gdy jest to uzasadnione.",
        "Uzywaj LIMIT do ograniczania liczby wynikow.",
        "Stosuj parametryzowane zapytania SQL.",
        "Ograniczaj liczbe danych pobieranych do Pandas.",
        "Porownuj wydajnosc na identycznych danych.",
        "Wykonuj wielokrotne pomiary czasu.",
        "Sprawdzaj zgodnosc wynikow po optymalizacji.",
        "Uwzgledniaj koszt tworzenia i utrzymania indeksow.",
        "Indeksy moga spowalniac operacje zapisu.",
        "Nie kazdy indeks poprawia wydajnosc.",
        "Pamiec DataFrame nie jest pamiecia calego procesu.",
        "Liczba wierszy jest przyblizeniem transferu danych.",
        "Proxy energii nie jest pomiarem rzeczywistej energii.",
        "Optymalizacja moze ograniczyc zuzycie zasobow.",
        "Wyniki benchmarku zaleza od sprzetu i danych."
    ]

    for i, conclusion in enumerate(
        conclusions, start=1
    ):
        print(f"{i}. {conclusion}")

    section("22. OGRANICZENIA BENCHMARKU")

    print("1. Baza SQLite dziala lokalnie w pamieci.")
    print("2. Nie mierzymy rzeczywistego transferu sieciowego.")
    print("3. Nie mierzymy rzeczywistego zuzycia energii.")
    print("4. Pamiec DataFrame nie obejmuje calego procesu.")
    print("5. Czas tworzenia bazy i indeksu jest poza pomiarem.")
    print("6. Kolejnosc prob i cache moga wplywac na wyniki.")
    print("7. Wyniki czasowe moga sie roznic miedzy uruchomieniami.")
    print("8. Testy nie wymagaja okreslonego przyspieszenia.")

    section("PODSUMOWANIE GREEN SQL CHALLENGE")

    print(f"Liczba rekordow: {N_RECORDS:,}")
    print("Liczba strategii: 3")
    print(f"Liczba pomiarow: {3 * REPEATS}")
    print(f"Przyspieszenie V3 vs V1: {speedup3:.2f}x")

    print(
        f"Redukcja czasu: "
        f"{reduction_percent(metrics1['time_s'], metrics3['time_s']):.4f}%"
    )

    print(
        f"Redukcja pamieci: "
        f"{reduction_percent(metrics1['memory_bytes'], metrics3['memory_bytes']):.6f}%"
    )

    print(
        f"Redukcja liczby rekordow: "
        f"{reduction_percent(metrics1['downloaded_rows'], metrics3['downloaded_rows']):.6f}%"
    )

    print(
        f"Redukcja proxy energii: "
        f"{energy_reduction:.6f}%"
    )

    print(f"Zgodnosc wszystkich wynikow: {equal12 and equal13 and equal23}")
    print(f"Zaliczone testy: {passed}/{len(tests)}")

    conn.close()

    assert passed == len(tests), "Nie wszystkie testy zaliczone."

    print("\nWszystkie testy zakonczone pomyslnie.")
    print("Green SQL Challenge wykonany poprawnie.")
    print("Zadanie 20 zakonczone.")


if __name__ == "__main__":
    main()
