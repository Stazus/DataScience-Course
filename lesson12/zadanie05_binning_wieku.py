# Lekcja 12 - Zadanie 5: Binning wieku

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
print("BINNING WIEKU - DATASET TITANIC")
print("=" * 75)


# Informacje o danych wejsciowych
section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Znany wiek: {df['Age'].notna().sum()}")
print(f"Brakujacy wiek: {df['Age'].isna().sum()}")


# Statystyki wieku
section("STATYSTYKI WIEKU PRZED BINNINGIEM")

print(df["Age"].describe().round(2))


# Definicja przedzialow wiekowych
bins = [0, 12, 18, 60, np.inf]

labels = [
    "Dziecko",
    "Nastolatek",
    "Dorosły",
    "Senior"
]


section("DEFINICJA KATEGORII WIEKOWYCH")

intervals = pd.DataFrame({
    "Kategoria": labels,
    "Przedzial": [
        "[0, 12]",
        "(12, 18]",
        "(18, 60]",
        "(60, inf)"
    ]
})

print(intervals.to_string(index=False))


# Glowna operacja - binning wieku
df["Age_Category"] = pd.cut(
    df["Age"],
    bins=bins,
    labels=labels,
    include_lowest=True,
    right=True
)


# Pierwsze rekordy po transformacji
section("PIERWSZE 10 REKORDOW PO BINNINGU")

columns = [
    "PassengerId",
    "Age",
    "Age_Category",
    "Survived"
]

print(
    df[columns]
    .head(10)
    .to_string(index=False)
)


# Informacje o nowej kolumnie
section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print("Nowa kolumna: Age_Category")
print(f"Typ danych: {df['Age_Category'].dtype}")

print(
    "Kategorie:",
    df["Age_Category"].cat.categories.tolist()
)

print(
    "Kategorie uporzadkowane:",
    df["Age_Category"].cat.ordered
)


# Rozklad kategorii wiekowych
section("LICZEBNOSC KATEGORII WIEKOWYCH")

age_counts = (
    df["Age_Category"]
    .value_counts(sort=False, dropna=False)
)

print(age_counts.to_string())


# Obliczenie survival rate
section("SURVIVAL RATE WEDLUG KATEGORII WIEKOWEJ")

survival_rate = (
    df.groupby("Age_Category", observed=False)
    ["Survived"]
    .mean()
    * 100
)

print(survival_rate.round(2).to_string())


# Szczegolowe statystyki grupowe
section("SZCZEGOLOWE STATYSTYKI KATEGORII")

age_stats = df.groupby(
    "Age_Category",
    observed=False
).agg(
    Liczba_pasazerow=("Survived", "size"),
    Przezyli=("Survived", "sum"),
    Przezywalnosc=("Survived", "mean"),
    Sredni_wiek=("Age", "mean"),
    Min_wiek=("Age", "min"),
    Max_wiek=("Age", "max")
)

age_stats["Nie_przezyli"] = (
    age_stats["Liczba_pasazerow"]
    - age_stats["Przezyli"]
)

age_stats["Przezywalnosc_%"] = (
    age_stats["Przezywalnosc"] * 100
)

age_stats["Smiertelnosc_%"] = (
    100 - age_stats["Przezywalnosc_%"]
)

result_columns = [
    "Liczba_pasazerow",
    "Przezyli",
    "Nie_przezyli",
    "Przezywalnosc_%",
    "Smiertelnosc_%",
    "Sredni_wiek",
    "Min_wiek",
    "Max_wiek"
]

print(
    age_stats[result_columns]
    .round(2)
    .to_string()
)


# Tekstowy wykres przezywalnosci
section("TEKSTOWY WYKRES PRZEZYWALNOSCI")

print("Legenda: jeden znak = okolo 2%")

for category, rate in survival_rate.items():
    bar = "█" * int(round(rate / 2))

    print(
        f"{category:<12} | "
        f"{bar:<50} {rate:6.2f}%"
    )


# Tekstowy wykres liczebnosci
section("TEKSTOWY WYKRES LICZEBNOSCI")

print("Legenda: jeden znak = okolo 10 pasazerow")

for category, row in age_stats.iterrows():
    count = int(row["Liczba_pasazerow"])

    bar = "█" * int(round(count / 10))

    print(
        f"{category:<12} | "
        f"{bar:<60} {count:4d}"
    )


# Tabela przestawna
section("TABELA PRZESTAWNA - WIEK I SURVIVED")

pivot = (
    df.groupby(
        ["Age_Category", "Survived"],
        observed=False
    )
    .size()
    .unstack(fill_value=0)
)

pivot = pivot.rename(columns={
    0: "Nie_przezyli",
    1: "Przezyli"
})

print(pivot.to_string())


# Analiza brakujacych wartosci wieku
section("ANALIZA BRAKUJACEGO WIEKU")

known_age = df[df["Age"].notna()]
unknown_age = df[df["Age"].isna()]

missing_age_count = len(unknown_age)

known_survival = (
    known_age["Survived"].mean() * 100
)

unknown_survival = (
    unknown_age["Survived"].mean() * 100
)

print(f"Pasazerowie ze znanym wiekiem: {len(known_age)}")
print(f"Pasazerowie bez wieku: {missing_age_count}")

print(
    f"Procent brakujacego wieku: "
    f"{missing_age_count / len(df) * 100:.2f}%"
)

print(
    f"Przezywalnosc przy znanym wieku: "
    f"{known_survival:.2f}%"
)

print(
    f"Przezywalnosc przy nieznanym wieku: "
    f"{unknown_survival:.2f}%"
)

print(
    "\nPasazerowie bez wieku nie zostali "
    "przypisani do kategorii wiekowych."
)


# Ranking kategorii
section("RANKING KATEGORII WEDLUG PRZEZYWALNOSCI")

ranking = age_stats[
    [
        "Liczba_pasazerow",
        "Przezyli",
        "Przezywalnosc_%"
    ]
].sort_values(
    "Przezywalnosc_%",
    ascending=False
)

print(ranking.round(2).to_string())


# Porownanie kategorii
section("POROWNANIE KATEGORII WIEKOWYCH")

best_category = survival_rate.idxmax()
worst_category = survival_rate.idxmin()

best_rate = survival_rate.max()
worst_rate = survival_rate.min()

difference = best_rate - worst_rate

largest_category = (
    age_stats["Liczba_pasazerow"].idxmax()
)

smallest_category = (
    age_stats["Liczba_pasazerow"].idxmin()
)

print(
    f"Najwyzsza przezywalnosc: "
    f"{best_category} - {best_rate:.2f}%"
)

print(
    f"Najnizsza przezywalnosc: "
    f"{worst_category} - {worst_rate:.2f}%"
)

print(f"Roznica: {difference:.2f} p.p.")
print(f"Najliczniejsza kategoria: {largest_category}")
print(f"Najmniej liczna kategoria: {smallest_category}")


# Porownanie sredniej wazonej
section("WERYFIKACJA GLOBALNEJ PRZEZYWALNOSCI")

global_survival = df["Survived"].mean() * 100

weighted_survival = np.average(
    survival_rate,
    weights=age_stats["Liczba_pasazerow"]
)

print(
    f"Przezywalnosc wszystkich pasazerow: "
    f"{global_survival:.2f}%"
)

print(
    f"Przezywalnosc pasazerow ze znanym wiekiem: "
    f"{known_survival:.2f}%"
)

print(
    f"Srednia wazona kategorii: "
    f"{weighted_survival:.2f}%"
)


# Testowanie granic przedzialow
section("TEST GRANIC PRZEDZIALOW")

boundary_ages = pd.Series([
    0,
    0.42,
    12,
    12.5,
    13,
    18,
    18.5,
    19,
    60,
    60.5,
    61,
    80,
    np.nan
])

boundary_categories = pd.cut(
    boundary_ages,
    bins=bins,
    labels=labels,
    include_lowest=True,
    right=True
)

boundary_results = pd.DataFrame({
    "Wiek": boundary_ages,
    "Kategoria": boundary_categories
})

print(boundary_results.to_string(index=False))


# Porownanie zuzycia pamieci
section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum()
)

memory_after = (
    df.memory_usage(deep=True).sum()
)

memory_category = (
    df["Age_Category"]
    .memory_usage(index=False, deep=True)
)

print(f"Przed: {memory_before / 1024:.2f} KiB")
print(f"Po: {memory_after / 1024:.2f} KiB")

print(
    f"Nowa kolumna: "
    f"{memory_category / 1024:.2f} KiB"
)

print(
    f"Wzrost pamieci: "
    f"{(memory_after - memory_before) / 1024:.2f} KiB"
)


# Wnioski
section("WNIOSKI")

conclusions = [
    "Binning zamienia wartosci liczbowe na kategorie.",
    "Pd.cut pozwala definiowac wlasne przedzialy.",
    "Utworzono cztery uporzadkowane kategorie wieku.",
    "Mean kolumny Survived wyznacza survival rate.",
    "Mnozenie przez 100 zamienia wskaznik na procenty.",
    "Brakujace wartosci wieku pozostawiono jako NaN.",
    "Binning ulatwia porownywanie grup wiekowych.",
    "Typ category jest korzystny pamieciowo.",
    "Binning powoduje utrate czesci informacji o wieku.",
    "Liczebnosc grup ma znaczenie dla interpretacji.",
    "Zaleznosc wieku i przezycia nie dowodzi przyczynowosci.",
    "Binning jest przykladem Feature Engineering."
]

for number, conclusion in enumerate(conclusions, 1):
    print(f"{number}. {conclusion}")


# Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kategorii: {len(labels)}")

print(
    f"Przypisane kategorie: "
    f"{df['Age_Category'].notna().sum()}"
)

print(
    f"Nieprzypisane kategorie: "
    f"{df['Age_Category'].isna().sum()}"
)

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")

print(
    f"Najwyzsza przezywalnosc: "
    f"{best_category} - {best_rate:.2f}%"
)

print(
    f"Najnizsza przezywalnosc: "
    f"{worst_category} - {worst_rate:.2f}%"
)


# Niezalezna weryfikacja kategorii
age = df["Age"]

expected_masks = {
    "Dziecko": age.ge(0) & age.le(12),
    "Nastolatek": age.gt(12) & age.le(18),
    "Dorosły": age.gt(18) & age.le(60),
    "Senior": age.gt(60)
}

expected_counts = np.array([
    mask.sum()
    for mask in expected_masks.values()
])

expected_rates = np.array([
    df.loc[mask, "Survived"].mean() * 100
    for mask in expected_masks.values()
])

expected_boundary_categories = [
    "Dziecko",
    "Dziecko",
    "Dziecko",
    "Nastolatek",
    "Nastolatek",
    "Nastolatek",
    "Dorosły",
    "Dorosły",
    "Dorosły",
    "Senior",
    "Senior",
    "Senior"
]


# Testy poprawnosci
section("WERYFIKACJA")

tests = {
    "Dataset ma 891 wierszy":
        len(df_original) == 891,

    "Dataset ma poczatkowo 12 kolumn":
        df_original.shape[1] == 12,

    "Dodano kolumne Age_Category":
        "Age_Category" in df.columns,

    "Wynik ma shape (891, 13)":
        df.shape == (891, 13),

    "Nowa kolumna ma typ category":
        isinstance(
            df["Age_Category"].dtype,
            pd.CategoricalDtype
        ),

    "Istnieja 4 kategorie":
        len(df["Age_Category"].cat.categories) == 4,

    "Kategorie maja poprawne nazwy":
        df["Age_Category"].cat.categories.tolist()
        == labels,

    "Kategorie sa uporzadkowane":
        df["Age_Category"].cat.ordered,

    "Przypisano 714 pasazerow":
        df["Age_Category"].notna().sum() == 714,

    "Pozostalo 177 brakujacych kategorii":
        df["Age_Category"].isna().sum() == 177,

    "Braki kategorii odpowiadaja brakom wieku":
        df["Age_Category"].isna().equals(
            df["Age"].isna()
        ),

    "Wszystkie kategorie sa reprezentowane":
        age_stats["Liczba_pasazerow"].gt(0).all(),

    "Liczebnosci kategorii sa poprawne":
        np.array_equal(
            age_stats["Liczba_pasazerow"].to_numpy(),
            expected_counts
        ),

    "Przezywalnosc obliczono poprawnie":
        np.allclose(
            survival_rate.to_numpy(),
            expected_rates
        ),

    "Przezywalnosc jest w zakresie 0-100":
        survival_rate.between(0, 100).all(),

    "Suma liczebnosci kategorii wynosi 714":
        age_stats["Liczba_pasazerow"].sum() == 714,

    "Uwzgledniono wszystkich pasazerow":
        age_stats["Liczba_pasazerow"].sum()
        + missing_age_count == len(df),

    "Liczba ocalalych jest zgodna":
        age_stats["Przezyli"].sum()
        == known_age["Survived"].sum(),

    "Przezyli i nie przezyli daja liczebnosc":
        (
            age_stats["Przezyli"]
            + age_stats["Nie_przezyli"]
        ).equals(age_stats["Liczba_pasazerow"]),

    "Przezywalnosc i smiertelnosc daja 100":
        np.allclose(
            age_stats["Przezywalnosc_%"]
            + age_stats["Smiertelnosc_%"],
            100
        ),

    "Tabela pivot ma shape (4, 2)":
        pivot.shape == (4, 2),

    "Tabela pivot uwzglednia 714 pasazerow":
        pivot.to_numpy().sum() == 714,

    "Srednia wazona jest poprawna":
        np.isclose(
            weighted_survival,
            known_survival
        ),

    "Granice przedzialow sa poprawne":
        boundary_categories.iloc[:-1].tolist()
        == expected_boundary_categories,

    "NaN pozostaje NaN":
        pd.isna(boundary_categories.iloc[-1]),

    "Ranking jest poprawnie posortowany":
        ranking["Przezywalnosc_%"]
        .is_monotonic_decreasing,

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
    raise AssertionError(
        "Nie wszystkie testy zostaly zaliczone."
    )
