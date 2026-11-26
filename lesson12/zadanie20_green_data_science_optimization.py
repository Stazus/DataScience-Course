# Lekcja 12 - Zadanie 20: Green Data Science Optimization

import gc
import time

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


def memory_mb(df):
    """Oblicza zuzycie pamieci DataFrame w MiB."""
    return df.memory_usage(deep=True).sum() / 1024**2


def aggregate_sales(df):
    """Agreguje sprzedaz i koszty wedlug regionu."""
    return df.groupby(
        "Region",
        observed=True,
        sort=True
    ).agg({
        "Sprzedaż": ["sum", "mean", "min", "max", "count"],
        "Koszt": ["sum", "mean", "min", "max"]
    })


def benchmark_aggregation(df, repetitions=3):
    """Mierzy czas agregacji i zwraca srednia z prob."""
    times = []

    for number in range(1, repetitions + 1):
        start = time.perf_counter()

        result = aggregate_sales(df)

        elapsed = time.perf_counter() - start
        times.append(elapsed)

        print(f"Proba {number}: {elapsed:.6f} s")

    return result, times, float(np.mean(times))


def text_bar(value, maximum, width=50):
    """Generuje tekstowy slupek."""
    if maximum <= 0:
        return ""

    length = round(value / maximum * width)
    return "█" * length


print("=" * 75)
print("GREEN DATA SCIENCE OPTIMIZATION")
print("=" * 75)


# ==========================================================
# 1. GENEROWANIE DATASETU
# ==========================================================

section("GENEROWANIE DATASETU")

np.random.seed(42)

N = 1_000_000

generation_start = time.perf_counter()

big_sales = pd.DataFrame({
    "Region": np.random.choice(
        ["North", "South", "East", "West"], N
    ),
    "Produkt": np.random.choice(list("ABCDE"), N),
    "Sprzedaż": np.random.randint(10, 1000, N),
    "Koszt": np.random.randint(5, 500, N)
})

# Jawne typy poczatkowe dla powtarzalnego benchmarku
big_sales = big_sales.astype({
    "Region": "object",
    "Produkt": "object",
    "Sprzedaż": "int64",
    "Koszt": "int64"
})

generation_time = time.perf_counter() - generation_start

original_shape = big_sales.shape
original_index = big_sales.index.copy()

print(f"Shape: {big_sales.shape}")
print(f"Liczba obserwacji: {len(big_sales):,}")
print(f"Liczba kolumn: {len(big_sales.columns)}")
print(f"Liczba regionow: {big_sales['Region'].nunique()}")
print(f"Liczba produktow: {big_sales['Produkt'].nunique()}")
print(f"Liczba NaN: {big_sales.isna().sum().sum()}")
print(f"Czas generowania: {generation_time:.6f} s")
print("Seed: 42")


section("PIERWSZE 10 REKORDOW")

print(big_sales.head(10).to_string(index=False))


section("TYPY DANYCH PRZED OPTYMALIZACJA")

types_before = big_sales.dtypes.astype(str)

print(types_before.to_string())


section("STATYSTYKI DANYCH LICZBOWYCH")

print(
    big_sales[["Sprzedaż", "Koszt"]]
    .describe()
    .round(2)
    .to_string()
)


# ==========================================================
# 2. PAMIEC PRZED OPTYMALIZACJA
# ==========================================================

section("ZUZYCIE PAMIECI PRZED OPTYMALIZACJA")

memory_columns_before = (
    big_sales.memory_usage(deep=True) / 1024**2
)

memory_before = memory_mb(big_sales)

print(memory_columns_before.round(6).to_string())
print(f"\nCalkowita pamiec: {memory_before:.6f} MiB")


# Zachowanie podstawowych metryk kontrolnych
sales_sum_before = int(big_sales["Sprzedaż"].sum())
cost_sum_before = int(big_sales["Koszt"].sum())

sales_min_before = int(big_sales["Sprzedaż"].min())
sales_max_before = int(big_sales["Sprzedaż"].max())

cost_min_before = int(big_sales["Koszt"].min())
cost_max_before = int(big_sales["Koszt"].max())

regions_before = set(big_sales["Region"].unique())
products_before = set(big_sales["Produkt"].unique())

sample_before = big_sales.head(100).copy()


# ==========================================================
# 3. BENCHMARK PRZED OPTYMALIZACJA
# ==========================================================

section("BENCHMARK AGREGACJI PRZED OPTYMALIZACJA")

aggregation_before, times_before, time_before = (
    benchmark_aggregation(big_sales, repetitions=3)
)

print(f"\nSredni czas: {time_before:.6f} s")


section("AGREGACJA PRZED OPTYMALIZACJA")

print(aggregation_before.round(2).to_string())


# ==========================================================
# 4. OPTYMALIZACJA TYPOW DANYCH
# ==========================================================

section("WERYFIKACJA ZAKRESU INT16")

int16_info = np.iinfo(np.int16)

print(f"Minimum int16: {int16_info.min}")
print(f"Maksimum int16: {int16_info.max}")

for column in ["Sprzedaż", "Koszt"]:
    minimum = big_sales[column].min()
    maximum = big_sales[column].max()

    print(f"{column}: {minimum} - {maximum}")

    if minimum < int16_info.min or maximum > int16_info.max:
        raise OverflowError(
            f"Kolumna {column} nie miesci sie w int16."
        )


section("OPTYMALIZACJA TYPOW DANYCH")

optimization_start = time.perf_counter()

big_sales["Region"] = big_sales["Region"].astype(
    "category"
)

big_sales["Produkt"] = big_sales["Produkt"].astype(
    "category"
)

big_sales["Sprzedaż"] = big_sales["Sprzedaż"].astype(
    "int16"
)

big_sales["Koszt"] = big_sales["Koszt"].astype(
    "int16"
)

optimization_time = (
    time.perf_counter() - optimization_start
)

print("Region: object -> category")
print("Produkt: object -> category")
print("Sprzedaz: int64 -> int16")
print("Koszt: int64 -> int16")
print(f"Czas konwersji: {optimization_time:.6f} s")


section("TYPY DANYCH PO OPTYMALIZACJI")

types_after = big_sales.dtypes.astype(str)

print(types_after.to_string())


section("POROWNANIE TYPOW DANYCH")

types_comparison = pd.DataFrame({
    "Przed": types_before,
    "Po": types_after
})

print(types_comparison.to_string())


# ==========================================================
# 5. PAMIEC PO OPTYMALIZACJI
# ==========================================================

section("ZUZYCIE PAMIECI PO OPTYMALIZACJI")

memory_columns_after = (
    big_sales.memory_usage(deep=True) / 1024**2
)

memory_after = memory_mb(big_sales)

memory_saved = memory_before - memory_after

memory_reduction = (
    memory_saved / memory_before * 100
)

compression_ratio = memory_before / memory_after

print(memory_columns_after.round(6).to_string())

print(f"\nPamiec przed: {memory_before:.6f} MiB")
print(f"Pamiec po: {memory_after:.6f} MiB")
print(f"Oszczednosc: {memory_saved:.6f} MiB")
print(f"Redukcja pamieci: {memory_reduction:.2f}%")
print(f"Wspolczynnik kompresji: {compression_ratio:.2f}x")


section("POROWNANIE PAMIECI WEDLUG KOLUMN")

memory_comparison = pd.DataFrame({
    "Przed_MiB": memory_columns_before,
    "Po_MiB": memory_columns_after
})

memory_comparison["Oszczednosc_MiB"] = (
    memory_comparison["Przed_MiB"]
    - memory_comparison["Po_MiB"]
)

memory_comparison["Redukcja_%"] = (
    memory_comparison["Oszczednosc_MiB"]
    / memory_comparison["Przed_MiB"] * 100
)

print(memory_comparison.round(4).to_string())


section("TEKSTOWY WYKRES ZUZYCIA PAMIECI")

print(
    f"Przed | "
    f"{text_bar(memory_before, memory_before):50s}"
    f" {memory_before:.2f} MiB"
)

print(
    f"Po    | "
    f"{text_bar(memory_after, memory_before):50s}"
    f" {memory_after:.2f} MiB"
)


# ==========================================================
# 6. BENCHMARK PO OPTYMALIZACJI
# ==========================================================

section("BENCHMARK AGREGACJI PO OPTYMALIZACJI")

aggregation_after, times_after, time_after = (
    benchmark_aggregation(big_sales, repetitions=3)
)

print(f"\nSredni czas: {time_after:.6f} s")


section("POROWNANIE CZASU AGREGACJI")

time_saved = time_before - time_after

time_reduction = (
    time_saved / time_before * 100
)

speedup = time_before / time_after

benchmark_table = pd.DataFrame({
    "Proba": [1, 2, 3],
    "Przed_s": times_before,
    "Po_s": times_after
})

print(
    benchmark_table.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}"
    )
)

print(f"\nSredni czas przed: {time_before:.6f} s")
print(f"Sredni czas po: {time_after:.6f} s")
print(f"Oszczednosc czasu: {time_saved:.6f} s")
print(f"Redukcja czasu: {time_reduction:.2f}%")
print(f"Przyspieszenie: {speedup:.2f}x")

if time_after < time_before:
    print("Agregacja po optymalizacji jest szybsza.")
elif time_after > time_before:
    print("Agregacja po optymalizacji jest wolniejsza.")
else:
    print("Czasy agregacji sa identyczne.")


section("TEKSTOWY WYKRES CZASU AGREGACJI")

maximum_time = max(time_before, time_after)

print(
    f"Przed | "
    f"{text_bar(time_before, maximum_time):50s}"
    f" {time_before:.6f} s"
)

print(
    f"Po    | "
    f"{text_bar(time_after, maximum_time):50s}"
    f" {time_after:.6f} s"
)


# ==========================================================
# 7. WERYFIKACJA ZGODNOSCI AGREGACJI
# ==========================================================

section("POROWNANIE WYNIKOW AGREGACJI")

# Ujednolicenie indeksow do porownania
before_check = aggregation_before.copy()
after_check = aggregation_after.copy()

before_check.index = before_check.index.astype(str)
after_check.index = after_check.index.astype(str)

before_check = before_check.sort_index()
after_check = after_check.sort_index()

try:
    pd.testing.assert_frame_equal(
        before_check,
        after_check,
        check_dtype=False,
        check_exact=False,
        rtol=1e-10,
        atol=1e-10
    )

    aggregations_equal = True

except AssertionError:
    aggregations_equal = False

print(
    "Czy agregacje przed i po sa zgodne:",
    aggregations_equal
)

print(aggregation_after.round(2).to_string())


# ==========================================================
# 8. ANALIZA SPRZEDAZY WEDLUG REGIONU
# ==========================================================

section("SZCZEGOLOWA ANALIZA REGIONALNA")

regional_sales = big_sales.groupby(
    "Region",
    observed=True
).agg(
    Liczba_transakcji=("Sprzedaż", "size"),
    Suma_sprzedazy=("Sprzedaż", "sum"),
    Srednia_sprzedaz=("Sprzedaż", "mean"),
    Suma_kosztow=("Koszt", "sum"),
    Sredni_koszt=("Koszt", "mean")
)

regional_sales["Zysk"] = (
    regional_sales["Suma_sprzedazy"]
    - regional_sales["Suma_kosztow"]
)

regional_sales["Rentownosc_%"] = (
    regional_sales["Zysk"]
    / regional_sales["Suma_sprzedazy"] * 100
)

regional_sales["Udzial_sprzedazy_%"] = (
    regional_sales["Suma_sprzedazy"]
    / regional_sales["Suma_sprzedazy"].sum() * 100
)

regional_sales = regional_sales.sort_values(
    "Suma_sprzedazy",
    ascending=False
)

print(regional_sales.round(2).to_string())


section("TEKSTOWY WYKRES SPRZEDAZY REGIONALNEJ")

max_sales = regional_sales["Suma_sprzedazy"].max()

for region, row in regional_sales.iterrows():
    value = row["Suma_sprzedazy"]

    print(
        f"{region:6s} | "
        f"{text_bar(value, max_sales):50s}"
        f" {value:,.0f}"
    )


section("TEKSTOWY WYKRES UDZIALU REGIONOW")

print("Legenda: jeden znak = okolo 2%")

for region, row in regional_sales.iterrows():
    share = row["Udzial_sprzedazy_%"]
    bar = "█" * round(share / 2)

    print(f"{region:6s} | {bar:50s} {share:.2f}%")


section("POROWNANIE REGIONOW")

best_sales_region = (
    regional_sales["Suma_sprzedazy"].idxmax()
)

best_profit_region = (
    regional_sales["Zysk"].idxmax()
)

best_margin_region = (
    regional_sales["Rentownosc_%"].idxmax()
)

print(f"Najwieksza sprzedaz: {best_sales_region}")
print(f"Najwiekszy zysk: {best_profit_region}")
print(f"Najwyzsza rentownosc: {best_margin_region}")

print(
    "Calkowita sprzedaz:",
    f"{regional_sales['Suma_sprzedazy'].sum():,}"
)

print(
    "Calkowite koszty:",
    f"{regional_sales['Suma_kosztow'].sum():,}"
)

print(
    "Calkowity zysk:",
    f"{regional_sales['Zysk'].sum():,}"
)


# ==========================================================
# 9. PAMIEC PO AGREGACJI
# ==========================================================

section("REDUKCJA PAMIECI DZIEKI AGREGACJI")

# Docelowy raport zamiast miliona surowych rekordow
aggregated_report = regional_sales.reset_index()

memory_aggregated = memory_mb(aggregated_report)

total_memory_reduction = (
    (memory_before - memory_aggregated)
    / memory_before * 100
)

print(f"Surowe dane: {original_shape}")
print(f"Raport zagregowany: {aggregated_report.shape}")

print(f"Pamiec przed: {memory_before:.6f} MiB")
print(f"Pamiec po zmianie typow: {memory_after:.6f} MiB")
print(f"Pamiec raportu: {memory_aggregated:.9f} MiB")

print(
    f"Pamiec raportu w KiB: "
    f"{memory_aggregated * 1024:.4f}"
)

print(
    f"Calkowita redukcja: "
    f"{total_memory_reduction:.6f}%"
)

print(
    "Agregacja zachowuje statystyki regionalne, "
    "ale nie zachowuje szczegolow transakcji."
)


# ==========================================================
# 10. RAPORT KONCOWY
# ==========================================================

section("RAPORT METRYK GREEN DATA SCIENCE")

metrics = pd.DataFrame({
    "Metryka": [
        "Liczba rekordow",
        "Pamiec przed (MiB)",
        "Pamiec po (MiB)",
        "Oszczednosc pamieci (MiB)",
        "Redukcja pamieci (%)",
        "Kompresja (x)",
        "Czas przed (s)",
        "Czas po (s)",
        "Oszczednosc czasu (s)",
        "Redukcja czasu (%)",
        "Przyspieszenie (x)",
        "Czas konwersji typow (s)",
        "Pamiec raportu (MiB)",
        "Calkowita redukcja (%)"
    ],
    "Wartosc": [
        f"{N:,}",
        f"{memory_before:.6f}",
        f"{memory_after:.6f}",
        f"{memory_saved:.6f}",
        f"{memory_reduction:.2f}",
        f"{compression_ratio:.2f}",
        f"{time_before:.6f}",
        f"{time_after:.6f}",
        f"{time_saved:.6f}",
        f"{time_reduction:.2f}",
        f"{speedup:.2f}",
        f"{optimization_time:.6f}",
        f"{memory_aggregated:.9f}",
        f"{total_memory_reduction:.6f}"
    ]
})

print(metrics.to_string(index=False))


section("WERYFIKACJA CELU OPTYMALIZACJI")

target_reduction = 50.0

target_achieved = memory_reduction >= target_reduction

print(f"Wymagana redukcja: {target_reduction:.2f}%")
print(f"Osiagnieta redukcja: {memory_reduction:.2f}%")
print(f"Czy osiagnieto cel: {target_achieved}")

if target_achieved:
    print("Cel optymalizacji zostal osiagniety.")
else:
    print("Cel optymalizacji nie zostal osiagniety.")


# ==========================================================
# 11. AUTOMATYCZNE TESTY
# ==========================================================

section("WERYFIKACJA")

sample_after = big_sales.head(100).astype(
    sample_before.dtypes.to_dict()
)

sample_equal = sample_before.equals(sample_after)

tests = {
    "Dataset ma milion wierszy":
        len(big_sales) == N,

    "Dataset ma 4 kolumny":
        big_sales.shape[1] == 4,

    "Zachowano shape":
        big_sales.shape == original_shape,

    "Zachowano indeksy":
        big_sales.index.equals(original_index),

    "Istnieja 4 regiony":
        big_sales["Region"].nunique() == 4,

    "Istnieje 5 produktow":
        big_sales["Produkt"].nunique() == 5,

    "Dataset nie zawiera NaN":
        not big_sales.isna().any().any(),

    "Poczatkowy Region ma typ object":
        types_before["Region"] == "object",

    "Poczatkowy Produkt ma typ object":
        types_before["Produkt"] == "object",

    "Poczatkowa Sprzedaz ma typ int64":
        types_before["Sprzedaż"] == "int64",

    "Poczatkowy Koszt ma typ int64":
        types_before["Koszt"] == "int64",

    "Region ma typ category":
        types_after["Region"] == "category",

    "Produkt ma typ category":
        types_after["Produkt"] == "category",

    "Sprzedaz ma typ int16":
        types_after["Sprzedaż"] == "int16",

    "Koszt ma typ int16":
        types_after["Koszt"] == "int16",

    "Sprzedaz miesci sie w zakresie 10-999":
        big_sales["Sprzedaż"].between(10, 999).all(),

    "Koszt miesci sie w zakresie 5-499":
        big_sales["Koszt"].between(5, 499).all(),

    "Zachowano wszystkie regiony":
        set(big_sales["Region"].unique()) == regions_before,

    "Zachowano wszystkie produkty":
        set(big_sales["Produkt"].unique()) == products_before,

    "Zachowano minimum sprzedazy":
        big_sales["Sprzedaż"].min() == sales_min_before,

    "Zachowano maksimum sprzedazy":
        big_sales["Sprzedaż"].max() == sales_max_before,

    "Zachowano minimum kosztu":
        big_sales["Koszt"].min() == cost_min_before,

    "Zachowano maksimum kosztu":
        big_sales["Koszt"].max() == cost_max_before,

    "Zachowano sume sprzedazy":
        big_sales["Sprzedaż"].sum() == sales_sum_before,

    "Zachowano sume kosztow":
        big_sales["Koszt"].sum() == cost_sum_before,

    "Probka danych pozostala niezmieniona":
        sample_equal,

    "Pamiec przed jest dodatnia":
        memory_before > 0,

    "Pamiec po jest dodatnia":
        memory_after > 0,

    "Pamiec zostala zmniejszona":
        memory_after < memory_before,

    "Region zajmuje mniej pamieci":
        memory_columns_after["Region"]
        < memory_columns_before["Region"],

    "Produkt zajmuje mniej pamieci":
        memory_columns_after["Produkt"]
        < memory_columns_before["Produkt"],

    "Sprzedaz zajmuje mniej pamieci":
        memory_columns_after["Sprzedaż"]
        < memory_columns_before["Sprzedaż"],

    "Koszt zajmuje mniej pamieci":
        memory_columns_after["Koszt"]
        < memory_columns_before["Koszt"],

    "Oszczednosc pamieci jest poprawna":
        np.isclose(
            memory_saved,
            memory_before - memory_after
        ),

    "Redukcja pamieci jest poprawna":
        np.isclose(
            memory_reduction,
            (1 - memory_after / memory_before) * 100
        ),

    "Redukcja pamieci wynosi minimum 50%":
        target_achieved,

    "Kompresja jest wieksza od 1":
        compression_ratio > 1,

    "Wykonano 3 pomiary przed":
        len(times_before) == 3,

    "Wykonano 3 pomiary po":
        len(times_after) == 3,

    "Wszystkie czasy przed sa dodatnie":
        all(t > 0 for t in times_before),

    "Wszystkie czasy po sa dodatnie":
        all(t > 0 for t in times_after),

    "Sredni czas przed jest poprawny":
        np.isclose(time_before, np.mean(times_before)),

    "Sredni czas po jest poprawny":
        np.isclose(time_after, np.mean(times_after)),

    "Oszczednosc czasu jest poprawna":
        np.isclose(time_saved, time_before - time_after),

    "Przyspieszenie jest poprawnie obliczone":
        np.isclose(speedup, time_before / time_after),

    "Agregacje przed i po sa zgodne":
        aggregations_equal,

    "Agregacja przed ma 4 regiony":
        len(aggregation_before) == 4,

    "Agregacja po ma 4 regiony":
        len(aggregation_after) == 4,

    "Raport regionalny ma 4 wiersze":
        len(regional_sales) == 4,

    "Uwzgledniono milion transakcji":
        regional_sales["Liczba_transakcji"].sum() == N,

    "Regionalna suma sprzedazy jest zgodna":
        regional_sales["Suma_sprzedazy"].sum()
        == sales_sum_before,

    "Regionalna suma kosztow jest zgodna":
        regional_sales["Suma_kosztow"].sum()
        == cost_sum_before,

    "Calkowity zysk jest poprawny":
        regional_sales["Zysk"].sum()
        == sales_sum_before - cost_sum_before,

    "Udzialy regionow sumuja sie do 100%":
        np.isclose(
            regional_sales["Udzial_sprzedazy_%"].sum(),
            100
        ),

    "Rentownosc zostala poprawnie obliczona":
        np.allclose(
            regional_sales["Rentownosc_%"],
            regional_sales["Zysk"]
            / regional_sales["Suma_sprzedazy"] * 100
        ),

    "Raport nie zawiera NaN":
        not aggregated_report.isna().any().any(),

    "Raport zajmuje mniej pamieci niz dane surowe":
        memory_aggregated < memory_after,

    "Calkowita redukcja przekracza 99%":
        total_memory_reduction > 99
}

# Zachowujemy wyniki testow przed usunieciem danych
tests = {
    name: bool(result)
    for name, result in tests.items()
}


# ==========================================================
# 12. ZWOLNIENIE SUROWYCH DANYCH
# ==========================================================

section("ZWOLNIENIE PAMIECI")

del big_sales
del sample_before
del sample_after
del original_index

gc.collect()

raw_data_removed = "big_sales" not in globals()

tests["Usunieto referencje do surowych danych"] = (
    raw_data_removed
)

tests["Zachowano raport zagregowany"] = (
    len(aggregated_report) == 4
)

print(f"Usunieto surowy DataFrame: {raw_data_removed}")
print("Zachowano raport regionalny i metryki.")

print(
    "Usuniecie DataFrame pozwala odzyskac pamiec, "
    "ale nie gwarantuje natychmiastowego spadku RSS."
)


# ==========================================================
# 13. WNIOSKI
# ==========================================================

section("WNIOSKI")

print("1. Dataset zawieral milion rekordow.")
print("2. Category ogranicza pamiec powtarzalnych etykiet.")
print("3. Int16 zajmuje 2 bajty zamiast 8 bajtow int64.")
print("4. Przed konwersja sprawdzono zakres wartosci.")
print("5. Optymalizacja nie zmienila wynikow agregacji.")

print(
    f"6. Sama zmiana typow zmniejszyla pamiec "
    f"o {memory_reduction:.2f}%."
)

print(
    f"7. Zaoszczedzono {memory_saved:.2f} MiB pamieci."
)

if time_saved > 0:
    print(
        f"8. Czas agregacji zmniejszyl sie "
        f"o {time_reduction:.2f}%."
    )
else:
    print(
        "8. W tym pomiarze nie uzyskano "
        "przyspieszenia agregacji."
    )

print("9. Benchmark obejmowal po trzy proby.")
print("10. Czas konwersji mierzono oddzielnie.")
print("11. Agregacja dodatkowo ogranicza zuzycie pamieci.")
print("12. Agregacja powoduje utrate szczegolow transakcji.")
print("13. Mniejsze dane moga poprawic skalowalnosc.")
print("14. Zuzycie energii nie bylo bezposrednio mierzone.")
print("15. Czasy zaleza od sprzetu i obciazenia systemu.")
print("16. Dane sprzedazowe sa syntetyczne.")


# ==========================================================
# 14. PODSUMOWANIE
# ==========================================================

section("PODSUMOWANIE")

print(f"Liczba rekordow: {N:,}")
print(f"Liczba regionow: {len(aggregated_report)}")
print(f"Pamiec przed: {memory_before:.2f} MiB")
print(f"Pamiec po: {memory_after:.2f} MiB")
print(f"Oszczednosc pamieci: {memory_saved:.2f} MiB")
print(f"Redukcja pamieci: {memory_reduction:.2f}%")
print(f"Czas przed: {time_before:.6f} s")
print(f"Czas po: {time_after:.6f} s")
print(f"Redukcja czasu: {time_reduction:.2f}%")
print(f"Przyspieszenie: {speedup:.2f}x")
print(f"Pamiec raportu: {memory_aggregated * 1024:.4f} KiB")
print(f"Cel minimum 50%: {target_achieved}")


section("WYNIKI TESTOW")

for name, result in tests.items():
    print(f"Czy {name}: {result}")

passed = sum(tests.values())
total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")

assert all(tests.values()), (
    "Nie wszystkie testy zostaly zaliczone."
)

print("Wszystkie testy zakonczone pomyslnie.")

