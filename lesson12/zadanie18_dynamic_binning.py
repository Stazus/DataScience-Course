# Lekcja 12 - Zadanie 18: Dynamic Binning

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


def calculate_statistics(data, bins):
    """Oblicza statystyki przezywalnosci dla przedzialow."""

    temp = data.assign(Age_Bin=bins)

    stats = (
        temp.groupby("Age_Bin", observed=True)
        .agg(
            Liczba_pasazerow=("Survived", "size"),
            Przezyli=("Survived", "sum"),
            Survival_Rate=("Survived", "mean"),
            Sredni_wiek=("Age", "mean"),
            Min_wiek=("Age", "min"),
            Max_wiek=("Age", "max")
        )
    )

    stats["Nie_przezyli"] = (
        stats["Liczba_pasazerow"] - stats["Przezyli"]
    )

    stats["Survival_Rate_%"] = (
        stats["Survival_Rate"] * 100
    )

    stats["Mortality_Rate_%"] = (
        100 - stats["Survival_Rate_%"]
    )

    return stats


def calculate_score(stats):
    """Oblicza rozpietosc survival rate."""

    rates = stats["Survival_Rate"]

    return float(rates.max() - rates.min())


def show_statistics(stats):
    """Wyswietla czytelna tabele wynikowa."""

    columns = [
        "Liczba_pasazerow",
        "Przezyli",
        "Nie_przezyli",
        "Survival_Rate_%",
        "Mortality_Rate_%",
        "Sredni_wiek"
    ]

    print(
        stats[columns]
        .round(2)
        .to_string()
    )


def text_chart(stats):
    """Wyswietla tekstowy wykres przezywalnosci."""

    print("Legenda: jeden znak = okolo 2%")

    for interval, row in stats.iterrows():

        rate = row["Survival_Rate_%"]

        bar = "█" * int(round(rate / 2))

        print(
            f"{str(interval):<24} | "
            f"{bar:<50} "
            f"{rate:6.2f}%"
        )


def strategy_summary(name, stats):
    """Tworzy podsumowanie strategii."""

    return {
        "Strategia": name,
        "Liczba_binow": len(stats),
        "Min_survival_%": (
            stats["Survival_Rate_%"].min()
        ),
        "Max_survival_%": (
            stats["Survival_Rate_%"].max()
        ),
        "Rozpietosc_pp": (
            calculate_score(stats) * 100
        ),
        "Min_liczebnosc": (
            stats["Liczba_pasazerow"].min()
        ),
        "Max_liczebnosc": (
            stats["Liczba_pasazerow"].max()
        ),
        "Liczba_pasazerow": (
            stats["Liczba_pasazerow"].sum()
        )
    }


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia danych do weryfikacji
df_original = df.copy()

# Analiza tylko pasazerow ze znanym wiekiem
data = df.dropna(
    subset=["Age", "Survived"]
).copy()


print("=" * 75)
print("DYNAMIC BINNING - DATASET TITANIC")
print("=" * 75)


section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Znany wiek: {df['Age'].notna().sum()}")
print(f"Brakujacy wiek: {df['Age'].isna().sum()}")
print(f"Liczba analizowanych pasazerow: {len(data)}")


section("PIERWSZE 10 REKORDOW")

print(
    df[["PassengerId", "Age", "Survived"]]
    .head(10)
    .to_string(index=False)
)


section("STATYSTYKI WIEKU")

print(
    data["Age"]
    .describe()
    .round(2)
    .to_string()
)


section("GLOBALNA PRZEZYWALNOSC")

global_rate = df["Survived"].mean() * 100
known_age_rate = data["Survived"].mean() * 100

print(f"Wszyscy pasazerowie: {global_rate:.2f}%")
print(f"Pasazerowie ze znanym wiekiem: {known_age_rate:.2f}%")


# =========================================================
# STRATEGIA 1 - EQUAL-WIDTH
# =========================================================

section("STRATEGIA 1 - EQUAL-WIDTH")

equal_width_bins = pd.cut(
    data["Age"],
    bins=5
)

equal_width_stats = calculate_statistics(
    data,
    equal_width_bins
)

print("Przedzialy:")

for interval in equal_width_bins.cat.categories:
    print(interval)

print()

show_statistics(equal_width_stats)

equal_width_score = calculate_score(
    equal_width_stats
)

print(
    f"\nRozpietosc survival rate: "
    f"{equal_width_score * 100:.2f} p.p."
)


section("EQUAL-WIDTH - WYKRES TEKSTOWY")

text_chart(equal_width_stats)


# =========================================================
# STRATEGIA 2 - EQUAL-FREQUENCY
# =========================================================

section("STRATEGIA 2 - EQUAL-FREQUENCY")

equal_frequency_bins = pd.qcut(
    data["Age"],
    q=5,
    duplicates="drop"
)

equal_frequency_stats = calculate_statistics(
    data,
    equal_frequency_bins
)

print("Przedzialy:")

for interval in equal_frequency_bins.cat.categories:
    print(interval)

print()

show_statistics(equal_frequency_stats)

equal_frequency_score = calculate_score(
    equal_frequency_stats
)

print(
    f"\nRozpietosc survival rate: "
    f"{equal_frequency_score * 100:.2f} p.p."
)


section("EQUAL-FREQUENCY - WYKRES TEKSTOWY")

text_chart(equal_frequency_stats)


# =========================================================
# STRATEGIA 3 - MANUAL OPTIMIZATION
# =========================================================

section("STRATEGIA 3 - MANUAL OPTIMIZATION")

candidate_edges = {
    "Zestaw 1": [0, 12, 18, 35, 60, 100],
    "Zestaw 2": [0, 8, 15, 25, 40, 60, 100],
    "Zestaw 3": [0, 6, 14, 22, 30, 45, 65, 100]
}

manual_results = {}
manual_summaries = []

for name, edges in candidate_edges.items():

    section(f"MANUAL OPTIMIZATION - {name}")

    print(f"Granice: {edges}")

    bins = pd.cut(
        data["Age"],
        bins=edges,
        include_lowest=True
    )

    stats = calculate_statistics(
        data,
        bins
    )

    score = calculate_score(stats)

    manual_results[name] = {
        "edges": edges,
        "bins": bins,
        "stats": stats,
        "score": score
    }

    manual_summaries.append(
        strategy_summary(name, stats)
    )

    show_statistics(stats)

    print(
        f"\nRozpietosc survival rate: "
        f"{score * 100:.2f} p.p."
    )

    print()

    text_chart(stats)


section("POROWNANIE ZESTAWOW GRANIC")

manual_comparison = pd.DataFrame(
    manual_summaries
).sort_values(
    "Rozpietosc_pp",
    ascending=False
).reset_index(drop=True)

print(
    manual_comparison
    .round(2)
    .to_string(index=False)
)


# Automatyczny wybor najlepszego zestawu
best_manual_name = max(
    manual_results,
    key=lambda name: manual_results[name]["score"]
)

best_manual = manual_results[best_manual_name]

best_manual_stats = best_manual["stats"]
best_manual_bins = best_manual["bins"]
best_manual_score = best_manual["score"]


section("NAJLEPSZY ZESTAW MANUAL OPTIMIZATION")

print(f"Zwyciezca: {best_manual_name}")
print(f"Granice: {best_manual['edges']}")

print(
    f"Rozpietosc survival rate: "
    f"{best_manual_score * 100:.2f} p.p."
)

print()

show_statistics(best_manual_stats)


# =========================================================
# POROWNANIE WSZYSTKICH STRATEGII
# =========================================================

strategies = {
    "Equal-width": {
        "bins": equal_width_bins,
        "stats": equal_width_stats,
        "score": equal_width_score
    },
    "Equal-frequency": {
        "bins": equal_frequency_bins,
        "stats": equal_frequency_stats,
        "score": equal_frequency_score
    },
    "Manual optimization": {
        "bins": best_manual_bins,
        "stats": best_manual_stats,
        "score": best_manual_score
    }
}


section("POROWNANIE TRZECH STRATEGII")

comparison = pd.DataFrame([
    strategy_summary(name, result["stats"])
    for name, result in strategies.items()
])

comparison = comparison.sort_values(
    "Rozpietosc_pp",
    ascending=False
).reset_index(drop=True)

print(
    comparison
    .round(2)
    .to_string(index=False)
)


section("RANKING STRATEGII")

for position, row in comparison.iterrows():

    print(
        f"{position + 1}. "
        f"{row['Strategia']} - "
        f"{row['Rozpietosc_pp']:.2f} p.p."
    )


section("TEKSTOWE POROWNANIE STRATEGII")

print("Legenda: jeden znak = okolo 2 p.p.")

for _, row in comparison.iterrows():

    score_pp = row["Rozpietosc_pp"]

    bar = "█" * int(round(score_pp / 2))

    print(
        f"{row['Strategia']:<22} | "
        f"{bar:<50} "
        f"{score_pp:.2f} p.p."
    )


# Automatyczny wybor najlepszej strategii
best_strategy_name = max(
    strategies,
    key=lambda name: strategies[name]["score"]
)

best_strategy = strategies[best_strategy_name]

best_stats = best_strategy["stats"]
best_bins = best_strategy["bins"]
best_score = best_strategy["score"]


section("REKOMENDACJA NAJLEPSZEJ STRATEGII")

print(f"Najlepsza strategia: {best_strategy_name}")

print(
    f"Najwieksza rozpietosc: "
    f"{best_score * 100:.2f} p.p."
)

print(f"Liczba przedzialow: {len(best_stats)}")

print(
    "Minimalna liczebnosc przedzialu: "
    f"{best_stats['Liczba_pasazerow'].min()}"
)

print(
    "Maksymalna liczebnosc przedzialu: "
    f"{best_stats['Liczba_pasazerow'].max()}"
)

print(
    "\nStrategia zostala wybrana automatycznie "
    "na podstawie najwiekszej rozpietosci "
    "survival rate."
)

if best_strategy_name == "Manual optimization":
    print(f"Najlepsze granice: {best_manual['edges']}")


section("NAJLEPSZY I NAJGORSZY PRZEDZIAL")

highest_bin = best_stats["Survival_Rate"].idxmax()
lowest_bin = best_stats["Survival_Rate"].idxmin()

highest_rate = best_stats.loc[
    highest_bin, "Survival_Rate_%"
]

lowest_rate = best_stats.loc[
    lowest_bin, "Survival_Rate_%"
]

print(f"Najwyzsza przezywalnosc: {highest_bin}")
print(f"Survival rate: {highest_rate:.2f}%")

print(f"\nNajnizsza przezywalnosc: {lowest_bin}")
print(f"Survival rate: {lowest_rate:.2f}%")

print(
    f"\nRoznica: "
    f"{highest_rate - lowest_rate:.2f} p.p."
)


# =========================================================
# ANALIZA STABILNOSCI
# =========================================================

section("ANALIZA LICZEBNOSCI PRZEDZIALOW")

# Dodatkowy prog diagnostyczny
minimum_group_size = 30

for name, result in strategies.items():

    counts = result["stats"]["Liczba_pasazerow"]

    small_groups = counts[
        counts < minimum_group_size
    ]

    print(f"\nStrategia: {name}")
    print(f"Najmniejsza grupa: {counts.min()}")
    print(f"Najwieksza grupa: {counts.max()}")
    print(f"Grupy ponizej 30 osob: {len(small_groups)}")

    if not small_groups.empty:
        print("Uwaga: male grupy moga dawac niestabilne wyniki.")
        print(small_groups.to_string())
    else:
        print("Wszystkie grupy maja co najmniej 30 osob.")


section("SREDNIA WAZONA SURVIVAL RATE")

weighted_rates = {}

for name, result in strategies.items():

    stats = result["stats"]

    weighted_rate = np.average(
        stats["Survival_Rate"],
        weights=stats["Liczba_pasazerow"]
    )

    weighted_rates[name] = weighted_rate

    print(f"{name:<22}: {weighted_rate * 100:.2f}%")

print(f"Globalna dla znanego wieku: {known_age_rate:.2f}%")


# =========================================================
# DODANIE NAJLEPSZEGO BINNINGU
# =========================================================

section("DODANIE NAJLEPSZEJ CECHY DO DATAFRAME")

df["Age_Dynamic_Bin"] = best_bins

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print("Nowa kolumna: Age_Dynamic_Bin")

print(
    f"Typ danych: "
    f"{df['Age_Dynamic_Bin'].dtype}"
)

print(
    f"Przypisane przedzialy: "
    f"{df['Age_Dynamic_Bin'].notna().sum()}"
)

print(
    f"Brakujace przedzialy: "
    f"{df['Age_Dynamic_Bin'].isna().sum()}"
)

print(
    df[
        ["PassengerId", "Age", "Age_Dynamic_Bin", "Survived"]
    ].head(20).to_string(index=False)
)


section("ROZKLAD NAJLEPSZYCH PRZEDZIALOW")

print(
    df["Age_Dynamic_Bin"]
    .value_counts(dropna=False, sort=False)
    .to_string()
)


section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum()
)

memory_after = (
    df.memory_usage(deep=True).sum()
)

print(f"Przed: {memory_before / 1024:.2f} KiB")
print(f"Po: {memory_after / 1024:.2f} KiB")

print(
    f"Wzrost: "
    f"{(memory_after - memory_before) / 1024:.2f} KiB"
)


section("DATA LEAKAGE - WAZNE W MACHINE LEARNING")

print(
    "1. Wybor granic wykorzystuje zmienna Survived."
)

print(
    "2. Optymalizacja na calym datasecie ma charakter "
    "eksploracyjny."
)

print(
    "3. W rzeczywistym ML granice nalezy dobierac "
    "wylacznie na danych treningowych."
)

print(
    "4. Dane walidacyjne i testowe powinny korzystac "
    "z wczesniej ustalonych granic."
)

print(
    "5. Nie wolno optymalizowac granic na danych testowych."
)

print(
    "6. Najwieksza rozpietosc survival rate nie gwarantuje "
    "najlepszej jakosci predykcji."
)

print(
    "7. Rozna liczba binow i male grupy moga faworyzowac "
    "niektore strategie."
)


section("WNIOSKI")

conclusions = [
    "Pd.cut tworzy przedzialy o rownej szerokosci.",
    "Pd.qcut tworzy grupy o zblizonej liczebnosci.",
    "Powtarzajace sie wartosci wieku moga zmieniac liczebnosci.",
    "Manual optimization testuje rozne zestawy granic.",
    "Mean zmiennej binarnej Survived wyznacza survival rate.",
    "Rozpietosc mierzy roznice pomiedzy skrajnymi grupami.",
    "Algorytm automatycznie wybiera najlepszy zestaw granic.",
    "Porownano trzy strategie binowania.",
    "Male grupy moga prowadzic do niestabilnych oszacowan.",
    "Brakujacy wiek pozostawiono jako NaN.",
    "Binning jest technika Feature Engineering.",
    "Wybor granic na podstawie targetu wymaga walidacji.",
    "Najlepsza strategia dotyczy przyjetego kryterium."
]

for number, conclusion in enumerate(
    conclusions, start=1
):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba analizowanych pasazerow: {len(data)}")
print(f"Liczba strategii: {len(strategies)}")
print(f"Liczba zestawow manualnych: {len(candidate_edges)}")
print("Laczna liczba testowanych konfiguracji: 5")
print(f"Najlepszy zestaw manualny: {best_manual_name}")
print(f"Najlepsza strategia: {best_strategy_name}")
print(f"Najlepszy wynik: {best_score * 100:.2f} p.p.")
print(f"Liczba najlepszych binow: {len(best_stats)}")
print(f"Shape koncowy: {df.shape}")


# =========================================================
# WERYFIKACJA
# =========================================================

section("WERYFIKACJA")

tests = {}


tests["Dataset ma 891 wierszy"] = (
    len(df_original) == 891
)

tests["Dataset ma poczatkowo 12 kolumn"] = (
    df_original.shape[1] == 12
)

tests["Istnieje 714 znanych wartosci wieku"] = (
    len(data) == 714
)

tests["Istnieje 177 brakujacych wartosci wieku"] = (
    df_original["Age"].isna().sum() == 177
)

tests["Survived jest zmienna binarna"] = (
    set(data["Survived"].unique()) == {0, 1}
)

tests["Equal-width tworzy 5 binow"] = (
    len(equal_width_stats) == 5
)

tests["Equal-frequency tworzy 5 binow"] = (
    len(equal_frequency_stats) == 5
)

tests["Przetestowano 3 zestawy manualne"] = (
    len(manual_results) == 3
)

tests["Porownano 3 strategie"] = (
    len(comparison) == 3
)

tests["Wszystkie granice sa rosnace"] = all(
    np.all(np.diff(edges) > 0)
    for edges in candidate_edges.values()
)

tests["Zestawy manualne obejmuja wszystkie dane"] = all(
    result["bins"].notna().all()
    for result in manual_results.values()
)

tests["Najlepszy zestaw manualny wybrano poprawnie"] = (
    np.isclose(
        best_manual_score,
        max(
            result["score"]
            for result in manual_results.values()
        )
    )
)

tests["Najlepsza strategie wybrano poprawnie"] = (
    np.isclose(
        best_score,
        max(
            result["score"]
            for result in strategies.values()
        )
    )
)

tests["Ranking strategii jest poprawny"] = (
    comparison["Rozpietosc_pp"]
    .is_monotonic_decreasing
)

tests["Ranking zestawow manualnych jest poprawny"] = (
    manual_comparison["Rozpietosc_pp"]
    .is_monotonic_decreasing
)


for name, result in strategies.items():

    stats = result["stats"]
    bins = result["bins"]
    score = result["score"]

    tests[f"{name}: wszystkie osoby przypisane"] = (
        bins.notna().all()
    )

    tests[f"{name}: zachowano liczebnosc"] = (
        stats["Liczba_pasazerow"].sum() == len(data)
    )

    tests[f"{name}: poprawna liczba ocalalych"] = (
        stats["Przezyli"].sum()
        == data["Survived"].sum()
    )

    tests[f"{name}: survival rate w zakresie 0-1"] = (
        stats["Survival_Rate"].between(0, 1).all()
    )

    tests[f"{name}: survival rate bez NaN"] = (
        stats["Survival_Rate"].notna().all()
    )

    tests[f"{name}: poprawna rozpietosc"] = (
        np.isclose(
            score,
            stats["Survival_Rate"].max()
            - stats["Survival_Rate"].min()
        )
    )

    tests[f"{name}: rozpietosc w zakresie 0-1"] = (
        0 <= score <= 1
    )

    tests[f"{name}: poprawna srednia wazona"] = (
        np.isclose(
            weighted_rates[name],
            data["Survived"].mean()
        )
    )

    tests[f"{name}: poprawne liczebnosci grup"] = (
        (
            stats["Przezyli"]
            + stats["Nie_przezyli"]
            == stats["Liczba_pasazerow"]
        ).all()
    )

    tests[f"{name}: survival i mortality daja 100"] = (
        np.allclose(
            stats["Survival_Rate_%"]
            + stats["Mortality_Rate_%"],
            100
        )
    )


tests["Dodano kolumne Age_Dynamic_Bin"] = (
    "Age_Dynamic_Bin" in df.columns
)

tests["Dodano tylko jedna kolumne"] = (
    df.shape[1] == df_original.shape[1] + 1
)

tests["Wynik ma shape (891, 13)"] = (
    df.shape == (891, 13)
)

tests["Nowa kolumna ma typ category"] = (
    isinstance(
        df["Age_Dynamic_Bin"].dtype,
        pd.CategoricalDtype
    )
)

tests["Przypisano 714 przedzialow"] = (
    df["Age_Dynamic_Bin"].notna().sum() == 714
)

tests["Pozostalo 177 brakujacych przedzialow"] = (
    df["Age_Dynamic_Bin"].isna().sum() == 177
)

tests["Braki odpowiadaja brakujacemu wiekowi"] = (
    df["Age_Dynamic_Bin"].isna().equals(
        df["Age"].isna()
    )
)

tests["Zachowano wszystkie indeksy"] = (
    df.index.equals(df_original.index)
)

tests["Zachowano wszystkich pasazerow"] = (
    len(df) == len(df_original)
)

tests["Istniejace kolumny pozostaly niezmienione"] = (
    df[df_original.columns].equals(df_original)
)

for name, passed in tests.items():
    print(f"Czy {name}: {bool(passed)}")

passed_tests = sum(
    bool(value) for value in tests.values()
)

total_tests = len(tests)

print(f"\nZaliczone testy: {passed_tests}/{total_tests}")

if passed_tests == total_tests:
    print("Wszystkie testy zakonczone pomyslnie.")
else:
    print("Nie wszystkie testy zostaly zaliczone.")

assert all(tests.values()), "Blad weryfikacji wynikow."
