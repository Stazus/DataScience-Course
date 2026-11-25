# Lekcja 12 - Zadanie 6: Feature Engineering - Family Size

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia danych do weryfikacji
df_original = df.copy()

print("=" * 75)
print("FEATURE ENGINEERING - FAMILY SIZE - TITANIC")
print("=" * 75)


# ============================================================
# 1. Dane wejsciowe
# ============================================================

section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Brakujace SibSp: {df['SibSp'].isna().sum()}")
print(f"Brakujace Parch: {df['Parch'].isna().sum()}")


section("PIERWSZE 10 REKORDOW PRZED TRANSFORMACJA")

print(
    df[
        ["PassengerId", "SibSp", "Parch", "Survived"]
    ].head(10).to_string(index=False)
)


# ============================================================
# 2. Feature Engineering - Family_Size
# ============================================================

df["Family_Size"] = df["SibSp"] + df["Parch"] + 1


section("DEFINICJA FAMILY_SIZE")

print("Family_Size = SibSp + Parch + 1")
print("SibSp - rodzenstwo i wspolmalzonkowie")
print("Parch - rodzice i dzieci")
print("1 - sam pasazer")


section("PIERWSZE 10 REKORDOW PO TRANSFORMACJI")

print(
    df[
        [
            "PassengerId",
            "SibSp",
            "Parch",
            "Family_Size",
            "Survived"
        ]
    ].head(10).to_string(index=False)
)


section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print("Nowa kolumna: Family_Size")
print(f"Typ danych: {df['Family_Size'].dtype}")
print(f"Brakujace wartosci: {df['Family_Size'].isna().sum()}")


# ============================================================
# 3. Statystyki rozmiaru rodziny
# ============================================================

section("STATYSTYKI FAMILY_SIZE")

print(df["Family_Size"].describe().round(2))


section("LICZEBNOSC WEDLUG ROZMIARU RODZINY")

family_counts = (
    df["Family_Size"]
    .value_counts()
    .sort_index()
)

print(family_counts.to_string())


# ============================================================
# 4. Survival rate wedlug rozmiaru rodziny
# ============================================================

survival_rate = (
    df.groupby("Family_Size")["Survived"]
    .mean()
    .mul(100)
)


section("SURVIVAL RATE WEDLUG ROZMIARU RODZINY")

print(survival_rate.round(2).to_string())


# ============================================================
# 5. Szczegolowe statystyki
# ============================================================

family_stats = (
    df.groupby("Family_Size")
    .agg(
        Liczba_pasazerow=("Survived", "size"),
        Przezyli=("Survived", "sum"),
        Przezywalnosc=("Survived", "mean")
    )
)

family_stats["Nie_przezyli"] = (
    family_stats["Liczba_pasazerow"]
    - family_stats["Przezyli"]
)

family_stats["Przezywalnosc_%"] = (
    family_stats["Przezywalnosc"] * 100
)

family_stats["Smiertelnosc_%"] = (
    100 - family_stats["Przezywalnosc_%"]
)

family_stats["Udzial_pasazerow_%"] = (
    family_stats["Liczba_pasazerow"] / len(df) * 100
)

family_stats = family_stats[
    [
        "Liczba_pasazerow",
        "Przezyli",
        "Nie_przezyli",
        "Przezywalnosc_%",
        "Smiertelnosc_%",
        "Udzial_pasazerow_%"
    ]
]


section("SZCZEGOLOWE STATYSTYKI WEDLUG FAMILY_SIZE")

print(family_stats.round(2).to_string())


# ============================================================
# 6. Tekstowy wykres przezywalnosci
# ============================================================

section("TEKSTOWY WYKRES PRZEZYWALNOSCI")

print("Legenda: jeden znak █ = okolo 2%")

for family_size, rate in survival_rate.items():

    bar = "█" * int(round(rate / 2))

    print(
        f"Rozmiar {family_size:>2} | "
        f"{bar:<50} {rate:6.2f}%"
    )


# ============================================================
# 7. Tekstowy wykres liczebnosci
# ============================================================

section("TEKSTOWY WYKRES LICZEBNOSCI")

print("Legenda: jeden znak █ = okolo 10 pasazerow")

for family_size, count in family_counts.items():

    bar = "█" * max(1, int(round(count / 10)))

    print(
        f"Rozmiar {family_size:>2} | "
        f"{bar:<55} {count:>4}"
    )


# ============================================================
# 8. Ranking rozmiarow rodzin
# ============================================================

ranking = family_stats.sort_values(
    "Przezywalnosc_%",
    ascending=False
)


section("RANKING WEDLUG PRZEZYWALNOSCI")

print(
    ranking[
        [
            "Liczba_pasazerow",
            "Przezyli",
            "Przezywalnosc_%"
        ]
    ].round(2).to_string()
)


best_rate = survival_rate.max()
worst_rate = survival_rate.min()

best_sizes = survival_rate.index[
    np.isclose(survival_rate, best_rate)
].tolist()

worst_sizes = survival_rate.index[
    np.isclose(survival_rate, worst_rate)
].tolist()


section("NAJWYZSZA I NAJNIZSZA PRZEZYWALNOSC")

print(f"Najlepsze rozmiary rodzin: {best_sizes}")
print(f"Najwyzsza przezywalnosc: {best_rate:.2f}%")

for size in best_sizes:
    print(
        f"Rozmiar {size}: "
        f"{family_counts.loc[size]} pasazerow"
    )

print(f"\nNajgorsze rozmiary rodzin: {worst_sizes}")
print(f"Najnizsza przezywalnosc: {worst_rate:.2f}%")
print(f"Roznica: {best_rate - worst_rate:.2f} p.p.")


# ============================================================
# 9. Pasazerowie samotni i z rodzina
# ============================================================

alone = df[df["Family_Size"] == 1]
with_family = df[df["Family_Size"] > 1]

comparison = pd.DataFrame({
    "Grupa": [
        "Samotni",
        "Z rodzina"
    ],
    "Liczba_pasazerow": [
        len(alone),
        len(with_family)
    ],
    "Przezyli": [
        alone["Survived"].sum(),
        with_family["Survived"].sum()
    ],
    "Przezywalnosc_%": [
        alone["Survived"].mean() * 100,
        with_family["Survived"].mean() * 100
    ]
})


section("SAMOTNI A PODROZUJACY Z RODZINA")

print(comparison.round(2).to_string(index=False))


section("TEKSTOWY WYKRES - SAMOTNI A Z RODZINA")

print("Legenda: jeden znak █ = okolo 2%")

for group, rate in zip(
    comparison["Grupa"],
    comparison["Przezywalnosc_%"]
):

    bar = "█" * int(round(rate / 2))

    print(f"{group:<12} | {bar:<50} {rate:6.2f}%")


# ============================================================
# 10. Tabela przestawna
# ============================================================

pivot = (
    df.groupby(["Family_Size", "Survived"])
    .size()
    .unstack(fill_value=0)
    .rename(
        columns={
            0: "Nie_przezyli",
            1: "Przezyli"
        }
    )
)


section("TABELA PRZESTAWNA - FAMILY_SIZE I SURVIVED")

print(pivot.to_string())


# ============================================================
# 11. Porownanie z globalna przezywalnoscia
# ============================================================

global_survival = df["Survived"].mean() * 100

comparison_global = family_stats[
    ["Liczba_pasazerow", "Przezywalnosc_%"]
].copy()

comparison_global["Roznica_od_globalnej_pp"] = (
    comparison_global["Przezywalnosc_%"]
    - global_survival
)


section("POROWNANIE Z GLOBALNA PRZEZYWALNOSCIA")

print(f"Globalna przezywalnosc: {global_survival:.2f}%\n")

print(comparison_global.round(2).to_string())


# ============================================================
# 12. Srednia wazona przezywalnosci
# ============================================================

weighted_survival = np.average(
    survival_rate.to_numpy(),
    weights=family_counts.reindex(
        survival_rate.index
    ).to_numpy()
)


section("WERYFIKACJA GLOBALNEJ PRZEZYWALNOSCI")

print(f"Globalna przezywalnosc: {global_survival:.4f}%")
print(f"Srednia wazona grup: {weighted_survival:.4f}%")


# ============================================================
# 13. Zuzycie pamieci
# ============================================================

memory_before = (
    df_original.memory_usage(deep=True).sum() / 1024
)

memory_after = (
    df.memory_usage(deep=True).sum() / 1024
)


section("ZUZYCIE PAMIECI")

print(f"Przed: {memory_before:.2f} KiB")
print(f"Po: {memory_after:.2f} KiB")
print(f"Wzrost: {memory_after - memory_before:.2f} KiB")


# ============================================================
# 14. Wnioski
# ============================================================

section("WNIOSKI")

conclusions = [
    "Feature Engineering pozwala tworzyc nowe cechy.",
    "Family_Size laczy informacje z SibSp i Parch.",
    "Dodanie 1 uwzglednia samego pasazera.",
    "Family_Size = 1 oznacza brak krewnych liczonych przez SibSp i Parch.",
    "GroupBy pozwala analizowac rozne rozmiary rodzin.",
    "Mean kolumny Survived wyznacza survival rate.",
    "Rozmiar rodziny wykazuje zwiazek z przezywalnoscia.",
    "Liczebnosc grup ma znaczenie dla interpretacji.",
    "Mala grupa moze miec niestabilny survival rate.",
    "Family_Size moze stanowic ceche modelu ML.",
    "Zaleznosc statystyczna nie dowodzi przyczynowosci.",
    "Liczebnosc grup oznacza liczbe pasazerow, nie odrebnych rodzin."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


# ============================================================
# 15. Podsumowanie
# ============================================================

section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(df)}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print("Nowa kolumna: Family_Size")
print(f"Liczba rozmiarow rodzin: {df['Family_Size'].nunique()}")
print(f"Minimalny rozmiar: {df['Family_Size'].min()}")
print(f"Maksymalny rozmiar: {df['Family_Size'].max()}")
print(f"Pasazerowie samotni: {len(alone)}")
print(f"Pasazerowie z rodzina: {len(with_family)}")
print(f"Najlepsze rozmiary rodzin: {best_sizes}")
print(f"Najwyzsza przezywalnosc: {best_rate:.2f}%")


# ============================================================
# 16. Automatyczna weryfikacja
# ============================================================

section("WERYFIKACJA")

expected_counts = {
    1: 537,
    2: 161,
    3: 102,
    4: 29,
    5: 15,
    6: 22,
    7: 12,
    8: 6,
    11: 7
}

manual_survival = (
    family_stats["Przezyli"]
    / family_stats["Liczba_pasazerow"]
    * 100
)

tests = {
    "Dataset ma 891 wierszy":
        len(df) == 891,

    "Dataset mial poczatkowo 12 kolumn":
        df_original.shape[1] == 12,

    "Dodano kolumne Family_Size":
        "Family_Size" in df.columns,

    "Wynik ma shape (891, 13)":
        df.shape == (891, 13),

    "Dodano tylko jedna kolumne":
        set(df.columns) - set(df_original.columns)
        == {"Family_Size"},

    "Family_Size obliczono poprawnie":
        df["Family_Size"].equals(
            df["SibSp"] + df["Parch"] + 1
        ),

    "Family_Size ma typ calkowity":
        pd.api.types.is_integer_dtype(df["Family_Size"]),

    "Family_Size nie zawiera NaN":
        not df["Family_Size"].isna().any(),

    "Family_Size jest dodatnie":
        df["Family_Size"].gt(0).all(),

    "Minimalny rozmiar wynosi 1":
        df["Family_Size"].min() == 1,

    "Maksymalny rozmiar wynosi 11":
        df["Family_Size"].max() == 11,

    "Istnieje 9 rozmiarow rodzin":
        df["Family_Size"].nunique() == 9,

    "Liczebnosci grup sa poprawne":
        family_counts.to_dict() == expected_counts,

    "Uwzgledniono wszystkich pasazerow":
        family_counts.sum() == len(df),

    "Pasazerow samotnych jest 537":
        len(alone) == 537,

    "Pasazerow z rodzina jest 354":
        len(with_family) == 354,

    "Obie grupy obejmuja wszystkich pasazerow":
        len(alone) + len(with_family) == len(df),

    "Survival rate obliczono poprawnie":
        np.allclose(survival_rate, manual_survival),

    "Przezywalnosc jest w zakresie 0-100":
        survival_rate.between(0, 100).all(),

    "Liczba ocalalych wynosi 342":
        family_stats["Przezyli"].sum() == 342,

    "Liczba ofiar wynosi 549":
        family_stats["Nie_przezyli"].sum() == 549,

    "Przezyli i nie przezyli daja liczebnosc":
        (
            family_stats["Przezyli"]
            + family_stats["Nie_przezyli"]
            == family_stats["Liczba_pasazerow"]
        ).all(),

    "Przezywalnosc i smiertelnosc daja 100":
        np.allclose(
            family_stats["Przezywalnosc_%"]
            + family_stats["Smiertelnosc_%"],
            100
        ),

    "Udzialy grup sumuja sie do 100":
        np.isclose(
            family_stats["Udzial_pasazerow_%"].sum(),
            100
        ),

    "Najwyzsza przezywalnosc ma rozmiar 4":
        best_sizes == [4],

    "Ranking jest poprawnie posortowany":
        ranking["Przezywalnosc_%"].is_monotonic_decreasing,

    "Tabela pivot ma shape (9, 2)":
        pivot.shape == (9, 2),

    "Tabela pivot uwzglednia wszystkich pasazerow":
        pivot.to_numpy().sum() == len(df),

    "Srednia wazona jest poprawna":
        np.isclose(weighted_survival, global_survival),

    "Zachowano wszystkie indeksy":
        df.index.equals(df_original.index),

    "Istniejace kolumny pozostaly niezmienione":
        df[df_original.columns].equals(df_original)
}

for description, result in tests.items():
    print(f"Czy {description}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

if all(tests.values()):
    print("Wszystkie testy zakonczone pomyslnie.")
else:
    print("Nie wszystkie testy zostaly zaliczone.")

