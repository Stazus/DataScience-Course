# Lekcja 11 - Zadanie 8: Filtrowanie przez query()

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

# Warunki filtrowania
klasa = 1
minimalna_cena = 50

# Filtrowanie za pomoca query()
df_filtered = df.query(
    "Pclass == @klasa and Fare > @minimalna_cena"
).copy()

# Obliczenie podstawowych statystyk
liczba_pasazerow = len(df_filtered)
srednia_cena = df_filtered["Fare"].mean()
mediana_ceny = df_filtered["Fare"].median()
minimalna = df_filtered["Fare"].min()
maksymalna = df_filtered["Fare"].max()

# Wszyscy pasazerowie pierwszej klasy
df_first_class = df.query("Pclass == 1")

liczba_pierwsza_klasa = len(df_first_class)

procent = (
    liczba_pasazerow / liczba_pierwsza_klasa * 100
)

# Porownanie z Boolean indexing
df_boolean = df[
    (df["Pclass"] == klasa)
    & (df["Fare"] > minimalna_cena)
]

print("FILTROWANIE PRZEZ QUERY() - DATASET TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Pasazerowie pierwszej klasy: {liczba_pierwsza_klasa}")

print("\nWARUNKI FILTROWANIA")
print("=" * 75)
print(f"Klasa: {klasa}")
print(f"Cena biletu: > {minimalna_cena} GBP")
print("Operator logiczny: and")
print("Metoda: DataFrame.query()")

print("\nWYNIKI FILTROWANIA")
print("=" * 75)
print(f"Liczba pasazerow: {liczba_pasazerow}")
print(f"Shape: {df_filtered.shape}")
print(f"Procent pasazerow pierwszej klasy: {procent:.2f}%")

print("\nPIERWSZE 10 PASAZEROW")
print("=" * 75)

kolumny = ["PassengerId", "Name", "Pclass", "Fare"]

print(
    df_filtered[kolumny]
    .head(10)
    .to_string(index=False)
)

print("\nSTATYSTYKI CEN BILETOW")
print("=" * 75)
print(f"Srednia cena: {srednia_cena:.2f} GBP")
print(f"Mediana ceny: {mediana_ceny:.2f} GBP")
print(f"Minimalna cena: {minimalna:.2f} GBP")
print(f"Maksymalna cena: {maksymalna:.2f} GBP")
print(f"Odchylenie standardowe: {df_filtered['Fare'].std():.2f} GBP")

print("\nSZCZEGOLOWE STATYSTYKI")
print("=" * 75)
print(df_filtered["Fare"].describe().round(2).to_string())

print("\nPOROWNANIE METOD FILTROWANIA")
print("=" * 75)
print(f"query(): {len(df_filtered)} pasazerow")
print(f"Boolean indexing: {len(df_boolean)} pasazerow")
print(f"Zgodnosc wynikow: {df_filtered.equals(df_boolean)}")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Wszyscy pasazerowie: {len(df)}")
print(f"Pasazerowie pierwszej klasy: {liczba_pierwsza_klasa}")
print(f"Pasazerowie spelniajacy oba warunki: {liczba_pasazerow}")
print(f"Srednia cena ich biletow: {srednia_cena:.2f} GBP")

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy dataset ma 12 kolumn: {df.shape[1] == 12}")
print(f"Czy pierwsza klasa ma 216 pasazerow: {liczba_pierwsza_klasa == 216}")
print(f"Czy wynik nie jest pusty: {not df_filtered.empty}")
print(f"Czy wszyscy sa w pierwszej klasie: {(df_filtered['Pclass'] == 1).all()}")
print(f"Czy wszystkie ceny przekraczaja 50 GBP: {(df_filtered['Fare'] > 50).all()}")
print(f"Czy liczba pasazerow jest poprawna: {liczba_pasazerow == len(df_boolean)}")
print(f"Czy srednia cena jest poprawna: {np.isclose(srednia_cena, df_boolean['Fare'].mean())}")
print(f"Czy srednia cena przekracza 50 GBP: {srednia_cena > 50}")
print(f"Czy srednia cena jest skonczona: {np.isfinite(srednia_cena)}")
print(f"Czy obie metody daja identyczne wyniki: {df_filtered.equals(df_boolean)}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
