# Lekcja 12 - Zadanie 15: Geographic Clustering

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 100)


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


# ==================================================
# KONFIGURACJA
# ==================================================

grid_size = 10
n_observations = 5000
seed = 42

# Generowanie datasetu
df = make_california_housing(
    n=n_observations,
    seed=seed
)

df_original = df.copy(deep=True)

print("=" * 100)
print("GEOGRAPHIC CLUSTERING - CALIFORNIA HOUSING")
print("=" * 100)


section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba obserwacji: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Liczba NaN: {df.isna().sum().sum()}")
print(f"Seed: {seed}")
print(f"Rozmiar siatki: {grid_size} x {grid_size}")
print(f"Maksymalna liczba regionow: {grid_size ** 2}")


section("PIERWSZE 10 REKORDOW")

print(df.head(10).to_string(index=False))


section("STATYSTYKI DATASETU")

print(df.describe().round(2).to_string())


section("ZAKRES WSPOLRZEDNYCH GEOGRAFICZNYCH")

print(
    f"Latitude: {df['Latitude'].min():.4f}"
    f" - {df['Latitude'].max():.4f}"
)

print(
    f"Longitude: {df['Longitude'].min():.4f}"
    f" - {df['Longitude'].max():.4f}"
)


# ==================================================
# TWORZENIE SIATKI 10 X 10
# ==================================================

df["lat_bin"], lat_edges = pd.cut(
    df["Latitude"],
    bins=grid_size,
    retbins=True,
    include_lowest=True
)

df["lon_bin"], lon_edges = pd.cut(
    df["Longitude"],
    bins=grid_size,
    retbins=True,
    include_lowest=True
)

# Numery przedzialow od 1 do 10
df["Lat_ID"] = df["lat_bin"].cat.codes + 1
df["Lon_ID"] = df["lon_bin"].cat.codes + 1

# Unikalna etykieta regionu
df["Region"] = (
    "R"
    + df["Lat_ID"].astype(str).str.zfill(2)
    + "_"
    + df["Lon_ID"].astype(str).str.zfill(2)
)


section("PRZEDZIALY LATITUDE")

for i, interval in enumerate(
    df["lat_bin"].cat.categories,
    start=1
):
    print(f"{i:2}. {interval}")


section("PRZEDZIALY LONGITUDE")

for i, interval in enumerate(
    df["lon_bin"].cat.categories,
    start=1
):
    print(f"{i:2}. {interval}")


section("PIERWSZE 10 REKORDOW Z REGIONAMI")

print(
    df[
        [
            "Latitude",
            "Longitude",
            "Lat_ID",
            "Lon_ID",
            "Region",
            "MedHouseVal"
        ]
    ].head(10).to_string(index=False)
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

print(f"Liczba regionow: {df['Region'].nunique()}")


# ==================================================
# AGREGACJA REGIONALNA
# ==================================================

regional_stats = (
    df.groupby("Region")
    .agg(
        Lat_ID=("Lat_ID", "first"),
        Lon_ID=("Lon_ID", "first"),
        Liczba_obserwacji=("MedHouseVal", "size"),
        Srednia_cena=("MedHouseVal", "mean"),
        Mediana_dochodow=("MedInc", "median"),
        Populacja=("Population", "sum"),
        Min_cena=("MedHouseVal", "min"),
        Max_cena=("MedHouseVal", "max"),
        Mediana_ceny=("MedHouseVal", "median"),
        Odchylenie_std=("MedHouseVal", "std"),
        Sredni_wiek_domu=("HouseAge", "mean"),
        Srednia_latitude=("Latitude", "mean"),
        Srednia_longitude=("Longitude", "mean")
    )
    .reset_index()
)

# Przeliczenie ceny na USD
regional_stats["Srednia_cena_USD"] = (
    regional_stats["Srednia_cena"] * 100000
)

# Udzial regionu w populacji datasetu
regional_stats["Udzial_populacji_%"] = (
    regional_stats["Populacja"]
    / regional_stats["Populacja"].sum()
    * 100
)

# Wspolczynnik zmiennosci cen
regional_stats["Zmiennosc_cen_%"] = (
    regional_stats["Odchylenie_std"]
    / regional_stats["Srednia_cena"]
    * 100
)


section("STATYSTYKI WSZYSTKICH REGIONOW")

main_columns = [
    "Region",
    "Liczba_obserwacji",
    "Srednia_cena",
    "Mediana_dochodow",
    "Populacja",
    "Srednia_cena_USD"
]

print(
    regional_stats[main_columns]
    .round(2)
    .to_string(index=False)
)


section("SZCZEGOLOWE STATYSTYKI REGIONALNE")

detail_columns = [
    "Region",
    "Min_cena",
    "Max_cena",
    "Mediana_ceny",
    "Odchylenie_std",
    "Zmiennosc_cen_%",
    "Sredni_wiek_domu"
]

print(
    regional_stats[detail_columns]
    .round(2)
    .to_string(index=False)
)


# ==================================================
# RANKING REGIONOW
# ==================================================

ranking = regional_stats.sort_values(
    ["Srednia_cena", "Region"],
    ascending=[False, True]
).reset_index(drop=True)

ranking.index = ranking.index + 1

top10 = ranking.head(10).copy()

bottom10 = (
    regional_stats.sort_values(
        ["Srednia_cena", "Region"],
        ascending=[True, True]
    )
    .head(10)
    .reset_index(drop=True)
)

bottom10.index = bottom10.index + 1


section("TOP 10 NAJDROZSZYCH REGIONOW")

print(
    top10[main_columns]
    .round(2)
    .to_string()
)


section("TOP 10 NAJTANSZYCH REGIONOW")

print(
    bottom10[main_columns]
    .round(2)
    .to_string()
)


# ==================================================
# KWARTYLE CEN REGIONALNYCH
# ==================================================

q1 = regional_stats["Srednia_cena"].quantile(0.25)
q2 = regional_stats["Srednia_cena"].quantile(0.50)
q3 = regional_stats["Srednia_cena"].quantile(0.75)

quartile_labels = [
    "Q1 - najtansze",
    "Q2 - nizsze ceny",
    "Q3 - wyzsze ceny",
    "Q4 - najdrozsze"
]

regional_stats["Kwartyl_ceny"] = pd.cut(
    regional_stats["Srednia_cena"],
    bins=[-np.inf, q1, q2, q3, np.inf],
    labels=quartile_labels
)


section("KWARTYLE SREDNICH CEN REGIONOW")

print(f"Q1: {q1:.4f}")
print(f"Q2 (mediana): {q2:.4f}")
print(f"Q3: {q3:.4f}")

print(f"Q1 w USD: {q1 * 100000:,.2f}")
print(f"Q2 w USD: {q2 * 100000:,.2f}")
print(f"Q3 w USD: {q3 * 100000:,.2f}")


section("LICZEBNOSC KWARTYLI")

print(
    regional_stats["Kwartyl_ceny"]
    .value_counts(sort=False)
    .to_string()
)


section("STATYSTYKI WEDLUG KWARTYLA CENY")

quartile_stats = (
    regional_stats.groupby(
        "Kwartyl_ceny",
        observed=True
    )
    .agg(
        Liczba_regionow=("Region", "size"),
        Liczba_obserwacji=(
            "Liczba_obserwacji", "sum"
        ),
        Srednia_cena=("Srednia_cena", "mean"),
        Min_cena=("Srednia_cena", "min"),
        Max_cena=("Srednia_cena", "max"),
        Populacja=("Populacja", "sum")
    )
)

print(quartile_stats.round(2).to_string())


# ==================================================
# HISTOGRAM 2D
# ==================================================

# Uzywamy numerow regionow utworzonych przez pd.cut.
# Zapewnia to identyczne przypisanie obserwacji
# do komorek w Pandas i NumPy.

id_edges = np.arange(
    0.5,
    grid_size + 1.5,
    1
)

count_grid, _, _ = np.histogram2d(
    df["Lat_ID"],
    df["Lon_ID"],
    bins=[id_edges, id_edges]
)

price_sum_grid, _, _ = np.histogram2d(
    df["Lat_ID"],
    df["Lon_ID"],
    bins=[id_edges, id_edges],
    weights=df["MedHouseVal"]
)

population_grid, _, _ = np.histogram2d(
    df["Lat_ID"],
    df["Lon_ID"],
    bins=[id_edges, id_edges],
    weights=df["Population"]
)

# Srednia cena = suma cen / liczba obserwacji
mean_price_grid = np.divide(
    price_sum_grid,
    count_grid,
    out=np.full(
        count_grid.shape,
        np.nan,
        dtype=float
    ),
    where=count_grid > 0
)


section("HISTOGRAM 2D - LICZBA OBSERWACJI")

print(count_grid.astype(int))

print(f"Shape: {count_grid.shape}")
print(f"Suma obserwacji: {count_grid.sum():.0f}")


section("HISTOGRAM 2D - SUMA POPULACJI")

print(population_grid.astype(int))

print(
    f"Suma populacji: "
    f"{population_grid.sum():,.0f}"
)


# ==================================================
# NUMERYCZNA HEATMAPA
# ==================================================

price_table = pd.DataFrame(
    mean_price_grid,
    index=range(1, grid_size + 1),
    columns=range(1, grid_size + 1)
)

price_table.index.name = "Latitude"
price_table.columns.name = "Longitude"


section("NUMERYCZNA HEATMAPA SREDNICH CEN")

print("Polnoc u gory, poludnie na dole.")
print("Zachod po lewej, wschod po prawej.")
print("Ceny w jednostkach 100 000 USD.\n")

print(
    price_table.iloc[::-1]
    .round(2)
    .to_string()
)


# ==================================================
# TEKSTOWA HEATMAPA 10 X 10
# ==================================================

def price_symbol(value):
    """Zwraca symbol odpowiedniego kwartyla."""

    if np.isnan(value):
        return "·"

    if value <= q1:
        return "░"

    if value <= q2:
        return "▒"

    if value <= q3:
        return "▓"

    return "█"


symbol_grid = np.array([
    [
        price_symbol(value)
        for value in row
    ]
    for row in mean_price_grid
])


section("TEKSTOWA HEATMAPA 10 X 10")

print("                  POLNOC")
print()

header = " ".join(
    f"{i:>2}"
    for i in range(1, grid_size + 1)
)

print(f"Lat/Lon | {header}")
print("-" * 42)

# Odwrocenie kolejnosci Latitude:
# polnoc znajduje sie na gorze mapy.

for row_id in range(grid_size - 1, -1, -1):

    symbols = " ".join(
        f"{symbol:>2}"
        for symbol in symbol_grid[row_id]
    )

    print(f"{row_id + 1:>7} | {symbols}")

print("-" * 42)
print("ZACHOD                         WSCHOD")
print("                 POLUDNIE")

print("\nLegenda:")
print(f"░ Q1 - ceny do {q1:.4f}")
print(f"▒ Q2 - ceny od {q1:.4f} do {q2:.4f}")
print(f"▓ Q3 - ceny od {q2:.4f} do {q3:.4f}")
print(f"█ Q4 - ceny powyzej {q3:.4f}")
print("· Brak obserwacji")


section("LICZEBNOSC SYMBOLI HEATMAPY")

symbols, frequencies = np.unique(
    symbol_grid,
    return_counts=True
)

symbol_counts = dict(
    zip(symbols, frequencies)
)

for symbol in ["░", "▒", "▓", "█", "·"]:
    print(
        f"{symbol}: "
        f"{symbol_counts.get(symbol, 0)} regionow"
    )


# ==================================================
# ANALIZA LICZEBNOSCI REGIONOW
# ==================================================

section("LICZEBNOSC OBSERWACJI W REGIONACH")

count_table = pd.DataFrame(
    count_grid.astype(int),
    index=range(1, grid_size + 1),
    columns=range(1, grid_size + 1)
)

print(count_table.iloc[::-1].to_string())

print(
    f"\nMinimalna liczebnosc: "
    f"{count_grid.min():.0f}"
)

print(
    f"Maksymalna liczebnosc: "
    f"{count_grid.max():.0f}"
)

print(
    f"Srednia liczebnosc: "
    f"{count_grid.mean():.2f}"
)

print(
    f"Puste regiony: "
    f"{np.count_nonzero(count_grid == 0)}"
)


# ==================================================
# POROWNANIE REGIONOW
# ==================================================

most_expensive = top10.iloc[0]
cheapest = bottom10.iloc[0]

price_difference = (
    most_expensive["Srednia_cena"]
    - cheapest["Srednia_cena"]
)

price_ratio = (
    most_expensive["Srednia_cena"]
    / cheapest["Srednia_cena"]
)


section("NAJDROZSZY REGION")

print(f"Region: {most_expensive['Region']}")
print(
    f"Srednia cena: "
    f"{most_expensive['Srednia_cena_USD']:,.2f} USD"
)
print(
    f"Mediana dochodow: "
    f"{most_expensive['Mediana_dochodow']:.4f}"
)
print(
    f"Populacja: "
    f"{most_expensive['Populacja']:,}"
)
print(
    f"Liczba obserwacji: "
    f"{most_expensive['Liczba_obserwacji']}"
)


section("NAJTANSZY REGION")

print(f"Region: {cheapest['Region']}")
print(
    f"Srednia cena: "
    f"{cheapest['Srednia_cena_USD']:,.2f} USD"
)
print(
    f"Mediana dochodow: "
    f"{cheapest['Mediana_dochodow']:.4f}"
)
print(
    f"Populacja: "
    f"{cheapest['Populacja']:,}"
)
print(
    f"Liczba obserwacji: "
    f"{cheapest['Liczba_obserwacji']}"
)


section("ROZNICE MIEDZY REGIONAMI")

print(
    f"Roznica srednich cen: "
    f"{price_difference * 100000:,.2f} USD"
)

print(
    f"Stosunek cen: "
    f"{price_ratio:.2f}x"
)

print(
    f"Srednia cena TOP 10: "
    f"{top10['Srednia_cena_USD'].mean():,.2f} USD"
)

print(
    f"Srednia cena BOTTOM 10: "
    f"{bottom10['Srednia_cena_USD'].mean():,.2f} USD"
)


section("TEKSTOWY WYKRES TOP 10")

print("Legenda: jeden znak = okolo 10 000 USD")

for _, row in top10.iterrows():

    price = row["Srednia_cena_USD"]
    bar = "█" * int(round(price / 10000))

    print(
        f"{row['Region']:8} | "
        f"{bar:50} {price:,.2f} USD"
    )


section("TEKSTOWY WYKRES BOTTOM 10")

print("Legenda: jeden znak = okolo 10 000 USD")

for _, row in bottom10.iterrows():

    price = row["Srednia_cena_USD"]
    bar = "█" * int(round(price / 10000))

    print(
        f"{row['Region']:8} | "
        f"{bar:50} {price:,.2f} USD"
    )


# ==================================================
# ANALIZA DOCHODOW I POPULACJI
# ==================================================

section("TOP 10 REGIONOW WEDLUG MEDIANY DOCHODOW")

print(
    regional_stats.nlargest(
        10,
        "Mediana_dochodow"
    )[
        [
            "Region",
            "Mediana_dochodow",
            "Srednia_cena_USD",
            "Populacja"
        ]
    ].round(2).to_string(index=False)
)


section("TOP 10 REGIONOW WEDLUG POPULACJI")

print(
    regional_stats.nlargest(
        10,
        "Populacja"
    )[
        [
            "Region",
            "Populacja",
            "Udzial_populacji_%",
            "Srednia_cena_USD"
        ]
    ].round(2).to_string(index=False)
)


section("KORELACJE REGIONALNE")

correlation_columns = [
    "Srednia_cena",
    "Mediana_dochodow",
    "Populacja",
    "Sredni_wiek_domu",
    "Srednia_latitude",
    "Srednia_longitude"
]

correlations = (
    regional_stats[correlation_columns]
    .corr()
)

print(correlations.round(4).to_string())


# ==================================================
# ANALIZA POLNOC - POLUDNIE
# ==================================================

section("POROWNANIE PASOW LATITUDE")

latitude_stats = (
    df.groupby("Lat_ID")
    .agg(
        Liczba_obserwacji=("MedHouseVal", "size"),
        Srednia_cena=("MedHouseVal", "mean"),
        Mediana_dochodow=("MedInc", "median"),
        Populacja=("Population", "sum")
    )
)

print(latitude_stats.round(4).to_string())


section("POROWNANIE PASOW LONGITUDE")

longitude_stats = (
    df.groupby("Lon_ID")
    .agg(
        Liczba_obserwacji=("MedHouseVal", "size"),
        Srednia_cena=("MedHouseVal", "mean"),
        Mediana_dochodow=("MedInc", "median"),
        Populacja=("Population", "sum")
    )
)

print(longitude_stats.round(4).to_string())


# ==================================================
# SREDNIA GLOBALNA I WAZONA
# ==================================================

global_mean = df["MedHouseVal"].mean()

weighted_mean = np.average(
    regional_stats["Srednia_cena"],
    weights=regional_stats["Liczba_obserwacji"]
)

unweighted_mean = (
    regional_stats["Srednia_cena"].mean()
)

histogram_mean = (
    price_sum_grid.sum()
    / count_grid.sum()
)


section("WERYFIKACJA SREDNIEJ GLOBALNEJ")

print(f"Srednia globalna: {global_mean:.6f}")
print(f"Srednia wazona regionow: {weighted_mean:.6f}")
print(f"Srednia niewazona regionow: {unweighted_mean:.6f}")
print(f"Srednia z histogramu 2D: {histogram_mean:.6f}")


# ==================================================
# POROWNANIE PANDAS I NUMPY
# ==================================================

pandas_price_grid = (
    regional_stats.pivot(
        index="Lat_ID",
        columns="Lon_ID",
        values="Srednia_cena"
    )
    .reindex(
        index=range(1, grid_size + 1),
        columns=range(1, grid_size + 1)
    )
    .to_numpy()
)

pandas_count_grid = (
    regional_stats.pivot(
        index="Lat_ID",
        columns="Lon_ID",
        values="Liczba_obserwacji"
    )
    .reindex(
        index=range(1, grid_size + 1),
        columns=range(1, grid_size + 1)
    )
    .fillna(0)
    .to_numpy()
)

pandas_population_grid = (
    regional_stats.pivot(
        index="Lat_ID",
        columns="Lon_ID",
        values="Populacja"
    )
    .reindex(
        index=range(1, grid_size + 1),
        columns=range(1, grid_size + 1)
    )
    .fillna(0)
    .to_numpy()
)


section("POROWNANIE PANDAS I NUMPY")

print(
    "Zgodnosc srednich cen:",
    np.allclose(
        pandas_price_grid,
        mean_price_grid,
        equal_nan=True
    )
)

print(
    "Zgodnosc liczebnosci:",
    np.array_equal(
        pandas_count_grid,
        count_grid
    )
)

print(
    "Zgodnosc populacji:",
    np.array_equal(
        pandas_population_grid,
        population_grid
    )
)


# ==================================================
# ZUZYCIE PAMIECI
# ==================================================

section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum()
    / 1024
)

memory_after = (
    df.memory_usage(deep=True).sum()
    / 1024
)

memory_stats = (
    regional_stats.memory_usage(deep=True).sum()
    / 1024
)

print(f"Dataset przed: {memory_before:.2f} KiB")
print(f"Dataset po: {memory_after:.2f} KiB")
print(f"Wzrost: {memory_after - memory_before:.2f} KiB")
print(f"Tabela regionalna: {memory_stats:.2f} KiB")


# ==================================================
# WNIOSKI
# ==================================================

section("WNIOSKI")

conclusions = [
    "Pd.cut pozwala tworzyc przedzialy geograficzne.",
    "Siatka 10x10 definiuje 100 mozliwych regionow.",
    "Region jest kombinacja Latitude i Longitude.",
    "GroupBy umozliwia agregacje regionalne.",
    "Agg pozwala obliczyc wiele statystyk jednoczesnie.",
    "Histogram2d tworzy dwuwymiarowa siatke danych.",
    "Srednia cena wymaga podzielenia sumy przez liczebnosc.",
    "Kwartyle pozwalaja porownywac poziomy cen.",
    "Tekstowa heatmapa nie wymaga bibliotek graficznych.",
    "Srednia wazona uwzglednia liczebnosc regionow.",
    "Liczebnosc regionu ma znaczenie dla interpretacji.",
    "Korelacja nie dowodzi zwiazku przyczynowego.",
    "Podzial na siatke nie jest algorytmem K-Means.",
    "Granice regionow wynikaja z przyjetego podzialu.",
    "Dane sa syntetyczne, a nie rzeczywiste.",
    "Wyniki nie stanowia analizy realnego rynku nieruchomosci."
]

for i, conclusion in enumerate(
    conclusions,
    start=1
):
    print(f"{i}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba obserwacji: {len(df)}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print(f"Siatka: {grid_size} x {grid_size}")
print(f"Liczba regionow: {len(regional_stats)}")
print(f"Liczba kwartylow: {len(quartile_labels)}")
print(f"Liczba regionow TOP: {len(top10)}")
print(f"Liczba regionow BOTTOM: {len(bottom10)}")

print(
    f"Puste regiony: "
    f"{np.count_nonzero(count_grid == 0)}"
)

print(
    f"Najdrozszy region: "
    f"{most_expensive['Region']}"
)

print(
    f"Najtanszy region: "
    f"{cheapest['Region']}"
)

print(
    f"Calkowita populacja datasetu: "
    f"{df['Population'].sum():,}"
)


# ==================================================
# AUTOMATYCZNA WERYFIKACJA
# ==================================================

tests = {
    "Dataset ma 5000 wierszy":
        len(df_original) == 5000,

    "Dataset ma poczatkowo 9 kolumn":
        df_original.shape[1] == 9,

    "Dataset nie zawiera NaN":
        not df_original.isna().any().any(),

    "Siatka ma rozmiar 10x10":
        grid_size == 10,

    "Istnieje 10 przedzialow Latitude":
        len(df["lat_bin"].cat.categories) == 10,

    "Istnieje 10 przedzialow Longitude":
        len(df["lon_bin"].cat.categories) == 10,

    "Granice Latitude sa rosnace":
        np.all(np.diff(lat_edges) > 0),

    "Granice Longitude sa rosnace":
        np.all(np.diff(lon_edges) > 0),

    "Latitude ID miesci sie w zakresie 1-10":
        df["Lat_ID"].between(1, 10).all(),

    "Longitude ID miesci sie w zakresie 1-10":
        df["Lon_ID"].between(1, 10).all(),

    "Wszystkie obserwacje maja region":
        df["Region"].notna().all(),

    "Utworzono 100 regionow":
        df["Region"].nunique() == 100,

    "Tabela regionalna ma 100 wierszy":
        len(regional_stats) == 100,

    "Etykiety regionow sa unikalne":
        regional_stats["Region"].is_unique,

    "Dodano 5 nowych kolumn":
        df.shape[1] == df_original.shape[1] + 5,

    "Zachowano wszystkie wiersze":
        len(df) == len(df_original),

    "Zachowano oryginalne indeksy":
        df.index.equals(df_original.index),

    "Suma liczebnosci wynosi 5000":
        regional_stats["Liczba_obserwacji"].sum()
        == 5000,

    "Suma populacji jest zgodna":
        regional_stats["Populacja"].sum()
        == df["Population"].sum(),

    "Udzial populacji sumuje sie do 100":
        np.isclose(
            regional_stats["Udzial_populacji_%"].sum(),
            100
        ),

    "Srednie ceny sa dodatnie":
        regional_stats["Srednia_cena"].gt(0).all(),

    "Mediany dochodow sa dodatnie":
        regional_stats["Mediana_dochodow"].gt(0).all(),

    "Populacja regionow jest dodatnia":
        regional_stats["Populacja"].gt(0).all(),

    "Minimum nie przekracza sredniej":
        (
            regional_stats["Min_cena"]
            <= regional_stats["Srednia_cena"]
        ).all(),

    "Maksimum nie jest mniejsze od sredniej":
        (
            regional_stats["Max_cena"]
            >= regional_stats["Srednia_cena"]
        ).all(),

    "Odchylenia standardowe sa nieujemne":
        regional_stats["Odchylenie_std"].ge(0).all(),

    "Ceny USD obliczono poprawnie":
        np.allclose(
            regional_stats["Srednia_cena_USD"],
            regional_stats["Srednia_cena"] * 100000
        ),

    "TOP zawiera 10 regionow":
        len(top10) == 10,

    "BOTTOM zawiera 10 regionow":
        len(bottom10) == 10,

    "TOP jest posortowany malejaco":
        top10["Srednia_cena"].is_monotonic_decreasing,

    "BOTTOM jest posortowany rosnaco":
        bottom10["Srednia_cena"].is_monotonic_increasing,

    "TOP i BOTTOM nie pokrywaja sie":
        set(top10["Region"]).isdisjoint(
            set(bottom10["Region"])
        ),

    "Najdrozszy region jest poprawny":
        np.isclose(
            most_expensive["Srednia_cena"],
            regional_stats["Srednia_cena"].max()
        ),

    "Najtanszy region jest poprawny":
        np.isclose(
            cheapest["Srednia_cena"],
            regional_stats["Srednia_cena"].min()
        ),

    "Kwartyle sa uporzadkowane":
        q1 <= q2 <= q3,

    "Istnieja 4 kategorie kwartylowe":
        len(
            regional_stats["Kwartyl_ceny"]
            .cat.categories
        ) == 4,

    "Wszystkie regiony maja kwartyl":
        regional_stats["Kwartyl_ceny"].notna().all(),

    "Kwartyle uwzgledniaja 100 regionow":
        quartile_stats["Liczba_regionow"].sum()
        == 100,

    "Histogram liczebnosci ma shape 10x10":
        count_grid.shape == (10, 10),

    "Histogram cen ma shape 10x10":
        price_sum_grid.shape == (10, 10),

    "Histogram populacji ma shape 10x10":
        population_grid.shape == (10, 10),

    "Histogram uwzglednia wszystkie obserwacje":
        count_grid.sum() == len(df),

    "Histogram zachowuje sume cen":
        np.isclose(
            price_sum_grid.sum(),
            df["MedHouseVal"].sum()
        ),

    "Histogram zachowuje populacje":
        population_grid.sum()
        == df["Population"].sum(),

    "Heatmapa numeryczna ma shape 10x10":
        mean_price_grid.shape == (10, 10),

    "Heatmapa tekstowa ma shape 10x10":
        symbol_grid.shape == (10, 10),

    "Heatmapa zawiera 100 symboli":
        symbol_grid.size == 100,

    "Heatmapa zawiera dozwolone symbole":
        set(symbol_grid.ravel()).issubset(
            {"░", "▒", "▓", "█", "·"}
        ),

    "Liczba symboli sumuje sie do 100":
        frequencies.sum() == 100,

    "Puste komorki maja symbol kropki":
        np.array_equal(
            symbol_grid == "·",
            count_grid == 0
        ),

    "Srednie cen Pandas i NumPy sa zgodne":
        np.allclose(
            pandas_price_grid,
            mean_price_grid,
            equal_nan=True
        ),

    "Liczebnosci Pandas i NumPy sa zgodne":
        np.array_equal(
            pandas_count_grid,
            count_grid
        ),

    "Populacje Pandas i NumPy sa zgodne":
        np.array_equal(
            pandas_population_grid,
            population_grid
        ),

    "Srednia wazona jest poprawna":
        np.isclose(weighted_mean, global_mean),

    "Srednia histogramu jest poprawna":
        np.isclose(histogram_mean, global_mean),

    "Roznica cen jest nieujemna":
        price_difference >= 0,

    "Stosunek cen jest nie mniejszy od 1":
        price_ratio >= 1,

    "Pasy Latitude uwzgledniaja wszystkie dane":
        latitude_stats["Liczba_obserwacji"].sum()
        == len(df),

    "Pasy Longitude uwzgledniaja wszystkie dane":
        longitude_stats["Liczba_obserwacji"].sum()
        == len(df),

    "Oryginalne kolumny pozostaly niezmienione":
        df[df_original.columns].equals(df_original)
}


section("WERYFIKACJA")

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(
    bool(result)
    for result in tests.values()
)

total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")

if passed == total:
    print("Wszystkie testy zakonczone pomyslnie.")
else:
    print("Nie wszystkie testy zostaly zaliczone.")

    failed = [
        name
        for name, result in tests.items()
        if not result
    ]

    print("Niezaliczone testy:")

    for name in failed:
        print(f"- {name}")

    raise AssertionError(
        "Weryfikacja zadania nie powiodla sie."
    )
