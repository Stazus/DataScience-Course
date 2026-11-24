# Lekcja 11 - Zadanie 18: Smart data cleaning pipeline

import pandas as pd
import numpy as np


def clean_titanic(df: pd.DataFrame) -> pd.DataFrame:
    """
    Automatyczne czyszczenie datasetu Titanic.

    Etapy:
    1. Utworzenie kopii danych.
    2. Usuniecie kolumn z ponad 60% NaN.
    3. Uzupelnienie Age mediana.
    4. Uzupelnienie Embarked dominanta.
    5. Optymalizacja typow danych.
    6. Dodanie cechy FamilySize.

    Funkcja nie modyfikuje oryginalnego DataFrame.
    """

    # Etap 1 - kopia danych
    df_clean = df.copy()

    # Etap 2 - usuwanie kolumn z ponad 60% NaN
    missing_ratio = df_clean.isna().mean()

    columns_to_drop = missing_ratio[
        missing_ratio > 0.60
    ].index

    df_clean = df_clean.drop(columns=columns_to_drop)

    # Etap 3 - uzupelnienie Age mediana
    median_age = df_clean["Age"].median()

    df_clean["Age"] = df_clean["Age"].fillna(
        median_age
    )

    # Etap 4 - uzupelnienie Embarked dominanta
    mode_embarked = df_clean["Embarked"].mode().iloc[0]

    df_clean["Embarked"] = df_clean["Embarked"].fillna(
        mode_embarked
    )

    # Etap 5 - optymalizacja typow danych
    int8_columns = [
        "Pclass",
        "Survived",
        "SibSp",
        "Parch"
    ]

    category_columns = [
        "Sex",
        "Embarked"
    ]

    int8_limits = np.iinfo(np.int8)

    for column in int8_columns:
        if not df_clean[column].between(
            int8_limits.min,
            int8_limits.max
        ).all():
            raise ValueError(
                f"Kolumna {column} nie miesci sie w int8"
            )

        df_clean[column] = df_clean[column].astype(
            "int8"
        )

    for column in category_columns:
        df_clean[column] = df_clean[column].astype(
            "category"
        )

    # Etap 6 - feature engineering
    df_clean["FamilySize"] = (
        df_clean["SibSp"].astype("int16")
        + df_clean["Parch"].astype("int16")
        + 1
    )

    return df_clean


def main():

    # Adres URL datasetu Titanic
    url = (
        "https://raw.githubusercontent.com/"
        "datasciencedojo/datasets/master/titanic.csv"
    )

    # Wczytanie surowych danych
    titanic = pd.read_csv(url)

    # Kopia do pozniejszej weryfikacji
    titanic_original = titanic.copy()

    print("SMART DATA CLEANING PIPELINE - TITANIC")
    print("=" * 75)

    print("\nDANE PRZED CZYSZCZENIEM")
    print("=" * 75)

    print(f"Shape: {titanic.shape}")
    print(f"Liczba wierszy: {len(titanic)}")
    print(f"Liczba kolumn: {len(titanic.columns)}")
    print(f"Liczba NaN: {titanic.isna().sum().sum()}")

    print("\nINFORMACJE O SUROWYCH DANYCH")
    print("=" * 75)

    titanic.info()

    # Uruchomienie pipeline
    titanic_clean = clean_titanic(titanic)

    print("\nINFORMACJE O OCZYSZCZONYCH DANYCH")
    print("=" * 75)

    # Demonstracja wymagana w zadaniu
    titanic_clean.info()

    # Porownanie kolumn
    removed_columns = titanic.columns.difference(
        titanic_clean.columns
    ).tolist()

    added_columns = titanic_clean.columns.difference(
        titanic.columns
    ).tolist()

    print("\nZMIANY W STRUKTURZE DATAFRAME")
    print("=" * 75)

    print(f"Shape przed: {titanic.shape}")
    print(f"Shape po: {titanic_clean.shape}")
    print(f"Usuniete kolumny: {removed_columns}")
    print(f"Dodane kolumny: {added_columns}")

    # Porownanie brakujacych danych
    missing_before = titanic.isna().sum().sum()
    missing_after = titanic_clean.isna().sum().sum()

    print("\nPOROWNANIE BRAKUJACYCH DANYCH")
    print("=" * 75)

    print(f"NaN przed: {missing_before}")
    print(f"NaN po: {missing_after}")
    print(
        f"Usuniete lub uzupelnione NaN: "
        f"{missing_before - missing_after}"
    )

    print("\nSTATYSTYKI AGE PRZED I PO")
    print("=" * 75)

    age_comparison = pd.DataFrame({
        "Przed": titanic["Age"].describe(),
        "Po": titanic_clean["Age"].describe()
    })

    print(age_comparison.round(4).to_string())

    print("\nROZKLAD EMBARKED PO CZYSZCZENIU")
    print("=" * 75)

    print(
        titanic_clean["Embarked"]
        .value_counts(dropna=False)
        .to_string()
    )

    print("\nROZKLAD FAMILY SIZE")
    print("=" * 75)

    print(
        titanic_clean["FamilySize"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nPIERWSZE 10 OCZYSZCZONYCH REKORDOW")
    print("=" * 75)

    selected_columns = [
        "PassengerId",
        "Pclass",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "FamilySize",
        "Embarked",
        "Survived"
    ]

    print(
        titanic_clean[selected_columns]
        .head(10)
        .to_string(index=False)
    )

    # Porownanie zuzycia pamieci
    memory_before = titanic.memory_usage(
        deep=True
    ).sum()

    memory_after = titanic_clean.memory_usage(
        deep=True
    ).sum()

    memory_reduction = (
        (memory_before - memory_after)
        / memory_before * 100
    )

    print("\nPOROWNANIE ZUZYCIA PAMIECI")
    print("=" * 75)

    print(
        f"Przed: {memory_before} B "
        f"({memory_before / 1024:.2f} KiB)"
    )

    print(
        f"Po: {memory_after} B "
        f"({memory_after / 1024:.2f} KiB)"
    )

    print(f"Redukcja: {memory_reduction:.2f}%")

    print("\nTEKSTOWY WYKRES ZUZYCIA PAMIECI")
    print("=" * 75)

    for label, memory in [
        ("Przed", memory_before),
        ("Po", memory_after)
    ]:
        bar_length = round(
            memory / memory_before * 50
        )

        bar = "█" * bar_length

        print(
            f"{label:6} | {bar:50} "
            f"{memory / 1024:.2f} KiB"
        )

    print("\nTEKSTOWY WYKRES BRAKUJACYCH DANYCH")
    print("=" * 75)

    print("Legenda: jeden znak = okolo 20 brakow")

    for label, count in [
        ("Przed", missing_before),
        ("Po", missing_after)
    ]:
        bar = "█" * round(count / 20)

        print(f"{label:6} | {bar:45} {count}")

    print("\nPODSUMOWANIE")
    print("=" * 75)

    print("Funkcja: clean_titanic(df)")
    print(f"Liczba pasazerow: {len(titanic_clean)}")
    print(f"Usuniete kolumny: {removed_columns}")
    print(f"Dodane kolumny: {added_columns}")
    print(f"Pozostale NaN: {missing_after}")
    print(f"Redukcja pamieci: {memory_reduction:.2f}%")
    print("Oryginalne dane nie zostaly zmodyfikowane.")

    # Weryfikacja wynikow
    age_missing = titanic["Age"].isna()
    embarked_missing = titanic["Embarked"].isna()

    expected_family_size = (
        titanic["SibSp"] + titanic["Parch"] + 1
    )

    checks = {
        "Dataset ma 891 wierszy":
            len(titanic) == 891,

        "Oryginal ma 12 kolumn":
            len(titanic.columns) == 12,

        "Funkcja zwraca DataFrame":
            isinstance(titanic_clean, pd.DataFrame),

        "Funkcja zwraca nowy obiekt":
            titanic_clean is not titanic,

        "Usunieto tylko Cabin":
            removed_columns == ["Cabin"],

        "Dodano tylko FamilySize":
            added_columns == ["FamilySize"],

        "Nie ma zadnych NaN":
            missing_after == 0,

        "Age uzupelniono mediana":
            titanic_clean.loc[age_missing, "Age"]
            .eq(titanic["Age"].median()).all(),

        "Embarked uzupelniono dominanta":
            titanic_clean.loc[
                embarked_missing, "Embarked"
            ].eq(titanic["Embarked"].mode().iloc[0]).all(),

        "Pclass ma typ int8":
            str(titanic_clean["Pclass"].dtype) == "int8",

        "Survived ma typ int8":
            str(titanic_clean["Survived"].dtype) == "int8",

        "SibSp ma typ int8":
            str(titanic_clean["SibSp"].dtype) == "int8",

        "Parch ma typ int8":
            str(titanic_clean["Parch"].dtype) == "int8",

        "Sex ma typ category":
            str(titanic_clean["Sex"].dtype) == "category",

        "Embarked ma typ category":
            str(titanic_clean["Embarked"].dtype)
            == "category",

        "FamilySize jest poprawne":
            titanic_clean["FamilySize"]
            .eq(expected_family_size).all(),

        "FamilySize jest dodatnie":
            titanic_clean["FamilySize"].gt(0).all(),

        "Zachowano wszystkie wiersze":
            len(titanic_clean) == len(titanic),

        "Zachowano indeksy":
            titanic_clean.index.equals(titanic.index),

        "Wynik ma ksztalt (891, 12)":
            titanic_clean.shape == (891, 12),

        "Zmniejszono zuzycie pamieci":
            memory_after < memory_before,

        "Zachowano znane wartosci wieku":
            titanic_clean.loc[~age_missing, "Age"]
            .equals(titanic["Age"].dropna()),

        "Oryginalne dane pozostaly niezmienione":
            titanic.equals(titanic_original)
    }

    print("\nWERYFIKACJA")
    print("=" * 75)

    for description, result in checks.items():
        print(f"Czy {description}: {result}")

    passed = sum(bool(result) for result in checks.values())

    print(f"\nZaliczone testy: {passed}/{len(checks)}")

    assert all(checks.values()), "Blad weryfikacji pipeline"

    print("Wszystkie testy zakonczone pomyslnie.")


if __name__ == "__main__":
    main()
