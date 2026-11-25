# Lekcja 12 - Zadanie 13: Feature Engineering Pipeline

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


def group_zscore(x):
    """Standaryzacja Z-score wewnatrz grupy."""
    std = x.std()

    if pd.isna(std) or std == 0:
        return x * 0

    return (x - x.mean()) / std


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia oryginalnych danych
df_original = df.copy(deep=True)


print("=" * 75)
print("FEATURE ENGINEERING PIPELINE - TITANIC")
print("=" * 75)


section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")

print("\nTypy danych:")
print(df.dtypes.to_string())

print("\nPierwsze 5 rekordow:")
print(df.head().to_string(index=False))


section("BRAKUJACE WARTOSCI PRZED PIPELINE")

missing_before = df.isna().sum()

print(missing_before.to_string())

print(f"\nLaczna liczba brakow: {missing_before.sum()}")


# =========================================================
# ETAP 1 - FEATURE ENGINEERING
# =========================================================

section("ETAP 1 - CECHY RODZINNE")

# Cecha 1
df["Family_Size"] = df["SibSp"] + df["Parch"] + 1

# Cecha 2
df["Is_Alone"] = (df["Family_Size"] == 1).astype(int)

print(
    df[
        ["SibSp", "Parch", "Family_Size", "Is_Alone"]
    ].head(10).to_string(index=False)
)

print("\nRozklad rozmiaru rodziny:")
print(df["Family_Size"].value_counts().sort_index())

print("\nPasazerowie podrozujacy samotnie:")
print(df["Is_Alone"].value_counts().sort_index())


section("ETAP 2 - EKSTRAKCJA TYTULOW")

# Cecha 3 - poczatkowo tekstowa
df["Title"] = (
    df["Name"]
    .str.extract(r",\s*([^.]*)\.", expand=False)
    .str.strip()
    .fillna("Unknown")
)

print("Tytuly przed kodowaniem:")
print(df["Title"].value_counts().to_string())

# Zachowanie nazw tytulow do raportu
title_names = df["Title"].copy()


section("ETAP 3 - WYPELNIANIE BRAKOW GRUPOWO")

# Cecha 11 - informacja o pierwotnym braku wieku
df["Age_Missing"] = df["Age"].isna().astype(int)

age_missing_before = df["Age"].isna().sum()

# Wypelnienie wieku mediana wedlug klasy i plci
df["Age"] = (
    df.groupby(["Pclass", "Sex"])["Age"]
    .transform(lambda x: x.fillna(x.median()))
)

# Dodatkowe zabezpieczenie
df["Age"] = df["Age"].fillna(df["Age"].median())

# Wypelnienie Fare mediana wedlug klasy
df["Fare"] = (
    df.groupby("Pclass")["Fare"]
    .transform(lambda x: x.fillna(x.median()))
)

df["Fare"] = df["Fare"].fillna(df["Fare"].median())

# Wypelnienie portu najczestsza wartoscia
df["Embarked"] = df["Embarked"].fillna(
    df["Embarked"].mode().iloc[0]
)

print(f"Braki Age przed: {age_missing_before}")
print(f"Braki Age po: {df['Age'].isna().sum()}")
print(f"Braki Fare po: {df['Fare'].isna().sum()}")
print(f"Braki Embarked po: {df['Embarked'].isna().sum()}")


section("ETAP 4 - DODATKOWE CECHY NUMERYCZNE")

# Cecha 4
df["Fare_Per_Person"] = df["Fare"] / df["Family_Size"]

# Cecha 5
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 12, 18, 60, np.inf],
    labels=[0, 1, 2, 3],
    include_lowest=True
).astype(int)

# Cecha 8
df["Has_Cabin"] = df["Cabin"].notna().astype(int)

# Cecha 9
df["Is_Child"] = (df["Age"] <= 12).astype(int)

# Cecha 10 - przyblizony wskaznik matki
df["Is_Mother"] = (
    (df["Sex"] == "female")
    & (df["Age"] >= 18)
    & (df["Parch"] > 0)
    & (title_names != "Miss")
).astype(int)

# Cecha 12
df["Fare_Log"] = np.log1p(df["Fare"])

# Cecha 19
df["Ticket_Group_Size"] = (
    df.groupby("Ticket")["Ticket"]
    .transform("size")
)

# Cecha 20
df["Is_Large_Family"] = (
    df["Family_Size"] >= 5
).astype(int)

print(
    df[
        [
            "Family_Size",
            "Fare_Per_Person",
            "Age_Group",
            "Has_Cabin",
            "Is_Child",
            "Is_Mother",
            "Age_Missing",
            "Fare_Log",
            "Ticket_Group_Size",
            "Is_Large_Family"
        ]
    ].head(10).round(2).to_string(index=False)
)


section("ETAP 5 - AGREGACJE GRUPOWE JAKO CECHY")

# Cecha 13
df["Avg_Fare_Pclass"] = (
    df.groupby("Pclass")["Fare"]
    .transform("mean")
)

# Cecha 14
df["Avg_Age_Pclass"] = (
    df.groupby("Pclass")["Age"]
    .transform("mean")
)

# Cecha 17
df["Fare_Difference"] = (
    df["Fare"] - df["Avg_Fare_Pclass"]
)

# Cecha 18
df["Age_Difference"] = (
    df["Age"] - df["Avg_Age_Pclass"]
)

print(
    df[
        [
            "Pclass",
            "Age",
            "Avg_Age_Pclass",
            "Age_Difference",
            "Fare",
            "Avg_Fare_Pclass",
            "Fare_Difference"
        ]
    ].head(10).round(2).to_string(index=False)
)


section("SURVIVAL RATE WEDLUG TYTULU")

# Agregacja wymagana w zadaniu
df["Title_Survival_Rate"] = (
    df.groupby("Title")["Survived"]
    .transform("mean")
)

title_report = df.groupby("Title").agg(
    Liczba_pasazerow=("Survived", "size"),
    Przezyli=("Survived", "sum"),
    Survival_Rate=("Title_Survival_Rate", "first")
)

title_report["Survival_Rate_%"] = (
    title_report["Survival_Rate"] * 100
)

print(
    title_report.sort_values(
        "Survival_Rate",
        ascending=False
    ).round(2).to_string()
)

print("\nTekstowy wykres przezywalnosci:")
print("Legenda: jeden znak = okolo 2%")

for title, row in title_report.iterrows():
    rate = row["Survival_Rate_%"]
    bar = "█" * int(round(rate / 2))

    print(f"{title:15} | {bar:50} {rate:6.2f}%")

print("\nUWAGA: Title_Survival_Rate sluzy tylko do analizy.")
print("Cecha nie zostanie dodana do X z powodu data leakage.")


section("ETAP 6 - KODOWANIE ZMIENNYCH KATEGORYCZNYCH")

# Cecha 6
df["Sex_Encoded"] = df["Sex"].map({
    "male": 0,
    "female": 1
}).astype(int)

# Cecha 7
df["Embarked_Encoded"] = df["Embarked"].map({
    "C": 0,
    "Q": 1,
    "S": 2
}).astype(int)

# Kodowanie tytulow przez pd.factorize()
title_codes, unique_titles = pd.factorize(
    df["Title"],
    sort=True
)

df["Title"] = title_codes

title_mapping = pd.DataFrame({
    "Title_Name": unique_titles,
    "Title_Code": np.arange(len(unique_titles))
})

print("Kodowanie plci:")
print("male = 0")
print("female = 1")

print("\nKodowanie portow:")
print("C = 0")
print("Q = 1")
print("S = 2")

print("\nKodowanie tytulow:")
print(title_mapping.to_string(index=False))

print("\nKodowanie grup wiekowych:")
print("0 = Dziecko")
print("1 = Nastolatek")
print("2 = Dorosly")
print("3 = Senior")


section("ETAP 7 - STANDARYZACJA GRUPOWA")

# Cecha 15
df["Age_Zscore_Pclass"] = (
    df.groupby("Pclass")["Age"]
    .transform(group_zscore)
)

# Cecha 16
df["Fare_Zscore_Pclass"] = (
    df.groupby("Pclass")["Fare"]
    .transform(group_zscore)
)

print(
    df[
        [
            "Pclass",
            "Age",
            "Age_Zscore_Pclass",
            "Fare",
            "Fare_Zscore_Pclass"
        ]
    ].head(10).round(4).to_string(index=False)
)

print("\nWeryfikacja standaryzacji:")

standardization_report = df.groupby("Pclass")[
    ["Age_Zscore_Pclass", "Fare_Zscore_Pclass"]
].agg(["mean", "std"])

print(standardization_report.round(6).to_string())


# =========================================================
# ETAP 8 - PRZYGOTOWANIE DATASETU NUMERYCZNEGO
# =========================================================

section("ETAP 8 - PRZYGOTOWANIE DATASETU ML")

new_features = [
    "Family_Size",
    "Is_Alone",
    "Title",
    "Fare_Per_Person",
    "Age_Group",
    "Sex_Encoded",
    "Embarked_Encoded",
    "Has_Cabin",
    "Is_Child",
    "Is_Mother",
    "Age_Missing",
    "Fare_Log",
    "Avg_Fare_Pclass",
    "Avg_Age_Pclass",
    "Age_Zscore_Pclass",
    "Fare_Zscore_Pclass",
    "Fare_Difference",
    "Age_Difference",
    "Ticket_Group_Size",
    "Is_Large_Family"
]

original_features = [
    "Pclass",
    "Age",
    "SibSp",
    "Parch",
    "Fare"
]

# X - cechy wejsciowe
X = df[original_features + new_features].copy()

# y - zmienna docelowa
y = df["Survived"].copy()

# Kompletny numeryczny dataset
df_ml = X.copy()
df_ml["Survived"] = y

print(f"Shape oryginalny: {df_original.shape}")
print(f"Shape po Feature Engineering: {df.shape}")
print(f"Shape X: {X.shape}")
print(f"Shape y: {y.shape}")
print(f"Shape df_ml: {df_ml.shape}")

print(f"\nLiczba nowych cech: {len(new_features)}")
print(f"Liczba wszystkich cech X: {X.shape[1]}")

print("\nLista nowych cech:")

for number, feature in enumerate(new_features, start=1):
    print(f"{number:2}. {feature}")

print("\nUsuniete z X kolumny:")

excluded_columns = [
    column for column in df.columns
    if column not in X.columns
]

print(excluded_columns)


section("PIERWSZE 10 REKORDOW DATASETU ML")

print(df_ml.head(10).round(3).to_string(index=False))


section("TYPY DANYCH DATASETU ML")

print(df_ml.dtypes.to_string())


section("BRAKUJACE WARTOSCI PO PIPELINE")

print(df_ml.isna().sum().to_string())

print(f"\nLaczna liczba brakow: {df_ml.isna().sum().sum()}")


section("STATYSTYKI NOWYCH CECH")

print(
    X[new_features]
    .describe()
    .T
    .round(3)
    .to_string()
)


section("ANALIZA CECH BINARNYCH")

binary_features = [
    "Is_Alone",
    "Sex_Encoded",
    "Has_Cabin",
    "Is_Child",
    "Is_Mother",
    "Age_Missing",
    "Is_Large_Family"
]

binary_report = pd.DataFrame({
    "Liczba_1": X[binary_features].sum(),
    "Udzial_%": X[binary_features].mean() * 100
})

print(binary_report.round(2).to_string())

print("\nTekstowy wykres cech binarnych:")
print("Legenda: jeden znak = okolo 2%")

for feature, row in binary_report.iterrows():
    percentage = row["Udzial_%"]
    bar = "█" * int(round(percentage / 2))

    print(f"{feature:20} | {bar:50} {percentage:6.2f}%")


section("KORELACJA CECH Z SURVIVED")

correlations = (
    df_ml.corr()["Survived"]
    .drop("Survived")
)

correlation_report = pd.DataFrame({
    "Korelacja": correlations,
    "Abs_Korelacja": correlations.abs()
}).sort_values(
    "Abs_Korelacja",
    ascending=False
)

print(correlation_report.round(4).to_string())

print("\nKorelacja nie oznacza zwiazku przyczynowego.")
print("Korelacje kodow kategorii nalezy interpretowac ostroznie.")


section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum() / 1024
)

memory_engineered = (
    df.memory_usage(deep=True).sum() / 1024
)

memory_ml = (
    df_ml.memory_usage(deep=True).sum() / 1024
)

memory_report = pd.DataFrame({
    "Dataset": [
        "Oryginalny",
        "Feature Engineering",
        "Dataset ML"
    ],
    "Pamiec_KiB": [
        memory_before,
        memory_engineered,
        memory_ml
    ]
})

print(memory_report.round(2).to_string(index=False))


section("ROZKLAD ZMIENNEJ DOCELOWEJ")

target_report = pd.DataFrame({
    "Liczba": y.value_counts().sort_index(),
    "Udzial_%": (
        y.value_counts(normalize=True)
        .sort_index() * 100
    )
})

print(target_report.round(2).to_string())


section("WNIOSKI")

conclusions = [
    "Feature Engineering tworzy nowe informacje z istniejacych danych.",
    "Family_Size laczy SibSp i Parch.",
    "Is_Alone identyfikuje osoby podrozujace bez rodziny.",
    "Title wydobywa informacje z kolumny Name.",
    "Fare_Per_Person jest przyblizona oplata na osobe.",
    "Age_Group zamienia wiek na kategorie.",
    "Braki wieku wypelniono mediana grupowa.",
    "Age_Missing zachowuje informacje o pierwotnych brakach.",
    "Map i factorize koduja zmienne kategoryczne.",
    "Transform zachowuje liczbe wierszy.",
    "Standaryzacja grupowa daje srednia 0 i odchylenie 1.",
    "Fare_Log ogranicza asymetrie wysokich oplat.",
    "Is_Mother jest cecha heurystyczna.",
    "Title_Survival_Rate nie trafia do X.",
    "X zawiera wylacznie cechy numeryczne.",
    "y jest oddzielna zmienna docelowa.",
    "Pipeline nie trenuje jeszcze modelu ML.",
    "Przed treningiem statystyki nalezy wyznaczac na zbiorze treningowym."
]

for number, conclusion in enumerate(conclusions, start=1):
    print(f"{number}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(df_ml)}")
print(f"Liczba nowych cech: {len(new_features)}")
print(f"Liczba cech wejsciowych: {X.shape[1]}")
print(f"Liczba kolumn datasetu ML: {df_ml.shape[1]}")
print(f"Liczba brakow: {df_ml.isna().sum().sum()}")
print(f"Shape X: {X.shape}")
print(f"Shape y: {y.shape}")
print(f"Shape df_ml: {df_ml.shape}")


# =========================================================
# TESTY WERYFIKACYJNE
# =========================================================

section("WERYFIKACJA")

numeric_only = all(
    pd.api.types.is_numeric_dtype(dtype)
    for dtype in df_ml.dtypes
)

age_zscore_stats = df.groupby("Pclass")[
    "Age_Zscore_Pclass"
].agg(["mean", "std"])

fare_zscore_stats = df.groupby("Pclass")[
    "Fare_Zscore_Pclass"
].agg(["mean", "std"])

expected_family_size = (
    df_original["SibSp"]
    + df_original["Parch"]
    + 1
)

expected_ticket_size = (
    df_original.groupby("Ticket")["Ticket"]
    .transform("size")
)

expected_age = (
    df_original.groupby(["Pclass", "Sex"])["Age"]
    .transform(lambda x: x.fillna(x.median()))
)

expected_age = expected_age.fillna(expected_age.median())

known_age_mask = df_original["Age"].notna()

tests = {
    "Dataset ma 891 wierszy":
        len(df_original) == 891,

    "Dataset ma poczatkowo 12 kolumn":
        df_original.shape[1] == 12,

    "Utworzono minimum 10 nowych cech":
        len(new_features) >= 10,

    "Utworzono dokladnie 20 nowych cech":
        len(new_features) == 20,

    "Nazwy nowych cech sa unikalne":
        len(set(new_features)) == len(new_features),

    "Wszystkie nowe cechy istnieja":
        set(new_features).issubset(X.columns),

    "Family_Size obliczono poprawnie":
        df["Family_Size"].equals(expected_family_size),

    "Family_Size jest dodatnie":
        df["Family_Size"].ge(1).all(),

    "Is_Alone obliczono poprawnie":
        df["Is_Alone"].equals(
            (expected_family_size == 1).astype(int)
        ),

    "Fare_Per_Person obliczono poprawnie":
        np.allclose(
            df["Fare_Per_Person"],
            df["Fare"] / df["Family_Size"]
        ),

    "Istnieja cztery grupy wiekowe":
        set(df["Age_Group"].unique()) == {0, 1, 2, 3},

    "Title jest numeryczne":
        pd.api.types.is_numeric_dtype(df["Title"]),

    "Title nie zawiera ujemnych kodow":
        df["Title"].ge(0).all(),

    "Kodowanie plci jest poprawne":
        df["Sex_Encoded"].equals(
            df_original["Sex"].map(
                {"male": 0, "female": 1}
            ).astype(int)
        ),

    "Kodowanie portow jest poprawne":
        df["Embarked_Encoded"].isin([0, 1, 2]).all(),

    "Has_Cabin obliczono poprawnie":
        df["Has_Cabin"].equals(
            df_original["Cabin"].notna().astype(int)
        ),

    "Is_Child obliczono poprawnie":
        df["Is_Child"].equals(
            (df["Age"] <= 12).astype(int)
        ),

    "Is_Mother jest binarne":
        df["Is_Mother"].isin([0, 1]).all(),

    "Age_Missing zachowuje pierwotne braki":
        df["Age_Missing"].equals(
            df_original["Age"].isna().astype(int)
        ),

    "Fare_Log obliczono poprawnie":
        np.allclose(
            df["Fare_Log"],
            np.log1p(df["Fare"])
        ),

    "Ticket_Group_Size obliczono poprawnie":
        df["Ticket_Group_Size"].equals(
            expected_ticket_size
        ),

    "Is_Large_Family obliczono poprawnie":
        df["Is_Large_Family"].equals(
            (df["Family_Size"] >= 5).astype(int)
        ),

    "Wypelniono wszystkie braki Age":
        df["Age"].notna().all(),

    "Wiek wypelniono mediana grupowa":
        np.allclose(df["Age"], expected_age),

    "Zachowano znane wartosci Age":
        df.loc[known_age_mask, "Age"].equals(
            df_original.loc[known_age_mask, "Age"]
        ),

    "Wypelniono wszystkie braki Fare":
        df["Fare"].notna().all(),

    "Wypelniono wszystkie braki Embarked":
        df["Embarked"].notna().all(),

    "Avg_Fare_Pclass obliczono poprawnie":
        np.allclose(
            df["Avg_Fare_Pclass"],
            df.groupby("Pclass")["Fare"].transform("mean")
        ),

    "Avg_Age_Pclass obliczono poprawnie":
        np.allclose(
            df["Avg_Age_Pclass"],
            df.groupby("Pclass")["Age"].transform("mean")
        ),

    "Fare_Difference obliczono poprawnie":
        np.allclose(
            df["Fare_Difference"],
            df["Fare"] - df["Avg_Fare_Pclass"]
        ),

    "Age_Difference obliczono poprawnie":
        np.allclose(
            df["Age_Difference"],
            df["Age"] - df["Avg_Age_Pclass"]
        ),

    "Survival rate wedlug tytulu jest poprawny":
        np.allclose(
            df["Title_Survival_Rate"],
            df.groupby("Title")["Survived"].transform("mean")
        ),

    "Survival rate miesci sie w zakresie 0-1":
        df["Title_Survival_Rate"].between(0, 1).all(),

    "Standaryzacja Age daje srednia 0":
        np.allclose(age_zscore_stats["mean"], 0),

    "Standaryzacja Age daje std 1":
        np.allclose(age_zscore_stats["std"], 1),

    "Standaryzacja Fare daje srednia 0":
        np.allclose(fare_zscore_stats["mean"], 0),

    "Standaryzacja Fare daje std 1":
        np.allclose(fare_zscore_stats["std"], 1),

    "Wszystkie cechy binarne sa poprawne":
        X[binary_features].isin([0, 1]).all().all(),

    "X ma shape (891, 25)":
        X.shape == (891, 25),

    "y ma 891 wartosci":
        y.shape == (891,),

    "Dataset ML ma shape (891, 26)":
        df_ml.shape == (891, 26),

    "X nie zawiera Survived":
        "Survived" not in X.columns,

    "X nie zawiera Title_Survival_Rate":
        "Title_Survival_Rate" not in X.columns,

    "X nie zawiera PassengerId":
        "PassengerId" not in X.columns,

    "Dataset ML zawiera tylko dane numeryczne":
        numeric_only,

    "Dataset ML nie zawiera NaN":
        df_ml.isna().sum().sum() == 0,

    "Dataset ML nie zawiera inf":
        np.isfinite(df_ml.to_numpy(dtype=float)).all(),

    "Zmienna docelowa jest binarna":
        y.isin([0, 1]).all(),

    "Zmienna docelowa pozostala niezmieniona":
        y.equals(df_original["Survived"]),

    "Zachowano oryginalne indeksy":
        df_ml.index.equals(df_original.index),

    "Zachowano wszystkich pasazerow":
        len(df_ml) == len(df_original),

    "Oryginalna kopia nadal ma 12 kolumn":
        df_original.shape[1] == 12
}

passed = 0

for name, result in tests.items():
    result = bool(result)

    print(f"Czy {name}: {result}")

    if result:
        passed += 1

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), (
    "Nie wszystkie testy zostaly zaliczone."
)

print("Wszystkie testy zakonczone pomyslnie.")
