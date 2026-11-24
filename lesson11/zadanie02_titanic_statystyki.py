# Lekcja 11 - Zadanie 2: Wczytanie CSV i podstawowe statystyki

import pandas as pd
import numpy as np


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych CSV
df = pd.read_csv(url)

# Obliczenie sredniego wieku pasazerow
sredni_wiek = df["Age"].mean()

# Informacje o brakujacych wartosciach wieku
znany_wiek = df["Age"].count()
brakujacy_wiek = df["Age"].isna().sum()

print("ANALIZA DATASETU TITANIC")
print("=" * 75)

print("\nPIERWSZE 5 WIERSZY")
print("=" * 75)
print(df.head().to_string(index=False))

print("\nINFORMACJE O DATAFRAME")
print("=" * 75)
df.info()

print("\nPODSTAWOWE STATYSTYKI")
print("=" * 75)
print(df.describe().round(2).to_string())

print("\nWYMIARY DATASETU")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {df.shape[0]}")
print(f"Liczba kolumn: {df.shape[1]}")

print("\nANALIZA WIEKU PASAZEROW")
print("=" * 75)
print(f"Sredni wiek: {sredni_wiek:.2f} lat")
print(f"Mediana wieku: {df['Age'].median():.2f} lat")
print(f"Najmlodszy pasazer: {df['Age'].min():.2f} lat")
print(f"Najstarszy pasazer: {df['Age'].max():.2f} lat")
print(f"Odchylenie standardowe: {df['Age'].std():.2f}")

print("\nBRAKUJACE DANE DOTYCZACE WIEKU")
print("=" * 75)
print(f"Pasazerowie ze znanym wiekiem: {znany_wiek}")
print(f"Pasazerowie bez informacji o wieku: {brakujacy_wiek}")
print(f"Procent brakujacych danych: {brakujacy_wiek / len(df) * 100:.2f}%")

print("\nBRAKUJACE WARTOSCI WE WSZYSTKICH KOLUMNACH")
print("=" * 75)
print(df.isna().sum().to_string())

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy dataset zawiera 891 pasazerow: {len(df) == 891}")
print(f"Czy dataset zawiera 12 kolumn: {df.shape[1] == 12}")
print(f"Czy istnieje kolumna Age: {'Age' in df.columns}")
print(f"Czy wiek jest znany dla 714 pasazerow: {znany_wiek == 714}")
print(f"Czy brakuje 177 wartosci wieku: {brakujacy_wiek == 177}")
print(f"Czy sredni wiek jest poprawny: {np.isclose(sredni_wiek, 29.69911764705882)}")
print(f"Czy sredni wiek jest skonczony: {np.isfinite(sredni_wiek)}")
print(f"Czy liczba danych o wieku jest poprawna: {znany_wiek + brakujacy_wiek == len(df)}")
