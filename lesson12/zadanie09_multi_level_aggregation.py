# Lekcja 12 - Zadanie 9: Multi-Level Aggregation

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
print("MULTI-LEVEL AGGREGATION - DATASET TITANIC")
print("=" * 75)


# Informacje o danych
section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Liczba klas: {df['Pclass'].nunique()}")
print(f"Brakujacy wiek: {df['Age'].isna().sum()}")


# Feature Engineering
section("TWORZENIE KOLUMNY IS_ALONE")

df["Is_Alone"] = (
    df["SibSp"] + df["Parch"] == 0
)

print("Formula: Is_Alone = (SibSp + Parch == 0)")
print(f"Typ danych: {df['Is_Alone'].dtype}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")


# Pierwsze rekordy
section("PIERWSZE 10 REKORDOW")

columns = [
    "PassengerId",
    "Pclass",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Is_Alone",
    "Survived"
]

print(df[columns].head(10).to_string(index=False))


# Rozklad Is_Alone
section("ROZKLAD IS_ALONE")

alone_counts = df["Is_Alone"].value_counts()

alone_count = int(df["Is_Alone"].sum())
family_count = len(df) - alone_count

print(alone_counts.to_string())
print(f"\nPodrozujacy samotnie: {alone_count}")
print(f"Podrozujacy z rodzina: {family_count}")

print(
    f"Samotnie: "
    f"{alone_count / len(df) * 100:.2f}%"
)

print(
    f"Z rodzina: "
    f"{family_count / len(df) * 100:.2f}%"
)


# Grupowanie wielopoziomowe
group_columns = [
    "Pclass",
    "Sex",
    "Is_Alone"
]

grouped = df.groupby(group_columns)


# Podstawowa agregacja
section("MULTI-LEVEL AGGREGATION")

aggregation = grouped.agg(
    Avg_Age=("Age", "mean"),
    Survival_Rate=("Survived", "mean")
)

print(aggregation.round(4).to_string())

print(f"\nTyp indeksu: {type(aggregation.index).__name__}")
print(f"Liczba poziomow indeksu: {aggregation.index.nlevels}")
print(f"Liczba grup: {len(aggregation)}")


# Splaszczenie MultiIndex
section("TABELA WYNIKOWA - RESET_INDEX")

results = aggregation.reset_index()

# Zamiana survival rate na procenty
results["Survival_Rate"] *= 100

print(results.round(2).to_string(index=False))

print(f"\nShape: {results.shape}")
print(f"Typ indeksu: {type(results.index).__name__}")


# Szczegolowe statystyki
section("SZCZEGOLOWE STATYSTYKI GRUPOWE")

details = grouped.agg(
    Liczba_pasazerow=("PassengerId", "size"),
    Znany_wiek=("Age", "count"),
    Sredni_wiek=("Age", "mean"),
    Mediana_wieku=("Age", "median"),
    Min_wiek=("Age", "min"),
    Max_wiek=("Age", "max"),
    Przezyli=("Survived", "sum"),
    Przezywalnosc_pct=("Survived", "mean")
).reset_index()

details["Nie_przezyli"] = (
    details["Liczba_pasazerow"] - details["Przezyli"]
)

details["Brakujacy_wiek"] = (
    details["Liczba_pasazerow"] - details["Znany_wiek"]
)

details["Przezywalnosc_pct"] *= 100

details["Smiertelnosc_pct"] = (
    100 - details["Przezywalnosc_pct"]
)

print(details.round(2).to_string(index=False))


# Czytelna tabela
section("CZYTELNA TABELA WSZYSTKICH KOMBINACJI")

readable = details[[
    "Pclass",
    "Sex",
    "Is_Alone",
    "Liczba_pasazerow",
    "Sredni_wiek",
    "Przezyli",
    "Przezywalnosc_pct"
]].copy()

readable["Sex"] = readable["Sex"].map({
    "female": "Kobieta",
    "male": "Mezczyzna"
})

readable["Is_Alone"] = readable["Is_Alone"].map({
    True: "Samotnie",
    False: "Z rodzina"
})

print(readable.round(2).to_string(index=False))


# Tabela przestawna sredniego wieku
section("PIVOT TABLE - SREDNI WIEK")

pivot_age = results.pivot(
    index=["Pclass", "Sex"],
    columns="Is_Alone",
    values="Avg_Age"
)

pivot_age = pivot_age.rename(columns={
    False: "Z_rodzina",
    True: "Samotnie"
})

print(pivot_age.round(2).to_string())


# Tabela przestawna przezywalnosci
section("PIVOT TABLE - PRZEZYWALNOSC (%)")

pivot_survival = results.pivot(
    index=["Pclass", "Sex"],
    columns="Is_Alone",
    values="Survival_Rate"
)

pivot_survival = pivot_survival.rename(columns={
    False: "Z_rodzina",
    True: "Samotnie"
})

print(pivot_survival.round(2).to_string())


# Roznice przezywalnosci
section("ROZNICE PRZEZYWALNOSCI")

comparison = pivot_survival.copy()

comparison["Roznica_pp"] = (
    comparison["Z_rodzina"]
    - comparison["Samotnie"]
)

print(comparison.round(2).to_string())

print(
    "\nDodatnia roznica oznacza wyzsza przezywalnosc "
    "osob podrozujacych z rodzina."
)


# Tekstowy wykres przezywalnosci
section("TEKSTOWY WYKRES PRZEZYWALNOSCI")

print("Legenda: jeden znak = okolo 2%")

for _, row in results.iterrows():

    status = (
        "Samotnie"
        if row["Is_Alone"]
        else "Z rodzina"
    )

    label = (
        f"Klasa {row['Pclass']}, "
        f"{row['Sex']}, {status}"
    )

    rate = row["Survival_Rate"]
    bar = "█" * round(rate / 2)

    print(f"{label:<30} | {bar:<50} {rate:6.2f}%")


# Tekstowy wykres sredniego wieku
section("TEKSTOWY WYKRES SREDNIEGO WIEKU")

print("Legenda: jeden znak = okolo 1 roku")

for _, row in results.iterrows():

    status = (
        "Samotnie"
        if row["Is_Alone"]
        else "Z rodzina"
    )

    label = (
        f"Klasa {row['Pclass']}, "
        f"{row['Sex']}, {status}"
    )

    age = row["Avg_Age"]
    bar = "█" * round(age)

    print(f"{label:<30} | {bar:<50} {age:6.2f}")


# Ranking grup
section("RANKING GRUP WEDLUG PRZEZYWALNOSCI")

ranking = details.sort_values(
    "Przezywalnosc_pct",
    ascending=False
).reset_index(drop=True)

ranking.index = ranking.index + 1

ranking_columns = [
    "Pclass",
    "Sex",
    "Is_Alone",
    "Liczba_pasazerow",
    "Sredni_wiek",
    "Przezywalnosc_pct"
]

print(
    ranking[ranking_columns]
    .round(2)
    .to_string()
)


# Najlepsza i najgorsza grupa
section("POROWNANIE SKRAJNYCH GRUP")

best_group = ranking.iloc[0]
worst_group = ranking.iloc[-1]

print("Najwyzsza przezywalnosc:")
print(f"Klasa: {best_group['Pclass']}")
print(f"Plec: {best_group['Sex']}")
print(f"Is_Alone: {best_group['Is_Alone']}")
print(f"Liczba osob: {best_group['Liczba_pasazerow']}")
print(
    f"Przezywalnosc: "
    f"{best_group['Przezywalnosc_pct']:.2f}%"
)

print("\nNajnizsza przezywalnosc:")
print(f"Klasa: {worst_group['Pclass']}")
print(f"Plec: {worst_group['Sex']}")
print(f"Is_Alone: {worst_group['Is_Alone']}")
print(f"Liczba osob: {worst_group['Liczba_pasazerow']}")
print(
    f"Przezywalnosc: "
    f"{worst_group['Przezywalnosc_pct']:.2f}%"
)

difference = (
    best_group["Przezywalnosc_pct"]
    - worst_group["Przezywalnosc_pct"]
)

print(f"\nRoznica przezywalnosci: {difference:.2f} p.p.")


# Porownanie samotnych i podrozujacych z rodzina
section("PRZEZYWALNOSC WEDLUG IS_ALONE")

alone_summary = df.groupby("Is_Alone").agg(
    Liczba_pasazerow=("PassengerId", "size"),
    Sredni_wiek=("Age", "mean"),
    Przezyli=("Survived", "sum"),
    Przezywalnosc_pct=("Survived", "mean")
)

alone_summary["Przezywalnosc_pct"] *= 100

print(alone_summary.round(2).to_string())


# Porownanie globalnych srednich
section("WERYFIKACJA SREDNICH WAZONYCH")

global_age = df["Age"].mean()
global_survival = df["Survived"].mean() * 100

weighted_age = np.average(
    details["Sredni_wiek"],
    weights=details["Znany_wiek"]
)

weighted_survival = np.average(
    details["Przezywalnosc_pct"],
    weights=details["Liczba_pasazerow"]
)

print(f"Globalny sredni wiek: {global_age:.4f}")
print(f"Srednia wazona wieku: {weighted_age:.4f}")

print(
    f"\nGlobalna przezywalnosc: "
    f"{global_survival:.4f}%"
)

print(
    f"Srednia wazona przezywalnosci: "
    f"{weighted_survival:.4f}%"
)


# Analiza brakujacych danych
section("BRAKUJACE DANE W GRUPACH")

print(
    details[[
        "Pclass",
        "Sex",
        "Is_Alone",
        "Liczba_pasazerow",
        "Znany_wiek",
        "Brakujacy_wiek"
    ]].to_string(index=False)
)

print(
    f"\nSuma brakujacego wieku: "
    f"{details['Brakujacy_wiek'].sum()}"
)

print("Mean automatycznie pomija NaN.")


# Zuzycie pamieci
section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum() / 1024
)

memory_after = (
    df.memory_usage(deep=True).sum() / 1024
)

print(f"Przed: {memory_before:.2f} KiB")
print(f"Po: {memory_after:.2f} KiB")
print(f"Wzrost: {memory_after - memory_before:.2f} KiB")


# Wnioski
section("WNIOSKI")

conclusions = [
    "Feature Engineering pozwala tworzyc nowe cechy.",
    "Is_Alone jest cecha logiczna typu bool.",
    "GroupBy pozwala grupowac wedlug trzech kolumn.",
    "Powstalo 12 kombinacji grup.",
    "Agg pozwala wykonywac wiele agregacji jednoczesnie.",
    "Mean kolumny Survived wyznacza survival rate.",
    "Reset_index zamienia MultiIndex na zwykle kolumny.",
    "Pivot ulatwia porownywanie grup.",
    "Brakujacy wiek nie jest uwzgledniany w sredniej.",
    "Srednia wazona uwzglednia liczebnosci grup.",
    "Liczebnosc grup ma znaczenie dla interpretacji.",
    "Zaleznosc statystyczna nie dowodzi przyczynowosci.",
    "Is_Alone nie uwzglednia wszystkich towarzyszy podrozy."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


# Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba klas: {df['Pclass'].nunique()}")
print(f"Liczba grup: {len(results)}")
print(f"Podrozujacy samotnie: {alone_count}")
print(f"Podrozujacy z rodzina: {family_count}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print(f"Shape tabeli wynikowej: {results.shape}")
print(f"Globalny sredni wiek: {global_age:.2f}")
print(f"Globalna przezywalnosc: {global_survival:.2f}%")


# Weryfikacja wynikow
section("WERYFIKACJA")

# Niezalezna weryfikacja poszczegolnych grup
manual_results_correct = True

for _, row in results.iterrows():

    mask = (
        (df["Pclass"] == row["Pclass"])
        & (df["Sex"] == row["Sex"])
        & (df["Is_Alone"] == row["Is_Alone"])
    )

    subset = df.loc[mask]

    manual_age = subset["Age"].mean()
    manual_survival = subset["Survived"].mean() * 100

    if not np.isclose(row["Avg_Age"], manual_age):
        manual_results_correct = False

    if not np.isclose(
        row["Survival_Rate"],
        manual_survival
    ):
        manual_results_correct = False


tests = {
    "Dataset ma 891 wierszy":
        len(df) == 891,

    "Dataset ma poczatkowo 12 kolumn":
        df_original.shape[1] == 12,

    "Dodano kolumne Is_Alone":
        "Is_Alone" in df.columns,

    "Dodano tylko jedna kolumne":
        df.shape[1] == df_original.shape[1] + 1,

    "Wynik ma shape (891, 13)":
        df.shape == (891, 13),

    "Is_Alone ma typ bool":
        pd.api.types.is_bool_dtype(df["Is_Alone"]),

    "Is_Alone nie zawiera NaN":
        df["Is_Alone"].notna().all(),

    "Is_Alone obliczono poprawnie":
        df["Is_Alone"].equals(
            df["SibSp"] + df["Parch"] == 0
        ),

    "Istnieje 537 samotnych pasazerow":
        alone_count == 537,

    "Istnieje 354 pasazerow z rodzina":
        family_count == 354,

    "Utworzono 12 grup":
        len(aggregation) == 12,

    "Agregacja posiada MultiIndex":
        isinstance(aggregation.index, pd.MultiIndex),

    "MultiIndex ma 3 poziomy":
        aggregation.index.nlevels == 3,

    "Reset_index usunal MultiIndex":
        not isinstance(results.index, pd.MultiIndex),

    "Tabela wynikowa ma shape (12, 5)":
        results.shape == (12, 5),

    "Tabela wynikowa zawiera wymagane kolumny":
        list(results.columns) == [
            "Pclass",
            "Sex",
            "Is_Alone",
            "Avg_Age",
            "Survival_Rate"
        ],

    "Tabela wynikowa nie zawiera NaN":
        results.notna().all().all(),

    "Wszystkie srednie wieku sa dodatnie":
        results["Avg_Age"].gt(0).all(),

    "Przezywalnosc jest w zakresie 0-100":
        results["Survival_Rate"].between(0, 100).all(),

    "Agregacje obliczono poprawnie":
        manual_results_correct,

    "Uwzgledniono wszystkich pasazerow":
        details["Liczba_pasazerow"].sum() == len(df),

    "Liczba ocalalych jest zgodna":
        details["Przezyli"].sum() == df["Survived"].sum(),

    "Liczba ofiar jest zgodna":
        details["Nie_przezyli"].sum()
        == (df["Survived"] == 0).sum(),

    "Poprawnie policzono znany wiek":
        details["Znany_wiek"].sum() == df["Age"].count(),

    "Poprawnie policzono brakujacy wiek":
        details["Brakujacy_wiek"].sum()
        == df["Age"].isna().sum(),

    "Przezywalnosc i smiertelnosc daja 100":
        np.allclose(
            details["Przezywalnosc_pct"]
            + details["Smiertelnosc_pct"],
            100
        ),

    "Pivot wieku ma shape (6, 2)":
        pivot_age.shape == (6, 2),

    "Pivot przezywalnosci ma shape (6, 2)":
        pivot_survival.shape == (6, 2),

    "Srednia wazona wieku jest poprawna":
        np.isclose(weighted_age, global_age),

    "Srednia wazona przezywalnosci jest poprawna":
        np.isclose(weighted_survival, global_survival),

    "Ranking jest poprawnie posortowany":
        ranking["Przezywalnosc_pct"].is_monotonic_decreasing,

    "Zachowano wszystkie indeksy":
        df.index.equals(df_original.index),

    "Istniejace kolumny pozostaly niezmienione":
        df[df_original.columns].equals(df_original)
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("Wszystkie testy zakonczone pomyslnie.")
