# Lekcja 12 - Zadanie 7: Grupowanie i sortowanie

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Generator datasetu zgodny z materialem lekcji 12
def make_california_housing(n=5000, seed=42):
    """Generuje syntetyczny dataset California Housing."""

    rng = np.random.default_rng(seed)

    # Wspolrzedne geograficzne
    latitude = rng.uniform(32.5, 41.5, n)
    longitude = rng.uniform(-123.5, -114.5, n)

    # Dochody
    med_inc = rng.gamma(
        shape=2.0, scale=1.8, size=n
    ) + 0.5

    # Wiek domu
    house_age = rng.integers(1, 55, n)

    # Pokoje, sypialnie i populacja
    ave_rooms = rng.normal(5.5, 1.5, n).clip(1, 15)

    ave_bedrms = (
        ave_rooms * rng.uniform(0.15, 0.25, n)
    ).clip(0.5, 5)

    population = rng.integers(50, 5000, n)
    ave_occup = rng.normal(3.0, 0.8, n).clip(1, 10)

    # Wartosc domu w jednostkach 100 000 USD
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


# Generowanie danych
df_housing = make_california_housing()

# Kopia danych do weryfikacji
df_original = df_housing.copy()

print("=" * 75)
print("GRUPOWANIE I SORTOWANIE - CALIFORNIA HOUSING")
print("=" * 75)


section("DANE WEJSCIOWE")

print(f"Shape: {df_housing.shape}")
print(f"Liczba obserwacji: {len(df_housing)}")
print(f"Liczba kolumn: {len(df_housing.columns)}")
print(f"Liczba NaN: {df_housing.isna().sum().sum()}")
print("Seed: 42")


section("PIERWSZE 10 REKORDOW")

print(df_housing.head(10).to_string(index=False))


section("STATYSTYKI DATASETU")

print(df_housing.describe().round(2).to_string())


section("ZAKRES WSPOLRZEDNYCH GEOGRAFICZNYCH")

print(
    f"Latitude: {df_housing['Latitude'].min():.4f}"
    f" - {df_housing['Latitude'].max():.4f}"
)

print(
    f"Longitude: {df_housing['Longitude'].min():.4f}"
    f" - {df_housing['Longitude'].max():.4f}"
)


# Podzial szerokosci geograficznej na 4 przedzialy
df_housing["lat_bin"] = pd.cut(
    df_housing["Latitude"],
    bins=4
)

# Podzial dlugosci geograficznej na 4 przedzialy
df_housing["lon_bin"] = pd.cut(
    df_housing["Longitude"],
    bins=4
)

# Polaczenie przedzialow w etykiete regionu
df_housing["region"] = (
    df_housing["lat_bin"].astype(str)
    + " | "
    + df_housing["lon_bin"].astype(str)
)


section("PRZEDZIALY LATITUDE")

for number, interval in enumerate(
    df_housing["lat_bin"].cat.categories, start=1
):
    print(f"{number}. {interval}")


section("PRZEDZIALY LONGITUDE")

for number, interval in enumerate(
    df_housing["lon_bin"].cat.categories, start=1
):
    print(f"{number}. {interval}")


section("PIERWSZE 10 REKORDOW Z REGIONAMI")

print(
    df_housing[
        ["Latitude", "Longitude", "region", "MedHouseVal"]
    ].head(10).to_string(index=False)
)


section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df_housing.shape}")

print(
    "Dodane kolumny:",
    df_housing.columns.difference(
        df_original.columns
    ).tolist()
)


# Podstawowe grupowanie
region_means = (
    df_housing.groupby("region")["MedHouseVal"]
    .mean()
)

section("SREDNIA WARTOSC DOMOW W REGIONACH")

print(region_means.round(4).to_string())


# Sortowanie malejaco
region_ranking = region_means.sort_values(
    ascending=False
)

section("RANKING WSZYSTKICH REGIONOW")

print(region_ranking.round(4).to_string())


# Wybor 5 najdrozszych regionow
top5 = region_ranking.head(5)

top5_table = top5.rename(
    "Srednia_wartosc"
).reset_index()

top5_table.insert(
    0, "Miejsce", range(1, len(top5_table) + 1)
)

# Przeliczenie jednostek na USD
top5_table["Srednia_USD"] = (
    top5_table["Srednia_wartosc"] * 100_000
)


section("TOP 5 REGIONOW Z NAJWYZSZA SREDNIA")

print(
    top5_table.round({
        "Srednia_wartosc": 4,
        "Srednia_USD": 2
    }).to_string(index=False)
)


# Rozszerzona analiza regionalna
region_stats = (
    df_housing.groupby("region")
    .agg(
        Liczba_obserwacji=("MedHouseVal", "size"),
        Minimum=("MedHouseVal", "min"),
        Maksimum=("MedHouseVal", "max"),
        Srednia=("MedHouseVal", "mean"),
        Mediana=("MedHouseVal", "median"),
        Odchylenie_std=("MedHouseVal", "std"),
        Sredni_dochod=("MedInc", "mean"),
        Populacja=("Population", "sum")
    )
    .sort_values("Srednia", ascending=False)
)

region_stats["Srednia_USD"] = (
    region_stats["Srednia"] * 100_000
)


section("SZCZEGOLOWE STATYSTYKI REGIONALNE")

print(region_stats.round(2).to_string())


# Tabela liczebnosci regionow 4 x 4
grid_counts = (
    df_housing.groupby(
        ["lat_bin", "lon_bin"],
        observed=False
    )
    .size()
    .unstack(fill_value=0)
)

section("SIATKA 4 X 4 - LICZBA OBSERWACJI")

print(grid_counts.iloc[::-1].to_string())


# Tabela srednich wartosci 4 x 4
grid_means = (
    df_housing.groupby(
        ["lat_bin", "lon_bin"],
        observed=False
    )["MedHouseVal"]
    .mean()
    .unstack()
)

section("SIATKA 4 X 4 - SREDNIA WARTOSC DOMOW")

print(grid_means.iloc[::-1].round(4).to_string())


section("TEKSTOWY WYKRES TOP 5")

print("Legenda: jeden znak = okolo 10 000 USD\n")

for row in top5_table.itertuples(index=False):
    bar = "█" * int(round(row.Srednia_USD / 10_000))

    print(f"Miejsce {row.Miejsce}: {row.region}")
    print(f"  {bar} {row.Srednia_USD:,.2f} USD")


section("POROWNANIE WSZYSTKICH REGIONOW")

print("Legenda: jeden znak = okolo 10 000 USD\n")

for number, (region, value) in enumerate(
    region_ranking.items(), start=1
):
    usd = value * 100_000
    bar = "█" * int(round(usd / 10_000))

    print(f"{number:2d}. {region}")
    print(f"    {bar:<50} {usd:,.2f} USD")


# Porownanie najlepszego i najtanszego regionu
best_region = region_ranking.idxmax()
worst_region = region_ranking.idxmin()

best_value = region_ranking.max()
worst_value = region_ranking.min()

global_mean = df_housing["MedHouseVal"].mean()

difference = best_value - worst_value
ratio = best_value / worst_value

section("POROWNANIE NAJDROZSZEGO I NAJTANSZEGO REGIONU")

print(f"Najdrozszy region: {best_region}")
print(f"Srednia: {best_value * 100_000:,.2f} USD")

print(f"\nNajtanszy region: {worst_region}")
print(f"Srednia: {worst_value * 100_000:,.2f} USD")

print(f"\nRoznica: {difference * 100_000:,.2f} USD")
print(f"Stosunek srednich: {ratio:.2f}x")
print(f"Srednia globalna: {global_mean * 100_000:,.2f} USD")


# Porownanie sredniej globalnej i wazonej
weighted_mean = np.average(
    region_stats["Srednia"],
    weights=region_stats["Liczba_obserwacji"]
)

section("WERYFIKACJA SREDNIEJ WAZONEJ")

print(f"Srednia globalna: {global_mean:.6f}")
print(f"Srednia wazona regionow: {weighted_mean:.6f}")


section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum() / 1024
)

memory_after = (
    df_housing.memory_usage(deep=True).sum() / 1024
)

print(f"Przed: {memory_before:.2f} KiB")
print(f"Po: {memory_after:.2f} KiB")
print(f"Wzrost: {memory_after - memory_before:.2f} KiB")


section("WNIOSKI")

conclusions = [
    "Pd.cut dzieli dane liczbowe na przedzialy.",
    "Podzial Latitude i Longitude tworzy siatke 4 x 4.",
    "Polaczenie przedzialow pozwala utworzyc region.",
    "GroupBy grupuje obserwacje wedlug regionu.",
    "Mean oblicza srednia wartosc domow w grupie.",
    "Sort_values pozwala uporzadkowac wyniki.",
    "Ascending=False oznacza sortowanie malejace.",
    "Head(5) wybiera piec najwyzszych wynikow.",
    "Agregacja zmniejsza liczbe analizowanych rekordow.",
    "MedHouseVal wyrazono w jednostkach 100 000 USD.",
    "Dane sa syntetyczne, a nie rzeczywiste.",
    "Generator uwzglednia wplyw Latitude na wartosc domu.",
    "Siatka jest prostokatna i nie odwzorowuje granic stanu.",
    "Wyniki nie opisuja rzeczywistego rynku nieruchomosci."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba obserwacji: {len(df_housing)}")
print(f"Liczba regionow: {len(region_means)}")
print(f"Liczba regionow TOP: {len(top5)}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df_housing.shape}")
print(f"Najdrozszy region: {best_region}")
print(f"Najwyzsza srednia: {best_value * 100_000:,.2f} USD")
print(f"Srednia globalna: {global_mean * 100_000:,.2f} USD")


# Automatyczna weryfikacja wynikow
section("WERYFIKACJA")

manual_means = pd.Series({
    region: df_housing.loc[
        df_housing["region"] == region,
        "MedHouseVal"
    ].mean()
    for region in region_means.index
})

expected_top5 = region_means.nlargest(5)

tests = {
    "Dataset ma 5000 wierszy":
        len(df_original) == 5000,

    "Dataset ma poczatkowo 9 kolumn":
        df_original.shape == (5000, 9),

    "Generator jest powtarzalny":
        df_original.equals(make_california_housing()),

    "Dataset nie zawiera NaN":
        not df_original.isna().any().any(),

    "Latitude miesci sie w zakresie":
        df_housing["Latitude"].between(32.5, 41.5).all(),

    "Longitude miesci sie w zakresie":
        df_housing["Longitude"].between(
            -123.5, -114.5
        ).all(),

    "MedHouseVal miesci sie w zakresie":
        df_housing["MedHouseVal"].between(
            0.15, 5.0
        ).all(),

    "Utworzono 4 przedzialy Latitude":
        len(df_housing["lat_bin"].cat.categories) == 4,

    "Utworzono 4 przedzialy Longitude":
        len(df_housing["lon_bin"].cat.categories) == 4,

    "Latitude nie zawiera brakujacych kategorii":
        df_housing["lat_bin"].notna().all(),

    "Longitude nie zawiera brakujacych kategorii":
        df_housing["lon_bin"].notna().all(),

    "Utworzono kolumne region":
        "region" in df_housing.columns,

    "Utworzono 16 regionow":
        df_housing["region"].nunique() == 16,

    "Agregacja zwraca 16 srednich":
        len(region_means) == 16,

    "Wynik ma shape (5000, 12)":
        df_housing.shape == (5000, 12),

    "Srednie regionow nie zawieraja NaN":
        region_means.notna().all(),

    "Srednie regionow obliczono poprawnie":
        np.allclose(
            region_means.sort_index(),
            manual_means.sort_index()
        ),

    "Ranking jest posortowany malejaco":
        region_ranking.is_monotonic_decreasing,

    "TOP 5 zawiera piec regionow":
        len(top5) == 5,

    "TOP 5 jest zgodne z nlargest":
        top5.equals(expected_top5),

    "TOP 5 ma poprawne miejsca":
        top5_table["Miejsce"].tolist() == [1, 2, 3, 4, 5],

    "Przeliczenie na USD jest poprawne":
        np.allclose(
            top5_table["Srednia_USD"],
            top5_table["Srednia_wartosc"] * 100_000
        ),

    "Uwzgledniono wszystkie obserwacje":
        region_stats["Liczba_obserwacji"].sum() == 5000,

    "Siatka liczebnosci ma shape (4, 4)":
        grid_counts.shape == (4, 4),

    "Siatka srednich ma shape (4, 4)":
        grid_means.shape == (4, 4),

    "Siatka uwzglednia wszystkie obserwacje":
        grid_counts.to_numpy().sum() == 5000,

    "Najdrozszy region ma najwyzsza srednia":
        np.isclose(top5.iloc[0], region_means.max()),

    "Srednia wazona jest poprawna":
        np.isclose(weighted_mean, global_mean),

    "Zachowano wszystkie indeksy":
        df_housing.index.equals(df_original.index),

    "Istniejace kolumny pozostaly niezmienione":
        df_housing[df_original.columns].equals(df_original)
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())
total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")

if all(tests.values()):
    print("Wszystkie testy zakonczone pomyslnie.")
else:
    raise AssertionError("Nie wszystkie testy zostaly zaliczone.")
