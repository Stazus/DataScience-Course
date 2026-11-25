# Lekcja 12 - Zadanie 12: Wykrywanie Outliers Grupowo

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


def make_california_housing(n=5000, seed=42):
    """Generuje syntetyczny dataset California Housing."""

    rng = np.random.default_rng(seed)

    latitude = rng.uniform(32.5, 41.5, n)
    longitude = rng.uniform(-123.5, -114.5, n)

    med_inc = rng.gamma(
        shape=2.0, scale=1.8, size=n
    ) + 0.5

    house_age = rng.integers(1, 55, n)

    ave_rooms = rng.normal(5.5, 1.5, n).clip(1, 15)

    ave_bedrms = (
        ave_rooms * rng.uniform(0.15, 0.25, n)
    ).clip(0.5, 5)

    population = rng.integers(50, 5000, n)
    ave_occup = rng.normal(3.0, 0.8, n).clip(1, 10)

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


def iqr_func(x):
    """Oblicza rozstep miedzykwartylowy."""
    return x.quantile(0.75) - x.quantile(0.25)


def text_boxplot(values, scale_min, scale_max, width=55):
    """Tworzy tekstowy boxplot pieciopunktowy."""

    points = np.array([
        values.min(),
        values.quantile(0.25),
        values.median(),
        values.quantile(0.75),
        values.max()
    ])

    if scale_max == scale_min:
        positions = np.zeros(5, dtype=int)
    else:
        positions = np.rint(
            (points - scale_min)
            / (scale_max - scale_min)
            * (width - 1)
        ).astype(int)

    positions = np.clip(positions, 0, width - 1)

    p_min, p_q1, p_med, p_q3, p_max = positions

    chars = [" "] * width

    for i in range(p_min, p_max + 1):
        chars[i] = "-"

    for i in range(p_q1, p_q3 + 1):
        chars[i] = "█"

    chars[p_min] = "|"
    chars[p_max] = "|"
    chars[p_q1] = "["
    chars[p_q3] = "]"
    chars[p_med] = "│"

    return "".join(chars)


# Generowanie datasetu
df_housing = make_california_housing()

# Kopia oryginalnych danych
df_original = df_housing.copy(deep=True)

print("=" * 75)
print("WYKRYWANIE OUTLIERS GRUPOWO - CALIFORNIA HOUSING")
print("=" * 75)


section("DANE WEJSCIOWE")

print(f"Shape: {df_housing.shape}")
print(f"Liczba obserwacji: {len(df_housing)}")
print(f"Liczba kolumn: {len(df_housing.columns)}")
print(f"Liczba NaN: {df_housing.isna().sum().sum()}")
print("Seed: 42")


section("PIERWSZE 10 REKORDOW")

print(df_housing.head(10).to_string(index=False))


section("STATYSTYKI MEDHOUSEVAL")

print(
    df_housing["MedHouseVal"]
    .describe()
    .round(4)
    .to_string()
)


# Podzial geograficzny na siatke 4 x 4
df_housing["lat_bin"] = pd.cut(
    df_housing["Latitude"],
    bins=4
)

df_housing["lon_bin"] = pd.cut(
    df_housing["Longitude"],
    bins=4
)

# Numery regionow od R01 do R16
lat_codes = df_housing["lat_bin"].cat.codes
lon_codes = df_housing["lon_bin"].cat.codes

region_numbers = lat_codes * 4 + lon_codes + 1

df_housing["Region"] = region_numbers.map(
    lambda x: f"R{x:02d}"
)


section("DEFINICJA REGIONOW")

region_definition = (
    df_housing[
        ["Region", "lat_bin", "lon_bin"]
    ]
    .drop_duplicates()
    .sort_values("Region")
)

print(region_definition.to_string(index=False))


section("LICZEBNOSC REGIONOW")

print(
    df_housing["Region"]
    .value_counts()
    .sort_index()
    .to_string()
)

print(
    f"\nLiczba regionow: "
    f"{df_housing['Region'].nunique()}"
)


# Grupowanie wedlug regionu
grouped = df_housing.groupby("Region")["MedHouseVal"]

# Kwartyle osobno dla kazdego regionu
df_housing["Q1"] = grouped.transform(
    lambda x: x.quantile(0.25)
)

df_housing["Q3"] = grouped.transform(
    lambda x: x.quantile(0.75)
)

# Rozstep miedzykwartylowy
df_housing["IQR"] = (
    df_housing["Q3"] - df_housing["Q1"]
)

# Granice IQR
df_housing["Lower_Bound"] = (
    df_housing["Q1"] - 1.5 * df_housing["IQR"]
)

df_housing["Upper_Bound"] = (
    df_housing["Q3"] + 1.5 * df_housing["IQR"]
)

# Wykrywanie wartosci odstajacych
df_housing["Is_Lower_Outlier"] = (
    df_housing["MedHouseVal"]
    < df_housing["Lower_Bound"]
)

df_housing["Is_Upper_Outlier"] = (
    df_housing["MedHouseVal"]
    > df_housing["Upper_Bound"]
)

df_housing["Is_Outlier"] = (
    df_housing["Is_Lower_Outlier"]
    | df_housing["Is_Upper_Outlier"]
)


section("PIERWSZE 10 REKORDOW PO DETEKCJI")

columns = [
    "Region",
    "MedHouseVal",
    "Q1",
    "Q3",
    "IQR",
    "Lower_Bound",
    "Upper_Bound",
    "Is_Outlier"
]

print(
    df_housing[columns]
    .head(10)
    .round(4)
    .to_string(index=False)
)


section("KWARTYLE I GRANICE IQR WEDLUG REGIONU")

regional_bounds = (
    df_housing.groupby("Region")
    .agg(
        Q1=("Q1", "first"),
        Q3=("Q3", "first"),
        IQR=("IQR", "first"),
        Lower_Bound=("Lower_Bound", "first"),
        Upper_Bound=("Upper_Bound", "first")
    )
)

print(regional_bounds.round(4).to_string())


# Podsumowanie outliers wedlug regionu
results = (
    df_housing.groupby("Region")
    .agg(
        Liczba_obserwacji=("MedHouseVal", "size"),
        Outliers=("Is_Outlier", "sum"),
        Dolne_outliers=("Is_Lower_Outlier", "sum"),
        Gorne_outliers=("Is_Upper_Outlier", "sum")
    )
)

results["Typowe_wartosci"] = (
    results["Liczba_obserwacji"]
    - results["Outliers"]
)

results["Outliers_%"] = (
    results["Outliers"]
    / results["Liczba_obserwacji"]
    * 100
)


section("LICZBA OUTLIERS WEDLUG REGIONU")

print(results.round(2).to_string())


# Statystyki pieciopunktowe
five_number_summary = grouped.agg(
    Minimum="min",
    Q1=lambda x: x.quantile(0.25),
    Mediana="median",
    Q3=lambda x: x.quantile(0.75),
    Maksimum="max"
)

five_number_summary["IQR"] = grouped.agg(iqr_func)


section("STATYSTYKI PIECIOPUNKTOWE")

print(
    five_number_summary
    .round(4)
    .to_string()
)


section("TEKSTOWE BOXPLOTY WEDLUG REGIONU")

scale_min = df_housing["MedHouseVal"].min()
scale_max = df_housing["MedHouseVal"].max()

print("Legenda:")
print("| = minimum lub maksimum")
print("[ = Q1")
print("] = Q3")
print("│ = mediana")
print("█ = obszar miedzy Q1 i Q3")
print("- = zakres poza kwartylami")
print("Znaki moga sie nakladac przy ograniczonej szerokosci.")
print(
    f"\nWspolna skala: "
    f"{scale_min:.2f} - {scale_max:.2f}"
)

print()

for region, values in grouped:
    plot = text_boxplot(
        values,
        scale_min,
        scale_max
    )

    outlier_count = int(
        results.loc[region, "Outliers"]
    )

    print(
        f"{region} |{plot}| "
        f"Outliers: {outlier_count}"
    )

print(
    "\nUwaga: boxplot przedstawia min/Q1/med/Q3/max."
)
print(
    "Minimum i maksimum nie sa granicami detekcji IQR."
)


section("SZCZEGOLOWE WARTOSCI BOXPLOTOW")

for region, row in five_number_summary.iterrows():
    print(
        f"{region}: "
        f"min={row['Minimum']:.4f}, "
        f"Q1={row['Q1']:.4f}, "
        f"med={row['Mediana']:.4f}, "
        f"Q3={row['Q3']:.4f}, "
        f"max={row['Maksimum']:.4f}"
    )


section("TEKSTOWY WYKRES LICZBY OUTLIERS")

print("Legenda: jeden znak = jeden outlier\n")

max_outliers = int(results["Outliers"].max())

for region, row in results.iterrows():
    count = int(row["Outliers"])
    bar = "█" * count

    print(
        f"{region} | "
        f"{bar:<{max_outliers}} "
        f"{count:3d}"
    )


section("TEKSTOWY WYKRES PROCENTU OUTLIERS")

print("Legenda: jeden znak = okolo 1 p.p.\n")

for region, row in results.iterrows():
    percentage = row["Outliers_%"]
    bar = "█" * int(round(percentage))

    print(
        f"{region} | "
        f"{bar:<20} "
        f"{percentage:.2f}%"
    )


section("PRZYKLADOWE WARTOSCI ODSTAJACE")

outliers = df_housing.loc[
    df_housing["Is_Outlier"]
].copy()

outliers["Odleglosc_od_granicy"] = np.where(
    outliers["Is_Lower_Outlier"],
    outliers["Lower_Bound"]
    - outliers["MedHouseVal"],
    outliers["MedHouseVal"]
    - outliers["Upper_Bound"]
)

outliers = outliers.sort_values(
    "Odleglosc_od_granicy",
    ascending=False
)

outlier_columns = [
    "Region",
    "MedHouseVal",
    "Lower_Bound",
    "Upper_Bound",
    "Odleglosc_od_granicy"
]

if outliers.empty:
    print("Nie wykryto wartosci odstajacych.")
else:
    print(
        outliers[outlier_columns]
        .head(15)
        .round(4)
        .to_string(index=False)
    )


section("RANKING REGIONOW WEDLUG LICZBY OUTLIERS")

ranking = results.sort_values(
    ["Outliers", "Outliers_%"],
    ascending=False
)

print(ranking.round(2).to_string())


section("RANKING REGIONOW WEDLUG PROCENTU OUTLIERS")

percentage_ranking = results.sort_values(
    "Outliers_%",
    ascending=False
)

print(percentage_ranking.round(2).to_string())


# Globalna metoda IQR
global_q1 = df_housing["MedHouseVal"].quantile(0.25)
global_q3 = df_housing["MedHouseVal"].quantile(0.75)

global_iqr = global_q3 - global_q1

global_lower = global_q1 - 1.5 * global_iqr
global_upper = global_q3 + 1.5 * global_iqr

global_mask = (
    (df_housing["MedHouseVal"] < global_lower)
    | (df_housing["MedHouseVal"] > global_upper)
)

group_mask = df_housing["Is_Outlier"]


section("POROWNANIE DETEKCJI GLOBALNEJ I GRUPOWEJ")

print(f"Globalne Q1: {global_q1:.4f}")
print(f"Globalne Q3: {global_q3:.4f}")
print(f"Globalne IQR: {global_iqr:.4f}")
print(f"Globalna dolna granica: {global_lower:.4f}")
print(f"Globalna gorna granica: {global_upper:.4f}")

comparison = pd.DataFrame({
    "Metoda": ["Globalna", "Grupowa"],
    "Outliers": [
        int(global_mask.sum()),
        int(group_mask.sum())
    ]
})

comparison["Outliers_%"] = (
    comparison["Outliers"]
    / len(df_housing)
    * 100
)

print()
print(comparison.round(4).to_string(index=False))


section("ZGODNOSC METOD DETEKCJI")

both = int((global_mask & group_mask).sum())

only_global = int(
    (global_mask & ~group_mask).sum()
)

only_group = int(
    (~global_mask & group_mask).sum()
)

neither = int(
    (~global_mask & ~group_mask).sum()
)

agreement = pd.DataFrame({
    "Kategoria": [
        "Outlier w obu metodach",
        "Tylko metoda globalna",
        "Tylko metoda grupowa",
        "Brak outlier w obu metodach"
    ],
    "Liczba": [
        both,
        only_global,
        only_group,
        neither
    ]
})

print(agreement.to_string(index=False))


section("POROWNANIE REGIONOW")

total_outliers = int(group_mask.sum())

total_percentage = (
    total_outliers / len(df_housing) * 100
)

regions_with_outliers = int(
    (results["Outliers"] > 0).sum()
)

regions_without_outliers = int(
    (results["Outliers"] == 0).sum()
)

print(f"Laczna liczba outliers: {total_outliers}")
print(f"Procent outliers: {total_percentage:.2f}%")

print(
    f"Regiony z outliers: "
    f"{regions_with_outliers}"
)

print(
    f"Regiony bez outliers: "
    f"{regions_without_outliers}"
)

if total_outliers > 0:
    best_count = results["Outliers"].max()
    best_percentage = results["Outliers_%"].max()

    top_count_regions = results.index[
        results["Outliers"] == best_count
    ].tolist()

    top_percentage_regions = results.index[
        results["Outliers_%"] == best_percentage
    ].tolist()

    print(
        "Najwiecej outliers: "
        + ", ".join(top_count_regions)
        + f" - {int(best_count)}"
    )

    print(
        "Najwyzszy procent outliers: "
        + ", ".join(top_percentage_regions)
        + f" - {best_percentage:.2f}%"
    )
else:
    print("Zaden region nie zawiera outliers.")


section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df_housing.shape}")

print(
    "Dodane kolumny:",
    df_housing.columns.difference(
        df_original.columns
    ).tolist()
)


section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum()
    / 1024
)

memory_after = (
    df_housing.memory_usage(deep=True).sum()
    / 1024
)

print(f"Przed: {memory_before:.2f} KiB")
print(f"Po: {memory_after:.2f} KiB")
print(
    f"Wzrost: "
    f"{memory_after - memory_before:.2f} KiB"
)


section("WNIOSKI")

conclusions = [
    "IQR pozwala wykrywac potencjalne wartosci odstajace.",
    "Kwartyle obliczono osobno dla kazdego regionu.",
    "Transform zachowuje indeksy i liczbe obserwacji.",
    "Kazdy region posiada wlasne granice IQR.",
    "Detekcja grupowa uwzglednia lokalny rozklad cen.",
    "Metoda globalna nie uwzglednia roznic regionalnych.",
    "Boxplot przedstawia pieciopunktowe podsumowanie.",
    "Liczba i procent outliers to rozne wskazniki.",
    "Outlier nie musi oznaczac bledu danych.",
    "Brak outliers nie oznacza braku nietypowych obserwacji.",
    "Oryginalne wartosci cen pozostaly niezmienione.",
    "Dane California Housing sa syntetyczne.",
    "Generator ogranicza ceny do zakresu 0.15-5.0.",
    "Ograniczenie cen moze wplywac na liczbe outliers.",
    "W ML granice IQR nalezy wyznaczac na danych treningowych."
]

for number, conclusion in enumerate(
    conclusions, start=1
):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba obserwacji: {len(df_housing)}")
print(f"Liczba regionow: {len(results)}")
print(f"Outliers grupowo: {total_outliers}")
print(f"Outliers globalnie: {int(global_mask.sum())}")
print(f"Procent outliers: {total_percentage:.2f}%")
print(
    f"Typowe wartosci: "
    f"{len(df_housing) - total_outliers}"
)
print(f"Liczba boxplotow: {len(grouped)}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df_housing.shape}")


section("WERYFIKACJA")

# Niezalezna weryfikacja za pomoca NumPy
manual_mask = pd.Series(
    False,
    index=df_housing.index
)

manual_counts = {}

for region, group in df_housing.groupby("Region"):
    values = group["MedHouseVal"].to_numpy()

    q1, q3 = np.quantile(values, [0.25, 0.75])

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    mask = (values < lower) | (values > upper)

    manual_mask.loc[group.index] = mask

    manual_counts[region] = int(mask.sum())

manual_counts = pd.Series(manual_counts)

# Weryfikacja granic na kontrolnym przykladzie
example = pd.Series([1, 2, 3, 4, 100])

example_q1 = example.quantile(0.25)
example_q3 = example.quantile(0.75)

example_iqr = iqr_func(example)

example_mask = (
    (example < example_q1 - 1.5 * example_iqr)
    | (example > example_q3 + 1.5 * example_iqr)
)

tests = {
    "Dataset ma 5000 wierszy":
        len(df_housing) == 5000,

    "Dataset ma poczatkowo 9 kolumn":
        df_original.shape[1] == 9,

    "Dataset nie zawiera NaN":
        not df_housing.isna().any().any(),

    "Istnieje 16 regionow":
        df_housing["Region"].nunique() == 16,

    "Utworzono 4 przedzialy Latitude":
        len(df_housing["lat_bin"].cat.categories) == 4,

    "Utworzono 4 przedzialy Longitude":
        len(df_housing["lon_bin"].cat.categories) == 4,

    "Dodano kolumne Is_Outlier":
        "Is_Outlier" in df_housing.columns,

    "Is_Outlier ma typ bool":
        pd.api.types.is_bool_dtype(
            df_housing["Is_Outlier"]
        ),

    "IQR jest nieujemny":
        (df_housing["IQR"] >= 0).all(),

    "Q1 nie przekracza Q3":
        (df_housing["Q1"] <= df_housing["Q3"]).all(),

    "Dolne granice sa poprawne":
        np.allclose(
            df_housing["Lower_Bound"],
            df_housing["Q1"] - 1.5 * df_housing["IQR"]
        ),

    "Gorne granice sa poprawne":
        np.allclose(
            df_housing["Upper_Bound"],
            df_housing["Q3"] + 1.5 * df_housing["IQR"]
        ),

    "Kazdy region ma jedna dolna granice":
        (
            df_housing.groupby("Region")
            ["Lower_Bound"].nunique() == 1
        ).all(),

    "Kazdy region ma jedna gorna granice":
        (
            df_housing.groupby("Region")
            ["Upper_Bound"].nunique() == 1
        ).all(),

    "Detekcja Pandas i NumPy jest zgodna":
        np.array_equal(group_mask, manual_mask),

    "Liczebnosci outliers sa zgodne z NumPy":
        np.array_equal(
            results["Outliers"],
            manual_counts.reindex(results.index)
        ),

    "Dolne i gorne outliers sa rozlaczne":
        not (
            df_housing["Is_Lower_Outlier"]
            & df_housing["Is_Upper_Outlier"]
        ).any(),

    "Suma dolnych i gornych outliers jest poprawna":
        (
            results["Dolne_outliers"]
            + results["Gorne_outliers"]
            == results["Outliers"]
        ).all(),

    "Uwzgledniono wszystkie obserwacje":
        results["Liczba_obserwacji"].sum() == 5000,

    "Suma outliers jest poprawna":
        results["Outliers"].sum() == total_outliers,

    "Typowe wartosci i outliers daja liczebnosc":
        (
            results["Typowe_wartosci"]
            + results["Outliers"]
            == results["Liczba_obserwacji"]
        ).all(),

    "Procenty sa w zakresie 0-100":
        results["Outliers_%"].between(0, 100).all(),

    "Procenty obliczono poprawnie":
        np.allclose(
            results["Outliers_%"],
            results["Outliers"]
            / results["Liczba_obserwacji"]
            * 100
        ),

    "Tabela statystyk ma 16 wierszy":
        len(five_number_summary) == 16,

    "Minimum nie przekracza Q1":
        (
            five_number_summary["Minimum"]
            <= five_number_summary["Q1"]
        ).all(),

    "Q1 nie przekracza mediany":
        (
            five_number_summary["Q1"]
            <= five_number_summary["Mediana"]
        ).all(),

    "Mediana nie przekracza Q3":
        (
            five_number_summary["Mediana"]
            <= five_number_summary["Q3"]
        ).all(),

    "Q3 nie przekracza maksimum":
        (
            five_number_summary["Q3"]
            <= five_number_summary["Maksimum"]
        ).all(),

    "Wlasna funkcja IQR jest poprawna":
        np.allclose(
            five_number_summary["IQR"],
            regional_bounds["IQR"]
        ),

    "Wygenerowano 16 boxplotow":
        len(grouped) == 16,

    "Boxploty maja poprawna szerokosc":
        all(
            len(text_boxplot(
                values, scale_min, scale_max
            )) == 55
            for _, values in grouped
        ),

    "Kontrolny przyklad wykrywa wartosc 100":
        example[example_mask].tolist() == [100],

    "Porownanie metod obejmuje wszystkie dane":
        both + only_global + only_group + neither
        == len(df_housing),

    "Ranking liczby outliers jest poprawny":
        ranking["Outliers"].is_monotonic_decreasing,

    "Ranking procentowy jest poprawny":
        percentage_ranking[
            "Outliers_%"
        ].is_monotonic_decreasing,

    "Zachowano wszystkie indeksy":
        df_housing.index.equals(df_original.index),

    "Istniejace kolumny pozostaly niezmienione":
        df_housing[df_original.columns].equals(
            df_original
        )
}

passed = sum(bool(result) for result in tests.values())

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

print(f"\nZaliczone testy: {passed}/{len(tests)}")

if passed == len(tests):
    print("Wszystkie testy zakonczone pomyslnie.")
else:
    print("Nie wszystkie testy zostaly zaliczone.")

assert passed == len(tests), "Blad weryfikacji."
