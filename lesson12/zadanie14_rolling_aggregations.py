# Lekcja 12 - Zadanie 14: Rolling Aggregations

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Konfiguracja
seed = 42
n_days = 365
window = 7
poisson_lambda = 100
sigma_multiplier = 2
start_date = "2025-01-01"

np.random.seed(seed)


# Generowanie syntetycznego datasetu
sales_time = pd.DataFrame({
    "Data": pd.date_range(
        start=start_date,
        periods=n_days,
        freq="D"
    ),
    "Sprzedaż": np.random.poisson(
        lam=poisson_lambda,
        size=n_days
    )
})

# Kopia danych do weryfikacji
sales_original = sales_time.copy()


print("=" * 75)
print("ROLLING AGGREGATIONS - ANALIZA SPRZEDAZY CZASOWEJ")
print("=" * 75)


section("KONFIGURACJA")

print(f"Seed: {seed}")
print(f"Liczba dni: {n_days}")
print(f"Rozklad Poissona - lambda: {poisson_lambda}")
print(f"Rozmiar okna: {window} dni")
print(f"Mnoznik odchylenia: {sigma_multiplier}")


section("DANE WEJSCIOWE")

print(f"Shape: {sales_time.shape}")
print(f"Liczba obserwacji: {len(sales_time)}")
print(f"Liczba kolumn: {len(sales_time.columns)}")
print(f"Liczba NaN: {sales_time.isna().sum().sum()}")
print(f"Pierwsza data: {sales_time['Data'].min().date()}")
print(f"Ostatnia data: {sales_time['Data'].max().date()}")


section("PIERWSZE 10 REKORDOW")

print(sales_time.head(10).to_string(index=False))


section("STATYSTYKI GLOBALNE SPRZEDAZY")

print(
    sales_time["Sprzedaż"]
    .describe()
    .round(2)
    .to_string()
)


# =========================================================
# ROLLING STATISTICS
# =========================================================

# Srednia kroczaca
sales_time["rolling_mean"] = (
    sales_time["Sprzedaż"]
    .rolling(window)
    .mean()
)

# Odchylenie standardowe kroczace
sales_time["rolling_std"] = (
    sales_time["Sprzedaż"]
    .rolling(window)
    .std()
)

# Gorna granica wykrywania anomalii
sales_time["upper_bound"] = (
    sales_time["rolling_mean"]
    + sigma_multiplier * sales_time["rolling_std"]
)

# Dolna granica - dodatkowa informacja
sales_time["lower_bound"] = (
    sales_time["rolling_mean"]
    - sigma_multiplier * sales_time["rolling_std"]
)

# Wykrywanie anomalii zgodnie z poleceniem
sales_time["anomaly"] = (
    sales_time["Sprzedaż"]
    > sales_time["upper_bound"]
)


section("STRUKTURA DATAFRAME")

print(f"Shape przed: {sales_original.shape}")
print(f"Shape po: {sales_time.shape}")

print(
    "Dodane kolumny:",
    sales_time.columns.difference(
        sales_original.columns
    ).tolist()
)

print("\nTypy danych:")
print(sales_time.dtypes.to_string())


section("PIERWSZE 30 DNI - ROLLING STATISTICS")

required_columns = [
    "Data",
    "Sprzedaż",
    "rolling_mean",
    "rolling_std",
    "anomaly"
]

print(
    sales_time[required_columns]
    .head(30)
    .to_string(index=False, float_format=lambda x: f"{x:.2f}")
)


section("PIERWSZE 30 DNI - GRANICE SPRZEDAZY")

print(
    sales_time[
        [
            "Data",
            "Sprzedaż",
            "rolling_mean",
            "rolling_std",
            "lower_bound",
            "upper_bound",
            "anomaly"
        ]
    ]
    .head(30)
    .to_string(index=False, float_format=lambda x: f"{x:.2f}")
)


section("ANALIZA BRAKUJACYCH WARTOSCI")

print(sales_time.isna().sum().to_string())

print(
    f"\nPierwsze {window - 1} dni "
    "nie posiadaja pelnego okna czasowego."
)

print(
    "Brak statystyk kroczacych nie oznacza "
    "braku danych sprzedazowych."
)


# =========================================================
# ANALIZA ANOMALII
# =========================================================

anomalies = sales_time.loc[
    sales_time["anomaly"]
].copy()

anomalies["Przekroczenie"] = (
    anomalies["Sprzedaż"]
    - anomalies["upper_bound"]
)

anomalies["Przekroczenie_%"] = (
    anomalies["Przekroczenie"]
    / anomalies["upper_bound"]
    * 100
)

anomalies["Z_score"] = (
    anomalies["Sprzedaż"]
    - anomalies["rolling_mean"]
) / anomalies["rolling_std"]


section("LISTA WSZYSTKICH ANOMALII")

anomaly_columns = [
    "Data",
    "Sprzedaż",
    "rolling_mean",
    "rolling_std",
    "upper_bound",
    "Przekroczenie",
    "Przekroczenie_%",
    "Z_score"
]

if anomalies.empty:
    print("Nie wykryto anomalii.")
else:
    print(
        anomalies[anomaly_columns]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}")
    )


# Dni posiadajace pelne okno
valid_days = sales_time["rolling_mean"].notna()

n_valid = int(valid_days.sum())
n_anomalies = len(anomalies)
n_normal = n_valid - n_anomalies
n_unavailable = n_days - n_valid

anomaly_rate = (
    n_anomalies / n_valid * 100
)


section("PODSUMOWANIE ANOMALII")

print(f"Liczba wszystkich dni: {n_days}")
print(f"Dni z pelnym oknem: {n_valid}")
print(f"Dni bez pelnego okna: {n_unavailable}")
print(f"Dni normalne z pelnym oknem: {n_normal}")
print(f"Liczba anomalii: {n_anomalies}")
print(f"Anomaly rate: {anomaly_rate:.2f}%")


section("RANKING ANOMALII")

if not anomalies.empty:
    print(
        anomalies[anomaly_columns]
        .sort_values(
            "Przekroczenie",
            ascending=False
        )
        .to_string(index=False, float_format=lambda x: f"{x:.4f}")
    )

    strongest = anomalies.loc[
        anomalies["Przekroczenie"].idxmax()
    ]

    print(
        "\nNajsilniejsza anomalia:",
        strongest["Data"].date()
    )

    print(
        f"Sprzedaz: {strongest['Sprzedaż']}"
    )

    print(
        f"Gorna granica: "
        f"{strongest['upper_bound']:.4f}"
    )

    print(
        f"Przekroczenie: "
        f"{strongest['Przekroczenie']:.4f}"
    )

else:
    print("Brak anomalii do porownania.")


# =========================================================
# ANALIZA MIESIECZNA
# =========================================================

monthly = (
    sales_time
    .groupby(
        sales_time["Data"].dt.to_period("M")
    )
    .agg(
        Liczba_dni=("Sprzedaż", "size"),
        Suma_sprzedazy=("Sprzedaż", "sum"),
        Srednia_sprzedaz=("Sprzedaż", "mean"),
        Minimum=("Sprzedaż", "min"),
        Maksimum=("Sprzedaż", "max"),
        Odchylenie_std=("Sprzedaż", "std"),
        Liczba_anomalii=("anomaly", "sum"),
        Dni_z_pelnym_oknem=("rolling_mean", "count")
    )
)

monthly["Anomaly_rate_%"] = (
    monthly["Liczba_anomalii"]
    / monthly["Dni_z_pelnym_oknem"]
    * 100
)


section("STATYSTYKI MIESIECZNE")

print(monthly.round(2).to_string())


section("TEKSTOWY WYKRES SREDNIEJ SPRZEDAZY")

print("Legenda: jeden znak = okolo 2 jednostek")

for month, row in monthly.iterrows():
    value = row["Srednia_sprzedaz"]
    bar = "█" * int(round(value / 2))

    print(
        f"{str(month)} | "
        f"{bar:<60} {value:7.2f}"
    )


section("TEKSTOWY WYKRES LICZBY ANOMALII")

print("Legenda: jeden znak = jedna anomalia")

for month, row in monthly.iterrows():
    value = int(row["Liczba_anomalii"])
    bar = "█" * value

    print(
        f"{str(month)} | "
        f"{bar:<20} {value}"
    )


section("TEKSTOWY WYKRES PIERWSZYCH 30 DNI")

print("Legenda: jeden znak = okolo 3 jednostek")
print("Gwiazdka oznacza wykryta anomalie.\n")

for _, row in sales_time.head(30).iterrows():
    value = row["Sprzedaż"]
    bar = "█" * int(round(value / 3))
    marker = "*" if row["anomaly"] else ""

    print(
        f"{row['Data'].date()} | "
        f"{bar:<45} {value:4d} {marker}"
    )


# =========================================================
# POROWNANIE ROZNYCH OKIEN CZASOWYCH
# =========================================================

section("POROWNANIE OKIEN CZASOWYCH")

window_results = []

for current_window in [3, 7, 14, 30]:

    current_mean = (
        sales_time["Sprzedaż"]
        .rolling(current_window)
        .mean()
    )

    current_std = (
        sales_time["Sprzedaż"]
        .rolling(current_window)
        .std()
    )

    current_bound = (
        current_mean
        + sigma_multiplier * current_std
    )

    current_anomaly = (
        sales_time["Sprzedaż"]
        > current_bound
    )

    current_valid = int(
        current_mean.notna().sum()
    )

    current_count = int(
        current_anomaly.sum()
    )

    window_results.append({
        "Okno_dni": current_window,
        "Dni_z_pelnym_oknem": current_valid,
        "Liczba_anomalii": current_count,
        "Anomaly_rate_%": (
            current_count / current_valid * 100
        ),
        "Zmiennosc_rolling_mean": (
            current_mean.std()
        )
    })

window_comparison = pd.DataFrame(
    window_results
)

print(
    window_comparison
    .to_string(index=False, float_format=lambda x: f"{x:.4f}")
)


# =========================================================
# POROWNANIE PROGOW WYKRYWANIA ANOMALII
# =========================================================

section("POROWNANIE PROGOW SIGMA")

threshold_results = []

for multiplier in [1.0, 1.5, 2.0, 2.5, 3.0]:

    threshold = (
        sales_time["rolling_mean"]
        + multiplier * sales_time["rolling_std"]
    )

    detected = (
        sales_time["Sprzedaż"] > threshold
    )

    count = int(detected.sum())

    threshold_results.append({
        "Mnoznik_sigma": multiplier,
        "Liczba_anomalii": count,
        "Anomaly_rate_%": count / n_valid * 100
    })

threshold_comparison = pd.DataFrame(
    threshold_results
)

print(
    threshold_comparison
    .to_string(index=False, float_format=lambda x: f"{x:.4f}")
)


# =========================================================
# WYKRYWANIE ANOMALII BEZ BIEZACEJ OBSERWACJI
# =========================================================

section("DODATKOWA ANALIZA - POPRZEDNIE 7 DNI")

# Alternatywny wariant:
# biezaca obserwacja nie uczestniczy
# w wyznaczaniu wlasnego progu.

previous_sales = sales_time["Sprzedaż"].shift(1)

previous_mean = (
    previous_sales.rolling(window).mean()
)

previous_std = (
    previous_sales.rolling(window).std()
)

previous_bound = (
    previous_mean
    + sigma_multiplier * previous_std
)

previous_anomaly = (
    sales_time["Sprzedaż"] > previous_bound
)

previous_valid = int(
    previous_mean.notna().sum()
)

previous_count = int(
    previous_anomaly.sum()
)

comparison = pd.DataFrame({
    "Metoda": [
        "Okno z biezacym dniem",
        "Okno z poprzednich 7 dni"
    ],
    "Dni_z_pelnym_oknem": [
        n_valid,
        previous_valid
    ],
    "Liczba_anomalii": [
        n_anomalies,
        previous_count
    ],
    "Anomaly_rate_%": [
        anomaly_rate,
        previous_count / previous_valid * 100
    ]
})

print(
    comparison
    .to_string(index=False, float_format=lambda x: f"{x:.4f}")
)

print(
    "\nGlowny wynik zadania wykorzystuje "
    "rolling(7) zgodnie z poleceniem."
)

print(
    "Wariant shift(1) jest dodatkowym "
    "porownaniem przydatnym w monitoringu."
)


# =========================================================
# ZUZYCIE PAMIECI
# =========================================================

section("ZUZYCIE PAMIECI")

memory_before = (
    sales_original
    .memory_usage(deep=True)
    .sum() / 1024
)

memory_after = (
    sales_time
    .memory_usage(deep=True)
    .sum() / 1024
)

print(f"Przed: {memory_before:.2f} KiB")
print(f"Po: {memory_after:.2f} KiB")

print(
    f"Wzrost: "
    f"{memory_after - memory_before:.2f} KiB"
)


section("WNIOSKI")

conclusions = [
    "Rolling pozwala analizowac dane w ruchomych oknach.",
    "Rolling mean wygladza krotkoterminowe wahania.",
    "Rolling std mierzy lokalna zmiennosc sprzedazy.",
    "Okno 7-dniowe obejmuje biezacy dzien i 6 poprzednich.",
    "Pierwsze 6 dni nie posiada pelnego okna.",
    "Pandas domyslnie stosuje std z ddof=1.",
    "Gorna granica zalezy od lokalnej sredniej i zmiennosci.",
    "Anomalia oznacza przekroczenie gornej granicy.",
    "Wieksze okno zwykle mocniej wygladza dane.",
    "Wyzszy prog sigma ogranicza liczbe wykrytych anomalii.",
    "Biezaca obserwacja moze wplywac na swoj prog.",
    "Shift(1) pozwala wykorzystac tylko dane historyczne.",
    "Anomalia statystyczna nie musi oznaczac bledu.",
    "Dane sprzedazowe maja charakter syntetyczny.",
    "Rolling statistics sa przydatne w Time Series Analysis."
]

for number, conclusion in enumerate(
    conclusions, start=1
):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba obserwacji: {len(sales_time)}")
print(f"Rozmiar okna: {window} dni")
print(f"Shape przed: {sales_original.shape}")
print(f"Shape po: {sales_time.shape}")

print(
    f"Calkowita sprzedaz: "
    f"{sales_time['Sprzedaż'].sum()}"
)

print(
    f"Srednia dzienna sprzedaz: "
    f"{sales_time['Sprzedaż'].mean():.2f}"
)

print(f"Liczba dni z pelnym oknem: {n_valid}")
print(f"Liczba anomalii: {n_anomalies}")
print(f"Anomaly rate: {anomaly_rate:.2f}%")


# =========================================================
# NIEZALEZNA WERYFIKACJA NUMPY
# =========================================================

sales_values = (
    sales_original["Sprzedaż"].to_numpy()
)

manual_means = np.full(n_days, np.nan)
manual_stds = np.full(n_days, np.nan)

for index in range(window - 1, n_days):

    current_values = sales_values[
        index - window + 1:index + 1
    ]

    manual_means[index] = np.mean(
        current_values
    )

    manual_stds[index] = np.std(
        current_values,
        ddof=1
    )

manual_upper = (
    manual_means
    + sigma_multiplier * manual_stds
)

manual_lower = (
    manual_means
    - sigma_multiplier * manual_stds
)

manual_anomalies = (
    sales_values > manual_upper
)


# =========================================================
# TESTY POPRAWNOSCI
# =========================================================

section("WERYFIKACJA")

tests = {
    "Dataset ma 365 wierszy":
        len(sales_time) == 365,

    "Dataset mial poczatkowo 2 kolumny":
        sales_original.shape == (365, 2),

    "Wynik ma shape (365, 7)":
        sales_time.shape == (365, 7),

    "Daty maja typ datetime":
        pd.api.types.is_datetime64_any_dtype(
            sales_time["Data"]
        ),

    "Daty sa unikalne":
        sales_time["Data"].is_unique,

    "Daty sa posortowane":
        sales_time["Data"].is_monotonic_increasing,

    "Daty wystepuja codziennie":
        (
            sales_time["Data"].diff().dropna()
            == pd.Timedelta(days=1)
        ).all(),

    "Sprzedaz ma typ calkowity":
        pd.api.types.is_integer_dtype(
            sales_time["Sprzedaż"]
        ),

    "Sprzedaz jest nieujemna":
        (sales_time["Sprzedaż"] >= 0).all(),

    "Sprzedaz nie zawiera NaN":
        sales_time["Sprzedaż"].notna().all(),

    "Dodano rolling_mean":
        "rolling_mean" in sales_time.columns,

    "Dodano rolling_std":
        "rolling_std" in sales_time.columns,

    "Dodano kolumne anomaly":
        "anomaly" in sales_time.columns,

    "Rolling mean ma 6 brakow":
        sales_time["rolling_mean"].isna().sum() == 6,

    "Rolling std ma 6 brakow":
        sales_time["rolling_std"].isna().sum() == 6,

    "Pierwsze 6 srednich to NaN":
        sales_time["rolling_mean"].head(6).isna().all(),

    "Pierwsze 6 odchylen to NaN":
        sales_time["rolling_std"].head(6).isna().all(),

    "Od 7 dnia srednie sa dostepne":
        sales_time["rolling_mean"].iloc[6:].notna().all(),

    "Od 7 dnia odchylenia sa dostepne":
        sales_time["rolling_std"].iloc[6:].notna().all(),

    "Istnieje 359 pelnych okien":
        n_valid == 359,

    "Rolling mean zgodne z NumPy":
        np.allclose(
            sales_time["rolling_mean"],
            manual_means,
            equal_nan=True
        ),

    "Rolling std zgodne z NumPy":
        np.allclose(
            sales_time["rolling_std"],
            manual_stds,
            equal_nan=True
        ),

    "Gorna granica jest poprawna":
        np.allclose(
            sales_time["upper_bound"],
            manual_upper,
            equal_nan=True
        ),

    "Dolna granica jest poprawna":
        np.allclose(
            sales_time["lower_bound"],
            manual_lower,
            equal_nan=True
        ),

    "Odchylenia sa nieujemne":
        (
            sales_time["rolling_std"].dropna() >= 0
        ).all(),

    "Anomaly ma typ bool":
        pd.api.types.is_bool_dtype(
            sales_time["anomaly"]
        ),

    "Anomaly nie zawiera NaN":
        sales_time["anomaly"].notna().all(),

    "Anomalie zgodne z NumPy":
        np.array_equal(
            sales_time["anomaly"].to_numpy(),
            manual_anomalies
        ),

    "Pierwsze 6 dni nie oznaczono jako anomalie":
        not sales_time["anomaly"].head(6).any(),

    "Wszystkie anomalie przekraczaja prog":
        (
            anomalies["Sprzedaż"]
            > anomalies["upper_bound"]
        ).all(),

    "Wszystkie przekroczenia sa dodatnie":
        (anomalies["Przekroczenie"] > 0).all(),

    "Z-score anomalii przekracza 2":
        (anomalies["Z_score"] > 2).all(),

    "Liczba anomalii jest zgodna":
        n_anomalies == sales_time["anomaly"].sum(),

    "Anomaly rate jest poprawny":
        np.isclose(
            anomaly_rate,
            n_anomalies / 359 * 100
        ),

    "Anomaly rate miesci sie w zakresie 0-100":
        0 <= anomaly_rate <= 100,

    "Uwzgledniono wszystkie dni":
        n_normal + n_anomalies + n_unavailable
        == n_days,

    "Tabela pierwszych 30 dni ma 30 wierszy":
        len(sales_time[required_columns].head(30))
        == 30,

    "Tabela wynikowa ma wymagane kolumny":
        len(required_columns) == 5,

    "Istnieje 12 miesiecy":
        len(monthly) == 12,

    "Suma dni miesiecznych jest poprawna":
        monthly["Liczba_dni"].sum() == n_days,

    "Suma sprzedazy miesiecznej jest poprawna":
        monthly["Suma_sprzedazy"].sum()
        == sales_time["Sprzedaż"].sum(),

    "Suma anomalii miesiecznych jest poprawna":
        monthly["Liczba_anomalii"].sum()
        == n_anomalies,

    "Porownano 4 okna czasowe":
        len(window_comparison) == 4,

    "Wynik okna 7 dni jest zgodny":
        window_comparison.loc[
            window_comparison["Okno_dni"] == 7,
            "Liczba_anomalii"
        ].iloc[0] == n_anomalies,

    "Porownano 5 progow sigma":
        len(threshold_comparison) == 5,

    "Wynik progu 2 sigma jest zgodny":
        threshold_comparison.loc[
            threshold_comparison["Mnoznik_sigma"] == 2,
            "Liczba_anomalii"
        ].iloc[0] == n_anomalies,

    "Wyzszy prog nie zwieksza liczby anomalii":
        threshold_comparison[
            "Liczba_anomalii"
        ].is_monotonic_decreasing,

    "Wariant historyczny ma 358 pelnych okien":
        previous_valid == 358,

    "Wariant historyczny nie ocenia pierwszych 7 dni":
        not previous_anomaly.head(7).any(),

    "Zachowano oryginalne indeksy":
        sales_time.index.equals(
            sales_original.index
        ),

    "Istniejace kolumny pozostaly niezmienione":
        sales_time[sales_original.columns].equals(
            sales_original
        )
}

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

assert passed == total, "Blad weryfikacji wynikow."
