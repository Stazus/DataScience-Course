# Lekcja 11 - Zadanie 16: Zaawansowane filtrowanie rodzin

import pandas as pd
import numpy as np


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia oryginalnych danych
df_original = df.copy()

# DataFrame do analizy rodzin
df_families = df.copy()

# Minimalny wskaznik przezycia
minimal_survival_rate = 0.5

# Utworzenie cechy FamilySize
df_families["FamilySize"] = (
    df_families["SibSp"]
    + df_families["Parch"]
    + 1
)

# Wyodrebnienie nazwiska z kolumny Name
df_families["Surname"] = (
    df_families["Name"]
    .str.split(",")
    .str[0]
    .str.strip()
)

# Utworzenie identyfikatora rodziny
df_families["FamilyID"] = (
    df_families["Surname"]
    + "_"
    + df_families["FamilySize"].astype(str)
)

print("ZAAWANSOWANE FILTROWANIE RODZIN - TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape przed: {df.shape}")
print(f"Shape po dodaniu cech: {df_families.shape}")
print(f"Liczba pasazerow: {len(df)}")
print("Nowe cechy: FamilySize, Surname, FamilyID")

print("\nPIERWSZE 10 PASAZEROW Z IDENTYFIKATOREM RODZINY")
print("=" * 75)

columns = [
    "Name",
    "Surname",
    "FamilySize",
    "FamilyID",
    "Survived"
]

print(
    df_families[columns]
    .head(10)
    .to_string(index=False)
)

# Filtrowanie pasazerow podrozujacych z rodzina
df_with_family = df_families[
    df_families["FamilySize"] > 1
].copy()

print("\nFILTROWANIE PASAZEROW")
print("=" * 75)
print(f"Wszyscy pasazerowie: {len(df_families)}")
print(f"Pasazerowie z rodzina: {len(df_with_family)}")
print(f"Pasazerowie samotni: {len(df_families) - len(df_with_family)}")
print(f"Unikalne FamilyID: {df_with_family['FamilyID'].nunique()}")

# Grupowanie i agregacja danych
family_stats = (
    df_with_family
    .groupby("FamilyID")
    .agg(
        Members=("Survived", "count"),
        Survivors=("Survived", "sum"),
        SurvivalRate=("Survived", "mean"),
        FamilySize=("FamilySize", "first")
    )
    .reset_index()
)

# Zachowanie rodzin z przynajmniej dwoma
# zarejestrowanymi czlonkami w datasecie
multi_member_families = family_stats[
    family_stats["Members"] > 1
].copy()

# Filtrowanie rodzin z przezywalnoscia >= 50%
happy_families = multi_member_families[
    multi_member_families["SurvivalRate"]
    >= minimal_survival_rate
].copy()

# Przeliczenie wskaznika przezycia na procenty
happy_families["SurvivalRate_%"] = (
    happy_families["SurvivalRate"] * 100
)

# Sortowanie wedlug liczebnosci rodziny
# Przy remisie: przezywalnosc, a nastepnie FamilyID
happy_families = happy_families.sort_values(
    by=["Members", "SurvivalRate", "FamilyID"],
    ascending=[False, False, True]
).reset_index(drop=True)

# Wybor TOP 10 rodzin
top10 = happy_families.head(10).copy()

print("\nSTATYSTYKI GRUPOWANIA")
print("=" * 75)
print(f"Wszystkie grupy FamilyID: {len(family_stats)}")
print(f"Grupy z minimum 2 rekordami: {len(multi_member_families)}")
print(f"Rodziny z przezywalnoscia >= 50%: {len(happy_families)}")
print(f"Rodziny w TOP 10: {len(top10)}")

print("\nTOP 10 NAJSZCZESLIWSZYCH RODZIN")
print("=" * 75)

result_columns = [
    "FamilyID",
    "FamilySize",
    "Members",
    "Survivors",
    "SurvivalRate_%"
]

print(
    top10[result_columns].to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)

# Rodziny ze stuprocentowa przezywalnoscia
all_survived = multi_member_families[
    multi_member_families["SurvivalRate"] == 1
]

# Rodziny bez ocalalych
none_survived = multi_member_families[
    multi_member_families["SurvivalRate"] == 0
]

print("\nDODATKOWE STATYSTYKI RODZIN")
print("=" * 75)
print(f"Rodziny ze 100% przezywalnoscia: {len(all_survived)}")
print(f"Rodziny z 0% przezywalnoscia: {len(none_survived)}")
print(f"Czlonkowie wybranych rodzin: {happy_families['Members'].sum()}")
print(f"Ocalali w wybranych rodzinach: {happy_families['Survivors'].sum()}")

# Wazony wskaznik przezycia wybranych rodzin
weighted_survival_rate = (
    happy_families["Survivors"].sum()
    / happy_families["Members"].sum()
)

print(f"Przezywalnosc wybranych rodzin: {weighted_survival_rate:.2%}")

# Tekstowa wizualizacja przezywalnosci
print("\nTEKSTOWY WYKRES PRZEZYWALNOSCI TOP 10")
print("=" * 75)
print("Legenda: jeden znak █ = okolo 2%")

for _, row in top10.iterrows():

    rate = row["SurvivalRate_%"]
    bar = "█" * round(rate / 2)

    print(
        f"{row['FamilyID']:<22} | "
        f"{bar:<50} "
        f"{rate:>6.2f}% "
        f"({row['Survivors']}/{row['Members']})"
    )

# Szczegoly pasazerow nalezacych do TOP 10
top10_members = df_with_family[
    df_with_family["FamilyID"].isin(top10["FamilyID"])
].copy()

print("\nCZLONKOWIE RODZIN Z TOP 10")
print("=" * 75)

for _, family in top10.iterrows():

    family_id = family["FamilyID"]

    members = top10_members[
        top10_members["FamilyID"] == family_id
    ]

    print(f"\nRodzina: {family_id}")
    print("-" * 75)

    print(
        members[
            ["Name", "Age", "Sex", "Survived"]
        ].to_string(index=False)
    )

# Porownanie liczebnosci deklarowanej i obserwowanej
incomplete_groups = multi_member_families[
    multi_member_families["Members"]
    != multi_member_families["FamilySize"]
]

print("\nOGRANICZENIA ANALIZY")
print("=" * 75)
print(f"Grupy o roznej liczebnosci deklarowanej i obserwowanej: {len(incomplete_groups)}")
print("FamilyID jest przyblizonym identyfikatorem rodziny.")
print("Osoby o tym samym nazwisku moga nie byc spokrewnione.")
print("Dataset nie musi zawierac wszystkich czlonkow rodziny.")
print("Przezywalnosc dotyczy rekordow dostepnych w datasecie.")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba wszystkich pasazerow: {len(df)}")
print(f"Pasazerowie z rodzina: {len(df_with_family)}")
print(f"Liczba grup rodzinnych: {len(family_stats)}")
print(f"Grupy z minimum 2 rekordami: {len(multi_member_families)}")
print(f"Rodziny spelniajace warunki: {len(happy_families)}")
print(f"Rodziny ze 100% przezywalnoscia: {len(all_survived)}")
print(f"Przezywalnosc wybranych rodzin: {weighted_survival_rate:.2%}")

# Automatyczna weryfikacja
print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy oryginal ma 12 kolumn: {len(df.columns) == 12}")
print(f"Czy dodano 3 nowe kolumny: {len(df_families.columns) == 15}")
print(f"Czy FamilySize jest poprawne: {(df_families['FamilySize'] == df['SibSp'] + df['Parch'] + 1).all()}")
print(f"Czy FamilyID nie zawiera NaN: {df_families['FamilyID'].notna().all()}")
print(f"Czy wszyscy wybrani pasazerowie maja rodzine: {(df_with_family['FamilySize'] > 1).all()}")
print(f"Czy pasazerow z rodzina jest 354: {len(df_with_family) == 354}")
print(f"Czy grupowanie zachowalo wszystkie rekordy: {family_stats['Members'].sum() == len(df_with_family)}")
print(f"Czy grupowanie zachowalo liczbe ocalalych: {family_stats['Survivors'].sum() == df_with_family['Survived'].sum()}")
print(f"Czy FamilyID sa unikalne po grupowaniu: {family_stats['FamilyID'].is_unique}")
print(f"Czy wskazniki przezycia sa poprawne: {np.allclose(family_stats['SurvivalRate'], family_stats['Survivors'] / family_stats['Members'])}")
print(f"Czy wszystkie wskazniki sa w zakresie 0-1: {family_stats['SurvivalRate'].between(0, 1).all()}")
print(f"Czy wybrane rodziny maja minimum 2 rekordy: {(happy_families['Members'] > 1).all()}")
print(f"Czy wszystkie wybrane rodziny maja przezywalnosc >= 50%: {(happy_families['SurvivalRate'] >= 0.5).all()}")
print(f"Czy TOP 10 zawiera 10 rodzin: {len(top10) == 10}")
print(f"Czy TOP 10 jest posortowane wedlug liczebnosci: {top10['Members'].is_monotonic_decreasing}")
print(f"Czy liczba ocalalych nie przekracza liczebnosci: {(family_stats['Survivors'] <= family_stats['Members']).all()}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
