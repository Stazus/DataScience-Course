# Lekcja 12 - Zadanie 8: Wypelnianie brakow grupowo

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

# Kopia oryginalnych danych
df_original = df.copy()

# Maska brakujacych wartosci wieku
missing_mask = df["Age"].isna()

# Liczba brakow przed uzupelnieniem
missing_before = df["Age"].isna().sum()

# Statystyki przed uzupelnieniem
stats_before = df["Age"].describe()

# Mediana globalna
global_median = df["Age"].median()

# Mediany wedlug klasy
class_medians = df.groupby("Pclass")["Age"].median()

print("=" * 75)
print("WYPELNIANIE BRAKOW GRUPOWO - DATASET TITANIC")
print("=" * 75)


# ==========================================================
# 1. Dane wejsciowe
# ==========================================================

section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Znany wiek: {df['Age'].count()}")
print(f"Brakujacy wiek: {missing_before}")
print(f"Procent brakow: {missing_before / len(df) * 100:.2f}%")


section("PIERWSZE 10 REKORDOW PRZED UZUPELNIENIEM")

print(
    df[["PassengerId", "Pclass", "Sex", "Age"]]
    .head(10)
    .to_string(index=False)
)


# ==========================================================
# 2. Statystyki przed uzupelnieniem
# ==========================================================

section("STATYSTYKI AGE PRZED UZUPELNIENIEM")

print(stats_before.round(2).to_string())


section("MEDIANA GLOBALNA I MEDIANY GRUPOWE")

print(f"Mediana globalna: {global_median:.2f}")

print("\nMediany wedlug klasy:")
print(class_medians.round(2).to_string())


# ==========================================================
# 3. Analiza brakow wedlug klasy
# ==========================================================

section("BRAKUJACE WARTOSCI AGE WEDLUG KLASY")

missing_by_class = (
    df.groupby("Pclass")["Age"]
    .agg(
        Liczba_pasazerow="size",
        Znany_wiek="count",
        Mediana_wieku="median"
    )
)

missing_by_class["Brakujacy_wiek"] = (
    missing_by_class["Liczba_pasazerow"]
    - missing_by_class["Znany_wiek"]
)

missing_by_class["Braki_%"] = (
    missing_by_class["Brakujacy_wiek"]
    / missing_by_class["Liczba_pasazerow"]
    * 100
)

print(missing_by_class.round(2).to_string())


# ==========================================================
# 4. Grupowe uzupelnianie brakow
# ==========================================================

section("GRUPOWE UZUPELNIANIE BRAKOW")

df["Age"] = df.groupby("Pclass")["Age"].transform(
    lambda x: x.fillna(x.median())
)

missing_after = df["Age"].isna().sum()

filled_count = missing_before - missing_after

print(f"Braki przed: {missing_before}")
print(f"Braki po: {missing_after}")
print(f"Uzupelnione wartosci: {filled_count}")

print("\nZastosowane mediany:")

for pclass, median in class_medians.items():
    print(f"Klasa {pclass}: {median:.2f} lat")


# ==========================================================
# 5. Porownanie rekordow przed i po
# ==========================================================

section("PIERWSZE 10 REKORDOW PO UZUPELNIENIU")

print(
    df[["PassengerId", "Pclass", "Sex", "Age"]]
    .head(10)
    .to_string(index=False)
)


section("PRZYKLADOWE UZUPELNIONE REKORDY")

filled_records = df.loc[
    missing_mask,
    ["PassengerId", "Pclass", "Sex", "Age"]
].copy()

filled_records["Age_przed"] = df_original.loc[
    missing_mask, "Age"
]

filled_records = filled_records.rename(
    columns={"Age": "Age_po"}
)

filled_records = filled_records[
    [
        "PassengerId",
        "Pclass",
        "Sex",
        "Age_przed",
        "Age_po"
    ]
]

print(filled_records.head(15).to_string(index=False))


# ==========================================================
# 6. Porownanie describe()
# ==========================================================

section("STATYSTYKI AGE PO UZUPELNIENIU")

stats_after = df["Age"].describe()

print(stats_after.round(2).to_string())


section("POROWNANIE STATYSTYK PRZED I PO")

comparison = pd.DataFrame({
    "Przed": stats_before,
    "Po": stats_after
})

comparison["Roznica"] = (
    comparison["Po"] - comparison["Przed"]
)

print(comparison.round(4).to_string())


# ==========================================================
# 7. Porownanie wedlug klasy
# ==========================================================

section("POROWNANIE STATYSTYK WEDLUG KLASY")

group_comparison = pd.DataFrame({
    "Liczba_pasazerow": df.groupby("Pclass").size(),

    "Braki_przed": (
        df_original.groupby("Pclass")["Age"]
        .apply(lambda x: x.isna().sum())
    ),

    "Braki_po": (
        df.groupby("Pclass")["Age"]
        .apply(lambda x: x.isna().sum())
    ),

    "Srednia_przed": (
        df_original.groupby("Pclass")["Age"].mean()
    ),

    "Srednia_po": (
        df.groupby("Pclass")["Age"].mean()
    ),

    "Mediana_przed": (
        df_original.groupby("Pclass")["Age"].median()
    ),

    "Mediana_po": (
        df.groupby("Pclass")["Age"].median()
    )
})

group_comparison["Uzupelnione"] = (
    group_comparison["Braki_przed"]
    - group_comparison["Braki_po"]
)

print(group_comparison.round(2).to_string())


# ==========================================================
# 8. Porownanie z mediana globalna
# ==========================================================

section("POROWNANIE MEDIANY GLOBALNEJ I GRUPOWEJ")

df_global = df_original.copy()

df_global["Age"] = df_global["Age"].fillna(
    global_median
)

methods_comparison = pd.DataFrame({
    "Oryginal": df_original["Age"].describe(),
    "Mediana_globalna": df_global["Age"].describe(),
    "Mediana_grupowa": df["Age"].describe()
})

print(methods_comparison.round(4).to_string())


section("WARTOSCI PRZYPISANE BRAKUJACYM REKORDOM")

imputation_comparison = pd.DataFrame({
    "Liczba_brakow": (
        missing_by_class["Brakujacy_wiek"]
    ),
    "Mediana_globalna": global_median,
    "Mediana_grupowa": class_medians
})

imputation_comparison["Roznica"] = (
    imputation_comparison["Mediana_grupowa"]
    - imputation_comparison["Mediana_globalna"]
)

print(imputation_comparison.round(2).to_string())


# ==========================================================
# 9. Tekstowe wykresy
# ==========================================================

section("TEKSTOWY WYKRES BRAKUJACYCH DANYCH")

print("Legenda: jeden znak = okolo 5 brakow")

for label, value in [
    ("Przed", missing_before),
    ("Po", missing_after)
]:
    bar = "█" * int(round(value / 5))
    print(f"{label:8} | {bar:40} {value:4}")


section("TEKSTOWY WYKRES BRAKOW WEDLUG KLASY")

print("Legenda: jeden znak = okolo 5 brakow")

for pclass, row in missing_by_class.iterrows():

    value = int(row["Brakujacy_wiek"])
    bar = "█" * int(round(value / 5))

    print(f"Klasa {pclass} | {bar:35} {value:4}")


section("TEKSTOWY WYKRES MEDIAN WIEKU")

print("Legenda: jeden znak = okolo 1 roku")

for pclass, median in class_medians.items():

    bar = "█" * int(round(median))

    print(f"Klasa {pclass} | {bar:40} {median:.2f}")


# ==========================================================
# 10. Analiza rozkladu wieku
# ==========================================================

section("POROWNANIE ROZKLADU WIEKU")

distribution = pd.DataFrame({
    "Przed": [
        df_original["Age"].mean(),
        df_original["Age"].median(),
        df_original["Age"].std(),
        df_original["Age"].var(),
        df_original["Age"].skew()
    ],

    "Mediana_globalna": [
        df_global["Age"].mean(),
        df_global["Age"].median(),
        df_global["Age"].std(),
        df_global["Age"].var(),
        df_global["Age"].skew()
    ],

    "Mediana_grupowa": [
        df["Age"].mean(),
        df["Age"].median(),
        df["Age"].std(),
        df["Age"].var(),
        df["Age"].skew()
    ]

}, index=[
    "Srednia",
    "Mediana",
    "Odchylenie_std",
    "Wariancja",
    "Skosnosc"
])

print(distribution.round(4).to_string())


# ==========================================================
# 11. Struktura i pamiec
# ==========================================================

section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print(f"Typ Age przed: {df_original['Age'].dtype}")
print(f"Typ Age po: {df['Age'].dtype}")

memory_before = (
    df_original.memory_usage(deep=True).sum() / 1024
)

memory_after = (
    df.memory_usage(deep=True).sum() / 1024
)

print(f"Pamiec przed: {memory_before:.2f} KiB")
print(f"Pamiec po: {memory_after:.2f} KiB")


# ==========================================================
# 12. Wnioski
# ==========================================================

section("WNIOSKI")

conclusions = [
    "GroupBy dzieli pasazerow wedlug klasy.",
    "Median oblicza mediane wieku dla kazdej klasy.",
    "Transform zachowuje liczbe wierszy i indeksy.",
    "Fillna uzupelnia tylko brakujace wartosci.",
    "Lambda pozwala zastosowac operacje w kazdej grupie.",
    "Mediana jest odporna na wartosci odstajace.",
    "Mediana grupowa uwzglednia roznice miedzy klasami.",
    "Nie zmieniono znanych wartosci wieku.",
    "Uzupelnianie mediana moze zmniejszac zmiennosc danych.",
    "Uzupelnione wartosci nie sa rzeczywistym wiekiem.",
    "Mediana grupowa nie zawsze jest najlepsza metoda.",
    "W ML mediany nalezy wyznaczac na danych treningowych."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


# ==========================================================
# 13. Podsumowanie
# ==========================================================

section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba klas: {df['Pclass'].nunique()}")
print(f"Braki Age przed: {missing_before}")
print(f"Braki Age po: {missing_after}")
print(f"Uzupelnione wartosci: {filled_count}")
print(f"Mediana globalna: {global_median:.2f}")
print(f"Mediana klasy 1: {class_medians.loc[1]:.2f}")
print(f"Mediana klasy 2: {class_medians.loc[2]:.2f}")
print(f"Mediana klasy 3: {class_medians.loc[3]:.2f}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")

if missing_before > 0:
    effectiveness = filled_count / missing_before * 100
else:
    effectiveness = 100.0

print(f"Skutecznosc uzupelniania: {effectiveness:.2f}%")


# ==========================================================
# 14. Automatyczna weryfikacja
# ==========================================================

section("WERYFIKACJA")

expected_age = df_original["Age"].fillna(
    df_original["Pclass"].map(class_medians)
)

expected_filled = df_original.loc[
    missing_mask, "Pclass"
].map(class_medians)

actual_filled = df.loc[missing_mask, "Age"]

known_mask = ~missing_mask

expected_medians = np.array([37.0, 29.0, 24.0])

expected_missing = np.array([30, 11, 136])

tests = {

    "Dataset ma 891 wierszy":
        len(df) == 891,

    "Dataset ma 12 kolumn":
        df.shape[1] == 12,

    "Istnieja 3 klasy":
        df["Pclass"].nunique() == 3,

    "Poczatkowo bylo 177 brakow":
        missing_before == 177,

    "Poczatkowo znano 714 wartosci wieku":
        df_original["Age"].count() == 714,

    "Mediana globalna wynosi 28":
        np.isclose(global_median, 28.0),

    "Mediany klas sa poprawne":
        np.allclose(
            class_medians.to_numpy(),
            expected_medians
        ),

    "Liczba brakow w klasach jest poprawna":
        np.array_equal(
            missing_by_class["Brakujacy_wiek"].to_numpy(),
            expected_missing
        ),

    "Suma brakow grupowych wynosi 177":
        missing_by_class["Brakujacy_wiek"].sum() == 177,

    "Usunieto wszystkie braki Age":
        missing_after == 0,

    "Uzupelniono 177 wartosci":
        filled_count == 177,

    "Age zawiera 891 wartosci":
        df["Age"].count() == 891,

    "Wszystkie wartosci wieku sa skonczone":
        np.isfinite(df["Age"]).all(),

    "Wszystkie wartosci wieku sa dodatnie":
        df["Age"].gt(0).all(),

    "Braki uzupelniono odpowiednia mediana":
        np.allclose(actual_filled, expected_filled),

    "Transform i map zwracaja zgodne wyniki":
        np.allclose(df["Age"], expected_age),

    "Znane wartosci wieku pozostaly niezmienione":
        df.loc[known_mask, "Age"].equals(
            df_original.loc[known_mask, "Age"]
        ),

    "Pozostale kolumny pozostaly niezmienione":
        df.drop(columns="Age").equals(
            df_original.drop(columns="Age")
        ),

    "Zachowano wszystkie wiersze":
        len(df) == len(df_original),

    "Zachowano wszystkie indeksy":
        df.index.equals(df_original.index),

    "Zachowano wszystkie kolumny":
        df.columns.equals(df_original.columns),

    "Shape pozostalo niezmienione":
        df.shape == df_original.shape,

    "Typ kolumny Age pozostaje numeryczny":
        pd.api.types.is_numeric_dtype(df["Age"]),

    "Minimum wieku pozostalo niezmienione":
        np.isclose(
            df["Age"].min(),
            df_original["Age"].min()
        ),

    "Maksimum wieku pozostalo niezmienione":
        np.isclose(
            df["Age"].max(),
            df_original["Age"].max()
        ),

    "Mediany grupowe pozostaly niezmienione":
        np.allclose(
            df.groupby("Pclass")["Age"].median(),
            class_medians
        ),

    "Wszystkie klasy sa pozbawione brakow Age":
        group_comparison["Braki_po"].eq(0).all(),

    "Porownanie describe zawiera 8 statystyk":
        comparison.shape == (8, 3),

    "Mediana globalna rowniez usuwa braki":
        df_global["Age"].isna().sum() == 0,

    "Oryginalna kopia nadal zawiera 177 brakow":
        df_original["Age"].isna().sum() == 177,

    "Skutecznosc uzupelniania wynosi 100%":
        np.isclose(effectiveness, 100.0)
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("Wszystkie testy zakonczone pomyslnie.")
