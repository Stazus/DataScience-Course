# Lekcja 12 - Zadanie 1: Podstawowe grupowanie

import pandas as pd
import numpy as np


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia danych do pozniejszej weryfikacji
df_original = df.copy()

print("=" * 75)
print("PODSTAWOWE GRUPOWANIE - DATASET TITANIC")
print("=" * 75)

# Informacje o danych
print("\nDANE WEJSCIOWE")
print("=" * 75)

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Brakujace wartosci Age: {df['Age'].isna().sum()}")

# Podglad danych
print("\nPIERWSZE 10 REKORDOW")
print("=" * 75)

print(
    df[["PassengerId", "Pclass", "Sex", "Age"]]
    .head(10)
    .to_string(index=False)
)

# Grupowanie wedlug klasy i plci
mean_age = df.groupby(["Pclass", "Sex"])["Age"].mean()

# Utworzenie czytelnej tabeli
results = mean_age.reset_index()

results = results.rename(
    columns={"Age": "Sredni_wiek"}
)

print("\nSREDNI WIEK WEDLUG KLASY I PLCI")
print("=" * 75)

print(results.round(2).to_string(index=False))

# Dodatkowe statystyki grupowe
group_stats = (
    df.groupby(["Pclass", "Sex"])
    .agg(
        Liczba_pasazerow=("PassengerId", "size"),
        Znany_wiek=("Age", "count"),
        Sredni_wiek=("Age", "mean"),
        Mediana_wieku=("Age", "median"),
        Min_wiek=("Age", "min"),
        Max_wiek=("Age", "max")
    )
    .reset_index()
)

group_stats["Brakujacy_wiek"] = (
    group_stats["Liczba_pasazerow"]
    - group_stats["Znany_wiek"]
)

print("\nSZCZEGOLOWE STATYSTYKI GRUPOWE")
print("=" * 75)

print(group_stats.round(2).to_string(index=False))

# Tabela przestawna
age_pivot = mean_age.unstack()

print("\nTABELA PRZESTAWNA - PCLASS X SEX")
print("=" * 75)

print(age_pivot.round(2))

# Tekstowy wykres sredniego wieku
print("\nTEKSTOWY WYKRES SREDNIEGO WIEKU")
print("=" * 75)

print("Legenda: jeden znak █ = okolo 1 roku")

for (pclass, sex), age in mean_age.items():
    bar = "█" * int(round(age))

    print(
        f"Klasa {pclass}, {sex:6s} | "
        f"{bar:45s} {age:.2f}"
    )

# Sredni wiek wedlug samej klasy
age_by_class = df.groupby("Pclass")["Age"].mean()

print("\nSREDNI WIEK WEDLUG KLASY")
print("=" * 75)

print(age_by_class.round(2))

# Sredni wiek wedlug samej plci
age_by_sex = df.groupby("Sex")["Age"].mean()

print("\nSREDNI WIEK WEDLUG PLCI")
print("=" * 75)

print(age_by_sex.round(2))

# Najstarsza i najmlodsza grupa
oldest_group = mean_age.idxmax()
youngest_group = mean_age.idxmin()

print("\nPODSUMOWANIE")
print("=" * 75)

print(f"Liczba grup: {len(mean_age)}")
print(f"Sredni wiek wszystkich pasazerow: {df['Age'].mean():.2f}")

print(
    f"Najstarsza grupa: klasa {oldest_group[0]}, "
    f"{oldest_group[1]} - {mean_age.max():.2f} lat"
)

print(
    f"Najmlodsza grupa: klasa {youngest_group[0]}, "
    f"{youngest_group[1]} - {mean_age.min():.2f} lat"
)

print(
    f"Roznica sredniego wieku: "
    f"{mean_age.max() - mean_age.min():.2f} lat"
)

# Wnioski
print("\nWNIOSKI")
print("=" * 75)

print("1. GroupBy pozwala grupowac dane wedlug wielu kolumn.")
print("2. Mean oblicza srednia osobno dla kazdej grupy.")
print("3. Powstalo 6 grup: 3 klasy i 2 plcie.")
print("4. Mean automatycznie pomija brakujace wartosci NaN.")
print("5. Pasazerowie pierwszej klasy byli srednio starsi.")
print("6. Reset_index zamienia MultiIndex na zwykle kolumny.")
print("7. Unstack pozwala utworzyc czytelna tabele przestawna.")

# Niezalezna weryfikacja srednich
manual_verification = all(
    np.isclose(
        age,
        df.loc[
            (df["Pclass"] == pclass)
            & (df["Sex"] == sex),
            "Age"
        ].mean()
    )
    for (pclass, sex), age in mean_age.items()
)

# Weryfikacja wynikow
tests = {
    "Dataset ma 891 wierszy": len(df) == 891,
    "Dataset ma 12 kolumn": df.shape[1] == 12,
    "Istnieja 3 klasy": df["Pclass"].nunique() == 3,
    "Istnieja 2 plcie": df["Sex"].nunique() == 2,
    "Utworzono 6 grup": len(mean_age) == 6,
    "Wynik ma MultiIndex": isinstance(
        mean_age.index, pd.MultiIndex
    ),
    "Tabela wynikowa ma 6 wierszy": len(results) == 6,
    "Tabela wynikowa ma 3 kolumny": results.shape[1] == 3,
    "Tabela przestawna ma shape (3, 2)": (
        age_pivot.shape == (3, 2)
    ),
    "Srednie nie zawieraja NaN": mean_age.notna().all(),
    "Srednie sa dodatnie": (mean_age > 0).all(),
    "Srednie obliczono poprawnie": manual_verification,
    "Uwzgledniono wszystkich pasazerow": (
        group_stats["Liczba_pasazerow"].sum() == len(df)
    ),
    "Poprawnie policzono znane wartosci Age": (
        group_stats["Znany_wiek"].sum()
        == df["Age"].count()
    ),
    "Poprawnie policzono brakujacy wiek": (
        group_stats["Brakujacy_wiek"].sum()
        == df["Age"].isna().sum()
    ),
    "Oryginalne dane pozostaly niezmienione": (
        df.equals(df_original)
    )
}

print("\nWERYFIKACJA")
print("=" * 75)

for name, result in tests.items():
    print(f"Czy {name}: {result}")

passed = sum(tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("Wszystkie testy zakonczone pomyslnie.")
