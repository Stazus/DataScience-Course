# Lekcja 11 - Zadanie 4: Filtrowanie danych

import pandas as pd


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia oryginalnych danych
df_original = df.copy()

# Boolean indexing - tworzenie warunkow
maska_wiek = df["Age"] < 18
maska_przezycie = df["Survived"] == 1

# Polaczenie warunkow logicznych
maska = maska_wiek & maska_przezycie

# Filtrowanie danych
df_filtered = df[maska].copy()

# Wybor wymaganych kolumn
wynik = df_filtered[["Name", "Age"]].copy()

# Obliczenie statystyk
liczba_niepelnoletnich = maska_wiek.sum()
liczba_ocalalych = len(wynik)

procent_ocalalych = (
    liczba_ocalalych / liczba_niepelnoletnich * 100
)

print("FILTROWANIE DANYCH - DATASET TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Brakujace wartosci wieku: {df['Age'].isna().sum()}")

print("\nWARUNKI FILTROWANIA")
print("=" * 75)
print("Warunek 1: Age < 18")
print("Warunek 2: Survived == 1")
print("Operator logiczny: & (AND)")

print("\nWYNIKI FILTROWANIA")
print("=" * 75)
print(f"Liczba niepelnoletnich: {liczba_niepelnoletnich}")
print(f"Liczba ocalalych niepelnoletnich: {liczba_ocalalych}")
print(f"Procent ocalalych: {procent_ocalalych:.2f}%")

print("\nLISTA OCALALYCH NIEPELNOLETNICH PASAZEROW")
print("=" * 75)
print(wynik.to_string(index=False))

print("\nSTATYSTYKI WIEKU OCALALYCH")
print("=" * 75)
print(f"Sredni wiek: {wynik['Age'].mean():.2f} lat")
print(f"Mediana wieku: {wynik['Age'].median():.2f} lat")
print(f"Minimalny wiek: {wynik['Age'].min():.2f} lat")
print(f"Maksymalny wiek: {wynik['Age'].max():.2f} lat")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba pasazerow przed filtrowaniem: {len(df)}")
print(f"Liczba pasazerow po filtrowaniu: {len(wynik)}")
print(f"Shape wynikowego DataFrame: {wynik.shape}")

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy dataset ma 12 kolumn: {df.shape[1] == 12}")
print(f"Czy wszyscy maja mniej niz 18 lat: {(df_filtered['Age'] < 18).all()}")
print(f"Czy wszyscy przezyli: {(df_filtered['Survived'] == 1).all()}")
print(f"Czy liczba niepelnoletnich wynosi 113: {liczba_niepelnoletnich == 113}")
print(f"Czy liczba ocalalych wynosi 61: {liczba_ocalalych == 61}")
print(f"Czy wybrano poprawne kolumny: {list(wynik.columns) == ['Name', 'Age']}")
print(f"Czy brak pustych wartosci w wyniku: {not wynik.isna().any().any()}")
print(f"Czy liczba wynikow jest zgodna z maska: {len(wynik) == maska.sum()}")
print(f"Czy oryginalny DataFrame pozostal niezmieniony: {df.equals(df_original)}")
