# Lekcja 12 - Zadanie 11: Normalizacja grupowa

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Generator datasetu zgodny z materialem lekcji
def make_california_housing(n=5000, seed=42):
    """Generuje syntetyczny dataset California Housing."""

    rng = np.random.default_rng(seed)

    latitude = rng.uniform(32.5, 41.5, n)
    longitude = rng.uniform(-123.5, -114.5, n)

    med_inc = rng.gamma(
        shape=2.0, scale=1.8, size=n
    ) + 0.5

    house_age = rng.integers(1, 55, n)

    ave_rooms = rng.normal(
        5.5, 1.5, n
    ).clip(1, 15)

    ave_bedrms = (
        ave_rooms * rng.uniform(0.15, 0.25, n)
    ).clip(0.5, 5)

    population = rng.integers(50, 5000, n)

    ave_occup = rng.normal(
        3.0, 0.8, n
    ).clip(1, 10)

    med_house_val = (
        med_inc * 0.6
        + (latitude - 36) * 0.15
        - (house_age / 100)
        + rng.normal(0, 0.3, n)
    ).clip(0.15, 5.0)

    return pd.DataFrame({
        "MedInc": med_inc.round(4),
        "HouseAge": house_age,
        "AveRooms": ave_rooms.round(4),
        "AveBedrms": ave_bedrms.round(4),
        "Population": population,
        "AveOccup": ave_occup.round(4),
        "Latitude": latitude.round(4),
        "Longitude": longitude.round(4),
        "MedHouseVal": med_house_val.round(4)
    })


# Wlasna funkcja normalizacji Min-Max
def min_max_normalize(x):
    """Normalizuje wartosci do zakresu [0, 1]."""

    minimum = x.min()
    maximum = x.max()

    # Zabezpieczenie przed dzieleniem przez zero
    if maximum == minimum:
        return x * 0.0

    return (x - minimum) / (maximum - minimum)


# Generowanie datasetu
df = make_california_housing()

# Kopia oryginalnych danych
df_original = df.copy()

print("=" * 75)
print("NORMALIZACJA GRUPOWA - CALIFORNIA HOUSING")
print("=" * 75)


section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba obserwacji: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Liczba NaN: {df.isna().sum().sum()}")
print("Seed: 42")


section("PIERWSZE 10 REKORDOW")

print(df.head(10).to_string(index=False))


section("STATYSTYKI MEDINC PRZED NORMALIZACJA")

print(df["MedInc"].describe().round(4))


# Podzial geograficzny na siatke 4 x 4
df["lat_bin"] = pd.cut(
    df["Latitude"],
    bins=4
)

df["lon_bin"] = pd.cut(
    df["Longitude"],
    bins=4
)

# Utworzenie etykiet regionow
df["Region"] = (
    df["lat_bin"].astype(str)
    + " | "
    + df["lon_bin"].astype(str)
)


section("UTWORZONE REGIONY")

print(f"Liczba regionow: {df['Region'].nunique()}")

print(
    df["Region"]
    .value_counts()
    .sort_index()
    .to_string()
)


section("STATYSTYKI DOCHODU WEDLUG REGIONU")

stats_before = (
    df.groupby("Region")["MedInc"]
    .agg(["count", "min", "max", "mean", "std"])
)

print(stats_before.round(4).to_string())


# Normalizacja grupowa - glowne wymaganie zadania
df["MedInc_norm"] = (
    df.groupby("Region")["MedInc"]
    .transform(min_max_normalize)
)


section("PIERWSZE 10 REKORDOW PO NORMALIZACJI")

print(
    df[
        ["Region", "MedInc", "MedInc_norm"]
    ].head(10).round(4).to_string(index=False)
)


section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")

print(
    "Dodane kolumny:",
    df.columns.difference(
        df_original.columns
    ).tolist()
)

print(
    f"Typ MedInc_norm: {df['MedInc_norm'].dtype}"
)

print(
    f"Brakujace MedInc_norm: "
    f"{df['MedInc_norm'].isna().sum()}"
)


section("WERYFIKACJA MIN I MAX W REGIONACH")

verification = (
    df.groupby("Region")["MedInc_norm"]
    .agg(["min", "max"])
)

print(verification.round(6).to_string())


# Sprawdzenie granic z tolerancja numeryczna
verification["Min_poprawne"] = np.isclose(
    verification["min"], 0
)

verification["Max_poprawne"] = np.isclose(
    verification["max"], 1
)

verification["Poprawna_normalizacja"] = (
    verification["Min_poprawne"]
    & verification["Max_poprawne"]
)


section("SZCZEGOLOWA WERYFIKACJA REGIONOW")

print(verification.to_string())

print(
    "\nPoprawnie znormalizowane regiony:",
    f"{verification['Poprawna_normalizacja'].sum()}"
    f"/{len(verification)}"
)


section("STATYSTYKI MEDINC PO NORMALIZACJI")

print(df["MedInc_norm"].describe().round(4))


section("POROWNANIE STATYSTYK PRZED I PO")

comparison = pd.DataFrame({
    "MedInc": df["MedInc"].describe(),
    "MedInc_norm": df["MedInc_norm"].describe()
})

print(comparison.round(4).to_string())


section("SZCZEGOLOWE STATYSTYKI REGIONALNE")

regional_stats = df.groupby("Region").agg(
    Liczba_obserwacji=("MedInc", "size"),
    Min_przed=("MedInc", "min"),
    Max_przed=("MedInc", "max"),
    Srednia_przed=("MedInc", "mean"),
    Min_po=("MedInc_norm", "min"),
    Max_po=("MedInc_norm", "max"),
    Srednia_po=("MedInc_norm", "mean"),
    Std_po=("MedInc_norm", "std")
)

print(regional_stats.round(4).to_string())


# Dodatkowe porownanie z normalizacja globalna
global_normalized = min_max_normalize(
    df["MedInc"]
)

global_comparison = pd.DataFrame({
    "Region": df["Region"],
    "Grupowa": df["MedInc_norm"],
    "Globalna": global_normalized
})

global_stats = (
    global_comparison.groupby("Region")
    .agg(["min", "max"])
)


section("NORMALIZACJA GRUPOWA A GLOBALNA")

print(global_stats.round(4).to_string())

print(
    "\nNormalizacja grupowa: kazdy region "
    "ma minimum 0 i maksimum 1."
)

print(
    "Normalizacja globalna: minimum 0 i maksimum 1 "
    "dotycza calego datasetu."
)


section("TEKSTOWY WYKRES SREDNICH PO NORMALIZACJI")

print("Legenda: jeden znak = okolo 0.02")

for number, (region, row) in enumerate(
    regional_stats.iterrows(), start=1
):
    value = row["Srednia_po"]
    bar = "█" * int(round(value * 50))

    print(
        f"Region {number:02d} | "
        f"{bar:<50} {value:.4f}"
    )


section("MAPOWANIE NUMEROW REGIONOW")

for number, region in enumerate(
    regional_stats.index, start=1
):
    print(f"Region {number:02d}: {region}")


section("RANKING REGIONOW WEDLUG SREDNIEJ MEDINC")

ranking = regional_stats.sort_values(
    "Srednia_przed",
    ascending=False
)

print(
    ranking[
        [
            "Liczba_obserwacji",
            "Srednia_przed",
            "Srednia_po"
        ]
    ].round(4).to_string()
)


section("WARTOSCI SKRAJNE W REGIONACH")

for region, group in df.groupby("Region"):

    min_row = group.loc[group["MedInc"].idxmin()]
    max_row = group.loc[group["MedInc"].idxmax()]

    print(f"\nRegion: {region}")

    print(
        f"  Minimum: {min_row['MedInc']:.4f}"
        f" -> {min_row['MedInc_norm']:.4f}"
    )

    print(
        f"  Maksimum: {max_row['MedInc']:.4f}"
        f" -> {max_row['MedInc_norm']:.4f}"
    )


section("TEST FUNKCJI MIN-MAX")

test_series = pd.Series(
    [10.0, 20.0, 30.0, 40.0, 50.0]
)

test_normalized = min_max_normalize(
    test_series
)

test_table = pd.DataFrame({
    "Przed": test_series,
    "Po": test_normalized
})

print(test_table.to_string(index=False))


section("TEST GRUPY O STALYCH WARTOSCIACH")

constant_series = pd.Series(
    [5.0, 5.0, 5.0]
)

constant_normalized = min_max_normalize(
    constant_series
)

print(
    pd.DataFrame({
        "Przed": constant_series,
        "Po": constant_normalized
    }).to_string(index=False)
)

print(
    "Dla stalej grupy przyjeto 0, "
    "aby uniknac dzielenia przez zero."
)


section("TEST BRAKUJACYCH WARTOSCI")

nan_series = pd.Series(
    [10.0, np.nan, 20.0, 30.0]
)

nan_normalized = min_max_normalize(
    nan_series
)

print(
    pd.DataFrame({
        "Przed": nan_series,
        "Po": nan_normalized
    }).to_string(index=False)
)


# Niezalezna weryfikacja normalizacji
group_min = (
    df.groupby("Region")["MedInc"]
    .transform("min")
)

group_max = (
    df.groupby("Region")["MedInc"]
    .transform("max")
)

expected_normalized = (
    (df["MedInc"] - group_min)
    / (group_max - group_min)
)


section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum()
    / 1024
)

memory_after = (
    df.memory_usage(deep=True).sum()
    / 1024
)

memory_norm = (
    df["MedInc_norm"].memory_usage(
        index=False, deep=True
    ) / 1024
)

print(f"Przed: {memory_before:.2f} KiB")
print(f"Po: {memory_after:.2f} KiB")
print(f"Kolumna MedInc_norm: {memory_norm:.2f} KiB")
print(
    f"Calkowity wzrost: "
    f"{memory_after - memory_before:.2f} KiB"
)


section("WNIOSKI")

conclusions = [
    "Normalizacja Min-Max przeksztalca dane do zakresu [0, 1].",
    "GroupBy pozwala normalizowac kazdy region niezaleznie.",
    "Transform zachowuje liczbe wierszy i indeksy.",
    "Kazdy region ma w tym datasecie minimum 0 i maksimum 1.",
    "Normalizacja grupowa zachowuje kolejnosc wartosci w grupie.",
    "Normalizacja grupowa rozni sie od normalizacji globalnej.",
    "Wartosc 0.5 nie musi oznaczac sredniej grupy.",
    "Wartosc 0.5 oznacza polowe zakresu min-max.",
    "Identyczne wartosci po normalizacji moga oznaczac rozne dochody.",
    "Normalizacja Min-Max jest wrazliwa na wartosci odstajace.",
    "Grupy o stalych wartosciach wymagaja obslugi dzielenia przez zero.",
    "Oryginalna kolumna MedInc pozostala niezmieniona.",
    "Normalizacja grupowa jest technika Feature Engineering.",
    "W ML parametry normalizacji nalezy wyznaczac na danych treningowych.",
    "Dataset California Housing jest tutaj syntetyczny."
]

for number, conclusion in enumerate(
    conclusions, start=1
):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba obserwacji: {len(df)}")
print(f"Liczba regionow: {df['Region'].nunique()}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print("Nowa cecha: MedInc_norm")
print(f"Minimum: {df['MedInc_norm'].min():.6f}")
print(f"Maksimum: {df['MedInc_norm'].max():.6f}")

print(
    f"Poprawnie znormalizowane regiony: "
    f"{verification['Poprawna_normalizacja'].sum()}"
    f"/{len(verification)}"
)


section("WERYFIKACJA")

tests = {
    "Dataset ma 5000 wierszy":
        len(df_original) == 5000,

    "Dataset ma poczatkowo 9 kolumn":
        df_original.shape[1] == 9,

    "Dataset nie zawiera NaN":
        not df_original.isna().any().any(),

    "Utworzono 4 przedzialy Latitude":
        len(df["lat_bin"].cat.categories) == 4,

    "Utworzono 4 przedzialy Longitude":
        len(df["lon_bin"].cat.categories) == 4,

    "Utworzono 16 regionow":
        df["Region"].nunique() == 16,

    "Regiony nie zawieraja NaN":
        not df["Region"].isna().any(),

    "Dodano kolumne MedInc_norm":
        "MedInc_norm" in df.columns,

    "Wynik ma shape (5000, 13)":
        df.shape == (5000, 13),

    "Zachowano wszystkie wiersze":
        len(df) == len(df_original),

    "Zachowano oryginalne indeksy":
        df.index.equals(df_original.index),

    "MedInc_norm ma typ numeryczny":
        pd.api.types.is_numeric_dtype(
            df["MedInc_norm"]
        ),

    "MedInc_norm nie zawiera NaN":
        not df["MedInc_norm"].isna().any(),

    "Wartosci sa skonczone":
        np.isfinite(df["MedInc_norm"]).all(),

    "Wartosci sa nieujemne":
        df["MedInc_norm"].ge(0).all(),

    "Wartosci nie przekraczaja 1":
        df["MedInc_norm"].le(1).all(),

    "Globalne minimum wynosi 0":
        np.isclose(df["MedInc_norm"].min(), 0),

    "Globalne maksimum wynosi 1":
        np.isclose(df["MedInc_norm"].max(), 1),

    "Minimum kazdego regionu wynosi 0":
        verification["Min_poprawne"].all(),

    "Maksimum kazdego regionu wynosi 1":
        verification["Max_poprawne"].all(),

    "Wszystkie regiony sa poprawnie znormalizowane":
        verification["Poprawna_normalizacja"].all(),

    "Kazdy region ma niezerowy zakres":
        (stats_before["max"] > stats_before["min"]).all(),

    "Uwzgledniono wszystkie obserwacje":
        regional_stats["Liczba_obserwacji"].sum() == 5000,

    "Normalizacja jest zgodna ze wzorem":
        np.allclose(
            df["MedInc_norm"],
            expected_normalized
        ),

    "Normalizacja zachowuje kolejnosc w grupach":
        all(
            group.sort_values("MedInc")[
                "MedInc_norm"
            ].is_monotonic_increasing
            for _, group in df.groupby("Region")
        ),

    "Funkcja poprawnie normalizuje dane testowe":
        np.allclose(
            test_normalized,
            [0, 0.25, 0.5, 0.75, 1]
        ),

    "Funkcja obsluguje stale wartosci":
        np.allclose(
            constant_normalized,
            [0, 0, 0]
        ),

    "Funkcja zachowuje NaN":
        nan_normalized.isna().equals(
            nan_series.isna()
        ),

    "Funkcja poprawnie normalizuje dane z NaN":
        np.allclose(
            nan_normalized,
            [0, np.nan, 0.5, 1],
            equal_nan=True
        ),

    "Ranking jest poprawnie posortowany":
        ranking["Srednia_przed"]
        .is_monotonic_decreasing,

    "Normalizacja globalna i grupowa roznia sie":
        not np.allclose(
            df["MedInc_norm"],
            global_normalized
        ),

    "Oryginalna kolumna MedInc jest niezmieniona":
        df["MedInc"].equals(
            df_original["MedInc"]
        ),

    "Istniejace kolumny pozostaly niezmienione":
        df[df_original.columns].equals(
            df_original
        )
}

for description, result in tests.items():
    print(f"Czy {description}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), (
    "Nie wszystkie testy zostaly zaliczone."
)

print("Wszystkie testy zakonczone pomyslnie.")
