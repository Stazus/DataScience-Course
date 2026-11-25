# Lekcja 12 - Zadanie 10: Custom funkcja agregujaca

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Generator datasetu zgodny z zadaniem 7
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


# Wlasna funkcja agregujaca
def iqr_func(x):
    """Oblicza rozstep miedzykwartylowy."""

    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)

    return q3 - q1


# Generowanie danych
df_housing = make_california_housing()

# Kopia danych do weryfikacji
df_original = df_housing.copy()

print("=" * 75)
print("CUSTOM FUNKCJA AGREGUJACA - CALIFORNIA HOUSING")
print("=" * 75)


section("DANE WEJSCIOWE")

print(f"Shape: {df_housing.shape}")
print(f"Liczba obserwacji: {len(df_housing)}")
print(f"Liczba kolumn: {len(df_housing.columns)}")
print(f"Liczba NaN: {df_housing.isna().sum().sum()}")
print("Seed: 42")
print("Jednostka MedHouseVal: 100 000 USD")


section("PIERWSZE 10 REKORDOW")

print(
    df_housing.head(10).to_string(index=False)
)


section("STATYSTYKI GLOBALNE MEDHOUSEVAL")

print(
    df_housing["MedHouseVal"]
    .describe()
    .round(4)
    .to_string()
)


# Podzial geograficzny na 16 regionow
df_housing["lat_bin"] = pd.cut(
    df_housing["Latitude"],
    bins=4
)

df_housing["lon_bin"] = pd.cut(
    df_housing["Longitude"],
    bins=4
)

df_housing["Region"] = (
    df_housing["lat_bin"].astype(str)
    + " | "
    + df_housing["lon_bin"].astype(str)
)


section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df_housing.shape}")
print(f"Liczba regionow: {df_housing['Region'].nunique()}")

print(
    "Dodane kolumny:",
    df_housing.columns.difference(
        df_original.columns
    ).tolist()
)


section("LICZEBNOSC REGIONOW")

region_counts = (
    df_housing["Region"]
    .value_counts()
    .sort_index()
)

print(region_counts.to_string())


# Globalny rozstep miedzykwartylowy
global_q1 = df_housing["MedHouseVal"].quantile(0.25)
global_q3 = df_housing["MedHouseVal"].quantile(0.75)

global_iqr = iqr_func(df_housing["MedHouseVal"])


section("GLOBALNY ROZSTEP MIEDZYKWARTYLOWY")

print(f"Q1: {global_q1:.4f}")
print(f"Q3: {global_q3:.4f}")
print(f"IQR: {global_iqr:.4f}")
print(f"IQR w USD: {global_iqr * 100000:,.2f}")


# Glowna agregacja wymagana w zadaniu
iqr_results = (
    df_housing.groupby("Region")["MedHouseVal"]
    .agg(iqr_func)
    .rename("IQR")
)


section("IQR WEDLUG REGIONU - CUSTOM AGG")

print(
    iqr_results.round(4).to_string()
)


# Czytelna tabela wynikowa
results = (
    iqr_results
    .reset_index()
    .sort_values("IQR", ascending=False)
    .reset_index(drop=True)
)


section("TABELA WYNIKOWA IQR")

print(
    results.round(4).to_string(index=False)
)


# Rozbudowana agregacja
regional_stats = (
    df_housing.groupby("Region")["MedHouseVal"]
    .agg(
        Liczba_obserwacji="size",
        Minimum="min",
        Q1=lambda x: x.quantile(0.25),
        Mediana="median",
        Q3=lambda x: x.quantile(0.75),
        Maksimum="max",
        Srednia="mean",
        Odchylenie_std="std",
        IQR=iqr_func
    )
)

regional_stats["Rozstep"] = (
    regional_stats["Maksimum"]
    - regional_stats["Minimum"]
)

regional_stats["IQR_USD"] = (
    regional_stats["IQR"] * 100000
)


section("SZCZEGOLOWE STATYSTYKI REGIONALNE")

print(
    regional_stats.round(4).to_string()
)


section("POROWNANIE KWARTYLI I IQR")

print(
    regional_stats[
        ["Q1", "Mediana", "Q3", "IQR", "IQR_USD"]
    ].round(4).to_string()
)


# Ranking regionow
ranking = (
    regional_stats
    .sort_values("IQR", ascending=False)
)


section("RANKING REGIONOW WEDLUG IQR")

print(
    ranking[
        [
            "Liczba_obserwacji",
            "Q1",
            "Q3",
            "IQR",
            "IQR_USD"
        ]
    ].round(4).to_string()
)


section("TOP 5 REGIONOW Z NAJWIEKSZYM IQR")

print(
    ranking[
        ["IQR", "IQR_USD"]
    ].head(5).round(4).to_string()
)


section("TOP 5 REGIONOW Z NAJMNIEJSZYM IQR")

print(
    ranking[
        ["IQR", "IQR_USD"]
    ].tail(5).sort_values("IQR")
    .round(4).to_string()
)


# Identyfikacja regionow
max_region = iqr_results.idxmax()
min_region = iqr_results.idxmin()

max_iqr = iqr_results.max()
min_iqr = iqr_results.min()

iqr_difference = max_iqr - min_iqr

iqr_ratio = (
    max_iqr / min_iqr
    if min_iqr > 0
    else np.nan
)


section("POROWNANIE REGIONOW")

print(f"Region z najwiekszym IQR: {max_region}")
print(f"Najwiekszy IQR: {max_iqr:.4f}")
print(f"Najwiekszy IQR w USD: {max_iqr * 100000:,.2f}")

print()

print(f"Region z najmniejszym IQR: {min_region}")
print(f"Najmniejszy IQR: {min_iqr:.4f}")
print(f"Najmniejszy IQR w USD: {min_iqr * 100000:,.2f}")

print()

print(f"Roznica IQR: {iqr_difference:.4f}")
print(f"Stosunek IQR: {iqr_ratio:.2f}x")
print(f"Sredni regionalny IQR: {iqr_results.mean():.4f}")
print(f"Mediana regionalnego IQR: {iqr_results.median():.4f}")


section("TEKSTOWY WYKRES IQR")

print("Legenda: jeden znak = okolo 0.05 jednostki")
print("Jednostka 0.05 odpowiada 5000 USD.\n")

for region, value in iqr_results.sort_values(
    ascending=False
).items():

    bar = "█" * int(round(value / 0.05))

    print(
        f"{region:<45} | "
        f"{bar:<65} {value:.4f}"
    )


section("POROWNANIE IQR I ODCHYLENIA STANDARDOWEGO")

comparison = regional_stats[
    ["IQR", "Odchylenie_std", "Rozstep"]
].copy()

comparison["IQR_do_std"] = (
    comparison["IQR"]
    / comparison["Odchylenie_std"].replace(0, np.nan)
)

print(
    comparison.round(4).to_string()
)


# Korelacja pomiedzy miarami rozproszenia
correlation = comparison[
    ["IQR", "Odchylenie_std", "Rozstep"]
].corr()


section("KORELACJA MIAR ROZPROSZENIA")

print(
    correlation.round(4).to_string()
)


# Porownanie regionalnego IQR z globalnym
comparison_global = iqr_results.to_frame()

comparison_global["Globalny_IQR"] = global_iqr

comparison_global["Roznica"] = (
    comparison_global["IQR"] - global_iqr
)

comparison_global["Roznica_%"] = (
    comparison_global["Roznica"]
    / global_iqr * 100
)

comparison_global["Pozycja"] = np.select(
    [
        comparison_global["IQR"] > global_iqr,
        comparison_global["IQR"] < global_iqr
    ],
    [
        "Powyzej globalnego IQR",
        "Ponizej globalnego IQR"
    ],
    default="Rowny globalnemu IQR"
)


section("REGIONALNY IQR A GLOBALNY IQR")

print(
    comparison_global.round(4).to_string()
)


section("LICZBA REGIONOW WZGLEDEM GLOBALNEGO IQR")

print(
    comparison_global["Pozycja"]
    .value_counts()
    .to_string()
)


# Niezalezna metoda obliczania IQR
quantiles = (
    df_housing.groupby("Region")["MedHouseVal"]
    .quantile([0.25, 0.75])
    .unstack()
)

iqr_alternative = (
    quantiles[0.75] - quantiles[0.25]
)


section("POROWNANIE DWÓCH METOD OBLICZANIA IQR")

method_comparison = pd.DataFrame({
    "Custom_agg": iqr_results,
    "Quantile": iqr_alternative
})

method_comparison["Roznica"] = (
    method_comparison["Custom_agg"]
    - method_comparison["Quantile"]
)

print(
    method_comparison.round(6).to_string()
)


section("TEST ODPORNOSCI IQR NA OUTLIERS")

sample = pd.Series([1, 2, 3, 4, 5])
sample_outlier = pd.Series([1, 2, 3, 4, 100])

robustness = pd.DataFrame({
    "Dane_standardowe": [
        sample.min(),
        sample.max(),
        sample.mean(),
        sample.std(),
        iqr_func(sample)
    ],
    "Dane_z_outlierem": [
        sample_outlier.min(),
        sample_outlier.max(),
        sample_outlier.mean(),
        sample_outlier.std(),
        iqr_func(sample_outlier)
    ]
}, index=[
    "Minimum",
    "Maksimum",
    "Srednia",
    "Odchylenie_std",
    "IQR"
])

print(
    robustness.round(4).to_string()
)

print(
    "\nIQR w tym przykladzie pozostaje niezmieniony "
    "pomimo wystapienia wartosci odstajacej."
)


section("TESTY FUNKCJI IQR_FUNC")

test_samples = {
    "Dane standardowe": pd.Series([1, 2, 3, 4, 5]),
    "Dane stale": pd.Series([7, 7, 7, 7, 7]),
    "Jedna obserwacja": pd.Series([10]),
    "Dane z NaN": pd.Series([1, 2, 3, 4, 5, np.nan]),
    "Dane ujemne": pd.Series([-5, -4, -3, -2, -1]),
    "Dane z outlierem": pd.Series([1, 2, 3, 4, 100])
}

for name, values in test_samples.items():
    print(f"{name:<25} IQR: {iqr_func(values):.4f}")


section("WNIOSKI")

conclusions = [
    "IQR jest roznica pomiedzy trzecim i pierwszym kwartylem.",
    "IQR opisuje rozproszenie srodkowych 50% obserwacji.",
    "Agg pozwala stosowac wlasne funkcje agregujace.",
    "Funkcja iqr_func zostala zastosowana osobno do kazdego regionu.",
    "Wiekszy IQR oznacza wieksze zroznicowanie srodkowych 50% cen.",
    "Mniejszy IQR oznacza mniejsze zroznicowanie centralnej czesci danych.",
    "IQR jest bardziej odporny na outliers niz odchylenie standardowe.",
    "IQR nie jest tym samym co rozstep maksimum minus minimum.",
    "Najwiekszy IQR nie oznacza najwyzszej sredniej ceny domu.",
    "IQR moze byc wykorzystywany do detekcji wartosci odstajacych.",
    "Globalny IQR nie musi byc srednia regionalnych IQR.",
    "Dane sa syntetyczne i nie opisuja rzeczywistego rynku nieruchomosci."
]

for number, conclusion in enumerate(
    conclusions, start=1
):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba obserwacji: {len(df_housing)}")
print(f"Liczba regionow: {len(iqr_results)}")
print("Funkcja agregujaca: iqr_func")
print("Metoda: groupby + agg")
print(f"Globalny IQR: {global_iqr:.4f}")
print(f"Najwiekszy regionalny IQR: {max_iqr:.4f}")
print(f"Najmniejszy regionalny IQR: {min_iqr:.4f}")
print(f"Roznica IQR: {iqr_difference:.4f}")
print(f"Shape tabeli wynikowej: {results.shape}")


# Automatyczna weryfikacja
tests = {
    "Dataset ma 5000 wierszy":
        len(df_housing) == 5000,

    "Dataset ma poczatkowo 9 kolumn":
        df_original.shape == (5000, 9),

    "Generator jest powtarzalny":
        df_original.equals(make_california_housing()),

    "Dataset nie zawiera NaN":
        not df_housing.isna().any().any(),

    "Utworzono kolumne Region":
        "Region" in df_housing.columns,

    "Utworzono 4 przedzialy Latitude":
        df_housing["lat_bin"].nunique() == 4,

    "Utworzono 4 przedzialy Longitude":
        df_housing["lon_bin"].nunique() == 4,

    "Utworzono 16 regionow":
        df_housing["Region"].nunique() == 16,

    "Uwzgledniono wszystkie obserwacje":
        region_counts.sum() == 5000,

    "Funkcja iqr_func jest wywolywalna":
        callable(iqr_func),

    "Funkcja poprawnie oblicza IQR":
        np.isclose(
            iqr_func(pd.Series([1, 2, 3, 4, 5])),
            2.0
        ),

    "IQR danych stalych wynosi zero":
        np.isclose(
            iqr_func(pd.Series([7, 7, 7])),
            0.0
        ),

    "IQR jednej obserwacji wynosi zero":
        np.isclose(
            iqr_func(pd.Series([10])),
            0.0
        ),

    "Funkcja pomija NaN":
        np.isclose(
            iqr_func(pd.Series([1, 2, 3, 4, 5, np.nan])),
            2.0
        ),

    "Funkcja obsluguje wartosci ujemne":
        np.isclose(
            iqr_func(pd.Series([-5, -4, -3, -2, -1])),
            2.0
        ),

    "Globalny IQR jest poprawny":
        np.isclose(global_iqr, global_q3 - global_q1),

    "Obliczono IQR dla 16 regionow":
        len(iqr_results) == 16,

    "Wyniki IQR nie zawieraja NaN":
        not iqr_results.isna().any(),

    "Wszystkie IQR sa nieujemne":
        (iqr_results >= 0).all(),

    "Tabela wynikowa ma shape (16, 2)":
        results.shape == (16, 2),

    "Q1 nie przekracza mediany":
        (
            regional_stats["Q1"]
            <= regional_stats["Mediana"]
        ).all(),

    "Mediana nie przekracza Q3":
        (
            regional_stats["Mediana"]
            <= regional_stats["Q3"]
        ).all(),

    "IQR jest zgodny z Q3 minus Q1":
        np.allclose(
            regional_stats["IQR"],
            regional_stats["Q3"] - regional_stats["Q1"]
        ),

    "IQR nie przekracza rozstepu":
        (
            regional_stats["IQR"]
            <= regional_stats["Rozstep"] + 1e-10
        ).all(),

    "Custom agg i quantile sa zgodne":
        np.allclose(
            iqr_results.sort_index(),
            iqr_alternative.sort_index()
        ),

    "Szczegolowa agregacja jest poprawna":
        np.allclose(
            regional_stats["IQR"].sort_index(),
            iqr_results.sort_index()
        ),

    "Ranking jest poprawnie posortowany":
        ranking["IQR"].is_monotonic_decreasing,

    "Najwiekszy IQR jest poprawny":
        np.isclose(
            ranking["IQR"].iloc[0],
            max_iqr
        ),

    "Najmniejszy IQR jest poprawny":
        np.isclose(
            ranking["IQR"].iloc[-1],
            min_iqr
        ),

    "Przeliczenie IQR na USD jest poprawne":
        np.allclose(
            regional_stats["IQR_USD"],
            regional_stats["IQR"] * 100000
        ),

    "IQR odporny na outlier w przykladzie":
        np.isclose(
            iqr_func(sample),
            iqr_func(sample_outlier)
        ),

    "Odchylenie wzroslo po dodaniu outliera":
        sample_outlier.std() > sample.std(),

    "Zachowano oryginalne indeksy":
        df_housing.index.equals(df_original.index),

    "Istniejace kolumny pozostaly niezmienione":
        df_housing[df_original.columns].equals(
            df_original
        )
}


section("WERYFIKACJA")

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())
total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")

if passed == total:
    print("Wszystkie testy zakonczone pomyslnie.")
else:
    raise AssertionError(
        "Nie wszystkie testy zostaly zaliczone."
    )
