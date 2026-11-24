# Lekcja 11 - Zadanie 11: Feature engineering

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

# DataFrame do feature engineering
df_features = df.copy()

# Cecha 1 - wielkosc rodziny
df_features["FamilySize"] = (
    df_features["SibSp"] + df_features["Parch"] + 1
)

# Cecha 2 - samotna podroz
df_features["IsAlone"] = (
    df_features["FamilySize"] == 1
).astype(int)

# Cecha 3 - grupy wiekowe
bins = [0, 12, 18, 35, 60, np.inf]
labels = ["0-12", "13-18", "19-35", "36-60", "60+"]

df_features["AgeGroup"] = pd.cut(
    df_features["Age"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

print("FEATURE ENGINEERING - DATASET TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape przed: {df.shape}")
print(f"Shape po: {df_features.shape}")
print(f"Liczba pasazerow: {len(df_features)}")
print("Nowe cechy: FamilySize, IsAlone, AgeGroup")

print("\nPIERWSZE 10 WIERSZY Z NOWYMI CECHAMI")
print("=" * 75)

kolumny = [
    "PassengerId", "Age", "SibSp", "Parch",
    "FamilySize", "IsAlone", "AgeGroup", "Survived"
]

print(
    df_features[kolumny].head(10).to_string(index=False)
)

# Rozklad wielkosci rodziny
family_counts = (
    df_features["FamilySize"]
    .value_counts()
    .sort_index()
)

print("\nROZKLAD FAMILY SIZE")
print("=" * 75)
print(family_counts.to_string())

# Rozklad samotnych pasazerow
alone_counts = (
    df_features["IsAlone"]
    .value_counts()
    .sort_index()
)

print("\nROZKLAD IS ALONE")
print("=" * 75)
print(alone_counts.to_string())
print("\n0 - podroz z rodzina")
print("1 - samotna podroz")

# Rozklad grup wiekowych
age_counts = (
    df_features["AgeGroup"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nROZKLAD GRUP WIEKOWYCH")
print("=" * 75)
print(age_counts.to_string())

# Podzial pasazerow
samotni = df_features[df_features["IsAlone"] == 1]
z_rodzina = df_features[df_features["IsAlone"] == 0]

# Wskazniki przezycia
survival_alone = samotni["Survived"].mean() * 100
survival_family = z_rodzina["Survived"].mean() * 100

print("\nWSKAZNIKI PRZEZYCIA")
print("=" * 75)

raport = pd.DataFrame({
    "Grupa": ["Samotni", "Z rodzina"],
    "Pasazerowie": [len(samotni), len(z_rodzina)],
    "Ocalali": [
        samotni["Survived"].sum(),
        z_rodzina["Survived"].sum()
    ],
    "Przezywalnosc_%": [
        survival_alone,
        survival_family
    ]
})

print(raport.round(2).to_string(index=False))

# Tekstowy wykres przezywalnosci
print("\nTEKSTOWY WYKRES PRZEZYWALNOSCI")
print("=" * 75)
print("Legenda: jeden znak = okolo 2%")

for grupa, wskaznik in zip(
    raport["Grupa"], raport["Przezywalnosc_%"]
):
    pasek = "█" * round(wskaznik / 2)
    print(f"{grupa:12} | {pasek:50} {wskaznik:.2f}%")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba nowych cech: 3")
print(f"Samotni pasazerowie: {len(samotni)}")
print(f"Pasazerowie z rodzina: {len(z_rodzina)}")
print(f"Przezywalnosc samotnych: {survival_alone:.2f}%")
print(f"Przezywalnosc z rodzina: {survival_family:.2f}%")
print(f"Roznica: {survival_family - survival_alone:.2f} p.p.")
print(f"Brakujace grupy wiekowe: {df_features['AgeGroup'].isna().sum()}")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy oryginal ma 12 kolumn: {df.shape[1] == 12}")
print(f"Czy wynik ma 15 kolumn: {df_features.shape[1] == 15}")

print(
    "Czy dodano wszystkie nowe cechy: "
    f"{all(c in df_features.columns for c in ['FamilySize', 'IsAlone', 'AgeGroup'])}"
)

print(
    "Czy FamilySize jest poprawne: "
    f"{(df_features['FamilySize'] == df['SibSp'] + df['Parch'] + 1).all()}"
)

print(
    "Czy FamilySize jest dodatnie: "
    f"{(df_features['FamilySize'] >= 1).all()}"
)

print(
    "Czy IsAlone zawiera tylko 0 i 1: "
    f"{df_features['IsAlone'].isin([0, 1]).all()}"
)

print(
    "Czy IsAlone jest poprawne: "
    f"{(df_features['IsAlone'] == (df_features['FamilySize'] == 1).astype(int)).all()}"
)

print(
    "Czy utworzono 5 grup wiekowych: "
    f"{len(df_features['AgeGroup'].cat.categories) == 5}"
)

print(
    "Czy zachowano brakujace wartosci wieku: "
    f"{df_features['AgeGroup'].isna().equals(df['Age'].isna())}"
)

print(
    "Czy grupy obejmuja wszystkich pasazerow: "
    f"{len(samotni) + len(z_rodzina) == len(df)}"
)

print(
    "Czy wskazniki przezycia sa poprawne: "
    f"{0 <= survival_alone <= 100 and 0 <= survival_family <= 100}"
)

print(
    "Czy zachowano oryginalne kolumny: "
    f"{df_features[df.columns].equals(df)}"
)

print(
    "Czy oryginalne dane pozostaly niezmienione: "
    f"{df.equals(df_original)}"
)
