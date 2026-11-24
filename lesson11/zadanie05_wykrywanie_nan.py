# Lekcja 11 - Zadanie 5: Wykrywanie NaN

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

# Prog brakujacych danych w procentach
prog = 10

# Liczba brakujacych wartosci w kazdej kolumnie
liczba_nan = df.isnull().sum()

# Procent brakujacych wartosci
procent_nan = liczba_nan / len(df) * 100

# Utworzenie raportu
raport = pd.DataFrame({
    "Liczba_NaN": liczba_nan,
    "Procent_NaN": procent_nan
})

# Sortowanie wedlug procentu brakujacych danych
raport = raport.sort_values(
    by="Procent_NaN",
    ascending=False
)

# Kolumny zawierajace brakujace dane
kolumny_z_brakami = raport[raport["Liczba_NaN"] > 0]

# Kolumny z ponad 10% brakujacych danych
kolumny_ponad_10 = raport[raport["Procent_NaN"] > prog]

# Statystyki calego datasetu
wszystkie_nan = liczba_nan.sum()
wszystkie_wartosci = df.size

procent_wszystkich_nan = (
    wszystkie_nan / wszystkie_wartosci * 100
)

print("WYKRYWANIE NaN - DATASET TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba wierszy: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Liczba wszystkich wartosci: {df.size}")

print("\nRAPORT BRAKUJACYCH WARTOSCI")
print("=" * 75)
print(raport.round(2).to_string())

print("\nKOLUMNY Z BRAKUJACYMI DANYMI")
print("=" * 75)
print(kolumny_z_brakami.round(2).to_string())

print("\nKOLUMNY Z PONAD 10% BRAKUJACYCH DANYCH")
print("=" * 75)
print(kolumny_ponad_10.round(2).to_string())

print("\nTEKSTOWY WYKRES BRAKUJACYCH DANYCH")
print("=" * 75)
print("Legenda: jeden znak █ = okolo 2% brakow")

for kolumna, procent in kolumny_z_brakami["Procent_NaN"].items():
    slupki = "█" * round(procent / 2)
    print(f"{kolumna:12} | {slupki} {procent:.2f}%")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba wszystkich NaN: {wszystkie_nan}")
print(f"Procent wszystkich NaN: {procent_wszystkich_nan:.2f}%")
print(f"Kolumny z brakami: {len(kolumny_z_brakami)}")
print(f"Kolumny bez brakow: {(liczba_nan == 0).sum()}")
print(f"Kolumny z ponad 10% brakow: {len(kolumny_ponad_10)}")

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy dataset ma 12 kolumn: {df.shape[1] == 12}")
print(f"Czy Age ma 177 brakow: {liczba_nan['Age'] == 177}")
print(f"Czy Cabin ma 687 brakow: {liczba_nan['Cabin'] == 687}")
print(f"Czy Embarked ma 2 braki: {liczba_nan['Embarked'] == 2}")
print(f"Czy lacznie jest 866 brakow: {wszystkie_nan == 866}")
print(f"Czy 3 kolumny maja braki: {len(kolumny_z_brakami) == 3}")
print(f"Czy 2 kolumny przekraczaja 10%: {len(kolumny_ponad_10) == 2}")
print(f"Czy wybrano poprawne kolumny: {set(kolumny_ponad_10.index) == {'Age', 'Cabin'}}")
print(f"Czy procenty sa poprawne: {np.allclose(procent_nan, df.isna().mean() * 100)}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
